# REHEARSAL RECORD -- DSGN_RBNDV2 cell RV-z-1 (serial 0.9.0_WK_DSGN_RBNDV2~22)

LOCAL rehearsal of the candidate branch cand/laptop/dsgn-rbndv2-light cut from the last PROD. Nothing pushed.

PROD-TIP 33ad65eef369face7ec7a9aa825ba7fb23f0fa28
FORK ad7c100b5cca9020f18a2957112361f4b9083272
COMMITS-REPLAYED 39 SKIPPED 0
CONFLICTS 0
TSC-BEFORE 0 TSC-AFTER 0
TESTS 27 pass 0 fail
ESLINT rc=0
CANDIDATE-TIP c8181090cab81e600a7f50c90e5d90adcecbfa5e
PUSHED NOTHING; remote candidate branch absent (git ls-remote --heads origin cand/laptop/dsgn-rbndv2-light printed nothing)

## Notes

- Replay: `git rev-list --reverse --no-merges ad7c100b..feature/dsgn-rbndv2-light` returned 39 commits, not the about-45 the order states. The 39 applied in order with `git cherry-pick -x`; none was empty, none conflicted. Candidate commits over PROD: 39, merges: 0.
- Conflicts: none. There are no conflict bullets to resolve.
- TSC-BEFORE is the PROD baseline (`TSC-BASELINE.txt`, 0 lines, rc=0). TSC-AFTER is the candidate (`TSC-CANDIDATE.txt`, 0 lines, rc=0). Lines present only after: none.
- Tests: `bun test src/__tests__/dsgn-rbndv2` on the candidate, 27 pass, 0 fail (`TESTS-CANDIDATE.txt`).
- ESLint: `bun x eslint src/__tests__/dsgn-rbndv2` rc=0 (`ESLINT-CANDIDATE.txt`); its one output line is a dependency age notice.
- Baseline scratch: the PROD scratch worktree was unregistered by `git worktree remove --force`, but its directory remains because a recursive delete is held for Andrew's word. It is untracked content under `ajb_wk/rbndv2-22/prod-baseline/`. See the surprise row.
