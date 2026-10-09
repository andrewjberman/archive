"""OG-rl-15 (re-cut r28b) which release files reach the host: runs the deploy script's own tar command (deploy-to-ec2.sh, the `tar -czf` block, gateway part
only, no dashboard bundle) on the release tree, LISTING only, and compares the listed files with the host md5 list and with the release's changed files.
usage: python r29_reaches_host.py <release gateway dir> <release sha>"""
import io
import os
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, REL = sys.argv[1], sys.argv[2]
LIVE = "aa75078e1b72a28219e6148d3ec8e9bf705ea111"
GIT_REPO = os.path.abspath(os.path.join(SRC, "..", "..", "..", ".."))
p = subprocess.run(["tar", "-cf", "-", "-C", SRC, "--exclude=.env", "--exclude=audit.jsonl", "--exclude=*.log", "--exclude=__pycache__",
                    "--exclude=.token_cache", "--exclude=infra", "--exclude=dev_smoke.py", "--exclude=make_diagram.py",
                    "app", "deploy", "requirements.txt", "identity_tool_allowlist.txt"], capture_output=True)
assert p.returncode == 0, p.stderr[:200]
with tarfile.open(fileobj=io.BytesIO(p.stdout)) as t:
    tar_files = sorted(m.name for m in t.getmembers() if m.isfile())
lst = sorted(ln.split("  ", 1)[1].strip() for ln in open(os.path.join(HERE, "r29_release_md5.txt"), encoding="utf-8") if ln.strip())
changed = [x[len("infra/aws/ec2/opal-gateway/"):] for x in subprocess.run(["git", "-C", GIT_REPO, "diff", "--name-only", LIVE, REL, "--", "infra/aws/ec2/opal-gateway"],
           capture_output=True, text=True).stdout.split("\n") if x]
print("OG-rl-15 (r29) which release files reach the host: the deploy script's tar command (gateway part, listing only) run on the release tree %s" % REL[:10])
print("tarball gateway files %d; release host md5 list %d; in tar not in list %s; in list not in tar %s" % (
    len(tar_files), len(lst), [f for f in tar_files if f not in lst], [f for f in lst if f not in tar_files]))
n = 0
for f in changed:
    a, b = f in tar_files, f in lst
    n += 1 if a and b else 0
    print("%s: in tarball %s; in host md5 list %s => reaches the host: %s" % (f, a, b, "YES" if a and b else ("NO" if not a and not b else "INCONSISTENT")))
print("release files %d; reach the host %d" % (len(changed), n))
print("tests/ or ops/ entries in tarball: %d" % sum(1 for f in tar_files if f.startswith(("tests/", "ops/"))))
