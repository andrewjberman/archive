"""IRPT_BCKEND round 171 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of five orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB171-1  IB-pr-496  the 49F builder no longer leaves the Tax membership snapshot in a temp file; raw_keys.json cites the live mint (rows W345-S3, W344-S2)
    AC1  the worker's new test file passes (3 or more, none failed)
    AC2  the issuer's seam probe: a build that raises, a build that returns, and an operator's own env-var file (kept)
    AC3  raw_keys.json: the 49financial account holdings_source cites the live mint (dim_balance, holdings_49f) and no longer names the smartx allocation map; the file is valid JSON
  IB171-2  IB-pr-497  ONE read-only count of leftover Tax-snapshot temp files on the host(s) that run the builder (counts and ages only)
    AC1  the record's shape and arithmetic; contents_read 0, files_deleted 0
    AC2  the record carries no path, no name, no id, no long digit run
    AC3  the recorded command is read-only (a find or ls; no rm, cat, tee, redirect, shred, mv, cp)
  IB171-3  IB-pr-498  irpt-holdings rebuilt from one pin (the staged HoldingsSnapshot schema copy re-pinned) and its never-widen packet
    AC1  the census: built twice identical, 0 signature and 0 attribute mismatches, the changed members equal the repo blobs at the pin, the schema copy among them, uploaded false
    AC2  the packet carries Branch A and B, the red list, the live and built sha256, the pair's halves and the rollback
    AC3  the replay arms: a node with account_id validates, a node without validates, an unknown node member is refused; served figures changed 0; the bound counters 0
  IB171-4  IB-pr-499  irpt-directory-search rebuilt from one pin (handler.py) and its never-widen packet
    AC1  the census, as above, handler.py among the changed members
    AC2  the packet, as above
    AC3  the replay arms (tail of a non-head account, shared tail, name query, no-masks entry) and the REACH counts per firm; the bound counters 0
  IB171-5  IB-pr-500  the portal's two stale generators reproduce their committed bytes, and selected_sections resolves
    AC1  running each generator leaves its outputs byte-equal to the committed files (end-of-line differences ignored)
    AC2  every selected_sections id in the portal ExportBundle wire fixture and the submit-export request fixture is a section_id of the portal AnalysisReport wire copy
    AC3  the five token-citing portal tests still pass and no AnalysisReport old section is back
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
GOLD = "data/assets/scripts/gold/investor_reporting/"
RAWKEYS = "infra/aws/lambda/investor-reporting/_ids/raw_keys.json"
PORTAL_IR = "portal/src/pages/InvestorReporting/"
HOSTREC = D + "0.7.0_AE_CloudOps~IB2/IB171-2_host_tmp_read.json"
ROOT = Path(".")
CID = ""
SUFFIX = "-taxsma_workbook_projected_snapshot.json"
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB171"))
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


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def zeros(rec):
    for k in BOUND_ZERO:
        if rec.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, rec.get(k)))


def probe_builder():
    sys.path.insert(0, str(ROOT / GOLD))
    sys.path.insert(0, str(ROOT / "lib"))
    import importlib
    h49 = importlib.import_module("holdings_49f")
    hs = importlib.import_module("holdings_snapshot")

    class Body:
        def __init__(self, b):
            self.b = b

        def read(self):
            return self.b

    class S3:
        def get_object(self, Bucket, Key, **k):  # noqa: N803
            return {"Body": Body(b'{"accounts": []}')}
    hs._latest_date_partition = lambda s3, b, p, **k: "2026-10-09"
    pat = os.path.join(tempfile.gettempdir(), "*" + SUFFIX)
    env = "IRPT_49F_TAX_MEMBERSHIP_SNAPSHOT"
    saved = os.environ.pop(env, None)
    made = []
    try:
        # arm 1: the build raises
        before = set(glob.glob(pat))
        h49.build_49f_actual = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            h49.build_49f_meshed(S3(), "2026-10-09")
            fail("the stubbed build was expected to raise")
        except RuntimeError:
            pass
        left = set(glob.glob(pat)) - before
        made += list(left)
        if left:
            fail("a build that raises leaves %d Tax-snapshot temp file(s) behind" % len(left))
        # arm 2: the build returns
        before = set(glob.glob(pat))
        h49.build_49f_actual = lambda *a, **k: ([], {"manifest": {}})
        h49.build_49f_meshed(S3(), "2026-10-09")
        left = set(glob.glob(pat)) - before
        made += list(left)
        if left:
            fail("a build that returns leaves %d Tax-snapshot temp file(s) behind" % len(left))
        # arm 3: an operator's own file (the env var) is read and is NOT deleted
        fd, mine = tempfile.mkstemp(suffix="-operator-owned.json")
        os.close(fd)
        made.append(mine)
        os.environ[env] = mine
        h49.build_49f_actual = lambda *a, **k: ([], {"manifest": {}})
        h49.build_49f_meshed(S3(), "2026-10-09")
        if not os.path.exists(mine):
            fail("the operator's own snapshot file (the env var) was deleted: only a file the builder created may be removed")
    finally:
        os.environ.pop(env, None)
        if saved is not None:
            os.environ[env] = saved
        for f in made:
            try:
                os.remove(f)
            except OSError:
                pass


def release_census(cell_tag, slot, function, must_member):
    rec = load(D + "0.9.0_WK_IRPT_BCKEND~%d/%s_release_census.json" % (slot, cell_tag))
    fn = rec.get("functions") or []
    if len(fn) != 1 or fn[0].get("function") != function:
        fail("functions must hold exactly %s" % function)
    f = fn[0]
    for k in ("built_sha256", "live_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", str(f.get(k, ""))):
            fail("%s must be 64-hex" % k)
    if f.get("built_twice_identical") is not True:
        fail("built_twice_identical must be true")
    if f.get("built_signature_mismatched") != 0 or f.get("built_attribute_mismatched") != 0:
        fail("the built zip must read 0 signature and 0 attribute mismatches")
    cm = f.get("changed_members") or []
    if not cm:
        fail("changed_members is empty")
    for m in cm:
        if not (re.fullmatch(r"[0-9a-f]{64}", str(m.get("built_member_sha256", ""))) and m.get("built_member_sha256") == m.get("repo_blob_sha256_at_pin")):
            fail("changed member %r: the built member's sha256 must equal the repo blob's at the pin" % m.get("name"))
    if not any(str(m.get("name", "")).endswith(must_member) for m in cm):
        fail("%s must be among the changed members" % must_member)
    if rec.get("uploaded") is not False:
        fail("uploaded must be false")
    if not re.fullmatch(r"[0-9a-f]{7,40}", str(rec.get("pin_commit", ""))):
        fail("pin_commit")
    return rec


def packet_ok(slot, name):
    pk = D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (slot, name)
    if not (ROOT / pk).is_file():
        fail("no %s" % pk)
    t = (ROOT / pk).read_text(encoding="utf-8")
    for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("live and built sha256", r"(?i)live.{0,40}sha256|sha256.{0,40}live"),
                      ("the pair's halves", r"(?i)COO half"), ("rollback", r"(?i)rollback|restore the live")):
        if not re.search(pat, t):
            fail("the packet lacks: %s" % need)
    if len(t) < 2000:
        fail("the packet is shorter than 2000 characters")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB171-1":
        if arm == "AC1":
            tf = GOLD + "tests/test_retained_capture_cleanup.py"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, p, f, e, out = pytest_counts(tf)
            if p < 3 or f or e:
                fail("%s: %d passed, %d failed, %d errors (3 passed and none failed are required)" % (tf, p, f, e))
            print("OK: %d tests pass" % p)
        elif arm == "AC2":
            probe_builder()
            print("OK: a raising build and a returning build leave no snapshot temp file; the operator's own file is kept")
        elif arm == "AC3":
            raw = load(RAWKEYS)
            acct = ((raw.get("firms") or {}).get("49financial") or {}).get("account") or {}
            src = str(acct.get("holdings_source", ""))
            if "dim_balance" not in src or "holdings_49f" not in src:
                fail("holdings_source must cite the live mint (dim_balance and holdings_49f), reads %r" % src[:120])
            if "fact_allocation_account_map" in src or re.search(r"(?i)smartx", src):
                fail("holdings_source still names the smartx allocation map")
            print("OK: holdings_source cites the live mint")
        else:
            fail("unknown criterion")
    elif cell == "IB171-2":
        r = load(HOSTREC)
        if arm == "AC1":
            if not is_int(r.get("hosts_read")) or r["hosts_read"] < 1 or r.get("contents_read") != 0 or r.get("files_deleted") != 0:
                fail("hosts_read (int >= 1), contents_read 0 and files_deleted 0 are required")
            ph = r.get("per_host") or []
            if len(ph) != r["hosts_read"]:
                fail("per_host must hold one row per host read")
            for h in ph:
                if not is_int(h.get("files_matching")) or h["files_matching"] < 0:
                    fail("files_matching must be an integer >= 0")
                for k in ("oldest_age_days", "newest_age_days"):
                    if h.get(k) is not None and not is_int(h.get(k)):
                        fail("%s must be an integer or null" % k)
                if h["files_matching"] == 0 and (h.get("oldest_age_days") is not None or h.get("newest_age_days") is not None):
                    fail("ages must be null when no file matched")
            print("OK: %d host(s) read, counts and ages only" % len(ph))
        elif arm == "AC2":
            raw = json.dumps(r)
            if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw) or re.search(r"/tmp|/var/|tmp[a-z0-9_]{6,}", raw):
                fail("the record carries a path, a temp file name or a long digit run")
            for k in ("paths", "files", "names", "instance_ids", "instance_id", "account", "ids"):
                if k in r or any(k in h for h in (r.get("per_host") or [])):
                    fail("record key %r is not allowed" % k)
            print("OK: no path, name, id or long digit run")
        elif arm == "AC3":
            cmd = str(r.get("command_run", ""))
            if not re.search(r"\b(find|ls)\b", cmd):
                fail("command_run must be a find or an ls")
            bad = [w for w in ("rm ", "rm\t", "cat ", "tee ", ">", "shred", "mv ", "cp ", "dd ", "truncate", "-delete", "-exec", "xargs") if w in cmd]
            if bad:
                fail("command_run is not read-only: %s" % bad[:3])
            print("OK: the recorded command is a read-only find or ls")
        else:
            fail("unknown criterion")
    elif cell == "IB171-3":
        if arm == "AC1":
            release_census("IB171-3", 348, "irpt-holdings", "HoldingsSnapshot.schema.json")
            print("OK: irpt-holdings built twice identical, the schema copy among the changed members, equal to the repo blobs")
        elif arm == "AC2":
            packet_ok(348, "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-498.md")
            print("OK: the packet carries Branch A and B, the red list, the shas, the halves and the rollback")
        elif arm == "AC3":
            r = load(D + "0.9.0_WK_IRPT_BCKEND~348/IB171-3_replay_arms.json")
            arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
            want = {"node_with_account_id": "valid", "node_without_account_id": "valid", "node_with_unknown_member": "refused"}
            if arms != want:
                fail("replay arms must read %s, read %s" % (want, arms))
            if r.get("served_figures_changed") != 0:
                fail("served_figures_changed must be 0")
            zeros(r)
            print("OK: the three replay arms read as required; no served figure changes")
        else:
            fail("unknown criterion")
    elif cell == "IB171-4":
        if arm == "AC1":
            release_census("IB171-4", 349, "irpt-directory-search", "handler.py")
            print("OK: irpt-directory-search built twice identical, handler.py among the changed members")
        elif arm == "AC2":
            packet_ok(349, "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-499.md")
            print("OK: the packet carries Branch A and B, the red list, the shas, the halves and the rollback")
        elif arm == "AC3":
            r = load(D + "0.9.0_WK_IRPT_BCKEND~349/IB171-4_reach_and_arms.json")
            arms = {a.get("arm"): a.get("verdict") for a in (r.get("arms") or [])}
            want = {"tail_of_non_head_account": "account_entry", "shared_tail": "two_account_entries", "name_query": "relationship_entry", "entry_without_masks": "unchanged"}
            if arms != want:
                fail("replay arms must read %s, read %s" % (want, arms))
            reach = r.get("reach") or {}
            if not reach:
                fail("reach (per firm) is required")
            for firm, v in reach.items():
                if not all(is_int(v.get(k)) and v[k] >= 0 for k in ("entries", "entries_with_masks", "accounts", "accounts_tail_addressable_after")):
                    fail("reach for %s needs integer entries, entries_with_masks, accounts, accounts_tail_addressable_after" % firm)
                if v["accounts_tail_addressable_after"] < v["accounts"] and v["entries_with_masks"] == v["entries"]:
                    fail("reach for %s: every entry has masks, so every account is tail-addressable after" % firm)
            raw = json.dumps(r)
            if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw):
                fail("the record carries a long digit run")
            zeros(r)
            print("OK: the four replay arms read as required; reach counted for %d firm(s)" % len(reach))
        else:
            fail("unknown criterion")
    elif cell == "IB171-5":
        gens = [("src/pages/InvestorReporting/__tests__/fe-s-15/gen-fixtures.ts", ["fixtures/fe-s-15", "fixtures/smoke/fe-s-15-clean.json", "fixtures/smoke/fe-s-15-needs-correction.json"]),
                ("src/pages/InvestorReporting/__tests__/fe-s-18/gen-fixtures.ts", ["fixtures/smoke"])]
        if arm == "AC1":
            for g, outs in gens:
                rc, out = run(["bun", "run", g], timeout=100, cwd=ROOT / "portal")
                if rc != 0:
                    fail("%s did not run: %s" % (g.split("/")[-2], re.sub(r"\s+", " ", out)[-160:]))
            rc, diff = run(["git", "-C", str(ROOT / "portal"), "diff", "--ignore-cr-at-eol", "--stat", "--", "src/pages/InvestorReporting/fixtures"], timeout=60)
            if diff.strip():
                fail("a generator drifts from the committed bytes: %s" % re.sub(r"\s+", " ", diff)[:200])
            print("OK: both generators run and reproduce the committed fixtures")
        elif arm == "AC2":
            wire = load(PORTAL_IR + "fixtures/wire/AnalysisReport.valid.json")
            sids = {s.get("section_id") for s in (wire.get("instance", wire).get("sections") or [])}
            n = 0
            for rel in (PORTAL_IR + "fixtures/wire/ExportBundle.valid.json", PORTAL_IR + "fixtures/wire/requests/submit-export.request.json"):
                d = load(rel)
                raw = json.dumps(d)
                found = re.findall(r'"selected_sections"\s*:\s*\[([^\]]*)\]', raw)
                if not found:
                    fail("%s carries no selected_sections" % rel)
                for chunk in found:
                    for sid in re.findall(r'"([^"]+)"', chunk):
                        n += 1
                        if sid not in sids:
                            fail("%s: selected section %r is not a section_id of the AnalysisReport wire copy %s" % (rel.split("/")[-1], sid, sorted(sids)))
            print("OK: %d selected section id(s) all resolve" % n)
        elif arm == "AC3":
            T = "src/pages/InvestorReporting/__tests__/dsgn-irptv1/"
            files = [T + "iv-e-101.opal-report-words.test.tsx", T + "iv-e-105.opal-document-words.test.tsx", T + "iv-e-106.sections-retained-ref.test.ts",
                     T + "iv-e-115.vendor-section-names-units.test.tsx", T + "iv-e-122.vendor-validation-and-source.test.tsx"]
            rc, out = run(["bun", "test"] + files, timeout=110, cwd=ROOT / "portal")
            out = re.sub(r"\x1b\[[0-9;]*m", "", out)
            m = re.search(r"(\d+) pass", out)
            f = re.search(r"(\d+) fail", out)
            if rc != 0 or not m or int(m.group(1)) < 21 or (f and int(f.group(1)) != 0):
                fail("the five portal tests: rc %s, %s pass, %s fail" % (rc, m.group(1) if m else "?", f.group(1) if f else "?"))
            hits = 0
            for p in (ROOT / PORTAL_IR / "fixtures").rglob("*.json"):
                t = p.read_text(encoding="utf-8", errors="replace")
                if re.search(r"section_type[\"']?\s*[:=]\s*[\"']annualized_return[\"']", t):
                    hits += 1
            if hits:
                fail("%d fixture(s) carry the old AnalysisReport section again" % hits)
            print("OK: the five portal tests pass and the old section is not back")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
