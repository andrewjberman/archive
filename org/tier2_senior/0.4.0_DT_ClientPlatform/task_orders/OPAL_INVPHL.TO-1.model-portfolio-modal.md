# Task Order OPAL_INVPHL.TO-1 — Model-portfolio popup modal (two trigger surfaces)

```xml
<task_order>
  <metadata>
    <id>OPAL_INVPHL-TO-1-model-portfolio-modal</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>{portal-frontend seat, on registration}</issued_to>
    <date>2026-08-11</date>
    <project>OPAL_INVPHL</project>
    <status>pending</status>
    <status_note>
      BUILD COMPLETE AND VERIFIED at portal DEV @84f6b3e2 (2026-08-11, 0.4.0_DT_ClientPlatform).
      All 8 acceptance criteria PASS, exercised on both trigger surfaces (5/5 models each),
      with a fired mutant on the C2 mapping and on the typecheck.
      The `complete` flip is WITHHELD -- not on my own judgement, but on this TO's own stated
      completion condition (a schema-valid proof-of-spec instance). That instance is INVALID on
      exactly 2 artifact-coverage violations that CANNOT be cleared honestly: the checker scans
      criterion_id only and wants the artifact stem inside the id, while this TO pins the id set
      to C1..C8 and the same script rejects any id outside that set. Silencing it would require a
      false declared_exclusion or a mis-typed artifact kind. Routed to 2.0.0_SA_COO for a ruling;
      instance + full mechanism at deliverables/PROOF_OF_SPEC_OPAL_INVPHL_TO1_20260811.json
      (surprises[6]). No code work outstanding.
    </status_note>
    <authority>
      Andrew-direct ~1953Z: "Approved your artifact-design on Investment Philosophy and all recs, get it
      done" — design concept + all nine decisions approved at COO recommendation. Record:
      org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20260811_OPAL_INVPHL_DESIGN_AND_NINE_DECISIONS_APPROVED.md
      B-1 field ruling: Andrew-direct ~1925Z @8fc01e9f98. Project registration @63eca83f34.
    </authority>
    <specs>
      PRD: docs/architecture/OPAL_INVPHL_PRD.md (frames)
      AUTHORITATIVE DEV SPEC: docs/references/OPAL_INVPHL/primer.md (specifies)
      Slide lookup: docs/references/OPAL_INVPHL/reference_guide.md
      ⚠ The primer PREDATES Andrew's B-1 ruling. Where the primer's field list and this TO disagree,
      THIS TO WINS — the primer still describes the deck's six fields incl. 3-Yr and 2025.
    </specs>
  </metadata>

  <objective>
    One modal component, reused at two call sites, opened by clicking a model name. RIGHT pane = the deck's
    "Key Notes" prose per model. LEFT pane = a performance block whose FIELDS are Andrew's ruled set and
    whose VALUES are live portal data. No new API field, no backend leg — PURE FRONTEND.
  </objective>

  <requirements>

    <requirement id="1" name="ONE dialog, built on the standard primitive">
      Build a single ModelPortfolioModal on src/ui/components/catalyst/dialog.tsx
      (Dialog/DialogTitle/DialogBody/DialogActions) — the primitive already used by UserSettingsModal.tsx
      and RollbackConfirmDialog.tsx.
      ⛔ NEVER hand-roll a `fixed inset-0` overlay. FearGreedModal.tsx does this; it is inconsistent
      precedent, NOT the pattern.
      ⛔ ONE component, TWO call sites. A second dialog for the second surface is a rejected outcome.
    </requirement>

    <requirement id="2" name="THE RULED FIELD SET — single labelled column, this order">
      Decision 2, RULED. Render ONE labelled column in exactly this order:
        Target Return  → per-model POLICY CONFIG (decision 4)
        YTD Return     → LIVE, getModelPortfolioBenchmarks() (src/api/portal-proxy.ts:833)
        1-Year Return  → LIVE, same response
        Since Inception→ LIVE, same response
        Current Yield  → LIVE, getPositioningData() (portal-proxy.ts:1085), characteristics.yield
        Portfolio Makeup→ LIVE, getPositioningData() allocation
      ⛔ 3-Yr Return and 2025 calendar-year return DO NOT EXIST in scope. Do not add them, do not stub
      them, do not add an API field for them. (Andrew ~1925Z: "We dont need to use their selection of
      figures aside from target return, we can just source YTD 1Y and SI from our existing data.")
      ⛔ NOT the deck's 2×3 grid. The deck is a FORMAT reference for the pane's weight and density only;
      its field LIST is superseded.
      ⛔ NO deck value rendered as if live. If a live field is unavailable at runtime, render an explicit
      unavailable state — a placeholder is LABELED a placeholder and none survives to merge.
    </requirement>

    <requirement id="3" name="Target Return config — one home, beside the model definitions">
      Decision 4, RULED. A per-model range string (e.g. "7–9%") authored in the SAME file as the model
      definitions (src/lib/modelPortfolioColors.ts or its immediate sibling — name + colour + target in one
      place). Initial content = the slide 17/19/21/23/25 Target values.
      ⚠ UNRULED and NOT yours to invent: WHO may change this value, and whether it surfaces anywhere else.
      Ship the config; if the question becomes load-bearing, surface it to COO — do not design an editor.
    </requirement>

    <requirement id="4" name="Prose keyed off CANONICAL names via the ONE existing alias map">
      Right pane = the "Key Notes" paragraphs from slides 17/19/21/23/25, one slide per model. Slides
      15, 16, 18, 20, 22, 24, 26 are EXPLICITLY EXCLUDED.
      ⛔ Key the content off CANONICAL model names using the EXISTING map at
      src/lib/modelPortfolioColors.ts:84-100. A SECOND mapping is PROHIBITED (B-2, single-homing).
      ⚠ TWO OF THE DECK NAMES ARE COUNTER-INTUITIVE AND WILL SILENTLY MIS-ASSIGN A MODEL'S STORY:
          deck "Long-Term Conservative" → canonical "Long Term"        (blue)
          deck "Long-Term Aggressive"   → canonical "Ultra-Long Term"  (red)
      Get these backwards and the wrong model shows the wrong prose with no error.
      Decision 3, RULED: the modal TITLE is the CANONICAL name. The deck alias is DROPPED — do not render it.
    </requirement>

    <requirement id="5" name="Two trigger surfaces — net-new click handlers">
      Neither surface has an affordance today; both model-name renders are plain spans.
        (a) /portfolios → Benchmark tab → heat map: src/components/BenchmarkHeatmap.tsx:554-560
        (b) /positioning → top stacked bars: src/pages/Positioning/panels/PositioningSummary.tsx:1069-1079
      Decision 5, RULED: NAME-ONLY hit target. Dotted underline at rest + a corner arrow, both going accent
      on hover AND focus. NOT a whole-row or whole-cell target — it would steal clicks from cells people are
      reading.
      Keyboard-operable and visibly focusable (the affordance is the client's ONLY hint that this is clickable).
      ⛔ The existing colour chips, heat colouring, and bar rendering are untouched.
    </requirement>

    <requirement id="6" name="OUT OF SCOPE — do not build">
      AUM metrics radial legend as a third trigger (Andrew's call). Any change to the benchmark/positioning
      data contracts. Any backend or serving-plane change.
    </requirement>

  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <step>
        <run>comp-transform schema-check ModelPortfolioModal</run>
        <run>comp-transform schema-check BenchmarkHeatmap</run>
        <run>comp-transform schema-check PositioningSummary</run>
        <expect>No MISSING props on any touched component (MISSING = runtime undefined).</expect>
        <if_mismatch>Fix before commit; a MISSING prop is a runtime crash for a client, not a lint nit.</if_mismatch>
      </step>
      <step>
        <run>comp-which "does clicking a model name have any cached query implication"</run>
        <expect>Rule 20(b). If the modal introduces or reuses a query key, comp-cache it.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="C1">BOTH trigger surfaces open the SAME modal component. Exactly one dialog implementation exists in the diff; catalyst/dialog is its base.</criterion>
    <criterion id="C2">Prose matches slides 17/19/21/23/25 per model, keyed off CANONICAL names through the EXISTING alias map. Verified explicitly for the two counter-intuitive mappings: clicking "Long Term" shows slide 23 content; clicking "Ultra-Long Term" shows slide 25.</criterion>
    <criterion id="C3">The performance pane renders EXACTLY the six ruled fields in the ruled order. 3-Yr Return and 2025 return appear NOWHERE in the diff.</criterion>
    <criterion id="C4">Every value is either a LIVE field from the two named existing endpoints or the per-model Target config. NO deck number is rendered as if live; no placeholder survives to merge.</criterion>
    <criterion id="C5">Modal title is the canonical model name; the deck alias is not rendered.</criterion>
    <criterion id="C6">Trigger affordance is keyboard-operable with a visible focus state, name-only hit target, on both surfaces.</criterion>
    <criterion id="C7">comp-transform schema-check clean on every touched component; no new console errors; portal CI leg green; portal worktree on DEV (Rule 19).</criterion>
    <criterion id="C8">NO new API field, NO backend change, NO serving-plane change in the diff.</criterion>
  </acceptance_criteria>

  <proof_of_spec>
    Required. Instance at org/tier2_senior/{your_serial}/deliverables/PROOF_OF_SPEC_OPAL_INVPHL_TO1_{YYYYMMDD}.json
    per org/standards/PROOF_OF_SPEC.schema.json.
    Validate with the id set POSITIONAL:
        python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8
    ⚠ The id set is sys.argv[2]. There is NO argparse and NO --expected-criteria flag — the flagged form
    trips the usage guard and exits rc=2. Run UNPIPED: a piped rc is the PIPE's rc, not the checker's.
    ⛔ Do NOT "fix" a usage error by dropping the id argument: the 2-arg form returns a clean rc=0 VALID
    that means COVERAGE UNCHECKED.
  </proof_of_spec>

  <execution_rules>
    Portal main worktree stays on DEV (Rule 19); promotes run via /prod-deploy in the DT lane — NOT yours.
    Commit via .tools/safe-commit.sh under your own author line, pathspec-scoped, no pre-git-add.
    Diff-stat BEFORE committing, not after (safe-commit commits what you NAME, not what you CHANGED, rc=0
    either way).
    Report to 2.0.0_SA_COO on completion or on ANY of: a ruled decision that cannot be built as ruled, a
    third trigger surface discovered, or the Target-Return-ownership question becoming load-bearing.
  </execution_rules>
</task_order>
```
