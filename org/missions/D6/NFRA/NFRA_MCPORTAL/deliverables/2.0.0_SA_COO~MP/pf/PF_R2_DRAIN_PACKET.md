# NFRA_MCPORTAL -- WORKSTREAMS PE + PF DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-16 ~02:4xZ

**Workstream:** PE (the /gateway view grouped by source, no Microsoft 365 default) and PF (the page segmented by CONTRACT C-GROUP:
bucket, and for opal-data-assets and opal-data-bd by vendor and firm). PRD v0.9 @532d1e68bb; CTO GO msg 34553. PD stays HELD.
**Risk:** LOCAL on every build cell. The live page is not yet SERVED: it needs MCPINDEX's C-GROUP catalog release and the gateway release
that carries the handler (NFRA_OPLGTW OG-ap-23, 2.0.0_SA_COO~O).
**Judgment criterion:** one, `MP-pf-2` AC2 (legibility at 1280 px and 390 px), for `3.0.0_SA_CVO~Z`. Everything else is mechanical with a VALID instance.

## Orders: 5 of 5 terminal

| Order | What it built | Drained / complete |
|---|---|---|
| MP-pe-1 | handler: the breakdown groups every tool by its declared source; no Microsoft 365 default | merged @8310672247, complete @eda189ed43 |
| MP-pe-2 | the Gateway page: one section per group, summary table, plain kind words | merged @4d59d9170f, complete @b006b05b90 |
| MP-pf-1 | handler: opal-data-assets and opal-data-bd channels carry `segments` by (vendor, firm) | merged @3317942ecc, complete @01960f5d08 |
| MP-pf-2 | the page: each bucket a segment, each assets/bd (vendor, firm) a sub-segment, `Data store` kind, a tool under every pair it serves | merged @7772bf7d1b, complete @747bea0554; mcportal `421f8fb` |
| MP-pf-3 | handler: reads the tool-level `serves` list (CTO ruling msg 34591) and accepts the `store` source kind | merged @54a75d46ba, complete @065926ab2b; admin suite 114 passed, 0 failed |

Push state (ls-remote read ~02:3xZ): workspace commits above are on origin `box/sitez` @569e4bb77e; mcportal origin `DEV` = `421f8fbe84`.
`python .tools/round-close-check.py --project NFRA_MCPORTAL --round 2` reads 19 orders, 16 complete, verdict=MAY-CLOSE (the 2 not complete,
MP-pd-7 and MP-pd-8, are PD's, held by CTO ruling msg 34212). Its strict-grade count reads judgment=0, so it does not count the MP-pf-2 AC2 below.

## THE JUDGMENT CRITERION FOR THE CVO

`MP-pf-2` AC2, in the order's words: legibility at 1280 px and 390 px, graded from the issuer's screenshots. The worker recorded it
UNVERIFIABLE-BY-INSTRUMENT with no verdict. Screenshots: `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/evidence_421f8fb/`
(`pf_1280.png` full page, `pf_1280_segment.png`, `pf_390_top.png`, `pf_390_segment.png`).

## The one real run (issuer, ~02:3xZ)

The checked-in fixture `gateway.cgroup.fixture.ts` rendered through the real `GatewayView` and the real CSS (`App.css`, `tokens.css`,
`gateway.css`) at mcportal `421f8fb`, served over localhost and loaded in a real browser at a true 390 px viewport (headless Edge floors at 477 px,
the cause of row Z-W33-S4). The script is `render_pf.tsx` beside the screenshots.

| reading | value |
|---|---|
| `scrollWidth` against `innerWidth` at 390 px | 390 against 390, no sideways page scroll |
| segment sub-sections present | 8 of 8 the fixture declares (7 under opal-data-assets, the last the unresolved pair; 1 under opal-data-bd) |
| scroll containers | 17, one per tools table |
| segment heading `overflow-wrap` | `normal` on all 8, so a heading breaks between words only |
| page title | black Lato 39 px, the DESIGN.md page-title value |

What a reader sees at 1280: a bordered card per segment, a bold `Vendor / Firm` heading, a count, one reason line under multi, none and
unresolved (the gap in red), an unwrapped table. At 390: the same cards; tables scroll inside their card (the Access column is cut at the
card edge until scrolled).

**What the run does not show:**
1. It is the FIXTURE, not the live catalog. The live page shows segments only after MCPINDEX's C-GROUP catalog release and the gateway release (OG-ap-23); until then it reads `Vendor not resolved / Firm not resolved` for every assets tool.
2. At 390 px the Indexes line breaks at a hyphen (`idx-` / `performance`): between hyphenated parts, not inside a word, but a reader may see it as a wrap. Not changed.
3. Nobody has looked at the live page in a browser as an owner; that look is Andrew's sitting.

## Rows touching this round

Every ARMED row with `disarm_owner` 2.0.0_SA_COO~MP on PE/PF has its disarm row: Z-S54 (Z-W32-S1), Z-S55 (Z-W32-S2), Z-S56 to Z-S59 (Z-W31-S1 to -S4),
Z-S60 (Z-W33-S7). `comp-surprise` still lists them armed because it does not join a `DISMISSED_WITH_REASON` row to the row it names in prose;
the join is by the id in each disarm row's text. The one armed row that is not mine is Z-S53 (disarm owner `0.0.0_AB_MSTR~Z`, site Z python).

## Open, for others

- `2.0.0_SA_COO~O`: the handler cells (MP-pe-1, pf-1, pf-3) ride its next code batch, OG-ap-23 (its msg 34637).
- Andrew (PE.6 item 3): regroup the integration channels by bucket as well? Unchanged; the page keeps them as their own group.
