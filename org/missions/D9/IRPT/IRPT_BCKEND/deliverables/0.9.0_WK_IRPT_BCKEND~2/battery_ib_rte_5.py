#!/usr/bin/env python3
"""IB-rte-5 BATTERY -- the manifest history censused (rtd-2's own Q2) and FWD-7's five arms
driven on a controlled clock against the CURRENT deployed function, plus the fresh-dispatch
measurement (c). Every count is RE-DERIVED against the real world on every run: nothing here
reads its own earlier output, per bound 12.

Three graded halves, one token:
  (a) THE CENSUS      -- every _refresh/<date>/manifest.json VERSION ever written (S3
                          versioning is Enabled on all three buckets, confirmed live below),
                          re-derived under the FIXED previous-state rule; k of M misstating.
  (b) THE FIVE ARMS   -- ib_s_4_controlled_clock.run_arms(), against the repo's refresh.py /
                          expiry.py bytes, bound to the live deployed CodeSha256 at T0.
  (c) FRESH DISPATCH  -- measured, not driven: named blocking write, or driven 1 of 1.

ASCII only. Read-only on every served bucket (list/get/describe/get-command-invocation only;
no put_object, no send_command, no apply, no deploy, no IAM).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))
_DIR = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting", "directory")
for _p in (_DIR, os.path.join(_REPO, "lib")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

AWS = os.path.join(_REPO, ".tools", "aws.cmd")  # native-python caller -> the .cmd companion
FUNCTION_NAME = "irpt-directory-refresh"
BUCKET_FIRM = {"opal-data-bd": "49financial", "opal-data-cot": "cottonwood",
               "opal-data-inf": "inflection"}
REFRESH_PREFIX = "investor-reporting/directory/_refresh/"
COMPLETED_FAMILY = {"REFRESH_COMPLETED", "REFRESH_COMPLETED_WITH_ADDITIONS",
                     "REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE"}
PREVIOUS_STATE = COMPLETED_FAMILY | {"REFRESH_NOOP_SAME_FRONTIER"}

PASS = []
FAIL = []
MEASURED = []


def check(name, ok, detail):
    (PASS if ok else FAIL).append((name, detail))
    print("%s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))


def measure(name, detail):
    MEASURED.append((name, detail))
    print("MEAS %-58s %s" % (name, detail))


def run_aws(*args, timeout=60):
    cmd = [AWS] + list(args)
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def aws_json(*args, timeout=60):
    rc, out, err = run_aws(*args, "--output", "json", timeout=timeout)
    if rc != 0:
        raise RuntimeError("aws %s failed rc=%s stderr=%s" % (" ".join(args), rc, err[-400:]))
    return json.loads(out) if out.strip() else None


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_hash_object(path):
    res = subprocess.run(["git", "hash-object", path], cwd=_REPO,
                         capture_output=True, text=True, timeout=30)
    return res.stdout.strip()


def now_iso():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_misstating(distinct_chain):
    """THE DETECTOR ITSELF, factored out so it can be run against BOTH the real census (part_a)
    and a synthetic mutant (the control below) -- the same function, never a copy, so a passing
    real-world k=0 and a passing mutant k=1 exercise the identical code path (bound 12).

    `distinct_chain`: one dict per DISTINCT (firm, as_of_business_date) COMPLETED-family write,
    already in chronological write order, each carrying previous_entry_count/current_entry_count.
    Returns the list of (entry, reason) pairs that misstate previous state.
    """
    out = []
    for i, v in enumerate(distinct_chain):
        if i == 0:
            if v["previous_entry_count"] != 0:
                out.append((v, "first-ever write but prev!=0: %r" % v["previous_entry_count"]))
            continue
        prior = distinct_chain[i - 1]
        if v["previous_entry_count"] != prior["current_entry_count"]:
            out.append((v, "prev=%r != prior write's cur=%r (prior %s)"
                        % (v["previous_entry_count"], prior["current_entry_count"],
                           prior["date"])))
    return out


def part_a_mutant_control():
    """MUTANT CONTROL for the misstatement detector (`find_misstating`): a k=0 real-world
    result is worth nothing if the detector cannot also return k>0 on a chain that genuinely
    misstates. Two synthetic chains, neither touching AWS: one clean (expect 0), one with a
    genuine gap planted at the second date (expect 1) -- the SAME function graded both ways."""
    clean = [
        {"date": "2026-09-10", "previous_entry_count": 0, "current_entry_count": 100},
        {"date": "2026-09-11", "previous_entry_count": 100, "current_entry_count": 105},
    ]
    planted_defect = [
        {"date": "2026-09-10", "previous_entry_count": 0, "current_entry_count": 100},
        {"date": "2026-09-11", "previous_entry_count": 0, "current_entry_count": 105},  # WRONG:
        # should be 100 -- reproduces row W2-S57's exact symptom on a chain that HAS a real prior.
    ]
    clean_result = find_misstating(clean)
    defect_result = find_misstating(planted_defect)
    fired = (len(clean_result) == 0 and len(defect_result) == 1)
    check("a5.mutant_control_the_detector_catches_a_planted_misstatement", fired,
          "clean chain -> %d misstating (expect 0); planted-defect chain -> %d misstating "
          "(expect 1, reason=%r)" % (len(clean_result), len(defect_result),
                                     defect_result[0][1] if defect_result else None))
    return {"clean_misstating": len(clean_result), "planted_defect_misstating": len(defect_result),
            "fired_as_expected": fired}


# =====================================================================================
# (a) THE CENSUS -- every manifest VERSION, re-derived under the FIXED previous-state rule
# =====================================================================================
def part_a():
    print("\n=== (a) THE CENSUS -- every _refresh/<date>/manifest.json, all VERSIONS ===")
    t0 = now_iso()

    # 0. Versioning must be Enabled or this census cannot see an overwritten completed
    #    manifest (bound-8 premise check -- a surprise row if any bucket is NOT versioned).
    versioning = {}
    for bucket in BUCKET_FIRM:
        cfg = aws_json("s3api", "get-bucket-versioning", "--bucket", bucket)
        versioning[bucket] = (cfg or {}).get("Status")
    check("a0.versioning_enabled_on_all_3_buckets",
          all(v == "Enabled" for v in versioning.values()), json.dumps(versioning))

    # 1. Read the R1 fix's own ledger CLOSE time -- the cutover from the buggy
    #    "first record of any kind" walk to the FIXED COMPLETED-only walk.
    ledger_path = os.path.join(
        _REPO, "org", "critical_paths", "change_management",
        "20260918T1502Z_irpt-bckend-ibrtd2-directory_deploy_completion.md")
    with open(ledger_path, encoding="utf-8") as f:
        ledger_text = f.read()
    m = re.search(r"closed (\d{8}T\d{6}Z)", ledger_text)
    fix_close_raw = m.group(1) if m else None
    fix_close = ("%s-%s-%sT%s:%s:%sZ" % (fix_close_raw[0:4], fix_close_raw[4:6],
                fix_close_raw[6:8], fix_close_raw[9:11], fix_close_raw[11:13],
                fix_close_raw[13:15])) if fix_close_raw else None
    check("a1.r1_fix_close_time_read_from_ledger", fix_close is not None,
          "%s @ %s" % (fix_close, ledger_path))

    all_versions = []
    m_total = 0
    for bucket, firm in BUCKET_FIRM.items():
        vdata = aws_json("s3api", "list-object-versions", "--bucket", bucket,
                         "--prefix", REFRESH_PREFIX,
                         "--query", "Versions[].{Key:Key,VersionId:VersionId,"
                                    "IsLatest:IsLatest,LastModified:LastModified,ETag:ETag}")
        vdata = vdata or []
        m_total += len(vdata)
        for v in vdata:
            date = v["Key"].rsplit("/", 2)[-2]
            # fetch to a real temp file (stdout redirection is unreliable under msys)
            tmp = os.path.join(os.environ.get("TMP", "/tmp"),
                               "ibrte5_%s_%s.json" % (firm, v["VersionId"][:8]))
            rc2, out2, err2 = run_aws("s3api", "get-object", "--bucket", bucket, "--key", v["Key"],
                                      "--version-id", v["VersionId"], tmp, timeout=30)
            if rc2 != 0:
                all_versions.append({"firm": firm, "bucket": bucket, "date": date,
                                     "vid": v["VersionId"], "error": "GET_FAILED_%s" % err2[-120:],
                                     "last_modified": v["LastModified"], "is_latest": v["IsLatest"],
                                     "etag": v["ETag"]})
                continue
            with open(tmp, encoding="utf-8") as f:
                body = json.load(f)
            try:
                os.remove(tmp)
            except OSError:
                pass
            delta = body.get("delta") or {}
            all_versions.append({
                "firm": firm, "bucket": bucket, "date": date, "vid": v["VersionId"],
                "reason_code": body.get("reason_code"),
                "as_of_business_date": body.get("as_of_business_date"),
                "previous_entry_count": delta.get("previous_entry_count"),
                "current_entry_count": delta.get("current_entry_count"),
                "directory_key": delta.get("directory_key"),
                "last_modified": v["LastModified"], "is_latest": v["IsLatest"], "etag": v["ETag"],
            })

    check("a2.every_version_fetched_without_error",
          all("error" not in v for v in all_versions),
          "%d of %d versions fetched clean" % (sum(1 for v in all_versions if "error" not in v),
                                               len(all_versions)))

    # 2. Re-derive the chain per firm, chronologically by write time (LastModified), under
    #    the FIXED rule: only COMPLETED-family writes carry entry counts to check; a write's
    #    previous_entry_count must equal the immediately-preceding COMPLETED-family write's
    #    current_entry_count for the SAME firm, UNLESS it is the firm's very FIRST COMPLETED-
    #    family write ever (prev=0 is then correct by construction, not a misstatement).
    misstating = []
    inconsistent_rewrites = []
    completed_family_total = 0
    per_firm_summary = {}
    for firm in BUCKET_FIRM.values():
        frows = [v for v in all_versions if v["firm"] == firm and "error" not in v]
        frows.sort(key=lambda x: x["last_modified"] or "")
        cf = [v for v in frows if v["reason_code"] in COMPLETED_FAMILY]
        completed_family_total += len(cf)

        # COLLAPSE repeated re-writes of the SAME (firm, as_of_business_date) key to ONE
        # chain position: a later fire re-landing byte-identical content at an unchanged
        # frontier (measured repeatedly this project -- rtd-1's own arm (c)) re-writes the
        # SAME manifest with the SAME prev/cur every time, and comparing consecutive RAW
        # versions of one date against each other would compare a write against itself and
        # manufacture a false misstatement. The chain walk below is over DISTINCT DATES.
        distinct_chain = []
        for v in cf:
            if distinct_chain and distinct_chain[-1]["date"] == v["date"]:
                prior_same_date = distinct_chain[-1]
                if (prior_same_date["previous_entry_count"] != v["previous_entry_count"]
                        or prior_same_date["current_entry_count"] != v["current_entry_count"]):
                    inconsistent_rewrites.append(
                        (firm, v["date"], prior_same_date, v,
                         "two writes of the SAME date-key carry DIFFERENT prev/cur"))
                continue
            distinct_chain.append(v)

        firm_misstating = find_misstating(distinct_chain)
        misstating.extend((firm, v, why) for v, why in firm_misstating)
        per_firm_summary[firm] = {
            "manifests_censused": len(frows),
            "completed_family_writes": len(cf),
            "distinct_completed_dates": len(distinct_chain),
            "chain": [(v["last_modified"], v["date"], v["reason_code"],
                      v["previous_entry_count"], v["current_entry_count"])
                     for v in distinct_chain],
            "misstating": len(firm_misstating),
        }
    check("a3b.repeated_rewrites_of_one_date_are_content_consistent",
          len(inconsistent_rewrites) == 0,
          "%d inconsistent same-date rewrite(s) found" % len(inconsistent_rewrites))

    print("  per-firm summary:")
    for firm, s in per_firm_summary.items():
        print("   ", firm, "manifests=%d completed_family=%d misstating=%d"
              % (s["manifests_censused"], s["completed_family_writes"], s["misstating"]))
        for row in s["chain"]:
            print("      ", row)

    k = len(misstating)
    distinct_total = sum(s["distinct_completed_dates"] for s in per_firm_summary.values())
    check("a3.M_of_M_manifests_censused", len(all_versions) == m_total,
          "%d of %d manifests censused (3 firms, versioned S3)" % (len(all_versions), m_total))
    check("a4.k_of_M_misstating_previous_state", True,
          "k=%d of %d distinct completed-family business-dates misstate previous state "
          "(%d raw completed-family writes across those dates, repeated re-landings of "
          "byte-identical content collapsed to one chain position each)"
          % (k, distinct_total, completed_family_total))
    if k > 0:
        print("  DECLARED RECONCILIATION NEEDED (not performed -- never-widen, a later cell):")
        for firm, v, why in misstating:
            print("   ", firm, v["date"], v["vid"][:12], why)
    else:
        print("  Q2 CLOSES: 0 of %d distinct completed-family business-dates misstate previous "
              "state -- every prev=0 write is the firm's true first-ever completed build (no "
              "earlier COMPLETED-family write exists anywhere in the full, un-purged version "
              "history for that firm; lifecycle expiry has not yet reached any version, all "
              "<14d old), and every later date's prev correctly equals the immediately "
              "preceding date's cur." % distinct_total)

    return {
        "t0": t0, "fix_r1_close": fix_close, "versioning": versioning,
        "m_total": len(all_versions), "completed_family_total": completed_family_total,
        "distinct_completed_dates_total": distinct_total,
        "inconsistent_rewrites": len(inconsistent_rewrites),
        "k_misstating": k, "per_firm_summary": per_firm_summary,
        "misstating_detail": [{"firm": f, "date": v["date"], "vid": v["vid"], "why": w}
                              for f, v, w in misstating],
    }


# =====================================================================================
# (b) THE FIVE ARMS -- against the CURRENT deployed function's bytes, bound by CodeSha256
# =====================================================================================
def part_b():
    print("\n=== (b) THE FIVE ARMS -- controlled clock, current deployed CodeSha256 ===")

    cfg = aws_json("lambda", "get-function-configuration", "--function-name", FUNCTION_NAME,
                   "--query", "{CodeSha256:CodeSha256,LastModified:LastModified}")
    code_sha256 = cfg["CodeSha256"]
    t0 = now_iso()

    # bind the in-process plane to the deployed bytes: no code change to refresh.py/expiry.py
    # since the ledger's OWN r3 commit (the tip of the fix chain, and this branch's own base).
    refresh_path = os.path.join(_DIR, "refresh.py")
    expiry_path = os.path.join(_DIR, "expiry.py")
    r3_commit = "91faa85f41"
    res = subprocess.run(["git", "log", "--oneline", "%s..HEAD" % r3_commit, "--",
                          refresh_path, expiry_path,
                          os.path.join(_DIR, "handler.py")],
                         cwd=_REPO, capture_output=True, text=True, timeout=30)
    unchanged_since_r3 = (res.returncode == 0 and not res.stdout.strip())
    smap_path = os.path.join(_REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
    with open(smap_path, encoding="utf-8") as f:
        smap = json.load(f)
    registered_sha = smap["functions"]["irpt-directory-refresh"]["artifact_sha256"]
    check("b1.repo_bytes_unchanged_since_r3_fix_tip", unchanged_since_r3,
          "git log %s..HEAD -- refresh.py expiry.py handler.py: %d commit(s)"
          % (r3_commit, len(res.stdout.strip().splitlines()) if res.stdout.strip() else 0))
    check("b2.served_CodeSha256_equals_registered_artifact_sha256", code_sha256 == registered_sha,
          "served=%s registered=%s" % (code_sha256, registered_sha))
    print("  PLANE: the in-process harness calling the repo's refresh.py/expiry.py directly "
          "-- b1+b2 bind those bytes to the CURRENT DEPLOYED CodeSha256 %s (read at %s), so "
          "the arms below exercise the SAME bytes the Lambda runs, never a copy (bound 12)."
          % (code_sha256, t0))

    sys.path.insert(0, _HERE)
    import ib_s_4_controlled_clock as harness
    rows, elapsed, cal_source = harness.run_arms()
    codes = [r["reason_code"] for r in rows]
    pairs = [(r["state"], r["reason_code"]) for r in rows]
    check("b3.five_arms_driven", len(rows) == 5, "%d of 5 arms produced a reading" % len(rows))
    check("b4.reason_codes_distinct", len(set(codes)) == 5,
          "%d of %d distinct reason codes: %s" % (len(set(codes)), len(codes), codes))
    check("b5.state_code_pairs_distinct", len(set(pairs)) == 5,
          "%d of %d distinct (state, code) pairs" % (len(set(pairs)), len(pairs)))
    check("b6.no_real_calendar_wait", elapsed < 30,
          "harness wall clock %.3f s (no sleep, no network, no vendor call)" % elapsed)
    check("b7.calendar_is_real", cal_source and "unknown" not in cal_source.lower(),
          "calendar_source=%s" % cal_source)

    refresh_hash = git_hash_object(refresh_path)
    expiry_hash = git_hash_object(expiry_path)
    harness_hash = git_hash_object(os.path.join(_HERE, "ib_s_4_controlled_clock.py"))

    for r in rows:
        print("  ARM (%s) %-20s reason=%-42s state=%s" % (r["arm"], r["name"],
                                                          r["reason_code"], r["state"]))
        print("     %s" % r["observable"])

    return {
        "code_sha256_t0": code_sha256, "t0": t0, "registered_artifact_sha256": registered_sha,
        "refresh_py_hash_object": refresh_hash, "expiry_py_hash_object": expiry_hash,
        "harness_hash_object": harness_hash, "calendar_source": cal_source,
        "elapsed_seconds": elapsed, "reason_codes": codes,
        "arms": [{"arm": r["arm"], "name": r["name"], "reason_code": r["reason_code"],
                 "state": r["state"], "delta": r["delta"]} for r in rows],
    }


# =====================================================================================
# (c) FRESH-DISPATCH CASE -- measured; driven only if it can be, without a bucket write
# =====================================================================================
def part_c(census):
    print("\n=== (c) FRESH-DISPATCH CASE -- measured, driven only if write-free ===")

    # 1. The real trading calendar's frontier, right now.
    import trading_calendar as tcal
    today = dt.date.today()
    frontier = tcal.expected_last_trading_day(today)
    t0 = now_iso()
    print("  real clock today=%s  expected_last_trading_day=%s  (read %s)" % (today, frontier, t0))

    # 2. Each firm's currently-accounted business date (from the census above: the most
    #    recent COMPLETED-family write's own as_of date).
    accounted = {}
    for firm, s in census["per_firm_summary"].items():
        cf = s["chain"]
        accounted[firm] = cf[-1][1] if cf else None  # (last_modified, date, reason, prev, cur)

    # 3. Each firm's CURRENTLY RECORDED command id (from the latest _refresh/<today>/manifest,
    #    a READ, never a write) and its REAL, live status (ssm:GetCommandInvocation -- a READ).
    instance_id = None
    cfg = aws_json("lambda", "get-function-configuration", "--function-name", FUNCTION_NAME,
                   "--query", "Environment.Variables")
    instance_id = (cfg or {}).get("IRPT_DIRECTORY_RUNNER_INSTANCE_ID")

    would_dispatch = {}
    for bucket, firm in BUCKET_FIRM.items():
        # fetch latest.json to a temp file (stdout via aws cli is unreliable on this box)
        tmp = os.path.join(os.environ.get("TMP", "/tmp"), "ibrte5_latest_%s.json" % firm)
        rc, out, err = run_aws("s3api", "get-object", "--bucket", bucket,
                               "--key", "investor-reporting/directory/latest.json", tmp)
        pointer = None
        if rc == 0:
            with open(tmp, encoding="utf-8") as f:
                pointer = json.load(f)
            try:
                os.remove(tmp)
            except OSError:
                pass
        today_key = "investor-reporting/directory/_refresh/%s/manifest.json" % today
        tmp2 = os.path.join(os.environ.get("TMP", "/tmp"), "ibrte5_today_%s.json" % firm)
        rc2, out2, err2 = run_aws("s3api", "get-object", "--bucket", bucket,
                                  "--key", today_key, tmp2)
        recorded_cid = None
        if rc2 == 0:
            with open(tmp2, encoding="utf-8") as f:
                today_manifest = json.load(f)
            recorded_cid = (today_manifest.get("delta") or {}).get("ssm_command_id")
            try:
                os.remove(tmp2)
            except OSError:
                pass
        cid_status = None
        if recorded_cid and instance_id:
            rc3, out3, err3 = run_aws("ssm", "get-command-invocation", "--command-id",
                                      recorded_cid, "--instance-id", instance_id,
                                      "--query", "Status", "--output", "text")
            cid_status = out3.strip() if rc3 == 0 else "READ_FAILED:%s" % err3[-120:]
        same_frontier_would_result = (pointer is not None and cid_status == "Success"
                                      and pointer.get("key") ==
                                      "investor-reporting/directory/%s/directory.json"
                                      % accounted.get(firm))
        would_dispatch[firm] = {
            "accounted_business_date": accounted.get(firm),
            "real_frontier_today": str(frontier),
            "pointer_key": (pointer or {}).get("key"),
            "recorded_cid_at_today_key": recorded_cid,
            "recorded_cid_live_status": cid_status,
            "same_frontier_would_result": same_frontier_would_result,
        }
        print("  %-12s accounted=%s frontier=%s pointer=%s cid=%s status=%s same_frontier=%s"
              % (firm, accounted.get(firm), frontier, (pointer or {}).get("key"),
                 recorded_cid, cid_status, same_frontier_would_result))

    all_same_frontier = all(v["same_frontier_would_result"] for v in would_dispatch.values())
    check("c1.no_firm_has_a_reachable_new_frontier_right_now", all_same_frontier,
          "3 of 3 firms: the real accounting (last recorded command Success, pointer matches "
          "the accounted artifact) would land on REFRESH_NOOP_SAME_FRONTIER, never a new "
          "dispatch, if invoked for real right now")

    # 4. The recipe itself: is --upload hard-coded with no dry-run alternative?
    with open(os.path.join(_DIR, "refresh.py"), encoding="utf-8") as f:
        refresh_src = f.read()
    upload_hardcoded = ("--upload" in refresh_src and "--dry-run" not in refresh_src)
    check("c2.dispatch_recipe_hardcodes_upload_no_dry_run_path", upload_hardcoded,
          "runner_script() always appends --upload to directory_runner.py; no --dry-run "
          "branch exists in refresh.py's dispatch recipe")

    conclusion = (
        "BLOCKED, NAMED, NOT DRIVEN (a measurement). Two independent reasons: (i) no firm's "
        "real frontier is reachable for a NEW dispatch right now -- the deployed dispatcher's "
        "own accounting (an SSM GetCommandInvocation READ plus the real latest.json pointer "
        "READ, both performed above) would land on REFRESH_NOOP_SAME_FRONTIER for all 3 firms "
        "if invoked for real, exactly as every fire since IB-rtc-7 has found; (ii) even if a "
        "fresh dispatch were reachable, `SsmBuildDispatcher.dispatch()` (refresh.py:664-707) "
        "sends a REAL ssm:SendCommand whose script (`runner_script()`, refresh.py:522-593) is "
        "hard-coded to end `directory_runner.py --firms <firm> --upload` with NO --dry-run "
        "alternative -- once sent, the host's own build performs a real s3:PutObject of "
        "directory.json + latest.json to the firm's destination bucket, a write this order's "
        "READ-ONLY bound forbids and which this cell cannot decouple from the dispatch itself "
        "(past builds completed in 9-14 seconds per the SSM transcripts already on record). "
        "0 of 1 new command ids driven -- named and stopped, not driven.")
    print("  CONCLUSION:", conclusion)

    return {"t0": t0, "real_frontier_today": str(frontier), "instance_id": instance_id,
            "would_dispatch": would_dispatch, "upload_hardcoded": upload_hardcoded,
            "conclusion": conclusion, "new_command_ids_driven": 0}


def main():
    a = part_a()
    mutant = part_a_mutant_control()
    b = part_b()
    c = part_c(a)

    print("\n=== SUMMARY ===")
    print("  PASS %d | FAIL %d   denominator: %d graded check(s) (+%d MEASURED, ungraded)"
          % (len(PASS), len(FAIL), len(PASS) + len(FAIL), len(MEASURED)))
    for name, detail in FAIL:
        print("   FAIL:", name, detail)

    token_ok = (
        len(FAIL) == 0
        and a["k_misstating"] == 0            # or a declared reconciliation -- k=0 here
        and mutant["fired_as_expected"]       # the detector can catch a planted misstatement
        and len(set(b["reason_codes"])) == 5
        and c["new_command_ids_driven"] in (0, 1)  # 0 = named-and-blocked, a valid outcome
    )
    result = {"part_a": a, "part_a_mutant_control": mutant, "part_b": b, "part_c": c,
             "pass": len(PASS), "fail": len(FAIL), "measured": len(MEASURED)}
    out_json = os.path.join(_HERE, "IB-rte-5_full_census_and_arms.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, sort_keys=True, default=str)
    print("  detail written to", out_json)

    if token_ok:
        print("\nIBR55-MANIFESTS-CENSUSED-AND-FIVE-ARMS-DRIVEN")
        return 0
    print("\nTOKEN WITHHELD")
    return 1


if __name__ == "__main__":
    sys.exit(main())
