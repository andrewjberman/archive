"""OG-rl-6 PHASE C-A2 step 16b: prove the release r17c's server.py / config.py / deploy-to-ec2.sh diffs equal the CLOUD-source diffs.

Run from anywhere: python rl8_diff_equality.py   (reads git only; writes nothing).
Method: the release diff is `git -C <rel> diff e91819e281 HEAD -- <file>`; the CLOUD-source diff is the commit's own diff of that file.
Hunk headers may differ (CLOUD's tree has other lines the live release does not); the BODY lines (+, - and context) must be equal.
deploy-to-ec2.sh's .env line is one very long printf line that differs between live and CLOUD for other reasons, so for it the
equality is stated on the CHANGE: the comment line added is byte-equal, and the .env line's delta is exactly one inserted token.
"""
import subprocess
import sys

REL = "C:/tmp/og-rel13"
WK = "C:/tmp/wk-oplgtw-15-r17"
G = "infra/aws/ec2/opal-gateway/"
BASE = "e91819e281"
NEWKEY = "YEARINREVIEW_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com" + chr(92) + "n"


def git(repo, *a):
    r = subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode != 0:
        raise SystemExit("git rc=%d: %s" % (r.returncode, r.stderr))
    return r.stdout


def body(diff):
    return [ln for ln in diff.split("\n") if not ln.startswith(("diff --git", "index ", "--- ", "+++ ", "@@"))]


def headers(diff):
    return [ln.split(" ")[1:3] and " ".join(ln.split(" ")[:4]) for ln in diff.split("\n") if ln.startswith("@@")]


def cmp_full(name, relref, cloud_a, cloud_b):
    rd = git(REL, "diff", BASE, relref, "--", G + name)
    cd = git(WK, "diff", cloud_a, cloud_b, "--", G + name)
    eq = body(rd) == body(cd)
    print("%s: release diff %d lines, CLOUD diff %d lines, body lines equal: %s; hunk headers release=%s cloud=%s"
          % (name, len(rd.split("\n")), len(cd.split("\n")), "yes" if eq else "NO", headers(rd), headers(cd)))
    return eq


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    ok = True
    # config.py: both trees' bases are byte-equal, so the diffs should be equal INCLUDING hunk headers.
    rd = git(REL, "diff", BASE, rel, "--", G + "app/config.py")
    cd = git(WK, "diff", "52ef7bef94~1", "52ef7bef94", "--", G + "app/config.py")
    full = rd.split("\n")[2:] == cd.split("\n")[2:]  # skip the two header lines (index hashes may differ not at all, a/ b/ equal)
    print("app/config.py: release vs CLOUD diff text equal (hunk headers included): %s" % ("yes" if full else "NO"))
    ok &= full
    ok &= cmp_full("app/config.py", rel, "52ef7bef94~1", "52ef7bef94")
    # server.py: CLOUD's change is commit 17d151f6cc (its parent is the pre-hookup file).
    ok &= cmp_full("app/server.py", rel, "17d151f6cc~1", "17d151f6cc")
    # deploy-to-ec2.sh: state the equality on the change.
    rd = git(REL, "diff", BASE, rel, "--", G + "deploy-to-ec2.sh").split("\n")
    cd = git(WK, "diff", "52ef7bef94~1", "52ef7bef94", "--", G + "deploy-to-ec2.sh").split("\n")
    r_add = [ln[1:] for ln in rd if ln.startswith("+") and not ln.startswith("+++")]
    r_del = [ln[1:] for ln in rd if ln.startswith("-") and not ln.startswith("---")]
    c_add = [ln[1:] for ln in cd if ln.startswith("+") and not ln.startswith("+++")]
    c_del = [ln[1:] for ln in cd if ln.startswith("-") and not ln.startswith("---")]
    print("deploy-to-ec2.sh: release +%d/-%d lines, CLOUD +%d/-%d lines" % (len(r_add), len(r_del), len(c_add), len(c_del)))
    r_cmt = [ln for ln in r_add if ln.startswith("# YEARINREVIEW_VIEW_ALLOWED_EMAILS (")]
    c_cmt = [ln for ln in c_add if ln.startswith("# YEARINREVIEW_VIEW_ALLOWED_EMAILS (")]
    same_cmt = len(r_cmt) == 1 and r_cmt == c_cmt
    print("deploy-to-ec2.sh: the added comment line (cites @121b7b016e: %s) is byte-equal in both: %s"
          % ("yes" if r_cmt and "@121b7b016e" in r_cmt[0] else "NO", "yes" if same_cmt else "NO"))
    r_env = [ln for ln in r_add if ln.startswith("printf 'MOCK_GRAPH=0")]
    c_env = [ln for ln in c_add if ln.startswith("printf 'MOCK_GRAPH=0")]
    rd_env = [ln for ln in r_del if ln.startswith("printf 'MOCK_GRAPH=0")]
    cd_env = [ln for ln in c_del if ln.startswith("printf 'MOCK_GRAPH=0")]
    one = len(r_env) == len(c_env) == len(rd_env) == len(cd_env) == 1
    r_delta = one and r_env[0].count(NEWKEY) == 1 and r_env[0].replace(NEWKEY, "", 1) == rd_env[0]
    c_delta = one and c_env[0].count(NEWKEY) == 1 and c_env[0].replace(NEWKEY, "", 1) == cd_env[0]
    print("deploy-to-ec2.sh: .env printf line delta is exactly ONE inserted token %r, release: %s, CLOUD: %s"
          % (NEWKEY, "yes" if r_delta else "NO", "yes" if c_delta else "NO"))
    other_r = [ln for ln in r_add if ln not in r_cmt + r_env]
    other_c = [ln for ln in c_add if ln not in c_cmt + c_env]
    print("deploy-to-ec2.sh: other added lines release %d, CLOUD %d; other removed lines release %d, CLOUD %d"
          % (len(other_r), len(other_c), len(r_del) - len(rd_env), len(c_del) - len(cd_env)))
    ok &= same_cmt and r_delta and c_delta and not other_r and not other_c and len(r_del) == len(c_del) == 1
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
