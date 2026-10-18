# AMGT_RESAPP round 114 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-18 ~01:5xZ; every order cut in round 114 is terminal (`bu-1`, `bu-2`, `bu-3`, `bu-4`, `bu-5`, `bu-7` complete).** Round 114 is the CTO's round-113 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round113.R1.md`, msg 7763), issued at `fce34ac73c` under this seat's keys (decomposition s.123). `python .tools/round-close-check.py --project AMGT_RESAPP --round 114` reads `judgment=0 ... verdict=MAY-CLOSE` once `bu-3`'s proof instance carries the corrected AC2 row (see section 1): the round carries NO judgment criterion, so no L9 grade is owed; the packet is the L8 compile and the ground for your L10 slug. Commits named are LOCAL on `box/dell1` unless a read says otherwise; push state is not measured here.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bu-1` | the Peers subject row's money cells read their currency code through the trimming helper (closes W497-S2 via W502-S1) | complete | worker ~504 (merged bd4f1bcd5b); candidate `cand/dell1/amgt-sa-peers-subject-currency` @a3f2b727; fresh-checkout re-run `PRICE CURRENCY RULE HARNESS YES (8 of 8)`, `PEERS CURRENCY HARNESS YES (6 of 6)`, typecheck and eslint rc 0; row 55a2 |
| `AMGT-bu-2` | the page's date sites: a census (102 sites, 30 bypass), 26 fixed, the scalar next-earnings row in the long form | complete | worker ~505 (merged ab326c03b7); candidate `cand/dell1/amgt-sa-page-dates-long-form` @9a8ef5e451, 21 files; fresh re-run `DATE RULE HARNESS YES (7 of 7)` and the three older What Changed harnesses green; row 5b5e. The 26 reason-text wraps are graded by review. Four bypasses are DEFERRED to `ModelTab.tsx` and `PeersTab.tsx` (rows W505-S1, S2) |
| `AMGT-bu-3` | the printed pack's dates through `long_day` (a census of 58 functions, 9 pack-path sites) | complete | worker ~506 (merged 0100aab018); 7 new tests; the six existing tests that pinned printed ISO text updated and named. **AC2 was FAIL in the worker's sparse worktree (18 failed: nine more read `infra/` and `integrations/` which the cone lacks, row W506-S1) and PASS in the full shared tree: exactly the nine named failures and 1155 passed**; the instance's AC2 row is corrected by the worker slot's own commit |
| `AMGT-bu-4` | the All figures grid shows that it scrolls sideways: a cue line and a visible thumb | complete | worker ~507, re-seated once after the issuer's AMENDMENT 1 (the sibling harness's B5 digest re-recorded; the thumb declarations take the trailing bang because Tailwind v4 utilities are layered and `src/index.css`'s scrollbar rules are not); candidate `cand/dell1/amgt-sa-model-grid-scroll-cue` @dac528b0; fresh re-run `GRID SCROLL CUE HARNESS YES (5 of 5)`, `MODEL TOOLTIP ROWS YES (9 of 9)`; row c1c6 |
| `AMGT-bu-5` | the landing: one chosen-set promote and the fold-back | complete | H2: PROD `d1bed0fb` to `26d998f7` (CI run 39080069302 success, tag `portal-v2.1.239`); fold-back under the CTO's one-time named waiver (@4ca08dbaae, row 22a3): DEV `2612bd72`, its tree equal to the pre-fold DEV's, `origin/DEV..origin/PROD` = 0 (issuer's fetch read) |
| `AMGT-bu-7` | the live printed pack prints every date in the long form | complete | `0.7.0_AE_CloudOps~SC1` applied from release pin `6bb7b23ee5` (CodeSha256 `hLW4fD..` to `RY998VO4..`, one member changed, ledger closed 9 of 9, rollback target the `bp-6` artifact); **the issuer's own second read: a fresh capture of the same eight live packs compared with the issuer's own earlier BEFORE set, `PACK COMPARE YES (8 of 8)`** |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` |

`W503-S1` (the short-grid tooltip) was NOT cut: the CTO ruled it latent (msg 7777) and set the read that closed it: ICICIBC IN, the name with the fewest figure mnemonics, rendered 113 table rows in the All figures fold (20 or more closes it NOT A DEFECT).

## 2. The issuer's real runs

- **Real-browser walk of the three portal candidates integrated** (`round114/CLOSE_WALK_INTEGRATED.md`): RIO LN, ICT PM, ICICIBC IN; not void; 10 findings against 11 at PROD `d1bed0fb`; **`format:dates` ABSENT** (it was 1, ICT PM's scalar next-earnings row); `occluded-popover` absent; `layout:clipped` the same two (ruled by design); the cue line reads under All figures.
- **Live site tied to PROD `26d998f7` by bytes** (`round114/LIVE_TIE_26D998F7.md`): `index.html`, six entry assets and the Security Analysis chunk `index-Bi-xI0II.js` equal the CI artifact; the marker `data-grid-scroll-cue` is in 1 chunk of the new artifact and 0 of the previous.
- **The scrollbar thumb on the running page** (`CLOSE_WALK_INTEGRATED.md` section 4): on a local build of the PROD head the grid scroller's computed thumb colour is `rgba(22, 51, 114, 0.35)` (the navy token), not transparent, with `scrollWidth` 1494 over `clientWidth` 1266. A computed-style read: headless Chromium paints no scrollbar.
- **The live printed packs** (`bu-7`): eight names (RIO LN, ICT PM, GOOGL US, ICICIBC IN, HD US, BA US, KMB US, TSM US) captured before and after; before 51, 51, 51, 30, 51, 50, 51, 33 ISO days, after 0, the same numbers of long-form days, and the text otherwise equal. Three of the eight (BA, HD, KMB) print quoted source passages; none carried an ISO day, so none was altered.

## 3. Findings for your judgment (read, none graded by the issuer)

1. **A latent rewrite:** the printed pack's wrap guard rewrites an ISO day inside ANY printed line, including a quoted source passage. The CTO ruled served prose in scope and verbatim quotations exempt (msg 7780): `W506-S5` becomes a round-115 cell with a census of verbatim-quote blocks first.
2. **The `format=rich` export still prints ISO days** (row W506-S4; the CTO's item named the page and the printed pack).
3. **Four date bypasses deferred** to `ModelTab.tsx` and `PeersTab.tsx` (rows W505-S1 and S2): the walk of three names did not show them.
4. **The pack's fixtures are hand-built** (no committed RIO LN or ICT PM block): the live comparison above is the real grade.
5. The 26 reason-text `daysInWords` wraps in the page are graded by review, not by a harness (`bu-2`).
6. **Process findings:** the worker's sparse worktree cannot meet an AC that runs the whole api test folder (row W506-S1: the order should carry `--full`, or the issuer re-grades in the full tree, as here); a CloudOps seat idle at its prompt for three hours held unread mail until a screen nudge (`/unstick`); two harness-passing sibling controls moved with an intended text change (the B5 digest).

7. **The worker rows of round 114 for your disposition** (15 rows `AMGT_RESAPP-D1-W504-S1..S3`, `W505-S1..S4`, `W506-S1..S5`, `W507-S1..S3` in `surprise-channel/investigations/INVESTIGATION_v1.md`; all `UNDER_INVESTIGATION`, three ARMED with this seat as `disarm_owner`). Resolved inside the round by the issuer: `W507-S1` (the thumb cascade: AMENDMENT 1, then the running-page read) and `W507-S2` (the B5 digest: AMENDMENT 1) and `W506-S1` (the sparse-tree AC2: re-graded in the full tree). Carried: `W504-S1` (the commit gate grades 0 files on a ts, tsx or cjs commit: an instrument gap, the gate owner's), `W505-S1` and `S2` (the four deferred date bypasses), `W506-S4` (rich export ISO), `W506-S5` (round 115). The rest are observations (`W504-S2` and `S3`, `W505-S3` and `S4`, `W506-S2` and `S3`, `W507-S3`). The file carries no disarm convention for this flat row shape (233 rows in it read ARMED), so the issuer edited none.

**Not verified by the issuer:** the live page opened with a staff login; a painted thumb on a person's screen; content markers for `bu-1` and `bu-2` in the served chunk (minified, no unique string); names other than the three walked and the eight packs; every What Changed pair.

## 4. Open and carried

- Round 115 (the CTO's analysis, after your slug): `W506-S5`'s census of verbatim-quote blocks; whether to take the four deferred date bypasses and the `format=rich` ISO days; the residual rows above.
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew); row `S57` (the fold-back verb) is the portal manager's, and every fold-back waits on a named waiver until it exists.
