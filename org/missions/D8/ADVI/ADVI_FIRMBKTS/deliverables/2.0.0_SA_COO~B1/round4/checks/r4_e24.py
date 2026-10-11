"""ADVI_FIRMBKTS round 4 check for cell FB-g-7 (E_24's explicit-mode refusal), issuer 2.0.0_SA_COO~B1.

CTO ruling (NEVER_WIDEN_ROUND3_ACT2_PRODUCERS_CTO_HALF.md, E_24 section): E_24 refuses to write a served key unless
BD_PLATINUM_MODE is set EXPLICITLY, so a hand run must choose.

--arms refuse [--root <tree>]  (4 arms; every run uses fake credentials and a dead endpoint, so nothing reaches AWS)
  E1 `--upload` with BD_PLATINUM_MODE unset: exits non-zero, prints a line naming BD_PLATINUM_MODE, and prints no
     'Loading advisor_fee_detail' line (the refusal comes BEFORE the first read).
  E2 `--upload` with BD_PLATINUM_MODE=legacy and again =canonical: passes the guard (prints 'Loading advisor_fee_detail').
  E3 a DRY RUN with BD_PLATINUM_MODE unset passes the guard (nothing is written, so nothing to refuse).
  E4 the file stays ASCII and py_compiles.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import os
import py_compile
import subprocess
import sys
import tempfile

GOLD = "data/black_diamond/scripts/gold"
SCRIPT = "E_24.rebuild_fee_scorecard.py"


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _run(root, args, mode):
    env = dict(os.environ)
    env.pop("BD_PLATINUM_MODE", None)
    if mode is not None:
        env["BD_PLATINUM_MODE"] = mode
    env.update({"AWS_ACCESS_KEY_ID": "x", "AWS_SECRET_ACCESS_KEY": "x", "AWS_DEFAULT_REGION": "us-east-1",
                "AWS_ENDPOINT_URL": "http://127.0.0.1:9", "AWS_MAX_ATTEMPTS": "1", "AWS_EC2_METADATA_DISABLED": "true",
                "AWS_RETRY_MODE": "standard", "PYTHONDONTWRITEBYTECODE": "1"})
    gold = os.path.join(root, GOLD)
    try:
        r = subprocess.run([sys.executable, SCRIPT] + args, cwd=gold, env=env, capture_output=True, text=True,
                           timeout=80)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def refuse(root):
    res = []
    rc, out = _run(root, ["--upload"], None)
    named = "BD_PLATINUM_MODE" in out
    loaded = "Loading advisor_fee_detail" in out
    print("  E1 unset --upload: rc=%s names the variable=%s reached the read=%s" % (rc, named, loaded))
    res.append(("E1 --upload with BD_PLATINUM_MODE unset exits non-zero, names the variable and refuses before any read",
                rc not in (0, None) and rc != 124 and named and not loaded))
    ok2 = True
    for m in ("legacy", "canonical"):
        rc, out = _run(root, ["--upload"], m)
        reached = "Loading advisor_fee_detail" in out
        print("  E2 mode=%s --upload: rc=%s reached the read=%s" % (m, rc, reached))
        ok2 = ok2 and reached
    res.append(("E2 --upload with the mode set explicitly (legacy and canonical) passes the guard", ok2))
    rc, out = _run(root, [], None)
    reached = "Loading advisor_fee_detail" in out
    print("  E3 unset dry run: rc=%s reached the read=%s" % (rc, reached))
    res.append(("E3 a dry run with the mode unset passes the guard", reached))
    path = os.path.join(root, GOLD, SCRIPT)
    raw = open(path, "rb").read()
    ascii_ok = all(b < 128 for b in raw)
    try:
        with tempfile.TemporaryDirectory() as td:
            py_compile.compile(path, cfile=os.path.join(td, "x.pyc"), doraise=True)
        comp = True
    except Exception:  # noqa: BLE001
        comp = False
    print("  E4 ascii=%s py_compile=%s" % (ascii_ok, comp))
    res.append(("E4 the script stays ASCII and compiles", ascii_ok and comp))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("refuse",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = refuse(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (SCRIPT, type(e).__name__, str(e)[:160]))
        res = [("E_24 present and runnable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 E24 REFUSE: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
