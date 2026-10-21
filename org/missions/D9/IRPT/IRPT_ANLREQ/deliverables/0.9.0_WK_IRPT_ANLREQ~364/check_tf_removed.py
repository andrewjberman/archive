"""AR-y-491 check: the throwaway residue Terraform file is removed from the tree.

Stdlib only. Offline: reads this worktree's git history; no AWS call, no network.
Prints one line. Default mode judges the real tree; --selftest feeds the three
predicates mutated in memory and prints CONTROL-FIRES only when all three read BAD.
"""
import subprocess
import sys

PATH = "infra/aws/terraform/investor-reporting/ycharts/irpt_residue_delete_r35.tf"
BASE = "1e6073761ca"
BLOB = "8897a25273c8547c2ba0d6f9fdd3ce76849fdddf"
INFRA = "infra/"


def git(*args):
    proc = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout


def check_tracked(ls_files_out):
    """Predicate 1: git ls-files prints nothing for the path."""
    lines = [ln for ln in ls_files_out.splitlines() if ln.strip()]
    if lines:
        return False, len(lines), "path still tracked"
    return True, 0, ""


def check_diff(name_status_lines):
    """Predicate 2: the base-to-HEAD infra diff is exactly one D line for the path."""
    lines = [ln for ln in name_status_lines if ln.strip()]
    reasons = []
    if len(lines) != 1:
        reasons.append("infra diff has %d lines, not 1" % len(lines))
    if not lines or lines[0] != "D\t" + PATH:
        reasons.append("infra diff line is not a D for the path")
    return not reasons, len(lines), "; ".join(reasons)


def check_blob(rev_parse_out, rc):
    """Predicate 3: the base content of the path is the signed blob."""
    got = rev_parse_out.strip()
    if rc != 0:
        return False, "rev-parse at base failed (rc=%d)" % rc
    if got != BLOB:
        return False, "base blob %s is not %s" % (got or "(empty)", BLOB)
    return True, ""


def real_run():
    rc1, out1 = git("ls-files", "--", PATH)
    ok1, n1, why1 = check_tracked(out1 if rc1 == 0 else "")
    if rc1 != 0:
        ok1, why1 = False, "git ls-files rc=%d" % rc1

    rc2, out2 = git("diff", "--name-status", BASE, "HEAD", "--", INFRA)
    lines2 = out2.splitlines() if rc2 == 0 else []
    ok2, n2, why2 = check_diff(lines2)
    if rc2 != 0:
        ok2, why2 = False, "git diff rc=%d" % rc2

    rc3, out3 = git("rev-parse", BASE + ":" + PATH)
    ok3, why3 = check_blob(out3, rc3)

    reasons = [w for ok, w in ((ok1, why1), (ok2, why2), (ok3, why3)) if not ok]
    if ok1 and ok2 and ok3:
        print(
            "RESIDUE-TF-REMOVED tracked=%d infra_changes=%d deletion=yes "
            "content_blob_in_history=%s" % (n1, n2, BLOB[:10])
        )
        return 0
    print("RESIDUE-TF-REMOVED-BAD " + "; ".join(r for r in reasons if r))
    return 1


def selftest():
    fired1 = not check_tracked(PATH + "\n")[0]
    fired2 = not check_diff(["D\t" + PATH, "M\tinfra/aws/ec2/EC2_MANIFEST.json"])[0]
    fired3 = not check_blob("0" * 40 + "\n", 0)[0]
    if fired1 and fired2 and fired3:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-SILENT tracked=%s diff=%s blob=%s" % (fired1, fired2, fired3))
    return 1


def main(argv):
    if "--selftest" in argv[1:]:
        return selftest()
    return real_run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
