#!/usr/bin/env python
"""ADVI_INSURE.TO-H2-AE H2-AC3 -- exercise bd49f_insurance_nav_current.py in a FLAT TEMP DIR.

WHY A TEMP DIR AND NOT THE REPO: the defect this order fixes was invisible from the repo BY
CONSTRUCTION. In the repo there IS an `org/` above the runner, so `_workspace_root()` resolved
and every local run passed; the deployed bundle is flat at /tmp/advi_49f_code with no `org/` at
any depth (MEASURED: 83 objects under s3://opal-data-49financial/_code/, h-1). An exercise run
from the repo would have scored the fix PASS without touching the failure. So this script builds
the bundle's shape -- the runner plus its two flat siblings, nothing above them -- and runs there.

FIVE ARMS. The positives prove the fix works; the negatives prove this harness can SEE a failure,
which is the half a green run cannot establish on its own.

  A0 POSITIVE  --help in the flat dir: rc 0, import reached, argparse reached.
  A1 POSITIVE  the emit-path site: import the module and CALL _forbidden_census() on a real
               column list. An exercise that stops before this call has NOT exercised row
               ADVI_INSURE-S16's site -- that derivation ran at CALL time, not import, which is
               exactly why the import-safety fix alone did not reach it.
  A2 NEGATIVE  the PRE-FIX runner in the same flat dir -> import-time RuntimeError. If this arm
               passes, the harness cannot detect the original defect and its greens mean nothing.
  A3 NEGATIVE  runner_common.py removed -> loud import failure naming that module.
  A4 NEGATIVE  insurance_forbidden_field_census.py removed -> the same loud shape (S16's module).

A3/A4 assert the DESIGNED failure mode: one carrier, one failure mode. A missing sibling is a
deploy defect the log must NAME at this file's own import line, never a silent default.

Run:  python ADVI_INSURE.TO-H2-AE_flat_bundle_exercise.py [--out <file>]
rc 0 = all five arms as expected. rc 1 = at least one arm did not.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

REPO_RUNNERS = os.path.join("data", "assets", "scripts", "gold", "runners_49f")
RUNNER = "bd49f_insurance_nav_current.py"
SIBLINGS = ["runner_common.py", "insurance_forbidden_field_census.py"]

# The pre-fix runner is pinned by COMMIT, not by "HEAD~1": once the fix commits, HEAD is the
# fixed file, and a relative ref would silently start comparing the fix against itself.
PREFIX_COMMIT = "bcb7f8a877"

EXPECTED_BUCKET = "opal-data-assets"  # the VALUE, never the carrier's NAME (rc.SILVER_BUCKET
# and silver_registry.ASSETS_BUCKET are two names for it; asserting the name would pass on the
# wrong carrier and fail on the right one).


def _repo_root() -> str:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _stage(root: str, tmp: str, files: list) -> None:
    for f in files:
        shutil.copyfile(os.path.join(root, REPO_RUNNERS, f), os.path.join(tmp, f))


def _assert_no_org_above(tmp: str, log: list) -> bool:
    """The whole point of the temp dir. If an `org/` sits above it the arms are meaningless."""
    cur = os.path.abspath(tmp)
    while True:
        if os.path.isdir(os.path.join(cur, "org")):
            log.append("  PRECONDITION FAILED: an org/ dir exists at %s -- the flat-bundle "
                       "shape is not reproduced and every arm below is void." % cur)
            return False
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    log.append("  PRECONDITION OK: no org/ directory at any level above %s" % tmp)
    return True


def _run(tmp: str, args: list) -> tuple:
    p = subprocess.run([sys.executable, RUNNER] + args, cwd=tmp,
                       capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    root = _repo_root()
    log = []
    results = {}

    def say(s=""):
        print(s)
        log.append(s)

    say("ADVI_INSURE.TO-H2-AE H2-AC3 -- flat-bundle exercise")
    say("repo root: %s" % root)
    say("pre-fix runner pinned at commit %s" % PREFIX_COMMIT)
    say("")

    # ---------------- A0 + A1: the fixed runner in a flat dir ----------------
    tmp = tempfile.mkdtemp(prefix="h2ae_flat_")
    try:
        _stage(root, tmp, [RUNNER] + SIBLINGS)
        say("ARM A0/A1 dir: %s" % tmp)
        say("  staged: %s" % sorted(os.listdir(tmp)))
        if not _assert_no_org_above(tmp, log):
            results["precondition"] = False
        else:
            results["precondition"] = True

        rc, out = _run(tmp, ["--help"])
        ok = rc == 0 and ("usage" in out.lower() or "--date" in out)
        results["A0_help_rc0"] = ok
        say("  A0 --help rc=%d -> %s" % (rc, "PASS" if ok else "FAIL"))
        if not ok:
            say("     output: %s" % out.strip()[:400])

        # A1 -- the emit-path site, called directly. This is S16's line.
        probe = (
            "import sys, json\n"
            "sys.path.insert(0, %r)\n"
            "import bd49f_insurance_nav_current as m\n"
            "res = {}\n"
            "res['bucket'] = m.ASSETS_BUCKET\n"
            "cols = ['relationship_id','account_number','nav','as_of_date','ssn']\n"
            "c = m._forbidden_census(cols)\n"
            "res['census_type'] = type(c).__name__\n"
            "res['census_keys'] = sorted(c.keys())[:6] if hasattr(c,'keys') else None\n"
            "print(json.dumps(res))\n" % tmp
        )
        p = subprocess.run([sys.executable, "-c", probe], cwd=tmp,
                           capture_output=True, text=True)
        a1_out = (p.stdout or "") + (p.stderr or "")
        a1_ok = p.returncode == 0 and EXPECTED_BUCKET in a1_out
        results["A1_emit_path_census_called"] = a1_ok
        say("  A1 import + ASSETS_BUCKET + _forbidden_census() rc=%d -> %s"
            % (p.returncode, "PASS" if a1_ok else "FAIL"))
        say("     %s" % a1_out.strip()[:600])
        say("     bucket asserted by VALUE (%r), not by carrier name" % EXPECTED_BUCKET)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    say("")

    # ---------------- A2: the PRE-FIX runner, same shape ----------------
    tmp = tempfile.mkdtemp(prefix="h2ae_prefix_")
    try:
        _stage(root, tmp, SIBLINGS)
        blob = subprocess.run(
            ["git", "show", "%s:%s" % (PREFIX_COMMIT, (REPO_RUNNERS + "/" + RUNNER).replace(os.sep, "/"))],
            cwd=root, capture_output=True, text=True)
        if blob.returncode != 0 or not blob.stdout:
            say("ARM A2: could not read the pre-fix blob (rc=%d) -- arm VOID, not passed"
                % blob.returncode)
            results["A2_prefix_raises"] = False
        else:
            with open(os.path.join(tmp, RUNNER), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(blob.stdout)
            rc, out = _run(tmp, ["--help"])
            ok = rc != 0 and "could not derive the workspace root" in out
            results["A2_prefix_raises"] = ok
            say("ARM A2 (negative -- pre-fix runner) rc=%d -> %s" % (rc, "PASS" if ok else "FAIL"))
            say("     %s" % out.strip().splitlines()[-1][:300] if out.strip() else "     (no output)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    say("")

    # ---------------- A3 / A4: a missing sibling must fail LOUDLY, by name ----------------
    for arm, missing in (("A3", "runner_common.py"),
                         ("A4", "insurance_forbidden_field_census.py")):
        tmp = tempfile.mkdtemp(prefix="h2ae_%s_" % arm.lower())
        try:
            keep = [f for f in SIBLINGS if f != missing]
            _stage(root, tmp, [RUNNER] + keep)
            rc, out = _run(tmp, ["--help"])
            mod = missing[:-3]
            ok = rc != 0 and mod in out and ("ModuleNotFoundError" in out or "ImportError" in out)
            results["%s_missing_%s_loud" % (arm, mod)] = ok
            say("ARM %s (negative -- %s removed) rc=%d -> %s"
                % (arm, missing, rc, "PASS" if ok else "FAIL"))
            last = out.strip().splitlines()[-1] if out.strip() else "(no output)"
            say("     %s" % last[:300])
            say("     names the module at this file's own import line: %s" % ("YES" if mod in out else "NO"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    say("")

    say("RESULTS (denominator %d arms):" % len(results))
    for k, v in results.items():
        say("  %-42s %s" % (k, "PASS" if v else "FAIL"))
    rc_final = 0 if all(results.values()) else 1
    say("")
    say("VERDICT: %s" % ("ALL ARMS AS EXPECTED (rc 0)" if rc_final == 0
                         else "AT LEAST ONE ARM NOT AS EXPECTED (rc 1)"))

    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(log) + "\n")
        print("written: %s" % a.out)
    return rc_final


if __name__ == "__main__":
    raise SystemExit(main())
