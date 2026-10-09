"""OG-bh-1 Phase B driver (0.9.0_WK_NFRA_OPLGTW~46): runs the signed batches one at a time, newest first.

  python bh1_drive.py <first_batch> <last_batch> <repo_root>      e.g.  1 9 .   (batch 10 = the closing 2000-day run)

For each batch: window check (start outside, finish before [09:15,11:35) [12:00,12:50) [21:15,23:35) UTC), DLQ baseline, SSM
puller run (bh1_tool.wrap), wait for the converter to drain, read back every date of the batch with the gateway's rule, name
the converter's Throttles/Errors, apply the signed stop rule, and fold the result into bh1_backfill_record.json.
Exit 0 all batches done, 3 = not startable now (window), 4 = STOP (stop rule), 5 = unexpected.
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import boto3

import bh1_tool as tool

HERE = Path(__file__).resolve().parent
RECORD = HERE / "bh1_backfill_record.json"
CENSUS = HERE / "bh1_census_record.json"
BOX = "i-0f3d57a97f14727af"
SEC_PER_FILE = 2.6
WINDOWS = ((dt.time(9, 15), dt.time(11, 35)), (dt.time(12, 0), dt.time(12, 50)), (dt.time(21, 15), dt.time(23, 35)))
BATCHES = {1: "2026-06-09", 2: "2026-03-12", 3: "2025-12-11", 4: "2025-09-11", 5: "2025-06-04", 6: "2025-02-27",
           7: "2024-11-19", 8: "2024-02-23", 9: "2023-10-03", 10: "2023-10-03"}
ERA_A_END = "2024-09-26"


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def in_window(t):
    return any(a <= t.time() < b for a, b in WINDOWS)


def next_window_start(t):
    """The next window start after t (today or tomorrow)."""
    cands = []
    for day in (t.date(), t.date() + dt.timedelta(days=1)):
        for a, _ in WINDOWS:
            c = dt.datetime.combine(day, a, tzinfo=dt.timezone.utc)
            if c > t:
                cands.append(c)
    return min(cands)


def load_record():
    if RECORD.exists():
        return json.loads(RECORD.read_text(encoding="utf-8"))
    return {"order": "NFRA_OPLGTW.TO-OG-bh-1", "worker": "0.9.0_WK_NFRA_OPLGTW~46", "master": "08403355",
            "started_utc": iso(now()), "batches": [], "backfilled": [], "unavailable": {},
            "qualified_by_scheduled_pull": [], "stops": [], "held": {}}


def save_record(rec):
    RECORD.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def census_counts():
    out = json.loads((HERE / "ssm_invocation_census_2000.json").read_text(encoding="utf-8"))["StandardOutputContent"]
    return {d: int(n) for d, n in re.findall(r"^DATE (\d{4}-\d{2}-\d{2}) (\d+)\s*$", out.replace("\r", ""), re.M)}


RPS_SUBJECTS = {"fact_rps", "fact_rps_s2", "dim_position", "dim_balance"}


def scan_errors(t0, t1):
    """Converter ERROR log lines in [t0, t1]: (rps SchemaDriftError dates, other error lines)."""
    logs = boto3.client("logs", region_name="us-east-1")
    drift, other = set(), []
    s, e = int(t0.timestamp() * 1000), int(t1.timestamp() * 1000)
    for pg in logs.get_paginator("filter_log_events").paginate(
            logGroupName="/aws/lambda/opal-assets-silver-schwab", startTime=s, endTime=e, filterPattern="ERROR"):
        for ev in pg["events"]:
            m = ev["message"].strip()
            if not m.startswith("[ERROR]"):
                continue
            mm = re.search(r"bronze/rps/(\d{8})/", m)
            if mm and "SchemaDriftError" in m and m.count("bronze/") == 1:
                d = mm.group(1)
                drift.add(d[:4] + "-" + d[4:6] + "-" + d[6:])
            else:
                other.append(m[:300])
    return drift, other


def run_ssm(ssm, params_path):
    params = json.loads(Path(params_path).read_text(encoding="utf-8"))
    r = ssm.send_command(InstanceIds=[BOX], DocumentName="AWS-RunPowerShellScript", Parameters=params,
                         Comment="OG-bh-1 Phase B batch")
    cid = r["Command"]["CommandId"]
    time.sleep(5)
    while True:
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=BOX)
        except ssm.exceptions.InvocationDoesNotExist:
            time.sleep(5)
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return cid, inv
        time.sleep(20)


def main(first, last, root):
    ssm = boto3.client("ssm", region_name="us-east-1")
    counts = census_counts()
    rec = load_record()
    save_record(rec)
    for k in range(first, last + 1):
        oldest = BATCHES[k]
        t0 = now()
        if k < 10:
            prev_oldest = BATCHES[k - 1] if k > 1 else None
            mine = [d for d in counts if d >= oldest and (prev_oldest or "2026-09-09") > d]
            files = sum(counts[d] for d in mine)
            grade_from, grade_to = oldest, (prev_oldest or "2026-10-08")
        else:
            files = 0
            grade_from, grade_to = "2023-10-03", "2026-10-08"
        est = int(files * SEC_PER_FILE) + 240
        nxt = next_window_start(t0)
        if in_window(t0) or t0 + dt.timedelta(seconds=est + 15 * 60) > nxt:
            print("WAIT: batch %d (files %d, est %ds) cannot start+finish at %s before %s" % (k, files, est, iso(t0), iso(nxt)))
            return 3
        deadline = nxt - dt.timedelta(minutes=8)
        lookback = (t0.date() - dt.date.fromisoformat(oldest)).days if k < 10 else 2000
        dlq0 = tool.dlq()
        params = Path(root).resolve() / ".scratch" / ("wrap_b%d.json" % k)
        tool.wrap(lookback, iso(deadline), "B%d" % k, str(params))
        print("BATCH %d start %s lookback %d files_expected %d deadline %s dlq0 %d" % (k, iso(t0), lookback, files, iso(deadline), dlq0))
        cid, inv = run_ssm(ssm, params)
        out = (inv.get("StandardOutputContent") or "").replace("\r", "")
        t1 = now()
        b = {"batch": k, "lookback_days": lookback, "oldest_date": oldest, "files_expected_new": files,
             "ssm_command_id": cid, "ssm_status": inv["Status"], "started_utc": iso(t0), "puller_ended_utc": iso(t1),
             "dlq_baseline": dlq0}
        m = re.search(r"LastTaskResult=(\d+) stopped_at_deadline=(\w+)", out)
        b["last_task_result"] = int(m.group(1)) if m else None
        b["stopped_at_deadline"] = (m.group(2) == "True") if m else None
        for tag, pat in (("denominator", r"DENOMINATOR: ([^\n]*)"), ("landing_guard", r"LANDING GUARD: ([^\n]*)"),
                         ("pull_ok", r"(DAILY PULL OK[^\n]*)"), ("fatal", r"(FATAL [^\n]*)"),
                         ("fail_lines", r"FAIL_LINES=(\d+)"), ("lines_unregistered", r"TASK_UNREGISTERED=(\w+)"),
                         ("copy_deleted", r"COPY_DELETED=(\w+)")):
            mm = re.search(pat, out)
            b[tag] = mm.group(1)[:300] if mm else None
        ts = re.findall(r"^\[(\d{4}-\d{2}-\d{2}T[\d:]+Z)\] (?:=== SDD DAILY PULL|=== DAILY PULL OK)", out, re.M)
        if len(ts) >= 2:
            a = dt.datetime.fromisoformat(ts[0].replace("Z", "+00:00"))
            z = dt.datetime.fromisoformat(ts[-1].replace("Z", "+00:00"))
            b["puller_minutes"] = round((z - a).total_seconds() / 60, 1)
        rec["batches"].append(b)
        save_record(rec)
        print("PULLER batch %d: ssm=%s rc=%s %s | %s | guard %s | minutes %s" % (
            k, inv["Status"], b["last_task_result"], b["denominator"], b["pull_ok"], b["landing_guard"], b.get("puller_minutes")))
        if inv["Status"] != "Success" or b["last_task_result"] not in (0,):
            rc = b["last_task_result"]
            rec["stops"].append({"batch": k, "reason": "puller did not finish cleanly", "rc": rc, "ssm_status": inv["Status"],
                                 "tail": out[-1500:]})
            save_record(rec)
            print("STOP: puller rc=%s ssm=%s (Die 7 = session contention, other = stop)" % (rc, inv["Status"]))
            print(out[-1800:])
            return 4
        # converter drain: every date has a record and the function has been idle 2 polls in a row
        idle = 0
        drained = None
        while True:
            tn = now()
            mt = tool.metrics(iso(t0), iso(tn))
            res = tool.grade(grade_from, grade_to, str(CENSUS), root)
            absent = [d for d, r in res.items() if r["class"] == "ABSENT" and d > ERA_A_END]
            idle = idle + 1 if (mt["invocations_last_6_min"] == 0 and not absent) else 0
            if idle >= 2:
                drained = tn
                break
            if tn > nxt - dt.timedelta(minutes=2):
                print("STOP: converter not drained by %s (absent %d)" % (iso(tn), len(absent)))
                rec["stops"].append({"batch": k, "reason": "converter not drained before the next window", "absent": len(absent)})
                save_record(rec)
                return 4
            time.sleep(75)
        b["drained_utc"] = iso(drained)
        b["drain_minutes_after_puller"] = round((drained - t1).total_seconds() / 60, 1)
        b["metrics"] = tool.metrics(iso(t0), iso(now()))
        b["dlq_after"] = tool.dlq()
        res = tool.grade(grade_from, grade_to, str(CENSUS), root)
        bad = {d: r for d, r in res.items() if r["class"] != "QUALIFIED"}
        if any(d > ERA_A_END for d in bad):
            time.sleep(180)  # one re-read: a record composed by the last sibling event can post a few seconds after the idle poll
            res = tool.grade(grade_from, grade_to, str(CENSUS), root)
            bad = {d: r for d, r in res.items() if r["class"] != "QUALIFIED"}
        drift, other_errors = scan_errors(t0, now())
        held_known = rec.setdefault("held", {})
        b["dates_graded"] = len(res)
        b["qualified"] = sum(1 for r in res.values() if r["class"] == "QUALIFIED")
        b["held_known_in_range"] = sorted(d for d in bad if d in held_known)
        new_held = []
        stop = []
        for d, r in sorted(bad.items()):
            if d in held_known or d <= ERA_A_END:
                continue
            subjects = set()
            for f in r.get("closure_findings", []):
                mm = re.search(r"'subject': '(\w+)'", f)
                subjects.add(mm.group(1) if mm else "?")
            if d in drift and subjects and subjects <= RPS_SUBJECTS and r.get("membership_findings") == []:
                new_held.append(d)
            else:
                stop.append("era B/C date %s not qualified and not only an RPS SchemaDriftError: %s" % (d, json.dumps(r)[:240]))
        if b["metrics"]["Errors"] > 3 * len(drift):
            stop.append("converter Errors %s exceed 3 attempts x %d RPS drift files" % (b["metrics"]["Errors"], len(drift)))
        if other_errors:
            stop.append("converter errors other than RPS SchemaDriftError: %d, first %s" % (len(other_errors), other_errors[0]))
        for d in new_held:
            held_known[d] = "held: vendor drift (RPS pin)"
        b["held_new"] = new_held
        b["not_qualified"] = {d: r for d, r in bad.items() if d not in held_known}
        sched = ("2026-09-09", "2026-10-08")
        for d, r in sorted(res.items()):
            if r["class"] == "QUALIFIED":
                if k == 1 and sched[0] <= d <= sched[1]:
                    if d not in rec["qualified_by_scheduled_pull"]:
                        rec["qualified_by_scheduled_pull"].append(d)
                elif d not in rec["backfilled"]:
                    rec["backfilled"].append(d)
            elif d <= ERA_A_END:
                rec["unavailable"][d] = json.dumps({kk: r[kk] for kk in r if kk != "version_id"}, sort_keys=True)[:600]
        rec["backfilled"].sort()
        if b["dlq_after"] > dlq0 + len(new_held):
            stop.append("DLQ depth %d above its baseline %d plus %d newly held RPS files" % (b["dlq_after"], dlq0, len(new_held)))
        if stop:
            rec["stops"].append({"batch": k, "reason": "; ".join(stop)})
            save_record(rec)
            print("STOP:", "; ".join(stop))
            return 4
        save_record(rec)
        print("BATCH %d OK: dates %d qualified %d (era A unavailable so far %d) puller %.1f min drain +%.1f min" % (
            k, b["dates_graded"], b["qualified"], len(rec["unavailable"]), b.get("puller_minutes") or -1, b["drain_minutes_after_puller"]))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]))
