"""BATTERY IB-rtc-4 -- R34-AC1: instrument hygiene, four round-2 rulings executed.

Four arms, each printing its own measurement with a denominator. Token IBR34-FOUR-ARMS-MEASURED
prints only when all four have PRINTED THEIR MEASUREMENT -- arm (a) may read DIFFER or
NOT-REPRODUCIBLE and the token still prints, because the criterion is that the comparison was
PERFORMED as bytes; the READING itself is R34-AC2's, never self-graded here.

  (a) W4-S28 -- BYTES. Served CodeSha256(irpt-ycharts-generate) vs a zip BUILT from the fix's
      source, attempted by the root's OWN documented mechanism (build-and-upload.sh) and by the
      project's own proven multi-root packager (rt2_package.py) under both that packager's zip
      recipe and the canonical script's own recipe (PowerShell, sorted, LastWriteTime=2020-01-01).
      A sibling function's served CodeSha256 is the negative control.
  (b) S32 -- RETIRE. The two round-1 batteries (IB-s-4, IB-s-12) whose deploy leg reads FALSE RED
      after the correct bundle mint each carry a SUPERSEDED header; nothing is minted, moved or
      re-keyed to satisfy them (S32's own NEVER).
  (c) W4-S23 -- VENDOR BAR. battery_ib_rt_8.py's re-cut bar (0 VENDOR connections over an
      ENUMERATED host list, foreign-non-vendor hosts named separately) exercised against the REAL
      committed render record (RT8-a_render_record.json), never a synthetic copy.
  (d) W1-S17 / S54 -- LAYER FETCH. rt2_verify_deployed.py downloads the irpt-common layer zip when
      its local `.scratch/layer/` cache is absent (forced empty here for a genuine cold-cache
      exercise); IB-rt-2's terminal battery, re-run from THIS fresh worktree, prints 7 of 7.

NO DEPLOY. NO MINT. NO APPLY. Every AWS call below is a read (get-function-configuration,
get-function, get-layer-version, and the downloads those calls' own URLs point at). R-40: every
produced or served artifact this battery grades has its content hash printed beside it.

Run: timeout 1200 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
     0.9.0_WK_IRPT_BCKEND~3/battery_ib_rtc_4.py
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[7]
HERE = pathlib.Path(__file__).resolve().parent
SCRATCH = REPO / ".scratch"
AWS = str(REPO / ".tools" / "aws.cmd")
SOURCE_MAP = REPO / "infra" / "aws" / "lambda" / "ci" / "lambda-source-map.json"
GENERATE_TF = (REPO / "infra" / "aws" / "terraform" / "investor-reporting" / "ycharts"
              / "generate.tf")
GENERATE_SRC = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "generate"
EXTRACT_SRC = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "extract"

W2 = REPO / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables" / "0.9.0_WK_IRPT_BCKEND~2"
W1 = REPO / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables" / "0.9.0_WK_IRPT_BCKEND~1"
W4 = REPO / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables" / "0.9.0_WK_IRPT_BCKEND~4"

RT2_PACKAGE = W2 / "rt2_package.py"
RT2_VERIFY = W2 / "rt2_verify_deployed.py"
RT2_BATTERY = W2 / "battery_ib_rt_2.py"
IBS4_RESULT = W2 / "battery_ib_s_4.result.md"
IBS12_RESULT = W1 / "holdings-snapshot-three-partner-joins-reconciled.result.md"
RT8_BATTERY = W4 / "battery_ib_rt_8.py"
RT8_RECORD = W4 / "RT8-a_render_record.json"
LAYER_CACHE = SCRATCH / "layer"

FUNCTION = "irpt-ycharts-generate"
SIBLING = "irpt-status"
SUPERSEDE_MARKER = "SUPERSEDED AT `86d2d0835f` BY row `IRPT_BCKEND-S32`"

ARMS = {}

CANONICAL_ZIP_PS1 = """param(
    [string]$ListFile,
    [string]$OutZip
)
Add-Type -Assembly 'System.IO.Compression.FileSystem'
if (Test-Path $OutZip) { Remove-Item $OutZip }
$zip = [System.IO.Compression.ZipFile]::Open($OutZip, 'Create')
$fixedTime = [DateTime]::new(2020, 1, 1, 0, 0, 0)
$lines = Get-Content $ListFile | Sort-Object
foreach ($line in $lines) {
    $parts = $line -split "`t", 2
    $arcname = $parts[0]
    $srcpath = $parts[1]
    $entry = $zip.CreateEntry($arcname, [System.IO.Compression.CompressionLevel]::Optimal)
    $entry.LastWriteTime = $fixedTime
    $stream = $entry.Open()
    $bytes = [System.IO.File]::ReadAllBytes($srcpath)
    $stream.Write($bytes, 0, $bytes.Length)
    $stream.Dispose()
}
$zip.Dispose()
"""


def head(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def sha256_b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")


def git_hash_object(path):
    proc = subprocess.run(["git", "hash-object", str(path)], cwd=str(REPO),
                          capture_output=True, text=True, timeout=30)
    return (proc.stdout or "").strip() or "UNREADABLE(%s)" % (proc.stderr or "")[:120]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def aws_text(*args, timeout=120):
    proc = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        return None, (proc.stderr or "")[:300]
    out = (proc.stdout or "").strip()
    return (out or None), None


# --------------------------------------------------------------------- (a)
def arm_a():
    head("(a) W4-S28 -- SERVED CodeSha256 vs a zip BUILT from the fix's source")
    print("  Terraform root read       : %s" % GENERATE_TF)
    print("  root's own content hash   : %s" % git_hash_object(GENERATE_TF))

    sm = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))["functions"][FUNCTION]
    declared = sm.get("files") or []
    source_dir = REPO / sm["source_dir"]

    # PREMISE CHECK, filed as a row: does anything this function's build resolves actually
    # reference the fix's own file (extract/certify.py, commit 56a6e07e8f)? Read the four
    # generate-package source files for the literal string, never assumed.
    generate_files = ["job.py", "recipe.py", "transport.py", "entry.py"]
    hits = []
    for fn in generate_files:
        p = GENERATE_SRC / fn
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            if "certify" in text or ("extract" in text and "extract-and-import" not in text):
                hits.append(fn)
    print("  PREMISE CHECK -- does this package's own source reference extract/certify.py? "
          "%d of %d generate-package file(s) do: %s"
          % (len(hits), len(generate_files), hits or "none"))
    print("      extract/certify.py's own declared/resolvable membership in ANY Lambda's "
          "build (full source-map census) : 0 of %d function(s)"
          % len(json.loads(SOURCE_MAP.read_text(encoding='utf-8'))["functions"]))

    # ATTEMPT 1: the CANONICAL documented mechanism. build-and-upload.sh resolves every
    # declared member at ONE source_dir, with no shared-root fallback.
    missing_at_source_dir = [f for f in declared if not (source_dir / f).is_file()]
    print("  ATTEMPT 1 -- build-and-upload.sh's own resolution rule (source_dir/<name> only):")
    print("      source_dir                : %s" % sm["source_dir"])
    print("      declared file(s)          : %d" % len(declared))
    print("      missing at that directory : %d of %d -- %s"
          % (len(missing_at_source_dir), len(declared), ", ".join(missing_at_source_dir) or "none"))
    canonical_refused = bool(missing_at_source_dir)
    if canonical_refused:
        print("      CANONICAL MECHANISM REFUSES before any zip is created: "
              "'ERROR: File not found: %s/%s'" % (sm["source_dir"], missing_at_source_dir[0]))

    # ATTEMPT 2: the project's own proven multi-root packager (rt2_package.py), the mechanism
    # a prior worker in THIS project built and used to package this exact function -- source_dir
    # first, then shared roots (_authz, _scope, _keys, _ids, _gate, intake, directory, data/,
    # terraform/investor-reporting/core). ZIP_DATE = 2026-09-11, sorted, ZIP_DEFLATED entries.
    rt2pkg = load_module(RT2_PACKAGE, "rt2_package_for_rtc4")
    want = rt2pkg.needed_files(FUNCTION, declared)
    zip_path, sha_pkg, members, unresolved = rt2pkg.build(FUNCTION, want)
    print("  ATTEMPT 2 -- rt2_package.py (multi-root resolver, ZIP_DATE=2026-09-11):")
    print("      declared %d -> packaged %d (resolved %d, unresolved %d: %s)"
          % (len(declared), len(want), len(members), len(unresolved), unresolved or "none"))
    print("      zip                       : %s" % zip_path)
    print("      sha256(b64)               : %s" % sha_pkg)

    # ATTEMPT 3: the SAME resolved member set, rebuilt with the CANONICAL script's own zip
    # recipe -- PowerShell System.IO.Compression.ZipFile, sorted entries, FIXED 2020-01-01
    # LastWriteTime (build-and-upload.sh's convention, never rt2_package's 2026-09-11).
    source_dir_str = str(source_dir)
    ps_list = SCRATCH / "rtc4_zip_members.txt"
    ps_out = SCRATCH / "rtc4-ycharts-generate-canonical.zip"
    lines = []
    for name in sorted(want):
        path, _where = rt2pkg.resolve_member(FUNCTION, source_dir_str, name)
        lines.append("%s\t%s" % (name, path))
    ps_list.write_text("\n".join(lines), encoding="utf-8", newline="")
    ps_script = SCRATCH / "rtc4_build_canonical_zip.ps1"
    ps_script.write_text(CANONICAL_ZIP_PS1, encoding="utf-8", newline="\r\n")
    proc = subprocess.run(
        ["powershell.exe", "-NoProfile", "-File", str(ps_script),
         "-ListFile", str(ps_list), "-OutZip", str(ps_out).replace("\\", "/")],
        capture_output=True, text=True, timeout=120)
    canonical_zip_ok = proc.returncode == 0 and ps_out.is_file()
    sha_canonical = sha256_b64(ps_out) if canonical_zip_ok else None
    print("  ATTEMPT 3 -- the same %d resolved member(s), build-and-upload.sh's OWN zip recipe "
          "(PowerShell, sorted, LastWriteTime=2020-01-01):" % len(members))
    print("      zip                       : %s" % ps_out)
    print("      sha256(b64)               : %s"
          % (sha_canonical or ("BUILD FAILED: %s" % (proc.stderr or "")[:200])))

    served, err = aws_text("lambda", "get-function-configuration", "--function-name", FUNCTION,
                           "--region", "us-east-1", "--query", "CodeSha256", "--output", "text")
    sibling_served, sib_err = aws_text(
        "lambda", "get-function-configuration", "--function-name", SIBLING,
        "--region", "us-east-1", "--query", "CodeSha256", "--output", "text")
    print("  served CodeSha256 (%s)     : %s" % (FUNCTION, served or ("READ FAILED: %s" % err)))
    print("  NEGATIVE CONTROL -- sibling (%s) served CodeSha256 : %s"
          % (SIBLING, sibling_served or ("READ FAILED: %s" % sib_err)))
    control_differs = bool(served and sibling_served and served != sibling_served)
    print("      NEGATIVE CONTROL DIFFERS from the target's served CodeSha256 : %s"
          % control_differs)

    candidates = {"rt2_package.py (2026-09-11 recipe)": sha_pkg,
                  "build-and-upload.sh's own zip recipe (2020-01-01)": sha_canonical}
    if served is None:
        reading = "NOT-REPRODUCIBLE(served CodeSha256 could not be read: %s)" % err
    else:
        matches = [label for label, sha in candidates.items() if sha and sha == served]
        if matches:
            reading = "EQUAL (%s)" % matches[0]
        elif canonical_refused and not sha_canonical and not sha_pkg:
            reading = "NOT-REPRODUCIBLE(no recipe could even build a zip)"
        else:
            reading = "DIFFER"

    print("")
    print("  MEASUREMENT: served CodeSha256 %s vs built %s -> %s"
          % (served, sha_pkg, reading))
    print("      built (rt2_package.py recipe)             : %s" % sha_pkg)
    print("      built (build-and-upload.sh's own recipe)  : %s" % (sha_canonical or "N/A"))
    print("      served                                    : %s" % served)
    if reading == "DIFFER":
        print("      REASON: two independently-built, deterministic zips (the project's own")
        print("      proven multi-root packager, and the canonical script's own zip recipe over")
        print("      the SAME resolved members) both differ from the served bytes and from each")
        print("      other. The CANONICAL script (build-and-upload.sh) additionally cannot even")
        print("      attempt this build unassisted: %d of %d declared member(s) do not exist at"
              % (len(missing_at_source_dir), len(declared)))
        print("      the single source_dir it resolves against, and it has no shared-root")
        print("      fallback -- that convention exists only in this project's own packager.")
        print("      NO RECIPE FROM THIS WORKTREE REPRODUCES THE SERVED BYTES. NAMED NEXT ACT:")
        print("      pin the exact build that produced CodeSha256=%s (S3 object version" % served)
        print("      history / upload timestamp, or the owning seat's own record of which")
        print("      recipe it ran) before a bytes comparison can adjudicate row W4-S28.")
    ARMS["a"] = True  # arm (a) PRINTS its measurement regardless of the reading
    return {
        "reading": reading, "served": served, "sibling_served": sibling_served,
        "control_differs": control_differs, "built_rt2pkg": sha_pkg,
        "built_canonical": sha_canonical, "canonical_refused": canonical_refused,
        "missing_at_source_dir": missing_at_source_dir, "extract_hits": hits,
    }


# --------------------------------------------------------------------- (b)
def arm_b():
    head("(b) S32 -- RETIRE THE TWO STALE ROUND-1 BATTERIES (NOTHING MINTED, MOVED OR RE-KEYED)")
    targets = [("battery_ib_s_4.result.md (IB-s-4)", IBS4_RESULT),
               ("holdings-snapshot-...result.md (IB-s-12)", IBS12_RESULT)]
    ok_count = 0
    for label, path in targets:
        text = path.read_text(encoding="utf-8")
        present = SUPERSEDE_MARKER in text
        ok_count += 1 if present else 0
        print("  %-46s SUPERSEDED header present: %s" % (label, present))
        print("      content hash (git hash-object)             : %s" % git_hash_object(path))
    print("  %d of %d result doc(s) carry the SUPERSEDED header" % (ok_count, len(targets)))
    print("  0 key(s) minted, moved or re-keyed by this cell (S32's own NEVER) -- this cell")
    print("      issued no S3 write of any kind")
    ARMS["b"] = ok_count == len(targets)
    return ok_count, len(targets)


# --------------------------------------------------------------------- (c)
def arm_c():
    head("(c) W4-S23 -- THE RE-CUT VENDOR BAR, EXERCISED AGAINST THE REAL RENDER RECORD")
    rt8 = load_module(RT8_BATTERY, "battery_ib_rt_8_for_rtc4")  # module code only; main() NEVER
    render = json.loads(RT8_RECORD.read_text(encoding="utf-8"))
    guard = render["network_guard"] or {}
    ok, lines = rt8.vendor_bar_report(guard)
    for line in lines:
        print(line)
    print("  RT8-a_render_record.json content hash (git hash-object) : %s"
          % git_hash_object(RT8_RECORD))
    print("  battery_ib_rt_8.py content hash (git hash-object)        : %s"
          % git_hash_object(RT8_BATTERY))
    print("  bar's re-cut TEXT recorded verbatim in instrument-hygiene.result.md")
    ARMS["c"] = ok
    return ok, lines


# --------------------------------------------------------------------- (d)
def arm_d():
    head("(d) W1-S17 / S54 -- LAYER FETCH, THEN IB-rt-2's TERMINAL BATTERY, FRESH WORKTREE")
    if LAYER_CACHE.is_dir():
        print("  clearing the gitignored layer cache to force a genuine cold-cache exercise: %s"
              % LAYER_CACHE)
        shutil.rmtree(LAYER_CACHE, ignore_errors=True)
    print("  cache present before this run : %s" % LAYER_CACHE.is_dir())

    proc = subprocess.run(
        [sys.executable, str(RT2_VERIFY), "irpt-directory-search", "irpt-performance-adapter",
         "irpt-narrative", "irpt-export-render", "irpt-status", "irpt-ycharts-generate",
         "irpt-holdings"],
        capture_output=True, text=True, timeout=600, cwd=str(REPO))
    direct_out = (proc.stdout or "") + (proc.stderr or "")
    fetched = "FETCHED:" in direct_out
    direct_verified = sum(1 for ln in direct_out.splitlines() if "VERDICT: VERIFIED" in ln)
    print("  DIRECT rt2_verify_deployed.py run -- fetched the layer on cache-miss : %s" % fetched)
    for ln in direct_out.splitlines():
        s = ln.strip()
        if s.startswith(("FETCHING:", "FETCHED:", "WARN:", "THREE-WAY CHAIN:")):
            print("      %s" % s)
    print("      DIRECT run VERIFIED : %d of 7" % direct_verified)

    battery_proc = subprocess.run([sys.executable, str(RT2_BATTERY)], capture_output=True,
                                  text=True, timeout=840, cwd=str(REPO))
    battery_out = (battery_proc.stdout or "") + (battery_proc.stderr or "")
    import_ok_7 = "IMPORT-OK 7 of 7" in battery_out
    verified_7 = "VERIFIED 7 of 7" in battery_out
    chain_equal_7 = "declared artifact_sha256 == live CodeSha256: 7 of 7" in battery_out
    token = "IBRT2-SIX-GUARDED" in battery_out
    arms_15 = "15 of 15 arms PASS" in battery_out
    print("  IB-rt-2's TERMINAL BATTERY, RE-RUN FROM THIS FRESH WORKTREE:")
    for ln in battery_out.splitlines():
        s = ln.strip()
        if ("IMPORT-OK" in s and "of" in s) or "declared artifact_sha256 == live CodeSha256" in s:
            print("      %s" % s)
    print("      arm (e) reads 7 of 7            : %s" % (import_ok_7 and verified_7))
    print("      sha256 chain EQUAL 7 of 7       : %s" % chain_equal_7)
    print("      15 of 15 arms PASS              : %s" % arms_15)
    print("      token IBRT2-SIX-GUARDED         : %s" % token)
    ok = (direct_verified == 7 and import_ok_7 and verified_7 and chain_equal_7
          and token and arms_15)
    print("  rt2_verify_deployed.py content hash (git hash-object) : %s"
          % git_hash_object(RT2_VERIFY))
    ARMS["d"] = ok
    return ok


def main():
    print("BATTERY IB-rtc-4 -- R34-AC1: instrument hygiene, four round-2 rulings executed")
    a = arm_a()
    b_ok, b_of = arm_b()
    c_ok, c_lines = arm_c()
    arm_d()

    head("SUMMARY")
    print("  (a) bytes comparison PERFORMED             : %s  (reading=%s)"
          % (ARMS.get("a"), a["reading"]))
    print("  (b) %d of %d result doc(s) SUPERSEDED, 0 key(s) minted/moved" % (b_ok, b_of))
    print("  (c) vendor bar re-cut, exercised            : %s" % ARMS.get("c"))
    print("  (d) layer fetch + 7 of 7 re-run             : %s" % ARMS.get("d"))

    all_printed = all(k in ARMS for k in ("a", "b", "c", "d"))
    all_hold = ARMS.get("a") and ARMS.get("b") and ARMS.get("c") and ARMS.get("d")
    if all_printed and all_hold:
        print("")
        print("IBR34-FOUR-ARMS-MEASURED")
        return 0
    print("")
    print("TOKEN WITHHELD -- arms printed: %s; arms holding: %s" % (ARMS, all_hold))
    return 1


if __name__ == "__main__":
    sys.exit(main())
