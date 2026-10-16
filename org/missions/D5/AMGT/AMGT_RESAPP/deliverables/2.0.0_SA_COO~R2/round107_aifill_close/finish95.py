"""finish95.py -- recover the three names run95.py logged FAILED (a file-name defect, not a model failure).

BP/_LN_Equity and NG/_LN_Equity: run.py wrote <slash-safe key>.json (BP-SLASH-_LN_Equity.json) but run95.py looked for the
raw key, so the document exists and is only stamped here. WALMEX*_MM_Equity: run.py raised OSError at its own write because
'*' is not a legal Windows file-name character, so the document was lost after its model spend; it is re-run here with the
LOCAL file name only changed ('*' to -STAR-) by patching crosswalk.slash_safe_key in this process. No S3 address is built
or written (no --to-s3). The key is read from the environment the caller set; never printed, logged or stored.
"""
import datetime
import json
import os

from lib.research.aifill import contract, run, validation
from lib.research.identity import crosswalk

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "live95", "raw")
STAMPED = os.path.join(HERE, "live95", "stamped")
LEDGER = os.path.join(HERE, "live95", "spend_ledger.jsonl")
IN_USD_PER_MTOK = 15.0
OUT_USD_PER_MTOK = 75.0
SEARCH_USD = 0.01

_orig = crosswalk.slash_safe_key
crosswalk.slash_safe_key = lambda key: _orig(key).replace("*", "-STAR-")


def doc_cost(doc):
    total, searches = 0.0, 0
    for block in doc.get("blocks", {}).values():
        for call in (block.get("model_call"), (block.get("grounding") or {}).get("model_call")):
            if call:
                total += call.get("input_tokens", 0) * IN_USD_PER_MTOK / 1e6
                total += call.get("output_tokens", 0) * OUT_USD_PER_MTOK / 1e6
                searches += call.get("web_search_requests", 0) or 0
    return total + searches * SEARCH_USD, searches


def stamp(key, rerun_cost_note):
    name = crosswalk.slash_safe_key(key) + ".json"
    with open(os.path.join(RAW, name), "r", encoding="utf-8") as handle:
        doc = json.load(handle)
    cost, searches = doc_cost(doc)
    problems = contract.validate_document(doc)
    stamped = validation.stamp_validation(doc, datetime.datetime.now(datetime.timezone.utc), state="HELD")
    with open(os.path.join(STAMPED, name), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(stamped, handle, indent=1, sort_keys=True)
        handle.write("\n")
    rec = {"key": key, "status": "OK", "recovered": rerun_cost_note, "file": name, "cost_usd": round(cost, 4),
           "web_searches": searches, "doc_problems": len(problems or []),
           "verdicts": {b: blk["validation"]["verdict"] for b, blk in stamped["blocks"].items()},
           "classes": {b: blk.get("source_class") for b, blk in doc["blocks"].items()},
           "sentence_verdicts": [s.get("verdict") for blk in doc["blocks"].values()
                                 for s in (blk.get("grounding") or {}).get("sentences", [])]}
    with open(LEDGER, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(rec, sort_keys=True) + "\n")
    print(key, name, "cost_this_document=%.4f" % cost, rerun_cost_note, flush=True)


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("BLOCKED: ANTHROPIC_API_KEY is not set")
    for key in ("BP/_LN_Equity", "NG/_LN_Equity"):
        stamp(key, "stamped from the existing raw file (spend already in the 119.40 total)")
    key = "WALMEX*_MM_Equity"
    code = run.main(["--key", key, "--out", RAW])
    if code not in (0, None):
        raise SystemExit("run failed rc=%r" % (code,))
    stamp(key, "re-run: this document's cost is NEW spend, on top of the first lost WALMEX run already in 119.40")


if __name__ == "__main__":
    main()
