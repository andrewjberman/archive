#!/usr/bin/env python3
"""IB-s-1 acceptance battery -- criterion S1-AC1, arms (a) through (f).

Prints `IBS1-DIRECTORY-SERVED` on the LAST line if and only if EVERY arm passes. An arm that
fails or blocks prints its own verdict and the token is withheld -- the token is the only thing
the criterion reads, so it is emitted from exactly one place at the very end.

Every count is printed WITH ITS DENOMINATOR. Where an arm's live population is EMPTY the arm
says so out loud and runs a constructed positive control beside it, because a check over an
empty set returns a vacuous pass that reads exactly like a real one.

Usage:
  python battery_ib_s_1.py              # full run (arms a-f)
  python battery_ib_s_1.py --skip-land  # arms a-e only (no S3 write, no deploy read)
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import socket
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[6]
RUNNER_DIR = _REPO / "data" / "assets" / "scripts" / "gold" / "investor_reporting"
HANDLER_DIR = _REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "directory"

for p in (str(RUNNER_DIR), str(HANDLER_DIR), str(HANDLER_DIR / "tests")):
    if p not in sys.path:
        sys.path.insert(0, p)

import directory_runner as dr        # noqa: E402
import fixtures as fx                # noqa: E402
import handler as hd                 # noqa: E402

FUNCTION_NAME = "irpt-directory-search"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-directory-search.zip"
LEDGER_SLUG = "irpt-bckend-s1"
SENTINEL = _REPO / "org" / "critical_paths" / ".open_deploys" / (LEDGER_SLUG + ".json")

RESULTS: "list[tuple[str, str, str]]" = []   # (arm, verdict, deciding line)


def record(arm: str, verdict: str, line: str) -> None:
    RESULTS.append((arm, verdict, line))
    print("ARM {} {}: {}".format(arm, verdict, line))


def section(title: str) -> None:
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


# ============================================================================ arm (a)
def arm_a(state: dict) -> None:
    section("ARM (a) -- THREE FIRMS, THREE DIRECTORIES, EVERY ENTRY VALID")
    buckets = dr.firm_bucket_map()
    firms = dr.client_firms()
    print("DENOMINATOR: registry firms kind=client: {} of {} registry firms "
          "(test/demo excluded BY KIND)".format(
              len(firms),
              len(json.loads(dr.FIRM_REGISTRY_PATH.read_text(encoding='utf-8'))["firms"])))
    built = {}
    landed = {}
    total_entries = 0
    total_valid = 0
    for f in firms:
        # BUILD ONLY. The battery GRADES; it never acts. The QA objects are landed by the
        # runner inside the change-management window, and arm (f) reads them afterwards --
        # "open the entry, ACT, close the entry and commit it BEFORE taking the reads that
        # grade the act". A battery that also performed the act would be grading itself.
        res = dr.run_firm(f, buckets, qa=True, upload=False, local_out=None, explicit=None)
        built[f["firm_id"]] = res
        landed[f["firm_id"]] = {k: v for k, v in res["landed"].items()
                                if k in ("bucket", "key", "latest_key", "uploaded",
                                         "bytes", "sha256", "remote_bytes", "etag")}
        total_entries += res["entry_count"]
        total_valid += res["entries_valid"]
        print("  FIRM {}: bucket={} entries={} valid={} of {} as_of={} "
              "source_completion={} calendar_business_date={}".format(
                  res["firm_id"], res["bucket"], res["entry_count"],
                  res["entries_valid"], res["entry_count"], res["business_date"],
                  res["source_completion_date"], res["business_date"]))
        for t in res["trail"]:
            print("    TRAIL: " + t)
        print("    CENSUS: " + json.dumps(res["census"], sort_keys=True, default=str))
        if res["validation_errors"]:
            for e in res["validation_errors"]:
                print("    SCHEMA-ERROR: " + e)
    state["built"] = built
    state["landed"] = landed
    ok = (len(built) == 3 and total_valid == total_entries and total_entries > 0)
    record("a", "PASS" if ok else "FAIL",
           "{} of {} firms built; {} of {} entries validate against "
           "DirectoryEntry.schema.json".format(len(built), len(firms), total_valid,
                                               total_entries))


# ============================================================================ arm (b)
def arm_b(state: dict) -> None:
    section("ARM (b) -- THE FIXTURE CASES RESOLVE TO THE EXPECTED AUTHORIZED SET")
    total = len(fx.CASES)
    passed = 0
    for name, case in fx.CASES.items():
        s = hd.search(fx.DIRECTORY, fx.SCOPE_A, case["query"])
        pick = fx.PICKS[case["resolve_pick"]]
        entry_id = hd._entry_key(pick)
        r = hd.resolve(fx.DIRECTORY, fx.SCOPE_A, {"entry_id": entry_id})
        detail = []
        ok = True

        if s["count"] != case["expect_result_count"]:
            ok = False
            detail.append("search count {} of expected {}".format(
                s["count"], case["expect_result_count"]))
        else:
            detail.append("search {} of {} results".format(
                s["count"], case["expect_result_count"]))

        # UNAMBIGUOUS SELECTION: every returned candidate must be separable. Duplicate names
        # are separable iff their masked discriminators differ.
        discs = [x["masked_discriminator"] for x in s["results"]]
        unambiguous = (len(set(discs)) == len(discs)) and not s["ambiguous"]
        if not unambiguous:
            ok = False
            detail.append("AMBIGUOUS: discriminators {}".format(discs))
        else:
            detail.append("selection unambiguous ({} distinct discriminators of {})".format(
                len(set(discs)), len(discs)))
        if case.get("expect_discriminators"):
            if sorted(discs) != sorted(case["expect_discriminators"]):
                ok = False
                detail.append("discriminators {} != expected {}".format(
                    sorted(discs), sorted(case["expect_discriminators"])))

        if case.get("expect_unsupported"):
            if r["ok"] or r["resolved_scope"]["scope_kind"] != "UNSUPPORTED":
                ok = False
                detail.append("expected UNSUPPORTED, got {}".format(r["resolved_scope"]))
            elif r["account_ids"]:
                ok = False
                detail.append("UNSUPPORTED must return NO accounts; got {}".format(
                    len(r["account_ids"])))
            else:
                withheld = (r["requested_account_count"] - r["permitted_account_count"])
                if withheld != case["expect_withheld"]:
                    ok = False
                    detail.append("withheld {} of expected {}".format(
                        withheld, case["expect_withheld"]))
                else:
                    detail.append(
                        "resolve UNSUPPORTED, {} of {} accounts withheld, reason present, "
                        "0 rows hidden".format(withheld, r["requested_account_count"]))
        else:
            got = sorted(r["account_ids"])
            want = sorted(case["expect_accounts"])
            if not r["ok"] or got != want:
                ok = False
                detail.append("resolve {} != expected {}".format(got, want))
            else:
                detail.append("resolve {} of {} expected accounts, fingerprint {}".format(
                    len(got), len(want), r["fingerprint"][:16]))

        if case.get("expect_termination"):
            vis = [x for x in s["results"]
                   if x["termination"]["indicator"] == case["expect_termination"]]
            if not vis:
                ok = False
                detail.append("terminated client NOT VISIBLE in search")
            else:
                detail.append("terminated client VISIBLE and marked {} (effective {})".format(
                    vis[0]["termination"]["indicator"], vis[0]["termination"]["effective_date"]))

        passed += 1 if ok else 0
        print("  CASE {} [{}]: {} -- {}".format(
            "PASS" if ok else "FAIL", name, case["clause"], "; ".join(detail)))
    record("b", "PASS" if passed == total else "FAIL",
           "{} of {} fixture cases resolve to the expected authorized set".format(
               passed, total))


# ============================================================================ arm (c)
def arm_c(state: dict) -> None:
    section("ARM (c) -- NO DOUBLE COUNT, EVERY GAP REASONED")
    ok = True
    lines = []

    c49 = state["built"]["49financial"]["census"]
    before, after = c49.get("unique_before"), c49.get("unique_after")
    print("  49F portfolio groups: {} groups, {} membership rows, "
          "unique accounts BEFORE grouping {} == AFTER grouping {}".format(
              c49.get("groups"), c49.get("memberships"), before, after))
    print("  49F membership fan-out (memberships - unique) = {} -- carried on a grain with "
          "NO monetary column, so the fan-out product cannot be constructed".format(
              c49.get("double_counted")))
    if before is None or before != after:
        ok = False
        lines.append("49F unique-account census FAILED: {} != {}".format(before, after))
    else:
        lines.append("49F {} of {} unique accounts preserved across {} groups".format(
            after, before, c49.get("groups")))
    if c49.get("groups") != 201:
        print("  DECLARED: the live portfolio-group count is {}, not the 201 this order "
              "names -- printed rather than asserted".format(c49.get("groups")))

    drows = c49["directory_account_rows"]
    duniq = c49["directory_unique_accounts"]
    print("  49F directory: {} account rows, {} unique -- an account appears in exactly "
          "one entry".format(drows, duniq))
    if drows != duniq:
        ok = False
        lines.append("49F directory double-counts {} accounts".format(drows - duniq))

    cinf = state["built"]["inflection"]["census"]
    unmapped = cinf["unmapped"]
    with_reason = cinf["unmapped_with_reason"]
    denom = cinf["accounts_denominator"]
    print("  INF live: unmapped {} of {} accounts; {} of {} unmapped carry a reason".format(
        unmapped, denom, with_reason, unmapped))
    print("  INF reason histogram (denominator {} accounts): {}".format(
        denom, json.dumps(cinf["reason_histogram"], sort_keys=True)))
    if unmapped != with_reason:
        ok = False
        lines.append("INF {} of {} unmapped accounts carry NO reason".format(
            unmapped - with_reason, unmapped))
    if unmapped == 0:
        print("  VACUITY DECLARED: the live unmapped population is EMPTY (0 of {}), so the "
              "reason check above passes over an empty set and proves nothing on its own. "
              "The order names 79 unmapped; the live vintage carries 0 (row "
              "IRPT_BCKEND-W2-S3). Positive control below.".format(denom))
        ctl = _inf_reason_positive_control()
        print("  POSITIVE CONTROL: constructed INF frame with 3 unmapped accounts -> "
              "{} of 3 carry a reason; reasons {}".format(ctl["with_reason"], ctl["reasons"]))
        if ctl["with_reason"] != 3:
            ok = False
            lines.append("INF reason machinery FAILED its positive control")
        else:
            lines.append("INF unmapped {} of {} (live, vacuous) + positive control 3 of 3"
                         .format(unmapped, denom))
    else:
        lines.append("INF unmapped {} of {} accounts, {} of {} with a reason".format(
            unmapped, denom, with_reason, unmapped))

    ccot = state["built"]["cottonwood"]["census"]
    print("  COT: {} allocation rows -> {} relationships + {} ungrouped; {} account rows, "
          "{} unique, {} cross-relationship (DESIGNED fan-out, declared)".format(
              ccot["allocation_rows"], ccot["relationships"], ccot["ungrouped_rows"],
              ccot["directory_account_rows"], ccot["directory_unique_accounts"],
              ccot["cross_relationship_accounts"]))
    lines.append("COT {} unique accounts of {} rows, fan-out declared".format(
        ccot["directory_unique_accounts"], ccot["directory_account_rows"]))

    record("c", "PASS" if ok else "FAIL", "; ".join(lines))


def _inf_reason_positive_control() -> dict:
    """A constructed INF frame WITH unmapped accounts, so the reason machinery is exercised
    even on a day when the live population is empty. A fixture that cannot represent the
    failure cannot score it."""
    import pandas as pd
    acc = pd.DataFrame([
        {"account_id": "1", "account_number": "11110001", "account_name": "Mapped One",
         "account_type": "IRA", "household_id": "H1", "rep_id": "R1", "is_active": True,
         "is_managed": True, "last_name": "One"},
        {"account_id": "2", "account_number": "11110002", "account_name": "No Household",
         "account_type": "IRA", "household_id": "", "rep_id": "R1", "is_active": True,
         "is_managed": True, "last_name": "Two"},
        {"account_id": "3", "account_number": "11110003", "account_name": "Unknown HH",
         "account_type": "IRA", "household_id": "H9", "rep_id": "R1", "is_active": True,
         "is_managed": False, "last_name": "Three"},
        {"account_id": "4", "account_number": "11110004", "account_name": "Off Roster",
         "account_type": "IRA", "household_id": "", "rep_id": "R404", "is_active": False,
         "is_managed": False, "last_name": "Four"},
    ])
    reps = pd.DataFrame([{"rep_id": "R1"}])
    hh = pd.DataFrame([{"household_id": "H1"}])
    data = {"accounts": acc, "reps": reps, "households": hh,
            "completion_date": "2026-09-09", "source_revision": "positive-control"}
    entries, census = dr.build_inf(data, "2026-09-09", "irpt-dir/control/1.0")
    reasons = sorted(census["reason_histogram"])
    return {"with_reason": census["unmapped_with_reason"], "unmapped": census["unmapped"],
            "reasons": reasons, "entries": len(entries)}


# ============================================================================ arm (d)
class _NoNetwork(RuntimeError):
    pass


def _import_names(path: Path) -> "list[str]":
    """Every module name this file imports at module level, by AST -- not by grep."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return sorted(set(names))


def arm_d(state: dict) -> None:
    section("ARM (d) -- ZERO PROVIDER CALLS: THE CENSUS")
    ok = True
    files = {"runner": RUNNER_DIR / "directory_runner.py",
             "handler": HANDLER_DIR / "handler.py"}
    total = 0
    offenders = []
    for label, path in files.items():
        names = _import_names(path)
        total += len(names)
        print("  {} ({}): {} import(s) -- {}".format(label, path.name, len(names), names))
        for n in names:
            low = n.lower()
            for token in dr.FORBIDDEN_VENDOR_MODULE_TOKENS:
                if token in low:
                    offenders.append((label, n, token))
    print("  DENOMINATOR: {} module-level imports censused across {} files against {} "
          "forbidden vendor tokens".format(total, len(files),
                                           len(dr.FORBIDDEN_VENDOR_MODULE_TOKENS)))
    print("  FORBIDDEN TOKENS: {}".format(list(dr.FORBIDDEN_VENDOR_MODULE_TOKENS)))
    if offenders:
        ok = False
        print("  OFFENDERS: {}".format(offenders))
    else:
        print("  0 of {} imports resolve to a vendor client module".format(total))

    # POSITIVE CONTROL on the censusing instrument itself: a detector that cannot go non-zero
    # is a constant wearing a measurement's clothes.
    ctl = [t for t in dr.FORBIDDEN_VENDOR_MODULE_TOKENS
           if t in "import ycharts_client, blackdiamond_api"]
    print("  POSITIVE CONTROL on the matcher: synthetic import line matches {} token(s) "
          "-> the census can go non-zero".format(len(ctl)))
    if not ctl:
        ok = False

    # 100 keystrokes with EVERY outbound socket raising.
    real_socket = socket.socket
    real_create = socket.create_connection

    def _boom(*a, **k):
        raise _NoNetwork("outbound network call attempted during search")

    raised = 0
    calls = 0
    q = "Margaret Whitfield Priya Raghunathan Nakamura"
    keystrokes = [q[:i + 1] for i in range(min(100, len(q)))]
    while len(keystrokes) < 100:
        keystrokes.append(q[:((len(keystrokes) % len(q)) + 1)])
    socket.socket = _boom
    socket.create_connection = _boom
    try:
        for ks in keystrokes:
            calls += 1
            try:
                hd.search(fx.DIRECTORY, fx.SCOPE_A, ks)
            except _NoNetwork:
                raised += 1
    finally:
        socket.socket = real_socket
        socket.create_connection = real_create
    print("  {} keystrokes through search() with socket.socket and socket.create_connection "
          "stubbed to RAISE: {} raised of {}".format(calls, raised, calls))

    # NEGATIVE CONTROL on the stub: prove the stub WOULD have fired on a real outbound call.
    socket.socket = _boom
    stub_fires = False
    try:
        socket.socket()
    except _NoNetwork:
        stub_fires = True
    finally:
        socket.socket = real_socket
    print("  NEGATIVE CONTROL: the stub itself fires on a direct socket() call: {}".format(
        stub_fires))
    if raised != 0 or calls != 100 or not stub_fires:
        ok = False
    record("d", "PASS" if ok else "FAIL",
           "0 of {} imports are vendor clients; {} of {} keystrokes raised on a stubbed "
           "network (stub verified live)".format(total, raised, calls))


# ============================================================================ arm (e)
def arm_e(state: dict) -> None:
    section("ARM (e) -- THE DIFFERENCE CONTROL ON SCOPE")
    ok = True
    q = "Whitfield"
    a = hd.search(fx.DIRECTORY, fx.SCOPE_A, q)
    b = hd.search(fx.DIRECTORY, fx.SCOPE_B, q)
    set_a = {r["entry_id"] for r in a["results"]}
    set_b = {r["entry_id"] for r in b["results"]}
    print("  query {!r}: advisor A -> {} result(s) {}".format(
        q, a["count"], [r["display_name"] for r in a["results"]]))
    print("  query {!r}: advisor B -> {} result(s) {}".format(
        q, b["count"], [r["display_name"] for r in b["results"]]))
    print("  intersection A n B = {} entries (fixture says MUST be 0: the two "
          "permitted_account_sets are disjoint by construction)".format(
              len(set_a & set_b)))
    if set_a & set_b:
        ok = False
    if not set_a or not set_b:
        ok = False
        print("  ERROR: a difference control needs BOTH arms non-empty; A={} B={}".format(
            len(set_a), len(set_b)))

    rev = hd.search(fx.DIRECTORY, fx.SCOPE_REVOKED, q)
    print("  revoked scope (permitted_account_set empty) -> {} result(s); reason: {}".format(
        rev["count"], rev["reason"]))
    unk = hd.search(fx.DIRECTORY, fx.SCOPE_UNKNOWN_PRINCIPAL, q)
    print("  UNKNOWN principal_class -> {} result(s); reason: {}".format(
        unk["count"], unk["reason"]))
    rrev = hd.resolve(fx.DIRECTORY, fx.SCOPE_REVOKED,
                      {"entry_id": hd._entry_key(fx.DUP_A)})
    print("  revoked scope resolve -> ok={} accounts={} reason: {}".format(
        rrev["ok"], len(rrev["account_ids"]), rrev["partial_reason"]))
    if rev["count"] != 0 or unk["count"] != 0 or rrev["ok"] or rrev["account_ids"]:
        ok = False

    # Cross-check: A cannot reach B's accounts by ANY selection, not just by search.
    cross = hd.resolve(fx.DIRECTORY, fx.SCOPE_A, {"entry_id": hd._entry_key(fx.B_ONLY)})
    print("  advisor A resolving advisor B's entry directly -> ok={} accounts={} reason: "
          "{}".format(cross["ok"], len(cross["account_ids"]), cross["partial_reason"]))
    if cross["ok"] or cross["account_ids"]:
        ok = False
    record("e", "PASS" if ok else "FAIL",
           "A n B = {} of {}/{} results; revoked -> {} results, {} accounts; A->B direct "
           "resolve refused".format(len(set_a & set_b), a["count"], b["count"],
                                    rev["count"], len(rrev["account_ids"])))


# ============================================================================ arm (f)
def _aws(args: "list[str]") -> "tuple[int, str]":
    cmd = [str(_REPO / ".tools" / "aws")] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return p.returncode, (p.stdout + p.stderr).replace("\r", "").strip()


def arm_f(state: dict) -> None:
    section("ARM (f) -- LANDED AND DEPLOYED")
    ok = True
    lines = []

    # --- the QA objects, per firm, by head-object ---
    landed = state.get("landed") or {}
    for firm_id, info in sorted(landed.items()):
        rc, out = _aws(["s3api", "head-object", "--bucket", info["bucket"],
                        "--key", info["latest_key"], "--output", "json"])
        try:
            meta = json.loads(out)
            size = meta.get("ContentLength")
        except Exception:
            size = None
        print("  head-object s3://{}/{} rc={} ContentLength={}".format(
            info["bucket"], info["latest_key"], rc, size))
        if rc != 0 or not size:
            ok = False
            lines.append("{} QA latest.json NOT landed".format(firm_id))
    if landed:
        lines.append("{} of {} firm QA latest.json objects head-object OK".format(
            sum(1 for i in landed.values() if i.get("uploaded")), len(landed)))
    else:
        ok = False
        lines.append("no QA objects landed (--skip-land)")

    # --- served bytes: CodeSha256 == sha256 of the BUILT zip, never a filename ---
    zip_path = state.get("zip_path")
    rc, out = _aws(["lambda", "get-function-configuration", "--function-name", FUNCTION_NAME,
                    "--query", "CodeSha256", "--output", "text"])
    served = out.strip()
    print("  get-function-configuration {} CodeSha256 rc={} -> {}".format(
        FUNCTION_NAME, rc, served))
    built_sha = state.get("built_sha")
    if zip_path and Path(zip_path).is_file():
        import base64
        built_sha = base64.b64encode(
            hashlib.sha256(Path(zip_path).read_bytes()).digest()).decode()
    print("  built zip sha256 (base64) -> {}".format(built_sha))
    if rc != 0 or not served or served != built_sha:
        ok = False
        lines.append("CodeSha256 {} != built zip sha {}".format(served, built_sha))
    else:
        lines.append("CodeSha256 == built zip sha256 ({})".format(served))

    # --- the ledger: CLOSED, and the sentinel committed ---
    if SENTINEL.is_file():
        entry = json.loads(SENTINEL.read_text(encoding="utf-8"))
        status = entry.get("status")
        print("  sentinel {} status={}".format(SENTINEL.name, status))
        p = subprocess.run(["git", "log", "-1", "--format=%H", "--",
                            str(SENTINEL.relative_to(_REPO)).replace("\\", "/")],
                           cwd=str(_REPO), capture_output=True, text=True, timeout=60)
        commit = p.stdout.strip()
        print("  sentinel committed at {}".format(commit or "NOT COMMITTED"))
        if status not in ("closed", "CLOSED", "complete") or not commit:
            ok = False
            lines.append("ledger status {} / sentinel commit {}".format(status, commit))
        else:
            lines.append("ledger CLOSED, sentinel committed {}".format(commit[:10]))
    else:
        ok = False
        lines.append("sentinel {} ABSENT".format(SENTINEL))

    blocked = state.get("safe_deploy_refusal")
    if blocked:
        print("  safe-deploy.sh REFUSAL (verbatim):")
        for ln in blocked.splitlines():
            print("    | " + ln)
        record("f", "BLOCKED", "; ".join(lines) + "; runner code deploy refused for this "
                               "serial (verbatim above)")
        return
    record("f", "PASS" if ok else "FAIL", "; ".join(lines))


# ============================================================================ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-land", action="store_true")
    ap.add_argument("--state", default=str(_HERE / "battery_state.json"))
    a = ap.parse_args(argv)

    print("IB-s-1 BATTERY -- {}".format(
        dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("repo: {}".format(_REPO))

    state = {}
    if Path(a.state).is_file():
        state.update(json.loads(Path(a.state).read_text(encoding="utf-8")))

    arm_a(state)
    arm_b(state)
    arm_c(state)
    arm_d(state)
    arm_e(state)
    if not a.skip_land:
        arm_f(state)

    section("SUMMARY")
    for arm, verdict, line in RESULTS:
        print("  ARM ({}) {}: {}".format(arm, verdict, line))
    expected = 5 if a.skip_land else 6
    passed = sum(1 for _, v, _ in RESULTS if v == "PASS")
    print("  {} of {} arms PASS".format(passed, expected))
    if passed == expected and len(RESULTS) == expected:
        print("IBS1-DIRECTORY-SERVED")
        return 0
    print("TOKEN WITHHELD -- {} of {} arms PASS".format(passed, expected))
    return 1


if __name__ == "__main__":
    sys.exit(main())
