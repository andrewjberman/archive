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
import importlib.util
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence


# --------------------------------------------------------------- the normative digest home

def _load_request_hash() -> Callable[[dict], str]:
    """Import `_request_hash` from C10-PRECOND rather than reimplementing it.

    The TO is explicit: "The digest derivation home is YOUR precondition_token.py
    _request_hash (normative; any other serialization is NON-CONFORMANT even if the sha256
    pattern matches)." Reimplementing it here would MINT A SECOND HOME for one derivation,
    which is the R8 two-homes class this program keeps finding -- and a divergent digest does
    not error, it silently mints a second identity for the same request.

    The sibling directory name contains a dot ('NFRA_EPISTEMY.C10-PRECOND'), so it is not a
    legal package path; importlib by file location is the correct loader, not a hack.

    FAILS LOUD. If C10 cannot be loaded we do NOT fall back to a local sha256 -- a silent
    fallback is exactly how the second home gets minted.
    """
    here = Path(__file__).resolve().parent
    target = here.parent / "NFRA_EPISTEMY.C10-PRECOND" / "precondition_token.py"
    if not target.is_file():
        raise ImportError(
            f"C6 requires the NORMATIVE digest home at {target}, which is absent. Refusing to "
            f"substitute a local sha256: any other serialisation is NON-CONFORMANT even if the "
            f"pattern matches, so a fallback would mint a SECOND derivation home."
        )
    name = "c10_precondition_token"
    cached = sys.modules.get(name)
    if cached is not None:
        return cached._request_hash
    spec = importlib.util.spec_from_file_location(name, target)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not build an import spec for {target}")
    mod = importlib.util.module_from_spec(spec)
    # REGISTER BEFORE exec_module. `dataclasses` resolves a class's __module__ through
    # sys.modules while processing the decorator, so a module that defines dataclasses
    # (C10 does) raises AttributeError: 'NoneType' object has no attribute '__dict__' if it
    # is executed while unregistered. Found by running this loader, not by reading it.
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        del sys.modules[name]   # never leave a half-executed module registered
        raise
    return mod._request_hash


# --------------------------------------------------------------------- C1 envelope enums

#: The RATIFIED C1 enums (observation_record.schema.json @6f944857c4). Named here so a call
#: site cannot invent a value; NEVER branched on.
RATIFIED_PLANES = ("DESIRED", "APPLIED", "EXERCISED")
RATIFIED_SUBSTRATES = ("aws", "portal", "codebase", "ms")

INSTRUMENT_ID = "transition_kernel.TransitionUnit"
INSTRUMENT_VERSION = "0.1.0-staged"


# --------------------------------------------------------------------------- refusals

class KernelRefusal(RuntimeError):
    """Base: the kernel declined to proceed. Always LOUD, never a silent degrade."""


class PrefixSafetyViolation(KernelRefusal):
    """A leg would breach prefix safety (sec.2.7's three-clause conjunction)."""


class InadmissibleRow(KernelRefusal):
    """Something tried to put an un-measured assertion into the residue ledger."""


class SupportHandoffViolation(KernelRefusal):
    """Required_Validity_Interval(c) is NOT a subset of Actual_Validity_Interval(c)."""


# ⛔ `PointOfNoReturn(KernelRefusal)` WAS DEFINED HERE AND IS DELETED. It was never raised
# (defined=1, raised=0, against a control of raised=3 for PrefixSafetyViolation) -- a dead
# token in the refusal vocabulary, found by auditing this module before handing it to CRO's
# spec cert rather than by anything failing.
#
# AND DELETION IS THE CORRECT FIX, NOT WIRING IT UP: crossing a declared point of no return
# is a LEGITIMATE ACT, not a refusal. The kernel records `_past_no_return` and the refusal
# happens LATER, at the next checkpoint's safe-terminal-reachable clause, which raises
# PrefixSafetyViolation (m2 exercises exactly that). The concept lives on the TERMINAL axis
# as ABANDONED_UNSAFE, not in the exception vocabulary.
#
# THE HAZARD IT POSED WAS NOT INERTNESS: a reader scanning the refusal vocabulary would
# reasonably conclude the kernel raises on crossing, and write a caller that catches an
# exception which cannot occur -- a handler for an unreachable branch, which reads as
# defensive and is dead. An enumerated name that nothing can produce is a Rule-24 defect on
# the refusal axis (a value with no member), one layer down from the enums.


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
    never mix (Rule-24 postulate ii: never a leg-level value beside a transition-level one).

    Declared layer: THE OUTCOME OF ONE LEG. CE closes with FAILED_MID_ACT (below).
    """

    LANDED = "LANDED"
    REFUSED_PREFIX_SAFETY = "REFUSED_PREFIX_SAFETY"
    REFUSED_SUPPORT_HANDOFF = "REFUSED_SUPPORT_HANDOFF"
    ABORTED_AT_CHECKPOINT = "ABORTED_AT_CHECKPOINT"

    #: MINTED BY 4.0.0_SA_CRO AS REGISTRY EXECUTOR, K1 spec cert A1 @b895b7e337, resolving
    #: the CE gap this packet declared as residual 1. Census run at base before the mint:
    #: 0 occupancy across the canon trio + CLAUDE.md + RULINGS.
    #:
    #: The leg's `act()` raised an UNEXPECTED exception mid-flight -- distinct from both
    #: REFUSED values (kernel-initiated, before the act) and from ABORTED_AT_CHECKPOINT
    #: (deliberate). CRO's reasoning, and it is the load-bearing half: THE MOST DANGEROUS
    #: LEG STATE -- possible PARTIAL EFFECTS, i.e. the stranded-state class -- MUST NOT BE
    #: THE LEAST RECORDED. Previously the exception propagated and no LegRecord existed at
    #: all, so the one outcome that can strand state was the one outcome the ledger could
    #: not express.
    #:
    #: RECORDING IS NOT SWALLOWING: the kernel records the row, marks the affected residue
    #: axis UNKNOWN (a crashed act's residue is genuinely unmeasured, never 0), and then
    #: RE-RAISES.
    FAILED_MID_ACT = "FAILED_MID_ACT"


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

    K6: every acquisition (= every measurement) emits a C1-envelope Observation_Record.

    ⛔ PLANE AND SUBSTRATE ARE CONSTRUCTOR PARAMETERS, NOT MODULE CONSTANTS, AND THE
    DIFFERENCE IS LOAD-BEARING. C10-PRECOND hardcodes PLANE="APPLIED" / SUBSTRATE="aws" and
    that is CORRECT THERE -- that emitter performs real conditional writes against real S3
    objects. C6's exercise runs on FIXTURE transitions behind the build-staging fence and
    touches no cloud substrate, so an emitted APPLIED/aws would assert a plane the
    measurement never stood on. A fixture run emits EXERCISED/codebase; only a call site
    activated by Andrew's worded act on a real mutation class passes APPLIED/aws.
    Hardcoding either bakes the fixture's identity into the production path or the reverse
    -- and it is precisely the constant that survives an activation nobody re-reads.
    """

    def __init__(self, plane: str = "EXERCISED", substrate: str = "codebase") -> None:
        if plane not in RATIFIED_PLANES:
            raise ValueError(f"plane {plane!r} is not in the ratified enum {RATIFIED_PLANES}")
        if substrate not in RATIFIED_SUBSTRATES:
            raise ValueError(
                f"substrate {substrate!r} is not in the ratified enum {RATIFIED_SUBSTRATES}")
        self._rows: list[LedgerRow] = []
        self._observations: list[dict] = []
        self._plane = plane
        self._substrate = substrate
        self._request_hash = _load_request_hash()

    def observations(self) -> Sequence[dict]:
        """The C1-envelope Observation_Records emitted, one per acquisition."""
        return tuple(self._observations)

    def _emit(self, leg_id: str, axis: str, method: str,
              value: Any, state: str, reason: Optional[str]) -> dict:
        """Build one Observation_Record conformant to the C1 envelope.

        The digest comes from C10's `_request_hash` -- the NORMATIVE home -- never a local
        sha256. Honesty rule mirrors C1's own allOf: a substantive value is KNOWN only when
        the whole status tuple succeeded.
        """
        request = {"leg_id": leg_id, "axis": axis, "method": method,
                   "instrument": INSTRUMENT_ID, "version": INSTRUMENT_VERSION}
        acquisition = "PRESENT" if state == "KNOWN" else "ABSENT"
        rec = {
            "instrument": {"id": INSTRUMENT_ID, "version": INSTRUMENT_VERSION},
            "request_hash": self._request_hash(request),
            "status": {"acquisition": acquisition, "transport": "SUCCEEDED",
                       "enumeration": "SUCCEEDED",
                       "parse": "SUCCEEDED" if state == "KNOWN" else "FAILED"},
            "plane": self._plane,
            "substrate": self._substrate,
            "population_predicate": (
                f"the residue produced on axis '{axis}' by leg '{leg_id}' of this transition"),
            "denominator": {"count": 1, "grain": "leg-axis measurement",
                            "generated_by": f"{INSTRUMENT_ID}.record_measurement"},
            "traversal_residue": [],
            "substantive_result": {"state": state, "value": value, "reason": reason},
            "control_references": [],
            "discrimination_certificate_ref": None,
            "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "support_pointers": [f"method:{method}"],
            "invalidation_predicates": [
                "the measured leg is re-run", "the transition manifest changes"],
        }
        self._observations.append(rec)
        return rec

    def record_measurement(
        self, leg_id: str, axis: str, measure_fn: Callable[[], float], method: str
    ) -> LedgerRow:
        # K6: EVERY acquisition emits an Observation_Record -- including the ones that FAIL.
        # A refused acquisition is still an acquisition, and C1's honesty rule covers it:
        # substantive_result UNKNOWN with the reason, never a missing record. Emitting only
        # on success would make the observation stream a census of survivors.
        if not callable(measure_fn):
            reason = (
                f"leg {leg_id} axis {axis}: record_measurement requires a CALLABLE that "
                f"measures the world. A value was passed instead, which is an agent "
                f"self-report -- inadmissible by construction (PRD sec.2.7)."
            )
            self._emit(leg_id, axis, method, None, "UNKNOWN", reason)
            raise InadmissibleRow(reason)

        measured = measure_fn()
        if isinstance(measured, bool) or not isinstance(measured, (int, float)):
            reason = (
                f"leg {leg_id} axis {axis}: measurement returned {measured!r}, not a number."
            )
            self._emit(leg_id, axis, method, None, "UNKNOWN", reason)
            raise InadmissibleRow(reason)

        row = LedgerRow(
            leg_id=leg_id,
            axis=axis,
            measured=float(measured),
            observed_at=datetime.now(timezone.utc),
            method=method,
        )
        self._rows.append(row)
        self._emit(leg_id, axis, method, float(measured), "KNOWN", None)
        return row

    def record_unknown(self, leg_id: str, axis: str, method: str, reason: str) -> dict:
        """Record that an axis's residue is UNMEASURED, with the reason (A1).

        No LedgerRow is appended -- there is no measurement to append, and inventing a 0
        would be the sentinel bug. What IS appended is the Observation_Record, carrying
        substantive_result UNKNOWN. So the ledger's ROW set stays a set of measurements,
        while the OBSERVATION set stays a complete census of acquisitions including the
        ones that could not be made.
        """
        return self._emit(leg_id, axis, method, None, "UNKNOWN", reason)

    def unknown_axes(self) -> frozenset[str]:
        """Axes with at least one UNKNOWN acquisition -- i.e. residue we cannot bound."""
        return frozenset(
            r["population_predicate"].split("'")[1]
            for r in self._observations
            if r["substantive_result"]["state"] == "UNKNOWN" and "'" in r["population_predicate"]
        )

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
        plane: str = "EXERCISED",
        substrate: str = "codebase",
    ) -> None:
        """plane/substrate default to the FIXTURE pair (EXERCISED/codebase).

        They are parameters rather than constants so that an activated call site -- which
        only Andrew's worded act can create -- passes APPLIED/aws, while a build-staging
        exercise cannot silently claim a cloud plane it never stood on.
        """
        self.manifest = manifest
        self.claims = tuple(claims)
        self.ledger = CumulativeResidueLedger(plane=plane, substrate=substrate)
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

        # A1 (CRO K1 spec cert @b895b7e337): an UNEXPECTED mid-act exception is RECORDED and
        # then RE-RAISED. Recording is not swallowing -- the caller still sees the exception,
        # and the ledger stops being blind to the one outcome that can strand state.
        try:
            act()
        except BaseException as exc:
            rec = LegRecord(
                leg_id,
                LegOutcome.FAILED_MID_ACT,
                f"{type(exc).__name__}: {exc}",
                # POSSIBLE partial effects. True is the CONSERVATIVE direction: it prevents
                # the transition from resolving ROLLED_BACK, which would claim a restoration
                # nobody performed on a leg whose effects are UNKNOWN.
                effects_survive=True,
            )
            self.legs.append(rec)
            # The residue this leg produced is genuinely UNMEASURED -- never 0. Emitting a
            # zero would be a scalar "nothing here", the sentinel bug one layer up.
            self.ledger.record_unknown(
                leg_id, residue_axis, method,
                f"act() raised {type(exc).__name__} mid-flight: {exc}")
            raise

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
        failed = [leg for leg in self.legs if leg.outcome is LegOutcome.FAILED_MID_ACT]

        # A1: a leg that crashed mid-act can NEVER resolve to COMPLETED or ROLLED_BACK, and
        # the reason must say the debt is UNBOUNDED rather than quoting a priced number --
        # the crashed leg's residue is UNKNOWN, so the sum of the measured rows is a FLOOR,
        # not the debt. Quoting it as the debt would be the wrong-denominator error inside
        # the very object that prices rollback.
        if failed:
            unknown = sorted(self.ledger.unknown_axes())
            return (
                Terminal.CONTAINED,
                f"{len(failed)} leg(s) FAILED MID-ACT ({'; '.join(f.detail for f in failed)}); "
                f"their effects are POSSIBLE BUT UNMEASURED on axes {unknown or ['<unnamed>']}. "
                f"Measured rollback debt {self._recovery_requirement()} is a FLOOR, not the "
                f"debt -- the crashed leg's residue is UNKNOWN. Restoration is neither "
                f"performed nor priceable; this is the stranded-state class, recorded.",
            )

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
