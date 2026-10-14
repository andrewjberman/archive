"""TO-DB-b-204 step 5: ONE live read of the served model series through the reader module.

One S3 GET of one key (json/benchmarks/model_portfolio_timeseries.json in opal-data-portal-v2). No put, copy or delete
method exists on the reader. Prints counts, dates, the VersionId and the window fill only; the series is held in memory
and is never written anywhere.

Run once: python <this file>
"""
import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
MODULE = ROOT / "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py"
CONTRACT = ROOT / "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
SAMPLE = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~159/HOUSEHOLD_SAMPLE.json")


class ReadOnlyReader:
    """GET only: get_object(bucket, key) -> (bytes, VersionId). No put, copy or delete method."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0
        self.version_id = None

    def get_object(self, bucket, key):
        self.gets += 1
        r = self._s3.get_object(Bucket=bucket, Key=key)
        self.version_id = r.get("VersionId")
        return r["Body"].read(), self.version_id


def main():
    spec = importlib.util.spec_from_file_location("model_series_windows", str(MODULE))
    mw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mw)

    reader = ReadOnlyReader()
    series, claim = mw.read_served_series(reader)
    assert reader.gets == 1, "exactly one GET"

    h = json.loads(SAMPLE.read_bytes().decode("utf-8"))["household"]
    as_of, first = h["as_of"], h["first_data_date"]
    contract = json.loads(CONTRACT.read_bytes().decode("utf-8"))
    wins = mw.windows_from_series(series, as_of, first)

    ids = [m["id"] for m in contract["members"] if any(m["id"].endswith("." + s) for s in mw.STEMS)]
    filled = 0
    for mid in ids:
        _table, w, stem = mid.split(".", 2)
        if wins[stem][w] is not None:
            filled += 1

    out = {
        "version_id": reader.version_id,
        "data_as_of": claim["data_as_of"],
        "claim_source_key": claim["source"].split("?", 1)[0],
        "as_of": as_of,
        "first_data_date": first,
        "members_total": len(ids),
        "members_filled": filled,
        "per_stem": {
            s: {
                "trading_days": len(series[s]),
                "first_date": series[s][0][0].isoformat(),
                "last_date": series[s][-1][0].isoformat(),
                "windows_none": [w for w in mw.WINDOWS if wins[s][w] is None],
            }
            for s in mw.STEMS
        },
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
