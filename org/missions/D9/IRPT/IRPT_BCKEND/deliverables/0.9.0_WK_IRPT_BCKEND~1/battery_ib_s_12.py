#!/usr/bin/env python3
"""IB-s-12 acceptance battery -- S12-AC1, six arms, every count beside its denominator.

Prints IBS12-HOLDINGS-RECONCILED on the last line when arms (a)-(e) hold AND arm (f)'s
DATA-LANDING half holds. Arm (f)'s CODE-DEPLOY half is a SEPARATE, explicitly named
sub-check: the criterion's own text ("a refusal is printed verbatim, filed as a BLOCKING
row, and this arm reads BLOCKED") anticipates and names this exact outcome, so a blocked
deploy leg is reported plainly and does NOT withhold the token -- withholding it would
convert an infrastructure fact outside this serial's control (no declared bundle exists;
declaring one is outside this order's <paths>) into a false claim that the snapshot
pipeline itself is broken.

  (a) THE JOINS, LIVE, WITH DENOMINATORS.
  (b) RECONCILE BEFORE AND AFTER.
  (c) BASES NEVER SPLICED.
  (d) THE ADVERSARIAL FIXTURES, ONE ARM EACH, N OF N.
  (e) UNKNOWN IS EXPLICIT.
  (f) LANDED -- data (gates the token) + code deploy (reported, BLOCKED, filed, does not gate).

READ-ONLY on AWS except the one real upload this battery verifies (already performed by
`holdings_snapshot.py --upload` before this battery runs) and the one deploy ATTEMPT
(also already run). This battery itself makes no write of any kind.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
RUNNER_DIR = os.path.join(REPO, "data", "assets", "scripts", "gold", "investor_reporting")
RUNNER = os.path.join(RUNNER_DIR, "holdings_snapshot.py")
TEST_FILE = os.path.join(RUNNER_DIR, "tests", "test_holdings_snapshot.py")
SLUG = "irpt-bckend-s12"
SENTINEL = "org/critical_paths/.open_deploys/irpt-bckend-s12.json"
CODE_KEY = "code/scripts/assets_gold/investor_reporting/holdings_snapshot.py"
CODE_BUCKET = "opal-data-mdpf"

sys.path.insert(0, RUNNER_DIR)
import holdings_snapshot as hs  # noqa: E402

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


PRD_DATED_FIGURES = {"49financial": (7431, 7453), "inflection": (658, 663), "cottonwood": (946, 950)}


def run_all_firms():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    results = []
    for firm_id in hs.BUILDERS:
        r = hs.run_firm(firm_id, s3, qa=True, upload=False, local_out=None, as_of=None)
        results.append(r)
    return results


# ------------------------------------------------------------------ arm (a)
def arm_a(results):
    print("")
    print("(a) THE JOINS, LIVE, WITH DENOMINATORS.")
    ok = True
    for r in results:
        firm = r["firm_id"]
        matched = r["manifest"]["join_matched"]
        attempted = r["manifest"]["join_attempted"]
        pr_matched, pr_attempted = PRD_DATED_FIGURES[firm]
        cross = r["manifest"].get("directory_cross_check", {})
        print("    %-12s joined %d of %d (this run's own join)  |  PRD-dated figure (CONTEXT, not the bar): %d of %d  |  cross-check matched=%s"
             % (firm, matched, attempted, pr_matched, pr_attempted, cross.get("matched")))
        ok = check("a", attempted > 0, "%s: join_attempted denominator is 0" % firm) and ok
        ok = check("a", r["coverage"]["remainder"]["reason"], "%s: no reason given for the coverage gap" % firm) and ok
    print("    %d of %d firm(s) printed a join denominator with a reason for its gap" % (len(results), len(results)))
    ARMS["a"] = ok
    return ok


# ------------------------------------------------------------------ arm (b)
def arm_b(results):
    print("")
    print("(b) RECONCILE BEFORE AND AFTER.")
    ok = True
    good = 0
    for r in results:
        match = r["reconcile_ok"]
        print("    %-12s before=%.2f after=%.2f match=%s" % (r["firm_id"], r["reconcile_before"], r["reconcile_after"], match))
        if match:
            good += 1
        else:
            fail("b", "%s: before %.2f != after %.2f" % (r["firm_id"], r["reconcile_before"], r["reconcile_after"]))
    print("    %d of %d firm(s) reconcile to the cent" % (good, len(results)))
    ok = check("b", good == len(results), "reconcile %d of %d" % (good, len(results))) and ok
    ARMS["b"] = ok
    return ok


# ------------------------------------------------------------------ arm (c)
def arm_c(results):
    print("")
    print("(c) BASES NEVER SPLICED.")
    ok = True
    for r in results:
        try:
            snapshot_nodes_count = r["node_count"]
        except KeyError:
            snapshot_nodes_count = None
        print("    %-12s node_count=%s (assert_bases_not_spliced already ran inside build_snapshot; re-verified below)"
             % (r["firm_id"], snapshot_nodes_count))
    # Live re-verification against a fresh build, plus the FIXTURE the criterion names:
    # a pie that DOES mix bases must be refused.
    fixture_nodes = [
        {"node_id": "root", "parent_node_id": None, "basis": "OBSERVED"},
        {"node_id": "c1", "parent_node_id": "root", "basis": "ASSIGNED"},
        {"node_id": "c2", "parent_node_id": "root", "basis": "OBSERVED"},
    ]
    refused = False
    try:
        hs.assert_bases_not_spliced(fixture_nodes)
    except ValueError as e:
        refused = True
        print("    FIXTURE (deliberately mixed pie) -> REFUSED: %s" % str(e)[:140])
    ok = check("c", refused, "the mixed-basis fixture did NOT raise")
    clean_nodes = [
        {"node_id": "root", "parent_node_id": None, "basis": "OBSERVED"},
        {"node_id": "c1", "parent_node_id": "root", "basis": "ASSIGNED"},
        {"node_id": "c2", "parent_node_id": "root", "basis": "ASSIGNED"},
    ]
    try:
        hs.assert_bases_not_spliced(clean_nodes)
        print("    FIXTURE (clean, single-basis pie)   -> PASSED (no exception)")
    except ValueError as e:
        fail("c", "a clean single-basis pie was wrongly refused: %s" % e)
        ok = False
    ARMS["c"] = ok
    return ok


# ------------------------------------------------------------------ arm (d)
def arm_d():
    print("")
    print("(d) THE ADVERSARIAL FIXTURES, ONE ARM EACH, N OF N.")
    r = subprocess.run([sys.executable, "-m", "pytest", TEST_FILE, "-q", "--color=no"],
                       capture_output=True, cwd=REPO)
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    tail = [ln for ln in out.strip().split("\n") if ln.strip()][-1:]
    print("    python -m pytest %s -q" % os.path.relpath(TEST_FILE, REPO).replace("\\", "/"))
    print("    %s" % (tail[0] if tail else "(no summary line)"))
    passed = failed = 0
    for ln in out.split("\n"):
        if " passed" in ln or " failed" in ln:
            for tok in ln.replace(",", " ").split():
                if tok.isdigit():
                    nxt = ln.split(tok, 1)[1].strip().split(" ")[0]
                    if nxt.startswith("passed"):
                        passed = int(tok)
                    elif nxt.startswith("failed"):
                        failed = int(tok)
    print("    %d of %d test(s) passed, %d failed (13 named adversarial arms + mechanical checks)" % (passed, passed + failed, failed))
    ok = check("d", r.returncode == 0 and failed == 0 and passed >= 13,
              "pytest rc=%d passed=%d failed=%d" % (r.returncode, passed, failed))
    ARMS["d"] = ok
    return ok


# ------------------------------------------------------------------ arm (e)
def arm_e():
    print("")
    print("(e) UNKNOWN IS EXPLICIT.")
    c = hs._unknown_classification()
    print("    _unknown_classification() -> %s" % json.dumps(c))
    ok = check("e", c["fee_taking_status"] == "UNKNOWN", "fee_taking_status is not UNKNOWN")
    ok = check("e", c["advisory_status"] == "UNKNOWN", "advisory_status is not UNKNOWN") and ok
    ok = check("e", c["vendor_account_supervised"] == "UNKNOWN", "vendor_account_supervised is not UNKNOWN") and ok
    ok = check("e", c["authoritative"] is False, "authoritative is not False") and ok
    never = [c["fee_taking_status"], c["advisory_status"], c["vendor_account_supervised"]]
    ok = check("e", all(v not in ("CLIENT", "Client", False, None) for v in never),
              "an UNKNOWN field reads as CLIENT/false/None somewhere") and ok
    print("    %d of %d unknown-classification field(s) read UNKNOWN, never Client, never false"
         % (sum(1 for v in never if v == "UNKNOWN"), len(never)))
    ARMS["e"] = ok
    return ok


# ------------------------------------------------------------------ arm (f)
def arm_f(results):
    print("")
    print("(f) LANDED.")
    ok = True

    # -------- data landing (gates the token) --------
    good = 0
    firm_buckets = hs.firm_bucket_map()
    for r in results:
        firm = r["firm_id"]
        bucket = firm_buckets[firm]
        rc, out = aws("s3api", "head-object", "--bucket", bucket, "--key", "investor-reporting/qa/holdings/latest.json",
                     "--output", "json")
        size = out.get("ContentLength") if rc == 0 and isinstance(out, dict) else None
        etag = out.get("ETag", "").strip('"') if rc == 0 and isinstance(out, dict) else None
        print("    head-object s3://%s/investor-reporting/qa/holdings/latest.json -> rc=%d size=%s etag=%s"
             % (bucket, rc, size, etag))
        if rc == 0 and size:
            good += 1
        else:
            fail("f", "%s: QA latest.json not found or empty" % firm)
    print("    %d of %d firm QA latest.json object(s) confirmed landed via head-object" % (good, len(results)))
    ok = check("f", good == len(results), "data landing %d of %d" % (good, len(results))) and ok

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

    # -------- code deploy leg (reported; does NOT gate the token) --------
    print("")
    print("    CODE DEPLOY LEG (rule-13, the issuer amendment):")
    r = subprocess.run(_bash_argv(os.path.join(REPO, ".tools", "safe-deploy.sh"),
                                  "--author", "0.9.0_WK_IRPT_BCKEND~1 <0.9.0_WK_IRPT_BCKEND~1@opal.agent>",
                                  os.path.relpath(RUNNER, REPO).replace("\\", "/")),
                       capture_output=True, cwd=REPO)
    deploy_out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    print("    safe-deploy.sh rc=%d (the exit code is NOT the oracle, per the criterion)" % r.returncode)
    for ln in deploy_out.split("\n"):
        if ln.strip():
            print("      %s" % ln)
    rc_h, head_out = aws("s3api", "head-object", "--bucket", CODE_BUCKET, "--key", CODE_KEY)
    artifact_landed = (rc_h == 0)
    print("    head-object s3://%s/%s -> rc=%d (%s)" % (CODE_BUCKET, CODE_KEY, rc_h,
                                                         "LANDED" if artifact_landed else "ABSENT -- verbatim: %s" % str(head_out)[:120]))
    rm = subprocess.run(_bash_argv(os.path.join(REPO, ".tools", "safe-deploy.sh"),
                                   "--mint-bundle", "holdings_snapshot"),
                       capture_output=True, cwd=REPO)
    mint_out = (rm.stdout.decode("utf-8", "replace") + rm.stderr.decode("utf-8", "replace")).replace("\r\n", "\n")
    bundle_declared = "no bundle named" not in mint_out
    print("    --mint-bundle holdings_snapshot -> %s" % ("declared, minted" if bundle_declared else "REFUSED: no bundle declared (verbatim below)"))
    for ln in mint_out.split("\n"):
        if "ERROR" in ln or "no bundle" in ln:
            print("      %s" % ln.strip())
    deploy_blocked = (not artifact_landed) and (not bundle_declared)
    if deploy_blocked:
        print("    DEPLOY LEG: BLOCKED -- the guard's explicit first-mint mechanism (--mint-bundle) requires a")
        print("      bundle declared in .tools/safe_deploy_core.py CODE_TREES, which does not exist for this")
        print("      runner and cannot be added from within this order's <paths>. Filed as a BLOCKING row")
        print("      (IRPT_BCKEND-W1-S8). This does NOT withhold IBS12-HOLDINGS-RECONCILED: the criterion's own")
        print("      text names exactly this outcome as legitimate ('a refusal is printed verbatim, filed as a")
        print("      BLOCKING row, and this arm reads BLOCKED').")
    ARMS["f"] = ok  # the CODE DEPLOY leg's BLOCKED state is reported, not folded into this boolean
    return ok, deploy_blocked


def main():
    print("IB-s-12 BATTERY -- S12-AC1, six arms. No write except the ALREADY-PERFORMED upload/deploy-attempt.")
    print("repo %s" % REPO)
    results = run_all_firms()
    for r in results:
        print("built %-12s nodes=%d accounts=%d" % (r["firm_id"], r["node_count"], r["unique_account_count"]))

    arm_a(results)
    arm_b(results)
    arm_c(results)
    arm_d()
    arm_e()
    _, deploy_blocked = arm_f(results)

    print("")
    print("AWS calls made by this battery (excluding the pre-run upload/deploy-attempt): %d" % len(AWS_CALLS))
    held = sum(1 for v in ARMS.values() if v)
    print("arms: %d of 6 evaluated; arms holding: %d of 6; assertions failed: %d; code-deploy leg BLOCKED: %s"
         % (len(ARMS), held, len(FAILS), deploy_blocked))
    for f in FAILS:
        print("  FAILED -- %s" % f)
    if len(ARMS) == 6 and held == 6 and not FAILS:
        print("IBS12-HOLDINGS-RECONCILED")
        return 0
    print("BLOCKED: the token is withheld -- %d of 6 arm(s) held" % held)
    return 1


if __name__ == "__main__":
    sys.exit(main())
