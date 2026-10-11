"""ADVI_FIRMBKTS round 4 check for cell FB-g-31 (act 4's IRPT leg: the eight consumers' staged `_authz/loaders.py` re-pinned to
the flip commit; COO ADDENDUM 2 of act 4), issuer 2.0.0_SA_COO~B1.

--arms repin --flip <40-hex flip commit> [--root <tree>] [--base <ref>]  (3 arms)
  R1 `infra/aws/lambda/ci/lambda-source-map.json` differs from the base in EXACTLY the `pin` and `sha256` of the one
     `staged_from` row whose `repo_path` is `_authz/loaders.py`, in each of the 8 consumers (16 field changes), nothing else:
     `pin` equals --flip and `sha256` equals the sha256 of `git show <flip>:<repo_path>`.
  R2 `BUILD_ONLY=1 build-and-upload.sh investor-reporting <function>` exits 0 for each of the 8 and prints its
     `BUILD_ONLY:` line with a sha256 (printed; the rehearsal's values are in the act-4 COO ADDENDUM 2).
  R3 each built artifact's `loaders.py` member equals the flip commit's blob byte for byte, and carries the canonical bucket.
Plain ASCII output; the last line carries the arm count. Builds are local; nothing is uploaded. Never edit this file.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

FUNCS = ["irpt-49f-reporting-read-lambda", "irpt-directory-search", "irpt-export-render", "irpt-holdings",
         "irpt-narrative", "irpt-performance-adapter", "irpt-status", "irpt-ycharts-generate"]
LOADERS = "infra/aws/lambda/investor-reporting/_authz/loaders.py"
SM = "infra/aws/lambda/ci/lambda-source-map.json"


def _git(root, *a, raw=False):
    r = subprocess.run(["git", "-C", root] + list(a), capture_output=True)
    return r.stdout if raw else r.stdout.decode("utf-8", "replace")


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def repin(root, flip, base):
    res = []
    old = json.loads(_git(root, "show", "%s:%s" % (base, SM)))
    new = json.load(open(os.path.join(root, *SM.split("/")), encoding="utf-8"))
    blob = _git(root, "show", "%s:%s" % (flip, LOADERS), raw=True)
    want_sha = hashlib.sha256(blob).hexdigest()
    fo, fn = old.get("functions", old), new.get("functions", new)
    changes, ok1 = [], True
    for k in set(fo) | set(fn):
        a, b = fo.get(k), fn.get(k)
        if a == b:
            continue
        if k not in FUNCS or a is None or b is None:
            ok1 = False
            changes.append("%s: outside the eight" % k)
            continue
        ka = {x: v for x, v in a.items() if x != "staged_from"}
        kb = {x: v for x, v in b.items() if x != "staged_from"}
        if ka != kb:
            ok1 = False
            changes.append("%s: non-staged fields differ" % k)
        sa, sb = a.get("staged_from") or [], b.get("staged_from") or []
        if len(sa) != len(sb):
            ok1 = False
            changes.append("%s: staged_from length differs" % k)
            continue
        for ra, rb in zip(sa, sb):
            if ra == rb:
                continue
            same = {x: v for x, v in ra.items() if x not in ("pin", "sha256")} == \
                {x: v for x, v in rb.items() if x not in ("pin", "sha256")}
            if ra.get("repo_path") != LOADERS or not same or rb.get("pin") != flip or rb.get("sha256") != want_sha:
                ok1 = False
                changes.append("%s: row %s not a clean re-pin" % (k, ra.get("repo_path")))
            else:
                changes.append("%s: pin and sha256" % k)
    done = sorted(c.split(":")[0] for c in changes if c.endswith("pin and sha256"))
    ok1 = ok1 and done == sorted(FUNCS) and re.fullmatch(r"[0-9a-f]{40}", flip or "") is not None
    print("  R1 re-pinned rows: %d of 8; violations: %s" % (len(done), [c for c in changes if not c.endswith("sha256")]))
    res.append(("R1 the source map differs only by the eight loaders rows' pin and sha256, to the flip commit", ok1))

    shas, ok2, ok3 = {}, True, True
    for k in FUNCS:
        e = dict(os.environ, BUILD_ONLY="1")
        r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", k], cwd=root,
                           capture_output=True, text=True, timeout=280, env=e)
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("BUILD_ONLY:")]
        if r.returncode or not line:
            ok2 = False
            shas[k] = "FAILED rc=%s" % r.returncode
            ok3 = False
            continue
        zp = line[0].split()[1]
        shas[k] = line[0].split("sha256=")[1].split()[0]
        # the MSYS /tmp maps to the Windows temp dir; read it back through bash
        z = subprocess.run(["bash", "-c", "unzip -p '%s' loaders.py" % zp], capture_output=True)
        if z.returncode or z.stdout != blob or b'"bucket": "opal-data-49financial"' not in z.stdout:
            ok3 = False
    for k, v in shas.items():
        print("  %-34s %s" % (k, v))
    res.append(("R2 all eight builds exit 0 and print a hash", ok2))
    res.append(("R3 each artifact's loaders.py equals the flip commit's blob and carries the canonical bucket", ok3))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("repin",), required=True)
    ap.add_argument("--flip", required=True)
    ap.add_argument("--root")
    ap.add_argument("--base", default="HEAD~1")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = repin(root, a.flip, a.base)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the source map and builds readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 REPIN: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
