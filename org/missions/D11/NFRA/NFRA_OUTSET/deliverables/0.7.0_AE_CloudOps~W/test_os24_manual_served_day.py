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

REPORT_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
REPORT_MD = "daily/2026/09/10/estate-report-2026-09-10.md"
MANIFEST_KEY = "manifest/2026-09-10.json"

# STEP (iii), as executed. The token's run_id is what arm (c) matches the report against.
INVOKE_AT = "2026-09-10T00:29:57Z"
TOKEN_KEY = "config/last-trigger.json"
TOKEN_RUN_ID = "a588a7ea-8ad2-4f03-a814-4f02668a66d6"

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

PINS = {
    "daily/2026/09/09/estate-report-2026-09-09.json": {
        "latest": "M.3hYlFn8PRvTcqxCUouBTNygDd73huK",
        "all": ["M.3hYlFn8PRvTcqxCUouBTNygDd73huK", "8SP4fGAuhE8twzBpucMPsYbotD6Tddty"],
        "versions": 2},
    "daily/2026/09/09/estate-report-2026-09-09.md": {
        "latest": "xfSKTGqkdljsQTyUt20nC1RJsPtPGBSU",
        "all": ["xfSKTGqkdljsQTyUt20nC1RJsPtPGBSU", "GcEjGK_GwkDzyyvVo190fPSODn9svmLx"],
        "versions": 2},
    "manifest/2026-09-09.json": {
        "latest": "68kpLcmJw.4hNCbaIjMgSFU3a.oHP9.G",
        "all": ["68kpLcmJw.4hNCbaIjMgSFU3a.oHP9.G"],
        "versions": 4},
}

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def iso(s):
    s = s.replace("+00:00", "Z")
    for f in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(s, f).replace(tzinfo=timezone.utc)
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

    for label, needle in (("COO half (issuance)", COO_HALF), ("CTO half (message id)", CTO_HALF)):
        if needle in text:
            ok("%s %s is quoted in the entry" % (label, needle))
        else:
            fail("a", "%s %s is NOT quoted in the entry" % (label, needle))

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
    print("      run_bundle.trigger : %r" % trig)
    print("      run_bundle.run_id  : %r" % rid)
    if trig == "manual":
        ok("trigger reads manual")
    else:
        fail("c", "trigger is %r, expected 'manual'" % trig)

    tok = json.loads(s3.get_object(Bucket=BUCKET, Key=TOKEN_KEY)["Body"].read().decode("utf-8"))
    print("      token trigger      : %r" % tok.get("trigger"))
    print("      token run_id       : %r" % tok.get("run_id"))
    print("      token invoked_at   : %r" % tok.get("invoked_at"))
    if rid and rid == tok.get("run_id") == TOKEN_RUN_ID:
        ok("run_id matches the token OS-s-26 wrote for THIS invoke (%s)" % TOKEN_RUN_ID)
    else:
        fail("c", "run_id %r does not match the token's %r / the recorded %r"
             % (rid, tok.get("run_id"), TOKEN_RUN_ID))
    # DISCRIMINATION: the mapping refuses to manufacture 'scheduled'. A caller who says
    # trigger=scheduled gets UNKNOWN; only the rule's own payload shape yields scheduled.
    if trig == "manual" and tok.get("trigger") == "manual":
        ok("both ends of the carrier agree, so this is not a clock inference")


# --------------------------------------------------------------------------- (d)
def arm_d(s3, report):
    print("\n(d) GROUP A per device, and GROUP B with its grain disclosed")
    strata = report.get("stages") or report.get("strata") or []
    by_name = {}
    for s in strata:
        if isinstance(s, dict):
            n = s.get("name") or s.get("id") or s.get("group")
            if n:
                by_name[str(n)] = s
    print("      DENOMINATOR: %d stratum/stage row(s); names: %s"
          % (len(strata), ", ".join(sorted(by_name)) or "(none)"))

    a = by_name.get("A_propagation")
    if not a:
        fail("d", "no A_propagation stratum in the served report")
    else:
        print("      A status     : %s" % a.get("status"))
        den = str(a.get("denominator") or "")
        print("      A denominator: %s" % den[:400])
        if a.get("status") == "OK":
            ok("group A renders OK from the seam")
        else:
            fail("d", "group A status is %r" % a.get("status"))
        if "laptop:" in den:
            ok("laptop is present BY NAME in the per-device composition")
        else:
            fail("d", "laptop is not named in group A's denominator")
        if "git_head" in den:
            ok("each device's vintage/head is disclosed in the denominator")
        if "SILENT" in den.upper() or "OUT-OF-CORPUS" in den.upper():
            ok("NEGATIVE ARM: a non-reporting device reads SILENT / OUT-OF-CORPUS, so a green here "
               "discriminates")
        else:
            fail("d", "no device reads SILENT/OUT-OF-CORPUS -- the negative arm did not fire")

    b = by_name.get("B_coevolution") or by_name.get("B_cochange")
    if not b:
        cand = [k for k in by_name if k.startswith("B")]
        b = by_name.get(cand[0]) if cand else None
    if not b:
        fail("d", "no group B stratum in the served report")
        return
    bden = str(b.get("denominator") or "")
    print("      B status     : %s" % b.get("status"))
    print("      B denominator: %s" % bden[:300])
    if "grain=file-pair" in bden or "file-pair" in bden:
        ok("group B discloses its grain (file-pair, NOT resource-grain)")
    else:
        fail("d", "group B does not disclose its grain")
    served_rows = len(b.get("rows") or [])
    print("      B rows in report : %d" % served_rows)
    art = json.loads(s3.get_object(Bucket=BUCKET,
                                   Key="outset/comp_fedobs_coevolution.json")["Body"].read()
                     .decode("utf-8"))
    indep = len(art.get("rows") or [])
    sig = ((art.get("signals") or {}).get("coevolution") or {}).get("row_count")
    print("      INDEPENDENT count from the seam artifact: rows=%d  signals.row_count=%s"
          % (indep, sig))
    if served_rows == 0:
        fail("d", "group B renders 0 rows")
    elif indep and served_rows != indep:
        fail("d", "served %d rows but the artifact holds %d" % (served_rows, indep))
    else:
        ok("group B row count %d is non-zero and equals an INDEPENDENT count of the artifact"
           % served_rows)


# --------------------------------------------------------------------------- (e)
def arm_e(s3):
    print("\n(e) THE PROTECTED RECORD -- the manual day overwrote nothing")
    print("      Read as THREE checks; see the module docstring for why not the literal wording.")
    for key, spec in PINS.items():
        resp = s3.list_object_versions(Bucket=BUCKET, Prefix=key)
        vs = [v for v in resp.get("Versions", []) if v["Key"] == key]
        ids = {v["VersionId"] for v in vs}
        latest = [v["VersionId"] for v in vs if v["IsLatest"]]
        print("      %s" % key)
        print("        DENOMINATOR %d version(s) (expected %d) | IsLatest %s (expected %s)"
              % (len(vs), spec["versions"], latest, [spec["latest"]]))
        if len(vs) != spec["versions"]:
            fail("e", "%s has %d versions, expected %d -- the manual day WROTE to a 09-09 key"
                 % (key, len(vs), spec["versions"]))
        if latest != [spec["latest"]]:
            fail("e", "%s IsLatest is %s, expected %s" % (key, latest, spec["latest"]))
        missing = [v for v in spec["all"] if v not in ids]
        if missing:
            fail("e", "%s is missing pinned version(s) %s" % (key, missing))
    if not [f for f in FAILS if f.startswith("e:")]:
        ok("all three 09-09 keys unchanged: denominators held, IsLatest held, every pin retrievable")


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
    print("\n(g) THE 13:00Z CONFIRMATION -- read IF PRESENT, never waited for")
    try:
        vs = s3.list_object_versions(Bucket=BUCKET, Prefix=REPORT_KEY).get("Versions", [])
    except Exception as exc:                                                 # noqa: BLE001
        print("      unreadable: %s" % type(exc).__name__)
        return
    vs = [v for v in vs if v["Key"] == REPORT_KEY]
    print("      DENOMINATOR: %d version(s) of %s" % (len(vs), REPORT_KEY))
    if len(vs) < 2:
        print("      NOT-PRESENT: only the manual run's version exists. The 13:00Z fire has not "
              "run yet; this is CONFIRMATION and is never a gate, so the arm does not fail.")
        return
    newest = sorted(vs, key=lambda v: v["LastModified"])[-1]
    body = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY,
                         VersionId=newest["VersionId"])["Body"].read()
    rb = (json.loads(body.decode("utf-8")).get("run_bundle") or {})
    print("      newest version %s @%s trigger=%r"
          % (newest["VersionId"], newest["LastModified"], rb.get("trigger")))
    if rb.get("trigger") == "scheduled":
        ok("the 13:00Z fire is present and reads scheduled -- confirmation recorded")
    else:
        print("      the newest version reads trigger=%r; recorded, not graded" % rb.get("trigger"))


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

    try:
        obj = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY)
    except Exception as exc:                                                 # noqa: BLE001
        print("\nBLOCKED: the served report %s is not readable (%s). Every remaining arm reads it."
              % (REPORT_KEY, type(exc).__name__))
        FAILS.append("report: %s unreadable" % REPORT_KEY)
        print("\nFAILED -- %d arm failure(s)" % len(FAILS))
        return 1
    report = json.loads(obj["Body"].read().decode("utf-8"))
    bundle = report.get("run_bundle") or {}
    print("\n      served report VersionId: %s  LastModified: %s"
          % (obj.get("VersionId"), obj["LastModified"].astimezone(timezone.utc)
             .strftime("%Y-%m-%dT%H:%M:%SZ")))

    arm_b(s3, cb, bundle)
    arm_c(s3, bundle)
    arm_d(s3, report)
    arm_e(s3)
    arm_f(ec2)
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
