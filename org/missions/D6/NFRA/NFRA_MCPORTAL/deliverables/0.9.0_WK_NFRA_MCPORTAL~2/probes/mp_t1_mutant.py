"""MP-t-1 mutant control (proof-of-spec CONTROLS.mutant).

IN-PROCESS mutant: monkeypatches app.owner_gate.is_owner to ALWAYS return True (the "the check
was silently removed" shape) and re-exercises require_owner() for both identities used by
tests/test_owner_gate.py. No tracked file is ever written -- the patch lives only in this
process's module object and is undone before exit; git porcelain is printed before/after to show
nothing moved.

Expected discrimination:
  - Andrew (owner):        REAL -> allowed.   MUTANT -> still allowed.   (no change; AC1 shape)
  - a verified non-owner:  REAL -> 403 refused. MUTANT -> allowed (the bug the mutant re-creates).

Usage: run from infra/aws/ec2/opal-gateway (cwd matters for `from app import ...`):
    python <this file>
"""
from __future__ import annotations

import os
import subprocess
import sys


def _find_repo_root(start: str) -> str:
    cur = start
    while True:
        if os.path.exists(os.path.join(cur, ".git")):  # a linked worktree's .git is a FILE, not a dir
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise RuntimeError("no .git found walking up from %s" % start)
        cur = parent


_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = _find_repo_root(_HERE)
_GW = os.path.join(_REPO_ROOT, "infra", "aws", "ec2", "opal-gateway")
if _GW not in sys.path:
    sys.path.insert(0, _GW)

os.environ.setdefault("MOCK_GRAPH", "1")

ANDREW = "andrew@opalinvest.com"
OTHER = "someone.else@opalinvest.com"


class _FakeRequest:
    def __init__(self, email: str):
        self._email = email


def _porcelain(repo_root: str) -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=repo_root,
                          capture_output=True, text=True)
    return out.stdout.strip()


def main() -> int:
    before = _porcelain(_REPO_ROOT)

    import importlib
    cfg = importlib.import_module("app.config").get_config()
    owner_gate = importlib.import_module("app.owner_gate")
    cfg.DASHBOARD_OWNER_EMAILS = (ANDREW,)

    def make_verifier(email):
        def fake(request):
            return email
        return fake

    results = {}

    # ---- REAL (unmutated) ----
    real_is_owner = owner_gate.is_owner
    owner_gate._alb_oidc_identity = make_verifier(ANDREW)
    try:
        owner_gate.require_owner(_FakeRequest(ANDREW))
        results["real_andrew"] = "ALLOWED"
    except owner_gate.OwnerGateError as e:
        results["real_andrew"] = "DENIED-%d" % e.status_code

    owner_gate._alb_oidc_identity = make_verifier(OTHER)
    try:
        owner_gate.require_owner(_FakeRequest(OTHER))
        results["real_other"] = "ALLOWED"
    except owner_gate.OwnerGateError as e:
        results["real_other"] = "DENIED-%d" % e.status_code

    # ---- MUTANT: is_owner always True (the check silently removed) ----
    owner_gate.is_owner = lambda email: True
    try:
        owner_gate._alb_oidc_identity = make_verifier(ANDREW)
        try:
            owner_gate.require_owner(_FakeRequest(ANDREW))
            results["mutant_andrew"] = "ALLOWED"
        except owner_gate.OwnerGateError as e:
            results["mutant_andrew"] = "DENIED-%d" % e.status_code

        owner_gate._alb_oidc_identity = make_verifier(OTHER)
        try:
            owner_gate.require_owner(_FakeRequest(OTHER))
            results["mutant_other"] = "ALLOWED"
        except owner_gate.OwnerGateError as e:
            results["mutant_other"] = "DENIED-%d" % e.status_code
    finally:
        owner_gate.is_owner = real_is_owner  # undo the mutant before anything else runs

    after = _porcelain(_REPO_ROOT)
    porcelain_equal = before == after

    print("results:", results)
    print("porcelain_equal=%s" % porcelain_equal)

    ok = (
        results.get("real_andrew") == "ALLOWED"
        and results.get("real_other") == "DENIED-403"
        and results.get("mutant_andrew") == "ALLOWED"
        and results.get("mutant_other") == "ALLOWED"   # the mutant DID let the non-owner through
        and porcelain_equal
    )
    print("VERDICT: %s" % ("PASS-MP-T1-MUTANT" if ok else "FAIL-MP-T1-MUTANT"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
