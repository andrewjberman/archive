"""NFRA_OPLGTW OG-bf-1 PHASES B and D -- the controlled replay over a SIGNED write set, one master per run.

Phase B (08242234): option W, COO half @35ca8013bb, CTO half @f9b1f1fd31.
Phase D (08335338): COO half @8be94ecce4, CTO half @fa71e133b6, after the Y date gate went live. For 08335338 the
run ALSO reads the advi-49f-gold-dispatch log after every date and STOPS on any `dispatched: doc=` line since the
phase started (the signed stop rule); a date moves from `unavailable` to `backfilled` when written.

Per candidate date, newest first, ONE invocation in flight: list the date's bronze keys, invoke
opal-assets-silver-schwab RequestResponse (one attempt, no retry) with them as a synthetic S3 event (the OG-c-2 form),
then read the completion record back at its current VersionId and apply the OG-cc-1 qualification rule
(catalog.membership_findings + catalog.validate_closure). STOP on the first record that is not QUALIFIED and on any
Lambda error, throttle or timeout. Never run inside 09:30-10:30Z, 12:10-13:00Z (sweep + floor) or 21:30-22:30Z.

State is kept in <out> (backfill_record.json) after every date, so a stop is resumable and nothing is re-written:
a date already under `backfilled` is skipped.

Usage: python bf1_backfill.py <repo_root> <plan.json> <out_record.json> [max_dates] [master: 08242234|08335338]
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys
import time

import boto3
from botocore.config import Config

BUCKET = "opal-data-assets"
MASTER = "08242234"
HELD_MASTER = "08335338"
DISPATCHER_LOG = "/aws/lambda/advi-49f-gold-dispatch"
HELD_REASON = "held: 49F accelerator; Y leg pending (A1)"
FUNCTION = "opal-assets-silver-schwab"
AVOID = ((9 * 60 + 30, 10 * 60 + 30), (9 * 60 + 40, 9 * 60 + 55), (12 * 60 + 10, 13 * 60), (21 * 60 + 30, 22 * 60 + 30))


def in_avoid_window(now):
    m = now.hour * 60 + now.minute
    return any(a <= m < b for a, b in AVOID)


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dispatched_lines(logs, start_ms):
    """Count of `dispatched: doc=` lines in the dispatcher log since start_ms (the signed stop rule)."""
    n = 0
    for pg in logs.get_paginator("filter_log_events").paginate(
            logGroupName=DISPATCHER_LOG, startTime=start_ms, filterPattern='"dispatched: doc="'):
        n += len(pg["events"])
    return n


def main(argv):
    global MASTER, HELD_MASTER
    if len(argv) > 5:
        if argv[5] not in ("08242234", "08335338"):
            raise SystemExit("master not in the signed sets")
        MASTER = argv[5]
        HELD_MASTER = "08335338" if MASTER == "08242234" else "08242234"
    phase_d = MASTER == "08335338"
    root = pathlib.Path(argv[1])
    plan = json.loads(pathlib.Path(argv[2]).read_text(encoding="utf-8"))
    out = pathlib.Path(argv[3])
    max_dates = int(argv[4]) if len(argv) > 4 else 10 ** 6
    sys.path.insert(0, str(root / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    contract = cat.parse_contract(json.loads(
        (root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8")))
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    s3 = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1",
                       config=Config(read_timeout=650, connect_timeout=10, retries={"max_attempts": 0}))

    dates = list(plan["masters"][MASTER]["dates_newest_first"])
    held = list(plan["masters"][HELD_MASTER]["dates_newest_first"])
    if out.exists():
        rec = json.loads(out.read_text(encoding="utf-8"))
    else:
        rec = {"slug": "nfra-oplgtw-og-bf-1-marker-backfill", "run_by": "0.9.0_WK_NFRA_OPLGTW~41",
               "signed": "COO half @35ca8013bb, CTO half @f9b1f1fd31 (option W, master 08242234 only)",
               "started_utc": utc(), "stopped": None, "writes": [],
               "masters": {MASTER: {"backfilled": [], "unavailable": {}},
                           HELD_MASTER: {"backfilled": [], "unavailable": {d: HELD_REASON for d in held}}}}
    done = set(rec["masters"][MASTER]["backfilled"])
    logs = boto3.client("logs", region_name="us-east-1")
    if phase_d and not rec.get("phase_d_started_utc"):
        rec["phase_d_started_utc"] = utc()
    d_start_ms = int(dt.datetime.fromisoformat(rec["phase_d_started_utc"].replace("Z", "+00:00")).timestamp() * 1000)         if phase_d else 0

    def save():
        out.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")

    save()
    n = 0
    for d in dates:
        if d in done:
            continue
        if n >= max_dates:
            break
        now = dt.datetime.now(dt.timezone.utc)
        if in_avoid_window(now):
            rec["stopped"] = {"at": utc(), "date": d, "why": "avoid window reached; resumable"}
            save()
            print("PAUSED at", d, "- avoid window")
            return 3
        ymd = d.replace("-", "")
        types = s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/" + MASTER + "/bronze/", Delimiter="/")
        keys = []
        for cp in sorted(c["Prefix"] for c in types.get("CommonPrefixes", [])):
            pg = s3.list_objects_v2(Bucket=BUCKET, Prefix=cp + ymd + "/")
            keys.extend(o["Key"] for o in pg.get("Contents", []))
        keys = sorted(keys)
        mkey = "schwab/" + MASTER + "/meta/complete/date=" + d + ".json"
        try:
            prior = s3.head_object(Bucket=BUCKET, Key=mkey).get("VersionId")
        except Exception:  # noqa: BLE001
            prior = None
        t0 = time.time()
        stop = None
        try:
            resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="None",
                              Payload=json.dumps({"Records": [{"s3": {"object": {"key": k}}} for k in keys]}))
            body = resp["Payload"].read().decode("utf-8")
            if resp.get("StatusCode") != 200 or resp.get("FunctionError"):
                stop = "lambda error: status=%s fn_error=%s body=%s" % (
                    resp.get("StatusCode"), resp.get("FunctionError"), body[:300])
            else:
                payload = json.loads(body)
        except Exception as exc:  # noqa: BLE001
            stop = "invoke exception: " + type(exc).__name__ + ": " + str(exc)[:200]
        if stop is None:
            if payload.get("complete_markers") != [mkey]:
                stop = "unexpected complete_markers: " + json.dumps(payload.get("complete_markers"))[:200]
        if stop is None:
            h = s3.head_object(Bucket=BUCKET, Key=mkey)
            new_v = h.get("VersionId")
            marker = json.loads(s3.get_object(Bucket=BUCKET, Key=mkey, VersionId=new_v)["Body"].read())
            closure = marker.get("closure") if isinstance(marker, dict) else None
            if not isinstance(closure, dict):
                stop = "record has no closure object"
            else:
                f = cat.membership_findings(marker, closure, MASTER, d, contract)
                v = cat.validate_closure(closure, contract.masters)
                qualified = (not any(x["class"] in rejected for x in f)
                             and v["status"] == cat.RESULT_QUALIFIED)
                if not qualified:
                    stop = "record NOT QUALIFIED: " + json.dumps(sorted({x["class"] for x in f}))
                elif new_v == prior:
                    stop = "no new version was written (version unchanged " + str(new_v) + ")"
        if stop is not None:
            rec["stopped"] = {"at": utc(), "date": d, "why": stop}
            save()
            print("STOP at", d, stop)
            return 1
        rec["writes"].append({
            "master": MASTER, "date": d, "bronze_keys": len(keys), "invoked_utc": utc(),
            "seconds": round(time.time() - t0, 1), "run_id": payload.get("run_id"),
            "manifest_key": (payload.get("manifests") or [None])[0],
            "marker_key": mkey, "marker_version_id": new_v, "prior_marker_version_id": prior,
            "closure_status": closure.get("status"), "closure_id": closure.get("closure_id"),
            "write_guard": closure.get("write_guard"), "converted": payload.get("converted")})
        rec["masters"][MASTER]["backfilled"].append(d)
        rec["masters"][MASTER]["unavailable"].pop(d, None)
        rec["stopped"] = None
        save()
        n += 1
        if phase_d:
            hits = dispatched_lines(logs, d_start_ms)
            if hits:
                rec["stopped"] = {"at": utc(), "date": d, "why": "STOP RULE: %d dispatched: doc= line(s) in the "
                                  "dispatcher log since %s" % (hits, rec["phase_d_started_utc"])}
                save()
                print("STOP at", d, rec["stopped"]["why"])
                return 1
        print(d, "OK", new_v, "prior", prior, "%.1fs" % (time.time() - t0), flush=True)
    if phase_d and len(rec["masters"][MASTER]["backfilled"]) == len(dates):
        time.sleep(90)  # let the last records' dispatcher invocations reach the log before the final read
        hits = dispatched_lines(logs, d_start_ms)
        rec["phase_d_dispatched_doc_lines"] = hits
        if hits:
            rec["stopped"] = {"at": utc(), "date": None, "why": "STOP RULE at final read: %d dispatched: doc= line(s)" % hits}
            save()
            print("STOP", rec["stopped"]["why"])
            return 1
    key = "phase_d_finished_utc" if phase_d else "finished_utc"
    rec[key] = utc() if len(rec["masters"][MASTER]["backfilled"]) == len(dates) else None
    save()
    print("backfilled", len(rec["masters"][MASTER]["backfilled"]), "of", len(dates))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
