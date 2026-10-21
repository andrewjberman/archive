#!/usr/bin/env python
"""OG-rl-18 Phase B: the `masterwide` measurements from the DEPLOYED tree (/opt/opal-gateway), every gateway-code run in a FRESH process under the cgroup hard guard (rl18_host.py's children). READ ONLY; the running service is not touched.
  (1) the sentinel scope parses in the deployed tree (rl18_host.py --sentinel);  (2) the explicit-scope comparison of Phase A step 3(b) is run against the deployed code (rl18_host.py --explicit) and compared with the live ref's answers recorded in
  Phase A (W/rl18_pa/host.json `explicit_live`, the same fixture ids);  (3) the store re-scan is rl18_sentinel_scan.py, run by the caller.
usage: python rl18_post.py <out.json> <phase_a_host.json>   (RUNNER, repository root)  |  python rl18_post.py --driver   (host)"""
from __future__ import annotations

import io
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

FILES = ["rl18_host.py", "rl18_post.py", "ap38_measure.py", "ap38_guard.py"]
KEYS = ("parsed", "masters", "check_scope", "resolver_candidate_list", "schwab_account_filter", "scope_summary_account_count")


def driver():
    import rl18_host as h
    expect = json.load(open("/tmp/rl18_post_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "marker_host": open("/opt/opal-gateway/.deployed_commit").read().strip()}
    pid0, nr0 = h.read_pid()
    out["pct_before"] = m.host_pct()
    if out["pct_before"] >= m.STOP_PCT:
        out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
        return out
    out["sentinel"] = h.run_child(["--sentinel", "/opt/opal-gateway"])
    out["explicit_deployed"] = h.run_child(["--explicit", "/opt/opal-gateway"])
    out["explicit_equal_to_live_ref_answers"] = all(out["explicit_deployed"].get(k) is not None and out["explicit_deployed"].get(k) == expect.get(k) for k in KEYS)
    pid1, nr1 = h.read_pid()
    out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
    return out


def runner(outp, expect_src):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    exp = json.load(io.open(expect_src, encoding="utf-8"))["explicit_live"]
    for n in FILES:
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/rl18_post_expect.json", Body=json.dumps({k: exp[k] for k in KEYS}).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in FILES + ["rl18_post_expect.json"]]
    cmd = ("cd /opt/opal-gateway && rm -f %s && %s && %s /tmp/rl18_post.py --driver; rc=$?; rm -f %s; exit $rc"
           % (" ".join("/tmp/" + n for n in FILES + ["rl18_post_expect.json"]), " && ".join(pulls), m.PY, " ".join("/tmp/" + n for n in FILES + ["rl18_post_expect.json"])))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "RL18_POST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL18_POST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    sentinel_ok = doc.get("sentinel", {}).get("parses") is True and doc["sentinel"].get("is_master_wide") == [True, False] and doc["sentinel"].get("malformed_shapes_refused") == [True, True, True]
    doc["masterwide_partial"] = {"sentinel_parse_in_deployed_tree": bool(sentinel_ok), "explicit_scope_unchanged": doc.get("explicit_equal_to_live_ref_answers") is True,
                                 "explicit_scope_compared_with": "the live ref 2923d1ee99's answers recorded in Phase A (rl18_pa/host.json explicit_live), same fixture ids"}
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1)[:2500])


if __name__ == "__main__":
    if "--driver" in sys.argv:
        print("RL18_POST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
