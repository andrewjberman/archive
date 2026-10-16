"""IRPT_DASHBD round 149, TO DB-c-29, worker 0.9.0_WK_IRPT_DASHBD~420 -- the labelled TEST READ (not a serve, not a production run).

Adapted from the round-148 harness (read_publish_r148.py, worker 0.9.0_WK_IRPT_DASHBD~419) to the 49 Financial publish prefix.

Read only: S3 list_objects_v2 and get_object on ONE prefix (the published series prefix of firm 49financial), region us-east-1.
No put, delete, create, invoke or update. Only series.json.gz objects are downloaded.

Usage: python -I read_publish_r149.py <worktree_root> <temporary_folder_outside_every_repository> <gold_first_date> <partition_template>

  <partition_template> is the series partition segment with its placeholder value, passed on the command line so no
  account segment is written in this file. <gold_first_date> is the first_date of account_return_daily from the gold census.

Downloads every series.json.gz into the folder as <n>.series.json.gz, then computes the python truth over those documents
and prints ONE JSON line: {"series_truth": {...}, "reads": {...}, "files_on_disk": n}. It prints no object key, no account
identifier and no series value. A failed call prints its error code only.
"""
import gzip
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FIRM = "49financial"


def error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        code = response.get("Error", {}).get("Code")
        if code:
            return str(code)
    return type(exc).__name__


def main(argv):
    root = Path(argv[0]).resolve()
    dest = Path(argv[1])
    gold_first = argv[2]
    template = argv[3]
    sys.path.insert(0, str(root))
    import boto3
    import lib.opal_naming as naming

    uri = naming.address("irpt", FIRM, "platinum", "reporting", template, "series.json.gz")
    bucket, key = re.match(r"s3://([^/]+)/(.*)$", uri).groups()
    prefix = key[: key.index(template.split("=")[0])]

    s3 = boto3.client("s3", region_name="us-east-1")
    reads = {"s3_list_calls": 0, "s3_get_calls": 0, "list_errors": [], "get_errors": []}
    lock = threading.Lock()

    keys, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
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

    def fetch(index_key):
        index, key_one = index_key
        name = "%d.series.json.gz" % (index + 1)
        try:
            body = s3.get_object(Bucket=bucket, Key=key_one)["Body"].read()
        except Exception as exc:  # noqa: BLE001
            with lock:
                reads["get_errors"].append(error_code(exc))
            return False
        with lock:
            reads["s3_get_calls"] += 1
        (dest / name).write_bytes(body)
        return True

    with ThreadPoolExecutor(32) as ex:
        ok = list(ex.map(fetch, list(enumerate(series))))

    out = {
        "objects_series": len(series),
        "objects_manifest": len(manifests),
        "objects_other": len(keys) - len(series) - len(manifests),
        "docs_total": 0, "docs_parse_ok": 0, "pair_present": 0, "pair_absent": 0, "nonempty_lists": 0,
        "total_listed_days": 0, "max_list_len": 0, "income_all_null_docs": 0, "income_any_number_docs": 0,
        "income_claim_present_docs": 0, "history_scope_counts": {}, "first_data_date_min": None,
        "first_data_date_max": None, "as_of_counts": {}, "day_quality_day_totals": {},
        "return_basis_day_totals": {}, "first_data_date_after_gold_first_day": 0,
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
        f, a = str(d.get("first_data_date")), str(d.get("as_of"))
        if isinstance(d.get("first_data_date"), str) and d["first_data_date"] > gold_first:
            out["first_data_date_after_gold_first_day"] += 1
        out["first_data_date_min"] = f if out["first_data_date_min"] is None or f < out["first_data_date_min"] else out["first_data_date_min"]
        out["first_data_date_max"] = f if out["first_data_date_max"] is None or f > out["first_data_date_max"] else out["first_data_date_max"]
        out["as_of_counts"][a] = out["as_of_counts"].get(a, 0) + 1
        for key_name, dest_name in (("day_quality", "day_quality_day_totals"), ("return_basis", "return_basis_day_totals")):
            for v in d.get(key_name, []):
                out[dest_name][str(v)] = out[dest_name].get(str(v), 0) + 1

    print(json.dumps({
        "series_truth": out,
        "reads": {
            "s3_list_calls": reads["s3_list_calls"],
            "s3_get_calls": reads["s3_get_calls"],
            "get_jobs": len(series),
            "get_ok": sum(1 for x in ok if x),
            "list_errors": reads["list_errors"],
            "get_errors": reads["get_errors"],
        },
        "files_on_disk": len(list(dest.iterdir())),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
