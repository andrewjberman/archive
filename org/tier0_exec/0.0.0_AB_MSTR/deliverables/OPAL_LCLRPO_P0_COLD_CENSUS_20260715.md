# OPAL_LCLRPO — P0 cold census + disposition proposal (2026-07-15)

**Author:** 0.0.0_AB_MSTR · **Authority:** LD-0300 (Andrew-direct) · **Status:** AWAITING ANDREW BATCH REVIEW — nothing moved yet.
**Method:** `comp-heat freshness` full-workspace snapshot (git-derived write history; 22,783 tracked paths; JSON persisted in session scratchpad), re-filtered at Andrew's **120-day threshold** (≈ untouched since 2026-03-15), aggregated at depth-1/2, then **every headline candidate cross-checked against `lambda-source-map.json`** (cold-by-git ≠ dead: deployed source that never changes is cold AND load-bearing). Portal/ is its own repo — out of LCLRPO scope.

## Headline

- **~5,500 of 22,783 tracked paths (~24%) are ≥120d untouched.**
- comp-heat's advisory cold-subtree list: 1,223 subtrees. After the KEEP-class filter (governance records) and the source-map cross-check, the actionable estate falls into five clean classes below.
- The cross-check **caught the trap four times**: `timeseries/`, `infra/aws/lambda/portal/`, `infra/aws/lambda/infrastructure_monitor/`, `data/smartx/` are all cold-by-git **and referenced by the deployed-lambda source map** — untouchable on age alone.

## Class B1 — BATCH-1 ARCHIVE (clear: ≥120d cold AND source-map-clear) — ~560 files

Proposed mechanics: `git mv` → `archive/2026-07/<original-path>` (history-preserving, one-revert reversible) + a per-batch manifest (`archive/MANIFEST_20260715_batch1.md`).

| Candidate | files | age (newest–oldest) | note |
|---|--:|---|---|
| `tools/market_update/` | 211 | 222–226d | dead tooling family |
| `data/seeking-alpha/` | 73 | 140–174d | retired vendor experiment |
| `research/` (debt_spiral 41 + vix_strategy 17) | 58 | 239d | research artifacts, never touched since Nov |
| `tools/seeking-alpha-ui/` | 30 | 163–174d | dead UI experiment |
| `docs/handoffs/` | 22 | 159–183d | superseded by org/ session-log law |
| `docs/security/` | 16 | 142–152d | pre-SCTY-era docs |
| `infra/orchestration/` | 15 | 142–235d | pre-fabric orchestration experiment |
| `docs/lambda-requests/` | 15 | 140–191d | superseded request-doc pattern |
| `tests/cloudfront/` | 10 | 191d | dead test family |
| `infra/testing/` | 10 | 145–148d | dead |
| `docs/cost_analysis/` | 10 | 148d | one-shot analysis |
| `infra/prompts/` | 9 | 141–222d | pre-org prompt experiments |
| `infra/linting/` | 9 | 141–162d | superseded by commit-gate |
| `infra/architectural_docs/` | 9 | 222–238d | superseded by docs/architecture |
| `org/daily_log/` | 8 | 126–135d | superseded by session-log standard |
| `docs/task-orders/` | 8 | 155–156d | superseded by per-agent task_orders/ |
| `docs/sessions/` | 7 | 141–153d | superseded |
| `tools/wyncht/` | 6 | 125–126d | dead |
| `tools/schwab_aum_carving/` | 6 | 235d | dead one-shot |
| `goldfish/` | 5 | 163d; **ONE commit ever (2026-02-02)** | Andrew's named exemplar — never used |
| `infra/aws/lambda/market_query/` | ~2 | 239d | **source-map-clear** legacy lambda dir |
| assorted `infra/aws/docs/` legacy session docs + one-off scrape reports | ~25 | 194–239d | RSS/news-era leftovers |

## Class B2 — DELETE candidates (bulk junk; your explicit word required per batch)

- `tools/analytics_venv/` (15 files) — a **committed virtualenv**. Nothing references it; recommend DELETE over archive (it is reconstructable by definition).
- `__pycache__/` trees committed under various paths (thousands of compiled-artifact files inside vendored trees) — DELETE + `.gitignore` (the ignore rule is a STNDRD-F seam item).
- `infra/aws/scripts/{beast_mode_report,massive_scrape,trending_topics_report}.json` — one-shot scrape outputs (239d).

## Class V — VENDORED-DEPENDENCY TREES IN GIT (structural; routes to OPAL_STNDRD, not age-based)

- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/**` — **~1,000+ files** of pygments/pyarrow/numpy/rich… (newest 36d — actively rebuilt, so NOT cold; it is *structurally* wrong per Rule 3's spirit: a layer BUILD ARTIFACT living in git).
- `infra/aws/lambda/infrastructure_monitor/openai/**` — **~600 files** of inline-vendored SDK, 194d, **backing a LIVE lambda** (source-map referenced). The flat-vendoring incident class (ADHC_LAMBDADOC) by name.
- Disposition belongs to CTO's STNDRD (registry/build-artifact law): artifacts → S3/layer + gitignore; repo carries the manifest, not the site-packages. **Biggest single file-count win available (~1,600+ files), but it is a build-chain change, not an archive move.**

## Class VC — VERIFY-class (cold AND deployed-referenced — owner check before ANY move)

- `timeseries/` (79, 183d) — source-map REFERENCED. Owner check: which lambda, still deployed?
- `infra/aws/lambda/portal/lambda_calc_*.py` (239d) — REFERENCED; live portal calc lambdas?
- `infra/aws/lambda/infrastructure_monitor/` (194d) — REFERENCED, live monitor (also the SES-sender migration touchpoint from LD-0291 lineage).
- `data/smartx/` old scripts/docs (239d) — REFERENCED in source-map AND superseded-in-spirit by the yaliu-era work; needs 0.5.0's word on which pieces are the live lambda's source vs. opal7-era dead docs.
- `data/yang_pkl/` (10, 159–212d) — source-map-clear but **client-adjacent data from Yang**; your word, not an age rule.

## Class K — KEEP regardless of age (the record is the product)

`org/**` governance records (ledger, cycles, reviews, audit logs, historical task_orders/logs — 1,366 cold files stay), `docs/references/**` + incident docs, `docs/architecture/**` (INDEX-ing is STNDRD-F's job, not archival), already-archived enclaves (`data/black_diamond/archive/` 292, `docs/architecture/archive/` 126 — already out of the way; consolidation under root `archive/` is optional polish, low value).

## Proposed execution (P1, on your word per batch)

1. **BATCH-1 GO** → git-mv archive of Class B1 (~560 files), one commit + manifest, off-peak (tonight's 22:00Z fire respected; cross-domain MCP to lane owners first — shared worktree).
2. **BATCH-2 word** → DELETE Class B2 (venv/pycache/scrape-junk) — explicitly confirmed as deletions.
3. **BATCH-3** → VERIFY-class resolutions (owner checks routed; anything confirmed dead joins the next archive batch).
4. **Class V** → hand to CTO/OPAL_STNDRD as the build-artifact-law work item (I flag it in the seam).
5. Component B (function canonization) proceeds under OPAL_STNDRD (registered @ 984944875); LCLRPO retires superseded copies after call-sites repoint.

**Asks:** (1) BATCH-1 archive GO? (2) DELETE confirmed for Class B2? (3) `data/yang_pkl` disposition?
