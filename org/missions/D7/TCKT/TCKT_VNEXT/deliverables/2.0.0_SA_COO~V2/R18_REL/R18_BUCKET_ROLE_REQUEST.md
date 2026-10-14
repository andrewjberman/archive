# TCKT_VNEXT round 18 -- ROLE REQUEST to the laptop: let the ticket API's role presign trade-form uploads in three firm buckets

**From:** `2.0.0_SA_COO~V2` (dell2), 2026-10-14. **To:** the laptop (via `0.0.0_AB_MSTR~DELL2`). **Why a request:** a Dell writes no bucket policy (PRD v0.6 C-DEPLOY,
NFRA_CTLPLN). **Needed for:** FWD-10 (Trade Request form upload, due 2026-10-24). **Not asked:** any new bucket, any other prefix, any other principal.

## What is being built (so the request is checkable)

The ticket API (Lambda `opal-ticket-api`, role `arn:aws:iam::313476888478:role/opal-ticket-api-role`) issues 300-second presigned PUT and GET URLs for a trade request
form (PDF, XLSX or CSV, at most 10 MB) that an Opal staff person uploads from the portal for a CHOSEN firm. Per doctrine R21 (`infra/logic/02_DOCTRINE.md:588`) and the
builder (`lib/opal_naming.py address()`, record `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json` on branch `wk-TCKT_VNEXT-43` @2e0b4b59f8), each firm's
objects live in that firm's own bucket:

| firm | bucket | the only prefix |
|---|---|---|
| 49financial | `opal-data-49financial` | `portal/49financial/state/ticket_attachments/trade-form/` |
| inflection | `opal-data-inflection` | `portal/inflection/state/ticket_attachments/trade-form/` |
| cottonwood | `opal-data-cottonwood` | `portal/cottonwood/state/ticket_attachments/trade-form/` |

The role's own IAM grant (Terraform source `TO-R18-TR3`, applied by the release order) is exactly `s3:PutObject` and `s3:GetObject` on those three ARNs, nothing else.

## What I READ (read-only, 2026-10-14 ~19:5xZ; the vintage, not the world now)

- All three buckets exist (`head-object`-class read: `head-bucket` rc 0). None has a CORS configuration (`NoSuchCORSConfiguration` on all three).
- Each bucket policy carries `DenyForeignFirmPrincipals`: `Deny` `s3:*` to every principal whose ARN is NOT LIKE the policy's list (`*-49f-*`, `*-inf-*`, `*-cot-*` and named roles
  and users). `opal-ticket-api-role` is on none of the three lists, so an IAM Allow alone would be refused by this explicit Deny. `opal-data-inflection` already shows the shape
  for a narrowly scoped exempt principal (`irpt-performance-adapter-role`: the `DenyScopedExemption1*` statements limit it to one action set and one prefix).

## What is requested, per bucket (three buckets, the same three changes)

1. **Exempt the role from `DenyForeignFirmPrincipals`** by adding `arn:aws:iam::313476888478:role/opal-ticket-api-role` to its `ArnNotLike` list.
2. **Bound it at once**, in the pattern of `DenyScopedExemption1*`: add Deny statements so that this role may do ONLY `s3:GetObject` and `s3:PutObject`, ONLY on
   `arn:aws:s3:::<bucket>/portal/<firm>/state/ticket_attachments/trade-form/*`, and may not `s3:ListBucket` (the presigned flow needs no listing). No other prefix in the bucket may be
   reachable by this role, including the cottonwood restricted prefix.
3. **CORS** (for the browser's PUT to a presigned URL): `AllowedOrigins` = the portal's DEV and PROD origins exactly (NO `*`), `AllowedMethods` `PUT` and `GET`,
   `AllowedHeaders` `Content-Type`, `ExposeHeaders` `ETag`, `MaxAgeSeconds` 300. The laptop knows the portal's origins; I do not type them here.

## What the release reads back (acceptance)

Before the release order applies the Terraform source, it reads `get-bucket-policy` and `get-bucket-cors` on EACH of the three buckets and stops if any one lacks the exemption, the
bounds or the CORS. Please answer with the three policy documents' statement ids and the CORS rule as applied (a read-back, not a claim), and say if any bucket already had a
change that made one of the three items unnecessary.

## Bounds and sign-off

This widens WHO may touch three client-confidential firm buckets (by one role, two actions, one prefix each). It is the laptop's change under its own never-widen sign-off; the
dell2 release pair names it as a precondition and does not substitute for it. Nothing here moves served output. The only data the role will ever write is a placeholder trade form
for a synthetic run, then real forms filed by Opal staff.
