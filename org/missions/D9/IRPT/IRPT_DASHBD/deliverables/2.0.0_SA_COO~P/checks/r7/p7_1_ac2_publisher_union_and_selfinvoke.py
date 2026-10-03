"""DB7-1-AC2 -- rows IRPT_DASHBD-W1-S12 and W1-S13: the publisher publishes every account any gold partition holds (not only the
newest partition's), and its role may invoke ITS OWN function for the shard fan-out, nothing wider.

Grades:
  1. infra/aws/lambda/investor-reporting/reporting-publish/tests/test_publisher_account_union.py names "union" and "newest"; at least
     2 tests pass, 0 failed or errored (bounded at 110 s).
  2. infra/aws/terraform/investor-reporting/reporting-publish/iam.tf grants "lambda:InvokeFunction", and every resource the file
     names in a statement carrying that action references the publish function's own name or ARN (the module output or the name
     module), never "*".
Usage: python <this file> <repo_root>
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "infra/aws/lambda/investor-reporting/reporting-publish/tests/test_publisher_account_union.py"
IAM = "infra/aws/terraform/investor-reporting/reporting-publish/iam.tf"


def fail(msg):
    print("FAIL: " + msg)
    print("DB7-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for word in ("union", "newest"):
        if word not in src:
            fail("the test file never names %r" % word)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST],
                       cwd=str(root), capture_output=True, text=True, timeout=110)
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad or not passed or int(passed.group(1)) < 2:
        fail("union tests: %s" % (bad.group(0) if bad else out.strip()[-200:]))
    tf = (root / IAM).read_text(encoding="utf-8")
    blocks = [b for b in re.split(r"\n\s*statement\s*\{", tf) if "lambda:InvokeFunction" in b]
    if not blocks:
        fail("iam.tf grants no lambda:InvokeFunction")
    for b in blocks:
        res = re.search(r"resources\s*=\s*\[(.*?)\]", b, re.S)
        if not res:
            fail("an InvokeFunction statement names no resources")
        items = [x.strip() for x in res.group(1).split(",") if x.strip()]
        if not items or any(x.strip('"') == "*" for x in items):
            fail("an InvokeFunction statement is wildcarded: %s" % items)
        if not all("irpt_reporting_publish" in x for x in items):
            fail("an InvokeFunction resource is not the publish function's own: %s" % items)
    print("OK: %s union tests; InvokeFunction scoped to the publish function itself (%d statement(s))"
          % (passed.group(1), len(blocks)))
    print("DB7-1-AC2 PASS")


if __name__ == "__main__":
    main()
