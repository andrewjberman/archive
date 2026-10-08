"""RIV-rg-1 AC2 (PRD v0.19 C-OWED-GRAIN, G.4; row ETFS_RIVALS-Z-S69; CTO term msg 31432 -- the AMENDED interface item 1): THE RULE on the one
shared function. Where several objects of a date hold the same (security_id, date), the rows are ordered (a) non-backfill before
backfill, (b) `source` not starting "import:" before an import row, (c) the later capture time in the object's name (every object
that reaches the union carries one: RIV-rg-2), (d) the later row `as_of`, (e) the object name descending. The merged row is built in TWO parts: THE PRICE GROUP
(`px_close`, `total_return_index`, `currency`, `as_of`, `source`, `as_of_source`) travels WHOLE from the first row in the order whose
`px_close` is not null (none has a close: the first row in the order) -- a close is never combined with a currency, price date or
price source of another object, even when its own currency is null; THE DESCRIPTIVE FIELDS (every other column) each take the
first non-null value in the order. A column an older object lacks reads as null for its rows. THIS CHECK GRADES THE AMENDED RULE.

Discovery (the cell does not name the function): the check looks for a callable named, in this order, `g4_rows`, `g4_union`, `read_g4`,
`g4_by_date`, `union_g4`, on the modules `rivalfunds.gold_holding_contribution`, `rivalfunds.price_series`, `rivalfunds.revision`, then
`rivalfunds.g4_read`, `rivalfunds.security_market` if they exist (first hit in name order, modules in that order). It is called as
`fn(s, "<date>")`, else `fn(s, "<date>", "<date>")`, else `fn(s, <datetime.date>)`, `s` being the `local:` sink, and its result is
taken as a DataFrame, a list of row dicts, a {security_id: row} dict or a {date: DataFrame | rows} dict. Only arms g and h need it.
EVERY OTHER ARM GRADES THE RULE THROUGH READERS, not through the name: `price_series.load` (`px_close` and `currency` of the merged
row, per day) and `gold_canonical_shape._g4_for(s, date, {})` (its `rows[security_id]` holds the merged row's every column; it leaves
backfill-marked rows out, as today, so no `_g4_for` fixture holds a backfill row).

Fixture: one `local:` sink, G4 objects built with the producer's own schema (`enrichment_bloomberg._market_table`), one scenario per date,
a security key per case:
  09-08 (a)  K1 close 100.0 in a non-backfill object (T10:00Z) and close 90.0 in a backfill object with the LATER name (T12:00Z); K2 only
             in the backfill object (close 80.0)
  09-09 (b)  K1 close 100.0 in a live object T10:00Z and 95.0 in an import (`source` "import:...") T13:00Z; K2 the same pair with the
             later name an import (`market-20260909T101500Z-53bc...` live 50.0, `market-20260909T131500Z-afcd...` import 45.0)
  09-10 (c)  K1 100.0 in `...T10:00Z-ffffffffffff` and 101.0 in `...T14:00Z-aaaaaaaaaaaa` (the later time wins though its hash sorts
             first); K2 50.0 in an EARLIER object (`...T09:00Z-ffffffffffff`) and 51.0 in the T14:00Z object
  09-11 (o)  K1 100.0 as_of 09-11 in `...T10:00Z-aaaaaaaaaaaa` and 101.0 as_of 09-10 in `...T10:00Z-bbbbbbbbbbbb` (same capture time:
             the later as_of wins); K2 identical in both but the close (200.0 / 201.0): everything ties and the name descending decides
  09-14 (d1) K1: live at T08:00Z, close 100.0, currency NULL, source live + import at T09:00Z with close NULL, currency "EUR" (the
             import's time is later); K1b: the same shape with two live objects, the older holding currency "EUR" and no close
  09-15 (d2) K1: newer live object (T14:00Z) close NULL, currency NULL, source blp_client.reference_data, as_of_source "pull"; older live
             object (T10:00Z) close 100.0, currency "USD", total return 0.5, source blp_client.historical_data, as_of_source
             "historical", as_of 09-14: the group comes whole from the older row; K2: neither row has a close: the group is the newer
             row's (currency "USD", total return 0.3), not a mix; K3: close in the newer row, GICS NULL in it, GICS "Energy" and parsekey
             "KK US Equity" only in the older row: the descriptive fields coalesce, the price group does not
  09-16 (f)  an OLD object (T10:00Z) written WITHOUT the columns as_of_source, security_parsekey, currency and total_return_index
             (K1 close 100.0, sector Energy) and a newer object (T14:00Z) with K1 (close NULL, currency "USD", parsekey "KK US Equity")
             and K2 (close 60.0, currency "USD", as_of_source "pull")
  09-18 (g)  three objects (T10:00Z, T12:00Z, T14:00Z) each holding K1 and K2, the last also K3
  - (a)..(f) and (o): by reader, as listed above; (c) is a control that already passes at the base; (d) grades the price group whole -- close 100.0 with currency NULL, never "EUR" (d1, both
    shapes); the group of an older row whole when the first row has no close (d2 K1: close, currency, total return); the first row
    when none has a close (d2 K2) -- and the descriptive coalesce (d2 K3: close from the newer row, GICS and parsekey from the older);
  - (e) the merged row's `source`, `as_of`, `as_of_source` are those of the row that supplied `px_close` (d2 K1: historical /
    09-14 / "historical", not the newer row's "pull"), read from `_g4_for` rows;
  - (f) an old object lacking columns does not break the read and reads as null there (K1's currency and as_of_source NULL from the
    old row, its parsekey from the newer one; K2 intact); a reader that raises fails the arm;
  - (g) [discovered function] exactly one row per (security_id, date) on the three-object date: 3 rows (K1, K2, K3);
  - (h) [discovered function] its merged row for 09-15 K1 equals the price group of the older row whole and the descriptive fields
    of the first non-null (K3: GICS "Energy" from the older row);
  - (i) control (PASSES at base): every planted object is on the sink and `revision.newest` picks the object its docstring says (the
    later capture time; a live object over an import for provenance records) on the 09-10 and 09-15 dates.
FAIL at base 4611085187: (a), (b), (o), (d), (e), (f), (g), (h) FAIL (AC2 RESULT: FAIL 8: a, b, o, d, e, f, g, h; g and h because no shared
function exists); (c) and (i) PASS (the later capture time already decides between two timed live objects).

Amended for RIV-rg-2 (round 26; row ETFS_RIVALS-Z-S71): the merged union now reads ONLY objects whose name carries a capture time, and a
date with timed AND untimed objects is the union of the timed only. Three fixtures relied on the union reading an untimed name; each is
renamed with a capture time, keeping the content and the ordering each arm tests (the untimed-not-read rule is graded in rg-2.AC1, not
here):
  09-09 (b)  the K2 pair `market-20260909-53bc...` (live 50.0) and `market-20260909-afcd...` (import 45.0) are now
             `market-20260909T101500Z-53bc...` and `market-20260909T131500Z-afcd...`; arm b unchanged (live beats import);
  09-10 (c)  the K2 50.0 object `market-20260910-ffffffffffff` (a name with no time, "oldest") is now `market-20260910T090000Z-ffffffffffff`
             (an earlier time, still the oldest); the sub-assertion "a name with no time is oldest" is DROPPED -- an untimed name no
             longer takes part in the order -- and arm c grades "the later capture time wins" alone (K1 101.0, K2 51.0);
  09-14 (d1) the K1 pair `market-20260914-53bc...` (live, close 100.0, currency NULL) and `market-20260914-afcd...` (import, close NULL,
             currency "EUR") are now `market-20260914T080000Z-53bc...` and `market-20260914T090000Z-afcd...`; arm d unchanged.
Arm i indexes planted objects by position and is unaffected (each date keeps its object count and order). No arm label changed.
At base bff3ec2e7f (RIV-rg-1 merged, RIV-rg-2 not built): AC2 RESULT: PASS 0 failures (measured; the merged union reads timed names).
"""
import datetime as dt
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LIVE, HIST, IMP = "blp_client.reference_data", "blp_client.historical_data", "import:bbg/characteristics.parquet"
FN_NAMES = ("g4_rows", "g4_union", "read_g4", "g4_by_date", "union_g4")
FN_MODS = ("gold_holding_contribution", "price_series", "revision", "g4_read", "security_market")
AMEND = ("the worker must expose the shared function under one of the names g4_rows, g4_union, read_g4, g4_by_date, union_g4 "
         "(on gold_holding_contribution, price_series, revision, g4_read or security_market), callable as fn(s, 'YYYY-MM-DD'); "
         "the issuer will accept an amendment naming another")


def mrow(eb, sec, date, px=None, tri=None, ccy=None, sector=None, source=LIVE, aos="pull", pk=None, as_of=None):
    r = {col: None for col in eb.MARKET_COLUMNS}
    r.update(security_id=sec, security_bloomberg=sec.replace("_", " "), date=dt.date.fromisoformat(date), px_close=px,
             total_return_index=tri, currency=ccy, gics_sector=sector, source=source,
             as_of=dt.date.fromisoformat(as_of or date), as_of_source=aos, security_parsekey=pk,
             producer_version=eb.GOLD_VERSION, input_manifest="{}", claim="MEASURED", produced_at=f"{date}T01:00:00Z")
    return r


def put_obj(eb, s, date, name, rows, drop=()):
    rev = name[len("market-"):-len(".parquet")]
    uri = eb.market_target_uri(date, rev)
    t = eb._market_table([dict(r, revision=rev) for r in rows])
    if drop:
        t = t.select([n for n in t.column_names if n not in drop])
    s.put(uri, eb._parquet_bytes(t), "application/octet-stream")
    return uri


def isnull(x):
    if x is None:
        return True
    try:
        return bool(x != x)
    except Exception:  # noqa: BLE001
        return False


def day10(x):
    return None if isnull(x) else str(x)[:10]


def near(a, b, tol=1e-9):
    return not isnull(a) and not isnull(b) and abs(float(a) - float(b)) < tol


def guard(v, label, desc, fn):
    try:
        ok = fn()
    except Exception as e:  # noqa: BLE001
        print(f"  ({label}) raised {type(e).__name__}: {e}")
        ok = False
    v.check(bool(ok), f"({label}) {desc}")


def plant(eb, s):
    """All scenarios on one sink. Returns {date: [uris]}."""
    u = {}
    d = "2026-09-08"
    u[d] = [put_obj(eb, s, d, "market-20260908T100000Z-aaaaaaaaaaaa.parquet", [mrow(eb, "K1", d, px=100.0, ccy="USD")]),
            put_obj(eb, s, d, "market-20260908T120000Z-bbbbbbbbbbbb.parquet",
                    [mrow(eb, "K1", d, px=90.0, ccy="USD", aos="backfill", source=HIST), mrow(eb, "K2", d, px=80.0, ccy="USD", aos="backfill", source=HIST)])]
    d = "2026-09-09"
    u[d] = [put_obj(eb, s, d, "market-20260909T100000Z-aaaaaaaaaaaa.parquet", [mrow(eb, "K1", d, px=100.0, ccy="USD")]),
            put_obj(eb, s, d, "market-20260909T130000Z-bbbbbbbbbbbb.parquet", [mrow(eb, "K1", d, px=95.0, ccy="USD", source=IMP, aos=None)]),
            put_obj(eb, s, d, "market-20260909T101500Z-53bc393958bd.parquet", [mrow(eb, "K2", d, px=50.0, ccy="USD")]),
            put_obj(eb, s, d, "market-20260909T131500Z-afcd903ad844.parquet", [mrow(eb, "K2", d, px=45.0, ccy="USD", source=IMP, aos=None)])]
    d = "2026-09-10"
    u[d] = [put_obj(eb, s, d, "market-20260910T100000Z-ffffffffffff.parquet", [mrow(eb, "K1", d, px=100.0, ccy="USD")]),
            put_obj(eb, s, d, "market-20260910T140000Z-aaaaaaaaaaaa.parquet",
                    [mrow(eb, "K1", d, px=101.0, ccy="USD"), mrow(eb, "K2", d, px=51.0, ccy="USD")]),
            put_obj(eb, s, d, "market-20260910T090000Z-ffffffffffff.parquet", [mrow(eb, "K2", d, px=50.0, ccy="USD")])]
    d = "2026-09-11"
    u[d] = [put_obj(eb, s, d, "market-20260911T100000Z-aaaaaaaaaaaa.parquet",
                    [mrow(eb, "K1", d, px=100.0, ccy="USD", as_of=d), mrow(eb, "K2", d, px=200.0, ccy="USD", as_of=d)]),
            put_obj(eb, s, d, "market-20260911T100000Z-bbbbbbbbbbbb.parquet",
                    [mrow(eb, "K1", d, px=101.0, ccy="USD", as_of="2026-09-10"), mrow(eb, "K2", d, px=201.0, ccy="USD", as_of=d)])]
    d = "2026-09-14"
    u[d] = [put_obj(eb, s, d, "market-20260914T080000Z-53bc393958bd.parquet", [mrow(eb, "K1", d, px=100.0, ccy=None)]),
            put_obj(eb, s, d, "market-20260914T090000Z-afcd903ad844.parquet", [mrow(eb, "K1", d, px=None, ccy="EUR", source=IMP, aos=None)]),
            put_obj(eb, s, d, "market-20260914T100000Z-aaaaaaaaaaaa.parquet", [mrow(eb, "K1b", d, px=None, ccy="EUR")]),
            put_obj(eb, s, d, "market-20260914T140000Z-bbbbbbbbbbbb.parquet", [mrow(eb, "K1b", d, px=70.0, ccy=None)])]
    d = "2026-09-15"
    u[d] = [put_obj(eb, s, d, "market-20260915T100000Z-aaaaaaaaaaaa.parquet", [
                mrow(eb, "K1", d, px=100.0, tri=0.5, ccy="USD", source=HIST, aos="historical", as_of="2026-09-14"),
                mrow(eb, "K2", d, px=None, tri=0.9, ccy="EUR", source=HIST, aos="historical", as_of="2026-09-14"),
                mrow(eb, "K3", d, px=10.0, ccy="USD", sector="Energy", pk="KK US Equity", source=HIST, aos="historical", as_of="2026-09-14")]),
            put_obj(eb, s, d, "market-20260915T140000Z-bbbbbbbbbbbb.parquet", [
                mrow(eb, "K1", d, px=None, ccy=None, source=LIVE, aos="pull"),
                mrow(eb, "K2", d, px=None, tri=0.3, ccy="USD", source=LIVE, aos="pull"),
                mrow(eb, "K3", d, px=11.0, ccy="USD", sector=None, source=LIVE, aos="pull")])]
    d = "2026-09-16"
    u[d] = [put_obj(eb, s, d, "market-20260916T100000Z-aaaaaaaaaaaa.parquet",
                    [mrow(eb, "K1", d, px=100.0, sector="Energy")], drop=("as_of_source", "security_parsekey", "currency", "total_return_index")),
            put_obj(eb, s, d, "market-20260916T140000Z-bbbbbbbbbbbb.parquet",
                    [mrow(eb, "K1", d, px=None, ccy="USD", pk="KK US Equity"), mrow(eb, "K2", d, px=60.0, ccy="USD", aos="pull")])]
    d = "2026-09-18"
    u[d] = [put_obj(eb, s, d, f"market-20260918T{t}Z-{h * 12}.parquet",
                    [mrow(eb, "K1", d, px=10.0 + i, ccy="USD"), mrow(eb, "K2", d, px=20.0 + i, ccy="USD")]
                    + ([mrow(eb, "K3", d, px=30.0, ccy="USD")] if i == 2 else []))
            for i, (t, h) in enumerate((("100000", "a"), ("120000", "b"), ("140000", "c")))]
    return u


def find_fn():
    """(callable, 'module.name') by the documented convention, or (None, None)."""
    for name in FN_NAMES:
        for m in FN_MODS:
            try:
                mod = importlib.import_module(f"rivalfunds.{m}")
            except ImportError:
                continue
            fn = getattr(mod, name, None)
            if callable(fn):
                return fn, f"rivalfunds.{m}.{name}"
    return None, None


def rows_of(res):
    """A function's result as a list of row dicts, whatever the container."""
    import pandas as pd
    if isinstance(res, pd.DataFrame):
        return res.to_dict("records")
    if isinstance(res, dict):
        out = []
        for k, val in res.items():
            if isinstance(val, pd.DataFrame):
                out += val.to_dict("records")
            elif isinstance(val, list):
                out += [r for r in val if isinstance(r, dict)]
            elif isinstance(val, dict):
                out.append(val if "security_id" in val else dict(val, security_id=k))
        return out
    if isinstance(res, (list, tuple)):
        return [r for r in res if isinstance(r, dict)]
    raise TypeError(f"unreadable result type {type(res).__name__}")


def call_fn(fn, s, d):
    last = None
    for args in ((s, d), (s, d, d), (s, dt.date.fromisoformat(d))):
        try:
            rows = rows_of(fn(*args))
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            continue
        if rows:
            return rows
        last = "returned no rows"
    raise RuntimeError(f"could not read {d} through the discovered function ({last})")


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_canonical_shape as g1mod
    from rivalfunds import price_series, revision, sinks

    spec = f"local:{c.tmpdir('rv_rg1_ac2_')}"
    s = sinks.get_sink(spec)
    planted = plant(eb, s)

    def px(d, keys):
        out = price_series.load(s, keys, dt.date.fromisoformat(d), dt.date.fromisoformat(d))
        got, ccy = {}, {}
        for k in keys:
            pts = (out.get(k) or {}).get("points") or []
            got[k] = next((None if isnull(p[1]) else float(p[1]) for p in pts if str(p[0])[:10] == d), None)
            ccy[k] = (out.get(k) or {}).get("currency")
        return got, ccy

    def g4(d):
        g = g1mod._g4_for(s, d, {})
        return (g or {}).get("rows") or {}

    # (a) non-backfill over backfill, even when the backfill object's name is newer
    def arm_a():
        got, _ = px("2026-09-08", ["K1", "K2"])
        print(f"  09-08 load: {got}")
        return near(got["K1"], 100.0) and near(got["K2"], 80.0)

    guard(v, "a", "a non-backfill row beats a backfill row though the backfill object's name is newer (K1 100.0 not 90.0); a "
                  "backfill-only security stays priced for the chart (K2 80.0)", arm_a)

    # (b) live over import, whatever the import's name or time
    def arm_b():
        got, _ = px("2026-09-09", ["K1", "K2"])
        print(f"  09-09 load: {got}")
        return near(got["K1"], 100.0) and near(got["K2"], 50.0)

    guard(v, "b", "a live row beats an import row though the import's name sorts later (K1 100.0 not 95.0; K2 50.0 not 45.0)", arm_b)

    # (c) later capture time in the name; a name with no time is oldest
    def arm_c():
        got, _ = px("2026-09-10", ["K1", "K2"])
        print(f"  09-10 load: {got}")
        return near(got["K1"], 101.0) and near(got["K2"], 51.0)

    guard(v, "c", "between live objects the later capture time in the name wins (K1 101.0 though its hash sorts first; K2 51.0 over "
                  "the earlier object)", arm_c)

    # (o) as_of, then the name descending
    def arm_o():
        got, _ = px("2026-09-11", ["K1", "K2"])
        print(f"  09-11 load: {got}")
        return near(got["K1"], 100.0) and near(got["K2"], 201.0)

    guard(v, "o", "at one capture time the later row as_of wins (K1 100.0), and when everything ties the name descending decides "
                  "(K2 201.0)", arm_o)

    # (d) the price group travels whole; the descriptive fields coalesce
    def arm_d():
        got14, ccy14 = px("2026-09-14", ["K1", "K1b"])
        rows14 = g4("2026-09-14")
        got15, ccy15 = px("2026-09-15", ["K1", "K2", "K3"])
        r15 = g4("2026-09-15")
        k1, k2, k3 = r15.get("K1") or {}, r15.get("K2") or {}, r15.get("K3") or {}
        print(f"  09-14 load {got14} currency {ccy14} | _g4_for K1 {(rows14.get('K1') or {}).get('currency')!r}")
        print(f"  09-15 load {got15} currency {ccy15}")
        print(f"  09-15 _g4_for K1 close {k1.get('px_close')} ccy {k1.get('currency')!r} tri {k1.get('total_return_index')} | "
              f"K2 close {k2.get('px_close')} ccy {k2.get('currency')!r} tri {k2.get('total_return_index')} | K3 close "
              f"{k3.get('px_close')} sector {k3.get('gics_sector')!r} parsekey {k3.get('security_parsekey')!r}")
        return (near(got14["K1"], 100.0) and isnull(ccy14["K1"]) and near(got14["K1b"], 70.0) and isnull(ccy14["K1b"])
                and near(got15["K1"], 100.0) and ccy15["K1"] == "USD" and near(k1.get("px_close"), 100.0)
                and k1.get("currency") == "USD" and near(k1.get("total_return_index"), 0.5)
                and isnull(k2.get("px_close")) and k2.get("currency") == "USD" and near(k2.get("total_return_index"), 0.3)
                and near(got15["K3"], 11.0) and k3.get("gics_sector") == "Energy" and k3.get("security_parsekey") == "KK US Equity")

    guard(v, "d", "the price group travels whole (close 100.0 with currency NULL, never EUR; an older row's close+currency+total return "
                  "when the first row has none; the first row's group when none has a close) and the descriptive fields "
                  "coalesce (K3 close from the newer row, GICS and parsekey from the older)", arm_d)

    # (e) source / as_of / as_of_source are those of the row that supplied px_close
    def arm_e():
        k1 = g4("2026-09-15").get("K1") or {}
        k2 = g4("2026-09-15").get("K2") or {}
        print(f"  09-15 K1 source {k1.get('source')!r} as_of {day10(k1.get('as_of'))} as_of_source {k1.get('as_of_source')!r} | "
              f"K2 (no close anywhere) source {k2.get('source')!r} as_of_source {k2.get('as_of_source')!r}")
        return (k1.get("source") == HIST and day10(k1.get("as_of")) == "2026-09-14" and k1.get("as_of_source") == "historical"
                and k2.get("source") == LIVE and k2.get("as_of_source") == "pull")

    guard(v, "e", "the merged row's source, as_of and as_of_source are those of the row that supplied px_close (else the first row in the "
                  "order)", arm_e)

    # (f) an older object that lacks columns
    def arm_f():
        got, ccy = px("2026-09-16", ["K1", "K2"])
        r = g4("2026-09-16")
        k1, k2 = r.get("K1") or {}, r.get("K2") or {}
        print(f"  09-16 load {got} currency {ccy} | _g4_for K1 ccy {k1.get('currency')!r} as_of_source {k1.get('as_of_source')!r} "
              f"parsekey {k1.get('security_parsekey')!r} sector {k1.get('gics_sector')!r} | K2 close {k2.get('px_close')}")
        return (near(got["K1"], 100.0) and isnull(ccy["K1"]) and near(got["K2"], 60.0) and ccy["K2"] == "USD"
                and isnull(k1.get("currency")) and isnull(k1.get("as_of_source")) and k1.get("security_parsekey") == "KK US Equity"
                and k1.get("gics_sector") == "Energy" and near(k2.get("px_close"), 60.0))

    guard(v, "f", "an older object lacking columns does not break the read and reads as null there (K1 close 100.0 with currency and "
                  "as_of_source NULL; parsekey and K2 from the newer object)", arm_f)

    # (g), (h) the discovered function
    fn, where = find_fn()
    print("discovered function:", where or "NONE")

    def arm_g():
        if fn is None:
            print("  " + AMEND)
            return False
        rows = call_fn(fn, s, "2026-09-18")
        keys = sorted((str(r.get("security_id")), day10(r.get("date"))) for r in rows)
        print(f"  {where}(s, 2026-09-18): {len(rows)} rows {keys}")
        return keys == [("K1", "2026-09-18"), ("K2", "2026-09-18"), ("K3", "2026-09-18")]

    guard(v, "g", "the shared function returns exactly one row per (security_id, date): 3 rows for a date of three objects", arm_g)

    def arm_h():
        if fn is None:
            print("  " + AMEND)
            return False
        by = {str(r.get("security_id")): r for r in call_fn(fn, s, "2026-09-15")}
        k1, k3 = by.get("K1") or {}, by.get("K3") or {}
        print(f"  {where}(s, 2026-09-15): K1 close {k1.get('px_close')} ccy {k1.get('currency')!r} source {k1.get('source')!r} | K3 close "
              f"{k3.get('px_close')} sector {k3.get('gics_sector')!r}")
        return (near(k1.get("px_close"), 100.0) and k1.get("currency") == "USD" and k1.get("source") == HIST
                and near(k3.get("px_close"), 11.0) and k3.get("gics_sector") == "Energy")

    guard(v, "h", "the shared function's merged row is the price group of the older row whole (K1) and the descriptive coalesce (K3)", arm_h)

    # (i) control: the objects are on the sink and revision.newest picks what its docstring says
    def arm_i():
        listed = {d: sorted(u for u in s.list(eb.market_target_uri(d, "x").rsplit("/", 1)[0] + "/") if u.endswith(".parquet"))
                  for d in planted}
        counts = {d: (len(listed[d]), len(planted[d])) for d in planted}
        n10 = revision.newest(planted["2026-09-10"][:2])
        n15 = revision.newest(planted["2026-09-15"])
        win = revision.newest([{"uri": u, "provenance": {"source": src}} for u, src in
                               ((planted["2026-09-09"][0], LIVE), (planted["2026-09-09"][1], IMP))])["uri"]
        print(f"  objects listed vs planted {counts}")
        print(f"  newest 09-10 {n10.rsplit('/', 1)[-1]} | newest 09-15 {n15.rsplit('/', 1)[-1]} | live-over-import record pick "
              f"{win.rsplit('/', 1)[-1]}")
        return (all(a == b and a > 0 for a, b in counts.values()) and n10.endswith("market-20260910T140000Z-aaaaaaaaaaaa.parquet")
                and n15.endswith("market-20260915T140000Z-bbbbbbbbbbbb.parquet")
                and win.endswith("market-20260909T100000Z-aaaaaaaaaaaa.parquet"))

    guard(v, "i", "control: the fixture's objects are on the sink and revision.newest picks the later capture time (and a live object over "
                  "an import record)", arm_i)


v = c.Verdict("AC2")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- a dead fixture is a failed check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = [m.split(")")[0].lstrip("(") for m in v.fails]
print("AC2 RESULT: PASS 0 failures" if not v.fails else f"AC2 RESULT: FAIL {len(v.fails)}: {', '.join(labels)}")
sys.exit(0 if not v.fails else 1)
