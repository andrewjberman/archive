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

## `white/N` OVERLAY CENSUS -- baseline, portal DEV ac3b018e (2026-10-06 ~04:4xZ)

Instrument: `scripts/overlay-census.mjs` (read-only, regex; `--json`, `--files`). It counts translucent-white BACKGROUNDS only (`bg-white/N`, `bg-[rgba(255,255,255,a)]`, inline `backgroundColor: 'rgba(255,255,255,a)'`; `hover:`/`focus:`/`active:`/`group-hover:` variants; `odd:`/`even:` zebra rows); `text-white/N`, `border-white/N`, `ring-white/N` are inks and rules, not counted.

- **DENOMINATOR:** 596 .ts/.tsx/.css files under `src/` (tests, harnesses, the vendored catalyst kit excluded; the same floor as the FWD-3 census).
- **COUNT:** 580 overlay backgrounds in 117 files: REST 387, HOVER 187, ODD 6.
- **By alpha (REST):** /5 161, /10 143, /50 28, /30 12, [.04] 9, [.02] 8, /15 7, /20 6, the rest singletons. **HOVER:** /10 106, /5 46, /20 16, /15 13, /8 5.
- **Largest files:** DistributionTab 35, AdvisorPublicProfile 19, PartnerAnalytics 19, StylePolicyComparison 17, `lib/designTokens.ts` 16, AdvisorsTab 15, ClientsTab 14.

**What this is and is not.** It is the baseline the PROOF asks to re-run per delivered page: the number of surfaces that still separate themselves by a translucent overlay. It does NOT map any overlay to a rung (FWD-12 is delivered page by page) and does not say which overlays are a SEPARATION (a tile on a panel) as against a hover or a decoration; REST /5 and /10 are the likely tile and inset washes, HOVER is FWD-13's. Instrument limit: a class assembled at runtime (`` `bg-white/${n}` ``) is not seen. **Not done:** the container-token census (each token's resolved role) and any before/after render (no render this seat; port 5174 is Andrew's F1 run).

## CONTAINER-TOKEN CENSUS -- portal DEV 79bad192 (2026-10-06 ~04:5xZ)

Instrument: `node scripts/layer-table.mjs --containers` (read-only). **DENOMINATOR:** 24 tokens whose names match `bg|layer|card|panel|surface|container|state-hover|state-selected` declared in `src/index.css` plus the root theme (`card-foreground` excluded as an ink); consumers = `var(--token)` occurrences over 597 src files. 0 tokens unresolved.

**Heaviest use:** `--bg-header` 408 var() uses (the section strip), `--bg-card` 31, `--state-hover-band` 24, `--layer-tile` 22, `--bg-page` 16. Zero uses: `--bg-medium-alt`, `--bg-tooltip-alt`, `--card`.

**Values shared by two or more tokens, BAND world (the finding the PROOF asks for):**
- Same role, legacy alias of the named layer (no defect): `--bg-header = --layer-strip = --bg-dark` #0A1733; `--bg-card = --layer-body` #192643; `--bg-medium = --bg-medium-alt = --layer-tile` #253456; `--bg-tooltip = --bg-tooltip-alt = --layer-tooltip` #081126; `--layer-hover = --state-hover-band` #2F426A; `--layer-selected = --state-selected-band` #344C7F; `--bg-page = --bg-band` #0B111D.
- **NEIGHBOURING ROLES sharing a value: `--bg-hover-light` (a hover) = `--bg-surface` (a panel body) = `--card`, all #1E2D4D.** A hover that resolves to the surface it sits on is invisible; `--bg-hover-light` has 2 var() uses, `--bg-surface` 13: those 2 sites need a look. This is the one real violation of "zero neighbouring roles sharing a value" the census found.

**LIGHT world: not measurable by this instrument for most tokens.** A token declared once (the root default is the dark/band value) reads identically in both columns, so the "light" column for `--bg-header`, `--bg-card`, `--layer-*` is the band value, not a light-world rung. Only `--bg-page` (#F4F6FA) and `--bg-surface` (#FFFFFF) carry a light declaration; `--layer-light-strip` and `--layer-light-tile` do not exist (printed MISSING by the table above). So the PRD's "each role has an opaque rung in the light world" is NOT met for strip, tile, hover or selected: the light world has 2 of its 6 roles. That is the defect list FWD-12 still owes.
