"""RIV-p-1 AC3 -- a rerun never silently overwrites a day's page (C-SERVING).

Publish the day after the 8th real report from 7 real days; land the 8th, rebuild, publish the SAME page day again. The bytes change, so
the first page must survive under revisions/<utc-ts>/index.html byte-identical, and the manifest must name it."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc
    from rivalfunds import publish_page

    files = c.archive_files(8)
    sink = c.tmpdir("rv_p1c_")
    c.run_chain(sink, files[:7], through="trades")
    newest = c.archive_meta(files[-1])["requested_date"]
    # the page day follows the 8th report: the first publish (7 reports) is stale and renders BASG "not updated";
    # the second (8 reports) renders the trades -- the bytes change on the same page prefix either way
    day = next(d for d in tc.trading_days_between(newest, "2099-12-31") if d.isoformat() > newest).isoformat()
    ev = {"date": day, "mode": "daily", "batch_id": "chk-1", "sink": f"local:{sink}"}
    r1 = publish_page.handler_entry(dict(ev))
    page_dir = c.local_path(sink, c.address("rivalfunds", "etfs", "platinum", "page", f"date={day}"))
    first = (page_dir / "index.html").read_bytes() if (page_dir / "index.html").exists() else b""
    v.check(bool(first), f"first publish wrote index.html (status {r1.get('status')})")
    c.run_chain(sink, files, through="trades")
    ev["batch_id"] = "chk-2"
    r2 = publish_page.handler_entry(dict(ev))
    second = (page_dir / "index.html").read_bytes() if (page_dir / "index.html").exists() else b""
    v.check(bool(second) and second != first, f"second publish wrote changed bytes (status {r2.get('status')})")
    revs = sorted((page_dir / "revisions").glob("*/index.html")) if (page_dir / "revisions").exists() else []
    v.check(len(revs) == 1 and revs[0].read_bytes() == first, f"the first page kept byte-identical under revisions/ ({len(revs)} revision(s))")
    man = json.loads((page_dir / "manifest.json").read_text(encoding="utf-8")) if (page_dir / "manifest.json").exists() else {}
    v.check(len(man.get("revisions", [])) == 1, f"manifest.revisions names the kept page ({man.get('revisions')})")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
