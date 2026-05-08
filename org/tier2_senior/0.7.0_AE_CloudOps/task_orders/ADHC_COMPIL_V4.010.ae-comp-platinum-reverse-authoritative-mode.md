<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.010</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-platinum reverse authoritative-only mode — annotated output (`[SPECULATIVE]` prefix) + `--strict` flag</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "distribute the Task orders" delegation. PRD v0.2 addendum §12.4 TO-10. Sequencing: independent (no dep on other v0.2 TOs). -->
    <priority>normal</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §12.4 TO-10 (v0.2 addendum 2026-05-08 PM)</ref>
    <ref type="anchor_incident">AUDIT-007 2026-05-05 DS~A: `comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m"` returned SPECULATIVE directory-prefix fallbacks (no verified TSX consumers). Tool limitation; fell back to `grep -rn "radial_12m" portal/src/` — 0 TSX hits; authoritative result.</ref>
    <ref type="second_anchor">Same session: `comp-platinum reverse "platinum/advisors/{id}/summary.json#active_since"` returned timeseries/nna_clients (wrong artifacts). Tool limitation; fell back to `grep -rn "active_since" portal/src/` — AdvisorPublicProfile.tsx sole consumer; authoritative result.</ref>
  </references>

  <context>
    `comp-platinum reverse &lt;s3-key#field&gt;` is documented as "return TSX consumers." Empirical AUDIT-007 (2026-05-05) showed two distinct failure modes:
    - Returns directory-prefix guesses when no AST-resolved consumers exist (instead of empty)
    - Returns wrong artifacts (timeseries/nna_clients when actual consumer is AdvisorPublicProfile.tsx)

    Silent wrong-result mode is the worst tool failure mode — agents trust the output without realizing it's speculative. DS~A had to fall back to direct `grep -rn` for both queries to get authoritative results. The tool's discovery utility is real (directory-prefix guesses CAN surface candidates worth investigating) but the trust boundary needs to be explicit.

    **Recommended approach (Option B from PRD §12.4):** annotated output + `--strict` flag. Preserves discovery utility; makes trust boundary explicit.
  </context>

  <scope>
    <step>
      <run>Read existing `comp-platinum reverse` implementation. Locate the result-emission logic — how does the tool currently distinguish AST-resolved consumers from directory-prefix guesses internally?</run>
      <expect>Internal distinction exists or is straightforward to add; emission combines both into one undifferentiated list currently.</expect>
      <if_mismatch>If no internal distinction, refactor result-collection to track classification per result (authoritative vs speculative) before emission.</if_mismatch>
    </step>
    <step>
      <run>Add classification tag to each result: `authoritative` (AST-resolved consumer; high-confidence) vs `speculative` (directory-prefix or substring match; low-confidence; agent must verify).</run>
      <expect>Per-result tag stored.</expect>
    </step>
    <step>
      <run>Emit results with `[SPECULATIVE]` prefix on speculative-tagged lines; authoritative lines unchanged. Default behavior: emit both classes (preserve discovery utility).</run>
      <expect>Output format clearly distinguishes both classes; reader can scan for `[SPECULATIVE]` prefix.</expect>
    </step>
    <step>
      <run>Add `--strict` flag. When set: filter out speculative results entirely AND exit non-zero if any speculative results would have been emitted (signals "no authoritative consumers found; consider manual `grep -rn`").</run>
      <expect>`comp-platinum reverse &lt;key&gt; --strict` returns 0 results + exit 2 on the AUDIT-007 case (no authoritative consumers); 1 authoritative result + exit 0 on summary.json#active_since case.</expect>
    </step>
    <step>
      <run>Empirical validation — rerun the two AUDIT-007 queries:
        (a) `comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m"` — default mode emits 0 authoritative + N speculative (current behavior preserved); --strict mode returns 0 + exit 2.
        (b) `comp-platinum reverse "platinum/advisors/{id}/summary.json#active_since"` — default mode emits 1 authoritative (AdvisorPublicProfile.tsx) + 0 speculative; --strict mode returns 1 + exit 0.</run>
      <expect>Both cases match expected output; trust boundary now explicit.</expect>
    </step>
    <step>
      <run>Regression — pick 3 known-good `comp-platinum reverse` queries from 2-week log (cases that returned correct authoritative results); rerun + verify no false-tagged speculative outputs.</run>
      <expect>Authoritative results unchanged; no regressions.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with both AUDIT-007 cases + 3 regression cases.</run>
      <expect>Clean ship; trust boundary documented.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">Per-result classification stored: `authoritative` (AST-resolved) vs `speculative` (directory-prefix/substring match).</ac>
    <ac id="2">Default output emits both classes; `[SPECULATIVE]` prefix on speculative lines; authoritative lines unchanged.</ac>
    <ac id="3">`--strict` flag filters out speculative results AND exits non-zero (exit 2) when speculative would have been emitted; "no authoritative consumers found; consider manual `grep -rn`" message printed.</ac>
    <ac id="4">AUDIT-007 case (a): `comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m" --strict` returns 0 results + exit 2.</ac>
    <ac id="5">AUDIT-007 case (b): `comp-platinum reverse "platinum/advisors/{id}/summary.json#active_since" --strict` returns 1 result (AdvisorPublicProfile.tsx) + exit 0.</ac>
    <ac id="6">3 known-good regression queries unchanged.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">
      <run>Read tool source + identify result-classification surface.</run>
      <expect>Clean refactor target.</expect>
    </phase>
    <phase id="2">
      <run>Pre-commit: 5-cell test matrix — 2 AUDIT-007 cases (default + strict modes) + 3 regression queries.</run>
      <expect>All cells produce expected output.</expect>
    </phase>
    <phase id="3">
      <run>Post-commit empirical: rerun all 5 cases; append rows to org/compiler-tools-log.md.</run>
      <expect>5/5 PASS; rows captured.</expect>
    </phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>5-cell matrix sample outputs + exit-code captures</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Improving the AST-resolution logic to reduce speculative results overall (separate scope; lower-priority since `--strict` handles the trust-boundary issue at low cost).</item>
    <item>Cache layer for comp-platinum reverse (separate optimization scope).</item>
  </out_of_scope>
</task_order>
