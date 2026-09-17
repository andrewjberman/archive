# DSGN_REBRND.TO-RB-s-6 -- result

**Worker:** `0.9.0_WK_DSGN_REBRND~1` (slot ~1, queue position 6) - **Cell:** `RB-s-6` - **Branch:** `wk-dsgn_rebrnd-1g`
in both repos (workspace start `7772585067`, portal start `845833fb`) - **Portal commit:** `23ff5e96`, LOCAL -
**Dev server:** 5186 (stopped before the report).

Every mechanical criterion (RB6-AC1..AC4) PASSES BY OUTPUT on the final committed bytes. RB6-AC5 and RB6-AC6 are
judgment criteria: recorded here with their evidence and NO verdict, graded by `3.0.0_SA_CVO` at L9.

## What changed (portal `23ff5e96`, 5 files, +80/-37)

| file | change |
|---|---|
| `src/index.css` | The blanket `outline: none !important` (every element, every pseudo-element, `:focus`, `:focus-visible` and `:focus-within`) is deleted. A new section 4.5 adds ONE unlayered `:focus-visible` rule: `box-shadow: 0 0 0 2px hsl(var(--bg-surface)), 0 0 0 4px hsl(var(--semantic-action-primary))`, the band variant `0 0 0 2px hsl(var(--palette-darkField)), 0 0 0 4px hsl(var(--palette-white))` for `.dark-band` and its descendants, `outline: 2px solid transparent` so forced-colors still shows focus, and `transition: none !important` on the ring under `prefers-reduced-motion: reduce`. |
| `src/App.tsx` | Active nav item: `bg-[hsl(var(--primary))] text-white shadow-md` becomes `font-bold text-[hsl(var(--palette-white))] border-l-2 border-[hsl(var(--palette-white))]`, which is weight and rule in band ink with no fill and no shadow. The idle branch takes `font-medium` (moved out of the base string, otherwise the weight does not land) plus `border-l-2 border-transparent`. Avatar: accent fill becomes an outlined circle (`border-[hsl(var(--palette-mediumGray))]`, band-ink letter). Row W1-S26. |
| `src/ui/components/panels/README.md` :5-12 | Comment: the light canvas `#F4F6FA`, `portal/DESIGN.md` C3 as the law, the 2026-09-11 ruling superseding the 2026-07-15 archetype. |
| `src/pages/TicketCenter/TicketCenter.tsx` :11-17 | The same, in the header comment. |
| `src/lib/designTokens.ts` :8-16 and :40-42 | The same, in two comments. |

The comment edits change no code: 33 of 33 changed lines in `TicketCenter.tsx` and `designTokens.ts` are comment lines
(diff read, 0 non-comment), and `README.md` is prose.

**Where the ring comes from.** The order says to use "the ring token RB-s-1 defines", but no such token exists (row
W1-S22). The ring is the one `portal/DESIGN.md` C11 ratifies, and it is composed from tokens that already exist. It is
unlayered so that it outranks the 121 Tailwind focus utilities (`focus:outline-none`, `focus:ring-*`) in 66 files that
live in the utilities layer; without that, each would keep its own local ring.

## Criteria, as run on the final bytes

| id | invocation | deciding output | denominator |
|---|---|---|---|
| RB6-AC1 | `cd <WS>/portal && timeout 120 bun run typecheck; echo rc=$?` | `$ tsc -b --noEmit` / `rc=0` | 1 of 1 typecheck project |
| RB6-AC2 | the order's python census of `outline:\s*none\s*!important` | `OUTLINE-NONE-IMPORTANT: 0` / `VERDICT: FOCUS-RESTORED` | 1 stylesheet; read 1 at issuance |
| RB6-AC3 | the order's python census of `:focus-visible` blocks that paint | `FOCUS-VISIBLE-SELECTORS: 6 THAT-PAINT-A-RING: 2` / `VERDICT: RING-WIRED` | 6 textual occurrences (3 in comments), 2 painting rules (light and band) |
| RB6-AC4 | `node scripts/ui-smoke.mjs market .../rb-s-6_market_1440.png --port 5186` | `LOC : /market` / `CANVAS: rgb(244, 246, 250)` / `rc=0` | 1 route at 1440x900; PNG read |

RB6-AC4's PNG, read: the canvas is light, the shell's active item (Market Overview) is a band-ink left rule with no
fill, the avatar is outlined, and the panels are unchanged from RB-s-5. Two panels were still loading at capture.

## The second folded act: shell accent, before and after

Measured by the walk script's DOM enumeration (every visible element inside `<aside>` whose computed
`background-color` is `rgb(95, 59, 227)`), on the untouched base and on the final tree:

| route | before (portal 845833fb) | after (portal 23ff5e96 bytes) |
|---|---|---|
| /market | SHELL-ACCENT-FILL: 2 (a "Market Overview", div "D") | SHELL-ACCENT-FILL: 0 |
| /positioning | SHELL-ACCENT-FILL: 2 (a "Positioning", div "D") | SHELL-ACCENT-FILL: 0 |
| /portfolio-management | SHELL-ACCENT-FILL: 2 (a "Portfolio Management", div "D") | SHELL-ACCENT-FILL: 0 |

After the edit, SHELL-ACCENT-ANY (fill, own text, border or box-shadow in the accent) also reads 0 on all three. The
active item computes `fontWeight 700`, `borderLeft 2px solid rgb(230, 234, 244)`, a transparent background and
`boxShadow none` (logs `rb-s-6_walk_kbd.log`, `rb-s-6_walk_kbd24.log`). The `/positioning` capture was read
(`rb-s-6_final_positioning_full.png`): no accent anywhere in the shell, the active item marked by rule and weight, the
avatar outlined.

## The first folded act: the comment census

Row W2-S15 is not in the channel (row W1-S23), so its census could not be re-run. This census stands in for it:
case-insensitive `silver|81%|222 24%` over the three named files.

| vintage | hit lines |
|---|---|
| portal 845833fb (git show) | 7 -- README.md:5, :6; TicketCenter.tsx:11, :171; designTokens.ts:10, :40, :42 |
| after (23ff5e96 bytes) | 1 -- TicketCenter.tsx:174, a FIFTH comment outside the four named (row W1-S24, not edited) |

Inside the four named comment blocks: 0.

## RB6-AC5 (judgment) -- the keyboard walk, RECORDED

Instrument: `rb-s-6_focus-walk.mjs`, headless Edge via playwright-core with the ui-smoke auth stub. It presses Tab
until the focus order wraps, reads the focused element's `:focus-visible` match and its computed `box-shadow` at every
stop, and screenshots a clip at every stop. `rb-s-6_contact-sheet.py` tiles the clips into one sheet per route. Then it
performs one real `page.mouse.click` on a non-text control and one on a text field where one exists.
`prefers-reduced-motion: reduce` is emulated, so the clip shows the settled ring.

| walk | routes | Tab stops | ring painted | ring at full 4px | mouse click, non-text control | mouse click, text field |
|---|---|---|---|---|---|---|
| three routes, 16px | 3 | 107 (every tab order wrapped) | 107 | 107 | 3 of 3 no ring | none found |
| RB-s-12 inventory, 16px | 18 | 355 (every tab order wrapped) | 355 | 355 | 12 of 12 no ring | 7 of 7 RING (row W1-S28) |
| base tree (control), 16px | 3 | 87 | 1 (Upload Portfolio's own shadow, not a focus ring) | 0 | -- | -- |

Ring kinds on the three routes: /market 22 light-ground plus 20 band; /positioning 21 plus 17; /portfolio-management 23
plus 4. All 54 shell stops paint the light-ground ring, because the sidebar is not `.dark-band` (row W1-S27). The inventory
routes are the 18 other routes that carry a `keyboard_obligation: true` row in `design/brand/portal-surface-inventory.json`
(21 routes in all), walked in their default state without fixtures. Where the visible-focusable count exceeds the stops
walked (/investor-reporting 32 vs 27, /trade-submission 34 vs 22), some focusables are not in the tab order. The walk
records the gap and does not judge it.

Sheets: `rb-s-6_sheet_kbd_<route>.png` (3), `rb-s-6_sheet_kbdinv2_<route>.png` (18), `rb-s-6_sheet_base_<route>.png` (3).
Read: `rb-s-6_sheet_kbd_positioning.png` shows the white-gap indigo ring on the sidebar and the header flip, the band
ring on the panel controls, and no ring after the mouse click on UST. Stop #1, the logo toggle at x=0, has its ring cut
off by the viewport edge.

`prefers-reduced-motion`, measured as a pair: with reduce, 42 of 42 /market stops show the full 4px ring 140 ms after
Tab. Without it (`rb-s-6_walk_motion.log`, `rb-s-6_sheet_motion_market.png`) only 20 of 42 do, because the controls'
`transition-all` animates the ring in (for example `rgba(95, 59, 227, 0.776) ... 3.10393px`).

## RB6-AC6 (judgment) -- raised browser default font size, RECORDED

The same walk with the BROWSER DEFAULT font size raised to 24px through CDP `Page.setFontSizes`, the setting the
browser's font-size preference drives. Positive control: `ROOT-FONT 24px BODY-FONT 24px` against `16px` in the normal walk.

| route | Tab stops | ring painted at full 4px | shell accent | horizontal overflow |
|---|---|---|---|---|
| /market | 42 (wrapped) | 42 | 0 | none (doc scroll width 1440) |
| /positioning | 38 (wrapped) | 38 | 0 | none |
| /portfolio-management | 27 (wrapped) | 27 | 0 | none |

Captures: `rb-s-6_font24_<route>_full.png` and `rb-s-6_sheet_kbd24_<route>.png`. Read (/positioning): the page title,
body copy and the sidebar grow with the root, the sidebar's nav list scrolls rather than overflowing, and much of the
panel type (headers, segmented labels, table text) stays near its 16px-root size. That type does not scale with the
default, which is what III.9 asks about. It is recorded here for L9, not judged.

## Surprise rows filed (all UNDER_INVESTIGATION)

- `DSGN_REBRND-W1-S22` OBSERVATION/INERT: no ring token from RB-s-1; the ring is DESIGN.md C11's.
- `DSGN_REBRND-W1-S23` OBSERVATION/INERT: row W2-S15, cited by the order, is not in the channel.
- `DSGN_REBRND-W1-S24` OBSERVATION/ARMED, disarm `2.0.0_SA_COO~D`: TicketCenter.tsx:174 still says "the silver canvas".
- `DSGN_REBRND-W1-S25` OBSERVATION/INERT: the band ring renders #E6EAF4, not #E8ECF5 (token rounding).
- `DSGN_REBRND-W1-S26` OBSERVATION/INERT: four App.tsx lines, not two, so the weight lands.
- `DSGN_REBRND-W1-S27` OBSERVATION/INERT: the #0A1733 sidebar takes the light-ground ring.
- `DSGN_REBRND-W1-S28` OBSERVATION/INERT: a click into a text field paints the ring.

## Not done, and why

- `TicketCenter.tsx:174` (row W1-S24), because the order names four comments.
- `.dark-band` on the sidebar (row W1-S27), because it would be a further App.tsx class edit with side effects.
- The sidebar's `--primary` border-image gradient (App.tsx:261), because it is not one of the two named class edits.
- A global reduced-motion rule for every transition, because the order asks the ring to respect the preference and the
  empty-state shimmer is RB-s-10's.
- No push, merge, rebase, `checkout --` or `clean` in either repo, and the workspace `portal` gitlink is not bumped
  (not in `<paths>`).
