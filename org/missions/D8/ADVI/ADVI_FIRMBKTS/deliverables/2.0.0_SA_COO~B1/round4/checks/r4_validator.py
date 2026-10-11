"""ADVI_FIRMBKTS round 4 check for cell FB-g-1 (auth-validator-edge's canonical ownership-map key, DORMANT), issuer
2.0.0_SA_COO~B1.

--arms key [--root <tree>]  grades the validator's key helper in <tree> (4 arms):
  K1 the helper file exists, exports a frozen EMPTY CANONICAL_PLATINUM_BUCKETS and ownershipMapKey(firmId, bucket, canonical).
  K2 DORMANT: with the shipped (empty) list every firm and bucket reads the legacy key `platinum/<firm>/ownership_map.json`.
  K3 ENGAGED: with the firm's own bucket named in the list, the key equals the producers' seam's canonical destination key
     for `platinum/<firm>/ownership_map.json` (lib/platinum_dest.py destination(), canonical mode) -- read from the
     CHECKOUT's seam, never typed here; a bucket not named stays legacy.
  K4 index.mjs builds the key through the helper and no longer carries the literal key template in code.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys

VAL = "infra/aws/lambda-edge/auth-validator-edge"
FIRMS = ("49financial", "inflection", "cottonwood")


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _bun(root, code):
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + os.path.join(os.path.expanduser("~"), ".bun", "bin")
    r = subprocess.run(["bun", "-e", code], capture_output=True, text=True, cwd=root, env=env, timeout=100)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def key(root):
    helper = os.path.join(root, VAL, "ownership_key.mjs")
    res = []
    spec = "file:///" + helper.replace("\\", "/").lstrip("/")
    ok1 = os.path.isfile(helper)
    exports = ""
    if ok1:
        rc, out, err = _bun(root, "import * as m from %s; console.log(JSON.stringify({names:Object.keys(m).sort(),"
                                  "frozen:Object.isFrozen(m.CANONICAL_PLATINUM_BUCKETS),"
                                  "len:m.CANONICAL_PLATINUM_BUCKETS.length}))" % json.dumps(spec))
        try:
            d = json.loads(out)
            ok1 = (rc == 0 and "ownershipMapKey" in d["names"] and d["frozen"] is True and d["len"] == 0)
            exports = out
        except Exception:  # noqa: BLE001
            ok1 = False
            exports = "unreadable: " + (err or out)[:120]
    print("  helper exports: %s" % exports)
    res.append(("K1 ownership_key.mjs exports a frozen empty CANONICAL_PLATINUM_BUCKETS and ownershipMapKey", ok1))
    if not ok1:
        res += [("K2 dormant: the shipped list keeps the legacy key for every firm and bucket", False),
                ("K3 engaged: a named bucket reads the seam's canonical key and an unnamed one stays legacy", False),
                ("K4 index.mjs builds the key through the helper, with no key literal left in code", False)]
        return res
    code = ("import {ownershipMapKey} from %s; const o={};"
            "for (const f of %s) { o[f]=[ownershipMapKey(f,'opal-data-bd'),ownershipMapKey(f,'opal-data-'+f),"
            "ownershipMapKey(f,undefined)]; } console.log(JSON.stringify(o))"
            % (json.dumps(spec), json.dumps(list(FIRMS))))
    rc, out, err = _bun(root, code)
    try:
        got = json.loads(out)
        legacy = all(v == ["platinum/%s/ownership_map.json" % f] * 3 for f, v in got.items())
    except Exception:  # noqa: BLE001
        got, legacy = {}, False
    print("  dormant keys: %s" % json.dumps(got)[:200])
    res.append(("K2 dormant: the shipped list keeps the legacy key for every firm and bucket", rc == 0 and legacy))

    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    from lib import platinum_dest as pd  # noqa: E402
    want = {}
    for f in FIRMS:
        try:
            want[f] = pd.destination("platinum/%s/ownership_map.json" % f, "canonical")[1]
        except Exception as e:  # noqa: BLE001
            want[f] = "ERR:" + type(e).__name__
    code = ("import {ownershipMapKey} from %s; const o={};"
            "for (const f of %s) { o[f]=[ownershipMapKey(f,'opal-data-'+f,['opal-data-'+f]),"
            "ownershipMapKey(f,'opal-data-bd',['opal-data-'+f])]; } console.log(JSON.stringify(o))"
            % (json.dumps(spec), json.dumps(list(FIRMS))))
    rc, out, err = _bun(root, code)
    try:
        eng = json.loads(out)
    except Exception:  # noqa: BLE001
        eng = {}
    # the seam registers the 49financial class only; for the others the seam is the identity (legacy key), so the
    # helper must agree with the seam firm by firm, whichever it is
    agree = bool(eng) and all(eng[f][0] == want[f] and eng[f][1] == "platinum/%s/ownership_map.json" % f for f in FIRMS)
    print("  seam canonical keys: %s" % json.dumps(want)[:220])
    print("  engaged keys:        %s" % json.dumps(eng)[:220])
    res.append(("K3 engaged: a named bucket reads the seam's canonical key and an unnamed one stays legacy",
                rc == 0 and agree))

    src = open(os.path.join(root, VAL, "index.mjs"), encoding="utf-8").read()
    code_only = "\n".join(ln for ln in src.splitlines() if not ln.lstrip().startswith(("//", "*", "/*")))
    uses = re.search(r"ownershipMapKey\s*\(", code_only) is not None and "./ownership_key.mjs" in code_only
    literal = re.search(r"`platinum/\$\{[^}]*\}/ownership_map\.json`", code_only) is not None
    print("  index.mjs uses the helper=%s, key literal left in code=%s" % (uses, literal))
    res.append(("K4 index.mjs builds the key through the helper, with no key literal left in code", uses and not literal))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("key",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = key(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (VAL, type(e).__name__, str(e)[:160]))
        res = [("the validator's key helper present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 VALIDATOR KEY: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
