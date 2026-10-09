# MDPF_STRATID FWD-1 -- the seat walk of the portal's Global view (round 2, workstream 1)

Walked by `2.0.0_SA_COO~S1` on 2026-10-09 at 15:48Z, under R1 of the CTO's round-1 analysis
(`ledger/ROUND_ANALYSIS.round1.md` @88e5ab7203, msg 2684). This follows the DSGN FWD-1 pattern from the CTO fold of UB-1152.
`3.0.0_SA_CVO` grades it at L9. R3 (the key-family read of msg 2501) was already printed in `L4_READ_20261009.md`
section "CTO ruling and the reads it asked for" at ~13:5xZ, so no act is owed for R3.

## The walk

- **Instrument:** `/ui-walk` (`node .claude/skills/ui-walk/walk.mjs --route /portfolios --press "SMAs"`).
- **Account:** the walker service account, signed in, armed and disarmed by the walker itself.
  - Holder `DESKTOP-HK1UU7N:20408:f572d654`.
  - Disarm at 15:49:19Z; a login with the walk password then answers HTTP 401, so the account is REFUSED again.
- **Build:** the local dev build on `localhost:5174`, portal `DEV` @2726bbe7, against the real backend through CloudFront.
- **Result:** walk void: no; 0 guard aborts.
- **Output:** `tmp/ui-walk/20261009T154815Z/` (gitignored; client data stays local).
- **Steps read:** `001--portfolios-load` and `002--portfolios-press-SMAs`. The SMA dialog was opened on the default partner,
  Global (All), before the walker's partner loop ran.

## What a person sees, beside the served artifact

The served artifact is `s3://opal-data-assets/portal/gold/mdpf/global/category-views/2026-10-08.json`:
- VersionId `eCS4t0TeU6U0VhQoZAY2LUOGvBYTs9Jq`;
- LastModified 2026-10-09T13:31:41Z, the 13:30Z scheduled fire.

| Page (Global (All), "October 8th, 2026, 5:00p ET") | Shown | Served value | Agrees |
|---|---|---|---|
| Total Assets | $2.15B | `sums.total_aua` 2,147,378,054.74 | yes |
| Models card | $1.83B | `nodes.Models` 1,828,584,618.67 | yes |
| SMAs card / dialog header | $50.28M | `nodes.SMA` 50,276,849.33 | yes |
| Client card | $268.52M | `nodes.Client` 268,516,586.73 | yes |
| SMAs > ALT Strategies > Tax-Managed SMA | $28.81M | 28,812,392.51 | yes |
| **SMAs > ETF Strategies** | **$21.46M** | 21,464,456.82 | yes |
| ETF Strategies > Dividend SMA | $17.08M | 17,079,326.24 | yes |
| ETF Strategies > Opal Equity Growth SMA | $3.97M | 3,974,709.60 | yes |
| **ETF Strategies > PFDE** | **$410K** | **410,420.98** (= Cottonwood served PFDE, `L4_READ_20261009.md` C) | yes |

The page prints figures rounded; the to-the-cent figure is the served one. The fourth ETF Strategies member serves `None` and is
not drawn, so the page shows 3 members.

- **Dialog source line:** "Source: SMArtX Advisory Solutions, SS&C Black Diamond Wealth Solutions, Orion Portfolio Solutions".
- **PFDE under Client:** 0 times (`L4_READ_20261009.md` D2). The Client card is unchanged at the served value.

## Not graded here

- FWD-1's grade is `3.0.0_SA_CVO`'s, at L9.
- Walker check hits (2 per step, the same on every route) are development pointers, not findings for this outcome. They are left
  in `findings.json`.
