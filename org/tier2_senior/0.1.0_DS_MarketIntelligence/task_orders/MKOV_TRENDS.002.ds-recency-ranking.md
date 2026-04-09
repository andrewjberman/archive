# MKOV_TRENDS.002 — DS: Recency-Weighted Trending Score

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-mkov-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>MKOV_TRENDS</project_code>
  </metadata>

  <objective>
    Steepen time decay in trending_score: today=1.0, yesterday=0.5, 2d=0.25, 3d+=0.1
    (half-life 1 day). Add recency_bonus: if >50% of articles are from last 24h,
    multiply score by 1.5x. Apply same to keyword intelligence ranking.
  </objective>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRENDS_PRD.md</ref>
  </references>

  <dependencies>None — parallel with .001 and .003</dependencies>
  <commit_pattern>feat(news): steepen trending score time decay + recency bonus</commit_pattern>
</task_order>
