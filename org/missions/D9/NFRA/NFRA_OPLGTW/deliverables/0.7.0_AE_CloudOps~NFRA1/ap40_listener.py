#!/usr/bin/env python
"""OG-ap-40 Phase A step 3: exercise the CANDIDATE loopback probe listener on the gateway host, in a FRESH process under the cgroup hard guard, with a FAKE lease source.
READ ONLY on the service: it is not touched (its MainPID is read before and after). The candidate is a scratch copy of the installed app/ and lib/ with the three release files laid over it
(their sha256 are checked against the release blobs); nothing is written to SSM, S3 or the audit lake (the audit call is captured in memory). Counts, booleans and fixed words only.
  python ap40_listener.py <out.json> <expect.json>   -> RUNNER (repository root): uploads this file, ap38_measure.py, the guard and the three candidate files; runs once over SSM
  python ap40_listener.py --driver                   -> HOST DRIVER (runs no gateway code; spawns the guarded children)
  python ap40_listener.py --resolve <stage>          -> HOST CHILD 1: resolves the test account's reference (written to <stage>/ref.txt, mode 600, never printed)
  python ap40_listener.py --listener <stage>         -> HOST CHILD 2: starts the candidate listener on 127.0.0.1:8099 and exercises it
expect.json = {"<published name>": "<sha256 of the release blob>", ...} for probe_listener.py, server.py and test_og_pr1.py."""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

CAND = {"probe_listener.py": "app/probe_listener.py", "server.py": "app/server.py"}
S3_PREFIX = "ec2/opal-gateway/ap40_cand/"
PORT = 8099
LEASE_MIN = 45


def parse_rss_mb(line, key):
    for tok in line.split():
        if tok.startswith(key + "="):
            digits = "".join(ch for ch in tok.split("=", 1)[1] if ch.isdigit())
            return round(int(digits) / 1024.0, 1) if digits else None
    return None


# ----------------------------------------------------------------------------------------------------- child 1: the test account's reference
def child_resolve(stage):
    cap = []
    real_emit = m.emit
    m.emit = cap.append
    try:
        m.child_resolve(stage)
    finally:
        m.emit = real_emit
    real_emit({"ref_resolved": bool(cap and cap[-1].get("ref_resolved"))})


# ----------------------------------------------------------------------------------------------------- child 2: the listener
def child_listener(stage):
    m.load_env(stage)
    import asyncio
    import datetime as dt
    import logging
    import signal
    import socket
    import urllib.error
    import urllib.request
    from app import audit
    from app import probe_listener as pl
    from app import server as srv

    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    records, logs = [], []
    audit.log_call = lambda *a, **k: records.append((a[1], a[3], str(a[4]), a[0]))
    handler = logging.Handler()
    handler.emit = lambda rec: logs.append(rec.getMessage())
    logging.getLogger("opal.gateway.probe").addHandler(handler)

    lease = [None]
    pl.LEASE_READER = lambda: lease[0]

    def lease_json(minutes, account, set_back=0):
        now = dt.datetime.now(dt.timezone.utc)
        return json.dumps({"order": "OG-ap-40", "account_ref": account, "set_at": (now - dt.timedelta(minutes=set_back)).isoformat(),
                           "expires_at": (now - dt.timedelta(minutes=set_back) + dt.timedelta(minutes=minutes)).isoformat()})

    def post_sync(tool, body, raw=None):
        data = raw if raw is not None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:%d/probe/%s" % (PORT, tool), data=data, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=100) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read().decode("utf-8"))
            except Exception:
                return exc.code, {}
        except Exception as exc:                       # a refused oversized body may reset the client's write: say so, never crash
            return -1, {"error": "connection:" + type(exc).__name__}

    async def main():
        loop = asyncio.get_running_loop()
        out = {"hookup": {"server_imports": True, "server_has_probe_listener": hasattr(srv, "probe_listener")}}
        task = pl.start()
        for _ in range(200):
            if getattr(pl._state.get("server"), "started", False):
                break
            await asyncio.sleep(0.05)
        out["listener_started"] = bool(getattr(pl._state.get("server"), "started", False))
        out["signal_installed"] = pl.install_heap_signal()

        out["http_requests"] = 0

        async def post(tool, body, raw=None):
            out["http_requests"] += 1
            return await loop.run_in_executor(None, post_sync, tool, body, raw)

        # the bind, read from the kernel, and the private-address connection attempt
        ss = subprocess.run(["ss", "-ltn"], capture_output=True, text=True).stdout
        rows = [ln.split() for ln in ss.splitlines() if (":%d " % PORT) in (ln + " ")]
        out["bound"] = sorted({r[3].rsplit(":", 1)[0] for r in rows if len(r) > 3})
        ip = (subprocess.run(["hostname", "-I"], capture_output=True, text=True).stdout.split() or [""])[0]
        if not ip:
            addr = subprocess.run(["ip", "-4", "-o", "addr", "show", "scope", "global"], capture_output=True, text=True).stdout.split()
            ip = next((t.split("/")[0] for i, t in enumerate(addr) if i and addr[i - 1] == "inet"), "")
        try:
            socket.create_connection((ip, PORT), timeout=3).close()
            out["private_address_connect"] = "connected"
        except ConnectionRefusedError:
            out["private_address_connect"] = "refused"
        except OSError as exc:
            out["private_address_connect"] = "error:" + type(exc).__name__
        out["private_address_present"] = bool(ip)

        heap0 = pl.heap_read()
        # 1. unarmed: nothing served
        lease[0] = None
        pl.reset_lease_cache()
        s, b = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": "x", "axis": "x"})
        out["unarmed"] = {"status": s, "error": b.get("error")}
        # 2. armed for LEASE_MIN minutes on the test account
        lease[0] = lease_json(LEASE_MIN, ref)
        pl.reset_lease_cache()
        s0, b0 = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": "x", "axis": "x"})
        ps, axs = m.lists_under(b0, "available_periods"), m.lists_under(b0, "available_axes")
        period, axis = next((v[0] for v in ps if v), None), next((v[0] for v in axs if v), None)
        out["peers_listing"] = {"status": s0, "periods_listed": sum(len(v) for v in ps), "axes_listed": sum(len(v) for v in axs)}
        s1, b1 = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": period, "axis": axis})
        bb = (m.dict_under(b1, "buying") or {}).get("rows") or []
        cc = (m.dict_under(b1, "contribution") or {}).get("rows") or []
        out["peers_valid_pair"] = {"status": s1, "rows_matched": len(bb) + len(cc), "pair_found": bool(period and axis)}
        today = dt.datetime.now(dt.timezone.utc).date()
        frm = (today - dt.timedelta(days=m.WINDOW_DAYS)).isoformat()
        cur, pages = today.isoformat(), []
        for _n in range(2):
            s2, b2 = await post("client_get_transactions", {"firm": m.FIRM, "account": ref, "platform": None, "from_date": frm, "to_date": cur})
            pages.append({"status": s2, "rows": len(m.rows_of(b2)), "error": b2.get("error"), "absent_reason": b2.get("absent_reason"), "next_cursor_present": b2.get("next_cursor") is not None})
            if s2 != 200 or b2.get("next_cursor") is None:
                break
            cur = b2.get("next_cursor")
        out["transactions"] = {"status": pages[0]["status"], "pages": len(pages), "rows_per_page": [x["rows"] for x in pages], "page_detail": pages}
        s3, b3 = await post("client_get_fees", {"firm": m.FIRM, "account": ref})
        out["other_tool"] = {"status": s3, "error": b3.get("error")}
        s4, b4 = await post("client_get_transactions", {"firm": m.FIRM, "account": "****0000/blackdiamond/other", "platform": None, "from_date": None, "to_date": None})
        out["other_account"] = {"status": s4, "error": b4.get("error")}
        s5, b5 = await post("etfs_compare_peers", None, raw=b"x" * 70000)
        out["oversized_body"] = {"status": s5, "error": b5.get("error")}
        s6, b6 = await post("etfs_compare_peers", None, raw=b"{not json")
        out["bad_json"] = {"status": s6, "error": b6.get("error")}
        # 3. expiry: the clock passes expires_at with no restart; an over-long lease; a malformed lease
        real_clock = pl.CLOCK
        pl.CLOCK = lambda: dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=LEASE_MIN + 5)
        pl.reset_lease_cache()
        s7, b7 = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": period, "axis": axis})
        out["after_expiry"] = {"status": s7, "error": b7.get("error")}
        pl.CLOCK = real_clock
        lease[0] = lease_json(120, ref)
        pl.reset_lease_cache()
        s8, b8 = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": period, "axis": axis})
        out["over_long_lease"] = {"status": s8, "error": b8.get("error")}
        lease[0] = "{not a lease"
        pl.reset_lease_cache()
        s9, b9 = await post("etfs_compare_peers", {"home_ticker": "IDVZ", "period": period, "axis": axis})
        out["malformed_lease"] = {"status": s9, "error": b9.get("error")}
        # 4. the heap read by signal, and the audit labels
        heap1 = pl.heap_read()
        n_before = len(logs)
        os.kill(os.getpid(), signal.SIGUSR2)
        await asyncio.sleep(0.5)
        out["heap"] = {"before_mb": parse_rss_mb(heap0, "VmRSS"), "after_mb": parse_rss_mb(heap1, "VmRSS"), "hwm_mb": parse_rss_mb(heap1, "VmHWM"),
                       "signal_line_written": len(logs) > n_before and any(x.startswith("probe heap pid=") for x in logs[n_before:])}
        labelled = [r for r in records if r[2].startswith("probe:")]
        unlabelled = {}
        for r in records:
            if not r[2].startswith("probe:"):
                unlabelled["%s/%s" % (r[0], r[1])] = unlabelled.get("%s/%s" % (r[0], r[1]), 0) + 1
        out["audit"] = {"records": len(records), "http_requests": out["http_requests"], "probe_labelled": len(labelled),
                        "all_labelled": len(labelled) == out["http_requests"],
                        "armed_label": sum(1 for r in labelled if r[2].startswith("probe:OG-ap-40")), "unarmed_label": sum(1 for r in labelled if r[2].startswith("probe:unarmed")),
                        "ok_outcomes": sorted({r[0] for r in labelled if r[1] == "ok"}), "unlabelled_tool_own_records": unlabelled}
        pl._state["server"].should_exit = True
        await pl.stop(task)
        return out

    res = asyncio.run(main())
    res["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(res)


# ----------------------------------------------------------------------------------------------------- host driver
def read_pid():
    rc, out = m.sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return kv.get("MainPID"), kv.get("NRestarts")


def run_child(flag, stage):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120",
           os.path.abspath(__file__), flag, stage]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-400:]}
    res["exit_code"] = p.returncode
    return res


def driver():
    import hashlib
    expect = json.load(open("/tmp/ap40_expect.json"))
    stage = "/tmp/ap40_stage_%d" % os.getpid()
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        pid0, nr0 = read_pid()
        os.makedirs(stage, mode=0o700)
        shutil.copytree("/opt/opal-gateway/app", stage + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree("/opt/opal-gateway/lib", stage + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        got = {}
        for name, rel in CAND.items():
            shutil.copyfile("/tmp/ap40_cand_" + name, os.path.join(stage, rel))
            got[name] = hashlib.sha256(open(os.path.join(stage, rel), "rb").read()).hexdigest()
        out["candidate_bytes_equal_release"] = {n: got[n] == expect[n] for n in CAND}
        if not all(out["candidate_bytes_equal_release"].values()):
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        out["resolve"] = run_child("--resolve", stage)
        if out["resolve"].get("ref_resolved"):
            out["listener"] = run_child("--listener", stage)
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
        rc, ssout = m.sh("ss -ltn")
        out["port_free_after"] = (":%d " % PORT) not in (ssout + " ")
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.getcwd()
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("ap40_listener.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    gw = "C:/tmp/og-rel-batch9/infra/aws/ec2/opal-gateway/"
    for name, rel in CAND.items():
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + name, Body=io.open(gw + rel, "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap40_listener.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/ap40_cand_%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, n, n) for n in CAND]
    pulls += ["aws s3 cp s3://%s/%sexpect.json /tmp/ap40_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap40_listener.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap40_cand_* /tmp/ap40_expect.json && %s && %s /tmp/ap40_listener.py --driver" % (" && ".join(pulls), m.PY)
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=900)["Command"]["CommandId"]
    inv = None
    for _ in range(220):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AP40_LISTENER_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP40_LISTENER_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))
    os.chdir(root)


if __name__ == "__main__":
    if "--resolve" in sys.argv:
        child_resolve(sys.argv[sys.argv.index("--resolve") + 1])
    elif "--listener" in sys.argv:
        child_listener(sys.argv[sys.argv.index("--listener") + 1])
    elif "--driver" in sys.argv:
        print("AP40_LISTENER_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
