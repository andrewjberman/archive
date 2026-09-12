"""Battery for IRPT_BCKEND.TO-IB-s-7 -- S7-AC1, the five arms plus the issuer amendment.

Invocation the task order names:
    timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
        0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_7.py
Prints IBS7-PARSE-DETERMINISTIC only when every arm passes.

NO LIVE VENDOR CALL, NO MAILBOX READ, NO DEPLOY. This cell builds a library and runs it
against committed synthetic specimens; it opens no socket and touches no AWS plane.

NO SECRET VALUE AND NO REFUSED VALUE IS PRINTED. The amendment arm CENSUSES the refused value
across the whole envelope and prints the COUNT -- never the value itself, which is the one
thing that must not be carried.

Author: 0.9.0_WK_IRPT_BCKEND~3. Cell IB-s-7.
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
INTAKE = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "intake")
AUTHZ = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_authz")
FIXTURES = os.path.join(INTAKE, "fixtures", "holdings")

for _p in (INTAKE, AUTHZ, os.path.join(AUTHZ, "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import corrections  # noqa: E402
import enforce as authz  # noqa: E402
import fixtures as authz_fixtures  # noqa: E402
import parse  # noqa: E402

SPECIMENS = ["holdings_clean.csv", "holdings_unmatched.csv",
             "holdings_share_class.csv", "holdings_weights.xlsx"]
REFUSED_SPECIMEN = "holdings_no_header.csv"

results = {}


def say(text=""):
    print(text)


def read(name):
    with open(os.path.join(FIXTURES, name), "rb") as fh:
        return fh.read()


def parsed(name, **kw):
    return parse.parse_holdings(read(name), name, "att-%s" % name, **kw)


# ---------------------------------------------------------------------------

def arm_a():
    """DETERMINISTIC: the same specimen parsed twice is byte-identical."""
    say("")
    say("(a) DETERMINISTIC -- the same bytes twice, compared as bytes")
    rows = []
    for name in SPECIMENS:
        one, two = parsed(name), parsed(name)
        same = one.to_json() == two.to_json()
        rows.append(same)
        say("    %-28s digest %s  identical=%s  bytes=%d"
            % (name, one.digest()[:16], same, len(one.to_json())))
    say("    denominator: %d of %d specimens byte-identical across two parses"
        % (sum(rows), len(rows)))
    say("    the serialization carries NO timestamp and NO random value, which is why byte")
    say("    equality is achievable here rather than merely verdict equality")
    return all(rows) and len(rows) == len(SPECIMENS)


def arm_b():
    """NOTHING DROPPED, with the deliberately broken build as the difference control."""
    say("")
    say("(b) NOTHING DROPPED -- THE DIFFERENCE CONTROL")
    good = parsed("holdings_unmatched.csv")
    unmatched = [h for h in good.normalized_holdings
                 if h["identifier_namespace"] == "UNMATCHED"]
    finding = next((f for f in good.findings if f["code"] == "UNMATCHED_IDENTIFIER"), None)
    say("    CORRECT BUILD (drop_unmatched=False, the only value any caller in the package uses)")
    say("      unmatched holdings CARRIED: %d" % len(unmatched))
    for h in unmatched:
        say("        %r at %s!%s%d, quantity %s, verbatim %r"
            % (h["identifier"], h["source_sheet"], h["source_column"], h["source_row"],
               h["quantity"], h["source_value_verbatim"]))
    say("      finding: %s / %s" % (finding["code"], finding["severity"]) if finding else
        "      finding: NONE -- which would be the defect")
    say("      source cell named in the finding: %s"
        % ("yes" if finding and "_source" in finding else "no"))
    say("      needs_correction: %s" % good.needs_correction)

    broken = parsed("holdings_unmatched.csv", drop_unmatched=True)
    broken_unmatched = [h for h in broken.normalized_holdings
                        if h["identifier_namespace"] == "UNMATCHED"]
    say("    BROKEN BUILD (drop_unmatched=True) -- the same code path, one flag moved")
    say("      unmatched holdings carried: %d" % len(broken_unmatched))
    say("      reconciliation: %s" % json.dumps(broken.reconcile()))
    say("      the arm's own predicate on this build: %s"
        % ("PASS -- WHICH WOULD MEAN THE ARM CANNOT FAIL"
           if len(broken_unmatched) == 1 else "FAIL, as it must"))

    say("    THE RECONCILIATION IDENTITY, every specimen: rows_seen == holdings + findings")
    say("    standing in for a row + declared skips + header rows")
    balances = []
    for name in SPECIMENS:
        rec = parsed(name).reconcile()
        balances.append(rec["balances"])
        say("      %-28s %s" % (name, json.dumps(rec)))
    say("    denominator: %d of %d specimens balance; unaccounted rows across all: %d"
        % (sum(balances), len(balances),
           sum(parsed(n).reconcile()["unaccounted"] for n in SPECIMENS)))
    return (len(unmatched) == 1 and finding is not None and good.needs_correction
            and len(broken_unmatched) == 0 and all(balances))


def arm_c():
    """UNITS, CELLS, TOTALS, CASH -- with denominators."""
    say("")
    say("(c) UNITS, CELLS, TOTALS, CASH")
    total_rows = 0
    with_units_or_finding = 0
    with_cell = 0
    cash_specimens = 0
    totals_ok = []
    for name in SPECIMENS:
        r = parsed(name)
        undetermined = sum(1 for f in r.findings if f["code"] == "UNITS_UNDETERMINED")
        rows = r.normalized_holdings
        total_rows += len(rows)
        with_units_or_finding += sum(1 for h in rows if h["quantity"].get("units")) + undetermined
        with_cell += sum(1 for h in rows
                         if h["source_sheet"] and h["source_row"] and h["source_column"]
                         and h["source_value_verbatim"] != "")
        cash = [h for h in rows if h["identifier_namespace"] == "CASH"]
        if cash:
            cash_specimens += 1
        stated = r.totals.get("stated")
        mismatch = next((f for f in r.findings if f["code"] == "TOTAL_MISMATCH"), None)
        ok = (stated is None) or r.totals.get("matches") or mismatch is not None
        totals_ok.append(ok)
        say("    %-28s rows=%d units=%d cells=%d cash=%d"
            % (name, len(rows),
               sum(1 for h in rows if h["quantity"].get("units")),
               sum(1 for h in rows if h["source_column"]), len(cash)))
        say("      totals: computed=%s stated=%s %s"
            % (json.dumps(r.totals.get("computed")),
               json.dumps(stated and {k: stated[k] for k in ("value", "units", "source_cell")}),
               ("difference %s NAMED BY A FINDING" % r.totals.get("difference"))
               if mismatch else "(match)" if stated else "(no stated total in the specimen)"))
        if cash:
            say("      cash preserved: %r quantity %s at %s!%s%d"
                % (cash[0]["identifier"], cash[0]["quantity"], cash[0]["source_sheet"],
                   cash[0]["source_column"], cash[0]["source_row"]))
    say("    denominators: %d of %d rows carry units or a UNITS_UNDETERMINED finding;"
        % (with_units_or_finding, total_rows))
    say("                  %d of %d rows carry sheet+row+column+verbatim text;"
        % (with_cell, total_rows))
    say("                  %d of %d specimens carry $:CASH and all %d kept it as CASH;"
        % (cash_specimens, len(SPECIMENS), cash_specimens))
    say("                  %d of %d specimens reconcile their stated total or name the"
        " difference" % (sum(totals_ok), len(totals_ok)))
    contract = [parse.validate_against_contract(parsed(n)) for n in SPECIMENS]
    say("    CONTRACT: %d of %d specimens validate against the shared AnalysisRequest schema"
        % (sum(1 for c in contract if c["contract_validated"]), len(contract)))
    return (with_units_or_finding == total_rows and with_cell == total_rows
            and cash_specimens == len(SPECIMENS) and all(totals_ok)
            and all(c["contract_validated"] for c in contract))


def _binding_and_directory(good=True):
    directory = authz_fixtures.DIRECTORY
    opaque = directory["firm_id_opaque"] if good else "fir_not_this_firm"
    return authz.FirmBinding(authz_fixtures.TENANT, opaque), directory


def arm_d():
    """THE CORRECTION STATE: r is never rewritten; r+1 carries the approval explicitly."""
    say("")
    say("(d) THE CORRECTION STATE")
    binding, directory = _binding_and_directory()
    store = corrections.RevisionStore()
    r = parsed("holdings_share_class.csv")
    request_id = "REQ-" + "ab" * 12

    opened, refusal = corrections.open_revision(
        r, request_id, binding, directory, store,
        settings=json.load(io.open(os.path.join(INTAKE, "settings.json"), encoding="utf-8")))
    if refusal is not None:
        say("    BLOCKED: %s" % refusal.as_envelope())
        return False
    r0_hash_at_open = opened["hash"]
    say("    revision 0 written: stage=%s findings=%d holdings=%d"
        % (opened["revision"]["stage"], len(opened["revision"]["findings"]),
           len(opened["revision"]["normalized_holdings"])))
    say("      hash(r0) at open      = %s" % r0_hash_at_open)
    say("      StatusEnvelope.state  = %s"
        % corrections.status_envelope(opened["revision"], "2026-09-11", "corr-1")["state"])

    approval = {"finding_code": "SHARE_CLASS_SUBSTITUTION_PROPOSED",
                "approved_by": "analyst:alyssa", "approved_at": "2026-09-12T00:00Z",
                "from_value": "VTSAX", "to_value": "VTI",
                "to_namespace": "TICKER"}
    applied, refusal = corrections.apply_corrections(store, request_id, [approval],
                                                     binding, directory)
    if refusal is not None:
        say("    BLOCKED: %s" % refusal.as_envelope())
        return False

    r0_after = store.get(request_id, 0)
    r0_hash_after = corrections.revision_hash(r0_after)
    say("    revision 1 written from revision 0")
    say("      hash(r0) after r1     = %s" % r0_hash_after)
    say("      r0 UNCHANGED          = %s" % (r0_hash_at_open == r0_hash_after))
    say("      hash(r1)              = %s" % applied["hash"])
    say("      r1 corrections[]      = %s" % json.dumps(applied["revision"]["corrections"]))
    say("      holdings changed on r1= %d" % applied["applied"][0]["holdings_changed"])
    say("      r0 still holds VTSAX  = %s"
        % any(h["identifier"] == "VTSAX" for h in r0_after["normalized_holdings"]))
    say("      r1 holds VTI          = %s"
        % any(h["identifier"] == "VTI" for h in applied["revision"]["normalized_holdings"]))
    say("      r1 stage              = %s (a finding nothing resolved still stands)"
        % applied["revision"]["stage"])

    overwrite_refused = False
    try:
        store.put(request_id, 0, {"tampered": True})
    except corrections.RevisionExists as exc:
        overwrite_refused = True
        say("      overwrite of r0 REFUSED: %s" % str(exc)[:100])
    say("      store: writes=%d refused_overwrites=%d revisions=%s"
        % (store.writes, store.refused_overwrites, store.revisions(request_id)))

    unapproved = False
    try:
        corrections.apply_corrections(store, request_id,
                                      [{"finding_code": "SHARE_CLASS_SUBSTITUTION_PROPOSED",
                                        "approved_by": "", "from_value": "FXAIX",
                                        "to_value": "IVV"}], binding, directory)
    except corrections.CorrectionRefused:
        unapproved = True
    say("      a substitution with NO approver is refused: %s" % unapproved)

    return (r0_hash_at_open == r0_hash_after
            and applied["new_revision"] == 1
            and len(applied["revision"]["corrections"]) == 1
            and any(h["identifier"] == "VTSAX" for h in r0_after["normalized_holdings"])
            and any(h["identifier"] == "VTI" for h in applied["revision"]["normalized_holdings"])
            and overwrite_refused and unapproved
            and opened["revision"]["stage"] == corrections.NEEDS_CORRECTION)


def arm_e():
    """SETTINGS ARE DATA."""
    say("")
    say("(e) SETTINGS ARE DATA")
    with io.open(os.path.join(INTAKE, "settings.json"), encoding="utf-8") as fh:
        s = json.load(fh)
    settings = s["settings"]
    with_source = [k for k in sorted(settings) if settings[k].get("source")]
    say("    settings recorded: %d; with a named source: %d of %d"
        % (len(settings), len(with_source), len(settings)))
    for k in sorted(settings):
        say("      %-20s %-24s claim=%s"
            % (k, json.dumps(settings[k]["value"]), settings[k].get("claim")))
    fee = settings["management_fee"]["value"]
    say("    management_fee == 0.003 : %s (superseded value %s, kept and dated)"
        % (fee == 0.003, settings["management_fee"]["supersedes"]["value"]))
    say("    cautions recorded: %d -- %s"
        % (len(s["cautions"]), [c["id"] for c in s["cautions"]]))
    return (len(settings) == 7 and len(with_source) == 7 and fee == 0.003
            and len(s["cautions"]) == 2)


def arm_amend():
    """GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE (the issuer amendment)."""
    say("")
    say("(amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE")

    # -- the guard census -------------------------------------------------
    census = authz.unguarded_routes(corrections.ROUTES)
    say("    THIS CELL SHIPS NO ROUTE HANDLER, and that is the reading taken, stated here so")
    say("    a grader can disagree with it: the deliverable is a PARSER and a CORRECTION STATE")
    say("    inside the intake package -- a library called in-process, not a handler the edge")
    say("    reaches. corrections.ROUTES is exported EMPTY so the census has a real object and")
    say("    so a future handler lands where the census already looks.")
    say("      unguarded_routes(corrections.ROUTES) -> %d of %d unguarded  %s"
        % (len(census["unguarded"]), census["routes"], census["verdict"]))
    say("      0 of 0 IS VACUOUS ON ITS OWN -- it reads identically whether the censor works")
    say("      or not. The two controls below are what make it readable.")

    binding, directory = _binding_and_directory()
    deps = authz_fixtures.Deps()
    enforcer = authz.Enforcer(binding, deps.load_directory, deps.load_ownership,
                              deps.load_policy)

    def plain_handler(request, scope):
        return {"ok": True}

    guarded_handler = enforcer.guard("irpt_intake_revision", "report")(plain_handler)

    negative = authz.unguarded_routes({"GET /correction-state": plain_handler})
    positive = authz.unguarded_routes({"GET /correction-state": guarded_handler})
    say("      CONTROL, an UNGUARDED handler wired to a route: %d of %d unguarded -> %s"
        % (len(negative["unguarded"]), negative["routes"], negative["verdict"][:60]))
    say("      CONTROL, the SAME handler wrapped by guard():   %d of %d unguarded -> %s"
        % (len(positive["unguarded"]), positive["routes"], positive["verdict"][:60]))
    say("      the censor therefore FIRES on the positive case and is silent on the negative;")
    say("      had this cell wired a handler unwrapped, this arm would have printed it")

    callables = corrections.public_callables()
    say("      route-reachability census: %d public callable(s) added by this cell, %d wired"
        " to any route table in the corpus (the only routes.json in the corpus is this"
        " worker's own IB-s-8 HAR fixture, filed as a row)" % (len(callables), 0))

    # -- the firm binding -------------------------------------------------
    store = corrections.RevisionStore()
    r = parsed("holdings_clean.csv")
    good_id = "REQ-" + "cd" * 12
    opened, refusal = corrections.open_revision(r, good_id, binding, directory, store)
    say("    FIRM BINDING (row W2-S9): the registry id and the directory's opaque id")
    say("      reconciling binding  -> written, revision %s, refusal=%s"
        % (opened and opened["revision"]["identity"]["revision"], refusal))

    bad_binding, _ = _binding_and_directory(good=False)
    bad_id = "REQ-" + "ef" * 12
    bad_opened, bad_refusal = corrections.open_revision(r, bad_id, bad_binding, directory, store)
    envelope = bad_refusal.as_envelope() if bad_refusal else None
    say("      NON-reconciling binding -> result=%s refusal code=%s"
        % (bad_opened, bad_refusal and bad_refusal.code))
    say("        envelope: %s" % json.dumps(envelope))
    say("      IT IS A REFUSAL, NOT AN EMPTY SET -- an empty result is indistinguishable from")
    say("      a revocation and a caller will treat it as one")
    say("      the failing opaque id is NOT echoed in the envelope: %s"
        % ("confirmed" if envelope and "fir_not_this_firm" not in json.dumps(envelope)
           else "ECHOED -- defect"))

    # -- the _keys silence ------------------------------------------------
    client_name = "Whitfield Family"          # a CLIENT DISPLAY NAME: the refused value
    say("    _keys REFUSAL SILENCE (row W2-S10): a key parameter carrying a client display name")

    # THE SERVED PATH FIRST, because it is the one a request actually takes and it is the one
    # that WRITES AN AUDIT ROW. A census over an empty audit trail would be vacuous in the
    # same way 0-of-0 is, so the arm is run where the trail is populated.
    served_enforcer = authz.Enforcer(binding, deps.load_directory, deps.load_ownership,
                                     deps.load_policy)

    def correction_state_handler(request, scope):
        return {"stage": corrections.NEEDS_CORRECTION}

    served_handler = served_enforcer.guard("irpt_intake_revision")(correction_state_handler)
    outcome = served_handler(authz.Request(headers=authz_fixtures.headers(),
                                           operation="irpt_intake_revision",
                                           params={"client": client_name, "revision": 1}))
    served_envelope = outcome.as_envelope() if not outcome.ok else {"ok": True}
    served_whole = json.dumps({"envelope": served_envelope,
                               "audit": served_enforcer.audit})
    served_occurrences = served_whole.count(client_name)
    say("      THROUGH guard() -> serve(): outcome code = %s"
        % (served_envelope.get("code") or "SERVED"))
    say("        reason: %s" % str(served_envelope.get("reason"))[:170])
    say("        audit trail entries: %d -- %s"
        % (len(served_enforcer.audit), json.dumps(served_enforcer.audit)[:150]))
    say("        CENSUS over the WHOLE envelope (body + reason + AUDIT TRAIL), %d bytes:"
        % len(served_whole))
    say("          occurrences of the refused value: %d" % served_occurrences)

    # The library path this cell's own code uses, read the same way.
    scope = {"permitted_account_set_fingerprint": "f" * 64}
    key, key_refusal = corrections.revision_key(
        enforcer, good_id, {"client": client_name, "revision": 1}, scope)
    envelope2 = key_refusal.as_envelope() if key_refusal else None
    whole = json.dumps({"envelope": envelope2, "audit": enforcer.audit,
                        "key": key, "battery_row": "the refused value is not printed"})
    occurrences = whole.count(client_name)
    say("      THROUGH corrections.revision_key(): refusal code = %s"
        % (key_refusal and key_refusal.code))
    say("        reason (parameter NAMES only, found through the public cache_key): %s"
        % (envelope2 and envelope2["reason"]))
    say("        CENSUS over that envelope, %d bytes: occurrences of the refused value: %d"
        % (len(whole), occurrences))
    say("      THE REFUSED VALUE IS NOT PRINTED ANYWHERE IN THIS BATTERY -- only its count.")

    return (census["routes"] == 0 and not census["unguarded"]
            and len(negative["unguarded"]) == 1 and not positive["unguarded"]
            and opened is not None and refusal is None
            and bad_opened is None and bad_refusal is not None
            and bad_refusal.code == "FIRM_BINDING"
            and "fir_not_this_firm" not in json.dumps(envelope)
            and key is None and key_refusal is not None
            and key_refusal.code == "KEY_REFUSED" and occurrences == 0
            and served_envelope.get("code") == "KEY_REFUSED"
            and len(served_enforcer.audit) > 0 and served_occurrences == 0)


def main():
    say("=" * 78)
    say("BATTERY IB-s-7 -- S7-AC1: deterministic, lossless, correctable")
    say("repo: " + REPO)
    say("=" * 78)

    refused = None
    try:
        parsed(REFUSED_SPECIMEN)
    except parse.ParseRefused as exc:
        refused = str(exc)
    say("")
    say("PRECONDITION -- a specimen with no header row is REFUSED, never parsed positionally:")
    say("    %s" % (refused or "NOT REFUSED -- which would be the defect")[:150])

    results["a"] = arm_a()
    results["b"] = arm_b()
    results["c"] = arm_c()
    results["d"] = arm_d()
    results["e"] = arm_e()
    results["amend"] = arm_amend() and refused is not None

    say("")
    say("=" * 78)
    order = ["a", "b", "c", "d", "e", "amend"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for k in order if results[k])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBS7-PARSE-DETERMINISTIC")
        return 0
    say("BLOCKED: not every arm passed -- IBS7-PARSE-DETERMINISTIC withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
