# IRPT_DASHBD round 49, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~16:0xZ)

For `3.0.0_SA_CVO`. Each order was re-graded in its worktree and again at box/dell2 after the last drain; all five criteria PASS at HEAD @a240939a26.
round-close-check: orders=4, complete 4, verdict MAY-CLOSE.

| order | worker | risk | criteria | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-99` classifier sensitivity | ~74 | LOCAL | DB49-1-AC1, AC2 PASS | @3d26f11dd6 |
| `IRPT_DASHBD.TO-DB-b-100` W73-S1 (74 DEFECT segments) | ~75 | WORLD | DB49-2-AC1 PASS | @a240939a26 |
| `IRPT_DASHBD.TO-DB-b-101` W73-S2 (123 DEFECT segments) | ~76 | WORLD | DB49-3-AC1 PASS | @be2a66b75a |
| `IRPT_DASHBD.TO-DB-b-102` method_version from the sources entry | ~77 | WORLD | DB49-4-AC1 PASS (106/106) | @e18a26ad12 |

## Results

- **DB-b-99:** thresholds pre-registered at 0faca21881, before the output at 91edf7f120. Nine settings, each summing to 990.
  - ZERO_GAIN_VENDOR_TWR is NOT robust (spread 26 against a limit of 22.5), so its 45 segments are re-graded UNEXPLAINED.
  - All reasons are `inferred`. ADDENDUM 17 relabels FLOW_TIMING and INCOME_DATE `inferred` until DB-b-106's two-sided read.
- **DB-b-100 (74):** all BD_SIDE, 0 producer fixes. Our served series equals the custodian equity on both boundary days in 74 of 74, and BD's own
  identity holds to 2 cents. Causes:
  - BD books admin service fees as flows: 17.
  - BD's boundary value accrues income the custodian paid later: 58 segments, 65 boundaries, 46 matched exactly, 1 unattributed.
  - BD books a net-zero securities transfer as a withdrawal: 1.
- **DB-b-101 (123):** all BD_SIDE, 0 producer fixes. 98 rest on a two-sided read; 25 are by exclusion only (row W76-S1). ADDENDUM 18 item 2: the 98
  are `confirmed`; the 25 stay `inferred`, do not count, and are read again by DB-b-106.
- **DB-b-102:** `method_version` comes from the entry: row 2 custodian, row 3 positions-based, `absent` when there is no entry, and a positions-based
  entry naming 2 is refused. ADVI_COTBKF's ~C2 was told; a Cottonwood entry is still owed on its side.

## For L9 and the CTO

1. **Row `IRPT_DASHBD-D2-W75-S1`: 73 of the 74 W73-S1 segments turn on two of OUR declared conventions,** not defects: service fees kept inside the
   return, and income counted on cash receipt. "BD_SIDE" there means "not a producer defect", not "BD is wrong". This is an ENDPOINT question for
   the CTO: should the FWD-8 comparator follow BD on either convention, or should those segments carry the convention as their stated reason?
2. **Row `IRPT_DASHBD-D2-W75-S2`: dollars are explained, but the return gap mostly is not closed.** After an inferred restatement to BD's convention,
   only 14 of 74 fall within 0.35pp, and 30 are over 2pp. The FWD-8 re-grade will still show most OUTSIDE unless the comparator or the classes
   change. Three income-row matches among 8+ candidates may be coincidental fits.
3. **DB-b-102: `emit_method_row(src=None)` still writes row 2.** The worker kept that so the existing tests pass; it is a residual default path.
4. **`W73_S1_EVIDENCE.json` and `W73_S2_EVIDENCE.json` hold per-account balances and fees** keyed by the tie-out's account keys. They are JSON evidence,
   not `.md`. Grade whether that is acceptable.
