"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Inflection launcher ASSUMES the narrow transaction role, and runs from a flat directory (cell DB-f-2705).

  The CTO's ruling (msg 10542, route B): the four-statement policy lives on a NEW role whose builder-made name matches role/*-inf-* (the cross-firm fence admits it);
  the runner role may assume it; the launcher assumes it for its reads and writes. This cell is the launcher's half.
  A DEFECT found while writing this cell (measured by the issuer): in the runner's flat-directory layout (the launcher, its bundle zip and receipt beside each other, NOT the repo
  layout) `orion_prefix()` REFUSES ("the naming registry is read from the repo layout only") before the bundle is ever opened, so `run()` cannot reach its first S3 listing there. The
  existing flat-directory test only exercised `plan()`. The launcher must read the naming registry through the verified bundle when it is not in the repo layout (as `_producers()` does).

  DBF139-5-AC1  `assumed_s3_client(sts=None, client_factory=None)`: the role ARN is arn:aws:iam::<caller account>:role/<builder name of the account-transaction role>, the session name is the
                fixed `g01-account-transaction`, the temporary credentials go to the S3 client, and a failed assume REFUSES naming the role (not the account)
  DBF139-5-AC2  `main()` with no injected client uses `assumed_s3_client()` (not a plain boto3 client) and with an injected client makes no STS call
  DBF139-5-AC3  a FLAT-directory run (launcher + zip + receipt only) completes `main(--dry-run)` against a fake S3 holding one synthetic snapshot and prints the S6 line

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAUNCHER = "data/inf/scripts/gold/INF_G_01.account_transaction_gold.py"
TESTS_DIR = "data/inf/scripts/gold/tests"
SESSION = "g01-account-transaction"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def load_launcher(root, path=None):
    p = Path(path) if path else Path(root, LAUNCHER)
    spec = importlib.util.spec_from_file_location("inf_g_01_assume_%d" % id(p), str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def expected_role_name(root):
    sys.path.insert(0, str(Path(root, "lib")))
    import opal_naming
    return opal_naming.name("orion", "inflection", "account-transaction", "role")


class FakeSts:
    def __init__(self, fail=False):
        self.fail = fail
        self.calls = []

    def get_caller_identity(self):
        self.calls.append(("get_caller_identity",))
        return {"Account": "111122223333"}

    def assume_role(self, **kw):
        self.calls.append(("assume_role", kw))
        if self.fail:
            raise RuntimeError("AccessDenied for 111122223333")
        return {"Credentials": {"AccessKeyId": "AKIATESTONLY", "SecretAccessKey": "secret-test", "SessionToken": "token-test"}}


def arn_problems(calls, role_name):
    """Problems with the recorded STS calls."""
    pr = []
    ar = [c for c in calls if c[0] == "assume_role"]
    if len(ar) != 1:
        return ["exactly one assume_role call is required (found %d)" % len(ar)]
    kw = ar[0][1]
    if kw.get("RoleArn") != "arn:aws:iam::111122223333:role/%s" % role_name:
        pr.append("RoleArn must be arn:aws:iam::<caller account>:role/%s (got %r)" % (role_name, kw.get("RoleArn")))
    if kw.get("RoleSessionName") != SESSION:
        pr.append("RoleSessionName must be the fixed %r (got %r)" % (SESSION, kw.get("RoleSessionName")))
    return pr


def ac1(root):
    L = load_launcher(root)
    need(getattr(L, "SESSION_NAME", None) == SESSION, "the launcher must carry SESSION_NAME = %r" % SESSION)
    need(callable(getattr(L, "assumed_s3_client", None)), "the launcher must define assumed_s3_client(sts=None, client_factory=None)")
    name = expected_role_name(root)
    sts = FakeSts()
    made = []

    def factory(service, **kw):
        made.append((service, kw))
        return ("s3-client", kw)

    out = L.assumed_s3_client(sts=sts, client_factory=factory)
    pr = arn_problems(sts.calls, name)
    if not (len(made) == 1 and made[0][0] == "s3" and made[0][1].get("aws_access_key_id") == "AKIATESTONLY" and made[0][1].get("aws_secret_access_key") == "secret-test"
            and made[0][1].get("aws_session_token") == "token-test"):
        pr.append("the S3 client must be built from the assumed credentials (aws_access_key_id, aws_secret_access_key, aws_session_token)")
    if out != ("s3-client", made[0][1] if made else None):
        pr.append("assumed_s3_client must return the client the factory made")
    bad = FakeSts(fail=True)
    try:
        L.assumed_s3_client(sts=bad, client_factory=factory)
        pr.append("a failed assume must REFUSE")
    except SystemExit as e:
        txt = str(e)
        if "REFUSED" not in txt or name not in txt or "111122223333" in txt:
            pr.append("a failed assume must REFUSE naming the role %s and never the account id: %r" % (name, txt[:160]))
    need(not pr, "; ".join(pr))


def ac2(root):
    L = load_launcher(root)
    need(callable(getattr(L, "assumed_s3_client", None)), "the launcher must define assumed_s3_client")
    summary = {"run_day": "2026-10-16", "snapshot": "2026-10-16", "upload": False, "rows_in": 1, "rows_planned": 1, "rows_out": 0, "days": [], "excluded": {},
               "price_null_reasons": {}, "window": {}, "s6": {"printed": "S6: 0 of 0"}}
    seen = {"assumed": 0, "run_s3": []}
    sentinel = object()
    other = object()

    def fake_assumed(*a, **k):
        seen["assumed"] += 1
        return sentinel

    def fake_run(s3, run_day, upload=True, since=None):
        seen["run_s3"].append(s3)
        return summary

    real_a, real_r = L.assumed_s3_client, L.run
    L.assumed_s3_client, L.run = fake_assumed, fake_run
    try:
        rc = L.main(["--date", "2026-10-16", "--dry-run"])
        pr = []
        if rc != 0 or seen["assumed"] != 1 or seen["run_s3"] != [sentinel]:
            pr.append("main() with no injected client must call assumed_s3_client() once and run with its client (got %d calls)" % seen["assumed"])
        L.main(["--date", "2026-10-16", "--dry-run"], s3=other)
        if seen["assumed"] != 1 or seen["run_s3"][-1] is not other:
            pr.append("main() with an injected client must not call assumed_s3_client()")
    finally:
        L.assumed_s3_client, L.run = real_a, real_r
    src = Path(root, LAUNCHER).read_text(encoding="utf-8")
    body = src[src.index("def main("):]
    if "boto3.client(" in body:
        pr.append("main() must not build a plain boto3 client: its reads and writes go through the assumed role")
    need(not pr, "; ".join(pr))


FLAT_SCRIPT = r'''
import importlib.util, io, sys
from contextlib import redirect_stdout
sys.path.insert(0, sys.argv[2])
import test_INF_G_01_account_transaction_gold as T
spec = importlib.util.spec_from_file_location("flat_launcher", sys.argv[1])
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)
s3 = T.FakeS3()
rows = [T.line(1, "2026-10-13"), T.line(2, "2026-10-14", desc="Client Contribution", amount=500.0, units=0.0), T.line(3, "2026-10-15")]
T.put_partition(s3, "2026-10-16", rows)
buf = io.StringIO()
with redirect_stdout(buf):
    rc = L.main(["--date", "2026-10-16", "--dry-run"], s3=s3)
out = buf.getvalue()
print("FLAT_RESULT rc=%s run_line=%s s6=%s puts=%d" % (rc, "INF_G_01 run_day" in out, "S6:" in out, len(s3.puts)))
'''


def ac3(root):
    root = str(Path(root).resolve())
    L = load_launcher(root)
    for fn in ("make_receipt", "build_bundle"):
        need(callable(getattr(L, fn, None)), "the launcher must define %s (cell DB-f-2701)" % fn)
    with tempfile.TemporaryDirectory() as td:
        flat = Path(td, "flat")
        flat.mkdir()
        dst = flat / Path(LAUNCHER).name
        shutil.copyfile(Path(root, LAUNCHER), dst)
        z = flat / "INF_G_01.bundle.zip"
        L.build_bundle(Path(root), z)
        (flat / "INF_G_01.bundle.receipt.json").write_text(json.dumps(L.make_receipt(Path(root), z)), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-c", FLAT_SCRIPT, str(dst), str(Path(root, TESTS_DIR))], capture_output=True, text=True, timeout=600, cwd=td)
        out = (r.stdout or "") + (r.stderr or "")
        line = next((ln for ln in out.splitlines() if ln.startswith("FLAT_RESULT")), None)
        need(line is not None, "the flat-directory run did not complete: %s" % out.strip()[-300:])
        need(line == "FLAT_RESULT rc=0 run_line=True s6=True puts=0", "the flat-directory dry run must print its run and S6 lines and write nothing: %s" % line)


def selftest():
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    good = [("get_caller_identity",), ("assume_role", {"RoleArn": "arn:aws:iam::111122223333:role/r", "RoleSessionName": SESSION})]
    arm("arn-green", arn_problems(good, "r"), [])
    arm("arn-wrong-role", len(arn_problems(good, "other")), 1)
    arm("arn-wrong-session", len(arn_problems([good[0], ("assume_role", {"RoleArn": "arn:aws:iam::111122223333:role/r", "RoleSessionName": "x"})], "r")), 1)
    arm("arn-two-assumes", len(arn_problems(good + [good[1]], "r")), 1)
    arm("arn-no-assume", len(arn_problems([good[0]], "r")), 1)
    sts = FakeSts()
    arm("fake-account", sts.get_caller_identity()["Account"], "111122223333")
    arm("fake-fail", FakeSts(fail=True).fail, True)
    arm("flat-script-has-result-line", "FLAT_RESULT" in FLAT_SCRIPT, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF139-5-AC1", "DBF139-5-AC2", "DBF139-5-AC3"):
        print("usage: p139_assume.py <repo_root> DBF139-5-AC1|AC2|AC3 | --selftest")
        return 2
    try:
        {"DBF139-5-AC1": ac1, "DBF139-5-AC2": ac2, "DBF139-5-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except SystemExit as e:
        print("reason: the launcher refused: %s" % (str(e)[:200],))
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
