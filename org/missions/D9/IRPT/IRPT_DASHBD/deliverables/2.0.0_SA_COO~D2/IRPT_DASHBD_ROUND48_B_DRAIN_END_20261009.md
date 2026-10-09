# IRPT_DASHBD round 48, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~14:4xZ)

For `3.0.0_SA_CVO`. One LOCAL order serving FWD-8. The issuer re-graded it in the worker worktree and again at box/dell2 after the drain.
round-close-check: orders=1, complete 1, verdict MAY-CLOSE.

| order | worker | risk | criterion (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-98` the 510 UNEXPLAINED tie-out segments | ~73 | LOCAL | DB48-1-AC1 PASS (990 of 990 outside in by_reason; 510 of 510 classified, distinct) | @3562d0ab96 |

## Result over the 990 OUTSIDE segments of TIEOUT_COMPOUND_V2 (49F vs Black Diamond, 0.35pp)

| reason | segments |
|---|---|
| FLOW_TIMING | 449 |
| NEAR_ZERO_BASE (new) | 156 |
| BOUNDARY_VALUE_GAP (new) | 96 |
| ZERO_GAIN_VENDOR_TWR (new) | 45 |
| INCOME_DATE | 26 |
| WINDOW_ONE_DAY_SHIFT (new) | 13 |
| COVERAGE_DAYS | 4 |
| FLOW_CONVENTION_ENVELOPE (new) | 3 |
| MISSING_PRICE | 1 |
| DEFECT | 197 |

The sum is 990. Of the 510 formerly UNEXPLAINED, 313 are reasoned and 197 are DEFECT. The reason set's rule-24 record is
`deliverables/0.9.0_WK_IRPT_DASHBD~73/REASON_SET_RULE24.md`.

## For L9 (judgment)

1. **Thresholds are the worker's choice.** NEAR_ZERO_BASE uses 1% of peak, and the dollar tie uses $1 or 0.1%. Grade whether they are defensible. The
   reasons are inferred from the inputs, not confirmed by Black Diamond.
2. **197 DEFECT segments in two rows.**
   - `IRPT_DASHBD-D2-W73-S1` (74): the dollars disagree with Black Diamond, and the dollar gap does not account for the return gap.
   - `IRPT_DASHBD-D2-W73-S2` (123): the dollars tie and the base is not near zero, but no test closes the gap.

   FWD-8's ACCEPT ("every day they disagree carries a stated reason") is not met while these stand. They are the CTO's next enrichment.
3. **`IRPT_DASHBD-D2-W73-S3`: an issuer face error.** The face said V2's segment rows carry no reason. Every OUTSIDE row does carry `reason` and
   `evidence`; the issuer sampled a WITHIN row. The 510 were re-derived from those rows, and the verdict is unaffected.

**Reads:** S3 GETs of the served gold series and Black Diamond's landed bronze only. No vendor call, no AWS write, no client identifier in any .md file.
The tolerance stays Andrew's word (open call 2f53, REC 0.35pp).
