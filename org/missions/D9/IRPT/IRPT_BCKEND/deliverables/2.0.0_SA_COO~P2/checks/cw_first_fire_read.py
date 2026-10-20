"""READ-ONLY. The issuer's read of the first scheduled Cottonwood fire after the retained-key release (TO IB-cw-6, packet NEVER_WIDEN_COTTONWOOD_RETAINED_KEY..., CTO msg 11103).

Prints COUNTS AND CLASS WORDS ONLY: no client key, no account id, no value. It never writes. Usage:
    python cw_first_fire_read.py <repo_root> <as_of YYYY-MM-DD> [<previous_as_of YYYY-MM-DD, default 2026-10-12>]

Reads, in order:
  1. latest.json: the served as-of date (did the fire land?)
  2. the fire's manifest (_refresh/<as_of>/manifest.json): reason code, the delta counts, whether a failure was recorded
  3. the new directory and the previous one: entry counts, how many previous keys are absent from the new directory, and how many of those
     have EVERY account id in ONE new entry (the re-keyed count); and whether any previous key is absent with an account in no new entry
  4. the CTO's added check: ONE re-keyed account's new client key -> the filled report address (lib/opal_naming.address) -> head_object: exists True/False
  5. the HMAC account-id list for cottonwood (hm5 leg L6): head_object only: exists and LastModified
"""
import json
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
AS_OF = sys.argv[2]
PREV = sys.argv[3] if len(sys.argv) > 3 else "2026-10-12"
sys.path.insert(0, str(REPO))
import boto3  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402

BUCKET = "opal-data-cot"
DPFX = "investor-reporting/directory"
s3 = boto3.client("s3", region_name="us-east-1")


def get_json(bucket, key):
    try:
        return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    except ClientError as exc:
        return {"__error__": (exc.response.get("Error") or {}).get("Code", "ERR")}


def head(bucket, key):
    try:
        h = s3.head_object(Bucket=bucket, Key=key)
        return {"exists": True, "last_modified": str(h.get("LastModified")), "bytes": h.get("ContentLength")}
    except ClientError as exc:
        return {"exists": False, "code": (exc.response.get("Error") or {}).get("Code", "ERR")}


def acc_sets(entries):
    out = {}
    for e in entries:
        ids = e.get("ids") or {}
        k = ids.get("client_id") or ids.get("relationship_id") or ""
        if k:
            out.setdefault(k, set()).update(str(a) for a in (ids.get("account_ids") or []))
    return out


latest = get_json(BUCKET, DPFX + "/latest.json")
print("latest.json as_of:", latest.get("as_of_business_date", latest.get("__error__")), "| wanted as_of:", AS_OF)
man = get_json(BUCKET, "%s/_refresh/%s/manifest.json" % (DPFX, AS_OF))
if "__error__" in man:
    print("manifest for %s: ABSENT (%s)" % (AS_OF, man["__error__"]))
else:
    d = man.get("delta") or {}
    print("manifest: reason", man.get("reason_code"), "| status", man.get("status"), "| delta", json.dumps({k: d.get(k) for k in ("added", "disappeared", "eligibility_changed", "terminated_count", "build_dispatch", "redispatched", "failed_command_id") if k in d}),
          "| failure keys", sorted(k for k in d if k.startswith("build_")))
new = get_json(BUCKET, "%s/%s/directory.json" % (DPFX, AS_OF))
old = get_json(BUCKET, "%s/%s/directory.json" % (DPFX, PREV))
if "__error__" in new or "__error__" in old:
    print("directory read: new", new.get("__error__", "ok"), "| previous", old.get("__error__", "ok"))
    sys.exit(0)
ne, oe = new.get("entries") or [], old.get("entries") or []
ns, os_ = acc_sets(ne), acc_sets(oe)
absent = [k for k in os_ if k not in ns]
rekeyed = [k for k in absent if os_[k] and any(os_[k] <= s for s in ns.values())]
lost = [k for k in absent if k not in rekeyed and any(v for v in [os_[k]])]
print("entries: new", len(ne), "previous", len(oe), "| previous keys absent from new", len(absent), "| re-keyed (every account in ONE new entry)", len(rekeyed), "| absent and NOT re-keyed", len(lost))
rk_new = None
if rekeyed:
    first = sorted(rekeyed)[0]
    for k, s in ns.items():
        if os_[first] <= s:
            rk_new = k
            break
if rk_new is None:
    print("filled-report check: no re-keyed account to test")
else:
    try:
        from lib import opal_naming
        uri = opal_naming.address("irpt", "cottonwood", "platinum", "reporting", "client=%s" % rk_new, "filled_report.json")
        _s, _, b, k = uri.split("/", 3)
        h = head(b, k)
        print("filled-report check: ONE re-keyed account's NEW key -> filled_report.json exists:", h.get("exists"), "| code", h.get("code", "-"))
    except Exception as exc:  # noqa: BLE001 -- the class only
        print("filled-report check: address builder refused (%s)" % type(exc).__name__)
hm = head("opal-data-assets", "globgrph/cottonwood/silver/account_id_list/hmac")
print("HMAC list (hm5 leg L6): exists", hm.get("exists"), "| last_modified", hm.get("last_modified", "-"), "| bytes", hm.get("bytes", "-"), "| code", hm.get("code", "-"))
