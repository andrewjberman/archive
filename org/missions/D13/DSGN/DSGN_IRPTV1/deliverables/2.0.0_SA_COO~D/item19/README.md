# DSGN_IRPTV1 FAST item 19 -- Positioning renders unchanged after the tree map extraction (CTO ruling 102510)

Portal: `ee949234` on origin DEV (extraction), on `5ff990dc` (item 18).

| File | What | sha256 |
|---|---|---|
| before-positioning.png | `/positioning` on 5174, portal at `5ff990dc` (before item 19) | b9768b7ff48218044d9a445351f6067f2bec5da808be9ccb7175fee55a59f22f |
| after-positioning.png | the same shot, working tree = `ee949234` | b9768b7ff48218044d9a445351f6067f2bec5da808be9ccb7175fee55a59f22f |
| control-positioning.png | the after tree with one INT holding (IEFA) removed from the fixture | 6b3c0f88570ca85d8c62785a3a31beaf6c14706413ca54101e871d273dc4bfc6 |

- **Result:** the before and after files are byte-identical, and the full-page PIL diff bbox is None at 1440x2133.
- **Control:** the control differs at bbox (111, 670, 1377, 2037). The instrument can therefore see a one-holding change in the map and the table.
- **Recipe:** `node scripts/ui-smoke.mjs positioning <out.png> --port 5174 --fixtures <fixtures.json>`. The fixtures are the served `json/positioning/positioning_data.json` and `holdings_attribution_data.json`, read from `s3://opal-data-portal-v2` (read-only, gunzipped) and keyed by URL substring. Result: FIXTURES-MATCH 2 of 2.
- **Not covered:**
  - The hover tooltip, which a static shot cannot show. It was moved verbatim.
  - IR's live Securities map. The cottonwood probe driver's selection flow no longer matches the page.
