"""IRPT_BCKEND round 65 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell IB-yr-651 (irpt-ycharts-generate RELEASE 2,
TCKT_VNEXT X-1, run as signed: pair NEVER_WIDEN_PAIR_RELEASE2.md @bf4707adf1 + CTO half @6d24511482; CTO round analysis E2).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads one committed JSON and re-reads live AWS state (read-only).

  Y65-1-AC1  the after-reads file reads 1-7 all "PASS", built_sha == the signed 798Lgqw2.., and the LIVE CodeSha256 (re-read here)
             equals it; rolled_back false. Base: FAIL (no file).
  Y65-1-AC2  the test row (opal-users-v2, the PK in test_filer_key, SK PROFILE) and every key in upload_keys read back NOT FOUND
             (re-read here), whichever branch ran. Base: FAIL (no file).
  Y65-1-AC3  branch coherence: every read PASS -> rolled_back false and live == built; any read not PASS -> rolled_back true and
             live == the rollback ZspX0qD2.. (re-read here); ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/deliverables/0.9.0_WK_IRPT_BCKEND~156/Y65-1_release2_after_reads.json"
FN = "irpt-ycharts-generate"
BUILT = "798Lgqw25X1am7uCjdgYdTSOY90saT2k3n8H01eOBJ0="
ROLLBACK = "ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI="
READS = [str(i) for i in range(1, 8)]
USERS = "opal-users-v2"


def live_sha():
    import boto3
    return boto3.client("lambda").get_function_configuration(FunctionName=FN)["CodeSha256"]


def absent(k):
    import boto3
    kind = k.get("kind")
    if kind == "ddb":
        key = {"PK": {"S": k["pk"]}}
        if k.get("sk") is not None:
            key["SK"] = {"S": k["sk"]}
        return "Item" not in boto3.client("dynamodb").get_item(TableName=k["table"], Key=key, ConsistentRead=True)
    if kind == "s3":
        from botocore.exceptions import ClientError
        try:
            boto3.client("s3").head_object(Bucket=k["bucket"], Key=k["key"])
            return False
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
                return True
            raise
    raise ValueError("unknown key kind %r" % kind)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "Y65"))
        sys.exit(1)

    if cid not in ("Y65-1-AC1", "Y65-1-AC2", "Y65-1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = d.get("reads") or {}
    all_pass = all(reads.get(r) == "PASS" for r in READS)

    if cid == "Y65-1-AC1":
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
    elif cid == "Y65-1-AC2":
        tk = d.get("test_filer_key") or {}
        if not tk.get("pk"):
            fail("no test_filer_key.pk")
        keys = [{"kind": "ddb", "table": USERS, "pk": tk["pk"], "sk": "PROFILE"}] + list(d.get("upload_keys") or [])
        if all_pass and len(keys) < 2:
            fail("reads PASS but upload_keys is empty (the admit read creates at least one record)")
        for k in keys:
            ok = absent(k)
            print("%s %s" % ("NOT-FOUND" if ok else "PRESENT", json.dumps(k, sort_keys=True)))
            if not ok:
                fail("still present: %r" % k)
        print("denominator: %d key(s)" % len(keys))
    else:
        if d.get("ledger_closed") is not True:
            fail("ledger_closed is %r" % d.get("ledger_closed"))
        live = live_sha()
        print("live CodeSha256 %s; reads all PASS: %s; rolled_back %r" % (live, all_pass, d.get("rolled_back")))
        if all_pass:
            if d.get("rolled_back") is not False or live != BUILT:
                fail("branch A incoherent")
        else:
            if d.get("rolled_back") is not True or live != ROLLBACK:
                fail("branch B incoherent: a failed read without a rollback to %s" % ROLLBACK)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
