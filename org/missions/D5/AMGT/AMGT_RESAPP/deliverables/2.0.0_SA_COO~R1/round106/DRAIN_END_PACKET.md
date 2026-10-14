# AMGT_RESAPP round 106 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: DRAFT, 2026-10-14 ~14:0xZ. Sections 1 and 2 are final for `bm-1` to `bm-4`; `bm-5` (the walk) and section 3 are filled after the walk of 2026-10-15.** Round 106 is the CTO's round-105 remediation list (`ledger/ROUND_ANALYSIS.round105.md`, msg 5426), issued at `d014b315df` under this seat's keys (`bm-1`, `bm-2`; workstreams `REDEPLOY` `bm-3`, `PROMOTE` `bm-4`, `WALK` `bm-5`).
`~R2`'s AIFILL workstream is NOT in this packet (it is compiled in its own). Do not send this packet until `bm-5` is terminal.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bm-1` | one Opal-internal portal feature: a historical P/E prints the price behind it; an All-figures grid dash states its reason (the research team's sentence only on a team row); a withheld forward P/E's dash shows the served reason | complete @6693cbbc5f | worker ~441 (three passes) merged @d1f7937d28, instance VALID; portal `84fd6461bb` (5 files under `src/pages/SecurityAnalysis/`, harness 10 of 10, feature green regressions 0); row `dell1-20261014T111220Z-faa4` CLOSED APPROVED (CTO; `f376` stayed bound to `4eb56d57d2`); rows `W441-S4`, `S5`, `S6` ruled in `D1-S30` |
| `AMGT-bm-2` | the served forward P/E whose price and EPS currencies differ is withheld, with a reason naming both codes and a `model.forecast_withheld` entry | complete @ce4df05861 | worker ~442 (two passes) merged @3818736e6b; 60 rows on 20 names withheld, 218 kept byte-equal; 15 unit tests |
| `AMGT-bm-3` | the redeploy of `opal-amgt-scoped-api` from pin `3818736e6b` (WORLD) | complete @cc01c88c1e | `0.7.0_AE_CloudOps~RA1`; CodeSha256 `0pWc69Vd..` -> `UIkRgr9gbz2RbsaOJq2uRe3aZPOgNE/YoCAG6j7HyO4=`, plan code only, the AI-fill hold, memory, timeout, role unchanged; first cold request handler 2,930 ms / Init 678 ms; pair signed (COO `6b74f4cb7a`, CTO `c65aa92726` with C1); the first AC1 read NO 5 of 7 (F2, F5) because the harvest runner refreshed the pool between capture and read, the CTO named KEEP (ADDENDUM 1 `358b460431`), AC1 amended to old-code-vs-deployed (`99237557be`) and read YES 7 of 7 twice (RA1, issuer); instance VALID `f767e1dce1` |
| `AMGT-bm-4` | the promote of that one feature to PROD (SERVED) | complete @01e28837a9 | `0.4.0_DT_ClientPlatform~R1` (a lane: the base DT held another fabric's order); PROD `501e998b` -> `6a5926fc` (portal-v2.1.219; the order named `7db035e4`, dell2's release landed first), CI run 38565663189 success; issuer re-read: 5 of 5 blobs EQUAL to `84fd6461bb`, 5 files differ from `501e998b` |
| `AMGT-bm-5` | the 93-name census (issuer, done) and the fresh-draw ten-name walk on a local build of PROD | STAGED for 2026-10-15 | worker ~443; **AC5 is JUDGMENT** (yours) |

## 2. The issuer's real runs

- **Census, re-run by the issuer on the live function after `bm-3` (`round106/census_v5.txt`, committed @60c22aefe7):** 95 of 95 names, 0 read failures; UNEXPLAINED 3 (`thesis.model_cases` on BABA_US, BA_US, PBR_US) and STATE_ONLY 187, both exactly as in `round105/census_v4.txt`; raw-code CANDIDATES 9,609 in 896 patterns (9,614 in 899): a candidate is not a verdict.
- **The served withhold, read by the issuer on the live function:** PBR US serves 0 `BEST_PE_RATIO` forecast rows and `model.forecast_withheld` names `USD` and `BRL`; `ai_fill` reads ABSENT (the hold).
- **Walk:** TO BE FILLED after 2026-10-15 00:00Z. The draw is for 2026-10-15 (round 105's draw of 2026-10-14 would repeat the same ten names): BNP FP, SHOP CN, SAP GY, NOKIA FH, VIVT3 BZ, 9433 JP, HD US, OMAB MM, ICICIBC IN, IMB LN (`round106/walk_draw_20261015.json`).

## 3. WHAT THE READINGS SAY

TO BE FILLED after the walk (the issuer's own read of the Model shots for SHOP CN and one name with a historical P/E, then the worker's one line per name).

## 4. Open and carried

`~R2`'s AIFILL workstream (the AI-fill hold stays until the CVO's five-name re-read is MET); the Terminal sign-in (Andrew); the CTO's note for later pairs on this function (hold or name the harvest pool's writers for the capture-to-verify window). Evidence outside the repository: `C:/dev/ui-walk-evidence/bm-5/`. Left on disk: `C:/dev/wk-resapp-418` and its leftovers, and the two stale build worktrees `C:/tmp/aa5-build`, `C:/tmp/bd2-build` (a recursive delete is Andrew-class, not done).
