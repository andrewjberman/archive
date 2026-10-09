"""IRPT_ANLREQ release 1 (issuer 2.0.0_SA_COO~Y2) -- checks of TO-APPLY-Y1 (irpt-status + the /original route; pair
release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_IRPT_STATUS.md (blob ae6a278722) + CTO half NEVER_WIDEN_RELEASE1_IRPT_STATUS_CTO_HALF.md (msg 2940)).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads committed JSON and re-reads live AWS state (read-only).

  APPLY1-AC1  the after-reads file reads "0".."5" each "PASS"; built_sha == the signed WTGCJPiS..; LIVE irpt-status CodeSha256 (re-read here)
              equals it; the /original route exists exactly ONCE on the API (CTO condition); rolled_back false. Base: FAIL (no file).
  APPLY1-AC2  read 3's own objects are named: `read3_objects` is a list of {key, version_id}, and every named object is present unless Andrew's
              delete is recorded (`deleted_on_andrews_word` true). Base: FAIL (no file).
  APPLY1-AC3  branch coherence: every read PASS -> live == built and the route present; any read not PASS -> rolled_back true, live ==
              E7VKvhg3.. and the route ABSENT; ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

F = "org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r1/APPLY-Y1_after_reads.json"
FN = "irpt-status"
BUILT = "BjUZjt2oq8GPJSibq4vD/0m8/LfdN0GF3THwCaBMVOM="  # AMENDMENT 1: pair REVISION 2 at f23639ea21 (was WTGCJPiS)
ROLLBACK = "E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA="
ROUTE = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original"
READS = [str(i) for i in range(0, 6)]


def live_sha():
    import boto3
    return boto3.client("lambda").get_function_configuration(FunctionName=FN)["CodeSha256"]


def route_count():
    import boto3
    api = boto3.client("apigatewayv2")
    n = 0
    for page in api.get_paginator("get_apis").paginate():
        for a in page.get("Items") or []:
            for rp in api.get_paginator("get_routes").paginate(ApiId=a["ApiId"]):
                n += sum(1 for r in rp.get("Items") or [] if r.get("RouteKey") == ROUTE)
    return n


def object_present(key, version_id):
    import boto3
    from botocore.exceptions import ClientError
    bucket, _, k = key.partition("/") if not key.startswith("s3://") else key[5:].partition("/")
    try:
        boto3.client("s3").head_object(Bucket=bucket, Key=k, VersionId=version_id)
        return True
    except ClientError:
        return False


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "APPLY1"))
        sys.exit(1)

    if cid not in ("APPLY1-AC1", "APPLY1-AC2", "APPLY1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = d.get("reads") or {}
    all_pass = all(reads.get(r) == "PASS" for r in READS)

    if cid == "APPLY1-AC1":
        if not all_pass:
            fail("reads not all PASS: %r" % {r: reads.get(r) for r in READS})
        if d.get("built_sha") != BUILT:
            fail("built_sha %r != signed %s" % (d.get("built_sha"), BUILT))
        live = live_sha()
        n = route_count()
        print("live CodeSha256 %s; route %r count %d" % (live, ROUTE, n))
        if live != BUILT:
            fail("live %s != built %s" % (live, BUILT))
        if n != 1:
            fail("route count %d, expected exactly 1" % n)
        if d.get("rolled_back") is not False:
            fail("rolled_back is %r" % d.get("rolled_back"))
    elif cid == "APPLY1-AC2":
        objs = d.get("read3_objects")
        if not isinstance(objs, list):
            fail("read3_objects missing")
        gone = [o for o in objs if not object_present(o.get("key", ""), o.get("version_id"))]
        print("denominator: %d named object(s), %d absent" % (len(objs), len(gone)))
        if gone and d.get("deleted_on_andrews_word") is not True:
            fail("named objects absent without Andrew's recorded delete: %r" % gone)
    else:
        if d.get("ledger_closed") is not True:
            fail("ledger_closed is %r" % d.get("ledger_closed"))
        live, n = live_sha(), route_count()
        print("live %s; reads all PASS: %s; rolled_back %r; route count %d" % (live, all_pass, d.get("rolled_back"), n))
        if all_pass:
            if d.get("rolled_back") is not False or live != BUILT or n != 1:
                fail("branch A incoherent")
        elif d.get("rolled_back") is not True or live != ROLLBACK or n != 0:
            fail("branch B incoherent")
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
