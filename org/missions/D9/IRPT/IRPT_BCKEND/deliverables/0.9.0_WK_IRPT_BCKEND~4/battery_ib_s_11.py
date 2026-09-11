"""IB-s-11 battery -- criterion S11-AC1.

Seven arms, (a) through (g), each printing the numbers it decided on and its denominator.
Everything but arm (g)'s two named AWS control-plane reads runs OFFLINE, under a socket
guard that REFUSES and RECORDS any outbound connection and is itself proven live by a
positive control.

Run:
    timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_s_11.py

Prints IBS11-PERFORMANCE-NORMALIZED on the last line if and only if every mechanical arm
passed. Any arm failing prints IBS11-ARM-FAILED and exits 1.
"""
from __future__ import annotations

import json
import pathlib
import socket
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "performance"
EVIDENCE_PATH = REPO / "docs" / "briefs" / "sources" / "INVESTOR_REPORTING_PERFORMANCE_EVIDENCE_20260910.json"
sys.path.insert(0, str(PACKAGE))

import bd_adapter  # noqa: E402
import handler  # noqa: E402
import normalize  # noqa: E402
import orion_adapter  # noqa: E402
import tenants  # noqa: E402
import transport as transport_mod  # noqa: E402
import units  # noqa: E402

VENDOR_HOSTS = ("bd3.bdreporting.com", "api.cloud.orionadvisor.com")
FUNCTION = "irpt-performance-adapter"
BUILT_ZIP_SHA256 = "Tl+NwcWAWl46YWeCrHShPpjoX5RgGUWm2UVQPLRJdFM="
LEDGER_SLUG = "irpt-bckend-s11"

RESULTS = []


def arm(name, passed, detail=""):
    RESULTS.append((name, bool(passed), detail))
    print("  %-6s %s%s" % ("PASS:" if passed else "FAIL:", name, ("  -- " + detail) if detail else ""))
    return passed


def head(text):
    print("")
    print("=" * 78)
    print(text)
    print("=" * 78)


# ---------------------------------------------------------------------------
# THE SOCKET GUARD. Installed before any adapter work; a positive control proves
# it fires, so a zero at the end is a MEASURED zero and not a dead instrument.
# ---------------------------------------------------------------------------
ATTEMPTS = []
_real_connect = socket.socket.connect
_real_connect_ex = socket.socket.connect_ex


class OutboundRefused(RuntimeError):
    pass


def _guard(self, address, *rest):
    ATTEMPTS.append(address)
    raise OutboundRefused("BLOCKED: outbound connection to %r refused by the IB-s-11 battery" % (address,))


def install_guard():
    socket.socket.connect = _guard
    socket.socket.connect_ex = _guard


def remove_guard():
    socket.socket.connect = _real_connect
    socket.socket.connect_ex = _real_connect_ex


def scope_for(firm_id, accounts, kind="ACCOUNT"):
    base = json.loads((PACKAGE.parent / "_contracts" / "fixtures" / "ResolvedScope.valid.json")
                      .read_text(encoding="utf-8"))["instance"]
    base["verified_request_firm_id"] = firm_id
    base["permitted_account_set"] = list(accounts)
    base["resolved_scope"] = {"scope_kind": kind, "scope_ids": list(accounts)}
    base["partial_reason"] = None
    return base


def main():
    install_guard()
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    receipts = {r["label"]: r for r in evidence["http_receipts"]}
    recorded = transport_mod.RecordedTransport(PACKAGE / "fixtures")

    print("IB-s-11 BATTERY -- performance adapters + normalizer")
    print("  package     : %s" % PACKAGE)
    print("  evidence    : %s" % EVIDENCE_PATH.relative_to(REPO))
    print("  transport   : %s (no credential, no host, no socket)" % recorded.kind)

    # ---------------------------------------------------------------- (a)
    head("(a) THREE TENANTS, THREE ROUTES")
    separation = tenants.separation_report()
    for firm_id in sorted(tenants.ROUTES):
        route = tenants.route_for(firm_id)
        print("  %-6s -> %-14s host=%-28s credential=%-28s plane=%s"
              % (firm_id, route.provider, route.host, route.session_secret_id,
                 route.data_plane_bucket + "/" + route.data_plane_prefix))
    for pair in separation["pairs"]:
        print("  pair %-14s same_host=%-5s same_credential=%-5s same_data_plane=%-5s SEPARATED=%s"
              % ("%s|%s" % pair["pair"], pair["same_host"], pair["same_credential"],
                 pair["same_data_plane"], pair["separated"]))
    bd49f, bdcot, inf = (tenants.route_for(f) for f in ("F-49F", "F-COT", "F-INF"))
    a_ok = (bd49f.provider == bdcot.provider == tenants.BLACK_DIAMOND
            and inf.provider == tenants.ORION
            and bd49f.host == bdcot.host
            and bd49f.route_key() != bdcot.route_key()
            and separation["all_separated"])
    try:
        tenants.route_for("F-NOT-A-FIRM")
        a_refuses = False
    except tenants.UnknownTenant:
        a_refuses = True
    arm("(a) 49F and COT are DIFFERENT BD routes on the SAME host; INF is Orion",
        a_ok and a_refuses,
        "%d of %d firm pairs separated; an unknown firm is refused, not defaulted"
        % (sum(p["separated"] for p in separation["pairs"]), separation["denominator"]))

    # ---------------------------------------------------------------- (b)
    head("(b) THE CAPTURED EVIDENCE REPLAYS -- 9 of 9 accounted")
    bd_scope = scope_for("F-49F", ["900000001"])
    inf_scope = scope_for("F-INF", ["900000002", "900000003"], kind="ACCOUNT")
    inf_scope["requested_scope"] = {"scope_kind": "RELATIONSHIP", "scope_ids": ["900000001"]}

    bd_out = handler.run(bd_scope, "2026-06-10", "2026-09-09", transport=recorded)
    inf_out = handler.run(inf_scope, "2026-06-10", "2026-09-09", transport=recorded)
    stale_out = handler.run(bd_scope, "2026-06-10", "2026-09-09", transport=recorded,
                            labels=handler.STALE_SESSION_LABELS)
    scope_out = handler.run(inf_scope, "2026-06-10", "2026-09-09", transport=recorded,
                            labels={"scope": "orion_252"})

    reports = {"F-49F (bd_refreshed_period + bd_refreshed_series)": bd_out,
               "F-INF (orion_daily)": inf_out,
               "F-INF (orion_252, the captured scope)": scope_out}
    validated = 0
    for name, out in reports.items():
        if out["report"] is not None:
            errors = normalize.report_errors(out["report"])
            ok = not errors
            validated += ok
            print("  REPORT   %-42s validates=%-5s errors=%d  series=%d  accounts=%d"
                  % (name, ok, len(errors),
                     len(out["report"]["returns"]["daily_cumulative_series"]),
                     len(out["report"]["returns"]["account_detail"])))
        else:
            print("  ABSENT   %-42s %s" % (name, out["absences"][0]["reason"][:60]))

    disposition = {}
    for label, receipt in receipts.items():
        if receipt["status"] == 401:
            disposition[label] = "ABSENT-WITH-REASON (HTTP 401, 0-byte body)"
        elif label == "bd_session_refresh":
            disposition[label] = ("NO BODY BY DESIGN (the probe never saves or digests a "
                                  "session-token response) -- accounted, not replayed")
        elif label == "orion_compact":
            disposition[label] = ("NOT COMMITTED (5,290,686 bytes, cumulative=true); its "
                                  "4,278-point/92-date counts read from the evidence")
        elif label in ("bd_refreshed_period", "bd_refreshed_series"):
            disposition[label] = "PARSED into the F-49F PerformanceReport"
        elif label == "orion_daily":
            disposition[label] = "PARSED into the F-INF PerformanceReport"
        elif label == "orion_252":
            disposition[label] = "PARSED into the F-INF captured-scope PerformanceReport"
        elif label == "orion_value_check":
            disposition[label] = "PARSED as the vendor ending-value oracle for arm (e)"
    for label in receipts:
        print("  %-20s %-3d %s" % (label, receipts[label]["status"], disposition[label]))

    stale_reasons = [a["reason"] for a in stale_out["absences"]]
    b_401_ok = (stale_out["report"] is None
                and any("HTTP 401" in r for r in stale_reasons)
                and all(a["fact"] and a["reason"] for a in stale_out["absences"]))
    print("  401 ARM  report=%r  absences=%d  first reason: %s"
          % (stale_out["report"], len(stale_out["absences"]), stale_reasons[0][:90]))
    arm("(b) the capture replays; 401s are absent-with-reason, never a value",
        validated == 3 and b_401_ok and len(disposition) == len(receipts) == 9,
        "%d of %d receipts accounted; %d of 3 reports validate against the contract"
        % (len(disposition), len(receipts), validated))

    # ---------------------------------------------------------------- (c)
    head("(c) UNITS ARE MEANING -- THE DIFFERENCE CONTROL")
    inf_result = orion_adapter.adapt(recorded, inf, "orion_daily")
    checks = inf_result.coverage["series_checks"]
    daily_body = recorded.fetch("orion_daily").body
    first_point = next(iter(orion_adapter.walk_groups(daily_body)))[1]
    breakdown = [c for c in first_point["calculations"]
                 if c["$type"] == orion_adapter.BREAKDOWN][0]
    raw = breakdown["series"][0]
    blind = units.Quantity(raw["performance"], units.DECIMAL_FRACTION, "$.series[0]")
    aware = units.Quantity(raw["performance"], units.PERCENT, "$.series[0]").to(units.DECIMAL_FRACTION)
    print("  ONE POINT (%s): vendor value %.12f" % (raw["endDate"], raw["performance"]))
    print("    read as PERCENT  -> %.12f  (the truth; factor-1 = %.12f)"
          % (aware.value, raw["factor"] - 1.0))
    print("    read as DECIMAL  -> %.12f  (%.1fx off)"
          % (blind.value, abs(blind.value / aware.value)))
    print("    conversion recorded: %s" % json.dumps(aware.conversions[0]))
    c_ok = abs(abs(blind.value / aware.value) - 100.0) < 1e-9
    for check in checks:
        print("  GROUP %-46s points=%d" % (check["group_path"], check["point_count"]))
        print("    max |daily percent/100 - (factor-1)|  = %r" % check["percent_factor_max_error"])
        print("    linked factors (product - 1)          = %.15f" % check["linked_factors"])
        print("    vendor summary (calculated-performance)= %.15f" % check["summary"])
        print("    |linked - summary|                    = %r" % check["linked_minus_summary"])
        print("    UNIT-BLIND link (control, must fail)  = %.15f" % check["unit_blind_linked"])
        c_ok = (c_ok
                and check["percent_factor_max_error"] == 0.0
                and check["linked_minus_summary"] < 1e-12
                and abs(check["unit_blind_linked"] - check["linked_factors"]) > 1.0)
    declared = {r["report"]["measurement_basis"]["return_units"]
                for r in (bd_out, inf_out) if r["report"]}
    print("  DECLARED OUTPUT UNIT across both providers: %s" % sorted(declared))
    arm("(c) two source units normalize to ONE declared unit; the unit-blind build fails",
        c_ok and declared == {"DECIMAL_FRACTION"},
        "3 of 3 groups tie to the vendor summary below 1e-12; the unit-blind link is "
        "%.6f against %.6f" % (checks[0]["unit_blind_linked"], checks[0]["linked_factors"]))

    # ---------------------------------------------------------------- (d)
    head("(d) NO FABRICATED AGGREGATE")
    comparison = orion_adapter.relationship_vs_accounts(inf_result)
    print("  relationship = a household of %d accounts, the EXACT selected set"
          % comparison["account_count"])
    for value in comparison["account_values"]:
        print("    account return                 = %.12f" % value)
    print("    SUM of account returns         = %.12f  (delta %+.12f)"
          % (comparison["sum_of_accounts"], comparison["sum_minus_vendor"]))
    print("    MEAN of account returns        = %.12f  (delta %+.12f)"
          % (comparison["mean_of_accounts"], comparison["mean_minus_vendor"]))
    print("    VENDOR household calculation   = %.12f  <-- the report carries THIS"
          % comparison["vendor_calculation"])
    print("    carried = %s" % comparison["carried"])
    try:
        normalize.use_summed_aggregate(comparison["account_values"])
        d_raises = False
        refusal_text = "NOT RAISED"
    except normalize.RefusedAggregation as exc:
        d_raises = True
        refusal_text = str(exc)
    print("  a build that sums: %s" % refusal_text)
    d_ok = (d_raises
            and comparison["carried"] == "vendor_calculation"
            and comparison["sum_minus_vendor"] > 0.018
            and 0 < comparison["mean_minus_vendor"] < 1e-6
            and any(r["code"] == normalize.REFUSE_SUMMED_AGGREGATE for r in inf_result.refusals))
    arm("(d) the vendor's relationship calculation is carried; a summing build fails",
        d_ok,
        "the MEAN is wrong by %+.3e -- close enough to survive review, which is why it is "
        "refused rather than tolerated" % comparison["mean_minus_vendor"])

    # ---------------------------------------------------------------- (e)
    head("(e) HIERARCHY, IDENTITY, SHORTCUT")
    bd_body = recorded.fetch("bd_refreshed_period").body
    bd_result = normalize.AdapterResult("BLACK_DIAMOND", bd49f.describe(), "bd", "x")
    bd_adapter.parse_period(bd_body, [], result=bd_result)
    account = bd_body["levels"][0]
    account_twr = account["dateRangePoints"][0]["timeWeightedReturns"]["return"]
    segment_returns = [s["dateRangePoints"][0]["timeWeightedReturns"]["return"]
                       for s in account["levels"]]
    print("  HIERARCHY  available=%s chosen=%r not_summed=%s"
          % (bd_result.hierarchy["available"], bd_result.hierarchy["chosen"],
             bd_result.hierarchy["not_summed"]))
    print("             both carry the SAME Account node -- summing them would double count")
    print("  LEVELS     account TWR                 = %.9f" % account_twr)
    print("             sum of its %2d Segment TWRs  = %.9f  (%.1fx the account)"
          % (len(segment_returns), sum(segment_returns), sum(segment_returns) / account_twr))
    print("             children carried as identities, never summed: %d"
          % len(bd_result.nodes[0].children))
    print("             report account-level rows: %d (Segment rows are NOT account rows)"
          % len(bd_out["report"]["returns"]["account_detail"]))

    collisions = inf_result.identity_collisions()
    print("  IDENTITY   repeated calculation ids: %s"
          % {cid: len(ids) for cid, ids in collisions.items()})
    for identity in collisions["Period"]:
        print("             id='Period'  group_path=%-46s node_type=%s"
              % ("/".join(identity.group_path), identity.node_type))
    print("             distinct triples for id='Period': %d of %d"
          % (len({i.key() for i in collisions["Period"]}), len(collisions["Period"])))

    census = orion_adapter.value_shortcut_census(daily_body, recorded.fetch("orion_value_check").body)
    print("  SHORTCUT   candidate: %s -> %s" % (census["candidate"], census["status"]))
    for row in census["rows"]:
        print("             %-46s %s  startValue+valueChange=%10.2f  vendor=%10.2f  diff=%7.2f  %s"
              % (row["node"], row["date"], row["shortcut"], row["vendor_ending_value"],
                 row["difference"], "match" if row["matches"] else "MISMATCH"))
    print("             %d of %d cells match; max |difference| = $%.2f"
          % (census["matching_cells"], census["comparisons"], census["max_absolute_difference"]))
    e_ok = (bd_result.hierarchy["chosen"] == "levels"
            and bd_result.hierarchy["not_summed"] == ["combinedLevels"]
            and len(segment_returns) == 11
            and sum(segment_returns) > account_twr * 5
            and len(bd_result.nodes[0].children) == 11
            and len(collisions["Period"]) == 6
            and len({i.key() for i in collisions["Period"]}) == 6
            and census["comparisons"] == 9 and census["nonmatching_cells"] == 3
            and census["status"] == "rejected_mapping"
            and abs(census["max_absolute_difference"] - 210.68) < 0.01)
    arm("(e) one hierarchy, the identity triple, and the value shortcut refused",
        e_ok,
        "%d of %d shortcut cells disagree by up to $%.2f; id 'Period' collides %d ways and "
        "the triple separates all %d"
        % (census["nonmatching_cells"], census["comparisons"],
           census["max_absolute_difference"], len(collisions["Period"]),
           len({i.key() for i in collisions["Period"]})))

    # ---------------------------------------------------------------- (f)
    head("(f) ABSENT STAYS ABSENT")
    absent_by_provider = {"F-49F": bd_out["absences"], "F-INF": inf_out["absences"]}
    total_absences = 0
    for firm_id, absences in absent_by_provider.items():
        for a in absences:
            total_absences += 1
            print("  %-6s %-12s %-24s %s" % (firm_id, a["status"], a["fact"], a["reason"][:78]))
    inf_facts = {a["fact"] for a in inf_out["absences"]}
    required = {"annualization", "money_weighted_return", "benchmark", "fee_basis",
                "accrual_basis"}
    missing = required - inf_facts
    print("  census: %d absence rows across 2 providers; %d of %d required Orion facts "
          "carried as absences (missing: %s)"
          % (total_absences, len(required) - len(missing), len(required), sorted(missing) or "none"))
    print("  UNSUPPORTED vs PARTIAL: %s"
          % {s: sum(1 for aa in absent_by_provider.values() for a in aa if a["status"] == s)
             for s in (normalize.UNSUPPORTED, normalize.PARTIAL)})
    basis = inf_out["report"]["measurement_basis"]
    print("  the report's own basis fields say UNKNOWN rather than guessing: "
          "fee_basis=%s accrual_basis=%s annualization=%s"
          % (basis["fee_basis"], basis["accrual_basis"], basis["annualization"]))
    f_ok = (not missing
            and all(a["reason"] for aa in absent_by_provider.values() for a in aa)
            and basis["fee_basis"] == "UNKNOWN"
            and basis["annualization"] == "UNKNOWN"
            and any(a["fact"] == "money_weighted_return" for a in bd_out["absences"]))
    arm("(f) every unsupported fact is absent WITH a reason; none is zero-filled",
        f_ok, "%d absence rows, %d of %d required Orion facts present"
        % (total_absences, len(required) - len(missing), len(required)))

    # ---------------------------------------------------------------- (g)
    head("(g) NOTHING LEFT THE MACHINE; THE LEDGER CLOSED")
    # SNAPSHOT BEFORE THE CONTROL. The adapter-phase count is the claim; the control
    # fires afterwards and MUST move it, or the zero above is a dead instrument.
    adapter_attempts = list(ATTEMPTS)
    adapter_vendor = [a for a in adapter_attempts if any(h in str(a) for h in VENDOR_HOSTS)]
    print("  socket guard active for every arm above")
    print("  outbound attempts during arms (a)-(f) : %d" % len(adapter_attempts))
    print("  of which to a VENDOR host             : %d (denominator: %s)"
          % (len(adapter_vendor), ",".join(VENDOR_HOSTS)))
    try:
        transport_mod.LiveTransport("no-such-token")
        live_refused = False
    except transport_mod.VendorEgressRefused as exc:
        live_refused = True
        print("  LiveTransport construction            : REFUSED -- %s" % str(exc)[:96])

    # POSITIVE CONTROL -- the guard must be able to fire, or its zero means nothing.
    control_fired = False
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("bd3.bdreporting.com", 443))
    except OutboundRefused:
        control_fired = True
    control_vendor = [a for a in ATTEMPTS if any(h in str(a) for h in VENDOR_HOSTS)]
    print("  POSITIVE CONTROL (deliberate connect)  : guard fired=%s; vendor attempts moved "
          "%d -> %d, so the zero above is MEASURED, not a dead guard"
          % (control_fired, len(adapter_vendor), len(control_vendor)))
    remove_guard()

    # The `.tools/aws` shim is a POSIX script; native Windows CreateProcess cannot run it
    # (WinError 193). `aws.cmd` is its cmd-plane sibling and both ship together.
    aws_shim = REPO / ".tools" / ("aws.cmd" if sys.platform == "win32" else "aws")
    config = subprocess.run(
        [str(aws_shim), "lambda", "get-function-configuration",
         "--function-name", FUNCTION,
         "--query", "[CodeSha256,State,LastUpdateStatus,Runtime,Handler]",
         "--output", "text"],
        capture_output=True, text=True, timeout=120)
    fields = config.stdout.replace("\r", "").strip().split("\t")
    print("  AWS CONTROL PLANE (named, not vendor): lambda get-function-configuration %s" % FUNCTION)
    print("    CodeSha256        = %s" % (fields[0] if fields else "UNREAD"))
    print("    built zip sha256  = %s" % BUILT_ZIP_SHA256)
    print("    equal             = %s" % (bool(fields) and fields[0] == BUILT_ZIP_SHA256))
    print("    State/Update/Runtime/Handler = %s" % (" / ".join(fields[1:]) if len(fields) > 1 else "UNREAD"))

    ledger_commit = subprocess.run(
        ["git", "-C", str(REPO), "log", "-1", "--format=%H %s", "--",
         "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG],
        capture_output=True, text=True, timeout=60).stdout.strip()
    sentinel_present = (REPO / "org" / "critical_paths" / ".open_deploys"
                        / ("%s.json" % LEDGER_SLUG)).exists()
    entry = list((REPO / "org" / "critical_paths" / "change_management").glob("*%s*" % LEDGER_SLUG))
    entry_text = entry[0].read_text(encoding="utf-8") if entry else ""
    closed = "CLOSED" in entry_text or "closed" in entry_text.lower()
    print("  LEDGER    sentinel committed at        : %s" % (ledger_commit or "NOT FOUND"))
    print("            sentinel on disk now         : %s (removed by the close, as designed)"
          % sentinel_present)
    print("            entry                        : %s" % (entry[0].name if entry else "MISSING"))
    print("            entry reads CLOSED           : %s" % closed)

    g_ok = (len(adapter_attempts) == 0        # nothing at all left the adapters
            and len(adapter_vendor) == 0
            and len(control_vendor) == 1       # and only the control moved the counter
            and control_fired
            and live_refused
            and bool(fields) and fields[0] == BUILT_ZIP_SHA256
            and len(fields) > 2 and fields[1] == "Active"
            and bool(ledger_commit) and closed and not sentinel_present)
    arm("(g) 0 vendor connections from the adapters; CodeSha256 == the built zip; ledger closed",
        g_ok,
        "%d of %d vendor connections during arms (a)-(f); the positive control moved the "
        "counter to %d, so the guard is live; CodeSha256 %s the built zip"
        % (len(adapter_vendor), len(adapter_attempts), len(control_vendor),
           "EQUALS" if (fields and fields[0] == BUILT_ZIP_SHA256) else "DIFFERS FROM"))

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, _ in RESULTS:
        print("  %-5s %s" % ("PASS" if ok else "FAIL", name))
    print("")
    print("  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    if passed == len(RESULTS):
        print("IBS11-PERFORMANCE-NORMALIZED")
        return 0
    print("IBS11-ARM-FAILED")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        remove_guard()
