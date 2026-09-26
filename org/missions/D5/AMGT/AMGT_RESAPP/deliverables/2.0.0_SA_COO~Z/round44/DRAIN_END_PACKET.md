# AMGT_RESAPP round 44 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.52, issuance @894cc7403d, on the CTO's round-43 analysis @37217d8053. Three orders,
all terminal, each proof instance re-graded VALID at HEAD by this seat. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | drain / entry | result |
|---|---|---|---|---|---|
| rs-1 the case value names its currency | SERVED | ~161 | e6aa711277 | a631ba6249 (portal DEV 53ccbc52 -> 6712c742, fast-forward; gitlink = 6712c742) | AC1 48 of 48; AC2 95 of 95, cases 285 of 285; AC3 tsc 0; VALID; AC4 is JUDGMENT (s.3) |
| rs-2 the redeploy | WORLD | `0.7.0_AE_CloudOps~A` | 758e4e21cd | NEVER-2 entry 2defc1b419, CLOSED 7 of 7 legs | CodeSha256 `982nlz5T...mYvo=` -> `LK9h47ju...DcO4s=`; AC2 95 of 95, cases 285 of 285; five stop limbs CLEAR before upload; pdf OUTPUT unmoved; VALID |
| rs-3 the four-input trace | LOCAL | ~162 | 13bfde96e1 | 7892fbee40 | AC1 4 of 4, citation defects 0 (issuer re-run exit=0); VALID |

Worktrees ~161 and ~162 are removed. `0.7.0_AE_CloudOps~A` was seated by this seat for rs-2 (pre-flight: 0 processes, 0 markers,
its one open order rs-2) and is idle with its order complete.

**Issuer acts in the round, each committed:**
- **The COO never-widen half, amended @4256b6ba46** at the CTO's msg 26029, to name BOTH branches: (i) a case gains its CRNCY;
  (ii) a disagreeing `quote_currency`, or no CRNCY, renders byte-unchanged. The CTO signed both @8e2a4a808f against rs-1's landed
  rule, and added stop limbs 4 (no code change to `_case_currency`/`_model_case_line` beyond a631ba6249) and 5 (pdf OUTPUT graded,
  not the diff). Both limbs were relayed in the GO.
- **rs-2's NEVER-2 entry** was unstaged by `2.0.0_SA_COO~O`'s drain at ~09:40Z (msg 26055) before it was committed. The lane was told
  under the order; it committed @2defc1b419 and stated the build had not started. Bound 1 held.
- **rs-2's `<status>` flipped to complete by the issuer @f4e94c87b7**, graded by proof-of-spec-check VALID.

## 2. THE RESULT -- FWD-30 on the served plane, population stated

| population | plane | OK | cases | currency on SERVED cases |
|---|---|---|---|---|
| the LIVE research library, 95 folders, read_at 2026-09-26T13:29:01Z | SERVED, deployed `LK9h47ju...DcO4s=` | **95 of 95** | 285 of 285, missing 0, extra 0 | **48 of 48** (USD 21, EUR 14, MXN 4, GBp 3, BRL 2, TWD/CAD/PHP/CHF 1 each) |

Evidence readable at a pin: `round44/close-run/` @f4e94c87b7 (TSV, log, PROVENANCE with the artifact id beside read_at). The lane's
own AC2 read the same numbers independently. **The denominator moved 94 -> 95:** AIA Group, pinned out in round 43, now serves.

**The page renders it** (real run on 5174, portal DEV 1e02be40 containing rs-1's 6712c742): `round44/real-run-rkt/` @6473d33fc2,
contract check PASS on 6 of 6 states. Every state carries a POSITIVE CONTROL beside its absence metrics
(`round44/real-run-rkt.CONTROL.txt`, 6 of 6: location under /security-analysis, not /login, and text length over 300 against the
login page's 141), as the CTO's msg 26033 asked. The Model tab reads "Base case: SERVED -- 7386.63633 GBp (...)" beside the Price
tile "GBp 4923.00". RKT's payloads sit under BA's route keys, as in round 43, because the instrument navigates to BA only.

**Bounds, stated:**
- Branch (ii) has population ZERO here: COVERED BY READING, NOT EXERCISED (the CTO's condition). The first name with a disagreeing
  `quote_currency` or no CRNCY is read before the next redeploy is signed.
- The page change is on portal DEV; the deployed page is not promoted.
- Served values print unrounded, e.g. "537.6961078500001 USD" (GOOGL) -- for the judgment reader, not a claim of a defect.

## 3. Judgment criterion (L9; never self-graded)

**rs-1 AC4.** `round44/rs-1.AC4.served.txt` prints the SERVED export's Model Cases section for RKT (GBp), AMD (USD) and GOOGL (added
this week), from the post-deploy close run. Read it beside `round44/real-run-rkt/model.png`: does each served value read as a price
in a named currency, the same on both surfaces?

## 4. Rows this round (L8 input)

None filed by the workers or the lane. rs-1 verified the order's own denominators before writing code (48 SERVED; 45 without
`quote_currency`, 3 GBp agreeing; 0 disagreeing; 0 CRNCY-absent). The channel is unchanged by this round.

## 5. Carried to the CTO's round-44 analysis

1. **rs-3's trace** (`deliverables/0.9.0_WK_AMGT_RESAPP~162/FOUR_INPUTS_TRACE.json`): spans `drafting_build.py:303` (RESAPP);
   unit_sign `model_block_pull.py:700` (shared RESAPP/CORPUS); social_chatter `scoped_amgt.py:1999-2000` (RESAPP, bare nulls);
   universe `build_universe.py:846-855` (RESAPP, held on Andrew naming the population).
2. **The team's own cases** (CTO msg 26065 @bfc179c2ea): the Upside/Downside card is STRUCK; 34 of 95 dossiers carry cited cases.
   The served "ABSENT -- methodology to be discussed with Andrew" is now a stale reason on every page. The render is FWD-24.
3. **FWD-31** @c2c6c507d6 (the management passage beside the roster): a NEWLY-ADDED round-45 order is refused until the ratified-text
   half is re-signed at v0.27.
4. **Two implementations of one rule:** `_case_currency` (Python) and `caseCurrency` (page). Drift will surface as an FWD-30
   comparison failure, not as a currency bug (CTO msg 26043).
5. **The portal promote.** Every page fix from rounds 40-44 is on DEV only.
6. **Throughput on site Z:** commits took over 120 s, and three failed on the shared index lock or a peer's open merge. Workers ran
   100-115 minutes. `0.0.0_AB_MSTR~Z` measured git status at ~380 ms paused against 822 ms with ten seats live.
7. **Standing:** ACCEPT (carded); FWD-7's route coverage; the span write; the wiring class; Z-S272; Z-S276; Z-S287 (resolver).
