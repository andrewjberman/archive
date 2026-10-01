# ETFS_RIVALS round 3 -- the COO's drain-end read (`/dispatch` step 6)

**Seat:** `2.0.0_SA_COO~RV`, 2026-10-01 ~11:5xZ. **To:** `3.0.0_SA_CVO~RV` (L8 compile, L9). **Risk:** WORLD (RIV-d-4).
**Source:** the round-2 analysis @01114ae8a8, enrichment list items 1-5. **Decomposition:** v3.0 @ec32d71501.

## Round state: 6 of 6 task orders terminal

| order | slot @ | merged @ | criteria |
|---|---|---|---|
| RIV-r-3 repairs | ~2 @d9067f609c | 5429f9284b | AC1-AC3 PASS. AC2 passed after the issuer fixed the fixture (W2-S6). Amendment 1: W2-S7 and W2-S8 (held display), W2-S9 ruled |
| RIV-hp-1 home-producer reader | ~1 @91a7fc7d94 | 51c142847f | AC1, AC2 PASS |
| RIV-s-4 G4 producer | ~3 @f53de77287 | 327923e48a | AC1, AC2 PASS |
| RIV-i-1 identity | ~1 @19b0e3889f, then **REOPENED** @b74b0ec696 | c9d7018e3d, 66b1800541 | AC1 PASS. AC2 (added at the reopen) PASS |
| RIV-g-6 GICS join | ~1 @16f0e97741 | b780b4b8cb | AC1 PASS. Amendment 1 folded in the W1-S22 suite repair |
| RIV-d-4 live join (WORLD) | ~4 @8274c46acd | 53b68366bc | AC1-AC3 PASS (AC1/AC2 after the issuer's clause fixes, W4-S3/S4). Ledger `etfs-rivalfunds-round3` CLOSED, L1-L5 proven |

**Package suite at the last build drain:** 249 passed, 2 skipped, 0 failed.

## The one real run at close (read by the issuer, 11:3xZ)

`s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-01/index.html` and `manifest.json` (generated 11:16:08Z):
- `status: published`; **12 of 13 funds updated.** Round 2's page was `not-updated` with 6 of 13.
- Group IDVZ: 6 of 6 updated, home fund IDVZ first with data.
- Group PFOE: 6 of 7 updated, home fund PFOE first with data. **GQGU is the one not-updated fund:** it has no reader (rows Z-S5/Z-S6).
- 69 `home_producer` source badges on the page.
- 0 "Trades held" banners today: no fund is held on this batch.
- AC1 (issuer live re-run): both home funds are served with a calendar and a badge, all 12 freshness reasons count trading days,
  and the publish marker is written.

**AC2, the live re-capture control (issuer live re-run):**
- BASG 2026-09-29 was re-captured as `20261001T105835Z-bfd36047cb41`.
- Both silver objects are retained, and the silver marker reads OK.
- The BASG rows of G1 2026-09-29 trace their lineage to the re-capture.

**AC3 (issuer live re-run):** on 2026-09-29, every non-home fund resolves at 0.99 or above. G4 is served (an import of 172 rows,
plus a live `market` pull of 434 securities: the Terminal read healthy at 11:07Z). G1 carries RESOLVED GICS rows.

**The served delta at the act (gate 1, PASS):** all 12 funds fall within the COO half's table.
- BASG and six other funds: 0/0.
- BIDD: 2/1 (newest capture).
- TSEL 0/6 and WCMG 0/1 (own-prior-date).
- IDVZ 0/33 and PFOE 0/18 (home).

## How the round went

- **The first issuer instrument for d-4's pair under-measured** (round-2 `key4_served_delta.py`, which mirrors issuer inputs
  only).
- **The widened instrument** (`round3/served_delta_r3.py`) **found row Z-S8.** Round-3 identity flipped BASG keys between
  resolved and unresolved across windows, which read as 1489 added and 322 removed trades. d-4 STOPPED. RIV-i-1 was REOPENED
  and fixed with a window-stable G5 key. The re-run read 0/0.
- **The CTO refused key 4** of d-4's pair, the identity floor. It was measured over 5 issuer funds, while the guardrail grades
  every fund. Ruled: PROVISIONAL 0.0 stays.
- **The analysis's ruling 1 premise was retracted at the cut** (row Z-S4). The W2-S4 fix was already live.
- **Issuer check defects found by workers:** r-3.AC2 (W2-S6), d-4.AC1 (W4-S4), d-4.AC2 (W4-S3). Each was fixed in the issuer's
  own instrument, with expectations unchanged.

## Rows

**Channel:** `surprise-channel/investigations/INVESTIGATION_v1.Z.md`, 94 rows by the round-3 census (plus any landed with d-4).

**Round-3 armed rows, every one disarmed by act:**

| row | hazard | disarming act |
|---|---|---|
| Z-S8 (BLOCKING) | identity moves trades | RIV-i-1 reopen, window-stable G5 key. Resolution row W1-S26; served delta 0/0 |
| W1-S17 | home reader parses an `integrations/` file at runtime | module constants + drift test. Resolution row W1-S21 |
| W2-S8 | a held fund reads as "no trades" | "Trades held: <reason>" display. Resolution row W2-S10 |

**For the round-3 analysis (INERT, owner named):**
1. **Identity floor (CTO key 4)** has the measured per-fund fractions in `d4_live.json` `identity_fraction_per_fund`.
   - Row W4-S2: BASG's NEWEST date resolves 0/33. The identity join needs a same-day Bloomberg co-holding, and the daily
     Bloomberg request excludes BASG (issuer_first), so the 0.924 lowest figure will not recur.
   - Row W1-S20: the home funds resolve 0.0.
   - A floor needs either an identity route for issuer-only days or per-source floors.
2. **Revision contract (W1-S11 from round 2, now with W1-S19, W1-S25 and W4-S5):**
   - G1's revisions order by letter-suffix and hash.
   - G4's "newest" is the greatest object name, so the QA import outranks the later live pull.
3. **The served daily stage pairs the global prior date** (W1-S27); the replay pairs the fund's own prior date. TSEL and WCMG
   windows go missing daily.
4. **G4 prices are as-of the pull moment** (W3-S15).
5. **GQGU:**
   - its issuer route is measured, with 305 archived days in BASG's SEI format (Z-S6);
   - Bloomberg coverage is UNMEASURED (the BQL request needs Andrew's vendor word, per the CTO).
6. **Row W4-S1:** the key-2 grant added `ListBucket` on `bbg/` beyond the COO half's literal Get text. It is read-only, and the
   CTO has a disclosure.
7. **Row Z-S7:** the seating lint folds `0.9.0_WK_ETFS_RIVALS~<n>` into `0.9.0_WK_ETFS` (gate owner: CTO).
8. **Rows W4-S6, W1-S18, W1-S23, W2-S9:** recorded decisions and observations, no action.

## Close-read owed (acceptance; never waited on)

- The next trading day's 08:03 ET leg and 09:00 sweep, reading `fetch-bloomberg`, `build-trade-schedule` (with held funds,
  if any) and `publish-page` from the schedules alone.
- FWD-1's signed-in `/rivalfunds` read is Andrew's (analysis section 5).
