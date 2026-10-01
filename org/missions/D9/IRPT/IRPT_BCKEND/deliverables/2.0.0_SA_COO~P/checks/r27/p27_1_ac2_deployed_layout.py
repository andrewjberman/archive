"""Round 27 AC (IB-pr-271; CTO issuer rule 103370: a cell that changes an import in deployed code proves the import in the
DEPLOYED layout) -- every Lambda bundle that ships `_authz/served.py` can import the service-profile reader served.py now uses.

Usage: python p27_1_ac2_deployed_layout.py <worktree root>
For EVERY function in infra/aws/lambda/ci/lambda-source-map.json whose `files` list ships `served.py` (7 at the cut:
irpt-performance-adapter, irpt-directory-search, irpt-narrative, irpt-ycharts-generate, irpt-export-render, irpt-holdings,
irpt-status; any added since is included), MATERIALIZE the bundle's own file list into a clean temp directory the way the build lays it
out -- each `files` entry at its own relative path, its bytes taken from the matching `staged_from` entry's repo_path (the
worktree copy, i.e. the candidate) when one packages it, else from <source_dir>/<entry> -- then, in a FRESH python whose
sys.path is that directory prepended in isolated mode (stdlib and site-packages otherwise), import `served` and every module name served.py imports
INSIDE the service-principal branch (`_service_allowed_firms` or whatever function holds the new profile read; read by AST, so a
renamed function is still found by its `canonical_profile_reads` import).
Requires: served.py (worktree) references canonical_profile_reads; every such bundle imports it and its top-level closure.
Prints, per function: files in the list, files materialized, the import result.
Pass line: P27-1-AC2 PASS. Base: FAIL (served.py does not use a service-profile reader yet).
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SERVED = root / "infra/aws/lambda/investor-reporting/_authz/served.py"


def fail(msg):
    print("P27-1-AC2 FAIL: " + msg)
    sys.exit(1)


tree = ast.parse(SERVED.read_text(encoding="utf-8"))
lazy = set()
for fn in ast.walk(tree):
    if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
        mods = {n.module.split(".")[0] for n in ast.walk(fn) if isinstance(n, ast.ImportFrom) and n.module and not n.level}
        mods |= {a.name.split(".")[0] for n in ast.walk(fn) if isinstance(n, ast.Import) for a in n.names}
        if "canonical_profile_reads" in mods:
            lazy |= mods
if "canonical_profile_reads" not in lazy:
    fail("served.py does not import canonical_profile_reads inside any function (no service-profile reader yet)")
lazy.discard("__future__")
print("  modules imported by the service-profile branch: %s" % sorted(lazy))

smap = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))["functions"]
targets = {k: v for k, v in smap.items() if "served.py" in (v.get("files") or [])}
if not targets:
    fail("no function in the source map ships served.py")
bad = []
for fn, v in sorted(targets.items()):
    staged = {s.get("packaged_as"): s.get("repo_path") for s in (v.get("staged_from") or []) if isinstance(s, dict)}
    src_dir = root / (v.get("source_dir") or "")
    tmp = Path(tempfile.mkdtemp(prefix="p27_%s_" % fn))
    made, missing = 0, []
    try:
        for entry in v.get("files") or []:
            src = root / staged[entry] if entry in staged and staged[entry] else src_dir / entry
            if not src.is_file():
                missing.append(entry)
                continue
            dst = tmp / entry
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            made += 1
        # -I (isolated): no script dir, no PYTHONPATH, no user site; the stdlib and site-packages stay (boto3 is
        # runtime-provided in Lambda). The bundle directory is prepended, so every NON-stdlib module resolves from the
        # bundle or not at all.
        code = ("import sys; sys.path.insert(0, %r)\n"
                "import served\n"
                "for m in %r:\n"
                "    __import__(m)\n"
                "print('ok')\n") % (str(tmp), sorted(lazy))
        env = {k: val for k, val in os.environ.items() if k not in ("PYTHONPATH",)}
        env["IRPT_DIRECTORY_BUCKET_MAP"] = "{}"
        r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=90, env=env)
        ok = r.returncode == 0 and r.stdout.strip().endswith("ok")
        err = (r.stderr.strip().splitlines() or [""])[-1][:160]
        print("  %-26s files %2d, materialized %2d, missing %d%s -> %s" % (
            fn, len(v.get("files") or []), made, len(missing), (" %s" % missing[:3]) if missing else "",
            "imports OK" if ok else "IMPORT FAILS: " + err))
        if not ok:
            bad.append(fn)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
if bad:
    fail("%d of %d bundles shipping served.py cannot import the service-profile branch: %s" % (len(bad), len(targets), bad))
print("P27-1-AC2 PASS (%d of %d bundles import the branch in their own layout)" % (len(targets), len(targets)))
