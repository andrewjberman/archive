"""OG-rl-15: the host md5 list of a gateway tree, taken through the deploy script's OWN tar command (the files that reach the host), and its comparison with the
live list (r29_live_md5.txt = the host-verified r28 list). usage: python r29_release_md5.py <gateway dir> <out md5 file>"""
import hashlib
import io
import os
import subprocess
import sys
import tarfile

SRC, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
p = subprocess.run(["tar", "-cf", "-", "-C", SRC, "--exclude=.env", "--exclude=audit.jsonl", "--exclude=*.log", "--exclude=__pycache__", "--exclude=.token_cache",
                    "--exclude=infra", "--exclude=dev_smoke.py", "--exclude=make_diagram.py", "app", "deploy", "requirements.txt", "identity_tool_allowlist.txt"], capture_output=True)
assert p.returncode == 0
t = tarfile.open(fileobj=io.BytesIO(p.stdout))
lines = ["%s  %s" % (hashlib.md5(t.extractfile(m).read()).hexdigest(), m.name) for m in sorted(t.getmembers(), key=lambda m: m.name) if m.isfile()]
open(OUT, "w", newline="\n").write("\n".join(lines) + "\n")
def rd(f):
    return dict((ln.rstrip("\n").split("  ", 1)[1], ln.split()[0]) for ln in open(f, encoding="utf-8") if ln.strip())


live, rel = rd(os.path.join(HERE, "r29_live_md5.txt")), rd(OUT)
shipped = sorted(k for k in rel if live.get(k) != rel[k])
print("live host list %d; release host list %d; only in live %s" % (len(live), len(rel), sorted(set(live) - set(rel))))
print("release files that differ from live or are new (reach the host): %d" % len(shipped))
for k in shipped:
    print("  %s %s" % ("NEW " if k not in live else "MOD ", k))
