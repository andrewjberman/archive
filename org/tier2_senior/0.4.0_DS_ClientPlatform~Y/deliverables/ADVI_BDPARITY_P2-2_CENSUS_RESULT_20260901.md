# ADVI_BDPARITY P2-2 -- the 5,309-account performance-feed parity census

**Seat:** `0.4.0_DS_ClientPlatform~Y` | **Completed:** 2026-09-01T04:1xZ | **Feed:** `performance` ONLY
**Authorisation:** Andrew-direct 03:4xZ, verbatim *"you have vendor egress yes, granted, talk with COO
and lets get this done"*, relayed `1.0.0_SA_CTO` 90604, both limbs discharged `2.0.0_SA_COO` 90614.
**Graded against:** `3.0.0_SA_CVO` 90610's four criteria, pre-registered BEFORE the run.
**Shape ruled by:** `1.0.0_SA_CTO` 90702 -- SELF-INVALID is a PRIOR GATE, not a parity band.

---

## THE STANDING SENTENCE

> **Performance-feed parity is MEASURED at n=15,445 cells over 5,309 accounts, with 1,994 LARGE
> cells (1,516 of them not explained by coverage) remaining open. NOT "parity proven."**

⭐ **AND THE LEAD, ratified by `1.0.0_SA_CTO` 90702 s.4 and `3.0.0_SA_CVO` 90686 s.2:**
**The census is a TWO-WAY AUDIT and it is currently finding more on OUR side than on BD's.** The
harness was built to check BD's numbers against ours. It caught ours.

---

## 1. TWO DENOMINATORS, NEVER ONE (criterion 1)

```
  accounts pulled                          5,309 of 5,309   (100%)
  cells attempted (accounts x 3 periods)  15,927
  ------------------------------------------------------------------
  cells COMPARED  -- the parity population 15,445
  cells WITHHELD -- withdrawn, OURS           112  over 61 accounts
  cells UNAVAILABLE-NO-LINKABLE-DAYS          370
  ------------------------------------------------------------------
  15,445 + 112 + 370 = 15,927   RECONCILES EXACTLY
```
⛔ **LABEL CORRECTED AFTER FIRST PUBLICATION. The withheld 112 are "WITHHELD PENDING PER-ROW
DISPOSITION", NOT "SELF-INVALID"** -- `2.0.0_SA_COO` 90727 (C) ruled that the token must not be
minted before the rows are read, and **my first version of this table asserted invalidity the
evidence had not yet established.**
⛔ **AND THE READ HAS SINCE SHOWN THEY ARE NOT ONE POPULATION -- ~21 OF THEM ARE NOT A DATA DEFECT AT
ALL** (`3.0.0_SA_CVO` 90742 s.4). Class **B** is a REAL recorded flow against a base too small to
divide by: **the percentage is meaningless but NO DATA IS MISSING.** That is a metric/presentation
problem with a different owner from class A's missing flow. **Counting all 112 as "broken cells"
would overstate the data defect by roughly a fifth and point remediation at the wrong producer.**
See section 5 for the A/B/C split.
**ATTEMPTED != COMPARED, and the shortfall is named rather than absorbed.** The 112 SELF-INVALID
cells never received a parity class: per `1.0.0_SA_CTO` 90702 they were screened out on OUR OWN
invariants BEFORE any comparison ran, because a cell whose own figure is impossible was never on the
parity axis. They are a PRODUCER finding with their own denominator (section 5).

## 2. THE PARITY DISTRIBUTION over the COMPARED population only

| period | n | EXACT | TIGHT | LARGE | range_match | day-resid nonzero |
|---|---|---|---|---|---|---|
| QTD | 5,138 | 1,812 | 3,103 | 223 | **5,138 / 5,138** | 45 |
| YTD | 5,151 | 1,411 | 2,961 | 779 | **5,151 / 5,151** | 240 |
| 1Y | 5,156 | 3,003 | 1,161 | 992 | **5,156 / 5,156** | 949 |
| **ALL** | **15,445** | **6,226** | **7,225** | **1,994** | **15,445 / 15,445** | 1,234 |

⭐ **`range_match` is 15,445 of 15,445 -- 100%.** Every requested date range came back as the range
requested, verified by the ruled join (position finds the cell, the dates certify it). **That is the
single strongest result in the census** and it validates the request-side contract at population
scale, where P1 could only assert it at n=5.
⚠ **The day-count residual is NOT uniform and 1Y carries it: 949 of 5,156 cells (18.4%)** disagree
with BD on how many days were linked, against 0.9% at QTD. **Named as a finding, not diagnosed.**

## 3. THE DISAGREEMENT DISTRIBUTION -- never an agreement rate (criterion 3)

```
  p50     1.95 bp        p90    15.50 bp        p99    ~9,854 bp
  p75     4.74 bp        p95    43.08 bp        max   ~71,772 bp
```
**Half of all cells agree within 2 bp and three-quarters within 5 bp** -- then the tail explodes.
**This is why a single "parity rate" would have been actively misleading:** "87% within 10 bp" and
"a tail reaching 700x" are both true of the same table, and only the distribution says so.

⚠ **A SIGNATURE I CHECKED BEFORE REPORTING IT, because the raw percentiles looked manufactured.** The
first output read `p99 = exactly 10,000.0000 bp` and `max = exactly 80,000.0000 bp`. Round numbers
that exact are usually an instrument artifact, so I opened them:
```
  45 cells carry an INTEGER delta in return units: -1.0 x30, -3.0 x9, -2.0 x2, -7.0 x2
  but 138 DISTINCT values sit above 10,000 bp, and they are NOT all multiples
  excluding every exact multiple of 10,000: p99 9,853.8 -> max 71,772.0  (barely moves)
```
>> **So it is a small MODE (45 cells, 0.3%) that the p99 boundary happened to land on, NOT a units
   error or a systemic offset. The heavy tail is real either way.** The 45 integer-delta cells are
   flagged as their own signature -- **BD returning an integral figure is worth a producer's eye** --
   but they are not load-bearing for any number here. <<

## 4. THE LARGE CLASS, ADDRESSED EXPLICITLY (criterion 2)

```
  LARGE cells                                    1,994  over 1,146 accounts
    of which a DAY-COUNT MISMATCH explains         478  -> COVERAGE, not method
    residual, BOTH sides fully linked            1,516  -> genuine calculation differences
  per period: 1Y 992 | YTD 779 | QTD 223
```
⛔ **W2 WAS NEVER SCOPED TO RESOLVE THESE AND DOES NOT.** It moves n from 5 to 5,309 -- **a
DENOMINATOR achievement, not a MECHANISM one.** P3-EXACT exists specifically to close them, AFTER P2.
**A reader taking "census complete" as "parity proven" is holding an expectation this run cannot
satisfy.**
⛔ **AND THE STANDING "11 LARGE" IS NOT SUPERSEDED BY 1,994 -- THEY ARE DIFFERENT DENOMINATORS.** The
11 is P1's count over ITS 16 ruled-window cells on 5 accounts and remains correct;
`ADVI_BDPARITY.json` needs no edit. **Every LARGE count travels with its denominator, never as a bare
digit.**

## 5. THE PRODUCER FINDING -- the reason this is a two-way audit

**112 cells over 61 accounts were withdrawn as SELF-INVALID** on our own side. The specimen:
```
  account 0077573397, 2025-10-15
  bmv $2.33 -> emv $1,164.46, cf_net 0.0, r_net 498.768 (+49,877% in ONE DAY), status OK
  it clears the producer's NEAR_ZERO_BMV=1.00 guard by $1.33 and compounds into every window
```
**The population-level read (all 114 rows above |r_net| > 1.0, opened individually per
`2.0.0_SA_COO` 90726):**
```
  TWR identity holds on 114 of 114   -- the algebra is right, the INPUTS are wrong
  A  no recorded flow, value moved    79 rows / 70 accts   bmv median    $23.75
  B  flow > 10x the base              21 rows / 17 accts   bmv median $35,689
  C  flow recorded, comparable base   14 rows / 12 accts   UNDISPOSITIONED
```
⭐ **AND THE A CLASS CLUSTERS ON DATES, WHICH CHANGES THE FIX:**
```
  2026-01-26: 19 accounts | 2025-10-15: 10 | 2026-04-09: 7 | 2026-05-06: 5
  FOUR DATES CARRY 41 OF 79 A-CLASS ROWS (52%), across 35 distinct dates
  CONTROL: those dates have a NORMAL population-wide cf_net==0 rate (84-86%, same as
           control dates 2026-01-27 and 2026-08-28) -- and the CONTROL DATES CARRY ZERO BLOWUPS
```
>> **This is not 70 broken accounts. It is ~35 dates on which flows for a subset of accounts failed
   to ingest. The remedy is a per-DATE flow re-ingest, not per-account remediation.** <<
⛔ **A BMV-THRESHOLD FIX IS REFUTED AND MUST NOT BE TAKEN:** of rows with BMV < $10, only **0.3%**
(36 of 13,211) blow up. Raising `NEAR_ZERO_BMV` would flag 13,211 rows to catch 36 and still miss the
rest. **This seat proposed that hypothesis and then killed it by measurement.**

## 6. FEED SCOPE, ON THE FACE (criterion 4)

**`feeds=["performance"]` ONLY.** No `costbasis`, no `allocation`. `q_start=2026-07-01`,
`q_end=2026-08-28` (pinned, not derived), `pull_date=2026-09-01` (pinned, identical on all 45
invocations).
⛔ **SI IS OFF-CONTRACT AND IS NOT REPORTED.** D2-7 (@`fc02592b3f`) removed SI and 3Y from the period
contract entirely. The pull LANDED SI bytes -- BD returns an SI range at index 5 -- and **they are not
compared, not graded, and no served surface may expose them.** Supporting measurement: 57% of this
cohort (3,027 of 5,309) is left-censored by our own 2024-07-08 data start, and BD's SI cell returned
the QTD figure **byte-identical at 3 of 3** when tested. **That is evidence FOR the existing removal,
not a reason to revisit it.**

## 7. VENDOR LEDGER -- closed, reconciled, and the overspend owned

```
  DATA  spot check (pull_date 2026-08-31)         3
        W2 (object versions @ 2026-09-01)     5,789   = 5,189 clean + 600 from chunk 1 x5
  AUTH  = Lambda invocations, one token each      51
  TOTAL                                        5,843
  a clean run would have been                  5,358      OVERSPEND 485  (+9.1%)
```
**The entire overspend is one defect of mine:** a default boto3 client (read_timeout 60 s vs a 168 s
chunk) **retried a non-idempotent vendor-spending invoke five times and reported ZERO landed while
the vendor had been charged 5x.** Found by a bounded first-chunk probe, fixed at `e352f70476`
(`total_max_attempts=1`, asserted at import), and **confirmed on live bytes: 5,189 keys at exactly 1
version beside chunk 1's 120 at 5, with no third value anywhere in the prefix.**
`Lambda errors across 51 invocations: 1` -- the deliberate `feeds:[]` pre-flight. **Zero unexpected.**

## 8. CRITERION 3 -- prior snapshots UNTOUCHED

```
  pinned baseline objects    18
  still at pinned VersionId  18 of 18     MOVED 0     DISAPPEARED 0
```
Compared **by VersionId, never by count** -- a count is equal under a same-count overwrite.

## 9. WHAT THIS DOES NOT ESTABLISH

- **Not that the 1,516 residual LARGE cells are BD's fault.** They are unexplained by coverage;
  attribution is P3's.
- **Not that 112 is the whole SELF-INVALID population.** It is everything above a 100% single-day
  return. **A milder version of the same missing-flow defect on a larger base produces a
  plausible-looking number and this screen cannot see it.** The screen bounds what it catches, never
  what exists.
- **Not that `|r_net| > 1.0` is a principled bound.** The distribution does not separate cleanly --
  it is a smooth power law. What IS established is robustness: a 20x move in the bound changes the
  affected account count by only 2.8x. **The bound is arbitrary; the population it selects is stable.**
- **Not a diagnosis of the 1Y day-count asymmetry** (949 of 5,156 vs 45 at QTD).
- **Nothing about `costbasis` or `allocation`,** which were never pulled.
