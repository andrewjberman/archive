"""One-time copy check, NFRA_SCHWABBF AL-p-1 (criterion AL1-p1-AC2). NOT a standing comparator: lives in the worker's
deliverables folder only, never under tests/.

Diffs the 49F Schwab Box puller (SOURCE) against the Alongside copy (COPY) line by line with difflib and proves the
copy differs in exactly these ways:
  - the one non-comment changed line is the $Master [ValidateSet(...)] line (the four Cottonwood masters);
  - every other difference is a comment line added or changed inside the header block, before the param( line.
A deleted line, or any changed line outside the header block, is a failure.

Prints exactly one line on success:  COPY-DIFF-OK changed_non_comment_lines=<n>
On failure prints COPY-DIFF-FAIL with the first offending hunk and exits 1.
Run from anywhere: python <this file> [-v]   (-v prints every hunk to stderr for review)
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

# this file: <repo>/org/missions/D8/NFRA/NFRA_SCHWABBF/deliverables/0.9.0_WK_NFRA_SCHWABBF~13/check_copy_diff.py
REPO = Path(__file__).resolve().parents[7]
SRC = REPO / "infra" / "aws" / "ec2" / "canonical-schwab-si2" / "sdd-daily-pull.ps1"
COPY = REPO / "infra" / "aws" / "ec2" / "alongside-schwab-si2" / "sdd-daily-pull.ps1"

F49 = {"08242234", "08335338", "08403355"}
COTTON = {"08719286", "08134043", "08165601", "08480305"}


def is_comment(line: str) -> bool:
    return line.lstrip().startswith("#")


def is_validateset_pair(src_line: str, cop_line: str) -> bool:
    # source: the 49F master ValidateSet on the $Master parameter; copy: the four Cottonwood masters, no 49F master
    src_names = set(re.findall(r"'(\d{8})'", src_line))
    cop_names = set(re.findall(r"'(\d{8})'", cop_line))
    return ("[ValidateSet(" in src_line and "$Master" in src_line and src_names == F49
            and "[ValidateSet(" in cop_line and "$Master" in cop_line and cop_names == COTTON)


def main() -> int:
    verbose = "-v" in sys.argv[1:]
    a = SRC.read_text(encoding="utf-8").splitlines()
    b = COPY.read_text(encoding="utf-8").splitlines()
    pa = next(i for i, line in enumerate(a) if line.startswith("param("))
    pb = next(i for i, line in enumerate(b) if line.startswith("param("))
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    nonc = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        src_chunk, cop_chunk = a[i1:i2], b[j1:j2]
        if verbose:
            print(f"HUNK {tag} src[{i1}:{i2}] copy[{j1}:{j2}]", file=sys.stderr)
            for line in src_chunk:
                print(f"  - {line}", file=sys.stderr)
            for line in cop_chunk:
                print(f"  + {line}", file=sys.stderr)
        # the one allowed non-comment change: the $Master ValidateSet line (one line replaced by one line)
        if tag == "replace" and len(src_chunk) == 1 and len(cop_chunk) == 1 \
                and not is_comment(src_chunk[0]) and not is_comment(cop_chunk[0]) \
                and is_validateset_pair(src_chunk[0], cop_chunk[0]) and i1 > pa and j1 > pb:
            nonc += 1
            continue
        # every other difference: comment lines only, replace or insert, inside the header block before param(
        if tag == "delete":
            print(f"COPY-DIFF-FAIL delete hunk src[{i1}:{i2}] copy[{j1}:{j2}]")
            for line in src_chunk:
                print(f"  - {line}")
            return 1
        if i2 > pa or j2 > pb:
            print(f"COPY-DIFF-FAIL hunk outside the header block: {tag} src[{i1}:{i2}] copy[{j1}:{j2}]")
            return 1
        if not all(is_comment(x) for x in src_chunk + cop_chunk):
            print(f"COPY-DIFF-FAIL non-comment change in the header block: {tag} src[{i1}:{i2}] copy[{j1}:{j2}]")
            for line in src_chunk:
                print(f"  - {line}")
            for line in cop_chunk:
                print(f"  + {line}")
            return 1
    print(f"COPY-DIFF-OK changed_non_comment_lines={nonc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
