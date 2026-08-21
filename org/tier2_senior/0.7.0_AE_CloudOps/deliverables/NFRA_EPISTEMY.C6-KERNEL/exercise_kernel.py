"""C6-KERNEL Phase 2/3 exercise -- the mutant battery m1-m7 + a multi-leg abort.

BUILD-STAGING. Fixture/scratch transitions only; nothing here touches a live write path.

A MUTANT BATTERY IS ONLY EVIDENCE IF EVERY MUTANT ACTUALLY FIRES. Each m-case below
BREAKS one property and asserts the kernel REFUSES. A case that passes silently is
reported as NOT-FIRED and the run fails -- a control that has never been made to fail has
not been tested (CLAUDE.md doctrine; COO's A3 bar on tonight's sibling build).

Run:  python exercise_kernel.py
Exit: 0 iff every mutant FIRED and the exercised abort reached its rollback terminal.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone

from transition_kernel import (
    Checkpoint,
    CumulativeResidueLedger,
    InadmissibleRow,
    Interval,
    PrefixSafetyViolation,
    ResidueVector,
    SupportClaim,
    SupportHandoffViolation,
    Terminal,
    TransitionManifest,
    TransitionUnit,
)

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, fired: bool, detail: str) -> None:
    RESULTS.append((name, fired, detail))
    flag = "FIRED" if fired else "*** NOT FIRED ***"
    print(f"  [{flag}] {name}: {detail}")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _manifest(
    envelope: dict[str, float] | None = None,
    capacity: float = 100.0,
    point_of_no_return_leg: str | None = None,
    n_legs: int = 3,
) -> TransitionManifest:
    checkpoints = tuple(
        Checkpoint(
            leg_id=f"leg{i}",
            description=f"checkpoint {i}",
            is_point_of_no_return=(f"leg{i}" == point_of_no_return_leg),
        )
        for i in range(1, n_legs + 1)
    )
    return TransitionManifest(
        transition_id="fixture-t1",
        targets=("scratch://fixture/a", "scratch://fixture/b"),
        action_classes=("write", "activate"),
        checkpoints=checkpoints,
        envelope=ResidueVector(axes=envelope or {"objects_written": 10.0, "keys_touched": 5.0}),
        recovery_capacity=capacity,
        policy_epoch="epoch-fixture-0",
        knowledge_basis="kb-fixture-0",
        harm_model="hm-stamp-only",   # rider (a): stamp only, nothing built against it
    )


def _live_lease(seconds: int = 3600):
    def actual_at(now: datetime):
        return Interval(now - timedelta(seconds=1), now + timedelta(seconds=seconds))
    return actual_at


# ---------------------------------------------------------------- m1: residue outside envelope

def m1_residue_outside_envelope() -> None:
    tu = TransitionUnit(_manifest(envelope={"objects_written": 2.0}))
    # land a leg that produces residue 5 on an axis whose envelope limit is 2
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 5.0, method="fixture count")
    try:
        tu.check_prefix_safety("leg2")
    except PrefixSafetyViolation as exc:
        record("m1 residue OUTSIDE envelope -> REFUSED", True, str(exc)[:110])
        return
    record("m1 residue OUTSIDE envelope -> REFUSED", False,
           "kernel PROCEEDED with residue outside the envelope")


# ---------------------------------------------------------------- m2: no safe terminal

def m2_no_safe_terminal() -> None:
    tu = TransitionUnit(_manifest(point_of_no_return_leg="leg1"))
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 1.0, method="fixture count")
    try:
        tu.check_prefix_safety("leg2")
    except PrefixSafetyViolation as exc:
        if "NO SAFE TERMINAL" in str(exc):
            record("m2 NO safe terminal reachable -> REFUSED", True, str(exc)[:110])
            return
        record("m2 NO safe terminal reachable -> REFUSED", False,
               f"refused, but on the WRONG clause: {str(exc)[:90]}")
        return
    record("m2 NO safe terminal reachable -> REFUSED", False, "kernel PROCEEDED past no-return")


# ---------------------------------------------------------------- m3: recovery > capacity

def m3_recovery_exceeds_capacity() -> None:
    tu = TransitionUnit(_manifest(envelope={"objects_written": 1000.0}, capacity=3.0))
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 9.0, method="fixture count")
    try:
        tu.check_prefix_safety("leg2")
    except PrefixSafetyViolation as exc:
        if "EXCEEDS capacity" in str(exc):
            record("m3 recovery requirement > capacity -> REFUSED", True, str(exc)[:110])
            return
        record("m3 recovery requirement > capacity -> REFUSED", False,
               f"refused on the WRONG clause: {str(exc)[:90]}")
        return
    record("m3 recovery requirement > capacity -> REFUSED", False,
           "kernel PROCEEDED with unpayable rollback debt")


# ---------------------------------------------------------------- m4: agent self-report

def m4_agent_self_reported_row() -> None:
    ledger = CumulativeResidueLedger()
    # An agent tries to assert a residue VALUE rather than supply a measurement.
    try:
        ledger.record_measurement("leg1", "objects_written", 7.0, "I counted them myself")  # type: ignore[arg-type]
    except InadmissibleRow as exc:
        # And the structural half: there is no row-accepting method at all.
        has_append = any(hasattr(ledger, n) for n in ("append", "add_row", "submit", "append_row"))
        if has_append:
            record("m4 agent self-reported row -> INADMISSIBLE", False,
                   "raised, but a row-accepting method EXISTS -- not inexpressible")
            return
        record("m4 agent self-reported row -> INADMISSIBLE", True,
               f"{str(exc)[:80]} | no append/add_row/submit method exists")
        return
    record("m4 agent self-reported row -> INADMISSIBLE", False,
           "ledger ACCEPTED an asserted value")


# ---------------------------------------------------------------- m5: required > actual

def m5_required_exceeds_actual() -> None:
    now = _now()
    claim = SupportClaim(
        claim_id="c-over-ask",
        required=Interval(now, now + timedelta(hours=8)),      # asks for 8h
        actual_at=_live_lease(seconds=600),                    # lease only good 10m
    )
    tu = TransitionUnit(_manifest(), claims=[claim])
    try:
        tu.check_prefix_safety("leg1", now=now)
    except SupportHandoffViolation as exc:
        record("m5 Required NOT subset-of Actual -> REFUSED", True, str(exc)[:110])
        return
    record("m5 Required NOT subset-of Actual -> REFUSED", False,
           "kernel ACCEPTED a claim asking beyond its lease")


# ---------------------------------------------------------------- m6: unexercised recovery

def m6_unexercised_recovery_is_assumed() -> None:
    tu = TransitionUnit(_manifest(), recovery_exercised=False)
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 1.0, method="fixture count")
    tu.abort_at_checkpoint("leg2", "fixture abort")
    terminal, reason = tu.terminal()
    if terminal is Terminal.CONTAINED and "ASSUMED" in reason:
        record("m6 unexercised recovery -> ASSUMED not PROVEN", True,
               f"{terminal.value}: {reason[:80]}")
        return
    record("m6 unexercised recovery -> ASSUMED not PROVEN", False,
           f"got {terminal.value} -- an unexercised path was reported as restored")


# ---------------------------------------------------------------- m7: lease expires mid-transition

def m7_lease_expires_midway() -> None:
    """MINE, added beyond the TO's m1-m6, per COO 64235 note (b).

    A lease VALID at leg-open and EXPIRED by a later checkpoint, with the kernel
    proceeding, must REFUSE at that checkpoint. m5 catches an over-asking claim at
    leg-open; it CANNOT catch one that was honest then and expired at leg-3. Without m7
    the kernel silently converts a lease into a lock -- the one thing sec.2.7 forbids by
    name.
    """
    now = _now()
    state = {"expired": False}

    def actual_at(t: datetime):
        if state["expired"]:
            return None
        return Interval(t - timedelta(seconds=1), t + timedelta(hours=2))

    claim = SupportClaim(
        claim_id="c-expires",
        required=Interval(now, now + timedelta(minutes=30)),
        actual_at=actual_at,
    )
    tu = TransitionUnit(_manifest(), claims=[claim])

    # leg1 opens cleanly -- the lease IS valid here.
    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 1.0, method="fixture count", now=now)

    # a peer commit lands; the lease expires mid-transition.
    state["expired"] = True

    try:
        tu.check_prefix_safety("leg2", now=now + timedelta(minutes=1))
    except SupportHandoffViolation as exc:
        record("m7 lease VALID at open, EXPIRED at leg2 -> REFUSED", True, str(exc)[:110])
        return
    record("m7 lease VALID at open, EXPIRED at leg2 -> REFUSED", False,
           "kernel carried the opening verdict -- a lease silently became a LOCK")


# ---------------------------------------------------------------- POSITIVE CONTROL

def positive_control_happy_path() -> None:
    """The battery must not be undiscriminating: a WELL-FORMED transition must COMPLETE."""
    claim = SupportClaim(
        claim_id="c-ok",
        required=Interval(_now(), _now() + timedelta(minutes=5)),
        actual_at=_live_lease(seconds=7200),
    )
    tu = TransitionUnit(_manifest(n_legs=2), claims=[claim])
    for leg in ("leg1", "leg2"):
        tu.run_leg(leg, act=lambda: None, residue_axis="objects_written",
                   measure_fn=lambda: 1.0, method="fixture count")
    terminal, reason = tu.terminal()
    ok = terminal is Terminal.COMPLETED
    record("POSITIVE CONTROL well-formed transition -> COMPLETED", ok,
           f"{terminal.value}: {reason[:80]}")


# ---------------------------------------------------------------- Phase 3: exercised abort

def phase3_exercised_abort() -> tuple[bool, str]:
    """A multi-leg transition where one leg ABORTS at a checkpoint and reaches its
    ROLLBACK terminal, with the priced debt visible in the ledger.

    An abort you cannot demonstrate is a terminal you do not have.
    """
    print("\n--- PHASE 3: multi-leg transition with a real abort ---")
    tu = TransitionUnit(_manifest(n_legs=3, envelope={"objects_written": 4.0}),
                        recovery_exercised=False)

    tu.run_leg("leg1", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 2.0, method="fixture count")
    print(f"  leg1 LANDED. cumulative residue={dict((tu.ledger.cumulative() or ResidueVector(axes={'none':0.0})).axes)} "
          f"remaining_capacity={tu.remaining_capacity()}")

    # leg2 would breach the envelope -> the kernel refuses, and we abort at the checkpoint.
    tu.run_leg("leg2", act=lambda: None, residue_axis="objects_written",
               measure_fn=lambda: 3.0, method="fixture count")
    print(f"  leg2 LANDED. cumulative residue={dict((tu.ledger.cumulative() or ResidueVector(axes={'none':0.0})).axes)}")

    try:
        tu.check_prefix_safety("leg3")
        aborted = False
        detail = "leg3 prefix check PASSED -- no abort demonstrated"
    except PrefixSafetyViolation as exc:
        tu.abort_at_checkpoint("leg3", f"prefix safety refused: {exc}")
        aborted = True
        detail = str(exc)[:100]

    terminal, reason = tu.terminal()
    print(f"  leg3 REFUSED -> aborted. detail={detail}")
    print(f"  TERMINAL = {terminal.value}")
    print(f"  reason   = {reason}")
    print(f"  ledger rows = {len(tu.ledger)}  (each one MEASURED, none asserted)")
    for row in tu.ledger.rows():
        print(f"    {row.leg_id}/{row.axis} = {row.measured} via '{row.method}' at {row.observed_at.isoformat()}")

    ok = aborted and terminal is Terminal.CONTAINED and "ASSUMED" in reason
    return ok, f"{terminal.value} / aborted={aborted}"


# ---------------------------------------------------------------- determinism

def determinism_check() -> bool:
    m = _manifest()
    a, b = m.manifest_digest(), _manifest().manifest_digest()
    print(f"\n--- DETERMINISM ---\n  manifest_digest run1 = {a}\n  manifest_digest run2 = {b}")
    same = a == b
    # negative control: perturbing one member MUST change the digest
    perturbed = _manifest(capacity=101.0).manifest_digest()
    discriminates = perturbed != a
    print(f"  NEGATIVE CONTROL (capacity 100->101) = {perturbed}")
    print(f"  stable={same}  discriminates={discriminates}")
    return same and discriminates


def main() -> int:
    print("=" * 78)
    print("C6-KERNEL mutant battery -- every case must FIRE")
    print("=" * 78)
    m1_residue_outside_envelope()
    m2_no_safe_terminal()
    m3_recovery_exceeds_capacity()
    m4_agent_self_reported_row()
    m5_required_exceeds_actual()
    m6_unexercised_recovery_is_assumed()
    m7_lease_expires_midway()
    positive_control_happy_path()

    p3_ok, p3_detail = phase3_exercised_abort()
    det_ok = determinism_check()

    fired = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print("\n" + "=" * 78)
    print(f"BATTERY: {fired}/{total} fired")
    print(f"PHASE 3 exercised abort: {'PASS' if p3_ok else 'FAIL'} ({p3_detail})")
    print(f"DETERMINISM: {'STABLE + DISCRIMINATING' if det_ok else 'FAIL'}")
    print("=" * 78)

    if fired != total or not p3_ok or not det_ok:
        print("RESULT: FAIL -- a mutant that does not fire is not a control.")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
