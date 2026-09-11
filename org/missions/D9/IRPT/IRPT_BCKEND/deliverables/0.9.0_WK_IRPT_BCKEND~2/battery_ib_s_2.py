#!/usr/bin/env python3
"""IB-s-2 acceptance battery -- criterion S2-AC1, arms (a) through (g).

Prints `IBS2-SCOPE-RESOLVED` on the LAST line if and only if EVERY arm passes. The token is
emitted from exactly one place at the very end, because the token is the only thing the criterion
reads.

Every count carries its DENOMINATOR. Every arm that asserts an absence runs a CONTROL that can
make the same instrument go non-zero -- an assertion never mutated has never been tested.

Usage:  python battery_ib_s_2.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))   # .../<serial>/ is 7 levels below the worktree root
SCOPE_DIR = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting", "_scope")
CONTRACTS = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting", "_contracts")
VALIDATOR = os.path.join(_REPO, "infra", "aws", "lambda-edge", "auth-validator-edge", "index.mjs")
_PARTNERS_REL = os.path.join("portal", "src", "pages", "AdvisorIntelligence", "_partners")


def _partners_dir():
    """Resolve the partner `roles.ts` home, and say WHICH checkout answered.

    `portal/` is a GITLINK. A linked worktree does not populate a submodule, so in this worktree
    the path exists as an empty directory and a census over it returns `0 of 0` -- a vacuous pass
    that reads exactly like a real one. The primary checkout is the fallback (reads only; no
    portal write is granted), and if NEITHER answers the arm must say so rather than print a zero.
    """
    for root, label in ((_REPO, "worktree"),
                        (os.path.join("C:" + os.sep, "Users", "AndrewBerman", "Desktop",
                                      "ajb_workspace"), "primary checkout")):
        cand = os.path.join(root, _PARTNERS_REL)
        if os.path.isfile(os.path.join(cand, "49financial", "roles.ts")):
            return cand, label
    return None, "NOT FOUND"

for p in (SCOPE_DIR, os.path.join(SCOPE_DIR, "tests")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fixtures as fx          # noqa: E402
import resolve as rs           # noqa: E402

RESULTS = []


def record(arm, verdict, line):
    RESULTS.append((arm, verdict, line))
    print("ARM {} {}: {}".format(arm, verdict, line))


def section(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def _schema(name):
    with open(os.path.join(CONTRACTS, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


# ============================================================================ arm (a)
def arm_a():
    section("ARM (a) -- THE TRACE IS PRINTED, WITH LINE NUMBERS")
    ok = True
    with open(VALIDATOR, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    print("  source: infra/aws/lambda-edge/auth-validator-edge/index.mjs ({} lines), read at "
          "branch HEAD".format(len(lines)))
    print("  DENOMINATOR: {} injected header(s) found in the allow-list, each VERIFIED against "
          "the line it claims".format(len(rs.TRUSTED_HEADERS)))
    verified = 0
    for name in sorted(rs.TRUSTED_HEADERS):
        claim, line_no = rs.TRUSTED_HEADERS[name]
        text = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
        hit = name in text
        verified += 1 if hit else 0
        print("    {:<18} :{:<4} from {:<42} {}".format(
            name, line_no, claim, "VERIFIED in source" if hit else "NOT FOUND -- STALE"))
        if not hit:
            ok = False
    print("  {} of {} header claims verified against index.mjs at HEAD".format(
        verified, len(rs.TRUSTED_HEADERS)))

    # NEGATIVE CONTROL: the same check must be able to FAIL.
    bogus_hit = "x-not-a-header" in (lines[382] if len(lines) > 382 else "")
    print("  NEGATIVE CONTROL: a header name that is NOT injected reads as present at :383? "
          "{} (must be False, else the check is a constant)".format(bogus_hit))
    if bogus_hit:
        ok = False

    # The file's own summary comment enumerates EIGHT; the code injects NINE.
    summary = " ".join(lines[10:12]).lower()
    missing_from_summary = [n for n in rs.TRUSTED_HEADERS if n not in summary]
    print("  the file's OWN summary comment (:11-12) enumerates {} of {} injected headers; "
          "missing: {} -- this trace is built from the CODE (:383-391), not the summary".format(
              len(rs.TRUSTED_HEADERS) - len(missing_from_summary), len(rs.TRUSTED_HEADERS),
              missing_from_summary))

    # THE OPAL-PRINCIPAL ANSWER.
    print("")
    print("  OPAL-PRINCIPAL QUESTION: is an Opal (non-firm) principal distinguishable from the "
          "injected header set?")
    print("    ANSWER: NOT DISTINGUISHABLE. Two independent reasons, both read at HEAD:")
    for ln in (205, 203, 184, 185):
        print("      :{:<4} {}".format(ln, lines[ln - 1].strip()))
    print("    (i)  the discriminating claim `firmRole` is READ at :205 and is NOT among the "
          "{} injected headers (census above)".format(len(rs.TRUSTED_HEADERS)))
    print("    (ii) :184-185 says role='admin' is carried by Opal staff AND partner-firm admins, "
          "which CONTRADICTS :202-204's 'role remains reserved for Opal-platform admins'")
    firmrole_injected = any("firmrole" in ln.lower() and "request.headers" in ln for ln in lines)
    print("    census: `firmRole` injected as a header anywhere in the file? {} "
          "(must be False)".format(firmrole_injected))
    if firmrole_injected:
        ok = False
    print("    CONSEQUENCE IN CODE: OPAL_GLOBAL is never minted from headers -- it requires the "
          "caller's explicit opal_principal_ids roster, EMPTY by default.")
    h = rs.trusted_only(fx.headers(role="admin", email="staff@opalinvest.dev"))[0]
    without = rs.classify_principal(h)[0]
    with_roster = rs.classify_principal(h, {"staff@opalinvest.dev"})[0]
    print("    same admin headers -> without roster: {} | with roster: {}".format(
        without, with_roster))
    if without != "FIRM_OPERATIONS" or with_roster != "OPAL_GLOBAL":
        ok = False
    print("    UPSTREAM OWNER (S2-AC2): infra/aws/lambda-edge/auth-validator-edge/index.mjs, "
          ".owned-paths.yaml longest match infra/aws/** -> lane CLOUD_OPS_OR_ETL (any AE agent); "
          "NOT in this order's <paths>.")
    record("a", "PASS" if ok else "FAIL",
           "{} of {} injected headers traced to source lines; Opal principal NOT "
           "distinguishable (firmRole read at :205, never injected)".format(
               verified, len(rs.TRUSTED_HEADERS)))


# ============================================================================ arm (b)
def arm_b():
    section("ARM (b) -- A PARTLY PERMITTED RELATIONSHIP NEVER SILENTLY GRANTS")
    ok = True
    rel_ix = rs._relationship_index(fx.DIRECTORY, fx.FIRM)
    reach = rel_ix[fx.R2]
    print("  fixture: relationship {} reaches {} account(s): {}".format(
        fx.R2, len(reach), reach))
    print("           advisor A's ownership grant covers {} of those {}".format(
        len([a for a in reach if a in fx.OWNERSHIP["advisors"][fx.ADVISOR_A]["accounts"]]),
        len(reach)))

    sub = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP,
                     requested_scope={"scope_kind": "RELATIONSHIP", "scope_ids": [fx.R2]})
    print("  DEFAULT MODE  requested RELATIONSHIP {} -> resolved {} {} ; permitted set {} ; "
          "partial_reason: {}".format(fx.R2, sub["resolved_scope"]["scope_kind"],
                                      sub["resolved_scope"]["scope_ids"],
                                      sub["permitted_account_set"], sub["partial_reason"]))
    if (sub["resolved_scope"]["scope_kind"] != "ACCOUNT"
            or sub["permitted_account_set"] != [fx.A3] or not sub["partial_reason"]):
        ok = False
    if fx.A4 in sub["permitted_account_set"]:
        ok = False

    strict = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP,
                        requested_scope={"scope_kind": "RELATIONSHIP", "scope_ids": [fx.R2]},
                        strict_partial=True)
    print("  STRICT MODE   same request -> resolved {} ; permitted set {} ; partial_reason: "
          "{}".format(strict["resolved_scope"]["scope_kind"], strict["permitted_account_set"],
                      strict["partial_reason"]))
    if strict["resolved_scope"]["scope_kind"] != "UNSUPPORTED" or strict["permitted_account_set"]:
        ok = False

    none_allowed = rs.resolve(fx.headers(advisor_id=fx.ADVISOR_B), fx.DIRECTORY, fx.OWNERSHIP,
                              requested_scope={"scope_kind": "ACCOUNT", "scope_ids": [fx.A4]})
    print("  WHOLLY UNPERMITTED request -> resolved {} (never an empty look-alike of the "
          "requested scope); reason: {}".format(none_allowed["resolved_scope"]["scope_kind"],
                                                none_allowed["partial_reason"]))
    if none_allowed["resolved_scope"]["scope_kind"] != "UNSUPPORTED":
        ok = False

    whole = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP,
                       requested_scope={"scope_kind": "ACCOUNT",
                                        "scope_ids": [fx.A1, fx.A2]})
    print("  CONTROL: a WHOLLY permitted request -> resolved {} with partial_reason {} "
          "(must be None, else partial_reason is a constant)".format(
              whole["resolved_scope"]["scope_kind"], whole["partial_reason"]))
    if whole["partial_reason"] is not None:
        ok = False
    print("  the requested WHOLE was returned in 0 of 3 partly/unpermitted cases")
    record("b", "PASS" if ok else "FAIL",
           "3 of 3 partial cases resolve to the exact allowed subset or an explicit UNSUPPORTED; "
           "0 of 3 returned the requested whole; control case carries partial_reason None")


# ============================================================================ arm (c)
def arm_c():
    section("ARM (c) -- THE FINGERPRINT IS STABLE AND DISCRIMINATING")
    ok = True
    a = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP)
    b = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP)
    print("  same headers + same directory, run twice:")
    print("    run 1 fp {}".format(a["permitted_account_set_fingerprint"]))
    print("    run 2 fp {}".format(b["permitted_account_set_fingerprint"]))
    print("    identical: {} (over a permitted set of {} account(s))".format(
        a["permitted_account_set_fingerprint"] == b["permitted_account_set_fingerprint"],
        len(a["permitted_account_set"])))
    if a["permitted_account_set_fingerprint"] != b["permitted_account_set_fingerprint"]:
        ok = False

    thinner = {"schema_version": 1, "advisors": {fx.ADVISOR_A: {
        "accounts": fx.OWNERSHIP["advisors"][fx.ADVISOR_A]["accounts"][1:], "relationships": []}}}
    c = rs.resolve(fx.headers(), fx.DIRECTORY, thinner)
    print("  ONE ACCOUNT REMOVED ({} of {} granted):".format(
        len(c["permitted_account_set"]), len(a["permitted_account_set"])))
    print("    fp {}".format(c["permitted_account_set_fingerprint"]))
    print("    differs from run 1: {}".format(
        c["permitted_account_set_fingerprint"] != a["permitted_account_set_fingerprint"]))
    if c["permitted_account_set_fingerprint"] == a["permitted_account_set_fingerprint"]:
        ok = False

    d = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP, entitlement_revision="ent-2")
    same_set = d["permitted_account_set"] == a["permitted_account_set"]
    print("  SAME SET, DIFFERENT ENTITLEMENT REVISION: sets identical {} ; fingerprints differ "
          "{} -- a set that looks the same under a different entitlement must not fingerprint "
          "the same".format(same_set,
                            d["permitted_account_set_fingerprint"]
                            != a["permitted_account_set_fingerprint"]))
    if not same_set or (d["permitted_account_set_fingerprint"]
                        == a["permitted_account_set_fingerprint"]):
        ok = False
    shape = (len(a["permitted_account_set_fingerprint"]) == 64
             and all(ch in "0123456789abcdef" for ch in a["permitted_account_set_fingerprint"]))
    print("  contract shape ^[0-9a-f]{{64}}$: {}".format(shape))
    if not shape:
        ok = False
    record("c", "PASS" if ok else "FAIL",
           "fingerprint identical across 2 of 2 identical runs; differs on a removed account and "
           "on an entitlement-revision change with an identical set")


# ============================================================================ arm (d)
def arm_d():
    section("ARM (d) -- NO DOUBLE COUNT, EVERY GAP REASONED")
    ok = True
    population, census = rs.firm_population(fx.DIRECTORY, fx.FIRM)
    print("  49F-SHAPED OVERLAP FIXTURE (one account under two relationships, modelled on the "
          "201-group overlap IB-s-1 measured):")
    print("    account ROWS across entries: {}".format(census["account_rows"]))
    print("    UNIQUE accounts after collapse: {}".format(census["unique_accounts"]))
    print("    duplicates collapsed: {} (rows - unique)".format(census["duplicates_collapsed"]))
    print("    entries excluded as cross-firm: {}".format(census["entries_excluded_cross_firm"]))
    if census["duplicates_collapsed"] < 1:
        ok = False
        print("    FAIL: the fixture carries no overlap, so this arm would pass vacuously")
    if len(population) != len(set(population)):
        ok = False

    admin = rs.resolve(fx.headers(role="admin"), fx.DIRECTORY, fx.OWNERSHIP)
    print("    a firm-operations viewer's permitted set: {} account(s) == {} unique in the "
          "population: {}".format(len(admin["permitted_account_set"]),
                                  census["unique_accounts"],
                                  len(admin["permitted_account_set"])
                                  == census["unique_accounts"]))
    if len(admin["permitted_account_set"]) != census["unique_accounts"]:
        ok = False

    granted = fx.OWNERSHIP["advisors"][fx.ADVISOR_A]["accounts"]
    gaps = rs.unmatched_reasons(granted, fx.DIRECTORY, fx.FIRM)
    print("  INF-SHAPED GAP LIST (every ownership id the verified firm's directory does not "
          "hold):")
    print("    DENOMINATOR: {} granted account(s); {} matched; {} unmatched".format(
        len(granted), len(granted) - len(gaps), len(gaps)))
    for g in gaps:
        print("      {} -> {}".format(g["account_id"], g["reason"]))
    with_reason = sum(1 for g in gaps if g["reason"])
    print("    {} of {} unmatched accounts carry a reason".format(with_reason, len(gaps)))
    if not gaps or with_reason != len(gaps):
        ok = False
    kinds = sorted({g["reason"].split(":")[0] for g in gaps})
    print("    reason kinds exercised by the live fixture: {}".format(kinds))
    probe = rs.unmatched_reasons(["12345678-SCHWAB"], fx.DIRECTORY, fx.FIRM)
    print("    POSITIVE CONTROL on the third kind (a custodian-shaped id, the W2-S7 seam): "
          "{} -> {}".format(probe[0]["account_id"], probe[0]["reason"].split(":")[0]))
    all_kinds = sorted(set(kinds) | {probe[0]["reason"].split(":")[0]})
    print("    {} of 3 reason kinds exercised: {}".format(len(all_kinds), all_kinds))
    if len(all_kinds) != 3:
        ok = False
    clean = rs.unmatched_reasons([fx.A1], fx.DIRECTORY, fx.FIRM)
    print("    NEGATIVE CONTROL: a MATCHED account produces {} gap row(s) (must be 0)".format(
        len(clean)))
    if clean:
        ok = False
    record("d", "PASS" if ok else "FAIL",
           "{} rows -> {} unique accounts ({} duplicates collapsed, 0 double counted); {} of {} "
           "unmatched ownership ids carry a reason; 3 of 3 reason kinds exercised".format(
               census["account_rows"], census["unique_accounts"],
               census["duplicates_collapsed"], with_reason, len(gaps)))


# ============================================================================ arm (e)
def arm_e():
    section("ARM (e) -- THE DIFFERENCE CONTROL ON FORGED HEADERS")
    ok = True
    clean = rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP)
    forged = rs.resolve(fx.headers(extra=fx.FORGED_EXTRA), fx.DIRECTORY, fx.OWNERSHIP)
    print("  the browser-supplied headers added to an OTHERWISE IDENTICAL request "
          "(denominator {}):".format(len(fx.FORGED_EXTRA)))
    for k, v in sorted(fx.FORGED_EXTRA.items()):
        print("    {}: {}".format(k, v[:60]))
    print("  without them: principal {} | {} account(s) | fp {}".format(
        clean["principal_class"], len(clean["permitted_account_set"]),
        clean["permitted_account_set_fingerprint"][:16]))
    print("  with them   : principal {} | {} account(s) | fp {}".format(
        forged["principal_class"], len(forged["permitted_account_set"]),
        forged["permitted_account_set_fingerprint"][:16]))
    same = (clean["permitted_account_set"] == forged["permitted_account_set"]
            and clean["permitted_account_set_fingerprint"]
            == forged["permitted_account_set_fingerprint"]
            and clean["principal_class"] == forged["principal_class"])
    print("  IDENTICAL in set, fingerprint and class: {}".format(same))
    print("  headers DROPPED before any authorization decision: {} of {} seen ({} trusted) -- "
          "{}".format(forged["_census"]["headers_dropped"], forged["_census"]["headers_seen"],
                      forged["_census"]["headers_trusted"],
                      forged["_census"]["dropped_names"]))
    if not same or forged["_census"]["headers_dropped"] != len(fx.FORGED_EXTRA):
        ok = False

    override = rs.resolve(fx.headers(extra={"X-Firm-Id-Override": fx.OTHER_FIRM}),
                          fx.DIRECTORY, fx.OWNERSHIP)
    print("  a forged FIRM OVERRIDE: verified_request_firm_id stays {} (not {}); the other "
          "firm's account {} in the permitted set: {}".format(
              override["verified_request_firm_id"][:12], fx.OTHER_FIRM[:12], fx.A7[:12],
              fx.A7 in override["permitted_account_set"]))
    if override["verified_request_firm_id"] != fx.FIRM or fx.A7 in override["permitted_account_set"]:
        ok = False

    # POSITIVE CONTROL: the SAME instrument must move when a TRUSTED header really changes.
    moved = rs.resolve(fx.headers(advisor_id=fx.ADVISOR_B), fx.DIRECTORY, fx.OWNERSHIP)
    print("  POSITIVE CONTROL: changing a TRUSTED header (X-Advisor-Id -> advisor B) moves the "
          "set: {} account(s), fp {} -- differs: {}".format(
              len(moved["permitted_account_set"]),
              moved["permitted_account_set_fingerprint"][:16],
              moved["permitted_account_set_fingerprint"]
              != clean["permitted_account_set_fingerprint"]))
    if (moved["permitted_account_set_fingerprint"]
            == clean["permitted_account_set_fingerprint"]):
        ok = False

    # The partner roles.ts vocabulary is PRESENTATION, never a grant.
    partners, source = _partners_dir()
    keys = []
    files_read = 0
    if partners is None:
        ok = False
        print("  partner roles.ts census: BLOCKED -- neither the worktree (portal/ is a GITLINK "
              "and is not populated in a linked worktree) nor the primary checkout carries the "
              "files. A 0 of 0 census here would be VACUOUS, so the arm FAILS instead.")
    else:
        print("  partner roles.ts source: {} ({})".format(partners, source))
        for firm in ("49financial", "cottonwood", "inflection"):
            path = os.path.join(partners, firm, "roles.ts")
            if not os.path.exists(path):
                continue
            files_read += 1
            with open(path, "r", encoding="utf-8") as fh:
                txt = fh.read()
            for tok in ("architect", "implementor", "consultant", "local_ops",
                        "additional_advisor", "rep", "firm"):
                if "'%s'" % tok in txt:
                    keys.append((firm, tok))
        if files_read != 3 or not keys:
            ok = False
            print("  VACUITY REFUSED: read {} of 3 partner files and found {} role key(s); a "
                  "census with an empty denominator cannot score this bound".format(
                      files_read, len(keys)))
    with open(os.path.join(SCOPE_DIR, "resolve.py"), "r", encoding="utf-8") as fh:
        src = fh.read()
    leaked = sorted({t for _f, t in keys if "'%s'" % t in src})
    print("  partner roles.ts vocabulary census: {} role key(s) across {} of 3 partner file(s) "
          "({}); appearing as a literal in resolve.py: {} of {} -- a role never "
          "authorizes".format(len(keys), files_read, sorted({k for _f, k in keys}), len(leaked),
                              len(keys)))
    probe_src = "role = 'architect'"
    print("  POSITIVE CONTROL on the leak matcher: a synthetic line carrying a role key matches "
          "{} of {} key(s) -- the census can go non-zero".format(
              len([1 for _f, tok in keys if "'%s'" % tok in probe_src]), len(keys)))
    if leaked:
        ok = False
    record("e", "PASS" if ok else "FAIL",
           "{} forged headers dropped, resolved set/fingerprint/class IDENTICAL; a trusted-header "
           "change DOES move the set (positive control); {} of {} partner role keys (read from {} "
           "of 3 real files) appear in the resolver".format(
               len(fx.FORGED_EXTRA), len(leaked), len(keys), files_read))


# ============================================================================ arm (f)
def arm_f():
    section("ARM (f) -- SCHEMA-VALID; SERVER-ONLY FIELDS STAY SERVER-SIDE")
    ok = True
    try:
        import jsonschema
    except ImportError:
        record("f", "BLOCKED", "jsonschema is not installed -- the arm cannot run and is NOT a "
                               "pass")
        return
    v = jsonschema.Draft202012Validator(_schema("ResolvedScope.schema.json"))
    cases = {
        "firm advisor": rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP),
        "firm operations (admin)": rs.resolve(fx.headers(role="admin"), fx.DIRECTORY,
                                              fx.OWNERSHIP),
        "opal global (rostered)": rs.resolve(
            fx.headers(email="staff@opalinvest.dev"), fx.DIRECTORY, fx.OWNERSHIP,
            opal_principal_ids={"staff@opalinvest.dev"},
            firm_catalogue=[{"firm_id": fx.FIRM, "selected": True}]),
        "unknown principal": rs.resolve(fx.headers(advisor_id=""), fx.DIRECTORY, fx.OWNERSHIP),
        "revoked entitlement": rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP_REVOKED),
        "partly permitted": rs.resolve(fx.headers(), fx.DIRECTORY, fx.OWNERSHIP,
                                       requested_scope={"scope_kind": "RELATIONSHIP",
                                                        "scope_ids": [fx.R2]}),
    }
    valid = 0
    for name, scope in cases.items():
        errs = sorted(v.iter_errors(rs.contract_view(scope)), key=str)
        if errs:
            ok = False
            print("    {:<26} INVALID -- {}".format(name, errs[0].message[:70]))
        else:
            valid += 1
            print("    {:<26} VALID   principal={} accounts={} resolved={}".format(
                name, scope["principal_class"], len(scope["permitted_account_set"]),
                scope["resolved_scope"]["scope_kind"]))
    print("  {} of {} resolved objects validate against ResolvedScope.schema.json".format(
        valid, len(cases)))

    broken = dict(rs.contract_view(cases["firm advisor"]))
    broken["principal_class"] = "SUPERUSER"
    print("  NEGATIVE CONTROL: an object with principal_class 'SUPERUSER' validates? {} (must "
          "be False)".format(not list(v.iter_errors(broken))))
    if not list(v.iter_errors(broken)):
        ok = False

    scope = dict(cases["firm advisor"])
    scope["vendor_ids"] = {"blackdiamond_account": "BD-12345", "orion_entity": "ORN-9"}
    view = rs.browser_safe_view(scope)
    server_only = rs._server_only_properties()
    print("  server-only properties declared by the contract (x-server-only): {}".format(
        server_only))
    print("  browser-safe view key census: {} key(s) -- {}".format(len(view), sorted(view)))
    hits = rs.browser_view_carries_vendor_id(view)
    print("  vendor-id-shaped keys or values in the browser view: {} of {} key(s)".format(
        len(hits), len(view)))
    if hits or "vendor_ids" in view:
        ok = False
    control = rs.browser_view_carries_vendor_id(rs.contract_view(scope))
    print("  POSITIVE CONTROL: the SERVER view (which does carry vendor_ids) trips the same "
          "census: {} hit(s) -- {}".format(len(control), control[:2]))
    if not control:
        ok = False
    record("f", "PASS" if ok else "FAIL",
           "{} of {} resolved objects schema-VALID; browser-safe view carries 0 of {} "
           "vendor-id-shaped keys while the server view trips the same census at {}".format(
               valid, len(cases), len(view), len(control)))


# ============================================================================ arm (g)
def arm_g():
    section("ARM (g) -- THE CONTRACT ADMITS THE NULL IT DESCRIBES (issuer amendment, W2-S2)")
    ok = True
    try:
        import jsonschema
    except ImportError:
        record("g", "BLOCKED", "jsonschema is not installed -- the arm cannot run")
        return
    amended = _schema("DirectoryEntry.schema.json")
    typ = amended["properties"]["ids"]["properties"]["relationship_id"]["type"]
    print("  ids.relationship_id type in DirectoryEntry.schema.json: {}".format(json.dumps(typ)))
    print("  its description (unchanged by the amendment): \"{}\"".format(
        amended["properties"]["ids"]["properties"]["relationship_id"]["description"]
        .split("--")[-1].strip()))
    if "null" not in typ:
        ok = False

    with open(os.path.join(CONTRACTS, "fixtures", "DirectoryEntry.valid.json"), "r",
              encoding="utf-8") as fh:
        vf = json.load(fh)
    acct_only = vf["instance_account_only"]
    print("  account-only fixture ids: {}".format(json.dumps(acct_only["ids"])))
    va = jsonschema.Draft202012Validator(amended)
    errs_amended = sorted(va.iter_errors(acct_only), key=str)
    print("  AMENDED schema -> account-only entry with relationship_id null: {}".format(
        "VALIDATES" if not errs_amended else "REFUSED -- " + errs_amended[0].message[:60]))
    if errs_amended:
        ok = False

    pre_path = os.path.join(CONTRACTS, "fixtures", "DirectoryEntry.pre_amendment.schema.json")
    with open(pre_path, "r", encoding="utf-8") as fh:
        pre = json.load(fh)
    vp = jsonschema.Draft202012Validator(pre)
    errs_pre = sorted(vp.iter_errors(acct_only), key=str)
    print("  PRE-AMENDMENT schema text (kept verbatim as a fixture copy) -> the SAME entry: "
          "{}".format("REFUSED -- " + errs_pre[0].message[:60] if errs_pre
                      else "VALIDATES -- THE DIFFERENCE CONTROL IS DEAD"))
    if not errs_pre:
        ok = False
    print("    pre-amendment ids.relationship_id type: {}".format(
        json.dumps(pre["properties"]["ids"]["properties"]["relationship_id"]["type"])))

    # NOTHING ELSE MOVED: leaf-by-leaf diff of the two schema texts.
    def flat(o, p=""):
        out = {}
        if isinstance(o, dict):
            for k, val in o.items():
                out.update(flat(val, p + "/" + str(k)))
        elif isinstance(o, list):
            for i, val in enumerate(o):
                out.update(flat(val, "%s/%d" % (p, i)))
        else:
            out[p] = o
        return out
    fa, fp = flat(amended), flat(pre)
    diff_paths = sorted({k for k in set(fa) | set(fp) if fa.get(k) != fp.get(k)})
    off_target = [k for k in diff_paths
                  if not k.startswith("/properties/ids/properties/relationship_id/type")]
    print("  ONE-TOKEN CHECK: {} leaf difference(s) between the two schema texts, {} of them "
          "outside ids.relationship_id.type (must be 0)".format(
              len(diff_paths), len(off_target)))
    if off_target:
        ok = False
        for k in off_target[:5]:
            print("    OFF-TARGET: {}".format(k))

    # The original fixture pair still behaves: valid accepted, invalid refused.
    orig_ok = not list(va.iter_errors(vf["instance"]))
    with open(os.path.join(CONTRACTS, "fixtures", "DirectoryEntry.invalid.json"), "r",
              encoding="utf-8") as fh:
        bad = json.load(fh)["instance"]
    bad_refused = bool(list(va.iter_errors(bad)))
    print("  REGRESSION on the pair IB-s-18's battery grades: valid fixture accepted {} ; "
          "invalid fixture still refused {}".format(orig_ok, bad_refused))
    if not (orig_ok and bad_refused):
        ok = False
    record("g", "PASS" if ok else "FAIL",
           "type {} ; account-only entry VALIDATES against the amended schema and is REFUSED by "
           "the pre-amendment text; {} of {} leaf diffs outside the one token".format(
               json.dumps(typ), len(off_target), len(diff_paths)))


# ============================================================================ main
def main():
    print("IB-s-2 BATTERY -- {}".format(
        dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("repo: {}".format(_REPO))
    for fn in (arm_a, arm_b, arm_c, arm_d, arm_e, arm_f, arm_g):
        fn()
    section("SUMMARY")
    for arm, verdict, line in RESULTS:
        print("  ARM ({}) {}: {}".format(arm, verdict, line))
    passed = sum(1 for _, v, _ in RESULTS if v == "PASS")
    print("  {} of 7 arms PASS".format(passed))
    if passed == 7 and len(RESULTS) == 7:
        print("IBS2-SCOPE-RESOLVED")
        return 0
    print("TOKEN WITHHELD -- {} of 7 arms PASS".format(passed))
    return 1


if __name__ == "__main__":
    sys.exit(main())
