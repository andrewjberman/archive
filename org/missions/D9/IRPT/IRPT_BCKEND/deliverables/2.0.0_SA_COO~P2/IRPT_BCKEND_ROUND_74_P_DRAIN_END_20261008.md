# L8 drain end -- IRPT_BCKEND round 74, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~02:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (the infra/
floor; the deployed zip is unchanged)

**Cut from:** the issuer's ruling on row S381 (0.7.0_AE_CloudOps~I). Issuance @cc2c684238, decomposition section 67. **Judgment criteria:** 0.

## The order

**IB-pr-360, slot ~168, drained @37d65133d1.**
- `backfill_covered_account_ids.py` (IB-pr-344's operator tool) moved by `git mv` from the top of the export Lambda's source dir to
  `export/tools/`.
- Its `sys.path` insert points at the parent export dir, so it still imports `bundle` unchanged.
- Its test changed only in its path setup.
- No build script, source map or packaged member changed.

**Graded.** IB74-1-AC1 PASS, re-run by the issuer at HEAD:
- the build's ADHC_DRIFTD.002 rule, reproduced exactly, finds 0 extras over 64 union members (base: 1);
- `--help` runs from the new home;
- the tool's 7 tests pass.

Proof VALID.

## Why it mattered

Every irpt-export-render build since IB-pr-344 needed `BAU_PARITY_SKIP=1`, which turns off the extras limb for the whole source dir.
The next export release (the custody route, IB-pr-351/352/355) can now build with the limb on.

## Rows

| row | status |
|---|---|
| S381 | Resolved by row S389. |
| S388 | Still open, ~P2: the portal wire drift in 4 AnalysisReport-related files, recorded for its owner. |

**Push state:** LOCAL at the time of writing.
