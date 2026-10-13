# MDPF_CANON -- the `code/` sync: the 8 "runner member" rows read one by one (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~22:4xZ)

Read-only. No sync, order or commit is made by this file. Input: CloudOps' classification `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/canon_r4_classification_20261012.md`
(8 RUNNER MEMBER rows of 33 non-EQUAL) and the newer print `canon_r6_equality_AFTER_20261013.out` (same 8 names). Every hash below was read from S3 with a head/get and from
`git show HEAD:<path>`, 2026-10-13.

## 0. Verdict

**None of the 8 needs a sync now.** Six are LEAVE, one is R2-HELD (a one-line provenance difference), one waits for M10 (Stage 6 is dead). The round-4 close
"every file the dispatch chain executes or reads is EQUAL" is, read this way, TRUE for the live legacy chain except `bronze_homes.json`'s one generated-comment line, which FIRMBKTS owns.
Three instrument facts explain why the table over-counts: (a) `mdpf-code-equality.py` hashes the WORKING-TREE bytes, and two files are CRLF in this Windows checkout against an LF blob
(`mdpf_model_registry.json`, config `partner_roster.json`), so they read DIFFER with equal content; (b) two rows are the frozen rollback target of the accrual bridge, deliberately
left behind; (c) two rows are named only in dispatch COMMENTS of stages deleted on 2026-08-11.

## 1. The eight, one by one

| # | member (S3 key under `s3://opal-data-mdpf/`) | repo vs S3 (measured) | runs today? (dispatch anchor) | served effect if synced | disposition |
|---|---|---|---|---|---|
| 1 | `scripts/gold/build_portal_gold_accrual.py` | S3 md5 cfc88b0b72d4, 2026-07-29 15,408 B; repo blob 006592de5ec0, 15,667 B; diff +8 -5, ALL in one docstring (the sentence that the roster ships "script-adjacent"); no code line differs | The accrual bridge runs it from a hash-stamped bundle `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-accrual-bridge.tar.gz` (LastModified 2026-10-09T02:59:31Z; its member script md5 006592de5e EQUALS the repo blob; `infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:116-126`). The loose S3 copy is "FROZEN-IN-PLACE as the rollback target" | none: it is not what runs | **LEAVE.** A sync would overwrite the rollback target. |
| 2 | `scripts/gold/mdpf_model_registry.json` | S3 md5 6b89cc935c65, 2026-06-12, 4,600 B; repo BLOB md5 6b89cc935c65, 4,600 B: IDENTICAL. The working tree is CRLF (md5 fa784dd4ab), which is why the tool says DIFFER | yes: Stage 0 `pull_orion_model_composition.py` (dispatch :248; opens `../gold/mdpf_model_registry.json`, `:71`) and WS-A `mdpf_aggregate_aua.py` (:407) | none (content equal). Hazard: a named-file deploy from THIS checkout would write the CRLF bytes (not verified whether `safe-deploy.sh` normalizes) | **LEAVE** (a false DIFFER). |
| 3 | `scripts/gold/taxsma_assets.py` | S3 md5 2b89e528db7f, LastModified **2026-09-21T20:30:17Z**, 33,083 B (already carries `from lib.opal_naming import address`, line 95); repo c5594c0e012a, 46,082 B; diff +258 -20: contract v0.5.0 -> v0.6.0, per-firm custodian bases, workbook fallback, `lookup` imported and called at module scope | only as a LIBRARY of `dim_mdpf_aggregate_aua_timeseries.py` (dispatch :154-163, :605), i.e. Stage 6. Stage 6 has been dead since 2026-08-14 | none today (Stage 6 writes only staged `gold/mdpf_revamp/*`). The S3 copy's date is the day the runner's `lib.opal_naming` ImportError began (first log 2026-09-21): this key is the proximate import | **SYNC WITH M10/M12** (no value now; HEAD also needs the registry files, `TAXSMA_S5_STAGE6_READ.md` section 2). |
| 4 | `scripts/backfill/build_legacy_compat_emit.py` | S3 md5 edc291408982, 2026-07-29, 45,626 B; repo 70149a08e81c, 46,227 B; diff +17 -11: the repo RETIRES the `aum-timeseries.json` put_object, the S3 copy still carries it | **No.** Dispatch :415-424: "Stage 3.5: DELETED (MDPF cutover act X-iv, 2026-08-11)"; the script is named ONLY in that comment (:417). Nothing executes it | none | **LEAVE** (not a runner member in fact; retired, never executed). |
| 5 | `config/bronze_homes.json` | S3 md5 b2d27b65d2e7, 2026-10-11T05:00:19Z, 464 B; repo 77da01184213, 464 B (last change 69679b90e3, the FIRMBKTS act-4 flip); diff +1 -1, line 2 only: the `_generated` provenance string (registry hash bd1619b411e1330c -> 280826a6a96c3b37) | yes: Stage 0 `pull_orion_model_composition.py` (`:62`) and the WS-C feeder (dispatch :346) | none by content (the homes are unchanged; only the generator stamp differs) | **R2-HELD.** FIRMBKTS-owned until its flip receipt passes ownership (PRD v2.11 R2). |
| 6 | `config/partner_roster.json` (MISSING_ON_S3) | repo blob 3d309b267e69, 27,433 B (CRLF in the working tree, md5 60886298d5); no object at `code/config/` | the readers resolve it script-adjacent in the gold dir (`dim_mdpf_aggregate_aua_timeseries.py:2065`, "runner synced prefix"), not from `config/`; Stage 6 only | none | **LEAVE** (nothing reads the config path). The authority copy ships inside the accrual bundle (member md5 3d309b267e = repo blob). |
| 7 | `scripts/gold/partner_roster.json` (EXTRA_ON_S3) | S3 md5 a22fc62be047, 2026-07-28, 22,725 B; no repo twin at that path | Stage 6 readers (dead) read this one; the bridge no longer does | none | **LEAVE:** the accrual bridge's frozen rollback roster (docstring of #1). |
| 8 | `scripts/gold/_trading_day_calendar.py` (EXTRA_ON_S3) | S3 md5 915960d891b9, 2026-07-21, 5,324 B; NO twin in the repo (`git ls-files` finds none) | imported only by `build_mdpf_etf_ownership_timeseries.py` (`:55`), whose dispatch stage is "Stage 5: DELETED (2026-08-11)" (:441-452) | none | **LEAVE** (dead stage). Side finding: the repo script still imports a module the repo does not hold. |

## 2. Minimal first sync window, and what a pair would read

There is no first window. If one is wanted anyway, it is a single named file `taxsma_assets.py` (#3), and only together with the nine `lib/` and registry keys, the IAM change for the runner role
(`s3:ListBucket` on `opal-data-assets`, C2) and the cross-axis gate read: that is the Stage 6 revival the CTO ruled out ("Stage 6 output means M10"). The pair for it would read: Stage 6's write set (all staged
`gold/mdpf_revamp/*`, `TAXSMA_S5_STAGE6_READ.md` section 3), the frozen 08-18 distribution that the lambda still reads (priced in `S5_FRONTIER_COUNTS_PRICE.md`, which CN-h-1 removes first), and a
byte-exact read-back of the nine keys by sha256 (outside the equality tool's five trees).

## 3. What changes in the round-4 close, if the CTO agrees

Restate (d) as: the live legacy chain's members are EQUAL by content; the three sets that read non-EQUAL are (i) Stage 6 members, dead, un-parked at M10 (`taxsma_assets.py`), (ii) the accrual bridge's frozen
rollback target (`build_portal_gold_accrual.py`, gold `partner_roster.json`), (iii) `bronze_homes.json`, FIRMBKTS-owned, one provenance line, and (iv) tool artifacts (two CRLF files, three S3-only or retired names).
A small tool fix would remove (iv): hash the git blob (LF-normalized) instead of the working-tree bytes. It is not made here.
