# MKOV_TRENDS.003 — DS: Article og:image Extraction

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-mkov-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>MKOV_TRENDS</project_code>
  </metadata>

  <objective>
    Extract og:image from each article URL during news ingestion or Layer 3 curation.
    Populate image_url field on TrendingTopic from the lead article's OG image.
    The trending topics JSON already has an optional image_url field — populate it.
  </objective>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRENDS_PRD.md</ref>
  </references>

  <dependencies>None — parallel with .001 and .002</dependencies>
  <commit_pattern>feat(news): extract og:image for trending topic lead articles</commit_pattern>
</task_order>
