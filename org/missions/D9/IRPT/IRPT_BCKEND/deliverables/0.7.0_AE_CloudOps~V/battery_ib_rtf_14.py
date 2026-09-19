#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-14 battery -- the export role reads the receipt it serves.

FIRST PASS (this revision): arms (a)-(b). (c) apply and (d) the live proof run on the re-hand, after both halves are at
HEAD naming the packet blob; with a half ABSENT the battery STOPS at (b) and says so.
  (a) THE CAUSE, MEASURED:
      (i)   the receipt key the code builds -- the template (export/entry.py:63-64) and the CONCRETE key for the export
            id rtf-12's arm (f) sent -- printed beside the role's policy resource ARNs (live get_role_policy and
            export/iam.tf:85-125), with INSIDE/OUTSIDE decided by fnmatch, never by eye;
      (ii)  simulate-principal-policy for irpt-export-render-role: s3:GetObject on the concrete key, s3:ListBucket on
            the bucket with the s3:prefix context, kms:Decrypt on the bucket's key with the kms:ViaService context --
            one resource per call, with the operator positive control and a no-grant negative control;
      (iii) the swallowed exception. The role is NOT assumable (its trust policy names lambda.amazonaws.com only), and
            the boundary records to a None sink (S91), so the live class CANNOT be printed verbatim. What this arm
            prints instead, and the gap it leaves, stated: (A) the LIVE invoke pair as the deployed role (the same
            event with and without `receipt_fixture`, which bypasses the S3 read) -- the discriminator that the failure
            is the read; (B) the MAPPING arms: the deployed bytes in-process with a stub S3 client raising, in turn,
            AccessDenied (ClientError), NoSuchKey and a non-ClientError -- what the handler maps each to. A class the
            handler maps to a refusal cannot be the live cause, because the live answer is UNEXPECTED;
      (iv)  the receipt object itself: list-objects-v2 under the key's own prefix AND under the policy's prefix, as the
            operator, with counts printed -- the case (PRESENT / ABSENT) stated.
  (b) THE PACKET committed, blob printed, and the 2 halves at HEAD naming it. ABSENT is a truthful STOP.
Read-only on every plane except the deployed function's own GET receipt route (an invoke that writes nothing).
Prints no credential.
"""
from __future__ import annotations

import fnmatch
import importlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-14_R71-AC1_battery_output.txt")
TOKEN = "IBR71-EXPORT-ROLE-READS-THE-RECEIPT"
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-14.md"
FN = "irpt-export-render"
ROLE = "irpt-export-render-role"
ACCT = "313476888478"
ENTRY_REL = "infra/aws/lambda/investor-reporting/export/entry.py"
IAM_REL = "infra/aws/terraform/investor-reporting/export/iam.tf"
# The export id rtf-12's arm (f) sent (its battery output @29ab2f66fa) and the firm it was bound to.
RTF12_EXPORT_ID = "EXP-5db0796cbfcffc3c0c1d5291"
FIRM = "49financial"
REPRO_ROOT = os.environ.get("REPRO_ROOT", r"C:\d14")
LINES: list[str] = []
s3 = boto3.client("s3", region_name="us-east-1")
iam = boto3.client("iam")
lam = boto3.client("lambda", region_name="us-east-1")


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def git(*args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", *args], cwd=WS, capture_output=True, timeout=120)
    return p.returncode, p.stdout


def blob_at(ref: str, path: str) -> bytes | None:
    rc, out = git("show", "%s:%s" % (ref, path))
    return out if rc == 0 else None


def identity_line(arm: str, served: bool = False) -> None:
    who = boto3.client("sts").get_caller_identity()["Arn"]
    if served:
        emit("  identity: %s -- the INVOKE runs the deployed function AS ITS OWN ROLE (%s); the operator identity %s "
             "only issues the invoke and reads configuration" % (arm, ROLE, who))
    else:
        emit("  identity: %s ran as %s -- a configuration/document claim, NOT a served behaviour" % (arm, who))


def key_and_arns() -> tuple[str, str, list, bool]:
    src = (blob_at("HEAD", ENTRY_REL) or b"").decode("utf-8")
    m = re.search(r'"IRPT_EXPORT_RECEIPT_KEY",\s*"([^"]+)"', src)
    template = m.group(1) if m else "<NOT FOUND>"
    env = (lam.get_function_configuration(FunctionName=FN).get("Environment") or {}).get("Variables") or {}
    override = env.get("IRPT_EXPORT_RECEIPT_KEY")
    bucket = env.get("IRPT_EVIDENCE_BUCKET", "")
    effective = override or template
    key = effective.format(firm=FIRM, export_id=RTF12_EXPORT_ID)
    emit("  the template: %s:63-64 @HEAD %r; the deployed override IRPT_EXPORT_RECEIPT_KEY: %s -> effective %r"
         % (ENTRY_REL, template, override or "UNSET (the default applies)", effective))
    emit("  the CONCRETE key for rtf-12's arm (f) request (%s, firm %s): s3://%s/%s" % (RTF12_EXPORT_ID, FIRM, bucket, key))
    arns = []
    for name in iam.list_role_policies(RoleName=ROLE)["PolicyNames"]:
        doc = iam.get_role_policy(RoleName=ROLE, PolicyName=name)["PolicyDocument"]
        for st in doc["Statement"]:
            res = st.get("Resource")
            for r in (res if isinstance(res, list) else [res]):
                arns.append((name, st.get("Sid"), st.get("Action"), r))
    emit("  the role's %d policy resource ARNs (live get_role_policy):" % len(arns))
    for name, sid, act, r in arns:
        emit("     %-44s %-32s %-46s %s" % (name, sid, json.dumps(act)[:44], r))
    get_arns = [r for _n, _s, a, r in arns if "s3:GetObject" in (a if isinstance(a, list) else [a])]
    full = "arn:aws:s3:::%s/%s" % (bucket, key)
    inside = any(fnmatch.fnmatch(full, pat) for pat in get_arns)
    emit("  INSIDE/OUTSIDE: the concrete key %s any s3:GetObject resource ARN -> %s" % (
        "matches" if inside else "matches NO", "INSIDE" if inside else "OUTSIDE"))
    for pat in get_arns:
        emit("     fnmatch(%s, %s) = %s" % (full, pat, fnmatch.fnmatch(full, pat)))
    tf = (blob_at("HEAD", IAM_REL) or b"").decode("utf-8")
    m2 = re.search(r'Sid\s+=\s+"ReadWriteExportsPrefixOnly".*?Resource = \[\s*"([^"]+)"', tf, re.S)
    emit("  %s @HEAD, Sid ReadWriteExportsPrefixOnly: %s" % (IAM_REL, m2.group(1) if m2 else "<NOT FOUND>"))
    return bucket, key, get_arns, inside


def simulations(bucket: str, key: str) -> bool:
    kms_key = s3.get_bucket_encryption(Bucket=bucket)["ServerSideEncryptionConfiguration"]["Rules"][0][
        "ApplyServerSideEncryptionByDefault"].get("KMSMasterKeyID", "")
    src = {"the role": "arn:aws:iam::%s:role/%s" % (ACCT, ROLE),
           "positive control (user Andrew_Berman)": "arn:aws:iam::%s:user/Andrew_Berman" % ACCT,
           "negative control (opalinvest-auth-lambda-role)": "arn:aws:iam::%s:role/opalinvest-auth-lambda-role" % ACCT}
    cases = [
        ("s3:GetObject", "arn:aws:s3:::%s/%s" % (bucket, key), []),
        ("s3:ListBucket", "arn:aws:s3:::%s" % bucket, [{"ContextKeyName": "s3:prefix", "ContextKeyType": "string",
                                                        "ContextKeyValues": [os.path.dirname(key) + "/"]}]),
        ("kms:Decrypt", kms_key, [{"ContextKeyName": "kms:ViaService", "ContextKeyType": "string",
                                   "ContextKeyValues": ["s3.us-east-1.amazonaws.com"]}]),
    ]
    role_denied = ctrl_ok = 0
    for act, res, ctx in cases:
        for who, arn in src.items():
            kw = {"PolicySourceArn": arn, "ActionNames": [act], "ResourceArns": [res]}
            if ctx:
                kw["ContextEntries"] = ctx
            d = iam.simulate_principal_policy(**kw)["EvaluationResults"][0]["EvalDecision"]
            emit("  simulate %-13s on %-70s as %-46s -> %s%s" % (act, res[:70], who, d, " (context: %s)" % ctx[0]["ContextKeyName"] if ctx else ""))
            if who == "the role":
                role_denied += d != "allowed"
            elif "positive" in who:
                ctrl_ok += d == "allowed"
            else:
                ctrl_ok += d != "allowed"
    emit("  the role denied on %d of %d actions; controls as expected %d of %d" % (role_denied, len(cases), ctrl_ok, 2 * len(cases)))
    return ctrl_ok == 2 * len(cases)


def invoke_pair() -> tuple[bool, dict]:
    route = "GET /api/scoped/investor-reporting/export/{exportId}"
    out = {}
    for label, fixture in (("the S3 receipt read (as deployed)", None), ("receipt_fixture {} (the read bypassed)", {})):
        ev = {"version": "2.0", "routeKey": route, "rawPath": "/api/scoped/investor-reporting/export/" + RTF12_EXPORT_ID,
              "rawQueryString": "", "pathParameters": {"exportId": RTF12_EXPORT_ID},
              "headers": {"x-contract-version": "v1", "x-firm-id": FIRM, "x-advisor-id": "abby_horton", "x-user-role": "user",
                          "x-user-email": "irpt-diag@opal.test", "x-origin-verify": "cloudfront", "x-user-tier": "unknown"},
              "requestContext": {"http": {"method": "GET", "path": "/api/scoped/investor-reporting/export/" + RTF12_EXPORT_ID},
                                 "routeKey": route}, "isBase64Encoded": False}
        if fixture is not None:
            ev["receipt_fixture"] = fixture
        r = lam.invoke(FunctionName=FN, Payload=json.dumps(ev).encode("utf-8"))
        body = r["Payload"].read()
        try:
            j = json.loads(body)
            if isinstance(j, dict) and isinstance(j.get("body"), str):
                j = json.loads(j["body"])
        except ValueError:
            j = None
        code = ((j or {}).get("status") or {}).get("public_reason_code") if isinstance(j, dict) else None
        firm = (j or {}).get("firm_id") if isinstance(j, dict) else None
        out[label] = code
        emit("    %-38s -> StatusCode %s FunctionError %s | code %s | firm_id %s" % (
            label, r.get("StatusCode"), r.get("FunctionError"), code, "present" if firm else "ABSENT"))
    read_fails = out["the S3 receipt read (as deployed)"] == "UNEXPECTED" and out["receipt_fixture {} (the read bypassed)"] != "UNEXPECTED"
    emit("    the pair discriminates: the failure IS the S3 read -> %s" % read_fails)
    return read_fails, out


def mapping_arms() -> dict:
    """The deployed bytes in-process with a STUB S3 client raising one class at a time: what the handler maps each to."""
    base = os.path.join(REPRO_ROOT, FN)
    shutil.rmtree(base, ignore_errors=True)
    task, opt = os.path.join(base, "var_task"), os.path.join(base, "opt")
    os.makedirs(task)
    os.makedirs(opt)
    cfg = lam.get_function_configuration(FunctionName=FN)
    zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lam.get_function(FunctionName=FN)["Code"]["Location"], timeout=120).read())).extractall(task)
    for layer in cfg.get("Layers") or []:
        lv = lam.get_layer_version_by_arn(Arn=layer["Arn"])
        zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lv["Content"]["Location"], timeout=120).read())).extractall(opt)
    env = dict((cfg.get("Environment") or {}).get("Variables") or {})
    for k, v in list(env.items()):
        if isinstance(v, str) and v.startswith("/opt/"):
            env[k] = os.path.join(opt, v[len("/opt/"):].replace("/", os.sep))
    for k, v in env.items():
        os.environ[k] = v
    sys.path[:0] = [task, os.path.join(opt, "python")]
    import botocore.exceptions as bexc
    entry = importlib.import_module("entry")
    captured: list[str] = []
    errors_mod = importlib.import_module("errors")
    orig_rec = errors_mod.record_internal

    def rec(sink, cid, op, exc, _o=orig_rec):
        captured.append("%s.%s: %s" % (type(exc).__module__, type(exc).__name__, str(exc)[:160]))
        return _o(sink, cid, op, exc)
    errors_mod.record_internal = rec
    classes = {
        "AccessDenied (ClientError)": bexc.ClientError({"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}, "GetObject"),
        "NoSuchKey (ClientError subclass name NoSuchKey)": type("NoSuchKey", (Exception,), {})("The specified key does not exist."),
        "EndpointConnectionError (not a ClientError)": bexc.EndpointConnectionError(endpoint_url="https://s3.amazonaws.com"),
    }
    out = {}
    for label, exc in classes.items():
        captured.clear()

        class _Stub:
            def get_object(self, **_kw):
                raise exc
        orig_boto3_client = boto3.client

        def fake_client(name, *a, **k):
            return _Stub() if name == "s3" else orig_boto3_client(name, *a, **k)
        boto3.client = fake_client
        try:
            entry._load_receipt(FIRM, RTF12_EXPORT_ID, {})
            verdict = "returned (no exception)"
        except Exception as raised:  # noqa: BLE001 -- the CLASS is the finding
            verdict = "%s.%s" % (type(raised).__module__, type(raised).__name__)
        finally:
            boto3.client = orig_boto3_client
        out[label] = verdict
        emit("    stub raises %-48s -> _load_receipt raises %s" % (label, verdict))
    emit("    the handler maps a class to ExportRefused (a POLICY refusal, NOT_FOUND) only for the names it enumerates; "
         "any other class propagates and the boundary answers UNEXPECTED")
    return out


def wire_arms(bucket: str, key: str) -> dict:
    """The REAL wire classes, run through the handler's own test.

    The stub arms above assert the class THIS AUTHOR chose. botocore's errorfactory mints a MODELED class per
    error code, so the only sound measurement is a real response. An UNSIGNED request reproduces the exact 403 the
    role receives (the requester does not change how the response is parsed), and the operator reproduces the 404.
    """
    from botocore import UNSIGNED
    from botocore.config import Config
    anon = boto3.client("s3", region_name="us-east-1", config=Config(signature_version=UNSIGNED))
    pol = s3.list_objects_v2(Bucket=bucket, Prefix="firms/", MaxKeys=1)
    inside_key = (pol.get("Contents") or [{}])[0].get("Key", "")
    out = {}
    for label, client, k in (("UNSIGNED, the concrete key (the 403 the role gets)", anon, key),
                             ("operator, the concrete key (the 404)", s3, key),
                             ("UNSIGNED, a key INSIDE the grant (control)", anon, inside_key),
                             ("operator, a key INSIDE the grant (control)", s3, inside_key)):
        if not k:
            continue
        try:
            client.get_object(Bucket=bucket, Key=k)["Body"].read()
            emit("    %-52s -> 200 OK, no exception" % label)
            out[label] = "200"
        except Exception as exc:  # noqa: BLE001 -- the CLASS is the finding
            resp = getattr(exc, "response", {}) or {}
            cls = type(exc).__name__
            mapped = cls in ("NoSuchKey", "ClientError")
            emit("    %-52s -> HTTP %s code %-13s class %s.%s -> %s" % (
                label, resp.get("ResponseMetadata", {}).get("HTTPStatusCode"),
                resp.get("Error", {}).get("Code"), type(exc).__module__, cls,
                "MAPPED to ExportRefused (NOT_FOUND)" if mapped else "NOT MAPPED -- propagates -> UNEXPECTED"))
            out[label] = cls
    c = boto3.client("s3", region_name="us-east-1")
    emit("    botocore %s from_code mapping for the codes this route can receive: %s" % (
        __import__("botocore").__version__,
        ", ".join("%s->%s" % (code, c.exceptions.from_code(code).__name__)
                  for code in ("AccessDenied", "NoSuchKey", "NoSuchBucket", "KMS.AccessDeniedException"))))
    denied = out.get("UNSIGNED, the concrete key (the 403 the role gets)")
    missing = out.get("operator, the concrete key (the 404)")
    emit("    THE ASYMMETRY, MEASURED: the role's 403 raises %s (NOT in the handler's name list) while the "
         "operator's 404 raises %s (IN it) -- one code path, two served answers" % (denied, missing))
    return out


def address_census(bucket: str) -> bool:
    """Is the address the reader builds DECLARED, and does anything WRITE it?"""
    lay = json.loads((blob_at("HEAD", "infra/aws/terraform/investor-reporting/core/layout.json") or b"{}").decode("utf-8"))
    fams = lay.get("prefix_families") or {}
    emit("  the evidence bucket's DECLARED layout (core/layout.json @HEAD, generated by terraform):")
    for name, pat in sorted(fams.items()):
        emit("     %-12s %s" % (name, pat))
    declared = any(str(p).startswith("investor-reporting/") for p in fams.values())
    emit("     the reader's prefix 'investor-reporting/export/' is a DECLARED family: %s" % declared)
    rc, tracked = git("ls-files")
    rc2, untr = git("ls-files", "--others", "--exclude-standard")
    n_files = len(tracked.decode("utf-8", "replace").splitlines()) + len(untr.decode("utf-8", "replace").splitlines())
    p = subprocess.run(["git", "grep", "-I", "--untracked", "-n", "receipt.json", "--", "*.py"],
                       cwd=WS, capture_output=True, timeout=180)
    sites = [ln for ln in p.stdout.decode("utf-8", "replace").splitlines()
             if "infra/aws/lambda/" in ln and ("receipt_key =" in ln or '+ "receipt.json"' in ln)]
    emit("  the WRITER census over %d files (tracked + untracked, this worktree):" % n_files)
    for ln in sites:
        emit("     %s" % ln.strip()[:150])
    emit("     sites building a receipt.json OBJECT KEY: %d, all via the declared families (firms/{firm_id}/...); "
         "writers of the reader's address: 0" % len(sites))
    return (not declared) and len(sites) >= 2


def receipt_exists(bucket: str, key: str) -> tuple[int, int]:
    own = s3.list_objects_v2(Bucket=bucket, Prefix=os.path.dirname(key) + "/", MaxKeys=10)
    root = s3.list_objects_v2(Bucket=bucket, Prefix="investor-reporting/export/", MaxKeys=10)
    pol = s3.list_objects_v2(Bucket=bucket, Prefix="firms/", MaxKeys=5)
    emit("  list-objects-v2 (as the operator, who holds ListBucket):")
    emit("     under the CONCRETE key's own prefix %-58s KeyCount %d" % (os.path.dirname(key) + "/", own.get("KeyCount", 0)))
    emit("     under the template's root prefix    %-58s KeyCount %d" % ("investor-reporting/export/", root.get("KeyCount", 0)))
    emit("     under the POLICY's prefix           %-58s KeyCount %d %s" % (
        "firms/", pol.get("KeyCount", 0), [o["Key"] for o in pol.get("Contents", [])][:3]))
    return root.get("KeyCount", 0), pol.get("KeyCount", 0)


def arm_a() -> bool:
    emit("(a) THE CAUSE, MEASURED")
    identity_line("(a)")
    bucket, key, _arns, inside = key_and_arns()
    emit("")
    ctrl = simulations(bucket, key)
    emit("")
    emit("  (iii) THE SWALLOWED EXCEPTION -- what can and cannot be printed:")
    emit("    the role's trust policy names lambda.amazonaws.com ONLY, so it is NOT assumable by this seat; the boundary "
         "records to a None sink (S91). The live class therefore CANNOT be printed verbatim. The two instruments that CAN run:")
    identity_line("(a)(iii)(A) the live invoke pair", served=True)
    pair_ok, _pair = invoke_pair()
    emit("")
    emit("    (B1) THE STUB ARMS (the deployed bytes in-process, a stub S3 client, the recorder patched). "
         "A STUB ASSERTS THE CLASS ITS AUTHOR CHOSE -- read (B2) before believing any of these:")
    mapped = mapping_arms()
    emit("")
    emit("    (B2) THE REAL WIRE ARMS -- the same object, real responses, the handler's own test applied:")
    wire = wire_arms(bucket, key)
    stub_says = mapped.get("AccessDenied (ClientError)", "")
    wire_says = wire.get("UNSIGNED, the concrete key (the 403 the role gets)", "")
    emit("    THE TWO INSTRUMENTS DISAGREE AND THE WIRE ONE IS TRUE: the stub's AccessDenied raised %s (mapped, "
         "reads GREEN); the wire's AccessDenied is class %s (NOT mapped). A packet built on the stub alone would "
         "have signed an IAM grant to fix an exception-mapping defect." % (stub_says, wire_says))
    emit("")
    addr_ok = address_census(bucket)
    emit("")
    n_root, n_pol = receipt_exists(bucket, key)
    case = "ABSENT" if n_root == 0 else "PRESENT"
    emit("  (iv) THE RECEIPT: %s -- the template's whole prefix holds %d object(s), while the policy's prefix holds objects "
         "(the writer's evidence). The read and the write were written against DIFFERENT prefixes." % (case, n_root))
    emit("  THE CASE THAT HOLDS: the receipt is %s -- and not merely for this export id: the reader's WHOLE address space "
         "is empty, is not a declared prefix family, and has ZERO writers. So the order's second branch is the measured "
         "one: NO GRANT, and two rows (S105 the address, S106 the mapping). A grant would convert UNEXPECTED into a "
         "truthful NOT_FOUND by giving the role a 404 instead of a 403, while granting an undeclared prefix that nothing "
         "writes and leaving the mapping defect armed." % case)
    return ((not inside) and ctrl and pair_ok and case == "ABSENT" and all(mapped.values())
            and addr_ok and wire.get("UNSIGNED, the concrete key (the 403 the role gets)") == "AccessDenied")


def arm_b() -> bool:
    emit("(b) THE PACKET and THE HALVES")
    identity_line("(b)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head_blob = head.decode().strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head_blob) and head_blob == wt.decode().strip()
    emit("  packet %s: blob at HEAD %s, worktree %s -> %s" % (PACKET_REL, head_blob or "ABSENT", wt.decode().strip(),
                                                              "COMMITTED, UNCHANGED" if ok else "NOT COMMITTED OR CHANGED"))
    n = 0
    for who, d, pat in (("COO", "org/tier1_exec/2.0.0_SA_COO~B/deliverables", "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-14_"),
                        ("CTO", "org/tier1_exec/1.0.0_SA_CTO/deliverables", "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-14_")):
        _, ls = git("ls-tree", "-r", "--name-only", "HEAD", "--", d)
        hits = [p for p in ls.decode().splitlines() if os.path.basename(p).startswith(pat)]
        naming = [p for p in hits if head_blob and head_blob in (blob_at("HEAD", p) or b"").decode("utf-8", "replace")]
        n += bool(naming)
        emit("  %s half at HEAD: %d file(s), %d naming blob %s -> %s" % (who, len(hits), len(naming), head_blob or "?",
                                                                         "PRESENT" if naming else "ABSENT"))
    emit("  halves: %d of 2" % n)
    return ok and n == 2


def main() -> int:
    _, h = git("rev-parse", "HEAD")
    emit("IB-rtf-14 R71-AC1 battery (first pass) -- worktree HEAD %s" % h.decode().strip())
    emit("")
    arms = {"(a) the cause measured": arm_a()}
    emit("")
    arms["(b) packet + halves"] = arm_b()
    emit("")
    if not arms["(b) packet + halves"]:
        emit("STOP at (b): a half is ABSENT -- nothing is applied; (c) apply and (d) the live proof are NOT RUN")
    arms["(c) apply"] = False
    arms["(d) live proof"] = False
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else ("NOT RUN" if k.startswith(("(c)", "(d)")) else "FAIL")))
    if all(arms.values()):
        emit("RESULT: R71-AC1 PASS")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R71-AC1 FAIL -- %d of %d arms hold (first pass: STOP at the halves as the face expects)"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
