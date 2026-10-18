#!/usr/bin/env python
"""OG-ap-39 Phase B, arm e13_notes_served and `served_notes` (amendments A3 and A5; the CVO's row Z-S385): read the served tool descriptions from the INSTALLED code's tool registry, in a FRESH process under the cgroup hard guard.
READ ONLY. Counts and booleans only: no description text is written to the record.
  python ap39_notes.py <out.json>     -> RUNNER (repository root): uploads this file, ap38_measure.py and the guard; runs once over SSM
  python ap39_notes.py --driver       -> HOST DRIVER (runs no gateway code; spawns the guarded child)
  python ap39_notes.py --notes <stage> -> HOST CHILD: imports the installed app.tools and reads the registry
The scratch stage holds symlinks app/ and lib/ to the installed folders (no copy); it is removed after."""
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

CODES = ("window_read_busy", "no_partition_at_as_of", "no_model_assignment_49f", "no_candidate_for_last4", "account_not_in_partition", "no_fee_rows_in_window",
         "window_required", "window_too_long", "no_model_assignment", "model_not_in_roster")
BANNED = ("true zero", "report zero", "zero fees")


def child_notes(stage):
    m.load_env(stage)
    from app import tools
    reg = {t.name: (getattr(t, "description", "") or "") for t in tools.mcp._tool_manager.list_tools()}
    clients = {n: d for n, d in reg.items() if n.startswith("client_")}
    with_notes = sorted(n for n, d in clients.items() if any(c in d for c in CODES))
    fee = clients.get("client_get_fees", "")
    out = {"tools_list_count": len(reg), "client_tools": len(clients), "client_tools_with_notes": len(with_notes), "client_tools_with_notes_names": with_notes,
           "window_read_busy_in_windowed_tools": all("window_read_busy" in clients.get(n, "") for n in ("client_get_transactions", "client_get_fees")),
           "fee_note_names_the_source": "source" in fee, "fee_note_denies_a_total": "does not establish a total" in fee,
           "fee_note_banned_phrases_present": [b for b in BANNED if b in fee]}
    out["client_get_fees_note_source_scoped"] = bool(out["fee_note_names_the_source"] and out["fee_note_denies_a_total"] and not out["fee_note_banned_phrases_present"])
    m.emit(out)


def driver():
    stage = "/tmp/ap39_notes_%d" % os.getpid()
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120",
               os.path.abspath(__file__), "--notes", stage]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
        out["notes"] = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stderr_tail": p.stderr[-300:], "stdout_tail": p.stdout[-200:]}
        out["exit_code"] = p.returncode
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    for n in ("ap39_notes.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap39_notes.py", "ap38_measure.py", "ap38_guard.py"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap39_notes.py /tmp/ap38_measure.py /tmp/ap38_guard.py && %s && %s /tmp/ap39_notes.py --driver" % (pulls, m.PY)
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
    if "AP39_NOTES_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP39_NOTES_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--notes" in sys.argv:
        child_notes(sys.argv[sys.argv.index("--notes") + 1])
    elif "--driver" in sys.argv:
        print("AP39_NOTES_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
