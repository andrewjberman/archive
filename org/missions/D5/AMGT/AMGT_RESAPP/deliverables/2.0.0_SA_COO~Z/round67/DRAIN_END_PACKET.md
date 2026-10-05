# AMGT_RESAPP round 67 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-05 ~00:1xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.75 + s.75e. **Issuance:** `e410b00b27`.

**Input:**
- The CTO's round-66 analysis @d76db3486c.
- The CTO's AMENDMENT 1 to the aq-5 half @14aa3c9200, on row Z-S346.
- Andrew-direct "recs approved" @c700426bc9.
- PRD v0.37.

**Note:** the drain was re-entered after the site-Z crash (18:58Z). All four build workers stalled at ~03:22Z, and three of them
had already committed. Slot ~222 was re-seated on its uncommitted state.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `aq-1` FWD-39 list repair | LOCAL | worker ~219 | complete | drained `fa22ce3149`; AC1-AC3 PASS (plant 18/18, mutant 13/18 fail) |
| `aq-2` FWD-36 tone from `chatter_window` | LOCAL | worker ~220 | complete, AC2 FAIL | drained `aac5a586d1`; AC2 FAIL on 21 covered names with no table row only (row Z-W220-S1) |
| `aq-3` FWD-38 (d) `/ledger` provenance | LOCAL | worker ~221 | complete | drained `e5ea575b16`; AC1-AC3 PASS |
| `aq-4` Z-S86 covered-no-block reason | LOCAL | worker ~222 (re-seated) | complete | drained `d8bafe6896`; AC1-AC3 PASS; universe: the Security Scanner S&P 500 file |
| `aq-5` the redeploy, three legs (`aq-6` is leg 3) | WORLD | `0.7.0_AE_CloudOps~A` | complete | instance @a8bed3d3af VALID, genre DEPLOY. Leg 1 scanner grant @f61711ef2b (Z-S345). Leg 2 code at `d8bafe6896`, `FcVBPafw` -> `aoQ+WrefJ`. Leg 3 chatter_window prefix grant @768731795b (Z-S346). Pairs: COO `0e415a64d9`/`4d3db86faa`, CTO `786d5e992e`/`5468d18362` (+`14aa3c9200`, `5a8f3ce6ff`) |

The function now runs AMGT_CORPUS al-5's build `2rFeF57l...` (at `288de3d95d`). It carries round 67 (`d8bafe6896` is its ancestor),
and leg 3 did not move it.

## The real run on the DEPLOYED function (`REAL_RUN_r67_deployed_20261004.txt` @389089e765, 23:37Z)

| check | result | detail |
|---|---|---|
| c23 (FWD-39 repair) | YES | 190 payloads, 128 non-empty, 0 own-ticker/short-name offenders, 0 extended-list words; the inverted window serves its reason |
| c24 (FWD-36 tone) | NO on ONE clause | per window 30/90/365: mismatches 0, old-reason 0, unreadable 0 (C2), no-table-row 21 |
| c25 (FWD-38 (d)) | YES | BA, AMD, VLO: 6 of 6 classes sourced or reasoned; news run = overlay last_run |
| c26 (Z-S86) | YES | DE thesis + peers 200 with a reason; ZZZZ_US_Equity 404 |
| grant (aq-6) | YES | GetObject + ListBucket(prefix) on chatter_window/ allowed; controls allowed |
| r64 c9-c14, r65 c17, r66 c18/c19/c22; c15 cold | YES; 1.9-2.0 s | per AE~A's aq-5 instance |

## For the CVO's L9 read (JUDGMENT, never self-graded)

1. **FWD-39:** read the repaired clouds as a reader would. The own ticker, the name words and the measured boilerplate are gone.
   The stop list is 165, with its source named.
2. **FWD-36 tone:** 74 names serve the window's tone and voters, and 0 voters reads "no clear tone".
   - The other 21 names serve the plain "window table holds no row" reason.
   - Their absence is the producer's: `window_tone.py` builds a 212-name set that misses them (Z-W220-S1). This is a round-68
     item for the CTO's analysis.
3. **FWD-38 (d):** `/ledger` classes name their source or a plain reason.
4. **Z-S86, DE_US_Equity:**
   - `/peers` serves "Deere & Company (DE) is a covered name (Security Scanner S&P 500 universe, as of 2026-10-02) and has no model
     block yet".
   - `/thesis` serves a reason that opens "identity UNRESOLVED -- no measured security key to read a drafted document by Deere &
     Company (DE) ...". That is system wording on a user-facing route (DSGN FWD-27). Grade it.

## Rows

- `Z-W220-S1` (OBSERVATION, INERT): the producer's 212-name set misses 21 covered names. Carried to round 68.
- `Z-S345` (OBSERVATION, INERT, issuer): the scanner read was implicitDeny at the cut. It was cured by aq-5 leg 1.
- `Z-S346` (OBSERVATION, ARMED, AE~A): the chatter_window read was denied. It was cured by leg 3, and DISARMED by its
  disarm_owner in row `Z-S347` @389089e765 (mismatches 74 -> 0, unreadable 95 -> 0).
- `Z-S347` (OBSERVATION, INERT, issuer): the disarm record.

**Instrument note for the analysis:** both cures were IAM grants that local checks could not see. A local run reads under the
operator's credentials, never the function role's. The c24 check also skipped rows its own index lacks. C2 now counts the
unreadable reason over every row. The issuer's halves predicted served outcomes from local reads, and a role simulate at the cut
would have caught both.
