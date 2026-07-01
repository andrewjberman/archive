"""SCTY_MCPGUARD -- the _run()-entry guard decision (tier + G2 fail-closed gate).

STAGED IMPLEMENTABLE-CHANGE (build-lane 0.5.0_AE_OpalETL). The landing-diff core the
CTO scoped: resolve tier ONCE at _run entry -> classify -> the TWO fail-closed denials
(CTO gate-(c) Q3 reqs (i)+(ii)). Destined for `infra/aws/ec2/m365-mcp-gateway/app/guard.py`,
called from tools._run() -- circulated to 0.7.0 (owner) for ack, deployed via THEIR lane
(Rule 12), CTO landing-gate + 0.8.0 no-bypass corroboration before GO-live.

SCOPE = the LANDING foundation (tier resolution + G2 classify + fail-closed denials + tier
for G6 audit). G3 confirm-on-irreversible / G1 recipient-cap layer ON TOP next (this module
is the seam they extend). SAFE reads bypass with zero added latency.

Grounding: tier.py (resolve_tier), destructive_ops.py (classify), CTO gate-(c) PASS
requirements Q3(i) identity-failure fail-closed + Q3(ii) READ_ONLY-cannot-mutate.
"""
from __future__ import annotations

from destructive_ops import OpClass, classify
from tier import Tier, resolve_tier


class GuardDenied(Exception):
    """A fail-closed denial at the guard. _run() converts this to a structured tool error
    (never a 500, never a silent pass) and audits it (G6)."""
    def __init__(self, reason: str, code: str):
        super().__init__(reason)
        self.reason = reason
        self.code = code


def enforce(tool: str, email: str, tier: Tier) -> None:
    """G2 + fail-closed gate. Call at _run() entry AFTER resolving tier once (tier also goes
    to the G6 audit for EVERY call). Returns None if the call may proceed; raises GuardDenied
    on a fail-closed condition.

    Fail-closed conditions (CTO Q3 reqs):
      - (ii) a READ_ONLY tier reaching a mutating tool -> DENY (belt to B2's permission-layer suspenders).
      - (i)  a mutating call with NO verified identity -> DENY (an identity we can't establish = no write).
    SAFE (read) tools bypass entirely. STANDARD_EMPLOYEE / MASTER_ADMIN pass THIS gate
    (G1 recipient-cap + G3 confirm-on-irreversible are layered next, not here).
    """
    tag = classify(tool)

    # SAFE reads: bypass the guard (tier already captured upstream for audit).
    if tag["class"] is OpClass.SAFE:
        return

    # From here the tool is mutating OR unclassified (fail-closed-destructive).

    # (i) identity-failure fail-closed: a mutating call requires a verified identity.
    #     (_run resolves email from the verified OIDC claim; empty = we could not establish one.)
    if not email:
        raise GuardDenied(
            f"mutating tool '{tool}' requires a verified identity; none established",
            code="identity_required",
        )

    # (ii) READ_ONLY cannot mutate -- guard-layer belt (B2 read-only-scope token is the
    #      permission-layer suspenders; a token-scope gap must NOT become a write).
    if tier is Tier.READ_ONLY:
        raise GuardDenied(
            f"tier READ_ONLY may not call mutating tool '{tool}'",
            code="read_only_denied",
        )

    # STANDARD_EMPLOYEE / MASTER_ADMIN: permitted at G2. (Next layers: G3 confirm-on-irreversible
    # applies to ALL tiers incl master-admin per the CTO safety-not-authz corollary; G1 recipient-cap
    # applies to non-master tiers.)
    return


def resolve_and_enforce(tool: str, email: str, cfg) -> Tier:
    """Convenience for _run(): resolve the tier ONCE (returned for the G6 audit on every call)
    and enforce the gate. Raises GuardDenied on a fail-closed condition."""
    tier = resolve_tier(email, cfg)
    enforce(tool, email, tier)
    return tier
