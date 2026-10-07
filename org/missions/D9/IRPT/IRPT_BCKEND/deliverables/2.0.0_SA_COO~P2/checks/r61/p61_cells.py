"""IRPT_BCKEND round 61 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- the mechanical checks of cells IB-pr-329..335,
cut from the CTO round analysis @e363a194ed section 5 (E-P1..E-P7).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB61-1-AC1  E-P1: ci/tests/test_build_artifact_key.sh passes against the worktree's builder AND fails against the base
              builder (BAU_BUILDER=<base copy>). Base: FAIL (no test).
  IB61-1-AC2  E-P1: BUILD_ONLY=1 of each irpt-49f-reporting-{read,gold,publish}-lambda prints "key=<k>" with <k> equal to that
              function's artifact_s3_key in lambda-source-map.json. Base: FAIL (no key printed).
  IB61-2-AC1  E-P2: ci/tests/test_record_terraform_deploy_paths.sh passes (dirty audit file present -> the recorder's commit
              carries only its own paths; a forced retry adds no second CHANGELOG entry). Base: FAIL (no test).
  IB61-3-AC1  E-P3: ci/tests/test_release_census.py passes (a planted extra file is reported), and release-census.py
              reads no worker-written census file. Base: FAIL (no tool).
  IB61-3-AC2  E-P3: release-census.py irpt-ycharts-generate --pin f36a8cdefd prints changed_members=19. Base: FAIL.
  IB61-4-AC1  E-P4: BUILD_ONLY=1 irpt-performance-adapter exits 0 past the ADHC_DRIFTD.002 parity gate, and none of
              build_candidate.py, build_dependencies.py, cot_probe.py sits at the top level of performance/. Base: FAIL.
  IB61-5-AC1  E-P5: directory/tests/test_refresh_manifest_dispatch_date.py passes (names 2026-10-06, dispatched_for, READY),
              and the directory suite passes with 0 failed. Base: FAIL (no test).
  IB61-6-AC1  E-P6: directory/tests/test_search_overage.py passes (names MAX_AGE_TRADING_DAYS and an over-age answer), and
              the directory suite passes with 0 failed. Base: FAIL (no test).
  IB61-6-AC2  E-P6: BUILD_ONLY=1 irpt-directory-search exits 0 and its zip carries expiry.py. Base: FAIL.
  IB61-7-AC1  E-P7: the committed transcript IB61-7_replay_output.json reads overall_pass true, route_count > 0, every
              route's arms present, and every gated arm carrying a reason. Base: FAIL (no transcript).
  IB61-G-<n>  A GUARD for slot ~<n>: that worker's own commits touch only its order's grant. Base: PASS.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BASE = "6e462d3499"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
CI = "infra/aws/lambda/ci"
IR = "infra/aws/lambda/investor-reporting"
MAP = CI + "/lambda-source-map.json"
REPORTING = ("irpt-49f-reporting-read-lambda", "irpt-49f-reporting-gold-lambda", "irpt-49f-reporting-publish-lambda")
TOOL_FILES = ("build_candidate.py", "build_dependencies.py", "cot_probe.py")
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
GRANTS = {
    "132": (CI + "/build-and-upload.sh", CI + "/tests/test_build_artifact_key.sh", CH, TO + "329.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~132/"),
    "133": (CI + "/record-terraform-deploy.sh", CI + "/tests/test_record_terraform_deploy_paths.sh", CH, TO + "330.",
            P + "/deliverables/0.9.0_WK_IRPT_BCKEND~133/"),
    "134": (CI + "/release-census.py", CI + "/tests/test_release_census.py", CH, TO + "331.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~134/"),
    "135": (IR + "/performance/", CH, TO + "332.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~135/"),
    "136": (IR + "/directory/", MAP, CH, TO + "333.", TO + "334.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~136/"),
    "137": (CH, TO + "335.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~137/"),
}
SCRATCH = None


def _run(cmd, root, env=None, timeout=110):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, env=e, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def _bash():
    return os.environ.get("BASH_EXE") or "bash"


def _build_only(root, fn):
    tmp = tempfile.mkdtemp(prefix="p61-")
    rc, out = _run([_bash(), CI + "/build-and-upload.sh", "investor-reporting", fn], root,
                   env={"BUILD_ONLY": "1", "TMPDIR": tmp})
    line = next((ln for ln in out.splitlines() if ln.startswith("BUILD_ONLY: ")), "")
    return rc, out, line, tmp


def _pytest(root, cwd_rel, target):
    rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], Path(root) / cwd_rel)
    return rc, _last(out)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB61"))
        sys.exit(1)

    if cid == "IB61-1-AC1":
        t = root / CI / "tests/test_build_artifact_key.sh"
        if not t.is_file():
            fail("no %s/tests/test_build_artifact_key.sh" % CI)
        rc, out = _run([_bash(), str(t)], root)
        if rc:
            fail("test fails against the worktree builder: %s" % _last(out))
        base_copy = Path(tempfile.mkdtemp(prefix="p61-base-")) / "build-and-upload.sh"
        r = subprocess.run(["git", "show", "%s:%s/build-and-upload.sh" % (BASE, CI)], cwd=str(root), capture_output=True)
        if r.returncode:
            fail("git show of the base builder failed")
        base_copy.write_bytes(r.stdout)
        rc2, out2 = _run([_bash(), str(t)], root, env={"BAU_BUILDER": str(base_copy)})
        if rc2 == 0:
            fail("test PASSES against the base builder %s, so it does not discriminate" % BASE)
        print("OK: test passes on the worktree builder; fails on the base builder (rc %d: %s)" % (rc2, _last(out2)))
    elif cid == "IB61-1-AC2":
        m = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]
        for fn in REPORTING:
            want = m[fn].get("artifact_s3_key")
            rc, out, line, _t = _build_only(root, fn)
            km = re.search(r"\bkey=(\S+)", line)
            if rc or not km:
                fail("%s: BUILD_ONLY rc %d, line %r carries no key=" % (fn, rc, line[:200]))
            if km.group(1) != want:
                fail("%s: builder key %s != map artifact_s3_key %s" % (fn, km.group(1), want))
            print("OK: %s key=%s = map" % (fn, km.group(1)))
    elif cid == "IB61-2-AC1":
        t = root / CI / "tests/test_record_terraform_deploy_paths.sh"
        if not t.is_file():
            fail("no %s/tests/test_record_terraform_deploy_paths.sh" % CI)
        rc, out = _run([_bash(), str(t)], root)
        if rc:
            fail("test: %s" % _last(out))
        print("OK: %s" % _last(out))
    elif cid == "IB61-3-AC1":
        tool = root / CI / "release-census.py"
        t = root / CI / "tests/test_release_census.py"
        if not tool.is_file() or not t.is_file():
            fail("tool or test absent")
        if re.search(r"CENSUS[A-Z0-9_]*\.json", tool.read_text(encoding="utf-8")):
            fail("release-census.py names a census .json file (it must read none)")
        rc, last = _pytest(root, CI + "/tests", "test_release_census.py")
        if rc or re.search(r"\d+ (failed|error)", last) or "passed" not in last:
            fail("tests: %s" % last)
        if "planted" not in t.read_text(encoding="utf-8"):
            fail("no planted-extra-file test")
        print("OK: %s" % last)
    elif cid == "IB61-3-AC2":
        tool = root / CI / "release-census.py"
        if not tool.is_file():
            fail("no release-census.py")
        rc, out = _run([sys.executable, str(tool), "irpt-ycharts-generate", "--pin", "f36a8cdefd"], root)
        m = re.search(r"changed_members=(\d+)", out)
        if rc or not m:
            fail("rc %d, no changed_members= line: %s" % (rc, _last(out)))
        if int(m.group(1)) != 19:
            fail("changed_members=%s, expected 19 (the issuer's re-census at f36a8cdefd)" % m.group(1))
        print("OK: changed_members=19")
    elif cid == "IB61-4-AC1":
        top = [f for f in TOOL_FILES if (root / IR / "performance" / f).is_file()]
        if top:
            fail("still at the top level of performance/: %s" % top)
        rc, out, line, _t = _build_only(root, "irpt-performance-adapter")
        if rc or not line:
            m = re.search(r"ADHC_DRIFTD\.002[^\n]*", out)
            fail("BUILD_ONLY rc %d; %s" % (rc, m.group(0) if m else _last(out)))
        print("OK: %s" % line[:160])
    elif cid in ("IB61-5-AC1", "IB61-6-AC1"):
        name, words = (("test_refresh_manifest_dispatch_date.py", ("2026-10-06", "dispatched_for", "READY"))
                       if cid == "IB61-5-AC1" else ("test_search_overage.py", ("MAX_AGE_TRADING_DAYS", "over")))
        t = root / IR / "directory/tests" / name
        if not t.is_file():
            fail("no directory/tests/%s" % name)
        src = t.read_text(encoding="utf-8")
        for w in words:
            if w not in src:
                fail("%s never names %r" % (name, w))
        rc, last = _pytest(root, IR + "/directory", "tests/" + name)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        rc, last2 = _pytest(root, IR + "/directory", "tests/")
        if rc or re.search(r"\d+ (failed|error)", last2):
            fail("directory suite: %s" % last2)
        print("OK: new %s; suite %s" % (last, last2))
    elif cid == "IB61-6-AC2":
        rc, out, line, tmp = _build_only(root, "irpt-directory-search")
        zp = os.path.join(tmp, "lambda-artifact-irpt-directory-search.zip")
        if rc or not line or not os.path.isfile(zp):
            fail("BUILD_ONLY rc %d, zip %s: %s" % (rc, "present" if os.path.isfile(zp) else "absent", _last(out)))
        names = zipfile.ZipFile(zp).namelist()
        if "expiry.py" not in names:
            fail("the irpt-directory-search zip carries no expiry.py (%d members)" % len(names))
        print("OK: expiry.py in the build (%d members)" % len(names))
    elif cid == "IB61-7-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~137/IB61-7_replay_output.json"
        if not f.is_file():
            fail("no transcript %s" % f.name)
        d = json.loads(f.read_text(encoding="utf-8"))
        routes = d.get("routes") or []
        if not d.get("overall_pass") or not d.get("route_count") or d.get("route_count") != len(routes):
            fail("overall_pass %r, route_count %r, routes listed %d" % (d.get("overall_pass"), d.get("route_count"), len(routes)))
        for r in routes:
            for arm in ("service_principal", "advisor_principal", "revoked_grant_warm_cache", "negative_no_protected_field"):
                a = r.get(arm)
                if not isinstance(a, dict) or a.get("state") not in ("DRIVEN-PASS", "GATED"):
                    fail("route %s arm %s: %r" % (r.get("route"), arm, a))
                if a["state"] == "GATED" and not a.get("reason"):
                    fail("route %s arm %s GATED with no reason" % (r.get("route"), arm))
        print("OK: %d routes, every arm DRIVEN-PASS or GATED with a reason" % len(routes))
    elif cid.startswith("IB61-G-"):
        slot = cid.rsplit("-", 1)[1]
        grant = GRANTS.get(slot)
        if not grant:
            fail("unknown slot %r" % slot)
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~%s" % slot, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~%s's grant" % (len(changed), slot))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
