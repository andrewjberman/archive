"""Scratch check: every `check <path> <sha>` line of the host script equals the sha256 of that member in the extracted
package (outside the product tree). ASCII only.

usage: python -I host_checks.py <host script> <extracted package root>
"""
import hashlib
import re
import sys

WANT_LIBRARY_LINE = re.compile(r"^WANT_LIBRARY=([0-9a-f]{64})\s*$", re.M)
CHECK_LINE = re.compile(r'^check\s+"?([^"\s]+)"?\s+(\$WANT_LIBRARY|[0-9a-f]{64})\s*$', re.M)

text = open(sys.argv[1], encoding="utf-8").read()
pkg = sys.argv[2]
want_library = WANT_LIBRARY_LINE.search(text).group(1)
rows = CHECK_LINE.findall(text)
ok, bad = 0, []
for name, want in rows:
    if want == "$WANT_LIBRARY":
        want = want_library
    got = hashlib.sha256(open(pkg + "/" + name, "rb").read()).hexdigest()
    if got == want:
        ok += 1
    else:
        bad.append({"member": name, "got": got, "script": want})
print("member checks in script: %d; equal to the tarball member bytes: %d; mismatches: %r" % (len(rows), ok, bad))
