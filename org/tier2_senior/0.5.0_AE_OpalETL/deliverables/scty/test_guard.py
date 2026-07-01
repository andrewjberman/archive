"""Wiring-tests for guard.enforce -- the CTO Q3 fail-closed requirements (i)+(ii) + SAFE bypass.
Standalone: `python test_guard.py` -> exit 0 all-pass. CVO does the LIVE cert on the gateway."""
from __future__ import annotations

import sys

from guard import GuardDenied, enforce, resolve_and_enforce
from tier import Tier

CASES = []
def ok(n, cond): CASES.append((n, bool(cond)))


def _denied(tool, email, tier, code=None):
    try:
        enforce(tool, email, tier)
        return False
    except GuardDenied as gd:
        return code is None or gd.code == code


def _allowed(tool, email, tier):
    try:
        enforce(tool, email, tier)
        return True
    except GuardDenied:
        return False


# --- SAFE reads bypass regardless of tier (incl READ_ONLY) ---
ok("SAFE read bypasses (READ_ONLY tier)", _allowed("read_email", "x@opalinvest.com", Tier.READ_ONLY))
ok("SAFE read bypasses (no email)", _allowed("list_onedrive", "", Tier.READ_ONLY))

# --- CTO Q3(ii): READ_ONLY tier + mutating tool -> DENY ---
ok("READ_ONLY + send_email -> DENY", _denied("send_email", "x@opalinvest.com", Tier.READ_ONLY, "read_only_denied"))
ok("READ_ONLY + send_channel_message -> DENY", _denied("send_channel_message", "x@opalinvest.com", Tier.READ_ONLY, "read_only_denied"))
ok("READ_ONLY + unknown/future delete tool -> DENY (fail-closed)", _denied("delete_item", "x@opalinvest.com", Tier.READ_ONLY, "read_only_denied"))

# --- CTO Q3(i): mutating call with NO verified identity -> DENY ---
ok("no-identity + send_email -> DENY", _denied("send_email", "", Tier.STANDARD_EMPLOYEE, "identity_required"))
ok("no-identity + unknown tool -> DENY (fail-closed)", _denied("delete_item", "", Tier.STANDARD_EMPLOYEE, "identity_required"))

# --- write-capable tiers pass THIS gate (G1/G3 layer next) ---
ok("STANDARD_EMPLOYEE + send_email -> allowed at G2", _allowed("send_email", "trader@opalinvest.com", Tier.STANDARD_EMPLOYEE))
ok("MASTER_ADMIN + send_email -> allowed at G2", _allowed("send_email", "andrew@opalinvest.com", Tier.MASTER_ADMIN))
ok("STANDARD_EMPLOYEE + create_draft (reversible) -> allowed", _allowed("create_draft", "trader@opalinvest.com", Tier.STANDARD_EMPLOYEE))

# --- unknown tool + write-capable tier: passes G2 (fail-closed only DENIES read-only/no-id;
#     a write-capable tier reaching an unclassified tool is allowed at THIS gate but the tool
#     is tagged irreversible so G3-confirm (next layer) will gate it) ---
ok("STANDARD + unknown tool -> allowed at G2 (G3 will confirm)", _allowed("delete_item", "trader@opalinvest.com", Tier.STANDARD_EMPLOYEE))


# --- resolve_and_enforce end-to-end via a fake cfg (verified provider) ---
class _Cfg:
    IDENTITY_PROVIDER = "alb_oidc"
    MASTER_ADMIN_EMAILS = ("andrew@opalinvest.com",)
    WRITE_CAPABLE_EMAILS = ()
    VA_SIGNATURE_VERIFIED = False
    CF_ACCESS_TEAM_DOMAIN = None
    CF_ACCESS_AUD = None
    ENV = "prod"

def _re_denied(tool, email, code):
    try:
        resolve_and_enforce(tool, email, _Cfg())
        return False
    except GuardDenied as gd:
        return gd.code == code

# andrew@ resolves MASTER_ADMIN under alb_oidc -> send allowed
try:
    t = resolve_and_enforce("send_email", "andrew@opalinvest.com", _Cfg())
    ok("resolve_and_enforce: andrew@ send_email -> MASTER_ADMIN allowed", t is Tier.MASTER_ADMIN)
except GuardDenied:
    ok("resolve_and_enforce: andrew@ send_email -> MASTER_ADMIN allowed", False)

# unknown employee resolves READ_ONLY (ADD-2 default) -> send DENIED
ok("resolve_and_enforce: unknown employee send_email -> READ_ONLY DENY",
   _re_denied("send_email", "newhire@opalinvest.com", "read_only_denied"))


fails = 0
for n, passed in CASES:
    print(f"{'PASS' if passed else 'FAIL'}: {n}")
    fails += 0 if passed else 1
print(f"\n{len(CASES)-fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
