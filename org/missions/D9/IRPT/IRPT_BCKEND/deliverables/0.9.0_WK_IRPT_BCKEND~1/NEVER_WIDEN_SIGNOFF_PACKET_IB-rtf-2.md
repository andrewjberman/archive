# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtf-2

**THE PARTIAL GRANT SERVED WITH ITS UNPROJECTED COUNT DISCLOSED.** CTO ruling @61627f39f9. Cell
`IB-rtf-2`. Worker `0.9.0_WK_IRPT_BCKEND~1`. Written per CLAUDE.md Rule 5 (`NEVER move served
output without never-widen sign-off`) and this order's arm (d): a served-behaviour change on a
live auth path carries its own never-widen halves, or it does not deploy.

This packet is the ACT's blast-radius description. It does not itself constitute a sign-off --
`2.0.0_SA_COO~B` (this project's issuer) and `1.0.0_SA_CTO` each sign their own half against the
`blob <hash>` this file carries at HEAD, per Rule 5's mechanism (`org/tier1_exec/<seat>/
deliverables/NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtf-2_*.md`).

## THE ACT

Deploy `infra/aws/lambda/investor-reporting/_authz/enforce.py` (the refusal-order inversion) and
`infra/aws/lambda/investor-reporting/_authz/served.py` (the `unprojected_grant` disclosure field
on `response_envelope()`) to every Lambda function that packages `_authz/` -- the shared module
is bundled into each function's own zip (there is no shared layer for `_authz` at this vintage;
`infra/aws/lambda/ci/build-and-upload.sh` packages it per function).

## THE KEYS -- THE N SERVING FUNCTIONS' BYTES

`N = 7`. Every function that packages `_authz/enforce.py` and `_authz/served.py`, per
`infra/aws/lambda/ci/lambda-source-map.json` / `BUILD_MANIFEST.json` declarations (the same
population `battery_ib_rte_6.py`'s `FUNCTIONS` tuple and its `arm_c_deploy` already enumerate for
this project):

| # | function_name              | prior `CodeSha256` (rollback target, read live this run) | LastModified (live) |
|---|-----------------------------|------------------------------------------------------------|----------------------|
| 1 | irpt-directory-search       | `v0MMA3yUxIPNdCMXhE/2pSD9lU+5LgI945JqkuULH8U=`               | 2026-09-19T00:42:28Z |
| 2 | irpt-export-render           | `WJ8Nk/Zr2g1/cafjnJvF1glFiMdPiFc7Bt8hktqsxuo=`               | 2026-09-19T00:48:52Z |
| 3 | irpt-holdings                | `R2+ff33uJO3jrCOuMII9y6SvEhvG43wfeXrGbn0pJGk=`               | 2026-09-19T00:50:04Z |
| 4 | irpt-narrative               | `XUJ68NaABwFNW9ItzMBO5l0Jvb2pG5t+ot833bkLY5g=`               | 2026-09-19T00:51:34Z |
| 5 | irpt-status                  | `twhh/jwDdSwzQ6/BtFdkl52jXYuO19AfVviu/+FlD5A=`               | 2026-09-19T00:52:59Z |
| 6 | irpt-performance-adapter     | `xI2iPO5/5WTf2a6rqgdL6kXJZ3ODiDZI22pz51jGMuQ=`               | 2026-09-19T00:55:02Z |
| 7 | irpt-ycharts-generate        | `4TF3bfgPezMaZvx7tZdwJHOF6S7GyRq0ayI6s5ryV3s=`               | 2026-09-19T01:01:28Z |

Read via `.tools/aws lambda get-function --function-name <fn> --query
"Configuration.[FunctionName,CodeSha256,LastModified]"`, this run, 2026-09-19. These are the
DEPLOYED bytes at packet-write time -- the ROLLBACK for each key is "re-publish this exact
`CodeSha256`" (Terraform `filename`/`source_code_hash` pinned back to the pre-deploy zip; NEVER
`aws lambda update-function-code`, per CLAUDE.md NEVER-9).

## THE BLAST RADIUS -- BOTH BRANCHES, EVERY FIRM

Every `FIRM_ADVISOR` (and `FIRM_OPERATIONS`/`OPAL_GLOBAL`/`CLIENT`) response served by these 7
functions, for every firm currently reachable through `IRPT_DIRECTORY_BUCKET_MAP`
(49financial/`opal-data-bd`, inflection/`opal-data-inf`, cottonwood/`opal-data-cot`), on BOTH
branches this order's inversion touches:

  * **SERVED (non-empty permitted set).** Every scoped response now carries one ADDITIONAL
    top-level field, `unprojected_grant: {count, denominator, kinds}`, present at zero. No
    existing field is renamed, removed or retyped; `additionalProperties` is closed only on
    `ResolvedScope` (untouched by this order) and NOT on the outer response envelope, so this is
    an additive change to a shape with no schema to violate. A grant that is FULLY projected
    (the ordinary case for every firm other than 49financial's abby_horton-class advisors) is
    unaffected in its `data` and reads `unprojected_grant.count == 0`.
  * **SERVED where the OLD code refused (the row W1-S27 case).** An advisor whose ownership grant
    partially fails to project (some ids in a key space this directory cannot join, e.g. the
    49financial identity-bridge seam's ~79 percent resolution rate, row W1-S25) is now SERVED the
    matched subset instead of refused whole. This is the load-bearing behaviour change: a caller
    that previously received `NOT_AUTHORIZED`-shaped `UNPROJECTED_GRANT` (data: null) for such a
    grant now receives a served, non-null `data` with the gap disclosed.
  * **REFUSED (still).** An EMPTY permitted set is refused on both codes exactly as before
    (`UNPROJECTED_GRANT` when every grant was unprojected, `EMPTY_GRANT` otherwise) -- the
    empty-projected-set branch is unconditionally preserved per the ruling's condition 3 and
    `test_an_unprojected_grant_is_refused_and_not_served_empty` / the new
    `test_a_cross_firm_advisor_id_is_refused_empty_grant_not_unprojected` (both pass, this run).
  * **The six OBJECT-swap refusals** (`firm`/`advisor`/`account`/`relationship`/`report`/`pdf`
    outside scope) and the cache-hit reauthorization path are UNCHANGED -- `Enforcer.covers()`
    and the cache-key/reauthorize machinery are not touched by this order.

## ROLLBACK

Per key: re-publish the function at the prior `CodeSha256` printed in the table above, via
Terraform (`filename`/`source_code_hash` pinned to the pre-deploy zip), never
`aws lambda update-function-code`. Verified by `served == CodeSha256` read back after rollback,
the same discriminator arm (e) uses to verify the forward deploy.

## WRITERS OF THE SERVED-BEHAVIOUR PROPERTY

`W = 1`. The ONLY writer of what these 7 functions serve for a scoped route is a Lambda code
deployment of `_authz/enforce.py` + `_authz/served.py` (bundled per function by
`infra/aws/lambda/ci/build-and-upload.sh`). Checked, not assumed: `comp-find
'cache_ttl|CachingEnabled|cache_enabled|cache_cluster' infra/aws/terraform/investor-reporting`
this run returns 0 hits across 47 files scanned -- no API Gateway response caching is configured
on this project's routes. The portal-auth CloudFront distribution in front of these routes
(`infra/aws/terraform/portal-auth/cloudfront-distribution.tf`) runs the Lambda@Edge AUTH
validator (`auth-validator-edge/index.mjs`) on `viewer-request`/`origin-request`; it authenticates
and injects the nine trusted headers `_scope.py` reads and does not cache or transform the
Lambda's response body, so it is not a second writer of this property. `Entry`'s own warm cache
(`served.py`, "THE CACHE IS PER-REQUEST UNLESS A CALLER EXPLICITLY SHARES ONE") is per-invocation
by default for every one of these 7 functions (none passes a shared `cache=` at construction --
re-derivable from each `entry.py`'s `ENTRY = _entry.Entry(...)` call, none of which supplies
`cache=`), so it is not a second writer either.

## EXPECTED OUTCOME, BOTH BRANCHES (READ FROM THE PRODUCER'S OWN RULE, PER RULE 5)

  * If both never-widen halves are SIGNED before this order's second pass: the deploy in arm (e)
    changes the 7 `CodeSha256` values above to the newly built zips, verified `served ==
    CodeSha256 == built` (never by filename), and the live request for `abby_horton`/49financial
    reads `k >= 1` permitted with `count = 43 - k` disclosed (row W1-S27's own numbers: k=21,
    count=22, measured by `battery_ib_rte_6.py arm_b_join_rates`, this project, prior cell).
  * If a half is REFUSED: no deploy occurs from this packet; the 7 functions stay at the
    `CodeSha256` values in the table above; row W1-S27 stays ARMED and this order stays open.

## VINTAGE

Written `0.9.0_WK_IRPT_BCKEND~1`, first pass, 2026-09-19, on worktree HEAD `958d6a8e94`. This
file's own `blob <hash>` (read via `git hash-object` after commit) is what each half's sign-off
names.
