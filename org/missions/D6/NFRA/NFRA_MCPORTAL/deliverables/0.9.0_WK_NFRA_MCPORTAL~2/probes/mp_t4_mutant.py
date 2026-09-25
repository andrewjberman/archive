"""MP-t-4 CONTROLS.mutant probe (org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~2).

Monkeypatches app.access_state.AccessState.get IN-PROCESS ONLY (no tracked file is touched) so a
DependencyUnavailable raised by a real store read is silently swallowed and reported as "no such
record" -- collapsing NO-PROFILE and STORE-UNAVAILABLE into one answer. That is exactly the failure
mode AC2 exists to catch: a caller could act on a store it could not reach as if the principal were
simply un-profiled. Live read (AWS READ-ONLY, per this cell's declared egress class): a real
never-profiled principal against the configured store, and a nonexistent table name.
"""
from __future__ import annotations

import os
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


_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
_GW = os.path.join(_ROOT, "infra", "aws", "ec2", "opal-gateway")
if _GW not in sys.path:
    sys.path.insert(0, _GW)

from app import access_state as acs  # noqa: E402
from app import admin_grants as g    # noqa: E402

TID = "00000000-0000-4000-8000-0000000000c3"
OID = "00000000-0000-4000-8000-0000000000d4"
BOGUS_TABLE = "opal-nonexistent-table-mp-t4-probe"


def _run() -> int:
    real_live = g.read_grant_state(TID, OID)
    real_bogus = g.read_grant_state(TID, OID, table=BOGUS_TABLE)

    orig_get = acs.AccessState.get

    def mutant_get(self, key):
        try:
            return orig_get(self, key)
        except acs.DependencyUnavailable:
            return None  # THE MUTANT: a store failure silently reads as "no record"

    acs.AccessState.get = mutant_get
    try:
        mutant_live = g.read_grant_state(TID, OID)
        mutant_bogus = g.read_grant_state(TID, OID, table=BOGUS_TABLE)
    finally:
        acs.AccessState.get = orig_get

    result = {"real_live": real_live, "real_bogus": real_bogus,
             "mutant_live": mutant_live, "mutant_bogus": mutant_bogus}
    ok = (real_live == g.NO_PROFILE and real_bogus == g.STORE_UNAVAILABLE
         and mutant_live == g.NO_PROFILE and mutant_bogus == g.NO_PROFILE)
    print(result)
    print("VERDICT:", "PASS-MP-T4-MUTANT" if ok else "FAIL-MP-T4-MUTANT")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_run())
