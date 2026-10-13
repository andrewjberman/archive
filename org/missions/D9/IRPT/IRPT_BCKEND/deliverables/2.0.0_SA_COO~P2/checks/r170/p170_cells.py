"""IRPT_BCKEND round 170 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of four orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB170-1  IB-pr-492  the directory search producer returns an ACCOUNT entry when the query matches an account's tail
    AC1  the worker's new test file passes (6 or more, none failed)
    AC2  the issuer's seam probe on a synthetic directory (tail of a non-head account, a shared tail, the head tail, a name query, an old entry with no masks, resolve)
    AC3  no existing directory test file changed, and the existing suite is no worse than its base (<= 38 failed or errored, >= 173 passed)
  IB170-2  IB-pr-493  an additive account_id member on each 49 Financial ACCOUNT node (builder, contract, fixture, raw_keys)
    AC1  hs._node takes an optional account_id (member only when given) and the worker's new builder tests pass (3 or more)
    AC2  the three HoldingsSnapshot schema copies are byte-identical and name account_id on a node; the valid fixture carries it and validates; the invalid fixture still fails; raw_keys.json names it
    AC3  the existing builder and contract tests still pass
  IB170-3  IB-pr-494  the read-only count of 49 Financial accounts whose node id differs from the directory's account id
    AC1  the record's arithmetic closes (per state: n = equal + differs_resolvable + differs_unresolvable; the states sum to the denominator)
    AC2  the record carries no id, no long digit run and no name key
    AC3  the worker's script is read-only (no write verb in it)
  IB170-4  IB-pr-495  the portal's AnalysisReport wire copy and its generated fixtures carry the extractor's section form
    AC1  no AnalysisReport section_type annualized_return and no section units DECIMAL_FRACTION in the portal fixtures folder or in the two test fixture files
    AC2  the five token-citing portal tests pass (a bound: PASS at base)
    AC3  the portal wire copy's section equals the producer fixture's section
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
DIRQ = "infra/aws/lambda/investor-reporting/directory/"
GOLD = "data/assets/scripts/gold/investor_reporting/"
CONTR = "infra/aws/lambda/investor-reporting/_contracts/"
PORTAL_IR = "portal/src/pages/InvestorReporting/"
COUNT_REC = D + "0.9.0_WK_IRPT_BCKEND~345/IB170-3_node_id_mismatch_count.json"
COUNT_SCRIPT = D + "0.9.0_WK_IRPT_BCKEND~345/mismatch_count.py"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB170"))
    sys.exit(1)


def run(cmd, timeout=100, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout: %s" % " ".join(map(str, cmd))[:100])
    except FileNotFoundError as e:
        fail("not found: %s" % e)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def pytest_counts(target, extra=()):
    rc, out = run([sys.executable, "-m", "pytest", target, "-q", "--no-header", "-p", "no:cacheprovider"] + list(extra), timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    m = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|error|errors)", out)}
    return rc, m.get("passed", 0), m.get("failed", 0), m.get("error", 0) + m.get("errors", 0), out


def probe_directory():
    sys.path.insert(0, str(ROOT / DIRQ))
    import importlib
    hd = importlib.import_module("handler")
    scope = {"principal_class": "STAFF", "permitted_account_set": ["a1", "a2", "a3", "b1", "b2", "z1"],
             "verified_request_firm_id": "f1", "entitlement_revision": "e1", "viewer_policy": {"policy_revision": "p1"}}

    def entry(cid, rid, accts, name, masks, kind="RELATIONSHIP", with_masks=True):
        e = {"ids": {"firm_id": "f1", "client_id": cid, "account_ids": accts}, "display_name": name,
             "masked_discriminator": masks[0], "permitted_scope": {"scope_kind": kind, "scope_ids": [rid or accts[0]]}}
        if rid:
            e["ids"]["relationship_id"] = rid
        if with_masks:
            e["account_masks"] = [{"account_id": a, "masked_discriminator": m} for a, m in zip(accts, masks)]
        return e
    R = entry("c1", "r1", ["a1", "a2", "a3"], "Alpha Beta", ["****1111 / IRA", "****2222 / Joint", "****3333 / Trust"])
    S = entry("c2", "r2", ["b1", "b2"], "Gamma Delta", ["****9999 / IRA", "****2222 / IRA"])
    OLD = entry("c3", None, ["z1"], "Old Entry", ["****7777 / IRA"], kind="ACCOUNT", with_masks=False)
    directory = {"entries": [R, S, OLD]}
    # (a) the tail of a non-head account, shared by two entries: two ACCOUNT results, no RELATIONSHIP result
    ra = hd.search(directory, scope, "2222")
    kinds = [x["scope_kind"] for x in ra["results"]]
    if sorted(kinds) != ["ACCOUNT", "ACCOUNT"]:
        fail("a tail query 2222 (shared by a2 and b2) must return exactly two ACCOUNT results and no relationship result, got %s" % kinds)
    if len({x["entry_id"] for x in ra["results"]}) != 2 or any(x["permitted_account_count"] != 1 for x in ra["results"]):
        fail("the two ACCOUNT results need distinct entry ids and one permitted account each")
    if any("2222" not in str(x["masked_discriminator"]) for x in ra["results"]):
        fail("an ACCOUNT result must carry that account's own mask")
    # (b) resolve of an ACCOUNT result's entry id is exactly that account
    got = set()
    for x in ra["results"]:
        r = hd.resolve(directory, scope, {"entry_id": x["entry_id"]})
        if not r.get("ok") or len(r.get("account_ids", [])) != 1:
            fail("resolve of an ACCOUNT result's entry_id must be ok and exactly one account, got %s" % {k: r.get(k) for k in ("ok", "account_ids")})
        got.add(r["account_ids"][0])
    if got != {"a2", "b2"}:
        fail("the two ACCOUNT results must resolve to a2 and b2, got %s" % sorted(got))
    # (c) the HEAD account's tail: an ACCOUNT result for a1
    rc = hd.search(directory, scope, "1111")
    if [x["scope_kind"] for x in rc["results"]] != ["ACCOUNT"]:
        fail("the head tail 1111 must return one ACCOUNT result, got %s" % [x["scope_kind"] for x in rc["results"]])
    r1 = hd.resolve(directory, scope, {"entry_id": rc["results"][0]["entry_id"]})
    if r1.get("account_ids") != ["a1"]:
        fail("the head tail must resolve to a1, got %s" % r1.get("account_ids"))
    # (d) a name query still returns the relationship entry, with no account entry
    rd = hd.search(directory, scope, "Alpha")
    if [x["scope_kind"] for x in rd["results"]] != ["RELATIONSHIP"]:
        fail("a name query must still return the relationship entry only, got %s" % [x["scope_kind"] for x in rd["results"]])
    # (e) an entry with no account_masks is unchanged
    re_ = hd.search(directory, scope, "7777")
    if [x["scope_kind"] for x in re_["results"]] != ["ACCOUNT"] or re_["count"] != 1:
        fail("an old account-only entry with no masks must be found as before, got %s" % [x["scope_kind"] for x in re_["results"]])
    # (f) the relationship's own resolve still returns all its accounts
    rr = hd.resolve(directory, scope, {"entry_id": hd._entry_key(R)})
    if rr.get("account_ids") != ["a1", "a2", "a3"] and sorted(rr.get("account_ids", [])) != ["a1", "a2", "a3"]:
        fail("resolving the relationship entry must still reach its three accounts, got %s" % rr.get("account_ids"))


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB170-1":
        tf = DIRQ + "tests/test_tail_account_entry.py"
        if arm == "AC1":
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, p, f, e, out = pytest_counts(tf)
            if p < 6 or f or e:
                fail("%s: %d passed, %d failed, %d errors (6 passed and none failed are required)" % (tf, p, f, e))
            print("OK: %d tests pass" % p)
        elif arm == "AC2":
            probe_directory()
            print("OK: the seam probe holds (tail of a non-head account, shared tail, head tail, name query, old entry, resolve, the relationship's own resolve)")
        elif arm == "AC3":
            rc, base = run(["git", "merge-base", "HEAD", "box/dell2"])
            base = base.strip()
            rc, names = run(["git", "diff", "--name-only", base, "--", DIRQ + "tests"])
            rc2, untr = run(["git", "ls-files", "--others", "--exclude-standard", "--", DIRQ + "tests"])
            changed = [n.strip() for n in (names + "\n" + untr).splitlines() if n.strip() and "__pycache__" not in n]
            bad = [n for n in changed if not n.endswith("test_tail_account_entry.py")]
            if bad:
                fail("existing directory test file(s) changed: %s" % bad[:3])
            rc, p, f, e, out = pytest_counts(DIRQ + "tests", ["--ignore=" + tf])
            if f + e > 38 or p < 173:
                fail("the existing directory suite is worse than its base: %d passed, %d failed, %d errors (base 173 / 10 / 28)" % (p, f, e))
            print("OK: no existing test file changed; existing suite %d passed, %d failed, %d errors (base 173 / 10 / 28)" % (p, f, e))
        else:
            fail("unknown criterion")
    elif cell == "IB170-2":
        if arm == "AC1":
            sys.path.insert(0, str(ROOT / GOLD))
            import importlib
            hs = importlib.import_module("holdings_snapshot")
            args = ("acc_x", None, 0, "ACCOUNT", "OBSERVED", 10.0, "USD", "UNIQUE_CUSTODY_TOTAL", 10.0, None, None, "P", "J", 1, 1, "measured")
            try:
                with_id = hs._node(*args, account_id="dir_acc_1")
            except TypeError as e:
                fail("hs._node has no account_id keyword: %s" % str(e)[:100])
            without = hs._node(*args)
            if with_id.get("account_id") != "dir_acc_1" or "account_id" in without:
                fail("account_id must appear only when given (given: %r, not given: %r)" % (with_id.get("account_id"), without.get("account_id")))
            tf = GOLD + "tests/test_holdings_49f_account_id.py"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, p, f, e, out = pytest_counts(tf)
            if p < 3 or f or e:
                fail("%s: %d passed, %d failed, %d errors (3 passed and none failed are required)" % (tf, p, f, e))
            print("OK: _node takes account_id additively; %d builder tests pass" % p)
        elif arm == "AC2":
            copies = [CONTR + "HoldingsSnapshot.schema.json", "infra/aws/lambda/investor-reporting/holdings/contracts/HoldingsSnapshot.schema.json",
                      "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"]
            shas = set()
            for c in copies:
                f = ROOT / c
                if not f.is_file():
                    fail("no %s" % c)
                shas.add(hashlib.sha256(f.read_bytes()).hexdigest())
            if len(shas) != 1:
                fail("the three HoldingsSnapshot schema copies are not byte-identical (%d distinct)" % len(shas))
            schema = load(copies[0])
            node = schema.get("properties", {}).get("nodes", {}).get("items", {})
            if (node.get("properties", {}).get("account_id") or {}).get("type") != "string":
                fail("the schema's node properties must name account_id as a string")
            import jsonschema
            valid = load(CONTR + "fixtures/HoldingsSnapshot.valid.json")
            inst = valid.get("instance", valid)
            accts = [n for n in inst.get("nodes", []) if n.get("node_kind") == "ACCOUNT"]
            if not accts or not all(isinstance(n.get("account_id"), str) and n["account_id"] for n in accts):
                fail("the valid fixture's ACCOUNT node(s) must carry account_id")
            try:
                jsonschema.validate(inst, schema)
            except Exception as e:  # noqa: BLE001
                fail("the valid fixture no longer validates: %s" % str(e)[:140])
            bad = load(CONTR + "fixtures/HoldingsSnapshot.invalid.json")
            try:
                jsonschema.validate(bad.get("instance", bad), schema)
                fail("the invalid fixture now validates (the schema was loosened)")
            except jsonschema.ValidationError:
                pass
            rk = (ROOT / "infra/aws/lambda/investor-reporting/_ids/raw_keys.json").read_text(encoding="utf-8")
            if "account_id" not in rk:
                fail("_ids/raw_keys.json must name account_id")
            print("OK: three identical schema copies name account_id; the valid fixture carries it and validates; the invalid one still fails; raw_keys.json names it")
        elif arm == "AC3":
            rc, p, f, e, out = pytest_counts(GOLD + "tests/test_holdings_49f.py")
            if f or e or p < 22:
                fail("test_holdings_49f.py: %d passed, %d failed, %d errors (base 22 passed)" % (p, f, e))
            rc, p2, f2, e2, out2 = pytest_counts("infra/aws/lambda/investor-reporting/_contracts/tests/test_holdings_classification_members.py")
            if f2 or e2 or p2 < 1:
                fail("test_holdings_classification_members.py: %d passed, %d failed, %d errors" % (p2, f2, e2))
            print("OK: the existing builder (%d) and contract (%d) tests pass" % (p, p2))
        else:
            fail("unknown criterion")
    elif cell == "IB170-3":
        if arm in ("AC1", "AC2"):
            r = load(COUNT_REC)
            if arm == "AC1":
                den = r.get("denominator")
                st = r.get("states") or {}
                if not isinstance(den, int) or isinstance(den, bool) or den < 1 or set(st) != {"served", "refused", "withheld"}:
                    fail("denominator (int >= 1) and states served/refused/withheld are required")
                tot = 0
                for k, v in st.items():
                    try:
                        n, a, b, c = v["n"], v["equal"], v["differs_resolvable"], v["differs_unresolvable"]
                    except KeyError as e:
                        fail("state %s lacks %s" % (k, e))
                    if not all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in (n, a, b, c)) or n != a + b + c:
                        fail("state %s: n must equal equal + differs_resolvable + differs_unresolvable" % k)
                    tot += n
                if tot != den:
                    fail("the states sum to %d, not the denominator %d" % (tot, den))
                if not isinstance(r.get("directory_present"), bool) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("as_of", ""))):
                    fail("directory_present (bool) and as_of (YYYY-MM-DD) are required")
                print("OK: %d accounts, the three states sum to the denominator and each closes" % den)
            else:
                raw = json.dumps(r)
                if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw):
                    fail("the record carries a long digit run (an account id?)")
                for k in ("account", "account_id", "account_ids", "ids", "client", "name", "nodes", "examples"):
                    if k in r:
                        fail("record key %r is not allowed" % k)
                print("OK: no id, no long digit run, no identifying key")
        elif arm == "AC3":
            f = ROOT / COUNT_SCRIPT
            if not f.is_file():
                fail("no %s" % COUNT_SCRIPT)
            src = f.read_text(encoding="utf-8")
            hit = [w for w in ("put_object", "upload_file", "upload_fileobj", "delete_object", "delete_objects", "copy_object", "put_item", "update_item", "PutObject", "DeleteObject", "write_text(", "to_parquet") if w in src]
            if hit:
                fail("the script contains a write verb: %s" % hit[:3])
            print("OK: the script holds no write verb")
        else:
            fail("unknown criterion")
    elif cell == "IB170-4":
        if arm == "AC1":
            roots = [ROOT / PORTAL_IR / "fixtures", ROOT / PORTAL_IR / "__tests__" / "fe-s-32" / "holdings-no-answer.json",
                     ROOT / PORTAL_IR / "__tests__" / "fe-s-74" / "fixtures" / "one-bad-key.json"]
            seen, hits = 0, []
            for rt in roots:
                files = [rt] if rt.is_file() else [p for p in rt.rglob("*") if p.is_file()]
                if not files:
                    fail("nothing found under %s (a zero is not an absence: the worktree lacks it)" % rt)
                for p in files:
                    if p.suffix.lower() not in (".json", ".ts", ".tsx"):
                        continue
                    seen += 1
                    t = p.read_text(encoding="utf-8", errors="replace")
                    # the OLD AnalysisReport section is a section_type of annualized_return or a section units of DECIMAL_FRACTION. The extractor-form
                    # section_id "2.annualized_return.c1" contains the field slug, and PerformanceReport return_units DECIMAL_FRACTION is a legitimate
                    # producer value, so neither bare word is the test: only a section_type value and a `units` key (not return_units).
                    if re.search(r"section_type[\"']?\s*[:=]\s*[\"']annualized_return[\"']", t) or re.search(r"(?<![A-Za-z_])units[\"']?\s*[:=]\s*[\"']DECIMAL_FRACTION[\"']", t):
                        hits.append(p.name)
            if seen < 20:
                fail("only %d files scanned; the portal worktree looks empty" % seen)
            if hits:
                fail("%d file(s) still carry the old section (section_type annualized_return or units DECIMAL_FRACTION): %s" % (len(hits), hits[:4]))
            print("OK: 0 of %d files carry the old tokens" % seen)
        elif arm == "AC2":
            T = "src/pages/InvestorReporting/__tests__/dsgn-irptv1/"
            files = [T + "iv-e-101.opal-report-words.test.tsx", T + "iv-e-105.opal-document-words.test.tsx", T + "iv-e-106.sections-retained-ref.test.ts",
                     T + "iv-e-115.vendor-section-names-units.test.tsx", T + "iv-e-122.vendor-validation-and-source.test.tsx"]
            rc, out = run(["bun", "test"] + files, timeout=110, cwd=ROOT / "portal")
            out = re.sub(r"\x1b\[[0-9;]*m", "", out)
            m = re.search(r"(\d+) pass", out)
            f = re.search(r"(\d+) fail", out)
            if rc != 0 or not m or int(m.group(1)) < 21 or (f and int(f.group(1)) != 0):
                fail("the five portal tests: rc %s, %s pass, %s fail (21 pass and 0 fail at base)" % (rc, m.group(1) if m else "?", f.group(1) if f else "?"))
            print("OK: the five portal tests pass (%s)" % m.group(1))
        elif arm == "AC3":
            prod = load(CONTR + "fixtures/AnalysisReport.valid.json")
            wire = load(PORTAL_IR + "fixtures/wire/AnalysisReport.valid.json")
            ps = (prod.get("instance", prod).get("sections") or [])
            ws = (wire.get("instance", wire).get("sections") or [])
            if not ps or ps != ws:
                fail("the portal wire copy's sections differ from the producer fixture's (%d vs %d sections)" % (len(ps), len(ws)))
            print("OK: the wire copy's sections equal the producer fixture's")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
