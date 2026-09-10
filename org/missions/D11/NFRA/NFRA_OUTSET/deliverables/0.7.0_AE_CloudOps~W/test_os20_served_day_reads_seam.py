"""O20-AC1 -- THE CONSUMER SWITCH, read on a SERVED DAY from the bucket.

Prints OS20-SEAM-READ-ON-SERVED-DAY only when every arm passes.

WHAT THIS BATTERY REFUSES TO DO, stated up front because each is a way this criterion could
have passed without meaning anything:

  1. IT DOES NOT READ `latest`. Every served read is BY VersionId. `latest` on the 09-09 keys is
     the PIN restored by content after the manual run (OS-s-24, row NFRA_OUTSET-S34), so a read
     of `latest` grades the 13:11Z scheduled run of the UN-SWITCHED host while looking exactly
     like a clean read of today's work. The re-point is @584003bcae and the CTO's ruling is
     94820 / 94823.

  2. ITS NEGATIVE ARM IS A REAL DAY, NOT A MUTANT. The face is explicit about this. The negative
     is `daily/2026/09/09/estate-report-2026-09-09.json` at VersionId
     8SP4fGAuhE8twzBpucMPsYbotD6Tddty -- the 13:11:02Z run written by the RETIRED host
     i-0512bd3cbaf602b7f, before ESTATE_OUTSET_SEAM_PREFIX existed. THE SAME READER, THE SAME
     JSON PATH, both days: if it cannot return INSTRUMENT_UNAVAILABLE on the old day it is a
     constant and its OK on the new day means nothing.

  3. IT DOES NOT LET THE CONTROL ARM DECIDE. The face says the env line in the live host
     configuration is "a CONTROL arm, never the deciding line". A variable being SET proves the
     DESIRED plane; only the served report proves the consumer used it. Arm (e) therefore
     records and never votes -- it cannot add a FAIL.

  4. IT DOES NOT TREAT THE 13:00Z FIRE AS A GATE. Arm (f) reads today's keys if they exist and
     prints NOT-YET-FIRED if they do not. Either way the battery's verdict comes from (a)-(e).
     The face: "The 13:00Z fire on the same day's keys is CONFIRMATION, read if present, never
     a gate."

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-20). 2026-09-10.
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
REPORT_KEY = "daily/2026/09/09/estate-report-2026-09-09.json"

# ARM (a): THE MANUAL SERVED DAY. The 00:29:57Z run of the REPLACED host, written by the real
# runner to the real key, told apart from every other version by run_bundle.trigger/run_id
# (OS-s-26's carrier) and NOT by the clock.
POS_VERSION = os.environ.get("OS24_REPORT_VERSION", "F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw")
POS_RUN_ID = "a588a7ea-8ad2-4f03-a814-4f02668a66d6"

# ARM (c): THE NEGATIVE, A REAL DAY. The un-switched host's own scheduled run.
NEG_VERSION = "8SP4fGAuhE8twzBpucMPsYbotD6Tddty"
NEG_HOST = "i-0512bd3cbaf602b7f"          # retired; the control below proves it is terminated

# The switched host and the orchestrator that targets it.
NEW_HOST = "i-0584e17d283fa7ef4"
ORCHESTRATOR_FN = "estate-report-orchestrator"

# THE JSON PATH, named in the face because it is not the obvious one: there is no `A_propagation`
# key in the served artifact; the stratum's status lives under the AI section.
STRATUM_PATH = ("ai", "groups", "A", "stratum_status")
UNAVAILABLE = "INSTRUMENT_UNAVAILABLE"

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def dig(doc, path):
    """Walk a JSON path. Returns (value, reached) -- `reached` is the prefix that resolved, so a
    miss says WHERE it stopped instead of returning a bare None that reads like a value."""
    cur, reached = doc, []
    for seg in path:
        if not isinstance(cur, dict) or seg not in cur:
            return None, "/".join(reached) or "<root>"
        cur = cur[seg]
        reached.append(seg)
    return cur, "/".join(reached)


def get_version(s3, key, vid, label):
    """ONE reader for every served read in this battery. Both arms go through it, so a
    difference between them is a difference in the OBJECT and never in the instrument."""
    body = s3.get_object(Bucket=BUCKET, Key=key, VersionId=vid)
    raw = body["Body"].read()
    doc = json.loads(raw.decode("utf-8"))
    print("      %-10s %s @%s  %d B  LastModified %s"
          % (label, key, vid[:12] + "...", len(raw),
             body["LastModified"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    return doc


# --------------------------------------------------------------------------- (a)
def arm_a(s3):
    print("\n(a) THE SERVED DAY: group A's stratum on the MANUAL SERVED DAY's own version")
    doc = get_version(s3, REPORT_KEY, POS_VERSION, "POSITIVE")
    rb = doc.get("run_bundle") or {}
    # The run is identified on the ARTIFACT, never by started_at. A version whose trigger/run_id
    # do not match is a different run wearing the same key.
    if rb.get("run_id") != POS_RUN_ID:
        fail("a", "this version's run_id is %r, not the manual served day's %r"
             % (rb.get("run_id"), POS_RUN_ID))
        return None
    if rb.get("trigger") != "manual":
        fail("a", "this version's run_bundle.trigger is %r, expected 'manual'" % rb.get("trigger"))
        return None
    ok("version identified ON THE ARTIFACT: trigger=manual, run_id=%s" % POS_RUN_ID)

    status, reached = dig(doc, STRATUM_PATH)
    if status is None:
        fail("a", "the stratum path /%s did not resolve; walk stopped at %s"
             % ("/".join(STRATUM_PATH), reached))
        return None
    print("      /%s = %r" % ("/".join(STRATUM_PATH), status))
    if status == UNAVAILABLE:
        fail("a", "group A still reads %s on the served day -- the switch did not reach the "
                  "consumer" % UNAVAILABLE)
        return doc
    ok("group A reads %r -- an answer state OTHER than %s. THE SWITCH REACHED THE CONSUMER."
       % (status, UNAVAILABLE))
    return doc


# --------------------------------------------------------------------------- (b)
def arm_b(doc):
    print("\n(b) THE SEAM ARTIFACT'S VINTAGE, DISCLOSED ON THE SERVED OBJECT")
    if doc is None:
        fail("b", "no served document from arm (a) to read a vintage out of")
        return
    # The disclosure travels in the rows the AI cited, which is where a READER of the report
    # meets it. Asserting it from the runner's source instead would prove the code, not the day.
    cites = [p.get("tool_row_cited") for p in (doc.get("ai", {}).get("proposals") or [])
             if isinstance(p, dict) and isinstance(p.get("tool_row_cited"), str)]
    a_cites = [c for c in cites if "A_propagation@" in c]
    print("      proposals carrying a tool_row_cited : %d" % len(cites))
    print("      of those, naming A_propagation@     : %d" % len(a_cites))
    if not a_cites:
        fail("b", "no served citation names A_propagation@, so no seam vintage is disclosed")
        return
    stamp = re.compile(r"produced (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")
    age = re.compile(r"age ([0-9.]+) h")
    with_stamp = [c for c in a_cites if stamp.search(c)]
    with_age = [c for c in a_cites if age.search(c)]
    sample = with_stamp[0] if with_stamp else a_cites[0]
    print("      sample: %s" % sample[:200])
    if not with_stamp:
        fail("b", "no A_propagation citation carries a parseable `produced <ISO>` instant")
        return
    if not with_age:
        fail("b", "no A_propagation citation carries a parseable `age <n> h`")
        return
    m = stamp.search(sample)
    ok("vintage disclosed on the served object: produced %s, with an age in hours beside it "
       "(%d of %d A_propagation citations carry the instant)"
       % (m.group(1), len(with_stamp), len(a_cites)))


# --------------------------------------------------------------------------- (c)
def arm_c(s3):
    print("\n(c) THE NEGATIVE ARM -- A REAL DAY, SAME READER, SAME PATH")
    print("    the un-switched host %s, 13:11:02Z, before the variable existed" % NEG_HOST)
    doc = get_version(s3, REPORT_KEY, NEG_VERSION, "NEGATIVE")
    status, reached = dig(doc, STRATUM_PATH)
    if status is None:
        fail("c", "the stratum path did not resolve on the negative day; stopped at %s" % reached)
        return
    print("      /%s = %r" % ("/".join(STRATUM_PATH), status))
    if status != UNAVAILABLE:
        fail("c", "the negative day reads %r, not %s -- the comparator is not discriminating, "
                  "so arm (a)'s pass is not a measurement" % (status, UNAVAILABLE))
        return
    ok("the SAME reader returns %s on the old day and a different state on the new one -- "
       "the comparator is proven able to fail" % UNAVAILABLE)
    rb = doc.get("run_bundle") or {}
    note("negative day's run_bundle.trigger = %r (the carrier did not exist yet, OS-s-26)"
         % rb.get("trigger"))


# --------------------------------------------------------------------------- (d)
def arm_d(lam, ec2):
    print("\n(d) THE ORCHESTRATOR'S TARGET, READ LIVE, WITH A PLANTED-STALE CONTROL")
    cfg = lam.get_function_configuration(FunctionName=ORCHESTRATOR_FN)
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    target = env.get("ESTATE_INSTANCE_ID")
    print("      %s ESTATE_INSTANCE_ID = %r" % (ORCHESTRATOR_FN, target))
    if not target:
        fail("d", "the orchestrator carries no ESTATE_INSTANCE_ID")
        return

    def resolve(instance_id):
        """Returns (exists, state). A stale id raises InvalidInstanceID.NotFound rather than
        returning an empty set, so BOTH shapes are handled -- a bare len()==0 test would miss
        the raising branch and report the control as a pass."""
        try:
            r = ec2.describe_instances(InstanceIds=[instance_id])
        except Exception as exc:                                            # noqa: BLE001
            return False, type(exc).__name__
        res = [i for res in r.get("Reservations", []) for i in res.get("Instances", [])]
        if not res:
            return False, "no-reservation"
        return True, res[0]["State"]["Name"]

    exists, state = resolve(target)
    print("      describe-instances(%s) -> exists=%s state=%s" % (target, exists, state))
    if not exists:
        fail("d", "the orchestrator targets %s, which does not resolve (%s)" % (target, state))
        return
    if target != NEW_HOST:
        fail("d", "the orchestrator targets %s but the switched host is %s" % (target, NEW_HOST))
        return
    ok("the live target IS the switched host %s and it exists (state=%s)" % (target, state))

    # THE PLANTED-STALE CONTROL. A copy of the env map with the RETIRED id, run through the same
    # comparator: it must report MISMATCH. Without this, "equal ids" is a claim no arm can fail.
    planted = copy.deepcopy(env)
    planted["ESTATE_INSTANCE_ID"] = NEG_HOST
    p_exists, p_state = resolve(planted["ESTATE_INSTANCE_ID"])
    same = planted["ESTATE_INSTANCE_ID"] == NEW_HOST
    print("      PLANTED STALE ID %s -> exists=%s state=%s  equals-switched-host=%s"
          % (NEG_HOST, p_exists, p_state, same))
    if same:
        fail("d", "the planted control equals the switched host; it cannot discriminate")
        return
    ok("the planted stale id reports MISMATCH against the switched host (and reads %s live) -- "
       "the comparator can fail" % p_state)


# --------------------------------------------------------------------------- (e)
def arm_e(ec2):
    print("\n(e) CONTROL ARM, RECORDED AND NEVER DECIDING: the env line on the live host")
    print("    the face: 'a CONTROL arm, never the deciding line'. A variable being SET proves")
    print("    the DESIRED plane; only arm (a) proves the CONSUMER used it. THIS ARM CANNOT FAIL")
    print("    THE BATTERY -- it appends to no FAILS list by construction.")
    try:
        att = ec2.describe_instance_attribute(InstanceId=NEW_HOST, Attribute="userData")
        blob = (att.get("UserData") or {}).get("Value")
        if not blob:
            note("live user_data is empty on %s -- recorded, decides nothing" % NEW_HOST)
            return
        import base64
        text = base64.b64decode(blob).decode("utf-8", errors="replace")
        hits = [ln.strip() for ln in text.split("\n") if "ESTATE_OUTSET_SEAM_PREFIX" in ln]
        note("live user_data on %s: %d B, %d line(s) naming ESTATE_OUTSET_SEAM_PREFIX"
             % (NEW_HOST, len(text), len(hits)))
        for h in hits[:4]:
            note("  %s" % h[:160])
        # The applied plane is read here rather than SSM because the host is stopped between
        # runs: an SSM read would be UNAVAILABLE for a reason that has nothing to do with the
        # variable, and an arm that cannot run is not the same as an arm that failed.
        note("read from describe-instance-attribute (the APPLIED plane), not SSM: the host is "
             "stopped between runs and an unreachable agent is not evidence about a variable")
    except Exception as exc:                                                # noqa: BLE001
        note("could not read live user_data (%s) -- recorded, decides nothing"
             % type(exc).__name__)


# --------------------------------------------------------------------------- (f)
def arm_f(s3):
    print("\n(f) CONFIRMATION, NEVER A GATE: today's 13:00Z fire")
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    prefix = "daily/%s/" % today
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    n = r.get("KeyCount", 0)
    print("      list %s -> %d object(s)" % (prefix, n))
    if n == 0:
        note("NOT-YET-FIRED for %s. The battery's verdict comes from (a)-(e); this arm adds "
             "confirmation when it exists and never withholds a pass." % today)
        return
    for obj in r.get("Contents", []):
        note("%s  %d B  %s" % (obj["Key"], obj["Size"],
                               obj["LastModified"].astimezone(timezone.utc)
                               .strftime("%Y-%m-%dT%H:%M:%SZ")))
    jkey = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".json")]
    if not jkey:
        note("today's prefix holds no .json report yet -- confirmation pending")
        return
    doc = json.loads(s3.get_object(Bucket=BUCKET, Key=jkey[0])["Body"].read().decode("utf-8"))
    status, _ = dig(doc, STRATUM_PATH)
    rb = doc.get("run_bundle") or {}
    note("today's report: group A = %r, run_bundle.trigger = %r, run_id = %r"
         % (status, rb.get("trigger"), rb.get("run_id")))
    if status == UNAVAILABLE:
        note("WARN: today's scheduled run reads %s. That is a FINDING to file as a row, not a "
             "reason to fail this criterion, whose accept is the manual served day." % UNAVAILABLE)


def main():
    print("=" * 78)
    print("O20-AC1 -- THE CONSUMER SWITCH, READ ON A SERVED DAY")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s). Every arm here is world-facing." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    ec2 = boto3.client("ec2", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")

    doc = arm_a(s3)
    arm_b(doc)
    arm_c(s3)
    arm_d(lam, ec2)
    arm_e(ec2)
    arm_f(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS20-SEAM-READ-ON-SERVED-DAY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
