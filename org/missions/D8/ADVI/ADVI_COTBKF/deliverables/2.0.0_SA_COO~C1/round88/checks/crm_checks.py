#!/usr/bin/env python3
"""ADVI_COTBKF round 88 record checks (2.0.0_SA_COO~C1): the grant, the job and the withdrawal records of the one-job CRM match.

  python crm_checks.py grant      --file GRANT_RECORD.json
  python crm_checks.py job        --file JOB_RECORD.json [--links PATH]
  python crm_checks.py withdrawal --file WITHDRAWAL_RECORD.json

Each prints ONE line that starts `CRM-GRANT:`, `CRM-JOB:` or `CRM-WITHDRAWAL:` and then `OK` or `BAD`, with counts only. No CRM column value, no name and no account number is ever printed:
the job check reads the links file's HEADER LINE only (and, for the row count, counts lines). ASCII only.
"""
import argparse
import json
import sys

KEY = "commonwealth/cottonwood/bronze/crm/date=2026-06-23/CRM_CottonwoodCapitalAdvisors.zip"
BUCKET = "opal-data-cottonwood"
ALLOW_COLUMNS = ["commonwealth_account", "bd_account_id", "rule", "tier"]
TIERS = {"DETERMINISTIC", "CANDIDATE"}


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def grant(d):
    bad = []
    if d.get("policy_actions") != ["s3:GetObject"]:
        bad.append("policy_actions")
    if d.get("policy_resources") != ["arn:aws:s3:::%s/%s" % (BUCKET, KEY)]:
        bad.append("policy_resources")
    plan = d.get("plan_summary") or {}
    if plan.get("other_changes") != 0:
        bad.append("plan_other_changes")
    if not str(d.get("role_arn", "")).startswith("arn:aws:iam::"):
        bad.append("role_arn")
    if str(d.get("bucket_policy_reader_added")) != str(d.get("role_arn")):
        bad.append("reader_is_not_the_role")
    if d.get("list_deny_unchanged") is not True or d.get("write_deny_unchanged") is not True:
        bad.append("list_or_write_deny_moved")
    if not d.get("ledger_entry") or not d.get("cvo_resigned_ref") or not d.get("deadline_utc"):
        bad.append("ledger_or_cvo_or_deadline")
    return "CRM-GRANT: %s role=%s plan_other_changes=%s bad=%s" % (
        "OK" if not bad else "BAD", "set" if d.get("role_arn") else "absent", plan.get("other_changes"), ",".join(bad) or "-")


def job(d, links=None):
    bad = []
    if d.get("key") != "s3://%s/%s" % (BUCKET, KEY):
        bad.append("key")
    if d.get("landed") not in (True, False):
        bad.append("landed")
    if d.get("scratch_disk_write") is not False:
        bad.append("disk_write")
    for k in ("role_arn", "session_name", "started", "ended"):
        if not d.get(k):
            bad.append(k)
    if d.get("landed") is True:
        if d.get("output_columns") != ALLOW_COLUMNS:
            bad.append("output_columns")
        c = d.get("counts") or {}
        total = sum(int(c.get(k, -10 ** 9)) for k in ("deterministic", "candidate"))
        if total != d.get("rows_total"):
            bad.append("rows_total")
        o = d.get("over_219") or {}
        if o.get("reachable") != 219 or o.get("matched", -1) + o.get("unmatched", -1) != 219:
            bad.append("over_219")
        if links:
            with open(links, encoding="utf-8") as f:
                header = f.readline().strip().split(",")
                n = sum(1 for _ in f)
            if header != ALLOW_COLUMNS:
                bad.append("links_header")
            if n != d.get("rows_total"):
                bad.append("links_rows")
    else:
        if d.get("rows_total") not in (0, None):
            bad.append("rows_without_landing")
    return "CRM-JOB: %s landed=%s rows=%s bad=%s" % ("OK" if not bad else "BAD", d.get("landed"), d.get("rows_total"), ",".join(bad) or "-")


def withdrawal(d):
    bad = []
    if d.get("role_deleted") is not True or d.get("reader_removed") is not True:
        bad.append("not_withdrawn")
    rp = d.get("replan") or {}
    if (rp.get("add"), rp.get("change"), rp.get("destroy")) != (0, 0, 0):
        bad.append("replan_not_clean")
    ev = d.get("assume_role_events")
    if not isinstance(ev, list) or d.get("assume_role_events_stated") is not True:
        bad.append("assume_role_events")
    if d.get("data_events_stated") is not True:
        bad.append("data_events_not_stated")
    if d.get("ledger_closed") is not True:
        bad.append("ledger")
    return "CRM-WITHDRAWAL: %s events=%s bad=%s" % ("OK" if not bad else "BAD", len(ev) if isinstance(ev, list) else "n/a", ",".join(bad) or "-")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["grant", "job", "withdrawal"])
    ap.add_argument("--file", required=True)
    ap.add_argument("--links")
    a = ap.parse_args(argv)
    try:
        d = _load(a.file)
    except Exception as e:  # a missing or unreadable record is BAD, never a pass
        print("CRM-%s: BAD record unreadable (%s)" % (a.which.upper(), type(e).__name__))
        return 1
    line = grant(d) if a.which == "grant" else job(d, a.links) if a.which == "job" else withdrawal(d)
    print(line)
    return 0 if ": OK" in line else 1


if __name__ == "__main__":
    sys.exit(main())
