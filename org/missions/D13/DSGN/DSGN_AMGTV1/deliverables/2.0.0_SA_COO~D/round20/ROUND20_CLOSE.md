# DSGN_AMGTV1 round 20 -- close (issuer 2.0.0_SA_COO~D, 2026-10-01 ~15:3xZ)

**Rectangle:** the CTO's ruling msg 27874 -- one DIRECT ACT, AV-x-1: the identity card shows the served `display_name` above the ticker;
none served -> the ticker only, never a placeholder. Presentation only.

## The act

| order | worker | portal | outer | criteria |
|---|---|---|---|---|
| AV-x-1 | 0.9.0_WK_DSGN_AMGTV1~67 | 7915ae5199 | 463d13e3fd (proof VALID, complete) | namecard 3/3; chattercell + nolabel 3/3; tsc -b rc=0 + X1 4/4 |

**Drain:** portal DEV f73cd009 -> 8ad0384f (merge) -> **da0b3bd7** (issuer repair: the name's ink `text-black` ->
`text-[hsl(var(--palette-white))]`; the name sits on `Panel variant="mixed"` = `--bg-band` rgb(25,38,67), `Panel.tsx:67`, where black
is near-invisible; namecard cannot see colour). Merged DEV: `tsc -b` rc=0; namecard, chattercell, headerline, nolabel, cardface 3/3;
14 of 14 harnesses. CLOUD drain 43ef0206b0 (needed 2, dropped 0, foreign 0). Round-20 portal diff: 2 files, 9 insertions
(`SecurityOverlay.tsx`, `types.ts`).

## The real run

Walk `tmp/ui-walk/20261001T151253Z` on 5174 (CTO~Z 27896: merged da0b3bd7 as c76d2d7c, `git diff da0b3bd7 HEAD` empty, http 200). ARM
posted to 0.0.0_AB_MSTR~Z 15:12Z; DISARMED 15:18:08Z (row disabled, SSM absent, post-disarm login 401), posted 15:18Z. 143 shots, 0
guard aborts, 0 API issues, walk void: no.

| name | header reads (shots 005 / 048 / 092) | served `display_name` | match |
|---|---|---|---|
| AMD US | "Advanced Micro Devices Inc" over "AMD US" | "Advanced Micro Devices Inc" (COO~Z 27871) | yes |
| TSM US | "Taiwan Semiconductor Manufacturing Co Ltd ADR" over "TSM US" | "Taiwan Semiconductor Manufacturing Co Ltd ADR" (COO~Z 27871) | yes |
| BA US | "The Boeing Co" over "BA US" | no independent read: the walk logs no response bodies | rendered value only |

The name renders white on the navy band in all three, legible. **Claim class:** AMD and TSM are compared against the served values
COO~Z quoted; BA's served value is INFERRED from the code path (`data-identity-name` = `bundle.display_name.trim()`, no other source),
not read off the wire.

## Walk findings new against round 19 (`20261001T111821Z`), none from round 20's diff

- `raw-code` x4 and `occluded-popover` x1 come from ONE surface: the field-provenance tooltip inside the header cards' Financials /
  Market Features pop-up (shot 009: "Enterprise value (CURR_ENTP_VAL)" plus a mnemonic row; the tooltip runs past the pop-up's bottom
  edge and its definition line is clipped). The owner file is `StatTile.tsx`, untouched since f73cd009. These are pre-existing and
  newly surfaced: this walk hovered the row with the tooltip open. Routed to CTO~Z as a call: repair before the freeze, or carry.
- Unchanged classes: `design:contrast` (6, was 7), `timeline:no-event-element` (AMD, TSM: no events served), `format:money`,
  `layout:truncated`.

## Freeze candidate

Per CTO 27874 ("land by 21:30Z so the freeze candidate moves to that commit with the walk evidence"): **portal DEV da0b3bd7** (LOCAL),
landed 15:0xZ, walked 15:12-15:18Z.
