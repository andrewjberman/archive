"""AMGT_RESAPP round 77 -- AMGT-ba-26, row Z-S242: etf-classifications.tf re-committed with LF endings.

  python r77_ba26.py --cell lf|content

The file is infra/aws/terraform/yang-pipeline/etf-classifications.tf. Its attribute is `eol=lf`; its blob at the cut carries 82 CR.
lf:      C1 the blob at HEAD carries 0 carriage returns; C2 `git check-attr eol` still reads lf.
content: C1 (the bound) the blob at HEAD with every CR removed is byte-equal to the cut's blob with every CR removed, so the
         commit changed line endings and nothing else. BASE_BLOB is the blob id at the cut.
Verdict: R77 BA26 <CELL>: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import subprocess
import sys

PATH = "infra/aws/terraform/yang-pipeline/etf-classifications.tf"
BASE_BLOB = "d9f082f9d72280ed3cf145761e98973219e73d47"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("lf", "content"), required=True)
    a = ap.parse_args()
    head = git("show", f"HEAD:{PATH}")
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "lf":
        clause("C1 the blob at HEAD carries no carriage return", len(head) > 0 and head.count(b"\r") == 0,
               f"{head.count(13)} CR in {len(head)} B")
        attr = git("check-attr", "eol", "--", PATH).decode("utf-8", "replace").strip()
        clause("C2 the eol attribute still reads lf", attr.endswith(": lf"), attr)
    else:
        base = git("cat-file", "blob", BASE_BLOB)
        clause("C1 only line endings moved (CR-stripped bytes equal the cut's)",
               len(base) > 0 and head.replace(b"\r", b"") == base.replace(b"\r", b""),
               f"head {len(head)} B, base {len(base)} B")
    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R77 BA26 {a.cell.upper()}: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
