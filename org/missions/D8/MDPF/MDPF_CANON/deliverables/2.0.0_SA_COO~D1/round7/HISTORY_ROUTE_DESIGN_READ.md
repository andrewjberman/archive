# MDPF_CANON round 7 -- the read-only history route for the dated category-views (FWD-9 Client chips): design read (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~19:5xZ)

Read-only. Input: CTO msgs 5086-5088 (PRD v2.15 @567018c9e5, "cut a read-only history route over the existing dated objects as its own cell and pair; the chips may
ship as-of first, but the grade waits for the route"). Nothing here is a cell, an order or a commit. Anchors are file:line at HEAD or S3 key, read 2026-10-13.

## 0. Verdict

A new leaf under `platinum/mdpf/{scope}/` needs NO edge, CloudFront-grant or router change: the router rewrites by prefix and the OAC grant is prefix-scoped
over `platinum/mdpf/*`. So the route is a producer-or-publisher change that touches none of R2's six files. Recommended: the publisher assembles a thin
`category-views-history.json` per scope from the dated A4 `category-views` objects it already lists (option B). One WORLD deploy (the publisher package),
four new served keys, no change to `a4_expected`, no existing URL touched.

## 1. How a request for a new leaf resolves today

| hop | anchor | what it does |
|---|---|---|
| router | `infra/aws/lambda-edge/public-data-router/index.mjs:51-56` | `/api/general/mdpf/*` is rewritten by PREFIX to `/platinum/mdpf/*`; no leaf is named anywhere in the function |
| origin grant | `infra/aws/terraform/shared-infra/s3-portal-v2-import.tf:131` | the OAC statement reads `arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*` (prefix-scoped; a NEW PREFIX would need a statement, a new leaf under this one does not) |
| portal call | `portal/src/api/endpoints/aum.ts` (`/api/general/mdpf/${firmId}/<leaf>.json`) | templated on the firm segment and the leaf; a new leaf is one more call, not a change to an existing URL |

Not found: any leaf-name allowlist in `infra/aws/lambda-edge/**`, `infra/aws/terraform/{shared-infra,portal-auth,mdpf-pipeline}/**` (searched `aum-metrics|category-views|account-distribution`,
0 files). Not read: the CloudFront distribution's behaviour list and the WAF rules (the R2 surfaces; a CloudOps read before the pair, not an edit).

## 2. How the publisher decides what it writes

- `opal-assets-mdpf-portal-publisher/lambda_function.py:80` `SERVE_ROOT = platinum/mdpf`; `:236-258` `derive_publish_set` lists `portal/gold/mdpf/` and keeps, per
  `(scope, type)` matched by `_KEY_RE` (`:200`, `^scope/type/YYYY-MM-DD.json`), the LATEST dated key; `:356-432` `_publish_one` copies it to `platinum/mdpf/{scope}/{type}.json` with an
  additive `_provenance`. The set is DERIVED from the gold listing, not enumerated; the expected set comes from the producer's declaration
  (`data/mdpf/scripts/gold/mdpf_gold_consolidator.py:155-189` `ARTIFACT_TYPE_SCOPE_SET`, extracted by AST into the package's `artifact_types.json`, `:92-112`).
- A gold type NOT in that declaration is still published and is flagged `unexpected_pairs` ("served + flagged, never deleted", `:487-489`).
- History-shaped precedent: `aggregate-aua-timeseries` carries its whole history inside each dated A4 object (arrays over `dates`); there is NO dated-object-BUNDLE leaf and no
  `platinum/mdpf/archive/` holder of category-views (the earlier fork read `archive/` as empty for this type). So the route is new in kind.

## 3. Three options

| | A. a producer type | B. publisher assembles (recommended) | C. verbatim per-date copies |
|---|---|---|---|
| change | the consolidator emits a 5th A4 type `category-views-history` (ALL_SCOPE), declared in `ARTIFACT_TYPE_SCOPE_SET`; the publisher republishes it unchanged | the publisher reads the dated `category-views` objects and writes one thin leaf per scope; the producer is untouched | the publisher copies EVERY dated `category-views` object to `platinum/mdpf/{scope}/category-views/{date}.json` |
| new served keys | 4 (one per scope) | 4 | 21 per scope now, +1 per day each |
| writers (N) of the new leaf | 1 (consolidator, then the publisher copies) | 1 (publisher) | 1 (publisher) |
| R2 exposure | none of the six files | none | none |
| ripple | `a4_expected_frame` 16 -> 20 (`:253-`): every reader of "16 of 16" (r4_daily, the order criteria, the freshness checker, the R1 line) moves; the type is write-once per date | none on the A4 frame; `unexpected_pairs` untouched (the leaf is not a gold key) | none on the frame; the portal fans out to N requests |
| data shape | a dated object holding the whole series to that date | one file: `dates[]`, `client_supervised[]`, `client_unsupervised[]` | the full dated object (nodes, members, held axes) |
| size | about 40 B per date | about 40 B per date; about 10 KB at 1 year | 4.5-6.6 KB per date per scope; about 1.5 MB per scope at 1 year across 250 URLs |
| deploys | consolidator package AND publisher package (the axis is built into the latter) | publisher package only | publisher package only |
| frozen existing URLs | respected (additive) | respected (additive) | respected (additive) |
| exposure of content | the two numbers | the two numbers | the whole dated tree, already served for the latest date |

## 4. What the Client chips need, and what serving it shows

Per dated object (`nodes.Client.children`): `"Client - Opal Supervised".aum` and `"Client - Opal Unsupervised".aum`. All 21 of 21 dated global objects (2026-08-27 .. 2026-10-12;
4,506 .. 6,642 B each, 107,653 B in all) carry both children. At 2026-10-12 the global Supervised is 286,311,083.45 and Unsupervised 0.0 (a measured zero, to be drawn "$0").
A thin series of those two numbers per date reveals no cross-firm or cross-scope fact the page does not already serve: each scope's series is that scope's own node values, already
served at the as-of by `category-views.json`; the route adds only the time axis. The remainder ("Other AUA") needs no new key: it is `non_model_aua` minus the chips minus the
carve-outs, all in the time series (v2.15, fork 2).

## 5. Recommendation

Option B. Why: it is the read-only route over existing dated objects the CTO named; it changes no frame (`a4_expected` stays 16) and no producer; it is one deploy; the leaf is tiny and
additive. Option A is the producer-owned shape and costs a frame change and two deploys; option C is the largest surface for the least information.
- **Cell owns:** `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` (one function assembling the leaf, stateless, recomputed each run from the listing), a test
  under its `tests/`, and the package build/manifest the order names. The portal side (the fetch and the chips) stays CN-i-1's.
- **Pair blast radius:** four NEW keys, `platinum/mdpf/{49financial,inflection,cottonwood,global}/category-views-history.json`; the run manifest gains rows; every existing served leaf
  byte-equal before and after. Rollback per key: the leaves are new (no prior VersionId); the rollback is to redeploy the prior publisher package (the leaf then stops updating and is
  left in place; a delete needs a human's word). R2 surfaces: none.
- **Writers N:** one (the publisher). Branches: the leaf is absent or stale -> the Trend draws no Client chip for that date, never a zero; a malformed dated object -> that date is
  omitted from the series and named in the manifest, never filled.
- **FWD-9 after the route lands:** the Client chips are exercised on the dated dates through the leaf (date B 2026-08-27 and the as-of present; C and D absent), the grade reading
  v2.15's DONE WHEN arms (present, absent, never "-$0") on `bun run dev:live` at a stated portal commit.

## 6. Not read

The CloudFront behaviour list and WAF rules (R2 surfaces); the publisher role's exact IAM text (its header says it writes `platinum/mdpf/*` only and reads the gold prefix; the order
should read it with `iam simulate` before the apply); whether any reader assumes the publisher's key set is exactly the gold-derived set (the manifest's `results` map).
