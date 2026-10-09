"""OG-rl-15 form step 5 (row Z-W28-S14): the rehearsal's STAGED file list, printed beside the release's SHIPPED list (the files of r29_release_md5.txt that differ from or are absent in
r29_live_md5.txt); the two must be equal, with equal md5, before the rehearsal's reads count. The staged md5s are the host's own `md5sum` lines in r29_rehearsal.out.
usage: python r29_staged_equal.py   (from anywhere; reads the files beside it)"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def rd(f):
    return dict((ln.rstrip("\n").split("  ", 1)[1], ln.split()[0]) for ln in open(os.path.join(HERE, f), encoding="utf-8") if ln.strip())


live, rel = rd("r29_live_md5.txt"), rd("r29_release_md5.txt")
shipped = sorted(k for k in rel if live.get(k) != rel[k])
staged = {}
for ln in open(os.path.join(HERE, "r29_rehearsal.out"), encoding="utf-8"):
    m = re.match(r"^([0-9a-f]{32})  /tmp/og_r29_\S+/gw/(\S+)$", ln.strip())
    if m:
        staged[m.group(2)] = m.group(1)
print("shipped list (release host list vs live host list): %d files" % len(shipped))
for k in shipped:
    print("  %-48s shipped %s staged %s" % (k, rel[k][:8], staged.get(k, "ABSENT")[:8]))
eq = sorted(staged) == shipped and all(staged[k] == rel[k] for k in staged)
print("staged %d, shipped %d; lists equal and every md5 equal: %s" % (len(staged), len(shipped), "yes" if eq else "NO"))
print("RESULT: " + ("PASS" if eq else "FAIL"))
sys.exit(0 if eq else 1)
