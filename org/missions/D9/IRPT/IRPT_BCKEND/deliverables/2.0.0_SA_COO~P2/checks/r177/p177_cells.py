"""IRPT_BCKEND round 177 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB177-1  IB-pr-510  the host-bundle pair: ONE minimal package per firm (live bytes plus only the two merged changes), BUILD ONLY, its census, scratch-install read and never-widen packet
    AC1  the record's shape: one package per BUILDERS firm; the replaced members are inside the allowed set; the member diff against live is exactly the replaced members plus SHA256SUMS
    AC2  each replaced member differs from its live bytes only by lines the allowed commits changed (the check re-derives it from git and the stored live and candidate files)
    AC3  the scratch-install read, the packet (Branch A, Branch B, rollback per firm, COO half, the four unchanged members named) and the bound counters
  IB177-2  IB-pr-511  the provenance read of the three package objects and the evidence archive of the four unattributed live members (row W361-S3 (b), (c))
    AC1  the record names the four members the census flagged, with diff counts against their nearest historical blob
    AC2  the archived files hash to the recorded and the census sha256, and the counts re-derive from git
    AC3  one CloudTrail PutObject reading per package object at its last_modified, and the bound counters
"""
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
GOLD = "data/assets/scripts/gold/investor_reporting/"
RUNNER = GOLD + "holdings_snapshot.py"
CAND = D + "0.9.0_WK_IRPT_BCKEND~362/IB177-1_candidate_packages.json"
PROV = D + "0.9.0_WK_IRPT_BCKEND~363/IB177-2_provenance_and_archive.json"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~361/IB176-1_holdings_packages_census.json"
ALLOWED_MEMBERS = {GOLD + "holdings_49f.py", GOLD + "holdings_inf.py", GOLD + "holdings_snapshot.py",
                   "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"}
ALLOWED_COMMITS = ("135fc3509e", "7ace854890", "aa5778d962")
BOUND_ZERO = ("aws_writes_made", "objects_uploaded", "functions_invoked", "ssm_commands_sent", "hosts_started", "accounts_written", "figures_written")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB177"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def sha_file(rel):
    f = ROOT / str(rel)
    if not f.is_file():
        fail("no file %s" % rel)
    return hashlib.sha256(f.read_bytes()).hexdigest()


def git(*args):
    p = subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, timeout=90)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def builders_firms():
    import ast
    src = (ROOT / RUNNER).read_text(encoding="utf-8")
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "BUILDERS" for t in node.targets):
            return sorted(k.value for k in node.value.keys)
    fail("BUILDERS not found")


def lines_of(text):
    return text.replace("\r\n", "\n").split("\n")


def commit_changed_lines(commits, path):
    out = set()
    for c in commits:
        rc, txt = git("show", "--format=", "-U0", c, "--", path)
        if rc != 0:
            fail("git show %s -- %s failed" % (c, path))
        for ln in txt.splitlines():
            if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith("+++") and not ln.startswith("---"):
                out.add(ln[1:].rstrip("\r"))
    return out


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB177-1":
        r = load(CAND)
        pk = r.get("packages") or []
        if arm == "AC1":
            want = builders_firms()
            if sorted(p.get("firm_id") for p in pk) != want:
                fail("the packages must be exactly the BUILDERS firms %s" % want)
            for p in pk:
                rep = p.get("members_replaced") or []
                names = {m.get("repo_path") for m in rep}
                if not rep or not names <= ALLOWED_MEMBERS:
                    fail("%s: replaced members %s must be a non-empty subset of the allowed set" % (p.get("firm_id"), sorted(names - ALLOWED_MEMBERS) or "none"))
                diff = p.get("member_diff_vs_live") or {}
                chg = sorted(diff.get("changed") or [])
                expect = sorted([m.get("name") for m in rep] + ["SHA256SUMS"])
                if chg != expect:
                    fail("%s: member_diff_vs_live.changed %s must equal the replaced members plus SHA256SUMS %s" % (p.get("firm_id"), chg, expect))
                if diff.get("total") != 45 or diff.get("unchanged_count") != 45 - len(chg):
                    fail("%s: total must read 45 and unchanged_count %d" % (p.get("firm_id"), 45 - len(chg)))
            f49 = [p for p in pk if p["firm_id"] == "49financial"][0]
            need = {GOLD + "holdings_49f.py", GOLD + "holdings_snapshot.py", "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"}
            if not need <= {m["repo_path"] for m in f49["members_replaced"]}:
                fail("49financial must replace holdings_49f.py, holdings_snapshot.py and the schema copy")
            print("OK: %d package(s); replaced members %s" % (len(pk), {p["firm_id"]: len(p["members_replaced"]) for p in pk}))
        elif arm == "AC2":
            n = 0
            for p in pk:
                for m in p.get("members_replaced") or []:
                    cs = m.get("commits_applied") or []
                    if not cs or not set(cs) <= set(ALLOWED_COMMITS):
                        fail("%s/%s: commits_applied %s must be a non-empty subset of %s" % (p.get("firm_id"), m.get("name"), cs, ALLOWED_COMMITS))
                    if sha_file(m.get("live_file")) != m.get("live_member_sha256") or sha_file(m.get("candidate_file")) != m.get("candidate_member_sha256"):
                        fail("%s/%s: a stored file does not hash to its recorded sha256" % (p.get("firm_id"), m.get("name")))
                    if m["live_member_sha256"] == m["candidate_member_sha256"]:
                        fail("%s/%s: the candidate equals the live bytes (nothing replaced)" % (p.get("firm_id"), m.get("name")))
                    live = lines_of((ROOT / m["live_file"]).read_text(encoding="utf-8", errors="replace"))
                    cand = lines_of((ROOT / m["candidate_file"]).read_text(encoding="utf-8", errors="replace"))
                    allowed = commit_changed_lines(cs, m["repo_path"])
                    stray = []
                    for ln in difflib.unified_diff(live, cand, lineterm="", n=0):
                        if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith("+++") and not ln.startswith("---"):
                            if ln[1:] not in allowed:
                                stray.append(ln[:80])
                    if stray:
                        fail("%s/%s: %d changed line(s) belong to no allowed commit, first: %s" % (p.get("firm_id"), m.get("name"), len(stray), stray[0]))
                    n += 1
            print("OK: %d replaced member(s) differ from live only by the allowed commits' lines" % n)
        elif arm == "AC3":
            si = r.get("scratch_install") or {}
            if si.get("sha256sum_c") != "OK" or si.get("import_ok") is not True:
                fail("scratch_install needs sha256sum_c OK and import_ok true")
            tp = si.get("temp_file_probe") or {}
            if tp.get("raise_leaves") != 0 or tp.get("return_leaves") != 0 or tp.get("operator_file_kept") is not True:
                fail("temp_file_probe must read raise_leaves 0, return_leaves 0, operator_file_kept true: %s" % tp)
            for k in BOUND_ZERO:
                if r.get(k) != 0:
                    fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
            pf = ROOT / str(r.get("packet", ""))
            if not pf.is_file():
                fail("the packet %r does not exist" % r.get("packet"))
            txt = pf.read_text(encoding="utf-8", errors="replace")
            for needle in ("Branch A", "Branch B", "COO half", "CTO half", "rollback", "scheduled Online", "reporting_policies.json", "resources.json"):
                if needle.lower() not in txt.lower():
                    fail("the packet lacks %r" % needle)
            for p in pk:
                if not str(p.get("rollback_version_id", "")).strip():
                    fail("%s: rollback_version_id (the live object version) is required" % p.get("firm_id"))
            print("OK: scratch install, probe, packet and rollback per firm")
        else:
            fail("unknown criterion")
    elif cell == "IB177-2":
        r = load(PROV)
        census = load(CENSUS)
        flagged = {}
        for p in census.get("packages") or []:
            for m in p.get("members") or []:
                if m.get("unattributed") is True:
                    flagged[(p["firm_id"], m["repo_path"])] = m["live_member_sha256"]
        mem = r.get("unattributed_members") or []
        if arm == "AC1":
            got = {(m.get("firm_id"), m.get("repo_path")) for m in mem}
            if got != set(flagged):
                fail("the members must be exactly the census' unattributed rows %s, read %s" % (sorted(flagged), sorted(got)))
            for m in mem:
                if not re.fullmatch(r"[0-9a-f]{7,40}", str(m.get("nearest_blob_commit", ""))):
                    fail("%s: nearest_blob_commit must be a commit id" % m.get("repo_path"))
                if not is_int(m.get("lines_added")) or not is_int(m.get("lines_removed")) or m.get("change_kind") not in ("comment", "data", "code", "eol", "mixed"):
                    fail("%s: needs integer lines_added, lines_removed and a change_kind in comment/data/code/eol/mixed" % m.get("repo_path"))
            print("OK: %d unattributed member(s) with diff counts" % len(mem))
        elif arm == "AC2":
            for m in mem:
                if sha_file(m.get("archived_file")) != m.get("live_sha256") or m.get("live_sha256") != flagged.get((m.get("firm_id"), m.get("repo_path"))):
                    fail("%s/%s: the archived file must hash to the recorded sha256 and the census' live sha256" % (m.get("firm_id"), m.get("repo_path")))
                rc, blob = git("show", "%s:%s" % (m["nearest_blob_commit"], m["repo_path"]))
                if rc != 0:
                    fail("%s is not a blob at %s" % (m["repo_path"], m["nearest_blob_commit"]))
                a = lines_of(blob)
                b = lines_of((ROOT / m["archived_file"]).read_text(encoding="utf-8", errors="replace"))
                add = rem = 0
                for ln in difflib.unified_diff(a, b, lineterm="", n=0):
                    if ln.startswith("+") and not ln.startswith("+++"):
                        add += 1
                    elif ln.startswith("-") and not ln.startswith("---"):
                        rem += 1
                if (add, rem) != (m.get("lines_added"), m.get("lines_removed")):
                    fail("%s: the recorded counts (%s, %s) do not re-derive (%d, %d)" % (m["repo_path"], m.get("lines_added"), m.get("lines_removed"), add, rem))
            print("OK: %d archived file(s) hash and re-derive" % len(mem))
        elif arm == "AC3":
            ct = r.get("cloudtrail") or []
            if sorted(x.get("firm_id") for x in ct) != builders_firms():
                fail("one CloudTrail reading per BUILDERS firm is required")
            lm = {p["firm_id"]: p["last_modified"] for p in census.get("packages") or []}
            from datetime import datetime
            for x in ct:
                if x.get("event_found") is False:
                    if not str(x.get("reason", "")).strip():
                        fail("%s: event_found false needs a reason" % x.get("firm_id"))
                    continue
                if x.get("event_name") != "PutObject" or not str(x.get("principal", "")).strip() or not str(x.get("event_time", "")).strip():
                    fail("%s: needs event_name PutObject, principal and event_time (or event_found false with a reason)" % x.get("firm_id"))
                t1 = datetime.fromisoformat(x["event_time"].replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(lm[x["firm_id"]])
                if abs((t1 - t2).total_seconds()) > 120:
                    fail("%s: the PutObject event is not within 120 seconds of the package's last_modified" % x["firm_id"])
            for k in BOUND_ZERO:
                if r.get(k) != 0:
                    fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
            print("OK: CloudTrail readings per package; bound counters 0")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
