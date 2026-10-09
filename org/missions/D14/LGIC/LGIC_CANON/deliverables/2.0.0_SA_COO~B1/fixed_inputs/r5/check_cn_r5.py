"""LGIC_CANON round 5 -- the issuer's fixed checks (2.0.0_SA_COO~B1). Run from the worktree root: python <this file> <arm>.
Each arm prints one PASS-*/FAIL-* verdict line last; exit 0 only on PASS.

  step13   CN-q-1  every name of the practice wave's contract (workflows/legacy_transform/blackdiamond-49financial/
                   20260918T011619Z-8db9eb1/contract.json, 184 rows) goes through `lib/opal_naming.py census --names` with NO
                   --not-judged file: the run COMPLETES (rc 0), 0 RAISE. A name that read RAISE on 2026-09-18 clears by reading
                   RULED (a name_rulings.json row) or by a verdict -- never by a card.
  paths    CN-q-2  `python lib/opal_portal_paths.py 49financial` derives the firm's portal paths from its scope row with no
                   prompt; its JSON (`--json`) lists `derived` and `carded`; derived + carded == the paths
                   portal/src/lib/firmAccess.ts FIRM_ALLOWED_PATHS['49financial'] carries today (the dashboard as before), every
                   carded path has an owner and a reason, and a firm with no scope row exits non-zero (never a default).
  run      CN-q-3  CANON_RUN_R5.json: reached + carded == 16 steps, step 13 and step 14a REACHED, every carded step's cause is
                   a firm-bucket one (steps 10, 14b, 16 only), the dashboard routes hash unchanged, live_acts == [].
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
CONTRACT = "workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/contract.json"
FIRM_ACCESS = "portal/src/lib/firmAccess.ts"
RUN_RECORD = "org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~1/CANON_RUN_R5.json"
FIRM_BUCKET_STEPS = {"10", "14b", "16"}


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def run(args, timeout=900):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout)
    return p.returncode, ((p.stdout or b"") + (p.stderr or b"")).decode("utf-8", "replace").replace("\r\n", "\n")


def contract_names():
    rows = json.load(open(os.path.join(ROOT, CONTRACT), encoding="utf-8"))["rows"]
    out = []
    for r in rows:
        nm = ((r.get("current") or {}).get("name") or {}).get("value")
        if nm:
            out.append((r["node_type"], nm))
    return out


def arm_step13():
    names = contract_names()
    need(names, "no names read from %s" % CONTRACT)
    tmp = tempfile.mkdtemp(prefix="cn-r5-")
    path = os.path.join(tmp, "wave_names.tsv")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for t, n in names:
            fh.write("%s\t%s\n" % (t, n))
    rc, out = run([sys.executable, "lib/opal_naming.py", "census", "--names", path])
    last = (out.strip().splitlines() or [""])[-1]
    raises = re.findall(r"^CENSUS RAISE .*$", out, re.M)
    ruled = len(re.findall(r"^CENSUS RULED ", out, re.M))
    print("wave names=%d rc=%d ruled=%d raise=%d last=%r" % (len(names), rc, ruled, len(raises), last[:160]))
    for r in raises[:3]:
        print("  " + r[:200])
    need(rc == 0 and not raises and last.startswith("CENSUS: COMPLETE"), "step 13 does not read 0 unresolved on the wave's names")
    return "PASS-R5-STEP13"


def allowed_today():
    src = open(os.path.join(ROOT, FIRM_ACCESS), encoding="utf-8").read()
    m = re.search(r"'49financial':\s*new Set\(\[(.*?)\]\)", src, re.S)
    need(m is not None, "FIRM_ALLOWED_PATHS['49financial'] not found in %s" % FIRM_ACCESS)
    return sorted(re.findall(r"'([^']+)'", m.group(1)))


def arm_paths():
    need(os.path.isfile(os.path.join(ROOT, "lib/opal_portal_paths.py")), "lib/opal_portal_paths.py absent")
    rc, out = run([sys.executable, "lib/opal_portal_paths.py", "49financial", "--json"], timeout=120)
    need(rc == 0, "the derivation exited %d for 49financial: %s" % (rc, out[-300:]))
    doc = json.loads(out[out.index("{"):])
    derived = sorted(doc.get("derived") or [])
    carded = doc.get("carded") or []
    want = allowed_today()
    got = sorted(set(derived) | set(c.get("path") for c in carded))
    print("today=%d derived=%d carded=%d" % (len(want), len(derived), len(carded)))
    need(got == want, "derived + carded != FIRM_ALLOWED_PATHS['49financial'] (missing %s, extra %s)"
         % (sorted(set(want) - set(got)), sorted(set(got) - set(want))))
    need(not (set(derived) & set(c.get("path") for c in carded)), "a path is both derived and carded")
    for c in carded:
        need(str(c.get("owner") or "").strip() and str(c.get("reason") or "").strip(), "carded path %r lacks owner or reason" % c)
    rc, out = run([sys.executable, "lib/opal_portal_paths.py", "zz-no-such-firm-r5", "--json"], timeout=120)
    need(rc != 0, "a firm with no scope row did not fail (rc=0): the derivation defaulted")
    return "PASS-R5-PATHS"


def arm_run():
    rec = json.load(open(os.path.join(ROOT, RUN_RECORD), encoding="utf-8"))
    reached = [str(s.get("step")) for s in rec.get("reached", [])]
    carded = rec.get("carded", [])
    steps = int(rec.get("steps") or 0)
    print("steps=%d reached=%d carded=%d" % (steps, len(reached), len(carded)))
    need(steps == 16 and len(reached) + len(carded) == steps, "reached + carded != 16")
    need("13" in reached and "14a" in reached, "step 13 and step 14a are not both REACHED")
    bad = [c for c in carded if str(c.get("step")) not in FIRM_BUCKET_STEPS]
    need(not bad, "carded steps outside the firm-bucket set: %s" % [c.get("step") for c in bad])
    for c in carded:
        need(str(c.get("owner") or "").strip(), "carded step %s has no owner" % c.get("step"))
    sv = rec.get("served") or {}
    need(sv.get("before") and sv.get("before") == sv.get("after"), "the dashboard routes hash moved (or was not read)")
    need(rec.get("live_acts") == [], "live_acts is not []")
    return "PASS-R5-RUN"


ARMS = {"step13": arm_step13, "paths": arm_paths, "run": arm_run}


def main():
    arm = (sys.argv[1:] or [""])[0]
    if arm not in ARMS:
        print("usage: check_cn_r5.py {%s}" % ",".join(sorted(ARMS)))
        return 2
    try:
        verdict = ARMS[arm]()
    except Fail as exc:
        print("FAIL-R5-%s: %s" % (arm.upper(), exc))
        return 1
    except (OSError, ValueError, KeyError) as exc:
        print("FAIL-R5-%s: %s: %s" % (arm.upper(), type(exc).__name__, exc))
        return 1
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
