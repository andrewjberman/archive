"""IRPT_DASHBD TO-DB-b-318 (applier 0.7.0_AE_CloudOps~IB2): C0, the READ-ONLY trace of the Cottonwood Performance read path.

  python cotc0_318.py run                     steps 2 to 6: the two clients by label, the three probes, the existence heads, the authorizer, the function record
                                              -> state318/*.json (labels, statuses, reason tokens and booleans only)
  python cotc0_318.py compile <auth_location> <lists_firms:true|false>
                                              assemble COT_READ_C0_RECORD.json from state318/ (the authorizer's firm-handling location is read by hand)

Writes nothing to AWS. The client's ids, its display name and the staff identity live in memory only: nothing printed or written carries them.
"""
import base64
import datetime as dt
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.config import Config

HERE = Path(__file__).resolve().parent
STATE = HERE / "state318"
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(HERE)).strip())
sys.path.insert(0, str(ROOT))
from lib import opal_naming  # noqa: E402

REGION = "us-east-1"
FUNCTION = "irpt-49f-reporting-read-lambda"
ROUTE_KEY = "GET /api/scoped/investor-reporting/reporting/{account_id}/{which}"
API_ID, AUTHORIZER_ID = "7k3ed8px20", "naqxlm"
OWN_BUCKET = "opal-data-cottonwood"
OWN_KEYS = {"legacy": "platinum/cottonwood/ownership_map.json", "canonical": "advi/cottonwood/platinum/cottonwood/ownership_map.json"}
STAFF_EMAIL = "andrew@opalinvest.com"  # an ACTIVE internal users row with no allowedFirmIds narrowing (read before the probes); in memory only
APPLIER = "0.7.0_AE_CloudOps~IB2"
s3 = boto3.client("s3", region_name=REGION)
lam_cfg = boto3.client("lambda", region_name=REGION)
lam = boto3.client("lambda", region_name=REGION, config=Config(read_timeout=900, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"}))


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def ids_module():
    p = ROOT / "infra/aws/lambda/investor-reporting/_ids/ids.py"
    spec = importlib.util.spec_from_file_location("irpt_ids_c0", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def split_uri(uri):
    b, k = uri[len("s3://"):].split("/", 1)
    return b, k


def published(firm, ids):
    """({opaque account id: raw key}, sorted raw keys) of every published account= prefix, from one delimiter listing."""
    b, k = split_uri(opal_naming.address("irpt", firm, "platinum", "reporting", "account=0"))
    prefix = k.rsplit("account=", 1)[0]
    out, raws = {}, []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []):
            tail = c["Prefix"][len(prefix):].strip("/")
            if tail.startswith("account="):
                raw = tail[len("account="):]
                raws.append(raw)
                try:
                    out[ids.opaque_account(firm, raw)] = raw
                except ids.IdRefused:
                    pass
    return out, sorted(raws)


def directory(firm):
    reg = json.loads((ROOT / "data/firm_registry.json").read_text(encoding="utf-8"))
    buckets = [f["bucket"] for f in reg["firms"] if f.get("firm_id") == firm and f.get("enabled") and f.get("bucket")]
    assert len(buckets) == 1
    ptr = json.loads(s3.get_object(Bucket=buckets[0], Key="investor-reporting/directory/latest.json")["Body"].read())
    return json.loads(s3.get_object(Bucket=buckets[0], Key=ptr["key"])["Body"].read()), buckets[0]


def staff_headers():
    return {"x-user-email": STAFF_EMAIL, "x-user-name": "c0 trace", "x-user-tier": "admin", "x-user-role": "admin", "x-firm-id": "opal-capital", "x-user-type": "Dev",
            "x-origin-verify": "cloudfront", "X-Contract-Version": "v1"}


def probe(label, account_id, which, tenant):
    event = {"routeKey": ROUTE_KEY, "headers": staff_headers(), "pathParameters": {"account_id": account_id, "which": which}, "queryStringParameters": {"selected_tenant": tenant}}
    t = now_utc()
    resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", Payload=json.dumps(event).encode("utf-8"))
    raw = resp["Payload"].read()
    out = json.loads(raw.decode("utf-8"))
    hdrs = {str(k).lower(): v for k, v in (out.get("headers") or {}).items()} if isinstance(out, dict) else {}
    status = out.get("statusCode") if isinstance(out, dict) else None
    reason, bare = None, False
    if isinstance(out, dict) and status is None and "operation" in out and isinstance(out.get("status"), dict):
        # a BARE refusal envelope: the function returned it without a statusCode (API Gateway's payload 2.0 default for such a return is 200: INFERRED)
        bare, status = True, 200
        cand = out["status"].get("public_reason_code")
        reason = cand if isinstance(cand, str) and re.match(r"^[A-Z][A-Z0-9_]{2,40}$", cand) else None
    elif isinstance(out, dict) and isinstance(out.get("body"), str) and (status is not None and (status >= 400 or not out.get("isBase64Encoded"))):
        try:
            body = out["body"]
            if out.get("isBase64Encoded"):
                body = base64.b64decode(body).decode("utf-8", "replace")
            cand = (json.loads(body).get("status") or {}).get("public_reason_code")
            reason = cand if isinstance(cand, str) and re.match(r"^[A-Z][A-Z0-9_]{2,40}$", cand) else None
        except (ValueError, KeyError, AttributeError):
            reason = None
    rec = {"label": label, "method": "lambda-invoke", "status": int(status) if status is not None else -1, "reason_code": reason,
           "content_encoding": hdrs.get("content-encoding"), "invoked_utc": t, "request_id": resp["ResponseMetadata"]["RequestId"]}
    print("PROBE %s status=%s bare_envelope_no_statusCode=%s reason_code=%s content_encoding=%s function_error=%s request_id=%s" % (label, rec["status"], bare, reason, rec["content_encoding"], resp.get("FunctionError"), rec["request_id"]))
    return rec


def exists(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as ex:  # noqa: BLE001
        code = getattr(ex, "response", {}).get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        print("STOP: head_object answered %s, not a clean absence" % (code or type(ex).__name__))
        raise SystemExit(3)


def cmd_run():
    cfg0 = lam_cfg.get_function_configuration(FunctionName=FUNCTION)
    before = cfg0["CodeSha256"]
    bucket_map = sorted(json.loads((cfg0.get("Environment") or {}).get("Variables", {}).get("IRPT_DIRECTORY_BUCKET_MAP", "{}")))
    print("FUNCTION code_sha256_before=%s directory_bucket_map=%s" % (before, bucket_map))
    ids = ids_module()
    # step 2: the two clients by label (ids in memory only)
    cdir, cbucket = directory("cottonwood")
    ent = [e for e in cdir["entries"] if str(e.get("display_name", "")).strip().lower().startswith("thiessen")]
    print("STEP2 cottonwood directory entries=%d matching the client by name=%d (the name is never printed)" % (len(cdir["entries"]), len(ent)))
    assert len(ent) >= 1
    acct_ids = (ent[0].get("ids") or {}).get("account_ids") or []
    cpub, craws = published("cottonwood", ids)
    first = acct_ids[0]
    mapped = first in cpub
    print("STEP2 cottonwood-client-1: account ids in its entry=%d; its first id maps to a published account prefix=%s; published cottonwood accounts=%d" % (len(acct_ids), mapped, len(craws)))
    fpub, fraws = published("49financial", ids)
    ctrl_raw = fraws[0]
    ctrl_opaque = ids.opaque_account("49financial", ctrl_raw)
    print("STEP2 control-49f: published 49financial accounts=%d; first sorted account mapped to its opaque id (not printed)" % len(fraws))
    # step 3: the three probes
    probes = [probe("cottonwood-client-1-manifest", first, "manifest", "cottonwood"),
              probe("cottonwood-client-1-series", first, "series", "cottonwood"),
              probe("control-49f-manifest", ctrl_opaque, "manifest", "49financial")]
    # step 4: existence heads and the directory
    om = {"bucket": OWN_BUCKET, "legacy_key_exists": exists(OWN_BUCKET, OWN_KEYS["legacy"]), "canonical_key_exists": exists(OWN_BUCKET, OWN_KEYS["canonical"])}
    dr = {"latest_json_exists": True, "entry_count": len(cdir["entries"])}
    print("STEP4 ownership_map legacy_exists=%s canonical_exists=%s ; directory latest.json exists=%s entry_count=%d (directory bucket %s)" % (om["legacy_key_exists"], om["canonical_key_exists"], dr["latest_json_exists"], dr["entry_count"], cbucket))
    # step 5: the authorizer
    au = boto3.client("apigatewayv2", region_name=REGION).get_authorizer(ApiId=API_ID, AuthorizerId=AUTHORIZER_ID)
    uri = au.get("AuthorizerUri", "")
    m = re.search(r"function:([A-Za-z0-9_-]+)", uri)
    auth = {"authorizer_id": AUTHORIZER_ID, "type": au.get("AuthorizerType"), "function_name": m.group(1) if m else None}
    print("STEP5 authorizer id=%s type=%s function=%s" % (auth["authorizer_id"], auth["type"], auth["function_name"]))
    after = lam_cfg.get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]
    print("FUNCTION code_sha256_after=%s equal=%s" % (after, after == before))
    save("probes.json", probes)
    save("existence.json", {"ownership_map": om, "directory": dr, "directory_bucket": cbucket, "first_id_maps_to_published": mapped, "published_cottonwood_accounts": len(craws)})
    save("authorizer.json", auth)
    save("function.json", {"name": FUNCTION, "code_sha256_before": before, "code_sha256_after": after, "directory_bucket_map": bucket_map})
    return 0 if after == before and probes[2]["status"] == 200 else 3


def cmd_compile(location, lists):
    ex = load("existence.json")
    rec = {"claim": "measured", "applier": APPLIER, "no_write": True, "probes": load("probes.json"), "ownership_map": ex["ownership_map"], "directory": ex["directory"],
           "authorizer": dict(load("authorizer.json"), firm_handling_location=location, lists_firms=(lists == "true")), "function": load("function.json"),
           "notes": open(STATE / "notes.txt", encoding="ascii").read().strip(), "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "COT_READ_C0_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COT_READ_C0_RECORD.json")
    return 0


if __name__ == "__main__":
    sys.exit(cmd_run() if sys.argv[1] == "run" else cmd_compile(sys.argv[2], sys.argv[3]))
