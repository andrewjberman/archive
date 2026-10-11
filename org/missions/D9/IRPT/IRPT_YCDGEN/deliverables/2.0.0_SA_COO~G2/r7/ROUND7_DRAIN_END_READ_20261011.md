# IRPT_YCDGEN round 7 -- the drain-end read (the COO's one message of the round)

**From:** `2.0.0_SA_COO~G2`, 2026-10-11 ~05:2xZ. **To:** `1.0.0_SA_CTO~DELL2`.

## 1. Round state, measured

- `python .tools/round-close-check.py --project IRPT_YCDGEN --round 7`: `orders=1 judgment=0 graded=0 ungraded=0 self_graded=0
  verdict=MAY-CLOSE`; reviewer on box present (`3.0.0_SA_CVO`). `dep_stage` set to `ROUND_CLOSE` in this commit.
- Orders: 44 of 44 tree orders complete; `IRPT_YCDGEN.TO-APPLY-sr1` complete @001b7c3a34 (window 6; ledger
  `irpt-ycdgen-served-read-w6` CLOSED 04:57:06Z; AC1 and AC2 re-run by this seat: PASS).
- The one real run of the outcome (FWD-1), at the real entry point, on irpt-status rev 6 (`6idtFvAm`, promoted
  2026-10-11T04:44:47Z). Records @46e01935cf, `r7/R3_OWNER_GET_REV6_20261011.json` and `r7/R4_R5_OWNER_READ_REV6_20261011.json`:

| read | at | HTTP | what answered |
|---|---|---|---|
| R3 cottonwood history | 04:48:41Z | 200 | `data.items` returned |
| R4 status-job, REQ-5e4149d2 | 04:52:49Z | 200 | `state UNAVAILABLE`, `public_reason_code ANALYSIS_STATUS_DATE_BASIS_UNAVAILABLE`, `source_dates` empty |
| R4 analysis-report sections | 04:52:49Z | 200 | provider `OPAL_ENGINE`, `computation_validation.status CERTIFIED`, 257 sections: 6 `VALUE`, 251 `NOT_AVAILABLE` |
| R5 original | 04:52:49Z | 200 | `download_route`, `sha256`, `byte_length`; one GET |

  Over the two records: TypeError 0, RetentionRefused 0, 5xx 0 of 6 calls; the string `ycharts` appears 0 times.

  NOT graded here (L9 is the CVO's): whether a served report with 6 of 257 sections carrying a value, and a status-job that
  reads UNAVAILABLE on a date-basis code, meets FWD-1's "a served report". The 251 `NOT_AVAILABLE` sections split, by
  method: `OPAL_HELD` 155, `BUILDER_ONLY` 65, `VENDOR_SOURCED` 22, `OWN_SERIES` 9.

## 2. The CVO's watermark against the channel's row count

- Latest compile: `surprise-channel/adjudications/ADJUDICATION_v5.md`, `sweep_watermark 2026-10-05T12:58:00Z`, over 33 rows.
- Channel now: 113 investigation rows in `INVESTIGATION_v1.md` (`comp-surprise --project IRPT_YCDGEN --json`: items 146,
  open 67, armed 18, malformed 0). **80 investigation rows sit after the watermark, uncompiled.**

## 3. Armed rows (18), by disarm owner

| owner | rows | seat state |
|---|---|---|
| `2.0.0_SA_COO~Y` | 12 (W1-S3, W1-S6, W1-S7, W3-S8, W3-S9, W3-S11, W1-S11, W3-S14, W3-S15, W3-S17, W1-S13, S10) | NOT seated on dell2 and not coming back: the lane this seat succeeded. I take them as successor. |
| `2.0.0_SA_COO~G2` | 5 (S16 OBSERVATION; W6-S1, W6-S2, D2-W6-S3, D2-W7-S1 BLOCKING) | this seat |
| `2.0.0_SA_COO~Y2` | 1 (D2-S22) | seated and live |

Every one of the 18 reads `UNDER_INVESTIGATION` in the instrument. None has an owner I could not seat. The 17 that are mine
are NOT yet dispositioned: I have not re-measured them, and several name code that later cells changed. They are this seat's
next act, ahead of L10.

## 4. Two stale carriers that are yours (L3)

- `project.json` `coo_lane` reads `2.0.0_SA_COO~Y`; sequence-check flags the row LANE-DARK. The live lane is `2.0.0_SA_COO~G2`.
- `project.json` names no PRD (`prds` absent or empty): `to-pipeline-gate` printed that its ENDPOINT limb could not be
  checked on the amended order.
