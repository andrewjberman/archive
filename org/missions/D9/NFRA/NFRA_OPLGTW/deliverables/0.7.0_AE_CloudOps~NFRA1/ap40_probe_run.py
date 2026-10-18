#!/usr/bin/env python
"""OG-ap-40 Phase B: the ONE ARMING (CTO ruling, msg 35661; A5): write the lease once (25 minutes), run the probes through the listener of the RUNNING service, let that same lease lapse on its own and show the
next call refused, then DELETE the parameter, show ParameterNotFound and a refused call. Any stop (the first call refused twice, a VmRSS over 1200 MB, an error) deletes the parameter at once.
Counts, MB, seconds, hashes and status words only: the account reference travels from the host's guarded child to the lease parameter inside this process and is never printed or written.
  python ap40_probe_run.py <out.json>      (repository root; the host side is ap40_probe_host.py, uploaded here)"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import shlex
import sys
import time

import boto3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

LEASE_PARAM = "/opal-gateway/probe/lease"
LEASE_MIN = 25
MAX_PAGES = 12
OUT = sys.argv[1]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
raw = {"started": None}


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def save():
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(raw, indent=1) + "\n")


def run_ssm(cmd, timeout=900):
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=timeout)["Command"]["CommandId"]
    inv = None
    for _ in range(timeout // 3):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    return inv


def host(args):
    inv = run_ssm("cd /opt/opal-gateway && %s /tmp/ap40_probe_host.py %s" % (m.PY, args))
    so = inv.get("StandardOutputContent", "")
    ref = None
    for ln in so.splitlines():
        if ln.startswith("AP40_REF "):
            ref = ln[len("AP40_REF "):].strip() or None
    if "AP40_PROBE_JSON" not in so:
        raise RuntimeError("no marker from the host (%s): %s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    return json.loads(so.split("AP40_PROBE_JSON", 1)[1].strip()), ref


def param_exists():
    try:
        ssm.get_parameter(Name=LEASE_PARAM)
        return True
    except ssm.exceptions.ParameterNotFound:
        return False


def delete_param():
    try:
        ssm.delete_parameter(Name=LEASE_PARAM)
    except ssm.exceptions.ParameterNotFound:
        pass


def setup():
    here = os.path.dirname(os.path.abspath(__file__))
    for n in ("ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py"))
    inv = run_ssm("cd /opt/opal-gateway && rm -f /tmp/ap40_probe_host.py && %s && echo PULLED" % pulls, 300)
    if "PULLED" not in inv.get("StandardOutputContent", ""):
        raise RuntimeError("the host scripts were not pulled")


def abort(why):
    delete_param()
    raw["aborted"] = why
    raw["emergency_delete"] = True
    raw["parameter_exists_after_abort"] = param_exists()
    save()
    raise SystemExit("ABORT: " + why)


def audit_counts(start, end):
    day = start[:10]
    keys, token = [], None
    first = True
    while first or token:
        first = False
        kw = {"Bucket": "opal-mcp-audit", "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, start[:-1])})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if k.split("/")[-1][:19] <= end[:-1]]
    armed = unarmed = total = errors = 0
    for k in inwin:
        try:
            for ln in s3.get_object(Bucket="opal-mcp-audit", Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    total += 1
                    armed += "probe:OG-ap-40" in ln
                    unarmed += "probe:unarmed" in ln
        except Exception:
            errors += 1
    return {"window_start": start, "window_end": end, "objects_in_window": len(inwin), "records_in_window": total, "probe_og_ap_40_labelled": armed, "probe_unarmed_labelled": unarmed, "read_errors": errors}


def main():
    raw["started"] = stamp()
    setup()
    raw["state_before"], _ = host("state")
    pid0 = raw["state_before"]["pid"]
    raw["parameter_absent_before"] = not param_exists()
    if not raw["parameter_absent_before"]:
        abort("a lease parameter exists before the arming (C2)")
    raw["unarmed_call"], _ = host("call")                                       # C8 (1): no lease -> 403 probe_not_armed
    save()
    gathered, ref = host("gather")
    raw["gather"] = gathered
    pair = gathered.get("pair") or {}
    if not ref or not pair.get("period") or not pair.get("axis"):
        abort("the test account's reference or a valid period and axis was not resolved")
    set_at = now()
    expires = set_at + dt.timedelta(minutes=LEASE_MIN)
    lease = {"order": "OG-ap-40", "account_ref": ref, "set_at": set_at.isoformat(), "expires_at": expires.isoformat()}
    ssm.put_parameter(Name=LEASE_PARAM, Value=json.dumps(lease), Type="String", Overwrite=False, Description="OG-ap-40 probe lease (one arming, 25 minutes)")
    ref = None
    lease = None
    raw["armings"] = 1
    raw["lease"] = {"minutes": LEASE_MIN, "armed_at": set_at.strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"), "order": "OG-ap-40"}
    save()
    try:
        time.sleep(7)                                                           # the unarmed read of the call above may sit in the 5-second cache
        raw["peers"], _ = host("peers %s %s" % (shlex.quote(pair["period"]), shlex.quote(pair["axis"])))
        save()
        pr = raw["peers"]
        if pr.get("c15_stop"):
            abort("C15: the first call after the lease was written answered 403 probe_not_armed twice")
        if pr.get("status") != 200 or pr.get("over_1200") or pr.get("pid_after") != pid0:
            abort("the peers probe did not answer 200 with the PID stable and VmRSS at or under 1200 MB")
        raw["chain"], _ = host("chain %d" % MAX_PAGES)
        save()
        ch = raw["chain"]
        if ch.get("stopped_over_1200") or ch.get("pid_after") != pid0:
            abort("the window chain passed 1200 MB or the service PID changed")
        raw["refusals"], _ = host("refuse")
        save()
        # the ONE lease lapses on its own
        while now() < expires + dt.timedelta(seconds=8):
            time.sleep(10)
        raw["parameter_present_at_expiry"] = param_exists()
        raw["expired_call"], _ = host("call")
        raw["expired_call_at"] = stamp()
        save()
        delete_param()
        raw["deleted_at"] = stamp()
        raw["parameter_not_found_after_delete"] = not param_exists()
        time.sleep(7)                                                           # the 5-second cache, then the wait of the CVO's condition 3
        raw["closed_call"], _ = host("call")
        raw["closed_call_at"] = stamp()
    finally:
        if param_exists():
            delete_param()
            raw["emergency_delete"] = True
        raw["parameter_exists_at_end"] = param_exists()
        save()
    raw["state_after"], _ = host("state")
    raw["audit_lake"] = audit_counts(raw["lease"]["armed_at"], stamp())
    raw["finished"] = stamp()
    save()
    print("DONE", json.dumps({"pid_stable": raw["state_after"]["pid"] == pid0, "nrestarts": raw["state_after"]["nrestarts"]}))


if __name__ == "__main__":
    main()
