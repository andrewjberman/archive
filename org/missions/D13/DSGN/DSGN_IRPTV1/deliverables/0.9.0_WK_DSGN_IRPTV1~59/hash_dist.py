"""sha256 over a build output folder: each file in sorted relative-path order (paths sorted case-insensitively),
update with the relative path (forward slashes, utf-8) then the file bytes. Usage: python hash_dist.py <dist dir>"""
import hashlib
import os
import sys

root = sys.argv[1]
files = []
for d, _, names in os.walk(root):
    for n in names:
        full = os.path.join(d, n)
        files.append(os.path.relpath(full, root).replace("\\", "/"))
files.sort(key=lambda s: s.lower())
h = hashlib.sha256()
total = 0
for rel in files:
    b = open(os.path.join(root, rel), "rb").read()
    total += len(b)
    h.update(rel.encode("utf-8"))
    h.update(b)
print("%s files=%d bytes=%d" % (h.hexdigest(), len(files), total))
