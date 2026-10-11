# THRESHOLD_CLAIM_RULE24 -- the claim each guard threshold carries in dim_return_method (IRPT_DASHBD TO-DB-b-118)

Authored by 0.9.0_WK_IRPT_DASHBD~93 BEFORE any producer edit, on base box/dell2 @449c59379b. The machine-read form is
`THRESHOLD_CLAIM_RULE24.json` in this folder; line evidence is there. CTO ruling msg 4060: thresholds are the run's own values with their claim.

**Schema adopted.** A per-value claim, drawn from the law's four (measured / inferred / held / absent), on each of the five guard thresholds the
method row states. Declared domain: how `emit_method_row` knows each threshold value it writes.

**Four postulates.**
- MECE: five values, four routes, zero left over. tolerance and large_flow_share are computed from the run (measured); the excluded-weight ceiling is
  derived from them and the band (inferred); the two band ends are constants (held); a value the code cannot produce is None (absent).
- Same grain: per threshold value, because one row mixes three ways of knowing; the row stays one per method_version.
- Intent coherence: the claim says how the value is known, nothing about whether it is good. Whether a claim was stated or defaulted is a second
  axis with its own single field, so `held` never means two things. Grading reads values, never claims.
- State coherence: re-measuring moves values (and the ceiling's value), not the band, not the claims; no claim change moves a grading path; the
  already-served 49F row 2 partition is not an input and is not rewritten.

**Token census.** Word-boundary, case-insensitive, 131 files scanned in the producer folder plus `org/standards`: measured 514 hits in 65 files,
inferred 122 in 23, held 159 in 37, absent 347 in 69. Whole repo (68,576 files): `threshold_claims` 6 hits in 2 files, all this cell's own order
and check; `tolerance_claim` and `threshold_claims_source` 0. No collision; the limit is that the four words are common English and are scoped.

**Decision.** Field `threshold_claims` (input key, an object value name -> claim). On the row: five flat string columns `<value>_claim` plus
`threshold_claims_source` (`stated` | `defaulted_no_claims`). Written to the dim_return_method parquet and, through the manifest's row spread, the
manifest. A thresholds input with NO claims is not refused and is never read as measured: each non-null value is written `held`, each null value
`absent`, source `defaulted_no_claims`. A present-but-malformed claims object is refused (partial, unknown key, claim outside the four, null under
a claim other than `absent`, non-null under `absent`). `thresholds=None` behaves exactly as before.

**Known cost.** The `dim_return_method` contract (`org/standards`, 0.3.0) declares the row's current columns; the round-10 check that equates them to
the row literal will fail for the six new columns until the issuer bumps the contract. It is outside this order's grant: a surprise row is filed.
