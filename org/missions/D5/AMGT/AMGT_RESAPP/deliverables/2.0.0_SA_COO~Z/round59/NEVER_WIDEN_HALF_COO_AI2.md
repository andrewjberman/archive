# AMGT_RESAPP round 59 -- `AMGT-ai-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-01 ~11:5xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names, which is the round-59 issuance tip or a
descendant whose CONTENT-DIFF equals the list below. Parts: build + upload ONE artifact; ONE code-only `safe-apply`.
Executor `0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-ai-2.the-price-identity-redeploy.md`; decomposition s.67.
DEMO-BLOCKING (CTO round-58 analysis ruling 1).

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `g9H0TW2garLGS0zMoLmJgFQU8a/6ZJUGMwJaYFSkc/c=` |
| function LastModified | `2026-10-01T09:48:26.000+0000` (ah-2) |
| artifact S3 VersionId | `hj5ITKr5Ct9Mn3ySEvztrK9eG.bnsHho` (LastModified 2026-10-01T09:42:12Z, 41,115,765 B) |

## WRITERS OF THE PROPERTY: 2 seats, 1 path

`build-and-upload-scoped-amgt.sh` + a code-only `safe-apply`; AMGT_RESAPP (this act) and AMGT_HARVST (no redeploy in flight).

## THE FILE LIST (`--build-only` at the cut, rc=0 incl. the isolated-runtime arm)

`CONTENT-DIFF SUMMARY: files 350, IDENTICAL 349, CHANGED 1, ADDED 0, REMOVED 0` against `g9H0TW2g...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | ai-1 | the ranking routes (`lead-panel/rankings/*`) key an unkeyed row by an exact ticker match against the covered universe (`identity_basis: covered_universe_bloomberg_join`, `identity_status` MEASURED); the crosswalk filler names newly keyed rows; every row gains `display_name` (and `display_name_source` when it is not the row's own `name`) |

Any other changed file at build time is a STOP.

## READERS

The Lead Panel's price bars and their click-through into the per-name overlay (`security_key`), on portal DEV and PROD. The chatter
rankings pass through the same function, and their rows are already keyed, so they gain only `display_name`.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of the artifact key (versioned) | the prior VersionId above |
| code-only `safe-apply` | the function's code (source hash) only | a code-only `safe-apply` with `hj5ITKr5Ct9Mn3ySEvztrK9eG.bnsHho`, restoring `g9H0TW2g...` |

## EXPECTED OUTCOME -- both branches, read from the code's own rule

- **The listing is readable (expected):** 62 of 94 rows per price axis gain a covered `security_key`; 0 rows stay unkeyed;
  `display_name` on 94 of 94; company `name` on 70 of 94 (measured locally); scores, ranks and units are unchanged.
- **The listing fails at serve time:** rows stay as served (the join's fail-safe), and C2 FAILS. That is the rollback trigger, and
  nothing is guessed.
- **Already-keyed rows:** unchanged except for `display_name`.
- **AC1 or AC2 fails after the act -> ROLLBACK** per the table.

## WHAT THIS HALF DOES NOT COVER

No producer change, no rewrite of the 09-30 generation, no store write, no S3 delete, no vendor call. No IAM, route or gateway change:
any of these in the plan is a STOP.
