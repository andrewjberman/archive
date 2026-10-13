"""AMGT_RESAPP round-102 PREP -- the two shape checks of `AMGT-bi-4` (NFRA_GATSCP D1-S18: the portal suite's red tests).

  python r102_d1s18_check.py table <table.md>
  python r102_d1s18_check.py boundary <portal worktree root> [--base <ref, default DEV>]

`table` grades the worker's table file (a document, not a test run):
  D1  the file names each of the six red test files by its base name, exactly once as a row key:
      iv-e-46.class-readers.test.ts, iv-e-115.vendor-section-names-units.test.tsx, iv-e-26.wire-regen.test.ts, iv-e-48.new-classes.test.tsx,
      iv-e-98.generators-drift.test.ts, producer-fixtures.test.ts
  D2  each of the six has a line `CAUSE: <at least 20 characters>` and a line `CLASS: <STALE-CITATION|GENERATED-DRIFT|PIN-DRIFT|CONTRACT-ENUM|OTHER>` in its block (a block
      runs from its `### <file>` heading to the next heading)
  D3  one line `SUITE-BEFORE: files <n> | pass <p> | fail <f> | skip <s>` with fail 6, and one `SUITE-AFTER: ...` line with the same files count (the denominator did not move)
      and fail 3 or fewer (the wire-drift tests wait on the contract decision; the cell does not touch them)
`boundary` lists the files the nested portal worktree changed against `--base` and reads YES only when every one is one of the three repair files:
  src/pages/AdvisorIntelligence/__tests__/iv-e-46.class-readers.test.ts, src/pages/InvestorReporting/contracts/vendorSectionNames.ts,
  src/pages/InvestorReporting/fixtures/wire/HoldingsSnapshot.valid.json (the wire folder and the three wire-drift tests are NOT in it).
Verdict lines `R102 D1-S18 TABLE: YES|NO` and `R102 D1-S18 BOUNDARY: YES|NO`. Exit 0 on YES. Writes nothing.
"""
import re
import subprocess
import sys

FILES = [
    "iv-e-46.class-readers.test.ts",
    "iv-e-115.vendor-section-names-units.test.tsx",
    "iv-e-26.wire-regen.test.ts",
    "iv-e-48.new-classes.test.tsx",
    "iv-e-98.generators-drift.test.ts",
    "producer-fixtures.test.ts",
]
CLASSES = ("STALE-CITATION", "GENERATED-DRIFT", "PIN-DRIFT", "CONTRACT-ENUM", "OTHER")
ALLOWED = (
    "src/pages/AdvisorIntelligence/__tests__/iv-e-46.class-readers.test.ts",
    "src/pages/InvestorReporting/contracts/vendorSectionNames.ts",
    "src/pages/InvestorReporting/fixtures/wire/HoldingsSnapshot.valid.json",
)


def table(path):
    text = open(path, encoding="utf-8").read()
    ok_all = True
    blocks = {}
    parts = re.split(r"^###\s+", text, flags=re.M)
    for part in parts[1:]:
        head, _, body = part.partition("\n")
        blocks[head.strip()] = body
    for f in FILES:
        matching = [h for h in blocks if h == f or h.endswith("/" + f)]
        d1 = len(matching) == 1
        body = blocks[matching[0]] if d1 else ""
        cause = re.search(r"^CAUSE:\s*(.{20,})$", body, flags=re.M)
        klass = re.search(r"^CLASS:\s*(%s)\s*$" % "|".join(CLASSES), body, flags=re.M)
        ok = d1 and cause is not None and klass is not None
        ok_all = ok_all and ok
        print("   %s %s | heading %s | cause %s | class %s" % ("PASS" if ok else "FAIL", f, "1" if d1 else str(len(matching)), "yes" if cause else "NO",
                                                                  klass.group(1) if klass else "NO"))
    before = re.search(r"^SUITE-BEFORE:\s*files (\d+) \| pass (\d+) \| fail (\d+) \| skip (\d+)\s*$", text, flags=re.M)
    after = re.search(r"^SUITE-AFTER:\s*files (\d+) \| pass (\d+) \| fail (\d+) \| skip (\d+)\s*$", text, flags=re.M)
    d3 = bool(before and after and int(before.group(3)) == 6 and before.group(1) == after.group(1) and int(after.group(3)) <= 3)
    print("   %s D3 suite lines | before %s | after %s" % ("PASS" if d3 else "FAIL", before.group(0) if before else "ABSENT", after.group(0) if after else "ABSENT"))
    verdict = "YES" if ok_all and d3 else "NO"
    print("R102 D1-S18 TABLE: %s" % verdict)
    return 0 if verdict == "YES" else 1


def boundary(root, base):
    out = subprocess.run(["git", "-C", root, "diff", "--name-only", "%s...HEAD" % base], capture_output=True, text=True)
    if out.returncode != 0:
        print("R102 D1-S18 BOUNDARY: NO (git diff rc=%d: %s)" % (out.returncode, out.stderr.strip()[:160]))
        return 1
    files = [x.strip() for x in out.stdout.splitlines() if x.strip()]
    bad = [f for f in files if not f.startswith(ALLOWED)]
    for f in files:
        print("   %s %s" % ("PASS" if f not in bad else "FAIL", f))
    verdict = "YES" if not bad else "NO"
    print("changed files %d | outside the grant %d" % (len(files), len(bad)))
    print("R102 D1-S18 BOUNDARY: %s" % verdict)
    return 0 if verdict == "YES" else 1


def main(argv):
    if len(argv) >= 2 and argv[0] == "table":
        return table(argv[1])
    if len(argv) >= 2 and argv[0] == "boundary":
        base = argv[argv.index("--base") + 1] if "--base" in argv else "DEV"
        return boundary(argv[1], base)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
