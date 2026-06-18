# TO DECK_CLAUDE.FANOUT-D — Compare + Flow + List archetype variations

<issued_to>0.4.2_RD_AdvisorIntelligence~D</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>complete</status>

## Objective
Bring **Compare**, **Flow**, and **List** to **4 variations each** (build the NEW ones; cores exist). You
own `deck_generation/engine/arch_compare.py` + `arch_flow.py` + `arch_list.py` exclusively (stubbed +
imported). This is the heaviest lane (3 families, ~7 new). Design targets in
`deck_generation/dev/docs/master-slide-archetype-map.md` — read it first.

## Build these (content fns take `(s, ...)`; caller does `s = d.slide("<tag>")`)

### Compare (arch_compare.py) — Andrew: "MUCH more active", wants Venn approaches
- **compare-venn** — 2 translucent overlapping TRUE circles (w==h) + a shared-middle label. B3: text sits
  on solid fields only (never over a triangular/overlap gap = white-on-white).
- **compare-convergence** — the Opal signature (master slide 9 = frame_0): 3 translucent overlapping
  circles (navy/purple/dark) meeting at the Opal interlock mark, each circle labeled (+ a left text column).
- **compare-balance** — an active vs treatment: a scale/balance beam or opposing arrows.
  (Core `compare` = 2-col header-banded -> 4 total.)

### Flow (arch_flow.py) — absorbs vsteps + flow; Andrew "make a couple more"
- **flow-loop** — nodes in a circular closed loop (true circles + connectors), a cycle.
- **flow-chevron-detail** — chevrons across the top + a per-step detail card column under each (master
  slide 65: PROCESS/RESULT header-banded columns). Chevrons are D2-exempt (label centers in the body).
  (Cores `flow` = chevrons + `vsteps` = vertical numbered -> 4 total.)

### List (arch_list.py) — absorbs list-sidebar + list
- **list-numbered** — a vertical numbered list (circle indices); ALSO support a dark "agenda/TOC" style:
  2-column, big purple 01-0N numbers + label + thin divider rule on a midnight slide (board B2).
- **list-checklist** — checkmark rows: a brand circle with a white GEOMETRIC check + text; 1- or 2-column
  (board B5/B10). Alternate states OK (e.g. a purple "?" circle, board B10).
  (Cores `list-sidebar` + `list` -> 4 total.)

## Build protocol (per variation)
1. **Read first:** `DESIGN_BIBLE.md` (law), `dev/docs/master-slide-archetype-map.md` (your targets + refs),
   `PROMPT_SPEC.md`, and the existing `engine/compose.py` (`compare`, `flow`, `vsteps`, `list_accent`,
   `list_sidebar`, `C.circle/ring/bar/banner/text/rrect`, `ramp`, `ton`) — mirror their style + compliance.
2. **Edit ONLY** `arch_compare.py` + `arch_flow.py` + `arch_list.py` (+ your showcase scripts + home-folder
   log). Do NOT touch shared files (pre-wired; zero-contention).
3. **Correct-by-construction vs DESIGN_BIBLE:** A1 palette + Lato only; **true circles w==h via C.circle**
   (critical for venn/convergence/loop — D1); for translucent overlap set fill alpha at the XML level but
   keep A1 colors; **B3 white-on-white guard** — light text only on a solid field, never over an overlap
   gap; >=0.5in margins; radius 0.10in via `C.rrect`; accent bars = plain rects via `C.bar`; no-wrap large
   text via `C.banner`; every slide carries a graphic element (D9); geometric marks only (F6 — the check
   mark is a drawn geometric shape).
4. **register()** each in your module (`method="arch_<family>.<func>"`, `family="Compare"/"Flow"/"List"`).
5. **Showcase:** `dev/scripts/showcase_compare.py` + `showcase_flow.py` + `showcase_list.py` — one slide per
   variation (all 4 each, incl. cores via `C.compare`/`C.flow`/`C.vsteps`/`C.list_accent`/`C.list_sidebar`),
   eyebrow-labeled + sample Opal content, via `Deck()` + `d.finalize(out)`. MUST print **GATE PASS: 0 lint +
   full coverage**; no consecutive-repeat (D10).
6. **Visual-QA (the product):** render each showcase to PNG via PowerPoint COM and READ every slide image.
   Venn/convergence are the highest-risk for B3 white-on-white + D1 egg-circles — inspect those closely.
   Fix and re-render until clean.
7. **Self-commit (DECK lane):** pull latest CLOUD first, then `.tools/safe-commit.sh --author
   "0.4.2_RD_AdvisorIntelligence~D <0.4.2_RD_AdvisorIntelligence~D@opal.agent>" -m "...~D: DECK_CLAUDE --
   compare + flow + list archetype variations ... GATE-NOTE: ruff E701 (pre-existing); no bulk --fix." --
   deck_generation/engine/arch_compare.py deck_generation/engine/arch_flow.py deck_generation/engine/arch_list.py
   deck_generation/dev/scripts/showcase_compare.py deck_generation/dev/scripts/showcase_flow.py
   deck_generation/dev/scripts/showcase_list.py`. Write your session log; RAVC2-report to base RD CC `2.0.0_SA_COO`.

<acceptance_criteria>
- `python -m engine.compose --catalog` shows Compare (4) + Flow (4) + List (4), incl. your new variants.
- showcase_compare.py + showcase_flow.py + showcase_list.py each print GATE PASS, 0 lint violations, full coverage.
- Every showcase slide passes your visual-QA read; venn/convergence circles are true (w==h) + no white-on-white.
- Committed under your ~D author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A — standalone deck tooling. Verification = design_lint gate + fidelity coverage + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>compose.py / registry.py PRE-WIRED — do not edit. You own arch_compare.py + arch_flow.py + arch_list.py exclusively (the other agents own different modules). Pull before commit. Base RD integrates all into one combined showcase.</cross_domain_coordination>
