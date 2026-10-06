"""RIV-fe-1 AC2 (ROUND_ANALYSIS.round11.md ruling 5 @3ae96d6bc7; CVO C-S36): the names stage asks for every key the page names
by its ticker form -- the trend's keys too, not only the rankings'.

Measured on the served 10-06 page: four securities still read in ticker form -- 8053 JP and RBLX US (in rankings / AI text),
9433 JP and 000270 KS (in the buying trend only). `security_names.handler_entry` reads only the newest holding_contribution
object, so a key the trend names but the rankings do not is never asked.

Interface (prescribed): the names stage's key space is the security-axis keys of the newest holding_contribution AND the newest
buying_trend object of the page day (same lookback), whose name is blank or a ticker form; everything else unchanged (one request,
inside the budget; a key the newest security_names object already names is not asked).
Fixture: round 9's nm-3 AC1 page (round 8 hc-1.AC2's fixture: PFOE holds AAA 'Aaa Corp', PCLG holds BBB named 'BBB US Equity'),
plus a buying_trend object at the page day naming CCC_US_Equity 'CCC US Equity' (a key no contribution row carries):
  - (a) the names stage asks for exactly ['BBB_US_Equity', 'CCC_US_Equity'];
  - (b) control: AAA is never asked.
FAIL at base: (a) FAILS (asks only BBB); (b) PASSES."""
import importlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

R9 = HERE.parents[1] / "round9" / "checks"
R8 = HERE.parents[1] / "round8" / "checks"


def load_hc_ac2():
    p = R8 / "hc-1.AC2.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("hc1_ac2_fixture")
    mod.__file__ = str(p)
    sys.path.insert(1, str(R8))
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import homes, sinks

    f = load_hc_ac2()
    orig_g4, orig_g1 = f.g4_rows, f.g1_rows
    spec = f"local:{c.tmpdir('rv_fe1_')}"
    s = sinks.get_sink(spec)
    for d in f.DAYS:
        f.put_parquet(s, homes.canonical_shape(d, f"holdings-{f.REV}.parquet"),
                      [dict(r, security_name="BBB US Equity") if r["security_id"] == "BBB_US_Equity" else r for r in orig_g1(d)])
        f.put_parquet(s, homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", f"market-{f.G4REV}.parquet"),
                      [dict(r, security_name=None) if r["security_id"] == "BBB_US_Equity" else r for r in orig_g4(d)])
    from rivalfunds import gold_holding_contribution as hc
    hc.handler_entry({"date": f.PAGE, "sink": spec})
    bt_rows = [{"fund_id": "PCLG", "role": "rival", "period": p, "axis": "security", "bucket": "CCC_US_Equity",
                "security_name": "CCC US Equity", "net_notional_base": -2.7e6, "n_windows": 3, "window_end": f.PAGE}
               for p in ("R30", "QTD", "YTD")]
    f.put_parquet(s, homes.address("rivalfunds", "etfs", "gold", "buying_trend", f"date={f.PAGE}",
                                   "buying_trend-20261005T000000Z-cccccccccccc.parquet"), bt_rows)
    asked = []

    def fake(keys):
        asked.append(sorted(keys))
        return {k: k.split("_")[0].title() + " Holdings Inc" for k in keys}

    sn = importlib.import_module("rivalfunds.security_names")
    r = sn.handler_entry({"date": f.PAGE, "sink": spec}, fetch=fake)
    print("names stage:", r.get("status"), "| asked", asked)
    v.check(asked[:1] == [["BBB_US_Equity", "CCC_US_Equity"]],
            "(a) the names stage asks for the rankings' AND the trend's ticker-named keys")
    v.check(not any("AAA_US_Equity" in a for a in asked), "(b) control: AAA (named by G4) is never asked")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
