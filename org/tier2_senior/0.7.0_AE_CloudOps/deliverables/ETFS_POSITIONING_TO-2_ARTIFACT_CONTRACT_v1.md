# ETFS_POSITIONING TO-2 Half 1 -- ROUTE DECISION + ARTIFACT CONTRACT v1.2

> **v1.2 (2026-08-24) -- NORMATIVE UNITS SECTION ADDED. If you are here about `weight`, read
> "⛔ UNITS" in PART 2 and nothing else: `holdings[].weight` is a FRACTION (0..1), `allocation` and
> `management` are PERCENT (0..100). DO NOT CONVERT `weight` — pass it through.**

**Owner:** `0.7.0_AE_CloudOps` | **TO:** `ETFS_POSITIONING.TO-2` | **Cells:** `ETFS-e-1`, `ETFS-e-2`
**decomp_ref:** `workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md`
**Status of the decomp this derives from:** UNCERTIFIED ON ITS FACE (issuer-disclosed, COO 65669).
**Consumers:** `0.4.0_DS_ClientPlatform`-class (TO-1, producer) + `0.4.0_DE_ClientPlatform` (TO-3, portal reader).
**Build against this. It does not wait for the artifact to exist.**

---

## PART 1 -- THE ROUTE DECISION (`ETFS-e-1`, AC1 + AC5)

### DECIDED: `platinum/etfs/` on `opal-data-portal-v2`, served at `/api/general/etfs/*`

| | value |
|---|---|
| **Served URL** | `/api/general/etfs/positioning_data.json` |
| **S3 key** | `s3://opal-data-portal-v2/platinum/etfs/positioning_data.json` |
| **CloudFront behavior** | `/api/general/*` (#20) -- **EXISTING, unchanged** |
| **Origin** | `S3-opal-data-portal-v2-json`, OAC `E24L6358YRRKAE` -- **EXISTING, unchanged** |
| **Auth** | `auth-validator-edge` (viewer-request) -- **EXISTING, unchanged** |
| **New router branch** | `/api/general/etfs/` -> `/platinum/etfs/` in `public-data-router` |
| **New bucket-policy ARN** | `arn:aws:s3:::opal-data-portal-v2/platinum/etfs/*` added to `AllowCloudFrontOACPublicData` (+ the advi restore, Amendment C) |
| **Pin drop (v1.1)** | `qualified_arn` removed from `public_data_router.ignore_changes`, `lambda-edge.tf:197` -- **without this the branch publishes a version CloudFront never serves** |

### AC5 -- IS THE CF PATH CLASS A MINT? **YES. IT IS A MINT, AND A MINT IS NOT A GAP.**

`comp-routes behaviors` (DESIRED plane per its own provenance header; parsed
`cloudfront-distribution.tf` + committed `index.mjs`, never a live `describe-distribution`) returns
**ZERO** matches for `etf` across all 27 behaviors. No ETF path class exists on the portal-v2
distribution today. **This is a MINT -- a thing not yet built, not a defect and not a coverage
hole in the instrument.**

**But the mint is SMALL, and naming its true size is the point of this section:** no new CloudFront
behavior, no new origin, no new OAC. `/api/general/*` already claims the path.

**THE MINT IS THREE EDITS (v1.1 -- v1.0 said two and undercounted; see the correction at item 4):**
1. a `public-data-router` branch `/api/general/etfs/` -> `/platinum/etfs/` (mdpf-shaped);
2. the bucket-policy Resource ARN for `platinum/etfs/*` -- **plus the `AllowAdvisorRouterOAIPlatinumAdvi`
   restore in the same edit** (TO-2 Amendment C: that statement is live but managed by no TF resource,
   so any `shared-infra` apply without it deletes a live serving grant);
3. **drop `qualified_arn` from `public_data_router`'s `ignore_changes`** at `lambda-edge.tf:197`,
   in the same commit as edit 1 -- without it, edit 1 publishes a version CloudFront never serves.

**Plus one verification step that no plan can substitute for:** read the LIVE distribution's
association ARN after the apply.

### The comp-routes evidence (PRD s.11.4(e) requires it)

1. **There is no `/api/general/positioning/*` behavior at all.** Positioning rides the `/api/general/*`
   catch-all (behavior #20) -> `S3-opal-data-portal-v2-json`. `comp-routes trace` resolves
   `/api/general/positioning/positioning_data.json` -> `s3://opal-data-portal-v2/json/positioning/positioning_data.json`.
2. **SOURCE-CONFIRMED mechanism:** `infra/aws/lambda-edge/public-data-router/index.mjs:42-46`
   @`6f1f242a6a` (2026-07-28T21:08:05-04:00) -- default branch `/api/general/` -> `/json/`.
   Line 9 names it outright: *"fallback - covers positioning, cma, etc."*
3. **THE PRECEDENT IS EXACT AND ALREADY EXERCISED:** `index.mjs:36-40` --
   `/api/general/mdpf/` -> `/platinum/mdpf/` (WO-3 re-point, v6 2026-07-29), a prefix-disjoint
   branch ahead of the default. The ETF branch is that shape, ~5 lines.
4. ⛔ **CORRECTED IN v1.1 -- THE EDIT DOES *NOT* TAKE EFFECT BY ITSELF.**
   *v1.0 said: "`comp-routes edge-versions` -- `public-data-router` is DYNAMIC / `qualified_arn`
   [OK], so it auto-updates on `safe-apply`. No version pin blocks it." **That was FALSE**, and
   false in the direction that ships a silently non-working route.*
   **SOURCE-CONFIRMED:** `infra/aws/terraform/portal-auth/lambda-edge.tf:197` --
   `aws_lambda_function.public_data_router` carries **`ignore_changes = [qualified_arn,
   source_code_hash]`**. It is one of exactly THREE still pinned (`auth-validator-edge` :96,
   `cache-control-injector` :151, `public-data-router` :197); `shared_advisor_router` :244 was
   fixed and carries only `source_code_hash`.
   **Consequence, verbatim from that file's header at :36-37:** *"Apply publishes a NEW Lambda
   version and CloudFront KEEPS SERVING THE OLD ONE."*
   **And the instrument I cited is documented as blind to exactly this** (`:44-47`):
   *"`comp-routes edge-versions` does NOT catch it: it reports these as 'DYNAMIC -- auto-update on
   terraform apply [OK]' ... **Do not read that [OK] as evidence an edge moved.**"* The pin passes
   every rung of Rule 22a at once -- clean plan, genuine 0-diff re-plan, a real new version, and a
   route running GREEN on the old code.
   **REMEDY (the file's own, `:54-58`):** drop `qualified_arn` from that function's
   `ignore_changes` **in the same commit as the branch**, and **CONFIRM THE LIVE ASSOCIATION
   VERSION AFTER APPLY** by reading the live distribution -- per `:42-43` that live read is the
   ONLY instrument that catches it. **A 0-diff re-plan is the SYMPTOM here, not the reassurance.**
5. **`opal-data-etfs` is NOT a CloudFront origin** -- 0 of 7 enumerated. That candidate would have
   required a full origin + OAC + behavior mint. COO removed it on independent grounds (below);
   this is the third, and it agrees.

### Why NOT the surviving alternative (`json/positioning/` family)

It is genuinely cheaper -- **zero** route work and **zero** bucket-policy work, because the default
branch already resolves and the OAC statement already carries `json/*`. **I am rejecting it anyway,
on two grounds:**

1. **It shares the LIVE Models prefix.** PRD s.11.1 makes *"Models mode byte-identical"* sovereign.
   COO ruled (65669) the ETF artifact is a separate FILE for that reason. Putting that separate file
   in the **same prefix** keeps a new producer writing into the tree Models mode serves from --
   byte-identity then rests on the producer's key list being correct, which is **discipline, not
   construction**. A separate prefix makes prefix-level collision *inexpressible*.
   **Care is not a control.**
2. **Rule 17b.** Serving-shaped work lives in `platinum/`. `json/positioning/` is a pre-17b legacy
   serving prefix; `platinum/mdpf/` is the ruled direction and the migration precedent. Landing new
   serving output in `json/` in 2026-08 adds to the tree 17b retires.

**Cost of the decision:** one router branch + one bucket-policy Resource ARN + a prefix-scoped
writer role. All single-apply, all rollback-in-window.

### AC6 -- `opal-data-etfs/platinum/` IS UNTOUCHED

`s3://opal-data-etfs/platinum/etf_ownership_dashboard.json` re-measured live at pickup:
**6,408 B, `LastModified 2026-08-21T16:00:04Z`** (s3api, UTC plane -- not `s3 ls`, which renders
local with no marker). Byte-identical to COO's measurement. It is ETFS_CANON's LIVE serving
artifact; ETFS_CANON is PRD s.11.4(h), declared OUT OF SCOPE.
**NOTHING in this contract writes, moves, or deletes anything under `opal-data-etfs/`.** Its
non-canonical placement is a pre-existing ETFS_CANON condition -- **surfaced, not chased**
(Rule 17b ratified-direction clause).

---

## PART 2 -- THE ARTIFACT CONTRACT (`ETFS-e-2`, AC2 + AC3)

### AC3 -- WHAT THIS PROJECT DOES NOT WRITE. Stated first because it is the sovereign constraint.

> **`json/positioning/positioning_data.json` IS NOT WRITTEN BY THIS PROJECT.**
> Nor is `model.json`, `allocation_summary.json`, or `holdings_attribution_data.json`.
> **No byte under `s3://opal-data-portal-v2/json/positioning/` changes as a result of
> ETFS_POSITIONING.** Models mode reads exactly the bytes it reads today, from exactly the
> producer that writes them today (`yang-generate-positioning` /
> `yang-generate-allocation-summary` / `yang-generate-holdings-attribution`).
> **Models-mode byte-identity is true BY CONSTRUCTION here: the ETF producer has no grant to
> that prefix and no key in it.** (The IAM half enforces this -- see Part 3.)

### The key

```
URL : /api/general/etfs/positioning_data.json
S3  : s3://opal-data-portal-v2/platinum/etfs/positioning_data.json
```

ONE artifact carrying all four books -- mirroring how Models mode carries five models in one file
(8,111 B live). DE's reader is then symmetric with `getPositioningData`, different endpoint.

### ⛔ UNITS (v1.2 -- NORMATIVE. Read this before the shape; it is the part v1.0/v1.1 got wrong.)

| field group | unit | range | invariant |
|---|---|---|---|
| `holdings[].weight` | **FRACTION** | `0..1` | the book's rows sum to **1.0** |
| `allocation{}` | **PERCENT** | `0..100` | the group sums to **100** |
| `management{}` | **PERCENT** | `0..100` | the group sums to **100** |
| `returns{}` | **PERCENT** | signed | per-period, not cumulative |

**Yes, that is mixed within one artifact, and it is mixed DELIBERATELY: it is the estate's existing
live convention, not a choice made here.** The authority is the artifact the *same Positioning
component* already renders correctly for real clients —
`s3://opal-data-portal-v2/json/positioning/positioning_data.json`, book `UST`: `holdings[0]` VGSH
`weight = 0.1451` with the rows summing to **1.0000** in **both** the A-form and B-form blocks, while
`allocation` carries `fixed_income: 100.0`. **The ETF artifact matches it exactly** (measured on the
live object, `generated_at 2026-08-21T21:25:52Z`: PFDE NVDA `0.0995`, 90 rows summing to `0.9999`,
`allocation.equity 99.64`).

> ⛔ **CONSUMERS: DO NOT CONVERT `weight`. PASS IT THROUGH.** The page already renders Models from
> fraction weights. A percent→fraction conversion in the adapter divides `0.0995` by 100 and renders
> NVDA at `0.0995%` instead of `9.95%` — **100x too small, and plausible-looking on any book whose
> largest position is under 10%, so nobody catches it by eye.**

> ⛔ **WHY v1.0/v1.1 WERE WRONG, stated because the mechanism generalises past this contract:** they
> never wrote the unit in words. They showed `"weight": 4.31` in the skeleton — an *example*, and
> therefore a **silent PERCENT specification**, because an example value is the only unit statement a
> reader gets. **AN UNLABELLED EXAMPLE VALUE IN A DATA CONTRACT IS A UNIT SPECIFICATION.** DE read
> v1.1 correctly and built the conversion it implied; two seats then corrected one 100x error from
> opposite ends and nearly shipped the double-fix. The grounding that settles it — the live Models
> artifact — was one read away when this contract was authored and I did not take it.

### The shape -- mirrors PRD s.4, B-form holdings

s.4.3 is explicit that the B-form (`current_holdings`) is *"the richer one, and the one an ETF book
must match."* This contract uses **B-form field names for holdings**. **Every numeric field below
carries the unit declared in the UNITS table above — read it there, not off the example values.**

```json
{
  "generated_at": "2026-08-22T07:14:03Z",
  "data_as_of":   "2026-08-21",
  "data_date":    "2026-08-21",
  "note":         "<free text, may be empty>",
  "portfolios": {
    "PFDE": {
      "code": "PFDE",
      "name": "<fund name>",
      "data_as_of": "2026-08-21",
      "prior_date": "2026-08-20",
      "holdings_status": "full",
      "num_holdings": 90,
      "aum": 123456789.0,
      "allocation":      { "cash": 0.0, "fixed_income": 0.0, "equity": 100.0, "hedge": 0.0 },
      "management":      { "active": 100.0, "passive": 0.0 },
      "characteristics": { "yield": null, "cost": null, "duration": null, "beta": null },
      "segment": {
        "sector":    { "<ETF-DECLARED VOCAB -- DS's Rule-24 act>": 0.0 },
        "geography": { "US": 0.0, "International": 0.0, "Other": 0.0, "Emerging": 0.0 }
      },
      "holdings": [
        {
          "ticker": "AAPL",
          "name": "Apple Inc",
          "asset_class": "Equity",
          "sub_asset_class": "<ETF-DECLARED VOCAB -- DS's Rule-24 act>",
          "weight": 0.0431,        // FRACTION, not percent -- see UNITS
          "fee": null, "aum": null, "yield": null, "duration": null,
          "credit": null, "beta": null, "active": true,
          "returns": { "1D": null, "WTD": null, "MTD": null, "1M": null,
                       "QTD": null, "1Q": null, "YTD": null, "1Y": null }
        }
      ]
    },
    "PFOE": { "...": "same shape as PFDE, holdings_status = full" },
    "DIVZ": {
      "code": "DIVZ", "name": "<fund name>",
      "data_as_of": "2026-08-21", "prior_date": "2026-08-20",
      "holdings_status": "book_only",
      "num_holdings": 0,
      "aum": 12345678.0,
      "allocation": { "...": 0.0 }, "management": { "...": 0.0 },
      "characteristics": { "yield": null, "cost": null, "duration": null, "beta": null },
      "segment": { "...": {} },
      "holdings": []
    },
    "IDVZ": { "...": "same shape as DIVZ, holdings_status = book_only" }
  }
}
```

### The four books and the two shells -- how "upgrading forward" works BY CONSTRUCTION

Ship shape is Andrew's (PRD s.10.4): **2 FULL (PFDE, PFOE) + 2 SHELLS (DIVZ, IDVZ)**.

**All four books appear in `portfolios` with the SAME key set.** A shell is not a missing entry and
not a different shape -- it is the same object with `holdings: []` and `holdings_status: "book_only"`.

> **WHY THE EXPLICIT `holdings_status` FIELD AND NOT JUST `holdings.length === 0`:**
> an empty array from a **designed shell** and an empty array from a **producer that failed to emit
> rows** are byte-identical. Inferring the state from emptiness makes a producer bug render as a
> normal shell -- silently, on a client-facing page. The explicit field makes the two discriminable,
> and lets DE fail loud on the third state (`"full"` with `holdings: []` = a defect, not a shell).

**Upgrade path, no code change at either end:** when TrueShares constituent rows land, the producer
fills `holdings[]` and flips `holdings_status` to `"full"`. DE renders the holdings table on
`holdings_status === "full"`. Neither side ships anything to upgrade a shell.

**Rule-24 four-postulate test on `holdings_status`** (a 2-value enum -- minting one is an authoring
act and carries the test):
- **MECE** -- `full` | `book_only` are mutually exclusive and collectively exhaust "does this book
  carry constituent rows".
- **SAME GRAIN** -- both are book-level properties of one book.
- **INTENT COHERENCE** -- one axis: constituent-row availability. It does not encode handling policy
  or freshness.
- **STATE COHERENCE** -- ONE remedy (TrueShares constituent capture landing) moves every
  `book_only` member to `full` together. DIVZ and IDVZ move on the same remedy. **Passes.**

### VOCABULARY -- NOT MINTED HERE. This is DS's Rule-24 act, deliberately left open.

PRD s.4.4 flags the hazard precisely: the model books hold **ETFs**, an ETF book holds **single
securities**, so `sub_asset_class` on a stock is a **GICS-style sector**, not a duration bucket --
**two grains on one axis** if the model vocabulary is reused.

**This contract fixes the FIELD NAMES (`asset_class`, `sub_asset_class`, `segment.sector`) and
explicitly does NOT fix their VALUES.** The ETF vocabulary is a separate declared enum and it is
the producer cell's Rule-24 authoring act (PRD s.10.5 L3 note). **DS: do not reuse the 10-value
model `sub_asset_class` vocabulary.** DE: treat these as opaque strings for rendering; do not
switch on specific values.

### Freshness / as-of

- `data_as_of` and `data_date` -- the **BDay(-1) trading-day** the content describes. **NEVER#1:
  T-1 logic lives in the producer, never in a cron, never wall-clock.**
- `generated_at` -- ISO8601 **UTC with a `Z`** produced by a UTC-native call, never a local
  formatter with a hand-typed `Z`.
- `prior_date` per book -- the prior trading day the deltas are measured against.
- **Production content comes from the SCHEDULED `bbg/{date}/` landing** (first fire 2026-08-22
  07:00 local site Z). `bbg-testpull/` is the frozen QA reference; `bbg/2026-08-20/` is ad-hoc
  output in the production prefix and is **build-time evidence only, never production evidence**
  (CTO 65615, Andrew's ad-hoc rule).

### Consumer-discovery limitation, carried per decomp L-3

Publish-layer S3 keys are the **~11% generative class**: only ~11% of in-scope key call sites NAME
their key (1 of 112 in the publish/serving layer). **A token census will not find the consumers of
this key.** This contract does not rest on one, and neither should any later sweep that asks
"who reads this?".

---

## PART 3 -- IAM (`ETFS-e-3`, AC4) -- SHAPE STATED, VERIFICATION PENDING

Half 2 is not complete. What is already grounded, and what is still to run:

### GROUNDED NOW -- the live bucket policy (APPLIED plane, read this session)

`aws s3api get-bucket-policy --bucket opal-data-portal-v2`: **THREE statements.** The one that
authorizes this serving path -- `AllowCloudFrontOACPublicData` (Service `cloudfront.amazonaws.com`,
`AWS:SourceArn` = distribution `EVTSA9VEHNZVH`) -- is **PREFIX-SCOPED** to exactly:

```
arn:aws:s3:::opal-data-portal-v2/json/*
arn:aws:s3:::opal-data-portal-v2/json-tiered/*
arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/*
```

**`platinum/etfs/*` IS NOT COVERED.** Without adding it, CloudFront gets **403** -- and the CF
custom-error rules mask JSON errors as HTML, so it surfaces as a confusing HTML 403 rather than a
clean one. The bucket-wide grant that exists (`opal-data-portal-v2/*`) sits on OAI
`EU39UXW7CMSI5`, which fronts a **different bucket** and is never the signer on this path.
`platinum/advi/*` needed its own third statement -- a second confirming precedent.

> **STALE RECORD, SURFACED NOT CHASED:**
> `infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf:46-48` states *"measured 2026-07-28:
> 2 statements, both Allow/GetObject for CloudFront."* The ZERO-Denys half is still true; the
> **count and the read scope are 24d stale**. A reader inheriting that line concludes a new
> platinum prefix is CloudFront-readable. **It is not.** Filed to CVO's channel as
> OBSERVATION/INERT; not edited by me (outside any cell I hold).

### TO RUN -- and the discipline is written into the cell, not left to the seat

- **`comp-iam` is a FLOOR, never a verdict** -- it models `(action)`, never `(action, resource)`.
  It will report `GRANTED` for `s3:GetObject` on a prefix that 403s. **Silence is the defect; never
  a deletion warrant.**
- `aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action>
  --resource-arns <ONE exact key>`.
- **ONE `--resource-arns` per call** -- 2+ flips the held ones to `implicitDeny`.
- **Positive control in a SEPARATE invocation** -- the multi-ARN mode silently disarms the very
  control being leaned on.
- **NEVER** `simulate-principal-policy` to test whether an action NAME is real (a nonexistent action
  returns `implicitDeny`, indistinguishable from a missing grant). Discriminating oracle:
  `aws accessanalyzer validate-policy`.
- `--context-entries` for any conditioned statement -- the OAC statement **is** conditioned
  (`AWS:SourceArn`), so this one bites here specifically.

### The writer, and the NEVER#3 question it raises

The producer needs `s3:PutObject` on `arn:aws:s3:::opal-data-portal-v2/platinum/etfs/*`,
**prefix-scoped, never the parent** -- the `advi-49f-publisher-platinum-put` /
`mdpf_egress_publisher` pattern.

**NEVER#3 flag, raised now rather than at apply time:** `mdpf_egress_publisher.tf:79-105` treats a
first automated writer onto a LIVE SERVED portal-v2 prefix as never-widen (CTO+COO), gated behind
`var.mdpf_egress_live_serve_write_cosigned`, and that paper is **scoped `platinum/mdpf/*` ONLY**.
`platinum/etfs/` is a **NEW, not-yet-served** prefix with no consumers and no live page, so my read
is that the first write CREATES a serve rather than moving one, and NEVER#3's "never move served
output" does not bite. **I am not self-certifying that.** COO/CTO: if you read it the other way,
say so before the apply -- it changes Half 2's paperwork, not its design, and it is cheaper to
answer now than at the gate.

---

## WHAT DS AND DE CAN START ON RIGHT NOW

- **DS (TO-1, producer):** write to `s3://opal-data-portal-v2/platinum/etfs/positioning_data.json`.
  Shape above. Four books in `portfolios`, B-form holdings, `holdings_status` per book. The ETF
  `sub_asset_class` / `segment.sector` vocabulary is **yours to declare** with the four-postulate
  test -- do not reuse the model vocabulary. Nulls are fine and expected (s.4.3 measured the live
  page rendering with `credit` 77/110 null, `beta` 59/110, `duration` 55/110).
- **DE (TO-3, portal reader):** fetch `/api/general/etfs/positioning_data.json`. Response shape is
  `portfolios: Record<string, PositioningPortfolio>`-compatible at the top level. Render the
  holdings table on `holdings_status === "full"`; a book with `"book_only"` renders book-level only.
  **Do not add ETF keys to `getPositioningData`** -- separate endpoint, separate artifact
  (COO ruling 65669).
- **The URL will 403 until Half 2 lands.** That is expected and is not a DE defect. Build against
  the shape; the route goes live with the bucket-policy ARN + router branch.

---

**v1.1. Half 1 (`ETFS-e-1` + `ETFS-e-2`) COMPLETE at this document. Half 2 (`ETFS-e-3`) IN PROGRESS.**

**v1.1 CHANGELOG (2026-08-21, author's own correction).** One change, and nothing a consumer builds
against moved: the edge-version claim at item 4 was **FALSE** and is corrected -- `public-data-router`
IS pinned (`lambda-edge.tf:197`), so the mint is **three edits, not two**, and the post-apply
live-association read is mandatory. **The route decision, the key, the URL, the shape,
`holdings_status`, the vocabulary boundary and AC3 are all UNCHANGED. DS and DE: nothing here
changes your build.** Root cause, stated plainly: I cited `comp-routes edge-versions`' `[OK]` as
evidence an edge would move, when the file governing that surface -- written the same day, by my own
lane, out of P4R-3 -- says in terms *"Do not read that [OK] as evidence an edge moved."* The tool's
blind spot was documented; I had not read the documentation for the surface I was standing on.
Plane discipline: route topology + rewrite = **DESIRED** (parsed TF + committed `.mjs`); bucket
policy + object vintages = **APPLIED** (live primitives). **Nothing here is EXERCISED** -- no ETF
path has been fetched, because none exists yet. The exercised fetch belongs to Half 2's close.
