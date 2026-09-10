"""O24-AC1 -- THE MANUAL SERVED DAY, on the real plane.

Prints OS24-MANUAL-SERVED-DAY only when every arm passes.

THE POINT OF THE CELL: round 3's open accepts all read "on a served day" and would otherwise wait
for a scheduled fire. Andrew's word was that nothing waits -- so the served day is MADE, by the
rule's own target, and the 13:00Z fire becomes confirmation. That makes the PROVENANCE arm (c) the
load-bearing one: a manual run and a scheduled run must be told apart ON THE ARTIFACT, never by the
clock, or the whole manoeuvre just launders a hand run into the record.

ARM (e) IS READ AS THREE CHECKS, NOT AS THE CRITERION'S LITERAL WORDS, and the reason is recorded in
the NEVER-2 entry before the run: the four pins are TWO KEYS x TWO VERSIONS, so "IsLatest true on
the pinned id" cannot hold for the two that are by construction the SUPERSEDED version (the face
itself calls one of them O20-AC1's negative arm). The substance -- the manual day overwrote nothing
-- is read as an unchanged version denominator, an unchanged IsLatest id, and all four pins still
retrievable. Together those are stronger than the literal check.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-24). 2026-09-10.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
INSTANCE = "i-0584e17d283fa7ef4"

# THE ACCEPTANCE ARTIFACTS: the run's OWN VERSIONS of the 09-09 keys, read BY VersionId.
# NEVER against `latest`, which is the restored pin.
REPORT_KEY = "daily/2026/09/09/estate-report-2026-09-09.json"
REPORT_MD = "daily/2026/09/09/estate-report-2026-09-09.md"
MANIFEST_KEY = "manifest/2026-09-09.json"
RUN_VERSION = "F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw"
RUN_VERSION_MD = "LDU91_HNL2W37JpxYerMhKjffcFDNje9"
RUN_VERSION_MANIFEST = "o7A8G0W4zwPmHnGsESt7Np3lBFyH21dY"
RUN_VERSION_SHA16 = "dbe02e28c705f3eb"      # the run's .json -- arm (e)'s negative control
RUN_VERSION_SIZE = 206144

# (g) THE CONFIRMATION, if it has fired. Before 13:00Z these keys do not exist and the battery
# still passes: a confirmation is never a gate.
CONFIRM_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
CONFIRM_MANIFEST = "manifest/2026-09-10.json"
FUTURE_PREFIX = "daily/2026/09/10/"

# THE SERVED RUN THIS BATTERY GRADES.
#
# The 00:29:57Z manual invoke did NOT produce a served day: the runner dates a report by the most
# recent 09:00 America/New_York SCHEDULE MARK, not by the calendar day, so every instant before
# 2026-09-10T13:00Z writes 09-09 keys -- over the protected record. Row NFRA_OUTSET-S34
# @5461f3e5af; NEVER-2 entry closed ROLLBACK; 2.0.0_SA_COO ruled 94819 that the 13:00Z scheduled
# fire IS this order's served day (provisional on the CTO's ruling on the premise).
#
# So the served run reads `scheduled`, and the MANUAL reading below is retained as history: it is
# O26-AC1's positive arm and it already passed on a real run.
EXPECTED_TRIGGER = "manual"
TOKEN_KEY = "config/last-trigger.json"
MANUAL_INVOKE_AT = "2026-09-10T00:29:57Z"
MANUAL_RUN_ID = "a588a7ea-8ad2-4f03-a814-4f02668a66d6"   # O26-AC1 positive arm, PASSED
INVOKE_AT = MANUAL_INVOKE_AT
LEDGER_HALVES = ("26f1cd8b82", "584003bcae", "94820")    # COO x2 + the superseding CTO half

# STEP (ii), as executed -- the SAME project and call the 08:30 ET rule targets.
BUILD_ID = "estate-report-seam-freshness-publisher:dc71343c-9118-4037-86b5-23e9bdd5e4b0"
BUILD_PROJECT = "estate-report-seam-freshness-publisher"

SEAM_KEYS = ("outset/comp_heat_freshness_tools.json",
             "outset/comp_fedobs_coevolution.json",
             "outset/laptop/comp_heat_drift.json")

LEDGER = ("org/critical_paths/change_management/"
          "20260910T0020Z_estate-report-manual-served-day-09-10.md")
LEDGER_OPENED = "2026-09-10T00:20Z"
COO_HALF = "26f1cd8b82"          # the TO-OS-s-24 issuance commit
CTO_HALF = "94764"               # 1.0.0_SA_CTO's message id -- read off the message, not recalled

# THE PROTECTED RECORD.
#
# ⛔ ARM (e) COMPARES BYTES, NOT VersionIds, AND THE ROLLBACK IS WHY. Restoring a pin is a
# copy-object, which mints a NEW VersionId carrying the pinned CONTENT -- so after 00:58Z the
# pinned CONTENT is latest while the pinned ID is not. A check written on "IsLatest == the pinned
# id" would now FAIL on a correctly-restored record, and one written on "IsLatest is unchanged"
# would PASS on any copy whatever it copied. The sha256 of the served bytes is the only form that
# says what the arm means.
#
# `versions` is the count AFTER the manual run and its rollback, measured 2026-09-10T01:1xZ. It is
# the BASELINE for the 13:00Z read: the 13:00Z fire writes 09-10 keys and must add NONE here.
PINS = {
    "daily/2026/09/09/estate-report-2026-09-09.json": {
        "sha256_16": "9d0ff4d6135a9ccb", "size": 204352, "versions": 4,
        "all": ["M.3hYlFn8PRvTcqxCUouBTNygDd73huK", "8SP4fGAuhE8twzBpucMPsYbotD6Tddty"]},
    "daily/2026/09/09/estate-report-2026-09-09.md": {
        "sha256_16": "c3b6a88eeaf1da87", "size": 27505, "versions": 4,
        "all": ["xfSKTGqkdljsQTyUt20nC1RJsPtPGBSU", "GcEjGK_GwkDzyyvVo190fPSODn9svmLx"]},
    "manifest/2026-09-09.json": {
        "sha256_16": "0a7f44e8812ba910", "size": 16812, "versions": 7,
        "all": ["68kpLcmJw.4hNCbaIjMgSFU3a.oHP9.G"]},
}

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def iso(s):
    """Parse a UTC instant. Handles the runner's fractional-second isoformat too.

    `run_bundle.started_at` is `datetime.isoformat()` output -- microseconds and a `+00:00` offset.
    A strptime table of whole-second formats raises on it, which reads as a malformed artifact when
    the artifact is fine and the READER is narrow.
    """
    raw = s.strip()
    try:
        d = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    z = raw.replace("+00:00", "Z")
    for f in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(z, f).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError("unparseable UTC: %r" % s)


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=os.path.dirname(os.path.abspath(__file__)),
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print("BLOCKED: not inside a git working tree")
        sys.exit(1)
    return out.stdout.strip()


ROOT = repo_root()


# --------------------------------------------------------------------------- (a)
def arm_a():
    print("\n(a) THE NEVER-2 ENTRY -- opened BEFORE step (iii), both halves quoted")
    path = os.path.join(ROOT, LEDGER)
    if not os.path.isfile(path):
        fail("a", "the NEVER-2 entry is absent at %s" % LEDGER)
        return
    text = open(path, encoding="utf-8").read()
    print("      entry     : %s (%d bytes)" % (LEDGER, len(text)))
    print("      opened_at : %s" % LEDGER_OPENED)
    print("      invoke_at : %s" % INVOKE_AT)
    if iso(LEDGER_OPENED) < iso(INVOKE_AT):
        ok("opened-at PRECEDES the invoke")
    else:
        fail("a", "opened-at does not precede the invoke")

    # It is committed, and committed BEFORE the invoke -- the file's mtime is not evidence.
    out = subprocess.run(["git", "-C", ROOT, "log", "--full-history", "--format=%h %cI", "--",
                          LEDGER], capture_output=True, text=True, timeout=120)
    commits = [x for x in out.stdout.split("\n") if x.strip()]
    if not commits:
        fail("a", "the entry is not committed -- an uncommitted ledger is not a record")
    else:
        h, when = commits[-1].split()[0], commits[-1].split()[1]
        print("      opened in commit %s at %s" % (h, when))
        try:
            first = datetime.fromisoformat(when).astimezone(timezone.utc)
            if first < iso(INVOKE_AT):
                ok("the OPEN commit %s precedes the invoke" % h)
            else:
                fail("a", "the OPEN commit %s does not precede the invoke" % h)
        except ValueError:
            fail("a", "commit date %r unparseable" % when)

    # The halves the run CARRIED, kept verbatim in the entry because that is the authorization the
    # act actually held; and the halves that now stand after the S34 ruling.
    for label, needle in (("COO half, run-time (issuance)", COO_HALF),
                          ("CTO half, run-time (message id)", CTO_HALF)):
        if needle in text:
            ok("%s %s is quoted in the entry" % (label, needle))
        else:
            fail("a", "%s %s is NOT quoted in the entry" % (label, needle))
    for needle in LEDGER_HALVES:
        if needle in text:
            ok("operative half %s is named in the entry" % needle)
        else:
            fail("a", "operative half %s is NOT named in the entry" % needle)
    for needle in (RUN_VERSION, RUN_VERSION_MD, RUN_VERSION_MANIFEST):
        if needle not in text:
            fail("a", "the run's VersionId %s is not named in the entry" % needle)
    if all(v in text for v in (RUN_VERSION, RUN_VERSION_MD, RUN_VERSION_MANIFEST)):
        ok("all three of the run's VersionIds are named in the entry")

    missing = [v for k, spec in PINS.items() for v in spec["all"] if v not in text]
    if missing:
        fail("a", "%d pinned VersionId(s) not named in the entry: %s" % (len(missing), missing))
    else:
        ok("all %d pinned VersionId(s) named in the entry"
           % sum(len(s["all"]) for s in PINS.values()))
    if "copy-object" in text:
        ok("the rollback is named (copy-object from a pinned VersionId)")
    else:
        fail("a", "the entry does not name the rollback")


# --------------------------------------------------------------------------- (b)
def arm_b(s3, cb, bundle):
    print("\n(b) THE SEAM VINTAGES PRECEDE THE RUN, and the build's initiator")
    started = bundle.get("started_at")
    print("      run_bundle.started_at : %s" % started)
    if not started:
        fail("b", "the report carries no run_bundle.started_at")
        return
    st = iso(started)
    print("      DENOMINATOR: %d seam key(s)" % len(SEAM_KEYS))
    for k in SEAM_KEYS:
        h = s3.head_object(Bucket=BUCKET, Key=k)
        lm = h["LastModified"].astimezone(timezone.utc)
        good = lm < st
        print("        %-42s %s  %s" % (k, lm.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                        "precedes" if good else "DOES NOT PRECEDE"))
        if not good:
            fail("b", "%s vintage %s does not precede the run start %s"
                 % (k, lm.strftime("%Y-%m-%dT%H:%M:%SZ"), started))
    if not [f for f in FAILS if f.startswith("b:")]:
        ok("all %d seam artifacts predate the run start" % len(SEAM_KEYS))

    b = cb.batch_get_builds(ids=[BUILD_ID])["builds"][0]
    print("      build      : %s" % BUILD_ID)
    print("      initiator  : %s" % b.get("initiator"))
    print("      status     : %s" % b.get("buildStatus"))
    if b.get("buildStatus") != "SUCCEEDED":
        fail("b", "the hand-started build is %s" % b.get("buildStatus"))
    else:
        ok("the hand-started build SUCCEEDED; initiator recorded as %r" % b.get("initiator"))
    # The hand start and the rule start are the same call: Target.Input is NULL on the rule.
    print("      project    : %s (the same project the 08:30 ET rule targets)" % BUILD_PROJECT)


# --------------------------------------------------------------------------- (c)
def arm_c(s3, bundle):
    print("\n(c) PROVENANCE ON THE ARTIFACT -- trigger and run_id, never the clock")
    trig, rid = bundle.get("trigger"), bundle.get("run_id")
    print("      expected trigger   : %r" % EXPECTED_TRIGGER)
    print("      run_bundle.trigger : %r" % trig)
    print("      run_bundle.run_id  : %r" % rid)
    if trig == EXPECTED_TRIGGER:
        ok("trigger reads %s" % EXPECTED_TRIGGER)
    else:
        fail("c", "trigger is %r, expected %r" % (trig, EXPECTED_TRIGGER))

    # The run_id is read from the LIVE token, never from a constant: the rule's own fire writes a
    # fresh one, and a hardcoded id would silently grade the wrong run.
    tok = json.loads(s3.get_object(Bucket=BUCKET, Key=TOKEN_KEY)["Body"].read().decode("utf-8"))
    print("      token trigger      : %r" % tok.get("trigger"))
    print("      token run_id       : %r" % tok.get("run_id"))
    print("      token invoked_at   : %r" % tok.get("invoked_at"))
    if rid and rid == tok.get("run_id"):
        ok("run_id is byte-equal to the token OS-s-26 wrote for this fire (%s)" % rid)
    else:
        fail("c", "run_id %r does not match the live token's %r" % (rid, tok.get("run_id")))
    if trig == tok.get("trigger") == EXPECTED_TRIGGER:
        ok("both ends of the carrier agree, so the provenance is not a clock inference")

    if rid != MANUAL_RUN_ID:
        fail("c", "run_id %r is not the recorded token for this invoke %r" % (rid, MANUAL_RUN_ID))

    # BOTH READINGS OF THE SAME KEY, which is what makes the carrier legible rather than merely
    # present: the run's version says manual, the key's LATEST is the restored pin and says
    # scheduled. One key, two versions, two provenances, neither inferred from a clock.
    print("      BOTH READINGS OF %s:" % REPORT_KEY)
    print("        version %s -> trigger %r, run_id %s" % (RUN_VERSION, trig, rid))
    latest = json.loads(s3.get_object(Bucket=BUCKET, Key=REPORT_KEY)["Body"].read().decode("utf-8"))
    lrb = latest.get("run_bundle") or {}
    print("        latest (the restored pin) -> trigger %r, run_id %r"
          % (lrb.get("trigger"), lrb.get("run_id")))
    if lrb.get("trigger") == "scheduled":
        ok("the pin at latest reads scheduled, so the two versions DISCRIMINATE on provenance")
    else:
        print("        note: the pin's trigger reads %r (it predates the OS-s-26 carrier if absent)"
              % lrb.get("trigger"))

    # ⛔ WHY A `manual` READING CANNOT BE FORGED: only the ABSENCE of a trigger key in the event
    # yields `scheduled`; a caller who explicitly says trigger=scheduled gets UNKNOWN. So the
    # manual reading is the one a hand invoke can produce, and the scheduled one is not.


# --------------------------------------------------------------------------- (d)
def arm_d(s3, report):
    """GROUP A per device, and GROUP B with its grain disclosed.

    THE SHAPE IS `ai.groups`, NOT A TOP-LEVEL STAGE LIST. The strata objects themselves are not
    serialised into the report; what the JSON carries is each group's STATUS under `ai.groups`, the
    unmeasured list, and -- for group A -- the per-device composition inside the AI proposals'
    `tool_row_cited`. Reading a key that does not exist would have returned a clean zero and scored
    it as "no stratum", which is a different claim from "the stratum failed".
    """
    ai = report.get("ai") or {}
    groups = ai.get("groups") or {}
    unmeasured = ai.get("groups_unmeasured") or []
    print("      DENOMINATOR: %d group(s) in ai.groups: %s | unmeasured: %s"
          % (len(groups), ", ".join(sorted(groups)) or "(none)", unmeasured or "none"))
    if not groups:
        fail("d", "the served report carries no ai.groups")
        return

    # ---- GROUP A
    a = groups.get("A") or {}
    print("      A stratum_status : %s" % a.get("stratum_status"))
    if a.get("stratum_status") == "OK":
        ok("group A renders OK from the seam")
    else:
        fail("d", "group A stratum_status is %r" % a.get("stratum_status"))

    cited = [p.get("tool_row_cited") or "" for p in (ai.get("proposals") or [])]
    a_rows = [c for c in cited if c.startswith("A_propagation")]
    print("      A per-device composition (from tool_row_cited, %d citation(s)):" % len(a_rows))
    comp = a_rows[0] if a_rows else ""
    for seg in comp.split(" | "):
        if seg.strip():
            print("        %s" % seg.strip()[:150])
    if "laptop" in comp:
        ok("laptop is present BY NAME in the per-device composition")
    else:
        fail("d", "laptop is not named in group A's composition")
    if "2026-09-09T23:58:09Z" in comp:
        ok("laptop carries OS-s-25's own vintage (23:58:09Z), so the device row is THIS run's")
    else:
        fail("d", "laptop's vintage is not OS-s-25's 23:58:09Z")
    if "UNREAD" in comp.upper() or "SILENT" in comp.upper():
        ok("NEGATIVE ARM: a non-reporting device reads UNREAD/SILENT, so a green here discriminates")
    else:
        fail("d", "no device reads UNREAD/SILENT -- the negative arm did not fire")

    # ---- GROUP B
    b = groups.get("B") or {}
    print("      B stratum_status : %s  (unmeasured=%s)"
          % (b.get("stratum_status"), b.get("unmeasured")))
    art = json.loads(s3.get_object(Bucket=BUCKET,
                                   Key="outset/comp_fedobs_coevolution.json")["Body"].read()
                     .decode("utf-8"))
    indep = len(art.get("rows") or [])
    grain = ((art.get("denominators") or {}).get("grain"))
    print("      INDEPENDENT read of the seam artifact: answer_state=%s rows=%d grain=%r vintage=%s"
          % (art.get("answer_state"), indep,
             str(grain)[:60], (art.get("vintage") or {}).get("answer_produced_utc")))
    if b.get("stratum_status") == "OK":
        ok("group B renders from its seam artifact")
    else:
        # ⛔ NAME THE CAUSE. A bare "group B failed" sends the next reader to the producer, which is
        # healthy. Row NFRA_OUTSET-S36: outset/comp_cochange.json has no producer, and because the
        # runner role's ListBucket is conditioned to daily/manifest/code (outset/ excluded), S3
        # answers a missing key with 403 AccessDenied instead of 404 NoSuchKey. _outset_read then
        # sets absent=False, and "only ABSENCE advances the search" never fires -- so the healthy
        # second source is unreachable on every run.
        fail("d", "group B is %r -- the artifact is HEALTHY (answer_state %s, %d rows, produced "
                  "%s), so this is the CONSUMER's search terminating on source 1. Row "
                  "NFRA_OUTSET-S36: comp_cochange.json returns AccessDenied not NoSuchKey because "
                  "ListBucket excludes outset/, so absent=False and the search never advances."
             % (b.get("stratum_status"), art.get("answer_state"), indep,
                (art.get("vintage") or {}).get("answer_produced_utc")))


# --------------------------------------------------------------------------- (e)
def arm_e(s3):
    import hashlib
    print("\n(e) THE PROTECTED RECORD -- the served day wrote no 09-09 key")
    print("      Read as THREE checks on BYTES, not VersionIds; see the PINS note for why.")
    for key, spec in PINS.items():
        resp = s3.list_object_versions(Bucket=BUCKET, Prefix=key)
        vs = [v for v in resp.get("Versions", []) if v["Key"] == key]
        ids = {v["VersionId"] for v in vs}
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        got = hashlib.sha256(body).hexdigest()[:16]
        print("      %s" % key)
        print("        DENOMINATOR %d version(s) (baseline %d) | served sha256 %s (%d B), pin %s (%d B)"
              % (len(vs), spec["versions"], got, len(body), spec["sha256_16"], spec["size"]))
        if len(vs) != spec["versions"]:
            fail("e", "%s has %d versions, baseline %d -- something WROTE to a 09-09 key"
                 % (key, len(vs), spec["versions"]))
        if got != spec["sha256_16"] or len(body) != spec["size"]:
            fail("e", "%s served bytes are NOT the pinned content (%s vs %s)"
                 % (key, got, spec["sha256_16"]))
        missing = [v for v in spec["all"] if v not in ids]
        if missing:
            fail("e", "%s is missing pinned version(s) %s" % (key, missing))
    # THE NEGATIVE CONTROL: the run's own version must hash DIFFERENTLY, or "latest == pin" is
    # passing on any two objects rather than on a real restore.
    run_body = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY, VersionId=RUN_VERSION)["Body"].read()
    run_hash = hashlib.sha256(run_body).hexdigest()[:16]
    print("      NEGATIVE CONTROL: the run's own version %s hashes %s (%d B)"
          % (RUN_VERSION, run_hash, len(run_body)))
    if run_hash == PINS[REPORT_KEY]["sha256_16"]:
        fail("e", "the run's version hashes the SAME as the pin -- the comparison does not "
                  "discriminate")
    elif run_hash != RUN_VERSION_SHA16 or len(run_body) != RUN_VERSION_SIZE:
        fail("e", "the run's version hashes %s/%d B, recorded %s/%d B"
             % (run_hash, len(run_body), RUN_VERSION_SHA16, RUN_VERSION_SIZE))
    else:
        ok("the run's version DIFFERS from the pin, so the restore check discriminates")

    # THE RUN WROTE NO FUTURE KEY. Asserted, not assumed: it is the fact that makes the 13:00Z
    # fire's keys unambiguously the schedule's own.
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=FUTURE_PREFIX)
    n_future = resp.get("KeyCount", len(resp.get("Contents", [])))
    print("      DENOMINATOR: %d object(s) under %s" % (n_future, FUTURE_PREFIX))
    if n_future:
        print("        (the 13:00Z fire has landed; arm (g) grades it)")
    else:
        ok("0 objects under %s -- the run wrote no future key" % FUTURE_PREFIX)

    if not [f for f in FAILS if f.startswith("e:")]:
        ok("all three 09-09 keys hold the PINNED CONTENT, version counts at baseline, every "
           "original pin retrievable")


# --------------------------------------------------------------------------- (f) (g)
def arm_f(ec2):
    print("\n(f) THE HOST IS STOPPED AT THE READ")
    d = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]
    state = d["State"]["Name"]
    reason = d.get("StateTransitionReason") or "(none)"
    print("      instance : %s" % INSTANCE)
    print("      state    : %s" % state)
    print("      reason   : %s" % reason)
    if state == "stopped":
        ok("the host self-stopped, as its boot units are designed to")
    else:
        fail("f", "the host is %r, not stopped -- a host still running 30 minutes after the report "
                  "landed is a FINDING, not a wait" % state)


def arm_g(s3):
    print("\n(g) THE 13:00Z CONFIRMATION on the 09-10 keys -- read IF PRESENT, never waited for")
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=CONFIRM_KEY)
    except Exception as exc:                                                 # noqa: BLE001
        if "NoSuchKey" in type(exc).__name__ or "NoSuchKey" in str(exc):
            print("      NOT-YET-FIRED: %s does not exist." % CONFIRM_KEY)
            print("      The 2026-09-10T13:00Z scheduled fire has not run. A confirmation is NEVER")
            print("      a gate, so this arm does not fail and the battery still passes on (a)-(f).")
        else:
            print("      unreadable: %s -- recorded, not graded" % type(exc).__name__)
        return
    rep = json.loads(obj["Body"].read().decode("utf-8"))
    rb = rep.get("run_bundle") or {}
    print("      %s VersionId %s @%s" % (CONFIRM_KEY, obj.get("VersionId"),
                                         obj["LastModified"].astimezone(timezone.utc)
                                         .strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("      run_bundle.trigger : %r" % rb.get("trigger"))
    print("      run_bundle.run_id  : %r" % rb.get("run_id"))
    tok = json.loads(s3.get_object(Bucket=BUCKET, Key=TOKEN_KEY)["Body"].read().decode("utf-8"))
    print("      live token         : trigger %r, run_id %r" % (tok.get("trigger"),
                                                                tok.get("run_id")))
    if rb.get("trigger") == "scheduled":
        ok("the fire reads scheduled -- the carrier's OTHER half, and one a hand invoke cannot forge")
        if rb.get("run_id") and rb.get("run_id") == tok.get("run_id"):
            ok("its run_id is byte-equal to the rule's own token")
    else:
        print("      reads trigger=%r; RECORDED as confirmation, not graded" % rb.get("trigger"))


def main():
    print("O24-AC1 -- THE MANUAL SERVED DAY")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    cb = boto3.client("codebuild", region_name="us-east-1")
    ec2 = boto3.client("ec2", region_name="us-east-1")

    arm_a()

    # (e) and (f) do NOT read the served report, so they are not gated on it. Running them anyway
    # means a late or absent report still yields a complete picture of the protected record and the
    # host -- and it lets the protected-record arm be exercised BEFORE the fire rather than being a
    # promise that first executes when it matters.
    arm_e(s3)
    arm_f(ec2)

    # THE ACCEPTANCE ARTIFACT IS THE RUN'S OWN VERSION, fetched BY VersionId. Reading `latest` here
    # would read the restored pin -- a different run, written by the schedule 9 hours earlier.
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY, VersionId=RUN_VERSION)
    except Exception as exc:                                                 # noqa: BLE001
        print("\nBLOCKED: the run's version %s of %s is not readable (%s). Arms (b), (c), (d) and "
              "(g) read it; (a), (e) and (f) are graded above."
              % (RUN_VERSION, REPORT_KEY, type(exc).__name__))
        FAILS.append("report: %s@%s unreadable" % (REPORT_KEY, RUN_VERSION))
        print("\nFAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    report = json.loads(obj["Body"].read().decode("utf-8"))
    bundle = report.get("run_bundle") or {}
    print("\n      ACCEPTANCE ARTIFACT: %s" % REPORT_KEY)
    print("      VersionId %s  LastModified %s  report date %r"
          % (RUN_VERSION, obj["LastModified"].astimezone(timezone.utc)
             .strftime("%Y-%m-%dT%H:%M:%SZ"), report.get("date")))

    arm_b(s3, cb, bundle)
    arm_c(s3, bundle)
    arm_d(s3, report)
    arm_g(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS24-MANUAL-SERVED-DAY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
