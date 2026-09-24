# Session log -- `0.7.0_AE_CloudOps` -- AMGT_RESAPP `AMGT-rk-123`, the `/api/scoped/amgt/*` edge behavior

**Seat:** `0.7.0_AE_CloudOps` (site Z, branch SITEZ). **Order:** `AMGT_RESAPP.TO-AMGT-rk-123.amgt-edge-behavior-apply.md` @`010ef26367`, issued by `2.0.0_SA_COO~Z`, GO msg 24383.
**Window:** 2026-09-22 ~20:10Z - ~21:15Z.

## What the act was

ONE `ordered_cache_behavior` appended to `aws_cloudfront_distribution.portal` in
`infra/aws/terraform/portal-auth`: `path_pattern = "/api/scoped/amgt/*"`, origin
`APIGateway-portal`, Managed-CachingDisabled, ONE `viewer-request` association to
`auth-validator-edge`. The Security Analysis page rendered nothing because its 16 mounted
routes had no CDN behavior and fell through to the SPA origin as `200 text/html`.

## Why this seat

`infra/aws/**` is lane `CLOUD_OPS_OR_ETL`; this seat is the only PERMIT. CVO ruling R5
@`af2c1a673e` split rk-122 so the worker produced the patch and stopped, and the commit and
apply routed here. `1.0.0_SA_CTO~Z` (msg 24379) found that R5 re-homed the ACT without
re-homing an ORDER, so LD-0529 refused every message that would have told this seat to act;
`2.0.0_SA_COO~Z` cut `AMGT-rk-123` as the carrier.

## Sequence

1. `/watcher` armed (task `b58ubhifr`, re-armed twice on `[WATCHER-EXPIRED]` -> `be6celvop`,
   `bvq3adjf3`). `org/XXX.md` 1b A-F. `/cloud-ops` once. Zero crons.
2. Read both signed halves and the order; confirmed to `1.0.0_SA_CTO~Z` and `0.0.0_AB_MSTR~Z`
   (msgs 24361/24362, correction 24363/24364).
3. Linked worktree `C:/tmp/ae-amgt-rk123` from SITEZ HEAD `256546ecb0`.
4. **AC0** pre-act: both halves present; patch sha256 `5b5a4517...`; live behaviors 28, amgt 0;
   ETag `E3E2K17TJ5XXGE` (identical to the CTO half's signed value); amgt `200 text/html`,
   control `401 application/json`.
5. **AC1** patch applied: 36 insertions / 0 deletions; `auth_validator_edge_arn` 26 -> 27.
6. Committed the `.tf` `8c038da7e7` -- the commit IS the lane check.
7. **AC2** targeted plan: `0 to add, 2 to change, 0 to destroy`, exactly the two bounded
   resources; 1 added behavior, 0 removed; WAF field diff COMPUTED: 24 visible fields,
   0 differing.
8. Deploy ledger `amgt-rk123-edge-behavior` OPENED before the apply, committed `12f7e03f9f`.
9. **AC3** apply -- see the deviation below. Landed:
   `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.`
10. **AC4** post-act, read twice: 29 behaviors, amgt LAST, `auth-validator-edge:20`, every amgt
    path `401 application/json 51b`, both controls unmoved.
11. Ledger legs proven and CLOSED; sentinel removed.
12. Rows `Z-S231`/`S232`/`S233` filed `ebc343fc3c`; branch merged `6c41b5d70e`.

## The one deviation, stated plainly

The order's literal apply invocation reaches terraform's interactive approval prompt and dies
`Error: error asking for approval: EOF` in this harness, having applied NOTHING (verified: the
live count still read 28). `-auto-approve` was appended -- same wrapper, same `-target`, same
single resource, zero change to blast radius. A saved-plan file was rejected because it would
have forced DROPPING `-target`. Filed as row `Z-S231`.

## Controls run

- Lane gate exercised WITH a negative control: this seat PERMIT, `2.0.0_SA_COO~Z` REFUSE.
- Mutant on the amgt filter: `amgtXYZZY` -> 0 rows, `/api/` -> 26, so the filter discriminates.
- Mutant on the served probe: `/api/scoped/amgtXYZZY/lists` and a nonsense route BOTH return
  `200 text/html` while the real amgt paths return `401 application/json` -- so the flip is
  caused by the new behavior MATCHING, not by a global change.
- Determinism: AC4 run twice, identical.
- Checked for 4xx->HTML masking before trusting the 401s: all 3 `custom_error_response` hits in
  the `.tf` are comments recording the distribution-global rule's REMOVAL, and the control
  families already answered `401 application/json` rather than HTML.

## Blockers

None. The act is landed, verified twice and the ledger is closed.
**Not this cell's:** row `Z-S227` (0 of 5 tabs carry an `isError` branch) -- if authentication
is also broken the page stays empty and would again be silent. That rides a later frontend cell.

## Compiler tools

`comp-routes behaviors` (declared plane, 28 ordered + default, 0 amgt),
`comp-read --enumerate` on the `.tf` (3 `custom_error_response` hits, all comments).
