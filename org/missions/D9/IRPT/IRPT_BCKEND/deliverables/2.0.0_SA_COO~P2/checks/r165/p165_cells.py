"""IRPT_BCKEND round 165 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of five orders (CTO PRD ADDENDUM v0.49, section 3, items 3 to 7):
  IB165-1  IB-pr-471  the names of the opening/closing value members: a census of the emitters and the wire contract, then a one-side
                      producer rename ONLY if the contract names them (worker ~326)
  IB165-2  IB-pr-472  the extractor locates a label inside its own section's bounds (worker ~327)
  IB165-3  IB-pr-473  the YCharts capture probe classifies a challenge, the pair runs only with a token, the receipt is kept per step (worker ~328)
  IB165-4  IB-pr-474  build-and-upload.sh exits non-zero when a restore from HEAD fails and names the files (worker ~329)
  IB165-5  IB-pr-475  two reads: commentary_ref at HEAD, and the prices store's writer and schedule (worker ~330)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Base: every criterion FAILs (no file).
  IBn-AC1  the cell's own test or its record's form;   IBn-AC2  the consistency or the regression arm;   IBn-AC3  the bound or the record.
Every verdict and count in a record is the worker's; these checks grade the form, the sums, that each cite exists, and that a named
test runs green.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~%d/"
INV = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"
ZERO_KEYS = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
PERF = "infra/aws/lambda/investor-reporting/performance/tests"
EXTRACT = "infra/aws/lambda/investor-reporting/ycharts/extract"
SESSION = "infra/aws/lambda/investor-reporting/ycharts/session/tests"
HOST = "infra/aws/ec2/investor-reporting-ycharts"
CI = "infra/aws/lambda/ci"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB165"))
    sys.exit(1)


def run(cmd, cwd=None, timeout=240):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout after %ss: %s" % (timeout, " ".join(cmd)[:120]))
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def pytest(target, timeout=240):
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
    """a repo-relative 'path:line' (line may be 'a-b'); the file exists and the first line is inside it"""
    m = re.match(r"^([^:]+):(\d+)(?:-(\d+))?$", str(c).strip())
    if not m:
        return False
    f = ROOT / m.group(1)
    if not f.is_file():
        return False
    n = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
    return 1 <= int(m.group(2)) <= n and (m.group(3) is None or int(m.group(3)) <= n)


def need_cites(rec, label):
    bad = [c for c in rec if not cite_ok(c)]
    if not rec or bad:
        fail("%s: %d cite(s), unresolved: %s" % (label, len(rec), bad[:3]))


def zeros(d):
    for k in ZERO_KEYS:
        if d.get(k) != 0:
            fail("%s must read 0, reads %r" % (k, d.get(k)))


def changed_outside(base, serial_n):
    """files changed against base (committed, staged or untracked) that are outside the worker's deliverables, the investigation file and its order"""
    rc, out = run(["git", "diff", "--name-only", base])
    if rc != 0:
        fail("git diff against %r: %s" % (base, out[:120]))
    rc2, out2 = run(["git", "ls-files", "--others", "--exclude-standard"])
    names = [n.strip() for n in (out + "\n" + out2).splitlines() if n.strip()]
    ok = (D % serial_n, INV, "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/")
    return [n for n in names if not n.startswith(ok)]


def one_line(s, lo=40):
    if not isinstance(s, str) or len(s.strip()) < lo:
        fail("a statement of at least %d characters is missing" % lo)


def arms(out, minimum):
    ls = [ln for ln in out.splitlines() if ln.startswith("ARM ")]
    if len(ls) < minimum or any(not ln.rstrip().endswith("PASS") for ln in ls):
        fail("%d ARM line(s), %d not PASS (need >= %d all PASS)" % (len(ls), sum(1 for ln in ls if not ln.rstrip().endswith("PASS")), minimum))
    return len(ls)


def leaves_ok(x, path=""):
    """a persisted receipt leaf: bool, int, null, or a short name with no url, mail or percent-escape"""
    if isinstance(x, dict):
        for k, v in x.items():
            leaves_ok(v, path + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            leaves_ok(v, path + "/%d" % i)
    elif isinstance(x, str):
        if len(x) > 120 or re.search(r"http|@|%", x):
            fail("receipt leaf %s is a long or url-shaped string" % path)
    elif not (x is None or isinstance(x, (bool, int))):
        fail("receipt leaf %s is a %s" % (path, type(x).__name__))


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell = CID[:7]
    arm = CID[8:]
    if cell == "IB165-1":
        n = 326
        rec = load(D % n + "IB165-1_value_member_names.json")
        if arm == "AC1":
            if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
                fail("base_commit")
            w = rec.get("wire_contract") or {}
            if not isinstance(w.get("names_declared"), list):
                fail("wire_contract.names_declared is not a list (an empty list says the contract names none)")
            need_cites(w.get("cites"), "wire_contract.cites")
            one_line(w.get("in_words"))
            em = rec.get("emitters") or []
            if len(em) < 2:
                fail("emitters: fewer than 2")
            for e in em:
                need_cites([e.get("cite")], "emitter cite")
                if not e.get("names"):
                    fail("an emitter without names")
            cs = rec.get("emitter_census") or {}
            if not (cs.get("pattern") and isinstance(cs.get("files_searched"), int) and cs["files_searched"] > 0
                    and isinstance(cs.get("files_with_a_hit"), int)):
                fail("emitter_census needs pattern, files_searched > 0, files_with_a_hit")
            if rec.get("decision") not in ("PRODUCER_RENAMED", "ADAPTER_SIDE_DISAGREES", "CONTRACT_NAMES_NONE", "NOT_ESTABLISHED"):
                fail("decision %r" % rec.get("decision"))
            zeros(rec)
            if not isinstance(rec.get("not_established"), list):
                fail("not_established is not a list")
            print("OK: %d emitter(s), decision %s, census %d files" % (len(em), rec["decision"], cs["files_searched"]))
        elif arm == "AC2":
            dec = rec.get("decision")
            if dec == "PRODUCER_RENAMED":
                fc = rec.get("files_changed") or []
                ren = rec.get("renamed") or []
                tp = rec.get("test_path")
                if not fc or not ren or not tp or not (ROOT / tp).is_file():
                    fail("PRODUCER_RENAMED needs files_changed, renamed and an existing test_path")
                rc, p, f, out = pytest(tp)
                if rc != 0 or p < 2 or f:
                    fail("the rename test: rc %s, %s passed, %s failed" % (rc, p, f))
                for r in ren:
                    for fn in fc:
                        if fn.endswith(".py") and (ROOT / fn).is_file() and re.search(r"""['"]%s['"]\s*:""" % re.escape(r["from"]),
                                                                                       (ROOT / fn).read_text(encoding="utf-8")):
                            fail("%s still keys %r" % (fn, r["from"]))
                print("OK: renamed %d member name(s); the rename test passes (%d)" % (len(ren), p))
            else:
                bad = changed_outside(rec.get("base_commit", ""), n)
                if bad:
                    fail("decision %s edits no product file, but changed: %s" % (dec, bad[:3]))
                print("OK: decision %s and no product file edited" % dec)
        elif arm == "AC3":
            rc, p, f, out = pytest(PERF)
            if p < 251 or f > 1:
                fail("performance suite: %d passed, %d failed (base: 251 passed, 1 failed)" % (p, f))
            if f == 1 and "test_the_fallback_calendar_is_graded_in_its_own_years" not in out:
                fail("the one failure is not the known calendar test")
            print("OK: performance suite %d passed, %d failed (the known calendar test)" % (p, f))
        else:
            fail("unknown arm")
    elif cell == "IB165-2":
        n = 327
        if arm == "AC1":
            tf = "%s/tests/test_label_locator_sections.py" % EXTRACT
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, p, f, out = pytest(tf)
            if rc != 0 or p < 3 or f:
                fail("%s: rc %s, %s passed, %s failed (need >= 3 passed)" % (tf, rc, p, f))
            print("OK: %d locator test(s) pass" % p)
        elif arm == "AC2":
            rc, p, f, out = pytest(EXTRACT)
            if rc != 0 or f or p < 42:
                fail("extract suite: rc %s, %s passed, %s failed (base 39 passed; need >= 42, 0 failed)" % (rc, p, f))
            print("OK: extract suite %d passed" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB165-2_label_locator_record.json")
            if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
                fail("base_commit")
            one_line(rec.get("section_bounds_rule"))
            ba = rec.get("before_after") or {}
            b, a = ba.get("before_sha256") or [], ba.get("after_sha256") or []
            if not b or b != a or ba.get("fixtures_compared") != len(b):
                fail("before_after: output hashes of the existing fixtures must be equal lists of length fixtures_compared (>= 1)")
            bf = rec.get("both_labels_fixture")
            if not bf or not (ROOT / bf).exists():
                fail("both_labels_fixture does not exist")
            if rec.get("request_sent") is not False or rec.get("deployed") is not False:
                fail("request_sent and deployed must be false")
            bad = changed_outside(rec["base_commit"], n)
            bad = [x for x in bad if not x.startswith(EXTRACT + "/")]
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: existing output unchanged for %d fixture(s)" % len(b))
        else:
            fail("unknown arm")
    elif cell == "IB165-3":
        n = 328
        if arm == "AC1":
            tf = HOST + "/tests/probe_challenge_and_pair.js"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, out = run(["node", "--require", "./tests/netguard.js", "tests/probe_challenge_and_pair.js"], cwd=ROOT / HOST)
            if rc != 0:
                fail("probe_challenge_and_pair.js rc %s" % rc)
            k = arms(out, 5)
            rc, out = run(["node", "--require", "./tests/netguard.js", "tests/run_offline_suite.js"], cwd=ROOT / HOST, timeout=400)
            if rc != 0:
                fail("run_offline_suite.js rc %s (rc 0 at base)" % rc)
            print("OK: %d arms PASS; the offline suite exits 0" % k)
        elif arm == "AC2":
            tf = SESSION + "/test_capture_receipt_per_step.py"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, p, f, out = pytest(SESSION)
            if rc != 0 or f or p < 130:
                fail("session tests: rc %s, %s passed, %s failed (base 127 passed, 2 skipped; need >= 130, 0 failed)" % (rc, p, f))
            print("OK: session tests %d passed" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB165-3_capture_probe_record.json")
            sp = D % n + "IB165-3_persisted_receipt_sample.json"
            samp = load(sp)
            raw = (ROOT / sp).read_text(encoding="utf-8")
            sec = rec.get("planted_secrets") or []
            if len(sec) < 4 or any(len(s) < 8 for s in sec) or any(s in raw for s in sec):
                fail("planted_secrets: >= 4 strings of >= 8 characters, none present in the sample")
            steps = samp.get("steps")
            if not isinstance(steps, list) or len(steps) < 2:
                fail("the sample needs a steps list of at least 2")
            for st in steps:
                for k in ("waf_action_class", "content_type_class", "body_marker", "probe_path_name", "identity_leg"):
                    if k not in st:
                        fail("a step lacks %s" % k)
            leaves_ok(samp)
            if rec.get("request_sent") is not False or rec.get("deployed") is not False:
                fail("request_sent and deployed must be false")
            if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
                fail("base_commit")
            one_line(rec.get("pair_rule_in_words"))
            print("OK: %d step(s) persisted, closed leaves, %d planted strings absent" % (len(steps), len(sec)))
        else:
            fail("unknown arm")
    elif cell == "IB165-4":
        n = 329
        if arm == "AC1":
            tf = CI + "/tests/test_build_restore_fails_loud.sh"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, out = run(["bash", tf], timeout=300)
            if rc != 0:
                fail("%s rc %s" % (tf, rc))
            k = arms(out, 3)
            print("OK: %d arms PASS" % k)
        elif arm == "AC2":
            rc, p, f, out = pytest(CI + "/test_build_staging_keeps_tracked.py")
            if rc != 0 or p < 5 or f:
                fail("test_build_staging_keeps_tracked.py: rc %s, %s passed, %s failed (base 5 passed)" % (rc, p, f))
            rc, out = run(["bash", CI + "/tests/test_build_only.sh"], timeout=300)
            if rc != 0:
                fail("tests/test_build_only.sh rc %s (rc 0 at base)" % rc)
            print("OK: staging test %d passed; test_build_only.sh exits 0" % p)
        elif arm == "AC3":
            rec = load(D % n + "IB165-4_restore_fails_loud_record.json")
            if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
                fail("base_commit")
            one_line(rec.get("exit_code_rule"))
            one_line(rec.get("failure_message_sample"), 20)
            if rec.get("deployed") is not False or rec.get("aws_calls_made") != 0:
                fail("deployed false and aws_calls_made 0")
            bad = [x for x in changed_outside(rec["base_commit"], n) if not x.startswith(CI + "/")]
            if bad:
                fail("changed outside the grant: %s" % bad[:3])
            print("OK: record complete; the change stays inside %s" % CI)
        else:
            fail("unknown arm")
    elif cell == "IB165-5":
        n = 330
        rec = load(D % n + "IB165-5_two_reads.json")
        if arm == "AC1":
            if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("base_commit", ""))):
                fail("base_commit")
            c = rec.get("commentary_ref") or {}
            if c.get("verdict") not in ("HEAD_READS_SIBLING", "HEAD_READS_RECORD", "NOT_ESTABLISHED"):
                fail("commentary_ref.verdict %r" % c.get("verdict"))
            need_cites(c.get("cites"), "commentary_ref.cites")
            one_line(c.get("in_words"))
            p = rec.get("prices_store") or {}
            if p.get("verdict") not in ("WRITER_SCHEDULED", "WRITER_UNSCHEDULED", "NO_WRITER"):
                fail("prices_store.verdict %r" % p.get("verdict"))
            need_cites(p.get("cites"), "prices_store.cites")
            one_line(p.get("in_words"))
            print("OK: commentary_ref %s; prices store %s" % (c["verdict"], p["verdict"]))
        elif arm == "AC2":
            p = rec.get("prices_store") or {}
            if not isinstance(p.get("retired_as_source"), bool):
                fail("prices_store.retired_as_source is not a boolean")
            if p.get("retired_as_source") != (p.get("verdict") == "NO_WRITER"):
                fail("retired_as_source must be true exactly when the verdict is NO_WRITER")
            if p.get("verdict") in ("WRITER_SCHEDULED", "WRITER_UNSCHEDULED"):
                if not p.get("writer") or not cite_ok(p.get("writer_cite")):
                    fail("a found writer needs a name and a resolving writer_cite")
            if p.get("verdict") == "WRITER_SCHEDULED":
                need_cites(p.get("schedule_cites"), "schedule_cites")
            cs = p.get("census") or {}
            if not (cs.get("scope") and isinstance(cs.get("files_searched"), int) and cs["files_searched"] > 0):
                fail("prices_store.census needs scope and files_searched > 0 (the denominator beside a no-writer verdict)")
            if not isinstance(rec.get("not_established"), list):
                fail("not_established is not a list")
            print("OK: prices store %s, retired_as_source %s, census %d files" % (p["verdict"], p["retired_as_source"], cs["files_searched"]))
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
