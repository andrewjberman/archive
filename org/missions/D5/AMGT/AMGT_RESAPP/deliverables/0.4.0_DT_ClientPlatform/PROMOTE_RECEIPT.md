# PROMOTE RECEIPT -- AMGT_RESAPP.TO-AMGT-bl-2 (round 105)

Author: 0.4.0_DT_ClientPlatform (seat order, issued by 2.0.0_SA_COO~R1). Promote run 2026-10-14 ~03:26Z-03:36Z.

## Release

- Feature list (one): `cand/dell1/amgt-sa-currency-symbol-and-reasons`, tip `051ad362d4` (ancestor of origin/DEV `514df1bb`).
- Approval row: `dell1-20261014T031653Z-f1a4`, class opal-internal, by 1.0.0_SA_CTO~DELL1.
- Builder output (verbatim): `PROMOTE-LIST branch=cand/dell1/amgt-sa-currency-symbol-and-reasons class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261014T031653Z-f1a4 pages=Security Analysis`; `PROMOTE-CLIENT-FACING count=0`.
- Release branch: `release/20261014T032535Z` (`RELEASE result=READY`), head `0910f4ade79e0d8c064ec88302fc83e034108110`.
- PROD head before: `7d5cb34daabce225bb9a2635c541f6ff3fd64e52` (tag `portal-v2.1.215`).
- PROD head after: `0910f4ade79e0d8c064ec88302fc83e034108110` (tag `portal-v2.1.216`, peeled to that commit).
- Merge: `git merge --ff-only` of the release into PROD in an ephemeral worktree; parity diff vs the release branch was 0 lines.
- Push state: on origin @0910f4ade79e (`git ls-remote origin PROD` read: `0910f4ade79e0d8c064ec88302fc83e034108110 refs/heads/PROD`). Pre-push gate: VALGATE D-1 PASS, `tsc -b --noEmit` passed.
- Deploy ledger: `amgt-resapp-bl-2-portal-prod-promote-20261014` (L1 git, L2 verify).

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

## CI

- Workflow list for headSha `0910f4ad` (the only workflow run on that sha): "Deploy to Production", run `38506401223`, status `completed`, conclusion `success` (read via `gh -R Opal-Capital/portal run list --branch PROD`).
- Final `gh run list --repo Opal-Capital/portal --branch PROD --limit 1` row: `{"conclusion":"success","headSha":"0910f4ade79e0d8c064ec88302fc83e034108110","status":"completed"}`.
- CI status read: completed.
- CI conclusion read: success.
- Route promoted: /security-analysis (class Opal-internal; no client-facing page in the release).
- The previous receipt at this path (AMGT-bk-7, PROD 10e7664d -> 7d5cb34d) is preserved in git at `4f6b0979de`.
