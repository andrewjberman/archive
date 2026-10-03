# CUT_NAMES -- AMGT-ao-1 (round 65), worker 0.9.0_WK_AMGT_RESAPP~216, measured 2026-10-03

## The width
The identity crosswalk's `record["identity"]["name"]` (Bloomberg identity bronze, `source` field of each record) is
cut at **28 characters**. Measured over the served crosswalk (`crosswalk.load_crosswalk()`): 237 records, 67 carry an
`identity.name`; **7 of 67 are exactly 28 wide** and no name is wider (widths seen: ... 22 x6, 23 x2, 24 x2, 25 x3, 27 x1, 28 x7).

## The count served at the width
The two routes serve 95 distinct security keys (price 94, chatter 95). Of the 7 width-28 crosswalk names, all 7 keys are
served; **4 are served from the crosswalk** (8306_JP, 8316_JP, AMXB_MM, BATS_LN), 3 are served from the classifications
table instead (OMAB_MM, ICT_PM, UNVGY_US) and already read a full name there. Model-block header names (a second Bloomberg
28-wide source) add 5 more served keys at width 28 or beyond (see residue).

## Each cut name, its full name, its source
Declared in `scoped_amgt.DISPLAY_NAME_CUT_FULL` (keyed by the cut string, applied at the seam `_clean_display_name`).

| Cut name (28 wide) | Served now | Source of the full name |
|---|---|---|
| MITSUBISHI UFJ FINANCIAL GRO | Mitsubishi UFJ Financial Group | `org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round33/securities.universe.r33.json`, key `8306_JP_Equity`, `company`; also crosswalk `source_row.folder` 'Mitsubishi UFJ Financial Group 8306 JP' (registrations.json) |
| SUMITOMO MITSUI FINANCIAL GR | Sumitomo Mitsui Financial Group | same file, key `8316_JP_Equity`, `company`; crosswalk `source_row.folder` 'Sumitomo Mitsui Financial Group 8316 JP' |
| AMERICA MOVIL SAB DE C-SER B | America Movil SAB de CV | same file, key `AMX_US_Equity` (same issuer's ADR line), `company` 'America Movil SAB de CV' |
| GRUPO AEROPORTUARIO DEL CENT | Grupo Aeroportuario del Centro Norte SAB de CV | classifications table `name` for ticker OMAB (what the key serves today via the classification limb; the universe file's 'Grupo Aeroportuario del Centro' is shorter and not used) |
| UNIVERSAL MUSIC GRO-UNSP ADR | Universal Music Group NV | classifications table `name` for ticker UNVGY (what the key serves today via the classification limb) |

Not cut, served as the estate holds it: BRITISH AMERICAN TOBACCO PLC (28 wide, but a complete name: folder 'British
American Tobacco' is shorter, no longer name exists) -> 'British American Tobacco PLC'; INTL CONTAINER TERM SVCS INC
(complete Bloomberg abbreviation; the key serves the classification name).

Cut-name count: **5 declared** (3 reach the routes through the crosswalk/model-block limb, 2 are shadowed by the
classification limb), against a denominator of 7 width-28 crosswalk names / 67 named crosswalk records.

## Residue (cut or doubtful, NO estate source for a longer name, left as the producer serves it, title-cased only)
- `ST_SP_Equity` 'SINGAPORE TELECOMMUNICATIONS' (28, model-block header; no estate name for the 'ST SP' line -- the only
  hit, data/inf/config/ticker_lookup.json 'Singapore Telecommunications Ltd Spons ADR', is the SGAPY ADR, not this key) -> 'Singapore Telecommunications'.
- `ROG_SW_Equity` 'ROCHE HOLDING AG-GENUSSCHEIN' (28, model-block header; a complete Bloomberg name) -> 'Roche Holding AG' (the '-GENUSSCHEIN' share-type tail is dropped by the all-caps tail rule, not by a name map).
- Model-block headers PBR_US, BABA_US, NU_US, UNVGY_US, OMAB_MM, ICT_PM also read 28 wide; their served name comes from the classification limb (PBR, NU, UNVGY, OMAB, ICT) or the all-caps tail rule (BABA -> 'Alibaba Group Holding').
- `HON HAI PRECISION INDUSTRY` (26, model-block header; probably 'Hon Hai Precision Industry Co Ltd') -- no estate source read, left as is.
