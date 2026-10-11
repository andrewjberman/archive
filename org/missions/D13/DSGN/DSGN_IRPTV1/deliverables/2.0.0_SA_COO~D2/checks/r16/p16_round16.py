"""DSGN_IRPTV1 round 16 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's retirement rulings msg 4446 and the 43-id table's UNCUT ids.

Cell: IV-e-94 ONE batched repair cell on the portal slot: the five git-diff arms on ModelPortfolios.tsx retired (behavioural arms kept),
the ycharts forbidden token retired with its duty, the explicit-null business_date arm decided from the contract's own line, the two stale
source pins re-pinned, and the five absent-to-null coalesces in contracts/adapt.ts each carried as absent or cited.

The baseline is ~43/SUITE_SAMPLE.json (43 ids); the table is ~50/FAILING_ID_TABLE.json.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV94-AC1  ~52/REPAIRS.json: items holds exactly the nine keys diff_arms, ycharts_token, business_date, ive116_pin, ive137_pin,
            adapt_coalesces, and the three explicit deferrals ive26_wire_generator, smoke_map, unprojected_grant; every non-deferred item
            has outcome DONE or STOPPED (a STOPPED carries a row id), ids (baseline ids it concerns) and evidence; business_date
            carries contract_line {file, line, text} and decision NULL_ADMITTED_REGRESSION or NULL_FORBIDDEN_RETIRED; ycharts_token
            carries guarded {commit, what} and rendered_text_assertion ADDED / NOT_NEEDED with a reason; adapt_coalesces lists five
            sites each ABSENT_CARRIED or CONTRACT_ADMITS_NULL with its contract line; each deferral names its owner and reason.
  IV94-AC2  the same record's suite_after: new_failing_ids == [] and every id under the DONE items is in fixed_ids or in retired_ids
            (an id whose assertion was retired is no longer run, so it is listed there with the ruling that retired it); portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~"
WORK = ("diff_arms", "ycharts_token", "business_date", "ive116_pin", "ive137_pin", "adapt_coalesces")
DEFER = ("ive26_wire_generator", "smoke_map", "unprojected_grant")
HEX = re.compile(r"^[0-9a-f]{7,40}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV16"))
        sys.exit(1)

    p = root / (D + "52/REPAIRS.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    items = r.get("items") or {}
    if sorted(items) != sorted(WORK + DEFER):
        fail("items %r, want exactly %r" % (sorted(items), sorted(WORK + DEFER)))
    if cid == "IV94-AC1":
        for k in WORK:
            x = items[k]
            if x.get("outcome") not in ("DONE", "STOPPED") or not isinstance(x.get("ids"), list) or not str(x.get("evidence") or "").strip():
                fail("%s lacks an outcome, ids or evidence" % k)
            if x["outcome"] == "STOPPED" and not str(x.get("row") or "").strip():
                fail("%s is STOPPED without a row id" % k)
        b = items["business_date"]
        cl = b.get("contract_line") or {}
        if b["outcome"] == "DONE" and (b.get("decision") not in ("NULL_ADMITTED_REGRESSION", "NULL_FORBIDDEN_RETIRED") or not cl.get("file")
                                       or not isinstance(cl.get("line"), int) or not str(cl.get("text") or "").strip()):
            fail("business_date lacks its contract line or decision")
        y = items["ycharts_token"]
        g = y.get("guarded") or {}
        if y["outcome"] == "DONE" and (not g.get("commit") or not str(g.get("what") or "").strip()
                                       or y.get("rendered_text_assertion") not in ("ADDED", "NOT_NEEDED") or not str(y.get("reason") or "").strip()):
            fail("ycharts_token lacks what it guarded or its rendered-text decision")
        a = items["adapt_coalesces"]
        sites = a.get("sites") or []
        if a["outcome"] == "DONE" and (len(sites) != 5 or any(s.get("result") not in ("ABSENT_CARRIED", "CONTRACT_ADMITS_NULL")
                                                              or not isinstance(s.get("line"), int) for s in sites)
                                       or any(s["result"] == "CONTRACT_ADMITS_NULL" and not str(s.get("contract_line") or "").strip() for s in sites)):
            fail("adapt_coalesces wants five sites, each ABSENT_CARRIED or CONTRACT_ADMITS_NULL with its contract line")
        for k in DEFER:
            x = items[k]
            if x.get("outcome") != "DEFERRED" or not str(x.get("owner") or "").strip() or not str(x.get("reason") or "").strip():
                fail("%s is not a DEFERRED item with an owner and a reason" % k)
        print("OK: six repair items %r; three deferrals named" % {k: items[k]["outcome"] for k in WORK})
    elif cid == "IV94-AC2":
        s = r.get("suite_after") or {}
        if s.get("new_failing_ids") != [] or not isinstance(s.get("fixed_ids"), list) or not isinstance(s.get("retired_ids"), list):
            fail("suite_after wants new_failing_ids == [] and the fixed_ids and retired_ids lists")
        done = set()
        for k in WORK:
            if items[k].get("outcome") == "DONE":
                done |= set(items[k].get("ids") or [])
        gone = set(s["fixed_ids"]) | set(x.get("id") for x in s["retired_ids"] if str(x.get("ruling") or "").strip())
        if not done <= gone:
            fail("%d id(s) of DONE items are neither fixed nor retired with a ruling: %r" % (len(done - gone), sorted(done - gone)[:3]))
        if not HEX.match(str(r.get("portal_commit") or "")):
            fail("portal_commit missing")
        print("OK: %d id(s) of DONE items accounted for (%d fixed, %d retired); no new failing id; %d still failing"
              % (len(done), len(s["fixed_ids"]), len(s["retired_ids"]), s.get("failed", -1)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
