# MKOV_TRENDS.005 — RD: Portal Bullet Rendering + Article Image

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-mkov-005-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.1_RD_MarketPerformance</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>MKOV_TRENDS</project_code>
  </metadata>

  <objective>
    1. Render context as bullet list (split on "- " prefix or "\n"), not prose paragraph.
    2. Replace TrendingTopicImage SVG arrow with actual article lead image (image_url
       from top_articles[0]). Fallback to colored initial avatar if no image.
    3. Verify hero card headline truncation (already fixed, just verify).
    All colors from chartColors.ts. No hardcoded hex.
  </objective>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRENDS_PRD.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.1.0_DS_MarketIntelligence" task="MKOV_TRENDS.001" status="complete">Bullet format must be live</dependency>
    <dependency agent="0.1.0_DS_MarketIntelligence" task="MKOV_TRENDS.003" status="complete">image_url must be populated</dependency>
  </dependencies>
  <commit_pattern>feat(MarketOverview): bullet summaries + article lead images in trending</commit_pattern>
</task_order>
