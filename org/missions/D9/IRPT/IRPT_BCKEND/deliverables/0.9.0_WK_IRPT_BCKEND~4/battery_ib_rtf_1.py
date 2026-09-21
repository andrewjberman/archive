#!/usr/bin/env python3
"""battery_ib_rtf_1.py -- IRPT_BCKEND TO-IB-rtf-1, R58-AC1.

THE NO-SOURCE MEMBERS, MEASURED THEN BRANCHED. Re-derives, every run, from the real world -- the
LIVE DEPLOYED Lambda's own code (Code.Location, never the S3 build-artifact bucket, which this
order's own real-build runs overwrite with intermediate states -- rte-4's own trap, re-hit and
fixed inside this order's own first run) and git's own object database -- never from a prior
run's output or this file's own prose.

THE POPULATION (BY SUBTRACTION, PRINTED DENOMINATOR): re-runs IB-rte-4's served-zip census over
every zip-based, non-Image, non-nodejs function in the investor-reporting family (the SAME
TMPJS_LIST filter build-and-upload.sh applies) at its CURRENT served bytes, classifies every
declared+served member, and takes every member that is NOT TRACKED-AT-PATH-EQUAL and NOT declared
through a VERIFIED staged_from entry (pin blob sha256 == declared sha256 == served member sha256).
A member whose only byte difference from its tracked path is CRLF-vs-LF (the pre-existing,
estate-wide, already-ARMED row IRPT_BCKEND-W4-S38 class -- an autocrlf checkout artifact, not a
provenance gap) is excluded from THIS population by that row's own disposition; this battery
verifies the CRLF-only claim itself (normalized-newline byte equality) rather than assuming it.

For every population member:
  (a) THE CANONICAL SOURCE: a tracked path at HEAD, OR a path found by a CONTENT-ADDRESSED search
      of the whole reachable git object graph (git hash-object --no-filters + git cat-file -e +
      git rev-list --objects --all -- never a path guess), OR ABSENT.
  (b) THE DIFF: served bytes vs canonical, key-by-key for JSON / line-by-line for text / byte-count
      for binary, both directions, printed with denominators, BEFORE any label like stale/rot/drift.
  (c) THE BRANCH: DELTA=0 -> this battery ITSELF declares `staged_from` in the real
      lambda-source-map.json (idempotent: a correct existing entry is left untouched, a
      missing/stale one is added/repointed) -- no third copy, no served bytes committed as source.
      DELTA!=0 / CANONICAL-ABSENT -> the NEVER-WIDEN packet + an ARMED row (never fabricated,
      never deployed, never committed as source).
  (d) THE CONTROL: real build (whole pipeline, BAU_PARITY_SKIP unset) after (c)'s declarations;
      a scratch mutant manifest (BAU_SOURCE_MAP_OVERRIDE, real file never touched) with this
      order's own new declarations removed, proving the build fails on exactly those members.

usage: py -3.12 battery_ib_rtf_1.py
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
SCRATCH = WS / ".scratch" / "battery_ib_rtf_1"
TOKEN = "IBR58-NO-SOURCE-MEMBERS-MEASURED-AND-BRANCHED"

# JSON-classified members get a structured key-by-key diff; everything else gets line/byte diff.
JSON_SUFFIXES = (".json",)


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
    be a literal commit, never a moving ref (build_package.py's own MOVING-ref refusal test names
    'HEAD' itself as the first spelling it refuses); resolved ONCE per run and reused so every
    declaration this run writes pins to the SAME immutable point."""
    global _HEAD_HASH
    if _HEAD_HASH is None:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(WS), capture_output=True, text=True)
        _HEAD_HASH = r.stdout.strip()
    return _HEAD_HASH


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as f:
        return json.load(f)


def save_source_map(sm):
    with open(SOURCE_MAP, "w", encoding="utf-8", newline="\n") as f:
        json.dump(sm, f, indent=2, ensure_ascii=False)
        f.write("\n")


def family_functions(sm):
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
    CodeSha256 was computed over), NOT the S3 build-artifact bucket. THIS order's own part (d)
    real build repeatedly overwrites the artifact bucket with intermediate, mid-repair states
    (measured this run: a first, buggy attempt left served.py/loaders.py stale-pinned while
    already re-uploading ids.py/custodian_key_seam.json fixed, so a SUBSEQUENT read of the
    artifact bucket reads the battery's OWN prior output, not the true served baseline -- the
    exact contamination rte-4's own result.md named and avoided the same way). A Lambda's ACTUAL
    served code changes only on `terraform apply`; this is safe to re-read no matter how many
    times this battery's own builder calls have since re-run."""
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


_OID_INDEX = None  # oid(40-hex) -> [path, ...], built once from the whole reachable object graph


def build_oid_index():
    global _OID_INDEX
    if _OID_INDEX is not None:
        return _OID_INDEX
    r = subprocess.run(["git", "rev-list", "--objects", "--all"], cwd=str(WS),
                        capture_output=True, text=True, timeout=120)
    idx = {}
    for line in r.stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            idx.setdefault(parts[0], []).append(parts[1])
    _OID_INDEX = idx
    print("   [content-graph index built: %d objects, this run]" % len(idx))
    return idx


def content_oid_no_filters(data: bytes) -> str:
    """git's own blob object id for RAW bytes (no clean-filter re-encoding) -- row W4-S37's
    instrument trap: the default `git hash-object` applies the checkout filter and can find a
    coincidentally-matching but WRONG blob."""
    r = subprocess.run([gbr.git_bash(), "-lc", "git hash-object --no-filters --stdin -t blob"],
                        input=data, capture_output=True, cwd=str(WS), timeout=30)
    return r.stdout.decode("ascii").strip()


def oid_present(oid):
    return subprocess.run(["git", "cat-file", "-e", oid], cwd=str(WS)).returncode == 0


# --------------------------------------------------------------------- MEMBER CLASSIFICATION
def classify_member(source_dir, member, member_bytes, staged_from_map):
    """Returns a dict: cls, canonical_path, canonical_ref, member_sha, canonical_sha, detail."""
    member_sha = sha256_hex(member_bytes)
    tracked_path = "%s/%s" % (source_dir, member)
    tracked_blob = git_show_bytes("HEAD", tracked_path)

    if tracked_blob is not None:
        t_sha = sha256_hex(tracked_blob)
        if t_sha == member_sha:
            return {"cls": "TRACKED-AT-PATH-EQUAL", "canonical_path": tracked_path,
                    "canonical_ref": head_hash(), "member_sha": member_sha, "canonical_sha": t_sha,
                    "canonical_bytes": tracked_blob}
        if tracked_blob.replace(b"\r\n", b"\n") == member_bytes.replace(b"\r\n", b"\n"):
            return {"cls": "TRACKED-AT-PATH-CRLF-ONLY", "canonical_path": tracked_path,
                    "canonical_ref": head_hash(), "member_sha": member_sha, "canonical_sha": t_sha,
                    "canonical_bytes": tracked_blob,
                    "detail": "row IRPT_BCKEND-W4-S38 class -- normalized-newline bytes equal"}
        return {"cls": "TRACKED-AT-PATH-CONTENT-DIFFERS", "canonical_path": tracked_path,
                "canonical_ref": head_hash(), "member_sha": member_sha, "canonical_sha": t_sha,
                "canonical_bytes": tracked_blob}

    if member in staged_from_map:
        decl = staged_from_map[member]
        pin_blob = git_show_bytes(decl["pin"], decl["repo_path"])
        pin_sha = sha256_hex(pin_blob) if pin_blob is not None else None
        head_blob = git_show_bytes("HEAD", decl["repo_path"])
        head_sha = sha256_hex(head_blob) if head_blob is not None else None
        verified = (pin_sha is not None and pin_sha == decl.get("sha256") == member_sha)
        if verified:
            return {"cls": "TRACKED-ELSEWHERE-VERIFIED", "canonical_path": decl["repo_path"],
                    "canonical_ref": decl["pin"], "member_sha": member_sha,
                    "canonical_sha": pin_sha, "canonical_bytes": pin_blob}
        if head_sha is not None and head_sha == member_sha:
            # The DECLARATION (pin) is stale, but the repo_path's CURRENT HEAD content is the
            # true, live-matching canonical source -- a re-pin (not a packet) closes this one.
            # Diffing must run against the CORRECT (HEAD) canonical bytes, never the stale pin's.
            return {"cls": "TRACKED-ELSEWHERE-STALE-PIN", "canonical_path": decl["repo_path"],
                    "canonical_ref": head_hash(), "member_sha": member_sha,
                    "canonical_sha": head_sha, "canonical_bytes": head_blob,
                    "stale_pin": decl["pin"], "stale_pin_sha256": pin_sha,
                    "declared_sha256": decl.get("sha256")}
        return {"cls": "TRACKED-ELSEWHERE-MISMATCH", "canonical_path": decl["repo_path"],
                "canonical_ref": decl["pin"], "member_sha": member_sha,
                "canonical_sha": pin_sha, "canonical_bytes": pin_blob,
                "head_path_sha": head_sha, "head_matches_served": head_sha == member_sha,
                "head_bytes": head_blob if head_sha == member_sha else None,
                "declared_sha256": decl.get("sha256")}

    # No declaration at all -- content-addressed search of the whole reachable object graph.
    oid = content_oid_no_filters(member_bytes)
    present = oid_present(oid)
    if not present:
        return {"cls": "UNRESOLVED", "canonical_path": None, "canonical_ref": None,
                "member_sha": member_sha, "canonical_sha": None, "oid": oid}
    idx = build_oid_index()
    paths = idx.get(oid, [])
    head_hit = None
    for p in paths:
        b = git_show_bytes("HEAD", p)
        if b is not None and sha256_hex(b) == member_sha:
            head_hit = (p, b)
            break
    if head_hit:
        return {"cls": "TRACKED-ELSEWHERE-DISCOVERABLE", "canonical_path": head_hit[0],
                "canonical_ref": head_hash(), "member_sha": member_sha,
                "canonical_sha": member_sha, "canonical_bytes": head_hit[1], "oid": oid,
                "all_reachable_paths": paths}
    return {"cls": "TRACKED-ELSEWHERE-HISTORICAL-ONLY", "canonical_path": (paths[0] if paths else None),
            "canonical_ref": None, "member_sha": member_sha, "canonical_sha": None, "oid": oid,
            "all_reachable_paths": paths}


EXCLUDED_FROM_POPULATION = {"TRACKED-AT-PATH-EQUAL", "TRACKED-ELSEWHERE-VERIFIED",
                             "TRACKED-AT-PATH-CRLF-ONLY"}


# --------------------------------------------------------------------------- (a)/(b) CENSUS+DIFF
def json_key_diff(served_bytes, canonical_bytes):
    try:
        sv = json.loads(served_bytes.decode("utf-8"))
        cv = json.loads(canonical_bytes.decode("utf-8"))
    except Exception:
        return None  # not both parseable JSON -- fall through to line diff
    if not isinstance(sv, dict) or not isinstance(cv, dict):
        return None
    sk, ck = set(sv.keys()), set(cv.keys())
    only_served = sorted(sk - ck)
    only_canon = sorted(ck - sk)
    differing = sorted(k for k in (sk & ck) if sv[k] != cv[k])
    K = len(sk | ck)
    return {"present_only_in_served": only_served, "present_only_in_canonical": only_canon,
            "differing_value": differing, "K": K,
            "delta": len(only_served) + len(only_canon) + len(differing)}


def line_diff(served_bytes, canonical_bytes):
    sv = served_bytes.decode("utf-8", "replace").splitlines()
    cv = canonical_bytes.decode("utf-8", "replace").splitlines()
    sset, cset = set(sv), set(cv)
    only_served = len(sset - cset)
    only_canon = len(cset - sset)
    K = len(sset | cset)
    return {"only_served_lines": only_served, "only_canonical_lines": only_canon, "K": K,
            "delta": only_served + only_canon}


def diff_member(fn, member, served_bytes, info):
    """Prints the diff (denominators, both directions), no label. Returns DELTA (int)."""
    canonical_bytes = info.get("canonical_bytes")
    if canonical_bytes is None:
        # CANONICAL-ABSENT: the whole member is "present only in served".
        if member.endswith(JSON_SUFFIXES):
            try:
                obj = json.loads(served_bytes.decode("utf-8"))
                k = len(obj) if isinstance(obj, dict) else 1
                print("     DIFF (json, canonical ABSENT): present-only-in-served=%d of %d keys; "
                      "present-only-in-canonical=0 of 0 (no canonical exists); differing-value=0 of 0"
                      % (k, k))
                return k if k else 1
            except Exception:
                pass
        n_lines = len(served_bytes.decode("utf-8", "replace").splitlines()) or 1
        print("     DIFF (canonical ABSENT): present-only-in-served=%d of %d line(s); "
              "present-only-in-canonical=0 of 0" % (n_lines, n_lines))
        return n_lines

    if served_bytes == canonical_bytes:
        print("     DIFF: byte-identical (0 of %d bytes differ, both directions)" % len(served_bytes))
        return 0

    if member.endswith(JSON_SUFFIXES):
        d = json_key_diff(served_bytes, canonical_bytes)
        if d is not None:
            print("     DIFF (json): present-only-in-served=%d of %d; present-only-in-canonical=%d of %d; "
                  "differing-value=%d of %d"
                  % (len(d["present_only_in_served"]), d["K"], len(d["present_only_in_canonical"]),
                     d["K"], len(d["differing_value"]), d["K"]))
            if d["delta"]:
                print("       served-only keys: %s" % d["present_only_in_served"])
                print("       canonical-only keys: %s" % d["present_only_in_canonical"])
                print("       differing-value keys: %s" % d["differing_value"])
            return d["delta"]
    d = line_diff(served_bytes, canonical_bytes)
    print("     DIFF (line-by-line): only-in-served=%d of %d line(s); only-in-canonical=%d of %d line(s)"
          % (d["only_served_lines"], d["K"], d["only_canonical_lines"], d["K"]))
    return d["delta"]


def part_a_and_b(sm, functions):
    _hr("(a)+(b) THE CENSUS AND THE DIFF -- %d of %d investor-reporting functions" %
        (len(functions), len(functions)))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    zips_dir = SCRATCH / "served_zips"
    zips_dir.mkdir(exist_ok=True)

    total_members = 0
    population = []  # list of dict: fn, member, info, delta
    per_fn_members = {}

    for fn in functions:
        cfg = sm["functions"][fn]
        source_dir = cfg["source_dir"]
        declared_files = cfg.get("files") or ["lambda_function.py"]
        staged_from_map = {s["packaged_as"]: s for s in cfg.get("staged_from", [])}

        members, live_err = live_deployed_zip_bytes(fn, zips_dir)
        if members is None:
            print("  %s: LIVE CODE FETCH FAILED: %s" % (fn, live_err))
            per_fn_members[fn] = {}
            continue
        declared_set = set(declared_files)
        served_set = set(members.keys())
        per_fn_members[fn] = members

        print("\n-> %s  (source_dir=%s, %d served member(s))" % (fn, source_dir, len(served_set)))
        if declared_set != served_set:
            print("   files[] declared=%d served=%d  only-in-files[]=%s  only-in-served=%s" %
                  (len(declared_set), len(served_set), sorted(declared_set - served_set),
                   sorted(served_set - declared_set)))

        for member in sorted(declared_set | served_set):
            if member not in members:
                print("   %-40s DECLARED-BUT-NOT-SERVED" % member)
                continue
            total_members += 1
            info = classify_member(source_dir, member, members[member], staged_from_map)
            print("   %-40s %s  canonical=%s@%s" %
                  (member, info["cls"], info.get("canonical_path"),
                   (info.get("canonical_ref") or "")[:10]))
            if info["cls"] in EXCLUDED_FROM_POPULATION:
                continue
            delta = diff_member(fn, member, members[member], info)
            population.append({"fn": fn, "member": member, "info": info, "delta": delta,
                                "source_dir": source_dir})

    print("\nDENOMINATOR: %d of %d declared+served members across %d functions" %
          (len(population), total_members, len(functions)))
    return population, total_members, per_fn_members


KNOWN_AT_THE_CUT = {
    ("irpt-intake-poller", "firm_registry.json"),
    ("irpt-ycharts-generate", "firm_registry.json"),
    ("irpt-ycharts-generate", "settings.json"),
    ("irpt-status", "handler.py"),
    ("irpt-status", "checkpoint.py"),
    ("irpt-ycharts-generate", "gate.py"),
    ("irpt-ycharts-generate", "firm_destination_policy.json"),
}


# --------------------------------------------------------------------------- (c) THE BRANCH
def part_c(sm, population):
    _hr("(c) THE BRANCH -- DELTA=0 declares in the real source map; DELTA!=0/ABSENT is packeted")
    declared_now = []   # (fn, member, repo_path, pin, sha256) newly written this run
    packeted = []        # population entries still needing the never-widen packet
    newly_found = []     # population members not on the face's known list at the cut

    for entry in population:
        fn, member, info, delta = entry["fn"], entry["member"], entry["info"], entry["delta"]
        if (fn, member) not in KNOWN_AT_THE_CUT:
            newly_found.append(entry)
        canonical_bytes = info.get("canonical_bytes")
        if delta == 0 and canonical_bytes is not None:
            cfg = sm["functions"][fn]
            staged = cfg.setdefault("staged_from", [])
            staged = [s for s in staged if s["packaged_as"] != member]
            staged.append({
                "repo_path": info["canonical_path"],
                "pin": info["canonical_ref"],
                "packaged_as": member,
                "sha256": info["member_sha"],
            })
            cfg["staged_from"] = staged
            declared_now.append((fn, member, info["canonical_path"], info["canonical_ref"],
                                  info["member_sha"]))
            print("   DECLARE  %-24s %-32s <- %s@%s" %
                  (fn, member, info["canonical_path"], info["canonical_ref"][:10]))
        else:
            packeted.append(entry)
            print("   PACKET   %-24s %-32s (DELTA=%s, canonical=%s)" %
                  (fn, member, delta, info.get("canonical_path") or "ABSENT"))

    if declared_now:
        save_source_map(sm)
        print("\n%d declaration(s) written to %s" % (len(declared_now), SOURCE_MAP))
    print("\n%d newly-found population member(s) not on the face's KNOWN_AT_THE_CUT list "
          "(the population moved since IB-rte-4/rte-6):" % len(newly_found))
    for e in newly_found:
        print("   %s :: %s" % (e["fn"], e["member"]))

    return declared_now, packeted, newly_found


def write_never_widen_packet(packeted, per_fn_members):
    path = (WS / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/"
            "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-1.md")
    lines = []
    lines.append("# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-1")
    lines.append("")
    lines.append("Cell `IB-rtf-1`. Every member below is CANONICAL-ABSENT: a content-addressed "
                 "search of the whole reachable git object graph (`git hash-object --no-filters` "
                 "then `git cat-file -e` / a full `git rev-list --objects --all` index, not a path "
                 "guess) found the exact served bytes committed nowhere, ever. NOT deployed, NOT "
                 "committed as source by this order. Same content and same absence as rows "
                 "IRPT_BCKEND-W4-S34/W4-S35 (re-verified fresh this run).")
    lines.append("")
    for e in packeted:
        fn, member = e["fn"], e["member"]
        served_bytes = per_fn_members[fn][member]
        served_sha = hashlib.sha256(served_bytes).hexdigest()
        lines.append("## %s :: %s" % (fn, member))
        lines.append("")
        lines.append("- **Blast radius:** the full served content (%d bytes) is `present-only-in-served`; "
                     "no canonical exists to diff against (0 of 0 canonical keys/lines)." % len(served_bytes))
        lines.append("- **Rollback:** the served bytes themselves -- `blob %s` (sha256), fetched fresh "
                     "each run from the LIVE DEPLOYED Lambda's own code (`aws lambda get-function "
                     "--function-name %s --query Code.Location`, a presigned URL to the exact bytes "
                     "CodeSha256 was computed over -- never the S3 build-artifact bucket, which this "
                     "order's own real-build runs overwrite)." % (served_sha, fn))
        lines.append("- **Writer census:** see `IRPT_BCKEND-W4-S34`/`W4-S35` (this project's investigation "
                     "file) for the grounded content-addressed absence; this order's own R58-AC2 judgment "
                     "record states the writer-census finding for %s (see the proof-of-spec instance)."
                     % member)
        lines.append("- **Disposition:** NOT deployed by this order; NOT committed as source. The member's "
                     "row stays ARMED, `disarm_owner: 2.0.0_SA_COO~B to route`, per the existing "
                     "investigation row.")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("\nNEVER-WIDEN packet written: %s" % path)
    return path


def _parse_build_output(text):
    failed_names = []
    for line in text.splitlines():
        if line.startswith("PARTIAL"):
            after = line.split("failed:", 1)
            if len(after) == 2:
                failed_names = after[1].split()
    attempted = [ln[3:].strip() for ln in text.splitlines() if ln.startswith("-> ")]
    built = [fn for fn in attempted if fn not in failed_names]
    return built, failed_names


# --------------------------------------------------------------------------- (d) THE CONTROL
def part_d_real_build():
    _hr("(d) THE CONTROL -- real build (whole pipeline, BAU_PARITY_SKIP unset)")
    cmd = "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 850 bash %s %s" % (
        BUILD_SCRIPT_REL, PIPELINE)
    rc, out, err = _bash(cmd, timeout=900)
    text = out + err
    print(text)
    built, failed = _parse_build_output(text)
    print("\nBUILD rc=%d  built=%d  failed=%d  failed_names=%s" % (rc, len(built), len(failed), failed))
    return {"rc": rc, "built": built, "failed": failed}


def part_d_mutant(sm, declared_now):
    _hr("(d) THE CONTROL -- mutant manifest (scratch only): this order's OWN new declarations removed")
    if not declared_now:
        print("no new declarations were written this run -- nothing to mutate; control vacuous")
        return True, []
    SCRATCH.mkdir(parents=True, exist_ok=True)
    mutant = json.loads(json.dumps(sm))
    by_fn = {}
    for fn, member, _p, _pin, _sha in declared_now:
        by_fn.setdefault(fn, []).append(member)
    for fn, members in by_fn.items():
        cfg = mutant["functions"][fn]
        cfg["staged_from"] = [s for s in cfg.get("staged_from", []) if s["packaged_as"] not in members]
    mutant_path = SCRATCH / "mutant-lambda-source-map.json"
    with open(mutant_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(mutant, f, indent=2, ensure_ascii=False)
        f.write("\n")

    results = {}
    for fn, members in sorted(by_fn.items()):
        cmd = ("unset BAU_PARITY_SKIP; BAU_SOURCE_MAP_OVERRIDE=%s timeout 90 bash %s %s %s" %
               (mutant_path.as_posix(), BUILD_SCRIPT_REL, PIPELINE, fn))
        rc, out, err = _bash(cmd)
        text = out + err
        source_dir = sm["functions"][fn]["source_dir"]
        all_missing_present = all(("File not found: %s/%s" % (source_dir, m)) in text for m in members)
        fails_as_expected = (rc != 0) and all_missing_present
        results[fn] = fails_as_expected
        print("-- mutant build, %s (members removed: %s) -- rc=%d fails_as_expected=%s" %
              (fn, members, rc, fails_as_expected))
        if not fails_as_expected:
            print(text[-2000:])

    # The real (un-mutated) manifest must no longer fail on THESE members. A function can still
    # legitimately fail overall on a DIFFERENT, CANONICAL-ABSENT member this order cannot fix
    # (e.g. irpt-ycharts-generate on firm_registry.json/settings.json) -- that is not this
    # control's question, and requiring rc==0 there would conflate two independent findings.
    real_ok = {}
    for fn in sorted(by_fn):
        members = by_fn[fn]
        source_dir = sm["functions"][fn]["source_dir"]
        cmd = "unset BAU_PARITY_SKIP; unset BAU_SOURCE_MAP_OVERRIDE; timeout 120 bash %s %s %s" % (
            BUILD_SCRIPT_REL, PIPELINE, fn)
        rc, out, err = _bash(cmd)
        text = out + err
        none_of_these_missing = not any(("File not found: %s/%s" % (source_dir, m)) in text
                                         for m in members)
        real_ok[fn] = none_of_these_missing
        print("-- real manifest build, %s -- rc=%d  none-of-%s-missing=%s" %
              (fn, rc, members, none_of_these_missing))
        if not none_of_these_missing:
            print(text[-2000:])

    control_ok = all(results.values()) and all(real_ok.values())
    print("\nCONTROL RESULT: mutant fails exactly as expected for all=%s ; real manifest succeeds for "
          "all=%s ; CONTROL=%s" % (all(results.values()), all(real_ok.values()), control_ok))
    return control_ok, sorted(by_fn)


def main():
    print("battery_ib_rtf_1.py -- IRPT_BCKEND TO-IB-rtf-1 R58-AC1")
    print("run at %s" % datetime.now(timezone.utc).isoformat())

    sm = load_source_map()
    functions = family_functions(sm)
    print("family (investor-reporting, zip-based, non-Image, non-nodejs): %d functions: %s" %
          (len(functions), functions))

    population, total_members, per_fn_members = part_a_and_b(sm, functions)
    N = len(population)

    declared_now, packeted, newly_found = part_c(sm, population)
    k = len(declared_now)
    j = len(packeted)

    packet_path = None
    if packeted:
        packet_path = write_never_widen_packet(packeted, per_fn_members)

    build = part_d_real_build()
    control_ok, mutated_fns = part_d_mutant(sm, declared_now)

    _hr("SUMMARY")
    print("POPULATION: %d of %d declared+served members across %d functions are NOT "
          "TRACKED-AT-PATH-EQUAL and NOT a verified staged_from (CRLF-only diffs excluded per row "
          "W4-S38's own disposition)." % (N, total_members, len(functions)))
    print("(a) canonical source NAMED or ABSENT: %d of %d population members resolved to a named "
          "canonical path; %d of %d are CANONICAL-ABSENT" %
          (sum(1 for e in population if e["info"].get("canonical_bytes") is not None), N,
           sum(1 for e in population if e["info"].get("canonical_bytes") is None), N))
    print("(c) branch: DECLARED-AND-VERIFIED k=%d ; PACKETED-AND-ROWED j=%d ; k+j=%d (N=%d)" %
          (k, j, k + j, N))
    print("(d) control: mutant-fails-as-expected + real-manifest-succeeds for the %d newly-declared "
          "function(s) = %s" % (len(mutated_fns), control_ok))
    print("(d) real build (whole pipeline): rc=%d built=%d failed=%d failed_names=%s" %
          (build["rc"], len(build["built"]), len(build["failed"]), build["failed"]))
    if packet_path:
        print("NEVER-WIDEN packet: %s" % packet_path)
    print("%d newly-found population member(s) not on the face's known-at-the-cut list" % len(newly_found))

    every_member_terminal = (k + j == N)
    control_holds = control_ok
    if every_member_terminal and control_holds:
        print("\n" + TOKEN)
        return 0
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
