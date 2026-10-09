"""OG-bh-1 Phase B helper (0.9.0_WK_NFRA_OPLGTW~46). Read-only against AWS except what `wrap` hands to SSM.

  python bh1_tool.py wrap <lookback_days> <deadline_utc_iso> <tag> <out_json>
      SSM parameters file: copy the S3 code object UNEDITED to C:/schwab-sdd/og-bh1/, register an Administrator
      task running it with -Mode download -Target monolith -LookbackDays N, prove it started, wait until it ends or the
      deadline (then stop the task), print the puller log lines of this run (progress lines thinned), unregister, delete the copy.
  python bh1_tool.py grade <from_date> <to_date> <census_json> <repo_root> [out_json]
      read schwab/08403355/meta/complete/date=<D>.json for every served date in the range and classify it with the
      gateway's own record-level rule (as bh1.AC2.py does).
  python bh1_tool.py metrics <start_iso> <end_iso>
      silver converter Invocations / Errors / Throttles / Duration / ConcurrentExecutions for the interval; DLQ depth.
  python bh1_tool.py dlq
      DLQ visible + in-flight message counts.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import boto3

BUCKET, NEW = "opal-data-assets", "08403355"
FUNC = "opal-assets-silver-schwab"
DLQ = "https://sqs.us-east-1.amazonaws.com/313476888478/opal-assets-silver-dlq"
SERVED = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def wrap(lookback, deadline, tag, out):
    cmds = [
        "$ErrorActionPreference='Continue'",
        "$ProgressPreference='SilentlyContinue'",
        "$aws='C:/Program Files/Amazon/AWSCLIV2/aws.exe'",
        "$s3='s3://opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1'",
        "$dir='C:/schwab-sdd/og-bh1'",
        "$local=$dir + '/sdd-backfill-bh1.ps1'",
        "New-Item -ItemType Directory -Force $dir | Out-Null",
        "& $aws s3 cp $s3 $local --only-show-errors",
        "if ($LASTEXITCODE -ne 0) { throw 'FATAL: could not pull sdd-daily-pull.ps1 from S3' }",
        "Write-Output ('BOX_COPY_MD5=' + (Get-FileHash $local -Algorithm MD5).Hash + ' lines=' + (Get-Content $local).Count)",
        "$tn='OpalOgBh1Backfill" + tag + "'",
        "$logf='C:/schwab-sdd/daily/08403355/daily-pull.log'",
        "$n0=0; if (Test-Path $logf) { $n0=(Get-Content $logf).Count }",
        "$tr='powershell.exe -ExecutionPolicy Bypass -File ' + $local + ' -Master 08403355 -Mode download -Target monolith -LookbackDays "
        + str(lookback) + "'",
        "$deadline=[datetime]::Parse('" + deadline + "').ToUniversalTime()",
        "Write-Output ('START_UTC=' + (Get-Date).ToUniversalTime().ToString('o') + ' DEADLINE_UTC=' + $deadline.ToString('o'))",
        "if ((Get-Date).ToUniversalTime() -ge $deadline) { Remove-Item $dir -Recurse -Force -ErrorAction SilentlyContinue; throw 'FATAL: past the deadline before start' }",
        "Unregister-ScheduledTask -TaskName $tn -Confirm:$false -ErrorAction SilentlyContinue",
        "schtasks /Create /TN $tn /TR $tr /SC ONCE /ST 23:59 /RU Administrator /IT /RL HIGHEST /F | Out-Null",
        "if ($LASTEXITCODE -ne 0) { throw 'FATAL: could not register the Administrator scheduled task' }",
        "$before = (Get-ScheduledTaskInfo -TaskName $tn).LastRunTime",
        "schtasks /Run /TN $tn | Out-Null",
        "$startDeadline = (Get-Date).AddSeconds(90)",
        "do { Start-Sleep -Seconds 5; $st = (Get-ScheduledTask -TaskName $tn).State; $now = (Get-ScheduledTaskInfo -TaskName $tn).LastRunTime } while ($st -ne 'Running' -and $now -eq $before -and (Get-Date) -lt $startDeadline)",
        "if ($st -ne 'Running' -and $now -eq $before) { Unregister-ScheduledTask -TaskName $tn -Confirm:$false -ErrorAction SilentlyContinue; Remove-Item $dir -Recurse -Force -ErrorAction SilentlyContinue; throw ('FATAL: scheduled task ' + $tn + ' NEVER STARTED (Administrator console logged off?)') }",
        "do { Start-Sleep -Seconds 10; $st = (Get-ScheduledTask -TaskName $tn).State } while ($st -eq 'Running' -and (Get-Date).ToUniversalTime() -lt $deadline)",
        "$stopped = $false",
        "if ($st -eq 'Running') { Stop-ScheduledTask -TaskName $tn; Start-Sleep -Seconds 5; Get-CimInstance Win32_Process -Filter \"Name='powershell.exe'\" | Where-Object { $_.CommandLine -like '*sdd-backfill-bh1*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; $stopped = $true }",
        "$rc = (Get-ScheduledTaskInfo -TaskName $tn).LastTaskResult",
        "Write-Output ('END_UTC=' + (Get-Date).ToUniversalTime().ToString('o') + ' LastTaskResult=' + $rc + ' stopped_at_deadline=' + $stopped + ' task_last_run=' + $now)",
        "$lines = @(Get-Content $logf -ErrorAction SilentlyContinue | Select-Object -Skip $n0)",
        "$keep = @($lines | Where-Object { $_ -notmatch 'progress:' -and $_ -notmatch '^.{22}   FAIL' })",
        "$prog = @($lines | Where-Object { $_ -match 'progress:' })",
        "$fails = @($lines | Where-Object { $_ -match '^.{22}   FAIL' })",
        "$keep | ForEach-Object { $_ }",
        "Write-Output ('PROGRESS_LINES=' + $prog.Count)",
        "$prog | Select-Object -First 1 | ForEach-Object { $_ }",
        "$prog | Select-Object -Last 2 | ForEach-Object { $_ }",
        "Write-Output ('FAIL_LINES=' + $fails.Count)",
        "$fails | Select-Object -First 25 | ForEach-Object { $_ }",
        "Unregister-ScheduledTask -TaskName $tn -Confirm:$false -ErrorAction SilentlyContinue",
        "Remove-Item $dir -Recurse -Force -ErrorAction SilentlyContinue",
        "Write-Output ('TASK_UNREGISTERED=' + ($null -eq (Get-ScheduledTask -TaskName $tn -ErrorAction SilentlyContinue)))",
        "Write-Output ('COPY_DELETED=' + (-not (Test-Path $dir)))",
        "exit 0",
    ]
    json.dump({"commands": cmds, "executionTimeout": ["14400"]}, open(out, "w"), indent=1)


def load_contract(root):
    sys.path.insert(0, str(Path(root) / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    raw = json.loads((Path(root) / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8"))
    raw["masters"] = dict(raw["masters"], **{NEW: raw["masters"].get(NEW, "TaxSMA")})
    for ds in SERVED:
        p = "schwab/%s/silver/%s/" % (NEW, ds)
        if p not in raw["data_prefixes"]:
            raw["data_prefixes"].append(p)
    if "schwab/%s/meta/complete/" % NEW not in raw["completion_prefixes"]:
        raw["completion_prefixes"].append("schwab/%s/meta/complete/" % NEW)
    return cat, cat.parse_contract(raw)


def grade(d_from, d_to, census_path, root, out=None):
    cat, contract = load_contract(root)
    census = json.load(open(census_path, encoding="utf-8"))
    dates = [d for d in sorted(census["served_dates"]) if d_from <= d <= d_to]
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    s3 = boto3.client("s3", region_name="us-east-1")
    res = {}
    for d in dates:
        key = "schwab/%s/meta/complete/date=%s.json" % (NEW, d)
        try:
            o = s3.get_object(Bucket=BUCKET, Key=key)
            marker = json.loads(o["Body"].read())
            vid = o.get("VersionId")
        except s3.exceptions.NoSuchKey:
            res[d] = {"class": "ABSENT"}
            continue
        closure = marker.get("closure") if isinstance(marker, dict) else None
        if not isinstance(closure, dict):
            res[d] = {"class": "LEGACY", "version_id": vid}
            continue
        f = cat.membership_findings(marker, closure, NEW, d, contract)
        v = cat.validate_closure(closure, contract.masters)
        ok = (not any(x["class"] in rejected for x in f)) and v["status"] == cat.RESULT_QUALIFIED
        row = {"class": "QUALIFIED" if ok else "NONQUALIFYING", "version_id": vid,
               "closure_status": closure.get("status"), "disposition": closure.get("day_disposition"),
               "write_guard": marker.get("write_guard") or closure.get("write_guard"),
               "tables": (closure.get("counts") or {}).get("tables_seen"),
               "source_partitions": (closure.get("counts") or {}).get("source_partitions")}
        if not ok:
            row["membership_findings"] = [x.get("class") for x in f][:6]
            row["validate_status"] = v.get("status")
            row["closure_findings"] = [str(x)[:160] for x in (closure.get("findings") or [])][:4]
        res[d] = row
    counts = {}
    for r in res.values():
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    print("grade %s..%s dates %d: %s" % (d_from, d_to, len(dates), json.dumps(counts, sort_keys=True)))
    bad = {d: r for d, r in res.items() if r["class"] != "QUALIFIED"}
    for d in sorted(bad)[:12]:
        print("  NOT QUALIFIED %s %s" % (d, json.dumps(bad[d])[:300]))
    if out:
        json.dump(res, open(out, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return res


def dlq():
    sqs = boto3.client("sqs", region_name="us-east-1")
    a = sqs.get_queue_attributes(QueueUrl=DLQ, AttributeNames=["ApproximateNumberOfMessages",
                                                              "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
    print("DLQ visible=%s in_flight=%s" % (a["ApproximateNumberOfMessages"], a["ApproximateNumberOfMessagesNotVisible"]))
    return int(a["ApproximateNumberOfMessages"]) + int(a["ApproximateNumberOfMessagesNotVisible"])


def metrics(start, end):
    cw = boto3.client("cloudwatch", region_name="us-east-1")
    s = dt.datetime.fromisoformat(start.replace("Z", "+00:00"))
    e = dt.datetime.fromisoformat(end.replace("Z", "+00:00"))
    out = {}
    for name, stat in (("Invocations", "Sum"), ("Errors", "Sum"), ("Throttles", "Sum"), ("Duration", "Average"),
                       ("Duration", "Maximum"), ("ConcurrentExecutions", "Maximum")):
        r = cw.get_metric_statistics(Namespace="AWS/Lambda", MetricName=name,
                                     Dimensions=[{"Name": "FunctionName", "Value": FUNC}],
                                     StartTime=s, EndTime=e, Period=60, Statistics=[stat])
        pts = r["Datapoints"]
        vals = [p[stat] for p in pts]
        if stat == "Sum":
            out[name] = sum(vals)
        elif stat == "Average":
            tot = sum(p["Average"] for p in pts)
            out[name + "_avg_of_minutes"] = round(tot / len(pts), 1) if pts else None
        else:
            out[name + "_max"] = max(vals) if vals else None
    last = cw.get_metric_statistics(Namespace="AWS/Lambda", MetricName="Invocations",
                                    Dimensions=[{"Name": "FunctionName", "Value": FUNC}],
                                    StartTime=e - dt.timedelta(minutes=6), EndTime=e, Period=60, Statistics=["Sum"])
    out["invocations_last_6_min"] = sum(p["Sum"] for p in last["Datapoints"])
    print("metrics %s..%s %s" % (start, end, json.dumps(out, sort_keys=True)))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "wrap" and len(a) == 5:
        wrap(a[1], a[2], a[3], a[4])
    elif a and a[0] == "grade" and len(a) in (5, 6):
        grade(a[1], a[2], a[3], a[4], a[5] if len(a) == 6 else None)
    elif a and a[0] == "metrics" and len(a) == 3:
        metrics(a[1], a[2])
    elif a and a[0] == "dlq":
        dlq()
    else:
        print(__doc__)
        sys.exit(2)
