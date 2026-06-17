# TO DECK_CLAUDE.FANOUT-A — Cover + Statement/Mood archetype variations

<issued_to>0.4.2_RD_AdvisorIntelligence~A</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>complete</status>

## Objective
Build **4 Cover variations** + **4 Statement/Mood variations** as bible-compliant, registered,
gate-clean archetypes, grounded in the Opal master designs. You own two module files exclusively:
`deck_generation/engine/arch_cover.py` and `deck_generation/engine/arch_statement.py` (both stubbed
+ already imported by compose.py). 8 variations total.

## Your families (specs from `deck_generation/dev/docs/master-slide-archetype-map.md`)

### Cover (arch_cover.py) — cover fns take `(d, title, subtitle=..., tag=...)` and create their own slide
Andrew LOCKED the cover refs to the blocked-graphic mosaics: **master slides 1, 14, 60** (+ analyst B1)
— "grab those unique blocked graphics." Reproduce the blocked grid GEOMETRICALLY (color blocks navy/purple/
cool-grey + true circles via C.circle + half-rounded single-corner shapes + concentric-ring arcs via C.ring),
placeable LEFT or RIGHT. No photos — solid color blocks stand in for the master's photo cells.
1. **cover-mosaic** — text-left + the blocked-graphic mosaic on the RIGHT (master slide 1 / B1).
2. **cover-mosaic-left** — mosaic on the LEFT + a section/deck title on the right (master slide 14 "OCIO SERVICES").
3. **cover-minimal** — type-forward: big title on white or navy, one accent + eyebrow, lots of space (no mosaic).
4. **cover-divider** — section-break: navy/purple field + the mosaic + one large centered section title (master slide 60).

### Statement / Mood (arch_statement.py) — fns take `(s, big, sub=...)`; caller makes the slide (often dark)
1. **statement-fullcolor** — full purple (or navy) bg, big white statement + sub + a mosaic accent (slide 98).
2. **statement-dark** — dark (midnight) cinematic, big white line + cool-grey sub, restrained (slide 80).
3. **statement-quote** — a pull-quote + attribution + a large ring/quote mark.
4. **statement-bignum** — a giant number or single word as the mood (stat-as-mood; dark or purple).

## Build protocol (per variation)
1. **Read first:** `DESIGN_BIBLE.md` (law), `dev/docs/master-slide-archetype-map.md` (your targets +
   slide refs), `PROMPT_SPEC.md`, and the existing `engine/compose.py` primitives (`set_cover`,
   `statement`, `C.circle/rrect/bar/banner/text`, `ramp(n)`) — mirror their style + compliance.
2. **Edit ONLY** `engine/arch_cover.py` + `engine/arch_statement.py` (+ your showcase scripts + your
   home-folder log). Do NOT touch `compose.py`, `registry.py`, or another family's module — the imports
   + wiring are DONE (zero-contention design). The mosaic = compose with `C.rrect` (blocks/half-rounds
   via MSO_SHAPE), `C.circle` (true circles, w==h), `C.ring` (concentric arcs), A1 palette only.
3. **Correct-by-construction vs DESIGN_BIBLE:** A1 palette + Lato only; >=0.5in margins (except a
   deliberate full-bleed field — covers/dark statements may bleed, that's allowed); radius 0.10in via
   `C.rrect`; true circles via `C.circle`; no-wrap large text via `C.banner`; on a dark field text is
   white/cool-grey (A4); every content slide carries a graphic element (D9). Covers shown as slide 1
   are lint-skipped, but keep them clean regardless.
4. **register()** each variation in your module: `("cover-mosaic", "arch_cover.cover_mosaic", "(title,
   subtitle,tag)", "<use>", 1, 1, "<example>")`, `family="Cover"` (and `family="Statement"` for the other).
5. **Showcase:** write `dev/scripts/showcase_cover.py` + `dev/scripts/showcase_statement.py` — one slide
   per variation, eyebrow-labeled with the variant name + sample Opal-flavored content, built via a
   `Deck()` and `d.finalize(out)`. MUST print **GATE PASS: 0 lint violations + full coverage**; no two
   consecutive identical archetype tags (D10).
6. **Visual-QA (the product):** render each showcase to PNG via PowerPoint COM (copy local +
   `Unblock-File` if Protected View blocks; `Open(path,$true,$false,$false)`; Export PNG) and **READ
   every slide image**. Fix 60-30-10 / white-on-white / orphans / grid alignment / footer collision /
   motif-fit, re-render until clean. Gate-pass is necessary but NOT sufficient — the eye is.
7. **Self-commit (DECK lane):** pull latest CLOUD first, then
   `.tools/safe-commit.sh --author "0.4.2_RD_AdvisorIntelligence~A <0.4.2_RD_AdvisorIntelligence~A@opal.agent>"`
   `-m "...~A: DECK_CLAUDE -- cover + statement archetype variations ... GATE-NOTE: ruff E701 = the dense`
   `one-line idiom (pre-existing); no bulk --fix."` `-- deck_generation/engine/arch_cover.py`
   `deck_generation/engine/arch_statement.py deck_generation/dev/scripts/showcase_cover.py`
   `deck_generation/dev/scripts/showcase_statement.py`. Write your session log; RAVC2-report to base RD
   (`0.4.2_RD_AdvisorIntelligence`) CC `2.0.0_SA_COO`.

<acceptance_criteria>
- `python -m engine.compose --catalog` lists your 8 new archetypes under Cover + Statement.
- showcase_cover.py + showcase_statement.py each print GATE PASS, 0 lint violations, full coverage.
- Every showcase slide passes your visual-QA read (on-brand, no white-on-white, no footer collision).
- Committed under your ~A author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A — standalone deck tooling (no data-pipeline / cloud / frontend change). Verification = the design_lint [AUTO] gate + fidelity coverage + PowerPoint-COM visual-QA, the correct verify-channel for this artifact class.</compiler_tools_mandate>

<cross_domain_coordination>Shared files (compose.py / registry.py) are PRE-WIRED — do not edit them. You own arch_cover.py + arch_statement.py exclusively; other agents (~B/~C/~D) own different modules. Pull before commit. Base RD integrates all modules into one combined showcase afterward.</cross_domain_coordination>
