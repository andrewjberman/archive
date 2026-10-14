# PROMOTE RECEIPT -- AMGT_RESAPP.TO-AMGT-bm-4 (round 106)

Executor: 0.4.0_DT_ClientPlatform~R1. Issuer: 2.0.0_SA_COO~R1. Read 2026-10-14 ~12:4xZ.

## Release

- Feature (the only one): `cand/dell1/amgt-sa-pe-basis-and-reasons`, approved head `84fd6461bb`, row `dell1-20261014T111220Z-faa4`, approver `1.0.0_SA_CTO~DELL1`, class Opal-internal. Candidate confirmed an ancestor of origin/DEV `97c66c9364` before the build (`IN-DEV`).
- Release branch: `release/20261014T123810Z`, built by `.tools/portal-release-build.sh --features cand/dell1/amgt-sa-pe-basis-and-reasons`. Result line: `RELEASE result=READY ... base=501e998b... head=6a5926fc1194...`; `RELEASE-CHECK features=1 first_parent_commits=1 unapproved=0`; `PROMOTE-CLIENT-FACING count=0`.
- PROD head before: `501e998b1e576252ba493bd5427e14fba748dcef`. PROD head after: `6a5926fc1194e1ce37e35ff267e5cf4914d9c172`.
- DEVIATION FROM THE ORDER'S TEXT: the order names `7db035e4` as the PROD head before. origin/PROD had moved to `501e998b` by the time of the build (dell2 release `release/20261014T122041Z`, run 38563449756, success, tag portal-v2.1.218, which merged IRPT_ANLREQ feature branches). This release was cut from the live PROD head, so it carries that release underneath and adds only this feature on top. `7db035e4` is an ancestor.
- Parity gate: `git diff release/20261014T123810Z HEAD` was empty after `git merge --ff-only`. `bun run` typecheck ran in the PROD pre-push hook: `OK: typecheck passed`.
- Push state: on origin @6a5926fc1194e1ce37e35ff267e5cf4914d9c172 (ls-remote read `refs/heads/PROD`, re-read after the CI run). Tag `portal-v2.1.219` peels to `6a5926fc`.
- Ephemeral worktree removed and pruned; main portal tree reads `DEV`. The main tree holds three modified files not authored by this seat (`src/lib/firmAccess.ts`, two `*.generated.ts`) and is behind origin/DEV; the release did not read the DEV working tree and none of it shipped.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

Five files, all under `src/pages/SecurityAnalysis/` (`tabs/ModelTab.tsx`, `types.ts`, three under `__harness__/`). No client-facing page.

## CI

- Workflow `Deploy to Production`, run `38565663189`, headSha `6a5926fc1194e1ce37e35ff267e5cf4914d9c172`: status completed, conclusion success (read from `gh run view`, and `gh run list --repo Opal-Capital/portal --branch PROD --limit 1` returns the same row).
- Runs listed for that headSha: one (`Deploy to Production`). The earlier run on `501e998b` (38563449756) also concluded success.
- Ledger: `org/critical_paths/change_management/20261014T1238Z_amgt-bm4-pe-basis-prod-promote-20261014_deploy_completion.md`, three legs proven, CLOSED.
