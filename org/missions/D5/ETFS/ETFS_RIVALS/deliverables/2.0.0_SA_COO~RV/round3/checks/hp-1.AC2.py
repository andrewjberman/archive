"""RIV-hp-1 AC2 -- the page shows each Opal fund beside its rivals (FWD-1; analysis ruling 4): with the home-producer
reader, IDVZ and PFOE carry G2 coverage and appear on the page with data, and the "home-producer reader: next round"
placeholder is gone.

Real data: the last 4 IDVZ-group captures and the 2 newest BASG issuer days run to the page in a local sink, with the
Positioning landings for the 4 capture dates copied READ-ONLY to their real keys. Then:
  - G2 (holdings_coverage) for the newest date has an IDVZ row with selected = true and source 'home_producer';
  - the page's IDVZ and PFOE fund blocks each carry a history calendar (data-calendar) and a 'home_producer' source badge;
  - the page contains no 'Home-producer reader: next round' text;
  - control: TXUE's block still carries a 'bloomberg' badge."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import gold_peer_group_map, publish_page

    sink = c.tmpdir("rv_hp1b_")
    files = c.idvz_captures(4)
    for f in files:
        c.mirror_s3(sink, c.HOME_LANDING_FMT.format(d=c.capture(f)["requested_date"]))
    c.land(sink, c.archive_files(2))
    c.replay("silver_issuer", sink, c.archive_meta(c.archive_files(1)[0])["requested_date"])
    c.run_idvz_chain(sink, files, "trades")
    date = c.capture(files[-1])["requested_date"]
    for m in ("gold_holdings_coverage", "gold_trade_schedule"):
        c.replay(m, sink, date, batch_id="hp-p")
    gold_peer_group_map.handler_entry({"mode": "daily", "date": date, "batch_id": "hp-p", "sink": f"local:{sink}"})
    r = publish_page.handler_entry({"mode": "daily", "date": date, "batch_id": "hp-p", "sink": f"local:{sink}"})
    print("publish:", r.get("status"))

    cov, n = c.read_parquets(c.gold_dir(sink, "holdings_coverage"))
    sel = cov[(cov.get("fund_id").astype(str) == "IDVZ")] if len(cov) else cov
    ok = len(sel) and any((str(s) == "home_producer") and bool(x) for s, x in zip(sel["source"], sel["selected"]))
    v.check(bool(ok), f"G2 has an IDVZ row selected from home_producer ({n} objects, {len(sel)} IDVZ rows)")

    p = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={date}")) / "index.html"
    html = p.read_text(encoding="utf-8") if p.is_file() else ""
    v.check(len(html) > 0, f"page written ({len(html)} chars)")
    for f in ("IDVZ", "PFOE"):
        blk = re.search(rf'data-fund="{f}"(.*?)(?=data-fund="|\Z)', html, re.S)
        body = blk.group(1) if blk else ""
        v.check("data-calendar" in body and 'data-source="home_producer"' in body,
                f"{f}: calendar and home_producer badge on the page")
    v.check("home-producer reader: next round" not in html.lower(), "no 'home-producer reader: next round' placeholder")
    blk = re.search(r'data-fund="TXUE"(.*?)(?=data-fund="|\Z)', html, re.S)
    v.check(bool(blk) and 'data-source="bloomberg"' in blk.group(1), "control: TXUE keeps a bloomberg badge")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
