"""IRPT_ANLREQ AR-g-169 checks (issuer 2.0.0_SA_COO~G2): the read-only trace of where the Opal model compositions live. Run from the worktree root.

    python ar_g169_checks.py build    the record exists and carries exactly six labelled answer lines Q1..Q6, each with a claim word
    python ar_g169_checks.py guard    every answer line cites at least one file:line, or says NOT READ for what it did not read (the control: a planted
                                      line with neither fails the same rule)
    python ar_g169_checks.py regress  the branch changed only the record, the worker's folder, the order and the channel file (merge-base with box/dell2)

Prints one RESULT line: AR-G169-OK / AR-G169-FAIL (or -REGRESS-); rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

RECORD = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~304/MODEL_COMPOSITION_TRACE.md"
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~304/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md",
              "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-169.")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/")
LABELS = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")
CLAIM = re.compile(r"\b(MEASURED|INFERRED|NOT READ)\b")
CITE = re.compile(r"[A-Za-z0-9_./~\-]+\.(?:py|json|tf|yaml|yml|md|sh|sql):\d+")


def answer_lines(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^(Q[1-6]) (.+)$", line)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2))
    return out


def load():
    try:
        return open(RECORD, encoding="utf-8").read()
    except OSError:
        return None


def build():
    text = load()
    if text is None:
        return ["the record %s is absent" % RECORD]
    got = answer_lines(text)
    fails = []
    for label in LABELS:
        n = len(got.get(label, []))
        if n != 1:
            fails.append("%s appears %d times, want exactly 1" % (label, n))
        elif not CLAIM.search(got[label][0]) or len(got[label][0]) < 60:
            fails.append("%s carries no claim word (MEASURED, INFERRED or NOT READ) or is under 60 characters" % label)
    return fails


def guard_rule(line):
    return bool(CITE.search(line)) or "NOT READ" in line


def guard():
    planted = "Q9 the model weights live somewhere under the MDPF tables, MEASURED by reading the pipeline (no file named)"
    if guard_rule(planted):
        return ["control: a planted line with no citation and no NOT READ was accepted by the rule"]
    text = load()
    if text is None:
        return []  # the build arm owns the record's existence; the control above has already run
    got = answer_lines(text)
    fails = ["%s has no file:line citation and does not say NOT READ" % label for label in LABELS
             if label in got and not guard_rule(got[label][0])]
    if not got:
        fails.append("the record carries no answer lines")
    return fails


def scope():
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if not n.startswith(OWN_PREFIX + ISSUER)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "regress":
        fails = scope()
        print("AR-G169-REGRESS-%s %s" % ("FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G169-FAIL usage: build | guard | regress")
        return 2
    fails = build() if mode == "build" else guard()
    print("AR-G169-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
