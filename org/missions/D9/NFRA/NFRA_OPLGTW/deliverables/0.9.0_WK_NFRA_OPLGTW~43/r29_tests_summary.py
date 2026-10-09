"""OG-rl-15 step 3: summarise a r29_perfile_tests.sh output: files run, files with rc!=0, and the FAILED/ERROR ids per file.
usage: python r29_tests_summary.py <out file> [<baseline out file>]  (with a baseline: failing ids in the release not in the baseline are NEW)"""
import re
import sys


def parse(p):
    files, cur = {}, None
    for ln in open(p, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\n")
        if ln.startswith("== "):
            cur = ln[3:]
            files[cur] = {"rc": None, "ids": [], "line": ""}
        elif cur and ln.startswith("rc="):
            files[cur]["rc"] = int(ln[3:])
        elif cur and re.match(r"^(FAILED|ERROR) ", ln):
            files[cur]["ids"].append(re.sub(r" - .*", "", ln))
        elif cur and re.search(r"\d+ (passed|failed|error)", ln):
            files[cur]["line"] = ln
    return files


rel = parse(sys.argv[1])
base = parse(sys.argv[2]) if len(sys.argv) > 2 else {}
bad = {f: v for f, v in rel.items() if v["rc"] != 0}
print("files run %d; files with rc!=0 %d" % (len(rel), len(bad)))
newids = 0
for f, v in sorted(bad.items()):
    b = base.get(f)
    bids = set(b["ids"]) if b else set()
    new = [i for i in v["ids"] if i not in bids]
    newids += len(new) if b else 0
    print("%s rc=%s | %s | ids=%d%s" % (f, v["rc"], v["line"], len(v["ids"]), ("" if not base else " | baseline %s, NEW in release: %s" % ("rc=%s" % b["rc"] if b else "ABSENT-in-baseline", new if b else v["ids"]))))
if base:
    print("files in baseline only: %s" % sorted(set(base) - set(rel)))
    print("files in release only (new test files): %s" % sorted(set(rel) - set(base)))
    print("new failing ids vs baseline (files present in both): %d" % newids)
