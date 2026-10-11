"""IRPT_YCDGEN round 8 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r8_checks.py d8      each of the six old rows has exactly one D2-W10 row that RESOLVES or RE-CUTS it
    python r8_checks.py gate    the surprise-row gate accepts the channel file

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
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
