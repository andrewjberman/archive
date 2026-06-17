# TO DECK_CLAUDE.FANOUT-B — Panels + Grid archetype variations

<issued_to>0.4.2_RD_AdvisorIntelligence~B</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>complete</status>
<!-- RAVC2 (0.4.2_RD_AdvisorIntelligence~B, 816ae5e79): panels-icon/bordered/formula + grid-outline/matrix/badge
     built in arch_panels.py + arch_grid.py. Both showcases GATE PASS 0 lint + full coverage; every slide
     COM visual-QA'd clean. Modules ruff-clean (no bypass). Grid catalog=4 (complete); Panels catalog=5 pending
     base RD de-registering the standalone core `formula` row (panels-formula absorbs it; compose.py is base lane). -->

## Objective
Bring **Panels** and **Grid** to **4 variations each** (build the NEW ones; the core `panels` and `grid`
already exist). You own `deck_generation/engine/arch_panels.py` + `deck_generation/engine/arch_grid.py`
exclusively (stubbed + imported). Design targets + slide refs are in
`deck_generation/dev/docs/master-slide-archetype-map.md` — read it first.

## Build these (content fns take `(s, items, ...)`; caller does `s = d.slide("<tag>")`)

### Panels (arch_panels.py) — absorbs the old `formula`
- **panels-icon** — rows: a brand circle/square badge with a GEOMETRIC mark (NOT clip-art, F6) + bold
  navy heading + body/bullets (master slides 8/86; board B5/B12/B15). Filled-card option per board B5/B12.
- **panels-bordered** — cards with a colored outline + header band + bullet list; optional labeled
  sub-sections (What/How) + a tinted footer tier (master slide 64; board B6).
- **panels-formula** — 3 cards with centered `+` and `=` operators (the old formula, folded in).
  (Core `panels` = the header-band version, already exists -> 4 total.)

### Grid (arch_grid.py) — "different container styles + orientations" (Andrew)
- **grid-outline** — tiles drawn as outlines (stroke only, no fill).
- **grid-matrix** — a positioning / rating matrix: rows x cols (e.g. Underweight/Neutral/Overweight), a
  filled circle marking each row on a rounded-rect track; supports two side-by-side (master slide 30). BUILDABLE.
- **grid-badge** — a 2x2 (or NxM) grid of icon-cards: brand circle badge + heading + body (board B12).
  (Core `grid` = accent-bar tiles, already exists -> 4 total.)

## Build protocol (per variation)
1. **Read first:** `DESIGN_BIBLE.md` (law), `dev/docs/master-slide-archetype-map.md` (your targets + refs),
   `PROMPT_SPEC.md`, and the existing `engine/compose.py` (`panels`, `grid`, `C.rrect/bar/circle/banner/
   text/topband`, `ramp(n)`, `uni_pt`) — mirror their style + compliance.
2. **Edit ONLY** `arch_panels.py` + `arch_grid.py` (+ your showcase scripts + your home-folder log). Do NOT
   touch `compose.py`/`registry.py`/another family's module (pre-wired; zero-contention).
3. **Correct-by-construction vs DESIGN_BIBLE:** A1 palette + Lato only; >=0.5in margins; radius 0.10in via
   `C.rrect`; accent bars are PLAIN rectangles via `C.bar` (rounded<0.3in fails D7); true circles via
   `C.circle` (w==h); no-wrap large text via `C.banner`; D3 symmetry (equal width + equal gutters per row);
   D8 one size for a parallel text group; every slide carries a graphic element (D9 counts filled panels +
   tables). Geometric marks only (F6) — for an "icon", use a simple drawn shape or a numbered badge.
4. **register()** each in your module: `("panels-icon", "arch_panels.panels_icon", "N x (head, body)",
   "<use>", <min>, <max>, "<example>")`, `family="Panels"` (and `family="Grid"`).
5. **Showcase:** `dev/scripts/showcase_panels.py` + `dev/scripts/showcase_grid.py` — one slide per variation
   (all 4 incl. the core via `C.panels`/`C.grid`), eyebrow-labeled with the variant name + sample Opal
   content, built via `Deck()` + `d.finalize(out)`. MUST print **GATE PASS: 0 lint + full coverage**; no
   two consecutive identical archetype tags (D10).
6. **Visual-QA (the product):** render each showcase to PNG via PowerPoint COM (copy-local + Unblock-File
   if needed) and READ every slide image. Fix 60-30-10 / white-on-white / orphans / grid alignment /
   footer collision / motif-fit; re-render until clean. Gate-pass is necessary, the eye is sufficient.
7. **Self-commit (DECK lane):** pull latest CLOUD first, then `.tools/safe-commit.sh --author
   "0.4.2_RD_AdvisorIntelligence~B <0.4.2_RD_AdvisorIntelligence~B@opal.agent>" -m "...~B: DECK_CLAUDE --
   panels + grid archetype variations ... GATE-NOTE: ruff E701 = the dense one-line idiom (pre-existing);
   no bulk --fix." -- deck_generation/engine/arch_panels.py deck_generation/engine/arch_grid.py
   deck_generation/dev/scripts/showcase_panels.py deck_generation/dev/scripts/showcase_grid.py`. Write your
   session log; RAVC2-report to base RD (`0.4.2_RD_AdvisorIntelligence`) CC `2.0.0_SA_COO`.

<acceptance_criteria>
- `python -m engine.compose --catalog` shows Panels (4) + Grid (4), incl. your new variants.
- showcase_panels.py + showcase_grid.py each print GATE PASS, 0 lint violations, full coverage.
- Every showcase slide passes your visual-QA read (on-brand, no white-on-white, no footer collision).
- Committed under your ~B author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A — standalone deck tooling. Verification = the design_lint [AUTO] gate + fidelity coverage + PowerPoint-COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>Shared files (compose.py / registry.py) are PRE-WIRED — do not edit. You own arch_panels.py + arch_grid.py exclusively. Pull before commit. Base RD integrates all modules into one combined showcase.</cross_domain_coordination>
