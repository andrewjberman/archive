"""RIV-c-1 AC1 -- the seam probe against the REAL issuer: one live daily fetch of BASG into a local sink.

The raw bytes land unchanged beside a sidecar that names the file's own report date, the stage marker is written,
and a second run of the same batch is a no-op.
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc
    from rivalfunds import collector_issuer

    import datetime
    import zoneinfo
    today_et = datetime.datetime.now(zoneinfo.ZoneInfo("America/New_York")).date()
    d = tc.prev_trading_day(today_et).isoformat()  # T-1: the newest file the issuer has published
    sink = c.tmpdir("rv_c1_")
    ev = {"date": d, "mode": "daily", "batch_id": f"chk-{d}", "sink": f"local:{sink}"}
    r1 = collector_issuer.handler_entry(dict(ev))
    print("first run:", json.dumps(r1, default=str)[:600])
    v.check(r1.get("status") in ("OK", "PARTIAL"), f"status {r1.get('status')} in OK/PARTIAL")
    txts = [o for o in r1.get("outputs", []) if o.endswith(".txt")]
    v.check(len(txts) == 1, f"exactly one raw .txt output ({len(txts)})")
    if txts:
        raw_p = c.local_path(sink, txts[0])
        prefix = c.address("issuer-site", "etfs", "bronze", "holdings", "date=")
        v.check(txts[0].startswith(prefix), f"raw lands under the builder's issuer bronze prefix {prefix}")
        side_p = next(iter(sorted(raw_p.parent.glob(raw_p.stem + "*.json"))), None)
        v.check(side_p is not None, "a JSON sidecar beside the raw object")
        if side_p:
            side = json.loads(side_p.read_text(encoding="utf-8"))
            raw = raw_p.read_bytes()
            v.check(side.get("sha256") == hashlib.sha256(raw).hexdigest(), "sidecar sha256 == sha256 of the landed bytes")
            v.check(side.get("requested_date") == d, f"sidecar requested_date == {d}")
            v.check(side.get("status") == "OK" and side.get("claimed_report_date") == d,
                    f"status OK and claimed_report_date == {d} (got {side.get('status')}, {side.get('claimed_report_date')})")
            v.check(side.get("date_evidence") == "internal-date-column", "date_evidence == internal-date-column")
            v.check(b"|BASG|" in raw, "the landed bytes carry BASG rows")
    v.check(bool(r1.get("marker")) and c.local_path(sink, r1["marker"]).exists(), "stage marker written")
    r2 = collector_issuer.handler_entry(dict(ev))
    v.check(r2.get("marker") == r1.get("marker"), "second run of the same batch returns the same marker")
    n_txt = len(list(pathlib.Path(sink).rglob("*.txt")))
    v.check(n_txt == 1, f"second run landed nothing new ({n_txt} raw object(s) in the sink)")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
