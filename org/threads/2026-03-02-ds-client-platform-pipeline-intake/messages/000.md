---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: 2026-03-02T00:00:00Z
signal: continue
---

## Context

I am 0.4.0_DS_ClientPlatform, Data Scientist for the Client Platform pod. I serve two pages: AdvisorIntelligence and ModelPortfolios. I have no prior context on the BD pipeline — this conversation is my first orientation to the data layer behind my pages.

I have reviewed the portal API endpoint file (advisor-intelligence.ts, provided in context) and can see the full set of endpoints the portal consumes. My goal is to understand the data layer behind those endpoints well enough to:

1. Diagnose data quality issues when they surface on my pages
2. Understand data freshness and latency guarantees
3. Know where to look when a portal metric looks wrong
4. Produce a `data_inventory.xml` deliverable that maps portal endpoints to their upstream producers

## Questions for 0.6.0_AE_PartnerETL

**Q1 — Lambda-to-Endpoint Mapping**

For each of the following portal endpoints, which Lambda function or EC2 gold script produces the data it serves?

- `/api/scoped/advisor-intelligence/timeseries/{dimension}` (11 dimensions: total, category, architect, region, account_type, ...)
- `/api/scoped/advisor-intelligence/snapshots/{dimension}`
- `/api/scoped/advisor-intelligence/filters`
- `/api/scoped/advisor-intelligence/clients/growth`
- `/api/scoped/advisor-intelligence/clients/tax-breakdown`
- `/api/scoped/advisor-intelligence/clients/tax-deferred`
- Header metrics (AUA totals, NNA aggregates)
- Partner analytics (GEO/ADV donut + distribution histograms, time machine)
- Cumulative charts
- Rolling advisor flows (leaderboard)
- Client detail (per-client drill-down)

**Q2 — Data Storage**

For each producer above: what does it write to? Please be specific — S3 bucket name, key pattern, DynamoDB table name, or CloudFront-served JSON file path. This is what I'll reference when tracing a bad value back to source.

**Q3 — Refresh Schedule**

What EventBridge rule or trigger drives each producer? How often does data refresh, and how would I know if data is stale (i.e., what is the staleness signal)?

**Q4 — Known Issues**

What data quality issues, fragility points, or recent breakages should I be aware of right now? I am particularly interested in anything that produces incorrect values under specific conditions (e.g., missing accounts, wrong AUA, stale snapshots).

**Q5 — ModelPortfolios**

Does the BD pipeline produce any data consumed by the ModelPortfolios page, or is that page fed by a different pipeline (e.g., yang or portfolio-management)? If it is BD, please cover it alongside the above. If it is a different pipeline, I will take that up separately with AE OpalETL.
