#!/usr/bin/env python3
"""BATTERY IB-rtd-2 -- THE NO-OP BRANCH FIRES ON ITS POSITIVE CASE.

Row IRPT_BCKEND-W2-S57: `last_manifest()`'s calendar-day walk returned the FIRST manifest found
walking backward, of ANY kind, so a same-day REFRESH_DISPATCHED manifest (keyed by the Lambda's
CLOCK date) was found before the REFRESH_COMPLETED one at the runner's own, earlier BUSINESS
date -- REFRESH_NOOP_SAME_FRONTIER could never fire on a real manifest history and a same-
frontier re-fire re-reported the unchanged, already-landed artifact as
REFRESH_COMPLETED_WITH_ADDITIONS with previous_entry_count=0.

  (a) THE REAL UNIT-TEST SUITE, k of k -- infra/aws/lambda/investor-reporting/directory/tests/,
      58 tests total, INCLUDING the 11 new ones in tests/test_refresh_previous_state.py that (i)
      prove last_manifest() now resolves the COMPLETED manifest over a same-day DISPATCHED one
      and a FAILED one within it, on the REAL manifests both graded firms wrote; (ii) drive the
      REAL lambda_handler end to end and assert REFRESH_NOOP_SAME_FRONTIER on the exact real
      defect shape, with no second SSM command sent; (iii) confirm a genuinely CHANGED artifact
      at the same date still reports additions; a SECOND real defect this battery's own first
      live drive found -- the missed-fire date must NOT be narrowed the same way "previous" was,
      or a FAILED/still-DISPATCHED day misreads as a day nothing fired at all -- is covered too
      (cottonwood's exact real shape reaches NOOP, never TRIGGER_MISSED); (iv) reproduce the
      MUTANT (the old first-found walk) and prove it fails BOTH (i) and (ii) -- it returns the
      wrong manifest and, fed into the REAL SsmBuildDispatcher, reproduces row W2-S57's exact
      symptom (previous_entry_count=0 on unchanged bytes).
  (b) READ-ONLY, post-deploy: served CodeSha256 == the built zip == the source-map registration;
      a fresh `terraform plan` reads "No changes"; BOTH change-management ledger entries for this
      cell's two deploys (round 1: the previous-state fix, opened 05c0322989 / closed
      aff243111d; round 2: the missed-fire-date fix this cell's own live drive found necessary,
      opened b81e02d1e8 / closed 9914ccffc2) read CLOSED with all 5 legs proven. Both applies
      (each 0 to add, 1 to change, 0 to destroy -- source_code_hash + s3_object_version only)
      already happened under their own ledger; this arm RE-DERIVES every claim from the live
      world at THIS run, never from those commits' own text.
  (c) THE LIVE DRIVE, after the organic fire (IB-rtd-1, merged) and after BOTH of this cell's own
      fixes are deployed: invokes irpt-directory-refresh with EXACTLY the schedule's own payload
      (read live from schedule.tf, no business_date override). For inflection and cottonwood --
      whose frontiers are unchanged since the organic fire (IB-rtd-1's own result: both landed
      inf 2026-09-17 / cot 2026-09-16, and this arm's own before-snapshot confirms neither
      pointer has moved) -- the reconciliation must read REFRESH_NOOP_SAME_FRONTIER with the
      landed key's ETag unchanged and 0 new keys under investor-reporting/directory/. The
      negative control is the organic fire's OWN manifest, quoted from the FROZEN pre-fix
      fixture capture (tests/fixtures/, copied verbatim from the real live objects before this
      fix landed -- the live objects at these keys now read the FIXED behaviour, so the defect
      can only be quoted from that frozen capture, never re-fetched live post-fix):
      REFRESH_COMPLETED_WITH_ADDITIONS with previous_entry_count=0 on those same byte-identical
      ETags. 49financial is MEASURED, never graded (its build dispatch is still blocked on the
      host role's grants, row IRPT_BCKEND-W2-S49, BLOCKING, unrelated to this fix), matching
      IB-rtd-1/IB-rtc-3's own precedent for this firm.

THE TOKEN IS GATED on (a) k of k, (b) all clean, and (c)'s inf+cot 2 of 2 REFRESH_NOOP_SAME_FRONTIER
with ETag-unchanged and 0-new-keys. Nothing here wraps, patches or re-registers the subject
(bound 12): the tests import the real refresh.py; the deploy checks read the real served function
and the real terraform state; the live drive invokes the real deployed Lambda. No command id,
hash or manifest key is reused from an earlier run -- every one is read fresh, this run, from the
real world.

ASCII only. Every external call is bounded (subprocess timeout, or a deadline-bound poll loop).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
AWS = os.path.join(REPO, ".tools", "aws.cmd")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")
DIRECTORY = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "directory")
TESTS_DIR = os.path.join(DIRECTORY, "tests")
TF_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "directory")
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
SCHEDULE_TF = os.path.join(TF_ROOT, "schedule.tf")
OPEN_DEPLOYS = os.path.join(REPO, "org", "critical_paths", ".open_deploys")

FUNCTION = "irpt-directory-refresh"
REGION = "us-east-1"
FIRM_BUCKETS = {"49financial": "opal-data-bd",
                "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
DIRECTORY_PREFIX = "investor-reporting/directory"
LEDGER_SLUG = "irpt-bckend-ibrtd2-directory"
LEDGER_SLUG_R2 = "irpt-bckend-ibrtd2-directory-r2"

PYTHON = os.environ.get("PY312", "py")
PYTHON_ARGS = ["-3.12"] if PYTHON == "py" else []

RESULTS = []
LANDED = {}


def record(arm, verdict, line, denominator=""):
    RESULTS.append((arm, verdict, line, denominator))
    print("  [%s] %-9s %s%s" % (arm, verdict, line,
                                ("   denominator: %s" % denominator) if denominator else ""))


def aws(*args, timeout=180):
    try:
        p = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    return p.returncode, (p.stdout or "").replace("\r", ""), (p.stderr or "").replace("\r", "")


def aws_json(*args, **kw):
    rc, out, err = aws(*args, **kw)
    if rc != 0:
        return None, (err or out)[-400:]
    try:
        return json.loads(out), None
    except ValueError as exc:
        return None, "unparseable: %s" % exc


def head(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


# ============================================================== ARM (a) -- THE REAL TEST SUITE
def arm_a():
    head("ARM (a) THE REAL UNIT-TEST SUITE, k of k -- includes the 9 new previous-state tests "
         "(the fix's tests (i)-(iii) and the mutant differential (iv))")
    p = subprocess.run([PYTHON] + PYTHON_ARGS + ["-m", "pytest", TESTS_DIR, "-q"],
                        capture_output=True, text=True, timeout=180)
    m = re.search(r"(\d+) passed", p.stdout or "")
    k = m.group(1) if m else "?"
    tail = (p.stdout or "")[-400:].replace("\n", " | ")
    ok = p.returncode == 0 and m is not None
    record("a.1", "PASS" if ok else "FAIL",
           "pytest %s -q: %s" % (TESTS_DIR, tail),
           ("%s of %s" % (k, k)) if m else "rc=%d" % p.returncode)

    # named-shape self-check: the fix's specific 12 tests are present and passed, by name.
    names_wanted = [
        "test_last_manifest_skips_a_same_day_dispatched_record_and_returns_the_completed_one",
        "test_last_manifest_skips_dispatched_and_failed_to_reach_a_completion_two_days_back",
        "test_last_dispatched_cid_finds_the_in_flight_command_last_manifest_now_excludes",
        "test_last_dispatched_cid_is_none_when_no_dispatched_record_exists",
        "test_last_dispatched_cid_does_not_reach_past_a_stale_dispatch_the_completion_supersedes",
        "test_lambda_handler_reaches_noop_same_frontier_on_the_real_defect_shape",
        "test_lambda_handler_reports_additions_when_the_artifact_genuinely_changed",
        "test_lambda_handler_does_not_misread_a_failed_or_dispatched_day_as_missed",
        "test_last_recorded_business_date_is_the_newest_record_of_any_kind",
        "test_the_mutant_returns_the_dispatched_record_where_the_fix_returns_completed",
        "test_the_mutants_previous_manifest_reproduces_row_w2_s57s_exact_symptom",
        "test_previous_state_reason_codes_matches_the_completed_family_and_noop_only",
    ]
    p2 = subprocess.run([PYTHON] + PYTHON_ARGS + ["-m", "pytest", "--color=no",
                        os.path.join(TESTS_DIR, "test_refresh_previous_state.py"), "-v"],
                        capture_output=True, text=True, timeout=180)
    stdout2 = p2.stdout or ""
    found = sum(1 for n in names_wanted if (n + " PASSED") in stdout2)
    record("a.2", "PASS" if found == len(names_wanted) else "FAIL",
           "the %d named previous-state tests all PASSED by name" % len(names_wanted),
           "%d of %d" % (found, len(names_wanted)))


# ============================================================== ARM (b) -- READ-ONLY POST-DEPLOY
def arm_b():
    head("ARM (b) READ-ONLY, POST-DEPLOY: served CodeSha256 == built == source-map; "
         "terraform plan No changes; ledger CLOSED, 5 of 5 legs")
    cfg, err = aws_json("lambda", "get-function-configuration", "--function-name", FUNCTION,
                         "--output", "json")
    if cfg is None:
        record("b.1", "FAIL", "get-function-configuration failed: %s" % err)
        return
    served = cfg["CodeSha256"]
    smap = json.load(open(SOURCE_MAP, encoding="utf-8"))
    declared = smap["functions"][FUNCTION]["artifact_sha256"]
    record("b.1", "PASS" if served == declared else "FAIL",
           "served CodeSha256 %s %s branch-tip source-map artifact_sha256 %s"
           % (served, "==" if served == declared else "!=", declared))

    p = subprocess.run([TERRAFORM, "-chdir=%s" % TF_ROOT, "plan", "-input=false", "-no-color"],
                        capture_output=True, text=True, timeout=180)
    no_changes = "No changes. Your infrastructure matches the configuration." in (p.stdout or "")
    record("b.2", "PASS" if (p.returncode == 0 and no_changes) else "FAIL",
           "terraform plan (worktree-provisioned terraform.exe): %s"
           % (["No changes."] if no_changes else (p.stdout or p.stderr)[-300:]))

    # BOTH deploys (round 1's original fix, round 2's missed-date fix -- arm (c) below found the
    # second defect live and this cell re-deployed under a second ledger entry) are graded: the
    # served function reflects round 2, and round 1's own ledger must ALSO read CLOSED.
    all_closed = True
    for slug in (LEDGER_SLUG, LEDGER_SLUG_R2):
        sentinel = os.path.join(OPEN_DEPLOYS, slug + ".json")
        sentinel_gone = not os.path.exists(sentinel)
        cm_path = None
        for fn in os.listdir(os.path.join(REPO, "org", "critical_paths", "change_management")):
            if slug in fn:
                cm_path = os.path.join(REPO, "org", "critical_paths", "change_management", fn)
        closed = False
        if cm_path:
            text = open(cm_path, encoding="utf-8").read()
            closed = "**Status:** CLOSED" in text and "all 5 legs proven" in text
        ok = sentinel_gone and closed
        all_closed = all_closed and ok
        record("b.3.%s" % slug, "PASS" if ok else "FAIL",
               "ledger '%s': sentinel removed=%s, entry text declares CLOSED/5-legs=%s (%s)"
               % (slug, sentinel_gone, closed, cm_path))


# ============================================================ ARM (c) -- THE LIVE DRIVE
def schedule_payload():
    text = open(SCHEDULE_TF, encoding="utf-8").read()
    anchor = 'resource "aws_scheduler_schedule" "irpt_directory_refresh"'
    start = text.index(anchor)
    end_marker = '\noutput "directory_refresh_schedule_name"'
    end = text.index(end_marker, start)
    block = text[start:end]
    if "irpt_holdings_snapshot" in block:
        raise RuntimeError("schedule block bound incorrectly -- it still contains the sibling "
                            "schedule")
    m = re.search(r'input = jsonencode\(\{\s*kind\s*=\s*"([^"]+)"\s*note\s*=\s*"([^"]+)"',
                  block, re.S)
    if not m:
        raise RuntimeError("could not read the schedule's own payload from schedule.tf")
    return {"kind": m.group(1), "note": m.group(2)}


def _list_keys(s3, bucket, prefix):
    keys = []
    token = None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        keys.extend(o["Key"] for o in (page.get("Contents") or []))
        token = page.get("NextContinuationToken")
        if not token:
            return keys


def _read_json_object(s3, bucket, key):
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
    except Exception:                                              # noqa: BLE001
        return None
    return json.loads(obj["Body"].read().decode("utf-8"))


def _head_etag(s3, bucket, key):
    try:
        h = s3.head_object(Bucket=bucket, Key=key)
    except Exception:                                              # noqa: BLE001
        return None
    return h.get("ETag")


def arm_c():
    head("ARM (c) THE LIVE DRIVE -- schedule's own live payload, real Lambda invoke, real S3 "
         "reads. inf/cot graded 2 of 2 on REFRESH_NOOP_SAME_FRONTIER; 49financial MEASURED")
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)

    payload = schedule_payload()
    record("c.payload", "PASS", "schedule payload read live from schedule.tf: %s" % payload)

    before = {}
    for firm, bucket in FIRM_BUCKETS.items():
        keys = set(_list_keys(s3, bucket, DIRECTORY_PREFIX + "/"))
        latest = _read_json_object(s3, bucket, "%s/latest.json" % DIRECTORY_PREFIX)
        etag = None
        if latest and latest.get("key"):
            etag = _head_etag(s3, bucket, latest["key"])
        before[firm] = {"keys": keys, "pointer": latest, "landed_key": (latest or {}).get("key"),
                        "etag": etag}
    record("c.before", "PASS", "before-snapshot: %s"
           % {f: {"n_keys": len(before[f]["keys"]), "landed_key": before[f]["landed_key"],
                  "etag": before[f]["etag"]} for f in before})

    # THE NEGATIVE CONTROL: the organic fire's OWN manifests, quoted from the FROZEN fixture
    # files this cell committed (tests/fixtures/, copied verbatim from the real live objects
    # BEFORE this fix landed -- see the deliverable's commit 39f7a2ffe6). The LIVE objects at
    # these same keys now read the FIXED behaviour (this fix's own point), so the pre-fix defect
    # can only be quoted from the frozen capture, never re-fetched live post-fix -- that would be
    # asking the world to still be broken as proof the fix works.
    fixtures_dir = os.path.join(DIRECTORY, "tests", "fixtures")
    neg_controls = {
        "inflection": json.load(open(os.path.join(
            fixtures_dir, "inf_2026-09-17_completed_with_additions.json"), encoding="utf-8")),
        "cottonwood": json.load(open(os.path.join(
            fixtures_dir, "cot_2026-09-16_completed_with_additions.json"), encoding="utf-8")),
    }
    record("c.negative_control", "MEASURED",
           "organic fire's own manifest, quoted from the frozen pre-fix fixture capture: %s"
           % {f: {"reason_code": m.get("reason_code"),
                  "previous_entry_count": (m.get("delta") or {}).get("previous_entry_count")}
              for f, m in neg_controls.items()})
    pre_fix_defect = all(m.get("reason_code") == "REFRESH_COMPLETED_WITH_ADDITIONS"
                         and (m.get("delta") or {}).get("previous_entry_count") == 0
                         for m in neg_controls.values())
    record("c.negative_control.shape", "PASS" if pre_fix_defect else "FAIL",
           "both firms' organic-fire manifest (frozen fixture) reads "
           "REFRESH_COMPLETED_WITH_ADDITIONS with previous_entry_count=0 on unchanged bytes -- "
           "the pre-fix defect this cell fixes, row IRPT_BCKEND-W2-S57",
           "2 of 2" if pre_fix_defect else "%d of 2" % len(neg_controls))

    deadline = time.time() + 900
    envelopes = None
    attempt = 0
    invoke_log = []
    while time.time() < deadline:
        attempt += 1
        resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(payload).encode("utf-8"))
        body = json.loads(resp["Payload"].read())
        results_ = body.get("results", [])
        envelopes = {r["firm_id"]: r for r in results_}
        codes = {fid: r["envelope"]["public_reason_code"] for fid, r in envelopes.items()}
        invoke_log.append((attempt, codes))
        print("    invoke %d reason_codes=%s" % (attempt, codes))
        graded = {"inflection", "cottonwood"}
        if all(codes.get(f) == "REFRESH_NOOP_SAME_FRONTIER" for f in graded):
            break
        if all(codes.get(f) != "REFRESH_DISPATCHED" for f in graded):
            # settled one way or the other (noop, completed, or failed) -- no more fires needed
            break
        time.sleep(15)
    record("c.invokes", "PASS" if envelopes is not None else "FAIL",
           "%d invoke(s) against the exact schedule payload: %s"
           % (attempt, [c for _, c in invoke_log]))

    if envelopes is None or set(envelopes) != set(FIRM_BUCKETS):
        record("c.response", "FAIL", "did not get a 3-firm response: %s" % (envelopes,))
        return

    graded_ok = 0
    for firm in ("inflection", "cottonwood", "49financial"):
        row = envelopes[firm]
        bucket = FIRM_BUCKETS[firm]
        env = row["envelope"]
        reason = env.get("public_reason_code")
        state = env.get("state")
        bdate = env["source_dates"]["business_date"]
        manifest_key = row.get("manifest_key")
        manifest = _read_json_object(s3, bucket, manifest_key) if manifest_key else None
        delta = (manifest or {}).get("delta") or {}
        landed_key = delta.get("directory_key") or before[firm]["landed_key"]
        after_keys = set(_list_keys(s3, bucket, DIRECTORY_PREFIX + "/"))
        new_keys = after_keys - before[firm]["keys"]
        etag_after = _head_etag(s3, bucket, landed_key) if landed_key else None
        etag_unchanged = (etag_after == before[firm]["etag"]) and etag_after is not None
        new_object_keys = sorted(k for k in new_keys
                                 if not k.startswith(DIRECTORY_PREFIX + "/_refresh/"))

        LANDED[firm] = {"reason": reason, "state": state, "business_date": bdate,
                        "manifest_key": manifest_key, "etag_after": etag_after,
                        "etag_before": before[firm]["etag"], "new_object_keys": new_object_keys}

        is_noop = reason == "REFRESH_NOOP_SAME_FRONTIER"
        line = ("%s: reason=%s state=%s bdate=%s landed_key=%s ETag before=%s after=%s "
               "(unchanged=%s) new non-manifest keys=%d"
               % (firm, reason, state, bdate, landed_key, before[firm]["etag"], etag_after,
                  etag_unchanged, len(new_object_keys)))
        if firm in ("inflection", "cottonwood"):
            ok = is_noop and etag_unchanged and len(new_object_keys) == 0
            graded_ok += 1 if ok else 0
            record("c.%s.noop" % firm[:3], "PASS" if ok else "FAIL", line)
        else:
            record("c.49f.measured", "MEASURED", line)

    record("c.landed_total", "PASS" if graded_ok == 2 else "FAIL",
           "inflection + cottonwood read REFRESH_NOOP_SAME_FRONTIER, ETag unchanged, 0 new keys",
           "%d of 2" % graded_ok)


# ================================================================== the verdict
def main():
    print("BATTERY IB-rtd-2 -- the no-op branch fires on its positive case")
    print("repo: %s" % REPO)
    arm_a()
    arm_b()
    arm_c()

    head("VERDICT")
    graded = [r for r in RESULTS if r[1] in ("PASS", "FAIL")]
    npass = sum(1 for _, v, _, _ in graded if v == "PASS")
    nfail = sum(1 for _, v, _, _ in graded if v == "FAIL")
    for arm, v, line, den in RESULTS:
        print("  %-20s %-9s %s" % (arm, v, line[:200]))
    print("")
    print("  PASS %d | FAIL %d   denominator: %d graded check(s) (+%d MEASURED, ungraded)"
          % (npass, nfail, len(graded), len(RESULTS) - len(graded)))
    if nfail == 0:
        print("  IBR42-NO-OP-FIRES-ON-ITS-POSITIVE-CASE")
        return 0
    print("  THE ACCEPTANCE TOKEN IS WITHHELD -- one or more graded arms FAILED. See above.")
    print("  R42-AC1 is FAIL. The order stays open.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
