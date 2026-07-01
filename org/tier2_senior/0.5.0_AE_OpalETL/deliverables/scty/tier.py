"""SCTY_MCPGUARD -- user-type tier resolution (root-of-trust for the guardrail model).

STAGED IMPLEMENTABLE-CHANGE (build-lane 0.5.0_AE_OpalETL) for CTO gate (c) BEFORE it
touches the live dispatch path. Destined for `infra/aws/ec2/m365-mcp-gateway/app/tier.py`
once (c) CTO implementable-gate + (a) 0.7.0 IDENTITY_PROVIDER + (b) 0.8.0 no-bypass land.
NOT yet wired into _run() (that wiring is the live-path landing, still gated).

Design + arch-gate: docs/briefs/scty-mcpguard-s0-tier-model-destructive-surface-spec-20260701.md
(spec ae651397e) -> CTO Part-A PASS (fail-closed rule + ADD-1/2/3, 171857Z).

ROOT-OF-TRUST AXIOM: a tier is only as trustworthy as the identity provider's SIGNATURE
verification. `identity.py` dispatches across 5 providers; only alb_oidc (ES256, always)
and cloudflare (RS256, ONLY if CF_ACCESS_TEAM_DOMAIN+CF_ACCESS_AUD configured) verify the
signature. verified_access (verify_signature=False -- PREMCP P1b TODO), tailscale and header
(DEV) do NOT. So an elevated tier resolves ONLY under a verified provider; otherwise EVERY
caller is forced to READ_ONLY. A master-admin tier keyed off a forgeable X-User-Email is the
single highest-severity failure of this design -- _provider_is_verified() prevents it
structurally (fail-closed).
"""
from __future__ import annotations

import enum


class Tier(enum.Enum):
    """Ordered least->most privileged. Compare by capability, never by name."""
    READ_ONLY = "read_only"            # default + the fail-closed floor; no write tools
    STANDARD_EMPLOYEE = "standard"     # write-capable, but G1-capped + G3-confirmed
    MASTER_ADMIN = "master_admin"      # andrew@ + systems allowlist; exempt from CAPS, NOT from G3


# Providers whose email claim is cryptographically SIGNATURE-verified in identity.py.
# alb_oidc: ES256 vs regional ELB key (identity.py:62) -- always verified.
# cloudflare: RS256 (identity.py:45) -- ONLY when CF_ACCESS_TEAM_DOMAIN+CF_ACCESS_AUD set
#   (else identity.py:30 skips verify and header-trusts) -> conditional, checked below.
# verified_access: identity.py:94 verify_signature=False -> NOT verified until PREMCP P1b.
# tailscale/header: header-trust / DEV -> NEVER verified.
_ALWAYS_VERIFIED = frozenset({"alb_oidc"})


def _provider_is_verified(cfg) -> bool:
    """True IFF the ACTIVE identity provider cryptographically verifies its email claim.
    This is the root-of-trust gate: no elevated tier is reachable when this is False."""
    provider = getattr(cfg, "IDENTITY_PROVIDER", None)
    if provider in _ALWAYS_VERIFIED:
        return True
    if provider == "cloudflare":
        # RS256 verification only actually runs when BOTH are configured (identity.py:30).
        return bool(getattr(cfg, "CF_ACCESS_TEAM_DOMAIN", None) and getattr(cfg, "CF_ACCESS_AUD", None))
    if provider == "verified_access":
        # Flips to True only once PREMCP P1b lands real signature verification.
        return bool(getattr(cfg, "VA_SIGNATURE_VERIFIED", False))
    # header, tailscale, unknown -> never verified.
    return False


def _norm(email: str) -> str:
    """identity.py already lowercases+strips; normalize defensively for exact-match safety."""
    return (email or "").strip().lower()


def _exact_in(email: str, allowlist) -> bool:
    """EXACT STRING EQUALITY only (CTO ADD-1). NEVER substring/domain/pattern -- so
    'andrew@opalinvest.com.evil' and 'andrew@opalinvest.co' can NOT match 'andrew@opalinvest.com'."""
    e = _norm(email)
    return any(e == _norm(a) for a in (allowlist or ()))


def resolve_tier(email: str, cfg) -> Tier:
    """Resolve the caller's user-type tier from the VERIFIED email claim + config.

    Fail-closed order (CTO Part-A PASS + ADD-1/2/3):
      1. Provider not signature-verified  -> READ_ONLY for EVERYONE (incl. andrew@). Root-of-trust.
      2. email exact-matches MASTER_ADMIN_EMAILS (andrew@ + systems allowlist) -> MASTER_ADMIN.
      3. email exact-matches WRITE_CAPABLE_EMAILS (explicit employee write-grant)  -> STANDARD_EMPLOYEE.
      4. any other verified identity (unknown/unmatched) -> READ_ONLY  (ADD-2: least-privilege default;
         write is opt-in per identity, never the default).
    """
    # (1) ROOT-OF-TRUST: an unverified provider means the email (=tier key) is forgeable.
    #     No elevated tier is reachable; force the floor for all. (ADD-3's config.validate
    #     boot-gate should already have refused header/tailscale in prod -- this is the
    #     belt to that suspenders, and also covers unconfigured-cloudflare / pre-P1b-VA.)
    if not _provider_is_verified(cfg):
        return Tier.READ_ONLY

    # (2) MASTER-ADMIN -- exact-match only (ADD-1).
    if _exact_in(email, getattr(cfg, "MASTER_ADMIN_EMAILS", ())):
        return Tier.MASTER_ADMIN

    # (3) STANDARD-EMPLOYEE -- write is an EXPLICIT per-identity grant (ADD-2), not "any @opalinvest.com".
    if _exact_in(email, getattr(cfg, "WRITE_CAPABLE_EMAILS", ())):
        return Tier.STANDARD_EMPLOYEE

    # (4) Verified but unmatched -> least-privilege floor (ADD-2).
    return Tier.READ_ONLY


# --- ADD-3 boot-gate helper (to be called from config.validate in the gateway) -------------
# Rejects a spoofable identity provider in production so the tier root-of-trust can't be
# silently undermined by a misconfig. Returns a list of fatal errors (empty = OK).
_SPOOFABLE_PROVIDERS = frozenset({"header", "tailscale"})


def validate_identity_provider_for_prod(cfg) -> list[str]:
    """Boot-gate: in prod, the IDENTITY_PROVIDER MUST be signature-verifying.
    Call from config.validate(); a non-empty return should FAIL boot (fail-closed)."""
    errs: list[str] = []
    env = str(getattr(cfg, "ENV", "") or "").lower()
    is_prod = env in ("prod", "production")
    provider = getattr(cfg, "IDENTITY_PROVIDER", None)
    if is_prod and provider in _SPOOFABLE_PROVIDERS:
        errs.append(
            f"IDENTITY_PROVIDER='{provider}' is spoofable and is FORBIDDEN in prod "
            f"(tier root-of-trust requires a signature-verified provider: alb_oidc, "
            f"or cloudflare with CF_ACCESS_TEAM_DOMAIN+CF_ACCESS_AUD)."
        )
    if is_prod and provider == "cloudflare" and not (
        getattr(cfg, "CF_ACCESS_TEAM_DOMAIN", None) and getattr(cfg, "CF_ACCESS_AUD", None)
    ):
        errs.append(
            "IDENTITY_PROVIDER='cloudflare' in prod without CF_ACCESS_TEAM_DOMAIN+CF_ACCESS_AUD "
            "falls back to header-trust (identity.py:30) -- configure JWT verification or fail boot."
        )
    if is_prod and provider == "verified_access" and not getattr(cfg, "VA_SIGNATURE_VERIFIED", False):
        errs.append(
            "IDENTITY_PROVIDER='verified_access' in prod but VA signature verification is not enabled "
            "(PREMCP P1b) -- elevated tiers (incl. master-admin) will NOT function until P1b lands."
        )
    return errs
