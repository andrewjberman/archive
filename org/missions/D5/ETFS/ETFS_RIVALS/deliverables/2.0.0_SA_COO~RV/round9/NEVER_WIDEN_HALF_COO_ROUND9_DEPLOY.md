# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 9 -- deploy the five rivalfunds Lambdas at CLOUD 8ba7b13b90, seed the security list ONCE off-Lambda, republish 2026-10-05 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~19:2xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** round 9 (the round-8 analysis @2097b5212b section 4) has 6 of 7 orders built, re-verified by the issuer and drained;
the 7th (gd-1) is a LOCAL read with nothing to deploy.
- Drains: gf-1 357f8b6d65, su-2 814fb96d57, ln-1 a3f8a8e458, nf-1 7dc0cf94e7, cb-1 + nm-3 3825462318.
- Issuer hookups: 238fb3dbe9 (run_dag passes `rebuild_funds`; `build-security-universe` runs incrementally after the page and
  SKIPS when no prior list exists, so the Lambda never seeds) and 8ba7b13b90 (collector import marker carries `rebuild_funds`).
- At the pin: package suite 695 passed, 2 skipped, 0 failed; ruff py39 clean. Every round-9 mechanical check PASS re-run by the
  issuer in its worker's worktree, with round-8 regressions (lg-1.AC1/AC2, su-1.AC1, fc-1.AC1/AC2, an-1.AC1, hc-1.AC1/AC2) PASS.
- nf-1's real-data proof (the D12 Step B mirror census with `rebuild_funds` IDVZ/PFOE, 189 report dates): G1 0 other-fund
  deltas (+12,798 IDVZ/PFOE rows); G5 other funds value-equal on every column the live objects carry (+367 IDVZ/PFOE trade rows);
  only `est_price_source` / `key_resolution`, newer columns, are null on carried rows (the render reads `key_resolution` as
  optional; `est_price_source` is not rendered).

## VERDICT: SIGNED

Conditions: the pin is CLOUD 8ba7b13b90; every gate below reads as stated; the act stops at the first differing read.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-round9`).
2. **`safe-apply` of `C:/tmp/rv_apply19.tfplan`** from `C:/tmp/rv-r8` detached at 8ba7b13b90 (plan text `C:/tmp/rv_plan19.txt`):
   **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified` only. Before = the live round-8 set (daily iEAsI4j6,
   fetch eszFeH2T, canonical N4BQNtC7, silver nzchVxil, publish MR4SLZaW); after = daily dMuSFoah, fetch 2XaLTXHM, canonical
   IHCy7pdV, silver g+Rb5Ip8, publish eGMhgbGj. No environment change: `RIVALFUNDS_LEG_*` stay unset and `leg_gates.json` ships
   every gate "0", so no fund's source moves.
3. **Seed the security list ONCE, off-Lambda:** on the terminal machine at the pin, `gold_security_universe.handler_entry(
   {"date": "2026-10-05", "sink": "s3", "mode": "seed"})`. One NEW key at `gold/security_universe/date=2026-10-02/`. Measured on
   the mirror: 19.5 s, peak working set 2,256 MB (why it cannot run in the 1,024 MB Lambda), 1,016 securities over 504 report
   dates. From then on the sweep extends it incrementally (one G1 date per day). The first key is relayed to the laptop
   (MDPF_SECCLASS) through `0.0.0_AB_MSTR~Z`.
4. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `--cli-read-timeout 960`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-05","mode":"daily","batch_id":"rv-publish-1005r9","sink":"s3","refresh_a1":false}`;
   the AI step reads SKIPPED_EXISTS (no vendor call).

## EXPECTED OUTCOME -- MEASURED ON THE MIRROR, NOT PREDICTED

`rivalfunds/etfs/` re-synced with `--delete` at 19:1xZ; the pin's own `publish_page.handler_entry` with the event above: status
PARTIAL (the IDVZ-group freshness lag, unchanged), 3.9 s, peak 583 MB, page 1,853,183 B (cap 2,097,152), 1,948 data-sec links
(1,568 on the served page), 441 dialogs (unchanged), "Benchmarks (SCHY)" 0. The real-context render measured the same bytes.
Branch NOT applied (the apply fails or a verify differs): stop, close the entry red; the served page stays rv-publish-1005r8b.

## WHAT CHANGES AT THE NEXT VEHICLE RUN (2026-10-06 07:00 ET, the CLOUD working tree, no act here)

- `collector_bloomberg` records every capture's rows in `%LOCALAPPDATA%/opal_bbg_budget` and refuses an over-budget BACKFILL
  (ceiling 150,000 rows, reserve 30,000); the daily pull is never refused.
- `enrichment_bloomberg --mode daily` runs the names stage after its G4 lands: one LONG_COMP_NAME request for the page keys named by
  a ticker form (135 measured; 1 row per key), inside the budget, written to a new `gold/security_names` object.
- Nothing moves while the Terminal's capacity is blocked: each Bloomberg leg then fails as today.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the b166e04416 set (live) | the 8ba7b13b90 set | a saved plan from a detached worktree at b166e04416 after `rivalfunds_package.py`, `safe-apply` |
| gold/security_universe/date=2026-10-02/universe-<rev>.parquet | absent | 1,016 rows | delete that key (human-confirmed S3 delete); nothing on the page reads it |
| platinum/page/date=2026-10-05/{index.html,manifest.json} | batch rv-publish-1005r8b (15:33:50Z), kept under revisions/ | batch rv-publish-1005r9 | republish after the code rollback |
| state/publish_page/date=2026-10-05/ | present | +1 marker | none needed |

Not in this act: the D12 gate flip in `leg_gates.json` and D12 Step B (the IDVZ/PFOE import with `rebuild_funds`) -- their own half,
next, with the per-date census as its proof.
