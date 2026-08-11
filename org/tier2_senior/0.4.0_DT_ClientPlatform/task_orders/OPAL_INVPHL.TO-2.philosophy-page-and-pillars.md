# Task Order OPAL_INVPHL.TO-2 — Philosophy page: rename + five-pillar strip + pillar modals

```xml
<task_order>
  <metadata>
    <id>OPAL_INVPHL-TO-2-philosophy-page-and-pillars</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>{portal-frontend seat, on registration}</issued_to>
    <date>2026-08-11</date>
    <project>OPAL_INVPHL</project>
    <status>complete</status>
    <status_note>
      COMPLETE. Built + verified at portal DEV @335dd198 (2026-08-11, 0.4.0_DT_ClientPlatform).
      C1-C6 and C8 PASS, exercised in a browser (redirect navigated, not read off the route
      table; 5/5 pillar mappings; reflow measured at 1440/900/600px). C7 is
      UNVERIFIABLE-BY-INSTRUMENT: the CLAUDE.md Rule 25 amendment is authored and verified
      in-tree but owned-paths refuses this lane (BASE_EXEC), and same-commit is structurally
      impossible anyway -- the rename lives in the portal SUBMODULE, CLAUDE.md in the
      workspace repo. Routed to COO+CTO in the same turn per the TO escape, and
      DISCHARGED the same window: CTO landed it @9d8217cb15, verified by me against HEAD
      (Andrew verbatim 1x untouched, artifact locator 1x, dangling route locator 0x).
      C7 is now PASS; PRD acceptance-5 discharged.
      HISTORY: the flip was WITHHELD alongside TO-1 on the same proof-of-spec conflict
      (criterion-id grammar vs the pinned C1..C8 id set). No code work was ever outstanding.
      CLOSURE 2026-08-11: proof-of-spec instance now VALID, 0 violations, on an HONEST
      declaration -- CVO added `frontend_component` to the schema kind enum @8d77cd1537 after
      two instances failed identically (Rule 24 postulate (i): the enum was not collectively
      exhaustive). Both available one-line greens were refused as false (a declared_exclusion on
      a covered artifact; rewriting criterion ids to embed stems). COO GO to flip: 214652Z,
      superseded 220314Z by the root fix. Flipped complete by the assignee.
    </status_note>
    <sequencing>
      Runs AFTER TO-1 if one seat holds both — TO-1 establishes the catalyst/dialog treatment this TO reuses.
      Independent file set, so a second seat could parallelize; COO is not requesting one.
    </sequencing>
    <authority>
      Andrew-direct ~1953Z: "Approved your artifact-design on Investment Philosophy and all recs, get it
      done." Record:
      org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20260811_OPAL_INVPHL_DESIGN_AND_NINE_DECISIONS_APPROVED.md
    </authority>
    <specs>
      PRD docs/architecture/OPAL_INVPHL_PRD.md · dev spec docs/references/OPAL_INVPHL/primer.md ·
      slide lookup docs/references/OPAL_INVPHL/reference_guide.md
      ⚠ The primer says the header becomes "Philosophy". Decision 1 RULED it "Investment Philosophy" for the
      HEADER and "Philosophy" for the SIDEBAR. THIS TO WINS.
    </specs>
  </metadata>

  <objective>
    Rename the Capital Market Assumptions page to the Philosophy page, add a five-pillar strip above the
    existing table, and give each pillar a modal carrying its talking-point paragraph. Everything already on
    the page stays byte-unchanged beneath the new strip.
  </objective>

  <requirements>

    <requirement id="1" name="Route + labels — the ruled wording">
      Decision 1, RULED:
        Route:          /cma → /philosophy   (src/App.tsx:415 route, :19 lazy import, + ALL internal links)
        Page header:    "Capital Market Assumptions" → "Investment Philosophy"
                        (CapitalMarketAssumptions.tsx:106, via PageHeaderCleanBadge)
        Sidebar label:  "Capital Markets" → "Philosophy"   (src/App.tsx:98)
      ⚠ The header and sidebar wording DIFFER on purpose — the nav column is narrow and every other label is
      one word. This is not an inconsistency to normalize.
    </requirement>

    <requirement id="2" name="REDIRECT the old URL — do not leave it dead">
      Decision 6, RULED: /cma REDIRECTS to /philosophy. Advisors bookmark pages and links live in email; a
      dead URL is a support ticket for no benefit. Updating internal links alone is NOT sufficient.
    </requirement>

    <requirement id="3" name="The five-pillar strip — NEW, above the existing panel">
      Rendered ABOVE the AssumptionsTable panel (CapitalMarketAssumptions.tsx:112-129). Titles from deck
      slide 9, "Five Key Investment Philosophy Pillars":
        1. Invest with a Long-Term Perspective
        2. Capitalize on Market Dislocations
        3. Balance Active and Passive Approaches
        4. Benchmark-Aware, Not Benchmark-Bound
        5. Optimize After-Tax Outcomes
      Decision 7, RULED: FIVE DISTINCT ICONS if slide 9's are clean enough to reuse; a single repeated gear
      is the SANCTIONED FALLBACK if extraction is messy. State which you used and why.
      Decision 8, RULED: on narrow screens REFLOW 3-up then 2-up. ⛔ NOT a horizontal scroller — a pillar the
      client never scrolls to is a pillar they never read.
      Each pillar is keyboard-operable with a visible focus state.
    </requirement>

    <requirement id="4" name="Pillar modals — same primitive as TO-1, this exact mapping">
      Reuse catalyst/dialog.tsx (never a hand-rolled overlay). Body = the matching talking-point paragraph:
        | Pillar                                  | Source paragraph                | Slide |
        | Invest with a Long-Term Perspective     | "Long-Term Perspective"         | 10 |
        | Capitalize on Market Dislocations       | "Tactical Flexibility"          | 10 |
        | Balance Active and Passive Approaches   | "Blend of Active and Passive"   | 11 |
        | Benchmark-Aware, Not Benchmark-Bound    | "Benchmark Aware"               | 11 |
        | Optimize After-Tax Outcomes             | "After-Tax Outcome"             | 12 |
      This mapping is CONFIRMED (reference_guide.md) — do not re-derive it from the slides.
      Decision 9, RULED: the copy SHIPS IN THE REPO. ⛔ NO CMS, NO admin editor, NO editable-text affordance.
      Yang/Manav editability is a SEPARATELY SCOPED question; if they need to iterate wording immediately the
      sanctioned intermediate is a served JSON the publishers already own — and that is NOT authorized here.
    </requirement>

    <requirement id="5" name="Everything below the strip is BYTE-UNCHANGED">
      The Expectations tab (10-Yr Assumptions table) and the Views tab (Tactical/Strategic inside
      OpalViewsTab.tsx via GradientSlider/ConvergingSlider) stay exactly as they are.
      The data plane does NOT move: getCMAAssumptions() / getOpalViews() (portal-proxy.ts:1370, :1412) are
      untouched. This task renames a ROUTE and LABELS.
    </requirement>

    <requirement id="6" name="⚠ THE RULE 25 CITATION RIDES THIS COMMIT — SAME ACT">
      PRD acceptance 5. CLAUDE.md Rule 25's only concrete exception example currently cites "the portal
      'cma'". This rename makes that locator dangle while the ARTIFACT keeps its identity.
      THE SAME COMMIT that lands the route rename amends the Rule 25 parenthetical to cite the ARTIFACT:
        (e.g. Capital Market Assumptions -- the `08_capital_market_assumptions` product, 1yr life)
      so the law survives every future route rename.
      ⛔ NOT a follow-up commit. A rename that lands without the doc amendment reintroduces the
      map-vs-territory drift this condition exists to prevent (the bd-client-detail precedent, where CTO made
      the doc update a same-commit condition for exactly this reason).
      NOTE: CLAUDE.md is a law surface — if your lane is refused on owned-paths, route the one-line amendment
      to COO/CTO IN THE SAME TURN as the rename commit, and say so in the report. Do not land the rename and
      leave the amendment for later.
    </requirement>

  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <step>
        <run>comp-transform schema-check CapitalMarketAssumptions</run>
        <run>comp-transform schema-check {the new pillar strip + pillar modal components}</run>
        <expect>No MISSING props.</expect>
      </step>
      <step>
        <run>comp-cache</run>
        <expect>Rule 20(b) — the route rename touches lazy imports and possibly cached routes/query keys.
        A stale cached route is a client seeing a dead page.</expect>
        <if_mismatch>Resolve before commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="C1">/philosophy serves the page; header reads "Investment Philosophy"; sidebar reads "Philosophy".</criterion>
    <criterion id="C2">/cma REDIRECTS to /philosophy — exercised, not assumed. No dead route, no 404.</criterion>
    <criterion id="C3">Five-pillar strip renders above the AssumptionsTable panel with the five ruled titles; icon choice (distinct vs fallback gear) is stated with its reason.</criterion>
    <criterion id="C4">Each pillar opens a catalyst/dialog modal carrying the CONFIRMED mapped paragraph. All five mappings verified individually.</criterion>
    <criterion id="C5">Strip reflows 3-up then 2-up on narrow widths; no horizontal scroller; each pillar keyboard-operable with visible focus.</criterion>
    <criterion id="C6">Expectations and Views tabs BYTE-UNCHANGED; getCMAAssumptions/getOpalViews untouched.</criterion>
    <criterion id="C7">⚠ The Rule 25 parenthetical amendment is IN THE SAME COMMIT as the rename (or routed to COO/CTO in the same turn with that stated in the report). Cites the ARTIFACT, not the route.</criterion>
    <criterion id="C8">NO CMS / editable-text affordance in the diff. comp-transform schema-check + comp-cache clean; no new console errors; portal CI green; worktree on DEV.</criterion>
  </acceptance_criteria>

  <proof_of_spec>
    Required. org/tier2_senior/{your_serial}/deliverables/PROOF_OF_SPEC_OPAL_INVPHL_TO2_{YYYYMMDD}.json
    Validate with the id set POSITIONAL, UNPIPED:
        python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8
    ⚠ No --expected-criteria flag exists (argv length 4 trips the usage guard, rc=2). Never drop the id
    argument to make the error go away — the 2-arg form returns rc=0 VALID meaning COVERAGE UNCHECKED.
  </proof_of_spec>

  <execution_rules>
    Portal main worktree stays on DEV (Rule 19). Promotes are the DT lane's /prod-deploy — NOT yours.
    safe-commit.sh under your own author line, pathspec-scoped, diff-stat BEFORE committing.
    Report to 2.0.0_SA_COO on completion, or immediately if: slide 9's icons cannot be cleanly extracted
    (so the fallback is in play), the owned-paths lane refuses the CLAUDE.md amendment, or anything below the
    strip turns out to require a change.
  </execution_rules>
</task_order>
```
