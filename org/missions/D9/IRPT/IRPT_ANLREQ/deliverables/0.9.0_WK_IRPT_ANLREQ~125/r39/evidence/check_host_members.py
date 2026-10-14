"""AR-y-311 step 2 control: every `check <path> <sha256>` line of a host script equals the extracted tarball member.

usage: python -I check_host_members.py <extracted package root> <host script>
"""
import hashlib
import re
import sys

pkg, script = sys.argv[1], sys.argv[2]
txt = open(script, "rb").read().decode("ascii")
ok = bad = 0
for m in re.finditer(r'^check "?([^" ]+)"? ([0-9a-f]{64})', txt, re.M):
    rel, want = m.group(1), m.group(2)
    got = hashlib.sha256(open(pkg + "/" + rel, "rb").read()).hexdigest()
    if got == want:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", rel, got, want)
print("member checks equal tarball: %d of %d" % (ok, ok + bad))
