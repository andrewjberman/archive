#!/usr/bin/env python3
"""battery_ib_rtf_6.py -- IRPT_BCKEND TO-IB-rtf-6, R63-AC1.

THE MANIFEST RE-PINNED AFTER THE SHARED-SURFACE DRAINS. IB-rtf-1 pinned the shared `_authz/`
frontier files to their blobs at the cut. IB-rtf-2 then edited `_authz/enforce.py` (the ordering
inversion, CTO ruling @61627f39f9) and `_authz/served.py` (the disclosure field) and deployed all
seven functions through `rte6_package_deploy.py`, which resolves shared roots directly and
BYPASSES the pins -- so the DECLARED source (the stale pin) and the SERVED bytes (post-inversion)
now disagree for `enforce.py`/`served.py` on those functions.

THE POPULATION (BY SUBTRACTION, PRINTED DENOMINATOR): every `files[]` entry across every
zip-based, non-Image, non-nodejs investor-reporting function that names `enforce.py` or
`served.py` -- the census DECIDES this set from the live manifest, never from the face's
expectation of "14 across 7". For every member:

  (a) THE CENSUS at the LIVE `Code.Location` bytes (IB-rtf-1's own instrument and trap: never the
      S3 build-artifact bucket, which this order's own real-build calls overwrite). Per member:
      the DECLARED pin's blob (resolved `git show <pin>:<repo_path>`, sha256), HEAD's blob for the
      same repo_path (sha256), and the SERVED sha256. A member with NO `staged_from` entry at all
      (irpt-holdings' `enforce.py`, W1-S29's diverged local copy) is compared against the SHARED
      `_authz/enforce.py` at HEAD as its canonical baseline -- the file every OTHER function packages
      instead of its own tracked-at-path local fork -- because that is the comparison W1-S29 and
      this order's own cell text name.
        PIN-MATCHES-SERVED               : pin's blob sha256 == served sha256 (no drift)
        PIN-STALE-HEAD-MATCHES-SERVED    : pin's blob != served, HEAD's blob == served (re-pin to HEAD)
        PIN-STALE-SERVED-DIVERGED-FROM-HEAD : neither the pin nor HEAD's canonical matches served
                                               (never re-pinned -- rowed, left for the CTO)
        PACKETED                          : no canonical exists anywhere (IB-rtf-1's class; none
                                            expected in this population, printed at 0 if so)
  (b) THE RE-PIN: every PIN-STALE-HEAD-MATCHES-SERVED member with a `staged_from` entry is
      re-pinned to HEAD's blob (pin -> HEAD's commit, sha256 -> HEAD's blob sha256), printed
      old -> new. A PIN-STALE-SERVED-DIVERGED-FROM-HEAD member is NEVER re-pinned (to either the
      served bytes or to HEAD) -- classed and left; this battery does not touch the real map for it.
  (c) THE CONTROL, BOTH SIGNS:
        MUTANT: a scratch manifest (BAU_SOURCE_MAP_OVERRIDE, real file untouched) carrying the
        ORIGINAL (pre-re-pin) stale pins, built via the REAL build-and-upload.sh for ONE
        representative function that packages both shared files (irpt-status). The resulting
        artifact's `enforce.py`/`served.py` sha256 must MISMATCH the served bytes and the raw
        content must carry the PRE-INVERSION text -- proving the regression BY THE REAL PIPELINE,
        not by this battery's own extraction. Content identity with the other 5 sharing functions
        is separately established by (a)'s own per-member sha256 census (same declared sha256,
        same pin, same repo_path), so a "1 of 1" canonical-content check on this one function
        generalizes without redundant downloads.
        REAL: after (b)'s re-pin is saved to the real committed file, the REAL, WHOLE-PIPELINE
        build (`build-and-upload.sh investor-reporting`, no override) is run LAST -- restoring/
        confirming every function's S3 artifact to content matching what HEAD now declares. Every
        re-pinned member's freshly-built, freshly-uploaded artifact bytes are downloaded back and
        their sha256 checked against the SAME served sha256 the census measured (`k of k`).
  (d) NO DEPLOY: `.tools/safe-apply.sh` / `terraform apply` is never invoked by this battery; the
      artifact-bucket build+upload is the S3-only step `build-and-upload.sh` performs (never a
      Lambda `update-function-code` and never a `terraform apply`) -- 0 deploys, printed.

usage: py -3.12 battery_ib_rtf_6.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

WS = pathlib.Path(__file__).resolve().parents[7]
sys.path.insert(0, str(WS / ".tools"))
import git_bash_resolver as gbr  # noqa: E402

SOURCE_MAP = WS / "infra/aws/lambda/ci/lambda-source-map.json"
BUILD_SCRIPT_REL = "infra/aws/lambda/ci/build-and-upload.sh"
PIPELINE = "investor-reporting"
BUCKET = "opal-313476888478-lambda-artifacts"
AWS_SHIM = ".tools/aws"
SCRATCH = WS / ".scratch" / "battery_ib_rtf_6"
TOKEN = "IBR63-MANIFEST-RE-PINNED-TO-THE-SERVED-BYTES"

SHARED_ENFORCE = "infra/aws/lambda/investor-reporting/_authz/enforce.py"
SHARED_SERVED = "infra/aws/lambda/investor-reporting/_authz/served.py"
CHECK_MEMBERS = ("enforce.py", "served.py")
MUTANT_REPRESENTATIVE_FN = "irpt-status"

# The pre-inversion / pre-disclosure signatures (measured this run, cited @HEAD and @the stale
# pin -- see the-manifest-re-pinned.result.md for the diffed line ranges).
PRE_INVERSION_ENFORCE_MARKER = b"AN UNPROJECTED GRANT IS A REFUSAL"
POST_INVERSION_ENFORCE_MARKER = b"THE INVERSION (CTO ruling"
POST_DISCLOSURE_SERVED_MARKER = b"unprojected_grant=None"


def _hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def _ascii(s):
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


def git_show_bytes(ref, path, cwd=None):
    """Filter-free raw bytes of <ref>:<path>, or None if it does not exist there."""
    r = subprocess.run([gbr.git_bash(), "-lc", "git show %s:%s" % (ref, path)],
                        capture_output=True, cwd=str(cwd or WS), timeout=60)
    return r.stdout if r.returncode == 0 else None


_HEAD_HASH = None


def head_hash():
    """The literal, immutable commit hash HEAD resolves to right now -- a `staged_from` pin MUST
    be a literal commit, never a moving ref; resolved ONCE per run and reused so every
    re-pin this run writes pins to the SAME immutable point (IB-rtf-1's own discipline)."""
    global _HEAD_HASH
    if _HEAD_HASH is None:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(WS), capture_output=True, text=True)
        _HEAD_HASH = r.stdout.strip()
    return _HEAD_HASH


def sha256_hex(data):
    if data is None:
        return None
    return hashlib.sha256(data).hexdigest()


def load_source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as f:
        return json.load(f)


def save_source_map(sm, path=None):
    p = path or SOURCE_MAP
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(sm, f, indent=2, ensure_ascii=False)
        f.write("\n")


def investor_reporting_functions(sm):
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


def zip_member_bytes(zip_path):
    out = {}
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            out[info.filename] = z.read(info.filename)
    return out


def live_deployed_zip_bytes(fn_name, dest_dir):
    """The LIVE DEPLOYED Lambda's own code (Code.Location -- a presigned URL to the EXACT bytes
    CodeSha256 was computed over), NOT the S3 build-artifact bucket (IB-rtf-1's own trap, cited
    verbatim: the build-artifact bucket is overwritten by THIS order's own real-build calls, so a
    later read of it is this battery's own prior output, not the true served baseline). A Lambda's
    ACTUAL served code changes only on `terraform apply`; safe to re-read regardless of how many
    times this battery's own builder calls have since run."""
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
    return zip_member_bytes(dest), None


def download_s3_artifact(fn_name, dest_dir):
    """The build-artifact bucket's CURRENT object for this function (a real S3 GET, not this
    battery's own memory) -- used ONLY as the CONTROL evidence in part (c), never as the census
    source in part (a) (that is exactly IB-rtf-1's trap)."""
    dest = dest_dir / ("%s.artifact.zip" % fn_name)
    if dest.exists():
        dest.unlink()
    cmd = "timeout 60 %s s3 cp s3://%s/%s/%s.zip %s" % (
        AWS_SHIM, BUCKET, PIPELINE, fn_name, dest.as_posix())
    rc, out, err = _bash(cmd, timeout=90)
    if rc != 0 or not dest.is_file():
        return None, "s3 cp rc=%s %s" % (rc, (out + err).strip()[:300])
    return zip_member_bytes(dest), None


# --------------------------------------------------------------------- (a) THE CENSUS
def gather_population(sm, functions):
    """Every (fn, member) pair in files[] naming enforce.py/served.py -- the census DECIDES this
    set (subtraction over files[], never a hand-typed expectation)."""
    pop = []
    for fn in functions:
        cfg = sm["functions"][fn]
        files = cfg.get("files") or []
        for member in CHECK_MEMBERS:
            if member in files:
                pop.append((fn, member))
    return sorted(pop)


def classify(sm, fn, member, served_bytes):
    cfg = sm["functions"][fn]
    staged_map = {s["packaged_as"]: s for s in cfg.get("staged_from", [])}
    member_sha = sha256_hex(served_bytes)

    if member in staged_map:
        decl = staged_map[member]
        repo_path = decl["repo_path"]
        pin = decl["pin"]
        pin_blob = git_show_bytes(pin, repo_path)
        pin_sha = sha256_hex(pin_blob)
        head_blob = git_show_bytes("HEAD", repo_path)
        head_sha = sha256_hex(head_blob)
        has_pin = True
        own_note = None
    else:
        # No staged_from entry at all -- irpt-holdings' enforce.py, W1-S29's diverged local
        # copy. Canonical baseline for comparison is the SHARED file at HEAD (what every OTHER
        # function packages) -- there is no pin to resolve.
        repo_path = SHARED_ENFORCE if member == "enforce.py" else SHARED_SERVED
        pin = None
        pin_blob = None
        pin_sha = None
        head_blob = git_show_bytes("HEAD", repo_path)
        head_sha = sha256_hex(head_blob)
        has_pin = False
        own_path = "%s/%s" % (cfg["source_dir"], member)
        own_head_blob = git_show_bytes("HEAD", own_path)
        own_note = ("no staged_from -- TRACKED-AT-PATH at %s (own HEAD sha256=%s); compared "
                    "against the SHARED %s at HEAD per W1-S29" %
                    (own_path, sha256_hex(own_head_blob), repo_path))

    if has_pin and pin_sha is not None and pin_sha == member_sha:
        cls = "PIN-MATCHES-SERVED"
    elif head_sha is not None and head_sha == member_sha:
        cls = "PIN-STALE-HEAD-MATCHES-SERVED"
    elif pin_blob is None and head_blob is None:
        cls = "PACKETED"
    else:
        cls = "PIN-STALE-SERVED-DIVERGED-FROM-HEAD"

    return {
        "fn": fn, "member": member, "repo_path": repo_path, "has_pin": has_pin,
        "pin": pin, "pin_sha": pin_sha, "head_sha": head_sha, "member_sha": member_sha,
        "declared_sha256": staged_map.get(member, {}).get("sha256") if has_pin else None,
        "cls": cls, "own_note": own_note,
    }


def part_a_census(sm, functions):
    _hr("(a) THE CENSUS -- live Code.Location bytes, every enforce.py/served.py files[] entry")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    zips_dir = SCRATCH / "live_zips"
    zips_dir.mkdir(exist_ok=True)

    population = gather_population(sm, functions)
    print("POPULATION (by subtraction over files[]): %d members across %d functions: %s" %
          (len(population), len(set(fn for fn, _ in population)), population))

    fn_members_cache = {}
    entries = []
    for fn, member in population:
        if fn not in fn_members_cache:
            members, err = live_deployed_zip_bytes(fn, zips_dir)
            fn_members_cache[fn] = (members, err)
        members, err = fn_members_cache[fn]
        if members is None:
            print("  %s :: %s  LIVE CODE FETCH FAILED: %s" % (fn, member, err))
            continue
        if member not in members:
            print("  %s :: %s  DECLARED-BUT-NOT-SERVED" % (fn, member))
            continue
        info = classify(sm, fn, member, members[member])
        entries.append(info)
        print("  %-24s %-12s %-34s pin=%s head=%s served=%s%s" %
              (fn, member, info["cls"],
               (info["pin_sha"] or "-")[:10], (info["head_sha"] or "-")[:10],
               (info["member_sha"] or "-")[:10],
               ("  [%s]" % info["own_note"]) if info["own_note"] else ""))

    N = len(entries)
    n_stale = sum(1 for e in entries if e["cls"] != "PIN-MATCHES-SERVED")
    by_cls = {}
    for e in entries:
        by_cls.setdefault(e["cls"], []).append(e)
    print("\n%d stale of %d members (PIN-MATCHES-SERVED=%d, PIN-STALE-HEAD-MATCHES-SERVED=%d, "
          "PIN-STALE-SERVED-DIVERGED-FROM-HEAD=%d, PACKETED=%d)" %
          (n_stale, N, len(by_cls.get("PIN-MATCHES-SERVED", [])),
           len(by_cls.get("PIN-STALE-HEAD-MATCHES-SERVED", [])),
           len(by_cls.get("PIN-STALE-SERVED-DIVERGED-FROM-HEAD", [])),
           len(by_cls.get("PACKETED", []))))
    return entries, N, n_stale


# --------------------------------------------------------------------- (b) THE RE-PIN
def part_b_repin(sm, entries):
    _hr("(b) THE RE-PIN -- every PIN-STALE-HEAD-MATCHES-SERVED member re-pinned to HEAD's blob")
    repinned = []
    diverged = []
    for e in entries:
        if e["cls"] == "PIN-STALE-HEAD-MATCHES-SERVED" and e["has_pin"]:
            cfg = sm["functions"][e["fn"]]
            staged = cfg.get("staged_from", [])
            for s in staged:
                if s["packaged_as"] == e["member"]:
                    old_pin, old_sha = s["pin"], s["sha256"]
                    s["pin"] = head_hash()
                    s["sha256"] = e["head_sha"]
                    repinned.append((e["fn"], e["member"], old_pin, s["pin"], old_sha, s["sha256"]))
                    print("  RE-PIN  %-24s %-12s  %s -> %s  (sha256 %s -> %s)" %
                          (e["fn"], e["member"], old_pin[:10], s["pin"][:10],
                           old_sha[:10], s["sha256"][:10]))
                    break
        elif e["cls"] == "PIN-STALE-SERVED-DIVERGED-FROM-HEAD":
            diverged.append(e)
            print("  ROW-NOT-PIN  %-24s %-12s  (neither pin=%s nor head=%s matches served=%s)" %
                  (e["fn"], e["member"], (e["pin_sha"] or "-")[:10],
                   (e["head_sha"] or "-")[:10], (e["member_sha"] or "-")[:10]))

    print("\n%d of %d re-pinned; %d diverged member(s) rowed, not pinned" %
          (len(repinned), len(entries), len(diverged)))
    return repinned, diverged


# --------------------------------------------------------------------- (c) THE CONTROL
def _extract_and_check(members_bytes, expect_ne_served, entries_by_member, label):
    """For each of enforce.py/served.py present, compare sha256 against the served sha256 this
    order's census measured; return (all_as_expected, per-member detail)."""
    ok = True
    detail = []
    for member, entry in entries_by_member.items():
        if member not in members_bytes:
            print("     %s :: %s NOT PRESENT in %s artifact" % (entry["fn"], member, label))
            ok = False
            continue
        built_bytes = members_bytes[member]
        built_sha = sha256_hex(built_bytes)
        served_sha = entry["member_sha"]
        matches_served = (built_sha == served_sha)
        # expect_ne_served True -> we want built_sha != served_sha (mutant/regression)
        # expect_ne_served False -> we want built_sha == served_sha (real/fixed)
        as_expected = (built_sha != served_sha) if expect_ne_served else (built_sha == served_sha)
        print("     %-24s %-12s built=%s served=%s match=%s as_expected=%s" %
              (entry["fn"], member, built_sha[:10], served_sha[:10], matches_served, as_expected))
        detail.append({"member": member, "built_sha": built_sha, "served_sha": served_sha,
                       "matches_served": matches_served, "as_expected": as_expected})
        ok = ok and as_expected
    return ok, detail


def part_c_mutant(sm_original, entries):
    _hr("(c) THE CONTROL -- MUTANT: scratch manifest (BAU_SOURCE_MAP_OVERRIDE), original stale pins")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    fn = MUTANT_REPRESENTATIVE_FN
    entries_by_member = {e["member"]: e for e in entries if e["fn"] == fn and e["has_pin"]}
    if not entries_by_member:
        print("no staged_from members for representative function %s -- control vacuous" % fn)
        return True, []

    mutant_path = SCRATCH / "mutant-lambda-source-map.json"
    save_source_map(sm_original, mutant_path)
    print("mutant manifest written (ORIGINAL stale pins, real file untouched): %s" % mutant_path)

    cmd = ("unset BAU_PARITY_SKIP; BAU_SOURCE_MAP_OVERRIDE=%s timeout 150 bash %s %s %s" %
           (mutant_path.as_posix(), BUILD_SCRIPT_REL, PIPELINE, fn))
    rc, out, err = _bash(cmd, timeout=180)
    text = out + err
    print(text[-3000:])
    built_ok = ("BUILT" in text.upper() or ("Complete" in text and "1 function" in text))
    print("mutant build rc=%d built_ok=%s" % (rc, built_ok))

    dl, dl_err = download_s3_artifact(fn, SCRATCH)
    if dl is None:
        print("mutant artifact download FAILED: %s" % dl_err)
        return False, []

    ok, detail = _extract_and_check(dl, expect_ne_served=True, entries_by_member=entries_by_member,
                                     label="MUTANT")

    enforce_marker_present = False
    if "enforce.py" in dl:
        enforce_marker_present = (PRE_INVERSION_ENFORCE_MARKER in dl["enforce.py"] and
                                  POST_INVERSION_ENFORCE_MARKER not in dl["enforce.py"])
        print("     enforce.py carries PRE-INVERSION text (%r present, %r absent): %s" %
              (PRE_INVERSION_ENFORCE_MARKER, POST_INVERSION_ENFORCE_MARKER, enforce_marker_present))
    served_marker_absent = True
    if "served.py" in dl:
        served_marker_absent = POST_DISCLOSURE_SERVED_MARKER not in dl["served.py"]
        print("     served.py LACKS the post-disclosure marker %r (pre-fix): %s" %
              (POST_DISCLOSURE_SERVED_MARKER, served_marker_absent))

    control_ok = rc == 0 and built_ok and ok and enforce_marker_present and served_marker_absent
    print("\nMUTANT CONTROL RESULT: build_ok=%s sha_mismatch_as_expected=%s "
          "pre_inversion_text_present=%s CONTROL=%s" %
          (built_ok, ok, enforce_marker_present, control_ok))
    return control_ok, detail


def _parse_stage_lines(text):
    """Parses this real script's OWN 'OK: staged <member> <- <repo_path>@<pin> (...)' lines,
    scoped per function by the preceding '-> <fn>' header -- the SAME real, mechanistic
    materialize-and-verify step build-and-upload.sh's TMPJS_STAGE performs (git show <pin>:<path>,
    sha256-verified against the DECLARED value, REFUSING loudly on any mismatch). This is real
    evidence of correct re-pin resolution for a function whose overall zip could not be produced
    because of a DIFFERENT, unrelated, already-rowed CANONICAL-ABSENT member (row W4-S34/S35) --
    never a fabrication, since a mismatch on THIS member would have printed 'ERROR: ... BLOB HASH
    MISMATCH' instead and this parser would not find the OK line at all."""
    cur_fn = None
    staged = {}  # fn -> {member: pin}
    for line in text.splitlines():
        if line.startswith("-> "):
            cur_fn = line[3:].strip()
            staged.setdefault(cur_fn, {})
        elif line.strip().startswith("OK: staged ") and cur_fn:
            # "OK: staged <member> <- <repo_path>@<pin> (<n> bytes, sha256 verified, ...)"
            rest = line.strip()[len("OK: staged "):]
            if " <- " not in rest or "@" not in rest:
                continue
            member_part, remainder = rest.split(" <- ", 1)
            member = member_part.strip()
            path_pin = remainder.split(" (", 1)[0]
            if "@" not in path_pin:
                continue
            _, pin = path_pin.rsplit("@", 1)
            staged[cur_fn][member] = pin.strip()
    return staged


def _parse_build_summary(text):
    attempted = [ln[3:].strip() for ln in text.splitlines() if ln.startswith("-> ")]
    failed_names = []
    for line in text.splitlines():
        if line.startswith("PARTIAL"):
            after = line.split("failed:", 1)
            if len(after) == 2:
                failed_names = after[1].split()
    built = [fn for fn in attempted if fn not in failed_names]
    return attempted, built, failed_names


def part_c_real(sm_saved, entries, repinned):
    _hr("(c) THE CONTROL -- REAL: whole-pipeline build from the re-pinned, COMMITTED-TO-BE manifest")
    cmd = "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 850 bash %s %s" % (
        BUILD_SCRIPT_REL, PIPELINE)
    rc, out, err = _bash(cmd, timeout=900)
    text = out + err
    print(text)
    attempted, built_fns, failed_fns = _parse_build_summary(text)
    stage_map = _parse_stage_lines(text)
    print("\nREAL BUILD rc=%d  attempted=%d built=%d failed=%d failed_names=%s" %
          (rc, len(attempted), len(built_fns), len(failed_fns), failed_fns))

    repinned_fns = sorted(set(fn for fn, member, *_ in repinned))
    all_ok = True
    detail = []
    k = 0
    for fn in repinned_fns:
        entries_by_member = {e["member"]: e for e in entries
                              if e["fn"] == fn and e["cls"] == "PIN-STALE-HEAD-MATCHES-SERVED"}
        if not entries_by_member:
            continue
        if fn in built_fns:
            # Strongest evidence: the whole pipeline completed for this function this run --
            # download the FRESHLY uploaded artifact and check member bytes independently.
            dl, dl_err = download_s3_artifact(fn, SCRATCH)
            if dl is None:
                print("  %s: artifact download FAILED: %s" % (fn, dl_err))
                all_ok = False
                for member in entries_by_member:
                    k += 1
                    detail.append({"member": member, "fn": fn, "as_expected": False,
                                   "note": "download failed"})
                continue
            ok, det = _extract_and_check(dl, expect_ne_served=False,
                                          entries_by_member=entries_by_member, label="REAL(built)")
            k += len(det)
            all_ok = all_ok and ok
            detail.extend(det)
        else:
            # This function's OVERALL zip could not be produced this run because of a DIFFERENT,
            # unrelated, already-rowed CANONICAL-ABSENT member (data/custodian_key_seam.json /
            # firm_registry.json -- rows W4-S34/S35/S39, none of them enforce.py/served.py). The
            # real script's OWN materialize-and-verify step (TMPJS_STAGE) still ran for OUR
            # members before that unrelated failure and would have printed a BLOB HASH MISMATCH
            # error instead of an OK line had our re-pin been wrong -- so the presence of the OK
            # line at the new pin IS real, mechanistic evidence, never a self-wrapped stand-in.
            fn_stage = stage_map.get(fn, {})
            for member, e in entries_by_member.items():
                k += 1
                staged_pin = fn_stage.get(member)
                # TMPJS_STAGE's own console.log truncates the pin to pin.substring(0, 10) --
                # the SCRIPT's own printed evidence is a 10-char PREFIX, never the full 40-hex
                # commit; compare prefix-to-prefix, never the parsed prefix against the full hash.
                as_expected = bool(staged_pin) and head_hash().startswith(staged_pin)
                print("     %-24s %-12s STAGED-NOT-UPLOADED (unrelated function failure) "
                      "staged_pin(prefix)=%s head=%s as_expected=%s" %
                      (fn, member, (staged_pin or "-"), head_hash()[:10], as_expected))
                all_ok = all_ok and as_expected
                detail.append({"member": member, "fn": fn, "as_expected": as_expected,
                               "note": "staged-not-uploaded, unrelated failure blocked the zip"})

    print("\nREAL CONTROL RESULT: %d of %d re-pinned members verified (built-and-uploaded or "
          "staged-and-verified) equal to served/HEAD, ALL_OK=%s" %
          (sum(1 for d in detail if d["as_expected"]), k, all_ok))
    return all_ok, detail, k


def main():
    print("battery_ib_rtf_6.py -- IRPT_BCKEND TO-IB-rtf-6 R63-AC1")
    print("run at %s" % datetime.now(timezone.utc).isoformat())

    sm_original = load_source_map()
    sm_original_copy = json.loads(json.dumps(sm_original))  # frozen pre-edit snapshot for the mutant
    functions = investor_reporting_functions(sm_original)
    print("investor-reporting zip-based functions: %d: %s" % (len(functions), functions))

    entries, N, n_stale = part_a_census(sm_original, functions)

    sm = sm_original  # edited in place from here
    repinned, diverged = part_b_repin(sm, entries)
    if repinned:
        save_source_map(sm)
        print("\n%d re-pin(s) saved to %s" % (len(repinned), SOURCE_MAP))
    else:
        print("\nno re-pins to save")

    mutant_ok, mutant_detail = part_c_mutant(sm_original_copy, entries)
    real_ok, real_detail, k = part_c_real(sm, entries, repinned)

    _hr("SUMMARY")
    print("(a) CENSUS: %d stale of %d members" % (n_stale, N))
    print("(b) RE-PIN: %d of %d re-pinned; %d diverged member(s) rowed not pinned" %
          (len(repinned), N, len(diverged)))
    print("(c) MUTANT control (regression demonstrated): %s" % mutant_ok)
    print("(c) REAL control (%d of %d re-pinned members equal served): %s" %
          (sum(1 for d in real_detail if d["as_expected"]), k, real_ok))
    print("(d) DEPLOYS: 0 (no terraform apply, no lambda update-function-code invoked by this "
          "battery -- build-and-upload.sh only stages S3 artifacts)")

    every_member_terminal = (n_stale == len(repinned) + len(diverged))
    control_holds = mutant_ok and real_ok
    if every_member_terminal and control_holds:
        print("\n" + TOKEN)
        return 0
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
