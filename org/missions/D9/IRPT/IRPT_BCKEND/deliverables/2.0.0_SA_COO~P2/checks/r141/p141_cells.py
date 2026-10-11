"""IRPT_BCKEND round 141 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB141-1  IB-pr-444  the fifth run's capture receipt: which of its leaves would confirm or kill "the sign-in was accepted and a
                      web firewall's challenge is what the probe meets", and why the new after-submit reason did not fire
                      (CTO msg 5524). A code and record read: no request, no sign-in, no AWS call.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB141-1-AC1  the leaves that decide are named: each with its path in the persisted receipt, the closed values the code can
               write there (with the code line), which values CONFIRM the hypothesis and which KILL it, and whether the
               whitelist persists it at all.
  IB141-1-AC2  why the after-submit reason did not fire is stated from the code (lines cited) with its claim, and what the
               202 / NOT_LIVE probe means in the code's own terms.
  IB141-1-AC3  the verdict on the hypothesis from what is ALREADY read is one of three words with its claim; the reads asked of
               the host reader are listed (leaf paths only); nothing was requested of the vendor, the host or AWS.
Whether the hypothesis holds is UNMEASURED by the issuer; "undecided" passes as well as the other two.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~302/"
OUT = D + "IB141-1_receipt_diagnosis.json"
READ = D + "IB141-1_RECEIPT_DIAGNOSIS_READ.md"
CLAIMS = ("measured", "inferred", "held", "absent")
VERDICTS = ("SUPPORTED", "CONTRADICTED", "UNDECIDED")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB141"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB141-1-AC1":
        leaves = a.get("deciding_leaves")
        if not isinstance(leaves, list) or not leaves:
            fail("deciding_leaves is empty")
        for x in leaves:
            if not x.get("receipt_path") or not isinstance(x.get("closed_values"), list) or not x["closed_values"] \
                    or ":" not in str(x.get("written_at") or "") or x.get("persisted_by_the_whitelist") not in (True, False):
                fail("leaf %r needs receipt_path, closed_values, written_at (file:line) and persisted_by_the_whitelist" % x.get("receipt_path"))
            if not isinstance(x.get("confirms_if"), list) or not isinstance(x.get("kills_if"), list) or not (x["confirms_if"] or x["kills_if"]):
                fail("leaf %s decides nothing: confirms_if and kills_if are both empty" % x["receipt_path"])
            if not set(x["confirms_if"]) <= set(x["closed_values"]) or not set(x["kills_if"]) <= set(x["closed_values"]) \
                    or set(x["confirms_if"]) & set(x["kills_if"]):
                fail("leaf %s: its confirming and killing values must be among its closed values and must not overlap" % x["receipt_path"])
        print("OK: %d deciding leaf/leaves named, %d persisted by the whitelist" % (len(leaves), sum(1 for x in leaves if x["persisted_by_the_whitelist"])))
    elif cid == "IB141-1-AC2":
        w = a.get("why_the_after_submit_reason_did_not_fire") or {}
        lines = w.get("code_lines")
        if w.get("claim") not in CLAIMS or not w.get("in_words") or not isinstance(lines, list) or not lines or any(":" not in str(x) for x in lines):
            fail("why_the_after_submit_reason_did_not_fire needs in_words, a claim and code_lines as file:line entries")
        p = a.get("what_the_probe_result_means") or {}
        if not p.get("status_202_in_the_code") or not p.get("not_live_in_the_code") or ":" not in str(p.get("classified_at") or ""):
            fail("what_the_probe_result_means needs status_202_in_the_code, not_live_in_the_code and classified_at (file:line)")
        print("OK: the branch's condition is cited at %d code line(s) (%s)" % (len(lines), w["claim"]))
    elif cid == "IB141-1-AC3":
        v = a.get("hypothesis") or {}
        if v.get("verdict_from_what_is_already_read") not in VERDICTS or v.get("claim") not in CLAIMS or not v.get("stated") or not v.get("reason"):
            fail("hypothesis needs stated, verdict_from_what_is_already_read in %s, a claim and a reason" % (VERDICTS,))
        if v["verdict_from_what_is_already_read"] != "UNDECIDED" and v["claim"] == "absent":
            fail("a decided verdict cannot carry the claim absent")
        asks = a.get("reads_asked_of_the_host_reader")
        if not isinstance(asks, list) or any(not x.get("receipt_path") or not x.get("what_it_decides") for x in asks):
            fail("reads_asked_of_the_host_reader must list receipt paths with what each decides")
        if not isinstance(a.get("other_explanations_not_excluded"), list):
            fail("other_explanations_not_excluded is not stated")
        for k in ("vendor_requests_made", "sign_ins_made", "host_commands_run", "aws_calls_made"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not (root / READ).is_file():
            fail("no %s" % READ)
        print("OK: hypothesis %s (%s); %d read(s) asked of the host reader; nothing requested anywhere" % (
            v["verdict_from_what_is_already_read"], v["claim"], len(asks)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
