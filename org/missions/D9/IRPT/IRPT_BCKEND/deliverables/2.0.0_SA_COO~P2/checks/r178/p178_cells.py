"""IRPT_BCKEND round 178 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB178-2  IB-pr-513  ONE more read-only count of leftover snapshot temp files on the runner host AFTER the 14:15Z holdings builds (the first read, IB178-1, preceded any build)
    AC1  the record: counts are integers taken after a real build, on a host that is Online; the build is named (start time, package VersionId equal to the apply's, package digest, its own log line showing the snapshot path)
    AC2  the command is a read-only count and the record carries no path, name or long digit run
    AC3  the counts read 0 for both firms, and the bound counters: no write, no host start, no deletion
  IB178-1  IB-pr-512  the APPLY of the signed host-bundle pair (IB-pr-510): the two minimal holdings packages put at the runner host's next SCHEDULED Online, digest-gated, with the first read
    AC1  the gates: step 0 (the runner role admitted by both firm buckets' policies), the schedule evidence (the host came Online by its schedule; no seat started it), the ledger entry
    AC2  each applied firm: the start read equals the packet's live values; the put-object; the read-back equals the candidate and its restamped metadata; cottonwood untouched
    AC3  the first read (leftover temp-file counts only) and the bound counters (two uploads, no host start, no figure written)
"""
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
REC = D + "0.7.0_AE_CloudOps~IB2/IB178-1_apply_record.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~362/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-510.md"
CAND = D + "0.9.0_WK_IRPT_BCKEND~362/IB177-1_candidate_packages.json"
FIRMS_APPLIED = ("49financial", "inflection")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB178"))
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


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB178-2":
        r2 = load(D + "0.7.0_AE_CloudOps~IB2/IB178-2_post_build_count.json")
        if arm == "AC1":
            c2 = r2.get("temp_file_counts") or {}
            if sorted(c2) != sorted(FIRMS_APPLIED) or not all(is_int(v) and v >= 0 for v in c2.values()):
                fail("temp_file_counts needs an integer >= 0 for %s" % list(FIRMS_APPLIED))
            if not str(r2.get("last_build_finished_utc", "")).strip() or not str(r2.get("read_at_utc", "")).strip() or r2["read_at_utc"] <= r2["last_build_finished_utc"]:
                fail("read_at_utc must be later than last_build_finished_utc (the count is taken after the builds)")
            if r2.get("host_state_at_read") != "running" or r2.get("ssm_status") not in ("Success", {"49financial": "Success", "inflection": "Success"}):
                fail("the read needs host_state_at_read running and ssm_status Success")
            bd = r2.get("build") or {}
            if not str(bd.get("start_utc", "")).strip() or bd.get("start_utc") > r2["last_build_finished_utc"]:
                fail("build.start_utc is required and must precede last_build_finished_utc")
            apply_rec = load(D + "0.7.0_AE_CloudOps~IB2/IB178-1_apply_record.json")
            newv = {a["firm_id"]: a["put"]["new_version_id"] for a in apply_rec.get("applies") or []}
            if bd.get("firm_id") not in newv or bd.get("package_version_id") != newv[bd.get("firm_id")]:
                fail("build.package_version_id must equal the VersionId the apply put for build.firm_id (%s)" % newv)
            if not re.fullmatch(r"[0-9a-f]{64}", str(bd.get("package_sha256", ""))):
                fail("build.package_sha256 must be the 64-hex digest of the package the build ran")
            if not str(bd.get("snapshot_path_log_line", "")).strip() or not str(bd.get("log_source", "")).strip():
                fail("build.snapshot_path_log_line and build.log_source are required (the positive control: the build's own log line showing it took the snapshot path)")
            print("OK: post-build counts %s; the build is named" % c2)
        elif arm == "AC2":
            cmd = str(r2.get("command_run", ""))
            if not re.search(r"find", cmd) or "wc -l" not in cmd or re.search(r"(rm|mv|cp|tee|shred|dd|truncate|xargs)|-delete|-exec", cmd):
                fail("command_run must be a read-only find piped to wc -l")
            if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r2.get("temp_file_counts"))) or re.search(r"/tmp/\S", json.dumps(r2.get("temp_file_counts"))):
                fail("the counts carry a path or a long digit run")
            print("OK: the command is a read-only count")
        elif arm == "AC3":
            if any((r2.get("temp_file_counts") or {}).get(f) != 0 for f in FIRMS_APPLIED):
                fail("PASS needs 0 leftover files for both firms after a build on the new packages; a non-zero count is reported and the criterion fails by design: %s" % r2.get("temp_file_counts"))
            for k, v in {"objects_uploaded": 0, "hosts_started": 0, "functions_invoked": 0, "files_deleted": 0, "aws_writes_made": 0}.items():
                if r2.get(k) != v:
                    fail("the bound counter %s must read %s, reads %r" % (k, v, r2.get(k)))
            print("OK: no write, no host start, no deletion")
        else:
            fail("unknown criterion")
        print("%s PASS" % CID)
        return
    if cell != "IB178-1":
        fail("unknown criterion %r" % CID)
    r = load(REC)
    cand = {p["firm_id"]: p for p in load(CAND).get("packages") or []}
    if arm == "AC1":
        s0 = r.get("step0") or {}
        pol = {x.get("firm_id"): x for x in s0.get("bucket_policies") or []}
        if sorted(pol) != sorted(FIRMS_APPLIED):
            fail("step0.bucket_policies must read exactly %s" % list(FIRMS_APPLIED))
        for f, x in pol.items():
            if (x.get("runner_role_admitted") is not True or x.get("assume_ok") is not True or x.get("apply_principal_may_put") is not True
                    or not str(x.get("statement_ids", "")).strip() or not str(x.get("run_principal", "")).strip()):
                fail("%s: the per-firm run principal must be named (run_principal), assumable (assume_ok), admitted (runner_role_admitted) with the Sids, and the applier may put (apply_principal_may_put); otherwise the apply STOPS and writes nothing" % f)
        sc = r.get("schedule") or {}
        for k in ("next_scheduled_online_utc", "source", "host_online_observed_at", "started_by"):
            if not str(sc.get(k, "")).strip():
                fail("schedule.%s is required" % k)
        if sc.get("started_by") != "scheduler":
            fail("the host must have come Online by its schedule (started_by 'scheduler'), not started by a seat: reads %r" % sc.get("started_by"))
        led = str(r.get("ledger_entry", ""))
        lf = ROOT / led
        if not led.startswith("org/critical_paths/change_management/") or not lf.is_file():
            fail("ledger_entry must be an existing file under org/critical_paths/change_management/")
        txt = lf.read_text(encoding="utf-8", errors="replace")
        for f in FIRMS_APPLIED:
            if cand[f]["rollback_version_id"] not in txt:
                fail("the ledger entry must name %s's rollback VersionId %s" % (f, cand[f]["rollback_version_id"]))
        print("OK: step 0 admitted both buckets; the host came Online by schedule; the ledger entry names both rollbacks")
    elif arm == "AC2":
        ap = {a.get("firm_id"): a for a in r.get("applies") or []}
        if sorted(ap) != sorted(FIRMS_APPLIED):
            fail("applies must read exactly %s (cottonwood is not in the apply)" % list(FIRMS_APPLIED))
        pk = (ROOT / PACKET).read_text(encoding="utf-8", errors="replace")
        for f, a in ap.items():
            c = cand[f]
            sr = a.get("start_read") or {}
            if sr.get("version_id") != c["rollback_version_id"] or sr.get("sha256") != c["live_object_sha256"]:
                fail("%s: the start read must equal the packet's live VersionId and sha256" % f)
            if a.get("candidate_sha256") != c["candidate_package_sha256"]:
                fail("%s: the rebuilt candidate must equal the packet's candidate sha256" % f)
            put = a.get("put") or {}
            rb = a.get("readback") or {}
            if not put.get("new_version_id") or put.get("new_version_id") == c["rollback_version_id"]:
                fail("%s: put.new_version_id must be a NEW VersionId" % f)
            if rb.get("sha256") != c["candidate_package_sha256"] or rb.get("version_id") != put.get("new_version_id"):
                fail("%s: the read-back of the new version must hash to the candidate sha256" % f)
            md = rb.get("metadata") or {}
            stamp = md.get("members-sha256", "")
            if not re.fullmatch(r"[0-9a-f]{64}", stamp) or stamp not in pk or md.get("member-count") not in ("44", 44):
                fail("%s: the read-back metadata must carry the packet's candidate members-sha256 and member-count 44" % f)
        cw = r.get("cottonwood_untouched") or {}
        if not cw.get("etag_before") or cw.get("etag_before") != cw.get("etag_after"):
            fail("cottonwood's ETag must be unchanged (etag_before equal etag_after)")
        if r.get("rollback_performed") is not False:
            fail("rollback_performed must be false (or the apply STOPPED: then applies is empty and this criterion fails by design)")
        print("OK: both firms applied by digest; read-backs equal the candidates; cottonwood untouched")
    elif arm == "AC3":
        fr = r.get("first_read") or {}
        counts = fr.get("temp_file_counts") or {}
        if sorted(counts) != sorted(FIRMS_APPLIED) or not all(is_int(v) and v >= 0 for v in counts.values()):
            fail("first_read.temp_file_counts needs an integer >= 0 for %s" % list(FIRMS_APPLIED))
        if "command_run" not in fr or re.search(r"\b(rm|mv|cp|tee|shred|dd|truncate|xargs)\b|-delete|-exec|>", str(fr.get("command_run"))):
            fail("first_read.command_run must be a read-only count (find/ls piped to wc)")
        raw = json.dumps(fr)
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw) or re.search(r"/tmp/\S", raw):
            fail("the first read carries a path or a long digit run: counts only")
        want = {"objects_uploaded": 2, "hosts_started": 0, "functions_invoked": 0, "accounts_written": 0, "figures_written": 0, "files_deleted": 0}
        for k, v in want.items():
            if r.get(k) != v:
                fail("the bound counter %s must read %s, reads %r" % (k, v, r.get(k)))
        print("OK: first read counts %s; bound counters as required" % counts)
    else:
        fail("unknown criterion")
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
