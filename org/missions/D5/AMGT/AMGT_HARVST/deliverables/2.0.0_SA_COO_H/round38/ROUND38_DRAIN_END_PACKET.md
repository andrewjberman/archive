# AMGT_HARVST round 38 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-02 ~23:0xZ

The round-37 analysis @29fbb123e0 (PRD v0.15) led to ONE issuance @dba4795105 (decomposition section 51).

**3 of 3 orders are terminal.**

## 1. Cells

| cell | result | merged | check at the base |
|---|---|---|---|
| `HVST-ak-1` `~90` FWD-16 | `finbert_sentiment.py` (scorer client over `opal-news-ai-sentiment`, the append-only `article_sentiment` store keyed by `record_hash`, a `score`/`census` CLI); 3 nullable tone fields on gold mention rows. The live contract was measured. **0 publisher text** reached FinBERT: 6 + 3 live calls, all fixed sentences. No `score` was run. | @23b1e6851d | AC2 PASS (3 fixed sentences: positive 0.946, negative -0.968, neutral 0.0); AC3 PASS |
| `HVST-ak-2` `~92` FWD-17 | `window_tone.py`: `chatter_window` per name per 30/90/365-day window ending at T-1. Voters are non-neutral with no threshold; tone is over voters only and null at 0 voters; the served start is stated. No served write. | @f175fbeb99 | AC2 PASS: 15 of 15 rows equal an independent recompute; the all-neutral name reads voters 0, tone None |
| `HVST-ak-3` `~91` FWD-6 density | Read-only census: served events 8; dry-built on current gold 438 over 205 securities. Spike days 634 at 2x and 564 at 3x; covered by dry-built events 315 (49.7%) and 281; by served events 8 (1.3%) and 7. | @b79d3781bd | AC2 PASS (the served snapshot of 8 rows was read by the check itself) |

The suite at the base reads 317 passed and 3 failed. The 3 are stale tests that pin the removed n-6 silver read path (row
Z-S68); RESAPP am-1 removed it by design.

The IAM invoke-grant cell (analysis item 1) was NOT cut. The site-Z gold-build identity's DryRun invoke reads 204.

## 3. Outcome state for your grade (the grader's figures; this seat does not grade)

| FWD | state this round |
|---|---|
| FWD-16 FinBERT tone | code built and graded; no score run, no tone served |
| FWD-17 window tone | code built and graded; no window served |
| FWD-6 density | census: re-deriving events on current gold covers 49.7% of 2x spikes against 1.3% served; the served event rebuild is not run |
| FWD-11 ft limb (1) | ft collection stopped (STOP_FT); collection is Andrew's |

## 4. Rows this round

- New: Z-S67 (`record_hash` includes `run_stamp`); Z-S68 (3 stale timeline tests).
- **The 10 ARMED rows** CTO 28792 named (9 from rounds 1-10 under `2.0.0_SA_COO~Y`, plus Z-W91-S10) are dispositioned in
  section 5.

## 5. The 10 ARMED rows -- disarmed on evidence, or placed in round 39

A read-only assessment checked each row against CLOUD HEAD 56eaa6d500. Every cited fix commit is an ancestor of HEAD.
The REMEDIATION rows still read OPEN only because no one re-checked them after the fixes landed.

| row | disposition | evidence | disarm row |
|---|---|---|---|
| Z-W9-S1 | DISARMED: both silver_append call sites use the suffix-retry wrapper | adc9d85b92, d5ef6e6371 (`uploads.py:277-309,337-385`) | Z-S70 |
| Z-W11-S1 | DISARMED by the tool owner: rows outside the cone are read from the git index | 651f750a5a (`missions-tree-index.py:191-219`) | Z-S71 |
| Z-S23 | DISARMED: the resolver reads remediation rows by id plus a structured disarm state | `surprise-row-gate.py:440`; Z-S26; REMEDIATION_v5 | Z-S72 |
| Z-W22-S2 | DISARMED: one job per invocation; a timeout is retried twice and no longer cools the publisher | 3669bd0f0a, 4901fd709b | Z-S73 |
| Z-W26-S1 | DISARMED: 0 dotted-string patch targets remain in the harvest tests | 58135da029 | Z-S74 |
| Z-W29-S1 | DISARMED: one pinned universe file (round33, 212 names) is the cited source | 78aac97ada; `publication_gold.py:1598` | Z-S75 |
| Z-W8-S2 | INERT-HISTORICAL: only h-8 (complete) used the ids form; the gate passes no ids | `proof-of-spec-check.py:530-541`; `to-pipeline-gate.py:3041` | Z-S76 |
| Z-W30-S1 | INERT-HISTORICAL: only y-3 (complete) diffs a portal path from the root | no other HARVST order | Z-S77 |
| Z-S11 | ROUTED to the checker's owner `1.0.0_SA_CTO`: invocation-alignment still compares strings and never parses the command | `proof-of-spec-check.py:1441-1484` | Z-S78 |
| Z-W91-S10 | PLACED as a round-39 LOCAL cell: a 200 listing with 0 hits gets its own status, proved on a planted page | `publishers.py:1008-1016,1155-1164` | Z-S79 |

Totals: 6 disarmed, 2 inert-historical, 1 routed to the CTO, and 1 placed in round 39.

## 6. Proposed for round 39 (the CTO decides)

1. **One batched LOCAL repair cell:**
   - retire or rewrite the 3 Z-S68 tests against the gold read path;
   - Z-W91-S10 (Z-S79): `listing_empty_200` as a distinct status, proved on a planted page.
   Neither needs collection.
2. **Z-S11 (Z-S78)** is the checker owner's (`1.0.0_SA_CTO`), not a HARVST cell.
3. **A scheduled gold producer** (CLAUDE.md: production pipelines are scheduled), which would also need the FinBERT
   invoke grant for its role.
