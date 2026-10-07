"""CB5e4-AC1 check (2.0.0_SA_COO~C2, round 5): the C-RESTRICTED apply write-in exists, is valid, and carries what the laptop needs.

Reads (never writes):
- every ADVI_COTBKF request record under org/devices/role_requests/dell2/, each run through `role_request.py validate`;
- the write-in note deliverables/0.9.0_WK_ADVI_COTBKF~19/C_RESTRICTED_WRITE_IN.md.
LAST line: E4-WRITE-IN request_valid=<bool> cites_policy_file=<bool> note_carries_ac1=<bool> records=<n>
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[8]
RECORDS = ROOT / "org" / "devices" / "role_requests" / "dell2"
NOTE = ROOT / "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~19/C_RESTRICTED_WRITE_IN.md"
POLICY_FILE = "infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf"
AC1 = "infra/aws/terraform/shared-infra/tests/check_restricted_prefix.py"


def main() -> int:
    recs = []
    for p in sorted(RECORDS.glob("*.json")) if RECORDS.is_dir() else []:
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(rec, dict) and rec.get("project") == "ADVI_COTBKF":
            recs.append((p, rec))
    valid = cites = False
    for p, rec in recs:
        r = subprocess.run([sys.executable, "org/devices/role_request.py", "validate", str(p)], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        ok = r.returncode == 0 and last.endswith("ok=True")
        cited = any(POLICY_FILE in str(perm) for perm in rec.get("permissions", []))
        print("%s: %s cites_policy_file=%s" % (p.name, last or "(no output)", cited))
        valid = valid or ok
        cites = cites or (ok and cited)
    note_ok = NOTE.is_file() and AC1 in NOTE.read_text(encoding="utf-8")
    print("E4-WRITE-IN request_valid=%s cites_policy_file=%s note_carries_ac1=%s records=%d" % (valid, cites, note_ok, len(recs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
