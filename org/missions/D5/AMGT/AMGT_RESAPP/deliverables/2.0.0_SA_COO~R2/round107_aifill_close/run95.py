"""run95.py -- the 95-name AI fill re-run, local files only, under a spend ceiling (AMGT_RESAPP AIFILL, round 108 step 3).

Reads the key from the environment the caller set in the same shell call; never prints, logs or writes it.
Per name: one `python -m lib.research.aifill.run --key K --out raw/` subprocess, then validate_document on the raw
file and a HELD stamp (lib.research.aifill.validation.stamp_validation) written to stamped/. Spend is estimated from the
token counts and web-search counts the documents record, at the CONSERVATIVE rates below (assumed, not measured), and the
run stops before a name that could push the running total past the ceiling.
"""
import concurrent.futures
import datetime
import json
import os
import subprocess
import sys
import threading

from lib.research.aifill import contract, validation

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "..", "..", "2.0.0_SA_COO~R1", "round106", "census_v5.json")
RAW = os.path.join(HERE, "live95", "raw")
STAMPED = os.path.join(HERE, "live95", "stamped")
LEDGER = os.path.join(HERE, "live95", "spend_ledger.jsonl")
CEILING_USD = 150.0
PER_NAME_MAX_USD = 1.0
IN_USD_PER_MTOK = 15.0   # assumed upper rate
OUT_USD_PER_MTOK = 75.0  # assumed upper rate
SEARCH_USD = 0.01        # per web-search request, assumed
WORKERS = 4

lock = threading.Lock()
state = {"spent": 0.0, "stop": False}


def doc_cost(doc):
    total = 0.0
    searches = 0
    for block in doc.get("blocks", {}).values():
        calls = [block.get("model_call"), (block.get("grounding") or {}).get("model_call")]
        for call in calls:
            if not call:
                continue
            total += call.get("input_tokens", 0) * IN_USD_PER_MTOK / 1e6
            total += call.get("output_tokens", 0) * OUT_USD_PER_MTOK / 1e6
            searches += call.get("web_search_requests", 0) or 0
    return total + searches * SEARCH_USD, searches


def one(key):
    with lock:
        if state["stop"] or state["spent"] + PER_NAME_MAX_USD > CEILING_USD:
            state["stop"] = True
            return {"key": key, "status": "NOT_RUN_CEILING"}
        state["spent"] += PER_NAME_MAX_USD  # reserve
    proc = subprocess.run(
        [sys.executable, "-m", "lib.research.aifill.run", "--key", key, "--out", RAW],
        capture_output=True, text=True,
    )
    path = os.path.join(RAW, key + ".json")
    rec = {"key": key, "rc": proc.returncode}
    cost = 0.0
    if proc.returncode == 0 and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
        cost, searches = doc_cost(doc)
        problems = contract.validate_document(doc)
        now = datetime.datetime.now(datetime.timezone.utc)
        stamped = validation.stamp_validation(doc, now, state="HELD")
        with open(os.path.join(STAMPED, key + ".json"), "w", encoding="utf-8", newline="\n") as handle:
            json.dump(stamped, handle, indent=1, sort_keys=True)
            handle.write("\n")
        verdicts = {b: blk["validation"]["verdict"] for b, blk in stamped["blocks"].items()}
        classes = {b: blk.get("source_class") for b, blk in doc["blocks"].items()}
        rec.update(status="OK", cost_usd=round(cost, 4), web_searches=searches, doc_problems=len(problems or []),
                   verdicts=verdicts, classes=classes)
        verdict_sentences = [s.get("verdict") for blk in doc["blocks"].values()
                             for s in (blk.get("grounding") or {}).get("sentences", [])]
        rec["sentence_verdicts"] = verdict_sentences
    else:
        rec.update(status="FAILED", stdout_tail=proc.stdout[-300:], stderr_tail=proc.stderr[-300:])
    with lock:
        state["spent"] += cost - PER_NAME_MAX_USD
        rec["running_total_usd"] = round(state["spent"], 4)
        with open(LEDGER, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("BLOCKED: ANTHROPIC_API_KEY is not set")
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(STAMPED, exist_ok=True)
    with open(CENSUS, "r", encoding="utf-8") as handle:
        names = json.load(handle)["names"]
    done = set()
    if os.path.exists(LEDGER):
        with open(LEDGER, "r", encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                if row.get("status") == "OK":
                    done.add(row["key"])
                    state["spent"] += row.get("cost_usd", 0.0)
    todo = [n for n in names if n not in done]
    print("names=%d already_ok=%d to_run=%d spent_so_far=%.4f" % (len(names), len(done), len(todo), state["spent"]), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for rec in pool.map(one, todo):
            print(rec["key"], rec["status"], rec.get("cost_usd"), rec.get("running_total_usd"), flush=True)
    print("DONE spent_usd=%.4f ceiling=%.1f stopped_on_ceiling=%s" % (state["spent"], CEILING_USD, state["stop"]), flush=True)


if __name__ == "__main__":
    main()
