#!/usr/bin/env python3
"""BATTERY IB-rt-1 -- THE SEAM. Five arms, each on the REAL artifact.

  (a) ONE CARRIER            the published routes.json IS the file Terraform reads
  (b) ELEVEN THROUGH THE     the consumer's request, the real dispatcher, the real handler,
      REAL DISPATCHER        the response graded against the producer schema
  (c) TWENTY-TWO NEGATIVES   mismatched version -> CONTRACT_VERSION; wrong firm -> FirmBinding,
                             0 protected bytes
  (d) THE API ROOT IS CLEAN  terraform plan after the carrier move
  (e) C-S77 REISSUED         the addendum, at the apply vintage, three things distinguished

NO SELF-WRAPPING HARNESS (bound 12). Every subject is the artifact the world uses: the published
contract file, `_authz/dispatch.py`, the handler modules named by `lambda-source-map.json` and
their own Terraform `handler =` declaration, the vendored `.tools/terraform.exe` against the real
state. Nothing is wrapped, patched or re-registered by this battery for this battery's benefit.
Every count PRINTS ITS DENOMINATOR and a `0 of 0` is printed as VACUOUS, never as a pass.

NO NETWORK, NO VENDOR CALL, NO DEPLOY. `terraform plan` is a READ of existing state.

ASCII only. Exit 0 always: the TOKEN is the verdict, not the exit code.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
V1 = os.path.join(REPO, "docs", "contracts", "investor-reporting", "v1")
API_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "api")
TESTS = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_contracts", "tests")
SEAM_TEST = os.path.join(TESTS, "test_seam_paired.py")
ADDENDUM = os.path.join(HERE, "S15-AC3_reissued_at_apply_vintage.md")

RESULTS = []


def arm(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))
    print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def head(text, n=1200):
    return text if len(text) <= n else text[:n] + " ...[truncated]"


# --------------------------------------------------------------------- (a) ONE CARRIER
def arm_a():
    print("\n=== ARM (a) ONE CARRIER ==========================================")
    contract_routes = os.path.join(V1, "routes.json")
    routes_tf = os.path.join(API_ROOT, "routes.tf")
    with open(routes_tf, "r", encoding="utf-8") as fh:
        tf_src = fh.read()

    # THE MECHANISM, READ RATHER THAN ASSERTED. routes.tf must resolve the contract path itself;
    # this battery re-derives the path from the HCL expression and hashes what THAT resolves to,
    # so "byte-equals" is a statement about the file Terraform opens, not about a path typed here.
    m = re.search(r'contract_routes_path\s*=\s*"\$\{path\.module\}/([^"]+)"', tf_src)
    if not m:
        arm("a1 mechanism", False, "routes.tf declares no ${path.module}-relative contract path")
        return
    resolved = os.path.abspath(os.path.join(API_ROOT, m.group(1).replace("/", os.sep)))
    reads_it = "jsondecode(file(local.contract_routes_path))" in tf_src
    print("    mechanism: routes.tf declares contract_routes_path = ${path.module}/%s" % m.group(1))
    print("               and reads it with jsondecode(file(local.contract_routes_path)): %s"
          % reads_it)
    print("    resolves to: %s" % resolved)
    print("    published  : %s" % contract_routes)
    h_resolved = sha256(resolved)
    h_published = sha256(contract_routes)
    print("    sha256(what Terraform opens) = %s" % h_resolved)
    print("    sha256(the published file)   = %s" % h_published)
    same_file = os.path.normcase(resolved) == os.path.normcase(os.path.abspath(contract_routes))
    arm("a1 one carrier", reads_it and h_resolved == h_published and same_file,
        "Terraform opens the published file itself (same path, identical sha256) -- there is no "
        "copy to drift")

    # The RETIRED carrier must point, not carry.
    with open(os.path.join(API_ROOT, "routes.json"), "r", encoding="utf-8") as fh:
        old = json.load(fh)
    arm("a2 retired carrier", "routes" not in old and "_the_carrier" in old,
        "the api root's routes.json carries no `routes` key and names the carrier: %s"
        % old.get("_the_carrier"))

    # The eleven schemas.
    names = sorted(f[: -len(".schema.json")] for f in os.listdir(V1)
                   if f.endswith(".schema.json"))
    bad = []
    for n in names:
        with open(os.path.join(V1, n + ".schema.json"), "r", encoding="utf-8") as fh:
            d = json.load(fh)
        if "/v1/" not in d.get("$id", ""):
            bad.append("%s: $id lacks v1" % n)
        if d.get("x-contract-version") != "v1":
            bad.append("%s: x-contract-version" % n)
        if ((d.get("properties") or {}).get("contract_version") or {}).get("const") != "v1":
            bad.append("%s: contract_version property" % n)
    arm("a3 schemas versioned", len(names) == 11 and not bad,
        "%d of 11 schemas carry $id with v1, x-contract-version and a contract_version property; "
        "defects: %s" % (len(names), bad or "none"))

    # CONTRACT.md's field census, RE-DERIVED here rather than trusted from the document
    # (bound 12: a manifest a cell writes is re-derived by its battery every run).
    total = quoted = 0
    for n in names:
        with open(os.path.join(V1, n + ".schema.json"), "r", encoding="utf-8") as fh:
            d = json.load(fh)
        for fname, fdef in (d.get("properties") or {}).items():
            if fname == "contract_version":
                continue
            total += 1
            if str((fdef or {}).get("description", "")).startswith("PRD CONTRACTS "):
                quoted += 1
    with open(os.path.join(V1, "CONTRACT.md"), "r", encoding="utf-8") as fh:
        md = fh.read()
    named = sum(1 for n in names if ("### `%s`" % n) in md)
    print("    field census RE-DERIVED from the schemas: %d of %d top-level properties cite a PRD "
          "location" % (quoted, total))
    arm("a4 CONTRACT.md census", total > 0 and quoted == total and named == 11,
        "%d of %d fields carry a PRD citation and %d of 11 schemas have a section in CONTRACT.md"
        % (quoted, total, named))


# ----------------------------------------------------- (b) + (c) the paired suite
def run_pytest():
    """Returns (rc, stdout, junit_path). THE CENSUS READS THE XML, NEVER THE PROSE.

    A count scraped from pytest's terminal summary reads the TOOL, not the run: the lines are
    ANSI-coloured, the verb moves between versions, and a regex that matches nothing returns a
    confident ZERO. The first run of this battery did exactly that -- 22 passing negatives were
    reported as `0 of 11` twice, and a zero is the shape that gets acted on. The JUnit XML is the
    machine-readable result of the same run; the terminal output is kept only for the verbatim
    deciding lines a human reads.
    """
    junit = os.path.join(REPO, ".scratch", "ibrt1_seam_junit.xml")
    os.makedirs(os.path.dirname(junit), exist_ok=True)
    cmd = [sys.executable, "-m", "pytest", SEAM_TEST, "-q", "--no-header", "-rA",
           "--color=no", "--junitxml=" + junit]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=540)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or ""), junit


def junit_census(junit_path, prefix):
    """(passed, failed, xfailed) for every case whose NAME starts with `prefix`.

    A prefix that matches no case returns (0, 0, 0) AND is reported as VACUOUS by the caller --
    an empty match is never a pass.
    """
    import xml.etree.ElementTree as ET
    tree = ET.parse(junit_path)
    p = f = x = 0
    for case in tree.iter("testcase"):
        if not (case.get("name") or "").startswith(prefix):
            continue
        kinds = {child.tag for child in case}
        if "failure" in kinds or "error" in kinds:
            f += 1
        elif "skipped" in kinds:
            # pytest records an xfail as <skipped type="pytest.xfail">.
            x += 1
        else:
            p += 1
    return p, f, x


def seam_module():
    """Import the paired suite's own module. NOT A WRAP -- the SAME measurement, read twice.

    `classify_operation` drives the REAL dispatcher into the REAL handler entry points and is the
    single place that walk exists. The battery calls it rather than re-implementing it, so the
    suite's verdict and this acceptance evidence cannot disagree about what happened; a battery
    with its own copy of the walk is two instruments that will eventually report different worlds.
    """
    if TESTS not in sys.path:
        sys.path.insert(0, TESTS)
    import test_seam_paired as seam
    return seam


def arm_bc():
    print("\n=== ARMS (b) + (c) THE PAIRED SUITE ==============================")
    try:
        rc, out, junit = run_pytest()
    except subprocess.TimeoutExpired:
        arm("b paired", False, "rc 124 -- pytest did not terminate within 540s")
        arm("b response contracts", False, "not reached")
        arm("c negatives", False, "not reached")
        return
    tail = [ln for ln in out.splitlines() if ln.strip()][-1:]
    print("    pytest rc=%d  last line: %s" % (rc, tail[0] if tail else "(no output)"))
    print("    census instrument: %s (the run's own JUnit XML, not its terminal prose)" % junit)

    def census(prefix):
        p, f, x = junit_census(junit, prefix)
        if p + f + x == 0:
            print("    WARN: VACUOUS -- no test case named %s* in the XML; 0 of 0 is not a pass"
                  % prefix)
        return p, f, x

    seam = seam_module()

    # ---- (b1) THE PUBLISHED RESPONSE CONTRACTS. This is the half of arm (b) that IS this cell's.
    routes, routes_path = seam.dp.load_routes()
    declared = [r for r in routes if r.get("status") == "DECLARED"]
    no_handler = [r for r in routes if r.get("status") != "DECLARED"]
    print("    (b1) response contracts -- denominator: %d route(s) in %s = %d DECLARED + %d "
          "NO-HANDLER-AT-HEAD" % (len(routes), os.path.basename(routes_path), len(declared),
                                  len(no_handler)))
    p_rc, f_rc, _x = census("test_every_declared_route_has_a_response_contract")
    published = sum(1 for r in declared
                    if seam.response_contract(r["operation"]) is not None)
    print("        published, valid as schemas, every data $ref resolved ... %d of %d DECLARED"
          % (published, len(declared)))
    for r in no_handler:
        print("        %s: NO response contract, and that is the answer -- it answers nothing"
              % r["operation"])
    arm("b1 response contracts", published == len(declared) == 11 and p_rc == 1 and f_rc == 0,
        "%d of %d DECLARED routes carry a response contract that validates as a schema and whose "
        "`data` $refs all resolve to a published document schema" % (published, len(declared)))

    # ---- (b2) THE CONTROL. A `0 of 11` from a BROKEN validator reads exactly like a `0 of 11`
    # from non-conforming handlers, so CONFORMS is proven REACHABLE before the census is quoted.
    p_ctl, f_ctl, _x = census("test_control_")
    print("        control: a known-good document CONFORMS and a known-bad one does NOT, per "
          "response contract .... %d of %d control case(s) pass" % (p_ctl, p_ctl + f_ctl))
    arm("b2 CONFORMS is reachable", p_ctl > 0 and f_ctl == 0,
        "%d of %d controls pass: the positive case is REACHABLE, so a 0 in the census below is a "
        "fact about the handlers and not about the validator" % (p_ctl, p_ctl + f_ctl))

    # ---- (b3) THE PAIRED CENSUS, four closed outcomes, every operation in exactly one.
    print("    (b) 11 operations, each dispatched through the REAL dispatcher into the REAL "
          "handler entry point declared by Terraform:")
    tally = {k: 0 for k in seam.OUTCOMES}
    for op, method, path, schema_name in seam.OPERATIONS:
        outcome, detail = seam.classify_operation(op, method, path, schema_name)
        tally[outcome] += 1
        print("        %-20s %-18s %s" % (op, outcome, detail[:150]))
    total = sum(tally.values())
    print("        ---")
    print("        CONFORMS .................. %d of 11" % tally["CONFORMS"])
    print("        BLOCKED-BY-W2-S16 ......... %d of 11   (IB-rt-2 arm (g) owns and deploys the "
          "six handlers)" % tally["BLOCKED-BY-W2-S16"])
    print("        DEPLOYED-ONLY ............. %d of 11   (row W2-S15; graded at IB-rtb-1)"
          % tally["DEPLOYED-ONLY"])
    print("        NOT-A-ROUTE ............... %d of 11   (row W2-S13; named in routes.json with "
          "its reason)" % tally["NOT-A-ROUTE"])
    p_pair, f_pair, _x = census("test_paired_consumer_request_through_the_real_dispatcher")
    # THE COUNT DOES NOT WITHHOLD THE TOKEN (the re-cut says so explicitly). What DOES withhold it
    # is an operation this cell could not classify at all, or a paired case that errored -- either
    # means the seam was not measured, which is a different thing from measuring a zero.
    arm("b paired census", total == 11 and f_pair == 0 and p_pair == 11,
        "%d of 11 operations classified into the four closed outcomes with 0 unclassified, and "
        "%d of 11 paired cases ran clean. CONFORMING: %d of 11 -- that count does NOT withhold "
        "the token: handler conformance is IB-rt-2 arm (g), and this cell publishes the contract "
        "the handlers must meet" % (total, p_pair, tally["CONFORMS"]))

    # ---- (c) 11 version negatives + 11 firm negatives = 22.
    pv, fv, _x = census("test_negative_mismatched_contract_version")
    pf, ff, _x = census("test_negative_wrong_firm_is_refused_with_zero_protected_bytes")
    print("    (c) mismatched X-Contract-Version refused with CONTRACT_VERSION, refused value "
          "never echoed ... %d of 11" % pv)
    print("        wrong firm refused through FirmBinding, 0 protected bytes in the envelope "
          "....... %d of 11" % pf)
    arm("c twenty-two negatives", pv == 11 and pf == 11 and fv == 0 and ff == 0,
        "%d of 22 negatives pass (%d version + %d firm); byte census: every refusal envelope was "
        "serialised and searched for the refused version string, the claimed firm token, the "
        "bound opaque firm id, a client surname and an e-mail address -- 0 bytes of any of them "
        "in any envelope. The ad-hoc envelopes printed above carry KEYS ONLY, asserted free of "
        "the same five strings before printing." % (pv + pf, pv, pf))

    if f_pair or fv or ff or f_ctl or f_rc:
        print("\n    --- the deciding failure lines, verbatim ---")
        for ln in out.splitlines():
            if ln.startswith("FAILED ") or ln.startswith("E   Assertion"):
                print("    " + head(ln, 300))


# --------------------------------------------------------------------- (d) THE PLAN
def arm_d():
    print("\n=== ARM (d) THE API ROOT IS CLEAN AFTER THE MOVE =================")
    tf = os.path.join(REPO, ".tools", "terraform.exe")
    if not os.path.isfile(tf):
        arm("d plan", False, "BLOCKED: .tools/terraform.exe absent (it is gitignored; a PATH "
                             "substitute would re-pin remote state and is never used)")
        return
    try:
        proc = subprocess.run([tf, "-chdir=" + API_ROOT, "plan", "-no-color", "-lock=false"],
                              capture_output=True, text=True, timeout=540)
    except subprocess.TimeoutExpired:
        arm("d plan", False, "rc 124 -- terraform plan did not terminate within 540s")
        return
    out = (proc.stdout or "") + (proc.stderr or "")
    clean = "No changes. Your infrastructure matches the configuration." in out
    deciding = [ln for ln in out.splitlines()
                if "No changes" in ln or ln.startswith("Plan:") or "Error" in ln]
    for ln in deciding:
        print("    " + ln.strip())
    arm("d plan clean", clean,
        "terraform plan on the api root after the carrier move: %s"
        % (deciding[0].strip() if deciding else "rc=%d, no deciding line" % proc.returncode))


# --------------------------------------------------------------------- (e) C-S77
def arm_e():
    print("\n=== ARM (e) C-S77 REISSUED AT THE APPLY VINTAGE ==================")
    if not os.path.isfile(ADDENDUM):
        arm("e addendum", False, "the addendum does not exist")
        return
    with open(ADDENDUM, "r", encoding="utf-8") as fh:
        text = fh.read()
    # The three things the ruling names, as literal headings. The census is over the THREE the
    # ruling names, subtracted from that list -- not a forward list of what this battery recalls.
    required = ["1. THE INTENDED CLOUDFRONT BEHAVIOR",
                "2. THE CLASSIFIED WAF NORMALISATION",
                "3. THE OBSERVED REFUSAL PLANE"]
    found = [h for h in required if ("### " + h) in text]
    for h in required:
        print("    [%s] %s" % ("x" if h in found else " ", h))
    commits = [c for c in ("a7659fa6af", "ac202969e8") if c in text]
    print("    apply vintage commits named: %d of 2 -- %s" % (len(commits), commits))
    arm("e reissued", len(found) == 3 and len(commits) == 2,
        "%d of 3 headings the ruling names are present and %d of 2 apply commits are named"
        % (len(found), len(commits)))


def main():
    print("BATTERY IB-rt-1 -- THE SEAM")
    print("repo: %s" % REPO)
    print("subjects: the published contract, the real dispatcher, the real handlers, the real "
          "terraform state")
    arm_a()
    arm_bc()
    arm_d()
    arm_e()

    print("\n=== SUMMARY ======================================================")
    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    for n, ok, d in RESULTS:
        print("  %-24s %s" % (n, "PASS" if ok else "FAIL"))
    print("  %d of %d arms PASS" % (passed, len(RESULTS)))
    if passed == len(RESULTS):
        print("\nIBRT1-SEAM-PUBLISHED")
    else:
        print("\nBLOCKED: %d of %d arms FAIL -- the token is withheld." % (len(RESULTS) - passed,
                                                                          len(RESULTS)))
        print("A battery that prints its token beside a failing arm is not evidence, it is a "
              "signature. The failing arm's row is the deliverable.")
        print("NOTE: the CONFORMING count in arm (b) is NOT one of these arms. Per the criterion "
              "re-cut (channel row IRPT_BCKEND-S26) it is REPORTED and does not withhold the "
              "token -- handler conformance is IB-rt-2 arm (g).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
