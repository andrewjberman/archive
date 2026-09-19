# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtf-8

**HOLDINGS' FORKED ENFORCER FOLDED ONTO THE SHARED MODULE.** CTO ruling S82 @b37fdfd5cd. Cell
`IB-rtf-8`. Worker `0.9.0_WK_IRPT_BCKEND~1`. Written per CLAUDE.md Rule 5 (`NEVER move served
output without never-widen sign-off`) and this order's arm (d): a served-behaviour change on a
live auth path carries its own never-widen halves, or it does not deploy.

This packet is the ACT's blast-radius description. It does not itself constitute a sign-off --
`2.0.0_SA_COO~B` (this project's issuer) and `1.0.0_SA_CTO` each sign their own half against the
`blob <hash>` this file carries at HEAD, per Rule 5's mechanism (`org/tier1_exec/<seat>/
deliverables/NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtf-8_*.md`).

## THE ACT

Deploy `irpt-holdings` with `enforce.py` now materialized at build time from the COMMITTED,
sha256-verified blob of `infra/aws/lambda/investor-reporting/_authz/enforce.py` (the shared,
already-corrected module -- CTO ruling @61627f39f9's project-first inversion) instead of the
STALE committed flat copy this function used to ship (`holdings/enforce.py`, deleted this order;
blob `8f849457be`, byte-identical to `_authz/enforce.py` as it stood at commit `28ccac62c9`,
which PRE-DATES the inversion). No other function's bytes are touched by this act; no other route
deploys.

## THE KEY -- THE ONE SERVING FUNCTION'S BYTES

`N = 1`. Only `irpt-holdings` packages the fork; the census below (this order's arm (c)) confirms
the other six functions this project ships already bind `_authz/enforce.py` through
`staged_from` and are unaffected by this act.

| # | function_name | prior `CodeSha256` (rollback target, read live this run) | LastModified (live) |
|---|----------------|------------------------------------------------------------|----------------------|
| 1 | irpt-holdings  | `oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs=`               | 2026-09-19T05:37:12Z |

Read via `.tools/aws lambda get-function-configuration --function-name irpt-holdings --query
"{CodeSha256:CodeSha256,LastModified:LastModified}"`, this run, 2026-09-19. This is the DEPLOYED
byte at packet-write time -- the ROLLBACK is "re-publish this exact `CodeSha256`" (Terraform
`filename`/`source_code_hash` pinned back to the pre-deploy zip; NEVER `aws lambda
update-function-code`, per CLAUDE.md NEVER-9).

**NOTE, surfaced as row `IRPT_BCKEND-W1-S31`:** this LIVE value does **not** match
`infra/aws/lambda/ci/lambda-source-map.json`'s own recorded `functions.irpt-holdings
.artifact_sha256` (`Bn7iLO/E/9CKYP0sz0YdneloZLHdldHkr/c3jWc25Xc=`) -- the manifest field is stale
relative to what AWS actually serves (a later redeploy, likely IB-rtf-6's own arm (e) pass over
`served.py`/`loaders.py`, moved the served bytes without updating this field, since it is
untouched by this order's own BOUNDS). This packet uses the LIVE read as the rollback target, per
Rule 5's "read from the producer's own rule at signing, never predicted from the input's shape."

## THE BLAST RADIUS -- BOTH BRANCHES, EVERY FIRM `irpt-holdings` SERVES

Every `FIRM_ADVISOR` (and `FIRM_OPERATIONS`/`OPAL_GLOBAL`) holdings-snapshot response served by
`irpt-holdings`, for every firm reachable through `IRPT_DIRECTORY_BUCKET_MAP`
(49financial/`opal-data-bd`, inflection/`opal-data-inf`, cottonwood/`opal-data-cot`), on BOTH
branches this fold touches:

  * **SERVED (non-empty permitted set, no gap, or a gap the fork's refusal branch never caught --
    e.g. a `NOT-IN-DIRECTORY` or `CROSS-FIRM` reason, never `UNPROJECTED-ID`).** Under the STALE
    fork this was served with `unprojected_grant` ABSENT from the Enforcer's own census, so
    `_authz/served.py`'s `response_envelope()` defaulted the top-level `unprojected_grant` field
    to `{count: 0, denominator: 0, kinds: {}}` regardless of the true gap -- a truthful partial
    masked as a clean one. Under the fixed shared module the SAME request now carries the REAL
    `{count, denominator, kinds}` for every gap between what was granted and what the directory
    could match. No existing field is renamed, removed or retyped; this is additive to a shape
    with no closed schema on the outer envelope.
  * **SERVED where the STALE fork REFUSED WHOLE (the load-bearing behaviour change).** The fork's
    `resolve_now` refused `UNPROJECTED_GRANT` whenever ANY grant carried an unprojected-id gap,
    even when the permitted set (after projecting the OTHER grants) was non-empty -- so an
    advisor with a mix of properly-projected and unprojected grants got NOTHING instead of a
    truthful partial. The fixed module projects first and refuses only when the RESULT is empty
    (CTO ruling @61627f39f9); such an advisor is now SERVED the projected subset with the gap
    disclosed in `unprojected_grant`.
  * **REFUSED (still).** An EMPTY permitted set is refused on both codes exactly as before
    (`UNPROJECTED_GRANT` when every grant was unprojected, `EMPTY_GRANT` otherwise) -- unchanged
    by this fold; `test_an_unprojected_grant_is_refused_and_not_served_empty` (in `_authz/tests/`)
    and this cell's own holdings suite both pass, this run.
  * **The six OBJECT-swap refusals** (`firm`/`advisor`/`account`/`relationship`/`report`/`pdf`
    outside scope) and `Enforcer.covers()` are UNCHANGED -- the fold touches only `enforce.py`'s
    provenance (which file's bytes get bound), never `covers()`'s logic, which was already
    byte-identical between the fork and the shared module (the diff arm (a) printed: `covers()`
    is not in the only-in-fork/only-in-shared hunks).

## ROLLBACK

Re-publish `irpt-holdings` at `CodeSha256` `oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs=` via
Terraform (`filename`/`source_code_hash` pinned to the pre-deploy zip), never `aws lambda
update-function-code`. Verified by `served == CodeSha256` read back after rollback, the same
discriminator arm (e) uses to verify the forward deploy.

## WRITERS OF THE SERVED-BEHAVIOUR PROPERTY

`W = 1`. The ONLY writer of what `irpt-holdings` serves for the holdings-snapshot route is a
Lambda code deployment of its own zip (`infra/aws/lambda/ci/build-and-upload.sh`, this cell's
`staged_from` addition for `enforce.py`). Checked, not assumed: `comp-find
'cache_ttl|CachingEnabled|cache_enabled|cache_cluster' infra/aws/terraform/investor-reporting`
(re-run this cell, same as `IB-rtf-2`'s packet) returns 0 hits across 47 files scanned -- no API
Gateway response caching on this project's routes. The portal-auth CloudFront distribution's
Lambda@Edge AUTH validator authenticates and injects trusted headers; it does not cache or
transform the Lambda's response body, so it is not a second writer. `Entry`'s own warm cache is
per-invocation for `irpt-holdings` (its `ENTRY = _entry.Entry(...)` call in `entry.py` supplies
no shared `cache=`), so it is not a second writer either.

## EXPECTED OUTCOME, BOTH BRANCHES (READ FROM THE PRODUCER'S OWN RULE, PER RULE 5)

  * If both never-widen halves are SIGNED before this order's second pass: arm (e) deploys the
    rebuilt zip, verified `served == CodeSha256 == built` (never by filename), and the live
    request for `abby_horton`/49financial against `irpt-holdings` reads a served holdings
    response with `unprojected_grant.count = denominator - k`, `count > 0` where the fork would
    have shown `count == 0` (or refused whole).
  * If a half is REFUSED: no deploy occurs from this packet; `irpt-holdings` stays at
    `CodeSha256` `oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs=`; the false-negative on this route
    stays live and this order stays open.

## VINTAGE

Written `0.9.0_WK_IRPT_BCKEND~1`, first pass, 2026-09-19, on worktree HEAD after the fold commit.
This file's own `blob <hash>` (read via `git hash-object` after commit) is what each half's
sign-off names.
