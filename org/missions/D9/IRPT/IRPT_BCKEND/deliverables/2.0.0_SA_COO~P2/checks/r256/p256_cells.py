"""IRPT_BCKEND workstream ~PM round 14 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: a failed directory build must not wedge every later fire (CTO ruling on row D2-S239, msg 10699).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBCW2  IB-cw-2  refresh.py records the failed command's id and status in the failure manifest, and the NEXT fire treats a reported failed command as terminal and re-dispatches once
    AC1  the six named tests exist in tests/test_refresh_failed_command_redispatch.py and ALL pass (run now)
    AC2  DIFFERENTIAL: a Success previous command and an in-flight previous command produce, from the BASE refresh.py (HEAD~1) and from the NEW one, byte-identical results and the same SSM calls (run now, both modules, one fixture)
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only refresh.py, the new test file and the order's paths, and both code files are in it
"""
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

DIRP = "infra/aws/lambda/investor-reporting/directory"
RUNNER = DIRP + "/refresh.py"
TESTS = DIRP + "/tests/test_refresh_failed_command_redispatch.py"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~457/"
NAMES = (
    "test_a_failed_previous_command_is_reported_with_its_id_and_status",
    "test_the_failure_record_carries_no_error_text",
    "test_an_unreported_failed_command_is_reported_and_not_redispatched",
    "test_a_reported_failed_command_is_terminal_and_the_fire_redispatches_exactly_once",
    "test_an_in_flight_command_returns_without_dispatch",
    "test_a_fire_never_dispatches_twice",
)
fail = P6.fail


def ac1(_):
    f = P6.ROOT / TESTS
    if not f.is_file():
        fail("no %s" % TESTS)
    src = f.read_text(encoding="utf-8")
    missing = [n for n in NAMES if "def %s(" % n not in src]
    if missing:
        fail("missing tests: %s" % ", ".join(missing))
    p = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-rA", "--color=no", "-p", "no:cacheprovider"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=300)
    out = p.stdout
    if p.returncode != 0:
        fail("pytest rc %s: %s" % (p.returncode, out[-300:].replace("\n", " | ")))
    passed = {ln.strip().split("::")[-1].strip() for ln in out.replace("\\", "/").splitlines()
              if ln.startswith("PASSED ") and "test_refresh_failed_command_redispatch.py::" in ln}
    notpassed = [n for n in NAMES if n not in passed]
    if notpassed:
        fail("named tests not reported PASSED: %s" % ", ".join(notpassed))
    print("OK: the six named tests exist and all pass")


class FakeS3(object):
    """list_objects_v2 and get_object over a dict of key -> bytes."""

    def __init__(self, objs):
        self.objs = dict(objs)

    def list_objects_v2(self, Bucket, Prefix, MaxKeys=1000, ContinuationToken=None):
        return {"Contents": [{"Key": k} for k in sorted(self.objs) if k.startswith(Prefix)][:MaxKeys]}

    def get_object(self, Bucket, Key):
        return {"Body": io.BytesIO(self.objs[Key])}


class FakeSSM(object):
    def __init__(self, status):
        self.status = status
        self.calls = []

    def describe_instance_information(self, **kw):
        self.calls.append(("describe_instance_information", json.dumps(kw, sort_keys=True)))
        return {"InstanceInformationList": [{"PingStatus": "Online"}]}

    def get_command_invocation(self, **kw):
        self.calls.append(("get_command_invocation", json.dumps(kw, sort_keys=True)))
        return {"Status": self.status}

    def send_command(self, **kw):
        self.calls.append(("send_command", json.dumps(kw, sort_keys=True, default=str)))
        return {"Command": {"CommandId": "cmd-new"}}


def _load(name, dirpath):
    spec = importlib.util.spec_from_file_location(name, str(Path(dirpath) / "refresh.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(dirpath))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(dirpath))
    return mod


def _fixture_result(mod, status):
    artifact_key = "investor-reporting/directory/2026-10-14/directory.json"
    objs = {
        "investor-reporting/directory/latest.json": json.dumps({"key": artifact_key, "as_of_business_date": "2026-10-14", "source_completion_date": "2026-10-14", "directory_revision": "r1"}).encode("utf-8"),
        artifact_key: json.dumps({"entries": [], "source_client_ids": []}).encode("utf-8"),
    }
    s3 = FakeS3(objs)
    ssm = FakeSSM(status)
    prev = {"as_of_business_date": "2026-10-13", "reason_code": "REFRESH_COMPLETED",
            "delta": {"ssm_command_id": "cmd-old", "dispatched_for": "2026-10-14", "directory_key": "investor-reporting/directory/2026-10-13/directory.json"}}
    d = mod.SsmBuildDispatcher("bucket-x", previous_manifest=prev, instance_id="i-fixture", bundle_uri="s3://bundle-x/k", ssm_client=ssm, s3_client=s3)
    try:
        res = d("cottonwood", "2026-10-15")
        out = {"result": res}
    except Exception as exc:                        # noqa: BLE001 -- the differential compares even a raise
        out = {"raised": type(exc).__name__, "token": getattr(exc, "token", None), "detail": str(getattr(exc, "detail", ""))}
    return json.dumps(out, sort_keys=True, default=str), ssm.calls


def ac2(_):
    new_dir = P6.ROOT / DIRP
    if not (new_dir / "refresh.py").is_file():
        fail("no %s" % RUNNER)
    g = subprocess.run(["git", "show", "HEAD~1:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    if g.returncode != 0:
        fail("cannot read the base refresh.py at HEAD~1: %s" % g.stderr.decode("utf-8", "replace").strip()[:200])
    h = subprocess.run(["git", "show", "HEAD:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    if h.returncode != 0:
        fail("cannot read refresh.py at HEAD: %s" % h.stderr.decode("utf-8", "replace").strip()[:200])
    if g.stdout == h.stdout:
        fail("refresh.py is byte-identical to the base: a differential over an unchanged file proves nothing")
    tmp = Path(tempfile.mkdtemp(prefix="p256_base_"))
    try:
        (tmp / "refresh.py").write_bytes(g.stdout)
        for sib in ("expiry.py",):
            s = new_dir / sib
            if not s.is_file():
                fail("no sibling %s to load the base module" % sib)
            shutil.copy(str(s), str(tmp / sib))
        base = _load("p256_refresh_base", tmp)
        new = _load("p256_refresh_new", new_dir)
        for status in ("Success", "InProgress"):
            b = _fixture_result(base, status)
            n = _fixture_result(new, status)
            if b != n:
                fail("the %s path differs between the base and the new refresh.py:\n base %s\n new  %s" % (status, b[0][:200], n[0][:200]))
            if status == "Success" and '"result"' not in b[0]:
                fail("the Success fixture did not produce a result (the fixture itself is broken): %s" % b[0][:200])
            if status == "InProgress" and any(c[0] == "send_command" for c in n[1]):
                fail("the in-flight path dispatched")
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
    print("OK: the Success and in-flight paths are byte-identical, with the same SSM calls, base versus new")


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if RUNNER not in files or TESTS not in files:
        fail("the worker's commit must contain both refresh.py and the new test file; it contains %s" % files)
    bad = [x for x in files if x not in (RUNNER, TESTS) and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-cw-2" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, refresh.py and the new test file in it, nothing outside the order's paths")


CHECKS = {"IBCW2-AC1": ac1, "IBCW2-AC2": ac2, "IBCW2-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p256_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
