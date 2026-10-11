"""python -I runtests_426.py <mirror> <reldir> <out_json> <test file>...  -- run the pin's test files against the mirror's flat tree, offline."""
import json
import os
import re
import subprocess
import sys
mirror, reldir, out = [os.path.abspath(a) if i != 1 else a for i, a in enumerate(sys.argv[1:4])]
files = sys.argv[4:]
work = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(mirror, "infra", "aws", "lambda", "investor-reporting", reldir)
code = ("import sys; sys.dont_write_bytecode=True; sys.path.insert(0, %r); sys.path.insert(1, %r); import pytest; "
        "sys.exit(pytest.main(['-q','-rA','--color=no','--tb=line','-p','guard426','--continue-on-collection-errors','-p','no:cacheprovider','--rootdir',%r] + %r))") % (work, os.path.join(work, "stubs"), base, [os.path.join(base, "tests", f) for f in files])
env = dict(os.environ, SITES=os.environ.get("SITES",""), SITES_OUT=os.environ.get("SITES_OUT",""), AWS_ACCESS_KEY_ID="fake", AWS_SECRET_ACCESS_KEY="fake", AWS_DEFAULT_REGION="us-east-1", PYTHONDONTWRITEBYTECODE="1")
for k in ("AWS_PROFILE", "AWS_SESSION_TOKEN"):
    env.pop(k, None)
r = subprocess.run([sys.executable, "-I", "-c", code], cwd=base, capture_output=True, env=env, timeout=900)
text = (r.stdout + r.stderr).decode("utf-8", "replace")
res = {}
for ln in text.splitlines():
    m = re.match(r"(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(\S+)", ln)
    if m:
        res[m.group(2).replace("\\", "/")] = m.group(1)
guard = re.search(r"OFFLINE-GUARD-ATTEMPTS=(\d+)", text)
json.dump({"rc": r.returncode, "results": res, "guard_attempts": int(guard.group(1)) if guard else None, "tail": text[-1500:]}, open(out, "w"), indent=1, sort_keys=True)
c = {}
for v in res.values():
    c[v] = c.get(v, 0) + 1
print(os.path.basename(mirror), reldir, "files", len(files), "rc", r.returncode, c, "guard", guard.group(1) if guard else None)
