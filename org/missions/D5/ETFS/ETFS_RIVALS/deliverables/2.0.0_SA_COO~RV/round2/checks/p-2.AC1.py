"""RIV-p-2 AC1 -- the page groups by Opal fund over REAL data: after the full local chain (4 IDVZ-group captures + 2 BASG
issuer days) and the G0 map, publish-page writes a page with one section per peer group (data-group="IDVZ" and
data-group="PFOE"), each group's home fund first and marked data-role="home", and for every fund with data a history
calendar (data-calendar) and a per-day source badge (data-source="bloomberg" / "issuer")."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def build(sink):
    c.land(sink, c.archive_files(2))
    c.replay("silver_issuer", sink, c.archive_meta(c.archive_files(1)[0])["requested_date"])
    files = c.idvz_captures(4)
    c.run_idvz_chain(sink, files, "trades")
    date = c.capture(files[-1])["requested_date"]
    for m in ("gold_holdings_coverage", "gold_trade_schedule"):
        c.replay(m, sink, date, batch_id="chk-p")
    from rivalfunds import gold_peer_group_map, publish_page

    gold_peer_group_map.handler_entry({"mode": "daily", "date": date, "batch_id": "chk-p", "sink": f"local:{sink}"})
    return publish_page.handler_entry({"mode": "daily", "date": date, "batch_id": "chk-p", "sink": f"local:{sink}"}), date


def page_html(sink, date):
    p = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={date}")) / "index.html"
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def run(v):
    c.setup_path()
    sink = c.tmpdir("rv_p2a_")
    r, date = build(sink)
    print("publish:", str(r)[:300])
    html = page_html(sink, date)
    v.check(len(html) > 0, f"page written ({len(html)} chars)")
    for g in ("IDVZ", "PFOE"):
        sec = re.search(rf'data-group="{g}"(.*?)(?=data-group="|\Z)', html, re.S)
        v.check(sec is not None, f"a section for group {g}")
        if sec:
            first = re.search(r'data-fund="([A-Z]+)"[^>]*data-role="([a-z_]+)"', sec.group(1))
            v.check(first is not None and first.group(1) == g and first.group(2) == "home",
                    f"{g}: home fund first and marked ({first.groups() if first else None})")
    for f in ["TXUE", "SCHY", "BASG"]:
        blk = re.search(rf'data-fund="{f}"(.*?)(?=data-fund="|\Z)', html, re.S)
        body = blk.group(1) if blk else ""
        v.check("data-calendar" in body, f"{f}: history calendar present")
        want = "issuer" if f == "BASG" else "bloomberg"
        v.check(f'data-source="{want}"' in body, f"{f}: source badge {want}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
