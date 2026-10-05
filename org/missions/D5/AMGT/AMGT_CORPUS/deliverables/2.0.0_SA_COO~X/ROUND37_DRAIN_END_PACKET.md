# AMGT_CORPUS round 37 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`, 2026-10-05 ~14:0xZ. **Decomposition:** v37.0 @`ece32e98a6`.

**Source:** the `1.0.0_SA_CTO~Z` round-36 analysis @`4c3e3755a7` s.4 (msg 29335). Serves FWD-20: a currency on every money figure,
a reason for every gap inside a showing row. Also serves FWD-22's carried regression read.

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-am-1` every money figure carries its currency (producer) | LOCAL | DONE in two seats, drained @`3ffe37a57a` | AC1 `am1 build 1/1 control 2/2` on the amended check (905 -> 0 on TSM / 1299 HK / SAP / BA; 0 values moved; 0 labels changed); AC2 10 passed; **AC3 JUDGMENT is yours** (each field's side) |
| `CRPS-am-2` re-derive the 96 + re-pin | SERVED | DONE, ledger `amgt-corpus-r37-am2` CLOSED @`ab5337b876` (Branch A); pair COO @`7c72c86057` / CTO @`a8ccfc4f88` | section 2 |
| `CRPS-am-3` gap reasons + row currency on the Model tab (portal) | LOCAL | DONE, outer drain @`ff24d30809`. Portal `2e7c5cdb` (am-3 merged with DEV 6936e92b) CTO-APPROVED @`0bafb7d826`; on portal DEV on Andrew's "approved" @`b6361adaa5`; CI 37248822834 success | AC1 `am3 build 2/2 control 2/2`; AC2 `CHECKS-OK 12 of 12`; typecheck clean; DSGN battery29 ALL PASS. **AC3 JUDGMENT is yours** (section 3) |
| `CRPS-am-4` `induction_request --pick` writes nothing (row Z-W4-S4) | LOCAL | DONE, drained @`78e4bb3f11` | AC1 `am4 build 1/1 control 1/1`; AC2 3 passed; induction suite 43 passed after the issuer's drain fix to `test_fwd4_planted_drive` @`0eb01d2a0b` (row Z-W3-S12) |
| `CRPS-am-5` the carried read of the 2026-10-05 13:00Z fire | LOCAL (read) | READ @`2fea465183`: **REFUSED by Bloomberg's daily capacity**, not retried | 96/96 `LIMIT: Daily capacity reached`, pulled 0, rc 1. The first refresh had already failed. Cause owned elsewhere: `ETFS_RIVALS-Z-S24`. Row `Z-S87` |

`fanout: 3 of 3 worker chains, cap 8`.

**Issuer acts inside the decomposition:**
- **The issuer's own money rule was wrong** (row Z-W1-S33). It counted `ABSOLUTE (share count)` units as money, against am-1's item
  3. The rule now excludes any "(share count)" unit, amended in all three checks @`5a02ae8e98`. The base still FAILs; the branch
  reads 1/1.
- Slot ~1 was re-seated to close am-1.
- The am-1 drain conflicted on the append-only channel, resolved as a union (164 rows, ids unique).
- am-4's drain fixed a test outside the worker's paths.
- The am-3 candidate was merged with DEV before review.
- **The am-2 pin is `3ffe37a57a`, not HEAD.** HEAD carries HARVST at-4 (`store.py` `silver_append`). The half makes any producer
  change beyond am-1 a STOP. The re-derive at HEAD is equivalent: the derive uses only `store.table_prefix` / `entity_partition`,
  which at-4 does not touch.

## 2. The SERVED act am-2

| leg | result |
|---|---|
| L0 | am-5 read. Dry run at HEAD (producer equal to `3ffe37a57a`): 96/96, money 31,985, unlabelled 23,365 -> 0, reasoned 51, values moved 0, labels changed 0. Plan names Python311 (live-task) |
| Ld | 96/96 re-derived on their newest raw (2026-10-04; today's fire landed none), 0 failed, no vendor call, `field_map.json` unchanged |
| Lr | Start In `opal-pinned/amgt-induction-daily/3ffe37a57a83`, Python311, daily 13:00Z. The first fire on the new pin is 2026-10-06 13:00Z |
| Lv | Census over the 96 SERVED blocks: labelled 31,934, reasoned 51, **unlabelled 0** (TSM 227/228 + 1 reasoned). v35: base values moved 0, pointer-unit figures 0. `al5_served` deployed 1/1 + 1/1. Page: section 3 |

The 51 reasoned nulls are round 25's 42 held-out figures, plus 9 `CRNCY_ADJ_MKT_CAP` on the 9 names whose `CUR_MKT_CAP` round 25 holds
out. They inherit the same measured `UNMEASURED:` reason.

## 3. The real run -- `evidence/r37_am3_real_page.md`, `evidence/r37_am2_leg_v_page.md`

- **Gap reasons (FWD-20 limit 1), on the running page at DEV 2e7c5cdb (walk 20261005T005134Z, 1299 HK).** Every `--` inside a
  showing row carries footnote mark 1, with a hover title. The note reads once: "The price-dated range is not reported at this
  company's fiscal year end, because its fiscal year does not end in December."
- **Currency (FWD-20 limit 2).** The deployed `/thesis` TSM payload carries 200 of 200 money figures with a currency (TWD). Through
  the real `modelSheet.ts` at DEV, **13 of 13 money rows name a currency** (at the cut, 1 of 13).
  - The page walk for TSM (20261005T135401Z) was occluded: the news-timeline day popup opened at step 005 stayed open over every tab
    shot. That is a walk-instrument finding for the /ui-walk owner. The seam read stands in for it.
  - One walker slot was lost to my own start command (the server never came up). The slot was announced and released through
    MSTR~Z.

**For your judgments:**
- **am-1 AC3:** each field's side. Every TSM money row reads TWD, including per-share EPS and DPS on a USD-quoted ADR.
  `HISTORICAL_MARKET_CAP` is labelled reporting against its basis text (row Z-W1-S34).
- **am-3 AC3:** the page.

## 4. Rows, and what the round-37 analysis receives

| row | standing | what |
|---|---|---|
| `Z-W1-S33` | was BLOCKING | the issuer's check counted share counts as money; disarmed @`5a02ae8e98` |
| `Z-W1-S34` | OBSERVATION | `HISTORICAL_MARKET_CAP`: the basis text says trading currency, but the landed values read on the reporting scale (BABA 7.89x, JD 7.81x CNY/USD; 1299 HK 0.15x) |
| `Z-W1-S35` | OBSERVATION | `IS_SH_FOR_DILUTED_EPS`, a share count, keeps the reporting currency it already carried (rule 4) |
| `Z-W3-S12` | was ARMED | the planted-drive test read the old default write; disarmed at the drain @`0eb01d2a0b` |
| `Z-S87` | OBSERVATION | the 10-05 fire refused by Bloomberg daily capacity (cause `ETFS_RIVALS-Z-S24`) |

**Candidates for round 38, mine to name and the CTO's to rule:**
1. FWD-22's regression read moves to the 2026-10-06 13:00Z fire, the first on pin `3ffe37a57a`: 96 pulled, rc 0, census unlabelled
   still 0.
2. Rows Z-W1-S34 and S35: a ruling on `HISTORICAL_MARKET_CAP`'s side, and on whether a share count should carry a currency.
3. HARVST at-4 reaches the daily task at the next pin, under its own pair.
4. The /ui-walk day-popup occlusion goes to its owner, so the next page read can see the Model tab.

Push state: LOCAL (ls-remote read at commit time).
