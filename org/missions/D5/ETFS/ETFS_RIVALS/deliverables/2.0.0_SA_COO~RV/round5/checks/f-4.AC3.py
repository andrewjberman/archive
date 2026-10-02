"""RIV-f-4 AC3 (hop-9 ruling b, its page half) -- a REFUSED window is shown as "not inferred", never as an empty "no trades" window.

Offline page fixture (test_p2's). A G6 object is planted for TXUE's window 2026-09-28 -> 2026-09-29 carrying the round-5 columns
`status` = REFUSED and `reason` = flow_factor_out_of_band (written directly with pyarrow, so this check does not depend on the G6
schema change of RIV-h-5). The page is published for 2026-09-30:
  - TXUE's block names that window as not inferred ("not inferred") with its reason token `flow_factor_out_of_band`;
  - control: BASG's block (no G6 row) carries neither phrase."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rivalfunds import gold_flow_reconciliation, homes, publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    spec, s, _ = c.page_fixture()
    row = tp2._g6_row("TXUE", tp2.DAY, "2026-09-28")
    row.update({"status": "REFUSED", "reason": "flow_factor_out_of_band"})
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pylist([row]), buf)
    s.put(gold_flow_reconciliation.target_uri(tp2.DAY, "zz-" + tp2.REV), buf.getvalue())
    r = publish_page.handler_entry(tp2._ev(spec))
    html = s.get(homes.page("2026-09-30", "index.html")).decode("utf-8")
    tx, ba = tp2._block(html, "TXUE"), tp2._block(html, "BASG")
    print("publish:", r.get("status"), "| TXUE block has 'not inferred':", "not inferred" in tx,
          "| reason token:", "flow_factor_out_of_band" in tx)
    v.check("not inferred" in tx and "flow_factor_out_of_band" in tx, "TXUE's REFUSED window reads 'not inferred' with its reason")
    v.check("not inferred" not in ba and "flow_factor_out_of_band" not in ba, "control: BASG's block carries neither")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
