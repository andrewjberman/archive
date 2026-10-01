# ETFS_RIVALS round 4 -- the COO's drain-end read (`/dispatch` step 6)

**Seat:** `2.0.0_SA_COO~RV`, 2026-10-01 ~22:5xZ. **To:** `3.0.0_SA_CVO~RV` (L8 compile, L9). **Risk:** WORLD (RIV-d-5 and its
addendum 1). **Source:** the round-3 analysis @d4a1e22801, items 1-4. **Decomposition:** round 4 v4.0. Fan-out 3 of 3 chains,
plus the d-5 join.

## Round state: 6 of 6 task orders terminal (complete, merged to CLOUD)

| order | slot | merged @ | criteria (issuer re-run) | reopened? |
|---|---|---|---|---|
| RIV-t-5 own-prior-date pairing | ~1 | 553866beaf | AC1 PASS. The check was amended @c17bb31c04: G5 has no row for a zero-trade window, so it reads G6 (rows W1-S28/S29) | -- |
| RIV-v-2 one revision contract | ~1 | b9ac3265ab, 7a922c536d, e92c2f5d28 | AC1-AC4 PASS | amendment 1: suite repair (S30/S31). Amendment 2: GQGU rows stamped `issuer-site:basg` (**Z-S9**) -> AC3. Amendment 3: the vehicle's enrichment step was a silent no-op (**Z-S10**, ARMED, from CRO~RV) -> AC4 |
| RIV-i-2 BASG issuer alias | ~1 | 7e537d4b5b | AC1 PASS (2026-09-30 BASG 33/33; control 34/34). S34 accepted: an alias-carrying G1 is its own revision | -- |
| RIV-q-1 GQGU issuer route | ~2, then ~1 | 014e381526, 9f18b52c62 | AC1-AC2 PASS | amendment 1: G2 stamped every issuer capture as BASG's (**Z-W4-S13**, ARMED; S12) -> AC2 |
| RIV-f-3 per-source identity floors | ~3, then ~1 | 91f5e09d9f, 1f09fac22b | AC1-AC2 PASS | amendment 1: d-5's committed floors turned 19 tests red (**Z-W4-S8**, ARMED) -> AC2 |
| RIV-d-5 live join (WORLD) + addendum 1 | ~4 | 623d245165, then d-5 complete 329e1176e7 | AC1-AC3 PASS after addendum 1. Before it, AC1 failed on GQGU: the calendar was unavailable (no G2 rows) and the config clause was the issuer's check defect (S11, amended @ba6af9b1d8) | addendum 1 (A1-A3) put the G2 fix live |

**Package suite at the last drain (CLOUD):** 306 passed, 2 skipped, 0 failed.

## The one real run at close (read by the issuer, 22:4xZ)

`s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-01/index.html` (917,070 B) and `manifest.json`, generated
22:03:35Z, batch `d5-publish-a1`:
- **13 funds; 12 updated.** Every fund block's calendar reads `ok`, and every fund carries its source badge:
  - `home_producer`: IDVZ, PFOE;
  - `issuer`: BASG, GQGU;
  - `bloomberg`: the other 9.
- **GQGU is served** (new this round) with issuer data, a calendar from its own G2 rows and an issuer badge. It reads
  **not-updated by report_date_freshness only** (latest report 2026-09-28 vs expected 2026-09-30, lag 2). Its archive ends on
  2026-09-28, and the daily route fetches T-1 (row S10).
  - **The acceptance is the 2026-10-02 07:00 ET issuer fetch, read at the close**, not waited on.
  - No backfill of 09-29/30 was in the cell or the halves.
- **No fund is not-updated by identity_coverage** under the committed per-source floors: issuer 0.23, bloomberg 0.99,
  home_producer 0.0, all PROVISIONAL.
- **AC2:** TSEL and WCMG served windows start on each fund's own prior report date (101 and 42 windows, 0 mismatched).
- **AC3:** G1 2026-09-29 GICS comes from the live G4 only, and BASG 2026-09-30 resolves 1.000 (33/33, via the `issuer-alias`).

## The served delta, measured per fund, and what moved

- **d-5** (`round4/served_delta_r4.py`, pin eb3f0cce93; re-run by the worker at gate 1, 13 of 13 equal):
  - GQGU: new, 305 dates and 10,798 G1 rows.
  - BIDD: one date at its newest capture (2025-12-09).
  - Own-prior windows: TSEL +2, ETFT/PCLG/WCMG +1.
  - BASG: alias labels only.
  - Every other fund: equal.
- **Addendum 1** (`round4/served_delta_g2.py`):
  - **Control:** the deployed module equals the served G2 on 4094 of 4094 keys.
  - **Fix:** GQGU 0 -> 307 G2 rows; BASG 645 -> 645; the other 11 funds equal; 0 cross-fund rows.
  - Read back after A2: 502 objects equal the table.

## Pairs and ledgers

- **d-5:** COO half @a10ebe8d92 + CTO half @a8913dccef (6 keys; key 3 "issuer floor 0.23 set by GQGU" signed as written).
  - Plan 0/5/0. Ledger `etfs-rivalfunds-round4` CLOSED.
  - The device identity is AdministratorAccess, so the negative control ran on the stage roles (S7).
- **Addendum 1:** COO half @ad07f847d2 + CTO half @1ef54f4ff8 (A1 Lambdas in place, A2 G2 replay, A3 republish).
  - Plan 0/5/0. Live base verified equal to d-5's apply before A1. Ledger `etfs-rivalfunds-round4-a1` CLOSED.
  - 0 rivalfunds sentinels open.

## Surprise rows this round (25 surfaced plus 2 issuer dispositions; all ARMED rows disarmed or bounded)

- **ARMED -> disarmed:**
  - W2-S11 by v-2 (issuer row Z-S11);
  - Z-S9 by v-2 amendment 2 (S35);
  - Z-S10 by v-2 amendment 3 (S36; the vehicle's next run does the designed daily enrichment pull);
  - W4-S8 by f-3 amendment 1 (S37);
  - W4-S13 by q-1 amendment 1 + addendum 1 (S38, S16). **Its live test is the 2026-10-02 07:00 ET fetch, BASG then GQGU.**
- **ARMED -> bounded:** W4-S9, the silver-triggered G1 replay over the 900 s ceiling.
  - It bites only on bulk batches; the daily batch is 1-2 dates (issuer row Z-S12).
  - The code fix is round-5 remediation.
- **Issuer check defects this round** (each caught by a failing worker run, never by the dry-run at base):
  - t-5.AC1 read G5 for a zero-trade window;
  - d-5.AC1 read the config's top level;
  - served_delta_g2 read 0 local rows (a partial `date=` prefix; caught before any result was used).
  - A check that FAILs at base is not proof it can PASS.

## Carried to the round-4 analysis (1.0.0_SA_CTO~Z), already named by the CTO

- **Rulings and spec:**
  - Hop-9 method rulings a/b/d @4baf852611;
  - PRD v0.8 @c168e72202 (signed by CVO~Z @18fca64073): IDVZ/PFOE to the Bloomberg leg, ACWI/IWM controls, the Bloomberg cost
    measure, the G9 style-read preview first.
- **Remediation from this round:**
  - a per-fund issuer floor (GQGU 0.2368 sets the issuer floor);
  - S9's bounded G1 replay;
  - the `extra_attributes` namespace still `basg` on GQGU rows (S35's neighbour; no page reader);
  - AC2's 353-382 s runtime (S14).
