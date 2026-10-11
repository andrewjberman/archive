"""ADVI_FIRMBKTS round 4 check for cell FB-g-1 (auth-validator-edge reads the ownership map at the key the generated
OWNERSHIP_KEYS block names, DORMANT), issuer 2.0.0_SA_COO~B1. Amended after the CTO's round-3 ADDENDUM 4: the key
templates are no longer typed in the validator; they come from `_shared/firm-config.mjs` (cell FB-g-12).

--arms key [--root <tree>]  grades the validator's key helper in <tree> (4 arms):
  K1 ownership_key.mjs exists, imports OWNERSHIP_KEYS from ../_shared/firm-config.mjs, and exports a frozen EMPTY
     CANONICAL_PLATINUM_BUCKETS and ownershipMapKey(firmId, bucket, canonical, keys).
  K2 DORMANT: with the shipped (empty) list, every firm OWNERSHIP_KEYS lists reads its `legacy` key for its own bucket,
     another bucket and no bucket; a firm it does not list (every other FIRM_CONFIG firm included) throws, and the call
     site fails closed on the throw as it did on the 404 of a key no producer wrote.
  K3 ENGAGED: with a firm's own routed bucket named in the list, the key equals the producers' seam's canonical
     destination key for that firm's legacy key (read from the CHECKOUT's lib/platinum_dest.py, never typed here); a
     bucket not named stays legacy.
  K4 index.mjs builds the key through the helper, and no `platinum/${...}/ownership_map.json` literal is left in code.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys

VAL = "infra/aws/lambda-edge/auth-validator-edge"
FC = "infra/aws/lambda-edge/_shared/firm-config.mjs"


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _bun(root, code):
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + os.path.join(os.path.expanduser("~"), ".bun", "bin")
    r = subprocess.run(["bun", "-e", code], capture_output=True, text=True, cwd=root, env=env, timeout=100)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def _url(root, rel):
    return json.dumps("file:///" + os.path.join(root, *rel.split("/")).replace("\\", "/").lstrip("/"))


def key(root):
    helper_rel = VAL + "/ownership_key.mjs"
    helper = os.path.join(root, *helper_rel.split("/"))
    res = []
    ok1, shown = False, ""
    if os.path.isfile(helper):
        src = open(helper, encoding="utf-8").read()
        imports = re.search(r"import\s*\{[^}]*OWNERSHIP_KEYS[^}]*\}\s*from\s*[\"']\.\./_shared/firm-config\.mjs[\"']", src)
        rc, out, err = _bun(root, "import * as m from %s; console.log(JSON.stringify({names:Object.keys(m).sort(),"
                                  "frozen:Object.isFrozen(m.CANONICAL_PLATINUM_BUCKETS),"
                                  "len:m.CANONICAL_PLATINUM_BUCKETS.length}))" % _url(root, helper_rel))
        try:
            d = json.loads(out)
            ok1 = rc == 0 and bool(imports) and "ownershipMapKey" in d["names"] and d["frozen"] is True
            shown = out
        except Exception:  # noqa: BLE001
            shown = "unreadable: " + (err or out)[:120]
    print("  helper exports: %s" % shown)
    res.append(("K1 ownership_key.mjs imports OWNERSHIP_KEYS and exports a frozen empty CANONICAL_PLATINUM_BUCKETS "
                "and ownershipMapKey", ok1))
    if not ok1:
        return res + [("K2 dormant: the shipped list reads each firm's legacy key", False),
                      ("K3 engaged: a named bucket reads the seam's canonical key", False),
                      ("K4 index.mjs builds the key through the helper, with no key literal left in code", False)]

    code = ("import {ownershipMapKey} from %s; import {FIRM_CONFIG, OWNERSHIP_KEYS} from %s; const o={};"
            "for (const f of Object.keys(OWNERSHIP_KEYS)) { o[f]={legacy:OWNERSHIP_KEYS[f].legacy,"
            "got:[ownershipMapKey(f,FIRM_CONFIG[f].bucket),ownershipMapKey(f,'x-other-bucket'),ownershipMapKey(f,undefined)]}; }"
            "const unlisted=Object.keys(FIRM_CONFIG).filter(f=>!(f in OWNERSHIP_KEYS)).concat(['no-such-firm-xyz']);"
            "let threw=unlisted.length>0; for (const f of unlisted) { try { ownershipMapKey(f,'b'); threw=false; } catch(e) {} }"
            "console.log(JSON.stringify({o,threw,unlisted:unlisted.length}))" % (_url(root, helper_rel), _url(root, FC)))
    rc, out, err = _bun(root, code)
    try:
        d = json.loads(out)
        legacy_ok = bool(d["o"]) and all(v["got"] == [v["legacy"]] * 3 for v in d["o"].values()) and d["threw"] is True
    except Exception:  # noqa: BLE001
        d, legacy_ok = {}, False
    print("  dormant: %d listed firms, %s unlisted firms all throw=%s" % (len(d.get("o", {})), d.get("unlisted"),
                                                                           d.get("threw")))
    res.append(("K2 dormant: the shipped list reads each firm's legacy key and an unknown firm throws",
                rc == 0 and legacy_ok))

    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    from lib import platinum_dest as pd  # noqa: E402
    code = ("import {ownershipMapKey} from %s; import {FIRM_CONFIG, OWNERSHIP_KEYS} from %s; const o={};"
            "for (const f of Object.keys(OWNERSHIP_KEYS)) { const b=FIRM_CONFIG[f].bucket; o[f]={legacy:OWNERSHIP_KEYS[f].legacy,"
            "named:ownershipMapKey(f,b,[b]),unnamed:ownershipMapKey(f,b,['x-other-bucket'])}; }"
            "console.log(JSON.stringify(o))" % (_url(root, helper_rel), _url(root, FC)))
    rc, out, err = _bun(root, code)
    try:
        eng = json.loads(out)
    except Exception:  # noqa: BLE001
        eng = {}
    want = {}
    for f, v in eng.items():
        try:
            want[f] = pd.destination(v["legacy"], "canonical")[1]
        except Exception as e:  # noqa: BLE001
            want[f] = "ERR:" + type(e).__name__
    agree = bool(eng) and all(v["named"] == want[f] and v["unnamed"] == v["legacy"] for f, v in eng.items())
    moved = [f for f, v in eng.items() if v["named"] != v["legacy"]]
    print("  engaged: firms=%d, firms whose key moves=%s" % (len(eng), moved))
    res.append(("K3 engaged: a named bucket reads the seam's canonical key and an unnamed one stays legacy",
                rc == 0 and agree and bool(moved)))

    src = open(os.path.join(root, *(VAL + "/index.mjs").split("/")), encoding="utf-8").read()
    code_only = "\n".join(ln for ln in src.splitlines() if not ln.lstrip().startswith(("//", "*", "/*")))
    uses = re.search(r"ownershipMapKey\s*\(", code_only) is not None and "./ownership_key.mjs" in code_only
    literal = re.search(r"platinum/\$\{[^}]*\}/ownership_map\.json", code_only) is not None
    print("  index.mjs uses the helper=%s, key literal left in code=%s" % (uses, literal))
    res.append(("K4 index.mjs builds the key through the helper, with no key literal left in code",
                uses and not literal))
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
