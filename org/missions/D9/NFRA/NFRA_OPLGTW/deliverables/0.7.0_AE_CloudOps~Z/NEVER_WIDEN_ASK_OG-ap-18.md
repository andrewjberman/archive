# NEVER-WIDEN ASK -- OG-ap-18: the ten G1 typed harvest tools (v2, re-cut on gt-8 and gt-9)

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-18` at A4/A5 (`@b6075b276d`).
**NOTHING IS DEPLOYED.** `ap18.AC1` PASS; 49 of 51 tests pass and the 2 that do not are named in full below.

| | |
|---|---|
| **release** | `7521aee72528ca4d1d5ec811e11af74a0153faa2` on `rel-nfra-oplgtw-gt2` |
| **base** | `bacec95ccd6cafd2201f7433af24ae2748732355` -- re-read at this cut and still live |
| **supersedes** | `4275edccad` -- **it could not have started on the host** |
| **ledger** | `nfra-oplgtw-gateway-release-gt` (Phase B; never opened for v1) |

**Why there is a v2 at all.** The signed v1 indexed `Path(__file__).resolve().parents[5]` in
`harvest_identity.py`; `/opt/opal-gateway/app/` has 4 parents, so the import would have raised
`IndexError` and `tools.py` imports it -- the service would not have come back. Nothing was deployed and
the ledger was never opened. The three signed halves do **not** carry (C3 of each): this ask is new.

## 1. The `diff`, by file -- 18 files, and `lib/` becomes a NEW artifact member

| file | +/- | taken |
|---|---|---|
| `app/harvest_identity.py` | +532 | whole, gt-8 -- **the safe calendar root** |
| `app/harvest_press.py` | +504 | whole, gt-9 -- the pruned search window |
| `app/harvest_figures.py` | +561 | whole |
| `app/harvest_research.py` | +540 | whole |
| `app/harvest_typed.py` | +222 | whole -- the shared admission, cap and envelope |
| `tests/test_og_gt0..gt4.py` | +1405 | whole, five files |
| `tests/test_og_gt8.py` | +100 | whole, gt-8 |
| `tests/test_og_gt9.py` | +214 | whole, gt-9 |
| `app/tools.py` | +63 | by hunk, `0cda8e2505` -- the ten registrations |
| `app/destructive_ops.py` | +10 | by hunk -- the ten into `SAFE_TOOLS` |
| `app/data_entitlement.py` | +10 | by hunk -- the ten into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | +2 -2 | by hunk -- `registered_tool_names` 65 -> 75 |
| `tests/test_data_entitlement_family.py` | +3 -3 | by hunk -- `non_data` 56 -> 66 |
| **`deploy-to-ec2.sh`** | **+8 -1** | **by hunk, gt-8 -- the artifact gains `lib/`** |

**`lib/` IS A NEW ARTIFACT MEMBER, and that is the one change here that is not application code.**
gt-8's deploy hunk refuses the upload outright when `lib/trading_calendar.py` is missing from the
repo, stages that one file into the bundle, and adds `lib` to the tar. So `/opt/opal-gateway/lib/`
appears on the host for the first time, carrying exactly one file. Nothing else enters the artifact.

One pin covers every whole-file take (`b6075b276d`): gt-8's `harvest_identity.py` and gt-9's
`harvest_press.py` are byte-identical to trunk HEAD, and the other three modules and the five
`gt0..gt4` tests are unchanged since v1's pin -- verified blob by blob rather than assumed.

**Absent from the cut AND from the tree:** `app/news_typed.py` (rides `OG-ap-19`),
`app/typed_scope.py`, `app/harvest_published.py`, `tests/test_og_gt5.py`, `tests/test_og_gt6.py`, the
gt-10 portal modules, and the `/yearinreview` refresh (its own `OG-yr-1`).

## 2. The ten `tools`, their class, and what they answer `refused`

All ten are READ tools, `SAFE` in `destructive_ops`, `legacy` class in `data_entitlement`
(`NATIVE_TOOLS`, deliberately NOT `DATA_GRANT_TOOLS`): `harvest_resolve_security`,
`harvest_security_coverage`, `harvest_get_chatter`, `harvest_search_articles`, `harvest_get_article`,
`harvest_get_fundamentals`, `harvest_query_columns`, `harvest_get_research`,
`harvest_get_filing_analysis`, `harvest_get_peers_and_scores`.

Each calls `harvest_typed.admit_typed` **before any S3 call** -- OG-hv-1's admission: a principal, then
`tools._is_opal_user`, then the served-prefix test. So each inherits `principal_required`,
`harvest_opal_only` and `harvest_prefix_not_served`, and adds `harvest_bad_argument`,
`harvest_over_cap`, `harvest_read_failed` and `harvest_unreadable`. A non-Opal caller is refused all ten.

## 3. The `widening`, stated plainly

**No new bucket reach. No IAM change. No grant.** These read `s3://opal-data-harvest` through the same
policy and the same Opal-only admission OG-hv-2 already put live, under the same 24 served prefixes.
`gateway-global-internal-reader-role` gains nothing and `harvest_read_iam.tf` is untouched.

What widens is **ease**: ten typed, projected readers over what `harvest_read` could already fetch one
object at a time -- research notes, filing analyses, press and social chatter, peer sets and scores, and
Bloomberg bronze tables **read from the bucket**. There is no vendor call in any of these modules, so
no Bloomberg entitlement is touched and nothing goes through their queue.

The second widening, smaller and worth naming: the host gains `lib/trading_calendar.py`. It is a pure
date-arithmetic module with no network and no credentials, and it is what lets these tools state a
trading-day lag instead of an absent reason.

## 4. The `order` of acts, and that no grant is part of it

ONE act: the deploy, under ledger `nfra-oplgtw-gateway-release-gt`, entry and sentinel first. No
Terraform, no IAM apply, no store write. Phase B: ledger, deploy from `C:/tmp/og-rel-gt2` under the A1
guard (deploy tree HEAD == the full `release_sha`, its parent == live `deployed_commit`), read back the
triggers, then the served read of all ten.

## 5. `Both branches` of a call

| branch | what happens | evidence |
|---|---|---|
| **refused** | the admission answers before any S3 call, so **zero S3 calls** | `admit_typed` runs first in every tool; OG-hv-2's served read measured `s3_calls_on_refusal 0` for the same admission with a counter in place of the client |
| **admitted** | the read is **capped at 64 MB on the body itself** (so a lying `Content-Length` cannot defeat it; over it -> `harvest_over_cap`) and the output **projected to 50 KB**, carrying `truncated` and `projected_to_bytes` | `app/harvest_typed.py:24-28, 54, 147-153` |

Every answer carries `as_of`, `source_keys`, `denominator`, `absent_reason`, so an empty answer says why.

## 6. The host-shaped import check -- the trigger A4 added, and the one v1 lacked

A4 made this a Phase A trigger because v1's evidence ("imports cleanly in the release tree") is a
property of a module **at a depth**: the checkout is 8 parents deep, the host is 4, and `parents[5]` is
correct in the first and fatal in the second.

Run here: the release tree's `app/` copied to `C:/tmp/g1/app` with `lib/trading_calendar.py` beside it,
then all five G1 modules **and `app.tools`** imported in a FRESH interpreter whose `sys.path` is that
root alone.

- **Depth proof:** `C:/tmp/g1/app/harvest_identity.py` has **exactly 4 parents**, the same as
  `/opt/opal-gateway/app/harvest_identity.py`.
- **Result: 6 of 6 OK.**
- At that depth gt-8's `_calendar()` **resolves**: `calendar_source` reads, T-1 is `2026-10-13`, and a
  `2026-10-09` stamp yields **`trading_days_behind_t1 = 2`** -- a number, not the absent reason. That is
  what Phase B must see, measured before the deploy at the host's own depth.
- gt-8's own `test_oggt8_ac01/ac02` corroborate it independently: the `harvest_identity` half of each
  asserts `{'import': 'ok', 'calendar': True}` with `lib/` present and `{'import': 'ok', 'calendar':
  False}` without it, and both halves pass.

## 7. Two tests fail, by construction, and the choice is the issuer's

`tests/test_og_gt8.py`: **2 failed, 1 passed**. `test_oggt8_ac01` and `ac02` each assert on TWO
modules -- `harvest_identity` AND `news_typed` -- and A4 keeps `news_typed` out of this release, so its
half reads `{'import': 'ModuleNotFoundError', 'calendar': None}` and the assertion fails. **The
`harvest_identity` half of both passes.** Nothing that ships is defective; gt-8's test suite simply
spans two modules the order split across two releases. Three routes, and this seat picked none: take
`news_typed` too (contradicts A4 and widens this release), accept these two as unmeetable here and name
them, or let `tests/test_og_gt8.py` ride `OG-ap-19` with the module it covers. Filed as a row.

Every other suite passes: `gt0` 5, `gt1` 4, `gt2` 5, `gt3` 5, `gt4` 7, `gt9` 4, `hv1` 5,
`entitlement_admin` 9, `data_entitlement_family` 4 -- **49 passed, 2 failed, 0 errors**.

## 8. The `rollback`

Redeploy the base `bacec95ccd` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`. Complete, not a
hope: that ref's parity with the host was measured at 107 of 107. No IAM to undo. Note that a rollback
leaves `/opt/opal-gateway/lib/` in place -- the older artifact simply does not reference it, and no code
in the base reads it.

## 9. The `triggers` Phase B reads back

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` | `{"ok":true}` |
| registry **+10** | the app's own registry; `registry_before` is already banked at **46** against the ref it was read at | **46 -> 56** |
| `.env` names unchanged | key NAMES only | unchanged |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/` vs `7521aee725` | all equal |
| **`lib/trading_calendar.py` on the host** | SSM md5 | **`3de6a337e268614698943b038248113b`** |
| **a numeric `trading_days_behind_t1`** | the served `harvest_resolve_security` / `harvest_security_coverage` answers | a number, not `absent_reason` -- this closes row `Z-S125` |

**The md5 oracle is not the repo's copy.** gt-8 stages `$WORKSPACE_ROOT/lib/trading_calendar.py`, and
`WORKSPACE_ROOT` is the DEPLOY TREE -- pinned at the base for every file this cut did not take. So the
artifact carries the base's calendar (`3de6a337`, hardcoded NYSE fallback 2024-2027), not trunk's newer
one (`6596e52f`, 2010-2027, generated, fail-closed outside its years). Both cover the current frontier,
and the numeric lag above was measured against the copy that will actually ship. Comparing the host
against `6596e52f` would read a correct deploy as a mismatch.

The CVO's A3 condition stands: `harvest_search_articles` is read through `mcp.opalinvest.dev` against
the ALB's 60 s idle timeout; a 502/504 or a call over 60 s pulls **only that tool**, with an ARMED row
naming the issuer, not the release. From this box the pruned call measures 38-48 s; the host is
in-region and the public-endpoint read is the measurement that counts.

Any trigger failing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 10. What is NOT asked

No IAM, no grant, no store write, no vendor call, no new bucket or prefix, no route, no `.env` key, no
catalog edit. `harvest_get_published_analysis` (gt-5), `typed_scope.py`, `news_typed.py` and the portal
modules are not in this release. And no deploy until all three halves are signed at this `release_sha`.
