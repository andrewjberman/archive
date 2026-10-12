"""IRPT_DASHBD round 86 (issuer 2.0.0_SA_COO~D2) -- the R45 REFRESH 4 apply, under the signed pair (COO half @598347202e, CTO half @e969a090cc).

Cell: DB-b-164 the gold Lambda release over live oNgy4rnr, built from the packet's FOUR pins, by the dell2 cloud-ops seat.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB86-1-AC1  <AE folder>/irpt_dashbd_r45/R45_REFRESH4_APPLY_RECORD.json: packet_sha256 equals the packet's; base_codesha256_before is
              oNgy4rnr; the four pins re-hashed and equal; upload_member_diff is EXACTLY the four member paths; plan is 0/1/0;
              live_codesha256_after equals built_codesha256 and is not the base; replan_no_changes is true; ledger_entry names a file;
              the one dry-run invoke ran with status 200, no function error, duration and memory under the 85 percent lines, 0 objects
              written; no rollback.
"""
import json
import sys
from pathlib import Path

REC = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_dashbd_r45/R45_REFRESH4_APPLY_RECORD.json"
PACKET_SHA = "04cf16cd48161a931f5e5da740e60562ec9505d58c154a467375d12c6415ad72"
BASE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="
PINS = {
    "infra/aws/lambda/investor-reporting/reporting-gold/handler.py":
        ("080dc90d92542d96817ae79f4f8a72a85dd9de09", "d95f42d54aacd7efa6d054b12d3901e49b109427f910ff7a60ef6dcc7d36a116"),
    "data/assets/scripts/gold/irpt_reporting/account_return_daily.py":
        ("739dbb240f19b6dd2c08ce982c44c9b7c17ca322", "73361b54df395ae4a0de39d149e4ca822144dd9f0003d0fef6f98d786374383a"),
    "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py":
        ("19ba6fe341da80c906d0a1ff7a0db0253fdd2115", "c5364a9f81f0105ce675c28991fa6691e52f264cbf8a3ff5fc0e64c29fa73d2f"),
    "data/assets/scripts/gold/irpt_reporting/sources.json":
        ("f043506a7c3f5a7d997e6e4096ba094435e419a5", "b8f40af776589a1d3dc00c5d63f1e93508b812215c71d6baa5bf899a7f42fc3b"),
}
DURATION_LINE_MS = 765000
MEMORY_LINE_MB = 2556.8


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else "DB86-1-AC1"

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % cid)
        sys.exit(1)

    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    if r.get("packet_sha256") != PACKET_SHA:
        fail("packet_sha256 %r" % r.get("packet_sha256"))
    if r.get("base_codesha256_before") != BASE:
        fail("base_codesha256_before %r" % r.get("base_codesha256_before"))
    if not isinstance(r.get("rollback_version_id"), str) or not r["rollback_version_id"].strip():
        fail("rollback_version_id %r" % r.get("rollback_version_id"))
    pv = {x.get("file"): x for x in (r.get("pins_verified") or []) if isinstance(x, dict)}
    if set(pv) != set(PINS) or len(r.get("pins_verified") or []) != len(PINS):
        fail("pins_verified files %r" % sorted(pv))
    for f, (pin, sha) in PINS.items():
        if pv[f].get("pin") != pin or pv[f].get("sha256") != sha or pv[f].get("equal") is not True:
            fail("pin of %s: %r" % (f, pv[f]))
    diff = r.get("upload_member_diff") or []
    if set(diff) != set(PINS) or len(diff) != len(PINS):
        fail("upload_member_diff %r" % diff)
    if r.get("plan") != {"add": 0, "change": 1, "destroy": 0}:
        fail("plan %r" % r.get("plan"))
    built = r.get("built_codesha256")
    if not built or built == BASE or r.get("live_codesha256_after") != built:
        fail("live %r built %r" % (r.get("live_codesha256_after"), built))
    if r.get("replan_no_changes") is not True:
        fail("replan_no_changes %r" % r.get("replan_no_changes"))
    if not r.get("ledger_entry") or not (root / r["ledger_entry"]).is_file():
        fail("ledger_entry %r" % r.get("ledger_entry"))
    d = r.get("dry_run") or {}
    ev = d.get("event") or {}
    if ev.get("backfill") != {"start": "2026-10-08", "end": "2026-10-08"} or ev.get("dry_run") is not True:
        fail("dry_run event %r" % ev)
    if d.get("invoke_status_code") != 200 or d.get("invoke_function_error") is not None:
        fail("dry_run status %r error %r" % (d.get("invoke_status_code"), d.get("invoke_function_error")))
    dur, mem = d.get("duration_ms"), d.get("max_memory_mb")
    if not isinstance(dur, (int, float)) or dur >= DURATION_LINE_MS:
        fail("duration_ms %r is not under %d" % (dur, DURATION_LINE_MS))
    if not isinstance(mem, (int, float)) or mem >= MEMORY_LINE_MB:
        fail("max_memory_mb %r is not under %s" % (mem, MEMORY_LINE_MB))
    if d.get("written_objects") != 0:
        fail("written_objects %r" % d.get("written_objects"))
    if r.get("rollback") is not None:
        fail("rollback %r" % r.get("rollback"))
    print("OK: R45 REFRESH 4 applied over oNgy4rnr; 4 members; live = built %s; dry run %s ms, %s MB" % (built[:8], dur, mem))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
