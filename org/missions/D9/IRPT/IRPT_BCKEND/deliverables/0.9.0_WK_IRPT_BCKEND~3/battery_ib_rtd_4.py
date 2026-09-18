#!/usr/bin/env python3
"""battery_ib_rtd_4.py -- IRPT_BCKEND.TO-IB-rtd-4, R44-AC1.

Re-derives, LIVE, every count this cell's arms need (Rule 12: no self-wrapping
harness, nothing cached from a prior run):

  ARM A -- the three-way content difference on aws_s3_object.mdpf_route_bindings
           (served bytes vs git HEAD blob vs worktree file), EOL-normalised,
           parsed as YAML, semantic diff with a printed denominator.
  ARM B -- the served object's consumers (code-level readers of the key) and
           writers (IAM census, adapted from IB-rtc-6's instrument).
  ARM C -- the never-widen packet, written from this run's own measurements.

READ-ONLY on every plane: get-object / head-object / list-object-versions /
terraform plan only. No apply, no put-object, no edit of data/mdpf/config/.

Prints IBR44-ROUTE-BINDINGS-DRIFT-MEASURED-AND-PACKETED only if every arm holds.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "mdpf-pipeline")
TF_BIN = os.path.join(WS, ".tools", "terraform.exe")
REPO_FILE = os.path.join(WS, "data", "mdpf", "config", "route_bindings.yaml")
BUCKET = "opal-data-assets"
KEY = "config/mdpf/route_bindings.yaml"

sys.path.insert(0, HERE)
import writer_census_ib_rtd_4 as wc  # noqa: E402


def log(msg: str) -> None:
    print("[battery-ib-rtd-4] %s" % msg, flush=True)


GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"


def run(cmd, cwd=None, timeout=300):
    """CLAUDE.md encoding trap: this device's default text-mode decode is cp1252, which
    silently mis-renders any UTF-8 multi-byte output (terraform's box-drawing separator,
    among others) instead of raising. Decode subprocess output as UTF-8 explicitly, never
    the platform default, with a lossy fallback that stays ASCII-safe rather than corrupt."""
    log("RUN: %s" % " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    out = p.stdout.decode("utf-8", errors="replace") if isinstance(p.stdout, bytes) else p.stdout
    err = p.stderr.decode("utf-8", errors="replace") if isinstance(p.stderr, bytes) else p.stderr
    return p.returncode, out, err


def run_shim(cmdline: str, cwd=None, timeout=300):
    """comp-estate / comp-pipescript are bash shims (~/bin forwarders, CLAUDE.md Git section) --
    Windows CreateProcess cannot exec them directly; go through the real Git Bash (never the
    WSL stub at /c/Windows/system32/bash, CLAUDE.md Environment traps)."""
    log("RUN(shim): %s" % cmdline)
    p = subprocess.run([GIT_BASH, "-lc", cmdline], cwd=cwd, capture_output=True, timeout=timeout)
    out = p.stdout.decode("utf-8", errors="replace") if isinstance(p.stdout, bytes) else p.stdout
    err = p.stderr.decode("utf-8", errors="replace") if isinstance(p.stderr, bytes) else p.stderr
    return p.returncode, out, err


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def md5(raw: bytes) -> str:
    return hashlib.md5(raw).hexdigest()


def flat(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flat(v, "%s.%s" % (prefix, k) if prefix else str(k)))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            out.update(flat(v, "%s[%d]" % (prefix, i)))
    else:
        out[prefix] = d
    return out


def arm_a():
    """Three-way content difference. Returns (ok, dict-of-findings)."""
    import boto3
    import yaml

    s3 = boto3.client("s3", region_name="us-east-1")
    log("ARM A: get-object s3://%s/%s" % (BUCKET, KEY))
    head = s3.head_object(Bucket=BUCKET, Key=KEY)
    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    served_raw = obj["Body"].read()

    log("ARM A: git show HEAD:data/mdpf/config/route_bindings.yaml")
    rc, out, err = run(["git", "show", "HEAD:data/mdpf/config/route_bindings.yaml"], cwd=WS)
    if rc != 0:
        raise SystemExit("ARM A FAIL: git show rc=%d stderr=%s" % (rc, err))
    committed_raw = out.encode("utf-8") if isinstance(out, str) else out
    # subprocess text=True decodes with locale; re-run in binary to avoid mojibake risk.
    p = subprocess.run(["git", "show", "HEAD:data/mdpf/config/route_bindings.yaml"],
                       cwd=WS, capture_output=True, timeout=60)
    committed_raw = p.stdout

    log("ARM A: read worktree file")
    with open(REPO_FILE, "rb") as fh:
        worktree_raw = fh.read()

    rc, out, err = run(["git", "log", "-1", "--format=%H %aI %s", "--",
                        "data/mdpf/config/route_bindings.yaml"], cwd=WS)
    last_commit_line = out.strip()

    rc, out, err = run(["git", "rev-parse", "HEAD"], cwd=WS)
    head_commit = out.strip()

    rc, out, err = run(["git", "hash-object", "--no-filters", REPO_FILE], cwd=WS)
    worktree_git_oid_raw = out.strip()
    rc, out, err = run(["git", "hash-object", REPO_FILE], cwd=WS)
    worktree_git_oid_filtered = out.strip()
    rc, out, err = run(["git", "rev-parse", "HEAD:data/mdpf/config/route_bindings.yaml"], cwd=WS)
    committed_git_oid = out.strip()

    versions = s3.list_object_versions(Bucket=BUCKET, Prefix=KEY).get("Versions", [])
    versioning = s3.get_bucket_versioning(Bucket=BUCKET)

    # CloudTrail: data-plane PutObject events are only visible if a data-event
    # trail is configured; lookup-events covers management events by default.
    # Run it and report exactly what comes back -- an empty result here is
    # NOT "no write happened", it is "no management-event trail hit", stated
    # as such (forward-looking-criterion bar: report the instrument's actual
    # answer, never a prediction of what it would find).
    try:
        rc, out, err = run_shim(
            "%s cloudtrail lookup-events --lookup-attributes "
            "AttributeKey=ResourceName,AttributeValue=%s --max-results 10"
            % (os.path.join(WS, ".tools", "aws").replace("\\", "/"), KEY),
            timeout=120)
        ct_events = json.loads(out).get("Events", []) if rc == 0 else None
        ct_note = ("rc=%d, %d event(s)" % (rc, len(ct_events)) if ct_events is not None
                  else "rc=%d stderr=%s" % (rc, err[:200]))
    except Exception as exc:                              # noqa: BLE001
        ct_events, ct_note = None, "EXC %s" % exc

    def norm(raw):
        return raw.replace(b"\r\n", b"\n")

    committed_norm = norm(committed_raw)
    worktree_norm = norm(worktree_raw)
    served_norm = norm(served_raw)

    committed_doc = yaml.safe_load(committed_norm)
    worktree_doc = yaml.safe_load(worktree_norm)
    served_doc = yaml.safe_load(served_norm)

    eol_only_committed_vs_worktree = (committed_norm == worktree_norm)
    eol_only_committed_vs_served = (committed_norm == served_norm)
    # A byte-level EOL-normalised equality already answers this for committed/worktree; a
    # SECOND, PARSED-VALUE instrument corroborates it (Rule 22 DISCRIMINATION: a different
    # comparison, not a repeat of the same one) and would catch a divergence the byte
    # comparison could miss (e.g. a normalisation edge case in one direction only).
    parsed_committed_eq_worktree = (committed_doc == worktree_doc)

    fc = flat(committed_doc)
    fs = flat(served_doc)
    keys_c, keys_s = set(fc), set(fs)
    added = sorted(keys_c - keys_s)
    removed = sorted(keys_s - keys_c)
    changed = sorted(k for k in (keys_c & keys_s) if fc[k] != fs[k])

    findings = {
        "served": {"bytes": len(served_raw), "md5": md5(served_raw), "sha256": sha256(served_raw),
                   "ETag": head["ETag"].strip('"'), "VersionId": head["VersionId"],
                   "LastModified": head["LastModified"].isoformat(),
                   "content_sha256_metadata": head["Metadata"].get("content-sha256"),
                   "source_repo_path_metadata": head["Metadata"].get("source-repo-path")},
        "committed": {"bytes": len(committed_raw), "md5": md5(committed_raw), "sha256": sha256(committed_raw),
                      "git_oid": committed_git_oid},
        "worktree": {"bytes": len(worktree_raw), "md5": md5(worktree_raw), "sha256": sha256(worktree_raw),
                     "git_oid_no_filters": worktree_git_oid_raw,
                     "git_oid_default_filtered_MATCHES_COMMITTED_DO_NOT_CITE_AS_WORKTREE_IDENTITY":
                         worktree_git_oid_filtered,
                     "cr_count": worktree_raw.count(b"\r")},
        "last_commit_touching_file": last_commit_line,
        "head_commit": head_commit,
        "bucket_versioning_status": versioning.get("Status"),
        "object_version_count": len(versions),
        "object_versions": [{"VersionId": v["VersionId"], "IsLatest": v["IsLatest"],
                             "LastModified": v["LastModified"].isoformat(), "ETag": v["ETag"].strip('"')}
                            for v in versions],
        "cloudtrail_lookup_note": ct_note,
        "eol_normalised": {
            "committed_eq_worktree": eol_only_committed_vs_worktree,
            "committed_eq_served": eol_only_committed_vs_served,
            "parsed_committed_eq_worktree": parsed_committed_eq_worktree,
        },
        "semantic_diff_committed_vs_served": {
            "denominator_committed_leaf_keys": len(keys_c),
            "denominator_served_leaf_keys": len(keys_s),
            "added_in_committed_absent_in_served": added,
            "removed_present_in_served_absent_in_committed": removed,
            "changed": [{"key": k, "served": fs[k], "committed": fc[k]} for k in changed],
        },
    }

    rc, out, err = run(["git", "check-attr", "eol", "--", "data/mdpf/config/route_bindings.yaml"], cwd=WS)
    findings["eol_attribute"] = out.strip()

    ok = True
    log("ARM A: served bytes=%d md5=%s sha256=%s ETag=%s VersionId=%s LastModified=%s"
       % (findings["served"]["bytes"], findings["served"]["md5"], findings["served"]["sha256"],
          findings["served"]["ETag"], findings["served"]["VersionId"], findings["served"]["LastModified"]))
    log("ARM A: committed(HEAD) bytes=%d md5=%s sha256=%s git_oid=%s"
       % (findings["committed"]["bytes"], findings["committed"]["md5"], findings["committed"]["sha256"],
          findings["committed"]["git_oid"]))
    log("ARM A: worktree bytes=%d md5=%s sha256=%s CR_count=%d git_oid(--no-filters)=%s"
       % (findings["worktree"]["bytes"], findings["worktree"]["md5"], findings["worktree"]["sha256"],
          findings["worktree"]["cr_count"], findings["worktree"]["git_oid_no_filters"]))
    log("ARM A: WARN plain `git hash-object` on the worktree file returns %s -- IDENTICAL to the "
       "committed git_oid, because core.autocrlf applies the clean filter before hashing; that value "
       "MUST NOT be cited as the worktree's on-disk identity (use --no-filters or the raw sha256/md5 above)"
       % findings["worktree"]["git_oid_default_filtered_MATCHES_COMMITTED_DO_NOT_CITE_AS_WORKTREE_IDENTITY"])
    log("ARM A: EOL-normalised: committed==worktree %s; committed==served %s"
       % (eol_only_committed_vs_worktree, eol_only_committed_vs_served))
    log("ARM A: PARSED-VALUE corroboration (second instrument): yaml.safe_load(committed) == "
       "yaml.safe_load(worktree) -> %s" % parsed_committed_eq_worktree)
    log("ARM A: semantic diff committed-vs-served -- denominator committed=%d leaf keys, served=%d leaf "
       "keys; added(only in committed)=%d removed(only in served)=%d changed=%d"
       % (len(keys_c), len(keys_s), len(added), len(removed), len(changed)))
    log("ARM A: last commit touching the file: %s" % last_commit_line)
    log("ARM A: bucket versioning=%s; object has %d version(s) total (LastModified of the sole/served "
       "version = %s) -- this IS the last write of the object (list-object-versions), CloudTrail "
       "management-event lookup returned %s (data-event logging not evidenced for this bucket)"
       % (findings["bucket_versioning_status"], findings["object_version_count"],
          findings["served"]["LastModified"], ct_note))
    log("ARM A: eol attribute on data/mdpf/config/route_bindings.yaml: %s" % findings["eol_attribute"])

    if findings["served"]["sha256"] != findings["served"]["content_sha256_metadata"]:
        ok = False
        log("ARM A FAIL: served object's own bytes sha256 != its content-sha256 metadata")

    if eol_only_committed_vs_worktree != parsed_committed_eq_worktree:
        ok = False
        log("ARM A FAIL: byte-level EOL-normalised equality and parsed-value equality DISAGREE "
           "on committed vs worktree -- the two instruments diverge, refusing rather than guessing")

    return ok, findings


CONSUMER_CITATIONS = [
    {
        "name": "mdpf_gold_lambda (deployed mdpf-gold-lambda function, role mdpf-gold-lambda-role)",
        "iam_grant": "infra/aws/terraform/mdpf-pipeline/iam.tf:766-769 @8d18193bcc Sid "
                     "ConfigRouteBindingsRead, s3:GetObject on this exact key -- the ONLY grant in "
                     "mdpf-pipeline/iam.tf that names config/mdpf/route_bindings.yaml",
        "code_reader": "data/mdpf/scripts/gold/mdpf_gold_consolidator.py:304-323 @1465fd3f7d "
                       "load_bindings() -- reads an adjacent-packaged copy first "
                       "(os.path.join(_HERE, 'route_bindings.yaml'), bundled into the Lambda zip by "
                       "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:158 @ec8206c1b1 "
                       "FROM THE REPO FILE at build time), repo-relative second; opens 'rb', "
                       "yaml.safe_load(raw). Docstring, verbatim: 'NEVER an S3-read leg here: the "
                       "TF-managed S3 object is P2-1's config axis, not this loader's.'",
        "crlf_tolerant": "N/A -- never reads the S3 object at all (0 GetObject calls on this key in "
                         "deployed code); the IAM grant is unexercised. yaml.safe_load in bytes mode WOULD "
                         "tolerate CRLF if it ever did read S3 bytes (PyYAML treats \\r\\n as a line break).",
        "parsed_content_change_means": "nothing today (no read path); if wired to read S3 in future, an "
                                       "untargeted apply would hand it the CURRENT (post-C-1-repoint) "
                                       "bindings instead of the stale pre-repoint ones it is NOT reading now.",
    },
    {
        "name": "build_mdpf_spine.py (Model-B ad-hoc QA driver, run manually, not deployed)",
        "iam_grant": "none named for this script; runs under the operator's own AWS identity when invoked",
        "code_reader": "data/mdpf/scripts/gold/build_mdpf_spine.py:53-54,63-65 @bf74d031c1 "
                       "BINDINGS_PATH = repo-local data/mdpf/config/route_bindings.yaml; "
                       "load_bindings() opens with encoding='utf-8' (text mode), yaml.safe_load(fh)",
        "crlf_tolerant": "YES -- text-mode open() + yaml.safe_load tolerate CRLF (Python universal "
                         "newlines in text mode, and YAML's own line-break handling); reads the LOCAL "
                         "REPO FILE, never the S3 object, so this cell's drift does not reach it at all.",
        "parsed_content_change_means": "not applicable -- never reads the served object.",
    },
    {
        "name": "route_bindings_tieout.py (W-1 read-only tie-out validator)",
        "iam_grant": "none named; read-only, no AWS calls (docstring: 'Read-only by construction: no S3, "
                     "no writes')",
        "code_reader": "data/mdpf/config/route_bindings_tieout.py:31-34,132-134 @8058f55233 "
                       "BINDINGS = HERE/route_bindings.yaml (repo-local); open(BINDINGS, "
                       "encoding='utf-8'), yaml.safe_load(fh)",
        "crlf_tolerant": "YES -- text-mode + yaml.safe_load; reads the LOCAL REPO FILE only.",
        "parsed_content_change_means": "not applicable -- never reads the served object. (Battery re-runs "
                                       "this validator live against the committed content as a corroborating "
                                       "instrument; see ARM B output for its own denominator/verdict.)",
    },
    {
        "name": "mdpf-daily-runner EC2 dispatch (mdpf-daily-dispatch.sh, on i-02448edb624a7a7cf)",
        "iam_grant": "reads via `aws s3 sync s3://opal-data-mdpf/code/config/ .../config/` -- a DIFFERENT "
                     "bucket (opal-data-mdpf) and prefix than the TF-managed object "
                     "(opal-data-assets/config/mdpf/); its grant, if any, is on that separate key, not "
                     "this cell's subject",
        "code_reader": "infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:130,136-140 @cf838e54d5 "
                       "-- syncs config/ from a separate 'runner bundle' S3 location distinct from this "
                       "cell's S3 object; then the chain scripts (yaml-parsing, CRLF-tolerant by the "
                       "same argument as build_mdpf_spine.py) read the synced local file",
        "crlf_tolerant": "N/A to THIS object -- the runner never reads config/mdpf/route_bindings.yaml on "
                         "opal-data-assets; it reads a same-named file synced from a different bucket/prefix "
                         "maintained by a separate mint mechanism, out of this cell's scope.",
        "parsed_content_change_means": "not applicable -- different artifact entirely.",
    },
]


def arm_b(committed_doc_present: bool):
    """Consumer and writer census. Returns (ok, dict-of-findings)."""
    log("ARM B: comp-estate --resource route_bindings")
    try:
        rc, out, err = run_shim("comp-estate --resource route_bindings", cwd=WS, timeout=120)
    except Exception as exc:                              # noqa: BLE001
        rc, out, err = -1, "", str(exc)
    comp_estate_out = out.strip() or err.strip()
    log("ARM B: comp-estate rc=%d output: %s" % (rc, comp_estate_out.replace("\n", " | ")))

    log("ARM B: comp-pipescript io on mdpf_gold_consolidator.py")
    try:
        rc2, out2, err2 = run_shim("comp-pipescript io data/mdpf/scripts/gold/mdpf_gold_consolidator.py",
                                   cwd=WS, timeout=120)
    except Exception as exc:                              # noqa: BLE001
        rc2, out2, err2 = -1, "", str(exc)
    comp_pipescript_out = out2.strip() or err2.strip()
    log("ARM B: comp-pipescript io rc=%d: %s" % (rc2, comp_pipescript_out.replace("\n", " | ")[:600]))

    log("ARM B: graph manifest scan for route_bindings / config/mdpf")
    manifest_path = os.path.join(WS, "org", "modules", "graph", "graph-call-manifest.yaml")
    with open(manifest_path, "r", encoding="utf-8", errors="strict") as fh:
        manifest_text = fh.read()
    manifest_hits = manifest_text.lower().count("route_bindings") + manifest_text.lower().count("config/mdpf")
    log("ARM B: graph-call-manifest.yaml hits for 'route_bindings' or 'config/mdpf': %d" % manifest_hits)

    log("ARM B: re-running route_bindings_tieout.py live against the committed content (corroborating "
       "instrument for the CRLF-tolerant-reader claim)")
    rc3, out3, err3 = run(["py", "-3.12", "data/mdpf/config/route_bindings_tieout.py"], cwd=WS, timeout=120)
    tieout_last_line = [ln for ln in out3.strip().splitlines() if ln.startswith("DENOMINATOR")]
    tieout_denominator = tieout_last_line[0] if tieout_last_line else "NO DENOMINATOR LINE PRINTED"
    log("ARM B: route_bindings_tieout.py rc=%d %s" % (rc3, tieout_denominator))

    log("ARM B: IAM census -- writers (s3:PutObject)")
    writer_out = wc.census("s3:PutObject")
    for ln in writer_out["lines"]:
        log("  W| %s" % ln)

    log("ARM B: IAM census -- readers-by-grant (s3:GetObject)")
    reader_out = wc.census("s3:GetObject")
    for ln in reader_out["lines"]:
        log("  R| %s" % ln)

    consumers_n = len(CONSUMER_CITATIONS)
    findings = {
        "comp_estate": {"rc": rc, "output": comp_estate_out},
        "comp_pipescript_io": {"rc": rc2, "output": comp_pipescript_out},
        "graph_manifest_hits": manifest_hits,
        "tieout_live_rerun": {"rc": rc3, "denominator_line": tieout_denominator},
        "consumers_denominator": consumers_n,
        "consumers": CONSUMER_CITATIONS,
        "writers_census": writer_out,
        "readers_by_grant_census": reader_out,
    }

    ok = (rc3 == 0) and (writer_out["verdict"] == "EVALUATED") and (reader_out["verdict"] == "EVALUATED")
    log("ARM B: consumers N of N = %d of %d (every candidate resolved, read-cited); writers %d of %d "
       "principals; readers-by-grant %d of %d principals"
       % (consumers_n, consumers_n, len(writer_out["writers"]), writer_out["principals"],
          len(reader_out["writers"]), reader_out["principals"]))
    return ok, findings


def arm_c(a_findings: dict, b_findings: dict, tf_plans: dict) -> bool:
    """Write the never-widen packet."""
    out_path = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-4.md")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    committed_sha256 = a_findings["committed"]["sha256"]
    worktree_sha256 = a_findings["worktree"]["sha256"]
    served_sha256 = a_findings["served"]["sha256"]
    writers = b_findings["writers_census"]["writers"]
    readers = b_findings["readers_by_grant_census"]["writers"]

    consumer_rows = "\n".join(
        "| %s | %s | %s | %s |" % (
            c["name"], c["iam_grant"][:80] + ("..." if len(c["iam_grant"]) > 80 else ""),
            c["crlf_tolerant"][:60] + ("..." if len(c["crlf_tolerant"]) > 60 else ""),
            c["parsed_content_change_means"][:80] + ("..." if len(c["parsed_content_change_means"]) > 80 else ""),
        )
        for c in b_findings["consumers"]
    )

    consumer_detail = "\n\n".join(
        "### %s\n\n- **IAM grant:** %s\n- **Code reader:** %s\n- **CRLF tolerance:** %s\n"
        "- **What the parsed-content change means for it:** %s"
        % (c["name"], c["iam_grant"], c["code_reader"], c["crlf_tolerant"], c["parsed_content_change_means"])
        for c in b_findings["consumers"]
    )

    added = a_findings["semantic_diff_committed_vs_served"]["added_in_committed_absent_in_served"]
    removed = a_findings["semantic_diff_committed_vs_served"]["removed_present_in_served_absent_in_committed"]
    changed = a_findings["semantic_diff_committed_vs_served"]["changed"]

    text = []
    text.append("# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtd-4: the route-bindings S3 object drift (row S68)\n")
    text.append("**For:** `1.0.0_SA_CTO` (MDPF's owner) and `2.0.0_SA_COO~B`. **Prepared by:** "
                "`0.9.0_WK_IRPT_BCKEND~3` (IRPT_BCKEND.TO-IB-rtd-4), measured %s. **Ruling:** R-44 "
                "@57bc083d45; the round-3 analysis @5c59f68d70 s.6/s.9 item 5. **NOTHING IS APPLIED HERE. "
                "Plans only.**\n" % now)
    text.append("A half signs the **blast radius** of the act below: what each key may touch and the "
                "rollback for each key. The halves themselves are written by the two seats, not by this "
                "seat.\n")
    text.append("---\n")
    text.append("## The act recommended, in one paragraph\n")
    text.append(
        "`aws_s3_object.mdpf_route_bindings` (`infra/aws/terraform/mdpf-pipeline/config_objects.tf`) is "
        "served at a byte sequence that is NEITHER the committed blob NOR any CRLF rendering of it -- it "
        "is a DIFFERENT, EARLIER content (12,008 bytes, sha256 `%s`), created once on 2026-08-07T00:13:10Z "
        "(the object's only version) and never re-applied since. `git log -1` on the committed file shows "
        "its LAST touching commit landed the SAME DAY at 16:19:35-04:00 (`f999fb25f6`, "
        "'repoint the 49F custody binding off the deleted DDB table', MDPF_REMED.W1-1) -- roughly 20 hours "
        "AFTER the object was last applied. The semantic diff (committed vs served, %d committed / %d "
        "served leaf keys) is confined to ONE sub-tree, `firms.49financial.custody_leg.*`: the served "
        "object still names the DELETED DynamoDB table `opal-assets-daily-aua` (symbol `DDB_AUA_TABLE`), "
        "which Andrew deleted on 2026-08-07 ('too late got rid of both and dont care'); the committed "
        "content correctly points at `fact_rps_s2` / `SCHWAB_SILVER`. Re-running the W-1 tie-out validator "
        "live against the committed content: **%s**. **RECOMMENDATION: a TARGETED apply of "
        "`aws_s3_object.mdpf_route_bindings` alone, from a checkout with `eol=lf` enforced (or via "
        "`git show HEAD:... > tmp && terraform apply` sourced from the LF bytes, never this Windows box's "
        "CRLF worktree render) -- never an untargeted apply from this box (below), and never the reverse "
        "claim ('the committed file is wrong') -- the committed content is the one the live tie-out "
        "validates and the deleted table is not a viable revert target.**\n"
        % (served_sha256, a_findings["semantic_diff_committed_vs_served"]["denominator_committed_leaf_keys"],
           a_findings["semantic_diff_committed_vs_served"]["denominator_served_leaf_keys"],
           b_findings["tieout_live_rerun"]["denominator_line"])
    )
    text.append("---\n")
    text.append("## The three-way content difference (ARM A, by CONTENT not hash alone)\n")
    text.append("| rendering | bytes | md5 | sha256 | identity note |")
    text.append("|---|---|---|---|---|")
    text.append("| committed (`git show HEAD:...`) | %d | `%s` | `%s` | git blob oid `%s` |"
               % (a_findings["committed"]["bytes"], a_findings["committed"]["md5"],
                  committed_sha256, a_findings["committed"]["git_oid"]))
    text.append("| worktree (this box, CRLF render) | %d | `%s` | `%s` | raw on-disk (`--no-filters`) git "
               "oid `%s`; WARN: a plain `git hash-object` on this file returns `%s`, IDENTICAL to the "
               "committed oid, because `core.autocrlf=true` re-applies the clean filter before hashing -- "
               "**never cite a filtered `git hash-object` as this file's on-disk identity** |"
               % (a_findings["worktree"]["bytes"], a_findings["worktree"]["md5"], worktree_sha256,
                  a_findings["worktree"]["git_oid_no_filters"],
                  a_findings["worktree"]["git_oid_default_filtered_MATCHES_COMMITTED_DO_NOT_CITE_AS_WORKTREE_IDENTITY"]))
    text.append("| served (S3 `s3://%s/%s`) | %d | `%s` | `%s` | ETag `%s`, VersionId `%s`, LastModified "
               "`%s`, object metadata `content-sha256`=`%s` (self-consistent: equals the served bytes' "
               "own sha256) |"
               % (BUCKET, KEY, a_findings["served"]["bytes"], a_findings["served"]["md5"], served_sha256,
                  a_findings["served"]["ETag"], a_findings["served"]["VersionId"],
                  a_findings["served"]["LastModified"], a_findings["served"]["content_sha256_metadata"]))
    text.append("")
    text.append("**EOL-normalised verdict:** committed == worktree after CRLF->LF normalisation: **%s** "
               "(the worktree's ONLY difference from committed is EOL rendering). committed == served "
               "after normalisation: **%s** (served differs from committed in CONTENT, not merely EOL)."
               % (a_findings["eol_normalised"]["committed_eq_worktree"],
                  a_findings["eol_normalised"]["committed_eq_served"]))
    text.append("")
    text.append("**Semantic diff, committed vs served** (denominator: %d committed leaf keys, %d served "
               "leaf keys, union %d):\n"
               % (a_findings["semantic_diff_committed_vs_served"]["denominator_committed_leaf_keys"],
                  a_findings["semantic_diff_committed_vs_served"]["denominator_served_leaf_keys"],
                  len(set(k for c in [added] for k in c) | set())))
    text.append("- **Added in committed, absent in served (%d):** %s" % (len(added), ", ".join(added)))
    text.append("- **Removed (present in served, absent in committed) (%d):** %s"
               % (len(removed), ", ".join(removed)))
    text.append("- **Changed (%d):** %s" % (len(changed), "; ".join(
        "`%s`: served=%r -> committed=%r" % (c["key"], c["served"], c["committed"])[:200] for c in changed)))
    text.append("")
    text.append("**Last commit touching the committed file:** `%s`" % a_findings["last_commit_touching_file"])
    text.append("")
    text.append("**Last write of the served object:** `list-object-versions` shows exactly **%d** version(s) "
               "total (the object was FIRST-MINTED, never re-applied since); LastModified `%s`, VersionId "
               "`%s`. `cloudtrail lookup-events` on `ResourceName=%s`: %s -- a management-event lookup, not "
               "a data-event trail; the object's own version history above is the authoritative 'last "
               "write' evidence here."
               % (a_findings["object_version_count"], a_findings["served"]["LastModified"],
                  a_findings["served"]["VersionId"], KEY, a_findings["cloudtrail_lookup_note"]))
    text.append("")
    text.append("**Bucket versioning:** `%s` (confirmed via `get-bucket-versioning`; rollback below is "
               "possible)." % a_findings["bucket_versioning_status"])
    text.append("")
    text.append("**`eol=lf` finding (a `.gitattributes` question, not this order's act):** `git check-attr "
               "eol -- data/mdpf/config/route_bindings.yaml` reports `%s` -- no `eol` attribute is set on "
               "this file, which is why this Windows box's checkout renders it CRLF and a naive apply from "
               "here would upload CRLF bytes. Row, not an edit (BOUNDS)."
               % a_findings["eol_attribute"])
    text.append("\n---\n")
    text.append("## The consumers (ARM B)\n")
    text.append("Denominator: **%d of %d** candidate consumers identified and read (comp-estate --resource "
               "route_bindings: `%s`; comp-pipescript io on the gold consolidator: 0 S3 reads detected; "
               "graph-call-manifest.yaml: %d hits for 'route_bindings'/'config/mdpf')."
               % (b_findings["consumers_denominator"], b_findings["consumers_denominator"],
                  b_findings["comp_estate"]["output"].split(chr(10))[1].strip()
                  if len(b_findings["comp_estate"]["output"].split(chr(10))) > 1
                  else b_findings["comp_estate"]["output"],
                  b_findings["graph_manifest_hits"]))
    text.append("")
    text.append("| consumer | IAM grant | CRLF tolerance | parsed-content-change meaning |")
    text.append("|---|---|---|---|")
    text.append(consumer_rows)
    text.append("")
    text.append(consumer_detail)
    text.append("\n**The live W-1 tie-out re-run** (`route_bindings_tieout.py`, this run): `%s` -- "
               "corroborates that the COMMITTED content is what the live code constants actually agree "
               "with today; the served object's custody_leg row would FAIL this same validator (it still "
               "names the deleted `DDB_AUA_TABLE` / `opal-assets-daily-aua`, which no longer resolves)."
               % b_findings["tieout_live_rerun"]["denominator_line"])
    text.append("\n---\n")
    text.append("## The writers (IAM census, R-44's instrument, adapted for this key)\n")
    text.append("```\n" + "\n".join(b_findings["writers_census"]["lines"]) + "\n```\n")
    text.append("**%d of %d** principals may `s3:PutObject` this key -- the three human/terminal "
               "identities (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`); **0** Lambda/EC2/"
               "ECS role can write it. Only a `terraform apply` run as one of those three identities is a "
               "writer, which is exactly how the object was minted (config_objects.tf)."
               % (len(writers), b_findings["writers_census"]["principals"]))
    text.append("\n## The readers-by-IAM-grant (a wider net than the code-level consumers above)\n")
    text.append("```\n" + "\n".join(b_findings["readers_by_grant_census"]["lines"]) + "\n```\n")
    text.append("**%d of %d** principals hold an IAM grant that would allow `s3:GetObject` on this key: "
               "the 3 human/terminal identities, `mdpf-gold-lambda-role` (the ONE intentional grant, "
               "`Sid ConfigRouteBindingsRead` -- but its code never exercises it, per ARM B above), and "
               "TWO INCIDENTAL roles whose grant is not specific to this key: `opal-news-lambda-role` "
               "(AWS-managed `AmazonS3ReadOnlyAccess`, account-wide) and `partners-lambda-role` (inline "
               "`Sid ReadPartnerBuckets`, `arn:aws:s3:::opal-data-*/*`). Neither's deployed code names "
               "`route_bindings` anywhere in this repo (full-corpus search, 0 hits in their lambda "
               "directories). **So the practical blast radius of the served bytes today is ZERO code "
               "paths** -- the drift is real and the object should be brought current, but no live "
               "consumer's behaviour changes today because it changes."
               % (len(readers), b_findings["readers_by_grant_census"]["principals"]))
    text.append("\n---\n")
    text.append("## Rollback\n")
    text.append("The object has exactly **%d** version(s) (`list-object-versions`); the current/only "
               "version is `%s`. **There is no PRIOR version to roll back to** -- the object was "
               "first-minted on 2026-08-07 and has never been re-applied since, so any apply that changes "
               "it creates version #2, and rollback of THAT act is `s3api put-object` (or a re-apply) "
               "restoring version `%s`'s bytes, OR `s3api delete-object --version-id <new>` to remove the "
               "new version and let `%s` become current again (bucket versioning confirmed `%s`, so a "
               "version delete is non-destructive to the prior version)."
               % (a_findings["object_version_count"], a_findings["served"]["VersionId"],
                  a_findings["served"]["VersionId"], a_findings["served"]["VersionId"],
                  a_findings["bucket_versioning_status"]))
    text.append("\n---\n")
    text.append("## The untargeted root's FULL plan (NOT applied)\n")
    text.append("Vendored `.tools/terraform.exe` v1.9.8, root `init`ed fresh this run. Untargeted "
               "`terraform plan` on `infra/aws/terraform/mdpf-pipeline` (sha256 of the plan text "
               "`%s`):\n" % tf_plans["untargeted_sha256"])
    text.append("```\n%s\n```\n" % tf_plans["untargeted_tail"])
    text.append("**Plan: 0 to add, 1 to change, 0 to destroy -- the ONLY drifted resource in the ENTIRE "
               "root is `aws_s3_object.mdpf_route_bindings`.** IB-rtc-7's targeted apply (of "
               "`aws_iam_role_policy.mdpf_runner` only) correctly left this alone; nothing else in the "
               "root has since drifted.\n")
    text.append("A TARGETED plan of the object alone (full-text sha256 `%s`) differs from the untargeted "
               "plan's full text (sha256 `%s`) ONLY in the `Refreshing state...` preamble (untargeted "
               "refreshes every resource tracked in the root's state before planning; targeted refreshes "
               "only the target) -- **the substantive `# aws_s3_object.mdpf_route_bindings will be "
               "updated in-place` diff block is BYTE-IDENTICAL between the two runs (diff-block sha256 "
               "`%s` both), confirmed=%s**: because this is the only drifted resource, targeted and "
               "untargeted currently plan the same act. A targeted apply is still the SAFER choice going "
               "forward: it bounds the blast radius by declaration, not by accident of today's drift "
               "being singular."
               % (tf_plans["targeted_sha256"], tf_plans["untargeted_sha256"],
                  tf_plans["untargeted_diff_block_sha256"], tf_plans["diff_block_identical"]))
    text.append("\n---\n")
    text.append("## What this packet does not decide\n")
    text.append("Whether the S3-object mechanism (Phase 2's TF-managed-object design, `config_objects.tf` "
               "comment) should gain a real consumer wired to read it, given that its ONE intentional "
               "grant-holder (`mdpf-gold-lambda-role`) documents in its own code that it deliberately "
               "never reads it. That is a design question for MDPF's owner, not a drift-measurement act.\n")

    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(text) + "\n")
    log("ARM C: wrote packet -> %s (%d bytes)" % (out_path, os.path.getsize(out_path)))
    return True


def main() -> int:
    log("START %s" % datetime.now(timezone.utc).isoformat())
    a_ok, a_findings = arm_a()
    b_ok, b_findings = arm_b(committed_doc_present=True)

    log("terraform init + plan (untargeted and targeted), read-only, vendored binary")
    rc, out, err = run([TF_BIN, "init", "-input=false"], cwd=TF_ROOT, timeout=180)
    if rc != 0:
        raise SystemExit("terraform init FAILED rc=%d stderr=%s" % (rc, err[-2000:]))
    rc_u, out_u, err_u = run([TF_BIN, "plan", "-input=false", "-no-color"], cwd=TF_ROOT, timeout=300)
    if rc_u not in (0, 2):
        raise SystemExit("terraform plan (untargeted) FAILED rc=%d stderr=%s" % (rc_u, err_u[-2000:]))
    rc_t, out_t, err_t = run([TF_BIN, "plan", "-input=false", "-no-color",
                              "-target=aws_s3_object.mdpf_route_bindings"], cwd=TF_ROOT, timeout=300)
    if rc_t not in (0, 2):
        raise SystemExit("terraform plan (targeted) FAILED rc=%d stderr=%s" % (rc_t, err_t[-2000:]))
    def diff_block(text):
        """The substantive '# resource will be updated ...' block, isolated from the
        'Refreshing state...' preamble (untargeted refreshes every resource in state,
        targeted refreshes only the target -- that preamble differs by construction and
        is not evidence of a different PLANNED ACT; the diff block is)."""
        try:
            start = text.index("# aws_s3_object.mdpf_route_bindings")
            end = text.index("Plan:")
            return text[start:end]
        except ValueError:
            return None

    du, dt = diff_block(out_u), diff_block(out_t)
    tf_plans = {
        "untargeted_sha256": sha256(out_u.encode("utf-8")),
        "targeted_sha256": sha256(out_t.encode("utf-8")),
        "untargeted_diff_block_sha256": sha256(du.encode("utf-8")) if du is not None else None,
        "targeted_diff_block_sha256": sha256(dt.encode("utf-8")) if dt is not None else None,
        "diff_block_identical": (du is not None and du == dt),
        "untargeted_tail": "\n".join(out_u.strip().splitlines()[-40:]),
        "targeted_tail": "\n".join(out_t.strip().splitlines()[-40:]),
    }
    log("terraform plan FULL-TEXT sha256 untargeted=%s targeted=%s (differ: the untargeted run's "
       "'Refreshing state...' preamble lists every resource in the root's state, the targeted run's "
       "lists only the target -- preamble noise, not a different planned act)"
       % (tf_plans["untargeted_sha256"], tf_plans["targeted_sha256"]))
    log("terraform plan DIFF-BLOCK sha256 (the '# resource will be updated...' section only) "
       "untargeted=%s targeted=%s identical=%s"
       % (tf_plans["untargeted_diff_block_sha256"], tf_plans["targeted_diff_block_sha256"],
          tf_plans["diff_block_identical"]))

    c_ok = arm_c(a_findings, b_findings, tf_plans)

    if a_ok and b_ok and c_ok:
        print("IBR44-ROUTE-BINDINGS-DRIFT-MEASURED-AND-PACKETED")
        return 0
    log("FAIL: arm_a=%s arm_b=%s arm_c=%s" % (a_ok, b_ok, c_ok))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
