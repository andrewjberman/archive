# IRPT_BCKEND round 183, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~20:4xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @2b6b3a6109 on the CTO's round-183 analysis (msg 7149) and its addition (msgs 7178 and 7189). One amendment (below). The round-183 analysis's other item, IB-pr-456's after-read and apply, was NOT cut: it waits on Andrew's own PROD submission and execution ID, which has not arrived.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 183 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB183-1 AC1 to AC3 on the merged tree: PASS (AC3: 31 passed, 55 subtests passed).
Push state: LOCAL. The merge `0d0e9e1229` is on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked, and no vendor was called.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-517 | the Opal Ultra Short-Term model added to the comparison catalogue keyed by Opal's own model identity (namespace OPAL, code UST, no YCharts id), the five models in canonical order, its code-pinned policy digest, the YCharts path's refusal of an unmapped entry, the tests | @0d0e9e1229 | 3 of 3 PASS |

## What the CVO needs to know

- **A build, not a served change.** `templates.json`, `maintained_sources.py` and `recipe.py` are packaged into a function; the catalogue serves the new model only after a later, separately signed apply moves that function. That census, never-widen packet and apply are the next cells (not cut here).
- **Design (Andrew-direct ~18:2xZ, vendor-agnostic; CTO msg 7189):** the entry has no YCharts id. The composition requires a `vendor_id` field and a code-pinned digest per key, not a YCharts id (row D2-S149), so the OPAL-namespace entry carries Opal's own code. Scope is the five models the Model Portfolios page lists; Fixed Income and the two 50/50 blends are in the portal's colour map but not in that served list and were not added.
- **ISSUER DEFECT (mine, caught by the worker's stop rule, rows D2-W366-S1 and S5):** my first design put the refusal of an unmapped entry only on the older `validate_envelope` path. The live YCharts path (`report_security_ids`, called by the resident worker) copies each comparison's `vendor_id` into the vendor body, so an OPAL entry would have been sent to YCharts as if `UST` were a YCharts id. AMENDMENT 1 (@f127a6570b) moved the refusal to `report_security_ids` and granted the pin-set test the new pin broke. I also first declared the order SERVED; the gate refused it against the WORLD floor `templates.json` sets, and I re-declared WORLD.
- **The check could fail for the right reason:** at the amended order, on the worker's tree before its fix, AC3 failed with "an OPAL comparison was sent to the YCharts body".
- **Not fixed here (row D2-S150, owner me):** four custody tests fail at base (cause untraced; the catalogue is not on their path); the older `comparison_security_ids` helper reads a `security_id` key the admitted projection lacks and has no non-test caller.
- **Rows:** D2-S148, S149 (the identity question and its answer), S150 (dispositions of the worker's S1 to S8). STILL ARMED, owner me: W349-S1, W361-S1, W348-S2.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
