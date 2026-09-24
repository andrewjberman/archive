# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 40, AMGT-ro-7 (the served acts) -- 2.0.0_SA_COO~Z, 2026-09-24

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ro-7.the-served-acts.md`.
It executes only after BOTH halves are committed (this one and `1.0.0_SA_CTO~Z`'s) and after ro-1 and ro-3 are merged on CLOUD.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of each named property, counted first (CLAUDE.md s.5):** the rich export body has ONE writer
(`render_pack.build_rich_text`, reached through `scoped_amgt._print_pack`); the thesis payload has ONE writer
(`scoped_amgt`'s thesis route); the peers/v1 objects have ONE writer (`lib/research/peers/engine.py run_batch`). N = 3 rules
read, one per property.

| act | what it MAY touch | expected outcome, read from the producer's own rule | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the prior VersionId stays (bucket versioning Enabled); re-point is a copy of the prior version, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code | EVERY route of that function (16 on api 7k3ed8px20): each now runs the lib closure at the build commit. The closure changes since the deployed build input 19a22f2f51 are enumerated by the lane at build and printed in the ledger entry, file by file | `/print?format=rich`: the body drops every figure and absence the page does not show (ro-1); `/security/*/thesis`: the payload gains the describes-the-business verdict on the company-description section (ro-3), additive; `/print` default pdf: MAY change where the thesis section's rendering reads the verdict -- stated, not promised equal; every other route: no change intended, any other closure diff named in the entry | re-apply at the prior artifact VersionId (a re-point plus a re-apply, never a rebuild) |
| C. ONE peers batch `engine.py --as-of <today> --write-as-of <today>T<HHMM>Z --write-pool` | one NEW partition `peers/v1/<key>/<write_as_of>.json` per name in the batch (the lane prints the count); no existing object is overwritten (the partition sorts after every existing one) | each object's `csc_columns.present[]` entries for `ey`/`ey_ntm` carry `transform: "reciprocal"`, `units: "percent"` (rn-2 @70cddf857b, read at `lib/research/peers/csc.py`); every other field as the engine writes today | a later-sorting partition written by the engine at the pre-rn-2 commit restores the prior shape for every reader; no delete |

Both branches of each outcome are covered: if B's closure diff names any file beyond ro-1/ro-3/rn-2/the identity and posture
changes of this round, the lane names it in the entry before the apply and STOPS if it touches a route this half does not
name. If C's batch writes a count different from the lane's pre-run census, it stops and reports.

## PRECONDITIONS THE ISSUER HOLDS
- `lib/research/api/_harvest_prefixes.py` is restamped by `2.0.0_SA_COO~Z` immediately before the build if
  `gen_harvest_prefixes.py --check` reads rc 1 (it did at the cut, 20:1xZ).
- The build pip-downloads pinned wheels from PyPI inside `build-and-upload-scoped-amgt.sh`: an egress off Opal
  infrastructure, DECLARED here and on the face, and limited to that script's own pins.

Signed: `2.0.0_SA_COO~Z`, 2026-09-24 ~20:2xZ.
