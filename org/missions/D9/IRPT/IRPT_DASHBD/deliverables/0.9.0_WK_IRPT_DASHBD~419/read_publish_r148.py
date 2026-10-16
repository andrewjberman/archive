"""IRPT_DASHBD round 148, TO DB-c-27, worker 0.9.0_WK_IRPT_DASHBD~419 -- the labelled TEST READ (not a serve, not a production run).

Read only: S3 list_objects_v2 and get_object on ONE prefix, region us-east-1. No put, delete, create, invoke or update.

Usage: python -I read_publish_r148.py <temporary_folder_outside_every_repository>

Downloads every series.json.gz and manifest.json under the prefix into the folder as <n>.series.json.gz and <n>.manifest.json,
then computes the python truth over those files and prints ONE JSON line of counts. It prints no object key, no account id
and no series value. A failed call prints its error code only.
"""
import gzip
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BUCKET = "opal-data-cottonwood"
PREFIX = "irpt/cottonwood/platinum/reporting/"


def error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        code = response.get("Error", {}).get("Code")
        if code:
            return str(code)
    return type(exc).__name__


def main(argv):
    dest = Path(argv[0])
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    reads = {"s3_list_calls": 0, "s3_get_calls": 0, "list_errors": [], "get_errors": []}
    lock = threading.Lock()

    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if token:
            kw["ContinuationToken"] = token
        try:
            r = s3.list_objects_v2(**kw)
        except Exception as exc:  # noqa: BLE001 -- a refused read is recorded, never repaired
            reads["list_errors"].append(error_code(exc))
            break
        reads["s3_list_calls"] += 1
        keys += [o["Key"] for o in r.get("Contents", [])]
        token = r.get("NextContinuationToken")
        if not token:
            break

    series = sorted(k for k in keys if k.endswith("/series.json.gz"))
    manifests = sorted(k for k in keys if k.endswith("/manifest.json"))
    jobs = [("series", k) for k in series] + [("manifest", k) for k in manifests]

    def fetch(job):
        index, (kind, key) = job
        n = index + 1
        name = "%d.series.json.gz" % n if kind == "series" else "%d.manifest.json" % n
        try:
            body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        except Exception as exc:  # noqa: BLE001
            with lock:
                reads["get_errors"].append(error_code(exc))
            return False
        with lock:
            reads["s3_get_calls"] += 1
        (dest / name).write_bytes(body)
        return True

    with ThreadPoolExecutor(8) as ex:
        ok = list(ex.map(fetch, list(enumerate(jobs))))

    out = {
        "objects_series": len(series),
        "objects_manifest": len(manifests),
        "objects_other": len(keys) - len(series) - len(manifests),
        "docs_total": 0, "docs_parse_ok": 0, "pair_present": 0, "pair_absent": 0, "nonempty_lists": 0,
        "total_listed_days": 0, "max_list_len": 0, "income_all_null_docs": 0, "income_any_number_docs": 0,
        "income_claim_present_docs": 0, "history_scope_counts": {}, "calendar_source_counts": {},
    }
    for path in sorted(dest.glob("*.series.json.gz")):
        out["docs_total"] += 1
        try:
            d = json.loads(gzip.decompress(path.read_bytes()))
        except Exception:  # noqa: BLE001
            continue
        out["docs_parse_ok"] += 1
        if "unreported_trading_days" in d and "unreported_trading_days_basis" in d:
            out["pair_present"] += 1
            n = len(d["unreported_trading_days"])
            out["total_listed_days"] += n
            out["max_list_len"] = max(out["max_list_len"], n)
            out["nonempty_lists"] += 1 if n else 0
        else:
            out["pair_absent"] += 1
        inc = d.get("income", [])
        if inc and all(x is None for x in inc):
            out["income_all_null_docs"] += 1
        if any(isinstance(x, (int, float)) for x in inc):
            out["income_any_number_docs"] += 1
        if "income_claim" in d:
            out["income_claim_present_docs"] += 1
        hs = str(d.get("history_scope"))
        out["history_scope_counts"][hs] = out["history_scope_counts"].get(hs, 0) + 1
    for path in sorted(dest.glob("*.manifest.json")):
        try:
            m = json.loads(path.read_bytes())
        except Exception:  # noqa: BLE001
            continue
        cs = str(m.get("calendar_source", "ABSENT"))
        out["calendar_source_counts"][cs] = out["calendar_source_counts"].get(cs, 0) + 1

    print(json.dumps({
        "python_truth": out,
        "reads": {
            "s3_list_calls": reads["s3_list_calls"],
            "s3_get_calls": reads["s3_get_calls"],
            "get_jobs": len(jobs),
            "get_ok": sum(1 for x in ok if x),
            "list_errors": reads["list_errors"],
            "get_errors": reads["get_errors"],
        },
        "files_on_disk": len(list(dest.iterdir())),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
