# PROMOTE RECEIPT -- MDPF_SECHIST.TO-SH-t26 -- Positioning frontier label to PROD

Author: 0.4.0_DT_ClientPlatform~H1. Order: org/missions/D8/MDPF/MDPF_SECHIST/task-orders/MDPF_SECHIST.TO-SH-t26.positioning-label-promoted-to-prod.md @aff3185498.
Deploy ledger: org/critical_paths/change_management/20261014T1852Z_sechist-positioning-label-prod-promote-dell1-20261014_deploy_completion.md (3 legs, all proven, CLOSED).

## Release

| Field | Value |
|---|---|
| Release branch | release/20261014T184507Z (built by the issuer; used as built, not rebuilt: PROD had not moved) |
| Feature | cand/dell1/sechist-frontier-label, row dell1-20261014T141244Z-c822, approved by andrew, head c77f23624d, in origin/DEV (merge-base --is-ancestor read IN-DEV) |
| PROD head before | 6a5926fc1194e1ce37e35ff267e5cf4914d9c172 (tag portal-v2.1.219) |
| PROD head after | fa10e75861abd352ab033f5c7ab4b9e1f0f297e9 (tag portal-v2.1.220, peeled with `rev-parse portal-v2.1.220^{commit}`) |
| Push state | on origin @fa10e75861abd352ab033f5c7ab4b9e1f0f297e9 (`git ls-remote origin refs/heads/PROD` read after the push; push output `6a5926fc..fa10e758  PROD -> PROD`) |
| Release check | `portal-release-build.sh --check`: features=1, first_parent_commits=1, unapproved=0, result=READY |
| Promotion | fast-forward of the release onto PROD in an ephemeral worktree; `git diff release HEAD` empty (0 bytes); 7 files changed, 392 insertions |
| Typecheck | `bun run typecheck` rc=0 on the merged tree; the PROD pre-push gate re-ran tsc and VALGATE D-1 (no-op) and passed |

## Pages changed

| page | route | class |
|---|---|---|
| Positioning | /positioning | client-facing |

Files (seven, the order's list): src/api/portal-proxy.ts, src/pages/Positioning/shared/etfAdapter.ts, src/pages/Positioning/tabs/HoldingsTab.tsx, src/pages/Positioning/tabs/ReturnsFrontier.tsx (new), and three harness files under src/pages/Positioning/__harness__/. Display-only: with neither `returns_frontier` nor `returns_frontier_holdings` served, the page renders as before.

## CI

Read with `gh -R Opal-Capital/portal run view 38619242657 --json status,conclusion` after a poll: status completed, conclusion success. Workflow "Deploy to Production", headSha fa10e75861abd352ab033f5c7ab4b9e1f0f297e9. Listed by headSha over the last 40 runs, that was the only workflow on the sha. The repo was named with `-R`; the PROD list returned the six prior Deploy to Production runs, so it is not the empty wrong-repo read.

## Not done, by the order's bounds

- Workspace submodule pointer bump (prod-deploy Step 6): not made. It writes `portal`, outside this order's `<paths>`, and the order's bound 3 limits writes to the receipt and the ledger entry. The issuer or the integrator carries the pointer.
- SH-t-24 (`etf-positioning-producer` apply) is not mine and was not started.

## Main tree

portal/ main tree on DEV (verified `branch --show-current`). Its modified files (src/lib/firmAccess.ts and two *.generated.ts) pre-date this promote, belong to other seats, and were not touched. Ephemeral worktree removed and pruned.
