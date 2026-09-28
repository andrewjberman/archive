"""AMGT_HARVST HVST-x-1 AC1 -- demonstrates the publishers.py:672 DowJones.check() .json()
guard DIRECTLY, never through the pytest suite (a green suite is not evidence for this item).

Prints, in order:
  (a) NEGATIVE CONTROL -- the PRE-FIX check() body, pulled VERBATIM from the git pin named
      below (not hand-retyped), run against a fake session whose .json() returns None ->
      must raise AttributeError.
  (b) the SAME fake session driven through the CURRENT (post-fix) DowJones.check() -> must
      raise AuthExpired.
  (c) two positive controls against the CURRENT DowJones.check(): a well-formed logged-in
      body still passes without raising, and a logged-out body still raises AuthExpired --
      so the guard is not swallowing the normal path.

Exit code 0 only if all four outcomes match their expectation; non-zero and a FAIL line
otherwise.
"""
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

# HVST-x-1 pin: the commit at the moment this cell started -- carries the UNGUARDED
# check() this script's negative control must reproduce exactly, not from memory.
PRE_FIX_PIN = "402a3414c7c8ae9a7ea9eb69c2209fef7a740ed8"
TARGET_REL_PATH = "lib/opal_data_harvest/publishers.py"

REPO_ROOT = Path(
    subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=Path(__file__).resolve().parent,
        text=True,
    ).strip()
)
sys.path.insert(0, str(REPO_ROOT))

from lib.opal_data_harvest.publishers import DowJones  # noqa: E402  (post-fix, current tree)
from lib.opal_data_harvest.transport import AuthExpired  # noqa: E402


def _extract_prefix_check_source():
    blob = subprocess.check_output(
        ["git", "show", "%s:%s" % (PRE_FIX_PIN, TARGET_REL_PATH)],
        cwd=str(REPO_ROOT),
        text=True,
    )
    start = "    def check(self):\n"
    end = "\n    @staticmethod\n"
    i = blob.index(start)
    j = blob.index(end, i)
    return blob[i:j]


def _build_prefix_dowjones():
    check_src = _extract_prefix_check_source()
    class_src = (
        "class _PreFixDowJones:\n"
        "    def __init__(self, pub, session):\n"
        "        self.pub, self.session, self.base = pub, session, 'https://www.%s.com' % pub\n"
        + check_src
        + "\n"
    )
    ns = {"AuthExpired": AuthExpired}
    exec(compile(class_src, "<%s:%s check() -- pre-fix>" % (PRE_FIX_PIN, TARGET_REL_PATH), "exec"), ns)
    return ns["_PreFixDowJones"]


class _NoneJsonSession:
    """.json() returns None -- the pre-fix defect trigger."""

    def get(self, *args, **kwargs):
        return SimpleNamespace(json=lambda: None)


class _DictJsonSession:
    def __init__(self, body):
        self._body = body

    def get(self, *args, **kwargs):
        return SimpleNamespace(json=lambda: self._body)


def run():
    ok = True

    # (a) NEGATIVE CONTROL: pre-fix check(), from the git pin, against a None-returning .json()
    PreFixDowJones = _build_prefix_dowjones()
    pre = PreFixDowJones("barrons", _NoneJsonSession())
    try:
        pre.check()
        outcome_a = "NO EXCEPTION RAISED (unexpected)"
        a_is_attributeerror = False
    except Exception as exc:
        outcome_a = "%s: %s" % (type(exc).__name__, exc)
        a_is_attributeerror = isinstance(exc, AttributeError)
    print("(a) NEGATIVE CONTROL -- pre-fix check() (pin %s), .json() -> None:" % PRE_FIX_PIN)
    print("    %s" % outcome_a)
    if not a_is_attributeerror:
        print("    FAIL: expected AttributeError")
        ok = False

    # (b) SAME input, post-fix check()
    post = DowJones("barrons", _NoneJsonSession())
    try:
        post.check()
        outcome_b = "NO EXCEPTION RAISED (unexpected)"
        b_is_authexpired = False
    except Exception as exc:
        outcome_b = "%s: %s" % (type(exc).__name__, exc)
        b_is_authexpired = isinstance(exc, AuthExpired)
    print("(b) SAME INPUT after the guard, post-fix check(), .json() -> None:")
    print("    %s" % outcome_b)
    if not b_is_authexpired:
        print("    FAIL: expected AuthExpired")
        ok = False

    # (c1) POSITIVE CONTROL: well-formed logged-in body still passes
    logged_in = DowJones("barrons", _DictJsonSession({"isLoggedIn": True, "type": "prosubscriber"}))
    try:
        logged_in.check()
        outcome_c1 = "PASSED, no exception (expected)"
        c1_ok = True
    except Exception as exc:
        outcome_c1 = "UNEXPECTED %s: %s" % (type(exc).__name__, exc)
        c1_ok = False
    print("(c1) POSITIVE CONTROL -- logged-in body {'isLoggedIn': True, 'type': 'prosubscriber'}:")
    print("    %s" % outcome_c1)
    if not c1_ok:
        print("    FAIL: guard swallowed the normal logged-in path")
        ok = False

    # (c2) POSITIVE CONTROL: logged-out body still raises AuthExpired
    logged_out = DowJones("barrons", _DictJsonSession({"isLoggedIn": False, "type": "prosubscriber"}))
    try:
        logged_out.check()
        outcome_c2 = "NO EXCEPTION RAISED (unexpected)"
        c2_ok = False
    except Exception as exc:
        outcome_c2 = "%s: %s" % (type(exc).__name__, exc)
        c2_ok = isinstance(exc, AuthExpired)
    print("(c2) POSITIVE CONTROL -- logged-out body {'isLoggedIn': False, 'type': 'prosubscriber'}:")
    print("    %s" % outcome_c2)
    if not c2_ok:
        print("    FAIL: expected AuthExpired on valid logged-out JSON")
        ok = False

    print()
    if ok:
        print("AC1 PASS: (a) is AttributeError pre-fix, (b) is AuthExpired post-fix on the same "
              "input, (c1) a valid logged-in body still passes, (c2) a logged-out body still "
              "raises AuthExpired.")
        return 0
    print("AC1 FAIL: see the FAIL line(s) above.")
    return 1


if __name__ == "__main__":
    sys.exit(run())
