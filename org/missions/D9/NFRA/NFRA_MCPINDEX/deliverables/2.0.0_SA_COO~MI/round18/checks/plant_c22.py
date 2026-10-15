"""plant_c22.py -- the ISSUER's cut-time planted arms for c22.AC1 and c22.AC2 (standing battery clause 1). NOT given to a worker. Run from the repo root.

Extracts the BASE gateway tree (git ref 06cfb6db64) into temp folders and plants: a GOOD tree (the new signature etfs_get_positioning(as_of="", fund_ticker=""), the answer path untouched, a 10-test file) and bad ones
(an answer that changed for an existing input, a typed S3 key, the arguments in the wrong order, nine tests). c22.AC3 (pytest) is not plantable in an extracted tree."""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "06cfb6db64"
GW = "infra/aws/ec2/opal-gateway"
PI = "app/integrations/portal_index/integration.py"
OLD = 'def etfs_get_positioning(as_of: str = "") -> dict:'
NEW = 'def etfs_get_positioning(as_of: str = "", fund_ticker: str = "") -> dict:'
tmp = tempfile.mkdtemp(prefix="plant_c22_")


def tree(name, sig=NEW, extra_line=None, tests=10, change_answer=False):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    subprocess.run("git archive %s %s | tar -x -C %s" % (BASE, GW, d.replace("\\", "/")), shell=True, check=True)
    root = os.path.join(d, GW)
    p = os.path.join(root, PI)
    s = open(p, encoding="utf-8").read()
    assert OLD in s, "the base signature moved"
    s = s.replace(OLD, sig)
    if extra_line:
        s = s.replace("def s3_getter()", extra_line + "\n\n\ndef s3_getter()", 1)
    if change_answer:
        a = '    return {"status": "ok", "tool": tool, "bucket": bucket, "key": key, "as_of": object_as_of,'
        assert a in s
        s = s.replace(a, '    return {"status": "ok", "extra": 1, "tool": tool, "bucket": bucket, "key": key, "as_of": object_as_of,')
    open(p, "w", encoding="utf-8", newline="\n").write(s)
    open(os.path.join(root, "tests", "test_positioning_extension.py"), "w", encoding="ascii").write("\n\n".join("def test_planted_%d():\n    assert True" % i for i in range(tests)) + "\n")
    return root


def run(script, ac, root):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), ac], env=dict(os.environ, C22_GW=root), capture_output=True, text=True, timeout=290)
    return r.returncode


good = tree("good")
typed = tree("typed", extra_line='_KEY = "gold/book/"')
order = tree("order", sig='def etfs_get_positioning(fund_ticker: str = "", as_of: str = "") -> dict:')
few = tree("few", tests=9)
changed = tree("changed", change_answer=True)
arms = [("good tree, ac1", "c22_equal.py", "ac1", good, 0), ("good tree, ac2", "c22_check.py", "ac2", good, 0), ("an existing answer changed, ac1", "c22_equal.py", "ac1", changed, 1),
        ("a typed S3 key added, ac2", "c22_check.py", "ac2", typed, 1), ("arguments in the wrong order, ac2", "c22_check.py", "ac2", order, 1), ("nine tests only, ac2", "c22_check.py", "ac2", few, 1)]
ok = wrong = 0
for label, script, ac, root, want in arms:
    rc = run(script, ac, root)
    if rc == want:
        ok += 1
        print("ARM ok:    %s -> rc=%d" % (label, rc))
    else:
        wrong += 1
        print("ARM WRONG: %s -> rc=%d want %d" % (label, rc, want))
print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
shutil.rmtree(tmp, ignore_errors=True)
sys.exit(0 if wrong == 0 else 1)
