"""RIV-p-1 AC2 -- a planted guardrail failure never publishes a quietly wrong page (H7, C-GUARDRAILS).

Same real chain as AC1, publish with plant_failure='completeness'. Accepted branches, both from the PRD: the page is
published with BASG marked not updated and the failing check named and NO trades table; or nothing is published."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc
    from rivalfunds import publish_page

    files = c.archive_files(8)
    sink = c.tmpdir("rv_p1b_")
    c.run_chain(sink, files, through="trades")
    newest = c.archive_meta(files[-1])["requested_date"]
    day = next(d for d in tc.trading_days_between(newest, "2099-12-31") if d.isoformat() > newest).isoformat()
    r = publish_page.handler_entry({"date": day, "mode": "daily", "batch_id": "chk-plant", "sink": f"local:{sink}",
                                    "plant_failure": "completeness"})
    print("publish (planted):", str(r)[:500])
    page_dir = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={day}"))
    html_p = page_dir / "index.html"
    if not html_p.exists():
        v.check(r.get("status") == "FAILED", f"branch 'publish nothing': no index.html and status FAILED (got {r.get('status')})")
        return
    html = html_p.read_text(encoding="utf-8")
    v.check('data-status="not-updated"' in html, "branch 'not updated': BASG carries data-status=\"not-updated\"")
    v.check("completeness" in html, "the failing check is named on the page")
    v.check('id="trades"' not in html, "no trades table rendered as normal")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
