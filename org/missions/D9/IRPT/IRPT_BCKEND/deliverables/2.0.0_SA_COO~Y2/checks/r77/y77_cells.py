"""IRPT_BCKEND round 77 (workstream ~Y, issuer 2.0.0_SA_COO~Y2) -- checks of cell TO-APPLY-Y77 (AMENDMENT 2: RELEASE 6b, pair NEVER_WIDEN_PAIR_RELEASE6B_CUSTODY.md + CTO half (msg 2888); originally RELEASE 6: the custody factory; pair release6_custody/NEVER_WIDEN_PAIR_RELEASE6_CUSTODY.md (blob a3c54ba263) + CTO half @96e03f8ba1 (msg 2269)).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Reads committed JSON and re-reads live AWS state (read-only).

  Y77-1-AC1  the after-reads file reads 0-5 "PASS"; built_sha == the signed V6EiBNcJ..; LIVE (re-read here) CodeSha256 equals it;
             the inline policy irpt-ycharts-generate-custody-factory-policy reads back with EXACTLY the 11 signed ARNs; the layers carry
             AWSSDKPandas-Python312:16; rolled_back false. Base: FAIL (no file).
  Y77-1-AC2  read 3's writes are named: every object version under the cottonwood custody_reports prefix (listed live here) that is
             not in the file's `custody_reports_before` set appears in `read3_objects` (key + VersionId), and nothing listed there is
             absent from the bucket unless Andrew's delete is recorded (`deleted_on_andrews_word` true). Base: FAIL (no file).
  Y77-1-AC3  branch coherence: every read PASS -> live == built, policy present; any read not PASS -> rolled_back true, live ==
             ZA0QJ5Wt.. (IB-pr-390), the policy ABSENT and the pandas layer still attached (390's); ledger_closed true either way. Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_BCKEND"
F = P + "/../../../../tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y77/Y77-1_release6_after_reads.json"
FN = "irpt-ycharts-generate"
ROLE = "irpt-ycharts-generate-role"
POLICY = "irpt-ycharts-generate-custody-factory-policy"
LAYER = "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:16"
BUILT = "tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk="  # AMENDMENT 2: release 6b at pin 66207bce7d (was V6EiBNcJ)
ROLLBACK = "ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8="  # AMENDMENT 2: IB-pr-390 live (was 5FRkux2o)
REPORTS_BUCKET = "opal-data-irpt"
REPORTS_PREFIX = "irpt/cottonwood/platinum/custody_reports/"
SIGNED_ARNS = sorted([
    "arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/date=*/data.parquet",
    "arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/date=*/data.parquet",
    "arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/holdings/current/manifest.json",
    "arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/holdings/date=*/*",
    "arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/platinum/holdings/current/manifest.json",
    "arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/platinum/holdings/date=*/*",
    "arn:aws:s3:::opal-data-inflection/irpt/inflection/platinum/holdings/current/manifest.json",
    "arn:aws:s3:::opal-data-inflection/irpt/inflection/platinum/holdings/date=*/*",
    "arn:aws:s3:::opal-data-irpt/irpt/49financial/platinum/custody_reports/*",
    "arn:aws:s3:::opal-data-irpt/irpt/cottonwood/platinum/custody_reports/*",
    "arn:aws:s3:::opal-data-irpt/irpt/inflection/platinum/custody_reports/*",
])
READS = [str(i) for i in range(0, 6)]  # AMENDMENT 2: read 5 = the ticket binding live


def live_config():
    import boto3
    c = boto3.client("lambda").get_function_configuration(FunctionName=FN)
    return c["CodeSha256"], [layer["Arn"] for layer in c.get("Layers") or []]


def live_policy_arns():
    """None when the inline policy is absent; else the sorted resource list across its statements."""
    import boto3
    iam = boto3.client("iam")
    try:
        doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    except iam.exceptions.NoSuchEntityException:
        return None
    arns = []
    for st in doc.get("Statement") or []:
        res = st.get("Resource")
        arns.extend(res if isinstance(res, list) else [res])
    return sorted(arns)


def live_report_versions():
    import boto3
    s3 = boto3.client("s3")
    out = set()
    for page in s3.get_paginator("list_object_versions").paginate(Bucket=REPORTS_BUCKET, Prefix=REPORTS_PREFIX):
        for v in page.get("Versions") or []:
            out.add((v["Key"], v["VersionId"]))
    return out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "Y77"))
        sys.exit(1)

    if cid not in ("Y77-1-AC1", "Y77-1-AC2", "Y77-1-AC3"):
        fail("unknown criterion %r" % cid)
    f = root / F
    if not f.is_file():
        fail("no %s" % F)
    d = json.loads(f.read_text(encoding="utf-8"))
    reads = d.get("reads") or {}
    all_pass = all(reads.get(r) == "PASS" for r in READS)

    if cid == "Y77-1-AC1":
        if not all_pass:
            fail("reads not all PASS: %r" % {r: reads.get(r) for r in READS})
        if d.get("built_sha") != BUILT:
            fail("built_sha %r != signed %s" % (d.get("built_sha"), BUILT))
        live, layers = live_config()
        print("live CodeSha256 %s; layers %d" % (live, len(layers)))
        if live != BUILT:
            fail("live %s != built %s" % (live, BUILT))
        if LAYER not in layers:
            fail("pandas layer not attached: %r" % layers)
        arns = live_policy_arns()
        print("policy %s: %s ARN(s) of %d signed" % (POLICY, "ABSENT" if arns is None else len(arns), len(SIGNED_ARNS)))
        if arns != SIGNED_ARNS:
            fail("policy ARNs differ from the signed 11: extra=%r missing=%r" % (
                sorted(set(arns or []) - set(SIGNED_ARNS)), sorted(set(SIGNED_ARNS) - set(arns or []))))
        if d.get("rolled_back") is not False:
            fail("rolled_back is %r" % d.get("rolled_back"))
    elif cid == "Y77-1-AC2":
        before = {(k, v) for k, v in (d.get("custody_reports_before") or [])}
        named = {(o.get("key"), o.get("version_id")) for o in (d.get("read3_objects") or [])}
        now = live_report_versions()
        new = now - before
        print("denominator: %d version(s) under s3://%s/%s now; %d before; %d new; %d named" % (
            len(now), REPORTS_BUCKET, REPORTS_PREFIX, len(before), len(new), len(named)))
        unnamed = sorted(new - named)
        if unnamed:
            fail("read-3 writes not named: %r" % unnamed)
        gone = sorted(named - now)
        if gone and d.get("deleted_on_andrews_word") is not True:
            fail("named objects absent without Andrew's recorded delete: %r" % gone)
    else:
        if d.get("ledger_closed") is not True:
            fail("ledger_closed is %r" % d.get("ledger_closed"))
        live, layers = live_config()
        arns = live_policy_arns()
        print("live CodeSha256 %s; reads all PASS: %s; rolled_back %r; policy %s; pandas layer %s" % (
            live, all_pass, d.get("rolled_back"), "ABSENT" if arns is None else "PRESENT", LAYER in layers))
        if all_pass:
            if d.get("rolled_back") is not False or live != BUILT or arns is None:
                fail("branch A incoherent")
        # AMENDMENT 2: the pandas layer is already live under IB-pr-390, so branch B keeps it; only the policy is removed.
        elif d.get("rolled_back") is not True or live != ROLLBACK or arns is not None or LAYER not in layers:
            fail("branch B incoherent: a failed read without a full rollback to %s" % ROLLBACK)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
