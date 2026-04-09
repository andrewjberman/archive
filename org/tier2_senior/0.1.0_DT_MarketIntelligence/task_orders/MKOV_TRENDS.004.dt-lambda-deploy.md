# MKOV_TRENDS.004 — DT: Deploy Lambda + Container (Bullet Summaries + Recency)

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-mkov-004-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DT_MarketIntelligence</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>MKOV_TRENDS</project_code>
  </metadata>

  <objective>
    Deploy updated news-trending-analysis Lambda (recency changes from .002).
    Deploy Layer 3 container image (bullet summaries from .001).
    Follow Lambda Deployment Protocol.
  </objective>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRENDS_PRD.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.1.0_DS_MarketIntelligence" task="MKOV_TRENDS.001" status="complete"/>
    <dependency agent="0.1.0_DS_MarketIntelligence" task="MKOV_TRENDS.002" status="complete"/>
  </dependencies>
  <commit_pattern>deploy(news): trending analysis Lambda + Layer 3 container</commit_pattern>
</task_order>
