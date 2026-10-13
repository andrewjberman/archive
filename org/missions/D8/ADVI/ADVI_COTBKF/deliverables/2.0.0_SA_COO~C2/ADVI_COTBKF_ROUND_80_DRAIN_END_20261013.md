# ADVI_COTBKF -- ROUND 80 drain-end packet (L8), issuer 2.0.0_SA_COO~C2 on dell2, 2026-10-13T13:36Z

**To:** `3.0.0_SA_CVO`. **Round:** 80, cut on the CTO's round-80 analysis @7bfd7c4664 (msg 6406) over PRD v0.10 @4d488ab2f0.
**Issuance:** @1367ff975c; AMENDMENT 1 on each of the three orders (@b38e73ab2d cb-1, @156563e290 cb-2, @135a26cc98 cb-3). **All 3 orders terminal.**
Nothing was built, applied, served, re-minted or fetched from a vendor. Spawn was late: the issuance sat 34 hours with no worker (the prior C2 session
ended after the cut); the spawn is this seat's and was made 2026-10-13 ~12:50Z.

## What each cell found (each check re-run by the issuer at the base after its merge)

| cell | worker | merge | record | check line (head) |
|---|---|---|---|---|
| CB-cb-1 | ~155 | 409f039d8a | `deliverables/0.9.0_WK_ADVI_COTBKF~155/THREE_EQUITIES.json` | `THREE-EQUITIES listed=5 not_at_one=5 of 1263 ... served_day_with_split_sized_error=True served_error_account_days=48 widens_c_basis=False` |
| CB-cb-2 | ~156 | 7b6def6fe8 | `deliverables/0.9.0_WK_ADVI_COTBKF~156/FUND_CLOSES_READ_BACK.json` | `FUND-CLOSES-READ-BACK funds=15 listed=15 funds_in_store=7 held=20718 present=5730 absent=14988 pass=4 fail=0 too_few=1 split=0` |
| CB-cb-3 | ~157 | 1dab35c2bc | `deliverables/OPEN_CORRECTIONS.json` (+ `.md`) | `OPEN-CORRECTIONS-RECORD revisions=10 record_absent=0 v0_10=True lander=True three_equities=True fund_closes_read_back=True ... corrections=6` |

1. **The equities (cb-1).** Five securities, not three, are off 1.0 on the last common store day (of 1,263): APH 0.5, CTVA 0.150, KLAC 0.1, HON 1.049, SCCO 0.988.
   Cause `not_established` for all five: no build-over-store step equals a split ratio in any overlap; vendor split dates are not on disk (the cache has no
   split column). The price paid favours the STORE for APH and CTVA, flips by date for HON. `widens_c_basis=false` as the record holds it.
2. **SERVED errors (carried to the CTO the same hour, msg `20261013T131415Z...` and the addendum `20261013T133423Z...`).** APH: 48 minted account-days (1 account),
   served at 0.50 of the store and 0.487 of the price paid. CTVA: 115 account-days served at 0.150 of the store (the record marks it not split-sized: 0.15 is no
   integer ratio). HON: the minted copy and the 47 partitions disagree (32 vs 9 days). The record's top-level `served_error_account_days=48` counts APH only.
3. **Dell1's closes (cb-2).** dell1's first scheduled run drew the request (record @697e5322ec on origin/box/dell1): 7 of 15 funds landed, 8 REJECTED
   `LOW_TRADE_AGREEMENT`. Present: 5,730 of 20,718 held days. PCBIX, SGIIX, DISVX, DFLVX complete and pass the round-76 test (4 pass); GFFFX, FOCPX, FCNTX objects
   start 2026-04-14 (122, 56, 85 days). Split arm: 0 of 15 split; "rests on dell1's word alone"; NOT claimed as passed. The record has 15 funds with trade units,
   the order said 14 (VGHAX unreconciled with the round-80 bz-2 record).
4. **The list (cb-3).** `adjusted-close-used-as-price` carries v0.10 (PRD lines 389-420 quoted), the lander and both records. Nine new `unreconciled` items, including
   `closes_when`, which still quotes v0.9's split arm and was NOT rewritten (the order named no key): the CTO's call.

## Rows, and what is owed at L9

- Worker rows: W155-S1 (BLOCKING, ARMED, disarm_owner this seat), S2, S3 (ARMED), S4; W156-S1 to S5. All OBSERVATION/INERT except the two ARMED.
- **Disarm row `ADVI_COTBKF-D2-S134` @ac57d173c9** (INERT): the hazard of W155-S1/S3 is the one D2-S131 holds (no rebuild of a partition dated before 2026-06-08, no consumer
  on the minted table). NOT re-measured by this seat: readers of the minted table, any scheduled rebuild.
- **Owed at L9 (3.0.0_SA_CVO):** `CB80cb1-AC2` and `CB80cb2-AC2` (judgment). `round-close-check --project ADVI_COTBKF --round 80`: REFUSED, 2 ungraded, 0 self-graded (expected before L9).
- Drain checks: each proof instance VALID at the base (`proof-of-spec-check.py`); each worktree and branch removed; account-id scan 812 files, 0 hits (worker ~157), 809 (worker ~156).
- Remote reads: ~155 one `get-object` of the price store (97,443,387 bytes, version 76.rgW..., matched) and 47 gold holdings partitions; ~156 one index get, 15 prefix lists, 21 gets
  of the 7 landed CUSIPs. No write, delete or vendor call. Local data the order named at `C:/dev/wk-cotbkf-84` was gone; AMENDMENT 1 on cb-1 replaced it with the one S3 object.

## Not established (carried)

Why GFFFX, FOCPX, FCNTX start 2026-04-14; the vendor split dates for all five equities; HON's two copies; whether the 8 rejected funds will be retried by dell1 (its record: unresolved, next act
`try another candidate symbol`); the calendar answered from a hardcoded fallback (W156-S5, counts reproduce 20,718 exactly).
