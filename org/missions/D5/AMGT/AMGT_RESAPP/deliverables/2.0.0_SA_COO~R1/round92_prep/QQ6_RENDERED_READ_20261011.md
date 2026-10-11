# AMGT-qq-6 -- FWD-38's rendered-page read on ASML, BA and ROG (issuer act, round 92)

**Reader:** `2.0.0_SA_COO~R1`, 2026-10-11 ~09:5xZ. **Source:** CTO round-91 analysis item 6: "On ASML, BA and ROG, read the cross-vintage caveat and
each member's `cap_vintage` as rendered. If the page shows neither the date nor the why, the engine date line is cut, riding the next scheduled rebuild."
**State read:** the function live at `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` (AMGT-qq-5, applied 09:26:42Z), peers partition `2026-10-11T0707Z`.

## Instrument (what "rendered" means here, stated)

The REAL `portal/src/pages/SecurityAnalysis/tabs/PeersTab.tsx` (transpiled with the portal's own TypeScript and rendered by `react-dom/server`, the loader of
`__harness__/peersPattern.harness.cjs`), fed the LIVE served payloads of the deployed function: `/security/<key>/peers` and `/security/<key>/overlay` (the header
figures the subject row prints). **It is a server render, not a browser walk:** it reads the markup and text the component produces; it does not exercise
CSS, visibility or hover. `HelperTip` content is in the markup as a hidden node (the harness stub), so hover text is read, not seen. `/ui-walk` (a live
browser walk through the dormant walker account) was not run: it arms a service account for a read this instrument answers.

## What is served, per name (peers route)

| | ASML_NA_Equity | BA_US_Equity | ROG_SW_Equity |
|---|---|---|---|
| `universe_vintage` | 2026-10-02 | 2026-10-02 | 2026-10-02 |
| `as_of` (the objects' partition) | 2026-10-11T0707Z | 2026-10-11T0707Z | 2026-10-11T0707Z |
| subject `cap_vintage` / `market_cap_vintage` | 2026-10-10T13:01:55Z | 2026-10-10T13:02:24Z | 2026-10-10T13:08:49Z |
| every member `cap_vintage` | 2026-10-02 (12 of 12 read) | 2026-10-02 (12 of 12) | 2026-10-02 (12 of 12) |
| subject `cross_vintage_caveat` | present (scalars at the model block's vintage, candidates at the scanner's asOf, graded ACROSS the two, neither re-dated) | present | present |
| `cap_fx_caveat` | EUR vs USD, no FX applied | none | CHF vs USD, no FX applied |

## What the page renders (the PeersTab markup)

| | ASML | BA | ROG |
|---|---|---|---|
| subtitle line | "12 comparable(s) universe vintage October 2nd, 2026 as of October 11th, 2026" | same | same |
| subject row Mkt Cap | "EUR 622B **as of October 10th, 2026**" | "USD 150B **as of October 10th, 2026**" | "CHF 290B **as of October 10th, 2026**" |
| member Mkt Cap cells | figure in USD, **no per-member date** | same | same |
| the `cross_vintage_caveat` sentence | **not rendered** (no match on "ACROSS", "re-dated" or "cross-vintage" in the markup) | not rendered | not rendered |
| the word "CAVEAT" (the `reason` field's FX caveat) | not rendered | n/a | not rendered |
| basis chip hover (`test`) | the derivation statement; it carries no vintage and no caveat | same | same |

The portal source never references `cross_vintage_caveat`, `cap_vintage` or `cap_fx_caveat` by name outside fixtures (Grep over `portal/src`, ts/tsx/js/cjs).

## Reading, against the CTO's condition

- **The DATE is shown.** The reader sees the members' vintage once ("universe vintage October 2nd") and the subject's own cap vintage on its row ("as of October 10th"):
  the 5-trading-day gap is on the page, in dates, for all three names. The member-level `cap_vintage` is not printed per member; it equals the universe vintage printed in the subtitle (12 of 12 on each name).
- **The WHY is not shown:** the sentence that says the band is graded across the two vintages and neither is re-dated is served and not rendered.
- **Condition "neither the date nor the why":** NOT MET (the date is shown). **The engine date line is NOT cut.** The unrendered why is carried as an enrichment candidate (a portal cell to render the served caveat under the table), not a defect of the engine.

## Seen in the same render (not in scope; recorded)

- ROG_SW_Equity lists "Roche Holding Ltd ROG SW" as the second member, under the subject "Roche Holding AG": the subject appears among its own peers (row `AMGT_RESAPP-D1-S21`; the reason line reads "2856 database minus 0 self").
- Some members read "currency not stated" beside a price (INTC US, the Tencent row, UNP US): the existing no-record path, byte-equal across qq-5 (the compare names none of these members).
- ROG's header carries `PX_LAST` null, so its subject row prints "--" for Price; unchanged by any round-92 cell.
