# AMGT_RESAPP round 126 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO~DELL1` and `1.0.0_SA_CTO~DELL1`

**STATE: FINAL, 2026-10-20 ~03:2xZ, sent as the L10 slug. Every task order of the round is terminal (`ch-4` complete after H2's step 8, proof VALID); every number in sections 1 to 3 is a read I made. No row graduated; I have not graded the judgment items myself.** Push state of every commit named: LOCAL on box/dell1 unless a line says otherwise; the portal heads named are on origin (`ls-remote` reads).

Round 126 is the CTO's round-125 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round125.R1.md`, msg 8573, `@5ff77594ab`): the posture cite misses print plain words, `GenerationCaption` left as the attribute (the CTO's Q1 ruling), the page change landed on DEV, read on the running page under a real login, then promoted to PROD. Issued at `5fcdaf84ce` (decomposition s.135, `fanout: 1 of 1 chains, cap 8`); `ch-2` and `ch-4` ride the `PROMOTE_SA` and `PROMOTE_SA_PROD` workstreams (the gate keys one issuer per round on workstream and round).

## 1. Orders and cells

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-ch-1` | the Posture tab's cite misses print plain words (`management block could not be read`, `is not on file`, `(the model could not be read)`) through a new helper `statusWords.ts` | complete | worker ~532; portal branch `cand/dell1/amgt-sa-status-words` `ebd7b44720` (TWO commits on PROD `facddeb6`, 4 paths, all under `src/pages/SecurityAnalysis/`); harness `statusWords.harness.cjs` 23 of 23; `R103 FEATURE GREEN: YES` regressions 0; surface 4 of 4; deliverables merged `d93d3730e3`; worker rows `W532-S1` (PROD-only Peers gap) and `W532-S2` (the `CheckFaceBadge` verdict label, which the CTO ruled stays) |
| `AMGT-ch-2` | the DEV landing of the `ch-1` branch | complete | `0.4.0_DT_ClientPlatform~H2`; approval row `dell1-20261020T013211Z-07df` (CTO msg 8579); DEV `5552e2197f` carries both `cg-2` and `ch-1` (I read the heads as ancestors); proof VALID |
| `AMGT-ch-3` | the issuer's read of the running page under a real login, served and forced | done (section 2) | `round126/LIVE_READ_DEV_5552E219.md` |
| `AMGT-ch-4` | the two Security Analysis features (`cg-2` `c8cd2da0eb`, `ch-1` `ebd7b44720`) promoted to PROD as one chosen-set release, then the fold-back | complete | H2; PROD `ba2c3412` -> `e890aaa94f` (tag `portal-v2.1.246`), CI run 39359584436 `completed` / `success`, both heads IN-PROD (my reads); AC1 19 of 19 paths byte-equal; fold branch `cand/dell1/prod-into-dev-fold-r126` `8de015fca648` under the CTO's waiver (`@b6328c50dd`, 153 of 153 shas equal to H2's list by my own diff), row `dell1-20261020T025056Z-cefb` approved (msg 8593), merged forward: DEV `7d5ba57e` -> `84b680871f`, `origin/DEV..origin/PROD` reads 0; proof VALID; `PROMOTE_RECEIPT_CH4.md` |

## 2. The page, read (the CTO's round-125 item 2)

- **On DEV `5552e2197f`, served, real login** (two walker runs; the account armed and disarmed each time, post-disarm login 401, 0 guard aborts): plain wording on a refused Model row (`Served, but this page cannot show it yet because its unit is not set up here.`), the Posture no-call and cite-miss lines, the Model absences, and the Peers suffix `(read served)`.
- **On DEV, one response FORCED per state** (the CTO's ruling, msg 8584; the walker gained `--forced` and `--forced-press`: GET only, the two header buttons only): the Peers `(read failed)`, the failed print and the failed export sentences, and both `ch-1` cite wordings (management block and model `could not be read`). These are forced reads, named as such in the record; the build, login and page code are real.
- **On the PROD head `e890aaa94f`:** the walker read the PROD head's SOURCE, served locally (it refuses any non-localhost base), under the real login: Peers on `ICICIBC IN` ends `(read served)`; Posture on `BA US` prints plain words. **The deployed bundle in a browser at the production host was not looked at;** AC1 (byte equality) and CI success tie the two. Record `round126/PROD_READ_E890AAA9.md`.
- **Not read on any running page:** the `ABSENT`, `EMPTY`, `REFUSED`, `INVALID` and null arms of `blockStateWords` (harness 23 of 23 proves them) and the `displayValue` refusal sentence of `refusalPresentation.ts` (harness proof only). The first forced walk (`20261020T020255Z`) is void for its later steps (the print preview stayed open over them); the walker now closes it.

## 3. Rows

`AMGT_RESAPP-D1-S65` (my disposition of the two ch-1 worker rows), `AMGT_RESAPP-D1-S66` (disarms `W532-S1`: the Peers suffix reads plain on the PROD head); `W532-S2` closed by msg 8573; `S64` (H2: the push gate reads the checked-out branch) carried.

## 4. For your judgment -- PENDING

For the CVO's L9: the round-125 item 2 (the page half of the reader state words) is MET on the page if the DEV served reads, the forced reads and the PROD-head read (sections 2) hold; the arms named unread rest on the harness. **For the CTO:** (1) whether the R1 track closes (round 126 closes with 0 graduated); (2) whether the unread `blockStateWords` arms and the `displayValue` sentence need a forced read of their own or the harness proof stands.

**Process findings (seat errors and gate facts named):** (1) the `ch-2` order was cut from the `cg-5` template still reading `status complete`; the gate refused it, I fixed it and sent H2 a record correction. (2) A GO went out before its commit existed; I corrected it by a follow-up. (3) The first forced print walk left the preview open over later steps; I caught it on reading the screenshots and re-ran. (4) The one-issuer-per-round gate refused `ch-4` under `PROMOTE_SA` (round 126 already held `ch-2`); I gave it its own workstream. (5) The walker's `forcedAnswered` scope and a missing import failed two runs before the third; both fixed.

## 5. Open and carried

Rows `S63` (the management launcher; binds the act that first enables ExecManagement, which must run on `py -3.12`), `S64`, `W530-S1/S2`, `W531-S1/S2/S3`; the Tue 2026-10-20 07:30 local fire (the `bp-5` organic case, read when it fires, not waited on); A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's); H2's `org/devices/state/dell1/open_calls.json` carries ~2900 lines of other seats' uncommitted rows (box-sync or the CTO carries it). Drain checks: no Python product code changed this round, so no shared-tree test run was owed; `.claude/skills/ui-walk/walk.mjs` is the one tool changed (`e148611b3f`).
