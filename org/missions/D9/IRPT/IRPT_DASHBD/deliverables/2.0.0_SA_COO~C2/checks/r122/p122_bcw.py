"""IRPT_DASHBD round 122, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood account_dim producer CODE (adapter upload path + Lambda entry point + tests).

  DBC122-1-AC1 every named test exists in its file and pytest passes on both test files
  DBC122-2-AC1 the bounds: only the five product files changed since BASE; lambda_function.py is ASCII, types no firm token, bucket or silver prefix, creates no boto3 client at import;
               the adapter's constants, schema and build_account_dim are byte-identical to BASE; a planted control (the refusal removed in a scratch copy) fails the refusal test

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "05ea78f452"
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py"
ADAPTER_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_account_dim.py"
LAMBDA = "infra/aws/lambda/investor-reporting/account-dim-cot/lambda_function.py"
LAMBDA_TEST = "infra/aws/lambda/investor-reporting/account-dim-cot/tests/test_lambda_function.py"
CONFTEST = "infra/aws/lambda/investor-reporting/account-dim-cot/tests/conftest.py"
ALLOWED = {ADAPTER, ADAPTER_TEST, LAMBDA, LAMBDA_TEST, CONFTEST}
PRODUCT_DIRS = ("infra", "data", "lib", ".tools", "docs")
ADAPTER_TESTS = ("test_default_emit_writes_nothing", "test_upload_requires_an_s3_client", "test_upload_refuses_a_non_empty_partition",
                 "test_upload_writes_exactly_one_key", "test_schema_hash_matches_contract")
LAMBDA_TESTS = ("test_target_day_is_the_t_minus_1_trading_day", "test_silver_locations_name_both_tables_at_the_day",
                "test_hold_on_absent_silver_raises_and_writes_nothing", "test_already_landed_partition_returns_without_reading_silver",
                "test_event_date_overrides_the_frontier", "test_handler_lands_one_key_for_a_present_silver")
FORBIDDEN_TOKENS = ("cottonwood", "z09", "opal-data-assets", "opal-data-cottonwood", "blackdiamond/")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, timeout=60)
    need(r.returncode == 0, "git %s failed rc=%s: %s" % (args[0], r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def pytest(root, *files, env_extra=None):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files)
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=110)
    return r.returncode, (r.stdout + r.stderr)[-600:]


def ac_1(root):
    for rel, names in ((ADAPTER_TEST, ADAPTER_TESTS), (LAMBDA_TEST, LAMBDA_TESTS)):
        p = Path(root) / rel
        need(p.is_file(), "test file absent: " + rel)
        txt = p.read_text(encoding="utf-8")
        for n in names:
            need(re.search(r"^def %s\(" % re.escape(n), txt, re.M) is not None, "named test absent: %s in %s" % (n, rel))
    need("test_emit_defaults_to_no_write_and_upload_is_refused" not in (Path(root) / ADAPTER_TEST).read_text(encoding="utf-8"),
         "the old upload-refused test is still present")
    rc, tail = pytest(root, ADAPTER_TEST, LAMBDA_TEST)
    need(rc == 0, "pytest failed: " + tail.replace("\n", " | ")[-300:])


def adapter_frozen_part(text):
    """Everything above emit_account_dim's def, minus the docstring head (the docstring's last paragraph may change)."""
    i = text.index("def emit_account_dim")
    body = text[:i]
    j = body.index('"""', 3)
    return body[j + 3:]


def ac_2(root):
    root = Path(root)
    changed = sorted({p for p in git(root, "log", "--first-parent", "--no-merges", "--name-only", "--format=", BASE + "..HEAD", "--", *PRODUCT_DIRS).splitlines() if p.strip()})  # the worker's own commits; a pull-merge of the shared branch adds none of its own
    need(changed, "no product file changed since the base")
    extra = sorted(set(changed) - ALLOWED)
    need(not extra, "product files outside the grant changed: " + ", ".join(extra))
    lam = root / LAMBDA
    need(lam.is_file(), "lambda_function.py absent")
    raw = lam.read_bytes()
    need(all(b < 128 for b in raw), "lambda_function.py carries non-ASCII bytes")
    low = raw.decode("ascii").lower().replace("cottonwood_account_dim", "")  # the adapter module name is an import, not a typed firm token
    for tok in FORBIDDEN_TOKENS:
        need(tok not in low, "lambda_function.py types a forbidden token: " + tok)
    for line in low.splitlines():
        need(not (line[:1].isalpha() and "boto3.client(" in line), "a boto3 client is created at module level")
    need(re.search(r"^def lambda_handler\(event, context=None\)", raw.decode("ascii"), re.M) is not None, "lambda_handler signature absent")
    now = (root / ADAPTER).read_text(encoding="utf-8")
    old = git(root, "show", "%s:%s" % (BASE, ADAPTER))
    need(adapter_frozen_part(now) == adapter_frozen_part(old), "the adapter's constants, schema or build_account_dim changed")
    need("raise FileExistsError" in now, "the adapter carries no FileExistsError refusal")
    tmp = Path(tempfile.mkdtemp(prefix="p122_"))
    try:
        scratch = tmp / "wt"
        shutil.copytree(root / "data", scratch / "data", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(root / "lib", scratch / "lib", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(root / "infra" / "logic", scratch / "infra" / "logic")
        (scratch / "org").mkdir()
        shutil.copytree(root / "org" / "standards", scratch / "org" / "standards")
        sa = scratch / ADAPTER
        txt = sa.read_text(encoding="utf-8")
        planted = re.sub(r"raise FileExistsError\([^\n]*\)", "pass", txt, count=1)
        need(planted != txt, "the planted control could not remove the refusal")
        sa.write_text(planted, encoding="utf-8")
        rc, tail = pytest(scratch, ADAPTER_TEST, "-k", "test_upload_refuses_a_non_empty_partition")
        need(rc != 0, "the planted control did not make the refusal test fail")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


ARMS = {"DBC122-1-AC1": ac_1, "DBC122-2-AC1": ac_2}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
