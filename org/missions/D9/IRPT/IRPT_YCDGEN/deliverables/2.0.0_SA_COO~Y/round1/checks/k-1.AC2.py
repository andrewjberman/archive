"""IRPT_YCDGEN round 1 check k-1.AC2 (YCD-k-1). Run from the repository root. Prints 'k-1.AC2 RESULT: PASS|FAIL <why>'."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"


def verdict(ok, why):
    print("k-1.AC2 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)


def pytest_count(test_file, minimum):
    path = RESEARCH / "tests" / test_file
    if not path.is_file():
        verdict(False, "absent: %s" % path.relative_to(ROOT).as_posix())
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(path)],
                         capture_output=True, text=True, timeout=110)
    tail = (out.stdout.strip().splitlines() or [""])[-1]
    passed = int((re.search(r"(\d+) passed", tail) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", tail) or [0, 0])[1]) + int((re.search(r"(\d+) error", tail) or [0, 0])[1])
    verdict(out.returncode == 0 and failed == 0 and passed >= minimum, "%d passed, %d failed (need >= %d): %s" % (
        passed, failed, minimum, tail[:160]))

sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
try:
    policy = opal_naming.reporting_policy("irpt-ycdgen-research-v1")
except Exception as exc:  # the registry refuses or the row is absent
    verdict(False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))
want = {"YCHARTS_RESPONSE": ("state", "ycharts_responses", "json"), "YCHARTS_RUN": ("state", "ycharts_runs", "json"),
        "YCHARTS_OPAL_REPORT": ("state", "ycharts_opal_reports", "pdf")}
fam = policy.get("families") or {}
got = {k: (v.get("tier"), v.get("table"), v.get("extension")) for k, v in fam.items()}
ok = (got == want and policy.get("state") == "PENDING_ENFORCEMENT" and policy.get("firms") == ["cottonwood"]
      and all(v.get("unreferenced_days") == 30 and v.get("accepted_ceiling_days") == 2555 for v in fam.values()))
verdict(ok, "families %s state %s firms %s" % (sorted(got), policy.get("state"), policy.get("firms")))
