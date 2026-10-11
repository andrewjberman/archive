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


def is_plant(r):
    """AMENDMENT 1 (CN-q-1): the wave's own planted rows (fictional by construction) are not estate names; the contract
    marks each by its name's evidence instrument starting with 'planted'."""
    ev = (((r.get("current") or {}).get("name") or {}).get("evidence") or {})
    return str(ev.get("instrument") or "").startswith("planted")


def contract_names():
    rows = json.load(open(os.path.join(ROOT, CONTRACT), encoding="utf-8"))["rows"]
    out, plants = [], []
    for r in rows:
        nm = ((r.get("current") or {}).get("name") or {}).get("value")
        if not nm:
            continue
        (plants if is_plant(r) else out).append((r["node_type"], nm))
    print("wave rows=%d planted excluded=%d %s" % (len(rows), len(plants), [n for _t, n in plants]))
    return out, plants


def arm_step13():
    names, plants = contract_names()
    need(names, "no names read from %s" % CONTRACT)
    rul = json.load(open(os.path.join(ROOT, "infra/logic/registry/name_rulings.json"), encoding="utf-8"))["name_rulings"]
    planted_rows = [r["name"] for r in rul if (r.get("type"), r.get("name")) in set(plants)]
    need(not planted_rows, "name_rulings.json carries a row for a planted fictional name: %s" % planted_rows)
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
    # AMENDMENT 2 (CN-q-3, row LGIC_CANON-D1-W1-S32): the order splits step 14 into 14a and 14b, so the 16 checklist steps are 17
    # units; the units must be exactly {1..13, 14a, 14b, 15, 16}, each once, reached or carded.
    units = [str(n) for n in range(1, 14)] + ["14a", "14b", "15", "16"]
    got = reached + [str(c.get("step")) for c in carded]
    print("steps=%d units=%d reached=%d carded=%d" % (steps, len(units), len(reached), len(carded)))
    need(steps == 16 and sorted(got) == sorted(units), "reached + carded != the 17 units {1..13,14a,14b,15,16} (missing %s, extra %s)"
         % (sorted(set(units) - set(got)), sorted(set(got) - set(units))))
    need("13" in reached and "14a" in reached, "step 13 and step 14a are not both REACHED")
    bad = [c for c in carded if str(c.get("step")) not in FIRM_BUCKET_STEPS]
    need(not bad, "carded steps outside the firm-bucket set: %s" % [c.get("step") for c in bad])
    for c in carded:
        need(str(c.get("owner") or "").strip(), "carded step %s has no owner" % c.get("step"))
    sv = rec.get("served") or {}
    need(sv.get("before") and sv.get("before") == sv.get("after"), "the dashboard routes hash moved (or was not read)")
    need(rec.get("live_acts") == [], "live_acts is not []")
    return "PASS-R5-RUN"


CORE = sorted(["/advisor-intelligence", "/macro", "/market", "/philosophy", "/portfolios", "/positioning", "/valuations"])


def arm_paths2():
    """CN-q-4 (ADDENDUM 1): the 7-page core derived for a client firm with the portal on, plus the firm's registry field
    tenant.pages; 49financial derives exactly its FIRM_ALLOWED_PATHS entry with 0 carded; `--check` passes on the live map and
    STOPs (non-zero) when the map grants a page the registry does not hold."""
    rc, out = run([sys.executable, "lib/opal_portal_paths.py", "49financial", "--json"], timeout=120)
    need(rc == 0, "the derivation exited %d for 49financial: %s" % (rc, out[-300:]))
    doc = json.loads(out[out.index("{"):])
    derived, carded = sorted(doc.get("derived") or []), doc.get("carded") or []
    want = allowed_today()
    print("49financial: today=%d derived=%d carded=%d" % (len(want), len(derived), len(carded)))
    need(set(CORE) <= set(derived), "the 7-page core is not all derived: missing %s" % sorted(set(CORE) - set(derived)))
    need(derived == want and not carded, "derived != FIRM_ALLOWED_PATHS['49financial'] or something is carded (missing %s, extra %s)"
         % (sorted(set(want) - set(derived)), sorted(set(derived) - set(want))))
    rc, out = run([sys.executable, "lib/opal_portal_paths.py", "--check"], timeout=120)
    print("check live: rc=%d last=%r" % (rc, (out.strip().splitlines() or [""])[-1][:160]))
    need(rc == 0, "--check fails on the live map")
    src = open(os.path.join(ROOT, FIRM_ACCESS), encoding="utf-8").read()
    planted = src.replace("'49financial': new Set([", "'49financial': new Set([\n    '/zz-planted-page-r5',", 1)
    need(planted != src, "could not plant a page into a copy of firmAccess.ts")
    tmp = os.path.join(tempfile.mkdtemp(prefix="cn-r5-"), "firmAccess.ts")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(planted)
    rc, out = run([sys.executable, "lib/opal_portal_paths.py", "--check", "--access", tmp], timeout=120)
    print("check planted: rc=%d last=%r" % (rc, (out.strip().splitlines() or [""])[-1][:160]))
    need(rc != 0 and "/zz-planted-page-r5" in out, "--check did not STOP on a granted page the registry does not hold")
    return "PASS-R5-PATHS2"


ARMS = {"step13": arm_step13, "paths": arm_paths, "run": arm_run, "paths2": arm_paths2}


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
