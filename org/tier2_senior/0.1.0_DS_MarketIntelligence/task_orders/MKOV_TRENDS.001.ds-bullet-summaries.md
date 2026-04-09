# MKOV_TRENDS.001 — DS: 3-Bullet Summary Format in Layer 3 GPT Prompt

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-mkov-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>MKOV_TRENDS</project_code>
  </metadata>

  <objective>
    Update the Layer 3 curation Lambda GPT prompt to produce exactly 3 bullet points
    per topic instead of free-form prose. Each bullet max 120 chars. Total context max ~400 chars.
    Format: "- What happened\n- Why it matters\n- What to watch"
    Add max_tokens cap to prevent runaway generation.
  </objective>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRENDS_PRD.md</ref>
  </references>

  <dependencies>None — parallel with .002 and .003</dependencies>
  <commit_pattern>feat(news): Layer 3 prompt — 3-bullet summary format</commit_pattern>
</task_order>
