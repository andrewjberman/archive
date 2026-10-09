"""IRPT_BCKEND round 94 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-383: apply the ONE directory release of
IB-pr-380 + IB-pr-381 (CTO ruling msg 1988) under its never-widen pair (COO half @8323d3fb19, CTO half @f0a2f049f7), with the per-firm seeding run, by
0.7.0_AE_CloudOps~DELL2.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB94-2-AC1  irpt-directory-refresh live CodeSha256 (read now) equals the built sha256 in IB-pr-381's census, and the after-reads file A
              records the runner bundle landed (bundle_live_version_after differs from bundle_live_version_before, bundle_sha256 equals
              the census), replay_before_ledger identical, ledger CLOSED. Base: FAIL (live is RbpsijC2; no A).
  IB94-2-AC2  A's driven refresh: every firm READY (reason_code not REFRESH_FAILED), read at its manifest's own as_of; terminated_count
              inflection 1, cottonwood 1, 49financial 0; the carried entry present in the served directory at inflection and cottonwood.
              49financial's first landing with the new bundle is read: per_firm.49financial.source_client_ids_present is a bool
              (CTO half condition). Base: FAIL (no A).
"""
import json
import subprocess
import sys
from pathlib import Path

CENSUS = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~189/IB93-1_release_census.json"
A = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~DELL2/IB94-2_directory_release_after_reads.json"
FN = "irpt-directory-refresh"
WANT_TERMINATED = {"inflection": 1, "cottonwood": 1, "49financial": 0}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB94-2"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB94-2-AC1":
        census = load(CENSUS)
        built = [f["built_zip"]["sha256_b64"] for f in census.get("functions") or [] if f.get("function") == FN
                 or FN in str(f.get("build_command", ""))]
        bundle_built = str(((census.get("runner_bundle") or {}).get("built") or {}).get("sha256", ""))
        if len(built) != 1 or len(bundle_built) != 64:
            fail("census built shas %r / %r" % (built, bundle_built))
        aws = str(root / ".tools" / "aws")
        p = subprocess.run(["bash", aws, "lambda", "get-function-configuration", "--function-name", FN,
                            "--query", "CodeSha256", "--output", "text"], capture_output=True, timeout=120)
        live = p.stdout.decode("utf-8", "replace").strip()
        if p.returncode != 0 or len(live) < 40:
            fail("live read rc %d: %r %r" % (p.returncode, live, p.stderr.decode("utf-8", "replace")[-200:]))
        if live != built[0]:
            fail("live %s != built %s" % (live, built[0]))
        a = load(A)
        b = a.get("bundle") or {}
        if not b.get("bundle_live_version_after") or b.get("bundle_live_version_after") == b.get("bundle_live_version_before"):
            fail("bundle %r" % b)
        if b.get("bundle_sha256") != bundle_built:
            fail("bundle_sha256 %r != built %s" % (b.get("bundle_sha256"), bundle_built))
        if a.get("replay_before_ledger") != "identical" or a.get("ledger") != "CLOSED":
            fail("replay %r ledger %r" % (a.get("replay_before_ledger"), a.get("ledger")))
        print("OK: live %s == built; bundle %s landed; ledger CLOSED" % (live, b["bundle_live_version_after"]))
    elif cid == "IB94-2-AC2":
        firms = (load(A).get("driven_refresh") or {}).get("per_firm") or {}
        for firm, want in WANT_TERMINATED.items():
            r = firms.get(firm) or {}
            if r.get("reason_code") in (None, "", "REFRESH_FAILED") or not r.get("manifest_as_of"):
                fail("%s %r" % (firm, r))
            if r.get("terminated_count") != want:
                fail("%s terminated_count %r, want %d" % (firm, r.get("terminated_count"), want))
            # IB-pr-383 AMENDMENT 3: the applier records the carried entry as a COUNT; >= 1 (or True) is "present in the served directory"
            carried = r.get("carried_in_served")
            if want and not (carried is True or (type(carried) is int and carried >= 1)):
                fail("%s carried_in_served %r" % (firm, r.get("carried_in_served")))
        if not isinstance((firms.get("49financial") or {}).get("source_client_ids_present"), bool):
            fail("49financial first landing not read: %r" % firms.get("49financial"))
        print("OK: READY at 3 of 3 firms; terminated inflection 1, cottonwood 1, 49financial 0; carried entries served")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
