"""IRPT_BCKEND round 60 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the r58 re-pin: for the four functions this seat releases, the
served.py and loaders.py members of lambda-source-map.json `staged_from` point at the merged blobs.

Usage: python <this file> <repo_root> <criterion_id>
  IB60-1-AC1  for each of irpt-49f-reporting-read-lambda, irpt-export-render, irpt-directory-search, irpt-holdings, the `_authz/served.py`
              and `_authz/loaders.py` members carry pin = the full 40-hex PIN below and sha256 = sha256 of `git show <pin>:<path>`
              (recomputed here, never trusted from the file); no other function's row and no other member of these four rows changed
              against BASE. Base: FAIL.
  IB60-1-AC2  a GUARD: the worker's own commits touch only lambda-source-map.json, its deliverables, the channel and its order. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PIN = "d8d8e7d868bc3a784afe5c87e6ad19743c0c53ac"
BASE = "01e4518df8"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
AUTHZ = "infra/aws/lambda/investor-reporting/_authz/"
FUNCS = ("irpt-49f-reporting-read-lambda", "irpt-export-render", "irpt-directory-search", "irpt-holdings")
MEMBERS = (AUTHZ + "served.py", AUTHZ + "loaders.py")
AUTHOR = "0.9.0_WK_IRPT_BCKEND~131"
GRANT = (MAP, "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~131/",
         "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-328.")


def git(root, *args):
    r = subprocess.run(["git", *args], cwd=str(root), capture_output=True)
    return r.returncode, r.stdout


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB60-1"))
        sys.exit(1)

    if cid == "IB60-1-AC1":
        cur = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]
        rc, raw = git(root, "show", "%s:%s" % (BASE, MAP))
        if rc:
            fail("cannot read the base map at %s" % BASE)
        base = json.loads(raw.decode("utf-8"))["functions"]
        for fn in FUNCS:
            members = {m["repo_path"]: m for m in cur[fn]["staged_from"]}
            for path in MEMBERS:
                m = members.get(path)
                if m is None:
                    fail("%s has no member %s" % (fn, path))
                rc, blob = git(root, "show", "%s:%s" % (PIN, path))
                if rc:
                    fail("cannot read %s at the pin" % path)
                want = hashlib.sha256(blob).hexdigest()
                if m.get("pin") != PIN or m.get("sha256") != want:
                    fail("%s %s: pin %s sha256 %s, want pin %s sha256 %s" % (
                        fn, path.rsplit("/", 1)[-1], str(m.get("pin"))[:10], str(m.get("sha256"))[:12], PIN[:10], want[:12]))
        changed = []
        for name in sorted(set(cur) | set(base)):
            if name not in FUNCS:
                if cur.get(name) != base.get(name):
                    changed.append(name)
                continue
            b = {m["repo_path"]: m for m in base[name]["staged_from"]}
            c = {m["repo_path"]: m for m in cur[name]["staged_from"]}
            if set(b) != set(c) or any(b[p] != c[p] for p in b if p not in MEMBERS):
                changed.append(name + " (members other than served.py/loaders.py)")
            rest_b = {k: v for k, v in base[name].items() if k != "staged_from"}
            rest_c = {k: v for k, v in cur[name].items() if k != "staged_from"}
            if rest_b != rest_c:
                changed.append(name + " (fields outside staged_from)")
        if changed:
            fail("unexpected changes: %s" % changed[:6])
        print("OK: 4 functions x 2 members at pin %s with recomputed sha256; nothing else changed" % PIN[:10])
    elif cid == "IB60-1-AC2":
        rc, out = git(root, "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format=")
        changed = sorted(set(ln for ln in out.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
