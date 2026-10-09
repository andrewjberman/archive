"""IRPT_DASHBD round 41 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 9.1 (msg 3011): the svc-custody-statement mint landing and
CU-g-2a (the first real retained Performance client statement, carrying E-P9's persist reads), absorbed from IRPT_CUSTDY (handover
@185805a565). E1 (the 11:41Z R37 fire read) is the issuer's own read, not a cell.

Cells: DB-b-84 the mint landing by 0.7.0_AE_CloudOps~DB2 under the existing pair; DB-b-85 the statement script and its offline test (a
worker build); DB-b-86 the two real writes and their live re-reads by ~DB2, with the other-firm refusals.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB41-1-AC1  ~DB2/MINT_RECORD.json before_read {secret_absent true, ib_pr_385_live true, release_6b_code starting "tdpterTM"}; claims
              {sub "svc-custody-statement", firmId "cottonwood", userType "service", tier "service"} with none of role, advisorId,
              allowedPages, allowedTabs, firmRole; ttl_days a number <= 90.
  DB41-1-AC2  secret {name "opal/investor-reporting/svc-custody-statement", arn non-empty}; reader {routed_via "0.0.0_AB_MSTR~DELL2",
              applied true, simulate_listed "allowed", simulate_unlisted "implicitDeny"}.
  DB41-1-AC3  ledger_entry an existing org/critical_paths/change_management/ file whose text names svc-custody-statement.
  DB41-2-AC1  pytest of data/assets/scripts/gold/irpt_custody/tests/test_e2a_real_statement.py passes (rc 0, "passed" in its output).
  DB41-2-AC2  `python data/assets/scripts/gold/irpt_custody/e2a_real_statement.py --help` names run, verify-submission and verify-persisted.
  DB41-3-AC1  `e2a_real_statement.py verify-submission --refs <~DB2/E2A_REFS.json>` prints "SUBMISSION RETAINED policy=irpt-custody-x10-v1".
  DB41-3-AC2  `e2a_real_statement.py verify-persisted --refs <~DB2/E2A_REFS.json>` prints "PERSISTED kind=CUSTODY_REPORT".
  DB41-3-AC3  the refs file's other_firm list holds 49financial and inflection, each {refused true, status, written false}.
"""
import json
import subprocess
import sys
from pathlib import Path

DB2 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.7.0_AE_CloudOps~DB2/"
SCRIPT = "data/assets/scripts/gold/irpt_custody/e2a_real_statement.py"
TEST = "data/assets/scripts/gold/irpt_custody/tests/test_e2a_real_statement.py"
ABSENT = ["role", "advisorId", "allowedPages", "allowedTabs", "firmRole"]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB41"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def run(args):
        if not (root / SCRIPT).is_file():
            fail("no %s" % SCRIPT)
        r = subprocess.run([sys.executable] + args, cwd=str(root), capture_output=True, text=True, timeout=600)
        return r.returncode, (r.stdout or "") + (r.stderr or "")

    if cid.startswith("DB41-1-"):
        r = load(DB2 + "MINT_RECORD.json")
        if cid == "DB41-1-AC1":
            b, c = r.get("before_read") or {}, r.get("claims") or {}
            if b.get("secret_absent") is not True or b.get("ib_pr_385_live") is not True or not str(b.get("release_6b_code") or "").startswith("tdpterTM"):
                fail("before_read %r" % b)
            want = {"sub": "svc-custody-statement", "firmId": "cottonwood", "userType": "service", "tier": "service"}
            if any(c.get(k) != v for k, v in want.items()) or any(k in c for k in ABSENT):
                fail("claims %r" % {k: c.get(k) for k in list(want) + ABSENT})
            if not num(r.get("ttl_days")) or r["ttl_days"] > 90:
                fail("ttl_days %r" % r.get("ttl_days"))
            print("OK: before-read holds; claims exact (cottonwood, service), TTL %s d" % r["ttl_days"])
        elif cid == "DB41-1-AC2":
            s, rd = r.get("secret") or {}, r.get("reader") or {}
            if s.get("name") != "opal/investor-reporting/svc-custody-statement" or not s.get("arn"):
                fail("secret %r" % s)
            if rd.get("routed_via") != "0.0.0_AB_MSTR~DELL2" or rd.get("applied") is not True \
                    or rd.get("simulate_listed") != "allowed" or rd.get("simulate_unlisted") != "implicitDeny":
                fail("reader %r" % rd)
            print("OK: secret created; reader grant routed via MSTR, simulated allowed / implicitDeny")
        elif cid == "DB41-1-AC3":
            le = str(r.get("ledger_entry") or "")
            p = root / le
            if not le.startswith("org/critical_paths/change_management/") or not p.is_file() \
                    or "svc-custody-statement" not in p.read_bytes().decode("utf-8", "replace"):
                fail("ledger_entry %r" % le)
            print("OK: ledger %s" % le)
        else:
            fail("unknown criterion %r" % cid)
    elif cid == "DB41-2-AC1":
        if not (root / TEST).is_file():
            fail("no %s" % TEST)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", TEST], cwd=str(root), capture_output=True, text=True, timeout=600)
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode != 0 or "passed" not in out:
            fail("pytest rc %d: %s" % (r.returncode, out.strip().splitlines()[-1:] if out.strip() else ""))
        print("OK: " + out.strip().splitlines()[-1])
    elif cid == "DB41-2-AC2":
        rc, out = run([SCRIPT, "--help"])
        miss = [s for s in ("run", "verify-submission", "verify-persisted") if s not in out]
        if rc != 0 or miss:
            fail("--help rc %d, missing %r" % (rc, miss))
        print("OK: the three subcommands are present")
    elif cid in ("DB41-3-AC1", "DB41-3-AC2"):
        refs = DB2 + "E2A_REFS.json"
        if not (root / refs).is_file():
            fail("no %s" % refs)
        sub, want = (("verify-submission", "SUBMISSION RETAINED policy=irpt-custody-x10-v1") if cid.endswith("AC1")
                     else ("verify-persisted", "PERSISTED kind=CUSTODY_REPORT"))
        rc, out = run([SCRIPT, sub, "--refs", refs])
        if rc != 0 or want not in out:
            fail("%s rc %d; %r not in output" % (sub, rc, want))
        print("OK: " + [ln for ln in out.splitlines() if want in ln][0].strip())
    elif cid == "DB41-3-AC3":
        r = load(DB2 + "E2A_REFS.json")
        of = {x.get("firm"): x for x in (r.get("other_firm") or []) if isinstance(x, dict)}
        bad = [f for f in ("49financial", "inflection") if (of.get(f) or {}).get("refused") is not True
               or (of.get(f) or {}).get("written") is not False or not (of.get(f) or {}).get("status")]
        if bad:
            fail("other-firm refusals missing or not refused/unwritten: %r" % bad)
        print("OK: 49financial and inflection refused, nothing written")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
