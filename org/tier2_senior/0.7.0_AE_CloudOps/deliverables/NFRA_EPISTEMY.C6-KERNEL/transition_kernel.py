"""C6-KERNEL -- the atomic transaction kernel (NFRA_EPISTEMY component 6).

SPEC OF RECORD: docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md sec.2.7
(Transition_Unit). CITED, NOT COPIED -- the object definitions here are schema-native
realisations of that section; the section itself is the authority and this module never
restates it as its own.

BUILD-STAGING ONLY. Nothing in this module is wired to a live write path. No gate is
armed on any real work. ACTIVATION OF THIS KERNEL ON ANY REAL MUTATION CLASS IS
ANDREW'S WORDED ACT -- not COO's, not CTO's, not this author's. The exercise runs on
scratch/fixture transitions.

WHAT THIS COMPONENT IS FOR, in one sentence: long transitions are NOT long transactions,
so instead of holding a lock across a chain we prove at EVERY LEG that the path is still
inside the envelope the opening word accepted.

THE TWO PROPERTIES THAT ARE STRUCTURAL RATHER THAN REVIEWED
-----------------------------------------------------------
1. A SCALAR RESIDUE IS INEXPRESSIBLE. `ResidueVector` has no constructor that accepts a
   number and no total ordering. sec.2.7 requires "a structured vector of INCOMPARABLE
   limits, never a scalar" -- so `within_envelope()` returns a per-axis verdict set, and
   there is deliberately no __lt__/__gt__ and no .total(). You cannot accidentally sum
   this object, because summing it is not implemented anywhere.

2. AN AGENT-SELF-REPORTED LEDGER ROW IS INEXPRESSIBLE. sec.2.7: the
   Cumulative_Residue_Ledger is gateway-maintained and AGENT SELF-REPORT IS INADMISSIBLE.
   The realisation of "inadmissible" here is not a validator that rejects bad rows -- it
   is that `CumulativeResidueLedger` HAS NO METHOD THAT ACCEPTS A ROW. The only way a row
   comes into being is `record_measurement(axis, measure_fn)`, which CALLS the measurement
   and records what it actually returned. There is no parameter anywhere into which an
   agent could pass an assertion about the world.

   ⛔ HONEST LIMIT, STATED RATHER THAN GLOSSED: Python has no true privacy. A determined
   caller can reach `_rows` directly. The claim this module makes is precisely
   "inexpressible through the public API", which is what distinguishes it from the
   deploy-completion ledger (S0 finding: `.tools/deploy_ledger.py` cmd_open/cmd_close_leg/
   cmd_close are CLI subcommands whose ENTIRE PURPOSE is to accept an agent's assertion).
   That is a difference in kind, not a claim of cryptographic integrity.

TERMINAL AXIS -- Rule-24 pre-record in S0_EMBRYO_GROUND_READ.md, routes through
4.0.0_SA_CRO base before 1.0.0_SA_CTO's arch gate. CONTAINED is distinct from ROLLED_BACK
on purpose: a kernel with only ROLLED_BACK must report a partially-landed transition as
rolled back, which is false in the direction that HIDES STRANDED STATE -- the class
NEVER#8 exists for.

Author: 0.7.0_AE_CloudOps. Digest home: precondition_token._request_hash (normative; any
other serialisation is NON-CONFORMANT even if the sha256 pattern matches).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Mapping, Optional, Sequence


# --------------------------------------------------------------------------- refusals

class KernelRefusal(RuntimeError):
    """Base: the kernel declined to proceed. Always LOUD, never a silent degrade."""


class PrefixSafetyViolation(KernelRefusal):
    """A leg would breach prefix safety (sec.2.7's three-clause conjunction)."""


class InadmissibleRow(KernelRefusal):
    """Something tried to put an un-measured assertion into the residue ledger."""


class SupportHandoffViolation(KernelRefusal):
    """Required_Validity_Interval(c) is NOT a subset of Actual_Validity_Interval(c)."""


class PointOfNoReturn(KernelRefusal):
    """Past a declared point of no return with insufficient recovery capacity."""


# --------------------------------------------------------------------------- terminals

class Terminal(str, Enum):
    """The terminal states of ONE governed transition. Declared layer, MECE over it.

    Disjoint on two questions: does any effect survive, and is that survival bounded?
    """

    COMPLETED = "COMPLETED"                  # every leg landed; intent achieved
    ROLLED_BACK = "ROLLED_BACK"              # no leg's effect survives; debt paid + proven
    CONTAINED = "CONTAINED"                  # some effects SURVIVE, bounded; debt outstanding, PRICED
    ABANDONED_UNSAFE = "ABANDONED_UNSAFE"    # past a point of no return; neither restorable nor bounded

    @classmethod
    def safe_terminals(cls) -> frozenset["Terminal"]:
        """Terminals the kernel may STEER TO. ABANDONED_UNSAFE is deliberately excluded.

        Rule-24 postulate (iv) is DECLARED-FAILING on this axis and that is recorded, not
        hidden: ABANDONED_UNSAFE is reachable only by escalation, never by kernel logic, so
        a "build the terminal handler" plan covers three of four members.
        """
        return frozenset({cls.COMPLETED, cls.ROLLED_BACK, cls.CONTAINED})


class LegOutcome(str, Enum):
    """Per-leg outcome. A DIFFERENT GRAIN from Terminal -- kept on its own axis so the two
    never mix (Rule-24 postulate ii: never a leg-level value beside a transition-level one)."""

    LANDED = "LANDED"
    REFUSED_PREFIX_SAFETY = "REFUSED_PREFIX_SAFETY"
    REFUSED_SUPPORT_HANDOFF = "REFUSED_SUPPORT_HANDOFF"
    ABORTED_AT_CHECKPOINT = "ABORTED_AT_CHECKPOINT"


# --------------------------------------------------------------------------- residue

@dataclass(frozen=True)
class ResidueVector:
    """A PATHWISE RESIDUE ENVELOPE -- a structured vector of INCOMPARABLE limits (sec.2.7).

    Deliberately absent, and their absence is the design: no __lt__, no __gt__, no
    .total(), no .scalar(), no __float__, no __int__. A scalar residue is not rejected
    here -- IT CANNOT BE WRITTEN. Two vectors are compared axis-by-axis and the result is
    a per-axis verdict, because incomparable limits do not collapse to one number.
    """

    axes: Mapping[str, float]

    def __post_init__(self) -> None:
        if not isinstance(self.axes, Mapping) or not self.axes:
            raise ValueError(
                "ResidueVector requires a non-empty mapping of NAMED axes. A residue with "
                "no named axes is a scalar wearing a vector's clothing."
            )
        for name, value in self.axes.items():
            if not isinstance(name, str) or not name:
                raise ValueError(f"residue axis names must be non-empty strings; got {name!r}")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"residue axis {name!r} must be numeric; got {value!r}")

    def within(self, envelope: "ResidueVector") -> dict[str, bool]:
        """PER-AXIS verdict. Never a single bool -- the caller must face each axis.

        An axis present in the residue and ABSENT from the envelope is False: an
        undeclared axis is not a permitted one. That is S6 absence semantics -- the
        envelope's silence about an axis DISQUALIFIES it rather than blessing it.
        """
        verdicts: dict[str, bool] = {}
        for name, value in self.axes.items():
            limit = envelope.axes.get(name)
            verdicts[name] = False if limit is None else value <= limit
        return verdicts

    def breached_axes(self, envelope: "ResidueVector") -> list[str]:
        return sorted(a for a, ok in self.within(envelope).items() if not ok)


# --------------------------------------------------------------------------- support

@dataclass(frozen=True)
class Interval:
    """A half-open validity interval [start, end)."""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ValueError("Interval endpoints must be timezone-aware (UTC).")
        if self.end <= self.start:
            raise ValueError("Interval end must be strictly after start.")

    def contains_interval(self, other: "Interval") -> bool:
        """other SUBSET-OF self."""
        return self.start <= other.start and other.end <= self.end


@dataclass(frozen=True)
class SupportClaim:
    """One claim whose support is leased (C4-LEASE is the producer; we CONSUME leases).

    `a lease is not a lock` -- sec.2.7, stated on the object per K4. The kernel therefore
    RE-READS actual validity at every checkpoint rather than caching the opening verdict.
    """

    claim_id: str
    required: Interval
    actual_at: Callable[[datetime], Optional[Interval]]

    def check(self, now: datetime) -> Interval:
        """Re-read the lease NOW. Never a cached verdict -- see m7."""
        actual = self.actual_at(now)
        if actual is None:
            raise SupportHandoffViolation(
                f"claim {self.claim_id}: no actual validity interval at {now.isoformat()} "
                f"(lease absent or expired). A lease is not a lock."
            )
        if not actual.contains_interval(self.required):
            raise SupportHandoffViolation(
                f"claim {self.claim_id}: Required_Validity_Interval "
                f"[{self.required.start.isoformat()}, {self.required.end.isoformat()}) is NOT "
                f"a subset of Actual [{actual.start.isoformat()}, {actual.end.isoformat()})."
            )
        return actual


# --------------------------------------------------------------------------- the ledger

@dataclass(frozen=True)
class LedgerRow:
    """A row that EXISTS ONLY as the return value of a measurement the kernel ran."""

    leg_id: str
    axis: str
    measured: float
    observed_at: datetime
    method: str


class CumulativeResidueLedger:
    """Kernel-maintained. AGENT SELF-REPORT IS INADMISSIBLE (sec.2.7).

    THERE IS NO append(row) / add_row(row) / submit(row). The absence is the control.
    `record_measurement` takes a CALLABLE and records what calling it actually returned,
    so a row cannot be authored -- only observed.
    """

    def __init__(self) -> None:
        self._rows: list[LedgerRow] = []

    def record_measurement(
        self, leg_id: str, axis: str, measure_fn: Callable[[], float], method: str
    ) -> LedgerRow:
        if not callable(measure_fn):
            raise InadmissibleRow(
                f"leg {leg_id} axis {axis}: record_measurement requires a CALLABLE that "
                f"measures the world. A value was passed instead, which is an agent "
                f"self-report -- inadmissible by construction (PRD sec.2.7)."
            )
        measured = measure_fn()
        if isinstance(measured, bool) or not isinstance(measured, (int, float)):
            raise InadmissibleRow(
                f"leg {leg_id} axis {axis}: measurement returned {measured!r}, not a number."
            )
        row = LedgerRow(
            leg_id=leg_id,
            axis=axis,
            measured=float(measured),
            observed_at=datetime.now(timezone.utc),
            method=method,
        )
        self._rows.append(row)
        return row

    def cumulative(self) -> Optional[ResidueVector]:
        """Cumulative residue as a VECTOR, summed WITHIN each axis and never ACROSS axes.

        Returns None when NOTHING HAS BEEN MEASURED YET -- which is not the same thing as
        "residue zero" and must not be spelled as a vector.

        ⛔ THIS RETURN TYPE IS A BUG FIX WITH A LESSON, KEPT IN THE COMMENT BECAUSE THE
        BUG WAS THE INTERESTING KIND. The first draft manufactured a sentinel axis
        `{"_no_measurement": 0.0}` so the return type could stay non-Optional. The battery
        refused leg1 of EVERY transition on its first run: the sentinel is an axis the
        envelope does not declare, and this module's own S6 rule (an undeclared axis is
        DISQUALIFIED, not blessed) correctly marked it breached. The sentinel was a scalar
        "nothing here" smuggled in wearing an axis name -- exactly the shape ResidueVector
        exists to make inexpressible. S6 absence semantics applied to the ledger itself:
        the absence of a measurement DISQUALIFIES a residue claim rather than valuing it 0.
        """
        totals: dict[str, float] = {}
        for row in self._rows:
            totals[row.axis] = totals.get(row.axis, 0.0) + row.measured
        if not totals:
            return None
        return ResidueVector(axes=totals)

    def rows(self) -> Sequence[LedgerRow]:
        return tuple(self._rows)

    def __len__(self) -> int:
        return len(self._rows)


# --------------------------------------------------------------------------- manifest

@dataclass(frozen=True)
class Checkpoint:
    leg_id: str
    description: str
    is_point_of_no_return: bool = False


@dataclass(frozen=True)
class TransitionManifest:
    """IMMUTABLE (sec.2.7): graph, targets, action classes, checkpoints, terminals.

    Frozen dataclass + tuple members: the manifest the opening word accepted cannot be
    edited mid-transition. If it could, "the path remains inside the envelope it accepted"
    would be trivially satisfiable by editing the envelope.
    """

    transition_id: str
    targets: tuple[str, ...]
    action_classes: tuple[str, ...]
    checkpoints: tuple[Checkpoint, ...]
    envelope: ResidueVector
    recovery_capacity: float
    policy_epoch: str
    knowledge_basis: str
    harm_model: str          # STAMP ONLY -- sec.2.9 is not buildable spec (rider (a))

    def manifest_digest(self) -> str:
        """Content-addressed id. DERIVATION HOME NAMED IN THE CONTRACT, per COO 64099:
        this function is the normative home, mirroring precondition_token._request_hash's
        serialisation (sorted keys, separators as below, trailing newline). ANY OTHER
        SERIALISATION IS NON-CONFORMANT EVEN IF THE sha256 PATTERN MATCHES.
        """
        payload = {
            "transition_id": self.transition_id,
            "targets": list(self.targets),
            "action_classes": list(self.action_classes),
            "checkpoints": [
                {"leg_id": c.leg_id, "description": c.description,
                 "is_point_of_no_return": c.is_point_of_no_return}
                for c in self.checkpoints
            ],
            "envelope": dict(sorted(self.envelope.axes.items())),
            "recovery_capacity": self.recovery_capacity,
            "policy_epoch": self.policy_epoch,
            "knowledge_basis": self.knowledge_basis,
            "harm_model": self.harm_model,
        }
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        return "tm:sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- the kernel

@dataclass
class LegRecord:
    leg_id: str
    outcome: LegOutcome
    detail: str
    effects_survive: bool


class TransitionUnit:
    """One governed transition. The opening word accepts the envelope; EACH CHECKPOINT
    proves the path remains inside it (sec.2.7)."""

    def __init__(
        self,
        manifest: TransitionManifest,
        claims: Sequence[SupportClaim] = (),
        recovery_exercised: bool = False,
    ) -> None:
        self.manifest = manifest
        self.claims = tuple(claims)
        self.ledger = CumulativeResidueLedger()
        self.legs: list[LegRecord] = []
        self._recovery_exercised = recovery_exercised
        self._past_no_return = False

    # -- prefix safety -----------------------------------------------------------

    def _recovery_requirement(self) -> float:
        """Rollback debt. Sum of residue on axes whose effects would need undoing.

        Priced, never ignored -- the half-landed-deploy class instrumented.
        """
        return sum(row.measured for row in self.ledger.rows())

    def remaining_capacity(self) -> float:
        return self.manifest.recovery_capacity - self._recovery_requirement()

    def _safe_terminal_reachable(self) -> bool:
        """A safe terminal is reachable while we are not past a point of no return."""
        return not self._past_no_return

    def check_prefix_safety(self, leg_id: str, now: Optional[datetime] = None) -> None:
        """sec.2.7's THREE-CLAUSE CONJUNCTION, all three per checkpoint.

        residue within envelope AND safe terminal reachable AND recovery requirement <=
        remaining capacity. Each clause raises on its own, so a battery can kill them
        independently -- a single fused boolean would make m1/m2/m3 indistinguishable.
        """
        now = now or datetime.now(timezone.utc)

        # clause 1 -- residue within envelope.
        # A ledger with NO measurements is not "residue zero" -- it is nothing measured,
        # and nothing measured cannot be outside anything. The opening leg legitimately
        # reaches here with an empty ledger.
        residue = self.ledger.cumulative()
        if residue is not None:
            breached = residue.breached_axes(self.manifest.envelope)
            if breached:
                raise PrefixSafetyViolation(
                    f"leg {leg_id}: residue OUTSIDE envelope on axes {breached} "
                    f"(residue={dict(residue.axes)}, envelope={dict(self.manifest.envelope.axes)})"
                )

        # clause 2 -- a safe terminal is reachable
        if not self._safe_terminal_reachable():
            raise PrefixSafetyViolation(
                f"leg {leg_id}: NO SAFE TERMINAL REACHABLE (past a declared point of no "
                f"return). Reachable set would be {{}} of {sorted(t.value for t in Terminal.safe_terminals())}."
            )

        # clause 3 -- recovery requirement <= remaining capacity (ROLLBACK DEBT PRICED)
        requirement = self._recovery_requirement()
        capacity = self.manifest.recovery_capacity
        if requirement > capacity:
            raise PrefixSafetyViolation(
                f"leg {leg_id}: recovery requirement {requirement} EXCEEDS capacity {capacity} "
                f"-- rollback debt unpayable, so the leg is refused BEFORE it is incurred."
            )

        # clause 4 (K4) -- support handoff, RE-READ per checkpoint, never cached (m7)
        for claim in self.claims:
            claim.check(now)

    # -- legs --------------------------------------------------------------------

    def run_leg(
        self,
        leg_id: str,
        act: Callable[[], None],
        residue_axis: str,
        measure_fn: Callable[[], float],
        method: str,
        now: Optional[datetime] = None,
    ) -> LegRecord:
        """Run ONE leg: check prefix safety, act, then MEASURE the residue it produced."""
        checkpoint = next((c for c in self.manifest.checkpoints if c.leg_id == leg_id), None)

        try:
            self.check_prefix_safety(leg_id, now=now)
        except SupportHandoffViolation as exc:
            rec = LegRecord(leg_id, LegOutcome.REFUSED_SUPPORT_HANDOFF, str(exc), effects_survive=False)
            self.legs.append(rec)
            raise
        except PrefixSafetyViolation as exc:
            rec = LegRecord(leg_id, LegOutcome.REFUSED_PREFIX_SAFETY, str(exc), effects_survive=False)
            self.legs.append(rec)
            raise

        act()
        if checkpoint is not None and checkpoint.is_point_of_no_return:
            self._past_no_return = True

        self.ledger.record_measurement(leg_id, residue_axis, measure_fn, method)
        rec = LegRecord(leg_id, LegOutcome.LANDED, "landed", effects_survive=True)
        self.legs.append(rec)
        return rec

    def abort_at_checkpoint(self, leg_id: str, reason: str) -> LegRecord:
        rec = LegRecord(leg_id, LegOutcome.ABORTED_AT_CHECKPOINT, reason, effects_survive=False)
        self.legs.append(rec)
        return rec

    # -- terminals ---------------------------------------------------------------

    def terminal(self) -> tuple[Terminal, str]:
        """Resolve the transition's terminal, with the reason stated.

        m6: a recovery path never exercised is ASSUMED, never PROVEN -- so a
        ROLLED_BACK claim requires `recovery_exercised`, otherwise the honest terminal is
        CONTAINED with the debt outstanding.
        """
        if self._past_no_return and self.remaining_capacity() < 0:
            return (
                Terminal.ABANDONED_UNSAFE,
                "past a declared point of no return with recovery requirement exceeding "
                "capacity -- escalation, not a terminal the kernel may choose",
            )

        aborted = [leg for leg in self.legs if leg.outcome is LegOutcome.ABORTED_AT_CHECKPOINT]
        landed = [leg for leg in self.legs if leg.outcome is LegOutcome.LANDED]

        if aborted:
            if any(leg.effects_survive for leg in landed):
                if not self._recovery_exercised:
                    return (
                        Terminal.CONTAINED,
                        f"{len(landed)} leg(s) landed and their effects SURVIVE; the recovery "
                        f"path has NOT been exercised on the real plane, so restoration is "
                        f"ASSUMED and priced, never PROVEN. Rollback debt outstanding: "
                        f"{self._recovery_requirement()}",
                    )
                return (
                    Terminal.ROLLED_BACK,
                    "recovery path EXERCISED; no leg's effect survives",
                )
            return (Terminal.ROLLED_BACK, "aborted before any leg landed; nothing to restore")

        if landed and len(landed) == len(self.manifest.checkpoints):
            return (Terminal.COMPLETED, "every leg landed; intent achieved")

        return (
            Terminal.CONTAINED,
            f"{len(landed)} of {len(self.manifest.checkpoints)} legs landed; intent NOT "
            f"achieved and effects survive. Rollback debt: {self._recovery_requirement()}",
        )
