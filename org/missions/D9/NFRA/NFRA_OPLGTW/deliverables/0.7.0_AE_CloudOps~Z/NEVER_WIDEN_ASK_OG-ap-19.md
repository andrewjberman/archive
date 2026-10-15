# NEVER-WIDEN ASK -- OG-ap-19: the eight G3 portal tools, the five G6 news tools, and their two read grants

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-19` at A1.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 29 of 29 tests pass; the targeted plan reads 2 to add.

| | |
|---|---|
| **release** | `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` on `rel-nfra-oplgtw-g36` |
| **base** | `047f11aa991e5c7ed188876f07a8599447cf2849` -- OG-ap-18's release, read live THREE ways |
| **ledger** | `nfra-oplgtw-gateway-release-g36` (Phase B; not opened) |
| **plan** | `W/G36_PLAN.txt` -- 2 to add, 0 to change, 0 to destroy |

## 0. READ THIS FIRST: one file is outside the order's take-list, and without it nothing imports

**RULED: amendment A2 `@68a7d83f97` takes route (a) -- `app/typed_scope.py` rides this release whole,
and the cut `ee23dd004c` stands unchanged.** `ap19.AC1` now reads `outside the G3-G6 set 0 (want 0)` and
**RESULT: PASS**; the COO half is signed at this `release_sha` (`@bcc91e7a86`). The paragraphs below are
kept as the reason, because the halves still signing should see why the file is here.

**`app/typed_scope.py`.** The order named it **nowhere** (0 mentions). `portal_models.py:33` does
`from . import typed_scope as ts`, and all three taken modules reference it -- `portal_models` 3,
`portal_macro` 3, `news_typed` 4. `app/tools.py` imports `portal_models` at start-up, so **the release
as originally listed would not have let the service come back.**

I took the file, because a half should rule on a release that works rather than one that cannot
start. It is one pure seam module, 8,093 bytes, introduced by `e6f3b2b1b7` (cell `OG-gt-6`, "the scope
seam over harvest_typed"), and it imports only `harvest_read` and `harvest_typed` -- both already live,
shipped by OG-ap-18 -- so taking it pulls in no further dependency.

**Why the gap existed and was invisible.** OG-ap-18 excluded `typed_scope.py` deliberately and was
RIGHT to: none of its five modules imports it (0 references each). Its own ask even listed the file as
absent, which made the exclusion look settled rather than pending. A take-list enumerates the files
*this release's cells* wrote and the files the hookup touched; a seam an EARLIER cell wrote, that these
modules were later built on, is invisible to such a list. Row `NFRA_OPLGTW-Z-S137`. Two routes: amend
the take-list (recommended -- it is tested at 29 of 29 with the file in), or let `OG-gt-6` ship its seam
first and re-cut this order on that release.

This is the same shape as `Z-S130` one order ago, and **the order's own host-shaped import check is what
caught it** -- the first run of the six suites read 4 errors and 2 failures, every one this single cause.

## 1. The `diff`, by file -- 16 files

| file | +/- | taken |
|---|---|---|
| `app/portal_models.py` | +~380 | whole, box/sitez -- the four G3 market/positioning readers |
| `app/portal_macro.py` | +~376 | whole -- macro, valuation, security scan, pipeline freshness |
| `app/news_typed.py` | +~586 | whole -- the five G6 news readers |
| **`app/typed_scope.py`** | **+172** | **whole -- the seam; added by A2's ruling, see section 0** |
| `tests/test_og_pt1.py` `pt2` `nw1` `gt10` | +~1,500 | whole, four files |
| `app/tools.py` | +81 | by hunk, `4500d443a0` -- the thirteen registrations + the import line |
| `app/destructive_ops.py` | +13 | by hunk -- the thirteen into `SAFE_TOOLS` |
| `app/data_entitlement.py` | +13 | by hunk -- the thirteen into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | +2 -2 | by hunk -- `registered_tool_names` **75 -> 88** |
| `tests/test_data_entitlement_family.py` | +3 -3 | by hunk -- `non_data` **66 -> 79** |
| `deploy-to-ec2.sh` | +1 -1 | by hunk -- the **three** `NEWS_*` `.env` keys only |
| `infra/aws/terraform/.../news_read_iam.tf` | new | G6 grant, unchanged, merged `21073a6055` |
| `infra/aws/terraform/.../portal_tiered_read_iam.tf` | new | G3 grant, my `530b3a3246` |

**THE SEAM IS TWO FILES AND THIS RELEASE TAKES ONE** (A2). Cell `OG-gt-6` (`e6f3b2b1b7`) wrote
`app/typed_scope.py` (172 lines) **and** `tests/test_og_gt6.py` (205 lines). A2 rules the test NOT
required, and the release does not take it -- the cut `ee23dd004c` is signed at that sha and adding a
file would move it and void a signed half, so the tree stands exactly as signed.

**The seam's own suite was still RUN, as evidence rather than as a take:** `tests/test_og_gt6.py`
checked out into the release worktree *uncommitted* reads **4 passed** against the very
`typed_scope.py` this release ships, then removed, leaving the worktree byte-identical to
`ee23dd004c`. So the module this release absorbs is covered by its author's own suite at 33 of 33 over
seven suites, without the release carrying a file A2 did not ask for. `tests/` is not an artifact
member either way, so nothing about the host changes on this point.

**The two pins were re-derived against this base, not taken from trunk.** The base reads 75 and 66, so
this release is **88 and 79**. Trunk HEAD reads **95 and 86** because work landed after the hookup, so
taking trunk's bytes for those two files would have pinned **twenty** extra tools in a release that adds
thirteen. The hookup `4500d443a0` sets exactly 88 and 79 and its pre-image is 66/75 -- the same base as
mine -- so its hunks are correct here and were applied as hunks, never as whole files.

**The `.env` hunk took a decision worth naming.** `c1f02c8f63`'s post-image adds **four** keys, not
three: `AMGT_SCOPED_API_FUNCTION` plus the three `NEWS_*` tables. AMGT is absent from this base (another
cell's key) and the order's list names only the three NEWS keys, so the 3-way conflict was resolved to
OURS plus the three, and AMGT was left out. Asserted after resolving: each NEWS key appears once, AMGT
appears zero times, ap-18's `lib/trading_calendar.py` staging survives intact, `bash -n` clean.

## 2. The thirteen `tools`, their class, and what they answer `refused`

Eight G3, all READ, `SAFE` in `destructive_ops`, `legacy` class in `data_entitlement` (`NATIVE_TOOLS`):
`portal_get_model_positioning`, `portal_get_model_attribution`, `portal_get_market_returns`,
`portal_get_market_regime`, `portal_get_macro`, `portal_get_valuation`, `portal_get_security_scan`,
`portal_get_pipeline_freshness`.

Five G6, same class: `news_search_articles`, `news_trending_topics`, `news_keyword_intelligence`,
`news_market_mood`, `news_for_security`.

Each admits **before any read**, through the same `typed_scope`/`harvest_typed` seam OG-hv-1 put live: a
principal, then `tools._is_opal_user`, then the served-prefix (G3) or table (G6) test. So each inherits
`principal_required`, `harvest_opal_only` and the prefix refusal, and adds `harvest_bad_argument`,
`harvest_over_cap`, `harvest_read_failed` and `harvest_unreadable`. **A non-Opal caller is refused all
thirteen.** `OG-pt-3`'s `mdpf_get_category_views` is SUPERSEDED and rides `NFRA_MCPINDEX`; it is not here.

## 3. The `widening`, stated plainly -- this is the half that matters

**Two grants, two different principals, and that distinction is the thing to sign.**

| | principal | gains |
|---|---|---|
| **G3** | `gateway-global-internal-reader-role` -- the role that *assumes* and makes the S3 call | `s3:GetObject` on **one** prefix: `arn:aws:s3:::opal-data-portal-v2/json-tiered/market-overview/*` |
| **G6** | `opal-gateway-role` -- the gateway instance role itself | `dynamodb:Query` and `dynamodb:GetItem` on `opal-news-articles`, `opal-news-trending-daily`, `opal-keyword-intelligence` and that table's `date-index` |

**The G3 resource list is COMPUTED, not typed**, which is why the order asked for a generator
(`W/g36_grant_gen.py`). It reads `portal_models.py` and `portal_macro.py` **by AST** -- module-level
string and string-tuple assignments only, no import, so no module-level code runs -- collects every
prefix those modules read, subtracts every prefix the existing grant already covers, and collapses the
remainder to its minimal covering set:

> **12** prefixes the code reads -> **9** already covered by the existing `json/*` grant -> **3** residue
> -> **1** after collapse, because `json-tiered/market-overview/` already covers `.../summary/` and
> `.../timeseries/`. The collapse is *asserted*: the generator refuses if any dropped prefix lacks a
> covering kept one, so it changes the diff and never the reach.

**Three readings of the bucket had to agree** before the generator would emit anything, because a grant
on a bucket the code does not read passes every static check and fails only at runtime: the code's own
`PORTAL_BUCKET`, the naming registry's bucket for scope `global`, and the bucket the **live** existing
policy already names. All three read `opal-data-portal-v2`. It also requires the existing grant's
`Resource` list to be identical in `mcpmsp_internal_reader.tf` **and** in live IAM, so the subtraction is
never computed against a fiction; both read `json/` and `platinum/`.

**What the data is, named:** market returns and timeseries, market regime and its history, model
positioning and holdings attribution, macro series, valuation and risk premium, the security scanner's
universes and factor metadata, the pipeline manifest -- and, on the news side, article text and
sentiment, trending topics and keyword intelligence. **Opal principals only**, for all thirteen.

**What does NOT change:** the ALB `authenticate-oidc` default action, GuardMiddleware, any route, the
internal reader's trust policy, the existing `json/*` and `platinum/*` statements, every other `.env`
key, and the ten G1 tools OG-ap-18 put live. No `*` resource, no Put, no Delete, no `ListBucket`.
**Who loses: nobody.** Both grants are additive.

The **third** widening, smaller and stated in section 0: `app/typed_scope.py` lands on the host. It is a
pure seam over `harvest_typed` with no network and no credentials of its own.

## 4. The `order` of acts -- both grants, then the deploy

1. Ledger `nfra-oplgtw-gateway-release-g36`, entry AND sentinel first.
2. The two policies through `safe-apply`, **targeted, ONE at a time**, each read back from IAM with
   `get-role-policy` before the next. The grants go FIRST so no request can run the new code without the
   permission it needs -- the ordering OG-hv-2's A5 established.
3. The deploy from `C:/tmp/og-rel-g36` under the A1 guard (deploy tree HEAD == the signed `release_sha`
   in full, its parent == live `deployed_commit` at the act). No `HALT_OVERRIDE`.
4. Read back the triggers, then the served read of all thirteen.

**The legacy address row landed first and on its own**, as the CTO ruling (msg 34173) requires -- written
by `4.0.0_SA_CRO~Z` at `bb0e3bd764`, because `infra/logic/**` is lane `PLATFORM_LOGIC_DOCS` and not mine
(row `Z-S136`). `lib/opal_naming.legacy_address("gateway-portal-tiered-market-overview")` resolves to
`s3://opal-data-portal-v2/json-tiered/market-overview/`.

## 5. `Both branches` of a call

| branch | what happens | evidence |
|---|---|---|
| **refused** | the admission answers before any read, so **zero S3 and zero DynamoDB calls** | the shared seam runs first in every tool; OG-ap-18 measured `s3_calls_on_refusal 0` for all ten of its tools with a counter in place of the client, and Phase B measures the same for these thirteen |
| **admitted** | the read is **capped on the body itself** and the output **projected to 50 KB**, carrying `truncated` and `projected_to_bytes` | `app/harvest_typed.py` + the `typed_scope` seam |

Every answer carries `as_of`, `source_keys`, `denominator`, `absent_reason`, so an empty answer says why
instead of reading as "no such data".

## 6. The `rollback`

Each policy is destroyed through `safe-apply`, targeted, by name:
`aws_iam_role_policy.portal_tiered_read` and `aws_iam_role_policy.gw_news_read`. Those two names are the
only keys these acts create; the internal reader's pre-existing `gateway-global-internal-reader-policy`
is a **different name** and must not be touched.

The binary rolls back by redeploying `047f11aa99` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`.
Complete, not a hope: that ref's parity with the host was measured at **113 of 113** across `app/`,
`deploy/` and `lib/` at this cut. A rollback leaves `/opt/opal-gateway/lib/` in place (OG-ap-18's
member, which the base reads) and removes `typed_scope.py` along with the thirteen tools.

**One rollback caveat, carried forward from `Z-S133`:** the `/yearinreview` page's served bytes follow
whichever tree performs a deploy, so pick the rollback tree deliberately. This release ships the page in
the LF form `3bbd5ab2` that OG-ap-18 established under A8's route (a); a clean checkout of `047f11aa99`
ships the same form, so a rollback from a clean tree is byte-stable for that page.

## 7. The `triggers` Phase B reads back

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` | `{"ok":true}` |
| registry **+13** | the app's own registry; `registry_before` is **56**, re-read on the live host | **56 -> 69** |
| the three `NEWS_*` key NAMES | key NAMES only, never a value; absent today (measured: 0) | all three present |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/`, `lib/` vs `ee23dd004c` | all equal |
| **both policies live in IAM** | `get-role-policy` per policy, read back one at a time | both present, each with exactly its own statement |
| all thirteen served | an Opal stand-in principal's real call, enveloped answer | 13 of 13 |
| all thirteen refused | a non-Opal principal, with a counter in place of the client | 13 of 13 `harvest_opal_only`, **0 reads on any refusal path** |

In the release tree these already read: **33 of 33 tests pass** over seven suites (pt1 4, pt2 5, nw1 5,
**gt6 4**, gt10 2, entitlement_admin 9, data_entitlement_family 4 -- gt6 run as evidence, not taken),
and the **host-shaped import check** reads 5 of 5 modules importing at exactly **4 parents** -- and the
five are named, because A2 asks for the seam to appear in the check explicitly: **`app.typed_scope`**,
`app.portal_models`, `app.portal_macro`, `app.news_typed` and `app.tools`, each resolving at 4 parents,
with `app.typed_scope` imported FIRST so a failure in the seam cannot be mistaken for a failure in the
modules built on it -- the host's own depth, where OG-ap-18 v1's `parents[5]`
was fatal -- with all thirteen tools in the registry the module itself builds, 0 missing, the tree's
registry reading **69 = 56 + 13**, and `portal_models._calendar()` RESOLVING, which exercises OG-gt-10's
fix (the portal modules find the staged calendar by search rather than a fixed index).

Any trigger failing: redeploy the base, destroy the two grants this ask adds, and file an ARMED row
naming `2.0.0_SA_COO~O`.

## 8. What is NOT asked

No new bucket. No new table. No `*` resource. No write of any kind -- both grants are read-only. No
route, no ALB change, no GuardMiddleware change, no `.env` key beyond the three `NEWS_*` names, no
catalog edit, no object written to any data bucket, no vendor call, no schedule or trigger created or
changed. `mdpf_get_category_views` (`OG-pt-3`) is superseded and absent. `AMGT_SCOPED_API_FUNCTION` was
deliberately not taken. And no deploy or apply until all three halves are signed at this `release_sha`
**and** section 0's `typed_scope.py` question is ruled.
