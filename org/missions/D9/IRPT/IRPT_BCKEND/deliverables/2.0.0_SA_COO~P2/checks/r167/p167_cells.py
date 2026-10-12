"""IRPT_BCKEND round 167 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of six orders (CTO PRD ADDENDUM v0.51, section 2, and ROUND-166 ANALYSIS section 3a):
  IB167-1  IB-pr-481  the frozen v1 PerformanceReport schema copies restored to their bytes at c16bf9d7bb^ (worker ~336)
  IB167-2  IB-pr-482  the C-CHAINCLAIM + PARTIAL release: the function rebuilt from one pin, and the never-widen packet with the MOVES and the reach (worker ~337)
  IB167-3  IB-pr-483  C-VALUEFACTS, reader first: the portal adapter reads start_value/end_value, the market-value names kept for the Black Diamond path (worker ~338, a portal cell)
  IB167-4  IB-pr-484  C-VALUEFACTS, the rename: bd_adapter writes start_value/end_value (worker ~339)
  IB167-5  IB-pr-485  ycharts/research rides the resident package; a test resolves every import on both binding branches (worker ~340)
  IB167-6  IB-pr-486  READ ONLY on the live host: does the installed resident_bindings.json carry commentary_ready_queue_url (0.7.0_AE_CloudOps~IB2)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Base: every criterion FAILs except the regression guards IB167-1-AC2, IB167-4-AC2 and IB167-5-AC2.
Every verdict and count in a record is the worker's; these checks grade the form, the sums, that each cite exists, and that a named test runs green.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~%d/"
D2 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/"
INV = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"
CHK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/"
TOS = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/"
ZERO_KEYS = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
IR = "infra/aws/lambda/investor-reporting"
PERF = IR + "/performance"
DOCS_SCHEMA = "docs/contracts/investor-reporting/v1/PerformanceReport.schema.json"
CON_SCHEMA = IR + "/_contracts/PerformanceReport.schema.json"
SHA_DOCS = "c4e2fdb122f0da2821fff846591d047463d9669117179ed7411a6e4ab3041f0f"
SHA_CON = "195c345fc2d13077f0a117bf257fc55fed31359d5998e05d78467896eef1cb81"
EXPECT_REACH = {"49F": {"SI": 23, "YTD": 19, "QTD": 2, "1Y": 20}, "orion": {"SI": 894, "YTD": 200, "QTD": 7, "1Y": 240}}
EXPECT_MOVES = {"49F": {"SI": 23, "YTD": 19, "QTD": 2, "1Y": 20}, "orion": {"SI": 750, "YTD": 76, "QTD": 7, "1Y": 106}}
FORBIDDEN = (r"systemctl\s+(start|stop|restart|reload|enable|disable|kill)", r"(?<![\w./-])(bash|sh|node|nodejs)\s+\S*(run-ycharts-session|ycharts_session)",
             r"get-secret-value", r"put-secret-value", r"update-secret", r"sqs\s+(send|receive|delete|purge)", r"\bcurl\b", r"\bwget\b",
             r"\bkill\b", r"\brm\s", r"\bmv\s", r"(?:^|[\s;|&()0-9])>>?\s*/(?!dev/null)", r"\btee\b", r"dynamodb\s+(put|update|delete)", r"\bcp\s", r"\bsed\s+-i")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB167"))
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


def changed_outside(base, serial_dir, extra=(), repo=None):
    """files changed against base (committed, staged or untracked) outside the worker's deliverables dir, its rows, its order, the issuer's
    check folder, any gitlink, and the product prefixes `extra` the order grants"""
    rc, out = run(["git", "diff", "--name-only", base])
    if rc != 0:
        fail("git diff against %r: %s" % (base, out[:120]))
    rc2, out2 = run(["git", "ls-files", "--others", "--exclude-standard"])
    names = [n.strip() for n in (out + "\n" + out2).splitlines() if n.strip()]
    ok = (serial_dir, INV, TOS, CHK) + tuple(extra)
    lk = links()
    return [n for n in names if not n.startswith(ok) and n not in lk]


def one_line(s, lo=40):
    if not isinstance(s, str) or len(s.strip()) < lo:
        fail("a statement of at least %d characters is missing" % lo)


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
    if cell == "IB167-1":
        n = 336
        if arm == "AC1":
            for rel, want in ((DOCS_SCHEMA, SHA_DOCS), (CON_SCHEMA, SHA_CON)):
                rc, out = run(["git", "show", "HEAD:" + rel])
                if rc != 0:
                    fail("git show HEAD:%s: %s" % (rel, out[:100]))
                f = ROOT / rel
                blob = subprocess.run(["git", "show", "HEAD:" + rel], cwd=str(ROOT), capture_output=True).stdout
                got = hashlib.sha256(blob).hexdigest()
                if got != want:
                    fail("%s at HEAD hashes %s, not the frozen %s" % (rel, got, want))
                if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() != want:
                    fail("%s in the working tree differs from HEAD (uncommitted or line endings)" % rel)
            print("OK: both schema copies hash to the frozen bytes at HEAD and in the working tree")
        elif arm == "AC2":
            rc, p, f, out = pytest(IR + "/_contracts")
            known = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve", "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]")
            failed = re.findall(r"^FAILED \S+::(\S+)", out, re.M)
            if p < 203 or f > 2 or any(not any(k in x for k in known) for x in failed):
                fail("_contracts suite: %d passed, %d failed %s (c16bf9d7bb^: 203 passed, 2 failed, the two known)" % (p, f, failed))
            print("OK: _contracts suite %d passed, %d failed (the two known)" % (p, f))
        elif arm == "AC3":
            rec = load(D % n + "IB167-1_revert_record.json")
            base_ok(rec)
            if rec.get("docs_copy_sha256") != SHA_DOCS or rec.get("contracts_copy_sha256") != SHA_CON:
                fail("the record's two hashes must equal the CTO's")
            if rec.get("docs_copy_equals_source_map_pin") is not True or not cite_ok(rec.get("source_map_pin_cite")):
                fail("docs_copy_equals_source_map_pin must be true with a resolving source_map_pin_cite")
            bad = changed_outside(rec["base_commit"], D % n, (CON_SCHEMA, DOCS_SCHEMA))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: record complete; only the two schema copies changed")
        else:
            fail("unknown arm")
    elif cell == "IB167-2":
        n = 337
        if arm == "AC1":
            rec = load(D % n + "IB167-2_release_census.json")
            base_ok(rec)
            fn = rec.get("functions") or []
            if len(fn) < 1:
                fail("functions: none")
            for f in fn:
                if f.get("function") != "irpt-performance-adapter":
                    fail("the function built must be irpt-performance-adapter, reads %r" % f.get("function"))
                if not re.fullmatch(r"[0-9a-f]{64}", str(f.get("built_sha256", ""))) or not re.fullmatch(r"[0-9a-f]{64}", str(f.get("live_sha256", ""))):
                    fail("built_sha256 and live_sha256 must be 64-hex")
                if f.get("built_twice_identical") is not True:
                    fail("built_twice_identical must be true")
                if f.get("built_signature_mismatched") != 0 or f.get("built_attribute_mismatched") != 0:
                    fail("the built zip must read 0 signature and 0 attribute mismatches")
                cm = f.get("changed_members") or []
                if not cm:
                    fail("changed_members is empty")
                for m in cm:
                    if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
                        fail("changed member %r: the built member's sha256 must equal the repo blob's at the pin (the zip carries the merged bytes)" % m.get("name"))
                if not any(str(m.get("name", "")).endswith("holdings_gold.py") for m in cm):
                    fail("holdings_gold.py must be among the changed members")
            if rec.get("uploaded") is not False:
                fail("uploaded must be false (nothing is uploaded here)")
            print("OK: %d function built twice identical, 0 mismatches" % len(fn))
        elif arm == "AC2":
            pk = D % n + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md"
            if not (ROOT / pk).is_file():
                fail("no %s" % pk)
            t = (ROOT / pk).read_text(encoding="utf-8")
            for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the ADDENDUM 18 red list", r"red list"), ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                              ("the moves with the reach beside them", r"(?i)moves?.{0,80}reach|reach.{0,80}moves?"), ("the pair's halves", r"(?i)COO half"), ("rollback per key", r"(?i)rollback|restore the live")):
                if not re.search(pat, t):
                    fail("the packet lacks: %s" % need)
            if len(t) < 2500:
                fail("the packet is shorter than 2500 characters")
            print("OK: the packet carries Branch A and B, the red list, the shas, the moves beside the reach, the halves and the rollback")
        elif arm == "AC3":
            rec = load(D % n + "IB167-2_release_counts.json")
            base_ok(rec)
            if rec.get("rule_reach") != EXPECT_REACH:
                fail("rule_reach %r != the CTO's v0.49 reach %r" % (rec.get("rule_reach"), EXPECT_REACH))
            if rec.get("claim_moves") != EXPECT_MOVES:
                fail("claim_moves %r != the moves %r (CTO ADDENDUM v0.51 item 2)" % (rec.get("claim_moves"), EXPECT_MOVES))
            if rec.get("latest_landed_day") != "2026-10-08":
                fail("latest_landed_day must be 2026-10-08")
            if rec.get("counts_taken_at_pin") != rec.get("pin_commit") or not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
                fail("the counts must be taken at the build's pin (counts_taken_at_pin == pin_commit)")
            cons = rec.get("consumers_read_through") or []
            need_cites([c.get("cite") for c in cons], "consumers_read_through")
            zeros(rec)
            print("OK: reach and moves equal the CTO's; %d consumer(s) read through" % len(cons))
        else:
            fail("unknown arm")
    elif cell == "IB167-3":
        n = 338
        pw = ROOT / "portal"
        if not (pw / "package.json").is_file():
            fail("no portal worktree at <root>/portal (provisioned with --portal-ref)")

        def bun(tf):
            if not (pw / tf).is_file():
                fail("no portal file %s" % tf)
            rc, out = run(["bun", "test", tf], cwd=pw, timeout=240)
            p = re.search(r"(\d+)\s+pass", re.sub(r"\x1b\[[0-9;]*m", "", out))
            f = re.search(r"(\d+)\s+fail", re.sub(r"\x1b\[[0-9;]*m", "", out))
            return rc, int(p.group(1)) if p else 0, int(f.group(1)) if f else 0
        if arm == "AC1":
            tf = "src/pages/InvestorReporting/__tests__/value-facts-members.test.ts"
            rc, p, f = bun(tf)
            if rc != 0 or p < 3 or f:
                fail("%s: rc %s, %d pass, %d fail (need >= 3 pass, 0 fail)" % (tf, rc, p, f))
            print("OK: the value-facts member test: %d pass" % p)
        elif arm == "AC2":
            tf = "src/pages/InvestorReporting/__tests__/fe-s-5/performance-wire-journey.test.ts"
            rc, p, f = bun(tf)
            if rc != 0 or p < 1 or f:
                fail("%s: rc %s, %d pass, %d fail (5 pass at the portal checkout dbeb6764ea; need >= 1 pass, 0 fail at the DEV head the worktree is cut from)" % (tf, rc, p, f))
            print("OK: the wire journey test: %d pass" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB167-3_portal_candidate_record.json")
            base_ok(rec)
            if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get("portal_base_commit", ""))) or not re.fullmatch(r"[0-9a-f]{40}", str(rec.get("portal_candidate_commit", ""))):
                fail("portal_base_commit and portal_candidate_commit must be 40-hex")
            if rec.get("portal_base_commit") != "53506d4903aeabac675d87b7fe208fc9945c8ce7":
                fail("portal_base_commit must be the portal DEV head named by the issuance, 53506d4903...")
            fc = rec.get("portal_files_changed") or []
            if not fc or any(not x.startswith("src/pages/InvestorReporting/") for x in fc):
                fail("portal_files_changed must be non-empty and inside src/pages/InvestorReporting/")
            rc, out = run(["git", "-C", str(pw), "diff", "--name-only", rec["portal_base_commit"], rec["portal_candidate_commit"]])
            if rc != 0 or sorted(x.strip() for x in out.splitlines() if x.strip()) != sorted(fc):
                fail("portal_files_changed does not match git diff base..candidate in the portal repo")
            if rec.get("market_value_names_kept_for") != "black-diamond-path-only":
                fail("market_value_names_kept_for must read black-diamond-path-only (the fallback lives one release window)")
            one_line(rec.get("fallback_removal_condition_in_words"))
            if rec.get("pushed") is not False:
                fail("pushed must be false")
            bad = changed_outside(rec["base_commit"], D % n, ("portal",))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: portal candidate %s on DEV head; %d portal file(s)" % (rec["portal_candidate_commit"][:10], len(fc)))
        else:
            fail("unknown arm")
    elif cell == "IB167-4":
        n = 339
        if arm == "AC1":
            test_file(PERF + "/tests/test_bd_value_members.py", 3, "bd_adapter writes the contract members")
        elif arm == "AC2":
            rc, p, f, out = pytest(PERF + "/tests")
            if f > 1 or p < 274 or (f == 1 and "test_the_fallback_calendar_is_graded_in_its_own_years" not in out):
                fail("performance suite: %d passed, %d failed (base 274 passed, 1 failed, the known calendar test)" % (p, f))
            print("OK: performance suite %d passed, %d failed (the known calendar test)" % (p, f))
        elif arm == "AC3":
            rec = load(D % n + "IB167-4_bd_rename_record.json")
            base_ok(rec)
            ren = rec.get("renamed") or []
            if sorted((r.get("from"), r.get("to")) for r in ren) != sorted([("beginning_market_value", "start_value"), ("ending_market_value", "end_value")]):
                fail("renamed must be exactly beginning_market_value->start_value and ending_market_value->end_value")
            src = ROOT / PERF / "bd_adapter.py"
            if not src.is_file():
                fail("no bd_adapter.py")
            t = src.read_text(encoding="utf-8")
            if re.search(r"""['"](beginning_market_value|ending_market_value)['"]\s*:""", t):
                fail("bd_adapter.py still keys a market-value name")
            rd = rec.get("in_repo_readers_of_the_old_names") or []
            if not isinstance(rd, list):
                fail("in_repo_readers_of_the_old_names is not a list")
            need_cites([r.get("cite") for r in rd], "in_repo_readers_of_the_old_names") if rd else None
            bad = changed_outside(rec["base_commit"], D % n, (PERF + "/bd_adapter.py", PERF + "/tests/"))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: the two names renamed in bd_adapter.py; %d in-repo reader(s) of the old names listed" % len(rd))
        else:
            fail("unknown arm")
    elif cell == "IB167-5":
        n = 340
        if arm == "AC1":
            test_file(IR + "/reports/tests/test_resident_package_imports.py", 3, "the resident package resolves its imports on both binding branches")
        elif arm == "AC2":
            rc, p, f, out = pytest(IR + "/reports")
            if rc != 0 or f or p < 202:
                fail("reports suite: rc %s, %s passed, %s failed (base 202 passed; need >= 202, 0 failed)" % (rc, p, f))
            print("OK: reports suite %d passed" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB167-5_resident_dirs_record.json")
            base_ok(rec)
            if "ycharts/research" not in (rec.get("dirs_after") or []) or "ycharts/research" in (rec.get("dirs_before") or []):
                fail("dirs_before must lack and dirs_after must carry ycharts/research")
            if rec.get("imports_resolved_both_branches") is not True:
                fail("imports_resolved_both_branches must be true")
            t = (ROOT / IR / "reports" / "build_resident_package.py")
            if not t.is_file() or not re.search(r"""['"]ycharts/research['"]|['"]ycharts['"]\s*,\s*['"]research['"]""", t.read_text(encoding="utf-8")):
                fail("build_resident_package.py does not name ycharts/research")
            if rec.get("request_sent") is not False or rec.get("deployed") is not False:
                fail("request_sent and deployed must be false")
            bad = changed_outside(rec["base_commit"], D % n, (IR + "/reports/",))
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: DIRS before/after recorded; the builder names ycharts/research")
        else:
            fail("unknown arm")
    elif cell == "IB167-6":
        rec = load(D2 + "IB167-6_host_bindings_read.json")
        if arm == "AC1":
            b = rec.get("commentary_ready_queue_url_bound")
            if b not in (True, False, "NOT_ESTABLISHED"):
                fail("commentary_ready_queue_url_bound must be true, false or NOT_ESTABLISHED")
            if rec.get("claim") not in ("measured", "inferred", "held", "absent"):
                fail("claim must be measured, inferred, held or absent")
            if b in (True, False) and rec.get("claim") != "measured":
                fail("a read of the file is measured")
            for k in ("instance", "bindings_path", "read_at_utc"):
                if not rec.get(k):
                    fail("%s is missing" % k)
            # AMENDMENT (issuer defect, IB2 msg 6519, row S110): the first form rejected any record containing the substring "queue_url", which the
            # required key `commentary_ready_queue_url_bound` itself contains. The queue URL VALUE is what must not be recorded: a url, an SQS host, or a
            # 12-digit account segment.
            if re.search(r"https?://|sqs\.[a-z0-9-]+\.amazonaws\.com|/\d{12}/", json.dumps(rec)):
                fail("the queue URL itself must not be recorded (a boolean and at most the queue NAME)")
            one_line(rec.get("in_words"))
            print("OK: bound=%s (%s)" % (b, rec["claim"]))
        elif arm == "AC2":
            cmds = rec.get("host_commands") or []
            if not cmds:
                fail("host_commands is empty (a host read lists its commands verbatim)")
            for c in cmds:
                if not (c.get("ssm_command_id") and c.get("status") and c.get("script")):
                    fail("a host command lacks ssm_command_id, status or script")
                for pat in FORBIDDEN:
                    if re.search(pat, c["script"]):
                        fail("a host command matches the forbidden pattern %r: %s" % (pat, c["script"][:100]))
            print("OK: %d host command(s), none matching a forbidden pattern" % len(cmds))
        elif arm == "AC3":
            if rec.get("sign_in_attempted") is not False or rec.get("secret_values_read") != 0 or rec.get("host_writes") != 0:
                fail("sign_in_attempted false, secret_values_read 0 and host_writes 0 are required")
            if not isinstance(rec.get("not_established"), list):
                fail("not_established is not a list")
            if rec.get("output_files") is not None and not isinstance(rec.get("output_files"), list):
                fail("output_files is not a list")
            print("OK: bounds hold: no sign-in, 0 secret values, 0 host writes")
        else:
            fail("unknown arm")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
