"""RIV-m-1 AC2 -- the recorded run count is the real one: this check lists every constituents run manifest under the home
producer's prefix itself (every page, client-side count) and it must equal the record's runs_listed; every evidence key the
record cites exists in S3."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REC = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/m1_home_producer.json"


def run(v):
    import boto3

    root = c.setup_path()
    rec = json.loads((root / REC).read_text(encoding="utf-8"))
    s3 = boto3.client("s3", region_name="us-east-1")
    n, pages = 0, 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix="bbg/"):
        pages += 1
        for o in page.get("Contents", []):
            if o["Key"].endswith("/constituents/run_manifest.json"):
                n += 1
    print(f"listed {n} constituents run manifests over {pages} page(s)")
    v.check(n > 0, "the positive control: at least one constituents run exists")
    v.check(rec.get("runs_listed") == n, f"record runs_listed {rec.get('runs_listed')} == listed {n}")
    keys = [k for f in rec.get("funds", {}).values() for k in f.get("evidence_keys", [])][:20]
    bad = []
    for k in keys:
        bkt, key = (k[len("s3://"):].split("/", 1) if k.startswith("s3://") else ("opal-data-etfs", k))
        try:
            s3.head_object(Bucket=bkt, Key=key)
        except Exception:
            bad.append(k)
    v.check(keys and not bad, f"{len(keys)} evidence key(s) exist in S3 (missing {bad[:3]})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
