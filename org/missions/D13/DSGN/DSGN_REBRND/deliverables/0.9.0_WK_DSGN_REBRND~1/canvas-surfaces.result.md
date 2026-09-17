# DSGN_REBRND.TO-RB-s-3 -- result (0.9.0_WK_DSGN_REBRND~1)

**Cell `RB-s-3`: canvas and surfaces.** Seven criteria: **five mechanical, all PASS by output**;
two (`RB3-AC6`, `RB3-AC7`) judgment, RECORDED with no verdict for `3.0.0_SA_CVO` at L9.
`<status>` flipped to `complete`.

- Portal commit **f46befb2bd3dbba836d3d0e83824d01ab5617341** (43 files, +487 / -253). LOCAL on
  `wk-dsgn_rebrnd-1d`. Never pushed.
- Workspace commit **cf9aabf452dc0ad937a771f676ce182722d49f49** -- channel rows `W1-S9..S11`.
- Proof of spec: `proof-of-spec-check.py` run from inside `<WS>` with the worktree's own copy:
  **rc=0 (VALID)**, read directly rather than through a pipe.

## THE ONE-LINE ANSWER

The contradiction is resolved **in kind but not in proportion.** The page is now a light canvas
with deliberate inverted bands, one container level deep, navy used as ink; it is not yet the
measured 56-67% canvas, because 4,887 light-on-dark idioms live in 171 page files this cell cannot
edit. That ceiling is `DSGN_REBRND-W1-S9`, BLOCKING, and it is the single most useful thing to read
here.

---

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| RB3-AC1 | PASS-by-output | `rc=0` | 1 of 1 project, 0 diagnostics over 43 touched files |
| RB3-AC2 | PASS-by-output | `LOC /market`, `CANVAS: rgb(244, 246, 250)`, real TEXT | 3 of 3 printed lines read, not the rc |
| RB3-AC3 | PASS-by-output | `LOC /positioning`, `CANVAS: rgb(244, 246, 250)`, real TEXT | 3 of 3 printed lines read |
| RB3-AC4 | PASS-by-output | `COLOR-SCHEME: light` / `FOLLOWS-CANVAS` | 1 of 2 declarations is the default this grades |
| RB3-AC5 | PASS-by-output | `RADII: ['2px','3px','4px','720px','50%']` / `SHARP` | 5 of 5 tokens in band + 102 utility tokens swept |
| RB3-AC6 | RECORDED (judgment) | see below -- NO VERDICT | 449 of 449 band instances enumerated |
| RB3-AC7 | RECORDED (judgment) | see the table below -- NO VERDICT | 40 pairs graded, 33 pass, 7 enumerated |

`rc=0` is deliberately **not** cited as the evidence for AC2/AC3: a blank page returns `rc=0` too.
The canvas value is the discriminator, and it moved `rgb(195,202,218)` → `rgb(245,246,250)` →
`rgb(244,246,250)` as the tokens changed, which is what makes it usable.

---

## WHAT CHANGED

| | before | after |
|---|---|---|
| canvas | `#C3CADA` (mid-silver, 81% L) | `#F4F6FA`, printed exactly as `rgb(244,246,250)` |
| container surfaces | three navy tiers (11% / 17% / 25% L) | **two states**: `#FFFFFF` + `#C4CBDB` hairline, or a `#0A1733` band |
| navy `#163372` | dominant panel fill | ink and hairline only; fills nothing |
| radius | `--radius: 0.5rem` (8px) | `2px / 3px / 4px` + `720px` pill + `50%` circle |
| elevation | `shadow-lg` on every Panel | none in the swept scope |
| `color-scheme` | `dark` on a light page | `light`, with `html.dark-mode` carrying its own |
| light-mode semantics | read `darkMode.palette` in 2 slots | 0 cross-references; dark values scoped to `.dark-mode` |

**Exact canvas.** The integer HSL triplet rendered `#F4F6FA` as `rgb(245,246,250)` — one unit out in
red. The palette tokens now carry lossless fractional HSL (`220 37.5% 96.86%`), verified by
round-tripping all five fixed brand values back to their exact bytes before applying.

---

## THE ENUMERATED BANDS (RB3-AC6)

Every inverted band, by the surface that produces it. **449 instances.**

| producing surface | occurrences | files |
|---|---|---|
| `Panel variant="chart"` / `"mixed"` (primitive) | 144 | 71 |
| page-level `bg-[hsl(var(--bg-header))]` | 202 | 68 |
| page-level `bg-[hsl(var(--semantic-background-contentPanel))]` | 66 | 12 |
| page-level `bg-[hsl(var(--bg-card))]` | 28 | 21 |
| `NestedCard` (primitive) | 8 | 3 |
| `DarkCard` (primitive) | 1 | 1 |

**The reason is one reason, and it is the same for all of them:** the content inside these
containers is authored light-on-dark in `portal/src/pages/` — 4,887 `text-white` / `text-white/N` /
`bg-white/N` / `border-white/N` idioms across 171 files — and `Panel`'s own pre-existing contract
states it: *"White-text idiom is legal inside. (Case A)"*. Turning these white without repainting
that text **in the same act** makes it invisible, and `portal/src/pages/**` is not in this cell's
`<paths>`. A band that cannot state why it is inverted is not a band; this one can.

---

## THE CONTRAST TABLE (RB3-AC7)

Measured by walking the rendered DOM of both routes in both modes, compositing each text node's
colour against its **effective** background, and grading against WCAG 2.1 SC 1.4.3.

| context | pairs | pass | fail |
|---|---|---|---|
| `/market` LIGHT (default) | 9 | **9** | 0 |
| `/positioning` LIGHT (default) | 9 | 8 | 1 |
| `/market` DARK (selected) | 12 | 9 | 3 |
| `/positioning` DARK (selected) | 10 | 7 | 3 |
| **TOTAL** | **40** | **33** | **7** |

**Every failure, named:**

| ratio | bar | pair | owner |
|---|---|---|---|
| 2.54:1 | 4.5 | `#ffffff` on `#10b981` — the "INT" model chip (both modes) | a DATA colour in a page file; out of grant, and *charts keep their colour* forbids darkening it |
| 4.27–4.39:1 | 4.5 | accent-on-band and white-on-accent, DARK mode only (3 pairs) | **structurally impossible**, see below — R5's decision |

**The three repairs the sweep found and forced** (this is why it was run at each stage, not once at
the end):

1. **Navy ink inherited INTO bands at 1.48:1** — with `--foreground` now navy, anything in a band
   with no explicit colour class went navy-on-near-black. A band now declares its own ink **once**
   (`.dark-band`) instead of 4,887 call sites remembering.
2. **The brand-derived status family at 3.06:1 / 3.54:1 on a band** — it was tuned for the light
   canvas. Inside a band it keeps its hues and takes a lighter step: success 7.92:1, danger 5.4:1,
   warning 6.23:1, info 6.1:1 on `#0A1733`.
3. **My own fix for (1) was wrong in dark mode** — it read `--semantic-text-inverse`, whose *meaning
   flips* with the mode, so the selected dark mode painted dark ink on a dark band at **1:1**. The
   band's ink is now a mode-stable token. Light went 14/19 → 17/18; dark 11/23 → 16/22.

**The dark accent cannot be fixed by tuning, and that is arithmetic.** White-on-accent at 4.5:1
requires the accent's relative luminance ≤ 0.1833; accent-on-band at 4.5:1 requires ≥ 0.2002. The
bounds do not overlap, and an exhaustive search of hue 240–265 × saturation 40–100% × lightness
30–85% returns **0 of 18,928** satisfying values. The resolution is an accent-vocabulary decision —
dark text on the fill, or separate fill and ink tokens — which the PRD gives to R5. Row `W1-S11`.

**The dark round trip (brief III.7):** `light rgb(244,246,250) → dark rgb(11,17,29) → light
rgb(244,246,250)` on both routes, **residue NONE**, `color-scheme` back to `light`.

**Not covered, stated rather than implied:** SC **1.4.11** (3:1 for UI component boundaries). This
instrument samples text pairs only — 0 of 40 are boundary pairs. If the `#C4CBDB` hairline on
`#FFFFFF` is read as a required boundary rather than decoration, it is 1.47:1 and below that bar.
The focus indicator is RB-s-6's and this cell adds no `box-shadow`.

---

## CONTROLS

- **Before retiring the three navy tiers**, censused every `--navy-*` reference: exactly **one**
  consumer outside the theme file (`NestedCard.tsx`), repaired in the same commit. A token
  something still reads would have resolved to nothing — invisible, not loud.
- **The theme-rewriter's own assert fired — on its own documentation.** A bare substring test could
  not tell a retired token *named* in the retirement note from one still *declared*; tightened to
  match a declaration. That is the fourth time this project has hit a check that cannot go red.
- **The proof-of-spec checker caught a defect in this very instance**: two file paths in one
  `path_or_key`, which resolves to a dead path. Split into two rows. And the first validation run
  reported `rc=0` from `echo rc=$?` **after a pipe** while the checker itself printed `INVALID
  (rc=1)` — the same pipeline trap as `W1-S6`. The `rc=0` quoted above was re-read without a pipe.

### The flip was made on a stale reading, and the re-run caught it

`RB3-AC5` was checked early and printed `SHARP`. Work continued on the same file; the `<status>`
flip was made and committed; **then** the whole battery was re-run against the final tree — and
`RB3-AC5` printed **`MID-RANGE`**. The cause was not the radii: a radius-token *usage* added later
(`border-radius` set from the control token) fell inside the criterion's pattern, whose wildcard
crosses newlines, so it read past the usage and graded the *next* declaration's value (`inherit`).
A comment written to explain that then tripped the same check a **second** time by naming the
pattern. The usage is now a literal mirroring the token, the comment describes rather than
reproduces, and the criterion prints `SHARP` on the committed tree with `AC1`–`AC4` re-run beside
it. Row `W1-S12`.

Stated plainly because it is the transferable part: **a per-criterion pass earlier in the turn is
not a pass at the flip.** The battery has to be re-run against the final tree immediately before
the flip, which is the only reason this was caught rather than shipped.

---

## SURPRISES

- **W1-S9** (BLOCKING, ARMED) — the canvas cannot reach its measured surface share from inside these
  paths: 4,887 light-on-dark idioms in 171 page files hold 449 band instances inverted.
- **W1-S10** (OBSERVATION, ARMED) — 184 occurrences colour **text** with a **background** token,
  which put the page title at 1:1 the moment a real dark mode existed. 64 repaired in grant, 120 in
  20 page files not. The defect is the *role collision*, not the value.
- **W1-S11** (OBSERVATION, INERT) — the dark-mode accent's two roles demand non-overlapping
  luminance bounds.

## WHAT THIS CELL DID NOT DO

Turn the bands white (W1-S9); touch `catalyst/` (its pseudo-elements *are* its control surfaces —
RB-s-5/RB-s-6); re-tune the dark accent (impossible, R5's); fix the `INT` chip (data colour, page
file); compute SC 1.4.11; change any information architecture; add any drop shadow; push, merge or
rebase. Full list with reasons in `declared_exclusions`.
