# NFRA_DEPLOYCENSUS — deployed-vs-built-from census (Rule 22a CODE layer), 2026-08-18

**Assignee:** 0.8.0_AE_CloudComp · **Issued by:** 2.0.0_SA_COO · **Authority:** Andrew-direct 08-18 ~1500Z (census pull-forward, item iv)
**One bounded read. CLASSIFY ONLY — zero fixes, zero deploys, zero staging writes performed.**
**Repo vintage of the read:** HEAD `c29e2aa3105af797ac2df4c45d4a3d64128ffa97` (Lambda pass began at `6d40b634a42`, EC2 pass at `c29e2aa310`; HEAD advanced under the census — each evidence file records the HEAD it measured against). All S3/Lambda/SSM reads live, 2026-08-18 ~1530–1610Z.

Method instruments (fenced, re-runnable by copy-out — see `INSTRUMENTS_APPENDIX.md` for why not raw `.py`) + machine evidence in this directory: lambda census → `lambda_census_v3_findings.json` / `_summary.json`; EC2 staged → `ec2_census_v2_rows.json`; EC2 on-box → `ec2_onbox_verdicts.json`.

---

## DC-1 — DENOMINATORS

**Lambdas:** source-map (`infra/aws/lambda/ci/lambda-source-map.json`) N = **197**. Live `list_functions` (all pages materialised) = **194**. In-map AND live = **188**; all 188 packages downloaded and member-hashed. In-map NOT live = **9** (named, class UNREAD/NOT-LIVE): m365-otp-liveness, m365-ms-ingest-liveness, bd-client-detail, find-insure-serving-{companies,employees,scoring,consolidate}, smartx-ec2-autostart, smartx-model-monthly-pull. Live NOT in map = **6** (map-coverage gap, named): opal-49f-served-guard, opal-cot-served-guard, opal-inf-served-guard, opal-ms-ingest-liveness, opal-otp-liveness, opal-data-refresh-api-qa-scratch. *(Note the m365→opal liveness pair: the map still carries the OLD names of two renamed functions — a map-hygiene row, not a code-drift row.)*

**EC2:** manifest (`infra/aws/ec2/EC2_MANIFEST.json`) N = **27** services on **24** distinct instance ids (+2 null). Staged-read (declared S3 staging enumerated + code-shaped objects byte-compared): **17** services with a readable staging surface, ~**460** code objects hashed. Staged-UNREAD = **10**, named with why in §4. On-box (APPLIED) read via read-only SSM hash commands: **5** boxes (every SSM-Online box: inf-gold-layer-runner, mdpf-daily-runner, opal-gateway, canonical-schwab-si2, opal-website-wp). On-box UNREAD = **22** boxes: 19 stopped-by-design/transient (not started for a read-only census), 2 manifest instance-ids that DO NOT EXIST (`orion-crawl-harness` i-010f195f1798b40ad, `estate-report-runner` i-04981b6aec3bed86b — the ASTN wrong-machine class recurring in the manifest), 1 null-id (bd-exporter).

**EventBridge:** 135 rules materialised (all pages) for the trigger-liveness reads.

## DC-4 — CONTROLS (both printed, instrument discriminates)

- **NEGATIVE (must read CURRENT): `smartx-jwt-refresher` → CURRENT.** Deployed member `lambda_function.py` blob == HEAD blob; live CodeSha256 == map artifact_sha256. Matches the COO three-way read 08-18 ~1355Z (@d5d7342da4).
- **POSITIVE (must be FOUND): `inf-silver-chain` → TWO-HOMES-DIVERGED on `build_billing_dim.py`.** Deployed bytes byte-identical to its OWN source dir (`infra/aws/lambda/inf-pipeline/inf-silver-chain/`, all 5 members CURRENT vs own tree) while the bundled copy has diverged hard from canonical `data/inf/scripts/silver/build_billing_dim.py` (similarity **0.345**, canonical last moved @d8fee4b04f 2026-08-11 by DS; SYNC.md's last recorded sync is f6b7238a9 2026-05-11). Also diverged in the same package: `_orion_api_silver_lib.py` (0.865), `convert_orion_api_to_silver.py` (0.874), `build_tax_dim.py` (sim 1.0, cosmetic-only). **The census found the known divergence — instrument PASS.**

## DC-2 — LAMBDA CLASSIFICATION (197 rows, every one classified)

| Class | N | Rows |
|---|---|---|
| CURRENT | **141** | (unlisted — every member blob == HEAD, or transformed-build provenance chain intact with no source movement) |
| DELIBERATELY-HELD | **11** | see 2a |
| STALE-BY-NEGLECT | **8** | see 2b |
| TWO-HOMES-DIVERGED | **16** | see 2c |
| UNREAD | **21** | see 2d |

*(Machine file says CURRENT 142 / STALE 9 / HELD 10; one manual reclass applied here with citation: `ycharts-market-data-pull` STALE→HELD per its own source-map `_build_note` "Deployed DORMANT … the live pull path stays unused until the dedicated YCharts seat (TO-D1)" — the hold is INFERRED from the dormancy declaration, flagged as such.)*

### 2a — DELIBERATELY-HELD (11) — a stated reason exists, cited per row
| Lambda | Subkind | The stated reason |
|---|---|---|
| etfs-canon-fanin | COSMETIC-ONLY drift | deployed@07d99dc4 vs head@3bfc5155 = docs-only commit; AST-identical after docstring strip. Precedent: COO 08-18 ~1355Z @d5d7342da4 ("no deploy off a docstring") |
| smartx-rest-pull | COSMETIC-ONLY drift | the 135226Z precedent case itself — one docstring path line from the 06-11 sweep |
| inf-api-assets-v2 | COSMETIC-ONLY drift | both members AST-identical after docstring strip (06-11 sweep) |
| inf-portal-advisor-publisher | COSMETIC-ONLY drift | sim 1.0, docstring-only |
| inf-unified-account-dim-daily | COSMETIC-ONLY drift | sim 1.0, docstring-only |
| inf-etf-ownership-daily | STATED-IN-COMMIT | @001a73530a: "COMMIT ALL / APPLY NOTHING per CTO F2 ruling 20260803T215051Z … DELIBERATELY NOT APPLIED … ARMING on any code-artifact deploy" (dedup_core.py + trading_calendar.py committed-never-deployed BY RULING; declared HEAD-ahead-of-applied divergence) |
| yang-generate-cma | STATED-IN-COMMIT | @b894ac431e: "⛔ COMMIT ONLY. NOT DEPLOYED. … the deploy is a separate act with COO" (OPAL_INVPHL philosophy-pillars producer leg — **open deploy act, flagged for routing: /philosophy is in PROD reading assumptions.json without pillars until this deploys**) |
| opal-assets-bd49f-reporting-pull | STATED-IN-COMMIT | @7d97a8bed2: "Producer DEPLOY (code+IAM) is CTO-gated (COO cond a) — staged, not applied" (TAXSMA registry leg) |
| opal-smartx-ingestion-pipeline | STATED-IN-COMMIT | @20e3567f03: "NOT DEPLOYED: log-only, no behavior change" (the summary-line-contradiction fix) — *but see 2c: same package also carries real two-homes rows* |
| finbert-batch-processor | STATED-IN-SOURCE-MAP | map `_note`: "Code managed outside TF (placeholder + ignore_changes)"; adopted 2026-08-04. Live LastModified 2026-01-03 — also a 90-day-dormancy candidate (Rule 25: check-successor before concluding; not adjudicated here) |
| ycharts-market-data-pull | STATED-IN-SOURCE-MAP (inferred) | `_build_note`: "Deployed DORMANT … live pull path stays unused until the dedicated YCharts seat (TO-D1)". 5 members drifted (all committed 05-22, same-day churn after the 05-22 deploy) — dormant function, so the drift is inert until TO-D1 wakes it, **at which point a rebuild is mandatory** |

### 2b — STALE-BY-NEGLECT (8) — deployed older than built-from, no stated hold found
| Lambda | Members behind | Delta kind | Evidence |
|---|---|---|---|
| **public-data-router** (Lambda@Edge, client-facing routing) | index.mjs (chain) | code | nodejs transformed build: live CodeSha256 == artifact built @e125c24d67 (05-14); source_dir moved since. Live LastModified 07-29 is a config/version touch, not a rebuild |
| **shared-advisor-router** (Lambda@Edge) | index.mjs (chain) | code | same shape, artifact @f215cfdddf (05-14), source moved since |
| inf-api-txn | 4 members, 1 behind each | **strings-only** (3) + cosmetic (1) | the 06-11 provenance sweep @46d0b98aef (data/orion→data/inf path strings in docstrings/log lines; AST-with-strings-masked identical). Internally coherent older vintage; converges on next real deploy |
| inf-tax-daily | orion_tax_dim.py, 1 behind | strings-only | same sweep |
| inf-billing-daily | orion_billing_dim.py, 1 behind | strings-only | same sweep |
| inf-performance-daily | pull_inflection_performance_dim.py, 1 behind | strings-only | same sweep |
| opal-inf-value-parity | 3 members behind + `sovereign_held.py` committed-never-deployed | code | inline-archive TF build; repo compdiff tree moved 07-09/07-10/07-11, no re-apply since |
| opal-cot-value-parity | same tree, 2 behind | code | twin of above (detection instruments, not client-serving) |

*(The 06-11-sweep quartet is the census's sharpest classification test: real byte drift, zero behavioral delta — the `strings-only` AST discriminator separates it from code drift so the "deploy" reflex isn't manufactured, exactly the failure mode the TO's authority clause names.)*

### 2c — TWO-HOMES-DIVERGED (16) — one logical producer, two independently-editable homes
**Own-tree shapes (2):**
- **opal-trending-image-generator** — map `source_dir` points at `infra/aws/lambda/trending_image_selector` but the deployed `lambda_function.py` bytes live at `infra/aws/lambda/trending_image_generator/` (sibling dir) — the MAP names the wrong home. Live LastModified 2025-12-30 (~7.5mo; 90-day-dormancy candidate, successor unchecked).
- **opal-globgrph-incremental-updater** — deployed member `_provenance.py` absent from the repo at any path (package carries a file git never had; source_dir holds only lambda_function.py + a prebuilt zip).

**Bundled-copy-diverged-from-canonical (14; deployed byte-identical to its OWN source dir — the second home moved):** inf-silver-chain (the positive control, 4 members), inf-api-reps / inf-api-positions / inf-accounts-v2-daily (`_orion_api_silver_lib.py` 0.68–0.87, `convert_orion_api_to_silver.py` 0.81–0.91 vs canonical `data/inf/scripts/silver/`), inf-api-txn + inf-api-assets-v2 (also carry bundled-copy divergence beside their own-tree class), opal-assets-silver-{orion,eclipse,etf,schwab} (`mirror_conversion.py` 0.79–0.87, `mirror_schemas.py` 0.986, `silver_registry.py` 0.966 vs canonical `data/assets/scripts/silver/`, canonical moved 07-22/07-23), opal-assets-silver-blackdiamond (`rebalancer_{conversion,schemas}.py` vs same canon), opal-smartx-ingestion-pipeline (6 members vs `data/smartx/scripts/`, sim 0.21–1.0), opal-partners-data (`etf_classifier.py` vs BOTH `data/black_diamond/.../lib/` 0.85 AND `data/cot/.../lib/` 0.915 — a THREE-homes row), news-ingestion-scheduler + news-trending-analysis (`text_cleaner.py` 0.916 / `stopwords.py` 0.554 vs `tools/news_scanner/`), exec-summary-generator (`template_library.py` 0.995 vs `data/black_diamond/scripts/exec_summary/`).

*Frame on 2c: "diverged" here = the copies differ NOW at HEAD; whether the bundled or the canonical copy is RIGHT is architectural (Rule 17a lesson) and is NOT adjudicated by this census. Several may be deliberate forks (Lambda-adapted variants). Each row needs its owner to declare fork-or-drift — that declaration is the remedy scoping, not mine.*

### 2d — UNREAD (21) — never silently CURRENT
9 NOT-LIVE (named in DC-1) · 3 CONTAINER-IMAGE (ycharts-session-capture, news-semantic-clustering, opal-news-ai-sentiment — image layers out of the zip-member domain, ECR digest read only) · 8 NO-REPO-SOURCE (trade-auth-handler, trade-authorizer, trade-identifier-cache, ec2-runtime-monitor, market-update-{data-aggregator,exporter,generator}, opal-session-analytics — map says EXTERNAL/no files[]; packages read, 1–4,673 members, nothing to diff against) · 1 inf-portal-publisher (map files[] empty though source_dir exists; package = 1 member).

## DC-3 — EC2 CLASSIFICATION (27 services, staged axis + on-box axis each)

| Service | STAGED (DESIRED) vs repo | ON-BOX (APPLIED) |
|---|---|---|
| consolidation-gold-runner | CURRENT (3/3) | UNREAD (stopped) |
| orion-crawl-harness | UNREAD — declared prefix EMPTY | UNREAD — **manifest instance id DOES NOT EXIST** |
| astn-wsjft-scraper | STALE-BY-NEGLECT: analyze.py 1 behind (staged@ae7eb9efb3 06-29), run.py 2 behind, send_ses.py 1 behind; +22 staged-orphan test/diag scripts | UNREAD (stopped, transient 3am-ET) |
| bd-49f-auto-login | CURRENT (3/3) + 1 staged-orphan (f1f2_exercise.js) | UNREAD (stopped, event-triggered) |
| etfs-reports-reporter | CURRENT (render leg) + 1 orphan probe.sh | UNREAD (stopped; next fire SEP-1) |
| smartx-exporter | UNREAD — deploy_mechanism "pre-manifest-era-unknown", NO declared staging | UNREAD (stopped) |
| seeking-alpha-scraper | UNREAD — same | UNREAD (stopped) |
| **bd-gold-layer-runner** | STALE-BY-NEGLECT: gold_validate_config.yaml **8 behind** (staged 04-22), gold_pipeline_deps.yaml 1 behind, ticker_overrides.py 2 behind (+137 CURRENT incl. all 60 deploy-gate gold scripts — cross-checked vs `comp-pipescript deployed`: 60 MATCH, 0 STALE, 48 S3-ONLY consistent with my 9 orphans at different extensions) | UNREAD (stopped; EVENTBRIDGE-ONLY access policy — correctly not touched) |
| bd-gold-qa-runner | STALE: setup-instance.sh 1 behind | UNREAD (stopped) |
| **bd-exporter fleet (bd-allocations, bd-transactions, bd-fees, bd-assets, bd-price-runner, bd-exporter)** | **TWO-HOMES-DIVERGED + STALE, EXECUTING DAILY — the census's immediate-report finding (sent 160830Z):** staging home `scripts/merge-daily-incremental.py` = vintage 12cc7e111c (06-29), **4 commits behind**, missing stub-guard @844a2cb45d + frontier-select @2acfb04014; SSM docs `opal-bd-{allocation,transaction}-download` lines 42–43 pull + `python3`-RUN it daily (EventBridge cron(0 22)/cron(53 21) both ENABLED, verified live). The OTHER staging home `code/silver/merge-daily-incremental.py` (bd-silver-merge Lambda pull) is CURRENT == HEAD. Stepwise TS export automation staged CURRENT (4/4 sampled). bd-price-runner CURRENT. | UNREAD (stopped between runs) |
| bd-gold-detail-generator | UNREAD — ephemeral, code baked into user-data at launch (STAGED-INERT by construction) | UNREAD (no instance) |
| historical-prices-fetcher | UNREAD — no declared code staging (yfinance fetch via lambda-scheduler) | UNREAD (stopped) |
| **inf-gold-layer-runner** | STALE-BY-NEGLECT: INF_D_10.aor_conformance.py 1 behind (staged@5fe87187 07-11), orion_cashflow_taxonomy.yaml 1 behind (+118 CURRENT; 49 staged-orphans = superseded pre-rename gold generations parked in code/gold/ — 26 of them dated 06-11; cross-checked: `comp-pipescript deployed` reads INF_D_02/INF_D_04/INF_D_10 STALE, same members) | **READ (SSM): 3-way CURRENT** on run-gold-layer.sh + watchdog-shutdown.sh (on-box == staged == repo). On-box `/home/ec2-user/orion-gold-dispatch.sh` ≠ staged is **INERT** — the run path pulls fresh to /tmp per `inf-gold-trigger/lambda_function.py:473`; staged dispatch == repo HEAD (CURRENT). *Note: watchdog pull is FIRST-BOOT-ONLY (user-data.sh:17) — currently in sync, but structurally the 22a STAGED-INERT shape; flagged.* |
| inf-gold-qa-runner | UNREAD — declared prefix code/runner-qa/ EMPTY | UNREAD (stopped) |
| inf-exporter | UNREAD — no declared code staging (s3-ssm, path unnamed) | UNREAD (stopped) |
| inf-bronze-runner | STALE: inf_backfill_billing.py 1 behind, run_backfill_orchestrator.sh 1 behind, orchestrator.py staged bytes not in path history on any ref (TWO-HOMES row; `comp-pipescript` aux:bronze-runner DRIFT agrees on all 3) + 20 orphans under manual_api/ (mirror copies of the inf-api-* Lambdas' sources — a THIRD home for that family) | UNREAD (stopped) |
| **mdpf-daily-runner** | STALE on 3: build_portal_gold_accrual.py 1 behind (staged 07-29), partner_roster.json 1 behind, build_legacy_compat_emit.py 1 behind (+41 CURRENT) | **READ (SSM): 44 files hashed — 41 == staged; 2 DIVERGE WITH ON-BOX AHEAD: on-box `gold/build_portal_gold_accrual.py` + `gold/partner_roster.json` == repo HEAD while STAGED is the stale copy.** Since the dispatch `s3 sync`s staged→box each run, a second delivery channel updated the box (accrual re-home / assets `_code` bridge is the INFERRED carrier — not source-confirmed). The staging home no longer describes what runs = two-homes at the delivery layer. |
| opal-gateway | staged read: only 2 cert/diag scripts at the artifact prefix (deploy artifact is a tar.gz, out of the code-shaped filter) — staged axis UNREAD-BY-SHAPE | **READ (SSM): CURRENT — 30/30 `app/*.py` on-box md5 == repo HEAD** (incl. all 9 manifest file_checksums entries) |
| canonical-schwab-si2 | UNREAD — windows-scheduled-tasks, no S3 staging by design | **READ (SSM PowerShell): TWO-HOMES-DIVERGED / NO-REPO-HOME — none of the 9 executing `C:\SchwabData\*.ps1` (incl. `sync-to-s3.ps1` = the live SchwabS3Sync task, tasks confirmed Ready with today's run times) exists in `infra/aws/ec2/canonical-schwab-si2/` by name.** Manifest discloses "persistent Andrew-direct box, not TF lifecycle-managed" — a stated reason for the INFRA plane; the CODE plane living outside git is still a census row. |
| opal-website-wp | CURRENT (9/9) | READ (SSM): 6/7 on-box == repo; `acme-dns-hook.sh` on-box-only (no repo home; TLS-issue vintage 07-16) |
| cot-exporter | UNREAD — s3-ssm, no declared code prefix in manifest | UNREAD (stopped) |
| estate-report-runner | CURRENT (1/1: estate_report_runner.py == HEAD) | UNREAD — **manifest instance id DOES NOT EXIST** (box replaced; manifest not synced) |

## DC-5 — SUMMARY COUNTS

**Per-Lambda (197):** CURRENT 141 · DELIBERATELY-HELD 11 · STALE-BY-NEGLECT 8 · TWO-HOMES-DIVERGED 16 · UNREAD 21.
**Findings (axis-separated, machine file):** own-tree HELD 10 · own-tree STALE 9 · own-tree TWO-HOMES 2 · bundled-vs-canonical TWO-HOMES 17 · UNREAD 21 (one row may carry findings on both axes).
**EC2 staged (27):** CURRENT 6 · STALE-BY-NEGLECT 6 · TWO-HOMES (incl. orphan-bearing) 3 · UNREAD 12.
**EC2 on-box (27):** READ 5 (of which CURRENT 2 [gateway, website±1], mixed/diverged 2 [mdpf ahead-of-staged, si2 no-repo-home], current-with-inert-leftover 1 [inf-gold]) · UNREAD 22 (named, with why).
**Answer to "how many more two-homes":** beyond the three known instances, the census surfaced **~20 distinct two-homes relationships** (14 bundled-copy Lambda rows incl. one three-homes, 2 own-tree rows, the bd merge-daily two-staging-homes [EXECUTING], the mdpf box-ahead-of-staging, the inf manual_api third home, the si2 code plane).

## DC-6 — METHOD NOTE: what this census COULD NOT see (its own domain boundary)

1. **Container images** (3 Lambdas): ECR digests read, layers not unpacked — image-member currency UNREAD.
2. **Runtime-fetched code**: Lambdas/boxes that pull code from S3 at RUN time (bd-49f-runner pulls cot_bronze_ingest.py, bd-silver-merge pulls merge-daily, inf gold dispatch pulls to /tmp) execute the STAGED copy at fire time — the staged axis covers their DESIRED state, but a run between my read and any staging change executes different bytes. The census reads a moment, not a guarantee.
3. **Stopped boxes** (19): on-box bytes UNREAD by design (read-only census, no starts). Baked/cached copies on those disks (the STAGED-INERT class) are invisible until next boot or an authorized SSM read on a started box.
4. **Transformed builds** (nodejs bun --minify, 4 Lambdas): byte-diff to source is malformed; the provenance chain (live CodeSha256 == recorded artifact + git-log-since-build) substitutes. A chain-verdict is weaker than a byte-verdict: it trusts the map's artifact_sha256 recording discipline.
5. **Lambda LAYERS**: not compared (dependency currency is Rule 3/layer-map territory, out of this TO's member-sha scope).
6. **The 8 EXTERNAL/no-source Lambdas**: readable but un-diffable — a repo-adoption backlog, not a drift verdict.
7. **basename resolution** (EC2 + resolution-D Lambdas): where the build input names a DIRECTORY, members resolve by relpath/basename with a similarity guard (<0.5 → STAGED-ORPHAN, never a false OLDER); ambiguous matches are labeled AMBIGUOUS in the rows rather than silently picked.
8. **Andrew's uncommitted working tree**: several member deltas matched dirty working-tree files (flagged `wt_dirty`/AHEAD-WT per row) — those verdicts move when he commits.
9. **Windows box (si2)**: name-level resolution only; content-level matching of differently-named scripts not attempted (would need on-box byte pulls — a follow-on authorized read if wanted).

## Routing (per TO: findings route to owners AFTER the census, by COO/CTO)
Immediate-report already sent (160830Z COO, CC CTO/MSTR): the bd merge-daily two-homes EXECUTING row. Everything else lands with this table. Nothing was fixed, deployed, or deleted by this census.
