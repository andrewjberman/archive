# MX-m-1 (a): the Z-S47 grain re-measured -- every latest-version fees log object, classified with the same predicate as m1_a_classify.py.
import glob
import re
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else ".scratch/a"
PATS = [r"^ERROR:.*fail", r"(Download|Merge) exit code: [1-9]", r"^FAILED\s*$"]
n = f = s886 = 0
first = None
last = None
lastgood = None
f886 = 0
for p in sorted(glob.glob(OUT + "/fees_all/fees-download-*.log")):
    t = open(p, encoding="utf-8", errors="replace").read()
    sz = os.path.getsize(p)
    fail = any(
        re.search(x, t, re.M | re.I if x.startswith("^ERROR") else re.M) for x in PATS
    )
    d = os.path.basename(p)[len("fees-download-") : -4]
    n += 1
    f += fail
    s886 += sz == 886
    f886 += fail and sz == 886
    if fail:
        first = first or d
        last = d
    else:
        lastgood = d
print(
    "fees log objects (latest version per key):",
    n,
    " log-records-failure:",
    f,
    " exactly 886 bytes:",
    s886,
    " failure AND 886 bytes:",
    f886,
)
print(
    "first failing date",
    first,
    " last failing date",
    last,
    " last non-failing date",
    lastgood,
)
