"""RIV-p-1 AC1 -- the day's page from real gold: 20 archived BASG days through the chain, then publish for the day
after the newest report. The page LEADS with trades, each trade opens a trace to its two reports and the issuer
file (URL + sha256), the manifest carries every guardrail result, and the object was read back."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

CHECKS = {"report_date_freshness", "content_repeat", "completeness", "identity_coverage", "analysis_grounding", "render_readback"}


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc
    from rivalfunds import publish_page

    files = c.archive_files(20)
    sink = c.tmpdir("rv_p1_")
    c.run_chain(sink, files, through="trades")
    newest = c.archive_meta(files[-1])["requested_date"]
    day = next(d for d in tc.trading_days_between(newest, "2099-12-31") if d.isoformat() > newest).isoformat()
    r = publish_page.handler_entry({"date": day, "mode": "daily", "batch_id": "chk", "sink": f"local:{sink}"})
    print("publish:", str(r)[:500])
    v.check(r.get("status") == "OK", f"publish status OK (got {r.get('status')})")
    page_dir = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={day}"))
    html_p, man_p = page_dir / "index.html", page_dir / "manifest.json"
    v.check(html_p.exists() and man_p.exists(), f"index.html and manifest.json at the platinum page prefix date={day}")
    if not (html_p.exists() and man_p.exists()):
        return
    html = html_p.read_text(encoding="utf-8")
    t, h = html.find('id="trades"'), html.find('id="holdings"')
    v.check(t != -1 and h != -1 and t < h, "the trades section precedes the holdings section")
    v.check("<script src" not in html.lower() and "http://" not in html.lower().replace("http://www.w3.org", ""), "self-contained: no external script")
    traces = re.findall(r'<[^>]+class="[^"]*\btrace\b[^"]*"[^>]*>(.*?)</(?:details|div|section)>', html, re.S)
    v.check(len(traces) >= 1, f"trace panels rendered ({len(traces)})")
    if traces:
        tr = traces[0]
        v.check(len(set(re.findall(r"\d{4}-\d{2}-\d{2}", tr))) >= 2, "the first trace names two report dates")
        v.check("brownadvisory.filepoint.live" in tr and re.search(r"\b[0-9a-f]{64}\b", tr), "the first trace names the issuer file URL and its sha256")
    man = json.loads(man_p.read_text(encoding="utf-8"))
    res = {x["check"]: x["status"] for x in man.get("checks", [])}
    v.check(set(res) == CHECKS, f"manifest names the six guardrails ({sorted(res)})")
    v.check(res.get("analysis_grounding") == "NOT-APPLICABLE", "analysis_grounding NOT-APPLICABLE in round 1")
    v.check(all(s in ("PASS", "NOT-APPLICABLE") for s in res.values()), f"every guardrail PASS or NOT-APPLICABLE ({res})")
    v.check(man.get("readback") is True, "manifest.readback is true")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
