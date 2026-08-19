"""BUILD_MANIFEST stamp coverage census (D0_TIGHTENING.TO-2, criterion T2a-2).

Measures stamp coverage on TWO PLANES and prints the denominator on BOTH sides, because
the two planes move independently and conflating them is how a builder-side improvement
gets reported as a deployed-side one:

  BUILDER plane   -- do the build_package.py homes emit a section-4b-complete stamp?
                     This is what TO-2 changes. Measurable at any git vintage.
  DEPLOYED plane  -- do the packages RUNNING in AWS carry the stamp?
                     TO-2 changes this for NOTHING until a rebuild+redeploy, which the TO
                     explicitly does not require. Reported so "coverage rose" cannot be
                     misread as "the deployed fleet improved".

Usage:
  python stamp_coverage_census.py --builders [--vintage <commit>]   # builder plane
  python stamp_coverage_census.py --deployed                        # live AWS read
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

def _workspace_root() -> Path:
    """Resolve the repo root the estate's canonical way -- NEVER a counted parent depth
    and never a baked path (CLAUDE.md device-agnostic rule).

    A counted depth is what broke the first run of this very census: parents[4] resolves
    to `org/`, so every working-tree read missed and the builder plane reported 0/0. It
    was caught only because this tool prints its DENOMINATOR -- a bare "0 complete" would
    have read as a real measurement instead of a broken retrieval.
    """
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       cwd=str(Path(__file__).resolve().parent),
                       capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    raise SystemExit("cannot resolve workspace root via git rev-parse --show-toplevel")


WS = _workspace_root()

HOMES = {
    "mdpf-gold-lambda":
        "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py",
    "opal-assets-mdpf-portal-publisher":
        "infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/build_package.py",
}

# The PRD section-4b IO contract, as four separately-checkable obligations.
CONTRACT = ["source_commit", "members_path_sha256", "zip_sha256", "built_at"]


def _src(path: str, vintage: str | None) -> str | None:
    """Read a file at a vintage. NEVER discards stderr: a mangled ref prints fatal: on
    stderr and returns CLEAN EMPTY stdout, which would render 'absent' out of a broken
    retrieval rather than a real absence."""
    if vintage is None:
        p = WS / path
        return p.read_text(encoding="utf-8") if p.exists() else None
    r = subprocess.run(["git", "show", f"{vintage}:{path}"],
                       cwd=str(WS), capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        print(f"  RETRIEVAL FAILED for {path}@{vintage}: rc={r.returncode} "
              f"{r.stderr.strip()[:160]}")
        return None
    return r.stdout


def audit_builder(src: str) -> dict:
    """Which contract obligations does this builder source actually satisfy?

    Checked structurally (does the emitted dict carry the key) rather than by bare
    substring, so a mention inside a comment cannot count as an emission.
    """
    out = dict.fromkeys(CONTRACT, False)
    out["emits_in_zip_manifest"] = "BUILD_MANIFEST.json" in src
    out["emits_sidecar"] = "sidecar" in src and "BUILD_MANIFEST.json" in src
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out
    keys: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.add(k.value)
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) \
                and isinstance(node.slice.value, str):
            keys.add(node.slice.value)
    out["source_commit"] = "source_vintage" in keys and "commit" in keys
    out["members_path_sha256"] = "modules" in keys and "sha256" in keys and "repo_path" in keys
    out["zip_sha256"] = "zip_sha256" in keys
    out["built_at"] = "built_at" in keys
    return out


def builders(vintage: str | None) -> int:
    label = vintage or "WORKING TREE"
    print("=" * 82)
    print(f"BUILDER-PLANE STAMP COVERAGE  --  vintage: {label}")
    print("=" * 82)
    rows = {}
    for name, path in HOMES.items():
        src = _src(path, vintage)
        rows[name] = audit_builder(src) if src else None
    complete = 0
    for name, r in rows.items():
        if r is None:
            print(f"\n  {name}: SOURCE UNREADABLE at this vintage -- not counted either way")
            continue
        sat = [c for c in CONTRACT if r[c]]
        ok = len(sat) == len(CONTRACT)
        complete += ok
        print(f"\n  {name}")
        print(f"    in-zip manifest emitted : {r['emits_in_zip_manifest']}")
        print(f"    sidecar emitted         : {r['emits_sidecar']}")
        for c in CONTRACT:
            print(f"    {c:22}: {'PRESENT' if r[c] else 'MISSING'}")
        print(f"    contract satisfied      : {len(sat)}/{len(CONTRACT)}"
              f"  -> {'COMPLETE' if ok else 'INCOMPLETE'}")
    n = len([r for r in rows.values() if r is not None])
    inzip = sum(1 for r in rows.values() if r and r["emits_in_zip_manifest"])
    side = sum(1 for r in rows.values() if r and r["emits_sidecar"])
    print(f"\n  TOTALS at {label}:")
    print(f"    homes emitting in-zip BUILD_MANIFEST : {inzip}/{n}  (denominator {n} homes)")
    print(f"    homes emitting a sidecar            : {side}/{n}  (denominator {n} homes)")
    print(f"    homes SECTION-4b COMPLETE           : {complete}/{n}  (denominator {n} homes)")
    return 0


def deployed() -> int:
    print("=" * 82)
    print("DEPLOYED-PLANE STAMP COVERAGE  --  live AWS read")
    print("=" * 82)
    n = ok = 0
    for fn in HOMES:
        n += 1
        r = subprocess.run(["aws", "lambda", "get-function", "--function-name", fn,
                            "--query", "Code.Location", "--output", "text"],
                           capture_output=True, text=True)
        loc = r.stdout.strip()
        if r.returncode != 0 or not loc or loc == "None":
            print(f"\n  {fn}: NOT RESOLVABLE -- reported, not silently skipped")
            continue
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "p.zip"
            c = subprocess.run(["curl", "-s", "-o", str(z), loc], capture_output=True)
            if c.returncode != 0 or not z.exists():
                print(f"\n  {fn}: DOWNLOAD FAILED -- reported, not silently skipped")
                continue
            try:
                zf = zipfile.ZipFile(z)
                has = "BUILD_MANIFEST.json" in zf.namelist()
                print(f"\n  {fn}: members={len(zf.namelist())} stamp={has}")
                if has:
                    m = json.loads(zf.read("BUILD_MANIFEST.json"))
                    print(f"    source_commit : {m.get('source_vintage', {}).get('commit', '(none)')}")
                    print(f"    zip_sha256    : {'PRESENT' if 'zip_sha256' in m else 'MISSING'}")
                    print(f"    built_at      : {'PRESENT' if 'built_at' in m else 'MISSING'}")
                    ok += 1
            except Exception as e:
                print(f"\n  {fn}: UNREADABLE {e}")
    print(f"\n  TOTALS: {ok}/{n} deployed packages carry an in-zip stamp "
          f"(denominator {n} functions -- the two TO-2 homes only, NOT the census's 188)")
    print("  NOTE: this plane cannot move until a rebuild+redeploy, which TO-2 explicitly")
    print("  does not require. A builder-side rise is NOT a deployed-side rise.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--builders", action="store_true")
    ap.add_argument("--deployed", action="store_true")
    ap.add_argument("--vintage", default=None)
    a = ap.parse_args()
    if a.deployed:
        sys.exit(deployed())
    sys.exit(builders(a.vintage))
