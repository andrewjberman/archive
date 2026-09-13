"""T5-AC2 -- FULL-TREE census of asset_class|assetClass, read from the GIT OBJECT STORE.

WHY A SECOND INSTRUMENT: the criterion's named invocation (comp-find) reads the WORKING TREE,
and this worktree is a cone-mode sparse checkout -- it printed 29824 UNREADABLE of 33520.
This instrument reads blobs from the object store at a pinned commit, so the sparse cone
cannot hide a file from it. Different instrument, not a re-run.

Usage: python ac2_objstore_census.py <repo_dir> <commit-ish> <label>
"""
import re
import subprocess
import sys
import collections

repo = sys.argv[1]
pin = sys.argv[2]
label = sys.argv[3]

PAT = re.compile(rb"asset_class|assetClass")


def git(args):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True)


ls = git(["ls-tree", "-r", pin])
if ls.returncode != 0:
    print("FATAL ls-tree rc=%d: %s" % (ls.returncode, ls.stderr.decode("utf-8", "replace")))
    sys.exit(2)

entries = []
for line in ls.stdout.decode("utf-8", "replace").splitlines():
    meta, path = line.split("\t", 1)
    mode, typ, sha = meta.split()
    entries.append((mode, typ, sha, path))

blobs = [e for e in entries if e[1] == "blob"]
nonblobs = [e for e in entries if e[1] != "blob"]

print("== CENSUS %s @ %s ==" % (label, pin))
print("DENOMINATOR: %d tree entries at pin | %d blobs | %d NON-BLOB (gitlink/submodule)"
      % (len(entries), len(blobs), len(nonblobs)))
for m, t, s, p in nonblobs:
    print("   NON-BLOB, unreadable through this instrument: %s  mode=%s type=%s -> %s" % (p, m, t, s))

# stream every blob through cat-file --batch
proc = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
inp = b"".join((e[2] + "\n").encode() for e in blobs)
out, _ = proc.communicate(inp)

pos = 0
hitfiles = collections.OrderedDict()
total_hits = 0
binary = 0
read = 0
for mode, typ, sha, path in blobs:
    nl = out.index(b"\n", pos)
    header = out[pos:nl].decode()
    size = int(header.split()[2])
    body = out[nl + 1:nl + 1 + size]
    pos = nl + 1 + size + 1
    read += 1
    if b"\x00" in body[:8192]:
        binary += 1
        # still search: a NUL early does not mean the token cannot be present
    n = len(PAT.findall(body))
    if n:
        hitfiles[path] = n
        total_hits += n

print("READ: %d blobs (of %d) | BINARY-ish (NUL in first 8KB, still searched): %d" % (read, len(blobs), binary))
print("HITS: %d occurrence(s) across %d file(s)" % (total_hits, len(hitfiles)))
print("ARITHMETIC: READ %d + NON-BLOB %d = %d (must equal tree entries %d)"
      % (read, len(nonblobs), read + len(nonblobs), len(entries)))
print()
print("== EVERY FILE WITH A HIT, sorted by path (NO head, NO page) ==")
for p in sorted(hitfiles):
    print("  %5d  %s" % (hitfiles[p], p))
