GOAL: Two views in AdvisorIntelligence are completely non-functional despite all upstream projects being marked complete. (1) Assets Overview 'Mix' toggle does not display -- should show asset class stacked bar (equity, fixed income, alternatives, other) in same format as NMEC/NMNC in Clients toggle. (2) Books tab 'Asset Mix' radial + 'Top Holdings' bars do not load at any drill level (firm, advisor, relationship). This thread is a diagnostic -- each agent traces their segment of the chain and identifies exactly where the break is.

ROLES:
- DS (knowledge source): Describes gold layer outputs -- what 06b and 12 produce, JSON shapes, S3 paths, field names
- AE (knowledge source): Confirms Lambda routes serve the data correctly -- HTTP status, response shape, S3 key mapping
- DE (knowledge receiver + fixer): Traces API fetch chain through TypeScript types to components, identifies wiring gaps
- RD (knowledge receiver + fixer): Identifies rendering expectations and what the components need from the data

DELIVERABLE: Thread receipt containing (1) confirmed data path from gold -> Lambda -> portal for each view, (2) exact location of every break in the chain, (3) agreed fix plan per agent.

DEFINITIONS:
- 'Mix' = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)
- 'Concentration' = breakdown by SECURITY (individual holdings ranked by market value)
- 'Other' in Mix context = residual AUA not in equity/fixed_income/alternatives (primarily cash). Do NOT add 'Cash' as a separate label.

CRITICAL CONSTRAINT: Do NOT assume data is missing. The gold rerun completed 2026-03-20 evening. Scripts 06b + 12 ran successfully. Lambda partners-api-v1.8.0 is deployed with all routes. The break is MOST LIKELY in the frontend wiring or a shape mismatch between Lambda response and TypeScript types. Verify before declaring anything missing.
