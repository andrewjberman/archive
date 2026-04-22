<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-001-rca</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status>
    <completed>2026-04-22</completed>
    <commit>bb823bf8</commit>
    <project_code>ADVI_STAUDT</project_code>
    <urgency>URGENT — Andrew watching. Target: root cause in 1-2 hours.</urgency>
    <supersedes>AUAGAP.002 + AUAGAP.003 (hypothesis-driven TOs withdrawn per Andrew/CTO directive)</supersedes>
  </metadata>

  <objective>
    Open-scoped root-cause investigation: AUA 2025 Q1-Q3 regression on 49F portal
    quarterly chart. DS chooses investigation path. Output: aua25q_rca.md with root
    cause confirmed, confidence level, and proposed fix scope (not the fix itself).
  </objective>

  <observation>
    Portal Advisor Intelligence AUA chart (49F, quarterly view) after the latest
    D-chain refresh shows ~70% drop in total_aua for 2025 Q1-Q3, recovering to ~$1.4B
    in Q4 2025 and growing normally into 2026. Both New Client and Existing Client
    cohorts are affected proportionally — uniform per-client AUA suppression, not a
    classification issue.

    Screenshot details:
    - Q4 2024: ~$1.4B (normal)
    - Q1 2025: $300M ($274M existing + $25.8M new, -65.7% QoQ / -$574M)
    - Q2-Q3 2025: similar low range
    - Q4 2025: ~$1.4B (recovery)
    - Q1-Q2 2026: $1.66B / $1.7B (normal)

    Chart source: D_00b.portal_timeseries.py _build_static_aua_periods, quarter-end
    snapshot of perf table, sum(total_aua).
  </observation>

  <scope>
    OPEN — DS investigates freely. No prescribed hypothesis ordering. Follow the data.

    Tools available: S3 parquet queries, git log/diff/blame, full gold/silver/bronze
    access, ad-hoc diagnostic scripts per EC2_CODE_DEPLOYMENT_STANDARD.
    No compiler-mandate gates for diagnostic-only work.
  </scope>

  <deliverable>
    File: data/black_diamond/diagnostics/aua25q_rca.md
    Content:
    - What DS actually investigated (data paths + code paths examined)
    - Evidence found (specific values, dates, deltas)
    - Root cause conclusion (one clear statement)
    - Confidence level + any residual uncertainty
    - Proposed fix scope (so COO can size the follow-up TO — not the fix itself)
  </deliverable>

  <acceptance_criteria>
    1. aua25q_rca.md committed.
    2. Root cause identified with specific evidence (not hypothesis).
    3. Proposed fix scope described (one-liner minimum).
    4. MCP CTO + COO with rca.md link + one-paragraph summary.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT implement the fix — root cause first, fix is a separate TO.</rule>
    <rule>Do NOT run gold pipeline scripts during investigation.</rule>
    <rule>AUAGAP.002 and AUAGAP.003 are SUPERSEDED — ignore them.</rule>
  </do_not>
</task_order>
