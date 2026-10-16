"""IRPT_BCKEND workstream ~PM round 3 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the 49 Financial holdings-performance role reads its own split-adjust transactions prefix (the forward fix of Act 1, row IRPT_BCKEND-D2-S217).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB245-1  IB-pr-614  one inline IAM policy gains list+get on schwab/08335338/silver/fact_trn/ only; then ONE recovery invoke with the schedule's own input
    AC1  the gates: the packet's blob, the CTO half signed at it, Act 1's ledger still open, the function at the signed candidate, one change at a time
    AC2  the change: one file edited, the plan 1 change / 0 add / 0 destroy on the one policy, safe-apply, re-plan 0, the simulate battery before and after (counts)
    AC3  the recovery: one invoke, the schedule's own input, no FunctionError, the manifest declares split_adjust, the next fire stated, the counters
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB245-1_iam_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_PERF_ROLE_TRANSACTIONS_READ_IAM_PAIR_PACKET_AND_COO_HALF.md"
CTO_DIR = D + "1.0.0_SA_CTO~DELL2"
CTO_GLOB = "*PERF_ROLE_TRANSACTIONS_READ*CTO_HALF*.md"
PACKET_BLOB = "03cd6e9d4618a0c46c36bc8adb8e2cfb9485fa86"
CAND = "LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg="
POLICY = "aws_iam_role_policy.irpt_holdings_performance"
LOCALS = "infra/aws/terraform/investor-reporting/holdings-performance/locals.tf"
SCHEDULE_INPUT = {"kind": "irpt_holdings_performance_daily", "note": "scheduled fire; handler.py resolves the target trading day itself", "source": "schwab_08335338"}
fail, load, is_int = P6.fail, P6.load, P6.is_int


def blob(rel):
    return subprocess.run(["git", "hash-object", "--stdin"], input=(P6.ROOT / rel).read_bytes(), capture_output=True, timeout=60).stdout.decode().strip()


def ac1(r):
    f = P6.ROOT / PACKET
    if not f.is_file() or blob(PACKET) != PACKET_BLOB:
        fail("the packet must exist with the signed blob %s" % PACKET_BLOB)
    halves = sorted((P6.ROOT / CTO_DIR).glob(CTO_GLOB)) if (P6.ROOT / CTO_DIR).is_dir() else []
    if not halves:
        fail("no CTO half matching %s/%s" % (CTO_DIR, CTO_GLOB))
    t = halves[0].read_text(encoding="utf-8")
    if PACKET_BLOB[:10] not in t or not re.search(r"(?<![A-Za-z])SIGNED", t.upper()):
        fail("the CTO half must name the packet blob and read SIGNED")
    g = r.get("gates") or {}
    if g.get("packet_blob") != PACKET_BLOB or g.get("both_halves_signed") is not True:
        fail("gates must carry the packet blob and both_halves_signed true")
    if g.get("act_1_ledger_open") is not True or g.get("function_code_sha256") != CAND or g.get("one_change_at_a_time") is not True:
        fail("gates: Act 1's ledger must read OPEN (this is its completion), the function at the signed candidate, one change at a time")
    print("OK: the gates: the packet blob, both halves signed, Act 1's ledger open, the candidate live")


def ac2(r):
    c = r.get("change") or {}
    if c.get("files_changed") != [LOCALS]:
        fail("change.files_changed must be exactly [%s]" % LOCALS)
    p = c.get("plan") or {}
    if p.get("add") != 0 or p.get("change") != 1 or p.get("destroy") != 0 or p.get("resources") != [POLICY]:
        fail("the plan must read add 0, change 1, destroy 0 on exactly [%s]" % POLICY)
    if c.get("path") != "terraform-safe-apply" or c.get("safe_apply_rc") != 0 or c.get("replan_changes") != 0:
        fail("the change must go through safe-apply with rc 0 and a re-plan of 0 changes")
    b, a = r.get("simulate_before") or {}, r.get("simulate_after") or {}
    if b.get("allowed_arms_implicit_deny") != 2 or b.get("denied_arms_implicit_deny") != 8 or b.get("unchanged_arms_allowed") != 4:
        fail("simulate_before must read allowed_arms_implicit_deny 2, denied_arms_implicit_deny 8, unchanged_arms_allowed 4 (the gap shown first)")
    if a.get("allowed_arms_allowed") != 2 or a.get("denied_arms_implicit_deny") != 8 or a.get("unchanged_arms_allowed") != 4:
        fail("simulate_after must read allowed_arms_allowed 2, denied_arms_implicit_deny 8, unchanged_arms_allowed 4")
    print("OK: one file, one policy, plan 1/0/0 through safe-apply, re-plan 0, the simulate battery before and after")


def ac3(r):
    v = r.get("recovery") or {}
    if v.get("invokes") != 1 or v.get("event") != SCHEDULE_INPUT or v.get("status_code") != 200 or v.get("function_error_absent") is not True:
        fail("recovery must be ONE invoke with exactly the schedule's own input, status 200, no FunctionError")
    if v.get("manifest_split_adjust_declared") is not True or v.get("run_ok") is not True or not is_int(v.get("days_written")) or v["days_written"] < 1:
        fail("recovery must read run_ok true, the manifest's split_adjust declared true and days_written 1 or more")
    if v.get("next_scheduled_fire_utc") != "2026-10-19T11:30:00Z":
        fail("recovery.next_scheduled_fire_utc must read 2026-10-19T11:30:00Z (Monday, from the schedule)")
    if r.get("rollback_performed") is not False or r.get("act2_started") is not False or r.get("ledger_closed_by_applier") is not False:
        fail("rollback_performed false, act2_started false, ledger_closed_by_applier false (the issuer closes)")
    k = r.get("counters") or {}
    want = {"lambda_invokes": 1, "iam_changes": 1, "artifact_uploads": 0, "schedule_changes": 0, "files_deleted": 0, "markers_closed": 0, "served_keys_written_by_me": 0}
    for key, val in want.items():
        if k.get(key) != val:
            fail("counters.%s must read %s, read %r" % (key, val, k.get(key)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: one recovery invoke with the schedule's own input, no error, the next fire stated, the counters")


CHECKS = {"IB245-1-AC1": ac1, "IB245-1-AC2": ac2, "IB245-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p245_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
