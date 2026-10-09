"""IRPT_BCKEND round 110 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ADDENDUM 18.1, msg 3284; row D2-S48):
  IB110-1  IB-pr-409  irpt-narrative: a no-row Opal caller stays UNKNOWN as live (no widening), the W201-S6 TypeError fix kept,
                      re-packeted with a NEW hash (worker ~272)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB110-1-AC1  narrative tests: `-k no_row_unknown` >= 2 pass, `-k served_error_path` >= 2 pass, `-k opal_capital_binding` >= 2 pass,
               and the narrative suite passes. Base: FAIL (no no_row_unknown tests).
  IB110-1-AC2  census C + replay R (worker ~272): BUILD_ONLY rc 0 on a clean tree; built sha256 != QiNRKpaC... (the stopped build);
               >= 14 arms all identical/expected-diff, with `no_row_internal_enforcer_scope`, `no_row_internal_selects_other_firm`
               and `internal_error_refusal` each `identical`; >= 1 negative control. Base: FAIL (no C).
  IB110-1-AC3  packet P names Branch A, Branch B, the pin and the built sha256, and states the shared served.py is unchanged.
               Base: FAIL (no P).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

NARR = "infra/aws/lambda/investor-reporting/narrative"
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~272/"
STOPPED = "QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw="


def pyt(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True,
                       timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB110"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB110-1-AC1":
        for sel in ("no_row_unknown", "served_error_path", "opal_capital_binding"):
            rc, n, last = pyt(root / NARR, "tests", "-k", sel)
            if rc != 0 or n < 2:
                fail("-k %s rc %d: %s" % (sel, rc, last))
        rc, n, last = pyt(root / NARR, "tests")
        if rc != 0:
            fail("narrative suite rc %d: %s" % (rc, last))
        print("OK: no-row UNKNOWN + error-path + binding tests; suite %s" % last)
    elif cid == "IB110-1-AC2":
        c = load(W + "IB110-1_release_census.json")
        bo, arts = c.get("build_only") or {}, c.get("artifacts") or []
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or len(arts) != 1:
            fail("census %r / %d artifact(s)" % (bo, len(arts)))
        built = arts[0].get("built_sha256")
        if not built or built == STOPPED:
            fail("built sha256 %r (must be new)" % built)
        arms = load(W + "IB110-1_release_replay.json").get("arms") or []
        by = {x.get("name"): x.get("verdict") for x in arms}
        if len(arms) < 14 or not all(v in ("identical", "expected-diff") for v in by.values()):
            fail("%d arm(s) / verdicts %r" % (len(arms), sorted(set(by.values()))))
        for name in ("no_row_internal_enforcer_scope", "no_row_internal_selects_other_firm", "internal_error_refusal"):
            if by.get(name) != "identical":
                fail("%s reads %r" % (name, by.get(name)))
        if not any(x.get("negative_control") for x in arms):
            fail("no negative control")
        print("OK: new build %s...; %d arms; enforcer scope, binding and error refusal identical" % (built[:8], len(arms)))
    elif cid == "IB110-1-AC3":
        c = load(W + "IB110-1_release_census.json")
        pp = root / (W + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-409.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        built = str(((c.get("artifacts") or [{}])[0]).get("built_sha256") or "")
        for s in ("Branch A", "Branch B", str(c.get("pin") or ""), built, "served.py"):
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: packet names both branches, the pin, the built sha256 and served.py")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
