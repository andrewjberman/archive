"""ADVI_PERFRP.TO-R1-AE / PRFR1AE-AC4 -- the fail-closed arm, re-runnable AT ANY VINTAGE.

WHY THIS FILE EXISTS AS AN ARTIFACT AND NOT AS A SCRATCH SCRIPT.
The criterion's exercised half was first run 2026-08-25 against chain_49f_entrypoint.py at
b9915d8271. By 2026-08-28 the deployed object had moved three commits and 1,473 LF bytes
(0.4.0_DS_ClientPlatform~U's P14-PRECOND / P14-STAMP edits) -- so the exercise that closed the
criterion no longer had the deployed bytes as its subject. A declared-but-unrun falsifier is a
promise, not a control; a harness nobody can re-run becomes one the moment its subject moves.
RUN THIS AGAINST THE DEPLOYED OBJECT, not against HEAD, and not against a remembered hash.

THE CRITERION, transcribed from the TO face BEFORE the implementation was read (a harness copied
out of the code it tests scores that code's blind spot as a pass):

    "a forced c04 failure leaves the projection UNRUN -- exercised"

TWO ARMS, reachable from DIFFERENT truths. The ONLY thing that varies is
c04_validation_battery.py's return code:

    ARM A  c04 returns 0        -> _run_perfrp_projection MUST be called
    ARM B  c04 returns nonzero  -> _run_perfrp_projection MUST NOT be called,
                                   and main() must return c04's rc

ARM A is load-bearing, not decoration: without it, ARM B's silence is equally consistent with the
call site having been DELETED. The c04_invoked assertion is the same discipline one level down --
an arm that skipped the battery would also report perfrp_projection_ran=False and read as a pass.

READ-ONLY BY CONSTRUCTION. subprocess and every S3 helper are stubbed; no stage script executes,
no AWS call is made, nothing is published, deployed or scheduled. It writes only into --workdir.

USAGE
    # fetch the deployed object into a bundle layout, then exercise it
    aws s3api get-object --bucket opal-data-49financial \
        --key _code/chain_49f_entrypoint.py <bundle>/chain_49f_entrypoint.py
    cp lib/trading_calendar.py <bundle>/lib/trading_calendar.py
    python ADVI_PERFRP.TO-R1-AE_AC4_FAILCLOSED_EXERCISE.py --target <bundle>/chain_49f_entrypoint.py

The bundle layout (HERE/lib/trading_calendar.py) is the layout the EC2 runner itself uses; the
entrypoint's bootstrap block resolves its calendar there or ABORTS rc=2.

READ THE VERDICT LINE, NOT THE EXIT CODE -- a bootstrap ABORT exits before either arm runs and
must never be read as a clean pass.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import subprocess
import sys
import types
from pathlib import Path


def lf_sha256(path: Path) -> tuple:
    b = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(b).hexdigest(), len(b)


def _load(target: Path, c04_rc: int, calls: list):
    """Load the target module fresh, with subprocess + every S3 helper stubbed."""
    spec = importlib.util.spec_from_file_location(f"chain_under_test_{c04_rc}", target)
    mod = importlib.util.module_from_spec(spec)

    def fake_run(cmd, *a, **kw):
        name = ""
        for tok in cmd:
            if isinstance(tok, str) and tok.endswith(".py"):
                name = Path(tok).name
                break
        calls.append(name)
        rc = c04_rc if name == "c04_validation_battery.py" else 0
        return types.SimpleNamespace(returncode=rc, stdout=b"", stderr=b"")

    sys.modules.setdefault("boto3", types.ModuleType("boto3"))
    spec.loader.exec_module(mod)

    mod.subprocess = types.SimpleNamespace(
        run=fake_run, PIPE=subprocess.PIPE, STDOUT=subprocess.STDOUT,
        CalledProcessError=subprocess.CalledProcessError)
    mod._s3 = lambda: types.SimpleNamespace()
    mod._upload_a07_pair = lambda w, d: 0
    mod._pull_prev_valuation_into_mirror = lambda w, d: {}
    mod._pull_canonical_for_c04 = lambda w, d: Path(w) / "c04_mirror"

    def spy(workdir, date):                      # THE FIELD UNDER TEST
        calls.append("PERFRP_PROJECTION_RAN")
        return 0

    mod._run_perfrp_projection = spy
    return mod


def arm(label: str, target: Path, c04_rc: int, workdir: Path, date: str):
    calls: list = []
    mod = _load(target, c04_rc, calls)
    old = sys.argv
    sys.argv = ["chain_49f_entrypoint.py", "--date", date, "--upload",
                "--workdir", str(workdir)]
    try:
        rc = mod.main()
    except SystemExit as e:
        rc = e.code
    finally:
        sys.argv = old
    ran = "PERFRP_PROJECTION_RAN" in calls
    c04_seen = "c04_validation_battery.py" in calls
    print(f"[{label}] c04_rc={c04_rc} -> main_rc={rc} | c04_invoked={c04_seen} | "
          f"perfrp_projection_ran={ran}")
    return rc, c04_seen, ran


def main() -> int:
    ap = argparse.ArgumentParser(description="AC4 fail-closed exercise at a named vintage")
    ap.add_argument("--target", required=True,
                    help="chain_49f_entrypoint.py to exercise -- point at the DEPLOYED bytes "
                         "staged in a bundle layout, never at the repo copy")
    ap.add_argument("--workdir", default=None, help="scratch workdir (created if absent)")
    ap.add_argument("--date", default="2026-08-27", help="partition date passed to the chain")
    ap.add_argument("--fail-rc", type=int, default=3,
                    help="rc the forced c04 failure returns in ARM B")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.is_file():
        print(f"BLOCKED: target not found: {target}")
        return 2
    if not (target.parent / "lib" / "trading_calendar.py").is_file():
        print(f"BLOCKED: bundle layout incomplete -- {target.parent}/lib/trading_calendar.py "
              f"absent. The entrypoint ABORTS rc=2 at bootstrap without it, and that abort "
              f"exits before either arm runs.")
        return 2

    workdir = Path(args.workdir) if args.workdir else target.parent / "arm_work"
    workdir.mkdir(parents=True, exist_ok=True)

    digest, nbytes = lf_sha256(target)
    print(f"SUBJECT: {target}")
    print(f"SUBJECT LF sha256={digest[:16]} LFbytes={nbytes}")
    print("  (compare this against `aws s3api head-object` + get-object on "
          "s3://opal-data-49financial/_code/chain_49f_entrypoint.py -- if they differ, this run "
          "is about the wrong bytes)")
    print()

    rc_a, c04_a, ran_a = arm("ARM A  c04 PASSES", target, 0, workdir, args.date)
    rc_b, c04_b, ran_b = arm("ARM B  c04 FAILS ", target, args.fail_rc, workdir, args.date)

    checks = [
        ("ARM A: c04 was actually invoked (arm is live, not skipped)", c04_a is True),
        ("ARM A: projection RAN when c04 passed", ran_a is True),
        ("ARM B: c04 was actually invoked (arm is live, not skipped)", c04_b is True),
        ("ARM B: projection did NOT run when c04 failed", ran_b is False),
        (f"ARM B: main() returned c04's rc ({args.fail_rc}), not 0", rc_b == args.fail_rc),
        ("ARMS DIFFER on the field under test", ran_a != ran_b),
    ]
    print()
    ok = True
    for name, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
        ok = ok and passed
    npass = sum(1 for _, p in checks if p)
    print()
    print(f"VERDICT: {'PASS' if ok else 'FAIL'} ({npass}/{len(checks)} arms+assertions)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
