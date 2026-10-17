"""IRPT_BCKEND workstream ~PM round 8 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the registry rows and builder outputs for the per-firm HMAC list (CTO msg 10234, rule 30).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM3A  IB-hm-3a  registry rows so the naming builders emit the three firm key addresses, the stage role name, its policy name and the secret name
    AC1  every recorded builder call is RE-RUN against the worktree and returns exactly the recorded result (no refusal); three address results in the globgrph bucket, one per firm; two name results
    AC2  the naming tests pass and the worker's ONE commit (HEAD~1..HEAD) touches only registry files, an optional naming test, and the order's paths
    AC3  the secret is a registered SECRET row of system irpt in slash grammar; the role and policy names are irpt names; the record holds no key material
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~450/IBhm3a_resolved.json"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~450/"
BUCKET = "s3://opal-313476888478-globgrph/"
RES = "infra/logic/registry/resources.json"
fail, load = P6.fail, P6.load


def _naming():
    f = P6.ROOT / "lib" / "opal_naming.py"
    if not f.is_file():
        fail("no lib/opal_naming.py in the worktree")
    sys.path.insert(0, str(P6.ROOT / "lib"))
    spec = importlib.util.spec_from_file_location("opal_naming_under_test", str(f))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ac1(r):
    calls = r.get("calls")
    if not isinstance(calls, list) or len(calls) != 5:
        fail("calls must be a list of exactly 5 builder calls (3 firm key addresses, the role name, the policy name)")
    mod = _naming()
    addrs, names = [], []
    for c in calls:
        fn = c.get("fn")
        if fn not in ("address", "name", "key"):
            fail("call fn must be address, name or key, read %r" % fn)
        try:
            got = getattr(mod, fn)(*(c.get("args") or []), **(c.get("kwargs") or {}))
        except Exception as e:  # a builder refusal is a missing registry row
            fail("the builder REFUSED call %s%r: %s: %s" % (fn, c.get("args"), type(e).__name__, str(e)[:160]))
        if got != c.get("result"):
            fail("call %s returned %r but the record says %r" % (fn, got, c.get("result")))
        (names if fn == "name" else addrs).append(got)
    if len(addrs) != 3 or len(names) != 2:
        fail("need 3 address/key calls and 2 name calls, read %d and %d" % (len(addrs), len(names)))
    if len(set(addrs)) != 3 or any(not a.startswith(BUCKET) for a in addrs):
        fail("the three addresses must be distinct and inside %s" % BUCKET)
    firms = r.get("firms")
    if not isinstance(firms, list) or len(firms) != 3 or len({str(f).lower() for f in firms}) != 3:
        fail("firms must list the three distinct firm tokens")
    for f in firms:
        if sum(1 for a in addrs if str(f).lower() in a.lower()) != 1:
            fail("firm token %r must appear in exactly one address" % f)
    print("OK: five builder calls re-run to the recorded results, three per-firm addresses in the globgrph bucket")


def ac2(_):
    p = subprocess.run([sys.executable, "-m", "pytest", "lib/tests", "-q", "-k", "naming", "--color=no", "-p", "no:cacheprovider"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        fail("naming tests rc %s: %s" % (p.returncode, p.stdout[-300:].replace("\n", " | ")))
    g = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if g.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % g.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in g.stdout.split() if x.strip()]
    reg = [x for x in files if x.startswith("infra/logic/registry/")]
    if not reg:
        fail("the commit must change at least one file under infra/logic/registry/")
    bad = [x for x in files if not (x.startswith("infra/logic/registry/") or re.fullmatch(r"lib/tests/test_opal_naming[A-Za-z0-9_]*\.py", x) or x.startswith(DELIV)
                                    or "INVESTIGATION_v1.md" in x or "TO-IB-hm-3a" in x)]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: the naming tests pass, one commit, registry files only (plus an optional naming test)")


def ac3(r):
    s = r.get("secret") or {}
    nm = str(s.get("name", ""))
    if not re.fullmatch(r"irpt/[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*", nm):
        fail("secret.name must be in the slash grammar irpt/<scope>/<purpose>, read %r" % nm)
    rows = load(RES)
    rows = rows if isinstance(rows, list) else (rows.get("resources") or rows.get("rows") or [])
    hit = [x for x in rows if isinstance(x, dict) and x.get("name") == nm and x.get("type") == "SECRET" and x.get("system") == "irpt"]
    if len(hit) != 1:
        fail("resources.json must hold exactly one SECRET row of system irpt named %s (found %d)" % (nm, len(hit)))
    for c in r.get("calls", []):
        if c.get("fn") == "name" and not str(c.get("result", "")).startswith("irpt-"):
            fail("the role and policy names must be irpt names, read %r" % c.get("result"))
    if re.search(r"[A-Za-z0-9+/]{40,}", json.dumps(r)):
        fail("the record holds a long base64-like run (key material?)")
    print("OK: one irpt SECRET row in slash grammar, irpt role and policy names, no key material")


CHECKS = {"IBHM3A-AC1": ac1, "IBHM3A-AC2": ac2, "IBHM3A-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p249_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    cid = sys.argv[2]
    CHECKS[cid](load(REC) if cid != "IBHM3A-AC2" else None)
    print("%s PASS" % cid)
