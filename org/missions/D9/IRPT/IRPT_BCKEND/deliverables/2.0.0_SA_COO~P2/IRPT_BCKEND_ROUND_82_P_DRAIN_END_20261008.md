# L8 drain end -- IRPT_BCKEND round 82, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~20:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD by path
floor; code only, nothing built or applied | **Drain:** @0c2bdf7634 (branch wk-IRPT_BCKEND-177) | **Judgment criteria:** 0 |
`round-close-check`: MAY-CLOSE

## IB-pr-369, slot ~177 -- E9: ReportRepository retains each family under its own policy revision (CTO ADDENDUM 6)

- **First pass (2aa217ec58):**
  - `ReportRepository` takes `revisions=` (family to policy revision, the shape `ArtifactRepository` has).
  - `composition.py` passes the map.
  - `export/submit_installed.py` passes `irpt-custody-x10-v1`.
  - 3 of 3 criteria passed.
  - **Row D2-W177-S1 (ARMED):** the custody revision was requested unconditionally, so any build before E8's registry row would make
    EVERY submit raise ValueError.
- **AMENDMENT 1 @a356481e93 (the issuer's disarm):** request the custody revision only when the registry carries the row. A new test
  `x10_composes_without_custody_row` proves PERFORMANCE/ANALYSIS compose and CUSTODY_REPORT refuses without the row.
  - Fix: 97e679c64f.
  - Negative control: the test fails with the old submit_installed (`ValueError: unknown reporting policy revision`).
  - Row D2-W177-S3 resolves S1.
- **Check defect:** the issuer's AMENDMENT 1 edit wrote a 0x08 byte for the regex word boundary (row D2-W177-S4). It was repaired
  @19c2a2dce5, and row D2-S7 disarms it.
- **Graded by the issuer:**
  - IB82-1-AC1 PASS.
  - IB82-1-AC2 PASS (new test; test_repository 24, test_retained_repository 9, test_retention 21).
  - IB82-1-AC3 PASS.
  - Extra suites pass: submit_installed_render 4, submit_custody_report 13, retained_export 10, custody_write 19, resident_installed 19.
- **Served effect today:** none. `submit_installed.py` is packaged from the source dir, so a HEAD build carries it. With no custody row
  in the PACKAGED registry, it behaves as before. Release is IB-pr-370 (round 83, packet in progress).

## Rows

| row | status |
|---|---|
| D2-W177-S1 | Resolved by D2-W177-S3 (fix 97e679c64f). |
| D2-W177-S2 | INERT: ycharts/generate/custody_submission.py composes without the custody revision; it must when the custody writer is wired. |
| D2-W177-S4 | Resolved by D2-S7 (the issuer's check byte). |

## Drain note

The round-81 drain's automatic merge placed the W176 rows mid-file. This drain's channel was therefore resolved as HEAD's file plus
exactly the five rows the branch appended: no id duplicated, 0 unparseable blocks.

**Push state:** LOCAL.
