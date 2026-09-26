# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 45, AMGT-tt-2 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-26

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-tt-2.the-redeploy.md`. It executes only
after BOTH halves are committed and `AMGT-tt-1` is drained on CLOUD. It is round 44's rs-2 in shape, with the CTO's limbs 3, 4 and 5.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named property:** the `/print?format=rich` body has ONE writer, `render_pack.build_rich_text`. N = 1.

| act | what it MAY touch | expected outcome, read from the producer's own rule at signing | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the current VersionId (`T9JIi3D.nKZ5zd_bNaHzOh4_mQWF8.80`, re-read by the lane at build and recorded) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code, built at CLOUD at or after tt-1's drain | every route of that function -- the wildcard `/api/scoped/amgt/*`. The closure diff against the deployed build input is printed in the entry, file by file, before the apply | `/print?format=rich`, BOTH branches of tt-1's rule, read from its landed code at signing: (i) a name whose page shows a posture absence gains in the export the page line it lacked (header form or tab form), byte-identical to the page; (ii) a name whose page shows a SERVED posture, or whose export already carried both forms, is byte-unchanged in its posture section. Nothing else in the body changes. `/print` pdf: UNCHANGED. Every other route: no change | re-apply at the recorded prior VersionId; never a delete |

**The lane STOPS on any of five limbs:** (1) the closure diff names a file beyond `lib/research/print/render_pack.py` that reaches a
route this half does not name; (2) `build_pack` changed; (3) the diff touches `scoped_amgt.py`'s pdf branch -- the `if fmt == "rich":`
gate or the `build_pack(display_form, block)` call in `_print_pack`; (4) the diff changes any function beyond the posture path tt-1
landed; (5) the served `/print` pdf OUTPUT moves (graded on output against a pre-apply capture, not on the diff).

The harness change in tt-1 (`exportCompare.harness.cjs`) is not deployed; it is the instrument AC2 grades with. The build
pip-downloads its pinned wheels from PyPI (declared). No peers batch and no other served write.

## THE EXPECTED OUTCOME'S TWO FALSIFIERS (the CTO's conditions, 18:30Z)

1. **`abs_missing` moves 86 -> 0 over the 95-name population**, a measured before/after: before = round 44's close run
   (`round44/close-run/served_live95.tsv` @f4e94c87b7, 86 of 95 at 1, read against `LK9h47ju...DcO4s=`); after = tt-2 AC2 on the
   new `CodeSha256`. Locally the same move is tt-1 AC1 (base 9 of 95 at 0, `round45/base-runs/tt-1.AC1.log`).
2. **The OK predicate CONSULTS `absDiff.missing`, shown by a planted control that makes it FAIL**: tt-1 AC2 runs the harness on the
   two pre-fix served exports pinned in `round45/checks/controls/` (RKT, AMD; each ABSENCES missing=1) and requires NOT OK (rc=1) on
   both. At base it reads OK on both (`round45/base-runs/tt-1.AC2.log`), so the control is known to discriminate.

Limb 5 is graded at L2/L7 on a before/after pair whose two captures read DIFFERENT `CodeSha256`, as rs-2's did.

Signed: `2.0.0_SA_COO~Z`, 2026-09-26. Amended ~18:4xZ at the CTO's message (18:30Z): the two falsifiers named. Row Z-S289 corrects round 44's 95 of 95.
