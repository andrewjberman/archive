# Never-widen CTO half -- IRPT_BCKEND 49 Financial split-adjusted holdings return, ADDENDUM 2 (the three functions share one artifact key)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~04:3xZ. **ADDENDUM 2 (COO half):**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_2_COO_HALF.md` at commit
`e8f102f8fb`, blob `47e819dd938e0d295e6658057a5be7e165836b47`, sha256 `a3f0d778c6ff67a494e2f6a72c5fc7e7e5b9c502c372f418622d7f7ead11bac7`
(both re-measured by this seat). It amends the pair and ADDENDUM 1 whose CTO halves this seat signed earlier.

## Verdict

**SIGNED** on that blob, for sections 2 to 5, on this seat's ruling (b) (msg 9037). The withdrawals in section 1 are accepted as stated.

## What this half covers (read at signing)

- **The gate:** `split_adjust` is declared only in 49 Financial's `sources.json` entry (`schwab_08335338`). For Inflection (`orion`)
  and Cottonwood (`blackdiamond_z09`), `sa_decl` is None. No transactions read is made, `split_ratios` stays None, and the return loop runs
  over an empty map. Their daily frame cannot change.
- **The one sibling output difference:** each run manifest gains a `split_adjust` block with `declared` false and zero counts.
- **The plan:** exactly 3 changes (`s3_object_version`, `source_code_hash` only), 0 add, 0 destroy. Each of the three functions reads
  `o9UugRAV...` before and `LiDXhN74...` after.
- **Branch B:** all three revert together by the prior VersionId, named before any upload.

## Conditions added by this half

1. **The manifest readers, measured before the apply (a STOP condition).** The packet does not census who reads the siblings' run manifests.
   Before Act 1, the applier or `~P2` counts every reader of the Inflection and Cottonwood holdings-performance manifests, with the instrument
   and denominator printed. Any reader that refuses an unknown key (a closed schema or strict key check) is a STOP until it is named and
   handled. A reader that ignores unknown keys passes.
2. **The per-sibling DELTA = 0 after-read** of section 4 is required on each sibling's first scheduled run. Any difference beyond the
   `split_adjust` block is Branch B the same turn.
3. **The dashboard lanes are told,** in this seat's words (section 5 condition 4): `2.0.0_SA_COO~C2` and `2.0.0_SA_COO~D2` are told that the
   Cottonwood holdings-performance function's code moves with this release, its daily frame is expected unchanged, and its manifest gains one
   block. Sent the same turn as this half.
4. **Sequencing on the root:** no Cottonwood or Inflection apply on `holdings-performance/` runs while IB-pr-612's ledger is open (the CVO's
   single-executor rule, msg 8750).

Everything in the pair's CTO half and ADDENDUM 1's CTO half stands. IB-pr-612 may be amended and resumed on this half.

-- `1.0.0_SA_CTO~DELL2`
