#!/usr/bin/env python3
"""RT2 PACKAGER -- build each guarded function's zip and PROVE it imports in the runtime layout.

WHY THIS EXISTS AND WHY NO EXISTING TEST REPLACES IT (row IRPT_BCKEND-W3-S26, and the issuer's
correction of 2026-09-11): `entry.py` and the modules it imports resolve in the REPOSITORY by
sibling-directory paths that do not exist at `/var/task`. An in-tree pytest run passes on a zip
that dies at cold start, and `CodeSha256` equality cannot see a missing module by construction --
a hash certifies bytes and nothing in the deploy path ever imports them. THE ONLY INSTRUMENT THAT
CAN SEE THIS is an extract-and-import in the flat layout, in a FRESH INTERPRETER, with the
repository stripped from `sys.path`. A saved-and-restored `sys.modules` is not isolation either.

THE MEMBER RESOLUTION IS THE BUILDER'S: `source_dir/<name>` first, then the flat shared roots
below. Slot ~3 measured this independently (14 of 14, 10 of 10, 27 of 27 -- nothing resolves
nowhere) and the drain's union rule stands: REMOVE NOTHING. `handler.py` for irpt-status resolves
from `directory/`, which looks wrong and is not.

THE ZIP RECIPE IS THE ONE PROVEN TO REPRODUCE THE LIVE ARTIFACTS BYTE-FOR-BYTE (3 of 3): sorted
arcnames, ZIP_DEFLATED at zlib default, date_time=(2026,9,11,0,0,0), external_attr=0o644<<16 and
create_system=0 -- that last member is the non-obvious one.

NO AWS CALL, NO UPLOAD, NO DEPLOY. This script builds into .scratch/ and reads.

ASCII only. Exit 0 always: the printed verdict is the result, never the exit code.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PKG = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
OUT = os.path.join(REPO, ".scratch", "rt2-zips")

# The flat shared roots, IN ORDER. `holdings/` is deliberately NOT a root: the enforce.py and
# errors.py in it are that function's own DECLARED vendored copies, pinned to an older commit.
SHARED_ROOTS = [
    os.path.join(PKG, "_authz"),
    os.path.join(PKG, "_scope"),
    os.path.join(PKG, "_keys"),
    os.path.join(PKG, "_ids"),
    os.path.join(PKG, "_gate"),
    os.path.join(PKG, "intake"),
    os.path.join(PKG, "directory"),
    os.path.join(REPO, "data"),
    os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "core"),
]

SIX = ["irpt-directory-search", "irpt-performance-adapter", "irpt-narrative",
       "irpt-export-render", "irpt-status", "irpt-ycharts-generate"]

# MEASURED FROM TERRAFORM AT THIS CUT, never from the layer map: `layers = []` means the zip is
# the only carrier. The layered three take ids/keys/jsonschema from irpt-common and MUST NOT gain
# a second copy of keys.py -- row IRPT_BCKEND-W3-S28 (the layer's keys.py and the tree's differ,
# two grammars are live, and it is not this order's to repair).
LAYERED = {"irpt-performance-adapter", "irpt-narrative", "irpt-export-render"}

ZIP_DATE = (2026, 9, 11, 0, 0, 0)


def source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


def resolve_member(function, source_dir, name):
    """(abs_path, where) the way the builder does: source_dir first, then the shared roots."""
    p = os.path.join(source_dir, name.replace("/", os.sep))
    if os.path.isfile(p):
        return p, "source_dir"
    for root in SHARED_ROOTS:
        q = os.path.join(root, os.path.basename(name))
        if os.path.isfile(q):
            return q, os.path.relpath(root, REPO).replace(os.sep, "/")
    return None, None


def build(function, entry_files, omit=()):
    """Build the zip. Returns (path, sha256_b64, members, unresolved)."""
    sm = source_map()["functions"][function]
    source_dir = os.path.join(REPO, sm["source_dir"].replace("/", os.sep))
    members, unresolved = {}, []
    for name in entry_files:
        if name in omit:
            continue
        path, _where = resolve_member(function, source_dir, name)
        if path is None:
            unresolved.append(name)
            continue
        members[name] = path
    os.makedirs(OUT, exist_ok=True)
    zip_path = os.path.join(OUT, "%s.zip" % function)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname in sorted(members):
            info = zipfile.ZipInfo(arcname, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.create_system = 0
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(members[arcname], "rb") as fh:
                zf.writestr(info, fh.read())
    with open(zip_path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).digest()
    import base64
    return zip_path, base64.b64encode(digest).decode("ascii"), members, unresolved


# THE PROBE. Run with `python -I` (isolated: no PYTHONPATH, no user site) from a temp directory
# OUTSIDE the repository, so sys.path is the script's own directory plus the standard library --
# exactly the shape of /var/task plus the runtime. The first version of this probe did
# `sys.path[:] = [os.getcwd()]`, which also removed the STANDARD LIBRARY and made all six
# functions fail on `No module named 'json'`: a probe that fails for its own reason reports
# IMPORT-FAIL on a sound artifact and, worse, makes the negative control fire for the wrong
# reason. So the repo's ABSENCE is now ASSERTED and printed rather than assumed, and the
# stdlib is left alone.
# THE LAYOUT IS `/var/task` PLUS, FOR AN ATTACHED LAYER, `/opt/python` -- and which functions
# have the second half is MEASURED FROM TERRAFORM (`layers = []` or an arn), never assumed. The
# layer directory handed to the probe is the LIVE irpt-common zip's own `python/`, downloaded
# from the layer version the roots attach, so `keys` and `ids` resolve here exactly as they
# resolve in the runtime -- from the layer, not from the tree.
IMPORT_PROBE = (
    "import sys, os\n"
    "TASK = os.path.dirname(os.path.abspath(__file__))\n"
    "LAYER = os.environ.get('RT2_LAYER_PYTHON') or ''\n"
    "sys.path.insert(0, TASK)\n"
    "if LAYER:\n"
    "    sys.path.insert(1, LAYER)\n"
    "repo_marks = [p for p in sys.path if 'investor-reporting' in p or 'wk-irpt' in p]\n"
    "assert not repo_marks, 'the repository is on sys.path: %r' % repo_marks\n"
    "print('sys.path: %d entry(ies), none in the repo; task dir + %s'\n"
    "      % (len(sys.path), 'LAYER /opt/python' if LAYER else 'NO layer (layers = [])'))\n"
    "import entry\n"
    "h = getattr(entry, 'lambda_handler', None)\n"
    "print('IMPORT-OK entry; lambda_handler=%s' % (h is not None))\n"
)

LAYER_ZIP = os.path.join(REPO, ".scratch", "layer", "irpt-common-5.zip")
_LAYER_DIR = []


def layer_python_dir():
    """The LIVE layer's `python/`, extracted once. Empty string if the zip is not present."""
    if _LAYER_DIR:
        return _LAYER_DIR[0]
    if not os.path.isfile(LAYER_ZIP):
        print("WARN: %s absent -- the layered functions cannot be probed in their real layout "
              "and are reported as such, never as a pass" % LAYER_ZIP)
        _LAYER_DIR.append("")
        return ""
    d = tempfile.mkdtemp(prefix="rt2-layer-")
    with zipfile.ZipFile(LAYER_ZIP) as zf:
        zf.extractall(d)
    _LAYER_DIR.append(os.path.join(d, "python"))
    return _LAYER_DIR[0]


def import_probe(zip_path, label, layered=False):
    """Extract to a temp dir OUTSIDE the repo and import `entry` in a FRESH interpreter.

    THE PROBE TOOK THREE VERSIONS AND THE FIRST TWO BOTH REPORTED IMPORT-FAIL ON ALL SIX, which
    is why the negative control is not optional here: a probe that fails for its OWN reason is
    indistinguishable from a broken artifact, and the control is what tells them apart.
      v1  sys.path[:] = [cwd]   removed the STANDARD LIBRARY too -> No module named 'json'
      v2  python -I alone       -I implies -P, so the SCRIPT'S OWN DIRECTORY is not on sys.path
                                and nothing in the zip was importable -> No module named 'entry'
      v3  (this one)            -I for isolation from PYTHONPATH and user site, and the task dir
                                inserted EXPLICITLY -- which is what the Lambda runtime does with
                                /var/task. The repo's absence is ASSERTED, not assumed.
    In v1 and v2 the negative control fired for the same wrong reason as the positive arm, so
    both arms agreeing is itself the tell that the instrument, not the artifact, was the subject.
    """
    tmp = tempfile.mkdtemp(prefix="rt2-import-")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        probe = os.path.join(tmp, "_probe.py")
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write(IMPORT_PROBE)
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        env.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")
        env["RT2_LAYER_PYTHON"] = layer_python_dir() if layered else ""
        proc = subprocess.run([sys.executable, "-I", "_probe.py"], cwd=tmp, env=env,
                              capture_output=True, text=True, timeout=120)
        out = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
        last = out[-1] if out else "(no output)"
        ok = proc.returncode == 0 and "IMPORT-OK" in (proc.stdout or "")
        print("      %-18s %s  %s" % (label, "IMPORT-OK  " if ok else "IMPORT-FAIL", last[:150]))
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def needed_files(function, declared):
    """The declared list PLUS what the guard needs, with nothing removed (the drain's union).

    ADDED ONLY WHERE IT RESOLVES NOWHERE TODAY: entry.py (the handler Terraform now names),
    served.py and loaders.py (this cell authored them and no function declares them), and the
    closure enforce/errors/resolve that served and enforce import. keys.py and ids.py are added
    ONLY for the layer-less functions -- the layered three resolve them from irpt-common, and
    giving them a second copy is the choice row W3-S28 says is not mine to make.
    """
    want = list(declared)
    add = ["entry.py", "served.py", "loaders.py", "enforce.py", "errors.py", "resolve.py"]
    if function not in LAYERED:
        add += ["keys.py", "ids.py"]
    for name in add:
        if name not in want:
            want.append(name)
    return want


def main():
    print("RT2 PACKAGER -- build, then import in the flat /var/task layout")
    print("repo: %s" % REPO)
    print("resolution: source_dir first, then %d shared root(s); REMOVE NOTHING"
          % len(SHARED_ROOTS))
    print("")
    sm = source_map()["functions"]
    results = []
    for function in SIX:
        declared = sm[function].get("files") or []
        want = needed_files(function, declared)
        added = [n for n in want if n not in declared]
        print("%s  (%s)" % (function, "LAYERED" if function in LAYERED else "LAYER-LESS"))
        print("    declared %d -> packaged %d (added %d: %s)"
              % (len(declared), len(want), len(added), ", ".join(added) or "none"))
        zip_path, sha, members, unresolved = build(function, want)
        where = {}
        source_dir = os.path.join(REPO, sm[function]["source_dir"].replace("/", os.sep))
        for name in want:
            _p, w = resolve_member(function, source_dir, name)
            where[w] = where.get(w, 0) + 1
        print("    resolved %d of %d: %s" % (len(members), len(want),
              ", ".join("%s=%d" % (k, v) for k, v in sorted(where.items()) if k)))
        if unresolved:
            print("    UNRESOLVED (%d): %s" % (len(unresolved), ", ".join(unresolved)))
        print("    zip: %s  sha256(b64)=%s" % (os.path.basename(zip_path), sha))
        layered = function in LAYERED
        ok = import_probe(zip_path, "POSITIVE", layered=layered)
        # THE NEGATIVE CONTROL, AND IT RUNS: the same build with served.py WITHHELD must FAIL to
        # import. A probe that cannot return the failing case is a constant wearing a
        # measurement's clothes -- and this exact build succeeded for months precisely because
        # nothing ever imported it. The control zip is built under a different name so it can
        # never be mistaken for a deployable artifact.
        neg_zip, _neg_sha, _neg_members, _neg_unres = build(
            function, want, omit=("served.py",))
        neg_named = os.path.join(OUT, "%s.NEGATIVE-CONTROL.zip" % function)
        shutil.move(neg_zip, neg_named)
        neg_ok = import_probe(neg_named, "NEGATIVE-CTL", layered=layered)
        control_fires = not neg_ok
        if not control_fires:
            print("      WARN: the negative control IMPORTED without served.py, so the positive "
                  "result above proves nothing about served.py being carried")
        # and rebuild the real artifact, because the control overwrote it
        zip_path, sha, members, unresolved = build(function, want)
        results.append((function, ok, sha, len(members), len(want), unresolved,
                        control_fires))
        print("")

    print("=== SUMMARY ===============================================")
    passed = sum(1 for r in results if r[1])
    controlled = sum(1 for r in results if r[6])
    for function, ok, sha, res, want, unresolved, ctl in results:
        print("  %-26s %-11s %d of %d member(s) resolved  control %s  sha256=%s"
              % (function, "IMPORT-OK" if ok else "IMPORT-FAIL", res, want,
                 "FIRES" if ctl else "DEAD", sha))
    print("  %d of %d function(s) import in the flat layout with the repo off sys.path, and "
          "%d of %d negative controls fire" % (passed, len(results), controlled, len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
