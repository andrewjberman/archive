"""RIV-cb-1 AC1 (row Z-S24 / Z-C-S32; round-8 analysis item 6): a MEASURED Bloomberg capacity budget, and no ad hoc pull past it.
Measured 2026-10-05: about 175k BQL rows of local backfill (IDVZ+PFOE 12,820; ACWI+IWM 76,859 + 84,655; probes) between 05:30Z and
07:06Z exhausted the Terminal's daily capacity ('#N/A Daily Capacity, request is blocked'), which then blocked the 07:00 ET
production pulls; no instrument recorded what was spent, and nothing refused a pull before it ran.

Interface (prescribed): module `rivalfunds.bbg_budget` with
  - `CONFIG_PATH` (default data/etfs/scripts/rivalfunds/bbg_budget.json: {"daily_ceiling_rows", "production_reserve_rows",
    "est_rows_per_fund_date": {<fund>: n, "default": n}}) and a ledger directory from the environment RIVALFUNDS_BBG_BUDGET_DIR
    (one JSON-lines file per UTC day; each line {"at", "mode", "rows", "batch_id"});
  - `spent(day) -> int` and `record(mode, rows, batch_id)`;
  - `collector_bloomberg` records the rows of every capture it fetches, and before a `backfill` fetch estimates the plan
    (funds x dates x est_rows_per_fund_date) and REFUSES when spent(today) + estimate > ceiling - reserve: status "BUDGET",
    no fetch called, `detail` names the remaining rows. `daily` mode (production) is never refused, only recorded.
Fixture (offline, local sink, a temporary ledger dir and config: ceiling 1000, reserve 200, est 100 per fund-date):
  - (a) 700 rows already spent today; a backfill of TXUE over 2026-09-28..09-29 (estimate 200 > 100 left) -> status "BUDGET"
    and the fake fetch is never called;
  - (b) a fresh ledger; a backfill of TXUE for 2026-09-29 (estimate 100) -> fetched, and spent(today) rises by the capture's
    rows (2);
  - (c) control: 1,500 rows spent; a daily pull for page day 2026-09-30 -> fetched (production is never refused), and
    recorded.
FAIL at base: (a) FAILS (no budget: the fetch runs) and (b) FAILS on the record (no bbg_budget module); (c) PASSES on its fetch."""
import datetime as dt
import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

HDR = ["ID", "SOURCE", "POSITION", "POSITION_CHANGE", "WEIGHTS", "CURRENCY", "REPORTED_MKT_VAL", "DATES", "REPORT_DATE",
       "ORIG_IDS", "POSITION_TYPE", "id()"]


def cap(date):
    rows = [[sec, "ETF", 10.0, 0.0, 1.5, "USD", 100.0, f"{date} 00:00:00+00:00", f"{date} 00:00:00+00:00", "TXUE US Equity",
             "L", sec] for sec in ("X1 US Equity", "X2 US Equity")]
    q = f"get(id(), name()) for(holdings(['TXUE US Equity'],dates={date}))"
    return {"requested_date": date, "at": dt.datetime.now(dt.timezone.utc).isoformat(), "query": q, "anchor": "ID",
            "rows": [HDR] + rows}


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import collector_bloomberg as cb

    try:
        from rivalfunds import bbg_budget as bb
    except ImportError:
        bb = None
    calls = []

    def fake(plan):
        calls.append(plan)
        return {d: cap(d) for d in plan}

    def arm(spent_rows, ev):
        calls.clear()
        d = tempfile.mkdtemp(prefix="rv_cb1_")
        os.environ["RIVALFUNDS_BBG_BUDGET_DIR"] = d
        cfg = pathlib.Path(d) / "bbg_budget.json"
        cfg.write_text(json.dumps({"daily_ceiling_rows": 1000, "production_reserve_rows": 200,
                                   "est_rows_per_fund_date": {"default": 100}}), encoding="utf-8")
        if bb is not None:
            bb.CONFIG_PATH = cfg
            if spent_rows:
                bb.record("seed", spent_rows, "seed")
        before = bb.spent(dt.datetime.now(dt.timezone.utc).date().isoformat()) if bb else None
        r = cb.handler_entry(dict(ev, sink=f"local:{tempfile.mkdtemp(prefix='rv_cb1_sink_')}", funds=["TXUE"]), fetch=fake)
        after = bb.spent(dt.datetime.now(dt.timezone.utc).date().isoformat()) if bb else None
        return r, len(calls), before, after

    saved = os.environ.get("RIVALFUNDS_BBG_BUDGET_DIR")
    try:
        ra, na, _, _ = arm(700, {"mode": "backfill", "start": "2026-09-28", "end": "2026-09-29", "batch_id": "a"})
        print("(a)", ra.get("status"), str(ra.get("detail"))[:160], "| fetch calls", na)
        v.check(ra.get("status") == "BUDGET" and na == 0, "(a) a backfill past the budget is refused before any fetch")
        rb, nb, b0, b1 = arm(0, {"mode": "backfill", "start": "2026-09-29", "end": "2026-09-29", "batch_id": "b"})
        print("(b)", rb.get("status"), "| fetch calls", nb, "| spent before/after", b0, b1)
        v.check(nb == 1 and b0 is not None and b1 == b0 + 2, "(b) a backfill under the budget is fetched and its rows recorded")
        rc, nc, c0, c1 = arm(1500, {"mode": "daily", "date": "2026-09-30", "batch_id": "c"})
        print("(c)", rc.get("status"), "| fetch calls", nc, "| spent before/after", c0, c1)
        v.check(nc == 1, "(c) control: a production daily pull is fetched whatever the budget")
    finally:
        if saved is None:
            os.environ.pop("RIVALFUNDS_BBG_BUDGET_DIR", None)
        else:
            os.environ["RIVALFUNDS_BBG_BUDGET_DIR"] = saved


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
