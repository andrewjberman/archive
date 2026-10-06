# FWD-12 layer table -- measured at portal DEV b0db73d1 (2026-10-06, 2.0.0_SA_COO~D, R4-4 first act)

PRD FWD-12 PROOF: "the role table printed with each role's two rungs and each neighbouring pair's separation ratio in both worlds (denominator = neighbouring
pairs, printed)". This is the measurement; it changes no token. Instrument: `node scripts/layer-table.mjs` (portal `b0db73d1`).

## What was measured

BAND world (`body { --layer-* }`, index.css; 6 roles, 5 neighbouring pairs, 5 measured):

| role | token | value | pair to the next role |
|---|---|---|---|
| tooltip (a navy rung is declared; the product's tooltip takes the accent) | `--layer-tooltip` | #081126 | 1.06:1 to strip |
| section strip, column header | `--layer-strip` | #0A1733 | 1.18:1 to body |
| panel body, modal body, data rows | `--layer-body` | #192643 | 1.22:1 to tile |
| tile, key card, group row | `--layer-tile` | #253456 | 1.24:1 to hover |
| hover | `--layer-hover` | #2F426A | 1.18:1 to selected |
| selected | `--layer-selected` | #344C7F | -- |

LIGHT world (root defaults; 6 roles named from the PRD's list, 5 pairs, 2 measured):

| role | token | value | pair to the next role |
|---|---|---|---|
| page | `--bg-page` (= `--palette-canvas`) | #F4F6FA | 1.08:1 to panel |
| panel body | `--bg-surface` | #FFFFFF | **UNMEASURABLE** (no light strip token) |
| section strip | `layer-light-strip` | **MISSING** | UNMEASURABLE |
| tile / inset | `layer-light-tile` | **MISSING** | UNMEASURABLE |
| hover | `--state-hover-light` | #E6EBF4 | 1.16:1 to selected |
| selected | `--state-selected-light` | #D3DBEE | -- |

## What it says

- **DENOMINATOR: band 5 of 5 pairs measured; light 2 of 5 measured.** Three light-world pairs cannot be measured because two roles have no declared rung.
- **The band pairs are 1.06 to 1.24:1; they are not one ratio.** The PRD's DONE WHEN says "neighbouring roles are separated by the same ratio in both worlds,
  under one opacity". The band world's own five pairs differ from each other by 0.18; the two measured light pairs (1.08, 1.16) differ from the band's.
  Whether "the same ratio" means equal ratios or the same rule is a reading for `1.0.0_SA_CTO`; the numbers are here either way.
- **"MISSING" is a statement about token names, not about the product.** The light strip and tile were named from the PRD's role list. A light page's
  title strip is today the dark band (a deliberate inverted band, the canvas ruling), so the light-world strip may legitimately be the band world's strip. That is a
  design question, not a measurement; it is not answered here.
- **The tooltip rung is declared but not used for the tooltip** (the product's tooltip is the accent, Andrew-direct 2026-09-14 ~19:0xZ); the 1.06:1 pair
  (tooltip to strip) is therefore a pair on paper only.

## An instrument error, kept in the record

A first run read `--bg-page` as #0B111D and `--bg-surface` as #1E2D4D (the band), because the reader took the LAST declaration of each name and the last ones are
the dark-theme overrides. The light world reads the FIRST (root) declaration and the band the last; the script states this. The wrong first numbers were not used.

## Not done

No token was added or changed. The container-token census and the `white/N` overlay census (the rest of FWD-12's PROOF) are not run; the latter is the
`state-census.mjs` `hover:bg-translucent` row for hover and has no equivalent for non-hover overlays yet.

-- 2.0.0_SA_COO~D
