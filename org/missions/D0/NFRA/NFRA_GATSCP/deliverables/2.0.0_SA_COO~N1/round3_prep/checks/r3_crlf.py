"""GS-f-2 AC1 (row D1-S6; ruling R4): to-pipeline-gate reads a modified task order the same whether its line endings are
CRLF or LF.

Each arm stages ONE modification of an existing NON-terminal tree order that declares `<placeholders>NONE</placeholders>`
(picked at run time from the index, named in the output)
in a private index and runs `python .tools/to-pipeline-gate.py <order>` (the dispatched path; the gate reads the staged
blob and `git diff --cached` for the modification).
Arm 1 (LF): one trailing blank line appended, LF kept -> rc 0.
Arm 2 (the build): the same file converted to CRLF, nothing else -> rc 0, as arm 1 (it differs only in line endings).
Arm 3 (still graded): CRLF and the `<placeholders>` line removed -> rc 1 (GATE (viii) still refuses a real defect).
"""
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import index_text, plant, run, tail, temp_index  # noqa: E402

def pick():
    """The first NON-terminal tree order in the index that declares `<placeholders>NONE</placeholders>` with LF endings:
    a terminal order's edit is a flip, which another limb grades, so it would confound the arms."""
    from r1_common import git
    for p in sorted(git(["ls-files", "--", "org/missions/D*/*/*/task-orders/*.md"]).stdout.split()):
        t = index_text(p)
        if "\r\n" not in t and "\n<status>pending</status>\n" in t and "\n<placeholders>NONE</placeholders>\n" in t:
            return p
    raise SystemExit("ERROR: no pending LF tree order declaring <placeholders>NONE</placeholders> in the index")


ORDER = pick()
print("subject order: %s" % ORDER)


def arm(text):
    d, env = temp_index()
    try:
        plant(env, ORDER, text)
        env["OPAL_AGENT_SERIAL"] = "2.0.0_SA_COO~N1"
        return run([sys.executable, ".tools/to-pipeline-gate.py", ORDER], env, timeout=110)
    finally:
        shutil.rmtree(d, ignore_errors=True)


lf = index_text(ORDER).replace("\r\n", "\n")
assert "<placeholders>NONE</placeholders>" in lf
rc1, out1 = arm(lf + "\n")
rc2, out2 = arm(lf.replace("\n", "\r\n"))
rc3, out3 = arm("\n".join(ln for ln in lf.split("\n") if "<placeholders>" not in ln).replace("\n", "\r\n"))
arms = [
    ("lf-modification-admitted", rc1 == 0, "rc=%s :: %s" % (rc1, tail(out1, 2))),
    ("crlf-same-as-lf", rc2 == 0 and rc2 == rc1, "rc=%s :: %s" % (rc2, tail(out2, 2))),
    ("crlf-defect-still-refused", rc3 == 1, "rc=%s :: %s" % (rc3, tail(out3, 2))),
]
for _n, _ok, _d in arms:
    print("  %s %s: %s" % ("PASS" if _ok else "FAIL", _n, _d))
_bad = sum(1 for a in arms if not a[1])
print("GS-F2-CRLF ok=%s arms=%d failed=%d" % (_bad == 0, len(arms), _bad))
sys.exit(0 if _bad == 0 else 1)
