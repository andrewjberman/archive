"""IRPT_BCKEND round 75 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell TO-APPLY-Y75 (irpt-ycharts-generate RELEASE 5b: E11 + E9 report modules shipped whole + the X-1 actor read-back; pair NEVER_WIDEN_PAIR_RELEASE5B_E11.md (blob 387405f9bf) + CTO half @114c10a09e (msg 2177)).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads committed JSON and re-reads live AWS state (read-only).

  Y75-1-AC1  the after-reads file reads 0-3 and 5-7 "PASS" and read 4 "STORED-NEXT-STATE" (admitted on the template lane with an upload id; RESOLVING then the resident's state), built_sha == the signed 5FRkux2o.., and the LIVE CodeSha256 (re-read here)
             equals it; rolled_back false. Base: FAIL (no file).
  Y75-1-AC2  cleanup in every branch: the test row (opal-users-v2, test_filer_key.pk, SK PROFILE) reads NOT FOUND here; and the
             laptop cleanup result file confirms the admit read-back (body sha256 matches, UPLOAD owner = the
             advisor, acting_principal_id = the filer) and names every key of the after-reads file's admit_keys with "NOT_FOUND" after its delete.
             (dell2 cannot decrypt irpt-requests, so that read is the laptop's, CTO 107133 / ADDENDUM 3.) Base: FAIL (no file).
  Y75-1-AC3  branch coherence: every read PASS -> rolled_back false and live == built; any read not PASS -> rolled_back true and
             live == Un0wVZqj.. (re-read here); ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/../../../../tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y75/Y75-1_release5b_after_reads.json"
LAPTOP = P + "/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_laptop_cleanup_result.json"
FN = "irpt-ycharts-generate"
BUILT = "5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY="
ROLLBACK = "Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY="
READS = [str(i) for i in range(0, 8)]
# AMENDMENT 3 (issuer 2026-10-09 ~10:2xZ): live has since moved under LATER SIGNED releases of the same function; a live
# CodeSha256 in this map is release 5b superseded, not undone. Nothing else is admitted.
LATER_SIGNED = {"ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8=": "IB-pr-390 via IB-pr-395 (CTO msgs 2833/2855)",
                "tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=": "release 6b, TO-APPLY-Y77 (CTO msg 2888)"}


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
        print("%s FAIL" % (cid or "Y75"))
        sys.exit(1)

    if cid not in ("Y75-1-AC1", "Y75-1-AC2", "Y75-1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = dict(d.get("reads") or {})
    # AMENDMENT 1 (issuer 2026-10-09 ~07:5xZ): read 0 asserts "live at start == ROLLBACK"; the applier records it as
    # `live_before`. A measured live_before equal to ROLLBACK is read 0 PASS; any other value is read 0 FAIL.
    if "0" not in reads and "live_before" in d:
        reads["0"] = "PASS" if d["live_before"] == ROLLBACK else "FAIL"
    all_pass = all(reads.get(r) == ("STORED-NEXT-STATE" if r == "4" else "PASS") for r in READS)

    if cid == "Y75-1-AC1":
        if not all_pass:
            fail("reads not all PASS: %r" % {r: reads.get(r) for r in READS})
        if d.get("built_sha") != BUILT:
            fail("built_sha %r != signed %s" % (d.get("built_sha"), BUILT))
        live = live_sha()
        print("live CodeSha256 %s" % live)
        if live != BUILT and live not in LATER_SIGNED:
            fail("live %s != built %s" % (live, BUILT))
        if live in LATER_SIGNED:
            print("live is a later signed release: %s" % LATER_SIGNED[live])
        if d.get("rolled_back") is not False:
            fail("rolled_back is %r" % d.get("rolled_back"))
    elif cid == "Y75-1-AC2":
        tfk = d.get("test_filer_key")
        # AMENDMENT 2 (issuer 2026-10-09 ~09:3xZ): the applier records the key as the PK string itself, or as {"pk": ...}.
        pk = tfk if isinstance(tfk, str) else (tfk or {}).get("pk")
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
            if reads.get("4") == "STORED-NEXT-STATE" and not (adm.get("body_sha256_match") is True
                    and adm.get("owner_is_advisor") is True and adm.get("acting_principal_is_filer") is True):
                fail("the laptop did not confirm the stored body and the UPLOAD record (owner, acting_principal_id)")
            rows = res.get("results") or []
            if rows and all("key_ref" in r for r in rows):
                # AMENDMENT 3 (issuer 2026-10-09 ~10:2xZ): the laptop names keys by opaque key_ref (12 hex; S3 refs carry
                # "@<version_id>"). Grade: one NOT_FOUND result per admit key; every S3 version of the keys file named by
                # its version id AND re-read absent HERE; the DDB rows rest on the laptop's own live re-read (dell2
                # cannot read irpt-requests).
                if len(rows) != len(keys) or any(r.get("after_delete") != "NOT_FOUND" for r in rows):
                    fail("laptop results: %d rows for %d keys, or one not NOT_FOUND" % (len(rows), len(keys)))
                named = {r["key_ref"].split("@", 1)[1] for r in rows if "@" in r["key_ref"]}
                import boto3
                from botocore.exceptions import ClientError
                s3 = boto3.client("s3")
                kf = (root / F).parent / "Y75-1_admit_keys.json"
                s3v = json.loads(kf.read_text(encoding="utf-8")).get("s3_versions") or {} if kf.is_file() else {}
                if not s3v:
                    fail("no s3_versions in %s" % kf)
                for skey, versions in s3v.items():
                    for v in versions:
                        if v not in named:
                            fail("S3 version %s not named in the laptop results" % v)
                        try:
                            s3.head_object(Bucket="opal-data-irpt", Key=skey, VersionId=v)
                            fail("S3 version %s still present" % v)
                        except ClientError:
                            print("ABSENT-HERE s3 version %s" % v)
                print("laptop rows %d of %d keys, all NOT_FOUND" % (len(rows), len(keys)))
            else:
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
            if d.get("rolled_back") is not False or (live != BUILT and live not in LATER_SIGNED):
                fail("branch A incoherent")
        elif d.get("rolled_back") is not True or live != ROLLBACK:
            fail("branch B incoherent: a failed read without a rollback to %s" % ROLLBACK)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
