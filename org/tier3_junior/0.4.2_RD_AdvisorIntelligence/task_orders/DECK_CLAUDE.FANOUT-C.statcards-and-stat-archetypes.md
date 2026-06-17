# TO DECK_CLAUDE.FANOUT-C — Statcards + Stat archetype variations

<issued_to>0.4.2_RD_AdvisorIntelligence~C</issued_to>
<issued_by>0.4.2_RD_AdvisorIntelligence (base, deck-system owner) — Andrew-direct fan-out</issued_by>
<project>DECK_CLAUDE</project>
<status>staged</status>

## Objective
Bring **Statcards** and **Stat** to **4 variations each** (build the NEW ones; core `statcards` and `stat`
exist). You own `deck_generation/engine/arch_statcards.py` + `deck_generation/engine/arch_stat.py`
exclusively (stubbed + imported). Design targets in `deck_generation/dev/docs/master-slide-archetype-map.md`.
NOTE: real charts are DEFERRED — these are **stat-as-type** treatments (shapes + type, F2: never fabricate a chart).

## Build these (content fns take `(s, ...)`; caller does `s = d.slide("<tag>")`)

### Statcards (arch_statcards.py)
- **statcards-clean** — big number + label only, no vs-line (clean KPI cards).
- **statcards-strip** — a compact single-row horizontal strip of 4-6 metrics (tight, divider-separated).
- **statcards-delta** — number + an up/down delta (a geometric triangle marker) + the change vs prior.
  (Core `statcards` = vs + takeaway cards -> 4 total.)

### Stat (arch_stat.py) — Andrew: "needs more text/design"
- **stat-context** — one oversized hero number beside a context paragraph.
- **stat-hero** — a big filled card with a giant number + label (board B10 "$30B+ / 10 year AUA goal"),
  pairs well beside a list; mood-ish.
- **stat-stacked** — a stacked-segment "composition" bar/column built from rectangles (master slide 51:
  sleeve composition, 3 stacked colored segments per column + left-axis labels + a divider). BUILDABLE.
  (Core `stat` = a single stat-as-type figure -> 4 total.)

## Build protocol (per variation)
1. **Read first:** `DESIGN_BIBLE.md` (law), `dev/docs/master-slide-archetype-map.md` (your targets + refs),
   `PROMPT_SPEC.md`, and the existing `engine/compose.py` (`stat`, `statcards`, `C.rrect/bar/circle/banner/
   text`, `ramp`, `uni_pt`, `ton`) — mirror their style + compliance.
2. **Edit ONLY** `arch_statcards.py` + `arch_stat.py` (+ your showcase scripts + your home-folder log). Do
   NOT touch shared files (pre-wired; zero-contention).
3. **Correct-by-construction vs DESIGN_BIBLE:** A1 palette + Lato only; **F2 — figures render as designed
   type / shape compositions, never a fabricated chart**; >=0.5in margins; radius 0.10in via `C.rrect`;
   true circles via `C.circle`; no-wrap large numbers via `C.banner`; D8 uniform big-number size across a
   parallel group; D3 symmetry; every slide carries a graphic element (D9). Geometric marks only (F6).
4. **register()** each in your module (`method="arch_statcards.<func>"` / `"arch_stat.<func>"`, `family=
   "Statcards"` / `"Stat"`).
5. **Showcase:** `dev/scripts/showcase_statcards.py` + `dev/scripts/showcase_stat.py` — one slide per
   variation (all 4 incl. core via `C.statcards`/`C.stat`), eyebrow-labeled + sample Opal content, via
   `Deck()` + `d.finalize(out)`. MUST print **GATE PASS: 0 lint + full coverage**; no consecutive-repeat (D10).
6. **Visual-QA (the product):** render each showcase to PNG via PowerPoint COM and READ every slide image;
   fix 60-30-10 / white-on-white / orphans / alignment / footer collision; re-render until clean.
7. **Self-commit (DECK lane):** pull latest CLOUD first, then `.tools/safe-commit.sh --author
   "0.4.2_RD_AdvisorIntelligence~C <0.4.2_RD_AdvisorIntelligence~C@opal.agent>" -m "...~C: DECK_CLAUDE --
   statcards + stat archetype variations ... GATE-NOTE: ruff E701 (pre-existing); no bulk --fix." --
   deck_generation/engine/arch_statcards.py deck_generation/engine/arch_stat.py
   deck_generation/dev/scripts/showcase_statcards.py deck_generation/dev/scripts/showcase_stat.py`. Write
   your session log; RAVC2-report to base RD CC `2.0.0_SA_COO`.

<acceptance_criteria>
- `python -m engine.compose --catalog` shows Statcards (4) + Stat (4), incl. your new variants.
- showcase_statcards.py + showcase_stat.py each print GATE PASS, 0 lint violations, full coverage.
- Every showcase slide passes your visual-QA read; no fabricated charts (F2).
- Committed under your ~C author line on the DECK lane.
</acceptance_criteria>

<compiler_tools_mandate>N/A — standalone deck tooling. Verification = design_lint gate + fidelity coverage + COM visual-QA.</compiler_tools_mandate>
<cross_domain_coordination>compose.py / registry.py PRE-WIRED — do not edit. You own arch_statcards.py + arch_stat.py exclusively. Pull before commit. Base RD integrates.</cross_domain_coordination>
