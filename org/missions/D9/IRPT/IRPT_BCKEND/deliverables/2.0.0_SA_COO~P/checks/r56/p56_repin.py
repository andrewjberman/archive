"""IRPT_BCKEND round 56 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the approved r55 re-pin set (CTO batch 260 @7bd2946ccd) applied
to lambda-source-map.json staged_from pins, with a BUILD_ONLY census and an import smoke per function.

Usage: python <this file> <repo_root> <criterion_id>
  IB56-1-AC1  every (function, member) in the plan's `proposal[fn].repin` has its staged_from pin moved to the plan's head commit
              (or a later commit whose content of that member equals HEAD's), and every pin NOT in a repin list is unchanged
              from base. Base: FAIL (nothing moved).
  IB56-1-AC2  CENSUS lists every function with a repin; for each, every added/removed/changed member is attributed to IB-pr-317,
              -320, -321 or -322, with `riders` empty. Base: FAIL (no census).
  IB56-1-AC3  CENSUS records an import smoke per function (`import_smoke.modules` > 0 and `import_smoke.import_errors` == []):
              every top-level module of the BUILD_ONLY bundle imports without ImportError. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import subprocess
import sys
from pathlib import Path

BASE = "fc30e2ca85"
PLAN = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/REPIN_PLAN_R55.json"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
CENSUS = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~127/R56_REPIN_CENSUS.json"
ORDERS = ("IB-pr-317", "IB-pr-320", "IB-pr-321", "IB-pr-322")


def _map_at(root, ref):
    if ref == "WORK":
        return json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
    out = subprocess.run(["git", "show", "%s:%s" % (ref, MAP)], cwd=str(root), capture_output=True).stdout
    return json.loads(out.decode("utf-8"))["functions"]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB56-1"))
        sys.exit(1)

    plan = json.loads((root / PLAN).read_bytes().decode("utf-8"))
    prop = plan["proposal"]
    repin = {(fn, m) for fn, v in prop.items() for m in v["repin"]}
    if cid == "IB56-1-AC1":
        base, now = _map_at(root, BASE), _map_at(root, "WORK")
        moved, kept, bad = 0, 0, []
        for fn in prop:
            b = {s["repo_path"]: s for s in base[fn].get("staged_from") or []}
            n = {s["repo_path"]: s for s in now[fn].get("staged_from") or []}
            for path, s in b.items():
                member = path.split("/")[-1]
                if (fn, member) in repin:
                    pin = n.get(path, {}).get("pin", "")
                    same = subprocess.run(["git", "diff", "--quiet", pin, "HEAD", "--", path], cwd=str(root)).returncode == 0
                    if pin == s.get("pin") or not same:
                        bad.append("%s %s not moved to HEAD content (pin %s)" % (fn, member, pin[:10]))
                    else:
                        moved += 1
                elif n.get(path, {}).get("pin") != s.get("pin"):
                    bad.append("%s %s moved but is not in the approved set" % (fn, member))
                else:
                    kept += 1
        if bad:
            fail("; ".join(bad[:6]))
        print("OK: %d pins moved to HEAD content, %d others unchanged" % (moved, kept))
    elif cid in ("IB56-1-AC2", "IB56-1-AC3"):
        p = root / CENSUS
        if not p.is_file():
            fail("no %s" % CENSUS)
        c = json.loads(p.read_bytes().decode("utf-8")).get("functions") or {}
        want = sorted(fn for fn, v in prop.items() if v["repin"])
        missing = [fn for fn in want if fn not in c]
        if missing:
            fail("census lacks %s" % missing)
        for fn in want:
            f = c[fn]
            if cid == "IB56-1-AC2":
                if f.get("riders"):
                    fail("%s riders %s" % (fn, f["riders"][:5]))
                for m in f.get("members") or []:
                    if m.get("status") != "unchanged" and m.get("order") not in ORDERS:
                        fail("%s member %s %s attributed to %r" % (fn, m.get("name"), m.get("status"), m.get("order")))
            else:
                s = f.get("import_smoke") or {}
                if not s.get("modules") or s.get("import_errors"):
                    fail("%s import smoke: modules %r errors %r" % (fn, s.get("modules"), (s.get("import_errors") or [])[:3]))
        print("OK: %d functions %s" % (len(want), "attributed, no riders" if cid == "IB56-1-AC2" else "import clean"))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
