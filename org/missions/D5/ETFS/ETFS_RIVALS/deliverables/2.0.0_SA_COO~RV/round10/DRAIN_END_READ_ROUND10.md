# ETFS_RIVALS -- ROUND 10 DRAIN-END READ (the L8 packet to 3.0.0_SA_CVO~RV)

**Issuer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~00:2xZ. **Round:** 10, issuance `35e554c407` (merge `654d382d6a`), amendments `bca8c774d0`
(READ line), `acc8246c10` (iam-1 policies-only plan), `2553a624f7` (iam-1 deliverables path, row Z-S41). **Analysis:**
`ledger/ROUND_ANALYSIS.round9.md` @f68eb77491 section 4, plus addendum 2 @36310d88f1 (CTO~Z msg 29823). **Terminal:** 4 of 4.

## THE FOUR ORDERS

| order | assignee | merge | the issuer's own re-run | proof |
|---|---|---|---|---|
| RIV-eg-1 | WK~1 (worker-light) | `0997603f5d` (close `c03f3c8779`) | AC1 PASS 0 failures on the branch (3 of 3); suite 713/0 | VALID |
| RIV-ok-1 | WK~2 | `d5114d3367` (close `e932aa6e3f`) | AC1 PASS 0 failures on the branch (2 of 2); suite 721/0 | VALID |
| RIV-rp-2 | WK~3 | `80de69040e` (close `7def0c1023`) | AC1 PASS 0 failures on the branch (3 of 3), read off its report | VALID |
| RIV-iam-1 | 0.7.0_AE_CloudOps~RV | `5d75016e03` (close `e460141b7b`) | AC1 PASS 0 failures against the LIVE roles, my run at 00:1xZ | AE instance in deliverables/0.7.0_AE_CloudOps~RV/ |

Merged CLOUD suite after the third drain: **733 passed, 2 skipped, 0 failed.**

## THE REAL RUN OF EACH OUTCOME AT CLOSE

- **eg-1 (SERVED):** the guard runs where G4 is produced. The terminal vehicle (`OPAL_BBGTML_daily_pull`,
  `scheduled_daily_pull.cmd:477`) runs `python -m rivalfunds.enrichment_bloomberg --mode daily` from the shared tree, and that
  file equals `0997603f5d`. No Lambda runs the market pull, so the fix ships with no deploy (CTO~Z told, msg 29823 reply).
  - **Organic read: the 2026-10-06 vehicle.** On a live Terminal, G4 lands as before.
  - On a no-data Terminal, the result reads REFUSED, nothing is written and the prior revision stays newest.
  - Fallback: the pre-signed one-key restore.
  - An ad-hoc QA run is not possible tonight: BQL reads '#N/A Daily Capacity' (probes 23:11Z, 23:59Z), and the order forbids a
    vendor call from the check.
- **ok-1 (SERVED):** merged, NOT deployed. CTO~Z addendum 2 (A) sequences the deploy after the round-11 `_g5_target` fix and
  the served replay. J1 (one dialog and one ranking row each for Nebius, Broadcom and Intuit) therefore has no served artifact
  this round. **J1 is UNGRADEABLE in round 10 and moves to round 11.** Its positive control stands: the served 10-05 page
  shows Nebius twice, as `N97284108` and `NBIS_US_Equity`.
- **rp-2 (LOCAL):** the tool's dry report (`deliverables/0.9.0_WK_ETFS_RIVALS~3/g5_replay_dry.json`):
  - coverage: 182 dates, 419 (date, fund) pairs;
  - rows by class: key_resolution_out_of_confidence 1,040, full_exit_priced 266, own_prior_pairing 7,
    implausible_window_refused 10 (equal to gd-1); rows_moved 1,316, because 7 rows sit in two classes;
  - outside the classes: 0 rows; G3 label columns moved: 0; `s3_writes` 0.
  - **The served replay is HELD** (row Z-S42 disarms Z-W3-S23): `_g5_target` returns the existing object on a same-input
    `rebuild_funds` pass. Per addendum 2, the fix is round 11's cell 1.
- **iam-1 (WORLD):** applied 0/2/0 under the pair (COO `1c714fe3e2`, CTO `4e9b59ea50`).
  - My live simulate: names list/get and universe put/get are `allowed` on both roles.
  - The (c) controls (put on names, a sibling prefix) are denied, and the (d) positive control is allowed.
  - **Not yet proven: that data flows.** The first exercise is the 2026-10-06 07:00 ET marker publish (holding_contribution
    reads stored names) and the 09:00 ET sweep (build-security-universe writes).

## ROWS THIS ROUND

| row | class / standing | disposition |
|---|---|---|
| Z-S40 (AE) | BLOCKING / INERT | the iam-1 deliverables folder was unwritable by its own assignee; DISARMED by amendment `2553a624f7` (Z-S41) |
| Z-W3-S22 (WK~3) | OBSERVATION / INERT | the replay changes G1 provenance labels on 4,950 rows and fills 5,287 additive cells; the tool counts them apart from moves -- **the CVO confirms or refuses this reading of AC1 (b)** |
| Z-W3-S23 (WK~3) | OBSERVATION / ARMED | same-input `rebuild_funds` writes nothing and reads OK; DISARMED by issuer hold (Z-S42); fix = round 11 cell 1 |

## FOR THE CVO

- **Judgment to grade:** ok-1 J1 is ungradeable this round (no deploy, by ruling).
- **Your reading asked:** Z-W3-S22's provenance-label rule.
- **Cosmetic carry for round 11:** G5's unresolved-row label `NBIS US Equity` vs the A1 bucket `NBIS_US_Equity`.
- **The 10-06 reads** (ruling 6), graded in one read: eg-1 on the vehicle; iam-1's first data run; the nm-3 / D12 daily-leg
  items carried from round 9.
