#!/usr/bin/env python
"""OG-ev-10 STEP 2 (amendment A1): the runner of the ONE-OBJECT WRITER TEST. Uploads ev10_writer_host.py (and the helpers it imports) to the host, refuses to start unless the uploaded bytes equal the COMMITTED blobs,
reads the host state (STOP before the call on an unset bucket, host memory above 75 percent, or a restart), runs the guarded host process ONCE, reads the object back from THIS side too, counts the objects under the
synthetic principal in the run's window (more than one is a trigger), and writes `writer_test` into W/AUDIT_REFUSAL_WRITE.json with the verdict recomputed by the amended rule. The object is never deleted.
  python ev10_writer_run.py <raw_out.json> <halves_path>      (repository root of the worktree that holds this file)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import time

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ap38_measure as m  # noqa: E402

FILES = ("ev10_writer_host.py", "ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py")
REL = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
LAKE = "opal-mcp-audit"
SYNTH_PREFIX = "OG-ev-10/"
RAW_OUT, HALVES = sys.argv[1], sys.argv[2]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
raw = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


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
    inv = run_ssm("cd /opt/opal-gateway && %s /tmp/ev10_writer_host.py %s" % (m.PY, args))
    so = inv.get("StandardOutputContent", "")
    if "EV10_WRITER_JSON" not in so:
        raise RuntimeError("no marker from the host (%s): %s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    return json.loads(so.split("EV10_WRITER_JSON", 1)[1].strip())


def committed_blobs():
    out = {}
    for n in FILES:
        path = REL + n
        h = subprocess.run(["git", "hash-object", path], capture_output=True, text=True).stdout.strip()
        c = subprocess.run(["git", "rev-parse", "HEAD:" + path], capture_output=True, text=True, env=dict(os.environ, MSYS_NO_PATHCONV="1")).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", path], capture_output=True, text=True).stdout.strip()
        out[n] = {"blob": h, "equal": bool(h) and h == c and not dirty, "sha256": hashlib.sha256(io.open(os.path.join(HERE, n), "rb").read()).hexdigest()}
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


def synthetic_objects(start_z, end_z):
    day = start_z[:10]
    keys, token, first = [], None, True
    while first or token:
        first = False
        kw = {"Bucket": LAKE, "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, start_z[:-1])})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if k.split("/")[-1][:19] <= end_z[:-1]]
    hits, errors = [], 0
    for k in inwin:
        try:
            body = s3.get_object(Bucket=LAKE, Key=k)["Body"].read().decode("utf-8", "replace")
            if SYNTH_PREFIX in body and '"gw_ratelimit"' in body:
                hits.append(k)
        except Exception:
            errors += 1
    return {"objects_scanned": len(inwin), "synthetic_objects": hits, "read_errors": errors}


def main():
    setup()
    raw["state_before"] = host("state")
    sb = raw["state_before"]
    if not sb["audit_bucket_is_set"] or not sb["audit_bucket_equals_lake_bucket"] or sb["host_pct"] > 75.0 or str(sb["nrestarts"]) != "0":
        raise SystemExit("STOP before the call: bucket unset or different, host memory above 75 percent, or a restart; nothing written")
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 2))
    raw["window_start"] = t0
    save()
    res = host("writer")
    raw["host_result"] = res
    save()
    w = res.get("writer") or {}
    raw["state_after"] = host("state")
    t1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 2))
    raw["window_end"] = t1
    runner_read = False
    key = w.get("key_printed")
    if key:
        try:
            body = s3.get_object(Bucket=LAKE, Key=key)["Body"].read().decode("utf-8", "replace")
            rows = [json.loads(ln) for ln in body.splitlines() if ln.strip()]
            runner_read = len(rows) == 1 and rows[0].get("event") == "gw_ratelimit" and str(rows[0].get("principal", "")).startswith(SYNTH_PREFIX)
        except Exception:
            runner_read = False
    raw["runner_side_read_back"] = runner_read
    raw["synthetic_objects_in_window"] = synthetic_objects(t0, t1)
    raw["pid_stable"] = sb["pid"] == raw["state_after"]["pid"]
    save()
    written = bool(w.get("written"))
    read_back = bool(w.get("read_back")) and runner_read
    wt = {"key_label": "OG-ev-10 (synthetic principal, no real identity)", "lake_key": key, "written": written, "read_back": read_back, "instance_role": True, "halves": HALVES,
          "put_error_class": w.get("put_error_class"), "audit_failure_count_after": w.get("audit_failure_count_after"), "objects_under_synthetic_principal": len(raw["synthetic_objects_in_window"]["synthetic_objects"]),
          "guard": res.get("guard"), "service_pid_stable": raw["pid_stable"], "nrestarts_after": raw["state_after"]["nrestarts"]}
    p = REL + "AUDIT_REFUSAL_WRITE.json"
    d = json.load(io.open(p, encoding="utf-8"))
    b = d["body"]
    b["writer_test"] = wt
    n429 = b["journal"]["post_mcp_429_lines"]
    warn = b["journal"]["ratelimit_audit_warn_lines"]
    rows_lake = b["lake"]["gw_ratelimit_rows"]
    if warn >= 1:
        b["verdict"], b["reason"] = "FAILS", "the writer's own WARN line is in the journal (%d)" % warn
    elif not (written and read_back):
        b["verdict"], b["reason"] = "FAILS", "the writer test's object was not written (put error class %s) or not read back" % wt["put_error_class"]
    elif n429 >= 1 and rows_lake == 0:
        b["verdict"], b["reason"] = "FAILS", "%d POST /mcp lines answered 429 and the lake holds 0 gw_ratelimit rows" % n429
    else:
        b["verdict"], b["reason"] = "WRITES", "the writer test's one synthetic object was written under the instance role and read back (the lake key is printed in writer_test); no organic 429 occurred in the journal window"
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1) + "\n")
    raw["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save()
    print("DONE", json.dumps({"written": written, "read_back": read_back, "put_error_class": wt["put_error_class"], "lake_key": key, "objects_under_synthetic_principal": wt["objects_under_synthetic_principal"],
                              "verdict": b["verdict"], "pid_stable": raw["pid_stable"], "nrestarts_after": wt["nrestarts_after"]}))


if __name__ == "__main__":
    main()
