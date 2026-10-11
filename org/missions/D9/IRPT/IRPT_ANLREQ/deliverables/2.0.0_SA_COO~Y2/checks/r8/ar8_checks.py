"""ar8_checks.py -- the mechanical checks of IRPT_ANLREQ round 8, workstream Y (cell AR-y-81, the drafter's READY gate).

Usage:  python ar8_checks.py <check> --root <workspace root>

  y81-gate   the gate's test file holds the five named tests and passes, and the design record exists with its
             members filled                                                                       -> Y81-GATE-OK
  y81-keep   the three test folders the gate could touch pass as at the base (the difference control) -> Y81-KEEP-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
DESIGN = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r8/READY_GATE_DESIGN.json"
NAMES = (
    "test_a_request_whose_job_reads_ready_is_answered_as_before",
    "test_a_request_whose_job_reads_received_is_refused",
    "test_a_request_with_no_job_row_is_refused",
    "test_the_refusal_names_no_job_state_and_no_identifier",
    "test_the_drafter_stores_no_draft_and_sends_nothing_when_the_gate_refuses",
)
# folder -> the failed count at the base, read by the issuer before the cut
KEEP = {IR + "/reports/tests": 0, "data/transcripts/scripts/tests": 0}
TOKENS = {"y81-gate": "Y81-GATE", "y81-keep": "Y81-KEEP"}


def run(cmd, cwd, env):
    got = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return got.returncode, (got.stdout or "") + (got.stderr or "")


def failed_count(out, rc):
    last = [line for line in re.sub(r"\x1b\[[0-9;]*m", "", out).splitlines() if line.strip()][-1:]
    found = re.search(r"(\d+) failed", last[0] if last else "")
    return (int(found.group(1)) if found else (0 if rc == 0 else -1)), (last[0] if last else "")


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    problems = []
    if check == "y81-gate":
        design = root / DESIGN
        if not design.is_file():
            problems.append("no design record %s" % DESIGN)
            test_file = None
        else:
            doc = json.loads(design.read_text(encoding="utf-8"))
            for key in ("where_the_gate_lives", "why_there", "how_job_state_is_read", "new_permission_needed", "refusal_reason",
                        "callers_of_the_gated_read", "test_file"):
                if doc.get(key) in (None, "", []):
                    problems.append("design record lacks %s" % key)
            if doc.get("new_permission_needed") not in ("NO", "YES"):
                problems.append("new_permission_needed must read NO or YES, with the grant named in why_there when YES")
            test_file = doc.get("test_file")
        if test_file:
            path = root / test_file
            if not path.is_file():
                problems.append("the named test file %s does not exist" % test_file)
            else:
                text = path.read_text(encoding="utf-8")
                for name in NAMES:
                    if not re.search(r"^def %s\(" % name, text, flags=re.M):
                        problems.append("no test named %s" % name)
                rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file], root, env)
                count, last = failed_count(out, rc)
                print(last)
                if rc != 0:
                    problems.append("pytest rc=%d on the gate's test file" % rc)
    else:
        for folder, base in KEEP.items():
            if not (root / folder).exists():
                problems.append("folder absent: %s" % folder)
                continue
            rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", folder], root, env)
            count, last = failed_count(out, rc)
            print("%s: %s" % (folder, last))
            if base is not None and count != base:
                problems.append("%s fails %d, the base failed %d" % (folder, count, base))
            if base is None and count != 0:
                problems.append("%s fails %d (the issuer's base read is in the order: compare and state it)" % (folder, count))
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
