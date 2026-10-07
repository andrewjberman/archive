"""IRPT_BCKEND round 69 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of cell IB-pr-350 (the back-fill of covered_account_ids into
export receipts written before IB-pr-343, PRD v0.30 item 35; laptop applier 0.7.0_AE_CloudOps~I, after IB-pr-349).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads one file; finishes in seconds.

  IB69-1-AC1  the committed IB69-1_backfill_after_reads.json reads: mode apply; denied 0; filled == would_write == wrote (each >= 0)
              and filled + unfillable + already_named == receipts_listed; every written receipt re-read names a non-empty
              covered_account_ids (rewritten_reread_ok == wrote); one back-filled export read by an in-scope Opal principal is
              admitted (backfilled_read_admitted true, with an admitted-read log line) when wrote >= 1; halves_present true.
              Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

F = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~I/IB69-1_backfill_after_reads.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB69"))
        sys.exit(1)

    if cid != "IB69-1-AC1":
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    ints = ("receipts_listed", "filled", "unfillable", "already_named", "would_write", "wrote", "denied", "rewritten_reread_ok")
    for k in ints:
        if not isinstance(d.get(k), int) or d[k] < 0:
            fail("%s is %r" % (k, d.get(k)))
    if d.get("mode") != "apply" or d.get("halves_present") is not True:
        fail("mode %r halves_present %r" % (d.get("mode"), d.get("halves_present")))
    if d["denied"] != 0:
        fail("denied %d: the applier identity could not read every receipt" % d["denied"])
    if d["filled"] + d["unfillable"] + d["already_named"] != d["receipts_listed"]:
        fail("filled+unfillable+already_named != receipts_listed")
    if not (d["would_write"] == d["wrote"] == d["rewritten_reread_ok"]):
        fail("would_write %d, wrote %d, re-read ok %d differ" % (d["would_write"], d["wrote"], d["rewritten_reread_ok"]))
    if d["wrote"] >= 1 and (d.get("backfilled_read_admitted") is not True or not d.get("admitted_read_log_lines")):
        fail("no admitted read of a back-filled export")
    print("OK: %d listed, %d written and re-read, %d unfillable, 0 denied" % (d["receipts_listed"], d["wrote"], d["unfillable"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
