"""F10-AC2 -- PULLED OUT OF SELECTION.

comp-which over the four `when:` phrasings that routed to comp-aws returns 0 comp-aws rows in
4 of 4 ranked lists, read from the SPILLED RANK FILE (.comp-graph/which/rank-<pid>.yaml) and never
from page 1 of stdout -- the terminal shows 3 of ~79, so a stdout read would certify nothing.

THE CONTROLS:
  * the BEFORE census (f10_baseline.json) recorded comp-aws at ranks 4 / 42 / 23 / 1 in those same
    four lists, read with THIS SAME instrument. The 0 is a DELTA, not a constant.
  * a control phrasing must still route to comp-kuzu -- so the router is not simply broken.
  * the pre-change curated tuple count (2 tuples naming comp-aws + 1 description string) is the
    control on the tuple census: the same counter returned 2 and 3 before the edit.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f10_lib as L  # noqa: E402

BASE = json.load(open(L.BASELINE, encoding="utf-8"))

print("F10-AC2 -- comp-aws pulled out of comp-which selection")
print("")

read_ok = 0
with_rows = 0
for q in L.PHRASINGS:
    rc, out, path = L.comp_which(q)
    rows = L.rank_rows(path)
    before = BASE["comp_which"][q]["comp_aws_ranks"]
    if rows is not None:
        read_ok += 1
    hits = [i + 1 for i, t in enumerate(rows or []) if t == "comp-aws"]
    if hits:
        with_rows += 1
    print("  Q: %s" % q)
    print("     rank_file=%s  tools_ranked=%d  comp-aws rows NOW=%d (rank %s)  BEFORE=%d (rank %s)"
          % (os.path.basename(path) if path else "(NONE -- NOT READ)", len(rows or []),
             len(hits), hits or "-", len(before), before or "-"))

rc, out, path = L.comp_which(L.CONTROL_PHRASING)
rows = L.rank_rows(path) or []
control_top = rows[0] if rows else "(none)"
print("")
print("  CONTROL Q: %s   -> rank 1 = %s" % (L.CONTROL_PHRASING, control_top))

cur = L.curated_tuple_census()
print("")
print("  curated tuples scanned: %d   naming comp-aws NOW: %d (lines %s)   BEFORE: %d (lines %s)"
      % (cur["tuples_total"], len(cur["tuples_naming_comp_aws"]), cur["tuples_naming_comp_aws"],
         len(BASE["curated"]["tuples_naming_comp_aws"]), BASE["curated"]["tuples_naming_comp_aws"]))
print("  non-comment CODE lines naming comp-aws NOW: %d %s   BEFORE: %d %s"
      % (len(cur["code_lines_naming_comp_aws"]), cur["code_lines_naming_comp_aws"],
         len(BASE["curated"]["code_lines_naming_comp_aws"]),
         BASE["curated"]["code_lines_naming_comp_aws"]))
print("")

print("COMP_AWS_ROWS=%d of %d phrasings" % (with_rows, len(L.PHRASINGS)))
print("RANKED_LISTS_READ=%d of %d" % (read_ok, len(L.PHRASINGS)))
print("CONTROL_PHRASING_ROUTES_TO=%s" % control_top)
print("CURATED_TUPLES_NAMING_COMP_AWS=%d of %d"
      % (len(cur["tuples_naming_comp_aws"]), cur["tuples_total"]))
print("BEFORE_CONTROL: comp-aws was in %d of %d ranked lists and named by %d of %d tuples -- the "
      "same instrument, before the edit"
      % (sum(1 for q in L.PHRASINGS if BASE["comp_which"][q]["comp_aws_ranks"]), len(L.PHRASINGS),
         len(BASE["curated"]["tuples_naming_comp_aws"]), BASE["curated"]["tuples_total"]))

ok = (with_rows == 0 and read_ok == len(L.PHRASINGS) and control_top == L.CONTROL_EXPECT
      and not cur["tuples_naming_comp_aws"])
print("RC=%d" % (0 if ok else 1))
sys.exit(0 if ok else 1)
