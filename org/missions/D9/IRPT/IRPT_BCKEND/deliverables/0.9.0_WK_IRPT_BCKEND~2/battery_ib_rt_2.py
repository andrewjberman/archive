#!/usr/bin/env python3
"""BATTERY IB-rt-2 -- GUARD THE SIX. Seven arms, each on the REAL artifact.

  (a) ZERO OF N, AND THE CONTROL      the census over the real route file, and `1 of N` on a
                                      throwaway copy with one handler unregistered
  (b) THE SWAPS                       six swapped identifiers per dispatched handler, refused
                                      with a byte census per swap
  (c) THE FIRM COMES FROM THE         a firm in the body that disagrees with the verified
      PRINCIPAL                       principal is refused; a reconciling one is not
  (d) THE PROJECTION IS ON THE        a grant with no projection refuses UNPROJECTED_GRANT
      SERVED PATH                     rather than serving the empty set it produces
  (e) DEPLOYED AND VERIFIED           CodeSha256 against the built zip, clean plan per root
  (f) THE PRINCIPAL                   minted through the existing path, or HUMAN-GATED with the
                                      operator's exact act
  (g) ENVELOPE CONFORMANCE, SERVED    the deployed responses validate against the v1 response
                                      contracts and the version check is served

NO SELF-WRAPPING HARNESS (bound 12). Every subject is the object the world reaches: the published
route file, each function's declared entry point resolved through `lambda-source-map.json` plus its
own Terraform `handler =` string, the real `_authz` guard and Enforcer. The only substitution is
the STORAGE boundary -- recorded artifacts instead of S3 -- and it carries a difference control:
the same recorded artifacts SERVE the authorized request and REFUSE every swap.

EVERY COUNT PRINTS ITS DENOMINATOR, and a route this order may not open is named and excluded on
its own line rather than folded into a number that would then read as this cell's defect.

NO NETWORK CALL, NO AWS CALL, NO VENDOR CALL, NO DEPLOY.

ASCII only. Exit 0 always: the TOKEN is the verdict, not the exit code.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PKG = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
TESTS = os.path.join(PKG, "_authz", "tests")
V1 = os.path.join(REPO, "docs", "contracts", "investor-reporting", "v1")
GATED = os.path.join(HERE, "RT2_test_principal_human_gated.md")

for _p in (os.path.join(PKG, "_authz"), os.path.join(PKG, "_scope"), os.path.join(PKG, "_keys"),
           TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)
os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")

RESULTS = []


def arm(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))
    print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def blocked(name, detail):
    RESULTS.append((name, False, detail))
    print("[BLOCKED] %s -- %s" % (name, detail))


def run_pytest(paths, junit_name):
    """(rc, output, junit_path). THE CENSUS READS THE XML, NEVER THE TERMINAL PROSE."""
    junit = os.path.join(REPO, ".scratch", junit_name)
    os.makedirs(os.path.dirname(junit), exist_ok=True)
    cmd = [sys.executable, "-m", "pytest"] + list(paths) + [
        "-q", "--no-header", "-rA", "--color=no", "--junitxml=" + junit]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=840)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or ""), junit


def junit_census(junit_path, prefix):
    import xml.etree.ElementTree as ET
    tree = ET.parse(junit_path)
    p = f = s = 0
    for case in tree.iter("testcase"):
        if not (case.get("name") or "").startswith(prefix):
            continue
        kinds = {child.tag for child in case}
        if "failure" in kinds or "error" in kinds:
            f += 1
        elif "skipped" in kinds:
            s += 1
        else:
            p += 1
    if p + f + s == 0:
        print("    WARN: VACUOUS -- no test case named %s* in the XML; 0 of 0 is not a pass"
              % prefix)
    return p, f, s


# --------------------------------------------------------------------- (a) the census
def arm_a():
    print("\n=== ARM (a) ZERO OF N, AND THE CONTROL ===========================")
    import enforce as ez
    import routetable as rt
    import test_unguarded_census as census

    table, skipped = rt.entry_points()
    unresolved = {k: v.reason for k, v in table.items() if isinstance(v, rt.Unresolved)}
    if unresolved:
        blocked("a census", "an entry point did not resolve, so the census would measure this "
                            "battery's reach and not the estate: %s" % unresolved)
        return
    in_lane, out_of_lane = rt.lane_split(table, census.IN_LANE_FUNCTIONS)
    whole = ez.unguarded_routes(table)
    inl = ez.unguarded_routes(in_lane)

    print("    denominator: %d published route(s) = %d with a declared handler + %d without"
          % (len(table) + len(skipped), len(table), len(skipped)))
    for s in skipped:
        print("      EXCLUDED, named and not counted: %s (%s) -- no handler at this vintage"
              % (s["operation"], s["route_key"]))
    print("    IN LANE (the 5 functions this order's <paths> name): %d of %d unguarded"
          % (len(inl["unguarded"]), inl["routes"]))
    print("    WHOLE FILE                                         : %d of %d unguarded"
          % (len(whole["unguarded"]), whole["routes"]))
    for route_key in whole["unguarded"]:
        print("      out of lane: %-58s -> %s (row IRPT_BCKEND-W2-S19)"
              % (route_key, rt.function_for(route_key)))

    arm("a1 zero in lane", not inl["unguarded"] and inl["routes"] == 8,
        "%d of %d route(s) this order may open reach an unguarded handler"
        % (len(inl["unguarded"]), inl["routes"]))

    if whole["unguarded"]:
        blocked("a2 zero over the whole file",
                "%d of %d route(s) still reach an unguarded handler and ALL %d dispatch to "
                "irpt-status, whose source dir and Terraform root are outside this order's "
                "<paths> -- BLOCKING row IRPT_BCKEND-W2-S19, disarm owner 2.0.0_SA_COO~B. The "
                "criterion's bar is `0 of N` with N = handler-bearing routes = %d; it is NOT met "
                "and is not graded around."
                % (len(whole["unguarded"]), whole["routes"], len(whole["unguarded"]),
                   whole["routes"]))
    else:
        arm("a2 zero over the whole file", True, "0 of %d" % whole["routes"])

    rc, out, junit = run_pytest([os.path.join("infra", "aws", "lambda", "investor-reporting",
                                              "_authz", "tests",
                                              "test_unguarded_census.py")],
                               "ibrt2_census_junit.xml")
    p, f, _s = junit_census(junit, "test_the_census_fires_when_one_handler_is_unregistered")
    print("    the control, on a THROWAWAY copy of the TABLE (never of a handler): %d of %d "
          "victim(s) moved the verdict to `1 of 8`" % (p, p + f))
    arm("a3 the control fires", p >= 3 and f == 0,
        "%d of %d control case(s) pass: the detector returns non-zero on the positive case, so "
        "the zero above is a measurement and not a constant" % (p, p + f))


# --------------------------------------------------------------------- (b)(c)(d)
def arm_bcd():
    print("\n=== ARMS (b) (c) (d) THROUGH THE REAL ENTRY POINTS ===============")
    import test_unguarded_census as census

    rc, out, junit = run_pytest([os.path.join("infra", "aws", "lambda", "investor-reporting",
                                              "_authz", "tests",
                                              "test_guarded_entries.py")],
                               "ibrt2_entries_junit.xml")
    tail = [ln for ln in out.splitlines() if ln.strip()][-1:]
    print("    pytest rc=%d  last line: %s" % (rc, tail[0] if tail else "(no output)"))

    n_functions = len(census.IN_LANE_FUNCTIONS)
    swaps_p, swaps_f, _s = junit_census(junit, "test_a_swapped_identifier_never_widens")
    diff_p, diff_f, _s = junit_census(junit, "test_the_authorized_request_is_not_refused")
    firm_p, firm_f, _s = junit_census(junit, "test_a_claimed_firm_that_disagrees")
    ok_p, ok_f, _s = junit_census(junit, "test_a_reconciling_firm_claim_is_served")
    proj_p, proj_f, _s = junit_census(junit, "test_an_unprojected_grant_refuses")
    rev_p, rev_f, _s = junit_census(junit, "test_a_revoked_grant_is_refused")
    env_p, env_f, _s = junit_census(junit, "test_every_refusal_carries_a_status_envelope")

    print("    (b) six swaps x %d dispatched function(s) this order may open ... %d of %d"
          % (n_functions, swaps_p, swaps_p + swaps_f))
    print("        the sixth function, irpt-status, is OUT OF LANE: 6 of 36 swaps are BLOCKED "
          "and are not counted as passes (row IRPT_BCKEND-W2-S19)")
    print("        difference control -- the authorized request is NOT refused for an "
          "authorization reason ... %d of %d" % (diff_p, diff_p + diff_f))
    arm("b swaps", swaps_p == n_functions * 6 and swaps_f == 0 and diff_f == 0,
        "%d of %d in-lane swaps hold and %d of %d difference controls hold. THE BAR IS 36 of 36 "
        "across six handlers; %d of 36 are measured and 6 of 36 are out of lane, so the arm's "
        "own number is NOT reached. Every refusal was serialised and searched for another firm's "
        "opaque id, another advisor's id, an account outside the grant, another firm's report "
        "and pdf, a client surname, an e-mail address and the refused firm token: 0 bytes of any "
        "of them in any of the %d refusals."
        % (swaps_p, swaps_p + swaps_f, diff_p, diff_p + diff_f, swaps_p, swaps_p))

    print("    (c) a claimed firm that disagrees with the principal -> FIRM_BINDING ... %d of %d"
          % (firm_p, firm_p + firm_f))
    print("        a reconciling claim is NOT an obstacle ......................... %d of %d"
          % (ok_p, ok_p + ok_f))
    arm("c the firm is the principal's", firm_p == n_functions and firm_f == 0 and ok_f == 0,
        "%d of %d functions refuse a request-controlled firm token with FIRM_BINDING and never "
        "echo it; %d of %d serve a reconciling claim" % (firm_p, firm_p + firm_f, ok_p,
                                                         ok_p + ok_f))

    print("    (d) an UNPROJECTED grant refuses rather than serving the empty set it produces "
          "... %d of %d" % (proj_p, proj_p + proj_f))
    print("        and a REVOKED grant does NOT read as an unprojected one ......... %d of %d"
          % (rev_p, rev_p + rev_f))
    arm("d the projection", proj_p == n_functions and proj_f == 0 and rev_f == 0,
        "%d of %d functions refuse UNPROJECTED_GRANT on a grant whose ids never join, and %d of "
        "%d distinguish it from a revoked grant -- the two are indistinguishable in the RESULT "
        "and only the order of the checks tells them apart"
        % (proj_p, proj_p + proj_f, rev_p, rev_p + rev_f))

    arm("b/c/d the envelope", env_p == n_functions and env_f == 0,
        "%d of %d refusals carry a full StatusEnvelope -- operation, one of the nine states, "
        "source dates, SAFE-only actions, a public reason CODE and an opaque correlation id"
        % (env_p, env_p + env_f))
    return junit


# --------------------------------------------------------------------- (e) the deploy
def arm_e():
    print("\n=== ARM (e) DEPLOYED AND VERIFIED ================================")
    print("    NOTHING WAS APPLIED BY THIS CELL, AND THE THREE REASONS ARE INDEPENDENT:")
    print("      1. BUILD INPUTS DO NOT RESOLVE (row IRPT_BCKEND-W2-S21): irpt-ycharts-generate "
          "declares 25 files of which 7 have never existed in this repository, irpt-status "
          "declares 7 of which 5 have not, and irpt-directory-search fails the builder's own "
          "disk->manifest parity check because two functions share one source dir.")
    print("      2. THE EXPORT FUNCTION IS BEING APPLIED BY ANOTHER CELL THIS WINDOW (row "
          "IRPT_BCKEND-W2-S22): the issuer's hand-off states IB-rt-4 is re-applying its "
          "error-path envelope on irpt-export-render from slot ~3.")
    print("      3. THE SHARED CODE HAS NO IN-LANE CARRIER (row IRPT_BCKEND-W2-S24): _authz "
          "reaches the zips through the irpt-common LAYER, whose source dir, build script and "
          "lambda-layer-map.json are outside this order's <paths> -- and the layer was "
          "republished as v5 at 13:08Z today by another cell.")
    print("    A deploy whose input cannot be reproduced, on a function another cell is "
          "applying, is the half-landed state NEVER-2 exists to prevent.")
    blocked("e deployed and verified",
            "0 of 5 roots applied, 0 of 5 CodeSha256 verified, 0 ledger entries opened. BLOCKED "
            "three independent ways; each is a row with disarm owner 2.0.0_SA_COO~B. The code is "
            "COMMITTED and the deploy is the issuer's to sequence.")


# --------------------------------------------------------------------- (f) the principal
def arm_f():
    print("\n=== ARM (f) THE PRINCIPAL =======================================")
    if not os.path.isfile(GATED):
        blocked("f the principal", "neither a minted principal nor a HUMAN-GATED record exists")
        return
    with open(GATED, "r", encoding="utf-8") as fh:
        text = fh.read()
    # The arm's own rule names what the record must carry. Checked as literal strings, so a
    # reworded record fails rather than being read charitably.
    required = {
        "the verdict": "`HUMAN-GATED`",
        "which console/CLI": "313476888478",
        "which user": "opal-users-v2",
        "which claim": "firmId",
        "the signing path (by NAME)": "opal/auth/jwt-private-key",
        "the verifying path (by NAME)": "opal/auth/jwt-public-key",
        "the expected served reading": "HTTP 200",
        "the expected refused reading": "FIRM_BINDING",
        "the delete is verified": "consistent-read",
    }
    found = {k: (v in text) for k, v in required.items()}
    for k, v in required.items():
        print("    [%s] %-30s %s" % ("x" if found[k] else " ", k, v))
    # AND NO SECRET VALUE: the record names secrets and must not carry one.
    leaked = [tok for tok in ("BEGIN PRIVATE KEY", "BEGIN RSA", "eyJhbGciOi") if tok in text]
    print("    secret VALUES in the record: %d (names only is the bound)" % len(leaked))
    arm("f the principal", all(found.values()) and not leaked,
        "HUMAN-GATED: %d of %d required elements present and 0 secret values. The arm's own rule "
        "admits this as a PASS of that rule, never as a skip -- a mint path EXISTS and a worker "
        "may not walk it (out of <paths>, a write to the production auth plane, and the "
        "alternative is using a private key to mint itself an identity)."
        % (sum(found.values()), len(found)))


# --------------------------------------------------------------------- (g) the envelope
def arm_g(junit):
    print("\n=== ARM (g) ENVELOPE CONFORMANCE, SERVED ========================")
    import test_guarded_entries as T

    # The in-process half, measured: which operations answer in the v1 response envelope at all.
    conforming, refusing, total = [], [], 0
    for function in sorted(T.entries()):
        route_key, handler = T.entries()[function]
        entry_obj = handler.__irpt_entry__
        restore = T._install_recorded_deps(entry_obj)
        try:
            operation = T._routes()[route_key]["operation"]
            answer = handler(T.base_event(route_key, operation), None)
        finally:
            restore()
        total += 1
        if answer.get("ok") is False:
            refusing.append((function, answer["status"]["public_reason_code"]))
        else:
            ok, reason = _validates(operation, answer)
            conforming.append((function, operation, ok, reason))

    print("    IN PROCESS, against the v1 response contracts:")
    for function, operation, ok, reason in conforming:
        print("      %-26s %-20s %s" % (function, operation,
                                        "CONFORMS" if ok else "DOES NOT: %s" % reason[:90]))
    for function, code in refusing:
        print("      %-26s refused %-14s -- a REFUSAL cannot validate against a RESPONSE "
              "contract (row IRPT_BCKEND-W2-S25)" % (function, code))
    print("      served-and-conforming: %d of %d in-lane function(s); refusing for their own "
          "reason: %d" % (sum(1 for c in conforming if c[2]), total, len(refusing)))

    ver_p, ver_f, _s = junit_census(junit, "test_a_mismatched_contract_version_is_refused")
    abs_p, abs_f, _s = junit_census(junit, "test_a_missing_contract_version_header")
    print("    the X-Contract-Version check, IN PROCESS: mismatched refused CONTRACT_VERSION "
          "%d of %d; absent refused too %d of %d" % (ver_p, ver_p + ver_f, abs_p, abs_p + abs_f))
    print("    and it is refused with the STORAGE LOADERS REMOVED, which is the proof that "
          "nothing was read before the version was checked.")

    blocked("g envelope conformance SERVED",
            "0 of 11 DEPLOYED responses measured: nothing was deployed by this cell (arm (e)), "
            "so the version check is COMMITTED AND NOT SERVED and no deployed response exists to "
            "validate. IN PROCESS: %d of %d in-lane functions answer in the v1 response envelope "
            "and %d of %d refuse the mismatched version with CONTRACT_VERSION. The amendment's "
            "denominator -- routes with a DEPLOYED handler at this HEAD -- is 0 until the deploy "
            "lands, and a 0 of 0 is VACUOUS, not a pass."
            % (sum(1 for c in conforming if c[2]), total, ver_p, ver_p + ver_f))


def _validates(operation, answer):
    try:
        import jsonschema
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError as exc:                         # pragma: no cover
        return False, "jsonschema/referencing unavailable: %s" % exc
    path = os.path.join(V1, "responses", "%s.response.schema.json" % operation)
    if not os.path.isfile(path):
        return False, "no response contract is published for %s" % operation
    with open(path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    resources = []
    for fn in sorted(os.listdir(V1)):
        if fn.endswith(".schema.json"):
            with open(os.path.join(V1, fn), "r", encoding="utf-8") as fh:
                resources.append(("../" + fn, Resource(contents=json.load(fh),
                                                       specification=DRAFT202012)))
    registry = Registry().with_resources(resources)
    try:
        jsonschema.Draft202012Validator(schema, registry=registry).validate(answer)
    except jsonschema.ValidationError as exc:
        return False, str(exc.message)
    return True, ""


def main():
    print("BATTERY IB-rt-2 -- GUARD THE SIX")
    print("repo: %s" % REPO)
    print("subjects: the published route file, each function's DECLARED entry point, the real "
          "_authz guard, Enforcer and scope resolver")
    arm_a()
    junit = arm_bcd()
    arm_e()
    arm_f()
    arm_g(junit)

    print("\n=== SUMMARY ======================================================")
    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    for n, ok, d in RESULTS:
        print("  %-32s %s" % (n, "PASS" if ok else "FAIL/BLOCKED"))
    print("  %d of %d arms PASS" % (passed, len(RESULTS)))
    if passed == len(RESULTS):
        print("\nIBRT2-SIX-GUARDED")
    else:
        print("\nBLOCKED: %d of %d arms FAIL or are BLOCKED -- the token is withheld."
              % (len(RESULTS) - passed, len(RESULTS)))
        print("A battery that prints its token beside a blocked arm is not evidence, it is a "
              "signature. The blocked arms' rows are the deliverable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
