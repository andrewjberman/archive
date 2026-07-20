# MDPF_REVAMP -- publish + re-point IMPLEMENTATION package (reference code + IAM/trigger plan)

**Author:** 0.2.0_DT_PortfolioAnalytics · **Date:** 2026-07-20 · **To:** 1.0.0_SA_CTO (code review + write-IAM plan-gate), 0.7.0_AE_CloudOps (commit + apply the opal-assets / lambda-edge infra)
**Design parents:** DT plan @0da51a8c9, router design @c4af27f0e (s3 CONFIRMED, IN-ALL, OAC; CTO 205634Z). **Nothing applies until the co-signed cutover.**

## LANE SPLIT (why this is a DT deliverable, not a DT commit)
The owned-paths hook blocks DT from `infra/aws/*` -- that is the AE (CloudOps) lane (opal-assets + lambda-edge; DT's own infra lane is yang-pipeline only). So, mirroring the router split CTO set ("DT authors, AE applies"): **DT authors the reference code + the IAM/trigger design (this doc); AE commits it into the opal-assets / lambda-edge TF + applies at the CTO-gated, Andrew-co-signed cutover.** DT owns the design + the CF-serving/parity decisions; AE owns the apply.

---

## 1. PUBLISH producer -- `opal-assets-mdpf-portal-publisher` (reference, AE commits to infra/aws/lambda/opal-assets/)
Staging `gold/mdpf_revamp/{seg}/{name}.json` (DS lane) -> `portal/*` (DT/AE lane) via same-bucket server-side copy. Explicit 9-key IN-ALL map (no derive -> no mis-route). Listing-based landing verify (never HeadObject). `all_present` = the machine-checkable cutover-precondition signal.

```python
from __future__ import annotations
import datetime as dt
import os
import boto3

BUCKET = os.environ.get("ASSETS_BUCKET", "opal-data-assets")
STAGING_ROOT = os.environ.get("STAGING_ROOT", "gold/mdpf_revamp")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")

# (segment, name) -> portal key.  IN-ALL (CTO Q1): 3 firm timeseries + 2 firm distributions + 4 global portfolios.
PUBLISH_MAP = {
    ("global", "aggregate_aua_timeseries"): "portal/model-portfolios/global/aggregate_aua_timeseries.json",
    ("49financial", "aggregate_aua_timeseries"): "portal/model-portfolios/49financial/aggregate_aua_timeseries.json",
    ("inflection", "aggregate_aua_timeseries"): "portal/model-portfolios/inflection/aggregate_aua_timeseries.json",
    ("49financial", "account_distribution"): "portal/model-portfolios/49financial/account_distribution.json",
    ("inflection", "account_distribution"): "portal/model-portfolios/inflection/account_distribution.json",
    ("global", "non_model_assets"): "portal/portfolios/global/non_model_assets.json",
    ("global", "aum_metrics"): "portal/portfolios/global/aum_metrics.json",
    ("global", "aum_timeseries"): "portal/portfolios/global/aum_timeseries.json",
    ("global", "account_distribution"): "portal/portfolios/global/account_distribution.json",
}

def _log(msg):
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def _list_one(s3, key):
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=key, MaxKeys=1)
    for obj in resp.get("Contents", []):
        if obj["Key"] == key:
            return obj
    return None

def _publish_one(s3, segment, name, portal_key):
    src_key = f"{STAGING_ROOT}/{segment}/{name}.json"
    try:  # AE-C hardening: one key's failure must not crash the run or lose all_present
        src = _list_one(s3, src_key)
        if src is None:
            _log(f"MISSING: staged source absent {src_key} -> {portal_key} NOT published")
            return {"portal_key": portal_key, "status": "missing_source", "published": False}
        s3.copy_object(Bucket=BUCKET, Key=portal_key,
                       CopySource={"Bucket": BUCKET, "Key": src_key}, MetadataDirective="COPY")
        dst = _list_one(s3, portal_key)
        if dst is None:
            return {"portal_key": portal_key, "status": "verify_absent", "published": False}
        if dst["Size"] != src["Size"]:
            _log(f"ERROR: size mismatch {portal_key} dst={dst['Size']} src={src['Size']}")
            return {"portal_key": portal_key, "status": "size_mismatch", "published": False}
        _log(f"OK: published {src_key} -> {portal_key} ({dst['Size']:,}B, etag_match={dst.get('ETag')==src.get('ETag')})")
        return {"portal_key": portal_key, "status": "published", "published": True, "size": dst["Size"]}
    except Exception as e:  # per-key error status; run still reports all_present + the full map
        _log(f"ERROR: publish {src_key} -> {portal_key} raised {type(e).__name__}: {e}")
        return {"portal_key": portal_key, "status": "error", "published": False, "error": str(e)}

def lambda_handler(event, context):
    s3 = boto3.client("s3", region_name=S3_REGION)
    results = [_publish_one(s3, seg, name, pk) for (seg, name), pk in PUBLISH_MAP.items()]
    missing = [r for r in results if not r["published"]]
    all_present = len(missing) == 0
    _log(f"SUMMARY: published {len(results)-len(missing)}/{len(PUBLISH_MAP)}; all_present={all_present}; "
         f"missing={[r['portal_key'] for r in missing]}")
    return {"all_present": all_present, "published_count": len(results)-len(missing),
            "total": len(PUBLISH_MAP), "missing": [r["portal_key"] for r in missing], "results": results}
```

## 2. RE-POINT translation router -- `mdpf-data-router` (Lambda@Edge origin-request; AE commits to infra/aws/lambda-edge/, publishes a us-east-1 numbered VERSION)
Associated ONLY with the new MDPF-family behaviors (origin = opal-data-assets). URI translation ONLY -- origin is set by the CF behavior, NOT here. `public-data-router` byte-unchanged.

```javascript
// Lambda@Edge origin-request. No env vars (Lambda@Edge). Translate /api/general/... -> /portal/... key.
const MDPF_FIRMS = new Set(['global', '49financial', 'inflection']);
const DIST_FIRMS = new Set(['49financial', 'inflection']);      // account-distribution: no mdpf/global
const PORTFOLIOS = {
  '/api/general/portfolios/non_model_assets.json': '/portal/portfolios/global/non_model_assets.json',
  '/api/general/portfolios/aum-metrics.json': '/portal/portfolios/global/aum_metrics.json',
  '/api/general/portfolios/aum-timeseries.json': '/portal/portfolios/global/aum_timeseries.json',
  '/api/general/portfolios/account-distribution.json': '/portal/portfolios/global/account_distribution.json',
};
export const handler = async (event) => {
  const request = event.Records[0].cf.request;
  const uri = request.uri;
  let m;
  m = uri.match(/^\/api\/general\/mdpf\/([^/]+)\/aggregate-aua-timeseries\.json$/);
  if (m && MDPF_FIRMS.has(m[1])) { request.uri = `/portal/model-portfolios/${m[1]}/aggregate_aua_timeseries.json`; return request; }
  m = uri.match(/^\/api\/general\/mdpf\/([^/]+)\/account-distribution\.json$/);
  if (m && DIST_FIRMS.has(m[1])) { request.uri = `/portal/model-portfolios/${m[1]}/account_distribution.json`; return request; }
  if (PORTFOLIOS[uri]) { request.uri = PORTFOLIOS[uri]; return request; }
  return request;   // unmatched: URI unchanged. Exact-match behaviors => unreachable; wildcard => 404 from origin (safe, no mis-route)
};
```

## 3. WRITE-IAM plans (CTO plan-gate; AE applies; 22a at apply)
**3a. Publisher role `opal-assets-mdpf-portal-publisher-role`** (least-privilege, copy needs GetObject src + PutObject dst):
- `s3:GetObject` on `opal-data-assets/gold/mdpf_revamp/*`
- `s3:PutObject` on `opal-data-assets/portal/model-portfolios/*` + `opal-data-assets/portal/portfolios/global/*`
- `s3:ListBucket` on `opal-data-assets` Condition prefix `["gold/mdpf_revamp/*","portal/*"]` (the listing-based verify)
- AES256 default SSE on opal-data-assets (no KMS/SSE header). NEVER a source layer (bronze/silver), NEVER bd/schwab, NEVER cross-firm.
- **22a AT APPLY (live simulate, ONE --resource-arns each, positive controls SEPARATE):** PutObject portal/model-portfolios/49financial/aggregate_aua_timeseries.json -> ALLOW; PutObject portal/portfolios/global/aum_metrics.json -> ALLOW; GetObject gold/mdpf_revamp/49financial/account_distribution.json -> ALLOW; PutObject bronze/... -> implicitDeny; PutObject silver/... -> implicitDeny; GetObject schwab/... -> implicitDeny; PutObject opal-data-cot/... -> explicitDeny (fence). comp-iam is NOT sufficient (fails GREEN on new (action,resource)); the live simulate is the instrument.
  **AE apply-discipline folds (0.7.0_AE 210705Z, BINDING at apply):** (A) the conditioned ListBucket (Condition s3:prefix) MUST be simulated WITH `--context-entries s3:prefix=gold/mdpf_revamp/...` AND `=portal/...` -- without them it returns implicitDeny byte-identical to a real deny (the smartx conditioned-ListBucket class), so the grant reads untested/self-denied. (B) the simulate proves the GRANT, not that CopyObject LANDS under the live bucket policy (the 17a deny + AES256-default; the code sets no SSE header) -- so AE EXERCISES a real publish (or the DS-pinged first run) + verifies portal/* via ListObjectsV2 = desired+applied+EXERCISED, never simulate-only.

**3b. Router role `mdpf-data-router-role`** (Lambda@Edge): trust `lambda.amazonaws.com` + `edgelambda.amazonaws.com` (replication); `AWSLambdaBasicExecutionRole` (logs) ONLY. NO S3 perms -- CF fetches from origin via OAC, the lambda only rewrites URIs.

**3c. CF serving (AE, per router design s3e):** opal-data-assets 2nd origin + `aws_cloudfront_origin_access_control` (type=s3, signing_behavior=always, sigv4) + a PURE-ADD bucket-policy statement (principal cloudfront.amazonaws.com, GetObject on portal/*, Condition SourceArn=<dist ARN>) -- never clobber the existing Rule-17a bronze/.parquet deny.

## 4. Behavior set + the MINIMIZE-check result (grounded)
`comp-grep portal/src` for `/api/general/portfolios/`: it carries EXACTLY the 4 MDPF-page keys (aum-metrics, aum-timeseries, non_model_assets, account-distribution) -- NO other traffic. So a `/api/general/portfolios/*` wildcard is feasible (=> 2 behaviors w/ a `/api/general/mdpf/*` wildcard). **BUT** with the quota now confirmed 75 (25 used, ~50 headroom -- AE 205531Z), count is NOT pressured, so I **recommend EXACT-MATCH (9 behaviors -> 34 total)** for orphan-404 safety (the mdpf/* wildcard would 404 the unused root /api/general/mdpf/aggregate-aua-timeseries.json; exact-match can't) + no future-key coupling. 2-wildcard is the minimal-footprint alternative -- **CTO's call.** Each behavior: viewer-request auth-validator-edge (HARD REQ), origin opal-data-assets, origin-request mdpf-data-router (published version ARN), origin-response cache-control-injector; inserted ABOVE behavior 18 (ordered precedence).

## 5. PUBLISH TRIGGER (no new alarms -- Andrew)
Build-alongside: on-demand invoke (DS pings after staging) is enough for the parity streak. Steady-state: an EventBridge schedule sequenced AFTER the DS gold run (mirrors the emitter's cron pattern, pure-add rule) -- exact cron TBD on the gold cadence. NO S3-notification trigger on opal-data-assets (adding a notification modifies the shared bucket notification config -> violates new-territory "no modifying notification-configs"; the schedule/invoke path is the pure-add).

## 6. PARITY HARNESS (DT owns the wiring; CVO adjudicates)
Compares each PUBLISHED portal/ artifact to its OWN served counterpart (never cross-artifact -- account_distribution keys by_model on DISPLAY NAME, aggregate on MODEL_KEY; both match their served, DS 205851Z -- do NOT normalize). Bar: shape/field-inventory identical (audit L21-22) + latest cross-section ties within tolerance; the F2 ~$4.1M + the two count denominators + the two non-model numbers reproduced distinctly (baseline doc). **NO historical byte-diff on aggregate_aua_timeseries model_aua[]/custody[]/non_model[] pending Andrew D1/D2** (measured-vs-backfill) -- history carried as a named delta. **TO-3 account_distribution is DECISION-INDEPENDENT + parity-final NOW** (DS a511dabbb: unfunded 34 EXACT, min EXACT, std within $0.71) -> it can be wired + parity-checked fully ahead of the aggregate history. N=3 consecutive cycles -> never-widen co-sign (CTO+Andrew) -> re-point.

## 7. Sequencing to cutover
1. DS wires `--upload` -> staging populated (TO-3 now parity-final; aggregate history post-D1/D2). 2. AE commits+applies (CTO-gated) the publisher + its IAM (build-alongside populates portal/*). 3. Parity streak N=3 (TO-3 first; aggregate after D1/D2). 4. AE commits+publishes mdpf-data-router (us-east-1 version) + the origin/OAC/policy + the behaviors (held un-live). 5. Cutover precondition green (publisher all_present + parity N=3). 6. Never-widen co-sign (CTO+Andrew) -> AE associates the behaviors ABOVE 18 -> shadow one cycle -> legacy retires.
