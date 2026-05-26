<task_order>
<metadata>
  <to_id>YALP_MKTOVR.005</to_id>
  <project>YALP_MKTOVR</project>
  <title>Side-by-side data spreadsheet finalization — D/E/F populate from TO-004 (~1-2h)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~15:30Z addendum)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MKTOVR.md v0.4 §6 TO-005 block (CTO `1f6387616` per Andrew direct).</ref>
    <ref type="structural_skeleton">docs/briefs/yalp_mktovr_side_by_side_spreadsheet_2026-05-22.md (CTO `1f6387616`) — 60+ rows; columns A/B/C populated from TO-001 Level-1 mapping; D/E/F currently "TO-004 PENDING".</ref>
    <ref type="predecessor">TO-004 (Level-2 value comparison) + TO-VAL (consolidated deliverable) — both gate this TO.</ref>
    <ref type="andrew_quote">Verbatim 2026-05-26 ~15:30Z: "every single component that pulls data on Market Overview portal ui page and each constituent data item in said component, then I want to see the side by side values from yang pkl and ycharts" in 6-column shape.</ref>
  </references>
  <dependencies>
    <dependency>TO-004 ship + per-field yang values + YCharts values + verdicts available.</dependency>
    <dependency>TO-VAL ship (consolidated brief) — concurrent or sequential per DS 0.1.0 judgment.</dependency>
  </dependencies>
</metadata>

<scope>
Populate columns D/E/F into the CTO structural skeleton at `docs/briefs/yalp_mktovr_side_by_side_spreadsheet_2026-05-22.md`:

- **D: Yang value** — from TO-004 yang-side rendered value on T*=2026-05-22
- **E: YCharts value** — from TO-004 YCharts pull on T*=2026-05-22
- **F: Variance = E/D** — computed ratio (sign discipline for ratios where signs matter, e.g., bond returns)

For rows where Level-1 marked `n/a` (Daily Cloud / Fear & Greed / Trending Topics per PRD §7 Q1), keep D/E/F as `n/a` — those have no Bloomberg/yang/YCharts equivalent.

**DRIFT-class top-of-doc surface:** rows where `|F − 1| > MATCH-threshold` (per PRD §3.1 MATCH-tolerance) listed in a separate top-of-document DRIFT section for Andrew review.

**Output BOTH formats:**
1. CSV at `docs/briefs/yalp_mktovr_side_by_side_spreadsheet_2026-05-22.csv` (spreadsheet-tool import)
2. Refreshed markdown table at `docs/briefs/yalp_mktovr_side_by_side_spreadsheet_2026-05-22.md`
</scope>

<acceptance_criteria>
- AC1: Every skeleton row has D/E/F populated where Level-1 isn't `n/a`.
- AC2: DRIFT-class rows explicitly flagged + listed in top-of-document DRIFT section.
- AC3: CSV + markdown both shipped to same commit.
- AC4: RAVC2 to COO with delivery confirmation; CC CTO + Andrew.
</acceptance_criteria>

<expected_evidence>
- Commit hash for CSV + markdown both
- DRIFT section row count + percentage of total
- Session log
</expected_evidence>

<notes>
This is mechanical fill-in (CTO skeleton + TO-004 value+verdict outputs → populate cells). Effort ~1-2h driven by row count not analytical complexity.

**COO 3-step project-close happens AFTER this TO + TO-VAL CVO surface-pass** (COO drives per CLAUDE.md Closure Discipline). If TO-005 ships before TO-VAL, COO holds 3-step close until TO-VAL is also done.

**Andrew explicit visibility on DRIFT-class rows** per the top-of-doc surface — this is the "Andrew sovereign sees the actual variance" satisfaction of the verbatim direct 15:30Z ask.

Standing for TO-004 + TO-VAL ship signals.
</notes>
</task_order>
