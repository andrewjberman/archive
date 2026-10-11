"""IRPT_BCKEND round 144 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders with disjoint write sets:
  IB144-1  IB-pr-447  READ ONLY: does the RUNNING irpt-intake-poller read firm_registry.json, and where would those firms come
                      from under the naming canon's registry instead (CTO msg 5611; IB-s-6).
  IB144-2  IB-pr-448  the live package's bytes held ONCE as the rollback artifact, its version id recorded, by the applier: found
                      among the artifact key's existing versions, or the order stops (it does not choose an address).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Every criterion FAILs at base (no file).
  IB144-1-AC1  the live package was read by its bytes (its digest equals the function's CodeSha256) and every place a LIVE member
               opens or reads the firm registry is listed with the member, the line and what is read from it; or none is found.
  IB144-1-AC2  whether the function reads the file on a path a request or a schedule reaches is answered with its claim; the
               fields the code takes from it are listed; where each would come from under the canon's registry is stated with
               the builder or loader call, or that the canon does not hold it.
  IB144-1-AC3  what a release from the tree that drops the file would do is one of three words with its claim; no AWS write; no
               firm name in the outputs' text beyond what the check permits (it greps for none; names are the worker's to avoid).
  IB144-2-AC1  the live CodeSha256 is recorded with its read time, and every version of the artifact key is listed with its
               content digest (count stated).
  IB144-2-AC2  exactly one outcome: FOUND (one version id whose digest equals the live digest, re-read by head-object) with 0
               writes, or NOT_FOUND with 0 writes and the stop stated. No other outcome exists.
  IB144-2-AC3  the bounds held by the record's own command list: reads only (no put, copy, delete, update or apply).
"""
import json
import re
import sys
from pathlib import Path

D1 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~305/"
D2 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/"
OUT1, READ1 = D1 + "IB144-1_poller_firm_registry_read.json", D1 + "IB144-1_POLLER_FIRM_REGISTRY_READ.md"
OUT2 = D2 + "IB144-2_poller_rollback_artifact.json"
CLAIMS = ("measured", "inferred", "held", "absent")
EFFECT = ("OUTAGE", "NO_EFFECT", "CANNOT_BE_TOLD")
WRITE = (r"\bput-object\b", r"\bcopy-object\b", r"\bdelete-object", r"\bs3\s+(cp|mv|rm|sync)\b", r"update-function", r"publish-version",
         r"\bterraform\b", r"safe-apply", r"put-", r"create-", r"delete-", r"\binvoke\b")
B64 = re.compile(r"^[A-Za-z0-9+/]{43}=$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB144"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB144-1-AC1":
        a = load(OUT1)
        p = a.get("live_package") or {}
        if not B64.match(str(p.get("code_sha256") or "")) or p.get("downloaded_bytes_hash_equals_code_sha256") is not True \
                or not isinstance(p.get("members"), int) or not p.get("read_at_utc"):
            fail("live_package needs code_sha256, downloaded_bytes_hash_equals_code_sha256 true, members and read_at_utc")
        r = a.get("registry_reads_in_live_members")
        if not isinstance(r, list) or any(not x.get("member") or not isinstance(x.get("line"), int) or not x.get("what_is_read") for x in r):
            fail("registry_reads_in_live_members must list each read with its member, line and what is read")
        if not r and not a.get("searched_for"):
            fail("no read was found and the record does not say what was searched for")
        if not isinstance(p.get("file_in_package"), bool) or not isinstance(a.get("env_var_points_at_it"), bool):
            fail("live_package.file_in_package and env_var_points_at_it must be stated")
        print("OK: live package %s..., %d members; %d read(s) of the firm registry in live members; the file is in the package: %s" % (
            p["code_sha256"][:8], p["members"], len(r), p["file_in_package"]))
    elif cid == "IB144-1-AC2":
        a = load(OUT1)
        q = a.get("reached_at_run_time") or {}
        if q.get("answer") not in (True, False, None) or "answer" not in q or q.get("claim") not in CLAIMS or not q.get("path_in_words"):
            fail("reached_at_run_time needs answer (true, false or null), a claim and the path in words")
        if q["answer"] is None and q["claim"] != "absent":
            fail("an untold answer must carry the claim absent")
        fields = a.get("fields_taken_from_the_file")
        if not isinstance(fields, list):
            fail("fields_taken_from_the_file is not a list")
        canon = a.get("under_the_canon") or {}
        if not isinstance(canon.get("per_field"), list) or len(canon["per_field"]) != len(fields):
            fail("under_the_canon.per_field must answer each field taken from the file")
        for x in canon["per_field"]:
            if not x.get("field") or x.get("canon_holds_it") not in (True, False) or (x["canon_holds_it"] and ":" not in str(x.get("read_by") or "")):
                fail("each field needs canon_holds_it and, where true, read_by as file:function-or-line")
        print("OK: reached at run time: %r (%s); %d field(s) taken from the file, %d the canon holds" % (
            q["answer"], q["claim"], len(fields), sum(1 for x in canon["per_field"] if x["canon_holds_it"])))
    elif cid == "IB144-1-AC3":
        a = load(OUT1)
        e = a.get("a_release_that_drops_the_file") or {}
        if e.get("effect") not in EFFECT or e.get("claim") not in CLAIMS or not e.get("reason"):
            fail("a_release_that_drops_the_file needs effect in %s, a claim and a reason" % (EFFECT,))
        if a.get("aws_writes_made") != 0 or a.get("functions_invoked") != 0 or not isinstance(a.get("not_established"), list):
            fail("aws_writes_made and functions_invoked must be 0 and not_established stated")
        if not (root / READ1).is_file():
            fail("no %s" % READ1)
        print("OK: a release that drops the file: %s (%s); no AWS write, no invoke" % (e["effect"], e["claim"]))
    elif cid == "IB144-2-AC1":
        a = load(OUT2)
        if not B64.match(str(a.get("live_code_sha256") or "")) or not a.get("live_read_at_utc"):
            fail("live_code_sha256 and live_read_at_utc are not recorded")
        v = a.get("artifact_versions")
        if not isinstance(v, list) or a.get("artifact_versions_count") != len(v) or any(not x.get("version_id") or "content_sha256" not in x for x in v):
            fail("artifact_versions must list every version with its version_id and content_sha256, and state the count")
        if not a.get("artifact_bucket_and_key_from"):
            fail("artifact_bucket_and_key_from (where the address was read) is not stated")
        print("OK: live %s...; %d version(s) of the artifact key listed" % (a["live_code_sha256"][:8], len(v)))
    elif cid == "IB144-2-AC2":
        a = load(OUT2)
        o = a.get("outcome")
        if o not in ("FOUND", "NOT_FOUND") or a.get("writes_made") != 0:
            fail("outcome must be FOUND or NOT_FOUND, with writes_made 0")
        if o == "FOUND":
            r = a.get("rollback_artifact") or {}
            if not r.get("version_id") or r.get("content_sha256") != a.get("live_code_sha256") or r.get("re_read_by_head_object") is not True \
                    or sum(1 for x in a.get("artifact_versions") or [] if x.get("content_sha256") == a.get("live_code_sha256")) < 1:
                fail("FOUND needs a version id whose content digest equals the live digest, re-read by head-object")
        elif not a.get("stopped_because"):
            fail("NOT_FOUND must say it stopped and why")
        print("OK: outcome %s; 0 writes" % o)
    elif cid == "IB144-2-AC3":
        a = load(OUT2)
        cmds = a.get("commands")
        if not isinstance(cmds, list) or not cmds:
            fail("commands is empty")
        for c in cmds:
            for pat in WRITE:
                if re.search(pat, str(c)):
                    fail("a recorded command matches the write pattern %r: %s" % (pat, str(c)[:90]))
        print("OK: %d command(s) recorded, all reads" % len(cmds))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
