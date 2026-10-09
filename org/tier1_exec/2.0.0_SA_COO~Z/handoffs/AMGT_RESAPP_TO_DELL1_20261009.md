# AMGT_RESAPP -- handoff from site Z (`2.0.0_SA_COO~Z`) to the DELL1 COO seat

Written 2026-10-09 ~01:2xZ by `2.0.0_SA_COO~Z`. The move is Andrew-direct ~22:5xZ 2026-10-08 (CTO msg 32099, record
@b7361ceb2a). This seat does not change `project.json`'s fabric: the CTO writes that carrier last.

## Where the project stands

- **Round 79 is closed at L8/L9.** 8 of 8 orders are terminal. The L8 packet is
  `deliverables/2.0.0_SA_COO~Z/round79/DRAIN_END_PACKET.md` @e4beab42f3. The CVO's slug @5d75eaf8fd grades cc-8 AC3 PASS,
  graduates 1 row (Z-W314-S1, INERT, the walker/port class) and dismisses 7.
- **L10 is the CTO's.** No round-79 analysis existed at 01:16Z. The next round is cut on DELL1 from that analysis.
- **The live function** `opal-amgt-scoped-api` (us-east-1) reads CodeSha256 `ltXvElwZ4iyRx6bJLDQRWksbDoiTesc8xvu1h+p3QI0=`.
  It was applied 2026-10-08T17:35:08Z at the build pin `63f0605039`. The /freshness snapshot is VersionId `ar7KPWgP...`,
  written 18:08Z.

## The build's duty (the next redeploy)

- The previous round's package is `C:/tmp/cc7-r79-63f0605039.zip` on site Z, 42,015,430 B. Its sha256 is
  `96d5ef125c19e22c91c7a6c92c34115a4b1b0e88937ac73cc6fbb587ea77408d` (base64 `ltXvElw...QI0=`), measured 2026-10-09 equal to
  the live CodeSha256. **DELL1 does not need the file:** `aws lambda get-function --function-name opal-amgt-scoped-api`
  returns the same bytes at `Code.Location`. Check the hash after download.
- The wheel folder of round 78 (`C:/tmp/bb18-wheels`, hashes in `round78/BB18_WHEEL_FOLDER_SHA256_20261008.txt`) is
  also a site-Z path. The hashes file is in the repo.
- Site-Z apply orders now go to `0.7.0_AE_CloudOps~Z` (MSTR~Z msg 32060). A DELL1 apply goes to DELL1's own applier.

## Carried items (cited, not cut)

1. **The page side of round 79** belongs to DSGN_AMGTV1: SAUX-41 (three Seeking Alpha states with sentences) and
   SAUX-42 (five sections). The AMD segment table is served and not drawn. FWD-7 is graded after that cell lands.
2. **ABNB's model-block Bloomberg pull.** It is queued as a call on the site-Z box list (2026-10-09 ~01:1xZ, CROSS-BOX)
   and needs its own pair and Andrew's per-use word.
3. **Z-S369's ICT identity read** (one key or two). It is queued as a call too; the recommendation folds it into the
   ABNB pair. Z-S377 holds the row unresolved.
4. **The walker/port contention** (Z-W314-S1 graduated). On DELL1 the walk runs on DELL1's own walker and port. The
   site-Z class does not follow the project, so read whether DELL1 has the same single-account shape.
5. **Bloomberg-side calls run on the terminal machine (site Z).** A DELL1 round that needs a Bloomberg read routes it
   to site Z's terminal seat; the BBG-dependency census of the move order decides how.

## What stays on site Z

- 15 drained worker branches, `wk-AMGT_RESAPP-300` to `-314`. All are ancestors of box/sitez, so they reach origin with
  it. Round 79's six worktrees (`C:/tmp/r79-308` to `-313`) were REMOVED 2026-10-09 ~01:3xZ under Andrew's ruling on
  call `sitez-20261008T165920Z-ce4b` ("Force-removing merged worktrees is mandatory, if that is already merged it should
  be gotten rid of"). Each was measured first: merged into HEAD, with 0 dirty tracked files. The scratch folders
  `C:/tmp/r79-faces`, `r79-half-backup` and `r79-half-scratch` are not worktrees and stay.
- **Correction:** this file's first version said the worktrees needed a word for rounds after 78. That was wrong:
  the ruling above was already on the site-Z call list.
- The ledger `mdpf-sechist-sh-t1-sitez-etf-daily-pull-20261007` (MDPF_SECHIST, not this project) is HELD to the
  2026-10-09 11:00Z pull @8be1b0639b.
