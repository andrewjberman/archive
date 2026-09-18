# EN-c-40 round 9 -- the result record

**TO:** `LGIC_ENFORCE.TO-EN-c-40-r9` (`org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-c-40-r9.hand-comparison.md` @`3c8c64692b`)
**Worker:** `0.9.0_WK_LGIC_ENFORCE~1` | **Worktree:** `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-9-1`
**Branch:** `wk-lgic-enforce-9-1`, base `3c8c64692b` | **Artifact commit:** `ea93996a87` (LOCAL)

## 1. The four mechanical criteria, as measured after the artifact commit

Each ran from the worktree root under `timeout 900`, verbatim from the order with `<WS>` expanded.

| criterion | verdict | deciding line | rc |
|---|---|---|---|
| `C40R9-AC1` | PASS-by-output | `cell counted: 45 \| register cites 43 \| issuer measured 45` / `VERDICT: PASS-C40-RECOUNT` | 0 |
| `C40R9-AC2` | PASS-by-output | `surfaces present: 3 of 3 ; missing []` / `VERDICT: PASS-C40-POPULATION` | 0 |
| `C40R9-AC3` | PASS-by-output | remainder 0 on 3 of 3 surfaces / `VERDICT: PASS-C40-AGREEMENT` | 0 |
| `C40R9-AC4` | PASS-by-output | 2 / 27 / 5 listed, 0 missing name/why / `VERDICT: PASS-C40-DISAGREEMENTS` | 0 |
| `C40R9-AC5` | RECORDED, no verdict | judgment; `3.0.0_SA_CVO` grades it at L9 | -- |

`selftest-arms` ran FIRST, before any write: `SELFTEST ARMS: 27 ; POSITIVE-SATISFIABILITY arms: 13 ; failures: 0`,
`VERDICT: PASS-SELFTEST-27-ARMS-13-POSITIVE`. No arm a correct record cannot satisfy, so no BLOCKING row.

## 2. The re-count

Section 9 of `GRADING_RULE.md` parses to **45** worked cases (CONFORMANT 18, OUT-OF-PATTERN 20, ALIAS 3, RAISE 2,
NOT-GRADED 2; 26 types), re-counted at write time by `json.loads` of the one json fence between `## 9.` and `## 10.`.
**43 is the stale figure.** The stale carriers are the register (`project.json`) and `LGIC_ENFORCE_ROUND8_ANALYSIS.md:151`.
43 was true at `GRADING_RULE.md` @`51b0952d71`. The v1.9 re-cut @`fd6ce8c330` added `mdpf-lambda-lambda` and
`orion-orion-lambda-lambda`, which EN-s-2's round-2 record had already measured.

## 3. The comparison

`grade()` was imported from `git archive 54659987c0`. That is the commit that wrote `NAMING_CENSUS_REPORT.r8.md`,
covering every path `lib/opal_naming.py` reads for a grade. `grade()` was also run at HEAD, with **0 vintage differences**
on N2 and N6. Per name, AGREE means an equal verdict AND, where the hand gives a canonical form, an equal canonical form, byte for byte.

| surface | agree | disagree | compared | own denominator |
|---|---|---|---|---|
| `GRADING_RULE.md` s.9 worked cases | 43 | 2 | 45 | 45 |
| `n6-grader-a.tsv` grader rows | 61 | 27 | 88 | 88 (89 lines = 1 header + 88) |
| `TENSION_RANKING.md` ranked surfaces | 5 | 5 | 10 | 10 |

**What the disagreements are:**
- **Stale hand records: 25 of N6's 27, and both of N2's 2.** Each hand record is older than the registry row or schema
  entry that decides it, and `HAND_COMPARISON_R9.json` names the introducing commit for each. `grade()` is right at
  the census vintage. The two hand products now contradict each other on `opal-globgrph` and `opal-gateway`.
- **`grade()` departs from the written rule, and the hand follows it: N6's other 2.**
  `opal-cot-bd-session-fetch` keeps the refused `bd` against R3 (row W1-S73).
  `ExecIncrParityFailure` is re-joined to `incrparity`, but N2 states no re-join (row W1-S74).
- **IV7: 5 of 10 surfaces disagree.**
  - Rank 1 (mixed-grain `~330`) and rank 4 (alarms: the hand's `6` contradicts its own source) are wrong on the hand side.
  - Rank 5 is an instrument mismatch. The census carries no drift class, so it cannot reproduce the hand's figure.
  - Rank 7 has an ambiguous log-group grain.
  - Rank 8 shows `s3-*` up by 4 in five days of estate drift.
- **Tolerance.** It was declared before any census figure was computed and never changed.
- **Grain revisions, disclosed.** The grain of rank 1, rank 4 and LOG_GROUP tokenisation was revised after a first run,
  to the grain the hand's own source states. The first run (3 agree / 7 disagree) and every changed figure are kept
  under `iv7_first_run`, so the CVO can judge the revision against its effect.

## 4. Controls

- **Mutants on the committed record.** Each was run alone through the real checker, then the bytes were restored:
  - M1 `counted=0` -> `FAIL-C40-RECOUNT`
  - M2 n6 surface removed -> `FAIL-C40-POPULATION`
  - M3 n6 agree+1 -> `FAIL-C40-AGREEMENT`
  - M4 one n6 disagreement dropped -> `FAIL-C40-DISAGREEMENTS`

  After each restore the arm read PASS and the sha256 was unchanged
  (`56a5075f47ffd80d5b871c8c1143b893f91d4a5224225c7c3def9a5e780570c0`).
- **Negative control at base.** At `3c8c64692b`, before this cell, `HAND_COMPARISON_R9.json` did not exist, and the
  issuer measured all four arms FAIL at the cut.
- **Determinism.** A rebuild before the commit was byte-identical. A rebuild after the commit differed in exactly one
  field, `census.grade_vintage`, which names the HEAD hash and so must move with HEAD. Every other key was equal. The
  committed bytes were restored with `git show HEAD:<path>`.

## 5. Rows filed

`LGIC_ENFORCE-W1-S71` through `LGIC_ENFORCE-W1-S74`, all OBSERVATION / INERT / UNDER_INVESTIGATION. They were spliced
into the list fence of `INVESTIGATION_v1.md`. The non-ASCII character count was 0 before and after, and the
backslash-u count was 79 before and after.
- S71: the comparison WAS attempted in rounds 1 and 2, on 3 names.
- S72: LGIC_NAMING's hand products are stale against the registry.
- S73: `grade()` keeps `bd` in a canonical form.
- S74: `grade()` re-joins pieces that N2 does not re-join.
