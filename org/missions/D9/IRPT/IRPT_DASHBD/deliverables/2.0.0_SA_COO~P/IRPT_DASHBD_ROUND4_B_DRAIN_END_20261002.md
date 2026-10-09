# IRPT_DASHBD round 4, workstream B -- drain end (one cell: DB-b-10, the Black Diamond like-day pull)

Author `2.0.0_SA_COO~P`, 2026-10-02 ~18:0xZ. For `3.0.0_SA_CVO` (L8 compile, L9 on FWD-8).

## The round

| cell | order | status | merged | criteria (issuer re-run) |
|---|---|---|---|---|
| `DB-b-10` | `IRPT_DASHBD.TO-DB-b-10.black-diamond-like-day-pull.md` | complete | @8b1df51795 (worker @a34108a065) | DB4-1-AC1 PASS, DB4-1-AC2 PASS; proof VALID rc=0 |

**Authority:** ANDREW-DIRECT ~13:2xZ "all recs approved", card 4 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261002_132xZ_ALL_RECS_APPROVED_OPEN_CALLS.md`,
@0abef798f7). The word allowed ONE pull, the five round-1 accounts, Opal's gap-free segments, and is not a standing grant.

## The real run (the pull is the run)

- **Vendor calls:** 3 `performancePeriod` POSTs, all HTTP 200, with 0 retries and 0 `performanceSeries`. The client also made 1
  GET `/session/token` to mint the bearer, which the estate's client cannot avoid. That companion is recorded as row
  `IRPT_DASHBD-W1-S11`.
- **Before calling:** the plan (segments and request bodies) was built and printed offline (`BD_LIKEDAY_PLAN_R4.json`). The live
  run refused to call unless the rebuilt plan equalled that file.
- **Accounts:**
  - mapped: acct#89d0916a (BD 22596361), 0076459710 (BD 23221671), 0084073310 (BD 22659431);
  - unmapped: 0035940058 and 0091939812, both `pending_resolution` in the roster with no BD id. Neither was called, and no id was
    guessed.
- **Tie-out:** 14 pairs, every one gap-free by `lib/trading_calendar.py`. **14 of 14 are like-day pairs**: BD's `daysHeld` equals
  Opal's linked days on every window, with no systematic offset.
  - `abs_diff` median **0.001637** (0.16%), max **0.012130** (1.21%, acct#89d0916a over 2026-06-25..07-06, 7 days).
  - Per pair: `deliverables/0.9.0_WK_IRPT_DASHBD~1/TIEOUT_49F_BLACKDIAMOND_R4.{json,md}`.
- **Records:**
  - `BD_LIKEDAY_PULL_R4.json`;
  - `bd_likeday_pull_r4.py`;
  - three raw responses `RAW_BD_PERIOD_<account>.sanitised.json.gz`. The account name is replaced. The issuer read every `name`
    value left: security and benchmark names only. The unsanitised hashes are in the `.md`.
- **No credential, cookie or token** is in any record. The issuer scanned the pull record.

## For the CVO

FWD-8 can now be graded on agreement over like day sets (PRD v0.6 ruling 23): round 1 had 0 such pairs, this round has 14. No
tolerance was ruled from round 1 (ruling 23 refused 3.7%), so the grade's bar is the CVO's judgment at L9.

**Row to read:** `IRPT_DASHBD-W1-S11` (the token mint; 0084073310's first segment precedes the roster `trade_start_date`, and BD
agrees with the gold over it).

**Not done:** P-5, the population tie-out, needs a further vendor word from Andrew (CTO batch 178).
