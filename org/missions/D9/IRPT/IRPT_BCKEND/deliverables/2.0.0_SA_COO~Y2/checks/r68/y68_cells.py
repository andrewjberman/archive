"""IRPT_BCKEND round 68 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell IB-yr-681 (irpt-ycharts-generate RELEASE 3: the E6 build proven on the TEMPLATE lane, no new grant; pair NEVER_WIDEN_PAIR_RELEASE3_A1.md @73140a8098 + CTO half (msg 1606) with
its AMENDMENT 1 (CSV grant withdrawn); GO msg 1643).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads committed JSON and re-reads live AWS state (read-only).

  Y68-1-AC1  the after-reads file reads 0-3 and 5-7 "PASS" and read 4 "STORED-NEXT-STATE" (admitted on the template lane with an upload id; RESOLVING then the resident's state), built_sha == the signed Un0wVZqj.., and the LIVE CodeSha256 (re-read here)
             equals it; rolled_back false. Base: FAIL (no file).
  Y68-1-AC2  cleanup in every branch: the test row (opal-users-v2, test_filer_key.pk, SK PROFILE) reads NOT FOUND here; and the
             laptop cleanup result file confirms the admit read-back (body sha256 matches, UPLOAD owner = the
             advisor, acting_principal_id = the filer) and names every key of the after-reads file's admit_keys with "NOT_FOUND" after its delete.
             (dell2 cannot decrypt irpt-requests, so that read is the laptop's, CTO 107133 / ADDENDUM 3.) Base: FAIL (no file).
  Y68-1-AC3  branch coherence: every read PASS -> rolled_back false and live == built; any read not PASS -> rolled_back true and
             live == ZspX0qD2.. (re-read here); ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/deliverables/0.9.0_WK_IRPT_BCKEND~159/Y68-1_release3_after_reads.json"
LAPTOP = P + "/deliverables/2.0.0_SA_COO~Y2/r68/Y68-1_laptop_cleanup_result.json"
FN = "irpt-ycharts-generate"
BUILT = "Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY="
ROLLBACK = "ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI="
READS = [str(i) for i in range(0, 8)]


def live_sha():
    import boto3
    return boto3.client("lambda").get_function_configuration(FunctionName=FN)["CodeSha256"]


def test_row_absent(pk):
    import boto3
    item = boto3.client("dynamodb").get_item(TableName="opal-users-v2",
                                             Key={"PK": {"S": pk}, "SK": {"S": "PROFILE"}}, ConsistentRead=True)
    return "Item" not in item


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "Y68"))
        sys.exit(1)

    if cid not in ("Y68-1-AC1", "Y68-1-AC2", "Y68-1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = d.get("reads") or {}
    all_pass = all(reads.get(r) == ("STORED-NEXT-STATE" if r == "4" else "PASS") for r in READS)

    if cid == "Y68-1-AC1":
        if not all_pass:
            fail("reads not all PASS: %r" % {r: reads.get(r) for r in READS})
        if d.get("built_sha") != BUILT:
            fail("built_sha %r != signed %s" % (d.get("built_sha"), BUILT))
        live = live_sha()
        print("live CodeSha256 %s" % live)
        if live != BUILT:
            fail("live %s != built %s" % (live, BUILT))
        if d.get("rolled_back") is not False:
            fail("rolled_back is %r" % d.get("rolled_back"))
    elif cid == "Y68-1-AC2":
        pk = (d.get("test_filer_key") or {}).get("pk")
        if not pk:
            fail("no test_filer_key.pk")
        ok = test_row_absent(pk)
        print("%s opal-users-v2 %s PROFILE" % ("NOT-FOUND" if ok else "PRESENT", pk))
        if not ok:
            fail("test row still present")
        keys = d.get("admit_keys") or []
        if reads.get("4") == "STORED-NEXT-STATE" and not keys:
            fail("the admit read PASSED but admit_keys is empty")
        if keys:
            lf = root / LAPTOP
            if not lf.is_file():
                fail("admit_keys present but no laptop cleanup result %s" % LAPTOP)
            res = json.loads(lf.read_text(encoding="utf-8"))
            got = {json.dumps(r.get("key"), sort_keys=True): r.get("after_delete") for r in (res.get("results") or [])}
            adm = res.get("admit_readback") or {}
            print("laptop admit read-back: body_sha256_match=%r owner_is_advisor=%r acting_principal_is_filer=%r" % (
                adm.get("body_sha256_match"), adm.get("owner_is_advisor"), adm.get("acting_principal_is_filer")))
            # AMENDMENT 1 (issuer, 2026-10-09 ~01:3xZ; CTO msg 2091 on CVO msg 2088): AC2 grades CLEANUP only. The X-1 actor
            # read-back (owner, acting_principal_id, body sha) moved to release 5 after-read 4 (CTO msg 1877), row IRPT_BCKEND-D2-S17.
            for k in keys:
                state = got.get(json.dumps(k, sort_keys=True))
                print("%s %s" % (state, json.dumps(k, sort_keys=True)))
                if state != "NOT_FOUND":
                    fail("admit key not confirmed NOT_FOUND by the laptop: %r" % k)
        print("denominator: 1 test row + %d admit key(s)" % len(keys))
    else:
        if d.get("ledger_closed") is not True:
            fail("ledger_closed is %r" % d.get("ledger_closed"))
        live = live_sha()
        print("live CodeSha256 %s; reads all PASS: %s; rolled_back %r" % (live, all_pass, d.get("rolled_back")))
        if all_pass:
            if d.get("rolled_back") is not False or live != BUILT:
                fail("branch A incoherent")
        elif d.get("rolled_back") is not True or live != ROLLBACK:
            fail("branch B incoherent: a failed read without a rollback to %s" % ROLLBACK)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
