"""Self-test for tier.resolve_tier -- proves the fail-closed root-of-trust + ADD-1/2/3.
Standalone (no pytest dep): `python test_tier.py` -> exits 0 on all-pass, 1 on any fail.
CVO does the LIVE cert on the running gateway; this proves the pure-logic correctness first.
"""
from __future__ import annotations

import sys

from tier import Tier, resolve_tier, validate_identity_provider_for_prod


class _Cfg:
    """Minimal fake of the gateway config surface tier.py reads."""
    def __init__(self, **kw):
        self.IDENTITY_PROVIDER = kw.get("provider")
        self.MASTER_ADMIN_EMAILS = kw.get("master", ("andrew@opalinvest.com",))
        self.WRITE_CAPABLE_EMAILS = kw.get("write", ())
        self.CF_ACCESS_TEAM_DOMAIN = kw.get("cf_domain")
        self.CF_ACCESS_AUD = kw.get("cf_aud")
        self.VA_SIGNATURE_VERIFIED = kw.get("va_verified", False)
        self.ENV = kw.get("env", "prod")


CASES = []
def case(name, got, want):
    CASES.append((name, got, want))


# --- ROOT-OF-TRUST: unverified provider forces READ_ONLY for EVERYONE (incl. andrew@) ---
case("header+andrew -> READ_ONLY (spoofable provider)",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="header")), Tier.READ_ONLY)
case("tailscale+andrew -> READ_ONLY",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="tailscale")), Tier.READ_ONLY)
case("verified_access (P1b not landed) + andrew -> READ_ONLY",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="verified_access", va_verified=False)), Tier.READ_ONLY)
case("cloudflare UNCONFIGURED + andrew -> READ_ONLY",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="cloudflare")), Tier.READ_ONLY)

# --- VERIFIED providers: elevated tiers reachable ---
case("alb_oidc + andrew EXACT -> MASTER_ADMIN",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="alb_oidc")), Tier.MASTER_ADMIN)
case("cloudflare CONFIGURED + andrew -> MASTER_ADMIN",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="cloudflare", cf_domain="opal.cloudflareaccess.com", cf_aud="aud123")), Tier.MASTER_ADMIN)
case("verified_access + P1b landed + andrew -> MASTER_ADMIN",
     resolve_tier("andrew@opalinvest.com", _Cfg(provider="verified_access", va_verified=True)), Tier.MASTER_ADMIN)

# --- ADD-1: exact-match only -- lookalikes must NOT become master-admin ---
case("alb_oidc + andrew@opalinvest.com.evil -> READ_ONLY (no substring match)",
     resolve_tier("andrew@opalinvest.com.evil", _Cfg(provider="alb_oidc")), Tier.READ_ONLY)
case("alb_oidc + andrew@opalinvest.co -> READ_ONLY (no prefix match)",
     resolve_tier("andrew@opalinvest.co", _Cfg(provider="alb_oidc")), Tier.READ_ONLY)
case("alb_oidc + evil+andrew@opalinvest.com -> READ_ONLY",
     resolve_tier("evil.andrew@opalinvest.com", _Cfg(provider="alb_oidc")), Tier.READ_ONLY)

# --- ADD-2: write is an EXPLICIT per-identity grant; unmatched verified -> READ_ONLY floor ---
case("alb_oidc + unknown verified employee -> READ_ONLY (least-priv default)",
     resolve_tier("newhire@opalinvest.com", _Cfg(provider="alb_oidc")), Tier.READ_ONLY)
case("alb_oidc + employee ON write-allowlist -> STANDARD_EMPLOYEE",
     resolve_tier("trader@opalinvest.com", _Cfg(provider="alb_oidc", write=("trader@opalinvest.com",))), Tier.STANDARD_EMPLOYEE)
case("alb_oidc + systems identity on master allowlist -> MASTER_ADMIN",
     resolve_tier("svc-ingest@opalinvest.com", _Cfg(provider="alb_oidc", master=("andrew@opalinvest.com", "svc-ingest@opalinvest.com"))), Tier.MASTER_ADMIN)

# --- case-insensitivity (identity.py lowercases; be robust) ---
case("alb_oidc + ANDREW@OPALINVEST.COM -> MASTER_ADMIN (case-insensitive exact)",
     resolve_tier("ANDREW@OPALINVEST.COM", _Cfg(provider="alb_oidc")), Tier.MASTER_ADMIN)

# --- ADD-3 boot-gate: prod must reject spoofable providers ---
case("boot-gate: header in prod -> error",
     bool(validate_identity_provider_for_prod(_Cfg(provider="header", env="prod"))), True)
case("boot-gate: alb_oidc in prod -> no error",
     validate_identity_provider_for_prod(_Cfg(provider="alb_oidc", env="prod")), [])
case("boot-gate: header in DEV -> no error (dev allowed)",
     validate_identity_provider_for_prod(_Cfg(provider="header", env="dev")), [])
case("boot-gate: cloudflare-unconfigured in prod -> error",
     bool(validate_identity_provider_for_prod(_Cfg(provider="cloudflare", env="prod"))), True)


fails = 0
for name, got, want in CASES:
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}: {name}  (got={got}, want={want})")
    if not ok:
        fails += 1

print(f"\n{len(CASES)-fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
