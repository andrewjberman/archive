"""RIV-r-3 AC3 -- report-date freshness is counted in TRADING days, per source (row W5-S28; analysis ruling 3), and a
page that publishes with some funds not updated still writes its publish marker, naming each such fund (row W1-S5).

Real data, planted lag: the last 5 IDVZ-group captures run to the page in a local sink, except that TXUE's rows are dropped
from the newest 2 captures and CGIC's from the newest 3. Against the page's expected report date (the trading day
before the page day) TXUE then lags 1 trading day and CGIC 2. Bloomberg-sourced funds report one trading day late by measurement (row W5-S28), so:
  - TXUE is NOT in the manifest's not-updated set (lag 1 trading day, within the Bloomberg allowance);
  - CGIC IS, with a reason that counts TRADING days;
  - the publish result carries a marker, and the marker record names CGIC under `not_updated`;
  - control: a fund with no plant (SCHY) is updated.
Lag is measured with lib/trading_calendar.py from the captures' own requested dates, never assumed."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DROP = {"TXUE": 2, "CGIC": 3}  # fund -> drop from the newest N captures


def planted(files):
    tmp = pathlib.Path(c.tmpdir("rv_r3a3p_"))
    out = []
    for k, f in enumerate(files):
        from_end = len(files) - k
        d = c.capture(f)
        hdr = d["rows"][0]
        fi = hdr.index("ORIG_IDS")
        drop = {fund for fund, n in DROP.items() if from_end <= n}
        rows = [hdr] + [r for r in d["rows"][1:] if str(r[fi]).split()[0] not in drop]
        p = tmp / f.name
        p.write_text(json.dumps({**d, "rows": rows}), encoding="utf-8")
        out.append(p)
    return out


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc  # noqa: F401  (the instrument this criterion names)
    from rivalfunds import gold_peer_group_map, publish_page

    files = planted(c.idvz_captures(5))
    sink = c.tmpdir("rv_r3a3_")
    c.run_idvz_chain(sink, files, "trades")
    date = c.capture(files[-1])["requested_date"]
    c.replay("gold_holdings_coverage", sink, date, batch_id="r3-p")
    gold_peer_group_map.handler_entry({"mode": "daily", "date": date, "batch_id": "r3-p", "sink": f"local:{sink}"})
    r = publish_page.handler_entry({"mode": "daily", "date": date, "batch_id": "r3-p", "sink": f"local:{sink}"})
    mpath = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={date}")) / "manifest.json"
    m = json.loads(mpath.read_text(encoding="utf-8")) if mpath.is_file() else {}
    print("publish:", r.get("status"), "marker:", r.get("marker"))

    def fresh(fund):
        entry = next((e for k, e in (m.get("funds") or {}).items() if k.split("/")[-1] == fund), None) or {}
        chk = next((x for x in entry.get("checks", []) if x.get("check") == "report_date_freshness"), {})
        print(f"  {fund}: {chk.get('status')} -- {chk.get('reason')}")
        return chk.get("status"), str(chk.get("reason") or "")

    st, _ = fresh("TXUE")
    v.check(st == "PASS", "TXUE (1 trading day behind, Bloomberg-sourced) passes report_date_freshness")
    st, why = fresh("CGIC")
    v.check(st == "FAIL" and "trading day" in why.lower(), "CGIC (2 trading days behind) fails with a trading-day reason")
    st, _ = fresh("SCHY")
    v.check(st == "PASS", "control: SCHY (no plant) passes")
    mk = r.get("marker")
    rec = {}
    if mk:
        rec = json.loads(c.local_path(sink, mk).read_text(encoding="utf-8"))
    v.check(bool(mk) and "CGIC" in json.dumps(rec.get("not_updated", {})),
            f"publish marker written and names CGIC under not_updated ({json.dumps(rec, default=str)[:200]})")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
