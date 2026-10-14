"""IRPT_BCKEND round 191 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB191-1  IB-pr-532  the never-widen packet for ONE release of the holdings producer carrying the cash rule on both layers and the repaired directory exemption: the movers per firm and per change, read by running the producer's own rules on each firm's newest candidate (READ ONLY)
    AC1  the counts: per firm the candidate built (date, nodes) or the stated reason; the cash rule's movers split canonical / fallback summing to the total with public tickers only; the gate's outcome and conditions before and after the repaired exemption, where the repair can only remove account_lost
    AC2  the packet: Branch A (mint-bundle), Branch B (rollback by bundle and manifest version), blast radius, the 49financial 2026-10-08 gap named as a key the release must not widen or hide, the releasing seat's own NEVER-2 ledger and its legs, both halves unsigned, the stop rule if the counts differ
    AC3  the record's honesty: both branches stated, a note per firm, no client identifier, no long digit run, the six bound counters 0
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC = D + "0.9.0_WK_IRPT_BCKEND~379/IB191-1_release_counts.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~379/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532.md"
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
FIRMS = ["49financial", "cottonwood", "inflection"]
CONDS = {"reconcile_difference", "multi_asset", "class_outside_six", "classified_security_lost", "account_lost", "source_frontier_older"}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB191"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def counts():
    r = load(REC)
    firms = r.get("firms") or {}
    if sorted(firms) != FIRMS:
        fail("firms must hold exactly 49financial, cottonwood and inflection")
    for k, v in firms.items():
        c = v.get("candidate") or {}
        if not isinstance(c.get("built"), bool):
            fail("%s: candidate.built must be true or false" % k)
        if not c["built"]:
            if not str(c.get("reason", "")).strip():
                fail("%s: a candidate not built needs its stated reason" % k)
            for key in ("cash_rule", "exemption"):
                if v.get(key) is not None:
                    fail("%s: no candidate was built, so %s must be null" % (k, key))
            continue
        if not (is_date(c.get("business_date")) and is_int(c.get("nodes")) and c["nodes"] > 0):
            fail("%s: a built candidate needs a business_date and a node count above 0" % k)
        cr = v.get("cash_rule") or {}
        a, b, t = cr.get("movers_canonical"), cr.get("movers_fallback"), cr.get("movers_total")
        if not all(is_int(x) and x >= 0 for x in (a, b, t)) or a + b != t or t > c["nodes"]:
            fail("%s: movers_canonical + movers_fallback must equal movers_total (integers >= 0, not above the node count)" % k)
        tk = cr.get("canonical_tickers")
        if not isinstance(tk, list) or len(tk) != len(set(tk)) or any(not re.fullmatch(r"[A-Z0-9.\-]{1,12}", str(x)) for x in tk) or (a == 0) != (len(tk) == 0) or len(tk) > a:
            fail("%s: canonical_tickers must be distinct public symbols, empty exactly when no canonical mover, no more than the movers" % k)
        vs = cr.get("vs_round189") or {}
        if not (is_int(vs.get("canonical")) and is_int(vs.get("fallback"))):
            fail("%s: vs_round189 needs integer deltas for canonical and fallback" % k)
        ex = v.get("exemption") or {}
        for key in ("gate_before", "gate_after"):
            if ex.get(key) not in ("PUBLISHED", "REFUSED"):
                fail("%s: exemption.%s must be PUBLISHED or REFUSED" % (k, key))
        cb, ca = ex.get("conditions_before"), ex.get("conditions_after")
        if not (isinstance(cb, list) and isinstance(ca, list) and set(cb) <= CONDS and set(ca) <= CONDS):
            fail("%s: conditions must be lists of the six gate conditions" % k)
        if (ex["gate_before"] == "PUBLISHED") != (cb == []) or (ex["gate_after"] == "PUBLISHED") != (ca == []):
            fail("%s: a gate outcome is PUBLISHED exactly when its conditions list is empty" % k)
        if not set(ca) <= set(cb):
            fail("%s: the repaired exemption can only remove account_lost, so conditions_after must be a subset of conditions_before" % k)
        if set(cb) - set(ca) - {"account_lost"}:
            fail("%s: the only condition the repair may remove is account_lost" % k)
        if not (is_int(ex.get("lost_accounts_listed_after")) and ex["lost_accounts_listed_after"] >= 0):
            fail("%s: lost_accounts_listed_after must be an integer >= 0" % k)
    print("OK: counts consistent for 3 firms")


def packet():
    f = ROOT / PACKET
    if not f.is_file():
        fail("no %s" % PACKET)
    txt = f.read_text(encoding="utf-8")
    if len(txt) < 4000:
        fail("the packet must be at least 4,000 characters")
    low = txt.lower()
    for w in ("branch a", "branch b", "blast radius", "rollback", "version", "mint-bundle", "coo half", "cto half", "unsigned", "never-2", "ledger",
              "first scheduled fire", "after-read", "2026-10-08", "must not widen", "the release stops", "listed", "cash"):
        if w not in low:
            fail("the packet must state %r" % w)
    print("OK: packet")


def honesty():
    r = load(REC)
    bb = r.get("both_branches") or {}
    if not (isinstance(bb.get("counts_match_expectation"), bool) and str(bb.get("stop_rule", "")).strip()):
        fail("both_branches needs counts_match_expectation (true or false) and a stop_rule")
    for k, v in (r.get("firms") or {}).items():
        if not str(v.get("note", "")).strip():
            fail("%s: a note stating what the counts rest on and what was not read is required" % k)
    no_long_digits(json.dumps(r))
    f = ROOT / PACKET
    if f.is_file():
        no_long_digits(f.read_text(encoding="utf-8"))
    else:
        fail("no %s" % PACKET)
    for k in BOUND:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    if r.get("uploaded") is not False:
        fail("uploaded must be false")
    print("OK: honest record")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB191-1" or arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    {"AC1": counts, "AC2": packet, "AC3": honesty}[arm]()
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
