"""Scratch verifier for the r28 resident build (outside the product tree). ASCII only.

usage: python -I verify_pkg.py <tarball> <extract dir>
Extracts the tarball into <extract dir> (must not exist), re-hashes every member, checks SHA256SUMS line by line,
and prints one JSON document.
"""
import hashlib
import json
import os
import sys
import tarfile

TAR, DEST = sys.argv[1], sys.argv[2]
if os.path.exists(DEST):
    raise SystemExit("extract dir exists: " + DEST)
os.makedirs(DEST)
names = []
with tarfile.open(TAR, "r:gz") as t:
    for m in t.getmembers():
        if not m.isfile():
            continue
        name = m.name[2:] if m.name.startswith("./") else m.name
        data = t.extractfile(m).read()
        target = os.path.join(DEST, *name.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        names.append(name)

def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

sums = {}
with open(os.path.join(DEST, "SHA256SUMS"), encoding="utf-8") as fh:
    for line in fh:
        digest, _, name = line.rstrip("\n").partition("  ")
        sums[name] = digest
mismatch = [n for n, d in sums.items() if sha(os.path.join(DEST, *n.split("/"))) != d]
unlisted = sorted(n for n in names if n != "SHA256SUMS" and n not in sums)
print(json.dumps({"members_including_SHA256SUMS": len(names), "sums_entries": len(sums),
                  "sums_mismatch": mismatch, "members_not_in_sums": unlisted}, indent=1))
