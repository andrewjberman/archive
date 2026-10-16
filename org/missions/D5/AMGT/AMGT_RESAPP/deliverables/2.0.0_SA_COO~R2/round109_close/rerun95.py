"""rerun95.py -- the 95-name AI fill RE-RUN after AMGT-gu-1 (AMGT_RESAPP AIFILL, round 109), local files only, under the 150 USD ceiling (CTO msg 6580).

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
from lib.research.identity import crosswalk

HERE = os.path.dirname(os.path.abspath(__file__))  # round109_close
CENSUS = os.path.join(HERE, "..", "..", "2.0.0_SA_COO~R1", "round106", "census_v5.json")
RAW = os.path.join(HERE, "live95", "raw")
STAMPED = os.path.join(HERE, "live95", "stamped")
LEDGER = os.path.join(HERE, "live95", "spend_ledger.jsonl")
USAGE = os.path.join(HERE, "live95", "usage")
LOCAL_NAME = lambda key: crosswalk.slash_safe_key(key).replace("*", "-STAR-")  # noqa: E731 -- a '*' is not a legal Windows file-name character
CEILING_USD = 150.0
PER_NAME_MAX_USD = 2.5   # reserve per in-flight name; the one-name test cost 0.96 USD
IN_USD_PER_MTOK = 5.0    # the repo rate card: lib/research/filings/analyze.py USD_PER_INPUT_TOKEN (Opus 5 list price)
OUT_USD_PER_MTOK = 25.0  # the repo rate card: analyze.py USD_PER_OUTPUT_TOKEN
SEARCH_USD = 0.01        # per web-search request (decomposition section 2: 21,743 tokens and 2 searches read about 13 cents)
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


WRAPPER = """import sys, os, json
from lib.research.identity import crosswalk as c
o = c.slash_safe_key
c.slash_safe_key = lambda k: o(k).replace('*', '-STAR-')
from lib.research.aifill import model as m, run
orig = m.call_model


def wrapped(*a, **k):
    r = orig(*a, **k)
    with open(os.environ['AIFILL_USAGE_LOG'], 'a') as h:
        h.write(json.dumps({'in': r.input_tokens, 'out': r.output_tokens, 'ws': r.web_search_requests}) + chr(10))
    return r


m.call_model = wrapped
sys.exit(run.main(sys.argv[1:]))
"""


def usage_cost(path):
    """The spend of EVERY model call the run made (kept or withheld block alike), from the wrapped seam's own log."""
    total, calls, searches = 0.0, 0, 0
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:  # log-open-ok: single-writer ASCII log written by the wrapped seam
            for line in handle:
                row = json.loads(line)
                calls += 1
                searches += row["ws"]
                total += row["in"] * IN_USD_PER_MTOK / 1e6 + row["out"] * OUT_USD_PER_MTOK / 1e6 + row["ws"] * SEARCH_USD
    return total, calls, searches


def one(key):
    with lock:
        if state["stop"] or state["spent"] + PER_NAME_MAX_USD > CEILING_USD:
            state["stop"] = True
            return {"key": key, "status": "NOT_RUN_CEILING"}
        state["spent"] += PER_NAME_MAX_USD  # reserve
    code = WRAPPER
    ulog = os.path.join(USAGE, LOCAL_NAME(key) + ".jsonl")
    proc = subprocess.run([sys.executable, "-c", code, "--key", key, "--out", RAW], capture_output=True, text=True,
                          env=dict(os.environ, AIFILL_USAGE_LOG=ulog))
    path = os.path.join(RAW, LOCAL_NAME(key) + ".json")
    rec = {"key": key, "rc": proc.returncode}
    cost = 0.0
    if proc.returncode == 0 and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
        recorded, _ = doc_cost(doc)
        cost, calls, searches = usage_cost(ulog)
        rec["recorded_cost_usd"] = round(recorded, 4)
        rec["model_calls"] = calls
        problems = contract.validate_document(doc)
        now = datetime.datetime.now(datetime.timezone.utc)
        stamped = validation.stamp_validation(doc, now, state="HELD")
        rec["recency_dropped"] = sum(1 for blk in doc["blocks"].values()
                                     for s in (blk.get("grounding") or {}).get("sentences", [])
                                     if s.get("verdict") == "CONTRADICTED" and isinstance(s.get("source"), int)
                                     and s["source"] >= len([c for c in blk["citations"] if c.get("source_kind") == "web"]))
        with open(os.path.join(STAMPED, LOCAL_NAME(key) + ".json"), "w", encoding="utf-8", newline="\n") as handle:
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
    os.makedirs(USAGE, exist_ok=True)
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
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        todo = [n for n in sys.argv[2].split(",") if n in names and n not in done]
    print("names=%d already_ok=%d to_run=%d spent_so_far=%.4f" % (len(names), len(done), len(todo), state["spent"]), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for rec in pool.map(one, todo):
            print(rec["key"], rec["status"], rec.get("cost_usd"), rec.get("running_total_usd"), flush=True)
    print("DONE spent_usd=%.4f ceiling=%.1f stopped_on_ceiling=%s" % (state["spent"], CEILING_USD, state["stop"]), flush=True)


if __name__ == "__main__":
    main()
