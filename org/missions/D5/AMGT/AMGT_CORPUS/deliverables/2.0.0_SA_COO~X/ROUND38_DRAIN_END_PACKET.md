# AMGT_CORPUS round 38 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**STATUS: COMPLETE (7 of 7 cells terminal). HELD, not delivered: Andrew-direct 2026-10-06 ~13:4xZ (msg 30061, record @`f42219ebfe`) made the Bloomberg index-benchmark issue the singular priority for site Z. The packet goes to `3.0.0_SA_CVO~Z` when that priority lifts.**

| | |
|---|---|
| issuer | `2.0.0_SA_COO~X` |
| decomposition | v38.1 (`decompositions/AMGT_CORPUS_DECOMP.md`; issuance @`fcbe7aa0dc`, amendment @`c0ca84e4f6`) |
| source | `1.0.0_SA_CTO~Z` round-37 analysis @`b12904724c` s.4 (msg 29603); the FWD sweep ordered in msg 29786; an-2 run on CTO half AMENDMENT 1 @`dc3aa39ada` (msg 29870) |

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-an-1` count and ratio fields carry no currency (producer) | LOCAL | DONE, drained @`6f6e472641` | AC1 `crc derive build 1/1 control 2/2` (4 names: 1,253 count/ratio, 0 with a currency; money 1,324, unlabelled 0; values moved 0); AC2 4 passed; 69 currency/model_block tests passed; proof VALID. `IS_SH_FOR_DILUTED_EPS` -> `(None, "invariant")` via `_COUNT_RATIO_NO_CURRENCY_FIELDS` |
| `CRPS-an-2` re-derive the 96 + re-pin | SERVED | DONE, ledger `amgt-corpus-r38-an2` CLOSED @`d1b66b2562` (Branch A); pair COO @`fd7950348f` (corrected @`96be925c0f`) / CTO @`9b10587d25` + AMENDMENT 1 @`dc3aa39ada` | section 2 |
| `CRPS-an-3` the 2026-10-06 13:00Z fire, the first on `6f6e472641` | LOCAL (read) + one same-day pull | READ: the fire pulled 0 (Z-S88); the same-day pull on CTO ruling (a) landed 96/96, ledger `amgt-corpus-r38-an3-pull` CLOSED | section 3 |
| `CRPS-an-4` the /ui-walk walker closes the timeline day | LOCAL | DONE, drained @`54b6c70647` | AC1 `an4 build 1/1 control 1/1`; proof VALID; confirmed on 2 real walks (no day dialog over any tab shot) |
| `CRPS-an-5` today's recovery run of the refused 10-05 fire | LOCAL | STRUCK by `1.0.0_SA_CTO~Z` (msg 29870, AMENDMENT 1) | no MSTR~Z recovery line arrived; the 10-06 fire supersedes it (round-37 ruling 3) |
| `CRPS-an-6` FWD-20's currency limb on the page | LOCAL (read) | READ @`68a16106a0` | section 4 |
| `CRPS-an-7` the FWD sweep (9 stale or ungraded outcomes) | LOCAL (read) | READ: census @`c0ca84e4f6`, page @`8e5d45b2f4` | section 5 |

## 2. The SERVED act an-2 (`checks/round38/count_ratio_currency.py`, `an2_derive.py`)

| leg | result |
|---|---|
| L0 | Dry run over 96 at HEAD (producer == `6f6e472641`): `crc derive build 1/1 control 2/2`. Count/ratio with a currency 0 of 34,894; money unlabelled 0 of 31,985; values moved 0; labels changed 0; 96 puts captured, none sent. The plan names Python311 (live-task). |
| Ld | `LD derived 96 failed 0 of 96`, derived 2026-10-06 03:20-03:23Z on raw 2026-10-04 13:xxZ. `sa_fallback=False`, so 0 vendor calls. |
| Lr | REGISTERED. Start In `opal-pinned\amgt-induction-daily\6f6e4726414e`, Python311, daily 13:00Z. |
| Lv | `crc served build 1/1 control 1/1`: count/ratio with a currency **932 -> 0** of 34,894; money unlabelled 0 of 31,985. v35 redone 96, base values moved 0, pointer units 0. `al5 deployed build 1/1 control 1/1`. |

The served move disarms row `Z-W1-S35`.

## 3. CRPS-an-3 -- the 2026-10-06 fire and the same-day pull

**The 13:00Z fire on `6f6e472641` pulled nothing** (`evidence/r38_an3_fire_20261006.txt`, row `Z-S88` @`8aa3ea928f`):
- It returned rc 0 in 28 s, with all 96 names `already_current` and `bloomberg_calls 0`.
- The cause: `cmd_refresh` skips any name whose latest DERIVED stamp is today's UTC date, and an-2's re-derive at 03:20Z wrote
  exactly such stamps.

**The same-day pull** ran on CTO ruling (a), an-2 half AMENDMENT 2 @`80b915d9b5` (ledger `amgt-corpus-r38-an3-pull` CLOSED):
- Driver: `checks/round38/an3_same_day_pull.py`, run from the pinned checkout on Python311. The skip was bypassed run-scoped,
  with no code edit, and the run would have stopped on a -4001/LIMIT error.
- Probe: `health ok True` on `127.0.0.1:8194` (`r38_an3_probe.txt`).
- Pull: `already_current 0 pulled 96 bloomberg_calls 768`, rc 0, 0 failed, no STOP (`r38_an3_pull.txt`).
- Verification (`r38_an3_leg_v.txt`):
  - `crc served build 1/1 control 1/1`: count/ratio figures with a currency 0, money unlabelled 0;
  - pointer units 0;
  - `al5 deployed 1/1 + 1/1`.
- **Values moved: 2,276**, not the 0 in condition 3. That 0 was written for a re-derive from the same raw; this is a new pull.
  - 1,706 are forecast consensus (BEST_*).
  - 569 are header market fields (price, volume, market cap, beta, EV).
  - **1 is history: ORA FP FY2024 `IS_COMP_EPS_ADJUSTED` 0.82 -> 0.9613**, a Bloomberg revision.

**Round-39 cell (CTO, msg 30045):** the skip must key on the PULL date, not the derive stamp. The proof is a 03:00Z re-derive
plant after which the 13:00Z fire still pulls.

## 4. CRPS-an-6 -- `evidence/r38_an6_page_read.md`

**The walk:** signed in on portal DEV `7d1ea524`, walk `tmp/ui-walk/20261006T033542Z`. 92 shots, 0 guard aborts. The slot was
MSTR~Z msg 29881, DISARMED 03:41:20Z.

**The page:**
- On TSM US (TWD), SAP GY (EUR) and BA US (USD, the control), every money row of the Model tab's financial summary names its currency.
- "Diluted shares (millions of shares)" (SAP, BA) and "Shares outstanding, as reported" (BA) carry none.
- 2026E-2028E are all visible on SAP and BA; on TSM, 2028E is clipped at the card edge.

**Laid against FWD-20 for your grade:** TSM's "What changed" Enterprise value row reads "unit not resolved -- raw figure ...
currency not stated". It states its reason; BA's reads USD.

## 5. CRPS-an-7 -- the FWD sweep, for your whole-outcome grades (`evidence/r38_an7_census_reads.md`, `evidence/r38_an7_page_reads.md`)

The ledger-gap record is `FWD_LEDGER_GAP_20261005.md` @`d1acde2040`. Each outcome is exercised against its DONE WHEN; "not
exercised" names a limb the reads did not drive.

| FWD | observed | not exercised |
|---|---|---|
| 10 | IMB LN: 6 pillars, bold lead + paragraph, marked the team's, each with its source line | an opener to the report passage was not seen |
| 11 | IMB LN: the team passage, with a roster ABSENT-with-reasons. ASML NA: the team passage beside a 7-officer Bloomberg fallback roster | a name whose pack carries none |
| 12 | Rows from the summary, with empty lines reasoned. ASML NA: Base, Upside and Downside cases cited to the pack. IMB LN: "no ... case yet" for each | -- |
| 14 | 3 of 3 named folder reads answer, with a dossier or a reason. **The three counts sum to 96 of 97 folders**; Brookfield BN CA is unresolved outside all three | -- |
| 15 | IMB LN: the fund and position on the header (uncited) and on the Posture tab (cited) | machine verdict byte-unchanged |
| 16 | ASML NA (PDF): pillars, management and cases from the PDF pack. IMB LN (docx) control: pillars and management | the docx before-count |
| 18 | Terms readable on the pillars | the feed filtered to a term |
| 19 | 97 folders, not 93: 83 / 13 / 1 sum to 97; 12 never-prose named (the PRD counted 11) | -- |
| 21 | 2026E-2028E beside the history (SAP, BA, ASML); clipped on TSM and ASML at 1440 px | history byte-unchanged |

## 6. Rows

One row was filed this round, `Z-S88`, the issuer's own: an-2's early re-derive tripped the same-day skip of the 10-06 fire. The same-day pull restored the data, and the round-39 cell keys the skip on the pull date.

| row | change |
|---|---|
| `Z-W1-S35` | disarmed by an-2's served move |
| `Z-W1-S34` | stays INERT (round-37 analysis ruling 4) |
