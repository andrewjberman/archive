"""OPLGTW OG-tm-1 AC1 (PRD v2.0 item 5(b), FWD-13): master 08403355 is in the daily pull, read LIVE from AWS.

  (a) the scheduled puller's code object s3://opal-data-assets/code/canonical-schwab-si2/sdd-daily-pull.ps1 carries
      '08403355' in the -Master ValidateSet, beside the two existing masters;
  (b) the new master's EventBridge rule exists and is ENABLED (its name is lib/opal_naming.py builder output, row
      NFRA_OPLGTW-Z-S68, default schwab-canonical-si2-08403355-pull-daily, override TM1_NEW_RULE), with a cron whose every
      fire time is at least 30 minutes from every fire time of the two existing masters' rules (read live; the siblings keep
      their names canonical-schwab-si2-<master>-daily-pull);
  (c) its one target is AWS-RunPowerShellScript on the SI2 box, and its input runs the puller with
      `-Master 08403355 -Target monolith`.
"""
import os
import re
import sys

import boto3

BOX = "i-0f3d57a97f14727af"
NEW, OLD = "08403355", ("08242234", "08335338")
NEW_RULE = os.environ.get("TM1_NEW_RULE", "schwab-canonical-si2-08403355-pull-daily")


def rule_name(m):
    return NEW_RULE if m == NEW else "canonical-schwab-si2-%s-daily-pull" % m


def fires(cron):
    m = re.match(r"cron\((\S+) (\S+) \S+ \S+ \S+ \S+\)$", cron or "")
    if not m or not re.match(r"^\d+$", m.group(1)) or not re.match(r"^[\d,]+$", m.group(2)):
        return None
    return [int(h) * 60 + int(m.group(1)) for h in m.group(2).split(",")]


def gap(a, b):
    d = abs(a - b) % 1440
    return min(d, 1440 - d)


def main():
    ok = True
    s3 = boto3.client("s3", region_name="us-east-1")
    body = s3.get_object(Bucket="opal-data-assets", Key="code/canonical-schwab-si2/sdd-daily-pull.ps1")["Body"].read()
    text = body.decode("utf-8", "replace")
    vs = re.search(r"\[ValidateSet\(([^)]*)\)\]\[string\]\$Master", text)
    members = re.findall(r"'(\d{8})'", vs.group(1)) if vs else []
    print("(a) code object -Master ValidateSet: %s" % members)
    if not vs or NEW not in members or not all(o in members for o in OLD):
        ok = False
        print("FAIL: (a)")
    ev = boto3.client("events", region_name="us-east-1")
    crons = {}
    for m in (NEW,) + OLD:
        name = rule_name(m)
        try:
            r = ev.describe_rule(Name=name)
        except ev.exceptions.ResourceNotFoundException:
            print("FAIL: (b) rule %s absent" % name)
            ok = False
            continue
        crons[m] = (r.get("ScheduleExpression"), r.get("State"))
        print("(b) %s: %s %s" % (name, r.get("ScheduleExpression"), r.get("State")))
    if NEW in crons:
        new_f = fires(crons[NEW][0])
        if crons[NEW][1] != "ENABLED" or not new_f:
            print("FAIL: (b) the new rule is not ENABLED with a parseable cron")
            ok = False
        else:
            for o in OLD:
                of = fires((crons.get(o) or (None,))[0]) or []
                close = [(a, b) for a in new_f for b in of if gap(a, b) < 30]
                if close or not of:
                    print("FAIL: (b) fires within 30 minutes of %s (or that rule unreadable): %s" % (o, close))
                    ok = False
        tg = ev.list_targets_by_rule(Rule=rule_name(NEW)).get("Targets") or []
        inp = tg[0].get("Input", "") if len(tg) == 1 else ""
        ids = (tg[0].get("RunCommandParameters") or {}).get("RunCommandTargets") if len(tg) == 1 else None
        box_ok = bool(ids) and any(t.get("Key") == "InstanceIds" and t.get("Values") == [BOX] for t in ids)
        doc_ok = len(tg) == 1 and tg[0].get("Arn", "").endswith(":document/AWS-RunPowerShellScript")
        run_ok = ("-Master %s -Target monolith" % NEW) in inp
        print("(c) targets %d; RunPowerShellScript %s; box %s; runs -Master %s -Target monolith %s"
              % (len(tg), doc_ok, box_ok, NEW, run_ok))
        if not (doc_ok and box_ok and run_ok):
            ok = False
            print("FAIL: (c)")
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
