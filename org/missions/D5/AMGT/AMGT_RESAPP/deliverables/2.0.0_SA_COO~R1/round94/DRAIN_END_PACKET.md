# AMGT_RESAPP round 94 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~15:3xZ. Five orders, all complete: `ff-1`, `ff-2`, `ff-3` built and merged (`ff-2`'s portal candidate LANDED on DEV);
`ff-5` (a served write) and `ff-4` (the ONE redeploy, `opal-amgt-scoped-api` `SOzAz9..` -> `VNcX9ntm..`) APPLIED and HELD.** `round-close-check.py --round 94`: orders 5, proof_ok 5 of 5, judgment 0,
verdict MAY-CLOSE. Round 94 implements the CTO~DELL1 round-93 analysis @bfa6b04c8c (items 1-4); decomposition s.102; issuance
@61d50fc7fa. Amendments (all the issuer's own check or face errors, each with its gate limb: none grades a criteria or face edit on the issuer's own order): ff-1 AMENDMENTS 1, 2, 3
(@77f0442827, @4cd8c70913, @38ea4b10fe), ff-5 AMENDMENT 1 (@090b13df6d), ff-4 AMENDMENTS 1, 2 (@e9675913e8 and @15b7af1601).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-ff-1` | 1: a classification name never overrides a disagreeing registered name | complete, merged @7e9d36c697 and @7b54de1245 (three amendments, four paths: the chain, the overlay header, the ranked rows, the rank timeseries); producer-and-serving side, rides ff-4 | worker ~387, proof VALID, re-seated three times |
| `AMGT-ff-2` | 2, 3: the peers Mkt Cap heading names its served codes; the Ticker cell says "no ticker held" | complete; portal candidate `wk-AMGT_RESAPP-388-portal` @f0229015 CTO-approved and LANDED on portal DEV @582ffe6eb8 (MSTR's landing receipt); PROD unchanged 37aa1247 | worker ~388, proof VALID; rendered read `round94_prep/FF2_RENDERED_READ_DEV_20261011.md` |
| `AMGT-ff-3` | 4: a mixed-scale series is shown on its unit's scale | complete, merged @ae14fab6f5; producer-side (`analyze.py`) | worker ~389, proof VALID |
| `AMGT-ff-5` | 4: SAP's stored driver re-verified and spliced on the unit's scale | complete, SERVED: SAP 0 -> 3 points (2023 = 13.745, 2024 = 18.078, 2025 = 21.05 EUR billions, stated scales kept); 2 of 24 VersionIds moved | RA1 ledger `amgt-resapp-r94-ff5-sap-rescale-dell1` CLOSED 8 of 8 @d63bbe34ba, proof VALID |
| `AMGT-ff-4` | 1: the ONE redeploy carrying the registered-name rule (and AMGT_CORPUS leg p) | complete, SERVED: the function's code moved `SOzAz9/gfKE..` -> `VNcX9ntm83qe07/eOOD16AYsDmoEp20eCzj9ljfGvGE=` (apply 14:57:16Z, 42,125,071 bytes), built at pin 15b7af1601; the build also carries AMGT_CORPUS leg p (`dossier.py` METHOD /12) | RA1 ledger `amgt-resapp-r94-ff4-name-redeploy-dell1` CLOSED 10 of 10 @f66420057c, proof VALID; pair `ledger/NEVER_WIDEN_ROUND94_NAME_REDEPLOY_{COO,CTO}_HALF.md` (COO @15b7af1601, CTO msg 3919) |

## 2. The issuer's ONE REAL RUN at close

- **ff-5 (SERVED, WORLD): re-run by the issuer, not RA1's report.** `r94_sap_served.py` on the live `/thesis` routes: V1 SAP 2023 = 13.745, 2024 = 18.078, 2025 = 21.05 with stated scales
  million / million / billion and `rescaled_to` billion; V2 ASML none; V3 BABA FY2025 = 118,028 and FY2026 = 158,132; `R94 SAP SERVED: YES`.
- **ff-2 (portal, LOCAL on DEV):** the real `PeersTab.tsx` at `origin/DEV` @1f0b1d68c5 server-rendered over live ASML, ROG and BA payloads: `r94_peers_units.cjs` 5 of 5 (ASML "Mkt Cap (EUR, USD)",
  ROG "Mkt Cap (CHF, USD)", BA "Mkt Cap (USD)"; four members with no held ticker print "no ticker held"). A server render, not a browser walk: the CVO's L9.
- **ff-1 / ff-3 (LOCAL): on the merged tree.** `r94_display_name.py` 12 of 12, `r94_name_census.py --where local` 243 of 243 judged DIFFERENT 0 with the ranked rows (126 judged) and the rank series (82
  judged) at 0, `r94_rescale.py` R1-R7, the whole `lib/research/api/tests` directory 944 passed.
- **ff-4 (SERVED, WORLD): re-run by the issuer on the live function, not RA1's report.** `r94_name_census.py --where deployed`: 243 of 243 judged, DIFFERENT company 0 on the overlay header (the base read 2:
  SAN_FP_Equity 'Banco Santander S.A.', CSL_AU_Equity 'Carlisle Cos Inc'), the four ranked lists 126 rows judged 0 different (C3; the base 2), the rank timeseries 82 series judged 0 (C4; the base 2);
  `R94 NAME CENSUS: YES`. Live: SAN FP overlay `display_name` 'Sanofi', `name` 'SANOFI', source `crosswalk`; CSL AU 'Csl Ltd', 'CSL LTD'; ranked row 67 and series 67 'Sanofi', `name_state` ABSENT;
  the classification objects of both tickers unmoved ('Health Care'; 'US Large Cap', sector null). `r92_minor_unit_census.py` M1-M4, `R92 MINOR-UNIT CENSUS: YES`; `r89_peers_deployed.sh` and
  `r89_deployed_close.sh --want amgt-corpus-dossier/12` YES. **RA1's compare** (`FF4_POST_APPLY_COMPARE_20261011.json`, the pre-apply baseline of 519 requests recorded 14:51-14:56Z against the
  live function after): 157 changed paths = **79 name paths** (12 overlay/peers, 8 ranked, 4 series, 49 timeline, 6 chatter) + **50 corpus paths** (AMGT_CORPUS's `model.team_sheet`) + 28
  `generated_at` clocks, **0 outside the pair's table**; status moved 0, missing 0; all 2,230 peer members, every score and rank, both classification objects byte-equal. AMGT_CORPUS's own post-act
  read (msg 3930): Branch A, team_sheet equals the stored /12 field 95 of 95. Portal PROD unchanged @37aa1247 (ls-remote read 15:2xZ); DEV @d7792da1bf. Two limits, stated: the series rule matches a
  ticker by the covered universe's exact ticker, so `CSL AU` asked for BY TICKER on the timeseries still reads 'Carlisle Cos Inc' (it is on no ranked list, so no page asks); and my scripts'
  `--after deployed` reads the live function twice, so the compare used the recorded baseline.

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **ff-1's cell text named the chain, the overlay and the peers subject; the name is served on four paths.** The table the redeploy's pair requires (live function against the merged handler,
   243 subjects x 2 routes) found the overlay header unmoved; reading the live function then found the rank timeseries. Cost: ff-1 reopened twice (two amendments), worker re-seated three times,
   and one existing test that pinned the superseded precedence for a disagreeing pair (row `D1-W387-S3`), which my census of tests, naming the nine names tests I knew, had not run. The control
   is now the whole `lib/research/api/tests` directory.
2. **ff-3's checks had no idempotence arm.** The rescale stores the shown `value` beside `stated_value`; `reverify_stored_thesis_driver` reads `value`, so a second re-verification of an already
   rescaled object keeps 1 of 3 points (SAP). ff-5's AC1 took its expected points from that very function and could not read YES after its own write; RA1 held the order open with the writes
   landed and correct. Row `D1-S24` (ARMED, owner this seat); ff-5 AMENDMENT 1 reads the served route against the pair's table; the CTO ruled ACCEPT (msg 3887) and named the repair round 95's
   first cell. Until it lands NO operator re-verifies SAP's object (recorded in the ff-5 ledger leg L8).
3. **ff-4's baseline would have missed the SAN name on three routes had the order's table been the two per-subject routes only.** The ranked lists, the rank timeseries, the timeline word cloud
   and the collected-chatter list each serve the name; `r94_rankings_table.py` and `r94_other_routes_table.py` read them, and the pair lists every changed path (79 name paths).
4. **ff-4's AC2 wanted `amgt-corpus-dossier/11`.** The build carries AMGT_CORPUS leg p, so the package's literal is /12 after a correct deploy; amended before the GO (it would have failed a
   correct apply).

## 4. JUDGMENT for L9

No JUDGMENT criterion in an order. Offered for the CVO's own re-run: `r94_name_census.py --where deployed` (243 subjects, the ranked lists and the rank timeseries), `r94_sap_served.py`,
`r92_minor_unit_census.py`, and the browser walk of the DEV peers page on ASML, ROG and BA for **round-93 items 2 and 3** (the heading and the Ticker cell), and of the Security Analysis header of
SAN FP and CSL AU for **item 1** (Sanofi and CSL Ltd named as themselves).

## 5. Rows filed this round

Workers: `D1-W387-S1`, `S2` (round 94 wave 0, ruled in the order statuses), `D1-W387-S3` (BLOCKING, ARMED: an existing test pinned the superseded precedence) ruled by ff-1 AMENDMENT 2. RA1:
the ff-5 finding file `AMGT_RESAPP.TO-AMGT-ff-5.RESCALED_OBJECT_DEGRADES_ON_REVERIFY.md` (became `D1-S24`). Issuer: **`D1-S24`** (ARMED): the verifier is not idempotent over a rescaled
object; **`D1-S25`** (ARMED, closed by ff-4 once it reads YES): the rank timeseries serves the table's name by bare ticker; **`D1-S26`** (ARMED): CSL AU serves Carlisle's classification (sub-asset
class 'US Large Cap', sector null), the same bare-ticker collision as the name, not moved by this round (it is served today). **Disarmed by this round:** `D1-S23` (the name, once ff-4 reads
YES).

## 6. For the next round (the ENRICHMENT LIST's inputs; the CTO's own words at msg 3919 and 3887)

1. **D1-S24, first cell:** `reverify_stored_thesis_driver` locates a point by its `stated_value` when the stored point carries one (and `held_uncited` the same); close: a re-verification of an
   already rescaled object keeps its 3 of 3, byte-equal, and a negative arm still holds (a stored value no excerpt prints is held).
2. **D1-S26, second cell:** the classification lookup applies the same disagreement rule: when the registered name disagrees with the table's name for the bare ticker, the classification is not
   served from that row and says why ("classification not available for this listing") until an exchange-qualified row exists. Close: CSL AU serves no Carlisle field; SAN FP's classification
   is read and printed, its 'Health Care' sector shown to be Sanofi's row and not a coincidence.
3. **The 'Csl Ltd' casing:** `_clean_display_name` title-cases a short all-capitals registered name ('CSL LTD' -> 'Csl Ltd'); cosmetic, the shared rule's limit.
4. **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6` and FWD-16 stay Andrew's.

checked 5 of 5 orders terminal, 5 of 5 proofs VALID
