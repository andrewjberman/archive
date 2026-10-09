"""NFRA_OPLGTW OG-bf-1 PHASE A -- the replay's DRY RUN over every missing date (writes nothing).

For each (master, date) the OG-cc-1 census named as having no QUALIFIED completion record, run the producer's own
convert_object over that date's bronze keys through a READ-ONLY S3 wrapper (any verb other than get_object,
head_object, list_objects_v2 is recorded and refused before it reaches S3), then compose the closure the replay
would write (day_inventory + build_closure) and grade it two ways:
  - the producer's validator (conversion_manifest.validate_closure), and
  - the gateway's record-level rule (catalog.membership_findings + catalog.validate_closure) on the would-be
    marker body, the same rule OG-cc-1 used.
A date is a CANDIDATE only if: no errors, zero write attempts, zero missing projection dims or facts, exactly
one marker date equal to the date, and both validators say qualified. Anything else is UNAVAILABLE with reasons.

Usage: python bf1_dry_run.py <repo_root> <census_record.json> <out.json> [workers] [master ...]
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import pathlib
import sys
import threading
import time

import boto3

BUCKET = "opal-data-assets"
READ_VERBS = {"get_object", "head_object", "list_objects_v2"}


class DryRunWriteRefused(Exception):
    pass


class ReadOnlyS3:
    def __init__(self, real):
        self._real = real
        self.writes = []
        self.head_miss = []

    def __getattr__(self, name):
        if name in READ_VERBS:
            fn = getattr(self._real, name)
            if name != "head_object":
                return fn

            def head(**kw):
                try:
                    return fn(**kw)
                except Exception:
                    self.head_miss.append(kw.get("Key"))
                    raise
            return head
        if name in ("exceptions", "meta"):
            return getattr(self._real, name)

        def refuse(*a, **kw):
            self.writes.append({"verb": name, "key": kw.get("Key")})
            raise DryRunWriteRefused(name + " refused in dry run: " + str(kw.get("Key")))
        return refuse


def main(argv):
    root = pathlib.Path(argv[1])
    census = json.loads(pathlib.Path(argv[2]).read_text(encoding="utf-8"))
    out_path = pathlib.Path(argv[3])
    workers = int(argv[4]) if len(argv) > 4 else 3
    only = argv[5:]
    os.environ.setdefault("OPAL_BUILD_COMMIT", "1f03a3f209")
    sys.path.insert(0, str(root / "infra/aws/lambda/opal-assets/opal-assets-silver-schwab"))
    sys.path.insert(1, str(root / "infra/aws/ec2/opal-gateway"))
    import conversion_manifest as cm
    import schwab_conversion as sc
    import schwab_runtime as rt
    from app.integrations.schwab import catalog as cat
    contract = cat.parse_contract(json.loads(
        (root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8")))
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    real = boto3.client("s3", region_name="us-east-1", config=boto3.session.Config(max_pool_connections=40))

    done = {}
    if out_path.exists():
        done = json.loads(out_path.read_text(encoding="utf-8")).get("rows", {})
    lock = threading.Lock()

    def one(master, date):
        ro = ReadOnlyS3(real)
        ymd = date.replace("-", "")
        row = {"master": master, "date": date}
        try:
            _k, types = rt._list_all(ro, BUCKET, "schwab/" + master + "/bronze/", "/")
            keys = []
            for t in sorted(types):
                k, _p = rt._list_all(ro, BUCKET, t + ymd + "/")
                keys.extend(k)
            keys = sorted(keys)
            results, errors = [], []
            for k in keys:
                try:
                    results.append(sc.convert_object(ro, BUCKET, k, silver_bucket=BUCKET, force=False))
                except DryRunWriteRefused as exc:
                    errors.append({"key": k, "error": str(exc)})
                except Exception as exc:  # noqa: BLE001
                    errors.append({"key": k, "error": type(exc).__name__ + ": " + str(exc)[:200]})
            silver_miss = [k for k in ro.head_miss if k and "/silver/" in k]
            missing_dims = [k for k in silver_miss if k.split("/")[3].startswith("dim_")]
            missing_facts = [k for k in silver_miss if not k.split("/")[3].startswith("dim_")]
            markers = cm.build_complete_markers("DRYRUN", master, results)
            marker_dates = [mk["date"] for mk in markers]
            inv = rt.day_inventory(ro, BUCKET, master, date)
            closure = cm.build_closure("DRYRUN", "event", master, date, inv, results, force=False)
            pv = cm.validate_closure(closure)
            gw_status, gw_classes = None, []
            if markers:
                body = json.loads(cm._marker_body(markers[0], closure).decode("utf-8"))
                f = cat.membership_findings(body, body["closure"], master, date, contract)
                v = cat.validate_closure(body["closure"], contract.masters)
                gw_status = "QUALIFIED" if (not any(x["class"] in rejected for x in f)
                                            and v["status"] == cat.RESULT_QUALIFIED) else "NONQUALIFYING"
                gw_classes = sorted({x["class"] for x in f} | {x.get("class") for x in v.get("findings", [])
                                                                 if isinstance(x, dict)})
            reasons = []
            if not keys:
                reasons.append("NO_BRONZE_SOURCE")
            if errors:
                reasons.append("CONVERT_ERRORS:" + str(len(errors)))
            if ro.writes:
                reasons.append("WOULD_WRITE_SILVER:" + str(len(ro.writes)))
            if missing_dims:
                reasons.append("MISSING_DIMS:" + str(len(missing_dims)))
            if missing_facts:
                reasons.append("MISSING_FACTS:" + str(len(missing_facts)))
            if keys and marker_dates != [date]:
                reasons.append("MARKER_DATES:" + json.dumps(marker_dates))
            if pv.get("status") != cm.QUALIFIED:
                reasons.append("PRODUCER_VALIDATOR:" + str(pv.get("status")) + ":"
                               + ",".join(sorted({str(x.get("class")) for x in pv.get("findings", [])
                                                  if isinstance(x, dict)})))
            if markers and gw_status != "QUALIFIED":
                reasons.append("GATEWAY_RULE:" + str(gw_status) + ":" + ",".join(c for c in gw_classes if c))
            row.update({
                "bronze_keys": len(keys),
                "bronze_types": sorted(inv.get("bronze", {})),
                "actions": sorted({r.action for r in results}),
                "silver_write_attempts": len(ro.writes),
                "missing_dims": len(missing_dims), "missing_facts": len(missing_facts),
                "errors": errors[:3], "marker_dates": marker_dates,
                "closure_status": closure.get("status"), "producer_validator": pv.get("status"),
                "gateway_status": gw_status, "silver_objects": len(closure.get("objects", [])),
                "inventory_errors": len(inv.get("errors") or []),
                "verdict": "CANDIDATE" if not reasons else "UNAVAILABLE", "reasons": reasons})
        except Exception as exc:  # noqa: BLE001
            row.update({"verdict": "UNAVAILABLE", "reasons": ["DRYRUN_EXCEPTION:" + type(exc).__name__ + ":"
                                                              + str(exc)[:200]]})
        return row

    todo = []
    for m, rec in sorted(census["masters"].items()):
        if only and m not in only:
            continue
        for d in rec["missing"]:
            if m + "|" + d not in done:
                todo.append((m, d))
    print("todo", len(todo), "already", len(done), flush=True)
    t0 = time.time()
    n = 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one, m, d): (m, d) for m, d in todo}
        for fut in cf.as_completed(futs):
            row = fut.result()
            with lock:
                done[row["master"] + "|" + row["date"]] = row
                n += 1
                if n % 10 == 0 or n == len(todo):
                    out_path.write_text(json.dumps({"rows": done}, indent=1, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
                    print(n, "of", len(todo), "elapsed", int(time.time() - t0), "s", flush=True)
    out_path.write_text(json.dumps({"rows": done}, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
