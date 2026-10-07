# DSGN_AMGTV1 round 47 item 4 -- the FWD-21 read: an ellipsised label's full name is reachable by hover (2.0.0_SA_COO~D, 2026-10-07)

**Asked by:** `ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md` @43d2e5eb3c, ruling 5 and ROUND 47 item 4: on the 30D face, hovering
or focusing an ellipsised label shows the full name; ten labels end in an ellipsis; read all ten.

**Reading: 10 of 10 ellipsised labels on the 30D face carry the full name on hover.** Denominator: 57 bubble labels drawn, 10 shortened.

**Source, and its claim class:** this is the round-46 walk's own read, not a new run: `round35/walk/read-20261007T093016Z/02-fwd21-labels-30D.json`
@caf62c0308 (closewalk35.mjs, portal DEV 8ddfe409 on the live API, 2026-10-07 09:3xZ; window served 30 days ending 2026-10-06). MEASURED by that
instrument at that time; nothing was re-run for this file. The portal has not changed since (DEV is still 8ddfe409 by the round's base).

**What the instrument can and cannot see:** the hover carrier is the bubble's SVG <title> (a native tooltip; a headless PNG does not draw it). The read asserts the full name is in that title text for each
shortened label. It does NOT establish keyboard focus: an SVG title is a pointer tooltip, and no focus read was made. If the ruling's
"hover or focus" needs focus as well, that is a separate read or a page cell.

| key | label drawn | full name | full name in the hover |
|---|---|---|---|
| `AMD_US_Equity` | Advanced... | Advanced Micro Devices Inc | YES |
| `TSM_US_Equity` | Taiwan Semiconductor... | Taiwan Semiconductor Manufacturing Co Ltd | YES |
| `CDNS_US_Equity` | Cadence Des... | Cadence Design Sys Inc | YES |
| `HD_US_Equity` | The Home De... | The Home Depot Inc | YES |
| `MNST_US_Equity` | Monster... | Monster Beverage Corp | YES |
| `2317_TT_Equity` | Hon Hai... | Hon Hai Precision Industry | YES |
| `CELH_US_Equity` | Celsius Holdi... | Celsius Holdings Inc | YES |
| `8306_JP_Equity` | Mitsubishi... | Mitsubishi UFJ Financial Group | YES |
| `ISRG_US_Equity` | Intuiti... | Intuitive Surgical Inc | YES |
| `KMB_US_Equity` | Kimberly... | Kimberly-Clark Corp | YES |
