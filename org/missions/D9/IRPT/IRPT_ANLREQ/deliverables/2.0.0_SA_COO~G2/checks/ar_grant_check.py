"""IRPT_ANLREQ round 60, cell AR-g-172 (issuer 2.0.0_SA_COO~G2): the checks of the Terraform read grant. Run from the worktree root.

    python ar_grant_check.py build|guard|regress

Terraform is not installed on the boxes, so the grant is graded on the TEXT of resident.tf at HEAD (AMENDMENT 1: the first delivery passed a
diff-only check and then FAILED `terraform fmt -check` at the CloudOps apply, so formatting is now graded here):
  build    the statement `ReadTheModelReturnSeriesAndPositioning` is in the policy: Effect Allow, Action exactly ["s3:GetObject"], Resource
           exactly the two object ARNs of C-MODEL-SOURCE (opal-data-portal-v2 json/benchmarks/model_portfolio_timeseries.json and
           json/positioning/positioning_data.json, built from the local model_source_bucket), no wildcard, no other action; the local
           model_source_bucket = "opal-data-portal-v2" exists once; AND its lines are `terraform fmt` clean: in every run of consecutive
           single-line `key = value` attributes the `=` signs are aligned to the longest key of THAT run (one space after it), and a line
           that opens a multi-line value (`[` or `{` at the end) is NOT part of the run.
  guard    against the parent of the first pin (50f7c709af2^): resident.tf deletes no line and adds exactly 16 lines; the branch changed no file
           but resident.tf, the order, the worker folder and the channel file.
  regress  resident.tf is still balanced HCL and every statement id of the parent of the first pin is still there.
Prints one RESULT line: AR-GRANT-OK / -FAIL (or -REGRESS-); rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

TF = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
PARENT = "50f7c709af2^"  # resident.tf before the grant was first added
SID = "ReadTheModelReturnSeriesAndPositioning"
KEYS = ("json/benchmarks/model_portfolio_timeseries.json", "json/positioning/positioning_data.json")
BUCKET = "opal-data-portal-v2"
ALLOWED_PREFIXES = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~331/",
                    "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-172.",
                    "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def head_text():
    return git("show", "HEAD:" + TF).stdout


def statement_block(text):
    """The lines of the `{ ... }` statement that holds the Sid, or None."""
    lines = text.splitlines()
    idx = [i for i, ln in enumerate(lines) if re.search(r'Sid\s*=\s*"%s"' % SID, ln)]
    if len(idx) != 1:
        return None
    start = idx[0]
    while start > 0 and lines[start].strip() != "{":
        start -= 1
    depth, end = 0, start
    for j in range(start, len(lines)):
        code = re.sub(r'#.*$', "", lines[j])
        depth += code.count("{") - code.count("}")
        if depth == 0 and j > start:
            end = j
            break
    return lines[start:end + 1]


def fmt_problems(block):
    """terraform fmt alignment of the single-line attributes of a block (the multi-line value line is its own group)."""
    problems, run = [], []

    def flush():
        if len(run) > 0:
            width = max(len(k) for k, _, _ in run)
            for key, pad, raw in run:
                if pad != width - len(key) + 1:
                    problems.append("not fmt-aligned (want %d spaces after %r, have %d): %s" % (width - len(key) + 1, key, pad, raw.strip()))
        run.clear()

    for ln in block[1:-1]:
        s = ln.strip()
        if not s or s.startswith("#"):
            flush()
            continue
        m = re.match(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*)=\s*(.*)$', ln)
        if not m:
            flush()
            continue
        value = m.group(4)
        if value.endswith("[") or value.endswith("{"):
            flush()
            continue
        run.append((m.group(2), len(m.group(3)), ln))
    flush()
    return problems


def build():
    text = head_text()
    fails = []
    block = statement_block(text)
    if block is None:
        return ["resident.tf has no single statement with Sid %s" % SID]
    code = "\n".join(re.sub(r'#.*$', "", ln) for ln in block)
    if not re.search(r'Effect\s*=\s*"Allow"', code):
        fails.append("the statement is not Effect Allow")
    actions = re.findall(r'Action\s*=\s*\[([^\]]*)\]', code)
    if len(actions) != 1 or sorted(re.findall(r'"([^"]+)"', actions[0])) != ["s3:GetObject"]:
        fails.append("the Action list is %s, want exactly [\"s3:GetObject\"]" % (actions,))
    res = re.search(r'Resource\s*=\s*\[(.*?)\]', code, re.S)
    arns = re.findall(r'"([^"]+)"', res.group(1)) if res else []
    want = ["arn:aws:s3:::${local.model_source_bucket}/" + k for k in KEYS]
    if arns != want:
        fails.append("the Resource list is %r, want exactly %r" % (arns, want))
    if "*" in (res.group(1) if res else ""):
        fails.append("a Resource carries a wildcard")
    for bad in ("s3:Put", "s3:Delete", "s3:List", "s3:*", "kms:", "sts:", "iam:", "GetObjectVersion"):
        if bad in code:
            fails.append("the statement mentions %s" % bad)
    locs = re.findall(r'^\s*model_source_bucket\s*=\s*"([^"]+)"\s*$', text, re.M)
    if locs != [BUCKET]:
        fails.append("the local model_source_bucket is %r, want exactly one, = %r" % (locs, BUCKET))
    fails += fmt_problems(block)
    return fails


def guard():
    fails = []
    stat = git("diff", "--numstat", PARENT, "HEAD", "--", TF).stdout.split()
    if len(stat) < 2 or stat[0] != "16" or stat[1] != "0":
        fails.append("resident.tf against the parent of the first pin is +%s/-%s, want +16/-0" % (stat[0] if stat else "?", stat[1] if len(stat) > 1 else "?"))
    rc = git("merge-base", "HEAD", "box/dell2")
    base = rc.stdout.strip()
    if rc.returncode != 0 or not base:
        return fails + ["no merge-base with box/dell2"]
    names = [n for n in git("diff", "--name-only", base, "HEAD").stdout.splitlines() if n.strip()]
    stray = [n for n in names if n != TF and not n.startswith(ALLOWED_PREFIXES)]
    if stray:
        fails.append("files outside the cell: %s" % ", ".join(stray[:6]))
    return fails


def regress():
    fails = []
    text = head_text()
    old = git("show", PARENT + ":" + TF).stdout
    code = "\n".join(re.sub(r'#.*$', "", ln) for ln in text.splitlines())
    stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    for o, c in (("{", "}"), ("[", "]"), ("(", ")")):
        if stripped.count(o) != stripped.count(c):
            fails.append("resident.tf has %d '%s' and %d '%s'" % (stripped.count(o), o, stripped.count(c), c))
    if code.count('"') % 2:
        fails.append("resident.tf has an odd number of double quotes")
    for sid in re.findall(r'Sid\s*=\s*"([^"]+)"', old):
        if sid not in text:
            fails.append("an existing statement id is gone: %s" % sid)
    return fails


def main():
    arm = sys.argv[1] if len(sys.argv) > 1 else ""
    if arm not in ("build", "guard", "regress"):
        print("AR-GRANT-FAIL usage: build|guard|regress")
        return 2
    fails = {"build": build, "guard": guard, "regress": regress}[arm]()
    tag = "AR-GRANT-REGRESS" if arm == "regress" else "AR-GRANT"
    print("%s-%s %s" % (tag, "FAIL" if fails else "OK", ("%s: " % arm if arm != "regress" else "") + ("; ".join(fails) if fails else "all arms")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
