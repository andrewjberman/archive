#!/usr/bin/env python3
"""Battery for IRPT_BCKEND.TO-IB-rtg-3, criterion R74-AC1.

THE CLAIM: `performance/tenants.py`'s `route_for` now resolves a `TenantRoute` for the SAME
opaque id space `_authz.enforce.Enforcer.resolve_now` binds `verified_request_firm_id` to (the
directory's OPAQUE firm id, `fir_...`, minted by the estate's ONE normalizer `_ids.opaque_firm`)
-- for EACH of the registry's enabled client firms -- with zero fourth-id-space literals
introduced. Round 6 measured `route_for` raising `UnknownTenant` on exactly this id (FWD-2, row
IRPT_BCKEND-W2-S27); this battery re-derives the firm count LIVE (never inherits round 6's
number) and drives the REAL production modules (`_ids`, `_scope.resolve`,
`_authz.enforce.FirmBinding`, `performance.tenants`) rather than a copy of any of them.

Run: py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rtg_3.py
"""
from __future__ import annotations

import os
import sys


def _find_repo_root(start):
    d = os.path.abspath(start)
    for _ in range(15):
        if os.path.isdir(os.path.join(d, "org")) and os.path.isdir(os.path.join(d, ".tools")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise RuntimeError("repo root not found walking up from %r" % start)
        d = parent
    raise RuntimeError("repo root not found within 15 levels of %r" % start)


REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
IRPT_ROOT = os.path.join(REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
PERF_DIR = os.path.join(IRPT_ROOT, "performance")
IDS_DIR = os.path.join(IRPT_ROOT, "_ids")
SCOPE_DIR = os.path.join(IRPT_ROOT, "_scope")
AUTHZ_DIR = os.path.join(IRPT_ROOT, "_authz")
REGISTRY_PATH = os.path.join(REPO_ROOT, "data", "firm_registry.json")

for _p in (PERF_DIR, IDS_DIR, SCOPE_DIR, AUTHZ_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import tenants               # noqa: E402  the cell under test (IB-rtg-3)
import ids as _ids           # noqa: E402  the ONE opaque-id normalizer (IB-rt-3)
import resolve as _scope     # noqa: E402  IB-s-2, the real scope resolver
import enforce as _enforce   # noqa: E402  IB-s-3, the real FirmBinding/Enforcer wrapper

FAILURES = []


def check(cond, msg):
    print(("OK: " if cond else "FAIL: ") + msg)
    if not cond:
        FAILURES.append(msg)


print("=== IRPT_BCKEND.TO-IB-rtg-3 / R74-AC1 battery ===")
print("REPO_ROOT=%s" % REPO_ROOT)
print("registry_path=%s" % REGISTRY_PATH)

# ---- arm (a): re-derive the enabled client firm count LIVE, never inherited from round 6. ----
firm_ids = _ids.firm_ids(REGISTRY_PATH)
print("MEASURED live enabled client firm count: %d -> %s" % (len(firm_ids), firm_ids))
check(len(firm_ids) == 3, "registry declares exactly 3 enabled client firms (measured live, "
                          "not inherited)")

# ---- the mutant: the RETIRED third spelling must no longer resolve a route. -------------------
# Confirms `ROUTES` genuinely moved off `F-49F`/`F-COT`/`F-INF` rather than merely gaining a
# second, coincidentally-also-working key.
for retired in ("F-49F", "F-COT", "F-INF", "F-NOT-A-FIRM"):
    try:
        tenants.route_for(retired)
        check(False, "retired/unknown token %r unexpectedly still resolves a route" % retired)
    except tenants.UnknownTenant:
        print("OK: token %r correctly refused (UnknownTenant)" % retired)

# ---- for EACH registry firm: reproduce the REAL boundary's id join, end to end. ----------------
# `_authz.enforce.Enforcer.resolve_now` (served path, `served.py:enforcer_for` -> `resolve_now`)
# overwrites headers["x-firm-id"] with `FirmBinding.opaque_firm_id` -- the directory artifact's
# OWN declared opaque id -- BEFORE `_scope.resolve` ever runs. `handler.run` then reads
# `scope["verified_request_firm_id"]` (handler.py:79) and hands it straight to
# `tenants.route_for` (handler.py:80). This loop drives exactly that chain, with a minimal
# directory artifact this firm's own binding proves against (comp-iam DECLARED-NOT-APPLICABLE:
# no live S3/directory grant is read here, per this order's preflight).
resolved_firm_names = []
for firm_id in firm_ids:
    opaque = _ids.opaque_firm(firm_id, registry_path=REGISTRY_PATH)
    print("firm_id=%s -> opaque=%s (via _ids.opaque_firm, the ONE normalizer)" % (firm_id, opaque))

    directory = {"firm_id_opaque": opaque, "entries": [], "as_of_business_date": "2026-09-19"}
    binding = _enforce.FirmBinding(firm_id, opaque)
    check(binding.proves(directory),
          "FirmBinding(%s) proves against its own declared directory artifact" % firm_id)

    # An AUTHORIZED, scope-resolved request: the trusted nine as the edge validator would leave
    # them for a verified firm-operations admin (index.mjs's own injected set, `_scope.resolve`
    # module docstring TRUSTED_HEADERS).
    headers = {
        "x-origin-verify": "cloudfront",
        "x-user-email": "battery@example.invalid",
        "x-user-role": "admin",
        "x-firm-id": opaque,
    }
    scope = _scope.resolve(headers, directory, ownership=None,
                           id_projection=None)
    verified = scope["verified_request_firm_id"]
    check(verified == opaque,
          "resolve() carries the OPAQUE id as verified_request_firm_id for %s" % firm_id)
    check(scope["principal_class"] == "FIRM_OPERATIONS",
          "principal resolves FIRM_OPERATIONS (authorized, not UNKNOWN) for %s: got %s"
          % (firm_id, scope["principal_class"]))

    # THE ACT UNDER TEST: handler.py:79-80's exact line, `route_for(verified_request_firm_id)`.
    try:
        route = tenants.route_for(verified)
        check(isinstance(route, tenants.TenantRoute),
              "route_for(%s) resolves a TenantRoute for %s (no DEPENDENCY_UNAVAILABLE)"
              % (verified, firm_id))
        print("  -> firm_name=%s provider=%s host=%s" % (route.firm_name, route.provider,
                                                          route.host))
        resolved_firm_names.append(route.firm_name)
    except tenants.UnknownTenant as exc:
        check(False, "route_for RAISED UnknownTenant for %s (%s) -- FWD-2 NOT fixed: %s"
              % (firm_id, verified, exc))

check(len(resolved_firm_names) == 3,
      "all 3 registry firms resolved a TenantRoute: %s" % resolved_firm_names)

# ---- 0 fourth-id-space literals: every ROUTES key is an ISSUED firm id, never a hand-typed one.
bad_keys = [k for k in tenants.ROUTES if not _ids.is_issued("firm", k)]
check(not bad_keys,
      "every tenants.ROUTES key is an ISSUED firm id (fir_ + 24 hex, _ids.is_issued); bad=%s"
      % bad_keys)
print("tenants.ROUTES keys (denominator=%d): %s" % (len(tenants.ROUTES), sorted(tenants.ROUTES)))

print("")
if FAILURES:
    print("FAILED: %d of %d check(s) did not pass: %s"
          % (len(FAILURES), len(FAILURES) + 1, FAILURES))
    sys.exit(1)

print("PASS: IBR74-PERFORMANCE-ROUTE-RESOLVES-EACH-FIRM")
sys.exit(0)
