"""C5-POLICY -- Policy_Object / Scope_Declaration / Policy_Epoch + the scope engine.

SPEC OF RECORD: docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md sec.2.5 (the
waiver law) and sec.2.6 (authority/scope gate, typed rejection, policy_epoch), plus S5
sec.2/sec.4. CITED, NOT COPIED.

sec.2.5, the component's spine, verbatim: "A NEW MEMBER IS NEVER COVERED BY AN OLD
ENUMERATED WAIVER; it may be covered by a RATIFIED PREDICATE whose declared scope includes
it."

⛔ THE FENCE, AND IT IS THE GOVERNING CONSTRAINT OVER ANY PROSE IT CONTRADICTS
------------------------------------------------------------------------------
THIS ENGINE IS **INERT BY CONSTRUCTION, NOT INERT BY CONFIGURATION.** It ANSWERS QUESTIONS
about declared policy objects. It has no method that blocks, denies, enforces, mutates, or
registers anything, and -- this is the load-bearing half -- **THERE IS NO FLAG THAT COULD
BE FLIPPED TO GIVE IT ONE.** A scope engine whose inertness is a setting is one commit from
being an approval step nobody authorized.

Andrew's standing law: NO GATE IS IMPLEMENTED ON ANY WORK WITHOUT HIS EXPLICIT WORD.
Nothing here evaluates a real act, blocks a real commit, or wires into a real hook.
`evaluate()` returns a VERDICT OBJECT to its caller and that is the entire surface.

⛔ SCOPE_DECLARATION CARRIES TWO PLANES AND DOES NOT FLATTEN THEM (CRO cert-shaping note,
64627, sent before this schema landed so it could be built once).
------------------------------------------------------------------------------------------
The S0 measurement of `.owned-paths.yaml` @09cb994306 found the estate's own authority
surface split across two axes in OPPOSITE representational regimes:

    WHAT plane (paths)      250 rules -- 26% enumeration / 74% PREDICATE
    WHO  plane (principals) 518 entries -- 99% ENUMERATION / 1 pattern / 4 dead

**THE TWO PLANES FAIL DIFFERENTLY, WHICH IS WHY ONE GRAMMAR OVER BOTH WOULD BE TWO GRAINS
ON ONE AXIS (Rule-24 postulate ii):**
  - a PREDICATE over-includes CONSERVATIVELY and fails LOUDLY -- you can see its scope.
  - an ENUMERATION under-includes SILENTLY, through DEAD MEMBERS: an entry naming a
    principal that never existed simply never matches, so the declaration READS as granting
    and BEHAVES as granting nothing, with no error at any point.
    Live exhibit: lane `POD4_OR_EXEC` enumerates `0.4.0_DS_ClientPlatform_A/_B/_C/_D` with
    an UNDERSCORE where lane serials use a TILDE. Measured 0 in liveness / 0 in spawn-audit
    / no inbox, against a positive control of 47 for the tilde form.

So the WHO plane carries PROVENANCE (each enumerated member can be asked whether it ever
resolved) and the WHAT plane does not need it. Same object, two planes, different absence
semantics -- declared rather than flattened.

Author: 0.7.0_AE_CloudOps. Objects route through 4.0.0_SA_CRO base for the spec cert, THEN
1.0.0_SA_CTO's arch gate (TO :74-75). NEVER landed in-lane.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Optional


# --------------------------------------------------------------------- typed rejection

class Gate(str, Enum):
    """S5 sec.2's GATE field. REUSED, not coined -- C5 mints no gate values."""

    AUTHORITY = "AUTHORITY"
    COMPILATION = "COMPILATION"


class Reason(str, Enum):
    """S5 sec.2's REASON field. REUSED, not coined.

    ⛔ TWO FIELDS, NEVER FLATTENED (sec.2.6). A scope miss is the PAIR
    (Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS) -- never a generic failure, and never a
    single fused string. m4 exists to make a flattened rejection fail the battery.

    If C5 needs a reason S5 lacks, that is a PROPOSAL to base, NOT a mint here. The
    precedent: C10's TOKEN_INADMISSIBLE was proposed and base did NOT accept it as minted --
    they homed those cases at (COMPILATION, BUNDLE_MALFORMED), on the principle that TWO
    REMEDIES NEVER SHARE ONE GATE.
    """

    AUTHORITY_SCOPE_MISS = "AUTHORITY_SCOPE_MISS"
    BUNDLE_MALFORMED = "BUNDLE_MALFORMED"


@dataclass(frozen=True)
class Rejection:
    """The two-field rejection. `gate` and `reason` are SEPARATE ATTRIBUTES by construction;
    there is no combined field and no __str__ that fuses them into one token."""

    gate: Gate
    reason: Reason
    detail: str

    def as_pair(self) -> tuple[str, str]:
        return (self.gate.value, self.reason.value)


# --------------------------------------------------------------------------- the planes

class Regime(str, Enum):
    """HOW a scope plane declares its members. Declared layer: the representational regime
    of ONE scope plane.

    MECE over that layer: a plane either lists its members (ENUMERATION) or describes them
    (PREDICATE). CE hunted -- a plane that does BOTH is not a third regime; it is two planes,
    which is exactly why Scope_Declaration has two rather than one grammar with a mode flag.
    """

    ENUMERATION = "ENUMERATION"
    PREDICATE = "PREDICATE"


@dataclass(frozen=True)
class WhatPlane:
    """The WHAT axis -- which objects are in scope. PREDICATE-CAPABLE.

    Absence semantics (S6): an object matching NO rule is NOT COVERED. Silence disqualifies;
    it never blesses. A predicate over-includes conservatively and its scope is READABLE,
    so this plane needs no provenance.
    """

    regime: Regime
    members: tuple[str, ...]

    _GLOB = re.compile(r"[*?\[\]]")

    def covers(self, target: str) -> bool:
        if self.regime is Regime.ENUMERATION:
            # THE WAIVER LAW, sec.2.5: an enumeration covers EXACTLY its listed members.
            # A new member is NEVER covered -- this is the literal-match branch and it is
            # the whole point of the distinction.
            return target in self.members
        return any(self._glob_match(m, target) for m in self.members)

    @staticmethod
    def _glob_match(pattern: str, target: str) -> bool:
        rx = re.escape(pattern).replace(r"\*\*", "\x00").replace(r"\*", "[^/]*")
        rx = rx.replace("\x00", ".*").replace(r"\?", ".")
        return re.fullmatch(rx, target) is not None

    def declared_regime_is_honest(self) -> bool:
        """A plane declaring PREDICATE whose members contain no glob is lying about itself."""
        if self.regime is Regime.PREDICATE:
            return any(self._GLOB.search(m) for m in self.members)
        return not any(self._GLOB.search(m) for m in self.members)


@dataclass(frozen=True)
class WhoPlane:
    """The WHO axis -- which principals hold the authority. ENUMERATION-WITH-PROVENANCE.

    ⛔ THE PROVENANCE HALF IS NOT SYMMETRY WITH WhatPlane; IT EXISTS BECAUSE THIS PLANE
    FAILS SILENTLY AND THE OTHER DOES NOT. An enumerated principal that never existed never
    matches, so the declaration reads GRANTED and behaves as granting nothing, with no error
    anywhere. `resolver` is how a member can be ASKED whether it ever resolved.

    S6 absence semantics, and note it differs from WhatPlane's: a principal absent from the
    enumeration is NOT COVERED (same as WHAT), but a principal PRESENT in the enumeration and
    UNRESOLVABLE is a DEAD MEMBER -- a third state that the WHAT plane has no analogue for,
    and the reason these are two planes rather than one grammar.
    """

    regime: Regime
    members: tuple[str, ...]
    #: Optional oracle: does this principal exist? None => provenance UNAVAILABLE, which is
    #: NOT the same as "all members are live" and is never reported as such.
    resolver: Optional[Callable[[str], bool]] = None

    _GLOB = re.compile(r"[*?\[\]]")

    def covers(self, principal: str) -> bool:
        if self.regime is Regime.ENUMERATION:
            return principal in self.members
        return any(WhatPlane._glob_match(m, principal) for m in self.members)

    def dead_members(self) -> Optional[tuple[str, ...]]:
        """Members that do not resolve to a real principal.

        Returns None when NO RESOLVER WAS SUPPLIED -- provenance is UNAVAILABLE, and that is
        reported as unavailable rather than as an empty list. An empty tuple means
        'asked, and none are dead'; None means 'not asked'. Collapsing those two is the
        absence-semantics error this object exists to avoid.
        """
        if self.resolver is None:
            return None
        if self.regime is Regime.PREDICATE:
            return tuple()   # a pattern has no enumerated members to be dead
        return tuple(m for m in self.members if not self.resolver(m))


# --------------------------------------------------------------------------- the objects

@dataclass(frozen=True)
class ScopeDeclaration:
    """TWO PLANES, DECLARED SEPARATELY (CRO 64627). Not one grammar with a mode flag."""

    declaration_id: str
    what: WhatPlane
    who: WhoPlane
    ratified: bool = False   # sec.2.5: only a RATIFIED predicate can cover a new member


@dataclass(frozen=True)
class PolicyEpoch:
    """WHEN a policy was in force. Half-open [in_force_from, in_force_until)."""

    epoch_id: str
    in_force_from: datetime
    in_force_until: Optional[datetime] = None   # None => still in force (S6: open, not absent)

    def __post_init__(self) -> None:
        if self.in_force_from.tzinfo is None:
            raise ValueError("in_force_from must be timezone-aware (UTC)")
        if self.in_force_until is not None and self.in_force_until <= self.in_force_from:
            raise ValueError("in_force_until must be strictly after in_force_from")

    def in_force_at(self, instant: datetime) -> bool:
        if instant < self.in_force_from:
            return False
        return self.in_force_until is None or instant < self.in_force_until


@dataclass(frozen=True)
class PolicyObject:
    """One declared authority.

    `required_authority_class` IS A FIELD, NEVER A THRESHOLD (S5 sec.4). There is no numeric
    comparison against it anywhere in this module and no parameter that could accumulate
    toward it: NO PROOF COUNT REACHES A WORD. m5 exists because 'enough evidence should
    satisfy it' is the intuitive and wrong implementation.
    """

    policy_id: str
    scope: ScopeDeclaration
    epoch: PolicyEpoch
    required_authority_class: str


# --------------------------------------------------------------------------- the verdict

@dataclass(frozen=True)
class ScopeVerdict:
    """WHAT THE ENGINE RETURNS. It is a description, not an action.

    There is no `.enforce()`, no `.block()`, no `.raise_if_denied()`. A caller that wants to
    act on this must decide to, in its own code, under its own authority.
    """

    admitted: bool
    rejection: Optional[Rejection]
    policy_id: str
    evaluated_at: datetime
    #: Provenance from the WHO plane. None => not asked (see WhoPlane.dead_members).
    dead_principals: Optional[tuple[str, ...]] = None
    notes: tuple[str, ...] = field(default_factory=tuple)


class ScopeEngine:
    """ANSWERS 'is this act inside this authority's declared scope?' -- and does nothing else.

    ⛔ INERT BY CONSTRUCTION. The public surface is exactly `evaluate`. There is deliberately
    no enforce/block/deny/apply/gate/register/install method and NO CONSTRUCTOR PARAMETER
    that could turn one on. The battery asserts that absence rather than trusting this
    docstring, because a claim about what an API refuses is not settleable by reading it.
    """

    def evaluate(
        self,
        policy: PolicyObject,
        *,
        principal: str,
        target: str,
        instant: datetime,
        is_new_member: bool = False,
    ) -> ScopeVerdict:
        """Evaluate one act against one policy, at one instant.

        Every clause raises no exception and blocks nothing -- it returns a verdict. The
        clauses are evaluated INDEPENDENTLY so a clause-independence mutant can disarm each
        one and kill exactly one check (COO's C6 method, adopted here).
        """
        notes: list[str] = []
        dead = policy.scope.who.dead_members()
        if dead is None:
            notes.append("WHO-plane provenance UNAVAILABLE (no resolver supplied) -- "
                         "dead members neither confirmed nor excluded")
        elif dead:
            notes.append(f"WHO-plane DEAD MEMBERS present: {list(dead)} -- these enumerate "
                         f"principals that do not resolve; the declaration reads as granting "
                         f"to them and grants nothing")

        # CLAUSE 1 -- EPOCH. An act is evaluated against the policy in force AT ITS INSTANT.
        if not policy.epoch.in_force_at(instant):
            return ScopeVerdict(
                False,
                Rejection(Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS,
                          f"policy {policy.policy_id} epoch {policy.epoch.epoch_id} was NOT "
                          f"in force at {instant.isoformat()}"),
                policy.policy_id, _now(), dead, tuple(notes))

        # CLAUSE 2 -- WHO plane.
        if not policy.scope.who.covers(principal):
            return ScopeVerdict(
                False,
                Rejection(Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS,
                          f"principal {principal!r} is not in the WHO plane of "
                          f"{policy.scope.declaration_id}"),
                policy.policy_id, _now(), dead, tuple(notes))

        # CLAUSE 3 -- THE WAIVER LAW (sec.2.5). THE COMPONENT'S SPINE.
        # A NEW member is never covered by an OLD ENUMERATED waiver. It may be covered by a
        # RATIFIED PREDICATE whose declared scope includes it.
        if is_new_member and policy.scope.what.regime is Regime.ENUMERATION:
            return ScopeVerdict(
                False,
                Rejection(Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS,
                          f"{target!r} is a NEW MEMBER and {policy.scope.declaration_id}'s "
                          f"WHAT plane is an ENUMERATION -- a new member is NEVER covered by "
                          f"an old enumerated waiver (PRD sec.2.5)"),
                policy.policy_id, _now(), dead, tuple(notes))

        if is_new_member and not policy.scope.ratified:
            return ScopeVerdict(
                False,
                Rejection(Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS,
                          f"{target!r} is a NEW MEMBER and {policy.scope.declaration_id} is a "
                          f"predicate that is NOT RATIFIED -- sec.2.5 admits a new member only "
                          f"under a RATIFIED predicate"),
                policy.policy_id, _now(), dead, tuple(notes))

        # CLAUSE 4 -- WHAT plane.
        if not policy.scope.what.covers(target):
            return ScopeVerdict(
                False,
                Rejection(Gate.AUTHORITY, Reason.AUTHORITY_SCOPE_MISS,
                          f"{target!r} is not in the WHAT plane of "
                          f"{policy.scope.declaration_id}"),
                policy.policy_id, _now(), dead, tuple(notes))

        return ScopeVerdict(True, None, policy.policy_id, _now(), dead, tuple(notes))


def _now() -> datetime:
    return datetime.now(timezone.utc)
