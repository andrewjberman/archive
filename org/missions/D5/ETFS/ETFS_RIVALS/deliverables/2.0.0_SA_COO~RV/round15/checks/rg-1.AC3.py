"""RIV-rg-1 AC3 (PRD v0.19 C-OWED-GRAIN, G.4; row ETFS_RIVALS-Z-S69): REGRESSION. The union applies to G4 only. Every other table still
reads ONE object per date through `_newest_by_date`, what a stage RECORDS as the date's G4 revision or location stays the
`revision.newest` object (interface item 4), and the checks of the neighbouring cells still pass.

Interface read (from the cell): "`_newest_by_date` keeps its one-object rule for every OTHER table (G1, G5 and the A1 tables are
written whole per revision)"; "what a stage RECORDS as the date's G4 revision or location (for example the G4 revision inside a G1
revision in `gold_canonical_shape`, `location` in `gold_input_census`) stays the `revision.newest` object of the date, as today."

Fixture: the rg-1.AC1 two-object date (2026-09-29: live `market-20260929-53bc393958bd.parquet`, import `market-20260929-afcd903ad844.parquet`)
plus, for arm a, TWO G1 objects on one report date (`holdings-20260929T100000Z-...` holds LVO, SHR, IMO and an extra holding XOLD;
the newer `holdings-20260929T140000Z-...` holds LVO, SHR, IMO only) and two G5 objects on one date.
  - (a) G1 and G5 with two objects on a date still read the NEWEST object only: `gold_holding_contribution.handler_entry` (page day
    2026-10-05) has no XOLD bucket (held only by the older G1 object) and holds LVO; `_newest_by_date(s, <G1 prefix>, lo, hi)` returns
    the later capture's uri for the date, and the same call on the trade_schedule prefix returns the later of two G5 objects;
  - (b) the G4 revision/location a stage records is the `revision.newest` object of the date: `gold_input_census.build('2026-09-29')`
    puts the uri `revision.newest([live, import])` (the same bare-uri call the readers make) in `location` of the LVO and IMO
    `price` rows, whatever their status; `gold_canonical_shape._g4_for('2026-09-29')` returns `uri` and `revision` of the object
    `revision.newest` picks from the date's provenance records (the live object: an import never outranks it), and `apply_g4`
    writes that revision into `gics_source`; the rankings table's `input_manifest` lists, for the date, that one G4 object
    (`revision.newest([live, import])`) under `g4`. [`input_manifest` is recorded by the stage beside the revision; if the issuer
    rules that the manifest should list every object read, drop the manifest clause here]
  - (c) these existing checks still end `PASS 0 failures` (each run as its own process from the worktree root, rc 0): ps-1.AC1,
    bk-1.AC1, bk-1.AC2, bk-1.AC3, co-1.AC1, pm-1.AC3 and round12/checks/pk-1.AC1 (run first at base 4611085187: it passes there, so it
    is in); one arm per file, labelled by file.
FAIL at base 4611085187: none -- every arm of this regression check PASSES at the base (it is a guard for the build; see the report).
"""
import datetime as dt
import io
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LIVE_SRC, IMPORT_SRC = "blp_client.reference_data", "import:bbg/2026-09-29/characteristics.parquet"
D29 = "2026-09-29"
LIVE_NAME, IMPORT_NAME = "market-20260929-53bc393958bd.parquet", "market-20260929-afcd903ad844.parquet"
LVO, SHR, IMO, XOLD = "LVO_US_Equity", "SHR_US_Equity", "IMO_US_Equity", "XOLD_US_Equity"
PAGE = "2026-10-05"
ENTS = [{"group_id": "IDVZ", "fund_id": "TXUE", "ticker": "TXUE", "role": "rival"}]
HERE = pathlib.Path(__file__).resolve().parent
OTHERS = (("ps-1.AC1", HERE / "ps-1.AC1.py"), ("bk-1.AC1", HERE / "bk-1.AC1.py"), ("bk-1.AC2", HERE / "bk-1.AC2.py"),
          ("bk-1.AC3", HERE / "bk-1.AC3.py"), ("co-1.AC1", HERE / "co-1.AC1.py"), ("pm-1.AC3", HERE / "pm-1.AC3.py"),
          ("pk-1.AC1", HERE.parents[1] / "round12" / "checks" / "pk-1.AC1.py"))


def mrow(eb, sec, date, px=None, tri=None, ccy=None, sector=None, source=LIVE_SRC, aos="pull", pk=None):
    r = {col: None for col in eb.MARKET_COLUMNS}
    r.update(security_id=sec, security_bloomberg=sec.replace("_", " "), date=dt.date.fromisoformat(date), px_close=px,
             total_return_index=tri, currency=ccy, gics_sector=sector, source=source, as_of=dt.date.fromisoformat(date),
             as_of_source=aos, security_parsekey=pk, producer_version=eb.GOLD_VERSION, input_manifest="{}", claim="MEASURED",
             produced_at=f"{date}T01:00:00Z")
    return r


def put_obj(eb, s, date, name, rows):
    rev = name[len("market-"):-len(".parquet")]
    uri = eb.market_target_uri(date, rev)
    s.put(uri, eb._parquet_bytes(eb._market_table([dict(r, revision=rev) for r in rows])), "application/octet-stream")
    return uri


def two_objects(eb, s):
    live = put_obj(eb, s, D29, LIVE_NAME, [
        mrow(eb, LVO, D29, px=50.0, tri=0.4, ccy="USD", sector="Energy"), mrow(eb, SHR, D29, px=20.0, tri=0.1, ccy="USD")])
    imp = put_obj(eb, s, D29, IMPORT_NAME, [
        mrow(eb, SHR, D29, sector="Health Care", source=IMPORT_SRC, aos=None),
        mrow(eb, IMO, D29, sector="Information Technology", source=IMPORT_SRC, aos=None)])
    return live, imp


def put_g1(s, d, lines, name):
    from rivalfunds import homes
    from rivalfunds.tests import test_r7cg1_census_reads_rankings_gics as t7
    t7._put(s, homes.canonical_shape(d, name), [dict(t7._line("TXUE", k, date=d), market_value=mv) for k, mv in lines])


def guard(v, label, desc, fn):
    try:
        ok = fn()
    except Exception as e:  # noqa: BLE001
        print(f"  ({label}) raised {type(e).__name__}: {e}")
        ok = False
    v.check(bool(ok), f"({label}) {desc}")


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_canonical_shape as g1mod
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import gold_input_census as ic
    from rivalfunds import homes, revision, sinks

    def sink(tag):
        spec = f"local:{c.tmpdir(f'rv_rg1_ac3_{tag}_')}"
        return spec, sinks.get_sink(spec)

    def table(spec, s):
        hc.universe.entries = lambda: list(ENTS)
        r = hc.handler_entry({"date": PAGE, "sink": spec})
        outs = r.get("outputs") or []
        if r.get("status") != "OK" or not outs:
            print(f"  handler_entry: {r.get('status')} {r.get('detail')}")
            return None
        return pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas()

    # ---- (a) every other table still reads one object per date ---------------------------------------------------------
    def arm_a():
        spec, s = sink("a")
        two_objects(eb, s)
        g_old = "holdings-20260929T100000Z-aaaaaaaaaaaa.parquet"
        g_new = "holdings-20260929T140000Z-bbbbbbbbbbbb.parquet"
        put_g1(s, "2026-09-28", [(k, 1000.0) for k in (LVO, SHR, IMO)], "holdings-20260928T100000Z-cccccccccccc.parquet")
        put_g1(s, D29, [(k, 1010.0) for k in (LVO, SHR, IMO, XOLD)], g_old)
        put_g1(s, D29, [(k, 1010.0) for k in (LVO, SHR, IMO)], g_new)
        g5 = []
        for n in ("trades-20260929T100000Z-aaaaaaaaaaaa.parquet", "trades-20260929T140000Z-bbbbbbbbbbbb.parquet"):
            buf = io.BytesIO()
            pq.write_table(pa.table({"fund_id": ["TXUE"], "fund_ticker": ["TXUE"], "security_key": [LVO], "action": ["add"],
                                     "window_end": [D29], "est_notional_base": [1.0]}), buf)
            u = homes.trade_schedule(D29, n)
            s.put(u, buf.getvalue())
            g5.append(u)
        t = table(spec, s)
        buckets = None if t is None else set(t[t.axis == "security"]["bucket"].astype(str))
        g1 = hc._newest_by_date(s, homes.canonical_shape(""), "2026-09-01", PAGE)
        g5n = hc._newest_by_date(s, homes.trade_schedule(""), "2026-09-01", PAGE)
        print(f"  rankings security buckets {sorted(buckets or [])} | G1 newest of {D29}: {str(g1.get(D29)).rsplit('/', 1)[-1]} | "
              f"G5 newest: {str(g5n.get(D29)).rsplit('/', 1)[-1]}")
        return (buckets is not None and XOLD not in buckets and LVO in buckets
                and str(g1.get(D29)).endswith(g_new) and g5n.get(D29) == g5[1])

    guard(v, "a", "G1 and G5 with two objects on a date are read newest-only (no XOLD bucket; _newest_by_date keeps its one-object "
                  "rule)", arm_a)

    # ---- (b) what a stage records stays the revision.newest object ------------------------------------------------------
    def arm_b():
        spec, s = sink("b")
        live, imp = two_objects(eb, s)
        newest_bare = revision.newest([live, imp])
        newest_rec = revision.newest([{"uri": live, "provenance": {"source": LIVE_SRC}},
                                      {"uri": imp, "provenance": {"source": IMPORT_SRC}}])["uri"]
        # ONE G1 report only: no holding-implied fallback can cover a price, so the price rows' location is the G4 one
        put_g1(s, D29, [(k, 1010.0) for k in (LVO, SHR, IMO)], "holdings-20260929T140000Z-bbbbbbbbbbbb.parquet")
        df = ic.build(D29, s, list(ENTS), readings=[], page_day=D29)
        locs = {k: set(df[(df.input_kind == "price") & (df.subject == k)]["location"]) for k in (LVO, IMO)}
        g = g1mod._g4_for(s, D29, {})
        rows = [{"security_id": k, "is_cash_line": False, "asset_class": None} for k in (LVO,)]
        g1mod.apply_g4(rows, g)
        want_rev = "20260929-53bc393958bd"
        t = table(spec, s)
        man = json.loads(str(t["input_manifest"].iloc[0])) if t is not None else {}
        print(f"  newest (bare uris) {newest_bare.rsplit('/', 1)[-1]} | newest (provenance records) {newest_rec.rsplit('/', 1)[-1]}")
        print(f"  census price locations {locs}")
        print(f"  _g4_for uri {str((g or {}).get('uri')).rsplit('/', 1)[-1]} revision {(g or {}).get('revision')!r} | gics_source "
              f"{rows[0].get('gics_source')!r}")
        print(f"  rankings manifest g4: {[u.rsplit('/', 1)[-1] for u in man.get('g4', [])]}")
        # issuer ruling at the cut: the census's price location and the rankings manifest's g4 are PRINTED, not graded --
        # a build may name the newest object or every object it read; _g4_for's recorded uri / revision stay as today
        return ((g or {}).get("uri") == newest_rec and (g or {}).get("revision") == want_rev
                and want_rev in str(rows[0].get("gics_source")))

    guard(v, "b", "the G4 uri / revision _g4_for records is the revision.newest object of the date by its provenance rule, and "
                  "gics_source carries it (the census location and the rankings manifest's g4 are printed, not graded)", arm_b)

    # ---- (c) the neighbouring checks -------------------------------------------------------------------------------------
    for label, path in OTHERS:
        def arm(label=label, path=path):
            ac = path.name.split(".")[1]
            want = f"{ac} RESULT: PASS 0 failures"
            p = subprocess.run([sys.executable, str(path)], cwd=str(c.ROOT), capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=480)
            lines = [ln.strip() for ln in (p.stdout or "").splitlines() if ln.strip()]
            last = lines[-1] if lines else ""
            print(f"  {label}: rc {p.returncode} | last line: {last}")
            return p.returncode == 0 and last == want

        guard(v, label, f"{label} still ends PASS 0 failures (own process, worktree root)", arm)


v = c.Verdict("AC3")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- a dead fixture is a failed check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = [m.split(")")[0].lstrip("(") for m in v.fails]
print("AC3 RESULT: PASS 0 failures" if not v.fails else f"AC3 RESULT: FAIL {len(v.fails)}: {', '.join(labels)}")
sys.exit(0 if not v.fails else 1)
