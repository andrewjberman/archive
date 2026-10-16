# DB-c-26 (the contract 0.3.1 page mirror): the built-bytes measurement the CTO's ruling asks for (msg 9136) -- 2.0.0_SA_COO~C2, 2026-10-16 ~06:5xZ

Claim words: MEASURED = this seat ran it in this session.

**Question (CTO msg 9136):** does DB-c-26 change what the portal emits? If every emitted JS and CSS chunk is byte-identical, the page does not change (class opal-internal, the CTO approves); if any differs it is client-facing (Andrew approves).

**What was built (MEASURED, `bun run build` = `tsc -b && vite build --configLoader runner`, rc 0 each, node_modules linked, no environment change):**
- **A** = the approved head of row 92c0, `cand/dell2/irpt-fwd10-unreported-days-sentence` @`9c24c7bdac5775d18a66460748adbb694d2b1f98` (the round 147 sentence and the 0.3.0 mirror).
- **B** = A plus DB-c-26's portal commit `d562c6fc7e51a30f98ba68ce6716133bedadf2fb` (cherry-picked clean; the diff A to B is exactly one file, `dashboard/seriesContract.ts`, +5 and -1).
- **C** = `origin/PROD` `a062c56e53b174eab043b1e50002c93eb7a56f8b` (the positive control).

**Why A and not PROD is the base for DB-c-26:** the mirror cell is stacked on the round 147 change (the 0.3.0 mirror it extends is in A and not yet on PROD). Compared against PROD it would also carry the sentence. The isolating comparison is A against B. The claim holds for the single-commit candidate cut from PROD once 92c0 lands, because that tree is A.

**Result (MEASURED, sha256 of every emitted file, 88 files, 63 `.js`/`.css` chunks each):**
- A against B: 0 chunks only in one side, 0 chunk names with different bytes, 63 of 63 JS and CSS chunks identical, and the WHOLE `dist` tree byte-identical (88 of 88 files). Chunk-set hash (sha256 over the sorted name and hash pairs, first 16 hex) A `8890552b43cca4fe`, B `8890552b43cca4fe`.
- **Positive control, C against A:** 44 chunk names exist on one side only (content-hashed names move when content moves), 19 of 63 identical, chunk-set hash C `ff77f4297b90940d`, A `8890552b43cca4fe`. So the build is sensitive: a real page change shows.

**Reading:** the type-only mirror change (two optional type members and one more entry in a `const` list read only by the test) compiles away; the dashboard's emitted bytes do not change. By the CTO's rule the class of DB-c-26's candidate is **opal-internal**, on the CTO's approval; the row records these hashes. Until the CTO says so, the default (client-facing) stands.

**Not read:** a build of the single-commit candidate itself (it cannot be cut from PROD until the 92c0 promote lands); a rerun of A and B for determinism (one build each).
