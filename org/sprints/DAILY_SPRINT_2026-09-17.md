# DAILY SPRINT - Thursday, September 17, 2026

Written from daily_reports/data/DAILY_REPORT_2026-09-17.json (edition to 7:15 PM Eastern), so this
text and the published page say the same thing. The PAGE is the deliverable (Andrew-direct 2026-08-26).

**Six fronts moved at once today, and phone sign-in is about to go live.**

The research app's API build kept pace, the tool index got a second look, and the first real taxonomy-remediation run landed clean.

## TODAY SPRINT

Item 1 - Text-message sign-in is going live shortly - Phone-based MFA moved from design to almost-live, closing the daily-sign-in-code complaint the platform team found and queued this week.
Item 2 - Produced the Opal AI cost/compliance slides - A deck showing what Claude actually costs against what it delivers, built from both machines' real usage: 70 projects attributed, one shared method, cross-checked twice.
Item 3 - The research application's API build continues - Round thirteen's adapter work landed, including closing a real gap: five orders' live checks had never actually been authenticating, now failing closed instead of passing open.
Item 4 - First real taxonomy-remediation run landed clean - The legacy-transform tool's first production run found one storage location that needs moving, registered it, expected complete within 24 hours.
Item 5 - Working with Alyssa to design the YCharts approach - YCharts data is already live in the platform; today's work designs how it should be pulled and used going forward, with the research team that uses it daily.
Item 6 - The Opal MCP tool index is being revisited - Ten of ten outcomes confirmed for how the Opal-wide Claude plugin's tool index will work: one shared catalog, one entry per tool.

Volume: 288 commits across 37 agents since midnight Eastern (day still open), both machines.

## DIRECTIVES (all 15, worked or not -- the absence is the signal)

- **D0 Agent Infrastructure** - Steady background work keeping both machines' agents running to plan.
- **D1 Model Portfolios**  _(no work today)_ - No work today.
- **D2 Advisor Intelligence** - Started designing the YCharts data approach with our research team.
- **D3 Portfolio Analytics**  _(no work today)_ - No work today.
- **D4 Positioning**  _(no work today)_ - No work today.
- **D5 Asset Management** - The research application's API build continued in round thirteen, including closing a real authentication gap on five orders.
- **D6 Opal AI**  _(no work today)_ - No work today.
- **D7 Opal Ticketing**  _(no work today)_ - No work today.
- **D8 Data Pipelines**  _(no work today)_ - No work today.
- **D9 Opal Workflows** - The Opal-wide Claude plugin's tool index was revisited: ten outcomes confirmed for one shared catalog.
- **D10 Partner Implementations**  _(no work today)_ - No work today. The register lists no member projects for this one.
- **D11 Substrate & Tooling**  _(no work today)_ - No work today.
- **D12 Platform Operations** - Text-message sign-in is going live shortly, ending the daily re-authentication complaint.
- **D13 Design** - Background work continued on the portal rebrand.
- **D14 Platform Logic** - The legacy-transform tool's first real run landed clean on real data, finding and registering one remediation, expected complete within 24 hours.

## PROCESS

- **D0 Agent Infrastructure** (Steady, ok) - Background upkeep, no new items.
- **D1 Model Portfolios** (Parked, idle) - No movement today.
- **D2 Advisor Intelligence** (Designing, act) - YCharts solution design with research team.
- **D3 Portfolio Analytics** (Parked, idle) - No movement today.
- **D4 Positioning** (Parked, idle) - No movement today.
- **D5 Asset Management** (Round 13, act) - API build continues; auth gap closed.
- **D6 Opal AI** (Parked, idle) - No movement today.
- **D7 Opal Ticketing** (Parked, idle) - No movement today.
- **D8 Data Pipelines** (Parked, idle) - No movement today.
- **D9 Opal Workflows** (Outcomes confirmed, act) - Tool-index outcomes set; build next.
- **D10 Partner Implementations** (Empty, idle) - No movement today. No member projects yet.
- **D11 Substrate & Tooling** (Parked, idle) - No movement today.
- **D12 Platform Operations** (Near-live, act) - Text-message sign-in going live shortly.
- **D13 Design** (Continuing, act) - Portal rebrand background work.
- **D14 Platform Logic** (First run, act) - First real remediation run clean; one found, 24h to complete.

## BLOCKED

None.

SOURCE: daily-sprint packet 2026-09-17 23:14Z (comp-state self-test PASS 4/4; 366 commits / 40
authors, all refs, UTC day) + commit_census and project_census 2026-09-17 --window et to 7:15 PM
Eastern, 288 commits / 37 agents, both censuses agreeing on the denominator and cross-checked
against each other. Both machines' commits read from the merged git history (git log --all). The
six sprint items are authored directly from Andrew's own end-of-day list, each grounded against its
real project and evidence before writing: MFA/OTP (D12_PHONE_OTP_ALL_AWS), the cost deck
(org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/CLAUDE_COST_REPORT_20260917/ plus this fabric's own
per-project attribution), AMGT_RESAPP round 13, the LGIC_LGCTFM first real run (commit 53d59778a1,
one new ADVI_FIRMBKTS remediation registered), the YCharts design work with Alyssa Keith, and
NFRA_MCPINDEX's ten confirmed outcomes (org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md).
The day is still open; this is an evening edition, not a final count.
