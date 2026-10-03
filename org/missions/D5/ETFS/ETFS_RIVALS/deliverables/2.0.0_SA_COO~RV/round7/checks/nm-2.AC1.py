"""RIV-nm-2 AC1 (RFW-D11, DESIGN.md C13): the G4 request asks Bloomberg for the security's full name, and the G4 rows
carry it, so a holding whose source name is a 30-character cut ('International Container Termin', IDVZ) has a full
name on file.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base):
IDVZ's home-producer names are cut at 30 characters and nothing replaces them. The G4 request -- `MARKET_MAP` /
`MARKET_FIELDS` (enrichment_bloomberg.py:103-116), sent for the '/cusip/<CUSIP>' keys `_market_request_keys` builds for
a home-producer line -- asks for GICS, PX_LAST, CRNCY and the total return only: no name field, and `MARKET_SCHEMA`
(:117-123) has no name column.
FIELD (decided here): LONG_COMP_NAME. The repo's Bloomberg notes measure NAME as an ALL-CAPS short name cut at 28
characters ('MITSUBISHI UFJ FINANCIAL GRO', 'SINGAPORE TELECOMMUNICATIONS'; integrations/bloomberg/research/
field_map.json, mnemonic NAME, value_sampled), which would trade one cut for another; the estate's own precedent reads
LONG_COMP_NAME first, NAME as its fallback (lib/research/filings/battery.py:563-565).
INTERFACE (prescribed): `enrichment_bloomberg.handler_entry({"mode": "plan-market", "date", "sink"})` lists
"LONG_COMP_NAME" in `fields` (offline, no session); a `market` pull lands it in a new G4 column `security_name`
(MARKET_SCHEMA, string), NULL when the response carries none (never guessed). Every other field and column unchanged.

Offline, local sink, date 2026-09-30 (the run date pinned to it, so no historical request). G1: an IDVZ home-producer
line with no Bloomberg id, security_cusip Y41157101, name 'International Container Termin'; TXUE Bloomberg lines
'AAPL US Equity' and 'ZZZ US Equity'. The client is a stub (`_blp_reference_data`, `_blp_historical_data` replaced in
process; boto3 and requests.post refused): it answers ONLY the fields it is asked for, from
  /cusip/Y41157101: LONG_COMP_NAME 'International Container Terminal Services Inc', NAME 'INTL CONTAINER TERM SVCS',
                    PX_LAST 5.1, GICS_SECTOR_NAME Industrials, CRNCY PHP;
  AAPL US Equity:   LONG_COMP_NAME 'Apple Inc', NAME 'APPLE INC', PX_LAST 189.5, GICS_SECTOR_NAME Information
                    Technology;
  ZZZ US Equity:    PX_LAST 10.0 (no name field).
  - the offline plan requests LONG_COMP_NAME beside the ten market fields, for the CUSIP-keyed '/cusip/Y41157101' among
    its securities, with no client call;
  - the market pull's G4 rows carry `security_name`: Y41157101 -> 'International Container Terminal Services Inc',
    AAPL_US_Equity -> 'Apple Inc' (the stub saw LONG_COMP_NAME in its request);
  - control: ZZZ_US_Equity's security_name is NULL; Y41157101 still lands px_close 5.1 and gics_sector Industrials; the
    plan still requests all ten market fields.
FAIL at base: the first two limbs; the control PASSes."""

import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-09-30"
FULL = "International Container Terminal Services Inc"
CUT = "International Container Termin"
TEN = {"GICS_SECTOR_NAME", "GICS_INDUSTRY_GROUP_NAME", "GICS_INDUSTRY_GROUP", "GICS_INDUSTRY_NAME", "GICS_INDUSTRY",
       "GICS_SUB_INDUSTRY_NAME", "GICS_SUB_INDUSTRY", "PX_LAST", "CRNCY", "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"}
VENDOR = {
    "/cusip/Y41157101": {"LONG_COMP_NAME": FULL, "NAME": "INTL CONTAINER TERM SVCS", "PX_LAST": 5.1,
                         "GICS_SECTOR_NAME": "Industrials", "CRNCY": "PHP"},
    "AAPL US Equity": {"LONG_COMP_NAME": "Apple Inc", "NAME": "APPLE INC", "PX_LAST": 189.5,
                       "GICS_SECTOR_NAME": "Information Technology", "CRNCY": "USD"},
    "ZZZ US Equity": {"PX_LAST": 10.0},
}


def plant_g1(s):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rivalfunds import homes

    base = {"report_date": D, "dataset_revision": "20260930T230000Z-dddddddddddd", "is_cash_line": False,
            "position_type": "long", "security_isin": None}
    rows = [dict(base, fund_id="IDVZ", fund_ticker="IDVZ", source_used="home_producer", security_bloomberg=None,
                 position_id=None, security_cusip="Y41157101", security_name=CUT),
            dict(base, fund_id="TXUE", fund_ticker="TXUE", source_used="bloomberg", security_bloomberg="AAPL US Equity",
                 position_id="AAPL US Equity", security_cusip=None, security_name=None),
            dict(base, fund_id="TXUE", fund_ticker="TXUE", source_used="bloomberg", security_bloomberg="ZZZ US Equity",
                 position_id="ZZZ US Equity", security_cusip=None, security_name=None)]
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(homes.canonical_shape(D, "holdings-20260930T230000Z-dddddddddddd.parquet"), buf.getvalue())


def run(v):
    import datetime as dt

    c.setup_path()
    c.offline_guards()
    import pandas as pd
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks

    seen = []

    def ref(securities, fields, overrides=None, timeout_s=90.0):
        seen.append(list(fields))
        return {x: {f: VENDOR.get(x, {}).get(f) for f in fields if f in VENDOR.get(x, {})} for x in securities}

    def hist(*a, **k):
        raise RuntimeError("no historical request is expected: the run date is pinned to the partition date")

    eb._blp_reference_data, eb._blp_historical_data = ref, hist
    eb._run_date_et = lambda: dt.date.fromisoformat(D)
    spec = f"local:{c.tmpdir('rv_nm2a_')}"
    s = sinks.get_sink(spec)
    plant_g1(s)
    plan = eb.handler_entry({"mode": "plan-market", "date": D, "sink": spec})
    fields, secs = set(plan.get("fields") or []), plan.get("securities") or []
    print("plan:", plan.get("status"), "| securities:", secs, "| fields:", sorted(fields))
    v.check(plan.get("status") == "OK" and "LONG_COMP_NAME" in fields and "/cusip/Y41157101" in secs and not seen,
            "the offline plan requests LONG_COMP_NAME for the CUSIP-keyed /cusip/Y41157101, with no client call")
    r = eb.handler_entry({"mode": "market", "date": D, "sink": spec, "batch_id": "nm2"})
    print("market:", r.get("status"), r.get("detail"))
    pre = homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={D}") + "/"
    us = [x for x in s.list(pre) if x.endswith(".parquet")]
    g4 = pd.read_parquet(io.BytesIO(s.get(us[0]))) if us else pd.DataFrame()
    print(g4.reindex(columns=["security_id", "security_name", "px_close", "gics_sector"]).to_string(index=False))
    rows = {str(x["security_id"]): x for x in g4.to_dict("records")} if len(g4) else {}

    def nm(k):
        val = rows.get(k, {}).get("security_name")
        return None if val is None or val != val else val

    v.check(nm("Y41157101") == FULL and nm("AAPL_US_Equity") == "Apple Inc"
            and any("LONG_COMP_NAME" in f for f in seen),
            f"the G4 rows carry security_name from LONG_COMP_NAME ({nm('Y41157101')!r}, {nm('AAPL_US_Equity')!r})")
    y = rows.get("Y41157101", {})
    v.check(len(rows) == 3 and nm("ZZZ_US_Equity") is None and y.get("px_close") == 5.1
            and y.get("gics_sector") == "Industrials" and TEN <= fields,
            "control: no name in the response reads NULL; price and sector still land; the ten market fields stay")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
