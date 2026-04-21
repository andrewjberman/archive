<task_order>
  <metadata>
    <id>1.1.0_SA_CTO-2026-04-16-comp-learns-018-program-md-v1</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>1.1.0_SA_CTO</issued_to><!-- Transferred 2026-04-21 from 1.0.0_SA_CTO per COMP_LEARNS_TARGET_CLOSEOUT.md §7.2. Scope amended same commit per §8.5 — 9th item added (Promoted Learnings section scaffold per TARGET_CLOSEOUT §3). Original authorship date + issuer preserved. -->
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — post-integration doctrine update</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ dc839e77 (v4.2)</ref>
    <ref type="prd_section">§4.5 dimensional ontology, §5.3 conflict resolution, §6.1 primary metric, §6.5 selector discipline, §6.6 mutation invariants, §7.5 active adversarial, §8-§11 v0 target + scorecard</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md v1.0 (§3 promotion rule; §6 closeout module)</ref>
    <ref type="prd_section">TARGET_CLOSEOUT §3 — Promoted Learnings section format + scaffold + enforcement hook into program_promotion.py</ref>
    <ref type="module">comp/framework/closeout/program_promotion.py (shipped by .024; consumed by program.md authoring)</ref>
  </references>

  <objective>
    Rewrite `comp/program.md` to v1.0 — the slow-evolving protocol that codifies the architectural decisions made in PRD v2. This is the "how to build a compiler for an arbitrary system" transferable doctrine.

    Per PRD §15 handoff: CTO-owned. Scheduled after `.017` lands (the doctrine documents what the ratchet proved).

    Incorporate:
    1. **Bootstrap-vs-target table (§9 revised).**
    2. **Dimensional ontology (§4.5)** — subtype kinds closed; variation via attributes.
    3. **Conflict resolution (§5.3)** — R1-R5 + sidecar discipline.
    4. **Selector discipline (§6.5)** — ≥3 selectors at v0, per-selector reporting, SelectorGameDetected.
    5. **Mutation invariants (§6.6)** — rename/reorder/noise × 3 seeds, ≥ 0.85 stability threshold.
    6. **Active adversarial pattern (§7.5)** — failure → targeted variants → re-test inside iteration.
    7. **Primary metric formula (§6.1).**
    8. **Confidence ladder (§5.1).**
    9. **Promoted Learnings section scaffold (TARGET_CLOSEOUT §3).** Empty `## Promoted Learnings` section with the format comment from TARGET_CLOSEOUT §3 inline. No actual learnings promoted at v1.0 ship — v1.0 is the skeleton the first close-out fills via `comp.framework.closeout.promote()` (shipped by .024). The append-only invariant of this section is enforced in code; v1.0 only needs to scaffold it correctly so `promote()`'s first call has a target.

    Explicitly out of scope: PRD v4.3+ content (future amendments), any re-architecting beyond v4.2 decisions, TOs .011-.017 implementation details (program.md is doctrine, not reference), target-2-specific content (that lands post-close-out).
  </objective>

  <scope>
    <files>
      <file action="modify">comp/program.md (rewrite to v1.0)</file>
    </files>
  </scope>

  <wire_contract>
    **Diff-size constraint:** `wc -l comp/program.md` v1.0 ≤ 4× v0 line count (Karpathy-sparse spirit preserved; amended scope needs more room than v1's single-pass target). Per PRD §12.2 TO .018 Phase 3.

    **Section structure (recommended):**
    - Header / status
    - The six concerns (parsers / ir / compiler_subtypes / graph_builder / bench / loop)
    - The dimensional ontology rule (§4.5)
    - The conflict resolution policy (§5.3)
    - The selector discipline (§6.5)
    - The mutation invariants (§6.6)
    - The active-adversarial pattern (§7.5)
    - The primary metric formula (§6.1)
    - The confidence ladder (§5.1)
    - The bootstrap-vs-target table (§9)
    - The invariants across concerns (§2 bullet list)

    **Tone:** doctrine, not tutorial. Reader is a future compiler-author arriving cold. They need the RULES, not the history.
  </wire_contract>

  <acceptance_criteria>
    1. `comp/program.md` v1.0 incorporates all 9 items from §objective (items 1-8 from v4.2 PRD + item 9 Promoted Learnings scaffold per TARGET_CLOSEOUT §3).
    2. `wc -l comp/program.md` ≤ 4× v0 line count (diff-size gate).
    3. Each of the 9 items has its own named section or subsection — searchable by reader.
    4. **No TO-level detail leaks in.** program.md does not reference `.011`, `.017`, specific test filenames, or commit SHAs. It cites §-numbers in the architecture PRD where needed.
    5. **Dimensional ontology section explicitly forbids flat-string subtype names** — the "imports_dynamic is banned, use attributes" rule is spelled out.
    6. **Conflict policy section lists R1-R5 verbatim** with one-sentence examples.
    7. **Selector discipline section mandates ≥3 selectors + SelectorGameDetected fork.**
    8. **Mutation invariants section states ≥0.85 stability threshold and per-failure active-adversarial.**
    9. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    10. MCP COMPLETE to 2.0.0_SA_COO~B with commit hash + before/after line counts + diff-size ratio.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>wc -l comp/program.md</run>
        <expect>Records current v0 line count. Used as denominator for diff-size ratio.</expect>
        <if_mismatch>File missing — pull latest from main.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/httpx/experiment_log.jsonl comp/targets/httpx/scorecards/</run>
        <expect>Both present — .017 landed, ratchet proven, doctrine can reference it as fact not hypothesis.</expect>
        <if_mismatch>STOP. .017 has not shipped. program.md v1.0 must describe a proven system, not a hypothesized one.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>grep -E "(imports_dynamic|imports_conditional|imports_framework)" comp/program.md</run>
        <expect>Matches ONLY in the "banned patterns" section (as counterexamples). Never as described-as-valid subtypes.</expect>
        <if_mismatch>Fix. §4.5 mechanical enforcement says flat-string subtype names are banned; program.md must reflect this.</if_mismatch>
      </step>
      <step>
        <run>grep -c "^##\|^###" comp/program.md</run>
        <expect>≥ 9 section headers (one per required item from §objective, plus header).</expect>
        <if_mismatch>Add missing sections.</if_mismatch>
      </step>
      <step>
        <run>grep -n "^## Promoted Learnings" comp/program.md</run>
        <expect>Exactly 1 match — the Promoted Learnings section scaffold per TARGET_CLOSEOUT §3 is present and named exactly.</expect>
        <if_mismatch>Add or rename the section. The section header must match exactly because `program_promotion.py` parses it by literal string.</if_mismatch>
      </step>
      <step>
        <run>echo "ratio = $(wc -l &lt; comp/program.md) / $V0_LINE_COUNT"; # Compute v1 / v0 ratio</run>
        <expect>Ratio ≤ 4.0. Per PRD §12.2.</expect>
        <if_mismatch>Trim until ratio ≤ 4.0. Doctrine is terse; reference is the PRD.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>diff comp/program.md.v0 comp/program.md | wc -l</run>
        <expect>Non-zero (substantive rewrite). Document the diff summary in session log.</expect>
        <if_mismatch>If diff is tiny, doctrine was not actually updated. Re-author.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty. (Medium/Critical) Mitigation: program.md codifies gold-before-code invariant + mutation second-line-of-defense. Future authors read this first.</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: program.md's dimensional-ontology section is the first thing a new subtype author reads — "do not add flat-string kinds."</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Only doctrine. No new design decisions. Every new rule must trace back to a v2 PRD §.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: program.md v1.0 explicitly preserves v0 three-file-separation discipline + Track A/B vocabulary.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.017" status="required">End-to-end ratchet landed — doctrine references proven mechanics, not hypothetical.</dependency>
  </dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>On commit + MCP COMPLETE: COMP_LEARNS v0 wave complete. Project moves to v0.1 planning (second subtype, second target, or LLM proposer).</next>
</task_order>
