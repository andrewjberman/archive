"""NFRA_OPLGTW OG-c-2 -- the replay's STOP precondition (G-B Half 1 s.6 / Half 2 s.E, ruling R-OG-5).

A read-only dry run of the deployed producer's convert_object for one date on each master, run
locally against the vendored package at this worktree. The S3 client is wrapped: only
get_object / head_object / list_objects_v2 pass; ANY other verb is recorded and refused
(raised) before it reaches S3. It prints, per master:
  - silver_writes: write-verb calls convert_object attempted (must be 0)
  - missing_dims: projection dim keys whose head_object missed (must be 0)
  - missing_facts: fact keys whose head_object missed (context; a missing fact is also a write)
  - the marker dates build_complete_markers would emit (must be exactly [date])
  - a closure preview composed read-only (day_inventory + build_closure + validate_closure)
Then one line: DRYRUN: ZERO-WRITES or DRYRUN: STOP <reason>.

Usage: py -3.12 dry_run.py <YYYY-MM-DD> <out.json>
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[8]
PKG = ROOT / "infra/aws/lambda/opal-assets/opal-assets-silver-schwab"
sys.path.insert(0, str(PKG))

import boto3  # noqa: E402

import conversion_manifest as cm  # noqa: E402
import schwab_conversion as sc  # noqa: E402
import schwab_runtime as rt  # noqa: E402

BUCKET = "opal-data-assets"
MASTERS = ("08242234", "08335338")
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
        if name == "exceptions" or name == "meta":
            return getattr(self._real, name)

        def refuse(*a, **kw):
            self.writes.append({"verb": name, "key": kw.get("Key")})
            raise DryRunWriteRefused(name + " refused in dry run: " + str(kw.get("Key")))
        return refuse


def bronze_keys(s3, master, date):
    ymd = date.replace("-", "")
    root = "schwab/" + master + "/bronze/"
    _k, types = rt._list_all(s3, BUCKET, root, "/")
    keys = []
    for t in sorted(types):
        k, _p = rt._list_all(s3, BUCKET, t + ymd + "/")
        keys.extend(k)
    return sorted(keys)


def main(date, out_path):
    real = boto3.client("s3", region_name="us-east-1")
    report = {"read_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "date": date, "package": str(PKG.relative_to(ROOT)), "masters": {}}
    stop = []
    for m in MASTERS:
        ro = ReadOnlyS3(real)
        keys = bronze_keys(ro, m, date)
        results, errors = [], []
        for k in keys:
            try:
                results.append(sc.convert_object(ro, BUCKET, k, silver_bucket=BUCKET, force=False))
            except DryRunWriteRefused as exc:
                errors.append({"key": k, "error": str(exc)})
            except Exception as exc:  # noqa: BLE001
                errors.append({"key": k, "error": type(exc).__name__ + ": " + str(exc)[:300]})
        silver_miss = [k for k in ro.head_miss if k and "/silver/" in k]
        missing_dims = [k for k in silver_miss if k.split("/")[3].startswith("dim_")]
        missing_facts = [k for k in silver_miss if not k.split("/")[3].startswith("dim_")]
        markers = cm.build_complete_markers("DRYRUN", m, results)
        inv = rt.day_inventory(ro, BUCKET, m, date)
        closure = cm.build_closure("DRYRUN", "event", m, date, inv, results, force=False)
        v = cm.validate_closure(closure)
        row = {
            "bronze_keys": keys,
            "results": [{"key": r.key, "action": r.action, "master": r.master,
                         "silver_keys": len(r.silver_keys)} for r in results],
            "errors": errors,
            "silver_writes": len(ro.writes),
            "write_attempts": ro.writes,
            "missing_dims": missing_dims,
            "missing_facts": missing_facts,
            "marker_dates": [mk["date"] for mk in markers],
            "marker_keys": [cm.complete_marker_key(m, mk["date"]) for mk in markers],
            "manifest_key_pattern": cm.manifest_key(m, "<run_id>"),
            "closure_preview": {"status": closure.get("status"), "validate": v.get("status"),
                                "findings": len(v.get("findings", [])),
                                "objects": len(closure.get("objects", [])),
                                "inventory_errors": inv.get("errors")},
            "writes_after_preview": len(ro.writes),
        }
        report["masters"][m] = row
        print(m + ": bronze=" + str(len(keys)) + " results=" + str(len(results)) + " errors=" + str(len(errors))
              + " silver_writes=" + str(len(ro.writes)) + " missing_dims=" + str(len(missing_dims))
              + " missing_facts=" + str(len(missing_facts)) + " actions="
              + json.dumps(sorted({r.action for r in results})) + " marker_dates=" + json.dumps(row["marker_dates"])
              + " closure_preview=" + json.dumps(row["closure_preview"]))
        if ro.writes:
            stop.append(m + " silver_writes=" + str(len(ro.writes)))
        if missing_dims:
            stop.append(m + " missing_dims=" + str(len(missing_dims)))
        if missing_facts:
            stop.append(m + " missing_facts=" + str(len(missing_facts)))
        if errors:
            stop.append(m + " errors=" + str(len(errors)))
        if row["marker_dates"] != [date]:
            stop.append(m + " marker_dates=" + json.dumps(row["marker_dates"]))
    report["verdict"] = "ZERO-WRITES" if not stop else "STOP " + "; ".join(stop)
    pathlib.Path(out_path).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("DRYRUN: " + report["verdict"])
    return 0 if not stop else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
