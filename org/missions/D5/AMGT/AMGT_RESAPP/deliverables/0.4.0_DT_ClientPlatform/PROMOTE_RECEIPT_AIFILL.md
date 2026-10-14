# PROMOTE RECEIPT -- AMGT_RESAPP.TO-AMGT-ar-6 (round 104, workstream AIFILLLAND)

Author: 0.4.0_DT_ClientPlatform (seat order, issued by 2.0.0_SA_COO~R2; seating bar lifted by 1.0.0_SA_CTO~DELL1, msg 5397). Promote run 2026-10-14 ~03:46Z-03:55Z.

## Release

- Feature list (one): `cand/dell1/aifill-blocks-prod`, local ref tip `53de2b9d` (ancestor of origin/DEV), eleven files under `src/pages/SecurityAnalysis/`.
- Approval row: `dell1-20261014T022349Z-a565`, class opal-internal, by 1.0.0_SA_CTO~DELL1 (call cf85 also on record).
- Builder output (verbatim): `PROMOTE-LIST branch=cand/dell1/aifill-blocks-prod class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261014T022349Z-a565 pages=Security Analysis`; `PROMOTE-CLIENT-FACING count=0`.
- Release branch: `release/20261014T034603Z` (`RELEASE result=READY`, `first_parent_commits=1 unapproved=0`), head `7db035e448d9e6bbc202ef4264989f54d3d3dded`.
- PROD head before (read again at the start): `0910f4ade79e0d8c064ec88302fc83e034108110` (tag `portal-v2.1.216`).
- PROD head after: `7db035e448d9e6bbc202ef4264989f54d3d3dded` (tag `portal-v2.1.217`, peeled to that commit).
- Merge: `git merge --ff-only` of the release into PROD in an ephemeral worktree; parity diff vs the release branch was 0 lines.
- Push state: on origin @7db035e448d9 (`git ls-remote origin PROD` read: `7db035e448d9e6bbc202ef4264989f54d3d3dded refs/heads/PROD`). Pre-push gate: VALGATE D-1 PASS, `tsc -b --noEmit` passed. The pushed head was sent to 2.0.0_SA_COO~R2 and ~R1 before the CI wait (msgs 5399, 5400).
- Deploy ledger: `amgt-resapp-ar-6-portal-prod-promote-20261014` (L1 git, L2 verify).
- The shared main portal tree carried three uncommitted files that are not this seat's; untouched, and not an input to the promote, which ran in an ephemeral worktree cut from PROD.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

## CI

- Workflow list for headSha `7db035e4` (the only workflow run on that sha): "Deploy to Production", run `38508112643`, status `completed`, conclusion `success` (read via `gh -R Opal-Capital/portal run list --branch PROD`, polled until no run was in progress; one poll showed it `queued` mid-run, the final read is below).
- Final `gh run list --repo Opal-Capital/portal --branch PROD --limit 1` row: `{"conclusion":"success","headSha":"7db035e448d9e6bbc202ef4264989f54d3d3dded","status":"completed"}`.
- CI status read: completed.
- CI conclusion read: success.
- Route promoted: /security-analysis (class Opal-internal; no client-facing page in the release).
