#!/usr/bin/env python
"""OG-hv-2 step 7: the SERVED read, exercised through the INSTALLED code on the gateway host.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python (bare python3 has no boto3).
It is uploaded to S3 and pulled by the host -- never inlined into an SSM command (cloud-ops Rule 12,
`docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md`).

WHAT IT PROVES, and why each arm is here:

  opal_packs_read            an Opal principal's `harvest_read` of one REAL packs/ object parses as
                             JSON. This is the only arm that proves the GRANT works: a simulate says
                             what IAM would decide, never what the assumed role actually gets back.
  non_opal_refused_packs     the same call under a non-Opal address is refused `harvest_opal_only`,
  non_opal_refused_wsj       on `packs/` AND on `wsj/harvest/` (the two prefixes the half names).
  off_prefix_refused         an Opal principal asking outside the 24 is refused
                             `harvest_prefix_not_served`.
  s3_calls_on_refusal        0, MEASURED: each refusal arm runs with `hv._client` replaced by a
                             counter that raises on any attribute access, so a single S3 call on a
                             refusal path would both count and fail loudly. Asserting the admission
                             "runs first" from reading the code is not the same claim.
  research_only_*            the SAME unprofiled standard-tier Opal principal that read packs/ is
                             refused a `schwab_*` tool and `blackdiamond_list_fees` by
                             `data_entitlement.tool_denial`, and is NOT refused the two harvest tools.
  tools_listed               both names are in the live registry the server itself builds -- not a
                             `grep -c '@mcp.tool'` over the tree, which counts decorators and reads
                             65 on the pre-release host.

NOTHING SENSITIVE IS PRINTED: no object content, no `.env` value, no person's address, no tenant or
object id. The probe principal is synthetic (`hv2.served.probe@<Opal domain>`), it is never written to
any store, and only booleans, refusal codes, counts and byte counts leave this process.

Usage (on the host): /opt/opal-gateway/.venv/bin/python /tmp/hv2_served_harness.py
Prints ONE json object to stdout, prefixed by the marker line HV2_SERVED_JSON.
"""
from __future__ import annotations

import json
import os
import sys
import traceback

ROOT = "/opt/opal-gateway"
PACKS_KEY = "packs/1299_HK_Equity/input_ledger.json"
WSJ_PREFIX = "wsj/harvest/"
OFF_KEY = "zzz-not-served/x.json"
PROBE_LOCAL = "hv2.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a02"   # synthetic, never written to any store


class _RefusalGuard:
    """Stands in for the S3 client on a refusal arm: any attribute touched is a counted FAILURE."""

    def __init__(self) -> None:
        self.calls = 0
        self.names: list = []

    def __getattr__(self, name: str):
        self.calls += 1
        self.names.append(name)

        def _boom(*a, **k):
            raise RuntimeError("S3 touched on a refusal path: %s" % name)

        return _boom


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out: dict = {"schema": "HV2_SERVED.v1", "body": {}}
    body = out["body"]

    from app import context, harvest_read as hv, identity_scope, tools  # noqa: E402
    from app import data_entitlement as de                              # noqa: E402
    import app.access_state as acs                                      # noqa: E402

    opal_email = "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN)
    non_opal_email = "%s@example.invalid" % PROBE_LOCAL
    tid = context.MOCK_TENANT_ID          # synthetic: the probe is unprofiled BY CONSTRUCTION
    probe = context.make_principal(tid, PROBE_OID, opal_email)
    non_opal = context.make_principal(tid, PROBE_OID, non_opal_email)

    def be(principal) -> None:
        # ONLY set_current_principal. `set_current_email` is the GUI-path setter and its FIRST act is
        # `_current_principal.set(None)` (context.py:105-109), so calling both leaves no principal and
        # every arm returns `principal_required` -- measured, first run of this harness.
        context.set_current_principal(principal)

    # ---- tools_listed: the live registry, not a decorator census -------------------------------
    names, how = [], "none"
    try:
        names = [t.name for t in tools.mcp._tool_manager.list_tools()]
        how = "mcp._tool_manager.list_tools()"
    except Exception:
        try:
            import asyncio
            names = [t.name for t in asyncio.run(tools.mcp.list_tools())]
            how = "asyncio.run(mcp.list_tools()) -- the policy-guarded view"
        except Exception as exc:
            how = "UNREADABLE: %s" % exc
    body["tools_listed"] = sorted(n for n in names if n in ("harvest_list", "harvest_read"))
    body["tools_listed_both"] = body["tools_listed"] == ["harvest_list", "harvest_read"]
    body["registry_total_native"] = len(names)
    body["registry_total_note"] = ("this is the NATIVE registry (app/tools.py decorators, 44 at the base); "
                                   "the 63 -> 65 figure is the composite native + per-integration count that "
                                   "tests/test_entitlement_admin.py::test_ogz2_ac08 asserts, and that test passes at the release")
    body["registry_instrument"] = how

    # ---- the real read, as an Opal principal, through the REAL client ---------------------------
    be(probe)
    try:
        res = hv.harvest_read(PACKS_KEY)
        err = isinstance(res, dict) and ("error" in res or res.get("guard_denied"))
        payload = json.dumps(res, default=str).encode("utf-8")
        body["opal_packs_read"] = bool(isinstance(res, dict) and not err)
        body["opal_packs_read_bytes"] = len(payload)
        body["opal_packs_read_code"] = (res or {}).get("code") if err else None
        body["opal_packs_read_keys"] = sorted(res)[:8] if isinstance(res, dict) else None
    except Exception as exc:
        body["opal_packs_read"] = False
        body["opal_packs_read_error"] = "%s: %s" % (type(exc).__name__, exc)

    # ---- the refusal arms, each with the S3 client replaced by the counter ----------------------
    real_client = hv._client
    guard = _RefusalGuard()
    hv._client = lambda: guard
    try:
        be(non_opal)
        r1 = hv.harvest_list("packs/")
        r2 = hv.harvest_list(WSJ_PREFIX)
        body["non_opal_refused_packs"] = (r1 or {}).get("code")
        body["non_opal_refused_wsj"] = (r2 or {}).get("code")
        body["non_opal_guard_denied"] = bool((r1 or {}).get("guard_denied")) and bool((r2 or {}).get("guard_denied"))
        be(probe)
        r3 = hv.harvest_read(OFF_KEY)
        body["off_prefix_refused"] = (r3 or {}).get("code")
    except Exception as exc:
        body["refusal_arm_error"] = "%s: %s" % (type(exc).__name__, exc)
    finally:
        hv._client = real_client
    body["s3_calls_on_refusal"] = guard.calls
    body["s3_attrs_touched_on_refusal"] = guard.names

    # ---- the research-only arm: the SAME principal, the entitlement guard's own verdict ---------
    be(probe)
    try:
        store = acs.AccessState()
        acc = de.current_access(probe, store)
        body["probe_restricted"] = bool(getattr(acc, "restricted", False))
        schwab = [t for t in sorted(de.DATA_GRANT_TOOLS) if t.startswith("schwab")] if hasattr(de, "DATA_GRANT_TOOLS") else []
        one_schwab = schwab[0] if schwab else "schwab_query"
        d_s = de.tool_denial(one_schwab, probe, store)
        d_b = de.tool_denial("blackdiamond_list_fees", probe, store)
        body["research_only_schwab_refused"] = (d_s or {}).get("code")
        body["research_only_schwab_tool"] = one_schwab
        body["research_only_bd_refused"] = (d_b or {}).get("code")
        body["harvest_tools_not_denied"] = all(
            de.tool_denial(t, probe, store) is None for t in ("harvest_list", "harvest_read"))
    except Exception as exc:
        body["research_only_error"] = "%s: %s" % (type(exc).__name__, exc)

    body["verdict"] = "PASS" if (
        body.get("tools_listed_both")
        and body.get("opal_packs_read")
        and body.get("non_opal_refused_packs") == "harvest_opal_only"
        and body.get("non_opal_refused_wsj") == "harvest_opal_only"
        and body.get("off_prefix_refused") == "harvest_prefix_not_served"
        and body.get("s3_calls_on_refusal") == 0
        and body.get("research_only_schwab_refused") == "entitlement_denied"
        and body.get("research_only_bd_refused") == "entitlement_denied"
        and body.get("harvest_tools_not_denied")
    ) else "FAIL"

    print("HV2_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("HV2_SERVED_JSON")
        print(json.dumps({"schema": "HV2_SERVED.v1", "body": {"verdict": "FAIL",
                                                              "fatal": traceback.format_exc()[-1500:]}}, indent=1))
        sys.exit(1)
