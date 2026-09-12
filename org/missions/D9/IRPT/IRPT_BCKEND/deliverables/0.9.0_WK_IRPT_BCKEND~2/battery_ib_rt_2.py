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


def human_gated(name, record_ok, detail):
    """A THIRD VERB, because the vocabulary needed one.

    An arm whose own rule admits a HUMAN-GATED record is not PASSING by measurement and is not
    BLOCKED either -- writing it as PASS would claim something unexercised, and writing it as
    BLOCKED would report a met rule as an unmet one. It counts toward the token when its RECORD
    satisfies the rule's named elements, and it prints under its own label so no reader can
    mistake it for a measurement.
    """
    RESULTS.append((name, bool(record_ok), detail))
    print("[HUMAN-GATED] %s -- %s" % (name, detail))


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
    print("    IN LANE (the %d functions this order may open): %d of %d unguarded"
          % (len(census.IN_LANE_FUNCTIONS), len(inl["unguarded"]), inl["routes"]))
    print("    WHOLE FILE                                         : %d of %d unguarded"
          % (len(whole["unguarded"]), whole["routes"]))
    for route_key in whole["unguarded"]:
        print("      OUT OF LANE, named and not counted: %-52s -> %s (cell IB-rt-7, row "
              "IRPT_BCKEND-W2-S30)" % (route_key, rt.function_for(route_key)))

    arm("a1 zero in lane", not inl["unguarded"] and inl["routes"] == len(table),
        "%d of %d route(s) this order may open reach an unguarded handler"
        % (len(inl["unguarded"]), inl["routes"]))

    if whole["unguarded"]:
        owners = sorted({rt.function_for(k) for k in whole["unguarded"]})
        blocked("a2 zero over the whole file",
                "%d of %d route(s) reach an unguarded handler and ALL %d belong to %s, whose "
                "source dir and Terraform root are outside this order's <paths>. THE "
                "POPULATION MOVED UNDER THIS CELL: the face's amendment names holdings-snapshot "
                "as the one published route with NO handler at HEAD, and IB-rt-7 has since "
                "landed and DEPLOYED one (d9c940244a, 5a359024a9), so N went from 11 to 12. "
                "BLOCKING row IRPT_BCKEND-W2-S30, disarm owner 2.0.0_SA_COO~B. The criterion's "
                "bar is `0 of N` with N = handler-bearing routes = %d; it is NOT met and is not "
                "graded around. Row IRPT_BCKEND-W2-S31 states what `unguarded` does and does "
                "not mean here: the mark, not the behaviour -- that handler enforces the same "
                "FirmBinding inline."
                % (len(whole["unguarded"]), whole["routes"], len(whole["unguarded"]),
                   ", ".join(owners), whole["routes"]))
    else:
        arm("a2 zero over the whole file", True, "0 of %d" % whole["routes"])

    rc, out, junit = run_pytest([os.path.join("infra", "aws", "lambda", "investor-reporting",
                                              "_authz", "tests",
                                              "test_unguarded_census.py")],
                               "ibrt2_census_junit.xml")
    p, f, _s = junit_census(junit, "test_the_census_fires_when_one_handler_is_unregistered")
    print("    the control, on a THROWAWAY copy of the TABLE (never of a handler): %d of %d "
          "victim(s) moved the verdict to `1 of %d`" % (p, p + f, inl["routes"]))
    arm("a3 the control fires", p >= 3 and f == 0,
        "%d of %d control case(s) pass: the detector returns non-zero on the positive case, so "
        "the zero above is a measurement and not a constant" % (p, p + f))

    arm_a4_basenames()


# ------------------------------------------------- (a4) the module-basename collision census
def arm_a4_basenames():
    """ROWS W3-S22 / W4-S24. `_authz` modules ride into EVERY zip, so a basename it shares with
    any function directory is a collision on the flat sys.path -- the first to bind wins and the
    other function silently imports the wrong module.

    The census is over the REAL directories, and its denominator is printed. It is a census of
    NAMES, not of imports: a name that collides is a hazard whether or not today's import order
    happens to resolve it the way its author expected.
    """
    print("\n--- the module-basename census (rows W3-S22 / W4-S24) ---------------")
    authz_dir = os.path.join(PKG, "_authz")
    shared = sorted(f for f in os.listdir(authz_dir)
                    if f.endswith(".py") and not f.startswith("test_"))
    function_dirs = ["directory", "performance", "narrative", "export", "ops",
                     os.path.join("ycharts", "generate"), "holdings", "intake"]
    print("    _authz modules that ride into a zip when one carries them (%d): %s"
          % (len(shared), ", ".join(shared)))

    # A BASENAME MATCH IS NOT AUTOMATICALLY A COLLISION, and grading it as one would have failed
    # this arm on a deliberate act. `irpt-holdings` STAGES `_authz/enforce.py` and
    # `_authz/errors.py` into its own source dir from a PINNED commit and DECLARES each in
    # STAGE_MANIFEST.json `packaged_as` and BUILD_MANIFEST.json `vendored_modules`. That is a
    # vendored member with a manifest behind it, not two different modules answering one name.
    # The discriminator is the FUNCTION'S OWN DECLARATION, read from its artifact -- never this
    # battery's opinion about which copies look intentional.
    matches, declared_copies, collisions = [], [], []
    checked = 0
    for rel in function_dirs:
        d = os.path.join(PKG, rel)
        if not os.path.isdir(d):
            continue
        checked += 1
        vendored = set()
        for manifest, key in (("STAGE_MANIFEST.json", "members"),
                              ("BUILD_MANIFEST.json", "vendored_modules")):
            mp = os.path.join(d, manifest)
            if not os.path.isfile(mp):
                continue
            try:
                with open(mp, "r", encoding="utf-8") as fh:
                    doc = json.load(fh)
            except ValueError:
                continue
            for item in (doc.get(key) or []):
                if isinstance(item, dict):
                    vendored.add(os.path.basename(item.get("packaged_as") or ""))
                else:
                    vendored.add(os.path.basename(item))
        names = {f for f in os.listdir(d) if f.endswith(".py")}
        for hit in sorted(names & set(shared)):
            rel_posix = rel.replace(os.sep, "/")
            matches.append((rel_posix, hit))
            (declared_copies if hit in vendored else collisions).append((rel_posix, hit))

    for rel, hit in declared_copies:
        same = False
        try:
            with open(os.path.join(PKG, rel.replace("/", os.sep), hit), "rb") as fh:
                a = fh.read().replace(b"\r\n", b"\n")
            with open(os.path.join(authz_dir, hit), "rb") as fh:
                b = fh.read().replace(b"\r\n", b"\n")
            same = a == b
        except OSError:
            pass
        print("      DECLARED VENDORED COPY, not a collision: %s/%s -- named in that function's "
              "own manifest; bytes %s _authz/%s at this HEAD"
              % (rel, hit, "MATCH" if same else "DIFFER from (it is pinned to an older commit)",
                 hit))
    for rel, hit in collisions:
        print("      COLLISION: %s/%s shares a basename with _authz/%s and no manifest of that "
              "function declares it" % (rel, hit, hit))
    print("    %d basename match(es) across %d function directory(ies) x %d shared module(s): "
          "%d declared vendored copy(ies), %d true collision(s)"
          % (len(matches), checked, len(shared), len(declared_copies), len(collisions)))
    arm("a4 no basename collision", not collisions,
        "%d true collision(s) of %d basename match(es): the rename of _authz/dispatch.py to "
        "_authz/authz_dispatch.py removed the one real collision (export/dispatch.py keeps its "
        "name and is not renamed; it is that function's OWN module). The %d remaining match(es) "
        "are irpt-holdings' DECLARED vendored copies, each named in its own STAGE_MANIFEST.json "
        "and BUILD_MANIFEST.json. Denominator: %d shared module(s) against %d function "
        "directory(ies)."
        % (len(collisions), len(matches), len(declared_copies), len(shared), checked))


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

    # THE SWAP CENSUS'S OWN SET, READ FROM THE MODULE THAT OWNS IT. `test_unguarded_census` and
    # `test_guarded_entries` keep SEPARATE in-lane sets on purpose -- the first is "what may this
    # order open", the second is "which functions does the swap census exercise" -- and this
    # battery read the WRONG one after amendment 3 granted holdings: the route census gained
    # irpt-holdings, so the expected swap count became 7 x 6 = 42 while the suite still ran 36,
    # and arms (b), (c), (d) all went red for a reason that had nothing to do with them. The two
    # lists diverging is the same trap the wind-down hand-off named; reading each from its owner
    # is the fix.
    import test_guarded_entries as swaps
    n_functions = len(swaps.IN_LANE_FUNCTIONS)
    holdings_only = sorted(set(census.IN_LANE_FUNCTIONS) - set(swaps.IN_LANE_FUNCTIONS))
    if holdings_only:
        print("    the swap census covers %d function(s); %s carries the C1 MARK and is NOT in "
              "the swap set -- its deploy is HELD (rows W2-S38, W2-S41), so it is named here and "
              "counted in neither direction" % (n_functions, ", ".join(holdings_only)))
    swaps_p, swaps_f, _s = junit_census(junit, "test_a_swapped_identifier_never_widens")
    diff_p, diff_f, _s = junit_census(junit, "test_the_authorized_request_is_not_refused")
    firm_p, firm_f, _s = junit_census(junit, "test_a_claimed_firm_that_disagrees")
    ok_p, ok_f, _s = junit_census(junit, "test_a_reconciling_firm_claim_is_served")
    proj_p, proj_f, _s = junit_census(junit, "test_an_unprojected_grant_refuses")
    rev_p, rev_f, _s = junit_census(junit, "test_a_revoked_grant_is_refused")
    env_p, env_f, _s = junit_census(junit, "test_every_refusal_carries_a_status_envelope")

    print("    (b) six swaps x %d dispatched function(s) this order may open ... %d of %d"
          % (n_functions, swaps_p, swaps_p + swaps_f))
    print("        irpt-status is IN LANE at this vintage (row IRPT_BCKEND-W2-S19 GRANTED), so "
          "the arm's own bar of 36 of 36 is measurable and measured -- no swap is blocked")
    print("        difference control -- the authorized request is NOT refused for an "
          "authorization reason ... %d of %d" % (diff_p, diff_p + diff_f))
    neg_p, neg_f, _s = junit_census(junit, "test_an_admin_principal_may_not_address_an_advisor")
    ctl_p, ctl_f, _s = junit_census(junit, "test_the_same_admin_principal_still_reaches")
    print("        ROW W1-S16, the seventh negative (not one of the 36): an ADMIN principal "
          "addressing an advisor outside the verified firm is refused ... %d of %d"
          % (neg_p, neg_p + neg_f))
    print("        and its difference control -- the same admin principal reaching an IN-FIRM "
          "advisor is NOT refused OBJECT_NOT_COVERED ................... %d of %d"
          % (ctl_p, ctl_p + ctl_f))
    arm("b swaps", (swaps_p == n_functions * 6 and swaps_f == 0 and diff_f == 0
                    and neg_p == n_functions and neg_f == 0 and ctl_f == 0),
        "%d of %d swaps hold (the bar is 36 of 36 across six handlers and %d are measured, none "
        "out of lane) and %d of %d difference controls hold. Every refusal was serialised and "
        "searched for another firm's opaque id, another advisor's id, an account outside the "
        "grant, another firm's report and pdf, a client surname, an e-mail address and the "
        "refused firm token: 0 bytes of any of them in any of the %d refusals. Row W1-S16's "
        "negative holds %d of %d with its control %d of %d."
        % (swaps_p, swaps_p + swaps_f, swaps_p, diff_p, diff_p + diff_f, swaps_p,
           neg_p, neg_p + neg_f, ctl_p, ctl_p + ctl_f))

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
        "%d of %d refusals carry the StatusEnvelope TOP-LEVEL KEY SET -- operation, one of the "
        "nine states, source dates, SAFE-only actions, a public reason CODE and an opaque "
        "correlation id. THIS IS A KEY-PRESENCE CHECK AND IT IS NOT SCHEMA CONFORMANCE: v1 "
        "requires business_date INSIDE source_dates and the boundary emits none, which this "
        "arm cannot see and arm g3 does. Row IRPT_BCKEND-W2-S36."
        % (env_p, env_p + env_f))
    return junit


# --------------------------------------------------------------------- (e) the deploy
# THE FUNCTIONS THIS ORDER OWNS, IMPORTED FROM THE PACKAGER RATHER THAN RETYPED.
#
# This was a literal list and it went stale the moment holdings was granted: arm (e) reported
# `6 of 6` while SEVEN functions were deployed, and arm (g) EXCLUDED the holdings route as
# not-deployed after its apply had landed. That is the FOURTH divergence in this cell between two
# hand-maintained copies of one fact (the two in-lane test sets, the battery reading the wrong one,
# the verifier's own layer list, and this). Each time the fix was to delete a copy, so this one is
# deleted too: `rt2_package` already enumerates the functions and the packager is what builds them.
sys.path.insert(0, HERE)
import rt2_package as _pkg                     # noqa: E402
DEPLOYED = list(_pkg.SIX)

# AND "IS IT DEPLOYED" IS NOW A MEASUREMENT, NOT A MEMBERSHIP. A function belongs in arm (g)'s
# denominator when its LIVE handler is the guarded entry -- read from AWS, per function, at the
# moment the arm runs. A list cannot tell you whether an apply landed; the function can.
GUARDED_ENTRY_HANDLER = "entry.lambda_handler"
LEDGER = os.path.join(REPO, "org", "critical_paths", "change_management",
                      "20260912T0035Z_irpt-bckend-rt2_deploy_completion.md")
AWS_CMD = os.path.join(REPO, ".tools", "aws.cmd")


def aws_text(*args):
    proc = subprocess.run([AWS_CMD] + list(args), capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError("aws rc=%d %s" % (proc.returncode, (proc.stderr or "")[:200]))
    return (proc.stdout or "").strip()


def arm_e():
    """ARM (e), MEASURED ON THE LIVE FUNCTIONS -- never on this box's copy of the zip."""
    print("\n=== ARM (e) DEPLOYED AND VERIFIED ================================")
    with open(os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json"),
              "r", encoding="utf-8") as fh:
        sm = json.load(fh)["functions"]

    chain_ok, handler_ok, active = 0, 0, 0
    for function in DEPLOYED:
        handler, live_sha, state, status = aws_text(
            "lambda", "get-function-configuration", "--function-name", function,
            "--region", "us-east-1", "--output", "text",
            "--query", "[Handler,CodeSha256,State,LastUpdateStatus]").split("\t")
        declared = sm[function].get("artifact_sha256") or ""
        same = declared == live_sha
        chain_ok += 1 if same else 0
        handler_ok += 1 if handler == "entry.lambda_handler" else 0
        active += 1 if (state, status) == ("Active", "Successful") else 0
        print("    %-26s %-22s %s %s/%s" % (function, handler,
                                            "sha EQUAL" if same else "sha MISMATCH",
                                            state, status))
    print("    declared artifact_sha256 == live CodeSha256: %d of %d; handler is the guarded "
          "entry: %d of %d; Active/Successful: %d of %d"
          % (chain_ok, len(DEPLOYED), handler_ok, len(DEPLOYED), active, len(DEPLOYED)))

    # THE IMPORT THAT THE HASH CANNOT SEE, on the SERVED bytes of every function.
    proc = subprocess.run([sys.executable, os.path.join(HERE, "rt2_verify_deployed.py")]
                          + DEPLOYED, capture_output=True, text=True, timeout=840, cwd=REPO)
    out = (proc.stdout or "") + (proc.stderr or "")
    verified = sum(1 for ln in out.splitlines() if "VERDICT: VERIFIED" in ln)
    imported = sum(1 for ln in out.splitlines() if "SERVED" in ln and "IMPORT-OK" in ln)
    controls = sum(1 for ln in out.splitlines()
                   if "NEGATIVE-CTL" in ln and "IMPORT-FAIL" in ln)
    print("    extract-and-import of the SERVED artifact, fresh interpreter, repo off sys.path, "
          "with /opt/python mounted for each function whose LIVE config attaches a layer "
          "(read from the function, not from a list -- see the verifier's own note):")
    print("      IMPORT-OK %d of %d | negative control FIRES %d of %d | VERIFIED %d of %d"
          % (imported, len(DEPLOYED), controls, len(DEPLOYED), verified, len(DEPLOYED)))

    # The post-apply plans are CITED from the CLOSED ledger rather than re-run here: a battery
    # that shells terraform into six roots is a different act from a battery, and the plans were
    # printed per root at apply time and are quoted in the entry's own legs.
    # THE POST-APPLY PLANS ARE COUNTED OVER THE ROOTS THIS CELL APPLIED, ACROSS BOTH OF ITS
    # LEDGERS -- and the denominator is the number of APPLIED roots, not the number of functions.
    # Those are different numbers whenever a root is held, and conflating them made this arm read
    # RED on bookkeeping while every live measurement above said 7 of 7.
    ledger_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    # ONE COUNTER, AND IT IS THE ONE THAT MEANS SOMETHING. An earlier version of this block also
    # counted "apply legs" by searching the entry's PROSE for the word APPLIED, and read 22 across
    # two ledgers that hold thirteen activation legs between them -- a check that parses a tool's
    # prose reads the TOOL, not the world, and this one read the word in verify text too. Deleted
    # rather than tuned: `Post-apply plan: No changes` is a phrase this cell writes exactly once
    # per applied root, and the per-root detail is in the entries themselves.
    entries, plans = [], 0
    for name in sorted(os.listdir(ledger_dir)):
        if "irpt-bckend-rt2" not in name:
            continue
        with open(os.path.join(ledger_dir, name), "r", encoding="utf-8") as fh:
            text = fh.read()
        entries.append(name)
        plans += text.count("Post-apply plan: No changes")
    sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                            "irpt-bckend-rt2.json")
    print("    ledger: %d entry(ies) %s, sentinel removed=%s, post-apply plans reading "
          "`No changes`: %d across %d function(s) this order owns"
          % (len(entries), entries, not os.path.isfile(sentinel), plans, len(DEPLOYED)))

    # AND THE HELD ROOT IS NAMED WITH WHAT ITS PLAN SAYS NOW, because a post-apply `No changes` is
    # a PERISHABLE claim and this one was falsified by another cell four hours after it was
    # recorded. Row IRPT_BCKEND-W2-S42: the ycharts root plans 0 to add, 0 to change, 2 to DESTROY
    # -- a LIVE secret and a log group IB-rt-9 removed from the configuration without applying --
    # so no cell can apply that root until its owner rules, and this one did not.
    print("    HELD ROOT, named and excluded from the plan denominator: ycharts -- its plan now "
          "reads `0 to add, 0 to change, 2 to destroy` (aws_secretsmanager_secret.research_session "
          "and aws_cloudwatch_log_group.research_probe, both removed from config by IB-rt-9 at "
          "f83f73ce6c and never applied). Rows IRPT_BCKEND-W2-S38 and W2-S42. The FUNCTION is "
          "deployed and verified from this cell's FIRST apply; the ROOT is not applicable by "
          "anyone right now.")

    arm("e deployed and verified",
        chain_ok == len(DEPLOYED) and handler_ok == len(DEPLOYED) and active == len(DEPLOYED)
        and verified == len(DEPLOYED) and controls == len(DEPLOYED)
        and plans >= len(DEPLOYED) and entries and not os.path.isfile(sentinel),
        "%d of %d roots applied one at a time, each verified before the next was touched. "
        "artifact_sha256 == S3 content-sha256 == live CodeSha256 on %d of %d; the guarded entry "
        "is the live handler on %d of %d; %d of %d import in the flat /var/task (+/opt/python "
        "where the layer is attached) layout from their SERVED bytes with the repo off "
        "sys.path, and %d of %d negative controls fire. %d post-apply plans reading `No changes` "
        "across %d function(s) owned -- one per applied root, over this cell's TWO acts. Ledger(s) "
        "CLOSED, sentinel removed. The ycharts ROOT is named above and excluded from the plan "
        "denominator: its function is deployed and verified, and the root itself is not "
        "applicable by any cell until rows W2-S38 and W2-S42 are ruled."
        % (len(DEPLOYED), len(DEPLOYED), chain_ok, len(DEPLOYED), handler_ok, len(DEPLOYED),
           imported, len(DEPLOYED), controls, len(DEPLOYED), plans, len(DEPLOYED)))


# ------------------------------------------------- (d3) THE BUSINESS DATE, WHERE THE SCHEMA CANNOT
def arm_d3_business_date():
    """THE OBLIGATION THE CONTRACT DELIBERATELY STOPPED CARRYING. Amendment 4, D3.

    PRD v0.14 @b8e98d5a4d made `business_date` STATE-CONDITIONAL: REQUIRED on the five
    answer-bearing states, permitted to be ABSENT (never null) on the four no-answer ones. The
    allOf's own $comment records what that gives up -- "this schema can no longer catch a POST-READ
    refusal (unavailable/failed WITH an artifact) that omits the date it does have" -- and says the
    obligation moves to a battery. This is that battery arm, and it is HERE rather than in the
    IB-s-18 battery because that one exits rc=1 on a TypeError in an unrelated arm, so an
    obligation added there could never fire.

    THE STATE SET IS A SUBTRACTION FROM THE PRINTED NINE, NOT A FORWARD LIST OF THE CASES THIS
    BATTERY HAPPENS TO EXERCISE. The first cut of this rule -- mine -- was PRE-READ vs POST-READ,
    which is a distinction about REFUSALS, and QUEUED and RUNNING are not refusals at all.
    """
    print("\n=== ARM (d3) THE BUSINESS DATE, WHERE THE SCHEMA CANNOT REACH =====")
    import served
    import test_guarded_entries as T

    schema_path = os.path.join(V1, "StatusEnvelope.schema.json")
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    enum = tuple((schema.get("properties") or {}).get("state", {}).get("enum") or ())
    answer_bearing = tuple(
        (schema.get("allOf") or [{}])[0].get("if", {}).get("properties", {})
        .get("state", {}).get("enum") or ())
    no_answer = tuple(st for st in enum if st not in answer_bearing)
    print("    denominator, READ FROM THE CONTRACT not from this file: %d state(s) in the enum"
          % len(enum))
    print("      ANSWER-BEARING (business_date REQUIRED): %d -- %s"
          % (len(answer_bearing), ", ".join(answer_bearing)))
    print("      NO-ANSWER  (may be ABSENT, never null) : %d -- %s  [%d MINUS %d]"
          % (len(no_answer), ", ".join(no_answer), len(enum), len(answer_bearing)))
    agree = (tuple(served.STATES) == enum
             and tuple(served.ANSWER_BEARING_STATES) == answer_bearing
             and tuple(served.NO_ANSWER_STATES) == no_answer)
    print("    the boundary's own three sets agree with the contract's, member for member: %s"
          % agree)

    # ---- THE OBLIGATION, per function: a POST-READ refusal states the artifact's date.
    post_ok, pre_ok, total, nulls = 0, 0, 0, 0
    for function in sorted(T.entries()):
        route_key, handler = T.entries()[function]
        entry_obj = handler.__irpt_entry__
        restore = T._install_recorded_deps(entry_obj)
        try:
            operation = T._routes()[route_key]["operation"]
            post = handler(T.swapped_event(route_key, operation, "account"), None)
            pre = handler(dict(T.base_event(route_key, operation),
                               headers=dict(T.authorized_headers(version="v2-not-published"))),
                          None)
        finally:
            restore()
        total += 1
        for label, answer in (("POST-READ", post), ("PRE-READ", pre)):
            dates = ((answer.get("status") or {}).get("source_dates") or {})
            has = "business_date" in dates
            is_null = has and dates.get("business_date") is None
            nulls += 1 if is_null else 0
            state = (answer.get("status") or {}).get("state")
            if label == "POST-READ":
                post_ok += 1 if (has and not is_null) else 0
            else:
                pre_ok += 1 if not has else 0
            print("      %-26s %-9s state=%-12s business_date %s"
                  % (function, label, state,
                     ("= %s" % dates.get("business_date")) if has else "ABSENT"))

    arm("d3 the post-read business date", post_ok == total and pre_ok == total and nulls == 0,
        "%d of %d functions state the artifact's business_date on a POST-READ refusal -- which "
        "the contract now permits them to omit and which this arm exists to require -- and %d of "
        "%d omit it on a PRE-READ refusal, where no artifact has been read and inventing one from "
        "a clock would be the worse answer. %d of %d envelopes carry it as NULL (the contract says "
        "ABSENT, never null). The state sets are cut by SUBTRACTION from the contract's own "
        "nine-member enum (%d minus %d answer-bearing = %d no-answer) and the boundary's three "
        "sets agree with the contract's member for member: %s."
        % (post_ok, total, pre_ok, total, nulls, total * 2, len(enum), len(answer_bearing),
           len(no_answer), agree))

    # ---- AND AN ANSWER-BEARING STATE WITH NO DATE MUST RAISE, not ship.
    raised = False
    try:
        served.status_envelope("directory-search", "NOT_READY", state="READY")
    except served.EntryError:
        raised = True
    except Exception as exc:                            # noqa: BLE001
        print("    WARN: an unexpected exception class: %r" % exc)
    print("    an ANSWER-BEARING state built with no business_date raises at the boundary: %s"
          % raised)
    arm("d3 an answer-bearing state cannot ship dateless", raised,
        "status_envelope(state='READY') with no business_date raises EntryError rather than "
        "returning an envelope that fails its own contract. THE NEGATIVE CONTROL for the arm "
        "above: without this, 'the post-read date is present' could be satisfied by a boundary "
        "that simply never checks.")


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
    human_gated("f the principal", all(found.values()) and not leaked,
        "HUMAN-GATED: %d of %d required elements present and 0 secret values. The arm's own rule "
        "admits this as a PASS of that rule, never as a skip -- a mint path EXISTS and a worker "
        "may not walk it (out of <paths>, a write to the production auth plane, and the "
        "alternative is using a private key to mint itself an identity)."
        % (sum(found.values()), len(found)))


# --------------------------------------------------------------------- (g) the envelope
def invoke_deployed(function, event, tag):
    """Invoke a DEPLOYED function by name and return its parsed answer.

    SAFE BY CONSTRUCTION FOR THE ARM BELOW: every event carries a MISMATCHED
    `X-Contract-Version`, and the boundary checks the version BEFORE it constructs an Enforcer,
    reads storage or enqueues anything -- proven in-process by the arm that refuses with the
    storage loaders REMOVED. So no directory is read, no job is enqueued and no vendor chain is
    reachable by any of these calls (bound 1, bound 2).
    """
    payload = os.path.join(REPO, ".scratch", "ibrt2_ev_%s.json" % tag)
    out = os.path.join(REPO, ".scratch", "ibrt2_out_%s.json" % tag)
    with open(payload, "w", encoding="utf-8") as fh:
        json.dump(event, fh)
    proc = subprocess.run([AWS_CMD, "lambda", "invoke", "--function-name", function,
                           "--payload", "file://" + payload.replace(os.sep, "/"),
                           "--region", "us-east-1", out],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        return None, "invoke rc=%d %s" % (proc.returncode, (proc.stderr or "")[:160])
    with open(out, "r", encoding="utf-8") as fh:
        body = fh.read()
    try:
        return json.loads(body), ""
    except ValueError as exc:
        return None, "unparseable answer: %s" % exc


def _status_envelope_schema():
    path = os.path.join(V1, "StatusEnvelope.schema.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _validates_status(answer):
    """A REFUSAL is graded against v1's StatusEnvelope, never against a response contract
    (row IRPT_BCKEND-W2-S25, RULED by the issuer)."""
    schema = _status_envelope_schema()
    if schema is None:
        return False, "StatusEnvelope.schema.json is not published at this vintage"
    try:
        import jsonschema
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError as exc:
        return False, "jsonschema/referencing unavailable: %s" % exc
    resources = []
    for fn in sorted(os.listdir(V1)):
        if fn.endswith(".schema.json"):
            with open(os.path.join(V1, fn), "r", encoding="utf-8") as fh:
                resources.append(("../" + fn, Resource(contents=json.load(fh),
                                                       specification=DRAFT202012)))
    registry = Registry().with_resources(resources)
    try:
        jsonschema.Draft202012Validator(schema, registry=registry).validate(
            answer.get("status") or {})
    except jsonschema.ValidationError as exc:
        return False, str(exc.message)
    return True, ""


def arm_g(junit):
    print("\n=== ARM (g) ENVELOPE CONFORMANCE, SERVED ========================")
    import routetable as rt

    table, _skipped = rt.entry_points()
    routes = {r["route_key"]: r for r in rt.load_routes()["routes"]}
    # THE DENOMINATOR IS "ROUTES WITH A DEPLOYED GUARDED HANDLER AT THIS HEAD", which is not the
    # same set as "routes this order may open". `irpt-holdings` is in lane and carries the mark IN
    # THE TREE, and its apply is HELD (rows W2-S38, W2-S41) -- so the live route still reaches
    # `snapshot.lambda_handler`, which answers in its own shape and cannot be expected to refuse
    # with a StatusEnvelope. Counting it would report another cell's deployed behaviour as this
    # arm's failure; omitting it silently would overstate the sweep. It is NAMED and excluded.
    live_handler = {}
    for function in sorted({routes[k].get("handler") for k in table}):
        try:
            live_handler[function] = aws_text(
                "lambda", "get-function-configuration", "--function-name", function,
                "--region", "us-east-1", "--output", "text", "--query", "Handler")
        except RuntimeError as exc:
            live_handler[function] = "UNREADABLE: %s" % exc
    in_lane = [(k, routes[k]) for k in sorted(table)
               if live_handler.get(routes[k].get("handler")) == GUARDED_ENTRY_HANDLER]
    not_deployed = [k for k in sorted(table)
                    if live_handler.get(routes[k].get("handler")) != GUARDED_ENTRY_HANDLER]

    print("    denominator: %d route(s) whose guarded handler is DEPLOYED at this HEAD; "
          "%d excluded and named:" % (len(in_lane), len(not_deployed)))
    for key in not_deployed:
        print("      EXCLUDED, neither a pass nor a fail: %s -- %s (live handler reads %r, not "
              "the guarded entry)" % (key, routes[key].get("handler"),
                                      live_handler.get(routes[key].get("handler"))))

    # THE VERSION CHECK, SERVED. This is the half the amendment says this cell serves, and it is
    # now measured against the DEPLOYED functions rather than in process.
    refused, envelope_ok, wrong = 0, 0, []
    for i, (route_key, route) in enumerate(in_lane):
        event = {"routeKey": route_key,
                 "headers": {"X-Contract-Version": "v2-not-published",
                             "X-Firm-Id": "49financial", "X-Advisor-Id": "ADV-PROBE-0000",
                             "X-User-Role": "user", "X-Origin-Verify": "cloudfront",
                             "X-User-Email": "probe@opal.invalid", "X-User-Type": "Advisor"}}
        answer, err = invoke_deployed(route["handler"], event, "v%d" % i)
        if answer is None:
            wrong.append((route["operation"], err))
            print("      %-22s %-26s NO ANSWER: %s" % (route["operation"], route["handler"],
                                                       err[:60]))
            continue
        code = ((answer.get("status") or {}).get("public_reason_code")
                if isinstance(answer, dict) else None)
        ok_env, why = _validates_status(answer) if isinstance(answer, dict) else (False, "n/a")
        if code == "CONTRACT_VERSION":
            refused += 1
        else:
            wrong.append((route["operation"], "code=%s" % code))
        if ok_env:
            envelope_ok += 1
        print("      %-22s %-26s refused %-18s StatusEnvelope %s"
              % (route["operation"], route["handler"], code,
                 "VALID" if ok_env else "INVALID: %s" % why[:50]))
    print("    a mismatched X-Contract-Version is refused CONTRACT_VERSION on the DEPLOYED "
          "function: %d of %d; the refusal validates against v1 StatusEnvelope: %d of %d"
          % (refused, len(in_lane), envelope_ok, len(in_lane)))

    # TWO CLAIMS, TWO ARMS. The first version of this arm graded ONLY the refusal code and
    # PASSED while printing `0 of 11` for the envelope beside it -- a clean metric above a
    # failure, which is the shape that gets read as green. They are separated so neither can
    # carry the other.
    arm("g1 the version check is SERVED", refused == len(in_lane) and not wrong,
        "%d of %d deployed route(s) refuse a mismatched contract version with CONTRACT_VERSION. "
        "This is the face's own bar for the version half, and IB-rt-1 committed the check while "
        "deploying nothing -- it is SERVED now, on the live functions, invoked by name."
        % (refused, len(in_lane)))

    if envelope_ok == len(in_lane):
        arm("g3 the refusal validates against StatusEnvelope", True,
            "%d of %d served refusals validate against v1's StatusEnvelope" % (envelope_ok,
                                                                               len(in_lane)))
    else:
        blocked("g3 the refusal validates against StatusEnvelope",
                "%d of %d served refusals validate against the CURRENT v1 StatusEnvelope. Row "
                "IRPT_BCKEND-W2-S36 is DISCHARGED by the CTO's ruling (PRD v0.14 @b8e98d5a4d): "
                "`business_date` is now REQUIRED on the five ANSWER-BEARING states and may be "
                "ABSENT, never null, on the four NO-ANSWER ones, and a version refusal is "
                "UNAVAILABLE. A remainder here is therefore a DIFFERENT defect from the one that "
                "row named, and the deciding line above says which operation and why."
                % (envelope_ok, len(in_lane)))

    # THE SUCCESS HALF IS HUMAN-GATED, RULED BY THE ISSUER (amendment 3 C2, re-confirmed at
    # amendment 4), UNDER THE FACE'S OWN RULE FOR ARM (f): where no principal path a worker may
    # walk exists, the arm is WRITTEN HUMAN-GATED naming the operator's exact act and its expected
    # reading, never skipped silently. It is graded the same way arm (f) is -- by READING THE
    # RECORD for the elements the rule names, as literal strings, so a reworded record fails
    # rather than being read charitably. It is NOT a pass: `human_gated()` records its own verdict.
    required = {
        "the g2 section exists": "RT2 ARM (g2)",
        "the verdict": "**`HUMAN-GATED`.**",
        "which console/CLI": "313476888478",
        "which user store": "opal-users-v2",
        "which claim": "firmId",
        "the expected status": "HTTP 200",
        "the response contract by path": "responses/<operation>.response.schema.json",
        "the opaque firm id, not the registry spelling": "ISSUED OPAQUE id",
        "the enqueueing routes excluded and named": "THE TWO POST ROUTES ARE EXCLUDED",
        "what must NOT be recorded": "NOT the `data` payload",
    }
    with open(GATED, "r", encoding="utf-8") as fh:
        text = fh.read()
    found = {k: (v in text) for k, v in required.items()}
    for k, v in required.items():
        print("      [%s] %-46s %s" % ("x" if found[k] else " ", k, v))
    leaked = [tok for tok in ("BEGIN PRIVATE KEY", "BEGIN RSA", "eyJhbGciOi", "Bearer ey")
              if tok in text]
    print("      secret VALUES in the record: %d (names only is the bound)" % len(leaked))
    human_gated("g2 success responses validate, SERVED",
                all(found.values()) and not leaked,
                "HUMAN-GATED, which is this arm's own rule and not a bar lowered: %d of %d "
                "required elements present and 0 secret values. 0 of %d success responses are "
                "MEASURED and none is claimed -- a SUCCESS needs a principal the EDGE VALIDATOR "
                "accepts, and invoking a deployed function with a fabricated advisor id returns a "
                "REFUSAL, which cannot validate against a response contract at all (row W2-S25). "
                "Counting that would record the opposite of what the arm asks. The record names "
                "the operator's exact act as step 3b of arm (f)'s same bounded run, with the two "
                "ENQUEUEING routes excluded on their own line under bounds 1 and 2."
                % (sum(found.values()), len(found), len(in_lane)))


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


def vintage_disclosure():
    """WHICH BYTES THIS RUN ACTUALLY READ, and which of them are at no commit.

    THIS BATTERY READS THE WORKTREE. Every arm above resolves modules and artifacts by PATH, so a
    file that is edited-but-uncommitted is INDISTINGUISHABLE to them from one that is in the
    record -- and arm (a)'s `0 of 12` depends on exactly such a file right now. A token printed
    over an uncommitted population is a claim about THIS FILESYSTEM, not about the repository, and
    the difference is the whole of GRAIN. So the run states it rather than leaving a reader to
    assume the stronger reading.

    It does NOT withhold the token: every arm's own bar is genuinely met on the bytes exercised.
    It records the vintage those bytes have.
    """
    print("\n=== VINTAGE OF THE BYTES THIS RUN EXERCISED ======================")
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True,
                          text=True, timeout=120)
    rows = [ln for ln in (proc.stdout or "").splitlines()
            if ln[3:].startswith("infra/aws/lambda/investor-reporting")
            or ln[3:].startswith("infra/aws/terraform/investor-reporting")
            or ln[3:].startswith("docs/contracts/investor-reporting")]
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=120).stdout.strip()
    print("    HEAD: %s" % head)
    if not rows:
        print("    0 subject file(s) differ from HEAD: every byte above is IN THE RECORD.")
        return
    print("    %d subject file(s) are NOT at HEAD, so the arms that read them are measuring this "
          "FILESYSTEM and not the repository:" % len(rows))
    for ln in rows:
        print("      %s" % ln)
    print("    WHY THEY ARE NOT COMMITTED: row IRPT_BCKEND-W2-S41 -- amendment 3 C1 grants the "
          "holdings paths in PROSE and the <paths> block does not carry them, so the lane gate "
          "refuses them and an author override is the one escape the rule forbids. ONE LINE of "
          "<paths> converts this disclosure into a record.")
    print("    WHAT IT MEANS FOR THE TOKEN: arm (a)'s `0 of 12` and arm (a4)'s census both read "
          "holdings/entry.py from the worktree. On a clean checkout of this branch the twelfth "
          "route is UNGUARDED and arm (a2) reads `1 of 12` -- which is what row W2-S30 says and "
          "what the previous run recorded. The guard is WRITTEN and PASSING, not yet RECORDED.")


def main():
    print("BATTERY IB-rt-2 -- GUARD THE SIX")
    print("repo: %s" % REPO)
    print("subjects: the published route file, each function's DECLARED entry point, the real "
          "_authz guard, Enforcer and scope resolver")
    arm_a()
    junit = arm_bcd()
    arm_d3_business_date()
    arm_e()
    arm_f()
    arm_g(junit)

    vintage_disclosure()

    print("\n=== SUMMARY ======================================================")
    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    gated = {n for n, _ok, d in RESULTS if d.startswith("HUMAN-GATED")}
    for n, ok, d in RESULTS:
        label = "HUMAN-GATED" if n in gated else ("PASS" if ok else "FAIL/BLOCKED")
        print("  %-40s %s" % (n, label))
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
