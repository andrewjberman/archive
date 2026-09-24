# AMGT_RESAPP round 39 -- drain-end packet and the issuer's one real run (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.47, issuance @3e2126d0c6. PRD v0.26 unchanged. Six orders, six terminal. Push state: LOCAL.
The CVO is engaged because one cell (rn-5) is `SERVED`; the other five are `LOCAL` and close on the checker's match plus the real run.

## 1. Orders and their terminal state

| cell | risk | slot | close carried | outer drain | result | rows |
|---|---|---|---|---|---|---|
| rn-1 the size-10 residue | LOCAL | ~146 | afe52707ba | db7bea0ef0 | 2/2 PASS, VALID; `text-[11px]` on PanelHeader's timestamp caller | W146-S1 (INERT) |
| rn-2 the P/E units | LOCAL | ~147 | 70cddf857b | 4258d3dc8f | 3/3 PASS, VALID; P/E in [0.5,200] 24 of 24 (base 5 of 24) | none |
| rn-3 the retired identity's prose + C13 | LOCAL | ~148 | 47594d1ee3 | 7bd77f0fe2 | 3/3 PASS, VALID; C13 in DESIGN.md verbatim, 0 files outside the allow-list, census unmoved | W148-S1 (INERT, dismissed) |
| rn-4 the ancestor-aware clip arm | LOCAL | ~149 | 304d6dfb7b | 9d1eb7da0b | 2/2 PASS, VALID; leafOnly=0 ancestorAware=1, mutant-controlled | none |
| rn-5 FWD-30 on the served plane | SERVED | ~150 | 7ff18c1b2c (AC1 amended @c89e9febdf) | af01ba8baa | complete AS A MEASUREMENT: AC1 met on the amended wording, AC2 FAIL recorded | W150-S1 (INERT), **Z-S268 (BLOCKING, ARMED, the CTO's)** |
| rn-6 the sidebar under the contract | LOCAL | ~151 | daf53756e4 | 87afe9bc14 | 2/2 PASS, VALID; App.tsx census 0/0/0/0 (was 2/5/5/2) | none |

Portal DEV 5e339ffd -> 46c0ae11 across six merges; the gitlink at CLOUD HEAD reads 46c0ae11. Worktrees and branches removed.

## 2. THE ONE REAL RUN -- shared 5174 build, portal DEV 46c0ae11, 2026-09-24 ~19:3xZ

`checks/drain.real-run.sh 5174 round39/real-run` -> **contract-check exit=0, the first on this project.** Every graded column PASS
on all six states in BOTH scopes: bandContainersTopLevel, fonts, weights, sizes, radii, shadows, lowContrastChars, purpleFills
6 of 6 main and 6 of 6 body; clippedTextBlocks 0 on 6 of 6 in both (the ancestor arm live). Six PNGs under `real-run/`.

**Looked at, all six, by the issuer** (FWD-29's person-read limb is the CVO's to record; these are the same six files):
- peers: P/E now plausible (Deere 34.70 trailing / 29.22 NTM; median 34.90 / 29.66; min 15.03, max 75.67).
- list, exec, model: render as the contract says; model shows the REFUSED dividend row and every absence line.
- **Four things no check sees, carried (s.5):** thesis's "COMPANY DESCRIPTION" section holds backlog figures while the header says
  "Description: ABSENT"; posture calls the Deere comparable identity UNRESOLVED while Peers lists Deere & Company as member one;
  posture prints a local Windows path (`org\missions\...\0.9.0_WK_AMGT_RESAPP~1\model_block_DE_US_Equity.json`) to the user; the
  header reads "BLOOMBERG: UNKNOWN" beside "BA US".

Drain hygiene (`real-run/drain.*.log`): typecheck exit 0; `lib/research/peers` + `lib/research/identity` 138 passed; magnitude
24 of 24; clip self-test leafOnly=0 ancestorAware=1.

**Bound, stated:** the real run is a LOCAL vite render on the captured fixtures; nothing in rounds 37-39 is deployed to the portal.

## 3. Item 7 -- Z-S226's authenticated render on the DEPLOYED surface: NOT OBTAINED this round

The authenticated read needs a headed sign-in with MFA as a real portal user; no seat or worker holds one, and signing in as
Andrew is his act. What IS measured on the served plane (16:0xZ, unauthenticated, discriminating): every AMGT path answers the
edge's 401 JSON exactly as the `tickets` control family does, and an unclaimed family path still returns 200 text/html -- routing
is fixed (rk-122/123). Whether the page renders for a signed-in user is open, and it is the one read that needs Andrew present.

## 4. Judgment criteria this round

NONE on any face. rn-5 is `SERVED` with mechanical criteria only; the CVO grades its outcome on the real-run record and on rn-5's
served artifacts (`deliverables/0.9.0_WK_AMGT_RESAPP~150/served/`).

## 5. New investigation rows (L8 input) and what is carried

Rows: W146-S1, W148-S1, W150-S1 (all INERT), **Z-S268** (BLOCKING, ARMED, disarm owner the CTO): FWD-30 is not met on the served
plane (the export omits the CIE_DES description absence the page discloses) and, on BOTH planes, the export publishes 17 figures
the page does not show -- 10 the IS_DIV_PER_SHR series the page REFUSES -- while `exportCompare.harness.cjs` computes extras and
never grades them. **FWD-30's round-38 REALIZED grade rested on that blind spot.**

Carried to the CTO's round-39 analysis:
- Z-S268's fix: `render_pack.build_rich_text` honours the page's REFUSED rows and absence lines, and the harness grades extras.
- rn-2's units are INFERRED from the served fixture's scale: the factor registry has no `unit` field on any of its 289 factors.
- The four person-read findings of s.2.
- Item 7 at Andrew (s.3).
- Standing from round 38: Z-S238 (a request log line on the scoped API, needs a pair), Z-S227 (isError branches),
  W85-S1 / W117-S3 / W58-S2 (hygiene).
