#!/usr/bin/env python
"""OG-ev-7 Step 2: the ONE ARMING (15 minutes, firm pinned, a PLACEHOLDER account reference: the CVO's and the CTO's CT2, so nothing here can reach a client's transactions) that measures etfs_compare_peers three
times through the listener of the RUNNING service (heap signal on / on / off) and once in a fresh guarded process, then DELETES the parameter. Any exception after the write deletes the parameter at once.
Preconditions checked here, each a STOP before any write: the uploaded bytes equal the COMMITTED blobs (their ids go into the record); the live ref is the GO's; the lease parameter is absent; the unarmed listener
answers 403 probe_not_armed (request 1 of 5); the firm READ on the host equals the ask's (49financial).
Counts, MB, seconds, shas and status words only: the lease carries no client reference and no response body is written.
  python ev7_run.py <raw_out.json> <PEERS_MEASURE.json>      (repository root of the worktree that holds this file)"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import shlex
import subprocess
import sys
import time

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ap38_measure as m  # noqa: E402

LEASE_PARAM = "/opal-gateway/probe/lease"
LEASE_MIN = 15
ORDER = "OG-ev-7"
ACCOUNT_REF = "****0000/probe/OG-ev-7"
ASK_FIRM = "49financial"
LIVE = "eff517546eeea48811cf13f3de38926c5944c6df"
FILES = ("ev7_probe_host.py", "ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py")
REL = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
RAW_OUT, REC_OUT = sys.argv[1], sys.argv[2]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
raw = {"started": None}


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def save():
    io.open(RAW_OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(raw, indent=1) + "\n")


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
    inv = run_ssm("cd /opt/opal-gateway && %s /tmp/ev7_probe_host.py %s" % (m.PY, args))
    so = inv.get("StandardOutputContent", "")
    if "EV7_PROBE_JSON" not in so:
        raise RuntimeError("no marker from the host (%s): %s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    return json.loads(so.split("EV7_PROBE_JSON", 1)[1].strip())


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


def committed_blobs():
    """The uploaded bytes must equal the COMMITTED blobs: git hash-object of the file equals rev-parse HEAD:<path>, and the file is clean."""
    out = {}
    for n in FILES:
        path = REL + n
        h = subprocess.run(["git", "hash-object", path], capture_output=True, text=True).stdout.strip()
        c = subprocess.run(["git", "rev-parse", "HEAD:" + path], capture_output=True, text=True, env=dict(os.environ, MSYS_NO_PATHCONV="1")).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", path], capture_output=True, text=True).stdout.strip()
        out[n] = {"blob": h, "committed_blob": c, "equal": bool(h) and h == c and not dirty, "sha256": hashlib.sha256(io.open(os.path.join(HERE, n), "rb").read()).hexdigest()}
    return out


def setup():
    raw["blobs"] = committed_blobs()
    if not all(v["equal"] for v in raw["blobs"].values()):
        raise SystemExit("STOP: an uploaded file differs from its committed blob")
    for n in FILES:
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(HERE, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in FILES)
    sums = " ; ".join("sha256sum /tmp/%s" % n for n in FILES)
    inv = run_ssm("cd /opt/opal-gateway && rm -f %s && %s && echo PULLED && %s" % (" ".join("/tmp/" + n for n in FILES), pulls, sums), 300)
    so = inv.get("StandardOutputContent", "")
    if "PULLED" not in so:
        raise SystemExit("STOP: the host scripts were not pulled")
    onhost = {ln.split()[1].replace("/tmp/", ""): ln.split()[0] for ln in so.splitlines() if ln.count(" ") >= 1 and ln.split()[1].startswith("/tmp/")}
    raw["host_sha256_equal"] = all(onhost.get(n) == raw["blobs"][n]["sha256"] for n in FILES)
    if not raw["host_sha256_equal"]:
        raise SystemExit("STOP: the uploaded bytes on the host differ from the committed blobs")


def abort(why):
    delete_param()
    raw["aborted"] = why
    raw["emergency_delete"] = True
    raw["parameter_exists_after_abort"] = param_exists()
    save()
    raise SystemExit("ABORT: " + why)


def state_read():
    inv = run_ssm("echo MARKER=$(cat /opt/opal-gateway/.deployed_commit); echo ENVKEYS=$(grep -cE '^[A-Za-z_][A-Za-z0-9_]*=' /opt/opal-gateway/.env); "
                  "echo PROCS=$(ps -eo args | grep -E 'uvicorn app.server' | grep -v grep | wc -l); systemctl show opal-gateway -p MemoryMax -p MemoryHigh -p OOMScoreAdjust -p NRestarts -p MainPID", 120)
    kv = {}
    for ln in inv.get("StandardOutputContent", "").splitlines():
        if "=" in ln:
            k, v = ln.split("=", 1)
            kv[k.strip()] = v.strip()
    return {"marker_is_live_sha": kv.get("MARKER") == LIVE, "marker_short": (kv.get("MARKER") or "")[:10], "env_keys": kv.get("ENVKEYS"), "uvicorn_processes": kv.get("PROCS"), "nrestarts": kv.get("NRestarts"),
            "main_pid": kv.get("MainPID"), "memory_max": kv.get("MemoryMax"), "memory_high": kv.get("MemoryHigh"), "oom_score_adj": kv.get("OOMScoreAdjust")}


def verdict_of(calls, fresh):
    w = [c["wall_s"] for c in calls]
    if w[0] >= 2 * w[1]:
        return "COLD"
    if all(x > 2 * fresh for x in w):
        return "SLOW_IN_SERVICE"
    if w[2] <= 0.8 * w[1]:
        return "SIGNAL_COST"
    return "INCONCLUSIVE"


def lake_labels(start, end):
    day = start[:10]
    keys, token, first = [], None, True
    while first or token:
        first = False
        kw = {"Bucket": "opal-mcp-audit", "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, start[:-1])})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if k.split("/")[-1][:19] <= end[:-1]]
    total = armed = unarmed = errors = 0
    for k in inwin:
        try:
            for ln in s3.get_object(Bucket="opal-mcp-audit", Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    total += 1
                    armed += ("probe:%s" % ORDER) in ln
                    unarmed += "probe:unarmed" in ln
        except Exception:
            errors += 1
    return {"objects_in_window": len(inwin), "records_in_window": total, "probe_og_ev_7_labelled": armed, "probe_unarmed_labelled": unarmed, "read_errors": errors}


def main():
    raw["started"] = stamp()
    setup()
    raw["state_before"] = host("state")
    raw["host_before"] = state_read()
    pid0 = raw["state_before"]["pid"]
    if not raw["host_before"]["marker_is_live_sha"]:
        raise SystemExit("STOP: the live ref is not the GO's")
    raw["parameter_absent_before"] = not param_exists()
    if not raw["parameter_absent_before"]:
        raise SystemExit("STOP: a lease parameter exists before the arming")
    t_start = now() - dt.timedelta(seconds=2)
    raw["window_start"] = t_start.strftime("%Y-%m-%dT%H:%M:%SZ")
    raw["unarmed_call"] = host("call")                                          # request 1 of 5: no lease -> 403 probe_not_armed
    save()
    if raw["unarmed_call"].get("status") != 403 or raw["unarmed_call"].get("error") != "probe_not_armed":
        raise SystemExit("STOP: the unarmed listener did not answer 403 probe_not_armed")
    fp = host("firmpair")
    raw["firm_read"] = (fp.get("firm") or {}).get("canonical_firm")
    raw["firm_asked"] = ASK_FIRM
    raw["pair_outcome"] = (fp.get("pair") or {}).get("outcome")
    pair = fp.get("pair") or {}
    save()
    if raw["firm_read"] != ASK_FIRM:
        raise SystemExit("STOP: the firm read on the host (%s) differs from the ask's, nothing written" % raw["firm_read"])
    if not pair.get("period") or not pair.get("axis"):
        raise SystemExit("STOP: no valid period and axis resolved, nothing written")
    set_at = now()
    expires = set_at + dt.timedelta(minutes=LEASE_MIN)
    lease = {"order": ORDER, "account_ref": ACCOUNT_REF, "firm": raw["firm_read"], "set_at": set_at.isoformat(), "expires_at": expires.isoformat()}
    ssm.put_parameter(Name=LEASE_PARAM, Value=json.dumps(lease), Type="String", Overwrite=False, Description="OG-ev-7 probe lease (one arming, 15 minutes, placeholder account)")
    raw["armings"] = 1
    raw["lease_as_written"] = {"order": ORDER, "account_ref_masked": "****0000/probe/<alias>", "firm": raw["firm_read"], "set_at": set_at.strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"), "minutes": LEASE_MIN}
    save()
    try:
        time.sleep(7)                                                           # the unarmed read may sit in the listener's 5-second cache
        three = host("three %s %s" % (shlex.quote(pair["period"]), shlex.quote(pair["axis"])))
        raw["three"] = three
        save()
        if three.get("stopped_early") or three.get("calls_made") != 3:
            abort("the three-call run stopped early (a status other than 200, VmRSS over 1200 MB, a PID change, or host memory over 85 percent)")
        raw["fresh"] = host("fresh %s %s" % (shlex.quote(pair["period"]), shlex.quote(pair["axis"])))
        save()
        delete_param()
        raw["deleted_at"] = stamp()
        raw["parameter_not_found_after_delete"] = not param_exists()
        time.sleep(7)                                                           # the 5-second cache, then the 6-second wait of the CVO's condition (c)
        raw["closed_call"] = host("call")                                       # request 5 of 5
        raw["closed_call_at"] = stamp()
    finally:
        if param_exists():
            delete_param()
            raw["emergency_delete"] = True
            raw["deleted_at"] = raw.get("deleted_at") or stamp()
        raw["parameter_exists_at_end"] = param_exists()
        save()
    raw["state_after"] = host("state")
    raw["host_after"] = state_read()
    time.sleep(3)
    raw["window_end"] = (now() + dt.timedelta(seconds=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sys.path.insert(0, HERE)
    import ap44_accesslog as al
    jr = al.journal(raw["window_start"], raw["window_end"])
    raw["counts"] = {"window_start": raw["window_start"], "window_end": raw["window_end"], "journal_post_mcp": jr.get("post_mcp_lines"), "journal_post_probe": jr.get("post_probe_lines"), "lake": lake_labels(raw["window_start"], raw["window_end"])}
    calls = [{"n": c["n"], "wall_s": c["wall_s"], "vmrss_mb": c["vmrss_mb"], "hwm_mb": c["hwm_mb"], "service_pid": c["service_pid"], "heap_signal": c["heap_signal"]} for c in raw["three"]["calls"]]
    fresh = raw["fresh"].get("wall_s")
    closed = raw["closed_call"]
    body = {"lease_minutes": LEASE_MIN, "armings": raw["armings"], "firm_pinned": True, "firm_as_read": raw["firm_read"], "calls": calls, "fresh_process_wall_s": fresh,
            "fresh_process_rows": raw["fresh"].get("rows_matched"), "fresh_process_hwm_mb": raw["fresh"].get("vm_hwm_mb"), "rows_per_service_call": [c["rows_matched"] for c in raw["three"]["calls"]],
            "verdict": verdict_of(calls, fresh), "parameter_not_found_after_delete": raw["parameter_not_found_after_delete"],
            "listener_closed_at_rest": closed.get("status") == 403 and closed.get("error") == "probe_not_armed", "nrestarts_after": int(raw["host_after"]["nrestarts"] or -1),
            "lease_as_written": raw["lease_as_written"], "deleted_at": raw["deleted_at"], "counts": raw["counts"], "committed_blobs": {k: v["blob"] for k, v in raw["blobs"].items()},
            "service_pid_throughout": all(c["service_pid"] == pid0 for c in calls) and raw["state_after"]["pid"] == pid0}
    io.open(REC_OUT, "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
    raw["finished"] = stamp()
    save()
    print("DONE", json.dumps({"walls": [c["wall_s"] for c in calls], "vmrss": [c["vmrss_mb"] for c in calls], "fresh": fresh, "verdict": body["verdict"], "deleted_at": raw["deleted_at"],
                              "post_probe": raw["counts"]["journal_post_probe"], "lake": raw["counts"]["lake"]}))


if __name__ == "__main__":
    main()
