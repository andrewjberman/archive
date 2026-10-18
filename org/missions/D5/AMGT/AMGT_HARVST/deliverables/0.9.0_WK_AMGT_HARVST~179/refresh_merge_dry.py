"""refresh_merge_dry.py -- merges the slice outputs of the HVST-cn-1 dry run into refresh_run_dry.out.

Usage (from the worktree root): python -I <this file> <slice.out> [<slice.out> ...]
Keeps every `REFRESH <name> ...` line in slice order, drops each slice's own REFRESH-CENSUS line, and writes the
merged REFRESH-CENSUS line LAST, counted from the merged REFRESH lines (never copied from a slice). Writes ASCII,
LF endings, to the deliverable folder beside this script.
"""

import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refresh_run_dry.out")
_STATUS = re.compile(r" status=(\S+) ")


def main(paths):
    rows = []
    for path in paths:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh.read().splitlines():
                if line.startswith("REFRESH ") and not line.startswith("REFRESH-"):
                    rows.append(line)
    names = [r.split()[1] for r in rows]
    if len(set(names)) != len(names):
        raise SystemExit("MERGE REFUSED: a name appears twice across the slices")
    counts = Counter(_STATUS.search(r).group(1) for r in rows)
    census = ("REFRESH-CENSUS names=%d written=%d would_write=%d unchanged=%d no_new_model_block=%d "
              "skipped_allowed=%d skipped_guard=%d errors=%d mode=dry-run"
              % (len(rows), counts["WRITTEN"], counts["WOULD_WRITE"], counts["UNCHANGED"],
                 counts["NO_NEW_MODEL_BLOCK"], counts["SKIPPED_ALLOWED"], counts["SKIPPED_GUARD"], counts["ERROR"]))
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(r + "\n")
        fh.write(census + "\n")
    print(census)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
