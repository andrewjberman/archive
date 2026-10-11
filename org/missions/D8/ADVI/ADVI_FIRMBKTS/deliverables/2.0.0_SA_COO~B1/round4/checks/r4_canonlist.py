"""ADVI_FIRMBKTS round 4 check for cell FB-g-17 (the router and the validator import the generated canonical-bucket list;
the CTO's round-3 ADDENDA 4 and 7), issuer 2.0.0_SA_COO~B1.

--arms list [--root <tree>]  (4 arms)
  L1 firm-config.mjs exports a frozen CANONICAL_PLATINUM_BUCKETS equal to the destination registry's unique canonical
     buckets (read through the tree's seam), and it names no firm's CURRENT routed bucket (the dormant proof: while the
     routed bucket is a legacy alias no firm is on the canonical layout).
  L2 the router's index.mjs imports CANONICAL_PLATINUM_BUCKETS from ../_shared/firm-config.mjs and no longer defines a
     list of its own (no `Object.freeze([` assignment to that name).
  L3 the validator's ownership_key.mjs imports it from ../../_shared/firm-config.mjs or ../_shared/firm-config.mjs, exports
     it unchanged as its default list, and defines no list of its own.
  L4 the router's own gate (`bash run-gate.sh`, bun) reads at least 51 pass and 0 fail, and the validator's spec reads
     0 fail.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys

FC = "infra/aws/lambda-edge/_shared/firm-config.mjs"
ROUTER = "infra/aws/lambda-edge/shared-advisor-router"
VAL = "infra/aws/lambda-edge/auth-validator-edge"


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _bun(cwd, args, env_extra=None):
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + os.path.join(os.path.expanduser("~"), ".bun", "bin")
    env.pop("FORCE_COLOR", None)
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env, timeout=110)
    return r.returncode, (r.stdout + r.stderr)


def lst(root):
    res = []
    sys.path.insert(0, os.path.join(root, "lib"))
    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    import opal_naming  # noqa: E402
    from lib import platinum_dest as pd  # noqa: E402
    reg = opal_naming._registry()
    rows = [r for r in reg["legacy_addresses"]["legacy_addresses"]
            if str(r.get("key", "")).endswith("-ownership-map") and r.get("shape") == "object"]
    want = sorted({pd.destination(r["template"], "canonical")[0] for r in rows})
    url = json.dumps("file:///" + os.path.join(root, *FC.split("/")).replace("\\", "/").lstrip("/"))
    rc, out = _bun(root, ["bun", "-e", "import * as m from %s; console.log(JSON.stringify({l:m.CANONICAL_PLATINUM_BUCKETS||null,"
                         "f:!!m.CANONICAL_PLATINUM_BUCKETS&&Object.isFrozen(m.CANONICAL_PLATINUM_BUCKETS),"
                         "b:Object.values(m.FIRM_CONFIG).map(x=>x.bucket)})) " % url])
    try:
        d = json.loads(out.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        d = {}
    got = sorted(d.get("l") or [])
    ok1 = rc == 0 and bool(want) and got == want and d.get("f") is True and not (set(got) & set(d.get("b") or []))
    print("  generated list=%s expected=%s frozen=%s routed buckets=%s" % (got, want, d.get("f"),
                                                                          sorted(set(d.get("b") or []))))
    res.append(("L1 firm-config.mjs exports the frozen canonical-bucket list equal to the destinations, naming no firm's "
                "current routed bucket", ok1))

    rsrc = open(os.path.join(root, *(ROUTER + "/index.mjs").split("/")), encoding="utf-8").read()
    code = "\n".join(ln for ln in rsrc.splitlines() if not ln.lstrip().startswith(("//", "*", "/*")))
    imp = re.search(r"import\s*\{[^}]*CANONICAL_PLATINUM_BUCKETS[^}]*\}\s*from\s*[\"']\.\./_shared/firm-config\.mjs[\"']", code)
    own = re.search(r"CANONICAL_PLATINUM_BUCKETS\s*=\s*Object\.freeze\(\s*\[", code)
    print("  router imports the list=%s, defines its own=%s" % (bool(imp), bool(own)))
    res.append(("L2 the router imports the generated list and defines none of its own", bool(imp) and not own))

    vsrc = open(os.path.join(root, *(VAL + "/ownership_key.mjs").split("/")), encoding="utf-8").read()
    vcode = "\n".join(ln for ln in vsrc.splitlines() if not ln.lstrip().startswith(("//", "*", "/*")))
    vimp = re.search(r"import\s*\{[^}]*CANONICAL_PLATINUM_BUCKETS[^}]*\}\s*from\s*[\"'](\.\./)+_shared/firm-config\.mjs[\"']",
                     vcode)
    vown = re.search(r"CANONICAL_PLATINUM_BUCKETS\s*=\s*Object\.freeze\(\s*\[", vcode)
    print("  validator helper imports the list=%s, defines its own=%s" % (bool(vimp), bool(vown)))
    res.append(("L3 the validator's helper imports the generated list and defines none of its own", bool(vimp) and not vown))

    rc1, out1 = _bun(os.path.join(root, *ROUTER.split("/")), ["bash", "run-gate.sh"])
    m = re.search(r"(\d+) pass", out1)
    f = re.search(r"(\d+) fail", out1)
    npass, nfail = int(m.group(1)) if m else -1, int(f.group(1)) if f else -1
    rc2, out2 = _bun(os.path.join(root, *VAL.split("/")), ["bun", "test", "tests/ownership_key.spec.mjs"])
    f2 = re.search(r"(\d+) fail", out2)
    print("  router gate: %d pass, %d fail (rc %d); validator spec fail=%s" % (npass, nfail, rc1,
                                                                              f2.group(1) if f2 else "?"))
    res.append(("L4 the router's gate reads at least 51 pass and 0 fail, and the validator's spec 0 fail",
                rc1 == 0 and npass >= 51 and nfail == 0 and rc2 == 0 and f2 is not None and f2.group(1) == "0"))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("list",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = lst(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the router, the validator and the generated view readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 CANONICAL LIST: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
