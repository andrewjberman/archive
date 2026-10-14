"""store_batch.py -- the issuer's step 2 of the AI-fill never-widen pair: run the producer for a list of names, store each document, stop at the spend cap.

  AIFILL_SERVED_FUNCTION=<fn> ANTHROPIC_API_KEY=<key> PYTHONPATH=<repo root> python store_batch.py --names A,B --out DIR [--confirm-write] [--workers 4] [--cap-usd 75] [--no-model]
  ... --census-file census_sections.json  takes every resolved name of the V1 census (95).

One `python -m lib.research.aifill.run --key K --out DIR --to-s3 [--confirm-write]` per name (a subprocess, so the producer is exactly the merged command). After EACH name finishes it reads that name's
document from DIR, sums the model calls' token cost at the module's rates (claude-opus-5: 5 USD per million input tokens, 25 per million output), and PROJECTS the total (spent / done * total, times 1.15 for the discarded Opal-path
calls the document does not record). A projection over --cap-usd STOPS the batch (no new name is started; names in flight finish) and reports. Without --confirm-write nothing is written to S3 (the command's own DRY-RUN).
Prints one line per name and a final `AIFILL STORE BATCH: ...` line; writes DIR/batch_census.json (per name: status, source class per block, tokens, usd).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import threading

USD_PER_INPUT_TOKEN = 5e-6
USD_PER_OUTPUT_TOKEN = 25e-6
MARGIN = 1.15
BLOCKS = ("mgmt_bio", "mgmt_recent", "mgmt_team_view", "thesis_pillars", "identity_description")


def slash_safe(key):
    from lib.research.identity import crosswalk

    return crosswalk.slash_safe_key(key)


def doc_cost(doc):
    inp = out = 0
    for block in (doc.get("blocks") or {}).values():
        call = block.get("model_call") or {}
        inp += int(call.get("input_tokens") or 0)
        out += int(call.get("output_tokens") or 0)
    return inp, out, inp * USD_PER_INPUT_TOKEN + out * USD_PER_OUTPUT_TOKEN


def run_one(key, out_dir, confirm, no_model):
    cmd = [sys.executable, "-m", "lib.research.aifill.run", "--key", key, "--out", out_dir, "--to-s3"]
    if confirm:
        cmd.append("--confirm-write")
    if no_model:
        cmd.append("--no-model")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1500)
    path = os.path.join(out_dir, "%s.json" % slash_safe(key))
    doc = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
    return proc, doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", default="")
    ap.add_argument("--census-file", default="")
    ap.add_argument("--exclude", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cap-usd", type=float, default=75.0)
    ap.add_argument("--confirm-write", action="store_true")
    ap.add_argument("--no-model", action="store_true")
    args = ap.parse_args()
    names = [n for n in args.names.split(",") if n]
    if args.census_file:
        with open(args.census_file, "r", encoding="utf-8") as handle:
            names += sorted(json.load(handle)["result"])
    skip = set(n for n in args.exclude.split(",") if n)
    names = [n for n in dict.fromkeys(names) if n not in skip]
    if not names:
        print("BLOCKED: no names")
        return 2
    os.makedirs(args.out, exist_ok=True)
    lock = threading.Lock()
    state = {"done": 0, "spent": 0.0, "stopped": False, "stop_note": ""}
    rows = {}

    def work(key):
        with lock:
            if state["stopped"]:
                return key, None
        proc, doc = run_one(key, args.out, args.confirm_write, args.no_model)
        summary = [ln for ln in proc.stdout.splitlines() if ln.startswith("AIFILL RUN:")]
        row = {"rc": proc.returncode, "summary": summary[0] if summary else (proc.stdout + proc.stderr)[-200:]}
        if doc is not None:
            inp, out, usd = doc_cost(doc)
            row.update({"classes": {b: doc["blocks"][b]["source_class"] for b in BLOCKS}, "input_tokens": inp, "output_tokens": out, "usd": round(usd, 4)})
        with lock:
            state["done"] += 1
            state["spent"] += row.get("usd", 0.0)
            projected = state["spent"] / state["done"] * len(names) * MARGIN
            row["wrote"] = bool(args.confirm_write and proc.returncode == 0 and any(ln.startswith("WROTE: s3://") for ln in proc.stdout.splitlines()))
            if projected > args.cap_usd and not state["stopped"]:
                state["stopped"] = True
                state["stop_note"] = "projected %.2f USD over the %.2f cap after %d of %d names (spent %.2f)" % (projected, args.cap_usd, state["done"], len(names), state["spent"])
            print("%-22s rc=%d %s usd=%s%s" % (key, proc.returncode, row["summary"][:110], row.get("usd"), "  [WROTE]" if row["wrote"] else ""), flush=True)
        return key, row

    with concurrent.futures.ThreadPoolExecutor(args.workers) as ex:
        for key, row in ex.map(work, names):
            if row is not None:
                rows[key] = row
    census = {"names": len(names), "ran": len(rows), "spent_usd": round(state["spent"], 2), "stopped": state["stopped"], "stop_note": state["stop_note"], "rows": rows}
    with open(os.path.join(args.out, "batch_census.json"), "w", encoding="utf-8") as handle:
        json.dump(census, handle, indent=1, sort_keys=True)
    bad = [k for k, r in rows.items() if r["rc"] != 0]
    wrote = sum(1 for r in rows.values() if r.get("wrote"))
    tally = {}
    for r in rows.values():
        for cls in (r.get("classes") or {}).values():
            tally[cls] = tally.get(cls, 0) + 1
    print("AIFILL STORE BATCH: ran %d of %d, wrote %d, failed %d, spent %.2f USD of %.2f cap, cells %s%s" % (
        len(rows), len(names), wrote, len(bad), state["spent"], args.cap_usd, json.dumps(tally, sort_keys=True), ("  STOPPED: " + state["stop_note"]) if state["stopped"] else ""))
    return 0 if not bad and not state["stopped"] else 1


if __name__ == "__main__":
    sys.exit(main())
