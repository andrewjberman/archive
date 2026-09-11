"""T5-AC2 -- the CODE subset of the reachability census, as a SUBTRACTION with printed remainders."""
import re
import subprocess
import sys
import collections

repo = sys.argv[1]
pin = sys.argv[2]

ls = subprocess.run(["git", "-C", repo, "ls-tree", "-r", pin], capture_output=True)
entries = []
for line in ls.stdout.decode("utf-8", "replace").splitlines():
    meta, path = line.split("\t", 1)
    mode, typ, sha = meta.split()
    entries.append((mode, typ, sha, path))
blobs = [e for e in entries if e[1] == "blob"]

proc = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, _ = proc.communicate(b"".join((e[2] + "\n").encode() for e in blobs))
bodies = {}
pos = 0
for mode, typ, sha, path in blobs:
    nl = out.index(b"\n", pos)
    size = int(out[pos:nl].decode().split()[2])
    bodies[path] = out[nl + 1:nl + 1 + size]
    pos = nl + 1 + size + 1

REG = re.compile(rb"etf-classifications|ETF_CLASSIFICATIONS|etf_classifications_dynamodb|ETFClassifier|classify_etf|etf_classification\b")
TOKEN = re.compile(rb"asset_class|assetClass")

# STEP 1: every blob carrying the token
step1 = {p for p, b in bodies.items() if TOKEN.search(b)}
print("STEP 1  every blob carrying asset_class|assetClass ............ %5d of %d blobs" % (len(step1), len(blobs)))

# STEP 2: subtract the RECORD plane (project records, docs, graph indexes, proofs)
RECORD = re.compile(r"^(org/|docs/|rcg/|memory/|\.claude/|\.scratch/)")
step2_out = {p for p in step1 if RECORD.match(p)}
step2 = step1 - step2_out
print("STEP 2  MINUS org/ docs/ rcg/ memory/ record plane ............ -%4d  -> %4d"
      % (len(step2_out), len(step2)))

# STEP 3: subtract blobs with NO registry reference AT ALL
step3_out = {p for p in step2 if not REG.search(bodies[p])}
step3 = step2 - step3_out
print("STEP 3  MINUS blobs with NO reference to the registry/module .. -%4d  -> %4d"
      % (len(step3_out), len(step3)))

print("\n== THE SURVIVING CODE-PLANE POPULATION (%d), by top directory ==" % len(step3))
byd = collections.Counter("/".join(p.split("/")[:5]) for p in step3)
for d, n in sorted(byd.items()):
    print("  %3d  %s" % (n, d))

print("\n== EVERY SURVIVOR, full path (no page) ==")
for p in sorted(step3):
    print("   %s" % p)

print("\n== THE STEP-3 REMAINDER (token but NO registry reference), by top dir -- the SUBTRACTED set, printed so it can be falsified ==")
byd2 = collections.Counter("/".join(p.split("/")[:4]) for p in step3_out)
for d, n in sorted(byd2.items()):
    print("  %3d  %s" % (n, d))
