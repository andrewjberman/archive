"""IRPT_ANLREQ round 60, cell AR-g-172 (issuer 2.0.0_SA_COO~G2): the checks of the Terraform read grant. Run from the worktree root.

    python ar_grant_check.py build|guard|regress

Terraform is not installed on the boxes, so the grant is graded on the TEXT of the diff against the merge-base with box/dell2:
  build    the diff adds ONE statement to resident.tf that allows exactly s3:GetObject on exactly the two keys of C-MODEL-SOURCE
           (opal-data-portal-v2 json/benchmarks/model_portfolio_timeseries.json and json/positioning/positioning_data.json), with no
           wildcard, no other action and no other bucket or key.
  guard    the diff deletes no line and changes no file but resident.tf (and the order, the worker folder and the channel file).
  regress  resident.tf is still balanced HCL (braces, brackets, parentheses, quotes) and every existing statement id is still present.
Prints one RESULT line: AR-GRANT-OK / -FAIL (or -REGRESS-); rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

TF = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
KEYS = ("json/benchmarks/model_portfolio_timeseries.json", "json/positioning/positioning_data.json")
BUCKET = "opal-data-portal-v2"
ALLOWED_PREFIXES = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~331/",
                    "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-172.",
                    "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def base():
    rc = git("merge-base", "HEAD", "box/dell2")
    return rc.stdout.strip() if rc.returncode == 0 else None


def added_text(b):
    diff = git("diff", "-U0", b, "HEAD", "--", TF).stdout
    return [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]


def removed_lines(b):
    diff = git("diff", "-U0", b, "HEAD", "--", TF).stdout
    return [ln for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]


def build(b):
    add = added_text(b)
    if not add:
        return ["resident.tf has no added line against the base"]
    code = "\n".join(ln for ln in add if not ln.strip().startswith("#"))  # comments may quote anything
    fails = []
    for k in KEYS:
        if k not in code:
            fails.append("the grant never names the key %s" % k)
    if BUCKET not in code and "portal" not in code:
        fails.append("the grant names neither the bucket %s nor a local/variable that carries it" % BUCKET)
    actions = re.findall(r'Action\s*=\s*\[([^\]]*)\]', code)
    if len(actions) != 1:
        fails.append("the diff adds %d Action lists, want exactly one statement" % len(actions))
    elif sorted(re.findall(r'"([^"]+)"', actions[0])) != ["s3:GetObject"]:
        fails.append("the Action list is %s, want exactly [\"s3:GetObject\"]" % actions[0].strip())
    for bad in ("s3:Put", "s3:Delete", "s3:List", "s3:*", "kms:", "sts:", "iam:"):
        if bad in code:
            fails.append("the added code mentions %s" % bad)
    res = re.findall(r'Resource\s*=\s*(\[[^\]]*\]|[^\n]+)', code)
    for r in res:
        if "*" in r:
            fails.append("a Resource carries a wildcard: %s" % r.strip())
    if code.count("Sid") != 1:
        fails.append("the diff adds %d Sid lines, want exactly one statement" % code.count("Sid"))
    return fails


def guard(b):
    fails = []
    rem = removed_lines(b)
    if rem:
        fails.append("the diff deletes %d line(s) of resident.tf, first: %s" % (len(rem), rem[0][:100]))
    names = [n for n in git("diff", "--name-only", b, "HEAD").stdout.splitlines() if n.strip()]
    stray = [n for n in names if n != TF and not n.startswith(ALLOWED_PREFIXES)]
    if stray:
        fails.append("files outside the cell: %s" % ", ".join(stray[:6]))
    return fails


def regress(b):
    fails = []
    text = git("show", "HEAD:" + TF).stdout
    old = git("show", b + ":" + TF).stdout
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
    b = base()
    if not b:
        print("AR-GRANT-FAIL no merge-base with box/dell2")
        return 1
    fails = {"build": build, "guard": guard, "regress": regress}[arm](b)
    tag = "AR-GRANT-REGRESS" if arm == "regress" else "AR-GRANT"
    print("%s-%s %s" % (tag, "FAIL" if fails else "OK", ("%s: " % arm if arm != "regress" else "") + ("; ".join(fails) if fails else "all arms")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
