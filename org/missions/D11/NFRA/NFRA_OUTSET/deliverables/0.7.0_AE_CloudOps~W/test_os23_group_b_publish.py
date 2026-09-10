"""O23-AC1 -- THE GROUP-B PUBLISH, read on a SERVED DAY.

Prints OS23-GROUP-B-PUBLISHED only when every arm holds.

⛔ TWO HALVES CANNOT BE READ BEFORE 2026-09-11 13:00Z, AND THE BATTERY SAYS SO RATHER THAN
SKIPPING THEM. The GRAIN TAG this criterion quotes verbatim (`[grain=file-pair, NOT
resource-grain]`) is appended to the stratum's VINTAGE at `estate_report_runner.py:1425`, and the
stratum's row count lives in its DENOMINATOR. NEITHER string reached any served artifact until
TO-OS-s-27 serialized them -- measured on four artifacts with a positive control (row S40,
corrected on the grain half by S41, which is why the remedy covers both strings). OS-s-27 is
TERMINAL and DEPLOYED and its bound forbids backfilling, so the first artifact carrying them is
tomorrow's scheduled fire.

WHAT THAT LEAVES READABLE TODAY, AND IT IS MOST OF THE CRITERION: that group B renders from the
seam artifact at all, its vintage and ordering, that the artifact is DERIVED rather than copied,
the ROSTER-VERSUS-GRANT arm in full, and the EXERCISED reading of the runner's own identity. Only
the two string-quoting halves wait.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-23). 2026-09-10.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
CODE_KEY = "code/estate_report_runner.py"
SEAM_PREFIX = "s3://opal-estate-report/outset"
FEDOBS_KEY = "outset/comp_fedobs_coevolution.json"

REPORT_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
REPORT_VERSION = "kIo74Zug6entwLkwzLOw5TYMktp7RJ1R"
MANUAL_REPORT_KEY = "daily/2026/09/09/estate-report-2026-09-09.json"
MANUAL_REPORT_VERSION = "F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw"

RUNNER_ROLE = "estate-report-runner-role"
RUNNER_POLICY = "estate-report-runner"
CEILING_H = 26.0
GRAIN_TAG = "[grain="

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def load_served_runner(s3, dest):
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
    spec = importlib.util.spec_from_file_location("os23_served", dest)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, raw


def arn_matches(pattern: str, target: str) -> bool:
    """IAM-style `*`/`?` matching, written locally. simulate-principal-policy is NOT used for the
    grant arms: four independent false-deny modes, and against a narrowly scoped principal -- which
    this role is -- a false deny reads as a correct negative. Its own positive control runs below."""
    import re as _re
    rx = "^" + "".join(".*" if c == "*" else ("." if c == "?" else _re.escape(c))
                       for c in pattern) + "$"
    return _re.match(rx, target) is not None


# --------------------------------------------------------------------------- (a)
def arm_a(s3):
    print("\n(a) GROUP B RENDERS FROM THE SEAM ARTIFACT, WITH A NON-ZERO ROW COUNT")
    doc = json.loads(s3.get_object(Bucket=BUCKET, Key=REPORT_KEY,
                                   VersionId=REPORT_VERSION)["Body"].read().decode("utf-8"))
    b = ((doc.get("ai") or {}).get("groups") or {}).get("B") or {}
    print("      /ai/groups/B/stratum_status = %r  (unmeasured=%s, candidates_raw=%s, kept=%s)"
          % (b.get("stratum_status"), b.get("unmeasured"), b.get("candidates_raw"),
             b.get("candidates_kept")))
    if b.get("stratum_status") != "OK":
        fail("a", "group B reads %r on the served day" % b.get("stratum_status"))
        return doc, None
    cit = ""
    for p in ((doc.get("ai") or {}).get("proposals") or []):
        c = p.get("tool_row_cited")
        if isinstance(c, str) and "B_relationships@" in c:
            cit = c
            break
    print("      served citation: %s" % cit[:200])
    if "comp-fedobs" not in cit:
        fail("a", "the served citation does not name comp-fedobs, so group B is not shown reading "
                  "the seam artifact")
        return doc, None
    ok("group B reads OK and its served citation names comp-fedobs coevolution -- it renders FROM "
       "the seam artifact")

    # THE INDEPENDENT COUNT: the artifact re-downloaded and counted by a SECOND reader, never the
    # report's own number. The version selected is the one this run read -- the latest preceding
    # its start -- for the reason row NFRA_OUTSET-S44 records.
    start = datetime.fromisoformat(str((doc.get("run_bundle") or {}).get("started_at")))
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    vs = [v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=FEDOBS_KEY).get("Versions", [])
          if v["Key"] == FEDOBS_KEY and v["LastModified"].astimezone(timezone.utc) < start]
    if not vs:
        fail("a", "no version of %s predates the run start" % FEDOBS_KEY)
        return doc, None
    v = max(vs, key=lambda x: x["LastModified"])
    art = json.loads(s3.get_object(Bucket=BUCKET, Key=FEDOBS_KEY,
                                   VersionId=v["VersionId"])["Body"].read().decode("utf-8"))
    rows = len(art.get("rows") or [])
    # ⛔ READ THE DECLARED COUNT WHERE IT ACTUALLY LIVES. An earlier version of this arm looked for
    # `summary.row_count`, which this artifact does not have, got None, skipped its own comparison,
    # and then PRINTED "equal to the artifact's own declared row_count" -- a false statement inside
    # a PASSING arm. An absent field must never be read as agreement.
    scal = ((art.get("denominators") or {}).get("tool_scalars") or {})
    declared = art.get("row_count")
    if declared is None:
        declared = scal.get("row_count")
    if declared is None:
        declared = ((art.get("summary") or {}).get("row_count"))
    print("      independent read of %s.. (%s): rows counted by a SECOND reader = %d"
          % (v["VersionId"][:20], v["LastModified"].astimezone(timezone.utc)
             .strftime("%Y-%m-%dT%H:%M:%SZ"), rows))
    print("      the artifact's OWN declared row count: %s" % (declared if declared is not None
                                                               else "ABSENT (no such field)"))
    if rows == 0:
        fail("a", "the independent count is ZERO -- a non-zero row count is required")
        return doc, art
    if declared is None:
        ok("independent count is %d rows and NON-ZERO. The artifact declares no row-count field, "
           "so NO equality is claimed -- the second reader's count stands alone and is stated as "
           "such rather than as agreement with a value that is not there." % rows)
        return doc, art
    if declared != rows:
        fail("a", "the artifact's own declared row count (%s) disagrees with a second reader's "
                  "count (%d) -- W2-S21's lesson" % (declared, rows))
        return doc, art
    ok("independent count is %d rows, non-zero, and EQUAL to the artifact's own declared count -- "
       "counted by a second reader, never taken from the report" % rows)
    return doc, art


# --------------------------------------------------------------------------- (b)
def arm_b(doc, art, s3):
    print("\n(b) THE ARTIFACT'S VINTAGE: inside the ceiling AND later than the fedobs nightly")
    if art is None:
        fail("b", "no artifact from arm (a)")
        return
    stamp = (art.get("vintage") or {}).get("answer_produced_utc")
    produced = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    start = datetime.fromisoformat(str((doc.get("run_bundle") or {}).get("started_at")))
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    age = (start - produced).total_seconds() / 3600.0
    nightly = produced.replace(hour=4, minute=30, second=0, microsecond=0)
    print("      artifact produced %s ; run started %s ; age at the run %.2f h (ceiling %.1f h)"
          % (stamp, start.strftime("%Y-%m-%dT%H:%M:%SZ"), age, CEILING_H))
    print("      that day's fedobs nightly mark: %s" % nightly.strftime("%Y-%m-%dT%H:%M:%SZ"))
    if age < 0 or age > CEILING_H:
        fail("b", "the artifact's age at the run is %.2f h, outside the 0..%.1f h window"
             % (age, CEILING_H))
        return
    if produced <= nightly:
        fail("b", "the artifact was produced %s, NOT later than that day's 04:30Z fedobs nightly"
             % stamp)
        return
    ok("produced %s -- inside the %.1f h ceiling at the run and LATER than the 04:30Z nightly, so "
       "it carries that day's CSE log rather than the previous one" % (stamp, CEILING_H))


# --------------------------------------------------------------------------- (c)
def arm_c(mod):
    print("\n(c) THE NEGATIVE ARMS -- a disabled publish reads FAILED, never the stand-in")
    now = datetime.now(timezone.utc)

    def absent_loader(src):
        raise FileNotFoundError(src)

    st = mod._stratum_cochange(".", now, {}, "PIN", prefix=SEAM_PREFIX, loader=absent_loader)
    print("      every declared source ABSENT -> status=%r" % st["status"])
    print("      error: %s" % (st.get("instrument_error") or "")[:220])
    if st["status"] != "INSTRUMENT_FAILED":
        fail("c", "a configured prefix with every source absent read %r, not INSTRUMENT_FAILED"
             % st["status"])
        return
    if st["rows"]:
        fail("c", "the FAILED stratum carried %d rows -- it fell through to the host stand-in"
             % len(st["rows"]))
        return
    ok("a configured-and-empty prefix reads INSTRUMENT_FAILED with ZERO rows -- it never quietly "
       "computes the host stand-in instead")

    # THE POSITIVE CONTROL of the same function: with a healthy source it must NOT read FAILED, or
    # the arm above is a constant.
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    good = json.dumps({"seam": mod.SEAM_TAG, "answer_state": "OK",
                       "vintage": {"answer_produced_utc": stamp},
                       "rows": [{"a": 1}, {"a": 2}],
                       "denominators": {"grain": "file-pair"}})

    def good_loader(src):
        if src.endswith(mod.OUTSET_FEDOBS_KEY):
            return good
        raise FileNotFoundError(src)

    st2 = mod._stratum_cochange(".", now, {}, "PIN", prefix=SEAM_PREFIX, loader=good_loader)
    print("      a healthy source present -> status=%r, %d row(s)" % (st2["status"],
                                                                      len(st2["rows"])))
    if st2["status"] != "OK":
        fail("c", "the positive control ALSO read %r -- the FAILED state is a constant and the "
                  "negative arm above is not a measurement" % st2["status"])
        return
    ok("the SAME function reads OK on a healthy source, so the FAILED state discriminates")

    # OUT-OF-CORPUS on an empty CSE log: a zero over an empty population is refused, not QUIET.
    empty = json.dumps({"seam": mod.SEAM_TAG, "answer_state": "PRESENT_WITH_ZERO_RESULTS",
                        "vintage": {"answer_produced_utc": stamp}, "rows": [],
                        "summary": {"cse_log_total": 0, "row_count": 0}})

    def empty_loader(src):
        if src.endswith(mod.OUTSET_FEDOBS_KEY):
            return empty
        raise FileNotFoundError(src)

    st3 = mod._stratum_cochange(".", now, {}, "PIN", prefix=SEAM_PREFIX, loader=empty_loader)
    den3 = st3["denominator"]
    print("      an EMPTY CSE log -> status=%r" % st3["status"])
    print("      denominator carries cse_log_total: %s" % ("cse_log_total" in den3))
    note("the seam's declared domain maps PRESENT_WITH_ZERO_RESULTS to OK, so a MEASURED zero is "
         "rendered as a RESULT with its denominator travelling -- the artifact's own "
         "cse_log_total=0 is what tells a reader the population was empty. This arm RECORDS that "
         "rather than asserting a state the runner does not emit.")


# --------------------------------------------------------------------------- (d)
def arm_d(art, s3):
    print("\n(d) THE ARTIFACT IS DERIVED, NOT A BYTE-COPY OF THE NIGHTLY'S SNAPSHOT")
    if art is None:
        fail("d", "no artifact from arm (a)")
        return
    keys = sorted(art.keys())
    print("      seam artifact top-level keys: %s" % keys)
    summary = art.get("summary") or {}
    print("      summary keys: %s" % sorted(summary.keys()))
    scal = ((art.get("denominators") or {}).get("tool_scalars") or {})
    print("      tool_scalars: %s" % sorted(scal.keys()))
    # THE DERIVATION IS NAMED ON THE ARTIFACT: its own recipe/producer fields must say comp-fedobs
    # coevolution and it must carry a source table, which a byte-copy of a snapshot would not.
    blob = json.dumps(art)
    named = "coevolution" in blob or "co-evolution" in blob
    src_table = scal.get("source_table")
    print("      names its own derivation: %s   source_table=%r" % (named, src_table))
    if not named:
        fail("d", "the artifact does not name comp-fedobs co-evolution as its producer -- it "
                  "cannot be distinguished from a copied snapshot")
        return
    if not src_table:
        fail("d", "the artifact declares no source_table, so its derivation from the CSE log is "
                  "not stated on the artifact")
        return
    # AND THE SCHEMA DIFFERS FROM A SNAPSHOT: it carries a ROW COUNT over PAIRS against a CSE
    # TOTAL, two different populations. A byte-copy would carry one.
    # THE TWO POPULATIONS, read where they actually live: the PAIR count is the artifact's own
    # rows, and the CSE total is a tool scalar. An earlier version looked for both under `summary`,
    # which this artifact does not carry at all, and failed for the wrong reason.
    rc = len(art.get("rows") or [])
    cse = scal.get("cse_log_total")
    if cse is None:
        cse = (summary or {}).get("cse_log_total")
    print("      row_count (PAIRS, counted) = %s over cse_log_total (CSEs, declared) = %s"
          % (rc, cse))
    if not rc or cse is None or rc == cse:
        fail("d", "the artifact does not carry two distinct populations (pairs=%r, cse_log_total="
                  "%r), so it is not shown to be DERIVED rather than copied" % (rc, cse))
        return
    ok("the artifact names its own derivation (comp-fedobs co-evolution over %s) and carries "
       "%s pairs over %s CSEs -- two populations at different grains, which a byte-copy of the "
       "snapshot could not be" % (src_table, rc, cse))


# --------------------------------------------------------------------------- (e)
def arm_e(mod, iam):
    print("\n(e) THE ROSTER-VERSUS-GRANT ARM -- the cost this seat named, made to FAIL")
    stmts = iam.get_role_policy(RoleName=RUNNER_ROLE,
                                PolicyName=RUNNER_POLICY)["PolicyDocument"]["Statement"]
    cond = []
    for s in stmts if isinstance(stmts, list) else [stmts]:
        if s.get("Sid") == "ListOwnPrefixes":
            c = ((s.get("Condition") or {}).get("StringLike") or {}).get("s3:prefix")
            cond = c if isinstance(c, list) else ([c] if c else [])
    print("      APPLIED Condition (iam get-role-policy, NOT the .tf source): %d value(s)"
          % len(cond))
    for c in cond:
        print("        %s" % c)

    def keys_the_code_can_read(devices=None):
        """FROM THE CODE'S OWN CONSTANTS AT RUN TIME, never a list retyped into this battery."""
        devs = tuple(devices) if devices is not None else mod.OUTSET_DEVICES
        out = ["%s/%s" % (d, mod.OUTSET_DRIFT_KEY) for d in devs]
        out += [k for k, _g, _n in mod.OUTSET_GROUP_B_SOURCES]
        out += ["comp_heat_freshness_tools.json"]
        return sorted(set(out))

    def check(devices, label):
        code_keys = keys_the_code_can_read(devices)
        prefixed = ["outset/%s" % k for k in code_keys]
        admitted = [c for c in cond if not c.endswith("/*")]
        wild = [c for c in cond if c.endswith("/*")]
        matched = [k for k in prefixed if any(arn_matches(c, k) for c in cond)]
        missing = [k for k in prefixed if k not in matched]
        over = [c for c in admitted if not any(arn_matches(c, k) for k in prefixed)]
        print("      [%s] DENOMINATOR BOTH WAYS: keys the CODE can read = %d ; values the GRANT "
              "admits = %d (%d exact, %d wildcard)"
              % (label, len(prefixed), len(cond), len(admitted), len(wild)))
        print("        intersection            : %d" % len(matched))
        print("        code reads, grant OMITS  : %s" % (missing or "NONE"))
        print("        grant admits, no code path: %s" % (over or "NONE"))
        return missing, over

    missing, over = check(None, "roster at its DEFAULT")
    if missing:
        fail("e", "%d key(s) the consumer can read are NOT matched by the applied Condition: %s"
             % (len(missing), missing))
        return
    if over:
        note("OVER-GRANT, named rather than failed: %s. These are the prefixes OS-s-18 granted for "
             "the report's own keys (daily/manifest/code), not seam keys -- they are outside this "
             "cell's subject and are recorded here so the asymmetry is visible." % over)
    ok("every key the code can read at the DEFAULT roster is matched by the applied Condition; "
       "0 omitted")

    # THE PLANTED EXTRA DEVICE, WHICH MUST FAIL. A control that cannot fail on the very drift it
    # exists to catch is a constant. `ESTATE_OUTSET_DEVICES` is env-overridable and the roster is a
    # DECLARED DOMAIN, so the day a fourth device is added its key falls outside the Condition and
    # NOTHING ELSE would fail.
    planted = tuple(list(mod.OUTSET_DEVICES) + ["_os23_planted_device"])
    pmissing, _ = check(planted, "roster with a PLANTED EXTRA DEVICE")
    if not pmissing:
        fail("e", "the planted extra device's key IS matched by the Condition -- this arm cannot "
                  "catch the drift it exists for, so the pass above is a constant")
        return
    ok("the planted extra device's key %s is NOT matched by the applied Condition, so the arm "
       "FAILS on exactly the drift it exists to catch -- the control fires" % pmissing)

    # THE MATCHER'S OWN POSITIVE CONTROL.
    if not arn_matches("outset/*", "outset/_os23_planted_device/comp_heat_drift.json"):
        fail("e", "the matcher fails a wildcard that plainly covers the planted key -- the NONE "
                  "above is an artefact of the matcher, not a fact about the grant")
        return
    ok("matcher positive control: an `outset/*` wildcard DOES match the planted key, so the "
       "non-match is a property of the GRANT")


# --------------------------------------------------------------------------- (f)
def arm_f(s3):
    print("\n(f) APPLIED IS NOT EXERCISED -- the runner's OWN identity, read BEHAVIOURALLY")
    before = json.loads(s3.get_object(Bucket=BUCKET, Key=MANUAL_REPORT_KEY,
                                      VersionId=MANUAL_REPORT_VERSION)["Body"]
                        .read().decode("utf-8"))
    after = json.loads(s3.get_object(Bucket=BUCKET, Key=REPORT_KEY,
                                     VersionId=REPORT_VERSION)["Body"].read().decode("utf-8"))
    bb = ((before.get("ai") or {}).get("groups") or {}).get("B") or {}
    ba = ((after.get("ai") or {}).get("groups") or {}).get("B") or {}
    print("      BEFORE the grant (00:29:57Z run): group B = %r" % bb.get("stratum_status"))
    print("      AFTER  the grant (13:01:01Z run): group B = %r" % ba.get("stratum_status"))
    print("      the grant landed @a9972bf008 at 2026-09-10T02:43Z, between the two")
    if bb.get("stratum_status") != "INSTRUMENT_FAILED":
        fail("f", "the BEFORE run does not read INSTRUMENT_FAILED, so there is no difference "
                  "across the grant and the exercise is not shown")
        return
    if ba.get("stratum_status") != "OK":
        fail("f", "the AFTER run does not read OK -- the grant is not exercised")
        return
    ok("group B moved INSTRUMENT_FAILED -> OK across the grant. THE CHAIN ADVANCES ONLY ON "
       "absent=True, absent=True IS SET ONLY BY THE FileNotFoundError ARM, AND THAT ARM IS "
       "REACHABLE ONLY ON A 404 -- so this transition IS the runner's own identity receiving a 404 "
       "on a certainly-absent, newly-conditioned key. APPLIED AND EXERCISED.")
    note("the 200 POSITIVE CONTROL on the same identity in the same run is group A reading "
         "outset/laptop/comp_heat_drift.json successfully -- an EXISTING key under a conditioned "
         "prefix. A uniformly failing call could not have produced both readings.")
    note("WHAT THIS ARM CANNOT PRINT: the caller ARN. The runner does not emit it, and no session "
         "can assume estate-report-runner-role (its trust policy names only Service "
         "ec2.amazonaws.com -- measured, and the method was ratified by the issuer at 94896). The "
         "identity is established by WHICH CODE PATH RAN, which only that role's grant can reach.")


# --------------------------------------------------------------------------- (g)
def arm_g(s3):
    print("\n(g) THE GRAIN TAG, QUOTED VERBATIM -- and why it cannot be read today")
    doc = json.loads(s3.get_object(Bucket=BUCKET, Key=REPORT_KEY,
                                   VersionId=REPORT_VERSION)["Body"].read().decode("utf-8"))
    b = ((doc.get("ai") or {}).get("groups") or {}).get("B") or {}
    print("      ai.groups.B keys on THIS served artifact: %s" % sorted(b.keys()))
    if "stratum_vintage" not in b:
        fail("g", "NOT-YET-SERVED. The grain tag is appended to the stratum's VINTAGE at "
                  "estate_report_runner.py:1425 (row S41 corrected S40 on exactly this point), and "
                  "no served artifact carried that string until TO-OS-s-27 serialized it. OS-s-27 "
                  "is TERMINAL and DEPLOYED and backfills nothing by its own bound, so the FIRST "
                  "artifact carrying it is the 2026-09-11 13:00Z fire. No ad-hoc run is fired to "
                  "manufacture one: after 13:00Z a manual run REWRITES today's served keys, the "
                  "act that produced the S34 rollback.")
        note("what CAN be said today: the grain tag is present in the DEPLOYED runner and renders "
             "into the serialized vintage offline from the same inputs -- proven under O27-AC1 "
             "arms (b)-(d). What is unproven is the last hop, the tag appearing in a SERVED "
             "artifact, and that is not claimed.")
        return
    vin = b.get("stratum_vintage") or ""
    print("      stratum_vintage verbatim: %s" % vin)
    if GRAIN_TAG not in vin:
        fail("g", "the serialized vintage carries no %r tag" % GRAIN_TAG)
        return
    ok("the grain tag is read VERBATIM out of the served bytes: %s"
       % vin[vin.index(GRAIN_TAG):][:80])


def main():
    print("=" * 78)
    print("O23-AC1 -- THE GROUP-B PUBLISH, ON A SERVED DAY")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    iam = boto3.client("iam", region_name="us-east-1")
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(here, ".served_runner_os23.py")
    try:
        mod, raw = load_served_runner(s3, dest)
    except Exception as exc:                                                # noqa: BLE001
        print("BLOCKED: could not load the SERVED runner (%s: %s)" % (type(exc).__name__, exc))
        return 1
    print("served runner %s (%d B)" % (CODE_KEY, len(raw)))

    doc, art = arm_a(s3)
    arm_b(doc, art, s3)
    arm_c(mod)
    arm_d(art, s3)
    arm_e(mod, iam)
    arm_f(s3)
    arm_g(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS23-GROUP-B-PUBLISHED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
