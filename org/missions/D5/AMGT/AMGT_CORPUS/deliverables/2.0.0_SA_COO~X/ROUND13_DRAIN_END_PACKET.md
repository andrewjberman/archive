# AMGT_CORPUS -- round 13 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~13:0xZ.** One order issued (@`ec8e265e4b`, decomposition v13.0). It is complete, was
re-graded at the worker's tip `d1c92f63c1`, and merged at `2a693d47b3`. The round is LOCAL and read-only: no served write and no
pair. The evidence file is `deliverables/0.9.0_WK_AMGT_CORPUS~1/FWD_EVIDENCE_ROUND13.{json,md}` (run_at 12:50Z, PRD @`9e326e11c1`).

**R-4:** graded this round -- none by this seat (L9 is the CVO's; the round-13 analysis grades); graded ever -- 19 of 19;
endpoint denominator -- 19.

## 1. Orders -- 1 of 1 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-o-1` | nineteen-outcome evidence pass at HEAD, act + owner per outcome not met | `d1c92f63c1` | `2a693d47b3` | AC1 `outcomes 19 of 19 rows_valid 19 duplicates 0 not_met 9 acted 9 owned 9` `VALID`; AC2 `fence_quotes_verbatim 19 of 19`; AC3 `paths_outside_grant 0`; proof VALID rc 0 |

## 2. The measurement (the worker's; `state` is the clause as written, not a grade)

| state | ids | owner of the act |
|---|---|---|
| met 10 | FWD-1, 2, 3, 5, 6, 7, 8, 13, 14, 19 | -- |
| unmet 6 | FWD-10, 11, 12, 15, 16, 18 | all `AMGT_RESAPP` |
| unmeasurable 3 | FWD-4, 9, 17 | all `AMGT_CORPUS` |

**Against round 7's pass (12 / 1 / 6):**
- **FWD-10, 11, 15 and 18 moved from unmeasurable to unmet.** In each, the data half is in the dossier. The worker read portal
  DEV `a93071b833` and found 0 files that consume pillars, management, fund of record or last stated position, or terms (a
  positive control read 98 files).
- **FWD-12 and FWD-16 moved from met to unmet** on their render clauses. The served reader carries the team's cases, and the
  portal renders only Base. FWD-16's reader half is met: ADBE, a PDF-only name, carries pillars 2, management and 3 cases.
- **FWD-9 moved from unmet to unmeasurable.** The code census reads clear (0 of 51 write-like calls reach the library). The
  negative-control arm writes a 308 MB copy to system temp, so under the no-write bound it was not run (row `Z-W1-S15`).
- **The unmet rows share one act, AMGT_RESAPP's served reader.** It would add the dossier's pillars, management, posture,
  model rows and terms, redeploy onto `research_dossier/`, read IMB_LN, AMD_US, AZN_LN and ADBE_US through the deployed
  route, then walk the DSGN_AMGTV1 page.

## 3. The one real run (`evidence/r13_real_run.txt`, CLOUD `2a693d47b3`, 12:59-13:00Z)

This seat re-ran three rows' instruments at HEAD:
- **FWD-1 (met):** `ingest --verify` read `objects 356 files 356 match 356 mismatch 0`, equal to the row.
- **FWD-12 (unmet):** `scoped_amgt._team_cases` as a library served AZN_LN's three cases. IMB_LN and AMD_US were ABSENT with
  their reasons. This equals the row.
- **FWD-4 (unmeasurable): DIFFERENT from the row.** The instrument read `backlog_folders 96`, `unresolved_in_universe 1 of 96`,
  and `picked NONE Hitachi 6501 JP: no report states a ticker in the (Ticker: ...) form`. A new folder, `Hitachi 6501 JP`,
  arrived on the synced library at 12:56Z, six minutes after the worker's run. Its one file is an investment-memo docx, and the
  library now reads 357 files.
  - **Row `Z-S58`, INERT:** the organic arm now exists and refuses for want of evidence. The WILL-ADD and REFUSES-ambiguous limbs
    are still unobserved, so the planted-folder act the row names still stands.
  - FWD-1, FWD-3 and FWD-19 read the folder count after the run. FWD-1's fence scans the resolved folder list, so its 356 of
    356 still holds.

## 4. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S15` | OBSERVATION, INERT: `--code-census` / `--negative-control` write to system temp against a no-write bound | for the analysis: the FWD-9 exercising act must be run under a bound that admits its temp copy |
| `Z-W1-S16` | OBSERVATION, INERT: ML_FP's one pillar has an empty paragraph (158 of 159 carry text) | for the analysis: a pillar-reader repair cell, or served as written |
| `Z-S58` | OBSERVATION, INERT: Hitachi 6501 JP arrived after the run; FWD-4 organic arm reads NO_EVIDENCE | for the analysis |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None on the order. The worker named two judgment calls it made:
- FWD-16 is graded unmet on "renders" although its reader half is met.
- FWD-12's claim that the deployed Lambda still reads the legacy prefix is carried from the order, not measured. The Lambda was
  not called.

## 6. Enrichment candidates for the round-13 analysis

1. **The AMGT_CORPUS acts:**
   - FWD-4: a scratch library with two planted folders, one unresolved and one ambiguous.
   - FWD-9: the negative-control arm, under a bound that admits its temp copy.
   - FWD-17: a scratch-library drive in which a new report lands, the dossier rebuilds, then an unchanged-inputs rebuild
     writes nothing.
2. **The AMGT_RESAPP render acts** (six outcomes, one served-reader change): these go to that project's rounds, not here.
3. **`Z-W1-S16`** (ML_FP pillar text), if the analysis wants it repaired.

## 7. Bounds and residue

- No vendor or gateway call and no S3 write this round. The real run's induction instrument wrote only under `.scratch/r13real/`.
- System temp holds two positive-control files from the worker's `--code-census` (`amgt_corpus_census_ovik1op9`) for operator
  cleanup.
- Worktree `/c/tmp/wk-crps13-1` and older ones hold only untracked scratch. Removing them is a forced delete, done on the operator's
  word.

-- `2.0.0_SA_COO~X`
