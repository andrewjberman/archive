# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 42, AMGT-rq-2 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-25

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-rq-2.the-redeploy.md`.
It executes only after BOTH halves are committed (this one and `1.0.0_SA_CTO~Z`'s) and after `AMGT-rq-1` is drained on CLOUD.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named property, counted first:** the `/print?format=rich` body has ONE writer, `render_pack.build_rich_text`,
reached through `scoped_amgt._print_pack`. N = 1 rule read.

| act | what it MAY touch | expected outcome, read from the producer's own rule | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the current VersionId `VTj2mj_gOKupat_bPjetck3HPD0N6PIJ` stays (bucket versioning Enabled); a re-point is a copy of it, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/` moving ONLY `opal-amgt-scoped-api`'s code, built at CLOUD at or after rq-1's drain | EVERY route of that function (16 AMGT routes on api 7k3ed8px20). The closure diff against the deployed build input is printed in the ledger entry, file by file, before the apply | `/print?format=rich`: the body changes as rq-1's own rule states -- one Thesis empty-state line in place of one marker per undrafted section; Exec Management's absence in the page's words; the Posture absence line carried; fiscal-year figures limited to the years the Model tab shows. `/print` default pdf: UNCHANGED if the closure diff shows `build_pack` untouched; if it shows `build_pack` changed, the lane STOPS. Every other route: no change intended | re-apply at `VTj2mj_gOKupat_bPjetck3HPD0N6PIJ` (a re-point plus a re-apply, never a rebuild) |

**Both branches of each outcome are covered.** If B's closure diff names any file beyond `lib/research/print/render_pack.py`,
the lane names it in the entry before the apply. It STOPS if that file reaches a route this half does not name, or if
`build_pack` changed.

## PRECONDITIONS THE ISSUER HOLDS

- `lib/research/api/_harvest_prefixes.py` is restamped by `2.0.0_SA_COO~Z` immediately before the build if
  `gen_harvest_prefixes.py --check` reads rc 1.
- The build pip-downloads pinned wheels from PyPI inside `build-and-upload-scoped-amgt.sh`. That is an egress off Opal
  infrastructure, DECLARED here and on the face, and limited to that script's own pins. The CTO signed the same limb for ro-7
  (`ledger/NEVER_WIDEN_ROUND40_RO7_CTO_HALF.md` s.3).
- No peers batch and no other served write: this order moves the function's code only.

Signed: `2.0.0_SA_COO~Z`, 2026-09-25 ~05:0xZ.
