"""IRPT_BCKEND round 166 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of five orders (CTO ROUND-166 ANALYSIS msg 6503, section 3):
  IB166-1  IB-pr-476  the performance reader: C-CHAINCLAIM (claim by the excluded day's status) and PARTIAL only when an absence holds (worker ~331)
  IB166-2  IB-pr-477  the capture: a challenged stored-bundle probe ends the run without a fresh sign-in; the pair gate (worker ~332)
  IB166-3  IB-pr-478  the packager reads commentary_ref from the item's sibling attribute; a round-trip test (worker ~333)
  IB166-4  IB-pr-479  every reader of value_facts (backend and portal) and the contract's two members in both schema copies (worker ~334)
  IB166-5  IB-pr-480  every reader of the landed prices store, and whether a served figure depends on it (worker ~335)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Base: every criterion FAILs (no file).
Every verdict and count in a record is the worker's; these checks grade the form, the sums, that each cite exists, and that a named test runs green.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~%d/"
INV = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"
CHK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/"
TOS = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/"
ZERO_KEYS = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
IR = "infra/aws/lambda/investor-reporting"
PERF = IR + "/performance"
HOST = "infra/aws/ec2/investor-reporting-ycharts"
EXPECT_COUNTS = {"49F": {"SI": 23, "YTD": 19, "QTD": 2, "1Y": 20}, "orion": {"SI": 894, "YTD": 200, "QTD": 7, "1Y": 240}}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB166"))
    sys.exit(1)


def run(cmd, cwd=None, timeout=240):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout after %ss: %s" % (timeout, " ".join(cmd)[:120]))
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def pytest(target, timeout=300):
    rc, out = run([sys.executable, "-m", "pytest", target, "-q", "--color=no", "-p", "no:cacheprovider"], timeout=timeout)
    m = re.findall(r"(\d+) (passed|failed|error|errors)", out.splitlines()[-1] if out.strip() else "")
    c = {k: int(n) for n, k in m}
    return rc, c.get("passed", 0), c.get("failed", 0) + c.get("error", 0) + c.get("errors", 0), out


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def cite_ok(c):
    m = re.match(r"^([^:]+):(\d+)(?:-(\d+))?$", str(c).strip())
    if not m:
        return False
    f = ROOT / m.group(1)
    if not f.is_file():
        return False
    n = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
    return 1 <= int(m.group(2)) <= n and (m.group(3) is None or int(m.group(3)) <= n)


def need_cites(rec, label):
    bad = [c for c in (rec or []) if not cite_ok(c)]
    if not rec or bad:
        fail("%s: %d cite(s), unresolved: %s" % (label, len(rec or []), bad[:3]))


def zeros(d):
    for k in ZERO_KEYS:
        if d.get(k) != 0:
            fail("%s must read 0, reads %r" % (k, d.get(k)))


def base_ok(rec):
    if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
        fail("base_commit")


def links():
    rc, out = run(["git", "ls-files", "-s"])
    return {ln.split("\t", 1)[1] for ln in out.splitlines() if ln.startswith("160000 ") and "\t" in ln}


def changed_outside(base, serial_n, extra=()):
    """files changed against base (committed, staged or untracked) outside the worker's deliverables, its rows, its order, the issuer's
    check folder, any gitlink, and the product prefixes `extra` the order grants"""
    rc, out = run(["git", "diff", "--name-only", base])
    if rc != 0:
        fail("git diff against %r: %s" % (base, out[:120]))
    rc2, out2 = run(["git", "ls-files", "--others", "--exclude-standard"])
    names = [n.strip() for n in (out + "\n" + out2).splitlines() if n.strip()]
    ok = (D % serial_n, INV, TOS, CHK) + tuple(extra)
    lk = links()
    return [n for n in names if not n.startswith(ok) and n not in lk]


def one_line(s, lo=40):
    if not isinstance(s, str) or len(s.strip()) < lo:
        fail("a statement of at least %d characters is missing" % lo)


def arms(out, minimum):
    ls = [ln for ln in out.splitlines() if ln.startswith("ARM ")]
    if len(ls) < minimum or any(not ln.rstrip().endswith("PASS") for ln in ls):
        fail("%d ARM line(s), %d not PASS (need >= %d all PASS)" % (len(ls), sum(1 for ln in ls if not ln.rstrip().endswith("PASS")), minimum))
    return len(ls)


def test_file(tf, minimum, label):
    if not (ROOT / tf).is_file():
        fail("no %s" % tf)
    rc, p, f, out = pytest(tf)
    if rc != 0 or p < minimum or f:
        fail("%s: rc %s, %s passed, %s failed (need >= %d passed, 0 failed)" % (tf, rc, p, f, minimum))
    print("OK: %s: %d test(s) pass" % (label, p))


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB166-1":
        n = 331
        if arm == "AC1":
            test_file(PERF + "/tests/test_chain_claim.py", 4, "the claim by the excluded day's status")
        elif arm == "AC2":
            test_file(PERF + "/tests/test_partial_only_when_absence_holds.py", 3, "PARTIAL only when an absence holds")
        elif arm == "AC3":
            rec = load(D % n + "IB166-1_reader_record.json")
            base_ok(rec)
            # AMENDMENT (issuer defect, worker ~331's row D2-W331-S2): the CTO's v0.49 counts are the accounts the RULE REACHES. The accounts whose
            # claim actually MOVES from measured to inferred are fewer where an account was already inferred at base for a missing trading day
            # (row D2-W319-S1). Both are required, and they must agree by arithmetic: fires - already_inferred = moves, per cell.
            if rec.get("rule_fires_counts") != EXPECT_COUNTS:
                fail("rule_fires_counts %r != the CTO's v0.49 counts %r (read at the cap day 2026-10-08)" % (rec.get("rule_fires_counts"), EXPECT_COUNTS))
            fires, already, moves = rec.get("rule_fires_counts") or {}, rec.get("rule_fires_on_accounts_already_inferred_at_base") or {}, rec.get("claim_move_counts") or {}
            for e in EXPECT_COUNTS:
                for w in EXPECT_COUNTS[e]:
                    try:
                        if fires[e][w] - already[e][w] != moves[e][w] or already[e][w] < 0:
                            fail("%s %s: fires %s - already inferred %s != claim_move_counts %s" % (e, w, fires[e][w], already[e][w], moves[e][w]))
                    except (KeyError, TypeError):
                        fail("claim_move_counts, rule_fires_counts and rule_fires_on_accounts_already_inferred_at_base must each hold {49F, orion} x {SI, YTD, QTD, 1Y}")
            cons = rec.get("consumers_of_claim_and_state") or []
            need_cites([c.get("cite") for c in cons], "consumers_of_claim_and_state")
            ab = rec.get("absences") or []
            if len(ab) < 3 or any(a.get("verdict") not in ("ALWAYS_HOLDS", "CONDITIONAL") or not cite_ok(a.get("cite")) for a in ab):
                fail("absences: at least 3, each ALWAYS_HOLDS or CONDITIONAL with a resolving cite")
            if rec.get("figures_unchanged") is not True or not isinstance(rec.get("figures_compared"), int) or rec["figures_compared"] < 1:
                fail("figures_unchanged must be true over figures_compared >= 1")
            cap = rec.get("latest_landed_day")
            if cap != "2026-10-08":
                fail("latest_landed_day must be 2026-10-08, the day the counts were taken")
            zeros(rec)
            bad = changed_outside(rec["base_commit"], n, (PERF + "/",))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: the rule reaches the CTO's 8 counts and the literal moves agree by arithmetic; %d consumer(s); %d absence(s) judged" % (len(cons), len(ab)))
        else:
            fail("unknown arm")
    elif cell == "IB166-2":
        n = 332
        if arm == "AC1":
            tf = HOST + "/tests/stored_bundle_challenge_and_pair_gate.js"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, out = run(["node", "--require", "./tests/netguard.js", "tests/stored_bundle_challenge_and_pair_gate.js"], cwd=ROOT / HOST)
            if rc != 0:
                fail("stored_bundle_challenge_and_pair_gate.js rc %s" % rc)
            print("OK: %d arms PASS" % arms(out, 4))
        elif arm == "AC2":
            rc, out = run(["node", "--require", "./tests/netguard.js", "tests/probe_challenge_and_pair.js"], cwd=ROOT / HOST)
            if rc != 0:
                fail("probe_challenge_and_pair.js rc %s (rc 0 and 9 arms at base)" % rc)
            print("OK: the round-165 probe test still has %d arms PASS" % arms(out, 9))
        elif arm == "AC3":
            rec = load(D % n + "IB166-2_stored_bundle_record.json")
            base_ok(rec)
            if rec.get("refresh_calls_on_challenge") != 0:
                fail("refresh_calls_on_challenge must be 0")
            one_line(rec.get("challenge_ending_in_words"))
            one_line(rec.get("pair_gate_rule_in_words"))
            if rec.get("request_sent") is not False or rec.get("deployed") is not False:
                fail("request_sent and deployed must be false")
            bad = changed_outside(rec["base_commit"], n, (HOST + "/", IR + "/ycharts/session/"))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: record complete; no fresh sign-in on a challenged stored-bundle probe")
        else:
            fail("unknown arm")
    elif cell == "IB166-3":
        n = 333
        if arm == "AC1":
            test_file(IR + "/ycharts/research/tests/test_commentary_ref_round_trip.py", 3, "the commentary_ref round trip")
        elif arm == "AC2":
            rc, p, f, out = pytest(IR + "/ycharts/research/tests")
            if rc != 0 or f or p < 305:
                fail("research tests: rc %s, %s passed, %s failed (base 302 passed; need >= 305, 0 failed)" % (rc, p, f))
            print("OK: research tests %d passed" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB166-3_commentary_ref_record.json")
            base_ok(rec)
            need_cites(rec.get("cites"), "cites")
            one_line(rec.get("reader_rule_in_words"))
            if not rec.get("record_immutable_test"):
                fail("record_immutable_test (the test that proves the record's bytes are unchanged) is missing")
            dw = rec.get("deployed_where") or {}
            if not dw.get("function_family") or not cite_ok(dw.get("cite")):
                fail("deployed_where needs function_family and a resolving cite (the source map or the resident package list)")
            if rec.get("request_sent") is not False or rec.get("deployed") is not False:
                fail("request_sent and deployed must be false")
            bad = changed_outside(rec["base_commit"], n, (IR + "/ycharts/research/", IR + "/ycharts/generate/", IR + "/reports/"))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: record complete; deployed_where %s" % dw["function_family"])
        else:
            fail("unknown arm")
    elif cell == "IB166-4":
        n = 334
        if arm == "AC1":
            rec = load(D % n + "IB166-4_value_facts_readers.json")
            base_ok(rec)
            if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get("portal_commit", ""))):
                fail("portal_commit must be the 40-hex commit of the portal checkout you read")
            if not (re.fullmatch(r"[0-9a-f]{40}", str(rec.get("portal_dev_head", ""))) or (rec.get("portal_dev_head") is None and rec.get("portal_dev_head_reason"))):
                fail("portal_dev_head: 40 hex, or null with portal_dev_head_reason")
            br = rec.get("backend_readers") or []
            if len(br) < 3:
                fail("backend_readers: fewer than 3")
            need_cites([r.get("cite") for r in br], "backend_readers")
            pr = rec.get("portal_readers") or []
            if not pr or any(not re.match(r"^src/[^:]+:\d+", str(r.get("cite", ""))) or not r.get("reads_names") for r in pr):
                fail("portal_readers: at least 1, each {cite: 'src/...:line', reads_names, in_words}")
            for k in ("backend_census", "portal_census"):
                c = rec.get(k) or {}
                if not (c.get("pattern") and isinstance(c.get("files_searched"), int) and c["files_searched"] > 0 and isinstance(c.get("files_with_a_hit"), int)):
                    fail("%s needs pattern, files_searched > 0, files_with_a_hit" % k)
            if not isinstance(rec.get("not_established"), list):
                fail("not_established is not a list")
            zeros(rec)
            bad = changed_outside(rec["base_commit"], n, (IR + "/_contracts/", "docs/contracts/investor-reporting/"))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: %d backend and %d portal reader(s) read; portal at %s" % (len(br), len(pr), rec["portal_commit"][:10]))
        elif arm == "AC2":
            try:
                import jsonschema
            except ImportError:
                fail("jsonschema is not importable")
            paths = [IR + "/_contracts/PerformanceReport.schema.json", "docs/contracts/investor-reporting/v1/PerformanceReport.schema.json"]
            # AMENDMENT (issuer defect, worker ~334's report): a contract fixture is a wrapper {_fixture, _source, _expect, instance};
            # the schema validates its `instance` member, as the contract tests do.
            valid = load(IR + "/_contracts/fixtures/PerformanceReport.valid.json")
            invalid = load(IR + "/_contracts/fixtures/PerformanceReport.invalid.json")
            valid = valid.get("instance", valid)
            invalid = invalid.get("instance", invalid)
            for sp in paths:
                sch = load(sp)
                vf = (((sch.get("properties") or {}).get("optional_facts") or {}).get("properties") or {}).get("value_facts") or {}
                props = vf.get("properties") or {}
                for m in ("start_value", "end_value"):
                    t = (props.get(m) or {}).get("type")
                    t = t if isinstance(t, list) else [t]
                    if "number" not in t or "null" not in t:
                        fail("%s: value_facts.properties.%s must be number-or-null, reads %r" % (sp, m, props.get(m)))
                if vf.get("additionalProperties") is False:
                    fail("%s: the other members of value_facts must stay open" % sp)
                cls = jsonschema.validators.validator_for(sch)
                v = cls(sch)
                if list(v.iter_errors(valid)):
                    fail("%s: the valid fixture no longer validates" % sp)
                if not list(v.iter_errors(invalid)):
                    fail("%s: the invalid fixture now validates" % sp)
                good = json.loads(json.dumps(valid))
                good.setdefault("optional_facts", {})["value_facts"] = {"start_value": 1.5, "end_value": None, "currency": "USD"}
                if list(v.iter_errors(good)):
                    fail("%s: a value_facts with the two members and an open member does not validate" % sp)
                bad = json.loads(json.dumps(good))
                bad["optional_facts"]["value_facts"]["start_value"] = "not a number"
                if not list(v.iter_errors(bad)):
                    fail("%s: a string start_value validates (the negative control)" % sp)
            print("OK: both schema copies declare the two members; the fixtures and the controls behave")
        elif arm == "AC3":
            rc, p, f, out = pytest(IR + "/_contracts")
            known = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve", "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]")
            failed = re.findall(r"^FAILED \S+::(\S+)", out, re.M)
            if p < 203 or f > 2 or any(not any(k in x for k in known) for x in failed):
                fail("_contracts suite: %d passed, %d failed %s (base: 203 passed, 2 failed, the two known)" % (p, f, failed))
            print("OK: _contracts suite %d passed, %d failed (the two known)" % (p, f))
        else:
            fail("unknown arm")
    elif cell == "IB166-5":
        n = 335
        rec = load(D % n + "IB166-5_prices_store_readers.json")
        if arm == "AC1":
            base_ok(rec)
            if not rec.get("store_key"):
                fail("store_key (the object key or name of the landed prices store) is missing")
            rd = rec.get("readers")
            if not isinstance(rd, list):
                fail("readers is not a list (an empty list says there is none)")
            need_cites([r.get("cite") for r in rd], "readers") if rd else None
            c = rec.get("census") or {}
            if not (c.get("pattern") and isinstance(c.get("files_searched"), int) and c["files_searched"] > 0 and isinstance(c.get("files_with_a_hit"), int)
                    and c.get("positive_control")):
                fail("census needs pattern, files_searched > 0, files_with_a_hit and a positive_control")
            if rec.get("verdict") not in ("NO_READER", "READERS_NONE_SERVED", "SERVED_FIGURE_DEPENDS"):
                fail("verdict %r" % rec.get("verdict"))
            one_line(rec.get("in_words"))
            print("OK: %d reader(s), verdict %s, census %d files" % (len(rd), rec["verdict"], c["files_searched"]))
        elif arm == "AC2":
            rd = rec.get("readers") or []
            v = rec.get("verdict")
            served = [r for r in rd if r.get("feeds_served_figure") is True]
            if (v == "NO_READER") != (len(rd) == 0):
                fail("verdict NO_READER exactly when readers is empty")
            if (v == "SERVED_FIGURE_DEPENDS") != bool(served):
                fail("verdict SERVED_FIGURE_DEPENDS exactly when a reader has feeds_served_figure true")
            for r in rd:
                if r.get("feeds_served_figure") not in (True, False, "NOT_ESTABLISHED"):
                    fail("a reader's feeds_served_figure is not true, false or NOT_ESTABLISHED")
                one_line(r.get("in_words"), 20)
            if v == "SERVED_FIGURE_DEPENDS" and not rec.get("dependent_figures"):
                fail("dependent_figures (which served figures) is missing")
            if not isinstance(rec.get("not_established"), list):
                fail("not_established is not a list")
            print("OK: verdict %s agrees with %d reader(s), %d feeding a served figure" % (v, len(rd), len(served)))
        elif arm == "AC3":
            zeros(rec)
            bad = changed_outside(rec.get("base_commit", ""), n)
            if bad:
                fail("a read edits no file outside its deliverables, but changed: %s" % bad[:3])
            print("OK: bounds hold; nothing outside the deliverables changed")
        else:
            fail("unknown arm")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
