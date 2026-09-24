"""IB-rtj-1 battery -- the capture tool, second repair (C-S153 navigation lifecycle, C-S156 runbook).

Arms: redirect | runbook.  Run from any cwd inside the worktree.
`redirect` re-runs the CVO~B round-9 diagnostic (IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs) and
the round-8 diagnostic (IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs), BOTH UNMODIFIED, against the repaired
source; then adds a single-difference regression pair and a fresh positive control via this worker's
own harness_ib_rtj_1.cjs (which, unlike IB-rti-1's harness, can vary the INITIAL navigation's own hop
chain -- needed to isolate the exact property the fix now checks).
`runbook` reads README.md and locates the delivery + hash-verification steps relative to the wrapper
invocation.
Everything is exercised under stubs / static text reads: no browser, network, credential, host action
or real file write. ASCII only.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC_DIR = "infra/aws/ec2/investor-reporting-export"
CAP = SRC_DIR + "/capture-session.cjs"
README = SRC_DIR + "/README.md"
R9_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs"
R8_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
HARNESS = os.path.join(HERE, "harness_ib_rtj_1.cjs")
BASELINE_R9 = os.path.join(HERE, "IB-rtj-1_baseline_r9_redirect_diagnostic.json")
BASELINE_R8 = os.path.join(HERE, "IB-rtj-1_baseline_r8_diagnostic.json")

ORIGIN = "https://opalinvest.dev"
IID = "i-0167fd745ad906a66"
CHECK = ORIGIN + "/investor-reporting/print"
FOREIGN = "https://example.invalid/hop"


def run_node(path, timeout=60):
    p = subprocess.run(["node", path], capture_output=True, text=True, timeout=timeout, cwd=REPO)
    return p.returncode, p.stdout, p.stderr


def run_harness(cfg):
    p = subprocess.run(["node", HARNESS, os.path.join(REPO, CAP), json.dumps(cfg)],
                        capture_output=True, text=True, timeout=60, cwd=REPO)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError("harness rc=%s stderr=%s" % (p.returncode, p.stderr[:400]))
    return json.loads(p.stdout.strip().splitlines()[-1])


def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", label, detail))
    return ok


def load(path):
    return json.loads(open(path, encoding="utf-8").read())


# The INTENDED shape of the R9 diagnostic's six cases against the REPAIRED source.
# (success, writes) per case index, by the case's own "name" field so a reorder in the CVO
# file (never expected, since it is read UNCHANGED) would be caught by a KeyError, not silently
# matched to the wrong row.
R9_INTENT = {
    "same-origin positive": (True, 1),
    "initial foreign hop returns to portal": (False, 0),       # THE C-S153 counterexample -- now refuses
    "initial final URL foreign control": (False, 0),
    "verification foreign hop returns control": (False, 0),
    "HTTP 500 refusal control": (False, 0),
    "marker absent refusal control": (False, 0),
}


def arm_redirect():
    print("=== ARM redirect (R101-AC1): navigation-lifecycle fix, C-S153 ===")
    ok = True

    print("--- baseline (unrepaired source, captured at arm (a) before any edit) ---")
    if os.path.isfile(BASELINE_R9) and os.path.isfile(BASELINE_R8):
        base9 = load(BASELINE_R9)
        for r in base9["results"]:
            print("  BASE R9  %-40s success=%s writes=%s" % (r["name"], r["success"], r["writes"]))
        base8 = load(BASELINE_R8)
        for r in base8["results"]:
            print("  BASE R8  %-40s writes=%s captureSuccessPrinted=%s" % (r["label"], r["writes"], r["captureSuccessPrinted"]))
        ok &= check("baseline reproduces C-S153 (case 'initial foreign hop returns to portal': writes=1, success=true)",
                     base9["results"][1]["name"] == "initial foreign hop returns to portal"
                     and base9["results"][1]["writes"] == 1 and base9["results"][1]["success"] is True)
        ok &= check("baseline verification-hop control already refuses (unaffected by this cell)",
                     base9["results"][3]["name"] == "verification foreign hop returns control"
                     and base9["results"][3]["writes"] == 0 and base9["results"][3]["success"] is False)
    else:
        ok &= check("baseline files present (%s, %s)" % (os.path.basename(BASELINE_R9), os.path.basename(BASELINE_R8)), False)

    print("--- R9 redirect diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source ---")
    rc9, out9, err9 = run_node(os.path.join(REPO, R9_DIAG))
    res9 = json.loads(out9)
    print("  source sha256: %s" % res9["diskSha256"][:16])
    for r in res9["results"]:
        want_success, want_writes = R9_INTENT[r["name"]]
        matched = (r["success"] is want_success) and (r["writes"] == want_writes)
        ok &= check("R9 case %-40s success=%-5s writes=%s (intent: success=%s writes=%s)"
                     % (r["name"], r["success"], r["writes"], want_success, want_writes), matched)
    print("  denominator: %d of %d R9 cases match intent" % (sum(1 for r in res9["results"] if R9_INTENT[r["name"]] == (r["success"], r["writes"])), len(res9["results"])))
    ok &= check("R9 diagnostic covered all 6 named cases (no case added/removed/renamed)",
                set(R9_INTENT) == set(r["name"] for r in res9["results"]))

    print("--- R8 diagnostic (CVO, UNMODIFIED) against the REPAIRED source -- must still match baseline ---")
    rc8, out8, err8 = run_node(os.path.join(REPO, R8_DIAG))
    res8 = json.loads(out8)
    base8_results = load(BASELINE_R8)["results"] if os.path.isfile(BASELINE_R8) else None
    for r in res8["results"]:
        print("  R8 case %-55s writes=%s captureSuccessPrinted=%s" % (r["label"], r["writes"], r["captureSuccessPrinted"]))
    if base8_results is not None:
        ok &= check("R8's 3 cases are BYTE-IDENTICAL to the pre-repair baseline (writes/navigations/errors)",
                     [(r["writes"], r["navigations"], r["captureSuccessPrinted"], r["errors"]) for r in res8["results"]]
                     == [(r["writes"], r["navigations"], r["captureSuccessPrinted"], r["errors"]) for r in base8_results])
    print("  denominator: 3 of 3 R8 cases printed")

    print("--- single-difference regression pair (this battery's own harness; C-S153's exact discriminating power) ---")
    # BAD: identical shape to the R9 'initial foreign hop returns to portal' counterexample.
    bad_cfg = {"origin": ORIGIN, "instanceId": IID, "initialHops": [ORIGIN, FOREIGN, ORIGIN],
               "verificationHops": [CHECK], "markerCount": 1, "passwordCount": 0, "status": 200}
    # GOOD: the ONE difference is the foreign hop's absence -- same chain length, same origin
    # everywhere, everything else (instance id, check route, marker, password, status) identical.
    good_cfg = {"origin": ORIGIN, "instanceId": IID, "initialHops": [ORIGIN, ORIGIN, ORIGIN],
                "verificationHops": [CHECK], "markerCount": 1, "passwordCount": 0, "status": 200}
    rbad = run_harness(bad_cfg)
    rgood = run_harness(good_cfg)
    print("  BAD  (foreign hop present):  writes=%d success=%s errors=%s" % (
        len(rbad["fileWrites"]), "OK: session state captured" in rbad["output"], rbad["errors"].strip()))
    print("  GOOD (foreign hop absent):   writes=%d success=%s" % (
        len(rgood["fileWrites"]), "OK: session state captured" in rgood["output"]))
    ok &= check("BAD refuses: 0 writes, no success, ORIGIN_HOP error naming the foreign URL",
                len(rbad["fileWrites"]) == 0 and "OK: session state captured" not in rbad["output"]
                and "ORIGIN_HOP" in rbad["errors"] and FOREIGN in rbad["errors"])
    ok &= check("GOOD (single difference: no foreign hop) succeeds: exactly 1 write",
                len(rgood["fileWrites"]) == 1 and "OK: session state captured" in rgood["output"])

    print("--- fresh authenticated positive control (this battery's own harness) ---")
    pos_cfg = {"origin": ORIGIN, "instanceId": IID, "initialHops": [ORIGIN], "verificationHops": [CHECK],
               "markerCount": 1, "passwordCount": 0, "status": 200}
    rpos = run_harness(pos_cfg)
    print("  POSITIVE: writes=%d success=%s" % (len(rpos["fileWrites"]), "OK: session state captured" in rpos["output"]))
    ok &= check("fresh positive control (2xx, same origin throughout, no password, marker present): exactly 1 write + success",
                len(rpos["fileWrites"]) == 1 and "OK: session state captured" in rpos["output"])

    if ok:
        print("IBR101-REDIRECT-DIAGNOSTIC-ALL-SIX-CASES-MATCH-INTENT")
        return 0
    print("FAIL: redirect arm")
    return 1


def arm_runbook():
    print("=== ARM runbook (R101-AC2): C-S156, delivery + hash-verification before the wrapper is invoked ===")
    ok = True
    text = open(os.path.join(REPO, README), encoding="utf-8").read()
    lines = text.splitlines()

    def find_line(pattern, flags=0):
        rx = re.compile(pattern, flags)
        for i, ln in enumerate(lines, start=1):
            if rx.search(ln):
                return i, ln.strip()
        return None, None

    cjs_deliver_line, cjs_deliver_text = find_line(
        r"aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/capture-session\.cjs")
    sh_deliver_line, sh_deliver_text = find_line(
        r"aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/capture-session\.sh ")
    hash_line, hash_text = find_line(r"^\s*sha256sum\s+/opt/investor-reporting-export/capture-session\.cjs\s+/opt/investor-reporting-export/capture-session\.sh")
    expect_cjs_line, expect_cjs_text = find_line(r"^\s*#\s*[0-9a-f]{64}\s+/opt/investor-reporting-export/capture-session\.cjs")
    expect_sh_line, expect_sh_text = find_line(r"^\s*#\s*[0-9a-f]{64}\s+/opt/investor-reporting-export/capture-session\.sh")
    stop_line, stop_text = find_line(r"STOP HERE if EITHER hash does not match")
    # The WRAPPER-INVOCATION line: runs capture-session.sh directly (bash .../capture-session.sh),
    # distinct from the two "aws s3 cp ... capture-session.sh" delivery lines above (those name the
    # file as a COPY TARGET, never as `bash <path>`).
    wrapper_line, wrapper_text = find_line(r"^\s*IRPT_CAPTURE_PORTAL_ORIGIN=.*bash /opt/investor-reporting-export/capture-session\.sh\s*$")

    found = {"cjs delivery (aws s3 cp)": cjs_deliver_line, "sh delivery (aws s3 cp)": sh_deliver_line,
             "sha256sum step": hash_line, "expected cjs hash line": expect_cjs_line,
             "expected sh hash line": expect_sh_line, "STOP instruction": stop_line,
             "wrapper invocation (bash capture-session.sh)": wrapper_line}
    for label, ln in found.items():
        print("  line %-4s  %s" % (ln, label))
        ok &= check("%s found" % label, ln is not None)

    if ok:
        print("  exact command text found:")
        print("    %s" % cjs_deliver_text)
        print("    %s" % sh_deliver_text)
        print("    %s" % hash_text)
        print("    %s" % expect_cjs_text)
        print("    %s" % expect_sh_text)
        print("    %s" % wrapper_text)
        before = [cjs_deliver_line, sh_deliver_line, hash_line, expect_cjs_line, expect_sh_line, stop_line]
        ok &= check("delivery + hash-verification steps ALL precede the wrapper invocation line (%d < %d)"
                     % (max(before), wrapper_line), max(before) < wrapper_line, "(max=%d, wrapper=%d)" % (max(before), wrapper_line))
        ok &= check("STOP instruction textually precedes the wrapper invocation", stop_line < wrapper_line)

    every_time = re.search(r"EVERY time before invoking the wrapper", text) is not None
    print("  'run EVERY time' (not one-time/optional) instruction present: %s" % every_time)
    ok &= check("the runbook states delivery+verify is unconditional (EVERY time), not one-time/optional", every_time)

    if ok:
        print("IBR101-RUNBOOK-DELIVERS-AND-VERIFIES-BEFORE-CAPTURE")
        return 0
    print("FAIL: runbook arm")
    return 1


def list_from(text, name):
    m = re.search(r"const %s = \[(.*?)\];" % name, text, re.S)
    return re.findall(r"'([^']+)'", m.group(1)) if m else None


def arm_origin():
    print("=== ARM origin (cell (c), row W9-S1): ALLOWED_ORIGINS kept typed + a drift detector against")
    print("=== the renderer's ACTUAL runtime-read source (not asserted equal to itself) ===")
    ok = True
    cap = open(os.path.join(REPO, CAP), encoding="utf-8").read()
    allowed = list_from(cap, "ALLOWED_ORIGINS")
    print("  capture-session.cjs ALLOWED_ORIGINS: %s" % allowed)

    # The renderer (render_export.cjs) READS its origin from env var IRPT_PORTAL_ORIGIN
    # (infra/aws/ec2/investor-reporting-export/render_export.cjs:141, need('IRPT_PORTAL_ORIGIN')).
    # That env var's VALUE is set by two Terraform writers that must themselves agree, walked to
    # their common root:
    renderer_src = os.path.join(REPO, SRC_DIR, "render_export.cjs")
    render_text = open(renderer_src, encoding="utf-8").read()
    reads_env_var = "need('IRPT_PORTAL_ORIGIN')" in render_text
    print("  render_export.cjs reads IRPT_PORTAL_ORIGIN at runtime: %s (%s)" % (reads_env_var, renderer_src))
    ok &= check("renderer reads IRPT_PORTAL_ORIGIN (not a fixed allowlist of its own -- row W9-S1)", reads_env_var)

    main_tf = os.path.join(REPO, "infra/aws/terraform/investor-reporting/export/main.tf")
    lambda_tf = os.path.join(REPO, "infra/aws/terraform/investor-reporting/export/lambda.tf")
    ssm_tf = os.path.join(REPO, "infra/aws/terraform/investor-reporting/export/ssm.tf")
    main_text = open(main_tf, encoding="utf-8").read()
    lambda_text = open(lambda_tf, encoding="utf-8").read()
    ssm_text = open(ssm_tf, encoding="utf-8").read()
    m = re.search(r'portal_origin\s*=\s*"([^"]+)"', main_text)
    root_value = m.group(1) if m else None
    lines = main_text.splitlines()
    root_line = next((i + 1 for i, ln in enumerate(lines) if 'portal_origin    = "' in ln), None)
    print("  root value: local.portal_origin = %r at infra/aws/terraform/investor-reporting/export/main.tf:%s" % (root_value, root_line))
    ok &= check("root value found (main.tf's local.portal_origin, the ONLY literal assignment)", root_value is not None)

    lambda_wires = re.search(r"IRPT_PORTAL_ORIGIN\s*=\s*local\.portal_origin", lambda_text) is not None
    ok &= check("lambda.tf wires the controller's env var to THIS SAME local (no second literal)", lambda_wires)
    ssm_wires = "IRPT_PORTAL_ORIGIN='{{PortalOrigin}}'" in ssm_text
    ok &= check("ssm.tf forwards the document parameter into the SAME env var name on the host (no default of its own -- the controller supplies it)", ssm_wires)

    ok &= check("capture-session.cjs's typed ALLOWED_ORIGINS[0] EQUALS the renderer's root value (drift detector, not tautology)",
                allowed is not None and len(allowed) == 1 and allowed[0] == root_value,
                "(tool=%r root=%r)" % (allowed, root_value))

    # The detector must be able to go NON-ZERO: prove it against a deliberately drifted copy.
    drifted = re.sub(r"(const ALLOWED_ORIGINS = \[)'[^']+'(\];)", r"\1'https://drifted.example'\2", cap)
    drifted_allowed = list_from(drifted, "ALLOWED_ORIGINS")
    ok &= check("drift detector is NON-VACUOUS: a mutated ALLOWED_ORIGINS is caught as NOT equal to the root value",
                drifted_allowed is not None and drifted_allowed[0] != root_value)

    no_dev_local = allowed is not None and all(o.startswith("https://") and "localhost" not in o for o in allowed)
    print("  No DEV/localhost origin admitted (CTO ruling msg 99312, W9-S1): %s" % no_dev_local)
    ok &= check("no allowed origin is http:// or contains 'localhost'", no_dev_local)

    if ok:
        print("IBR101-ALLOWLIST-TYPED-WITH-LIVE-DRIFT-DETECTOR")
        return 0
    print("FAIL: origin arm")
    return 1


ARMS = {"redirect": arm_redirect, "runbook": arm_runbook, "origin": arm_origin}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rtj_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
