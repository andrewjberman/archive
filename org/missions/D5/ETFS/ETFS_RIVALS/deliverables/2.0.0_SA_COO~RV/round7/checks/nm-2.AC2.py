"""RIV-nm-2 AC2 (RFW-D11, DESIGN.md C13; RIV-nm-1's display_name): the two producers that name holdings on the page
read the G4 full name as a display_name candidate, so a 30-character source cut gives way to it.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base):
IDVZ holdings read 'International Container Termin' on the rankings and the trend. Today's candidates:
  - gold_holding_contribution.py:413: display_name([the holding's G1 name, identity_maps' newest G1 name]) -- G1 only;
    its handler reads G4 with the columns (security_id, date, px_close, total_return_index, gics_sector) (:640);
  - gold_buying_trend.py:223: display_name([identity_maps' newest G1 name]) -- G1 only; its handler reads no G4.
`names.display_name` already ranks a 30-character candidate below any other real name, so the G4 name wins once it
is a candidate.
INTERFACE (prescribed): each producer's `handler_entry({"date": <page day>, "sink"})` reads the G4 `security_name`
(nm-2 AC1's column; the newest G4 object of each date on or before the page day, as holding_contribution already
reads G4) and adds it, keyed by G4 `security_id`, to the display_name candidates of the matching security key. A
security with no G4 name keeps today's candidates.

Offline, local sink (page day 2026-10-02, as-of 2026-10-01, the real universe). IDVZ (home) reports 2026-09-30 and
2026-10-01, three lines keyed by their bare CUSIP (no Bloomberg id):
  Y41157101 'International Container Termin' (30) -- G4 2026-10-01 security_name
            'International Container Terminal Services Inc';
  G0593M107 'AstraZeneca PLC'                      -- G4 row, security_name NULL;
  P60694117 'Kimberly-Clark de Mexico SAB d' (30)  -- no G4 row.
G4 (2026-10-01) prices Y41157101 and G0593M107. G5: one add of each in the window ending 2026-09-15.
  - holding_contribution: every IDVZ security row of Y41157101 reads 'International Container Terminal Services Inc';
  - buying_trend: IDVZ's security line Y41157101 reads 'International Container Terminal Services Inc';
  - control: G0593M107 reads 'AstraZeneca PLC' and P60694117 keeps 'Kimberly-Clark de Mexico SAB d' in both tables
    (no G4 name: never guessed), and each handler wrote its table (status OK).
FAIL at base: the first two limbs; the control PASSes."""

import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, AS_OF = "2026-10-02", "2026-10-01"
REV = "20261001T230000Z-eeeeeeeeeeee"
FULL = "International Container Terminal Services Inc"
LINES = (  # (key, G1 name, quantity, market value on 09-30, on 10-01, weight)
    ("Y41157101", "International Container Termin", 1000.0, 5000.0, 5100.0, 0.02),
    ("G0593M107", "AstraZeneca PLC", 100.0, 7000.0, 7070.0, 0.03),
    ("P60694117", "Kimberly-Clark de Mexico SAB d", 500.0, 900.0, 910.0, 0.01),
)
G4_ROWS = (("Y41157101", FULL, 5.1, "Industrials"), ("G0593M107", None, 70.7, "Health Care"))


def put(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def plant(s):
    import datetime as dt

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes

    for i, d in enumerate(("2026-09-30", AS_OF)):
        put(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), [
            {"fund_id": "IDVZ", "fund_ticker": "IDVZ", "report_date": d, "security_id": None, "raw_identifier": k,
             "security_cusip": k, "security_name": nm, "quantity": q, "market_value": (mv0, mv1)[i], "weight": w,
             "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "source_used": "home_producer",
             "resolution_status": "UNRESOLVED", "dataset_revision": REV, "gics_sector": None}
            for k, nm, q, mv0, mv1, w in LINES])
    put(s, eb.market_target_uri(AS_OF, "20261001T230500Z-ffffffffffff"), [
        {"security_id": k, "security_bloomberg": f"/cusip/{k}", "date": dt.date.fromisoformat(AS_OF), "px_close": px,
         "total_return_index": None, "currency": "PHP", "gics_sector": sec, "security_name": nm,
         "source": "blp_client.reference_data", "as_of": dt.date.fromisoformat(AS_OF), "as_of_source": "pull"}
        for k, nm, px, sec in G4_ROWS])
    put(s, homes.trade_schedule("2026-09-15", f"trades-{REV}.parquet"), [
        {"fund_id": "IDVZ", "fund_ticker": "IDVZ", "security_id": k, "security_key": k, "action": "add",
         "window_start": dt.date(2026, 9, 14), "window_end": dt.date(2026, 9, 15), "est_notional_base": 1.0e6 * (j + 1),
         "dataset_revision": REV} for j, (k, *_) in enumerate(LINES)])


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import sinks

    spec = f"local:{c.tmpdir('rv_nm2b_')}"
    s = sinks.get_sink(spec)
    plant(s)
    out = {}
    for name, mod in (("holding_contribution", hc), ("buying_trend", bt)):
        r = mod.handler_entry({"date": PAGE, "sink": spec})
        print(name, r.get("status"), r.get("outputs"), "" if r.get("status") == "OK" else r.get("detail"))
        ok = r.get("status") == "OK" and bool(r.get("outputs"))
        df = pd.read_parquet(io.BytesIO(s.get(r["outputs"][0]))) if ok else None
        out[name] = (r.get("status"), df)

    def names(table, key):
        df = out[table][1]
        if df is None or not len(df):
            return set()
        sel = df[(df["fund_id"] == "IDVZ") & (df["axis"] == "security") & (df["bucket"] == key)]
        return {str(x) for x in sel["security_name"]}

    for t in out:
        print(f"  {t}: " + "; ".join(f"{k} -> {sorted(names(t, k))}" for k, *_ in LINES))
    v.check(names("holding_contribution", "Y41157101") == {FULL},
            "holding_contribution names Y41157101 by its G4 full name on every row, not the 30-character cut")
    v.check(names("buying_trend", "Y41157101") == {FULL},
            "buying_trend names Y41157101 by its G4 full name, not the 30-character cut")
    ctl = all(names(t, "G0593M107") == {"AstraZeneca PLC"} and names(t, "P60694117") == {LINES[2][1]}
              and out[t][0] == "OK" for t in out)
    v.check(ctl, "control: without a G4 name the G1 name stands (AstraZeneca PLC; the Kimberly-Clark cut is kept)")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
