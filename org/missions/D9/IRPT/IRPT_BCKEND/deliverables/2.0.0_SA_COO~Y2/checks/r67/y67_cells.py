"""IRPT_BCKEND round 67 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell IB-yr-671 (irpt-ycharts-generate RELEASE 2 = E6:
X-1 with the E5 guard, run as signed: pair NEVER_WIDEN_PAIR_RELEASE2_E6.md @8c11ac4ff1 + CTO half @2df0aa0c99; grant applied by the
laptop TO-APPLY-E6).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads committed JSON and re-reads live AWS state (read-only).

  Y67-1-AC1  the after-reads file reads 0-7 all "PASS", built_sha == the signed Un0wVZqj.., and the LIVE CodeSha256 (re-read here)
             equals it; rolled_back false. Base: FAIL (no file).
  Y67-1-AC2  cleanup in every branch: the test row (opal-users-v2, test_filer_key.pk, SK PROFILE) reads NOT FOUND here; and the
             laptop cleanup result file names every key of the after-reads file's admit_keys with "NOT_FOUND" after its delete.
             (dell2 cannot decrypt irpt-requests, so that read is the laptop's, CTO 107133 / ADDENDUM 3.) Base: FAIL (no file).
  Y67-1-AC3  branch coherence: every read PASS -> rolled_back false and live == built; any read not PASS -> rolled_back true and
             live == ZspX0qD2.. (re-read here); ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/deliverables/0.9.0_WK_IRPT_BCKEND~158/Y67-1_release2_after_reads.json"
# AMENDMENT 1 (issuer, ~21:0xZ): the laptop result lives in the issuer folder (TREE_DELIVERABLES owner-in-path), as a
# normalized copy of the laptop leg-2 result @0ca54dbc3d.
LAPTOP = P + "/deliverables/2.0.0_SA_COO~Y2/r67/Y67-1_laptop_cleanup_result.json"
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
        print("%s FAIL" % (cid or "Y67"))
        sys.exit(1)

    if cid not in ("Y67-1-AC1", "Y67-1-AC2", "Y67-1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = d.get("reads") or {}
    all_pass = all(reads.get(r) == "PASS" for r in READS)

    if cid == "Y67-1-AC1":
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
    elif cid == "Y67-1-AC2":
        pk = (d.get("test_filer_key") or {}).get("pk")
        if not pk:
            fail("no test_filer_key.pk")
        ok = test_row_absent(pk)
        print("%s opal-users-v2 %s PROFILE" % ("NOT-FOUND" if ok else "PRESENT", pk))
        if not ok:
            fail("test row still present")
        keys = d.get("admit_keys") or []
        if reads.get("4") == "PASS" and not keys:
            fail("the admit read PASSED but admit_keys is empty")
        if keys:
            lf = root / LAPTOP
            if not lf.is_file():
                fail("admit_keys present but no laptop cleanup result %s" % LAPTOP)
            res = json.loads(lf.read_text(encoding="utf-8"))
            got = {json.dumps(r.get("key"), sort_keys=True): r.get("after_delete") for r in (res.get("results") or [])}
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
