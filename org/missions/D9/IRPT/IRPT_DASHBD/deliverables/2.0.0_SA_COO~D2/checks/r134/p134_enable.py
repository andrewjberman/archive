"""IRPT_DASHBD round 134, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-266, ENABLE the Cottonwood landing schedule `irpt-cot-account-return-daily-daily` (CTO ROUND-128 ANALYSIS
ADDENDUM 1 @143709c44f, msg 8486): ONE line of `infra/aws/terraform/investor-reporting/account-return-daily/schedule.tf` (state DISABLED to ENABLED), applied by `.tools/safe-apply.sh` under its
own ledger with a plan of exactly 1 change, no invoke, the ledger left OPEN for the issuer's read of the first scheduled fire.

  DB-b-266 (0.7.0_AE_CloudOps~DB2)  DBE134-1-AC1 (the record and the git diff: the one line, the gates, the plan 0/1/0),
                                    DBE134-2-AC1 (FRESH live reads: the schedule ENABLED and everything else unchanged, nothing written by the apply, the ledger open)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_SCHEDULE_ENABLE_RECORD.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-266.enable-cottonwood-landing-schedule-one-line.md"
CTO_REL = "org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_B-49F_ROUND_128_20261015.md"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md"
PACKET_SHA12 = "31f8e1620b90"
ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
SCHEDULE_TF = ROOT_DIR + "schedule.tf"
SLUG = "irpt-dashbd-cottonwood-schedule-enable-20261015"
FUNCTION = "irpt-cot-account-return-daily-lambda"
SCHEDULE = "irpt-cot-account-return-daily-daily"
ADDRESS = "aws_scheduler_schedule.irpt_account_return_daily"
CRON, ZONE = "cron(15 8 ? * MON-FRI *)", "America/New_York"
GOLD_BUCKET, GOLD_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/"
LAST_CATCHUP_DAY, FIRST_DAY = "2026-10-14", "2026-07-10"
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("code_sha256", "ledger_entry", "apply_finished_utc", "commit", "packet_sha12", "addresses")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.split()[-1]


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_one_line(base_text, new_text):
    b, n = base_text.splitlines(), new_text.splitlines()
    need(len(b) == len(n), "schedule.tf changed its line count (%d to %d): only the state line may change" % (len(b), len(n)))
    diffs = [(i, x, y) for i, (x, y) in enumerate(zip(b, n)) if x != y]
    need(len(diffs) == 1, "exactly one line of schedule.tf may change, %d did" % len(diffs))
    _i, x, y = diffs[0]
    need(re.fullmatch(r'\s*state\s*=\s*"DISABLED"\s*', x) and re.fullmatch(r'\s*state\s*=\s*"ENABLED"\s*', y), "the one line must be state DISABLED to ENABLED, read %r to %r" % (x.strip(), y.strip()))
    return True


def check_record(rec, cto_text, packet_ok, ledger_open_ok):
    exp = {"claim", "gates", "ledger_entry", "before", "edit", "plan", "apply_finished_utc", "after", "invoke", "ledger_closed", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"cto_ruling_read", "packet_sha12", "landing_ledger_closed", "one_change_at_a_time"}, "gates keys")
    need(g["cto_ruling_read"] is True and "RULED: enable" in cto_text and "irpt-cot-account-return-daily-daily" in cto_text, "the CTO's addendum must read RULED: enable the schedule")
    need(g["packet_sha12"] == PACKET_SHA12 and packet_ok, "the packet's sha256 must be the signed revision 3 (%s)" % PACKET_SHA12)
    need(g["landing_ledger_closed"] is True, "the landing ledger must be recorded closed")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 1,
         "one_change_at_a_time: the denominator, and exactly the one marker (this order's own ledger)")
    need(rec["ledger_entry"] == SLUG and ledger_open_ok, "the ledger entry %s must exist" % SLUG)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"schedule", "function"}, "before keys")
    need(b["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "before.schedule must read DISABLED at %s %s" % (CRON, ZONE))
    need(isinstance(b["function"], dict) and b["function"].get("memory") == 1024 and b["function"].get("timeout") == 900, "before.function")
    e = rec["edit"]
    need(isinstance(e, dict) and set(e) == {"file", "lines_changed", "commit"} and e["file"] == SCHEDULE_TF and e["lines_changed"] == 1 and isinstance(e["commit"], str) and len(e["commit"]) >= 10, "edit: the one line of schedule.tf and its commit")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "replan_no_changes"}, "plan keys")
    need(p["add"] == 0 and p["change"] == 1 and p["destroy"] == 0 and [re.sub(r"^module\.[^.]+\.", "", str(a)) for a in p["addresses"]] == [ADDRESS] and p["replan_no_changes"] is True,
         "the plan must read 0 add / 1 change / 0 destroy on %s, and a post-apply plan with no changes" % ADDRESS)
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"schedule", "function"}, "after keys")
    need(a["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "after.schedule must read ENABLED at %s %s" % (CRON, ZONE))
    need(a["function"] == b["function"], "the function must be unchanged by the apply")
    need(rec["invoke"] == {"count": 0}, "no invoke is permitted by this order")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN for the issuer's read of the first scheduled fire")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def live():
    import boto3
    lam, sch, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1"), boto3.client("s3")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    sc = sch.get_schedule(Name=SCHEDULE)
    objs, tok = [], None
    while True:
        kw = {"Bucket": GOLD_BUCKET, "Prefix": GOLD_PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        objs += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    return {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "arn": cfg["FunctionArn"], "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "target": sc["Target"]["Arn"], "window": sc.get("FlexibleTimeWindow", {}).get("Mode"), "objects": objs}


def run(root, cid):
    root = Path(root)
    rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
    cto = (root / CTO_REL).read_text(encoding="utf-8")
    import hashlib
    packet_ok = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest().startswith(PACKET_SHA12)
    ledger_ok = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % SLUG))) or (root / "org/critical_paths/.open_deploys" / (SLUG + ".json")).is_file()
    check_record(rec, cto, packet_ok, ledger_ok)
    base = base_commit(root)
    bt, rc = git(root, "show", "%s:%s" % (base, SCHEDULE_TF))
    need(rc == 0, "cannot read the base schedule.tf")
    check_one_line(bt, (root / SCHEDULE_TF).read_text(encoding="utf-8"))
    others, _ = git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", ROOT_DIR)
    for f in others.split():
        if f != SCHEDULE_TF:
            need(git(root, "show", "HEAD:" + f)[0] == git(root, "show", "%s:%s" % (base, f))[0], "another root file changed: %s" % f)
    if cid == "DBE134-1-AC1":
        print("OK: gates (the CTO's addendum reads RULED: enable, packet revision 3, the landing ledger closed, one change at a time), ledger %s, the one line of schedule.tf, plan 0/1/0 on %s" % (SLUG, ADDRESS))
        return True
    lv = live()
    if cid == "DBE134-2-AC1":
        need(lv["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "live schedule: %s" % lv["schedule"])
        need(lv["target"] == lv["arn"] and lv["window"] == "OFF", "the schedule's target is not the function or its flexible window is not OFF")
        need(lv["memory"] == 1024 and lv["timeout"] == 900, "the function changed: %s %s" % (lv["memory"], lv["timeout"]))
        fin = rec["apply_finished_utc"]
        by_day = {}
        for k, t in lv["objects"]:
            by_day.setdefault(k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15], []).append((k, t))
        old = [k for d, items in by_day.items() if d <= LAST_CATCHUP_DAY for k, t in items if t.strftime("%Y-%m-%dT%H:%M:%SZ") >= fin]
        need(not old, "keys of days up to %s were modified after the apply finished: %d (the apply writes nothing)" % (LAST_CATCHUP_DAY, len(old)))
        later = sorted(d for d in by_day if d > LAST_CATCHUP_DAY)
        for d in later:
            need(sorted(k.rsplit("/", 1)[1] for k, _ in by_day[d]) == ["data.parquet", "manifest.json"], "a partition after the catch-up (%s) does not hold exactly its two objects" % d)
        need((root / "org/critical_paths/.open_deploys" / (SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: live: schedule ENABLED at %s %s with the function as target, flexible window OFF, function unchanged; nothing up to %s was written after the apply; %d partition(s) after the catch-up, each exactly its two objects; ledger open" % (CRON, ZONE, LAST_CATCHUP_DAY, len(later)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = 'resource "x" "y" {\n  state                        = "DISABLED"\n  schedule_expression          = "cron(1)"\n}\n'
    assert check_one_line(base, base.replace('"DISABLED"', '"ENABLED"'))
    red(lambda: check_one_line(base, base), "no change")
    red(lambda: check_one_line(base, base.replace('"DISABLED"', '"ENABLED"').replace("cron(1)", "cron(2)")), "two lines")
    red(lambda: check_one_line(base, base.replace('"DISABLED"', '"ENABLED"') + "# x\n"), "line count")
    red(lambda: check_one_line(base, base.replace('"DISABLED"', '"PENDING"')), "wrong value")
    cto = "RULED: enable `irpt-cot-account-return-daily-daily`"
    good = {"claim": "measured", "gates": {"cto_ruling_read": True, "packet_sha12": PACKET_SHA12, "landing_ledger_closed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 1}},
            "ledger_entry": SLUG, "before": {"schedule": {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "function": {"memory": 1024, "timeout": 900}},
            "edit": {"file": SCHEDULE_TF, "lines_changed": 1, "commit": "abcdef1234"}, "plan": {"add": 0, "change": 1, "destroy": 0, "addresses": [ADDRESS], "replan_no_changes": True},
            "apply_finished_utc": "2026-10-15T18:00:00Z", "after": {"schedule": {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "function": {"memory": 1024, "timeout": 900}},
            "invoke": {"count": 0}, "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    assert check_record(copy.deepcopy(good), cto, True, True)
    arms = (("cto", lambda r: r["gates"].update(cto_ruling_read=False)), ("packet", lambda r: r["gates"].update(packet_sha12="000000000000")), ("landing ledger", lambda r: r["gates"].update(landing_ledger_closed=False)),
            ("markers", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=0)), ("before", lambda r: r["before"]["schedule"].update(state="ENABLED")),
            ("lines", lambda r: r["edit"].update(lines_changed=2)), ("file", lambda r: r["edit"].update(file="x")), ("plan change", lambda r: r["plan"].update(change=2)), ("plan add", lambda r: r["plan"].update(add=1)),
            ("address", lambda r: r["plan"].update(addresses=["aws_lambda_function.this"])), ("replan", lambda r: r["plan"].update(replan_no_changes=False)), ("after", lambda r: r["after"]["schedule"].update(state="DISABLED")),
            ("function", lambda r: r["after"]["function"].update(memory=2048)), ("invoke", lambda r: r["invoke"].update(count=1)), ("ledger closed", lambda r: r.update(ledger_closed=True)),
            ("utc", lambda r: r.update(apply_finished_utc="soon")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r["after"]["schedule"].update(note="id 1234567890")))
    for label, fn in arms:
        r = copy.deepcopy(good)
        fn(r)
        red(lambda: check_record(r, cto, True, True), label)
    red(lambda: check_record(copy.deepcopy(good), "not ruled", True, True), "cto text")
    red(lambda: check_record(copy.deepcopy(good), cto, False, True), "packet bytes")
    red(lambda: check_record(copy.deepcopy(good), cto, True, False), "no ledger")
    print("selftest: one-line (4 red arms) and record (%d red arms) clauses behave" % (len(arms) + 3))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
