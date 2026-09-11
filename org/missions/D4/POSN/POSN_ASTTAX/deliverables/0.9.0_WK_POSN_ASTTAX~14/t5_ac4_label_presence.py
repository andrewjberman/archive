"""T5-AC4 -- does ANY portal source at the pin know the three NEW ratified labels?
Positive control included: the two OLD labels must be found, or the instrument is broken.
"""
import re
import subprocess
import collections

PORTAL = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/portal"
PIN = "e85f6eb84f"

ls = subprocess.run(["git", "-C", PORTAL, "ls-tree", "-r", PIN], capture_output=True)
entries = []
for line in ls.stdout.decode("utf-8", "replace").splitlines():
    meta, path = line.split("\t", 1)
    mode, typ, sha = meta.split()
    entries.append((mode, typ, sha, path))
blobs = [e for e in entries if e[1] == "blob"]
src = [e for e in blobs if e[3].startswith("src/")]

proc = subprocess.Popen(["git", "-C", PORTAL, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, _ = proc.communicate(b"".join((e[2] + "\n").encode() for e in src))
bodies = {}
pos = 0
for mode, typ, sha, path in src:
    nl = out.index(b"\n", pos)
    size = int(out[pos:nl].decode().split()[2])
    bodies[path] = out[nl + 1:nl + 1 + size]
    pos = nl + 1 + size + 1

print("DENOMINATOR: %d blobs under src/ of %d blobs at portal pin %s" % (len(src), len(blobs), PIN))
TERMS = collections.OrderedDict([
    ("Fixed Income  [POSITIVE CONTROL -- old label, must be found]", rb"Fixed Income"),
    ("Equity        [POSITIVE CONTROL -- old label, must be found]", rb"Equity"),
    ("Commodities   [NEW ratified label]", rb"Commodities"),
    ("Alternatives  [NEW ratified label]", rb"Alternatives"),
    ("Structured    [NEW ratified label]", rb"Structured"),
    ("structured    [lower, any casing route]", rb"structured"),
    ("ZZZ_NONEXISTENT [NEGATIVE CONTROL -- must be 0]", rb"ZZZ_NONEXISTENT_TOKEN"),
])
for name, pat in TERMS.items():
    rx = re.compile(pat)
    files = {p: len(rx.findall(b)) for p, b in bodies.items() if rx.search(b)}
    print("\n%-62s %3d file(s) / %4d occurrence(s)" % (name, len(files), sum(files.values())))
    for p in sorted(files):
        print("      %4d  %s" % (files[p], p))
