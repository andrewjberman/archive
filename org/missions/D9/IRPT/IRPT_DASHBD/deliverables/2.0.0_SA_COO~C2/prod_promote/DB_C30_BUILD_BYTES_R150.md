# DB-c-30 (the contract 0.3.3 page mirror, stacked on the 0.3.1 mirror): the built-bytes measurement -- 2.0.0_SA_COO~C2, 2026-10-16 ~12:0xZ

Claim words: MEASURED = this seat ran it in this session. Method and ruling: the CTO's msgs 9136 and 9144 (class follows whether the built page changes, measured).

**What was built (MEASURED, `bun run build` = `tsc -b && vite build --configLoader runner`, rc 0 each, node_modules linked, no environment change):**
- **C** = `origin/PROD` `8012cd1afbaad0e537cf48b1fa5f5ddb1e549f9f` (portal-v2.1.230, the unreported-days sentence promoted).
- **B** = the candidate `cand/dell2/irpt-series-mirror-contract-033` @`831f974aa1d4b3df061af3a29337917c154eda01`: two commits on the PROD tip, `a8d5dafc` (DB-c-26, the 0.3.1 mirror: six optional names) and `831f974a` (DB-c-30, the 0.3.3 mirror: eight names). Two-dot diff `origin/PROD` to the candidate: exactly one file, `src/pages/InvestorReporting/dashboard/seriesContract.ts`, +10 and -1.

**Result (MEASURED, sha256 of every emitted file, 88 files, 63 `.js`/`.css` chunks each):** C against B: 0 chunks only on one side, 0 chunk names with different bytes, 63 of 63 JS and CSS chunks identical, and the WHOLE `dist` tree byte-identical (88 of 88). Chunk-set hash (first 16 hex) C `8890552b43cca4fe`, B `8890552b43cca4fe`. The positive control of the same method is on record: `DB_C26_BUILD_BYTES_R148.md` (origin/PROD before the promote against the 92c0 head differed in 44 chunk names, so the build is sensitive to a real page change).

**Other gates on the candidate (MEASURED, scratch tree with a copy of the trunk 0.3.3 contract):** `iv-e-124` plus the round-147 `fwd10-unreported-days` test 9 of 9 pass; `bun run typecheck` rc 0.

**Reading:** both commits are type-only and compile away; the emitted bytes of the dashboard do not change. By the CTO's rule the class is **opal-internal**. Both scratch worktrees and links were removed (non-recursive `rmdir` of each node_modules junction first, main `node_modules` verified intact; a stale link left from round 146 in `C:/dev/g-cand-fwd10` was found and removed the same way).

**Not read:** a determinism rerun of the two builds (one build each).
