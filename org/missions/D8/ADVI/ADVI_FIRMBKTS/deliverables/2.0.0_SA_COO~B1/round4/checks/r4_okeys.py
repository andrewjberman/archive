"""ADVI_FIRMBKTS round 4 check for cell FB-g-12 (the builder renders the per-firm OWNERSHIP-KEY block into
infra/aws/lambda-edge/_shared/firm-config.mjs; the CTO's round-3 ADDENDUM 4), issuer 2.0.0_SA_COO~B1.

--arms block [--root <tree>] [--base <ref>]  (5 arms)
  O1 firm-config.mjs exports a frozen OWNERSHIP_KEYS with exactly one entry per FIRM_CONFIG firmId, each carrying string
     `legacy` and `canonical`.
  O2 every `legacy` is `platinum/<firmId>/ownership_map.json`, and for 49financial it equals the template of the registered
     legacy address `blackdiamond-platinum-49financial-ownership-map` (read from the tree's builder, never typed here).
  O3 every `canonical` equals the producers' seam's canonical destination key for that legacy key (read from the tree's
     lib/platinum_dest.py): the ownership class of 49financial is placed, every other firm is the identity.
  O4 DORMANT: against the base, firm-config.mjs differs only by the added block (every base line is still present, in
     order, and the added lines are all inside `OWNERSHIP_KEYS`).
  O5 the committed file is what the tree's builder generates, and `lib/opal_naming.py validate` exits 0.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

FC = "infra/aws/lambda-edge/_shared/firm-config.mjs"
LEGACY_KEY = "blackdiamond-platinum-49financial-ownership-map"


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _base(root, arg):
    if arg:
        return arg
    wl = _git(root, "worktree", "list", "--porcelain").stdout.split("\n")
    primary = next((ln.split()[1] for ln in wl if ln.startswith("HEAD ")), "")
    return _git(root, "merge-base", "HEAD", primary).stdout.strip()


def _bun(root, code):
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + os.path.join(os.path.expanduser("~"), ".bun", "bin")
    r = subprocess.run(["bun", "-e", code], capture_output=True, text=True, cwd=root, env=env, timeout=100)
    return r.returncode, r.stdout.strip()


def block(root, base):
    res = []
    spec = "file:///" + os.path.join(root, *FC.split("/")).replace("\\", "/").lstrip("/")
    rc, out = _bun(root, "import * as m from %s; console.log(JSON.stringify({keys:m.OWNERSHIP_KEYS?m.OWNERSHIP_KEYS:null,"
                         "frozen:!!m.OWNERSHIP_KEYS&&Object.isFrozen(m.OWNERSHIP_KEYS),firms:Object.keys(m.FIRM_CONFIG)}))"
                  % json.dumps(spec))
    try:
        d = json.loads(out)
    except Exception:  # noqa: BLE001
        d = {}
    keys, firms = d.get("keys") or {}, d.get("firms") or []
    ok1 = rc == 0 and bool(keys) and d.get("frozen") is True and sorted(keys) == sorted(firms) and all(
        isinstance(v, dict) and isinstance(v.get("legacy"), str) and isinstance(v.get("canonical"), str)
        for v in keys.values())
    print("  OWNERSHIP_KEYS entries=%d FIRM_CONFIG firms=%d frozen=%s" % (len(keys), len(firms), d.get("frozen")))
    res.append(("O1 firm-config.mjs exports a frozen OWNERSHIP_KEYS with one legacy/canonical entry per firmId", ok1))

    sys.path.insert(0, os.path.join(root, "lib"))
    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    import opal_naming  # noqa: E402
    from lib import platinum_dest as pd  # noqa: E402
    try:
        reg_tmpl = [r for r in opal_naming._registry()["legacy_addresses"]["legacy_addresses"]
                    if r["key"] == LEGACY_KEY][0]["template"]
    except Exception:  # noqa: BLE001
        reg_tmpl = None
    ok2 = ok1 and all(v["legacy"] == "platinum/%s/ownership_map.json" % f for f, v in keys.items()) \
        and keys.get("49financial", {}).get("legacy") == reg_tmpl
    print("  registered legacy template=%r; legacy keys=%s" % (reg_tmpl, sorted({v["legacy"] for v in keys.values()})[:4]))
    res.append(("O2 every legacy key is the platinum/<firm>/ownership_map.json shape and 49financial's equals the "
                "registered legacy address", ok2))

    want = {}
    for f, v in keys.items():
        try:
            want[f] = pd.destination(v["legacy"], "canonical")[1]
        except Exception as e:  # noqa: BLE001
            want[f] = "ERR:" + type(e).__name__
    ok3 = ok1 and all(v["canonical"] == want[f] for f, v in keys.items()) and \
        keys.get("49financial", {}).get("canonical") != keys.get("49financial", {}).get("legacy")
    print("  canonical equals the seam's: %s" % {f: (v["canonical"] == want[f]) for f, v in keys.items()})
    res.append(("O3 every canonical key equals the producers' seam's canonical destination (49financial placed, "
                "the others identity)", ok3))

    old = _git(root, "show", "%s:%s" % (base, FC)).stdout.splitlines()
    cur_lines = open(os.path.join(root, *FC.split("/")), encoding="utf-8").read().splitlines()
    # the block region: from the line that opens [OWNERSHIP_KEYS] to the line that ends it
    lo = next((k for k, ln in enumerate(cur_lines) if "GENERATED" in ln and "[OWNERSHIP_KEYS]" in ln
               and "END" not in ln), None)
    hi = next((k for k, ln in enumerate(cur_lines) if "END GENERATED [OWNERSHIP_KEYS]" in ln), None)
    # a mark line (the registry hash and file list) may differ: the block reads more registry files than FIRM_CONFIG
    old = [ln for ln in old if "GENERATED by lib/opal_naming.py" not in ln]
    i, outside = 0, 0
    for k, ln in enumerate(cur_lines):
        in_block = lo is not None and hi is not None and lo <= k <= hi
        if "GENERATED by lib/opal_naming.py" in ln:
            continue
        if i < len(old) and ln == old[i] and not in_block:
            i += 1
        elif not in_block:
            outside += 1
    dormant = lo is not None and hi is not None and i == len(old) and outside == 0
    print("  base lines kept in order %d of %d; lines outside the block that are not the base's: %d (block at %s-%s)"
          % (i, len(old), outside, lo, hi))
    res.append(("O4 dormant: the base's lines are all kept in order and the only additions are the OWNERSHIP_KEYS block",
                dormant))

    code = ("import sys; sys.path.insert(0,'lib'); import opal_naming as n; n.generate(sys.argv[1], "
            "['%s']); print('done')" % FC)
    with tempfile.TemporaryDirectory() as td:
        g = subprocess.run([sys.executable, "-c", code, td], cwd=root, capture_output=True, text=True, timeout=120)
        gen_p = os.path.join(td, *FC.split("/"))
        gen = open(gen_p, encoding="utf-8").read() if os.path.isfile(gen_p) else None
    cur = open(os.path.join(root, *FC.split("/")), encoding="utf-8").read()
    v = subprocess.run([sys.executable, "lib/opal_naming.py", "validate"], cwd=root, capture_output=True, text=True,
                       timeout=100)
    print("  generate rc=%d in sync=%s; validate rc=%d" % (g.returncode, gen == cur, v.returncode))
    res.append(("O5 the committed file is the builder's output and validate exits 0",
                g.returncode == 0 and gen == cur and v.returncode == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("block",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = block(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (FC, type(e).__name__, str(e)[:160]))
        res = [("firm-config.mjs readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 OWNERSHIP KEYS: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
