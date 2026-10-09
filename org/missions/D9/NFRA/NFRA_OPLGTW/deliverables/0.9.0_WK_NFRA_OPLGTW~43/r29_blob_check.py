"""OG-rl-15 A7: proof BY BLOB that the committed release carries the bytes the Phase A BEFORE / REHEARSAL already read.
For every file that differs live..release: its release blob, the blob of the same path at the hand-off commit (10e525c7de), and whether the file reaches the host. Then the host md5 list of
the COMMITTED release tree (the deploy script's tar command) against r29_release_md5.txt, which is the list the rehearsal staged and verified (r29_staged_equal.out).
A host file whose release blob differs from the staged one would force a new rehearsal; none does when the last line reads yes.
usage: python r29_blob_check.py <release worktree> <repo with the hand-off commit>"""
import hashlib
import io
import os
import subprocess
import sys
import tarfile

WT, REPO = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
LIVE, HAND = "aa75078e1b72a28219e6148d3ec8e9bf705ea111", "10e525c7de"
G = "infra/aws/ec2/opal-gateway/"


def git(repo, *a):
    return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


head = git(WT, "rev-parse", "HEAD")
names = [x for x in git(WT, "diff", "--name-only", LIVE, head).split("\n") if x]
print("release %s: %d files differ from live %s" % (head, len(names), LIVE[:10]))
same = 0
for f in names:
    rb, hb = git(WT, "rev-parse", "%s:%s" % (head, f)), git(REPO, "rev-parse", "%s:%s" % (HAND, f))
    eq = rb == hb
    same += 1 if eq else 0
    print("  %-62s release %s hand-off %s %s" % (f, rb[:8], hb[:8], "SAME BLOB" if eq else "differs (a named release-time edit or the CT-i-11 lines)"))
print("same blob as the hand-off: %d of %d" % (same, len(names)))
p = subprocess.run(["tar", "-cf", "-", "-C", WT + "/" + G.rstrip("/"), "--exclude=.env", "--exclude=audit.jsonl", "--exclude=*.log", "--exclude=__pycache__", "--exclude=.token_cache",
                    "--exclude=infra", "--exclude=dev_smoke.py", "--exclude=make_diagram.py", "app", "deploy", "requirements.txt", "identity_tool_allowlist.txt"], capture_output=True)
t = tarfile.open(fileobj=io.BytesIO(p.stdout))
now = dict((m.name, hashlib.md5(t.extractfile(m).read()).hexdigest()) for m in t.getmembers() if m.isfile())
lst = dict((ln.rstrip("\n").split("  ", 1)[1], ln.split()[0]) for ln in open(os.path.join(HERE, "r29_release_md5.txt"), encoding="utf-8") if ln.strip())
live = dict((ln.rstrip("\n").split("  ", 1)[1], ln.split()[0]) for ln in open(os.path.join(HERE, "r29_live_md5.txt"), encoding="utf-8") if ln.strip())
shipped = sorted(k for k in now if live.get(k) != now[k])
ok = now == lst
print("host list of the committed tree: %d files; equals r29_release_md5.txt (the staged and rehearsed bytes): %s; reach the host: %d" % (len(now), "yes" if ok else "NO", len(shipped)))
print("RESULT: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
