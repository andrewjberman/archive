"""RIV-p-2 AC2 -- the trade view carries the income-clean facts and one failing fund never blocks the rest: every fund's
trade list shows its excluded-event count from G6 (data-excluded-cash, data-excluded-ca, data-excluded-income present); and
with ONE rival's canonical_shape objects removed before publishing (a PLANTED failure), that fund is marked
data-status="not-updated" with a reason while the other funds still publish with data-status="updated"."""
import importlib.util
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

_spec = importlib.util.spec_from_file_location("p2a", pathlib.Path(__file__).resolve().parent / "p-2.AC1.py")


def run(v):
    c.setup_path()
    import re

    sink = c.tmpdir("rv_p2b_")
    src = (pathlib.Path(__file__).resolve().parent / "p-2.AC1.py").read_text(encoding="utf-8")
    ns = {"__name__": "p2a_mod", "__file__": str(pathlib.Path(__file__).resolve().parent / "p-2.AC1.py")}
    exec(src.split("def run(v):")[0], ns)  # the shared build/page_html helpers, without running AC1
    r, date = ns["build"](sink)
    html = ns["page_html"](sink, date)
    for f in ["TXUE", "SCHY"]:
        blk = re.search(rf'data-fund="{f}"(.*?)(?=data-fund="|\Z)', html, re.S)
        body = blk.group(1) if blk else ""
        v.check(all(k in body for k in ("data-excluded-cash", "data-excluded-ca", "data-excluded-income")),
                f"{f}: excluded-event counts shown")
    g1 = c.gold_dir(sink, "canonical_shape")
    import pandas as pd

    for p in g1.rglob("*.parquet"):
        df = pd.read_parquet(p)
        col = "fund_ticker" if "fund_ticker" in df.columns else "fund_id"
        keep = df[df[col] != "CGIC"]
        if len(keep) != len(df):
            keep.to_parquet(p, index=False)
    from rivalfunds import publish_page

    publish_page.handler_entry({"mode": "daily", "date": date, "batch_id": "chk-p2-planted", "sink": f"local:{sink}"})
    html2 = ns["page_html"](sink, date)
    cg = re.search(r'data-fund="CGIC"[^>]*data-status="([a-z-]+)"', html2)
    tx = re.search(r'data-fund="TXUE"[^>]*data-status="([a-z-]+)"', html2)
    v.check(cg is not None and cg.group(1) == "not-updated", f"CGIC (planted failure) not-updated ({cg.group(1) if cg else None})")
    v.check(tx is not None and tx.group(1) == "updated", f"TXUE still updated ({tx.group(1) if tx else None})")
    reason = re.search(r'data-fund="CGIC"(.*?)(?=data-fund="|\Z)', html2, re.S)
    v.check(reason is not None and "data-reason" in reason.group(1), "CGIC carries its reason")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
