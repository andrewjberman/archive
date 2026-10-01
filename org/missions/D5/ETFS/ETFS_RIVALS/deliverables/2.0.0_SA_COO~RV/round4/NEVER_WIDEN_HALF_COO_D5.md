# NEVER-WIDEN -- COO HALF: the ETFS_RIVALS round-4 live join (`RIV-d-5`)

The act:
1. Deploy in place.
2. Import GQGU's 305 archived days as issuer bronze.
3. Set the per-source identity floors.
4. Replay G1, G5 and G6, then publish.
5. Read the page.

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-01. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Serves:**
- PRD `org/missions/D5/ETFS/ETFS_RIVALS/prd/ETFS_RIVALS_PRD.md`;
- the round-3 analysis @d4a1e22801, items 1-4;
- task order `ETFS_RIVALS.TO-RIV-d-5.live-join-round4`.

**Andrew-direct, binding** (record `deliverables/2.0.0_SA_COO~RV/ANDREW_DIRECT_20260930_20xxZ_DO_NOT_MODIFY_POSITIONING_PULL.md`):
- *"do not modify the existing daily etfs pull for Positioning"*;
- *"Anything we do for this would have to be additive"*.

This act READS the Positioning landings. It writes nothing under `bbg/` and edits no Positioning file. It makes no Bloomberg
request: GQGU's BQL stays withdrawn.

**Code pin:** CLOUD at the drain of the RIV-v-2 reopen (amendment 2, row Z-S9), or a descendant. That pin carries every round-4
build: t-5, v-2 with amendments 1 and 2, i-2, q-1 and f-3. The worker prints `git log --oneline -3` first.

## VERDICT: SIGNED (2026-10-01 ~16:4xZ, at pin CLOUD eb3f0cce93)

## THE SERVED DELTA, MEASURED (not predicted)

**Instrument:** `round4/served_delta_r4.py`, which is round 3's instrument widened to GQGU and G6.
- **Mirror:** it mirrors EVERY served input, read-only:
  - issuer silver 327 and issuer sidecars 327;
  - Bloomberg silver 3619;
  - G3 1;
  - home landings 28;
  - G4 from `bbg/2026-09-30/characteristics.parquet`.
- **GQGU:** it lands the 305 GQGU archive days locally with `land_bronze(..., fund="GQGU")` at their own capture time. All 305
  are OK, under bronze date 2026-09-29.
- **Replay:** it replays silver, G1, G5 and G6 into a local sink.
- **Diff:** it diffs PER FUND against the newest served object per date. Trades are keyed identity-independently on
  (window_end, action, shares_delta), and G6 on (window_start > window_end).
- **No S3 write:** S3 holds no `gqgu-*` silver after the run, which confirms it. The control is BASG's object at the same
  `date=`, which is present.

**Runs:**
- At CLOUD 7e537d4b5b: `round4/served_delta_r4.json`, committed @2be56969b2.
- The re-run at the pin is recorded at the foot.

| fund | G1 rows served -> new | G5 removed / added | G6 windows served -> new | class |
|---|---|---|---|---|
| BASG | 11306 -> 11306 | 0 / 0 | 325 -> 325 | **alias labels**: the 2026-09-30 non-cash rows resolve 33/33 by `issuer-alias` (i-2); no row or trade moves |
| CGIC, INEQ, TXUE, SCHY | equal | 0 / 0 | equal | none |
| BIDD | 20769 -> 20768 (1 date) | 2 / 1 | 464 -> 464 | **newest-capture**: 2025-12-09 has two Bloomberg captures, 151237Z (46 rows, served) and 151241Z (45 rows). The new code reads the newer one by the v-2 contract. The 2025-12-09/11 trades follow it (trim -> exit). This is the same class and count signed in round 3 |
| TSEL | equal | 0 / 7 | 392 -> 394 | **own-prior-date** (t-5): new windows 2025-08-15 > 2025-10-09 and 2026-09-28 > 2026-09-30 |
| ETFT | equal | 0 / 0 | 205 -> 206 | own-prior-date: 2026-09-28 > 2026-09-30, a zero-trade window |
| PCLG | equal | 0 / 1 | 224 -> 225 | own-prior-date: 2026-09-28 > 2026-09-30 |
| WCMG | equal | 0 / 1 | 90 -> 91 | own-prior-date: 2026-09-28 > 2026-09-30 |
| IDVZ, PFOE (home) | equal | 0 / 0 | equal | none |
| GQGU | 0 -> 10798 (305 dates) | 0 / 1280 | 0 -> 304 | **new fund by design** (q-1). Newest report 2026-09-28: 38 non-cash rows, 9 by `issuer-alias`, 29 crosswalk misses, resolved 0.2368 |

- **Replay window:** all funds 2025-07-14..2026-09-30. Excluding GQGU, the changed dates are 2025-10-09, 2025-12-09, 2025-12-11
  and 2026-09-30.
- **Labels only:** G1 also gains `issuer-alias` resolution labels on BASG's issuer-only dates. Per S34, an alias-carrying G1 is
  its own revision, so the replay writes a NEW newest G1 object for those dates and keeps the old ones.
- **Re-run gate:** **anything at the act beyond these classes STOPs it as an unexpected served delta.** The worker re-runs
  `served_delta_r4.py` from the act's worktree BEFORE the first apply and compares per fund to this table. A non-GQGU fund
  outside its row's counts STOPs. So does a GQGU row whose `source_channel` is not `issuer-site:gqgu` (row Z-S9).

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| 1 | the five stage Lambdas | round-3 code (source map at d-4's apply) | in-place `source_code_hash` update to the round-4 package. No create or destroy | re-apply at the prior source map, same window |
| 2 | issuer-site bronze + silver for GQGU | 0 `gqgu-*` objects | +305 bronze captures and sidecars (`gqgu-<requested_date>-<ts>-<sha12>`, bronze date of the archive's capture time), then silver by marker: one `gqgu-*` object per report date. QA-class with provenance. The writer is the device identity; its PutObject on `issuer-site/etfs/bronze/holdings/` is MEASURED with the IAM simulator before the first landing, and DENIED STOPs step 2 | a delete is a HUMAN word |
| 3 | `guardrails_config.json` `min_resolved_fraction` | every source PROVISIONAL 0.0 | per the cell rule (the minimum newest-date resolved fraction of the source's funds, rounded DOWN): **issuer 0.23** (GQGU 0.2368; BASG 1.0), **bloomberg 0.99** (SCHY 0.9905; others 1.0), **home_producer 0.00** (IDVZ 0.0, PFOE 0.0), all still PROVISIONAL, in one commit | revert the commit |
| 4 | gold G1, G2, G5 and G6, and the platinum page | round-3 revisions | NEW revision objects only, never an overwrite: GQGU's dates, the alias-revised BASG dates, BIDD's newest-capture dates and the own-prior windows above, then a publish | same |
| 5 | the daily `fetch-holdings` run | BASG only on the issuer route | BASG + GQGU: the deployed map sends GQGU's 07:00 fetch to `gqg.filepoint.live` (egress to the issuer's public site, BASG's twin; no IAM change) | key 1's rollback |
| 6 | state markers | round-3 markers | new batch markers for the import, the replay and the publish | same |

**Writers counted:**
- **Key 1:** `safe-apply` only.
- **Key 2:** the device identity, which lands bronze, plus the build-silver stage role.
- **Key 3:** this act's one commit.
- **Keys 4 and 6:** the stage Lambdas, one role per stage.
- **Key 5:** the fetch-holdings Lambda on its schedule.

**Disclosed for the CTO's half -- key 3's issuer floor:**
- Under the cell rule GQGU sets the issuer floor at 0.23, so BASG (1.0 today) is held only to 0.23 as well.
- The rule is the ratified cell's, and this half signs it as written.
- A per-fund issuer floor is not in `resolved_floor()` today: it has per-fund entries only for `home_producer`. Making BASG's
  floor its own is an enrichment candidate for the round-4 analysis, not a rider on this act.

**Unmoved** (the act must not touch):
- `bbg/` and the Positioning pull (READ only);
- the vehicle;
- `etfs-netassets-daily`;
- `opal-data-assets`;
- the bucket's tier-first keys;
- the gateway: no deploy;
- any IAM role other than one a half names. None is named, so a role change in the plan STOPs.

## ACT-START GATES (the worker STOPS with a BLOCKING row on any)

1. **The served-delta re-run matches the table**, per fund (above).
2. **The plan is in place only:** five `source_code_hash` updates.
   - Any create, destroy or replace STOPs.
   - So does any policy change or any change to a non-rivalfunds resource.
   - **Any action the generator adds that neither half names is DISCLOSED to both signers BEFORE the apply** (CTO forward
     condition, addendum @5247bfbb2d). It is not applied until one of them answers.
3. **The IAM simulator allows key 2's PutObject** for the device identity. The control is a Put on an unrelated prefix, which
   stays DENIED.
4. **NEVER-2:** the ledger entry `etfs-rivalfunds-round4` and its sentinel are committed before the first apply, after the union
   read over every live worktree, with the per-tree denominator printed.
5. **Rows:**
   - Z-S9 is RESOLVED at the pin.
   - W2-S11 is DISARMED: v-2.AC2 holds BASG 35 and GQGU 35 in one G1.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES, BOTH BRANCHES

- **GQGU on the page:** the page shows GQGU with issuer data, and its rows carry `source_channel` `issuer-site:gqgu`.
  `identity_coverage` grades GQGU at its source floor:
  - **Branch A**, its newest report resolves at or above 0.23 (0.2368 measured): the fund is updated.
  - **Branch B**, a newer GQGU report resolves below 0.23: the fund reads not-updated by `identity_coverage`. The act completes,
    and d-5.AC1 FAILs on that fund, which is recorded as a row. The floor is not lowered at the act.
- **Own-prior windows:** TSEL's and WCMG's served windows in the replay window start on each fund's own prior report date.
- **BASG:** its newest report date resolves 1.0 (d-5.AC3 needs at least 0.90). G1 2026-09-29 takes GICS from the live G4 only.
- **Acceptance:** the next trading day's 07:00 issuer fetch for both funds, the 08:03 leg and the 09:00 sweep are the
  acceptance, read at the close.

## ROLLBACK

- **Keys 1 and 3:** as the table says, in the same window.
- **Keys 2, 4 and 6:** new objects or revisions that nothing else reads. A delete is a HUMAN word, never the worker's.
- **Key 5:** rolls back with key 1.

## PIN

- **Pin:** CLOUD **eb3f0cce93**. It descends from the RIV-v-2 amendment-2 drain 7a922c536d, which is checked with
  `merge-base --is-ancestor`, and `tests/test_v2_source_channel.py` is present at HEAD as a positive control.
- **Re-run:** `round4/served_delta_r4.py` at the pin gives `round4/served_delta_r4_pin.json`, rc=0.
  - It mirrored the same inputs: issuer silver 327 and sidecars 327, Bloomberg silver 3619, G3 1, home landings 28, G4 from
    `bbg/2026-09-30/characteristics.parquet`, and GQGU 305 days landed.
  - **13 of 13 funds are equal to the table on every counted field** (G1 rows, rowcount-differing dates, new-only dates, newest
    date and resolved fraction, G5 removed/added, G6 windows). 0 differ.
  - The replay window is 2025-07-14..2026-09-30. Excluding GQGU, the changed dates are 2025-10-09, 2025-12-09, 2025-12-11 and
    2026-09-30.
- **Source channel, newest date, per fund:**
  - BASG: `issuer-site:basg`.
  - GQGU: `issuer-site:gqgu`, so row Z-S9 is resolved at the pin.
  - IDVZ and PFOE: `positioning-landing:constituents_issuer_fill`.
  - The 9 Bloomberg funds: `bloomberg:holdings`.
