# DSGN_AMGTV1 round 55 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~00:5xZ)

| item | value |
|---|---|
| list | round 54's list, re-cut on DELL1 (decomposition v55): the CTO's round-53 finding + rows Z-S25, Z-S26 |
| order | `DSGN_AMGTV1.TO-AV-zzg-1` -> `0.9.0_WK_DSGN_AMGTV1~119` (worker-light, direct act), issued @8bfd66d9f5, complete |
| drain | merged @2c40585c38 through `safe-merge.sh`; instance VALID (`proof-of-spec-check` rc=0); rows minted: 0 |
| AC1 | `round54/checks/r54.cjs`: 4 of 4 arms, exit=0 (base 1 of 4) |
| AC2 | `round53/checks/r53a.cjs`: 3 of 3 arms, exit=0 |
| AC3 | `round29/checks/battery29.sh`: ALL PASS (0 skipped), 14 of 14 harnesses |
| worker extra | `bun test src/pages/Freshness/Freshness.test.tsx`: 19 pass, 0 fail |
| round-close-check | `verdict=MAY-CLOSE` (1 of 1 orders complete, proof_ok=1, judgment=0) |
| portal candidate | `8d2a08a9` = DEV `84e13d0f` + 1 commit (3 files under `src/pages/Freshness/`, +11 -5); ref `cand/dsgn-amgtv1-r55` in the dell1 portal repo; LOCAL, not pushed |

## The one real run -- NOT DONE, blocked on dell1 IAM

The candidate's dev build ran on dell1 port 5174 (`bun run dev:live`, HTTP 200). The signed-in `/ui-walk --route /freshness` armed the
walker account (`HOLDER DESKTOP-HK1UU7N:7760:9fe888f0`), then failed at `secret`. The cause is `cloudops-dell1-agent-user`, which is not
authorized for `ssm:GetParameter` on `/opal/ui-walker/password` (AccessDeniedException). No page was looked at, and no screenshot exists.

The walker's own disarm failed at the same read. The issuer ran its remaining steps through the module's functions: the row now reads
`status=disabled`, `armedBy` removed, with an unusable bcrypt hash, so no login with any password is possible. The parameter delete was
also denied (`ssm:DeleteParameter`), so `/opal/ui-walker/password` still holds the dead password (describe count 1). The login-refused proof
needs that password and could not run on dell1. Owner of the residue and the IAM gap: `0.0.0_AB_MSTR~DELL1`.

The real run is owed when a box that can read the parameter walks `/freshness` on this candidate, or when dell1's user gets the walker's
SSM actions.
