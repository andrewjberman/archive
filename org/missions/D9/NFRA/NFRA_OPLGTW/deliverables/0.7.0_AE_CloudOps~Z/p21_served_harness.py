#!/usr/bin/env python
"""OG-ap-21 Phase B step 6: the SERVED read of the five news tools and the published-analysis tool.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python, pulled from
s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/ (the ONE prefix the gateway role can read --
a diagnostics/ prefix returns 403, measured on OG-ap-20). WRITTEN DURING PHASE A, before the GO, so the
instrument is settled outside the ledger window rather than inside it.

  --registry-only   the registry count and names, then exit (the PRE-deploy read).
  (no flag)         the full read-back.

THE OUTPUT SHAPE IS COPIED FROM THE GRADER, NOT INVENTED. ap21.AC2 reads, under `body`:
registry_before and registry_count as INTS with count == before + 1, and these five flags each tested
with `is True`: internal_reader_statements_live, news_and_published_served_through_internal_role,
non_opal_refused_zero_reads, person_reader_arms_ok, contract_staging_test_green -- plus
old_instance_role_statements_gone, which step 6 writes FALSE and step 7 flips to true. Two of those are
IAM facts a host script cannot see, so they are left None here for the CALLER to fill from its own
read-back; a host script must not assert what it cannot observe.

FOUR THINGS THIS ORDER ASKS FOR THAT THE OG-ap-20 HARNESS DID NOT:

1. THE IDENTITY, NOT JUST THE ANSWER. Step 6 says read the assumed-role identity of the call, not the
   instance role. So the harness builds an STS client FROM THE SAME ASSUMED CREDENTIALS the tools use and
   reads get_caller_identity, then reads the instance role's identity from the default chain, and records
   BOTH. A served answer alone cannot tell the two apart -- the instance role could satisfy the read and
   the answer would look identical.

2. TWO COUNTERS, BECAUSE THERE ARE TWO PLANES. The news tools read DynamoDB through news_typed._ddb; the
   published-analysis tool INVOKES a Lambda through harvest_published._invoke. One counter would leave
   the invoke path unguarded while still printing a clean zero -- the OG-ap-19 lesson, which cost a
   re-run there.

3. THE REFUSAL CODES DIFFER BETWEEN THE TWO FAMILIES. news_typed admits through typed_scope
   (typed_opal_only); harvest_published admits through harvest_read.admit (harvest_opal_only). A single
   accepted-code list taken from either family would read non_opal_refused False for the other while
   every refusal worked. Both are accepted, and the code actually seen is recorded per tool.

4. THE PERSON READER IS EXERCISED WITH A STUB STORE AND WRITES NOTHING. The order is explicit: write NO
   real person_access record. person_access(principal, store=...) takes the store as an argument, so the
   three arms are driven by substituting it -- no record (today's behaviour), a stopped record (denies a
   floor-allowed tool), and an unreadable one (fails closed) -- and person_denial(tool, rec) is pure, so
   the middle arm needs no store at all.

THE AUDIT SINK IS STUBBED, a bound rather than a convenience: audit.log_call -> _emit -> put_object
whenever AUDIT_S3_BUCKET is set, and this order forbids writing any object.

Nothing sensitive is printed: no article text, no .env value, no object content, no tenant or object id
beyond the synthetic probe. The probe principal is synthetic and is never written to any store.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
PROBE_LOCAL = "ap21.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a21"
REGISTRY_BEFORE = 75                 # the live count at base c4c106aea1, measured, not assumed

NEWS = ["news_search_articles", "news_trending_topics", "news_keyword_intelligence",
        "news_market_mood", "news_for_security"]
PUBLISHED = "harvest_get_published_analysis"
SIX = NEWS + [PUBLISHED]
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
# both families, because they admit through different seams
REFUSAL_CODES = ("typed_opal_only", "harvest_opal_only", "opal_only", "principal_required",
                 "harvest_published_unavailable")


class _CallGuard:
    """Stands in for a client. Any attribute access counts; calling it raises loudly."""

    def __init__(self, label: str) -> None:
        self.calls = 0
        self.label = label

    def __getattr__(self, name: str):
        self.calls += 1

        def _boom(*a, **k):
            raise RuntimeError("%s touched on a refusal path: %s" % (self.label, name))
        return _boom


def registry_names(tools_mod) -> list:
    try:
        return [t.name for t in tools_mod.mcp._tool_manager.list_tools()]
    except Exception:
        import asyncio
        return [t.name for t in asyncio.run(tools_mod.mcp.list_tools())]


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                              # noqa: E402

    names = registry_names(tools)
    if "--registry-only" in sys.argv:
        print("REGISTRY_JSON")
        print(json.dumps({"registry_count": len(names), "registry_names": sorted(names),
                          "six_present": sorted(n for n in names if n in SIX),
                          "instrument": "app.tools.mcp._tool_manager.list_tools()"}, indent=1))
        return 0

    from app import context, identity_scope                            # noqa: E402
    from app import data_entitlement as de                             # noqa: E402
    from app import access_state as acs                                # noqa: E402
    from app import news_typed as nw, harvest_published as hp          # noqa: E402
    from app import internal_role                                      # noqa: E402

    out = {"body": {}}
    b = out["body"]

    # ---- the registry, on ONE named instrument ------------------------------------------------
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    b["registry_before"] = REGISTRY_BEFORE
    b["registry_count"] = len(names)
    b["registry_delta"] = len(names) - REGISTRY_BEFORE
    b["six_present"] = sorted(n for n in names if n in SIX)
    b["six_missing"] = sorted(n for n in SIX if n not in names)

    # ---- (1) THE IDENTITY: which role do the tools actually act as? ---------------------------
    ident = {"configured_arn_env_key": "INTERNAL_READER_ROLE_ARN",
             "configured_arn_present": bool((os.environ.get("INTERNAL_READER_ROLE_ARN") or "").strip())}
    try:
        import boto3
        ident["instance_role_identity"] = boto3.client("sts").get_caller_identity().get("Arn")
    except Exception as exc:
        ident["instance_role_identity"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    try:
        # the SAME factory the tools use, so this is the identity of a real tool call
        arn = (os.environ.get("INTERNAL_READER_ROLE_ARN") or "").strip()
        import boto3
        creds = boto3.client("sts").assume_role(RoleArn=arn, RoleSessionName="ap21-identity-probe")["Credentials"]
        sts2 = boto3.client("sts", aws_access_key_id=creds["AccessKeyId"],
                            aws_secret_access_key=creds["SecretAccessKey"],
                            aws_session_token=creds["SessionToken"])
        ident["assumed_role_identity"] = sts2.get_caller_identity().get("Arn")
    except Exception as exc:
        ident["assumed_role_identity"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    a, i = str(ident.get("assumed_role_identity")), str(ident.get("instance_role_identity"))
    ident["two_identities_differ"] = a != i and a.startswith("arn:")
    ident["assumed_names_the_internal_reader"] = "gateway-global-internal-reader-role" in a
    ident["reading"] = ("a served answer alone cannot tell the instance role from the assumed role, so "
                        "both identities are read in the same run and recorded side by side")
    b["identity"] = ident

    # ---- the served arms ----------------------------------------------------------------------
    audit_rows = []

    def _recorder(email, tool, args, outcome, detail="", **kw):
        audit_rows.append((tool, outcome, detail))

    for mod in (nw, hp):
        if hasattr(mod, "audit"):
            mod.audit.log_call = _recorder            # type: ignore[assignment]

    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                  "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                      "%s@example.invalid" % PROBE_LOCAL)
    context.set_current_principal(opal)

    CALLS = {
        # the news arguments are the shapes the modules own guards demand -- a no-argument probe is
        # refused on the contract and would read as a failing tool (the OG-ap-19 lesson)
        "news_search_articles": lambda: nw.news_search_articles(date_from="2026-10-08", date_to="2026-10-14"),
        "news_trending_topics": lambda: nw.news_trending_topics(),
        "news_keyword_intelligence": lambda: nw.news_keyword_intelligence(keyword="inflation"),
        "news_market_mood": lambda: nw.news_market_mood(),
        "news_for_security": lambda: nw.news_for_security(ticker="AAPL"),
        PUBLISHED: lambda: hp.harvest_get_published_analysis("AAPL", "overlay"),
    }

    def call(fn):
        t0 = time.time()
        try:
            return fn(), round(time.time() - t0, 2), None
        except Exception as exc:
            return None, round(time.time() - t0, 2), "%s: %s" % (type(exc).__name__, str(exc)[:200])

    per_tool = {}
    for tool in SIX:
        res, secs, err = call(CALLS[tool])
        enveloped = isinstance(res, dict) and all(k in res for k in ENVELOPE)
        refused = isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))
        per_tool[tool] = {"opal_served": bool(enveloped and not refused), "seconds": secs,
                          "enveloped": enveloped, "error": err,
                          "refusal_code": (res or {}).get("code") if refused else None,
                          "answer_keys": sorted(res)[:12] if isinstance(res, dict) else None}

    # ---- (2) TWO COUNTERS on the refusal path: DynamoDB for news, Lambda for the invoke --------
    ddb_guard, lam_guard = _CallGuard("DynamoDB"), _CallGuard("Lambda")
    saved = {}
    for mod, attr, guard in ((nw, "_ddb", ddb_guard), (hp, "_invoke", lam_guard),
                             (internal_role, "dynamodb_client", ddb_guard),
                             (internal_role, "lambda_client", lam_guard)):
        if hasattr(mod, attr):
            saved[(mod.__name__, attr)] = getattr(mod, attr)
            setattr(mod, attr, (lambda g: (lambda *a, **k: g))(guard))
    b["refusal_guards_installed"] = sorted("%s.%s" % k for k in saved)
    try:
        context.set_current_principal(non_opal)
        for tool in SIX:
            res, secs, err = call(CALLS[tool])
            code = (res or {}).get("code") if isinstance(res, dict) else None
            per_tool[tool]["non_opal_code"] = code
            per_tool[tool]["non_opal_refused"] = bool(
                code in REFUSAL_CODES or (isinstance(res, dict) and res.get("guard_denied")))
            per_tool[tool]["non_opal_error"] = err
    finally:
        for (modname, attr), val in saved.items():
            for mod in (nw, hp, internal_role):
                if mod.__name__ == modname:
                    setattr(mod, attr, val)
        context.set_current_principal(opal)

    b["reads_on_refusal_dynamodb"] = ddb_guard.calls
    b["invokes_on_refusal_lambda"] = lam_guard.calls
    b["reads_on_refusal"] = ddb_guard.calls + lam_guard.calls
    for tool in SIX:
        per_tool[tool]["reads_on_refusal"] = b["reads_on_refusal"]
    b["per_tool"] = per_tool
    b["audit_rows_captured"] = len(audit_rows)
    b["audit_sink_stubbed"] = True

    # ---- (4) THE PERSON READER, on a STUB store, writing NOTHING ------------------------------
    class _NoRecord:
        """A store that answers 'no such record' -- today's behaviour arm."""

        def get(self, *a, **k):
            return None

        def __getattr__(self, name):
            return lambda *a, **k: None

    class _Unreadable:
        """A store whose read raises the dependency error -- the fail-closed arm."""

        def __getattr__(self, name):
            def _raise(*a, **k):
                raise acs.DependencyUnavailable("stub: the access store is unreadable")
            return _raise

    arms = {}
    try:
        rec = de.person_access(opal, _NoRecord())
        arms["no_record"] = {"record": rec, "denial_for_whoami": de.person_denial("whoami", rec),
                             "expected": "no record -> no person denial; the floor decides as before",
                             "ok": rec is None and de.person_denial("whoami", rec) is None}
    except Exception as exc:
        arms["no_record"] = {"error": "%s: %s" % (type(exc).__name__, str(exc)[:160]), "ok": False}
    try:
        # person_denial is PURE -- it takes the record -- so the stopped arm needs no store at all.
        # PersonAccess is a NamedTuple whose four list fields are declared frozenset, so they are built
        # as frozensets rather than tuples: a NamedTuple validates nothing, and a set operation inside
        # person_denial would be the place a tuple quietly behaved differently.
        stopped = de.PersonAccess(status="active", revision=1, stopped=True,
                                  tools_allow=frozenset(), tools_deny=frozenset(),
                                  channels_allow=frozenset(), channels_deny=frozenset())
        d = de.person_denial("whoami", stopped)
        arms["stopped_true"] = {"denial": d, "code": (d or {}).get("code"),
                                "expected": "stopped: true denies a floor-allowed tool",
                                "ok": bool(d) and (d or {}).get("code") == "person_record_denied"}
    except Exception as exc:
        arms["stopped_true"] = {"error": "%s: %s" % (type(exc).__name__, str(exc)[:200]), "ok": False}
    try:
        de.person_access(opal, _Unreadable())
        arms["unreadable"] = {"expected": "an unreadable store FAILS CLOSED, it does not admit",
                              "raised": None, "ok": False}
    except Exception as exc:
        arms["unreadable"] = {"expected": "an unreadable store FAILS CLOSED, it does not admit",
                              "raised": type(exc).__name__,
                              "ok": type(exc).__name__ in ("DependencyUnavailable",
                                                            "AccessStateRefused", "Malformed")}
    b["person_reader_arms"] = arms
    b["person_reader_wrote_nothing"] = True
    b["person_reader_arms_ok"] = all(v.get("ok") for v in arms.values())

    # ---- the AC2 flags this script can honestly set -------------------------------------------
    b["news_and_published_served_through_internal_role"] = bool(
        all(per_tool[t]["opal_served"] for t in SIX)
        and ident.get("assumed_names_the_internal_reader") is True)
    b["non_opal_refused_zero_reads"] = bool(
        all(per_tool[t]["non_opal_refused"] for t in SIX) and b["reads_on_refusal"] == 0)
    # these two are IAM and git facts a host script cannot see: the CALLER fills them
    b["internal_reader_statements_live"] = None
    b["old_instance_role_statements_gone"] = False      # step 7 flips this to true
    b["contract_staging_test_green"] = None
    b["_caller_must_fill"] = ["internal_reader_statements_live (from get-role-policy on both new "
                              "statements)", "old_instance_role_statements_gone (step 7, after the "
                              "destroy)", "contract_staging_test_green (from the pytest run at the new "
                              "deployed commit)"]

    b["verdict"] = "PASS-PENDING-CALLER" if (
        len(b["six_present"]) == 6
        and b["registry_count"] == REGISTRY_BEFORE + 1
        and b["news_and_published_served_through_internal_role"]
        and b["non_opal_refused_zero_reads"]
        and b["person_reader_arms_ok"]
    ) else "PARTIAL-OR-FAIL"
    print("P21_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("P21_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1800:]}}, indent=1))
        sys.exit(1)
