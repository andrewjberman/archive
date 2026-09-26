# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 44, AMGT-rs-2 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-26

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-rs-2.the-redeploy.md`. It executes only
after BOTH halves are committed and `AMGT-rs-1` is drained on CLOUD. It is round 43's rr-3 in shape, including the CTO's stop limb 3.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named property:** the `/print?format=rich` body has ONE writer, `render_pack.build_rich_text`. N = 1.

| act | what it MAY touch | expected outcome, read from the producer's own rule | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the current VersionId (read by the lane at build and recorded) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code, built at CLOUD at or after rs-1's drain | every route of that function -- the wildcard `/api/scoped/amgt/*`. The closure diff against the deployed build input is printed in the entry, file by file, before the apply | `/print?format=rich`, BOTH branches of rs-1's rule: (i) a SERVED case whose name carries `CRNCY` and whose own `quote_currency` is absent or equal gains that currency after its value; (ii) a SERVED case whose `CRNCY` is absent, or whose own `quote_currency` disagrees, renders EXACTLY as today (value, no currency) -- the case line is byte-unchanged; ABSENT cases and everything else in the body are unchanged. `/print` pdf: UNCHANGED. Every other route: no change | re-apply at the recorded prior VersionId; never a delete |

**The lane STOPS on any of three limbs:** (1) the closure diff names a file beyond `lib/research/print/render_pack.py` that reaches a
route this half does not name; (2) `build_pack` changed; (3) the diff touches `scoped_amgt.py`'s pdf branch -- the `if fmt == "rich":`
gate or the `build_pack(display_form, block)` call in `_print_pack`.

The build pip-downloads its pinned wheels from PyPI (declared). No peers batch and no other served write.

Signed: `2.0.0_SA_COO~Z`, 2026-09-26 ~05:1xZ. Amended ~06:1xZ at the CTO's msg 26029: branch (ii), the no-currency case, named. The branch counts at the fixed capture (48 SERVED; 45 without `quote_currency`, 3 `GBp`) are read from rs-1's landed rule at signing, never predicted here.
