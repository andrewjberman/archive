# Session log -- 0.9.0_WK_NFRA_MCPORTAL~3, MP-p-1

1. Bar check: `git rev-parse --abbrev-ref HEAD` -> `wk-NFRA_MCPORTAL-3`; `test -d org && test -d .tools` -> TREE-OK.
2. Read the task order's WORKER FACE (up to the RECORD FACE marker) only.
3. Read `mcportal/src/api/admin.ts`, `mcportal/src/pages/recent-changes/**` and the round-1 entitlements test
   (`mcportal/src/pages/mcp-server/entitlements/entitlements.test.tsx`) for the existing mocked-fetch style.
   `getRecentChanges()` already fetched `/api/admin/changes` with no parameters, and `RecentChanges`/`RecentChangesView`
   already showed who/when/what/before/after/verdict newest-first -- neither needed a change.
4. Edited `readJson` in `mcportal/src/api/admin.ts` to refuse a response whose `content-type` header is present and not
   `application/json`, before attempting `response.json()`.
5. First attempt refused whenever content-type was ABSENT too, which broke round-1's `entitlements.test.tsx` "narrow
   posts..." test (its mocked `Response` sets no content-type header) -- bound 1 says round 1's 4 tests stay green, and
   that file is outside this order's write surface (read-only). Narrowed the refusal to fire only when a content-type
   is present and is not JSON-like; verified `bun test src` back to 6 pass / 0 fail.
6. Added `mcportal/src/api/admin.test.ts` with the two named tests, following `entitlements.test.tsx`'s
   `afterEach(restore fetch)` + `mock(async ...)` pattern.
7. `bun run typecheck` (tsc -b --noEmit): rc=0.
8. Committed inside the nested repo: `git -C mcportal add src/api/admin.test.ts && git -C mcportal commit --author
   "0.9.0_WK_NFRA_MCPORTAL~3 <0.9.0_WK_NFRA_MCPORTAL~3@opal.agent>" -F <msgfile> -- src/api/admin.ts
   src/api/admin.test.ts` -> `a3bff71ffa` on `wk-NFRA_MCPORTAL-3-mcportal`.
9. Ran the literal AC1 invocation from `/c/tmp/mp-3` -> RESULT: PASS, exit=0.
10. Mutant: neutralised the refusal (`if (false && ...)`, uncommitted) -> RESULT: FAIL, exit=1 (5 pass / 1 fail).
    Restored the file from a pre-mutant backup; `git -C mcportal diff --stat` clean.
11. Determinism: ran AC1 twice post-restore -> byte-identical deciding line both times.
12. No surprise encountered (no deviation from the face); `surprises` in the proof-of-spec instance is `[]`.
13. Wrote the proof-of-spec instance and validated it with `.tools/proof-of-spec-check.py`.
