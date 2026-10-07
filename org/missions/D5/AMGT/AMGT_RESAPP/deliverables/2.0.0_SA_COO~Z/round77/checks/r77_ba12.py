"""AMGT_RESAPP round 77 -- AMGT-ba-12: the batched repair cell (COO adjudication @fb9ca91ad5, section A, non-adapter rows).

  --crit AC1|AC2|AC3 --where local

AC1 (build; rows Z-C-S35, Z-W7-S7): every test under lib/research/watchlist/tests runs with the `block_all_sockets`
    fixture (pytest --fixtures-per-test: N of N tests list it, N at least 5).
AC2 (build; row Z-S343): ONE pytest run collecting lib/research/management/tests beside
    lib/research/harvest/test_am1_marker_once.py and lib/research/harvest/test_al2_content_key.py has 0 failures and
    0 errors.
AC3 (build; rows Z-W88-S1, Z-C-S372): `bright_data_serp.harvest_serp(..., max_pages=2)` REFUSES with a ValueError
    naming max_pages BEFORE it calls the vendor primitive or touches the store; `max_pages=1` is not refused by that
    rule (the control: it goes on to the store read).
Verdict: R77 BA12 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys


class _Touched(Exception):
    pass


class _Client:
    """A store client that records the first touch: the refusal must come before any store call."""

    def __getattr__(self, name):
        raise _Touched(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    def run(args, timeout):
        p = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "--color=no"] + args,
                           capture_output=True, timeout=timeout)
        return p.returncode, re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", errors="replace"))

    if a.crit == "AC1":
        rc, out = run(["--fixtures-per-test", "-q", "lib/research/watchlist/tests"], 600)
        blocks = re.split(r"-+ fixtures used by ", out)[1:]
        tests = [b.split(" ", 1)[0].strip("- ") for b in blocks]
        blocked = [t for t, b in zip(tests, blocks) if re.search(r"^block_all_sockets\b", b, re.M)]
        print(f"   watchlist tests {len(tests)}; run with block_all_sockets {len(blocked)}; "
              f"without {[t for t in tests if t not in blocked]}")
        clause("C1 every watchlist test runs socket-blocked", len(tests) >= 5 and len(blocked) == len(tests),
               f"{len(blocked)} of {len(tests)}")
        return verdict(a, ok)

    if a.crit == "AC2":
        rc, out = run(["-q", "lib/research/management/tests", "lib/research/harvest/test_am1_marker_once.py",
                       "lib/research/harvest/test_al2_content_key.py"], 1500)
        tail = out.strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 one collection, 0 failed and 0 errors", rc == 0 and " passed" in tail and "failed" not in tail
               and "error" not in tail, f"rc={rc}")
        return verdict(a, ok)

    from lib.research.harvest import bright_data_serp

    called = []

    def records_fn(*args, **kwargs):
        called.append("vendor primitive")
        raise AssertionError("the vendor primitive was called")

    refused, detail = False, ""
    try:
        bright_data_serp.harvest_serp(records_fn, "plant query", inner=object(), max_pages=2, client=_Client())
        detail = "returned without refusing"
    except ValueError as err:
        refused = "max_pages" in str(err)
        detail = f"ValueError {str(err)[:90]!r}"
    except _Touched as err:
        detail = f"the store was touched first ({err})"
    except Exception as err:  # noqa: BLE001 -- any other failure is not the refusal
        detail = f"{type(err).__name__}: {str(err)[:90]}"
    clause("C1 max_pages=2 is refused before the vendor call and before the store", refused and not called, detail)
    control = ""
    try:
        bright_data_serp.harvest_serp(records_fn, "plant query", inner=object(), max_pages=1, client=_Client())
        control = "returned"
    except ValueError as err:
        control = f"ValueError {str(err)[:60]!r}" if "max_pages" in str(err) else "past the rule"
    except (_Touched, AssertionError, Exception):  # noqa: BLE001 -- reaching the store or the primitive is the control
        control = "past the rule"
    clause("C2 control: max_pages=1 is not refused by the rule", control == "past the rule" or control == "returned",
           control)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R77 BA12 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
