"""fix_set.py -- the round-111 pass over the stored round-110 documents (AMGT_RESAPP AIFILL): the re-check and the retry of failed blocks.

  python fix_set.py            no model call: for each of the 95 round-110 stamped documents fetch the name's served inputs (a GET) and run
                               orchestrate.refinish_document (the opening-sentence subject rule and the OPAL restatement rule)
  python fix_set.py --retry    ALSO rebuild the blocks that failed ("This block could not be produced") through
                               orchestrate.retry_failed_blocks, every model call metered (needs ANTHROPIC_API_KEY set in the same shell call)

Per name the result is the round-110 document, a retry of its failed blocks when asked, and the re-check, stamped HELD again ONLY when it changed.
Unchanged documents are copied byte for byte. Output under round111_close/live95: stamped/ (all 95 final files), raw/ (the changed documents before
stamping), changed.json (what changed, per name), spend_ledger.jsonl and usage.jsonl (every model call: tokens and web searches). Spend is
counted at the repo rate card (lib/research/filings/analyze.py: 5 and 25 USD per Mtok, 0.01 per search) and the retry stops at CEILING_USD.
Local files only: no S3 write. The key is read from the environment, never printed or stored.
"""
import datetime
import json
import os
import shutil
import sys

from lib.research.aifill import contract, model, orchestrate, sources, store, validation
from lib.research.api import scoped_amgt
from lib.research.aifill import inputs as served

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "round110_close", "live95", "stamped")
OUT = os.path.join(HERE, "live95")
CEILING_USD = 30.0
IN_USD_PER_MTOK = 5.0
OUT_USD_PER_MTOK = 25.0
SEARCH_USD = 0.01
FUNCTION_ENV = "AIFILL_SERVED_FUNCTION"

usage = []


def metered(*args, **kwargs):
    result = model.call_model(*args, **kwargs)
    row = {"in": result.input_tokens, "out": result.output_tokens, "ws": result.web_search_requests}
    usage.append(row)
    with open(os.path.join(OUT, "usage.jsonl"), "a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row) + "\n")
    return result


def spent():
    return sum(r["in"] * IN_USD_PER_MTOK / 1e6 + r["out"] * OUT_USD_PER_MTOK / 1e6 + r["ws"] * SEARCH_USD for r in usage)


def has_failed_block(doc):
    return any(str(blk.get("reason") or "").startswith(orchestrate.FAILED_PREFIX) for blk in doc["blocks"].values())


def main():
    retry = "--retry" in sys.argv
    function_name = os.environ.get(FUNCTION_ENV)
    if not function_name:
        raise SystemExit("BLOCKED: set %s" % FUNCTION_ENV)
    if retry and not os.environ.get(model.KEY_ENV):
        raise SystemExit("BLOCKED: --retry needs %s set in this shell call" % model.KEY_ENV)
    for sub in ("raw", "stamped"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    changed = {}
    for name in sorted(os.listdir(SRC)):
        src_path = os.path.join(SRC, name)
        with open(src_path, "rb") as handle:
            raw = handle.read()
        doc = json.loads(raw.decode("utf-8"))
        key = doc["security_key"]
        inputs = served.served_inputs(key, function_name=function_name)
        new = doc
        notes = []
        if retry and has_failed_block(new):
            if spent() >= CEILING_USD:
                notes.append("RETRY SKIPPED: ceiling %.0f USD reached" % CEILING_USD)
            else:
                before = [b for b, blk in new["blocks"].items() if str(blk.get("reason") or "").startswith(orchestrate.FAILED_PREFIX)]
                new = orchestrate.retry_failed_blocks(new, key, inputs, metered, now=now, fetch=sources.fetch_source)
                notes.append("retried %s" % ",".join(before))
        refinished = orchestrate.refinish_document(new, inputs)
        if refinished["blocks"]["mgmt_bio"] != new["blocks"]["mgmt_bio"]:
            notes.append("mgmt_bio withheld: %s" % refinished["blocks"]["mgmt_bio"]["reason"][:60])
        new = refinished
        local = os.path.join(OUT, "stamped", name)
        if new == doc:
            shutil.copyfile(src_path, local)
            continue
        with open(os.path.join(OUT, "raw", name), "wb") as handle:
            handle.write(store.document_bytes(new) + b"\n")
        problems = contract.validate_document(new, require_grounding=True)
        ok, why = scoped_amgt._validate_ai_fill_document(new, key)
        stamped = validation.stamp_validation(new, now, state="HELD")
        with open(local, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(stamped, handle, indent=1, sort_keys=True)
            handle.write("\n")
        changed[key] = {"file": name, "notes": notes, "contract_problems": len(problems or []), "serve_rules_ok": ok}
        print("CHANGED %s: %s" % (key, "; ".join(notes)), flush=True)
    with open(os.path.join(OUT, "changed.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(changed, handle, indent=1, sort_keys=True)
        handle.write("\n")
    with open(os.path.join(OUT, "spend_ledger.jsonl"), "a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps({"mode": "retry" if retry else "refinish", "model_calls": len(usage), "web_searches": sum(r["ws"] for r in usage),
                                 "true_cost_usd": round(spent(), 4), "changed": len(changed)}, sort_keys=True) + "\n")
    print("DONE: changed %d of %d; model calls %d; metered spend %.2f USD (ceiling %.0f)" % (len(changed), len(os.listdir(SRC)), len(usage), spent(), CEILING_USD))


if __name__ == "__main__":
    main()
