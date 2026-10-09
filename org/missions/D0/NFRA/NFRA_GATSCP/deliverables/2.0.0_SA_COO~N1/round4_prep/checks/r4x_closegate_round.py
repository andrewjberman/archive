"""GS-x-1 AC1 (direct act; row D1-S15; 1.0.0_SA_CTO~DELL1 msg 2776): the missions-tree close gate grades the ROUND being closed.

Replays a real round close in a PRIVATE git dir (box-sync's own pattern; no ref and no working-tree file moves): LGIC_BLANKFIX round
14, commit 96a8832de7 (its row EXECUTING -> ROUND_CLOSE). HEAD is pinned to 96a8832de7^ and the index is read from 96a8832de7, with
HEAD's committed LGIC_BLANKFIX adjudication documents overlaid. The hook `.tools/git-hooks/missions-tree-check.sh` then sees that
commit's act and its close gate runs round-close-check. (AMGT_CORPUS round 40, the case msg 2776 cites, is not used: its round-40
grades are in an UNCOMMITTED ADJUDICATION_v47.md, so a staged read of round 40 is ungraded -- row D1-S15.)
Arm 1 (the build): the close-gate line reads `orders=3` and `verdict=MAY-CLOSE` -- round 14 alone (across every round it reads 69
  orders and REFUSED).
Arm 2 (the negative arm): with one ungraded `judgment="true"` criterion planted in a round-14 order of the same index, the close-gate
  line reads `verdict=REFUSED`.
"""
import os
import re
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT, git, git_bash, index_text, plant, run  # noqa: E402

ROW = "org/missions/D14/LGIC/LGIC_BLANKFIX/project.json"
FLAT = "org/projects/LGIC_BLANKFIX.json"
PIN = "96a8832de7"
ADJ = "org/missions/D14/LGIC/LGIC_BLANKFIX/surprise-channel/adjudications/"


def r14_order():
    names = git(["ls-tree", "-r", "--name-only", PIN, "--", "org/missions/D14/LGIC/LGIC_BLANKFIX/task-orders/"]).stdout.split()
    for p in sorted(names):
        t = git(["show", "%s:%s" % (PIN, p)]).stdout
        if re.search(r"(?m)^<round>14</round>", t):
            return p
    raise SystemExit("ERROR: no round-14 LGIC_BLANKFIX order")


def gate_line(probe):
    d = tempfile.mkdtemp(prefix="gatscp-r4x-")
    try:
        common = git(["rev-parse", "--path-format=absolute", "--git-common-dir"]).stdout.strip()
        parent = git(["rev-parse", PIN + "^"]).stdout.strip()
        with open(os.path.join(d, "HEAD"), "w") as fh:
            fh.write(parent + "\n")
        with open(os.path.join(d, "commondir"), "w") as fh:
            fh.write(common + "\n")
        env = dict(os.environ, GIT_DIR=d, GIT_WORK_TREE=ROOT)
        env.pop("GIT_INDEX_FILE", None)
        git(["read-tree", PIN], env=env)
        # overlay HEAD's LGIC_BLANKFIX adjudication documents (the committed grades that exist now)
        for ln in git(["ls-tree", "-r", "HEAD", "--", ADJ]).stdout.splitlines():
            meta, path = ln.split("\t", 1)
            mode, _typ, blob = meta.split()
            git(["update-index", "--add", "--cacheinfo", "%s,%s,%s" % (mode, blob, path)], env=env)
        assert '"ROUND_CLOSE"' in index_text(ROW, env)
        staged = [ROW, FLAT]
        if probe:
            p = r14_order()
            t = index_text(p, env)
            t = t.rstrip("\n") + '\n\n<criterion id="ZZ-R4X-PROBE" cell_refs="PROBE" judgment="true"/>\n'
            assert "ZZ-R4X-PROBE" in t
            plant(env, p, t)
            staged.append(p)
        env.update(PRECOMP_REPO_ROOT=ROOT, OWNED_PATHS_STAGED_FILES="\n".join(staged))
        rc, out = run([git_bash(), ".tools/git-hooks/missions-tree-check.sh"], env, timeout=115)
        lines = [ln for ln in out.splitlines() if "close-gate" in ln]
        return " || ".join(lines)[-400:] or ("no close-gate line (rc=%s): %s" % (rc, out[-240:]))
    finally:
        shutil.rmtree(d, ignore_errors=True)


g1 = gate_line(False)
g2 = gate_line(True)
arms = [
    ("round-being-closed-graded", "orders=3 " in g1 and "verdict=MAY-CLOSE" in g1, g1),
    ("ungraded-judgment-still-refuses", "verdict=REFUSED" in g2, g2),
]
for name, ok, detail in arms:
    print("  %s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
bad = sum(1 for a in arms if not a[1])
print("GS-X1-CLOSEGATE ok=%s arms=%d failed=%d" % (bad == 0, len(arms), bad))
sys.exit(0 if bad == 0 else 1)
