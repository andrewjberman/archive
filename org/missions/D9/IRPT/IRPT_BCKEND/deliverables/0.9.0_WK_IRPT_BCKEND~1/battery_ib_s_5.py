#!/usr/bin/env python3
"""IB-s-5 acceptance battery -- S5-AC1, six arms, every count beside its denominator.

Prints IBS5-POLICY-BOUND on the last line ONLY when all six arms hold.

  (a) EACH FIRM LANDS ONLY IN ITS OWN LOCATIONS.
  (b) A WRITE INTO A SECOND FIRM'S LOCATION IS REFUSED -- THE DIFFERENCE CONTROL.
  (c) UNKNOWN, SPOOFED, CONTRADICTORY, OPAL-ORIGIN.
  (d) THE BOUND FIRM IS IMMUTABLE.
  (e) COMPLETENESS FAILS LOUD.
  (f) THE POLICY IS VERSIONED AND OWNED; THE IAM HALF IS APPLIED.

Arms (a)-(d) exercise gate.py directly (in-process, pure, no AWS call). Arm (e) invokes
pytest twice in subprocesses -- once against the REAL registry/policy (expect PASS), once
against a scratch registry carrying a planted 4th firm (expect FAIL naming it) -- because
"fails loud" is a claim about the TEST HARNESS's behavior, not about gate.py's return
value, and the only honest way to prove a test fails correctly is to make it fail and
read the output. Arm (f) reads the APPLIED PLANE: get-role on each stub role, and the
ledger's own closed state.

READ-ONLY on AWS (get-role only). No write of any kind: no PutObject, no PutItem, no
apply, no vendor call, no mailbox read.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
GATE_DIR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_gate")
KEYS_DIR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_keys")
CORE = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "core")
POLICY_PATH = os.path.join(CORE, "firm_destination_policy.json")
REGISTRY_PATH = os.path.join(REPO, "data", "firm_registry.json")
SCRATCH = os.path.join(REPO, ".scratch")
SLUG = "irpt-bckend-s5"
SENTINEL = "org/critical_paths/.open_deploys/irpt-bckend-s5.json"

sys.path.insert(0, GATE_DIR)
sys.path.insert(0, KEYS_DIR)
import gate  # noqa: E402

FAILS = []
ARMS = {}
AWS_CALLS = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("ERROR: [%s] %s" % (arm, msg))


def check(arm, cond, msg):
    if not cond:
        fail(arm, msg)
    return bool(cond)


def _bash_argv(script, *args):
    spec = importlib.util.spec_from_file_location(
        "gbr", os.path.join(REPO, ".tools", "git_bash_resolver.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.bash_argv(script, *args)


def aws(*args):
    argv = _bash_argv(os.path.join(REPO, ".tools", "aws"), *args)
    r = subprocess.run(argv, capture_output=True, cwd=REPO)
    AWS_CALLS.append(" ".join(args))
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    err = r.stderr.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    if r.returncode != 0:
        return r.returncode, err
    if not out:
        return 0, {}
    try:
        return 0, json.loads(out)
    except ValueError:
        return 0, out


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, cwd=REPO)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip()


def evidence(domain_local_part="advisor", domain="49financial.com", verified="VERIFIED",
            method="FORWARDING_ARRANGEMENT_HEADERS", display_from_used=False):
    return {"verified": verified, "original_sender_address": "%s@%s" % (domain_local_part, domain),
            "verification_method": method, "display_from_used": display_from_used}


def policy():
    return gate.load_policy(POLICY_PATH)


# ------------------------------------------------------------------ arm (a)
def arm_a():
    print("")
    print("(a) EACH FIRM LANDS ONLY IN ITS OWN LOCATIONS.")
    firms = policy()["firms"]
    print("    DENOMINATOR: %d firm(s) in the applied policy" % len(firms))
    ok = check("a", len(firms) == 3, "expected 3 firms, found %d" % len(firms))
    firm_pass = 0
    for entry in firms:
        fid = entry["firm_id"]
        bound = gate.bind_firm(evidence(domain=entry["sender_domain"]), policy_path=POLICY_PATH)
        if not check("a", isinstance(bound, gate.BoundRequest) and bound.firm_id == fid,
                     "%s did not bind to itself" % fid):
            continue
        kinds = sorted(entry["destinations"])
        kind_pass = 0
        for kind in kinds:
            key = gate.destination_for(bound, kind, id="REQ-1", r=0, a=1, revision="rev-1",
                                       year=2026, month=9, day=10)
            own = key.startswith("firms/%s/" % fid)
            leaks = [o["firm_id"] for o in firms if o["firm_id"] != fid and key.startswith("firms/%s/" % o["firm_id"])]
            if own and not leaks:
                kind_pass += 1
            else:
                fail("a", "%s/%s escaped its firm: %r (leaks into %r)" % (fid, kind, key, leaks))
        print("    %-12s %d of %d destination kind(s) land under firms/%s/ only"
              % (fid, kind_pass, len(kinds), fid))
        if kind_pass == len(kinds):
            firm_pass += 1
    print("    %d of %d firm(s) x every destination kind land only in their own locations" % (firm_pass, len(firms)))
    ok = check("a", firm_pass == len(firms), "firm_pass %d of %d" % (firm_pass, len(firms))) and ok
    ARMS["a"] = ok
    return ok


# ------------------------------------------------------------------ arm (b)
def arm_b():
    print("")
    print("(b) A WRITE INTO A SECOND FIRM'S LOCATION IS REFUSED -- THE DIFFERENCE CONTROL.")
    firms = policy()["firms"]
    a_firm, b_firm = firms[0], firms[1]
    bound_a = gate.bind_firm(evidence(domain=a_firm["sender_domain"]), policy_path=POLICY_PATH)
    refused = False
    try:
        gate.destination_for(bound_a, "requests", firm_id=b_firm["firm_id"], id="X", r=0)
    except gate.GateRefusal as e:
        refused = True
        print("    cross-firm request (%s bound, asking for %s) REFUSED: %s"
             % (a_firm["firm_id"], b_firm["firm_id"], str(e)[:140]))
    ok = check("b", refused, "a cross-firm destination request did NOT raise")
    key = gate.destination_for(bound_a, "requests", id="X", r=0)
    same_firm_ok = key.startswith("firms/%s/" % a_firm["firm_id"])
    print("    same-firm request (%s bound, %s requested) SUCCEEDED: %s"
         % (a_firm["firm_id"], a_firm["firm_id"], key))
    ok = check("b", same_firm_ok, "the same-firm call after the refusal did not succeed") and ok
    ARMS["b"] = ok
    return ok


# ------------------------------------------------------------------ arm (c)
def arm_c():
    print("")
    print("(c) UNKNOWN, SPOOFED, CONTRADICTORY, OPAL-ORIGIN.")
    fixtures = [
        ("unknown domain", evidence(domain="example-firm.com"), gate.Quarantined),
        ("spoofed display-From", evidence(display_from_used=True), gate.Quarantined),
        ("contradictory evidence", evidence(method="UNKNOWN"), gate.Quarantined),
        ("Opal-origin, no target-firm rule", evidence(domain_local_part="requests", domain="opalinvest.com"),
         gate.Unresolved),
    ]
    good = 0
    for label, ev, expect_type in fixtures:
        outcome = gate.bind_firm(ev, policy_path=POLICY_PATH)
        never_firm = not isinstance(outcome, gate.BoundRequest)
        right_type = isinstance(outcome, expect_type)
        # Deliberately NOT `outcome.reason` unguarded: Quarantined/Unresolved carry it,
        # BoundRequest does not, and a fixture that (wrongly) bound would otherwise crash
        # this loop with an AttributeError instead of printing a controlled failure --
        # exactly the crash a red-first mutant on the spoofing check exposed here.
        detail = outcome.reason if hasattr(outcome, "reason") else (
            "BOUND to firm_id=%r -- THIS FIXTURE SHOULD NEVER HAVE BOUND" % getattr(outcome, "firm_id", None))
        print("    %-34s -> %-24s (never-a-firm=%s, expected-type=%s) reason=%s"
             % (label, type(outcome).__name__, never_firm, right_type, detail[:90]))
        if never_firm and right_type:
            good += 1
        else:
            fail("c", "%s: never_firm=%s right_type=%s detail=%s" % (label, never_firm, right_type, detail[:120]))
    print("    %d of %d fixture(s) NEVER became a firm, each with the policy's own outcome type" % (good, len(fixtures)))
    ok = check("c", good == 4, "expected 4 of 4, got %d" % good)
    ARMS["c"] = ok
    return ok


# ------------------------------------------------------------------ arm (d)
def arm_d():
    print("")
    print("(d) THE BOUND FIRM IS IMMUTABLE.")
    firms = policy()["firms"]
    bound = gate.bind_firm(evidence(domain=firms[0]["sender_domain"]), policy_path=POLICY_PATH)
    attempts = []
    try:
        bound.firm_id = firms[1]["firm_id"]
        attempts.append(("attribute set", False))
    except Exception as e:
        attempts.append(("attribute set", True))
        print("    bound.firm_id = <other>            -> RAISED %s: %s" % (type(e).__name__, str(e)[:100]))
    try:
        bound.rebind(firms[1]["firm_id"])
        attempts.append(("rebind()", False))
    except Exception as e:
        attempts.append(("rebind()", True))
        print("    bound.rebind(<other>)              -> RAISED %s: %s" % (type(e).__name__, str(e)[:100]))
    try:
        del bound.firm_id
        attempts.append(("attribute delete", False))
    except Exception as e:
        attempts.append(("attribute delete", True))
        print("    del bound.firm_id                  -> RAISED %s: %s" % (type(e).__name__, str(e)[:100]))
    # NAMED FINDING: `.firm_id` is a read-only PROPERTY (no setter/deleter) on
    # BoundRequest, so the three attempts above are caught by TWO INDEPENDENT
    # mechanisms at once -- the property's own missing accessor, AND __setattr__'s
    # explicit raise. A red-first mutant that disables ONLY __setattr__'s raise still
    # passes the three attempts above, because the property alone still blocks them --
    # a WEAK mutant that does not discriminate the mechanism this arm claims to test.
    # This fourth attempt targets an actual __slots__ member (`_binding`) that carries
    # NO property protection, so it exercises __setattr__ ALONE and DOES discriminate:
    # disabling the raise there lets the slot be overwritten.
    try:
        bound._binding = None
        attempts.append(("internal slot set (_binding)", False))
    except Exception as e:
        attempts.append(("internal slot set (_binding)", True))
        print("    bound._binding = None              -> RAISED %s: %s" % (type(e).__name__, str(e)[:100]))
    good = sum(1 for _, ok in attempts if ok)
    # Reading bound.firm_id here is NOT guaranteed safe: if the internal-slot attempt
    # above SUCCEEDED (a mutation broke __setattr__), `_binding` may now be None, and the
    # property's `self._binding.firm_id` would raise AttributeError -- crashing this
    # SUMMARY line before the check() below ever runs, exactly the arm-c crash class.
    # Guarded so a corrupted internal state is REPORTED, never allowed to abort the arm.
    try:
        current_firm = bound.firm_id
    except Exception as e:
        current_firm = "<CRASHED reading firm_id: %s: %s>" % (type(e).__name__, e)
    print("    %d of %d mutation attempt(s) RAISED; firm_id after all attempts: %s (unchanged: %s)"
         % (good, len(attempts), current_firm, current_firm == firms[0]["firm_id"]))
    ok = check("d", good == len(attempts) == 4, "only %d of 4 mutation attempts raised" % good)
    ok = check("d", current_firm == firms[0]["firm_id"], "firm_id changed despite raised attempts") and ok
    ARMS["d"] = ok
    return ok


# ------------------------------------------------------------------ arm (e)
def arm_e():
    print("")
    print("(e) COMPLETENESS FAILS LOUD.")
    test_file = os.path.join(GATE_DIR, "tests", "test_policy_completeness.py")
    ok = True

    r1 = subprocess.run([sys.executable, "-m", "pytest", test_file, "-q", "--color=no"],
                        capture_output=True, cwd=REPO)
    out1 = r1.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    tail1 = [ln for ln in out1.strip().split("\n") if ln.strip()][-1:]
    print("    RUN 1 (HEAD -- real registry, real policy): rc=%d -- %s" % (r1.returncode, tail1[0] if tail1 else ""))
    ok = check("e", r1.returncode == 0, "the completeness test does not pass at HEAD (registry 3 == policy 3)") and ok

    os.makedirs(SCRATCH, exist_ok=True)
    with io.open(REGISTRY_PATH, encoding="utf-8") as fh:
        reg = json.load(fh)
    reg["firms"].append({
        "firm_id": "planted4th", "tree_token": None, "display_name": "Planted Fourth Firm (test)",
        "aliases": [], "kind": "client", "enabled": True, "bucket": "opal-data-planted4th",
        "email_domain": "planted4th.com", "scopes": {"portal": True, "mdpf": True, "pipeline": True},
        "aua_source": None, "model_source": None, "fee_scope": None, "series_start": "DYNAMIC",
        "delivery_cadence": None,
    })
    scratch_registry = os.path.join(SCRATCH, "firm_registry.planted4th.json")
    with io.open(scratch_registry, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=1)

    env = dict(os.environ)
    env["IRPT_FIRM_REGISTRY"] = scratch_registry
    r2 = subprocess.run([sys.executable, "-m", "pytest", test_file, "-q", "--color=no", "-k",
                        "test_policy_firms_match_the_registrys_enabled_client_firms"],
                        capture_output=True, cwd=REPO, env=env)
    out2 = r2.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    named = "planted4th" in out2
    tail2 = [ln for ln in out2.strip().split("\n") if ln.strip()][-1:]
    print("    RUN 2 (scratch registry + planted 4th firm 'planted4th'): rc=%d -- %s"
         % (r2.returncode, tail2[0] if tail2 else ""))
    print("      the failure output NAMES the missing firm 'planted4th': %s" % named)
    ok = check("e", r2.returncode != 0, "the completeness test did NOT fail against a planted 4th firm") and ok
    ok = check("e", named, "the failure output does not name the planted firm") and ok
    ARMS["e"] = ok
    return ok


# ------------------------------------------------------------------ arm (f)
def arm_f():
    print("")
    print("(f) THE POLICY IS VERSIONED AND OWNED; THE IAM HALF IS APPLIED.")
    p = policy()
    print("    policy_version = %r" % p.get("policy_version"))
    print("    owner          = %r" % p.get("owner"))
    ok = check("f", bool(p.get("policy_version")), "policy_version is empty")
    ok = check("f", bool(p.get("owner")), "owner is empty") and ok

    role_names = ["irpt-core-firm-49financial", "irpt-core-firm-cottonwood", "irpt-core-firm-inflection",
                 "irpt-core-quarantine"]
    good = 0
    for name in role_names:
        rc, out = aws("iam", "get-role", "--role-name", name, "--output", "json")
        trust = None
        if rc == 0 and isinstance(out, dict):
            trust = out.get("Role", {}).get("AssumeRolePolicyDocument", {})
        assumes_lambda = False
        if trust:
            for stmt in trust.get("Statement", []):
                principals = stmt.get("Principal", {})
                svc = principals.get("Service")
                svcs = svc if isinstance(svc, list) else [svc]
                if "lambda.amazonaws.com" in svcs and stmt.get("Action") == "sts:AssumeRole":
                    assumes_lambda = True
        print("    get-role %-28s rc=%d trust-to-lambda=%s" % (name, rc, assumes_lambda))
        if rc == 0 and assumes_lambda:
            good += 1
        else:
            fail("f", "%s: rc=%d assumes_lambda=%s" % (name, rc, assumes_lambda))
    print("    %d of %d role(s) exist with a trust policy naming lambda.amazonaws.com" % (good, len(role_names)))
    ok = check("f", good == len(role_names), "roles %d of %d" % (good, len(role_names))) and ok

    r = subprocess.run([sys.executable, os.path.join(REPO, ".tools", "deploy_ledger.py"), "check"],
                       capture_output=True, cwd=REPO)
    out = (r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")).replace("\r\n", "\n")
    mine = [ln for ln in out.split("\n") if SLUG in ln]
    print("    deploy_ledger.py check -> line(s) naming this slug: %d" % len(mine))
    for ln in mine:
        print("      %s" % ln)
    ok = check("f", not any("OPEN" in ln for ln in mine),
              "deploy_ledger check still reports this slug OPEN: %r" % mine) and ok

    rc, h = git("log", "-1", "--format=%H", "--", SENTINEL)
    print("    git log -1 --format=%%H -- %s -> %s" % (SENTINEL, h or "(no commit)"))
    ok = check("f", bool(h), "the sentinel has no commit") and ok
    rc, status = git("status", "--porcelain", "--", SENTINEL)
    print("    working-tree status of the sentinel: %s" % (status if status else "clean"))
    ok = check("f", not status, "sentinel has an uncommitted change: %r" % status) and ok

    ARMS["f"] = ok
    return ok


def main():
    print("IB-s-5 BATTERY -- S5-AC1, six arms. AWS calls: get-role only (read-only). No write, no vendor call.")
    print("repo %s | policy %s" % (REPO, POLICY_PATH))
    if not os.path.exists(POLICY_PATH):
        fail("pre", "firm_destination_policy.json is missing -- has the apply run?")

    arm_a()
    arm_b()
    arm_c()
    arm_d()
    arm_e()
    arm_f()

    print("")
    print("AWS calls made by this battery: %d, all read-only get-role" % len(AWS_CALLS))
    held = sum(1 for v in ARMS.values() if v)
    print("arms: %d of 6 evaluated; arms holding: %d of 6; assertions failed: %d"
         % (len(ARMS), held, len(FAILS)))
    for f in FAILS:
        print("  FAILED -- %s" % f)
    if len(ARMS) == 6 and held == 6 and not FAILS:
        print("IBS5-POLICY-BOUND")
        return 0
    print("BLOCKED: the token is withheld -- %d of 6 arm(s) held" % held)
    return 1


if __name__ == "__main__":
    sys.exit(main())
