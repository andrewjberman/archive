# AMGT_RESAPP round 46 close run -- the issuer's ONE REAL RUN of the round's outcome (2.0.0_SA_COO~Z)

- **Served artifact:** opal-amgt-scoped-api CodeSha256 `CtIvirvMTG47vvgBGmouk3GrTNKPjPIPx/6ovB+EAOM=` (the combined uu-4 + HVST-a-2
  act; AC1 re-measured by the issuer, LastModified 2026-09-29T01:58:24Z).
- **Fixture:** `fixture.AMD_US_Equity.json`, re-captured 2026-09-29 ~03:5xZ from the DEPLOYED function (one read-only invoke per
  route, six routes, shape of `0.9.0_WK_AMGT_RESAPP~164`'s fixture, keyed under BA_US_Equity; `_provenance.code_sha256` above).
  Served thesis `model_cases.base`: SERVED 415.64057358490567, formula "adjusted consensus EPS (FY1) x adjusted trailing-median P/E
  (PX_LAST / IS_COMP_EPS_ADJUSTED)".
- **The running page:** port 5174 (the only dev port), `portal/scripts/ui-contract-check.mjs --states list,model`, rc=0, contract PASS on
  both states. Positive control: loc `/security-analysis/BA_US_Equity`, textChars 5654 (the /login page reads 141).
- **LOOKED AT (`real-run-AMD_US_Equity/model.png`):** the Model tab reads "Base case: SERVED -- 415.64057358490567 USD (adjusted
  consensus EPS (FY1) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED))" beside Price USD 630.63; Upside and Downside
  read the ruled ABSENT reason. **The served adjusted Base case crosses to the page.**
- **BOUND, stated -- the page's two-decimal rule is NOT on this run:** 5174 is `1.0.0_SA_CTO~Z`'s walk build for Andrew
  (`C:/tmp/amgt-walk-5174`, branch `amgt-walk-5174-20260928` @e3f77e40, vite started 2026-09-28T21:28Z), which does NOT contain portal
  DEV 8fa7abde (uu-3's `ModelTab.tsx` `toFixed(2)`). So the running page prints the raw float while the deployed export prints
  "415.64". The two-decimal page rule is proven only by the harness at portal DEV (uu-3 AC2 2 of 2; uu-4 AC2 95 of 95, cases 285/285).
  No second dev server was started (5174 only). The timeline panel's 401 is HARVST's mount on that build, not this round's.

**BOUND CLOSED (2026-09-29 ~04:0xZ):** `1.0.0_SA_CTO~Z` merged local portal DEV 8fa7abde into the walk build (branch now af19fedd;
vite hot-reloaded `ModelTab.tsx` at 03:56Z). Re-run on 5174, same fixture, `--states model`, rc=0, contract PASS:
`real-run-AMD_US_Equity-after-walk-ff/model.png` read -- **"Base case: SERVED -- 415.64 USD (adjusted consensus EPS (FY1) x adjusted
trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED))"**, two decimals, the same line the deployed export prints. The running page and
the export now agree on the round's outcome.
