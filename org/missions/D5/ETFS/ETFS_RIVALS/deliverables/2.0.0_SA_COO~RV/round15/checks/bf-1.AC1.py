"""RIV-bf-1 AC1 (FWD-22; F.5 card 2 answer; WORLD; ROUND15_CELLS_DRAFT.md revision 1.5): the range backfill PLANS before it
spends -- a dry run returns the plan and makes no request, and a plan over `max_points` or over the day's Bloomberg budget is
REFUSED before any request.

Measured today (CLOUD 90e794e816): `enrichment_bloomberg._handler_entry` knows import, plan, daily, plan-market, market,
import-market; `{"mode": "market-range"}` returns FAILED "bad event: mode 'market-range' is not ...". `bbg_budget.json`:
ceiling 150000, reserve 30000, so a backfill may spend 120000 - spent(today).

Interface (prescribed, verbatim from the cell): new mode `market-range` of stage `pull-enrichment`: event `{"mode":
"market-range", "start", "end", "securities": [...], "batch_id", "sink", "max_points": int, "dry_run": bool}`. It plans
`len(securities) x trading days in [start, end]` points; `dry_run` returns the plan and spends nothing; if the plan exceeds
`max_points`, or exceeds `bbg_budget`'s `ceiling - reserve - spent(today)`, it REFUSES before any request, naming the points left.
NO Bloomberg call: the vendor seam is the one `tests/test_s4_security_market.py` and `tests/test_r12eb1_session_attempts.py` stub
(`enrichment_bloomberg._blp_historical_data` / `_blp_reference_data`), bound here to a RECORDING stub; `integrations.bloomberg.mcp`
is replaced by a module that records and raises; `_run_date_et` is pinned to 2026-10-06; the budget ledger is a fresh temp dir per
arm (`RIVALFUNDS_BBG_BUDGET_DIR`); every sink is `local:`.
Fixture: 60 securities (`S000 US Equity` .. `S059 US Equity`), start 2026-09-21 (Monday), end 2026-09-28 (Monday): 6 NYSE
trading days (the weekend 26/27 is not one), so the plan is 60 x 6 = 360 points.
  - (a) dry run (`dry_run` true, `max_points` 1000): status OK, the result carries a `points` figure of 360, the stub records
    ZERO calls, no `security_market` object is written and the ledger records nothing;
  - (b) over `max_points` (211 < 360, `dry_run` false, an empty ledger): status REFUSED, ZERO calls, nothing written, nothing
    recorded, and the detail names the plan (360) and the points left (211 of `max_points`, or the budget's 120000);
  - (c) over the budget (a planted ledger line leaves 137 of the 120000; `max_points` 100000): status REFUSED, ZERO calls, nothing
    written, no `market-range` ledger line, and the detail names the 137 points left;
  - (d) control: the existing mode `plan-market` over the same 60 securities returns OK with 2 batches and no vendor call.
FAIL at base: (a), (b), (c) FAIL (the mode is refused as a bad event: FAILED, no plan); (d) PASSES."""
import datetime as dt
import json
import os
import pathlib
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SECS = [f"S{i:03d} US Equity" for i in range(60)]
START, END = "2026-09-21", "2026-09-28"
RUN_DATE = dt.date(2026, 10, 6)
PLAN = 360


class Vendor:
    """The recording stub of the vendor seam: every call is recorded; a historical call answers each requested field for each
    trading day inside its own [start, end]."""

    def __init__(self, days):
        self.days, self.hist, self.ref, self.leaked = days, [], [], []

    @staticmethod
    def _iso(x):
        s = str(x)[:10]
        return s if "-" in s else f"{s[:4]}-{s[4:6]}-{s[6:8]}"

    def historical(self, securities, fields, start=None, end=None, *a, **k):
        lo, hi = self._iso(start), self._iso(end)
        self.hist.append((list(securities), list(fields), lo, hi))
        return {s: {d: {f: 100.0 + i + int(d[-2:]) / 100 for f in fields} for d in self.days if lo <= d <= hi}
                for i, s in enumerate(securities)}

    def reference(self, securities, fields, *a, **k):
        self.ref.append((list(securities), list(fields)))
        return {}

    @property
    def calls(self):
        return len(self.hist) + len(self.ref) + len(self.leaked)


def bind(eb, days):
    """Bind the recording stub at the tests' seam and make the shared client itself unreachable."""
    vd = Vendor(days)
    eb._blp_historical_data = vd.historical
    eb._blp_reference_data = vd.reference
    eb._run_date_et = lambda: RUN_DATE

    def _leak(*a, **k):
        vd.leaked.append(a)
        raise PermissionError("offline check: blp_client is refused (no Bloomberg call)")

    fake = types.ModuleType("integrations.bloomberg.mcp")
    fake.blp_client = types.SimpleNamespace(reference_data=_leak, historical_data=_leak)
    sys.modules["integrations.bloomberg.mcp"] = fake
    return vd


def find(obj, pred, path=""):
    """Every (path, value) in a nested result whose KEY satisfies pred."""
    out = []
    if isinstance(obj, dict):
        for k, val in obj.items():
            if pred(str(k)):
                out.append((f"{path}{k}", val))
            out += find(val, pred, f"{path}{k}.")
    elif isinstance(obj, (list, tuple)):
        for i, val in enumerate(obj):
            out += find(val, pred, f"{path}{i}.")
    return out


def market_objects(s, homes):
    """{date: [object uris]} of gold/security_market over every calendar day of the range."""
    out, d = {}, dt.date.fromisoformat(START)
    while d <= dt.date.fromisoformat(END):
        us = [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d.isoformat()}") + "/")
              if u.endswith(".parquet")]
        if us:
            out[d.isoformat()] = us
        d += dt.timedelta(days=1)
    return out


def ledger_lines(bb):
    f = bb._ledger_file(bb._utc_today())
    return [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()] if f.is_file() else []


def arm(eb, bb, sinks, homes, days, name, event, planted_spend=0):
    """One isolated arm: its own ledger dir, its own local sink, its own recording stub. Returns the measured facts."""
    os.environ[bb.ENV_DIR] = str(c.tmpdir(f"rv_bf1_{name}_ledger_"))
    if planted_spend:
        bb.record("daily", planted_spend, "planted-production-spend")
    spec = f"local:{c.tmpdir(f'rv_bf1_{name}_sink_')}"
    vd = bind(eb, days)
    try:
        res = eb.handler_entry({"mode": "market-range", "start": START, "end": END, "securities": list(SECS),
                                "batch_id": f"bf1-{name}", "sink": spec, **event})
    except Exception as e:  # noqa: BLE001 -- a raising mode is a failed arm, not a dead check
        res = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}
    objs = market_objects(sinks.get_sink(spec), homes)
    mr = [ln for ln in ledger_lines(bb) if ln.get("mode") == "market-range"]
    return {"res": res, "status": res.get("status"), "calls": vd.calls, "objects": sum(len(x) for x in objs.values()),
            "range_lines": mr, "spent": bb.spent(), "text": json.dumps(res, default=str)}


def run(v):
    c.setup_path()
    c.offline_guards()
    from lib import trading_calendar as tc
    from rivalfunds import bbg_budget as bb
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks

    days = [d.isoformat() for d in tc.trading_days_between(START, END)]
    cfg = bb.config()
    limit = int(cfg["daily_ceiling_rows"]) - int(cfg["production_reserve_rows"])
    print(f"fixture: {len(SECS)} securities x {len(days)} trading days {days[0]}..{days[-1]} = {len(SECS) * len(days)} points"
          f" | backfill budget {limit} (ceiling {cfg['daily_ceiling_rows']} - reserve {cfg['production_reserve_rows']})")
    fixture_ok = len(SECS) * len(days) == PLAN and limit > 1000

    a = arm(eb, bb, sinks, homes, days, "dry", {"max_points": 1000, "dry_run": True})
    pts = find(a["res"], lambda k: "points" in k.lower() and k != "max_points")
    print(f"dry run: status {a['status']} | points keys {pts} | vendor calls {a['calls']} | objects {a['objects']} | "
          f"ledger spent {a['spent']} | detail {str(a['res'].get('detail'))[:160]}")
    v.check(fixture_ok and a["status"] == "OK" and any(val == PLAN for _, val in pts) and a["calls"] == 0 and a["objects"] == 0
            and a["spent"] == 0, "(a) dry run returns the plan (360 points), makes ZERO calls, writes and spends nothing")

    b = arm(eb, bb, sinks, homes, days, "maxpts", {"max_points": 211, "dry_run": False})
    names_b = str(PLAN) in b["text"] and ("211" in b["text"] or str(limit) in b["text"])
    print(f"over max_points: status {b['status']} | vendor calls {b['calls']} | objects {b['objects']} | ledger spent {b['spent']}"
          f" | names 360 and the points left: {names_b} | detail {str(b['res'].get('detail'))[:200]}")
    v.check(fixture_ok and b["status"] == "REFUSED" and b["calls"] == 0 and b["objects"] == 0 and b["spent"] == 0 and names_b,
            "(b) a plan over max_points is REFUSED before any call, naming the points left")

    left = 137
    cc = arm(eb, bb, sinks, homes, days, "budget", {"max_points": 100000, "dry_run": False}, planted_spend=limit - left)
    print(f"over the budget: status {cc['status']} | vendor calls {cc['calls']} | objects {cc['objects']} | ledger spent "
          f"{cc['spent']} of {limit} | market-range lines {len(cc['range_lines'])} | names 137: {str(left) in cc['text']} | "
          f"detail {str(cc['res'].get('detail'))[:200]}")
    v.check(fixture_ok and cc["status"] == "REFUSED" and cc["calls"] == 0 and cc["objects"] == 0 and not cc["range_lines"]
            and cc["spent"] == limit - left and str(left) in cc["text"],
            "(c) a plan over ceiling - reserve - spent(today) is REFUSED before any call, naming the 137 points left")

    vd = bind(eb, days)
    spec = f"local:{c.tmpdir('rv_bf1_ctl_sink_')}"
    p = eb.handler_entry({"mode": "plan-market", "date": END, "sink": spec, "securities": list(SECS)})
    print(f"plan-market: status {p['status']} | securities {len(p.get('securities') or [])} | batches "
          f"{[len(x) for x in p.get('batches') or []]} | vendor calls {vd.calls}")
    v.check(p["status"] == "OK" and p.get("securities") == sorted(SECS) and [len(x) for x in p.get("batches") or []] == [50, 10]
            and vd.calls == 0, "(d) control: plan-market still plans the 60 securities in 2 batches with no vendor call")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
