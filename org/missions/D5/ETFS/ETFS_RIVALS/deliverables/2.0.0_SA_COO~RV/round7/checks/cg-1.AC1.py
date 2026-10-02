"""RIV-cg-1 AC1 (ROUND_ANALYSIS.round6.md section 3 item 4): the census reads the RANKINGS' own GICS classification. A
GICS input the rankings classify (holding_contribution `sector_source` own | g4 | other_fund) never reads `missing`;
one the rankings leave Unclassified still does. Source: the round-6 served-delta measurement (C:/tmp/r6measure/a1_510,
the round-6 code at 510566a0f8): 33 gics rows read missing while the rankings classify them -- ETFT 9, PCLG 11, TSEL 9,
WCMG 4 -- and ALL 33 carry sector_source "g4" and the reason "no G4 row for 2026-10-01"; the rankings' G4 window was
{date=2026-09-29, date=2026-10-01}, and the 33 have a G4 sector only in the 09-29 partition.

The two join-key differences (base ed61068340):
  (a) G4, the measured 33: the census joins G4 on (security_id, date == the as-of day) and reads ONLY the as-of day's
      partition (`gold_input_census.py:87` `_newest_by_date(..., day, day)`, `:102` `_d(date) == day`); the rankings
      join G4's gics_sector on security_id ALONE over every partition from earliest_start(as_of) - 10 days to the page
      day (`gold_holding_contribution.py:636-639`, `_prices` :217-228), so a sector on an older G4 date classifies.
  (b) other_fund, latent (0 of the 33; the round-6 census reads 0 gics rows covered_by_fallback): the census keys the
      other fund's statement on the exact security key, security_id else alias(raw_identifier), over a 14-day G1
      window (`gold_input_census.py:56` `_sector_funds`, `:85`, `:141`); the rankings match on ANY shared identifier of
      `_XID` (security_id, security_bloomberg, security_cusip, security_isin, security_sedol, raw_identifier;
      upper-cased) over the YTD G1 window (`gold_holding_contribution.py:232-264` `_cross_sectors`).

Interface (prescribed): `gold_input_census.handler_entry({"date": <page day>, "sink", "readings": []})`, status
arrived | covered_by_fallback | missing | stale, column `fallback` as ic-2 set it. A gics row the rankings classify
reads `arrived` (NULL fallback) or `covered_by_fallback` with `fallback` naming the rule: "other_fund" for (b); a value
beginning "g4" (e.g. "g4_prior") for (a) when it is not read as arrived. `missing` only where the rankings say
Unclassified. `gold_holding_contribution.handler_entry` unchanged.

Offline, local sink (page day 2026-10-02, as-of 2026-10-01). TXUE reports on 09-30 and 10-01, quantity 100, value
1000 -> 1010, no gics_sector in its file except O; BASG reports the same days. G4: date=2026-09-29 holds G (px_close,
Information Technology); date=2026-10-01 holds A (px_close, Energy).
  A: G4 row on the as-of day                       -> rankings g4;   census arrived (control);
  O: Health Care in TXUE's own file                -> rankings own;  census arrived (control);
  G: G4 sector only on 09-29                       -> rankings g4;   census today missing (limb a);
  K: TXUE keys it KKK_US_Equity with security_cusip 123456789; BASG keys the same security by its CUSIP 123456789 and
     states Financials                             -> rankings other_fund; census today missing (limb b);
  U: no sector in any file, no G4 row on any date  -> rankings Unclassified; census missing, NULL fallback (control).
  - (0) fixture: the rankings classify A g4, O own, G g4, K other_fund, and leave U unclassified;
  - (a) TXUE gics G reads arrived, or covered_by_fallback with a fallback beginning "g4";
  - (b) TXUE gics K reads covered_by_fallback with fallback other_fund;
  - (c) control: TXUE gics U reads missing with a NULL fallback;
  - (d) control: TXUE gics A and O read arrived with a NULL fallback.
FAIL at base: (a) and (b) FAIL (both read missing); (0), (c), (d) PASS."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, AS = "2026-10-02", "2026-10-01"
REV = "20261001T000000Z-aaaaaaaaaaaa"
DATES = ("2026-09-30", "2026-10-01")
# key: (name, TXUE's own gics_sector, security_cusip)
TXUE = {"AAA_US_Equity": ("Alpha", None, None), "OOO_US_Equity": ("Omicron", "Health Care", None),
        "GGG_US_Equity": ("Gamma", None, None), "KKK_US_Equity": ("Kappa", None, "123456789"),
        "UUU_US_Equity": ("Upsilon", None, None)}
SA, SO, SG, SK, SU = TXUE


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def read_out(s, res):
    import pandas as pd
    import pyarrow.parquet as pq
    uri = (res.get("outputs") or [None])[0]
    return pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else pd.DataFrame()


def null(x) -> bool:
    return x is None or x != x


def g1_rows(d, i):
    base = {"report_date": d, "is_cash_line": False, "position_type": "long", "asset_class": "Equity",
            "quantity": 100.0, "market_value": 1000.0 + 10.0 * i, "weight": 0.2, "raw_identifier": None,
            "security_bloomberg": None, "security_isin": None, "security_sedol": None, "provider_security_type": None,
            "dataset_revision": REV}
    rows = [dict(base, fund_id="TXUE", fund_ticker="TXUE", security_id=k, security_name=n, gics_sector=sec,
                 security_cusip=cu) for k, (n, sec, cu) in TXUE.items()]
    rows.append(dict(base, fund_id="BASG", fund_ticker="BASG", security_id="123456789", security_name="Kappa",
                     gics_sector="Financials", security_cusip="123456789"))
    return rows


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, sinks

    spec = f"local:{c.tmpdir('rv_cg1_')}"
    s = sinks.get_sink(spec)
    for i, d in enumerate(DATES):
        put_parquet(s, homes.canonical_shape(d, f"holdings-{REV}.parquet"), g1_rows(d, i))
    put_parquet(s, eb.market_target_uri("2026-09-29", "20260929T010000Z-bbbbbbbbbbbb"),
                [{"security_id": SG, "date": "2026-09-29", "px_close": 10.0, "gics_sector": "Information Technology"}])
    put_parquet(s, eb.market_target_uri(AS, "20261001T010000Z-cccccccccccc"),
                [{"security_id": SA, "date": AS, "px_close": 10.0, "gics_sector": "Energy"}])

    rk_res = hc.handler_entry({"date": PAGE, "sink": spec})
    rk = read_out(s, rk_res)
    sec = rk[(rk.get("axis") == "security") & (rk.get("fund_id") == "TXUE")] if len(rk) else rk
    src = {str(r.bucket): (None if null(r.sector_source) else str(r.sector_source)) for r in sec.itertuples()}
    print("rankings:", rk_res.get("status"), "| TXUE sector_source by security:", src)
    if len(rk):
        sct = rk[(rk.axis == "sector") & (rk.fund_id == "TXUE") & (rk.period == "MTD")]
        print("rankings TXUE MTD sectors:", sorted(str(b) for b in sct.bucket))
    v.check(src.get(SA) == "g4" and src.get(SO) == "own" and src.get(SG) == "g4" and src.get(SK) == "other_fund"
            and SU in src and src.get(SU) is None,
            "(0) fixture: the rankings classify A g4, O own, G g4 (older G4 date), K other_fund (shared CUSIP); U none")

    ic_res = ic.handler_entry({"date": PAGE, "sink": spec, "readings": []})
    out = read_out(s, ic_res)
    print("census:", ic_res.get("status"))
    cols = [k for k in ("fund_id", "input_kind", "subject", "status", "fallback", "reason") if k in out.columns]
    if len(out):
        print(out[out.input_kind == "gics"][cols].to_string(index=False))

    def row(subj):
        x = out[(out.fund_id == "TXUE") & (out.input_kind == "gics") & (out.subject == subj)] if len(out) else out
        return x.iloc[0].to_dict() if len(x) == 1 else {}

    g, k, u = row(SG), row(SK), row(SU)
    g_fb, k_fb = ("" if null(x.get("fallback")) else str(x.get("fallback")) for x in (g, k))
    v.check((g.get("status") == "arrived" and null(g.get("fallback")))
            or (g.get("status") == "covered_by_fallback" and g_fb.startswith("g4")),
            "(a) TXUE gics G (G4 sector on 09-29 only, rankings g4) reads arrived, or covered_by_fallback with a g4 "
            f"fallback (reads {g.get('status')}/{g_fb or 'NULL'})")
    v.check(k.get("status") == "covered_by_fallback" and k.get("fallback") == "other_fund",
            "(b) TXUE gics K (BASG states Financials under the shared CUSIP, rankings other_fund) reads "
            f"covered_by_fallback, fallback other_fund (reads {k.get('status')}/{k_fb or 'NULL'})")
    v.check(u.get("status") == "missing" and null(u.get("fallback")),
            "(c) control: TXUE gics U (the rankings leave it Unclassified) reads missing with a NULL fallback")
    v.check(all(row(x).get("status") == "arrived" and null(row(x).get("fallback")) for x in (SA, SO)),
            "(d) control: TXUE gics A (as-of G4 row) and O (own file) read arrived with a NULL fallback")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
