# AMGT_RESAPP round 37 -- drain-end packet (L7 -> L8/L9 handoff to `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.45 @373c431072 (+592b1a942d, 53793b671f). PRD v0.25 ADDENDUM B (FWD-21..FWD-30).
Ten cells, one instrument first, seven surface cells in wave 1, two in wave 2. Every order is terminal at this packet.
DRAFT written at the wave-1/wave-2 boundary (10:2xZ); the wave-2 rows are filled at the second drain. Push state: LOCAL.

## 1. Orders and their terminal state

| cell | order | worker | drain | close-out | criteria | rows |
|---|---|---|---|---|---|---|
| rl-1 the instrument | AMGT-rl-1 | ~130 | 5c2af33d86 | bc15e1957e | 3 of 3 PASS, VALID | W130-S1 (resolved by Z-S244) |
| rl-2 shell + identity header | AMGT-rl-2 | ~131 | 973dc1cf5d | 42667f7f2f | 3 of 3 PASS, VALID | none |
| rl-3 thesis ladder | AMGT-rl-3 | ~132 | a8aa8bff17 | e8b909f937 | 3 of 3 PASS, VALID | none |
| rl-4 exec management | AMGT-rl-4 | ~133 | 2488c1bf0d | 9fd81fb52c | 3 of 3 PASS, VALID | none |
| rl-5 peers present columns | AMGT-rl-5 | ~134 | 5a24b4612f | 894631e0a9 | 3 of 3 PASS, VALID | none |
| rl-6 model sheet | AMGT-rl-6 | ~135 | 75591cc1b9 | 7dda7167be | 3 of 3 PASS, VALID | W135-S1 (INERT); issuer's Z-S247 |
| rl-7 posture | AMGT-rl-7 | ~136 | 6d2c73459b | b1d42fb62b | 3 of 3 PASS, VALID | W136-S1 (INERT) |
| rl-8 lead panel | AMGT-rl-8 | ~137 | 6b1f1d838d | ca52fa60c1 | 3 of 3 PASS, VALID | W137-S1 (ARMED -> resolved at the drain), W137-S2 (INERT) |
| rl-9 designed states + re-assert | AMGT-rl-9 | ~138 | (wave 2) | (wave 2) | AC1-AC3 mechanical, **AC4 JUDGMENT** | (wave 2) |
| rl-10 the export | AMGT-rl-10 | ~139 | fa3b0152d2 | 096a06ca6b | 3 of 3 PASS, VALID | none |

Proof instances: `deliverables/0.9.0_WK_AMGT_RESAPP~<n>/*.proof_of_spec.json`, each re-validated by the issuer inside the worker's
worktree before its drain (the main tree's checker refuses an out-of-tree instance by design).

## 2. The ONE judgment criterion of the round -- rl-9 AC4

FWD-29's last clause: *the six PNGs read by a person, a rejection citing its clause* (`C-CLAUSE-CITED-REJECTION`,
`C-RENDER-IS-THE-ORACLE`). The PNGs sit under `deliverables/0.9.0_WK_AMGT_RESAPP~138/contract-check-final/` after the wave-2 drain;
the worker records AC4 as UNVERIFIABLE-BY-INSTRUMENT naming the CVO. Graded at L9 against `portal/DESIGN.md` C1-C12.

## 3. New investigation rows this round (the L8 input: "new rows and no others")

`surprise-channel/investigations/INVESTIGATION_v1.md`: W130-S1, Z-S244 (GRADUATED), W135-S1, W136-S1, Z-S247 (UNDER_INVESTIGATION,
ARMED, disarm owner the issuer, fix routed to rl-9), W137-S1, W137-S2, plus any wave-2 rows (filled at the second drain).

## 4. Drain-time instrument reads (repo-wide hygiene at the drain)

`deliverables/2.0.0_SA_COO~Z/round37/contract-check-after-rl-<n>/` (n = 2..8, 10), six states each, json + png. Movement through the
wave: thesis lowContrast 185 -> PASS (rl-3), peers band -> PASS (rl-5), posture lowContrast 7 -> PASS (rl-7), model lowContrast
PASS -> 37 (rl-6, row Z-S247), list purpleFills 4 -> 3 (rl-8). Wave-wide residue at rl-8: weights [300,500,600], sizes [10],
radii ["8px"], shadows 1 on every state; band list 3 / peers 1 / others 2 -- rl-9's cell. Final read: `contract-check-final/`
(wave 2).

## 5. Issuer moves outside any cell, all recorded in the close-outs

- fixtures re-homed under `__harness__/tests/` (naming gate's exemption class; portal 513bb3c5, row Z-S244).
- `tabs.harness.cjs` loader stubs (PanelFooter, Segmented, HelperTip; portal 1267a67e) so the shared harness loads over the merged
  page; its three pre-round assertions now read wrong-way by design and are rl-9's AC3.
- the append-only channel resolved at each drain by taking HEAD whole and appending the worker's rows (the gitlink set by hash).

## 6. What the round does NOT close (for the CTO's round-37 analysis)

- FWD-30's route change (serving the rich-text export) returned to the CTO on rl-10's ROUTE_ASK_export_rich_text.md (existing /print leaf, `?format=rich`, text/markdown); no route was edited. rl-10 also measured the landed pack: 8 pages vs the 2-page cap, model-block only, 11 of 11 DESIGN_BIBLE items NOT MET -- branch (a) is NOT met and branch (b) is built on the producer, not yet served.
- The PRD's F2/F3 corrections ride the post-drain edit (CTO).
- Portal DEV carries this round's commits at c6ecc9ba after rl-10 (+ rl-9); the deploy is the integrator's on Andrew's word.
