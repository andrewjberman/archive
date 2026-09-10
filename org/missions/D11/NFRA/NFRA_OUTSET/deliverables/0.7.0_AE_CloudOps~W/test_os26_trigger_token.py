"""O26-AC1 -- THE TRIGGER TOKEN, proved END TO END on the real plane.

Prints OS26-TRIGGER-TOKEN-CARRIED only when every arm passes.

THE FUNCTION UNDER TEST IS THE SERVED ONE, NOT THE REPO'S. Arm (b) exercises
`_trigger_token_read` by importing it out of the object the host actually pulls
(`s3://opal-estate-report/code/estate_report_runner.py`, downloaded at run time), not out of the
worktree. A battery that imported the checkout would grade the code this seat can see rather than
the code the estate runs, and arm (d) -- which proves those two are byte-equal -- would then be
verifying a premise the battery had already assumed. Testing the served bytes makes (d) an
independent check instead of a circular one.

WHAT THIS BATTERY REFUSES TO DO:

  1. IT NEVER INFERS THE TRIGGER FROM A CLOCK. The face is explicit: run_id is matched against the
     TOKEN THE ORCHESTRATOR WROTE FOR THAT INVOKE, "never inferred from started_at". The token key
     is overwritten by every invoke, so the manual run's token is fetched BY VersionId.

  2. IT NEVER WRITES A SERVED KEY TO MAKE A NEGATIVE ARM. Both negative arms in (b) are produced by
     pointing the real function at a key that does not exist and by supplying a boot instant --
     no put-object, no delete, nothing on the data plane. PRD R-5 (NEVER-AUTO-DELETE) is absolute
     and a battery that had to mutate served state to prove a negative would be trading a real
     artifact for a test result.

  3. IT DOES NOT USE simulate-principal-policy FOR ARM (c). That instrument has four independent
     false-deny modes (a conditioned statement with no context entries, a batched multi-ARN call,
     an unvalidated action name, and a wrong-grain resource ARN -- the last one measured at this
     seat as NFRA_OUTSET-S3). The applied Resource LIST is read directly instead and matched with
     a local ARN matcher that carries its own positive control, so the negative arm cannot be an
     artefact of the instrument.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-26). 2026-09-10.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

BUCKET = "opal-estate-report"
CODE_KEY = "code/estate_report_runner.py"
TOKEN_KEY = "config/last-trigger.json"
REPO_RUNNER = "infra/aws/ec2/estate-report-runner/estate_report_runner.py"

RUNNER_ROLE = "estate-report-runner-role"
RUNNER_POLICY = "estate-report-runner"
ORCH_ROLE = "estate-report-orchestrator-role"
ORCH_POLICY = "estate-report-orchestrator"

# ARM (a): the manual served day and the token written for THAT invoke.
REPORT_KEY = "daily/2026/09/09/estate-report-2026-09-09.json"
POS_REPORT_VERSION = os.environ.get("OS24_REPORT_VERSION", "F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw")
POS_TOKEN_VERSION = os.environ.get("OS24_TOKEN_VERSION", "QRHqSjmNPdImTp_rmka.gCcoK1MLWfDR")

# A key that certainly does not exist, used ONLY as a read target. Nothing is ever written here.
ABSENT_TOKEN_KEY = "config/last-trigger-NO-SUCH-KEY-os26-battery.json"

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=os.path.dirname(os.path.abspath(__file__)),
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print("BLOCKED: not inside a git working tree")
        sys.exit(1)
    return out.stdout.strip()


ROOT = repo_root()


def load_served_runner(s3, dest):
    """Download the SERVED runner and import it. Returns (module, bytes, version_id, etag)."""
    r = s3.get_object(Bucket=BUCKET, Key=CODE_KEY)
    raw = r["Body"].read()
    with open(dest, "wb") as fh:
        fh.write(raw)
    # The runner reads six variables at import. They are supplied here so the MODULE loads; none
    # of them is used by the function under test, and the bucket is the real one.
    os.environ.setdefault("ESTATE_REPORT_BUCKET", BUCKET)
    for k in ("ESTATE_GITHUB_SECRET_ID", "ESTATE_KIMI_SECRET_ID", "ESTATE_KIMI_MODEL"):
        os.environ.setdefault(k, "battery-placeholder")
    os.environ.setdefault("ESTATE_KIMI_URL", "http://placeholder.invalid")
    os.environ.setdefault("ESTATE_REPO_URL", "http://placeholder.invalid")
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    spec = importlib.util.spec_from_file_location("served_runner", dest)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, raw, r["VersionId"], r["ETag"].strip('"')


def arn_matches(pattern: str, target: str) -> bool:
    """IAM resource-ARN matching with `*` and `?`. Written locally rather than asked of
    simulate-principal-policy, whose four false-deny modes would make a negative arm
    indistinguishable from an instrument failure. Its own positive control runs in arm (c)."""
    import re as _re
    rx = "^" + "".join(".*" if c == "*" else ("." if c == "?" else _re.escape(c))
                       for c in pattern) + "$"
    return _re.match(rx, target) is not None


def policy_statements(iam, role, policy):
    doc = iam.get_role_policy(RoleName=role, PolicyName=policy)["PolicyDocument"]
    st = doc.get("Statement")
    return st if isinstance(st, list) else [st]


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# --------------------------------------------------------------------------- (a)
def arm_a(s3):
    print("\n(a) THE POSITIVE ARM: the served report's run_id EQUALS the token written for that invoke")
    rep = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY, VersionId=POS_REPORT_VERSION)
    doc = json.loads(rep["Body"].read().decode("utf-8"))
    rb = doc.get("run_bundle") or {}
    print("      report %s @%s..  %s" % (REPORT_KEY, POS_REPORT_VERSION[:12],
                                         rep["LastModified"].astimezone(timezone.utc)
                                         .strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("      run_bundle.trigger = %r   run_bundle.run_id = %r"
          % (rb.get("trigger"), rb.get("run_id")))
    if rb.get("trigger") != "manual":
        fail("a", "the served report's trigger is %r, expected 'manual'" % rb.get("trigger"))
        return
    if not rb.get("run_id"):
        fail("a", "the served report carries no run_bundle.run_id")
        return

    # head-object FIRST (the face names it), so the token version is cited with its own vintage
    # before its body is read.
    h = s3.head_object(Bucket=BUCKET, Key=TOKEN_KEY, VersionId=POS_TOKEN_VERSION)
    tok_raw = s3.get_object(Bucket=BUCKET, Key=TOKEN_KEY,
                            VersionId=POS_TOKEN_VERSION)["Body"].read()
    tok = json.loads(tok_raw.decode("utf-8"))
    print("      token  %s @%s..  %d B  LastModified %s"
          % (TOKEN_KEY, POS_TOKEN_VERSION[:12], h["ContentLength"],
             h["LastModified"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("      token.trigger = %r   token.run_id = %r   token.invoked_at = %r"
          % (tok.get("trigger"), tok.get("run_id"), tok.get("invoked_at")))

    # THE TOKEN KEY IS OVERWRITTEN BY EVERY INVOKE, so `latest` is a LATER run's token. Reading it
    # here would compare this run's report against another run's token and could only ever fail --
    # or, worse, pass by coincidence if the ids were ever reused.
    if tok.get("run_id") != rb.get("run_id"):
        fail("a", "token run_id %r != report run_bundle.run_id %r"
             % (tok.get("run_id"), rb.get("run_id")))
        return
    if tok.get("trigger") != "manual":
        fail("a", "token trigger is %r, expected 'manual'" % tok.get("trigger"))
        return
    ok("THE CARRIER IS PROVEN END TO END: the orchestrator wrote run_id %s at %s and the RUNNER "
       "stamped that same id into the served report -- matched on the ID, never on the clock"
       % (tok.get("run_id"), tok.get("invoked_at")))
    note("started_at on the report is %r and is NOT used by this arm" % rb.get("started_at"))


# --------------------------------------------------------------------------- (b)
def arm_b(mod, s3):
    print("\n(b) THE TWO NEGATIVE ARMS, on the SERVED function, against the REAL bucket")
    print("    no put-object, no delete, no served-key write of any kind (PRD R-5)")
    real_key = mod.OUTSET_TRIGGER_KEY
    loader = mod._outset_loader

    # --- the head-object control pair: 404 on the absent key beside 200 on the present one.
    def head_status(key):
        try:
            r = s3.head_object(Bucket=BUCKET, Key=key)
            return r["ResponseMetadata"]["HTTPStatusCode"]
        except Exception as exc:                                            # noqa: BLE001
            meta = getattr(exc, "response", None)
            if isinstance(meta, dict):
                return (meta.get("ResponseMetadata") or {}).get("HTTPStatusCode")
            return type(exc).__name__

    absent_status = head_status(ABSENT_TOKEN_KEY)
    present_status = head_status(real_key)
    print("      head-object %s -> %s" % (ABSENT_TOKEN_KEY, absent_status))
    print("      head-object %s -> %s   (the control: a uniformly failing call cannot read as a verdict)"
          % (real_key, present_status))
    if present_status != 200:
        fail("b", "the PRESENT key did not read 200 (%s) -- the absent-key read below cannot be "
                  "attributed to absence" % present_status)
        return
    if absent_status != 404:
        fail("b", "the absent key read %s, not 404" % absent_status)
        return
    ok("404 on the absent key beside 200 on the present one -- absence is measured, not assumed")

    fresh_boot = datetime.now(timezone.utc) - timedelta(days=3650)

    # --- NEGATIVE 1: the token key ABSENT.
    try:
        mod.OUTSET_TRIGGER_KEY = ABSENT_TOKEN_KEY
        trig, rid = mod._trigger_token_read(loader, fresh_boot)
    finally:
        mod.OUTSET_TRIGGER_KEY = real_key
    print("      ABSENT token   -> (%r, %r)" % (trig, rid))
    if trig != "UNKNOWN":
        fail("b", "an absent token returned %r, not UNKNOWN" % trig)
    else:
        ok("an ABSENT token reads UNKNOWN -- never 'scheduled', which would be a confident claim "
           "manufactured out of nothing")

    # --- NEGATIVE 2: a STALE token. The real, present token with a boot instant AFTER its
    # invoked_at. Nothing is written: the staleness is supplied by the caller's boot instant,
    # which is exactly the parameter the runner's own docstring says the caller supplies.
    tok = json.loads(loader("s3://%s/%s" % (BUCKET, real_key)))
    invoked = datetime.strptime(tok["invoked_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)
    stale_boot = invoked + timedelta(seconds=1)
    trig_s, rid_s = mod._trigger_token_read(loader, stale_boot)
    print("      STALE token    -> (%r, %r)   [token invoked_at %s, boot instant %s]"
          % (trig_s, rid_s, tok["invoked_at"],
             stale_boot.strftime("%Y-%m-%dT%H:%M:%SZ")))
    if trig_s != "UNKNOWN":
        fail("b", "a stale token returned %r, not UNKNOWN" % trig_s)
    else:
        ok("a STALE token reads UNKNOWN -- a token from an earlier invoke is not this run's")

    # --- THE POSITIVE CONTROL OF THE SAME FUNCTION. Without it, a function that returned UNKNOWN
    # unconditionally would pass both negative arms. This is the arm that makes them measurements.
    ok_boot = invoked - timedelta(seconds=1)
    trig_p, rid_p = mod._trigger_token_read(loader, ok_boot)
    print("      FRESH token    -> (%r, %r)   [boot instant %s, one second BEFORE invoked_at]"
          % (trig_p, rid_p, ok_boot.strftime("%Y-%m-%dT%H:%M:%SZ")))
    if trig_p == "UNKNOWN":
        fail("b", "the positive control also read UNKNOWN -- the function may be a constant, so "
                  "neither negative arm above is a measurement")
    elif trig_p != tok.get("trigger"):
        fail("b", "the positive control returned %r but the token says %r"
             % (trig_p, tok.get("trigger")))
    else:
        ok("the SAME function returns %r on a fresh token -- it is not a constant, so both "
           "negative arms are measurements" % trig_p)


# --------------------------------------------------------------------------- (c)
def arm_c(iam):
    print("\n(c) THE GRANTS ON THE APPLIED PLANE, exact-key, with a sibling-key negative control")
    sibling = "arn:aws:s3:::%s/config/some-other-object.json" % BUCKET
    token_arn = "arn:aws:s3:::%s/%s" % (BUCKET, TOKEN_KEY)

    for label, role, policy, action, expect_exact in (
            ("ORCHESTRATOR Put", ORCH_ROLE, ORCH_POLICY, "s3:PutObject", True),
            ("RUNNER Get", RUNNER_ROLE, RUNNER_POLICY, "s3:GetObject", False)):
        sts = [s for s in policy_statements(iam, role, policy)
               if s.get("Effect") == "Allow" and action in as_list(s.get("Action"))]
        res = [r for s in sts for r in as_list(s.get("Resource"))]
        hit = [r for r in res if arn_matches(r, token_arn)]
        sib = [r for r in res if arn_matches(r, sibling)]
        print("      %-18s %s/%s  statements=%d  resources=%d" % (label, role, policy,
                                                                  len(sts), len(res)))
        print("        resources: %s" % ", ".join(res))
        print("        matches the token key : %s" % (hit or "NONE"))
        print("        matches a SIBLING key : %s   <- must be NONE" % (sib or "NONE"))
        if not hit:
            fail("c", "%s does not reach %s on the applied plane" % (label, token_arn))
            continue
        if sib:
            fail("c", "%s ALSO reaches a sibling key under config/ via %s -- the grant is wider "
                      "than the one key" % (label, sib))
            continue
        if expect_exact and res != [token_arn]:
            fail("c", "%s's Resource list is %r, not exactly [%s]" % (label, res, token_arn))
            continue
        ok("%s reaches the token key and NOT a sibling under config/ (%d resource(s) declared)"
           % (label, len(res)))

    # THE MATCHER'S OWN POSITIVE CONTROL. The sibling read above is a NEGATIVE; if arn_matches
    # returned False for everything, that negative would pass for the wrong reason.
    if not arn_matches("arn:aws:s3:::%s/config/*" % BUCKET, sibling):
        fail("c", "the ARN matcher fails to match a wildcard that plainly covers the sibling -- "
                  "the negative control above is an artefact of the matcher, not a fact")
    else:
        ok("matcher positive control: a `config/*` wildcard DOES match the sibling key, so the "
           "NONE above is a property of the grant and not of the matcher")


# --------------------------------------------------------------------------- (d)
def arm_d(served_raw, served_etag, served_version):
    print("\n(d) THE SERVED RUNNER == THE BUILD INPUT (the OS-s-19 control)")
    out = subprocess.run(["git", "-C", ROOT, "show", "HEAD:%s" % REPO_RUNNER],
                         capture_output=True, timeout=180)
    if out.returncode != 0:
        fail("d", "git show HEAD:%s failed rc=%d" % (REPO_RUNNER, out.returncode))
        return
    head = out.stdout
    served_md5 = hashlib.md5(served_raw).hexdigest()
    head_md5 = hashlib.md5(head).hexdigest()
    print("      served  %d B  VersionId %s..  ETag %s" % (len(served_raw), served_version[:12],
                                                           served_etag))
    print("      HEAD    %d B  md5  %s" % (len(head), head_md5))
    print("      served sha256 %s" % hashlib.sha256(served_raw).hexdigest()[:32])
    print("      HEAD   sha256 %s" % hashlib.sha256(head).hexdigest()[:32])
    if served_etag != head_md5:
        fail("d", "served ETag %s != md5 of the HEAD blob %s" % (served_etag, head_md5))
        return
    if served_md5 != head_md5:
        fail("d", "served bytes md5 %s != HEAD md5 %s" % (served_md5, head_md5))
        return
    ok("the served ETag EQUALS md5 of the HEAD blob, and the re-downloaded bytes agree")

    # THE OS-s-19 CONTROL: the comparator must be able to say MISMATCH. One bit flipped, length
    # held fixed, so a length check cannot be what catches it.
    mutant = bytearray(served_raw)
    mutant[100] ^= 0x01
    if len(bytes(mutant)) != len(head):
        fail("d", "the mutant changed length; it is not a content-only control")
        return
    if hashlib.md5(bytes(mutant)).hexdigest() == head_md5:
        fail("d", "a one-bit mutant still compares EQUAL -- the comparator is a constant")
        return
    ok("NEGATIVE CONTROL: one bit flipped at offset 100 with the length held fixed -> MISMATCH. "
       "The match above is a measurement.")


# --------------------------------------------------------------------------- (e)
def arm_e(s3):
    print("\n(e) CONFIRMATION, NEVER WAITED FOR: the 13:00Z scheduled fire")
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix="daily/%s/" % today)
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".json")]
    print("      daily/%s/ -> %d object(s), %d .json" % (today, r.get("KeyCount", 0), len(keys)))
    if not keys:
        note("NOT-YET-FIRED. Recorded and NOT waited for; the verdict comes from (a)-(d).")
        return
    doc = json.loads(s3.get_object(Bucket=BUCKET, Key=keys[0])["Body"].read().decode("utf-8"))
    rb = doc.get("run_bundle") or {}
    print("      %s  run_bundle.trigger = %r  run_id = %r"
          % (keys[0], rb.get("trigger"), rb.get("run_id")))
    if rb.get("trigger") != "scheduled":
        fail("e", "the scheduled fire's report carries trigger %r, expected 'scheduled'"
             % rb.get("trigger"))
        return
    ok("the scheduled fire reads trigger='scheduled' -- the carrier tells the two apart on the "
       "ARTIFACT, which is the whole point of the cell")


def main():
    print("=" * 78)
    print("O26-AC1 -- THE TRIGGER TOKEN, END TO END")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("repo   %s" % ROOT)
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s). Every arm here is world-facing." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    iam = boto3.client("iam", region_name="us-east-1")

    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".served_runner_os26.py")
    try:
        mod, raw, vid, etag = load_served_runner(s3, dest)
    except Exception as exc:                                                # noqa: BLE001
        print("BLOCKED: could not load the SERVED runner (%s: %s)" % (type(exc).__name__, exc))
        return 1
    print("served runner imported from %s @%s (%d B)" % (CODE_KEY, vid[:12], len(raw)))

    arm_a(s3)
    arm_b(mod, s3)
    arm_c(iam)
    arm_d(raw, etag, vid)
    arm_e(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS26-TRIGGER-TOKEN-CARRIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
