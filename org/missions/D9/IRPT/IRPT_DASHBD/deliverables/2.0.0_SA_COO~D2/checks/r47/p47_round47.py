"""IRPT_DASHBD round 47 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's R44 CTO half (@fa8d2c2961) and ADDENDUM 13.1 (msg 3413).

Cells: DB-b-95 the R44 apply (DB-b-90 + DB-b-91 as ONE gold Lambda release over yIAQjspL); DB-b-96 the per-firm sources entry carries
valuation_source / fee_treatment / price_basis and the returns manifest reads them, never defaulting (W66-S1); DB-b-97 the backfill path
clears a landed day from the lots status record (W69-S2).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB47-1-AC1  ~70/R44_APPLY_RECORD.json: base_codesha256_before == yIAQjspL; upload_member_diff is EXACTLY the two member paths;
              status_prefix_objects_before == 0; plan == {add 0, change 1, destroy 0}; live_codesha256_after == built_codesha256;
              replan_no_changes is true; ledger_entry names a file at HEAD.
  DB47-2-AC1  ~71/SOURCES_FIELDS.json tests {passed > 0, failed == 0, new_test, negative_test} with both functions at HEAD; every custody
              source in data/assets/scripts/gold/irpt_reporting/sources.json carries valuation_source, fee_treatment and price_basis; the
              producer account_return_daily.py carries the literals "valuation_source" and "absent".
  DB47-3-AC1  ~72/BACKFILL_CLEARS.json tests {passed > 0, failed == 0, new_test} with the function at HEAD; reporting-gold handler.py calls
              record_lots_status from at least two call sites.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
BASE = "yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE="
MEMBERS = {"data/assets/scripts/gold/irpt_reporting/account_activity_lots.py",
           "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"}
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB47"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def fn_ok(s):
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(s or ""))
        return bool(m) and (root / m.group(1)).is_file() and bool(
            re.search(r"^def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M))

    def tests_ok(r, *extra):
        t = r.get("tests") or {}
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not fn_ok(t.get("new_test")) \
                or any(not fn_ok(t.get(k)) for k in extra):
            fail("tests %r" % t)
        return t

    if cid == "DB47-1-AC1":
        r = load(D + "70/R44_APPLY_RECORD.json")
        if r.get("base_codesha256_before") != BASE:
            fail("base_codesha256_before %r" % r.get("base_codesha256_before"))
        if set(r.get("upload_member_diff") or []) != MEMBERS or len(r.get("upload_member_diff") or []) != 2:
            fail("upload_member_diff %r" % r.get("upload_member_diff"))
        if r.get("status_prefix_objects_before") != 0:
            fail("status_prefix_objects_before %r" % r.get("status_prefix_objects_before"))
        if r.get("plan") != {"add": 0, "change": 1, "destroy": 0}:
            fail("plan %r" % r.get("plan"))
        if not r.get("built_codesha256") or r.get("live_codesha256_after") != r.get("built_codesha256"):
            fail("live %r != built %r" % (r.get("live_codesha256_after"), r.get("built_codesha256")))
        if r.get("replan_no_changes") is not True:
            fail("replan_no_changes %r" % r.get("replan_no_changes"))
        if not r.get("ledger_entry") or not (root / r["ledger_entry"]).is_file():
            fail("ledger_entry %r" % r.get("ledger_entry"))
        print("OK: R44 applied over yIAQjspL; 2 members; live = built %s" % r["built_codesha256"][:8])
    elif cid == "DB47-2-AC1":
        r = load(D + "71/SOURCES_FIELDS.json")
        t = tests_ok(r, "negative_test")
        doc = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
        srcs = {k: v for k, v in doc.items() if isinstance(v, dict) and not k.startswith("_")}
        if not srcs:
            fail("no custody source in sources.json")
        for k, v in srcs.items():
            for f in ("valuation_source", "fee_treatment", "price_basis"):
                if not isinstance(v.get(f), str) or not v[f].strip():
                    fail("source %s lacks %s" % (k, f))
        src = (root / PRODUCER).read_text(encoding="utf-8")
        if "valuation_source" not in src or '"absent"' not in src and "'absent'" not in src:
            fail("producer does not read valuation_source with an absent arm")
        print("OK: %d source(s) carry the three fields; %d passed" % (len(srcs), t["passed"]))
    elif cid == "DB47-3-AC1":
        r = load(D + "72/BACKFILL_CLEARS.json")
        t = tests_ok(r)
        h = (root / HANDLER).read_text(encoding="utf-8")
        calls = len(re.findall(r"(?<!def )\brecord_lots_status\(", h))
        if calls < 2:
            fail("record_lots_status has %d call site(s); want >= 2" % calls)
        print("OK: record_lots_status called from %d sites; %d passed" % (calls, t["passed"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
