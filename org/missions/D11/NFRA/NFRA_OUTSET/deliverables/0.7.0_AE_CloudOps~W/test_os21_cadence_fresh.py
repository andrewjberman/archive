"""O21-AC1 -- THE CADENCE, read on the first SCHEDULED fire that could carry it.

Prints OS21-CADENCE-FRESH only when every arm passes.

WHICH DAY THIS GRADES, AND WHY IT IS NOT THE ONE PRD v0.8 NAMED. v0.8 re-pointed this criterion
onto TO-OS-s-24's MANUAL SERVED DAY. The freshness artifact latest at that run (00:18:59Z) was
written by a build whose CodeBuild `initiator` is `Andrew_Berman` -- a HAND publish -- and the
face says in terms: "a pass read against a hand-published artifact is INVALID", and "This
criterion CANNOT pass before the first scheduled fire that lands AFTER OS-s-20's switch is live
on the served day." The 2026-09-10 13:00Z run IS that first eligible fire. So this battery grades
the SCHEDULED run, which is the harder reading and the only valid one. The re-point was written
at 22:2xZ on 09-09, when no such fire existed yet.

WHAT THIS BATTERY REFUSES TO DO:

  1. IT DOES NOT ATTRIBUTE A PUBLISH BY ITS TIMESTAMP. The face demands the vintages be
     "ATTRIBUTED to the schedule and not to a hand publish (the fire's own log or event, not a
     timestamp alone)". A timestamp inside a schedule's window is exactly what a hand publish at
     the same minute would produce. Arm (c) reads CodeBuild's own `initiator` field, and its
     control is that the three preceding builds of the SAME project carry a human's name.

  2. IT DOES NOT RE-DERIVE THE DRIFT HALF. 2.0.0_SA_COO 94867: "drift half by OS-s-25". That
     order is TERMINAL at 520503aa98 with its own battery and its own proof instance. Re-grading
     it here would be a second seat's restatement lending credibility the claim has not earned;
     arm (f) CITES it and reads the one thing this day adds -- that the device's artifact is
     still inside its ceiling on this run.

  3. IT DOES NOT DECIDE THE STALE PREFIX CLAUSE ON ITS OWN JUDGEMENT. See PREFIX_MODE below.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-21). 2026-09-10.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
CODE_KEY = "code/estate_report_runner.py"
SEAM_PREFIX = "outset/"
FRESHNESS_KEY = "outset/comp_heat_freshness_tools.json"

SCHEDULE_NAME = "estate-report-seam-freshness-0830et"
CODEBUILD_PROJECT = "estate-report-seam-freshness-publisher"
SCHEDULER_ROLE_TOKEN = "estate-report-seam-freshness-scheduler"

# The served day this grades: the first SCHEDULED 13:00Z fire after OS-s-20's switch.
REPORT_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
CEILING_H = 26.0

# THE CLAUSE AS RE-CUT BY THE ISSUER, 2026-09-10T13:59Z (2.0.0_SA_COO, msg 95207).
#
# O21-AC1 originally read "the seam prefix listed and holding ONLY the two seam keys plus the
# untouched R2 probe (a fourth key is a FAIL)". That line predates the per-device layout the SAME
# criterion's 15:2xZ re-cut mandates ("ONE KEY PER DEVICE"), so read literally it fails on changes
# the face itself ordered. The issuer RE-CUT it to: THE PREFIX HOLDS NO KEY THAT MAPS TO NO
# AUTHORIZING CELL -- and recorded that as its own defect rather than a weakening, because the
# artifact is correct and the criterion was not.
#
# ⛔ IT IS NOT WEAKER THAN THE ORIGINAL, which is the test that matters: a stray publish, a
# wrong-prefix write and a fourth device nobody declared all still FAIL. That is everything
# "a fourth key is a FAIL" existed to catch. What changed is that the clause now names the
# PROPERTY (nothing publishes here unaccounted for) instead of a PROXY for it (a key count) --
# a proxy that breaks the moment the authorized population grows, while the property does not.
#
# The literal reading was OFFERED by this seat and DECLINED by the issuer in terms: it would spend
# a real FAIL on a criterion already known to be stale, and a FAIL everyone agrees is spurious
# teaches a reader to discount the next one. It is kept here only so the mode is auditable.
PREFIX_MODE = os.environ.get("OS21_PREFIX_MODE", "attributed")

# Every key the prefix may hold, mapped to the cell that authorized it. A key absent from this map
# is UNATTRIBUTED and fails arm (d) in either mode.
AUTHORIZED_KEYS = {
    "outset/comp_heat_freshness_tools.json":
        "OS-s-21 -- seam key 1, the freshness half, published by the 08:30 ET CodeBuild",
    "outset/comp_fedobs_coevolution.json":
        "OS-s-23 -- GROUP B's source 2 (file-pair grain), published on the same fire",
    "outset/comp_heat_drift.json":
        "OS-s-18 -- the SINGLE-KEY drift read, RETIRED as a read by OS-s-22; the OBJECT survives "
        "under PRD R-5 (never auto-delete), so its presence is required, not tolerated",
    "outset/laptop/comp_heat_drift.json":
        "O21-AC1 re-cut clause (3) -- ONE KEY PER DEVICE, the laptop's own",
    "outset/_os22_probe_device/comp_heat_drift.json":
        "OS-s-22 -- the QA fixture, excluded from the reporting-device headline count by design",
    "outset/_os18_red_arm_probe.json":
        "OS-s-18 -- the red-arm probe (the face's 'untouched R2 probe')",
}
LITERAL_ALLOWANCE = 3

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def utc(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_served_runner(s3, dest):
    """Import the SERVED runner, so arm (e)'s ceiling is exercised on the estate's own code."""
    r = s3.get_object(Bucket=BUCKET, Key=CODE_KEY)
    raw = r["Body"].read()
    with open(dest, "wb") as fh:
        fh.write(raw)
    os.environ.setdefault("ESTATE_REPORT_BUCKET", BUCKET)
    for k in ("ESTATE_GITHUB_SECRET_ID", "ESTATE_KIMI_SECRET_ID", "ESTATE_KIMI_MODEL"):
        os.environ.setdefault(k, "battery-placeholder")
    os.environ.setdefault("ESTATE_KIMI_URL", "http://placeholder.invalid")
    os.environ.setdefault("ESTATE_REPO_URL", "http://placeholder.invalid")
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    spec = importlib.util.spec_from_file_location("served_runner_os21", dest)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, r["VersionId"]


# --------------------------------------------------------------------------- (a)
def arm_a(sched):
    print("\n(a) THE SCHEDULE, READ LIVE FROM THE SCHEDULER -- never from the face")
    s = sched.get_schedule(Name=SCHEDULE_NAME)
    state, expr, tz = s["State"], s["ScheduleExpression"], s.get("ScheduleExpressionTimezone")
    target = s["Target"]["Arn"]
    print("      %s  State=%s  %s  %s" % (SCHEDULE_NAME, state, expr, tz))
    print("      target %s" % target)
    if state != "ENABLED":
        fail("a", "the schedule reads %s, not ENABLED" % state)
        return None
    if CODEBUILD_PROJECT not in target:
        fail("a", "the schedule targets %s, which does not name %s" % (target, CODEBUILD_PROJECT))
        return None
    # THE FIRE TIME MUST PRECEDE 13:00Z, and it is derived from the expression the scheduler holds
    # rather than from a number typed into this battery.
    parts = expr[expr.find("(") + 1:expr.rfind(")")].split()
    minute, hour = int(parts[0]), int(parts[1])
    # America/New_York is UTC-4 on this date; stated rather than assumed, and the ASSERTION below
    # is on the fire's own observed instant in arm (c), not on this arithmetic.
    fire_utc_h = hour + 4
    print("      fire time from the expression: %02d:%02d %s == %02d:%02d UTC (EDT, -04:00)"
          % (hour, minute, tz, fire_utc_h, minute))
    if fire_utc_h * 60 + minute >= 13 * 60:
        fail("a", "the fire time %02d:%02d UTC does not precede 13:00Z" % (fire_utc_h, minute))
        return None
    ok("ENABLED, targets the freshness publisher, and fires %d min before the 13:00Z run"
       % (13 * 60 - (fire_utc_h * 60 + minute)))
    return s


# --------------------------------------------------------------------------- (b)
def arm_b(s3):
    print("\n(b) THE SEAM ARTIFACT'S VINTAGE PRECEDES THE DAY'S RUN START")
    print("    LastModified is read with s3api head-object, in UTC -- `aws s3 ls` renders LOCAL")
    rep = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY)
    doc = json.loads(rep["Body"].read().decode("utf-8"))
    rb = doc.get("run_bundle") or {}
    started = datetime.fromisoformat(str(rb.get("started_at")))
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    print("      run %s  trigger=%r  started_at %s" % (REPORT_KEY, rb.get("trigger"), utc(started)))
    if rb.get("trigger") != "scheduled":
        fail("b", "the graded run's trigger is %r, not 'scheduled' -- this criterion cannot be "
                  "read on a hand-started day" % rb.get("trigger"))
        return None, None
    h = s3.head_object(Bucket=BUCKET, Key=FRESHNESS_KEY)
    lm = h["LastModified"].astimezone(timezone.utc)
    print("      %s  %d B  VersionId %s  LastModified %s"
          % (FRESHNESS_KEY, h["ContentLength"], h["VersionId"][:16] + "..", utc(lm)))
    delta = (started - lm).total_seconds()
    print("      vintage precedes run start by %.0f s (%.1f min)" % (delta, delta / 60.0))
    if delta <= 0:
        fail("b", "the artifact's vintage %s does NOT precede the run start %s"
             % (utc(lm), utc(started)))
        return None, None
    ok("the seam artifact's vintage precedes the run start")
    return doc, (h["VersionId"], lm)


# --------------------------------------------------------------------------- (c)
def arm_c(cb, vintage):
    print("\n(c) THE VINTAGE ATTRIBUTED TO THE SCHEDULE -- the fire's own event, not a timestamp")
    if vintage is None:
        fail("c", "no vintage from arm (b) to attribute")
        return
    vid, lm = vintage
    ids = cb.list_builds_for_project(projectName=CODEBUILD_PROJECT,
                                     sortOrder="DESCENDING")["ids"][:6]
    builds = cb.batch_get_builds(ids=ids)["builds"]
    print("      %d build(s) read from %s" % (len(builds), CODEBUILD_PROJECT))
    sched_builds, hand_builds, covering = [], [], None
    for b in builds:
        st = b["startTime"].astimezone(timezone.utc)
        en = b.get("endTime")
        en = en.astimezone(timezone.utc) if en else None
        init = b.get("initiator", "")
        is_sched = SCHEDULER_ROLE_TOKEN in init
        (sched_builds if is_sched else hand_builds).append(init)
        mark = "SCHEDULED" if is_sched else "hand"
        print("        %-9s %s -> %s  %-9s initiator=%s"
              % (mark, utc(st), utc(en) if en else "(running)", b["buildStatus"], init[:56]))
        if en and st <= lm <= en and is_sched:
            covering = (b["id"], utc(st), utc(en), init)
    print("      DENOMINATOR: %d scheduler-initiated, %d hand-initiated, %d read"
          % (len(sched_builds), len(hand_builds), len(builds)))
    if covering is None:
        fail("c", "no SCHEDULER-initiated build's window contains the artifact's LastModified %s "
                  "-- the vintage is not attributable to the schedule" % utc(lm))
        return
    ok("the artifact was written INSIDE a scheduler-initiated build's window: %s .. %s, "
       "initiator %s" % (covering[1], covering[2], covering[3][:48]))
    # THE CONTROL. `initiator` is only evidence if it can read something else. The same project's
    # earlier builds carry a human's name, so the field discriminates rather than always agreeing.
    if not hand_builds:
        fail("c", "every build read is scheduler-initiated, so the `initiator` field has not been "
                  "shown to discriminate -- attribution is unproven")
        return
    ok("CONTROL: %d build(s) of the SAME project carry a human initiator (%s), so the field "
       "discriminates a scheduled fire from a hand publish"
       % (len(hand_builds), ", ".join(sorted(set(hand_builds)))[:60]))


# --------------------------------------------------------------------------- (d)
def arm_d(s3):
    print("\n(d) THE SEAM PREFIX, ENUMERATED LIVE, EVERY KEY MAPPED TO ITS AUTHORIZING CELL")
    print("    mode=%s (see PREFIX_MODE -- the issuer's ruling sets it, not this seat)" % PREFIX_MODE)
    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": SEAM_PREFIX}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        keys.extend(o["Key"] for o in r.get("Contents", []))
        token = r.get("NextContinuationToken")
        if not token:
            break
    keys = sorted(set(keys))
    unattributed = [k for k in keys if k not in AUTHORIZED_KEYS]
    # BOTH DENOMINATORS PRINTED, as the issuer's re-cut requires: a reader sees the literal count
    # the original clause would have judged AND the attributed count the re-cut judges, so the
    # re-cut is visible in the output rather than only in the record.
    print("      DENOMINATOR, LITERAL   : %d key(s) present against an allowance of %d "
          "(the ORIGINAL clause -- it would read FAIL here, on changes this face itself ordered)"
          % (len(keys), LITERAL_ALLOWANCE))
    print("      DENOMINATOR, ATTRIBUTED: %d of %d key(s) map to a named authorizing cell; "
          "%d UNATTRIBUTED (the RE-CUT clause, 2.0.0_SA_COO 95207)"
          % (len(keys) - len(unattributed), len(keys), len(unattributed)))
    for k in keys:
        print("        %-52s %s" % (k, AUTHORIZED_KEYS.get(k, "*** UNATTRIBUTED ***")))
    if unattributed:
        fail("d", "%d key(s) under the seam prefix map to NO authorizing cell: %s"
             % (len(unattributed), ", ".join(unattributed)))
        return
    if PREFIX_MODE == "literal":
        if len(keys) > LITERAL_ALLOWANCE:
            fail("d", "LITERAL mode: %d keys present, clause admits %d. Every extra traces to a "
                      "cell this face's own re-cut ordered, so this is a FACE defect and not a "
                      "work defect -- reported as such." % (len(keys), LITERAL_ALLOWANCE))
            return
        ok("LITERAL mode: %d key(s), within the clause's allowance" % len(keys))
        return
    ok("every key present traces to a named cell; 0 unattributed. A stray publish, a wrong-prefix "
       "write or an undeclared device would fail this arm.")


# --------------------------------------------------------------------------- (e)
def arm_e(doc, mod, s3):
    print("\n(e) THE SERVED STRATUM READS FRESH, WITH ITS AGE DISCLOSED AND UNDER THE CEILING")
    if doc is None:
        fail("e", "no served document from arm (b)")
        return
    status = ((doc.get("ai") or {}).get("groups") or {}).get("A", {}).get("stratum_status")
    print("      /ai/groups/A/stratum_status = %r" % status)
    cites = [p.get("tool_row_cited") for p in ((doc.get("ai") or {}).get("proposals") or [])
             if isinstance(p, dict) and isinstance(p.get("tool_row_cited"), str)
             and "A_propagation@" in p.get("tool_row_cited")]
    print("      A_propagation citations on the served artifact: %d" % len(cites))
    if not cites:
        fail("e", "no served citation names A_propagation@, so no age is disclosed")
        return
    print("      %s" % cites[0][:220])
    import re
    ages = [float(m) for m in re.findall(r"age ([0-9.]+) h", cites[0])]
    if not ages:
        fail("e", "the served citation discloses no `age <n> h`")
        return
    print("      ages disclosed: %s  (ceiling %.1f h)" % (ages, CEILING_H))
    if status != "OK":
        fail("e", "group A reads %r, not OK" % status)
        return
    over = [a for a in ages if a >= CEILING_H]
    if over:
        fail("e", "%d disclosed age(s) at or over the %.1f h ceiling: %s" % (len(over), CEILING_H, over))
        return
    ok("group A reads OK with every disclosed age under the %.1f h ceiling (max %.1f h)"
       % (CEILING_H, max(ages)))

    # THE NEGATIVE ARM, on the SERVED function against the REAL artifact, with NO write: the same
    # reader must convict the same object STALE when the ceiling is lowered. Without this, "FRESH"
    # is a reading no input could have made fail.
    now = datetime.now(timezone.utc)
    src = "s3://%s/%s" % (BUCKET, "outset/laptop/comp_heat_drift.json")
    fresh = mod._outset_read(src, mod._outset_loader, now, CEILING_H)
    stale = mod._outset_read(src, mod._outset_loader, now, 0.001)
    print("      NEGATIVE ARM on the SAME object and the SAME reader:")
    print("        ceiling %.3f h -> status=%r" % (CEILING_H, fresh["status"]))
    print("        ceiling %.3f h -> status=%r  err=%s" % (0.001, stale["status"],
                                                           (stale["error"] or "")[:110]))
    if fresh["status"] != "OK":
        fail("e", "the device artifact does not read OK at the real ceiling (%r) -- the negative "
                  "arm below cannot be interpreted" % fresh["status"])
        return
    if stale["status"] != "INSTRUMENT_FAILED" or "STALE" not in (stale["error"] or ""):
        fail("e", "a lowered ceiling did NOT convict the same object STALE (status %r) -- the "
                  "freshness reading is not falsifiable" % stale["status"])
        return
    ok("the SAME reader convicts the SAME object STALE -> INSTRUMENT_FAILED when the ceiling is "
       "lowered, so no green here comes from a raised ceiling")


# --------------------------------------------------------------------------- (f)
def arm_f(s3):
    print("\n(f) THE DRIFT HALF -- CITED, NOT RE-DERIVED")
    print("    2.0.0_SA_COO 94867: 'drift half by OS-s-25'. TO-OS-s-25 is TERMINAL at 520503aa98")
    print("    with its own battery (OS25-DRIFT-ON-DEMAND) and its own VALID proof instance.")
    print("    Re-grading it here would be a second seat's restatement lending credibility the")
    print("    claim has not earned. What THIS day adds is read below and nothing more.")
    h = s3.head_object(Bucket=BUCKET, Key="outset/laptop/comp_heat_drift.json")
    lm = h["LastModified"].astimezone(timezone.utc)
    age_h = (datetime.now(timezone.utc) - lm).total_seconds() / 3600.0
    print("      outset/laptop/comp_heat_drift.json  VersionId %s  LastModified %s  age %.1f h"
          % (h["VersionId"][:16] + "..", utc(lm), age_h))
    if age_h >= CEILING_H:
        note("the device artifact is now PAST its %.1f h ceiling (age %.1f h). That is not a "
             "failure of this arm -- it is row NFRA_OUTSET-S38, the timer's missed fire, and it "
             "is reported there rather than absorbed here." % (CEILING_H, age_h))
    else:
        ok("the device's artifact is still inside its %.1f h ceiling on this run (age %.1f h)"
           % (CEILING_H, age_h))
    note("ROW NFRA_OUTSET-S38 stands against the CADENCE of this half: the device timer's first "
         "scheduled fire (2026-09-10T11:30Z) was SKIPPED, so every drift artifact in the bucket is "
         "hand-started. This arm does NOT claim the drift cadence is exercised.")


def main():
    print("=" * 78)
    print("O21-AC1 -- THE CADENCE, ON THE FIRST SCHEDULED FIRE THAT COULD CARRY IT")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    sched = boto3.client("scheduler", region_name="us-east-1")
    cb = boto3.client("codebuild", region_name="us-east-1")

    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".served_runner_os21.py")
    try:
        mod, vid = load_served_runner(s3, dest)
        print("served runner imported from %s @%s" % (CODE_KEY, vid[:12]))
    except Exception as exc:                                                # noqa: BLE001
        print("BLOCKED: could not load the SERVED runner (%s: %s)" % (type(exc).__name__, exc))
        return 1

    arm_a(sched)
    doc, vintage = arm_b(s3)
    arm_c(cb, vintage)
    arm_d(s3)
    arm_e(doc, mod, s3)
    arm_f(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS21-CADENCE-FRESH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
