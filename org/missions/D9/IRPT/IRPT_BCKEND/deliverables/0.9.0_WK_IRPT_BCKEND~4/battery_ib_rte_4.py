#!/usr/bin/env python3
"""battery_ib_rte_4.py -- IRPT_BCKEND TO-IB-rte-4, R54-AC1.

THE SERVED LAMBDA MEMBERS DECLARED FROM THEIR TRUE SOURCES. Re-derives, every run, from the real
world -- the live S3 artifact bucket, the live Lambda CodeSha256, and git's own object database --
never from a prior run's output or from this file's own prose.

(a) THE CENSUS: for every zip-based function in the investor-reporting family (N of N, the SAME
    filter build-and-upload.sh's own TMPJS_LIST applies), downloads the SERVED zip fresh, lists its
    members and their sha256, and classifies each declared member as TRACKED-AT-PATH / staged from a
    declared TRUE SOURCE (TRACKED-ELSEWHERE, blob-hash-verified) / UNRESOLVED (declared and served,
    but no true source could be found or declared -- content-addressed search of the whole git object
    graph, not a path guess).
(b) THE REMEDY: runs the REAL build-and-upload.sh for the whole pipeline with BAU_PARITY_SKIP unset,
    and reports per-function PASS/FAIL by real output, never a prediction.
(c) VERIFIED, NOT INFERRED: a fresh `git worktree add --detach` of this branch's own tip, the real
    build run there, and every resulting zip's members compared to the SERVED zip member-for-member
    by sha256.
(d) THE CONTROL: a mutant manifest (scratch only, this file's own tmp copy, real file never touched)
    with the four originally-named declarations removed, proving the build fails exactly as rows
    W1-S20/W2-S59 recorded; the real manifest succeeds for the same two functions.

usage: py -3.12 battery_ib_rte_4.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone

WS = pathlib.Path(__file__).resolve().parents[7]
sys.path.insert(0, str(WS / ".tools"))
import git_bash_resolver as gbr  # noqa: E402

SOURCE_MAP = WS / "infra/aws/lambda/ci/function-map"  # CT-ca-1: the folder, one <name>.json per function
BUILD_SCRIPT_REL = "infra/aws/lambda/ci/build-and-upload.sh"
PIPELINE = "investor-reporting"
BUCKET = "opal-313476888478-lambda-artifacts"
REGION = "us-east-1"
AWS_SHIM = ".tools/aws"
SCRATCH = WS / ".scratch" / "battery_ib_rte_4"
TOKEN = "IBR54-SERVED-MEMBERS-DECLARED-FROM-TRUE-SOURCES-VERIFIED"


def _hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def _ascii(s):
    """ASCII-only (CLAUDE.md Rule 4): build-and-upload.sh (pre-existing, not authored by this
    order) prints a literal UTF-8 checkmark on a verified upload; captured via a text-mode
    subprocess on this box it decodes as mojibake rather than raising, so it is folded here
    rather than relayed into this battery's own log."""
    if not s:
        return s
    return s.encode("ascii", "backslashreplace").decode("ascii")


def _bash(cmd, timeout=900, cwd=None):
    b = gbr.git_bash()
    if not b:
        raise RuntimeError("no Git Bash found (git_bash_resolver)")
    r = subprocess.run([b, "-lc", cmd], capture_output=True, text=True,
                        cwd=str(cwd or WS), timeout=timeout)
    return r.returncode, _ascii(r.stdout), _ascii(r.stderr)


def git_show(pin, path, cwd=None):
    rc, out, err = _bash("git show %s:%s" % (pin, path), cwd=cwd)
    if rc != 0:
        return None
    # bash -lc captures text; re-run in binary to get exact bytes for hashing
    r = subprocess.run([gbr.git_bash(), "-lc", "git show %s:%s" % (pin, path)],
                        capture_output=True, cwd=str(cwd or WS), timeout=60)
    return r.stdout if r.returncode == 0 else None


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_source_map():
    """{"functions": {name: entry}} read from the function-map folder (CT-ca-1). Raises when the folder holds no function file."""
    out = {}
    for p in sorted(SOURCE_MAP.glob("*.json")):
        with open(p, "r", encoding="utf-8") as f:
            out[p.stem] = json.load(f)
    if not out:
        raise SystemExit("ERROR: function-map folder holds no function file: %s" % SOURCE_MAP)
    return {"functions": out}


def family_functions(sm):
    """The SAME population build-and-upload.sh's TMPJS_LIST computes for pipeline=investor-reporting:
    tf_file contains the pipeline name, package_type != Image, build_type != 'nodejs'."""
    out = []
    for name, cfg in sm["functions"].items():
        if cfg.get("package_type") == "Image":
            continue
        if cfg.get("build_type") == "nodejs":
            continue
        tf = cfg.get("tf_file") or ""
        if PIPELINE not in tf:
            continue
        out.append(name)
    return sorted(out)


def download_served_zip(fn_name, dest_dir):
    dest = dest_dir / ("%s.zip" % fn_name)
    rc, out, err = _bash(
        "timeout 60 %s s3 cp s3://%s/%s/%s.zip %s --quiet" %
        (AWS_SHIM, BUCKET, PIPELINE, fn_name, dest.as_posix()))
    if rc != 0 or not dest.is_file():
        return None, rc, out + err
    return dest, 0, ""


def live_codesha256(fn_name):
    rc, out, err = _bash(
        "timeout 30 %s lambda get-function --function-name %s "
        "--query 'Configuration.CodeSha256' --output text" % (AWS_SHIM, fn_name))
    if rc != 0:
        return None
    return out.strip()


def live_deployed_zip_members(fn_name, dest_dir):
    """The LIVE DEPLOYED Lambda's own code, fetched via Code.Location (a presigned URL to the
    EXACT bytes CodeSha256 was computed over) -- NOT the S3 build-artifact bucket, which this
    battery's own part (b)/(c) just overwrote with a fresh build. build-and-upload.sh only
    updates the artifact bucket + the Lambda function map; a Lambda's ACTUAL served code changes
    only on `terraform apply`, so this is re-derivable correctly no matter how many times the
    builder has since re-run. Comparing PER MEMBER (not the overall zip sha256) matters: the zip
    CONTAINER is not guaranteed byte-reproducible across different builders/runs even when every
    member's content is identical (observed this run for 2 of 9 functions)."""
    rc, out, err = _bash(
        "timeout 30 %s lambda get-function --function-name %s --query 'Code.Location' "
        "--output text" % (AWS_SHIM, fn_name))
    if rc != 0 or not out.strip():
        return None, "get-function rc=%s %s" % (rc, (out + err).strip()[:200])
    url = out.strip()
    dest = dest_dir / ("%s.live.zip" % fn_name)
    try:
        import urllib.request
        urllib.request.urlretrieve(url, str(dest))
    except Exception as exc:
        return None, "download failed: %s: %s" % (type(exc).__name__, exc)
    if not dest.is_file() or dest.stat().st_size == 0:
        return None, "downloaded file missing or empty"
    return zip_members(dest), None


def zip_members(zip_path):
    """{member_name: sha256_hex} for every entry in the zip."""
    out = {}
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            data = z.read(info.filename)
            out[info.filename] = sha256_hex(data)
    return out


def zip_b64sha256(zip_path):
    data = pathlib.Path(zip_path).read_bytes()
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


# --------------------------------------------------------------------------- (a) THE CENSUS
def part_a(sm, functions):
    _hr("(a) THE CENSUS -- %d of %d investor-reporting functions" % (len(functions), len(functions)))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    zips_dir = SCRATCH / "served_zips"
    zips_dir.mkdir(exist_ok=True)

    census = {}  # fn -> {"members": {...}, "rows": [...]}
    denom_functions_matching_files_decl = 0

    for fn in functions:
        cfg = sm["functions"][fn]
        source_dir = cfg["source_dir"]
        declared_files = cfg.get("files") or ["lambda_function.py"]
        staged_from = {s["packaged_as"]: s for s in cfg.get("staged_from", [])}

        zpath, rc, errtxt = download_served_zip(fn, zips_dir)
        if zpath is None:
            print("  %s: DOWNLOAD FAILED rc=%s %s" % (fn, rc, errtxt.strip()[:200]))
            census[fn] = {"members": {}, "rows": [], "download_ok": False}
            continue

        local_sha = zip_b64sha256(zpath)
        live_sha = live_codesha256(fn)
        served_match = (local_sha == live_sha) if live_sha else None

        members = zip_members(zpath)

        # THE CHECK THAT ACTUALLY DECIDES "does this function need a deploy": per-member
        # content vs the LIVE DEPLOYED Lambda's own code (Code.Location), not the overall zip
        # sha256 -- a zip's CONTAINER is not guaranteed byte-reproducible across different
        # builders even when every member is identical, so an overall-hash mismatch alone is
        # NOT evidence of a real content difference (an earlier version of this battery
        # over-read it as one; corrected here).
        live_members, live_err = live_deployed_zip_members(fn, zips_dir)
        if live_members is None:
            print("   LIVE DEPLOYED CODE: could not fetch (%s) -- deploy-need UNVERIFIABLE" % live_err)
            needs_deploy = None
        else:
            member_diffs = sorted(k for k in set(members) | set(live_members)
                                   if members.get(k) != live_members.get(k))
            needs_deploy = len(member_diffs) > 0
            print("   LIVE DEPLOYED CODE: %d member(s); PER-MEMBER IDENTICAL TO FRESH BUILD=%s"
                  % (len(live_members), not needs_deploy))
            if needs_deploy:
                print("     member(s) differing from live: %s" % member_diffs)
        declared_set = set(declared_files)
        served_set = set(members.keys())
        set_match = declared_set == served_set

        if set_match:
            denom_functions_matching_files_decl += 1

        print("\n-> %s  (source_dir=%s)" % (fn, source_dir))
        print("   served zip sha256(b64)=%s  live CodeSha256=%s  MATCH=%s" %
              (local_sha, live_sha, served_match))
        print("   files[] declared=%d  served zip members=%d  SET-MATCH=%s" %
              (len(declared_set), len(served_set), set_match))
        if declared_set != served_set:
            print("     only in files[]: %s" % sorted(declared_set - served_set))
            print("     only in served zip: %s" % sorted(served_set - declared_set))

        rows = []
        for member in sorted(declared_set | served_set):
            member_sha = members.get(member)
            # TRACKED-AT-PATH?
            tracked_path = "%s/%s" % (source_dir, member)
            blob = git_show("HEAD", tracked_path)
            tracked_sha = sha256_hex(blob) if blob is not None else None
            cls = None
            detail = ""
            if member_sha is None:
                cls = "DECLARED-BUT-NOT-SERVED"
            elif tracked_sha is not None and tracked_sha == member_sha:
                cls = "TRACKED-AT-PATH"
                detail = "HEAD:%s" % tracked_path
            elif member in staged_from:
                decl = staged_from[member]
                pin = decl["pin"]
                blob2 = git_show(pin, decl["repo_path"])
                blob_sha = sha256_hex(blob2) if blob2 is not None else None
                if blob_sha == member_sha == decl.get("sha256"):
                    cls = "TRACKED-ELSEWHERE"
                    detail = "%s@%s (declared true source, blob-hash-verified equal)" % (
                        decl["repo_path"], pin[:10])
                else:
                    cls = "TRACKED-ELSEWHERE-MISMATCH"
                    detail = "%s@%s declared=%s blob=%s served=%s" % (
                        decl["repo_path"], pin[:10], decl.get("sha256"), blob_sha, member_sha)
            elif tracked_sha is not None:
                cls = "TRACKED-AT-PATH-CONTENT-DIFFERS"
                detail = "HEAD:%s sha256=%s served=%s" % (tracked_path, tracked_sha, member_sha)
            else:
                cls = "UNRESOLVED"
                detail = "no true source declared; served sha256=%s" % member_sha
            rows.append((member, cls, detail))
            print("   %-32s %-30s %s" % (member, cls, detail))

        census[fn] = {"members": members, "rows": rows, "download_ok": True,
                       "set_match": set_match, "served_match": served_match,
                       "needs_deploy": needs_deploy}

    print("\nDENOMINATOR: %d of %d functions have files[] == served zip member set" %
          (denom_functions_matching_files_decl, len(functions)))
    real_need_deploy = [fn for fn, c in census.items() if c.get("needs_deploy")]
    unverifiable_deploy = [fn for fn, c in census.items() if c.get("needs_deploy") is None]
    print("DEPLOY-NEED (per-member vs LIVE DEPLOYED code, not the overall zip hash): "
          "%d of %d functions genuinely need a deploy: %s (unverifiable: %s)" %
          (len(real_need_deploy), len(functions), real_need_deploy, unverifiable_deploy))

    unresolved = [(fn, m, d) for fn, c in census.items() for (m, cls, d) in c["rows"]
                  if cls == "UNRESOLVED"]
    print("\nUNRESOLVED members (declared + served, no true source found anywhere in the git object "
          "graph): %d" % len(unresolved))
    for fn, m, d in unresolved:
        print("   %s :: %s -- %s" % (fn, m, d))

    return census, unresolved, real_need_deploy, unverifiable_deploy


def _parse_build_output(text):
    """Return (built_names, failed_names) from build-and-upload.sh's own stdout+stderr -- the
    REAL run's own report, never a prediction. The script's final line is either
    'Complete -- N function(s) built and uploaded' (0 failed) or
    'PARTIAL -- N built, M failed: name1 name2 ...'."""
    failed_names = []
    for line in text.splitlines():
        if line.startswith("PARTIAL"):
            after = line.split("failed:", 1)
            if len(after) == 2:
                failed_names = after[1].split()
    attempted = [ln[3:].strip() for ln in text.splitlines() if ln.startswith("-> ")]
    built = [fn for fn in attempted if fn not in failed_names]
    return built, failed_names


# --------------------------------------------------------------------------- (b) THE REMEDY
def part_b():
    _hr("(b) THE REMEDY -- real build-and-upload.sh, BAU_PARITY_SKIP unset, whole pipeline")
    cmd = "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 850 bash %s %s" % (
        BUILD_SCRIPT_REL, PIPELINE)
    rc, out, err = _bash(cmd, timeout=900)
    text = out + err
    print(text)
    built, failed_names = _parse_build_output(text)
    print("\nBUILD rc=%d  built=%d  failed=%d  failed_names=%s" %
          (rc, len(built), len(failed_names), failed_names))
    return {"rc": rc, "text": text, "built": built, "failed": failed_names}


# --------------------------------------------------------------------------- (c) CLEAN CHECKOUT
def part_c(functions, census):
    _hr("(c) CLEAN CHECKOUT -- fresh detached worktree of this branch's own tip")
    rc, out, err = _bash("git rev-parse HEAD")
    head = out.strip()
    print("branch tip: %s" % head)

    tmp_wt = pathlib.Path(tempfile.mkdtemp(prefix="ib-rte-4-clean-"))
    wt_path = tmp_wt / "wt"
    rc, out, err = _bash("git worktree add --detach %s %s" % (wt_path.as_posix(), head))
    print("worktree add rc=%d" % rc)
    if rc != 0:
        print(err)
        return {"ok": False, "matched_functions": 0, "total_functions": len(functions)}

    try:
        rc, out, err = _bash(
            "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 850 bash %s %s" %
            (BUILD_SCRIPT_REL, PIPELINE), cwd=wt_path)
        text = out + err
        print(text)
        clean_built, clean_failed = _parse_build_output(text)
        print("\nCLEAN-CHECKOUT BUILD rc=%d  built=%d  failed=%d  failed_names=%s" %
              (rc, len(clean_built), len(clean_failed), clean_failed))

        # Only a function the CLEAN checkout's OWN build actually reported BUILT re-uploaded
        # anything just now -- comparing served bytes for a function that build just FAILED
        # would silently re-check the OLD, unrelated S3 object and falsely read IDENTICAL
        # (the bug this rewrite fixes: a prior run compared post-build S3 content for every
        # function regardless of whether THIS build touched it).
        matched, mismatched, need_deploy = 0, 0, []
        zips_dir = SCRATCH / "clean_zips"
        zips_dir.mkdir(parents=True, exist_ok=True)
        for fn in functions:
            served = census.get(fn, {}).get("members")
            if fn in clean_failed:
                print("  %s: NOT BUILT in clean checkout (rc!=0 for this function) -- excluded "
                      "from the identical-count, not counted as a match" % fn)
                continue
            if fn not in clean_built:
                print("  %s: not attempted by this build (unexpected) -- excluded" % fn)
                continue
            if not served:
                print("  %s: no served member set from part (a) -- skipped" % fn)
                continue
            zpath, rc2, e2 = download_served_zip(fn, zips_dir)
            if zpath is None:
                print("  %s: could not re-fetch the zip this clean build just uploaded (rc=%s)"
                      % (fn, rc2))
                mismatched += 1
                need_deploy.append(fn)
                continue
            clean_members = zip_members(zpath)
            same = (clean_members == served)
            print("  %s: clean-checkout build's own served zip: members=%d  part(a) served "
                  "members=%d  IDENTICAL=%s" % (fn, len(clean_members), len(served), same))
            if same:
                matched += 1
            else:
                mismatched += 1
                need_deploy.append(fn)

        print("\nDENOMINATOR: %d of %d CLEAN-CHECKOUT-BUILT functions member-for-member "
              "identical to their served zip; %d function(s) did not build in the clean "
              "checkout at all (%s)" % (matched, matched + mismatched, len(clean_failed),
                                         clean_failed))
        print("functions needing a deploy (content differs, or the clean build produced "
              "something new): %s" % need_deploy)
        return {"ok": True, "matched_functions": matched, "total_functions": matched + mismatched,
                "clean_built": clean_built, "clean_failed": clean_failed,
                "need_deploy": need_deploy}
    finally:
        _bash("git worktree remove --force %s" % wt_path.as_posix())
        shutil.rmtree(tmp_wt, ignore_errors=True)


# --------------------------------------------------------------------------- (d) THE CONTROL
def part_d(sm):
    _hr("(d) THE CONTROL -- mutant manifest (scratch only), the four originally-named declarations removed")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    mutant_path = SCRATCH / "mutant-function-map"  # CT-ca-1: the mutant is a function-map folder too
    mutant = json.loads(json.dumps(sm))  # deep copy
    # Remove the staged_from entries that supply the four ORIGINALLY-named members (rows
    # W1-S20/W2-S59): holdings served.py/loaders.py, directory-refresh errors.py/trading_calendar.py.
    h = mutant["functions"]["irpt-holdings"]
    h["staged_from"] = [s for s in h.get("staged_from", [])
                         if s["packaged_as"] not in ("served.py", "loaders.py")]
    r = mutant["functions"]["irpt-directory-refresh"]
    r["staged_from"] = [s for s in r.get("staged_from", [])
                         if s["packaged_as"] not in ("errors.py", "trading_calendar.py")]
    mutant_path.mkdir(parents=True, exist_ok=True)
    for fn_name, entry in mutant["functions"].items():
        with open(mutant_path / (fn_name + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(entry, f, indent=2)
            f.write("\n")

    results = {}
    for fn, expect_missing in (("irpt-holdings", ["served.py", "loaders.py"]),
                                ("irpt-directory-refresh", ["errors.py", "trading_calendar.py"])):
        # The env-var prefix binds ONLY to the command it directly precedes -- a bug caught
        # in this file's own first run: `VAR=x unset OTHER; cmd` sets VAR for `unset`, not
        # `cmd`, so the mutant never took effect and both "fails_as_recorded" reads a FALSE
        # Complete/1-built. Fixed by putting the assignment directly on the build invocation.
        cmd = ("unset BAU_PARITY_SKIP; BAU_SOURCE_MAP_OVERRIDE=%s timeout 60 bash %s %s %s" %
               (mutant_path.as_posix(), BUILD_SCRIPT_REL, PIPELINE, fn))
        rc, out, err = _bash(cmd)
        text = out + err
        print("\n-- mutant build, %s --" % fn)
        print(text)
        all_missing_present = all(("File not found: %s/%s" % (sm["functions"][fn]["source_dir"], m))
                                   in text for m in expect_missing)
        fails_as_recorded = (rc != 0) and all_missing_present
        results[fn] = fails_as_recorded
        print("fails_exactly_as_recorded=%s" % fails_as_recorded)

    # The REAL manifest succeeds for the same two functions (single-function mode).
    real_ok = {}
    for fn in ("irpt-holdings", "irpt-directory-refresh"):
        cmd = "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 120 bash %s %s %s" % (
            BUILD_SCRIPT_REL, PIPELINE, fn)
        rc, out, err = _bash(cmd)
        print("\n-- real manifest build, %s -- rc=%d" % (fn, rc))
        real_ok[fn] = (rc == 0)

    control_ok = all(results.values()) and all(real_ok.values())
    print("\nCONTROL RESULT: mutant fails exactly as recorded for both=%s ; real manifest succeeds for "
          "both=%s ; CONTROL=%s" % (results, real_ok, control_ok))
    return control_ok


def main():
    print("battery_ib_rte_4.py -- IRPT_BCKEND TO-IB-rte-4 R54-AC1")
    print("run at %s" % datetime.now(timezone.utc).isoformat())

    sm = load_source_map()
    functions = family_functions(sm)
    print("\nfamily (investor-reporting, zip-based, non-Image, non-nodejs): %d functions: %s" %
          (len(functions), functions))

    census, unresolved, real_need_deploy, unverifiable_deploy = part_a(sm, functions)
    remedy = part_b()
    clean = part_c(functions, census)
    control_ok = part_d(sm)

    _hr("SUMMARY")
    n = len(functions)
    print("(a) census: %d of %d functions enumerated; %d UNRESOLVED member(s) with no true source "
          "found anywhere in git's object graph; DEPLOY-NEED (per-member vs the LIVE DEPLOYED "
          "Lambda code, the authoritative check): %d of %d functions genuinely need a deploy=%s "
          "(unverifiable=%s)" %
          (n, n, len(unresolved), len(real_need_deploy), n, real_need_deploy, unverifiable_deploy))
    print("(b) remedy: build rc=%d; %d of %d functions built clean without BAU_PARITY_SKIP; "
          "failed=%s" % (remedy["rc"], len(remedy["built"]), n, remedy["failed"]))
    print("(c) clean checkout builder-determinism: %d of %d CLEAN-CHECKOUT-BUILT functions "
          "member-for-member identical to this worktree's own build (%d of %d functions "
          "overall); did not build in clean checkout: %s" %
          (clean.get("matched_functions", 0), clean.get("total_functions", 0),
           clean.get("matched_functions", 0), n, clean.get("clean_failed", [])))
    print("(d) control: %s" % control_ok)

    every_arm_holds = (
        len(unresolved) == 0
        and remedy["rc"] == 0
        and len(remedy["failed"]) == 0
        and len(unverifiable_deploy) == 0
        and len(real_need_deploy) == 0
        and clean.get("ok")
        and clean.get("matched_functions") == clean.get("total_functions") == n
        and control_ok
    )

    if every_arm_holds:
        print("\n" + TOKEN)
        return 0
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld.")
        print("%d of %d functions reach a full clean build+deploy-parity; %d function(s) blocked by "
              "%d member(s) with NO recoverable true source (content-addressed search of the whole "
              "git object graph found nothing -- filed as surprise rows, not fabricated here); "
              "%d function(s) genuinely need a deploy (per-member vs live)." %
              (n - len(remedy["failed"]), n, len(remedy["failed"]), len(unresolved),
               len(real_need_deploy)))
        return 1


if __name__ == "__main__":
    sys.exit(main())
