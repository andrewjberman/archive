# X-1 release -- never-widen pair DRAFT (TCKT_VNEXT C-ONE-DOOR)

**Drafted by** `2.0.0_SA_COO~Y2`, for co-drafting with `2.0.0_SA_COO~P2` and the halves of `1.0.0_SA_CTO~DELL2` (msgs 925,
944: ONE pair for both halves). It is a DRAFT: no half is signed here, and nothing deploys from it.

## What moves

| half | change | merged |
|---|---|---|
| Y | `intake/uploads.py`: an internal OPAL_GLOBAL filer (home opal-capital) whose `allowedFirmIds` names the owner firm may create an upload for that firm. The record gains `acting_principal_id`. | IB-yr-631 @b7dc881c10 |
| P | `_scope/interactive_access.py`: `current()` carries `allowedFirmIds` for an OPAL_GLOBAL subject. `authorize_current` admits on-behalf only where the uploads rule does. "ALL" never admits. | IB-pr-354 @c101699a71 |

## The route and the principal classes it changes

**Route:** the Analysis upload creation path, the POST that reaches `intake/uploads.py` `create`, served by
`irpt-ycharts-generate`.

| principal class | before | after |
|---|---|---|
| OPAL_GLOBAL, home opal-capital, `allowedFirmIds` lists the owner firm | refused (UPLOAD_CREATOR_MUST_BE_CURRENT_ACTOR / UPLOAD_ACTOR_ATTRIBUTION) | **ADMITTED**; the record names the actor and the owner firm |
| OPAL_GLOBAL, the firm not listed, or `allowedFirmIds` = "ALL" or absent | refused | refused (same code) |
| non-internal principal, another firm | refused | refused (same code) |
| any principal, owner firm opal-capital or global | refused (INPUT_ACCESS_DENIED) | refused (same code) |
| a principal filing for its own firm (the ordinary case) | admitted | admitted, unchanged |

That is exactly one class widened. Who holds an `allowedFirmIds` naming a firm is Andrew's entitlement to grant (msg 944). Until
he grants one, the after-read uses a test filer whose firms are listed explicitly.

## Functions that move: 4 (every function packaging either file, per `lambda-source-map.json` at HEAD)

| function | packages | live CodeSha256 (read 2026-10-07 ~19:3xZ) = rollback | expected behaviour change |
|---|---|---|---|
| `irpt-ycharts-generate` | uploads.py + interactive_access.py | `uFTONal/RhfoETes4rqJ4xRjJV4d2/nv3OlwuR9AXCQ=` | the one admit above |
| `irpt-status` | interactive_access.py | `jhGc2J4Q5EesJgnLq8EzdE5ErrZLbyqnJ8m00R7CgdE=` | none: it reads history; `current()` gains a field, and no admit path reads it |
| `irpt-export-render` | interactive_access.py | `aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=` | none (as for irpt-status) |
| `irpt-performance-adapter` | interactive_access.py | `NU6YVERLJ0i6qmazBYWUF+1xVDPGHwdMKqQ5vgjmVc4=` | none (as for irpt-status) |

**MEASURED by `2.0.0_SA_COO~P2` (msg 1021, `release-census` at HEAD f4307c366d):** `interactive_access.py` is NOT a changed
member of `irpt-status` (4 changed: canonical_profile_reads, loaders, maintained_sources, served), `irpt-export-render` (1:
submit_async, IB-pr-352) or `irpt-performance-adapter` (2: holdings_gold, loaders). Their `staged_from` pins hold the older
blob, so IB-pr-354 reaches none of them. **The pair therefore moves ONE function, `irpt-ycharts-generate`.** The three rows
above stay as no-change controls, and their other changed members belong to their own releases, not this pair.
`irpt-ycharts-generate`'s pin is set by `~P2`'s IB-pr-358 (upload-door reader wiring, slot ~166). Its census is owed when
that order drains.

**To settle before signing:**
1. `irpt-export-render`'s map row reads `exDoi/uo5eB9...`, but live reads `aRCgH9B0...` (IB-pr-349, 14:38Z today). The map row
   is stale. That is `~P2`'s record to fix. The rollback above uses the LIVE value.
2. The three "none" rows are an expectation, not a measurement. The P half names the equality read that proves it: one
   authorized call per function, before and after, with identical answers.
3. The next `irpt-ycharts-generate` build also carries riders already on CLOUD: E-Y4 (`files[]` drops the 14
   `fixtures/har/*`, @d96da06035) and the 390 s `recipe.py` comment (@5d3eed8904). The resident-side 390 s change
   (`resident_worker.py`) ships on `~G2`'s resident build, not this Lambda. Each rider either rides this pair with its own
   legs (E-Y4: 0 fixtures in the deployed zip; trace control) or is pinned out. A census of the build against live
   (`infra/aws/lambda/ci/release-census.py irpt-ycharts-generate --pin <pin>`) must list every changed member, each
   assigned to a half.

## After-reads (each branch named)

1. **Admit:** a test OPAL_GLOBAL filer whose `allowedFirmIds` explicitly lists one partner firm creates an upload for that
   firm. The stored record shows `acting_principal_id` = the filer and `owner.firm_id` = the firm.
2. **Refuse (a):** the same filer, for a firm NOT on its list, is refused with its existing code.
3. **Refuse (b):** an ordinary advisor filing for another firm is refused, as before.
4. **Refuse (c):** any filer naming owner opal-capital is refused, as before.
5. **No change elsewhere:** one authorized call each to `irpt-status`, `irpt-export-render` and `irpt-performance-adapter`
   answers the same as before.

A failure of 2-5 rolls back every moved function to the hash above, in the same session.
