"""IRPT_YCDGEN round 8 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r8_checks.py d8      each of the six old rows has exactly one D2-W10 row that RESOLVES or RE-CUTS it
    python r8_checks.py gate    the surprise-row gate accepts the channel file
    python r8_checks.py f8      the ycharts/research tests: 0 failed, at least 240 passed
    python r8_checks.py f8fold  closed_reason and NotHeld tell NO_RULE from NO_ROW

Prints one RESULT line: R8-<MODE>-OK or R8-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

CHANNEL = "org/missions/D9/IRPT/IRPT_YCDGEN/surprise-channel/investigations/INVESTIGATION_v1.md"
OLD = ("IRPT_YCDGEN-W6-S1", "IRPT_YCDGEN-W6-S2", "IRPT_YCDGEN-D2-W6-S3", "IRPT_YCDGEN-D2-W7-S1", "IRPT_YCDGEN-D2-W6-S1",
       "IRPT_YCDGEN-D2-W6-S2")
HEAD = re.compile(r"^## (IRPT_YCDGEN-D2-W10-S[0-9]+) -- (RESOLVES|RE-CUTS) (IRPT_YCDGEN-[A-Z0-9-]+)(?![A-Z0-9-])", re.M)


def main(mode):
    if mode == "d8":
        text = open(CHANNEL, encoding="utf-8", errors="replace").read()
        found = {}
        for new, verb, old in HEAD.findall(text):
            found.setdefault(old, []).append((new, verb))
        bad = [o for o in OLD if len(found.get(o, [])) != 1]
        for o in OLD:
            print(o, found.get(o, []))
        if bad:
            print("R8-D8-FAIL %d of %d old rows lack exactly one RESOLVES or RE-CUTS row: %s" % (len(bad), len(OLD), ", ".join(bad)))
            return 1
        print("R8-D8-OK rows=%d of %d" % (len(OLD), len(OLD)))
        return 0
    if mode == "gate":
        out = subprocess.run([sys.executable, ".tools/surprise-row-gate.py", "--check", CHANNEL], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        tail = (out.stdout + out.stderr).strip().splitlines()[-1:] or ["(no output)"]
        print(tail[0][:300])
        if out.returncode != 0:
            print("R8-GATE-FAIL rc=%d" % out.returncode)
            return 1
        print("R8-GATE-OK")
        return 0
    if mode == "f8":
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no",
                              "infra/aws/lambda/investor-reporting/ycharts/research/tests"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
        line = lines[-1].strip() if lines else "(no summary line)"
        print(line)
        m = re.search(r"([0-9]+) passed", line)
        passed = int(m.group(1)) if m else 0
        if out.returncode != 0 or "failed" in line or "error" in line or passed < 240:
            print("R8-F8-FAIL rc=%d passed=%d (need >= 240, 0 failed, 0 errors)" % (out.returncode, passed))
            return 1
        print("R8-F8-OK passed=%d" % passed)
        return 0
    if mode == "f8fold":
        sys.path.insert(0, "infra/aws/lambda/investor-reporting/ycharts/research")
        try:
            import held_data
            import layout_overview as lo
            import opal_producer as op
            no_rule = [g for g in ("bond_maturity_1_to_3_years", "market_cap_giant", "zz_no_such_group")
                       if held_data.RULES.get(g) is None][0]
            got = held_data.value_of(no_rule, "ANY", [{"ticker": "AAA", "amount": 1}], {})
            cause = getattr(got, "cause", None)
            el = {"id": "e1", "source": {"computed": "OPAL_HELD", "group": "g1"}}
            a = op.closed_reason(lo.NOT_HELD_PREFIX + "NO_RULE:x", el)
            b = op.closed_reason(lo.NOT_HELD_PREFIX + "NO_ROW:x", el)
        except Exception as exc:  # a missing attribute or a changed signature is a FAIL, stated
            print("R8-F8FOLD-FAIL %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        print("cause=%r no_rule->%r no_row->%r" % (cause, a, b))
        if cause != "NO_RULE" or a != "NOT_IN_THIS_VERSION" or b != "INPUT_MISSING:security_not_covered":
            print("R8-F8FOLD-FAIL the three answers are not NO_RULE / NOT_IN_THIS_VERSION / INPUT_MISSING:security_not_covered")
            return 1
        print("R8-F8FOLD-OK")
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
