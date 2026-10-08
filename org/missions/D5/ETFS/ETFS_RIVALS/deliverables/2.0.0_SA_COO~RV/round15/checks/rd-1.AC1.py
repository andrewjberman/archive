"""RIV-rd-1 AC1 (PRD v0.19 C-OWED-GRAIN, G.4; CTO ruling R13; row ETFS_RIVALS-Z-S71 and worker row Z-W15-S2): THE READER READS A CLOSE ONLY
ON ITS OWN TRADING DAY. The shared G4 reader (`gold_holding_contribution.g4_rows` / `g4_window`, read by `price_series.load` and every
stage) (1) lets a row's price group (`px_close`, `total_return_index`, `currency`, `as_of`, `source`, `as_of_source`, `price_date`) take
part in the merge only where the row's `price_date` column is null or absent, or equals the partition date -- a row whose non-null
`price_date` is another day offers NO price group (its descriptive fields still coalesce); (2) on a date holding timed AND untimed objects,
lets the ONE untimed object `revision.newest` picks among the date's UNTIMED uris contribute its descriptive fields (sector, parsekey, name)
last in the order and NEVER a price group; other untimed objects are still not read; (3) lets `drop_backfill` keep a merged row whose price
group came from a backfill row when a non-backfill row supplied its descriptive fields: the row stays with the price group nulled, sector and
parsekey kept (`price_series.load` still receives the backfill close); a security whose every row is a backfill row is still dropped.

Fixture: G4 objects built with the producer's own schema (`enrichment_bloomberg._market_table`) plus a `price_date` column appended the way
the daily leg lands it (RIV-tw-1: the ISO trading date the vendor returned); the column's TYPE is not named by the cell, so arm (a) runs
twice, once with a date32 column and once with an ISO-string column. Every object sits on a `local:` sink.
  - (a) THE PRICE DATE, 2026-10-02, two timed objects: OK (close 10.0, price_date = the day, Energy); LATE (close 20.0, price_date
    2026-10-05, Utilities); EARLY (close 30.0, price_date 2026-10-01, Financials); TWO (the correctly dated close 41.0 in the EARLIER object,
    a close 40.0 dated 2026-10-05 in the LATER object -- at base the later one wins). `g4_rows`, `g4_window` and `price_series.load`: OK 10.0;
    LATE and EARLY have NO close but their sector arrives; TWO reads 41.0 (not 40.0);
  - (b) NULL / ABSENT price_date, read as today: 2026-10-01 holds a timed object WITH the column (null on its rows) and a later timed object
    WITHOUT the column (the later capture wins BOTH: 16.0), and 2026-09-25 holds two untimed objects with a null-price_date column (the
    `revision.newest` one is read, as before). Every close arrives by `g4_rows` and `price_series.load`. PASSES at base and keeps passing;
  - (c) THE UNTIMED DATE THAT GAINS A TIMED OBJECT, 2026-09-29: the named untimed pair `market-20260929-53bc393958bd.parquet` (closes: LVO,
    SHR, SHS, a CUSIP) and `market-20260929-afcd903ad844.parquet` (an import: SHR Health Care, SHS Utilities, IMO Information Technology, a
    CUSIP with a parsekey; no price) plus ONE timed top-up (SHS close 31.0, currency EUR, no sector). `g4_rows`, `g4_window` and
    `price_series.load`: the import's sectors and parsekey arrive for its securities (SHR, SHS, IMO, the CUSIP); NO close of the untimed pair
    arrives (SHR has none, LVO and the other CUSIP are absent); the timed close arrives whole (SHS 31.0 EUR, sector Utilities from the import);
    A second date, 2026-09-24, repeats the rule where the object `revision.newest` picks DOES hold a close: untimed `...-bbbbbbbbbbbb` (PRICED
    close 40.0, Industrials) and `...-aaaaaaaaaaaa` (OTHER), timed top-up TOPUP close 9.0 -> PRICED has its sector and no close, OTHER is
    absent, TOPUP 9.0;
  - (d) THE BACKFILL CLOSE, 2026-10-02: a security (a CUSIP, parsekey, GICS sector) whose live row has NO close and whose backfill row (later
    object, `as_of_source` backfill, price_date = the day) has 150.0; a second security with a live close; a third whose only row is a
    backfill row (sector and close). `price_series.load` returns the backfill closes; after `drop_backfill` -- on the merged frame, and on the
    frame the rankings stage `handler_entry` itself hands it (captured) -- the first security's row is STILL there with its sector and
    parsekey and a NULL `px_close`, the live-close security is untouched, the backfill-only security is still dropped, and `parsekey_map`
    still maps the CUSIP;
  - (e) one row per (security, date) over a two-day window, and a merged row's price group is never mixed across objects: a close with a
    NULL currency stays NULL (never the other object's EUR), and the later object's close travels with its own (null) currency, not the
    older object's USD. PASSES at base;
  - (f) REGRESSION: each of rg-2.AC1, rg-1.AC1, rg-1.AC2, rg-1.AC3, bk-1.AC1, bk-1.AC2, bk-1.AC3 and ps-1.AC1 ends `PASS 0 failures` run
    as its own process from the worktree root (all eight pass at base 361b735308); one arm per file, labelled `f:<file>`;
  - (g) CONTROL (PASSES at base): the fixtures are on the sink, `revision.capture_time` is None for the two untimed names and a time for the
    timed ones, `revision.newest` of the two untimed 2026-09-29 uris is the import, and `g4_rows` on a timed-only date returns the union.
FAIL at base 361b735308: (a), (c), (d) FAIL (a misdated close is read; the untimed date's sectors and parsekey are lost once a timed object lands; the backfill-closed security's row is dropped with its sector and parsekey); (b), (e), (f) all eight, (g) PASS.
At base 361b735308: AC1 RESULT: FAIL 3: a, c, d (measured).
"""
import concurrent.futures
import datetime as dt
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LIVE_SRC, HIST_SRC = "blp_client.reference_data", "blp_client.historical_data"
IMPORT_SRC = "import:bbg/2026-09-29/characteristics.parquet"
HERE = pathlib.Path(__file__).resolve().parent
REGRESSION = ("rg-2.AC1", "rg-1.AC1", "rg-1.AC2", "rg-1.AC3", "bk-1.AC1", "bk-1.AC2", "bk-1.AC3", "ps-1.AC1")
D29, DA, DB, DBU = "2026-09-29", "2026-10-02", "2026-10-01", "2026-09-25"
MISDATED_NAME, IMPORT_NAME = "market-20260929-53bc393958bd.parquet", "market-20260929-afcd903ad844.parquet"
LVO, SHR, SHS, IMO = "LVO_US_Equity", "SHR_US_Equity", "SHS_US_Equity", "IMO_US_Equity"
CUSIP, CUSIP_PK, ICUSIP, ICUSIP_PK = "N97284108", "NBIS US Equity", "037833100", "AAPL US Equity"
PAGE = "2026-10-05"
ENTS = [{"group_id": "IDVZ", "fund_id": "TXUE", "ticker": "TXUE", "role": "rival"}]


def mrow(eb, sec, date, px=None, tri=None, ccy=None, sector=None, source=LIVE_SRC, aos="pull", pk=None, pdate=None):
    """One G4 row in the producer's own column set; a column not named is NULL. `pdate` (ISO string or None) rides as the key `price_date`."""
    r = {col: None for col in eb.MARKET_COLUMNS}
    r.update(security_id=sec, security_bloomberg=sec.replace("_", " "), date=dt.date.fromisoformat(date), px_close=px,
             total_return_index=tri, currency=ccy, gics_sector=sector, source=source, as_of=dt.date.fromisoformat(date),
             as_of_source=aos, security_parsekey=pk, producer_version=eb.GOLD_VERSION, input_manifest="{}", claim="MEASURED",
             produced_at=f"{date}T01:00:00Z", price_date=pdate)
    return r


def put_obj(eb, s, date, name, rows, ptype=None):
    """One G4 object at the producer's own address. `ptype` None = no price_date column; 'date' = a date32 column; 'str' = an ISO-string column."""
    import pyarrow as pa
    rev = name[len("market-"):-len(".parquet")]
    uri = eb.market_target_uri(date, rev)
    t = eb._market_table([dict(r, revision=rev) for r in rows])
    if ptype == "date":
        t = t.append_column("price_date", pa.array([dt.date.fromisoformat(r["price_date"]) if r.get("price_date") else None for r in rows],
                                                   type=pa.date32()))
    elif ptype == "str":
        t = t.append_column("price_date", pa.array([r.get("price_date") for r in rows], type=pa.string()))
    s.put(uri, eb._parquet_bytes(t), "application/octet-stream")
    return uri


def isnull(x):
    if x is None:
        return True
    try:
        return bool(x != x)
    except Exception:  # noqa: BLE001
        return False


def near(a, b, tol=1e-9):
    return not isnull(a) and not isnull(b) and abs(float(a) - float(b)) < tol


def rows_by_sec(df):
    """A frame as ({security_id: {col: value}}, [duplicate security ids])."""
    out, dup = {}, []
    for r in df.to_dict("records"):
        k = str(r.get("security_id"))
        if k in out:
            dup.append(k)
        out[k] = r
    return out, dup


def px_of(g, k):
    return (g.get(k) or {}).get("px_close")


def day_price(ps, s, keys, d):
    """{key: close of day d} from price_series.load over [d, d]; None for an unpriced key."""
    out = ps.load(s, keys, dt.date.fromisoformat(d), dt.date.fromisoformat(d))
    got = {}
    for k in keys:
        pts = (out.get(k) or {}).get("points") or []
        got[k] = next((None if isnull(p[1]) else float(p[1]) for p in pts if str(p[0])[:10] == d), None)
    return got


def guard(v, label, desc, fn):
    """Run one arm; a raising reader is that arm's failure, never a dead check."""
    try:
        ok = fn()
    except Exception as e:  # noqa: BLE001
        print(f"  ({label}) raised {type(e).__name__}: {e}")
        ok = False
    v.check(bool(ok), f"({label}) {desc}")


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import price_series, revision, sinks

    def new_sink(tag):
        spec = f"local:{c.tmpdir(f'rv_rd1_{tag}_')}"
        return spec, sinks.get_sink(spec)

    def both_readers(s, d, cols):
        """(g4_rows by security, duplicates, g4_window by security) of one date; the window is read with `cols` (a stage's own column filter)."""
        g, dup = rows_by_sec(hc.g4_rows(s, d))
        win, _ = hc.g4_window(s, d, d, cols)
        w, wdup = rows_by_sec(win)
        return g, dup, w, wdup

    # ---- (a) the price date ------------------------------------------------------------------------------------------------
    def build_a(ptype, tag):
        _, s = new_sink(tag)
        d = DA
        put_obj(eb, s, d, "market-20261002T111000Z-aaaaaaaaaaaa.parquet", [
            mrow(eb, "OK_US_Equity", d, px=10.0, ccy="USD", sector="Energy", pdate=d),
            mrow(eb, "LATE_US_Equity", d, px=20.0, ccy="USD", sector="Utilities", pdate="2026-10-05"),
            mrow(eb, "EARLY_US_Equity", d, px=30.0, ccy="USD", sector="Financials", pdate="2026-10-01"),
            mrow(eb, "TWO_US_Equity", d, px=41.0, ccy="USD", sector="Materials", pdate=d)], ptype)
        put_obj(eb, s, d, "market-20261002T150000Z-bbbbbbbbbbbb.parquet", [
            mrow(eb, "TWO_US_Equity", d, px=40.0, ccy="USD", pdate="2026-10-05")], ptype)
        return s

    def arm_a_for(ptype):
        s = build_a(ptype, f"a_{ptype}")
        cols = ("security_id", "date", "px_close", "gics_sector")
        g, dup, w, wdup = both_readers(s, DA, cols)
        keys = ["OK_US_Equity", "LATE_US_Equity", "EARLY_US_Equity", "TWO_US_Equity"]
        px = day_price(price_series, s, keys, DA)
        print(f"  [{ptype}] g4_rows closes {({k: px_of(g, k) for k in keys})} | sectors "
              f"{({k: (g.get(k) or {}).get('gics_sector') for k in keys})} | window closes {({k: px_of(w, k) for k in keys})} | load {px}")
        ok = True
        for src in (g, w):
            ok = (ok and near(px_of(src, "OK_US_Equity"), 10.0) and isnull(px_of(src, "LATE_US_Equity"))
                  and isnull(px_of(src, "EARLY_US_Equity")) and near(px_of(src, "TWO_US_Equity"), 41.0)
                  and (src.get("LATE_US_Equity") or {}).get("gics_sector") == "Utilities"
                  and (src.get("EARLY_US_Equity") or {}).get("gics_sector") == "Financials")
        return (ok and not dup and not wdup and near(px["OK_US_Equity"], 10.0) and px["LATE_US_Equity"] is None
                and px["EARLY_US_Equity"] is None and near(px["TWO_US_Equity"], 41.0))

    def arm_a():
        res = [arm_a_for(p) for p in ("date", "str")]
        return all(res)

    guard(v, "a", "a close whose price_date is another day is read by no reader (g4_rows, g4_window, price_series.load: LATE and EARLY have no "
                  "close, their sector still arrives; TWO reads the correctly dated 41.0 not the later object's misdated 40.0); price_date as a "
                  "date32 column and as an ISO-string column", arm_a)

    # ---- (b) a null price_date and a missing column read as today -----------------------------------------------------------
    def arm_b():
        _, s = new_sink("b")
        d = DB
        put_obj(eb, s, d, "market-20261001T110000Z-aaaaaaaaaaaa.parquet", [
            mrow(eb, "NULLPD_US_Equity", d, px=11.0, ccy="USD", pdate=None), mrow(eb, "BOTH_US_Equity", d, px=15.0, ccy="USD", pdate=None)], "date")
        put_obj(eb, s, d, "market-20261001T150000Z-bbbbbbbbbbbb.parquet", [
            mrow(eb, "NOCOL_US_Equity", d, px=12.0, ccy="USD"), mrow(eb, "BOTH_US_Equity", d, px=16.0, ccy="USD")], None)
        u = DBU
        put_obj(eb, s, u, "market-20260925-bbbbbbbbbbbb.parquet", [mrow(eb, "UNT_US_Equity", u, px=13.0, ccy="USD", pdate=None)], "str")
        put_obj(eb, s, u, "market-20260925-aaaaaaaaaaaa.parquet", [mrow(eb, "OTHER_US_Equity", u, px=7.0, ccy="USD", pdate=None)], "str")
        g, dup = rows_by_sec(hc.g4_rows(s, d))
        gu, _ = rows_by_sec(hc.g4_rows(s, u))
        keys = ["NULLPD_US_Equity", "NOCOL_US_Equity", "BOTH_US_Equity"]
        px = day_price(price_series, s, keys, d)
        pxu = day_price(price_series, s, ["UNT_US_Equity", "OTHER_US_Equity"], u)
        print(f"  {d} g4_rows {({k: px_of(g, k) for k in keys})} dup {dup} | load {px} | {u} untimed pair g4_rows {sorted(gu)} | load {pxu}")
        return (near(px_of(g, "NULLPD_US_Equity"), 11.0) and near(px_of(g, "NOCOL_US_Equity"), 12.0) and near(px_of(g, "BOTH_US_Equity"), 16.0)
                and not dup and near(px["NULLPD_US_Equity"], 11.0) and near(px["NOCOL_US_Equity"], 12.0) and near(px["BOTH_US_Equity"], 16.0)
                and near(px_of(gu, "UNT_US_Equity"), 13.0) and "OTHER_US_Equity" not in gu and near(pxu["UNT_US_Equity"], 13.0))

    guard(v, "b", "a row with a null price_date, an object with no price_date column, and an untimed date with a null-price_date column are "
                  "read exactly as today (their closes arrive; the later capture wins; one object on the untimed date)", arm_b)

    # ---- (c) the untimed date that gains a timed object ---------------------------------------------------------------------
    def build_c(tag):
        spec, s = new_sink(tag)
        d = D29
        live = put_obj(eb, s, d, MISDATED_NAME, [
            mrow(eb, LVO, d, px=50.0, tri=0.4, ccy="USD", sector="Energy"), mrow(eb, SHR, d, px=20.0, tri=0.1, ccy="USD"),
            mrow(eb, SHS, d, px=30.0, ccy="USD", sector="Financials"), mrow(eb, CUSIP, d, px=5.0, ccy="USD", pk=CUSIP_PK)])
        imp = put_obj(eb, s, d, IMPORT_NAME, [
            mrow(eb, SHR, d, sector="Health Care", source=IMPORT_SRC, aos=None), mrow(eb, SHS, d, sector="Utilities", source=IMPORT_SRC, aos=None),
            mrow(eb, IMO, d, sector="Information Technology", source=IMPORT_SRC, aos=None),
            mrow(eb, ICUSIP, d, source=IMPORT_SRC, aos=None, pk=ICUSIP_PK)])
        top = put_obj(eb, s, d, "market-20260929T150000Z-cccccccccccc.parquet", [mrow(eb, SHS, d, px=31.0, ccy="EUR", pdate=d)], "date")
        return spec, s, live, imp, top

    def arm_c():
        _, s, live, imp, top = build_c("c")
        pick = revision.newest([live, imp])
        cols = ("security_id", "date", "px_close", "currency", "gics_sector", "security_parsekey")
        g, dup, w, wdup = both_readers(s, D29, cols)
        keys = [LVO, SHR, SHS, IMO, CUSIP, ICUSIP]
        px = day_price(price_series, s, keys, D29)
        win, _ = hc.g4_window(s, D29, D29, cols)
        pk = hc.parsekey_map(win)
        print(f"  revision.newest of the two untimed uris: {pick.rsplit('/', 1)[-1]} | g4_rows securities {sorted(g)} (duplicates {dup}) | "
              f"closes {({k: px_of(g, k) for k in sorted(g)})} | load {px}")
        print(f"  sectors {({k: x.get('gics_sector') for k, x in sorted(g.items())})} | SHS currency {(g.get(SHS) or {}).get('currency')!r} | "
              f"window parsekey_map {pk}")
        want = sorted([SHR, SHS, IMO, ICUSIP])
        ok = pick == imp and sorted(g) == want and not dup and sorted(w) == want and not wdup
        for src in (g, w):
            ok = (ok and (src.get(SHR) or {}).get("gics_sector") == "Health Care" and isnull(px_of(src, SHR))
                  and (src.get(SHS) or {}).get("gics_sector") == "Utilities" and near(px_of(src, SHS), 31.0)
                  and (src.get(SHS) or {}).get("currency") == "EUR"
                  and (src.get(IMO) or {}).get("gics_sector") == "Information Technology" and isnull(px_of(src, IMO))
                  and (src.get(ICUSIP) or {}).get("security_parsekey") == ICUSIP_PK and isnull(px_of(src, ICUSIP)))
        ok = (ok and px[SHS] == 31.0 and all(px[k] is None for k in (LVO, SHR, IMO, CUSIP, ICUSIP))
              and pk.get(ICUSIP) == ICUSIP_PK.replace(" ", "_") and CUSIP not in pk)
        # the same rule where the object revision.newest picks DOES hold a close: its sector arrives, its close does not
        _, s2 = new_sink("c2")
        d = "2026-09-24"
        priced = put_obj(eb, s2, d, "market-20260924-bbbbbbbbbbbb.parquet", [mrow(eb, "PRICED_US_Equity", d, px=40.0, ccy="USD", sector="Industrials")])
        other = put_obj(eb, s2, d, "market-20260924-aaaaaaaaaaaa.parquet", [mrow(eb, "OTHER_US_Equity", d, px=7.0, ccy="USD", sector="Utilities")])
        put_obj(eb, s2, d, "market-20260924T150000Z-cccccccccccc.parquet", [mrow(eb, "TOPUP_US_Equity", d, px=9.0, ccy="USD", pdate=d)], "date")
        g2, dup2 = rows_by_sec(hc.g4_rows(s2, d))
        px2 = day_price(price_series, s2, ["PRICED_US_Equity", "OTHER_US_Equity", "TOPUP_US_Equity"], d)
        print(f"  {d}: revision.newest of the untimed pair {revision.newest([priced, other]).rsplit('/', 1)[-1]} (the priced one is ...-bbbbbbbbbbbb) | "
              f"g4_rows {sorted(g2)} (duplicates {dup2}) | PRICED close {px_of(g2, 'PRICED_US_Equity')} sector "
              f"{(g2.get('PRICED_US_Equity') or {}).get('gics_sector')!r} | load {px2}")
        return (ok and revision.newest([priced, other]) == priced and sorted(g2) == ["PRICED_US_Equity", "TOPUP_US_Equity"] and not dup2
                and isnull(px_of(g2, "PRICED_US_Equity")) and (g2.get("PRICED_US_Equity") or {}).get("gics_sector") == "Industrials"
                and near(px_of(g2, "TOPUP_US_Equity"), 9.0) and px2["PRICED_US_Equity"] is None and px2["OTHER_US_Equity"] is None
                and near(px2["TOPUP_US_Equity"], 9.0))

    guard(v, "c", "a date of two untimed objects that gains a timed top-up keeps the sectors and parsekey of the untimed object revision.newest "
                  "picks (SHR, SHS, IMO, the CUSIP), reads NO close from an untimed object (SHR none; LVO and the other CUSIP absent) and reads "
                  "the timed close whole (SHS 31.0 EUR); and where the picked untimed object itself holds a close (2026-09-24: PRICED 40.0, Industrials, beside an untimed OTHER and a timed TOPUP 9.0) its sector arrives and its close does not", arm_c)

    # ---- (d) the backfill close ---------------------------------------------------------------------------------------------
    def build_d(tag):
        spec, s = new_sink(tag)
        d = DA
        put_obj(eb, s, d, "market-20261002T110000Z-aaaaaaaaaaaa.parquet", [
            mrow(eb, ICUSIP, d, px=None, sector="Information Technology", pk=ICUSIP_PK, pdate=None),
            mrow(eb, "LIVE_US_Equity", d, px=25.0, ccy="USD", sector="Industrials", pdate=d)], "date")
        put_obj(eb, s, d, "market-20261002T150000Z-bbbbbbbbbbbb.parquet", [
            mrow(eb, ICUSIP, d, px=150.0, ccy="USD", source=HIST_SRC, aos="backfill", pdate=d),
            mrow(eb, "ALLBF_US_Equity", d, px=7.0, ccy="USD", sector="Financials", source=HIST_SRC, aos="backfill", pdate=d)], "date")
        return spec, s

    def judge_d(label, frame):
        """The post-drop_backfill frame: the first security kept with sector and parsekey and a NULL close; LIVE untouched; ALLBF gone."""
        got, dup = rows_by_sec(frame)
        pk = hc.parsekey_map(frame)
        r, live = got.get(ICUSIP) or {}, got.get("LIVE_US_Equity") or {}
        print(f"  {label}: securities {sorted(got)} (duplicates {dup}) | CUSIP row sector {r.get('gics_sector')!r} parsekey "
              f"{r.get('security_parsekey')!r} px_close {r.get('px_close')!r} | LIVE px {live.get('px_close')} | parsekey_map {pk}")
        return (ICUSIP in got and "ALLBF_US_Equity" not in got and not dup and r.get("gics_sector") == "Information Technology"
                and r.get("security_parsekey") == ICUSIP_PK and isnull(r.get("px_close")) and near(live.get("px_close"), 25.0)
                and pk.get(ICUSIP) == ICUSIP_PK.replace(" ", "_"))

    def arm_d():
        spec, s = build_d("d")
        px = day_price(price_series, s, [ICUSIP, "ALLBF_US_Equity", "LIVE_US_Equity"], DA)
        print(f"  price_series.load closes {px}")
        ok = near(px[ICUSIP], 150.0) and near(px["ALLBF_US_Equity"], 7.0) and near(px["LIVE_US_Equity"], 25.0)
        merged = hc.g4_rows(s, DA)
        ok = judge_d("drop_backfill(g4_rows)", hc.drop_backfill(merged)) and ok
        # the frame the rankings stage hands drop_backfill, captured while handler_entry runs (the stage's own column filter and call)
        seen = []
        orig = hc.drop_backfill

        def spy(g4):
            out = orig(g4)
            seen.append(out)
            return out

        hc.drop_backfill = spy
        hc.universe.entries = lambda: list(ENTS)
        try:
            hc.handler_entry({"date": PAGE, "sink": spec})
        except Exception as e:  # noqa: BLE001 -- only the captured frame matters; the build with no G1 may refuse
            print(f"  handler_entry raised after the read: {type(e).__name__}: {e}")
        finally:
            hc.drop_backfill = orig
        if not seen:
            print("  handler_entry never called drop_backfill")
            return False
        window = seen[0][seen[0]["date"].map(lambda x: str(x)[:10]) == DA] if "date" in seen[0].columns else seen[0]
        return judge_d("handler_entry's drop_backfill output", window) and ok

    guard(v, "d", "a security whose live row has no close and whose backfill row has one: price_series.load returns the backfill close; after "
                  "drop_backfill (on the merged frame and on the frame handler_entry hands it) the row is still there with its sector and "
                  "parsekey and a null px_close and parsekey_map maps it; a live-close security is untouched; a backfill-only security is dropped", arm_d)

    # ---- (e) one row per (security, date); the price group never mixed across objects -------------------------------------------
    def arm_e():
        _, s = new_sink("e")
        d1, d2 = "2026-10-05", "2026-10-06"
        for d in (d1, d2):
            put_obj(eb, s, d, f"market-{d.replace('-', '')}T100000Z-aaaaaaaaaaaa.parquet", [
                mrow(eb, "X_US_Equity", d, px=100.0, ccy=None, pdate=d), mrow(eb, "Y_US_Equity", d, px=50.0, ccy="USD", pdate=d)], "date")
            put_obj(eb, s, d, f"market-{d.replace('-', '')}T140000Z-bbbbbbbbbbbb.parquet", [
                mrow(eb, "X_US_Equity", d, px=None, ccy="EUR", pdate=None), mrow(eb, "Y_US_Equity", d, px=55.0, ccy=None, pdate=d)], "date")
        win, _ = hc.g4_window(s, d1, d2)
        keys = [(str(r["security_id"]), str(r["date"])[:10]) for r in win.to_dict("records")]
        by = {(str(r["security_id"]), str(r["date"])[:10]): r for r in win.to_dict("records")}
        x, y = by.get(("X_US_Equity", d2)) or {}, by.get(("Y_US_Equity", d2)) or {}
        print(f"  window rows {len(keys)} unique {len(set(keys))} | X close {x.get('px_close')} currency {x.get('currency')!r} | "
              f"Y close {y.get('px_close')} currency {y.get('currency')!r}")
        return (len(keys) == 4 and len(set(keys)) == 4 and near(x.get("px_close"), 100.0) and isnull(x.get("currency"))
                and near(y.get("px_close"), 55.0) and isnull(y.get("currency")))

    guard(v, "e", "one row per (security, date) over a two-day window; a close keeps its own currency (X 100.0 with NULL currency, never the "
                  "other object's EUR; Y 55.0 with NULL currency, never the older object's USD)", arm_e)

    # ---- (g) control (before the regression arms so a dead fixture is visible) -------------------------------------------------
    def arm_g():
        _, s2, live, imp, top = build_c("g")
        d = "2026-10-06"
        c1 = put_obj(eb, s2, d, "market-20261006T100000Z-aaaaaaaaaaaa.parquet", [mrow(eb, "P1_US_Equity", d, px=1.0, ccy="USD")])
        c2 = put_obj(eb, s2, d, "market-20261006T140000Z-bbbbbbbbbbbb.parquet", [mrow(eb, "P2_US_Equity", d, px=2.0, ccy="USD")])
        listed = sorted(u for u in s2.list(eb.market_target_uri(D29, "x").rsplit("/", 1)[0] + "/") if u.endswith(".parquet"))
        times = {u.rsplit("/", 1)[-1]: revision.capture_time(u) for u in (live, imp, top, c1, c2)}
        union, _ = rows_by_sec(hc.g4_rows(s2, d))
        print(f"  listed on 2026-09-29: {len(listed)} | capture_time {times} | revision.newest of the untimed pair: "
              f"{revision.newest([live, imp]).rsplit('/', 1)[-1]} | timed-only g4_rows {sorted(union)}")
        return (len(listed) == 3 and times[MISDATED_NAME] is None and times[IMPORT_NAME] is None
                and times["market-20260929T150000Z-cccccccccccc.parquet"] is not None
                and times["market-20261006T100000Z-aaaaaaaaaaaa.parquet"] is not None and revision.newest([live, imp]) == imp
                and sorted(union) == ["P1_US_Equity", "P2_US_Equity"] and near(px_of(union, "P1_US_Equity"), 1.0)
                and near(px_of(union, "P2_US_Equity"), 2.0))

    guard(v, "g", "control: the fixtures are on the sink; capture_time is None for the two untimed names and a time for the timed ones; "
                  "revision.newest of the untimed pair is the import; g4_rows on a timed-only date returns the union", arm_g)

    # ---- (f) the neighbouring checks, each its own process, run together ------------------------------------------------------
    def run_one(name):
        path = HERE / f"{name}.py"
        p = subprocess.run([sys.executable, str(path)], cwd=str(c.ROOT), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=480)
        lines = [ln.strip() for ln in (p.stdout or "").splitlines() if ln.strip()]
        return p.returncode, (lines[-1] if lines else "")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futs = {n: pool.submit(run_one, n) for n in REGRESSION}
    for name in REGRESSION:
        def arm(name=name):
            ac = name.split(".")[1]
            rc, last = futs[name].result()
            print(f"  {name}: rc {rc} | last line: {last}")
            return rc == 0 and last == f"{ac} RESULT: PASS 0 failures"

        guard(v, f"f:{name}", f"{name} still ends PASS 0 failures (own process, worktree root)", arm)


v = c.Verdict("AC1")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- a dead fixture is a failed check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = [m.split(")")[0].lstrip("(") for m in v.fails]
print("AC1 RESULT: PASS 0 failures" if not v.fails else f"AC1 RESULT: FAIL {len(v.fails)}: {', '.join(labels)}")
sys.exit(0 if not v.fails else 1)
