# PROMOTE RECEIPT -- AMGT_RESAPP.TO-AMGT-bk-7 (0.4.0_DT_ClientPlatform, 2026-10-14)

## Release

- Release branch: `release/20261014T003210Z` (builder `RELEASE result=READY`, `first_parent_commits=1 unapproved=0`), one feature: `cand/dell1/amgt-sa-header-money-and-dash-reasons` @ `624e2533f6`, approval row `dell1-20261014T001511Z-633a`, class opal-internal.
- Builder lines: `PROMOTE-LIST branch=cand/dell1/amgt-sa-header-money-and-dash-reasons class=opal-internal by=1.0.0_SA_CTO~DELL1 ... pages=Security Analysis`; `PROMOTE-CLIENT-FACING count=0`.
- PROD head before: `10e7664d6c4824cb88f04acf47f06264345b5b8b`. PROD head after: `7d5cb34daabce225bb9a2635c541f6ff3fd64e52` (fast-forward, parity diff 0 lines, `bun run typecheck` rc=0).
- Push state: on origin @7d5cb34daabce225bb9a2635c541f6ff3fd64e52 (`git ls-remote origin PROD` read after the push and again after teardown).
- Tag: `portal-v2.1.215` (tag object `a10d1ec8`, peeled `7d5cb34d`).
- Main portal tree: back on DEV (verified). The main tree carried three uncommitted files that are not this seat's (`src/lib/firmAccess.ts`, two `*.generated.ts`); untouched, and not an input to the promote, which ran in an ephemeral worktree cut from PROD.

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

## CI

- Workflow `Deploy to Production`, run `38491072873`, headSha `7d5cb34daabce225bb9a2635c541f6ff3fd64e52`: status `completed`, conclusion `success`, as read by `gh run view --json` and `gh run list --branch PROD --limit 1`. It is the only workflow run on that sha (listed by `--commit`).
- CI status read: completed.
- CI conclusion read: success.
- Route promoted: /security-analysis (class Opal-internal; no client-facing page in the release).
- Ledger entry `org/critical_paths/change_management/20261014T0033Z_amgt-bk-7-header-promote-20261014_deploy_completion.md`: CLOSED, three legs proven.
