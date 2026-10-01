"""RIV-d-4 AC2 (live, READ-ONLY) -- the positive control of the issuer-side retain (row Z-S4; analysis ruling 1's
control): a live re-capture of one LANDED BASG report date, made on the deployed code, kept the earlier silver object,
wrote its silver marker, and canonical_shape for that date reads the NEW capture.

Reads d4_live.json `control` {report_date, recapture_capture_id, silver_marker}; then S3 issuer silver at that date, the
named marker, and the newest canonical_shape object at that date."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def run(v):
    ctl = L.record().get("control") or {}
    rd, cid = ctl.get("report_date"), ctl.get("recapture_capture_id")
    objs = sorted(k for k in L.keys(f"issuer-site/etfs/silver/holdings/date={rd}/") if k.endswith(".parquet"))
    print("control", rd, cid, "silver objects", [k.rsplit("/", 1)[-1] for k in objs])
    v.check(len(objs) >= 2 and any(k.endswith(f"basg-{cid}.parquet") for k in objs),
            f"the re-capture {cid} and an earlier object are both in silver ({len(objs)})")
    v.check(max(objs).endswith(f"basg-{cid}.parquet") if objs else False, "the re-capture is the newest by capture id")
    mk = ctl.get("silver_marker") or ""
    body = json.loads(L.get(mk[len("s3://opal-data-etfs/"):])) if mk else {}
    v.check(body.get("status") == "OK", f"silver marker {mk} status OK ({body.get('status')})")
    key, g1 = L.latest_parquet(f"rivalfunds/etfs/gold/canonical_shape/date={rd}/")
    revs = set(g1.loc[g1["fund_ticker"].astype(str).str.strip() == "BASG", "dataset_revision"].astype(str)) if g1 is not None else set()
    v.check(any(cid in r for r in revs), f"G1 {key} reads the re-capture for BASG ({sorted(revs)[:2]})")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
