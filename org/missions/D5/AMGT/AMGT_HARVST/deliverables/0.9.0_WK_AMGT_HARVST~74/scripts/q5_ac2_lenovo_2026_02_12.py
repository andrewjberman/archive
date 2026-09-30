"""HVST-q-5 AC2: a LOCAL in-memory `build_daily` over the current gold inputs (S3 GET/LIST only, `write_gold` is
replaced by a capture so NO put happens), then prints the Lenovo 2026-02-12 line and the found-not-subset-of-covered
total. No deploy, no vendor call."""
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve()
while not (REPO / "lib" / "research" / "harvest").is_dir():
    REPO = REPO.parent
sys.path.insert(0, str(REPO))

import lib.research.harvest.publication_gold as gold  # noqa: E402

UNIVERSE = REPO / "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json"
securities = json.loads(UNIVERSE.read_text(encoding="utf-8"))
captured = {}


def _capture(table, rows, as_of_date, run_stamp, schema=None, client=None):
    captured["table"], captured["rows"], captured["schema"] = table, rows, schema
    return {"key": "(in-memory, not written)"}


gold.write_gold = _capture
summary = gold.build_daily(securities, datetime.date.today())
rows = captured["rows"]
print("BUILD (in memory, no put): table=%s securities=%d rows=%d schema_has_found=%s" % (
    captured["table"], summary["securities"], len(rows), "publishers_found_codes" in captured["schema"].names))

day = datetime.date(2026, 2, 12)
(row,) = [r for r in rows if r["security_key"] == "992_HK_Equity" and r["day"] == day]
print("992_HK_Equity 2026-02-12 covered=%s found=%s" % (row["publishers_covered_codes"], row["publishers_found_codes"]))
print("  (data_status=%s articles_total=%d)" % (row["data_status"], row["articles_total"]))

not_subset = [r for r in rows if not set(r["publishers_found_codes"]) <= set(r["publishers_covered_codes"])]
print("DAYS where found is not a subset of covered: %d of %d rows (%d securities)" % (
    len(not_subset), len(rows), len({r["security_key"] for r in not_subset})))
found_days = [r for r in rows if r["publishers_found_codes"]]
print("DAYS with any found publisher: %d" % len(found_days))
bad_status = [r for r in rows if len(r["publishers_covered_codes"]) != r["publishers_covered"]]
print("ROWS where len(covered_codes) != publishers_covered: %d (found never feeds the count)" % len(bad_status))
