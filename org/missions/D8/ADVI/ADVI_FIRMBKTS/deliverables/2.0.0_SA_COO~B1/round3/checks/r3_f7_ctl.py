"""ADVI_FIRMBKTS round 3 check for cell FB-f-1 (the F7 compare instrument, row D1-C-S7), issuer 2.0.0_SA_COO~B1.

The instrument under test is the worker's r3_f7.py (a copy of r2_f7.py whose `compare` hashes the manifest's source
VERSION and prints destination-vs-manifest apart from source drift). This file only drives it; it never edits it.

--arms live     (3 arms) runs `r3_f7.py compare` against the round-2 manifest and the live buckets, read-only:
                  L1 a line `DEST-VS-MANIFEST: EQUAL` (every manifest key present and equal at the destination)
                  L2 a line `SOURCE-VS-MANIFEST:` that is its own line, with the changed count
                  L3 the verdict line `COPY-COMPLETE` and exit 0
--arms mutant   (2 arms) runs the same compare on a copy of the manifest with ONE single-part entry's ETag altered:
                  M1 the destination reads one mismatch and the verdict is COPY-NOT-COMPLETE (difference control)
                  M2 the line `DEST-VS-MANIFEST: DIFFERENT` is printed and `SOURCE-VS-MANIFEST:` is still its own line
--root points at another tree (the worker's worktree). Plain ASCII; the last line carries the arm count.
"""
import argparse
import gzip
import os
import subprocess
import sys
import tempfile

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
INSTR = DELIV + "/2.0.0_SA_COO~B1/round3/checks/r3_f7.py"
MANIFEST = DELIV + "/0.9.0_WK_ADVI_FIRMBKTS~8/F7_MANIFEST.tsv.gz"


def _run(root, manifest):
    p = os.path.join(root, INSTR)
    if not os.path.isfile(p):
        return None, "ABSENT %s" % INSTR
    out = subprocess.run([sys.executable, p, "compare", "--manifest", manifest], capture_output=True, text=True,
                         cwd=root, timeout=110)
    return out, ""


def live(root):
    out, why = _run(root, os.path.join(root, MANIFEST))
    if out is None:
        print("  " + why)
        return [("L1", False), ("L2", False), ("L3", False)]
    text = out.stdout
    print("\n".join("  " + ln for ln in text.splitlines()[:12]))
    src_lines = [ln for ln in text.splitlines() if ln.startswith("SOURCE-VS-MANIFEST:")]
    return [
        ("L1 a line `DEST-VS-MANIFEST: EQUAL` is printed", any(ln.startswith("DEST-VS-MANIFEST: EQUAL")
                                                             for ln in text.splitlines())),
        ("L2 `SOURCE-VS-MANIFEST:` is its own line and names the changed count",
         len(src_lines) == 1 and "changed=" in src_lines[0]),
        ("L3 the verdict is COPY-COMPLETE and the exit code is 0",
         out.returncode == 0 and "COPY-COMPLETE: every manifest key present and equal" in text),
    ]


def mutant(root):
    with gzip.open(os.path.join(root, MANIFEST), "rt", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    done = False
    for i, ln in enumerate(lines):
        if ln.startswith("#"):
            continue
        src, size, etag = ln.split("\t")
        if "-" not in etag:
            lines[i] = "\t".join((src, size, "0" * 32))
            done = True
            break
    if not done:
        print("  no single-part entry to alter")
        return [("M1", False), ("M2", False)]
    with tempfile.TemporaryDirectory() as td:
        mp = os.path.join(td, "mutant.tsv.gz")
        with gzip.open(mp, "wt", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        out, why = _run(root, mp)
    if out is None:
        print("  " + why)
        return [("M1", False), ("M2", False)]
    text = out.stdout
    print("\n".join("  " + ln for ln in text.splitlines()[:12]))
    return [
        ("M1 one mismatch is read at the destination and the verdict is COPY-NOT-COMPLETE",
         out.returncode != 0 and "COPY-NOT-COMPLETE" in text and "mismatch=1" in text),
        ("M2 `DEST-VS-MANIFEST: DIFFERENT` is printed and the source line stays its own line",
         any(ln.startswith("DEST-VS-MANIFEST: DIFFERENT") for ln in text.splitlines())
         and any(ln.startswith("SOURCE-VS-MANIFEST:") for ln in text.splitlines())),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("live", "mutant"), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    total = 3 if a.arms == "live" else 2
    try:
        res = (live if a.arms == "live" else mutant)(root)
    except Exception as e:  # noqa: BLE001
        print("ERROR %s: %s" % (type(e).__name__, str(e)[:200]))
        res = []
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 F7 COMPARE %s: %d of %d arms" % (a.arms.upper(), n, total))
    sys.exit(0 if n == total and res else 1)


if __name__ == "__main__":
    main()
