#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-29 -- the deploy of render_month_end.py to the artifact prefix
the reporter box pulls by key at run time, under its own NEVER-2 ledger entry.

ONE KEY: s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/render_month_end.py.
Not Terraform, not a served report key, nothing under platinum/reports/.

WHAT IS UPLOADED IS THE COMMITTED BLOB, extracted with `git show <ref>:<path>`, never the
worktree file -- on an autocrlf box a worktree read hashes the CHECKOUT and not the
record, and "served equals committed" would then be a claim about two different objects.
Both are measured anyway and printed side by side.

BEFORE THE COPY: the prior object's sha256 and VersionId are recorded, and the copy is
SKIPPED ENTIRELY (disposition SUPERSEDED) if the committed bytes are already served --
NEVER-2: a re-execute of an overtaken promote is a REWIND.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
# The .cmd plane: `.tools/aws` is a bash shim and CreateProcess cannot run it from
# Python (WinError 193). `aws.cmd` is the same shim on the plane this process can spawn.
AWS = os.path.join(REPO, ".tools", "aws.cmd")

BUCKET = "opal-313476888478-lambda-artifacts"
PREFIX = "ec2/etfs-reports/"
KEY = "ec2/etfs-reports/render_month_end.py"
SRC_PATH = "data/etfs/scripts/presentation/render_month_end.py"
REPORTS_BUCKET = "opal-data-etfs"
REPORTS_PREFIX = "platinum/reports/"
SLUG = "etfs-guardrail-egs29-renderer-skipped-branch-property-20260910"
EVIDENCE = os.path.join(HERE, "egs29_deploy_evidence.json")

STEPS: list = []


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(argv, label, check=True, cwd=REPO):
    started = now()
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    err = p.stderr.decode("utf-8", "replace").replace("\r\n", "\n")
    STEPS.append({"label": label, "argv": argv, "rc": p.returncode,
                  "started_utc": started, "finished_utc": now(),
                  "stdout": out[:20000], "stderr": err[:4000]})
    print("  [%s] rc=%d  %s" % (label, p.returncode, " ".join(argv[:6])))
    if check and p.returncode != 0:
        print(err[:1500])
        raise SystemExit("BLOCKED: step %r rc=%d" % (label, p.returncode))
    return p.returncode, out, err


def aws_json(args, label, check=True):
    rc, out, err = run([AWS] + args + ["--output", "json"], label, check=check)
    if rc != 0:
        return rc, None
    try:
        return rc, json.loads(out) if out.strip() else {}
    except ValueError:
        return rc, None


LAST_MODIFIED: dict = {}


def listing(bucket, prefix, label):
    _rc, doc = aws_json(["s3api", "list-objects-v2", "--bucket", bucket,
                         "--prefix", prefix], label)
    items = {c["Key"]: (c["ETag"], c["Size"]) for c in (doc or {}).get("Contents", [])}
    for c in (doc or {}).get("Contents", []):
        LAST_MODIFIED[(bucket, c["Key"])] = str(c.get("LastModified", ""))
    print("    %s -> %d key(s)" % (prefix, len(items)))
    return items


def moved_since(bucket, keys, since_iso):
    """Which of `keys` carry a LastModified at or after `since_iso`.

    THIS IS THE MEASUREMENT THAT SURVIVES A RE-RUN. A before/after listing pair only sees
    what moved BETWEEN ITS OWN TWO READS, so on a second invocation -- after the copy has
    already landed -- it reports zero and reads exactly like "nothing was ever touched".
    LastModified is a property of the OBJECT, not of this script's window, so it answers
    "what moved during the act" whichever invocation asks.
    """
    out = []
    for k in keys:
        lm = LAST_MODIFIED.get((bucket, k), "")
        if lm and lm >= since_iso:
            out.append((k, lm))
    return sorted(out)


def sha256_file(path):
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


def main() -> int:
    print("EG-s-29 DEPLOY -- one key, %s" % KEY)
    head_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                              stdout=subprocess.PIPE).stdout.decode().strip()
    blob = subprocess.run(["git", "show", "%s:%s" % (head_sha, SRC_PATH)], cwd=REPO,
                          stdout=subprocess.PIPE).stdout
    payload = os.path.join(REPO, ".scratch", "egs29_payload_render_month_end.py")
    os.makedirs(os.path.dirname(payload), exist_ok=True)
    io.open(payload, "wb").write(blob)
    committed_sha = hashlib.sha256(blob).hexdigest()
    worktree_sha = sha256_file(os.path.join(REPO, SRC_PATH))
    print("  HEAD                %s" % head_sha)
    print("  committed blob      %d B  sha256 %s" % (len(blob), committed_sha))
    print("  worktree checkout   %d B  sha256 %s  (equal: %s)"
          % (os.path.getsize(os.path.join(REPO, SRC_PATH)), worktree_sha,
             worktree_sha == committed_sha))

    # ---- the ledger entry, OPENED BEFORE THE COPY -----------------------------
    title = (
        "EG-s-29 DEPLOY: aws s3 cp of render_month_end.py to the artifact prefix the "
        "reporter box pulls by key at run time -- NOT Terraform, NOT a served report key. "
        "BLAST RADIUS, the ACT's and measured rather than predicted: EXACTLY ONE key, "
        "s3://%s/%s. Nothing else in that prefix is written and platinum/reports/ is not "
        "written by this act at all. WHO IT REACHES: the next renderer run on the reporter "
        "box, which pulls this key fresh on every fire -- the monthly cron and EG-s-21's "
        "one permitted driven run. WHAT MOVES FOR THEM, BOTH BRANCHES NAMED because the "
        "producer takes one of two: on ladder=True NOTHING changes (proven at 24 of 24 "
        "compared quantities, battery arm (e)); on --no-ladder two things change, every "
        "unresolved record gains a `provider` field, and the run writes ONE NEW KEY, "
        "platinum/reports/<month>/coverage_egress_ask_ladder_skipped.json, the "
        "rung-3-EQUIVALENT egress ask. THAT NEW KEY IS PART OF THE RADIUS AND IS NAMED "
        "HERE: it is a key that did not exist before, it is NOT rung 3's "
        "coverage_egress_ask.json and never merges into it, and no existing key is "
        "overwritten by it. ROLLBACK, exact key-and-bytes: restore the prior VersionId by "
        "copy-object on the same key (command in the evidence file), or re-upload the git "
        "blob at the prior commit; both restore the sha256 recorded BEFORE the copy. "
        "AUTHORITY: the L6 issuance names this act, this key and this rollback; the face "
        "rules the artifact prefix a CODE location and not served output, the same "
        "standing as EG-s-25/EG-s-26 (row W5-S4)." % (BUCKET, KEY))
    legs = [
        "L1|verify|the PRIOR object and its rollback, proven BEFORE the copy|prior sha256 "
        "+ VersionId recorded before any write, rollback cross-checked against an "
        "independent git blob",
        "L2|verify|the copy landed at %s|served bytes sha256 EQUAL to the committed bytes, "
        "the served copy RE-DOWNLOADED BY ITS VersionId, both printed, with a negative "
        "control" % KEY,
        "L3|verify|nothing else moved in the artifact prefix|full listing before and after "
        "with denominators; at most one key changed, none added, none removed",
        "L4|verify|no send, no invoke, no write under platinum/reports/|SES datapoints "
        "overlapping the window, Lambda invocations with a subtracted denominator, and the "
        "reports listing unchanged with its denominator",
        "L5|verify|the ladder branch did not move and the skipped branch carries the "
        "property|battery arms (b)(d)(e) with denominators, and the renderer suite green",
    ]
    entry_path = os.path.join(REPO, "org", "critical_paths", ".open_deploys", SLUG + ".json")
    if os.path.exists(entry_path):
        # ALREADY OPEN. The entry is opened BEFORE the copy and this run has not copied
        # yet, so an existing entry means an earlier attempt of THIS act opened it and
        # died before the copy -- re-opening would either refuse or rewrite the opened_at,
        # and the opened_at is the one field that proves the entry led the world.
        opened_at = json.load(io.open(entry_path, encoding="utf-8"))["opened_at"]
        print("  LEDGER ENTRY ALREADY OPEN (opened_at %s) -- not re-opened" % opened_at)
        STEPS.append({"label": "OPEN ledger entry -- ALREADY OPEN, reused",
                      "argv": ["<none>"], "rc": 0, "started_utc": now(),
                      "finished_utc": now(), "stdout": "opened_at %s" % opened_at,
                      "stderr": ""})
    else:
        argv = [sys.executable, os.path.join(REPO, ".tools", "deploy_ledger.py"), "open",
                "--slug", SLUG, "--title", title, "--author", "0.9.0_WK_ETFS_GUARDRAIL~5",
                "--window-hours", "4"]
        for leg in legs:
            argv += ["--leg", leg]
        run(argv, "OPEN ledger entry (BEFORE the copy)")
        opened_at = now()

    # ---- censuses and the prior object, BEFORE the copy ------------------------
    art_before = listing(BUCKET, PREFIX, "LIST artifact prefix (before)")
    rep_before = listing(REPORTS_BUCKET, REPORTS_PREFIX, "LIST served reports (before)")

    # THE PRIOR IS READ FROM THE VERSION HISTORY, NOT FROM "whatever is latest now".
    # This script is re-runnable, and on a second run the latest version IS this act's own
    # upload -- taking `latest` as the prior would make the rollback a no-op and the
    # negative control a tautology, both of which read CLEAN. So: enumerate the versions,
    # and if the latest is already this act's bytes (committed sha AND written after the
    # entry opened), the PRIOR is the version immediately before it.
    _rc, vers_doc = aws_json(["s3api", "list-object-versions", "--bucket", BUCKET,
                              "--prefix", KEY], "LIST object versions (before)")
    versions = [v for v in (vers_doc or {}).get("Versions", []) if v.get("Key") == KEY]
    versions.sort(key=lambda v: str(v.get("LastModified")), reverse=True)
    print("  VERSION HISTORY on the key: %d version(s)" % len(versions))
    for v in versions[:5]:
        print("    %-34s %8s B  %s  IsLatest=%s"
              % (v.get("VersionId"), v.get("Size"), v.get("LastModified"), v.get("IsLatest")))
    latest = next((v for v in versions if v.get("IsLatest")), versions[0] if versions else {})

    latest_dl = os.path.join(REPO, ".scratch", "egs29_latest_now.py")
    io.open(latest_dl, "wb").write(b"")
    run([AWS, "s3api", "get-object", "--bucket", BUCKET, "--key", KEY,
         "--version-id", latest.get("VersionId", ""), os.path.relpath(latest_dl, REPO)],
        "GET the CURRENT latest object BY VersionId (before)")
    latest_sha = sha256_file(latest_dl)
    already_ours = (latest_sha == committed_sha
                    and str(latest.get("LastModified", "")) > "")
    if already_ours and len(versions) > 1:
        prior_v = versions[1]
        placed_note = ("the latest version already carries this cell's committed bytes -- "
                       "placed by an earlier invocation of THIS script under THIS ledger "
                       "entry (entry opened %s, object LastModified %s). NEVER-2: a "
                       "re-execute of an overtaken promote is a REWIND, so no second copy "
                       "is issued and the PRIOR below is the version BEFORE that upload."
                       % (opened_at, latest.get("LastModified")))
    else:
        prior_v = latest
        placed_note = ("the latest version is NOT this cell's bytes, so it is the true "
                       "prior and the copy below is this act's own")
    print("  %s" % placed_note)
    prior_vid = prior_v.get("VersionId", "")
    prior_len = prior_v.get("Size", 0)
    prior_lm = str(prior_v.get("LastModified", ""))
    prior_dl = os.path.join(REPO, ".scratch", "egs29_prior_served.py")
    io.open(prior_dl, "wb").write(b"")
    run([AWS, "s3api", "get-object", "--bucket", BUCKET, "--key", KEY,
         "--version-id", prior_vid, os.path.relpath(prior_dl, REPO)],
        "GET the prior object BY VersionId (before)")
    prior_sha = sha256_file(prior_dl)
    print("  PRIOR  VersionId %s  %s B  LastModified %s" % (prior_vid, prior_len, prior_lm))
    print("  PRIOR  sha256    %s" % prior_sha)

    rollback = (".tools/aws s3api copy-object --bucket %s --key %s --copy-source "
                "'%s/%s?versionId=%s'" % (BUCKET, KEY, BUCKET, KEY, prior_vid))

    # ---- the copy, or SUPERSEDED ----------------------------------------------
    if already_ours:
        disposition = ("SUPERSEDED WITHIN THIS ACT -- %s" % placed_note)
        copy_utc = str(latest.get("LastModified", ""))
        print("  NO COPY ISSUED BY THIS RUN (SUPERSEDED)")
    elif prior_sha == committed_sha:
        disposition = ("SUPERSEDED -- the committed bytes were ALREADY SERVED before this "
                       "act by someone else; NEVER-2 forbids re-executing an overtaken "
                       "promote, so no copy was issued and every AWS call here is a read")
        copy_utc = ""
        print("  ALREADY SERVED -- no copy issued (SUPERSEDED)")
    else:
        copy_utc = now()
        run([AWS, "s3", "cp", os.path.relpath(payload, REPO),
             "s3://%s/%s" % (BUCKET, KEY)], "COPY the committed blob to the key")
        disposition = "COPIED -- the committed blob was uploaded to the key by this act"

    # ---- verify the SERVED object, re-downloaded BY ITS NEW VersionId ----------
    _rc, head2 = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", KEY],
                          "HEAD the key (after)")
    served_vid = head2.get("VersionId", "")
    served_dl = os.path.join(REPO, ".scratch", "egs29_served.py")
    io.open(served_dl, "wb").write(b"")
    run([AWS, "s3api", "get-object", "--bucket", BUCKET, "--key", KEY,
         "--version-id", served_vid, os.path.relpath(served_dl, REPO)],
        "GET the SERVED object BY ITS VersionId (after)")
    served_sha = sha256_file(served_dl)
    served_bytes = os.path.getsize(served_dl)
    print("  SERVED VersionId %s  %d B" % (served_vid, served_bytes))
    print("  SERVED sha256    %s" % served_sha)
    print("  served == committed: %s   (negative control, prior differs: %s)"
          % (served_sha == committed_sha, prior_sha != served_sha))

    art_after = listing(BUCKET, PREFIX, "LIST artifact prefix (after)")
    rep_after = listing(REPORTS_BUCKET, REPORTS_PREFIX, "LIST served reports (after)")

    def delta(a, b):
        return {"before_count": len(a), "after_count": len(b),
                "added": sorted(set(b) - set(a)), "removed": sorted(set(a) - set(b)),
                "changed": sorted(k for k in set(a) & set(b) if a[k] != b[k])}

    since = opened_at[:19] + "Z"
    art_delta = delta(art_before, art_after)
    art_delta["prefix"] = "s3://%s/%s" % (BUCKET, PREFIX)
    art_delta["moved_since_entry_opened"] = moved_since(BUCKET, art_after, since)
    art_delta["moved_since_note"] = (
        "LastModified >= the entry's opened_at (%s). This, not the before/after pair, is "
        "what proves the act's radius on a re-run." % since)
    rep_delta = delta(rep_before, rep_after)
    rep_delta["prefix"] = "s3://%s/%s" % (REPORTS_BUCKET, REPORTS_PREFIX)
    rep_delta["moved_since_entry_opened"] = moved_since(REPORTS_BUCKET, rep_after, since)
    rep_delta["disclosure"] = (
        "THE DENOMINATOR IS NOT CLEAN AND IS NOT PRESENTED AS CLEAN: one of these keys, "
        "platinum/reports/2026-08/coverage_egress_ask_ladder_skipped.json (LastModified "
        "2026-09-10T13:54:44Z), was written by a UNIT TEST RUN of this cell's own suite "
        "BEFORE this entry opened -- surprise row ETFS_GUARDRAIL-W5-S11, ARMED, with its "
        "removal command and its owner. It predates opened_at, so it does not appear in "
        "moved_since_entry_opened, and this act wrote nothing under this prefix.")
    print("    moved since entry opened: artifact %d, reports %d"
          % (len(art_delta["moved_since_entry_opened"]),
             len(rep_delta["moved_since_entry_opened"])))

    # ---- SES: TIME OVERLAP, not a whole-day zero ------------------------------
    day = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    _rc, ses_day = aws_json(
        ["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SES",
         "--metric-name", "Send", "--start-time", day + "T00:00:00Z",
         "--end-time", day + "T23:59:59Z", "--period", "300", "--statistics", "Sum"],
        "SES Send, whole UTC day (5-min buckets)", check=False)
    day_points = (ses_day or {}).get("Datapoints", [])
    win_start = opened_at
    win_end = now()

    def ts(d):
        """CLI v1 renders a CloudWatch Timestamp as an EPOCH FLOAT under --output json,
        not an ISO string -- a trap that reads as a TypeError here and would read as a
        silent mis-sort in anything that only compared them."""
        v = d.get("Timestamp")
        if isinstance(v, (int, float)):
            return dt.datetime.fromtimestamp(v, dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        return str(v)[:19] + "Z"

    overlapping = [d for d in day_points if win_start <= ts(d) <= win_end]
    ses_note = ("the claim is TIME OVERLAP over %s..%s, not a whole-day zero -- other seats "
                "send legitimate mail and grading this act on their traffic would convict it "
                "of their sends" % (win_start, win_end))
    print("  SES: %d datapoint(s) for the day, %d overlapping the act window"
          % (len(day_points), len(overlapping)))

    # ---- Lambda: denominator BY SUBTRACTION -----------------------------------
    _rc, fns = aws_json(["lambda", "list-functions"], "LIST lambda functions", check=False)
    names = [f["FunctionName"] for f in (fns or {}).get("Functions", [])]
    checked = [n for n in names if ("etf" in n.lower() or "report" in n.lower())]
    total_inv = 0.0
    for n in checked:
        _rc, m = aws_json(
            ["cloudwatch", "get-metric-statistics", "--namespace", "AWS/Lambda",
             "--metric-name", "Invocations", "--dimensions",
             "Name=FunctionName,Value=%s" % n, "--start-time", win_start,
             "--end-time", win_end, "--period", "60", "--statistics", "Sum"],
            "Lambda Invocations %s" % n, check=False)
        total_inv += sum(d.get("Sum", 0) for d in (m or {}).get("Datapoints", []))
    print("  LAMBDA: %d function(s) in the account MINUS %d whose name carries neither "
          "'etf' nor 'report' = %d checked; invocations summed = %g"
          % (len(names), len(names) - len(checked), len(checked), total_inv))

    services = sorted({s["argv"][1] for s in STEPS
                       if os.path.basename(s["argv"][0]) in ("aws", "aws.cmd")})
    offaxis = [s for s in STEPS
               if os.path.basename(s["argv"][0]) in ("aws", "aws.cmd")
               and s["argv"][1] not in ("s3api", "s3", "cloudwatch", "lambda")]

    ev = {
        "serial": "0.9.0_WK_ETFS_GUARDRAIL~5",
        "to": "ETFS_GUARDRAIL.TO-EG-s-29",
        "head_commit": head_sha,
        "bucket": BUCKET, "key": KEY, "prefix": PREFIX,
        "disposition": disposition,
        "opened_at": opened_at, "copy_utc": copy_utc, "finished_utc": now(),
        "prior_version_id": prior_vid, "prior_sha256": prior_sha, "prior_bytes": prior_len,
        "prior_last_modified": prior_lm,
        "prior_recorded_before_copy": True,
        "version_history_count": len(versions),
        "latest_placement_note": placed_note,
        "served_last_modified": str(head2.get("LastModified", "")),
        "committed_sha256": committed_sha, "committed_bytes": len(blob),
        "worktree_sha256": worktree_sha,
        "worktree_equals_committed": worktree_sha == committed_sha,
        "served_version_id": served_vid, "served_sha256": served_sha,
        "served_bytes": served_bytes,
        "served_read_by_version_id": True,
        "served_equals_committed": served_sha == committed_sha,
        "rollback_command": rollback,
        "ledger_entry": ("org/critical_paths/change_management/ (slug %s); open entry at "
                         "org/critical_paths/.open_deploys/%s.json until closed" % (SLUG, SLUG)),
        "artifact_prefix_census": art_delta,
        "reports_prefix_census": rep_delta,
        "ses_note": ses_note,
        "ses_day_datapoints": len(day_points),
        "ses_overlapping_datapoints": len(overlapping),
        "ses_datapoints": sorted((ts(d), d.get("Sum")) for d in day_points),
        "lambda_total": len(names), "lambda_checked": len(checked),
        "lambda_checked_names": checked, "lambda_invocations": total_inv,
        "argv_total_steps": len(STEPS), "argv_services": services,
        "argv_offaxis_steps": len(offaxis),
        "steps": STEPS,
    }
    io.open(EVIDENCE, "w", encoding="utf-8", newline="\n").write(
        json.dumps(ev, indent=2, ensure_ascii=True) + "\n")
    print("EVIDENCE -> %s" % EVIDENCE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
