"""RIV-bk-1 AC2 (PRD v0.18 FWD-22; row ETFS_RIVALS-Z-S60; change 3 of the cell; WORLD): every row the range backfill writes
carries its security's quote currency -- the stored one where G4 holds it, ONE budgeted CRNCY request for the rest -- and the
plan counts only the dates not already held.

Measured at the base: `_market_range` writes rows built from `{"PX_LAST": ...}` alone, so `currency` is NULL on every
backfill row (and `price_series` then draws no holding-implied price for the key: RIV-pc-1 reads the NEWEST row's
currency); the plan is `securities x trading days` whether or not a date is already held.

Interface (prescribed, from the cell): in mode `market-range` every backfill row carries `currency`. Per security: the
STORED currency = the `currency` of its newest non-backfill G4 row at or before the run (read through the sink); for the
securities with NO stored currency the mode makes ONE reference request asking the single field "CRNCY" for exactly those
securities, through the client hook the mode already uses (`_blp_call(_blp_reference_data, ...)`), with
`bbg_budget.check_points` before and `bbg_budget.record` after (points = the securities asked); a security Bloomberg gives no
CRNCY for gets currency None. A dry run's plan gains "currency_lookups": <how many securities would be asked>. The plan's
`points` and the budget check count only the dates NOT already held (a date holding a `market-*.parquet` costs nothing).
  Open details this check accepts both ways: (i) the budget check of the lookup may be its own `check_points(3)` or one
  `check_points(plan + 3)`, as long as it comes before the reference request; (ii) the ledger line of the lookup may carry
  any `mode`; (iii) `currency_lookups` may sit in `plan` or beside it; (iv) `points` may or may not include the lookups
  (30 or 33 here), as long as one held date lowers it by exactly securities x 1.
  Chosen where the cell is silent: the stored rows sit on dates AFTER the range and before the run (2026-10-01 .. 10-05,
  run date 2026-10-06), which is the real case (a past range, today's daily partitions); and a backfill-marked row that
  carries a currency is NOT a stored currency (the cell says "non-backfill"), so its security is still asked.

NO Bloomberg call: bf-1.AC2's own recording stub and helpers (`bind`, `find`, `market_objects`, `ledger_lines`, loaded
from round15/checks/bf-1.AC2.py without its verdict) at the tests' seam (`enrichment_bloomberg._blp_historical_data` /
`_blp_reference_data`); the reference stub here answers CRNCY; `integrations.bloomberg.mcp` records and raises;
`_run_date_et` is 2026-10-06; each arm has its own ledger dir and its own `local:` sink; `bbg_budget.check_points` and
`record` are wrapped to log their order.
Fixture: start 2026-09-21, end 2026-09-28 (6 NYSE trading days), `max_points` 1000, five securities, 30 points:
  JJJ JP Equity  stored: G4 2026-10-05 currency JPY (`as_of_source` "pull")
  UUU US Equity  stored: G4 2026-09-30 CAD, then 2026-10-02 USD (the NEWEST wins: USD)
  LKA US Equity  no stored currency; a backfill-marked G4 row 2026-10-01 carries CHF (not a stored currency); stub: EUR
  LKB LN Equity  no G4 row; stub: GBp
  NON US Equity  no G4 row; the stub answers it with no CRNCY
  - (a) dry run: status OK, "currency_lookups" is 3, ZERO requests, nothing written, nothing recorded;
  - (b) live run: status OK; exactly ONE reference request, its fields ["CRNCY"] and its securities exactly LKA, LKB, NON;
    the historical side is the one PX_LAST request over the range; nothing reaches the shared client;
  - (c) each of the 6 dates holds one object of 5 rows, all `backfill`, with currency JPY / USD / EUR / GBp / None for
    JJJ / UUU / LKA / LKB / NON;
  - (d) `check_points` is consulted for the lookup (3, or the plan + 3) before the reference request, and `record` is called
    with 3 after it; the ledger's lines sum to the historical points + 3;
  - (e) the plan counts only dates not held: a dry run on a sink that also holds a `market-*.parquet` on 2026-09-23 plans
    exactly 5 points fewer than the dry run of (a), and names that date as skipped;
  - (f) control: the live run sends the historical request (5 securities, ["PX_LAST"], 2026-09-21..2026-09-28), lands 6
    objects of `backfill` rows, and the stored rows read back from the sink as planted (JPY, CAD then USD, CHF on a backfill
    row).
FAIL at base 0ed013f33d: (a), (b), (c), (d), (e) FAIL (no currency_lookups; no reference request; currency NULL on every
row; one check_points(30), no record of 3; the plan is 30 with or without the held date); (f) PASSES."""
import datetime as dt
import io
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

JJJ, UUU, LKA, LKB, NON = "JJJ JP Equity", "UUU US Equity", "LKA US Equity", "LKB LN Equity", "NON US Equity"
SECS = [JJJ, UUU, LKA, LKB, NON]
ASKED = sorted([LKA, LKB, NON])
ANSWERS = {LKA: {"CRNCY": "EUR"}, LKB: {"CRNCY": "GBp"}, NON: {}, JJJ: {"CRNCY": "XXX"}, UUU: {"CRNCY": "XXX"}}
WANT = {JJJ: "JPY", UUU: "USD", LKA: "EUR", LKB: "GBp", NON: None}
HELD = "2026-09-23"
# (date, security, currency, as_of_source) of the G4 rows the sink holds before the run
STORED = (("2026-10-05", JJJ, "JPY", "pull"), ("2026-09-30", UUU, "CAD", "pull"), ("2026-10-02", UUU, "USD", "pull"),
          ("2026-10-01", LKA, "CHF", "backfill"))


def load_bf1():
    """bf-1.AC2's module with its stub and helpers only (its own verdict never runs)."""
    p = HERE / "bf-1.AC2.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("bf1_ac2_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def put_market(eb, s, date, data, tag, as_of_source):
    prov = {"revision": f"{date.replace('-', '')}T010000Z-{tag * 12}", "produced_at": f"{date}T01:00:00Z",
            "producer_version": eb.GOLD_VERSION, "input_manifest": "{}"}
    uri = eb.market_target_uri(date, prov["revision"])
    s.put(uri, eb._parquet_bytes(eb._market_table(eb.market_rows(data, date, eb.MARKET_SOURCE_LIVE, prov, as_of_source))),
          "application/octet-stream")
    return uri


def arm(bf, eb, bb, sinks, days, name, dry_run, held=False):
    """One isolated arm: its own ledger dir and sink, the stored rows planted, the stubs bound, the budget calls logged."""
    os.environ[bb.ENV_DIR] = str(c.tmpdir(f"rv_bk1_{name}_ledger_"))
    spec = f"local:{c.tmpdir(f'rv_bk1_{name}_sink_')}"
    s = sinks.get_sink(spec)
    for i, (d, sec, ccy, src) in enumerate(STORED):
        put_market(eb, s, d, {sec: {"PX_LAST": 50.0 + i, "CRNCY": ccy}}, "abcd"[i], src)
    if held:
        put_market(eb, s, HELD, {"ZZZ US Equity": {"PX_LAST": 1.0}}, "e", "historical")
    vd = bf.bind(eb, days)
    log = []
    inner_hist, inner_check, inner_record = vd.historical, bb.check_points, bb.record

    def hist(securities, fields, start=None, end=None, *a, **k):
        log.append(("hist", len(list(securities))))
        return inner_hist(securities, fields, start, end, *a, **k)

    def ref(securities, fields, *a, **k):
        vd.ref.append((list(securities), list(fields)))
        log.append(("ref", len(list(securities))))
        return {x: {f: ANSWERS.get(x, {}).get(f) for f in fields if f in ANSWERS.get(x, {})} for x in securities}

    def check_points(points, *a, **k):
        log.append(("check", int(points)))
        return inner_check(points, *a, **k)

    def record(mode, rows, batch_id, *a, **k):
        log.append(("record", int(rows), str(mode)))
        return inner_record(mode, rows, batch_id, *a, **k)

    eb._blp_historical_data, eb._blp_reference_data = hist, ref
    bb.check_points, bb.record = check_points, record
    try:
        res = eb.handler_entry({"mode": "market-range", "start": bf.START, "end": bf.END, "securities": list(SECS),
                                "batch_id": f"bk1-{name}", "sink": spec, "max_points": 1000, "dry_run": dry_run})
    except Exception as e:  # noqa: BLE001 -- a raising mode is a failed arm, not a dead check
        res = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}
    finally:
        bb.check_points, bb.record = inner_check, inner_record
    plan = res.get("plan") if isinstance(res.get("plan"), dict) else {}
    return {"res": res, "status": res.get("status"), "vd": vd, "log": log, "s": s, "plan": plan,
            "points": plan.get("points", res.get("points")), "lines": bf.ledger_lines(bb), "spent": bb.spent()}


def landed(bf, s, pq, homes):
    """{date: {security_bloomberg: (currency, as_of_source)}} over the range's partitions (the planted held object aside)."""
    out = {}
    for d, uris in bf.market_objects(s, homes).items():
        rows = {}
        for u in uris:
            df = pq.read_table(io.BytesIO(s.get(u))).to_pandas()
            for sec, ccy, src in zip(df["security_bloomberg"], df["currency"], df["as_of_source"]):
                rows[str(sec)] = (None if ccy is None or ccy != ccy else str(ccy), str(src))
        out[d] = rows
    return out


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from lib import trading_calendar as tc
    from rivalfunds import bbg_budget as bb
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks

    bf = load_bf1()
    days = [d.isoformat() for d in tc.trading_days_between(bf.START, bf.END)]
    plan0 = len(SECS) * len(days)
    fixture_ok = plan0 == 30 and HELD in days and bf.RUN_DATE == dt.date(2026, 10, 6)
    print(f"fixture: {len(SECS)} securities x {len(days)} trading days {days[0]}..{days[-1]} = {plan0} points | no stored "
          f"currency: {ASKED} | run date {bf.RUN_DATE}")

    # ---- (a) the dry run ------------------------------------------------------------------------------------------
    a = arm(bf, eb, bb, sinks, days, "dry", dry_run=True)
    lookups = bf.find(a["res"], lambda k: k == "currency_lookups")
    n_obj = sum(len(x) for x in bf.market_objects(a["s"], homes).values())
    print(f"dry run: status {a['status']} | plan {a['plan']} | currency_lookups {lookups} | vendor calls {a['vd'].calls} | "
          f"objects in the range {n_obj} | ledger spent {a['spent']}")
    v.check(fixture_ok and a["status"] == "OK" and bool(lookups) and all(val == len(ASKED) for _, val in lookups)
            and a["vd"].calls == 0 and n_obj == 0 and a["spent"] == 0,
            "(a) a dry run's plan carries currency_lookups 3 (the securities with no stored currency) and makes no request")

    # ---- (b), (c), (d) the live run --------------------------------------------------------------------------------
    b = arm(bf, eb, bb, sinks, days, "live", dry_run=False)
    vd = b["vd"]
    refs = [(sorted(secs), fields) for secs, fields in vd.ref]
    hists = [(len(secs), fields, lo, hi) for secs, fields, lo, hi in vd.hist]
    print(f"live run: status {b['status']} | reference requests {refs} | historical requests {hists} | reached blp_client "
          f"{len(vd.leaked)} | detail {str(b['res'].get('detail'))[:200]}")
    v.check(fixture_ok and b["status"] == "OK" and refs == [(ASKED, ["CRNCY"])] and hists == [(5, ["PX_LAST"], bf.START, bf.END)]
            and not vd.leaked,
            "(b) exactly ONE reference request, for CRNCY only and for exactly the securities with no stored currency")

    rows = landed(bf, b["s"], pq, homes)
    good = []
    for d in days:
        got = {sec: val[0] for sec, val in rows.get(d, {}).items()}
        srcs = sorted({val[1] for val in rows.get(d, {}).values()})
        good.append(got == WANT and srcs == [eb.BACKFILL_SOURCE])
        print(f"  date={d}: currency by security {got} | as_of_source {srcs}")
    v.check(len(good) == 6 and all(good),
            "(c) every landed backfill row carries currency: the stored one, else the looked-up one, else None")

    log = b["log"]
    at_ref = next((i for i, e in enumerate(log) if e[0] == "ref"), None)
    checks_before = [e[1] for e in log[: at_ref or 0] if e[0] == "check"]
    records_after = [e[1] for e in log[(at_ref if at_ref is not None else len(log)):] if e[0] == "record"]
    hist_points = sum(e[1] for e in log if e[0] == "record") - (len(ASKED) if len(ASKED) in records_after else 0)
    total = sum(int(ln.get("rows", 0)) for ln in b["lines"])
    print(f"budget order: {log} | check_points before the reference request {checks_before} | record after it {records_after} | "
          f"ledger lines {[(ln.get('mode'), ln.get('rows')) for ln in b['lines']]} sum {total}")
    v.check(at_ref is not None and any(x in (len(ASKED), plan0 + len(ASKED)) for x in checks_before)
            and records_after.count(len(ASKED)) == 1 and hist_points == plan0 and total == plan0 + len(ASKED)
            and b["spent"] == total,
            "(d) the lookup is checked against the budget before it is sent and recorded (3 points) after")

    # ---- (e) the plan counts only the dates not held ---------------------------------------------------------------
    e = arm(bf, eb, bb, sinks, days, "held", dry_run=True, held=True)
    skipped = bf.find(e["res"], lambda k: "skip" in k.lower())
    named = any(val == [HELD] for _, val in skipped)
    print(f"dry run with {HELD} held: status {e['status']} | plan {e['plan']} | points {e['points']} (free sink: {a['points']}) | "
          f"skip keys {skipped} | vendor calls {e['vd'].calls}")
    v.check(a["status"] == "OK" and e["status"] == "OK" and isinstance(a["points"], int) and isinstance(e["points"], int)
            and a["points"] in (plan0, plan0 + len(ASKED)) and a["points"] - e["points"] == len(SECS) and named
            and e["vd"].calls == 0,
            "(e) a date already holding a market object costs nothing: the plan's points drop by securities x 1")

    # ---- (f) control -----------------------------------------------------------------------------------------------
    stored = []
    for d, sec, _ccy, _src in STORED:
        us = [u for u in b["s"].list(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}") + "/")]
        df = pq.read_table(io.BytesIO(b["s"].get(us[0]))).to_pandas() if len(us) == 1 else None
        stored.append(None if df is None or len(df) != 1 else
                      (d, str(df["security_bloomberg"][0]), str(df["currency"][0]), str(df["as_of_source"][0])))
    n_back = sum(1 for d in days if rows.get(d) and {val[1] for val in rows[d].values()} == {eb.BACKFILL_SOURCE}
                 and sorted(rows[d]) == sorted(SECS))
    print(f"control: historical requests {hists} | dates holding 5 backfill rows {n_back} of {len(days)} | stored rows read "
          f"back {stored}")
    v.check(fixture_ok and b["status"] == "OK" and hists == [(5, ["PX_LAST"], bf.START, bf.END)] and n_back == 6
            and stored == list(STORED) and not vd.leaked,
            "(f) control: the live run sends the historical request and lands 6 backfill objects, and the stored-currency "
            "rows are in the sink as planted")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
