# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 43, AMGT-rr-3 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-25

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-rr-3.the-redeploy.md`. It executes
only after BOTH halves are committed and `AMGT-rr-2` is drained on CLOUD. It is round 42's rq-2 in shape, including the CTO's stop
limb 3.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named property:** the `/print?format=rich` body has ONE writer, `render_pack.build_rich_text`. N = 1.

| act | what it MAY touch | expected outcome, read from the producer's own rule | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the current VersionId (read by the lane at build and recorded) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code, built at CLOUD at or after rr-2's drain | every route of that function -- the wildcard `/api/scoped/amgt/*`. The closure diff against the deployed build input (`9b7b146d9a`) is printed in the entry, file by file, before the apply | `/print?format=rich`: the Model Cases section renders each case the Model tab renders (a SERVED case's value; an ABSENT case's reason) in place of the one contradictory line; nothing else in the body changes. `/print` pdf: UNCHANGED. Every other route: no change | re-apply at the recorded prior VersionId; never a delete |

**The lane STOPS on any of three limbs:** (1) the closure diff names a file beyond `lib/research/print/render_pack.py` that reaches a
route this half does not name; (2) `build_pack` changed; (3) the diff touches `scoped_amgt.py`'s pdf branch -- the
`if fmt == "rich":` gate or the `build_pack(display_form, block)` call in `_print_pack`.

The build pip-downloads its pinned wheels from PyPI (declared, as for ro-7 and rq-2). No peers batch and no other served write.

Signed: `2.0.0_SA_COO~Z`, 2026-09-25 ~20:4xZ.
