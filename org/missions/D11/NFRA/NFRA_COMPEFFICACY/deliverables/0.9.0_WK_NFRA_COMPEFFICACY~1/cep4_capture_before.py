"""CE-p-4 BEFORE capture -- run ONCE on the UNPATCHED .tools/comp-which.

Writes cep4_before.json: for every question in the battery, the rc, the ranked rows from the
spilled rank file, the terminal route block, and the rank-row count. The AC1 battery compares
against this file and NEVER re-derives it -- a baseline re-taken after the change is not a
baseline.

Usage:  python cep4_capture_before.py            # writes cep4_before.json (refuses to clobber)
        python cep4_capture_before.py --force    # deliberate re-capture
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cep4_lib as L  # noqa: E402

OUT = os.path.join(L.HERE, "cep4_before.json")


def main() -> int:
    if os.path.exists(OUT) and "--force" not in sys.argv[1:]:
        print("REFUSED: %s already exists. A baseline re-taken after the change is not a "
              "baseline. Pass --force only if you know the tool is still unpatched." % OUT)
        return 2

    per_dir, all_ids = L.authority_census()
    print("AUTHORITY CENSUS (at capture time)")
    for rel, ids in per_dir:
        print("  %s: %d ids" % (rel, len(ids)))
    print("  DISTINCT ACROSS ALL %d DIRS: %d ids" % (len(per_dir), len(all_ids)))

    data = {
        "captured_by": "0.9.0_WK_NFRA_COMPEFFICACY~1",
        "tool": ".tools/comp-which",
        "authority_dirs": [{"dir": d, "id_count": len(i), "ids": i} for d, i in per_dir],
        "distinct_ids": all_ids,
        "questions": {},
    }

    qs = list(L.PHRASINGS) + [L.PLANTED_Q, L.MISSPELLED_Q, L.REAL_Q]
    for i, q in enumerate(qs, 1):
        rc, text, spill = L.comp_which(q)
        rows = L.ranked_rows(spill)
        data["questions"][q] = {
            "rc": rc,
            "ranked_rows": rows,
            "rank_row_count": L.rank_row_count(spill),
            "terminal": L.terminal_routes(text),
            "spill_present": bool(spill),
        }
        print("  [%d of %d] rc=%d  rank_rows=%d  spill=%s  %s"
              % (i, len(qs), rc, L.rank_row_count(spill), bool(spill), q))

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=True, indent=2, sort_keys=True)
        fh.write("\n")
    print("WROTE %s (%d questions)" % (OUT, len(data["questions"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
