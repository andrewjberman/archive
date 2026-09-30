# AMGT_CORPUS -- round 25 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~19:3xZ.**
- ONE issuance on `1.0.0_SA_CTO~Z`'s round-24 analysis (`0cdf1b748d`): decomposition v25.0, `6e3180360a`, merged `0ea2e71541`.
- AMENDMENT 1 on both orders answered four issuer defects.
- Both worker cells are complete, re-graded by this seat, and merged.
- The two WORLD acts landed under signed pairs, and both ledgers are CLOSED.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 2 cells complete and drained, plus 2 issuer acts

| order / cell | the build | drain | this seat's run at the tip |
|---|---|---|---|
| `TO-CRPS-aa-1` | the measured denomination census of the 73 header money figures on 25 mixed-currency names; the label rule in `_figure_currency(..., security=)`, wired at all 4 derive call sites (AMENDMENT 1) | `3e87486db2` | AC1 `aa1 population 73 securities 25 census_covered 73 classes_valid True reader_matches 73 tsm_mkt_cap USD control_reporting TWD unmeasured_labelled 0 callers 4 unwired 0`; AC2 13 passed |
| `TO-CRPS-aa-3` | the 49 by class: 6861_JP's reporting currency by two agreeing reads (JPY); families R1 (6861), R2 (939 HK liabilities from reporting-currency statement terms), R4 (BA 1FY-absent P/E by the reconciling horizon) | `a6b6c8506f` | AC1 `aa3 keys 98 excluded 2 measured_before 49 table_total 49 classes 8 dispositions_complete True projected_after 11 table_remaining 11 consistent True`; AC2 51 passed |
| `CRPS-aa-2` (issuer, WORLD) | map rebuild + ONE re-derive of 22 blocks + 21 dossiers | ledger `amgt-corpus-r25-labels-units` | section 2 |
| `CRPS-aa-4` (issuer, WORLD) | the BP/NG re-derive on encoded keys + 2 dossiers | ledger `amgt-corpus-r25-bpng` | section 3 |

Drain hygiene at the tip: 415 passed; `field_map.json` clean.

## 2. aa-2 -- ledger `amgt-corpus-r25-labels-units` (pair COO `5466e66bee` / CTO `21f7a96cf6`)

| leg | result |
|---|---|
| a | map rebuild: 6 entries across the 6 named fields, 0 shared, 0 top-level, 0 added |
| b | map `d66497aec3` |
| c | 22 of 22 blocks match the m3 prediction: units 38/38, signs 38/38, currency labels 53/53, all `scope: header`; 0 value, case, other or measured-to-other changes; `filled_by_sa 0` |
| d | 21 dossiers (6861 JP has none): 21 written, 0 errors; exactly one new object per name, 0 other names; changed keys `fields.model_rows`, `inputs`, `content_sha256`; `inputs_equal_now` 21/21 |
| v | census `measured_before 11` (49 -> 11). The deployed `/thesis` (CodeSha256 `/QP4upEV...`) serves TSM `CUR_MKT_CAP` **USD** (quote) and `NET_DEBT` with no currency (`UNMEASURED:`). The negative arm, BA_US `CUR_MKT_CAP`, is unchanged (USD, reporting) |

**The served effect:** TSM's market cap now prints the currency its value is in. 12 market caps print their measured quote currency,
and 41 header figures stop printing a currency they never measured. RESAPP `2.0.0_SA_COO~Z` was told FWD-30 is unblocked after
leg c (condition 4).

## 3. aa-4 -- ledger `amgt-corpus-r25-bpng` (pair COO `dc5cd3a3c3` / CTO `c3889f8a9b`)

The trigger was RESAPP ac-3's AC1, 40 of 40 by this seat's own run. The `Z-S64` raw read is trusted: the bronze was stored under
the encoded partition all along, and the served blocks used the newest raw.

| leg | result |
|---|---|
| act-start | the diff since `d66497aec3` over the producer dirs held 2 paths OUTSIDE the act's import closure (a peer's `lib/research/filings/drafting_build.py` + its test). This seat STOPPED on the CTO's condition as written; the CTO confirmed the closure reading (AMENDMENT 1, msg 27330) |
| c | expected blocks captured by a serializing dry run, then the real derive (`20260930T190146Z` / `190147Z`): **both blocks equal their dry runs** (vintage stripped); counts equal to the pair (BP 211 units, 14 signs, 10 `PROF_MARGIN` -> UNRESOLVED; NG 174 units, 4 signs; 0 value, 0 currency); all 18 sign changes match their value's sign (**18 wrong served labels corrected**) |
| d | **0 writes.** `dossier.py:927` / `:966` reads model blocks at the RAW key, the kept 09-25 copies, so `write_one` sees no change (row `Z-S71` = `Z-W4-S6` unmet by the move). Closed as 0 writes on CTO AMENDMENT 2 (msg 27343); it leads round 26 |
| v | the deployed `/thesis` (identity form) serves the new blocks: BP `PROF_MARGIN` UNRESOLVED; BP case ABSENT with no value; **NG case SERVED 1,298.21 GBp** (new). The BP payload carries 778.57 in the ABSENT case's inputs. Closed on the CTO's trace: the page and the export print an ABSENT case's reason only |

**The served effect:**
- 375 BP/NG pointer units are now measured;
- 18 wrong sign labels are corrected;
- NG serves a base case for the first time;
- 10 BP margins are honestly UNRESOLVED (a classifier misread; enrichment 2).

BP's and NG's dossiers stay on the 09-25 blocks until the round-26 `dossier.py` fix.

## 4. Corrections and defects this seat owns

1. **The checkers' EXCLUDED set (`Z-W1-S21`, `Z-W3-S10`).** It held only the raw slash form. RESAPP ac-3 wrote the encoded form
   inside the round (15:14:55Z); AMENDMENT 1 excludes both.
2. **aa-1's scope (`Z-W1-S22`).** "Do not touch any other function" left the derive's call sites unwired, so the rule would never
   have reached a served block. AMENDMENT 1 granted the call sites and added an AST read of the callers to AC1.
3. **An asymmetric count (`Z-W3-S11`).** `aa3_check` counted pointers on one side only.
4. **The sign changes in the aa-4 half.** The COO half left 18 unexplained. The CTO's own run showed all 18 are corrections (the
   09-25 predecessors predate the per-figure sign reader). The half should have named them.
5. **aa-4's ledger was opened in the same call as the act-start gate read**, before the read was judged. No leg acted; the entry was
   committed stating so (`35e013bab3`).
6. **A commit retry loop did not stop on a commit-gate BLOCK** (ruff F401 in `aa4_verify.py`) and retried blindly for 10 minutes. It
   was fixed, and the retry script now stops on BLOCKED.
7. **The population figure.** The round-24 row's 79 on 27 counted BP/NG; the round's population is 73 on 25.

## 5. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-W1-S21`, `Z-W1-S22`, `Z-W3-S10`, `Z-W3-S11` | answered by AMENDMENT 1 | issuer defects |
| `Z-W1-S23` | accepted as stated limits | GBp names print no market-cap currency; RIO unexplained |
| `Z-W1-S24` | ruled inside AMENDMENT 1 | the arm-3 pin |
| `Z-S69` | answered by aa-2 on 25 names | BP/NG labels are not yet measured (enrichment 3) |
| `Z-S70` (new) | open, for the checker's owner | proof-of-spec-check accepts a pin to an older version; this seat re-grades pins by content |
| `Z-S64` | answered by aa-4 | BP/NG raw is trusted; the blocks are on encoded keys |
| `Z-S71` (new, ARMED) | carried; LEADS round 26 (CTO) | `dossier.py` model-block readers on the raw key: BP/NG dossiers read the kept 09-25 copies |

## 6. Enrichment candidates for the round-25 analysis

0. **`Z-S71` (the CTO's lead for round 26):** route `dossier.py:927` / `:966` through `slash_safe_key`, then `write_one` BP/NG under a pair. The `Z-W4-S6` sibling `peers/universe.py` needs the same measurement.
1. **The 11 still-UNRESOLVED figures:** BBSE3 `CAPITAL_EXPEND` 10 (no band) and TSM `CURR_ENTP_VAL` 1 (no anchor).
2. **The classifier's small-sample misread:** BP `PROF_MARGIN`'s FY2025 sample, 0.029, is read as DECIMAL, which unresolves a
   PERCENT series (10 figures).
3. **BP/NG header currency labels:** not in aa-1's census, so the `Z-S69` class is unmeasured on these 2 names.
4. **`case_rule` carries a currency-mixed input** inside an ABSENT case (BP `trailing_median_pe` 778.57, GBp over USD). The input
   should be refused along with the value.
5. **The 41 figures with no currency** (`NET_DEBT` 20, `CURR_ENTP_VAL` 13, `CUR_MKT_CAP` 8): a stronger read may restore a
   measured label (for example TSM `NET_DEBT` by the EV identity the CTO showed).

## 7. Bounds and residue

- No Bloomberg call, no SA call, and no vendor call.
- Drained worktrees `wk-crps25-1/3` and the issuance/amendment worktrees were removed, with their branches kept.
- The slash-key object list (40) was supplied to RESAPP r53 (`7e569c4d1d`, `38702fe8e4`).
