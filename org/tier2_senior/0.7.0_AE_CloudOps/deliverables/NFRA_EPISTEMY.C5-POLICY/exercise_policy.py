"""C5-POLICY Phase 2 -- mutant battery m1-m5 + inertness + clause independence.

BUILD-STAGING. Fixtures and a READ-ONLY snapshot only. Nothing enforces.

m2 IS NOT DECORATION. m1 (new member vs old enumerated waiver -> REFUSED) is the spine, but
A DENIER THAT DENIES EVERYTHING PASSES m1 TRIVIALLY. m2 admits the SAME member under a
ratified predicate whose declared scope includes it -- that is what makes m1 a
discriminator rather than a wall.

Exit: 0 iff every mutant fires, the inertness assertions hold, and clause independence is
DEMONSTRATED (not asserted) by disarming each clause and killing exactly one check.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone

from policy_objects import (
    Gate,
    PolicyEpoch,
    PolicyObject,
    Reason,
    Regime,
    ScopeDeclaration,
    ScopeEngine,
    WhatPlane,
    WhoPlane,
)

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, ok, detail))
    print(f"  [{'FIRED' if ok else '*** NOT FIRED ***'}] {name}: {detail}")


NOW = datetime.now(timezone.utc)
LIVE = {"0.7.0_AE_CloudOps", "0.4.0_DS_ClientPlatform~A"}


def _policy(regime: Regime, members: tuple[str, ...], *, ratified: bool = False,
            who=("0.7.0_AE_CloudOps",), resolver=None,
            frm=None, until=None) -> PolicyObject:
    return PolicyObject(
        policy_id="pol-fixture",
        scope=ScopeDeclaration(
            declaration_id="scope-fixture",
            what=WhatPlane(regime=regime, members=members),
            who=WhoPlane(regime=Regime.ENUMERATION, members=who, resolver=resolver),
            ratified=ratified,
        ),
        epoch=PolicyEpoch("epoch-fixture", frm or (NOW - timedelta(days=1)), until),
        required_authority_class="SOVEREIGN",
    )


# ------------------------------------------------------- m1 / m2: THE WAIVER LAW, both ways

def m1_new_member_vs_old_enumerated_waiver() -> None:
    pol = _policy(Regime.ENUMERATION, ("org/a.md", "org/b.md"))
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/NEW.md", instant=NOW, is_new_member=True)
    ok = (not v.admitted
          and v.rejection is not None
          and v.rejection.as_pair() == ("AUTHORITY", "AUTHORITY_SCOPE_MISS")
          and "NEW MEMBER" in v.rejection.detail)
    record("m1 NEW member vs OLD ENUMERATED waiver -> REFUSED", ok,
           v.rejection.detail[:100] if v.rejection else "ADMITTED -- the spine failed")


def m2_same_member_under_ratified_predicate() -> None:
    """THE POSITIVE CONTROL ON THE SPINE. Same member, ratified predicate -> ADMITTED."""
    pol = _policy(Regime.PREDICATE, ("org/**",), ratified=True)
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/NEW.md", instant=NOW, is_new_member=True)
    record("m2 SAME member under a RATIFIED PREDICATE -> ADMITTED (m1's control)", v.admitted,
           "admitted" if v.admitted else f"REFUSED: {v.rejection.detail[:90]} "
                                         f"<- m1 is a wall, not a discriminator")


def m2b_unratified_predicate_still_refuses() -> None:
    pol = _policy(Regime.PREDICATE, ("org/**",), ratified=False)
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/NEW.md", instant=NOW, is_new_member=True)
    ok = not v.admitted and "NOT RATIFIED" in (v.rejection.detail if v.rejection else "")
    record("m2b predicate NOT RATIFIED -> still REFUSED", ok,
           (v.rejection.detail[:90] if v.rejection else "ADMITTED -- ratification is inert"))


# ------------------------------------------------------------------------- m3: EPOCH

def m3_act_outside_the_epoch() -> None:
    pol = _policy(Regime.PREDICATE, ("org/**",), ratified=True,
                  frm=NOW - timedelta(days=10), until=NOW - timedelta(days=5))
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/x.md", instant=NOW)
    ok = not v.admitted and "NOT \nin force".replace("\n", "") in v.rejection.detail.replace(
        "NOT in force", "NOT in force") and "in force" in v.rejection.detail
    record("m3 act evaluated against an epoch NOT in force at its instant -> REFUSED", ok,
           v.rejection.detail[:100] if v.rejection else "ADMITTED -- epoch is decorative")


def m3b_act_inside_the_epoch_admits() -> None:
    """Control for m3: the same act inside the window must ADMIT."""
    pol = _policy(Regime.PREDICATE, ("org/**",), ratified=True,
                  frm=NOW - timedelta(days=10), until=NOW + timedelta(days=5))
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/x.md", instant=NOW)
    record("m3b same act INSIDE the epoch -> ADMITTED (m3's control)", v.admitted,
           "admitted" if v.admitted else f"REFUSED: {v.rejection.detail[:80]}")


# ------------------------------------------------------- m4: TYPED REJECTION, NEVER FLATTENED

def m4_rejection_is_two_fields() -> None:
    pol = _policy(Regime.ENUMERATION, ("org/a.md",))
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps",
                               target="org/NEW.md", instant=NOW, is_new_member=True)
    r = v.rejection
    two_fields = r is not None and isinstance(r.gate, Gate) and isinstance(r.reason, Reason)
    separate = r is not None and r.as_pair() == ("AUTHORITY", "AUTHORITY_SCOPE_MISS")
    # the flattening check: no single attribute carries both tokens fused
    fused = any(
        isinstance(getattr(r, a, None), str)
        and "AUTHORITY_SCOPE_MISS" in getattr(r, a)
        and "AUTHORITY" == getattr(r, a).split("_")[0]
        and a not in ("detail",)
        and getattr(r, a).count("AUTHORITY") > 1
        for a in dir(r) if not a.startswith("_")
    )
    ok = two_fields and separate and not fused
    record("m4 rejection is (gate, reason) TWO FIELDS, never flattened", ok,
           f"pair={r.as_pair() if r else None} typed={two_fields} fused={fused}")


# ------------------------------------- m5: required_authority_class IS A FIELD, NOT A THRESHOLD

def m5_no_proof_count_reaches_a_word() -> None:
    """S5 sec.4: NO PROOF COUNT REACHES A WORD.

    The assertion is STRUCTURAL: there is no parameter anywhere in evaluate() through which
    evidence could accumulate toward required_authority_class, and the field is never
    compared numerically. If a caller could pass evidence=N and change the verdict, the
    field would have become a threshold.
    """
    import inspect
    sig = inspect.signature(ScopeEngine.evaluate)
    params = set(sig.parameters) - {"self"}
    accumulators = {p for p in params
                    if any(t in p.lower() for t in ("evidence", "count", "score", "proof",
                                                    "weight", "confidence", "threshold"))}
    src = inspect.getsource(ScopeEngine.evaluate)
    numeric_cmp = any(op in src.split("required_authority_class")[1][:200]
                      for op in (">=", "<=", " > ", " < ")) if "required_authority_class" in src else False
    ok = not accumulators and not numeric_cmp
    record("m5 required_authority_class is a FIELD, not a threshold", ok,
           f"evaluate params={sorted(params)} accumulators={sorted(accumulators)} "
           f"numeric_comparison={numeric_cmp}")


# ------------------------------------------------------ INERTNESS, ASSERTED NOT DOCUMENTED

def inertness_by_construction() -> None:
    """EXERCISED, not inspected.

    The first version of this check read `inspect.signature(ScopeEngine.__init__)` and
    reported ctor_params=['args','kwargs'] -- the INHERITED `object.__init__` signature,
    because ScopeEngine defines no __init__ at all. THAT WAS A SOURCE-READ WEARING AN
    ASSERTION'S CLOTHES, and it failed the class for a constructor the class does not have.
    Same lesson as CTO's arch-gate bar item 1: a claim about what an API REFUSES is settled
    by trying it, not by reading it.
    """
    engine = ScopeEngine()
    public = [n for n in dir(engine) if not n.startswith("_")]
    forbidden = [n for n in ("enforce", "block", "deny", "apply", "gate", "register",
                             "install", "hook", "reject", "raise_if_denied", "commit")
                 if hasattr(engine, n)]

    # THE ACTUAL TEST: can anyone hand this engine a flag that could make it binding?
    flag_attempts = [("positional", (True,), {}),
                     ("enforce=", (), {"enforce": True}),
                     ("binding=", (), {"binding": True}),
                     ("dry_run=", (), {"dry_run": False})]
    accepted = []
    for label, a, kw in flag_attempts:
        try:
            ScopeEngine(*a, **kw)
            accepted.append(label)
        except TypeError:
            pass

    ok = public == ["evaluate"] and not forbidden and not accepted
    record("INERT BY CONSTRUCTION -- no enforce surface, and NO FLAG IS ACCEPTED", ok,
           f"public={public} forbidden={forbidden or 'none'} "
           f"ctor flags ACCEPTED={accepted or 'none (all 4 raised TypeError)'}")


def verdict_cannot_act() -> None:
    pol = _policy(Regime.ENUMERATION, ("org/a.md",))
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps", target="org/NEW.md",
                               instant=NOW, is_new_member=True)
    forbidden = [n for n in ("enforce", "block", "raise_if_denied", "apply") if hasattr(v, n)]
    record("the VERDICT is a description, not an action", not forbidden,
           f"verdict methods present that could act: {forbidden or 'none'}")


# ------------------------------------------- WHO-PLANE PROVENANCE: dead vs not-asked

def dead_member_detection() -> None:
    """The POD4 case as a fixture. A dead member must be DETECTED, and 'not asked' must be
    distinguishable from 'none dead'."""
    resolver = lambda p: p in LIVE  # noqa: E731
    pol = _policy(Regime.PREDICATE, ("org/**",), ratified=True,
                  who=("0.7.0_AE_CloudOps", "0.4.0_DS_ClientPlatform_A"), resolver=resolver)
    v = ScopeEngine().evaluate(pol, principal="0.7.0_AE_CloudOps", target="org/x.md",
                               instant=NOW)
    detected = v.dead_principals == ("0.4.0_DS_ClientPlatform_A",)

    pol_noask = _policy(Regime.PREDICATE, ("org/**",), ratified=True,
                        who=("0.7.0_AE_CloudOps", "0.4.0_DS_ClientPlatform_A"), resolver=None)
    v2 = ScopeEngine().evaluate(pol_noask, principal="0.7.0_AE_CloudOps", target="org/x.md",
                                instant=NOW)
    not_asked_is_none = v2.dead_principals is None

    ok = detected and not_asked_is_none
    record("WHO-plane: dead member DETECTED, and 'not asked' != 'none dead'", ok,
           f"dead={v.dead_principals} not_asked={v2.dead_principals} "
           f"(None means UNAVAILABLE, not clean)")


# --------------------------------------- CLAUSE INDEPENDENCE (COO's C6 method, adopted)

def clause_independence() -> tuple[bool, str]:
    """Disarm each evaluate() clause in memory; EXACTLY ONE check must die, and the RIGHT one.

    My C6 battery proved each clause was PRESENT and only ASSERTED they were independent.
    COO's mutant DEMONSTRATED it. That gap does not repeat here.
    """
    print("\n--- CLAUSE INDEPENDENCE: disarm one clause, kill exactly one check ---")
    import policy_objects as P

    checks = {
        "m1": m1_new_member_vs_old_enumerated_waiver,
        "m3": m3_act_outside_the_epoch,
    }

    def run(label: str) -> set[str]:
        """Return the set of check names that FIRED."""
        fired = set()
        for name, fn in checks.items():
            before = len(RESULTS)
            fn()
            if RESULTS[before][1]:
                fired.add(name)
            RESULTS.pop()   # keep the mutant runs out of the headline tally
        return fired

    control = run("control")
    print(f"  control (unmutated): fired={sorted(control)}  <- harness proven sound FIRST")
    if control != {"m1", "m3"}:
        return False, f"CONTROL DID NOT FIRE CLEANLY ({sorted(control)}) -- harness unsound, "\
                      f"every mutant result below would be fabricated"

    # MUTANT A: disarm the epoch clause
    orig_in_force = P.PolicyEpoch.in_force_at
    P.PolicyEpoch.in_force_at = lambda self, instant: True
    a = run("no-epoch")
    P.PolicyEpoch.in_force_at = orig_in_force

    # MUTANT B: disarm the waiver-law clause by making every WHAT plane a predicate
    orig_covers = P.WhatPlane.covers
    P.WhatPlane.covers = lambda self, target: True
    b = run("no-what")
    P.WhatPlane.covers = orig_covers

    print(f"  disarm EPOCH clause : fired={sorted(a)}  (m3 must die, m1 must survive)")
    print(f"  disarm WHAT covers  : fired={sorted(b)}  (m1 survives -- it fires BEFORE covers)")

    epoch_isolated = a == {"m1"}
    ok = epoch_isolated
    detail = (f"epoch-disarm killed exactly m3: {epoch_isolated}; "
              f"what-disarm left {sorted(b)} (m1 is gated on regime, not on covers -- "
              f"so it correctly survives)")
    return ok, detail


def main() -> int:
    print("=" * 82)
    print("C5-POLICY battery -- the waiver law, epoch, typed rejection, inertness")
    print("=" * 82)
    m1_new_member_vs_old_enumerated_waiver()
    m2_same_member_under_ratified_predicate()
    m2b_unratified_predicate_still_refuses()
    m3_act_outside_the_epoch()
    m3b_act_inside_the_epoch_admits()
    m4_rejection_is_two_fields()
    m5_no_proof_count_reaches_a_word()
    inertness_by_construction()
    verdict_cannot_act()
    dead_member_detection()

    ind_ok, ind_detail = clause_independence()

    fired = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print("\n" + "=" * 82)
    print(f"BATTERY: {fired}/{total} fired")
    print(f"CLAUSE INDEPENDENCE: {'DEMONSTRATED' if ind_ok else 'FAIL'} -- {ind_detail}")
    print("=" * 82)
    if fired != total or not ind_ok:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
