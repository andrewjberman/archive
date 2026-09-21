# DAILY SPRINT - Friday, September 18, 2026

Written from daily_reports/data/DAILY_REPORT_2026-09-18.json (edition to 5:27 PM Eastern), so this
text and the published page say the same thing. The PAGE is the deliverable (Andrew-direct 2026-08-26).

**Text-message sign-in is live for everyone on the dashboard.**

Client reporting now serves any firm straight to the advisor's dashboard, the migration system is hours from V1, and the research APIs came back validated.

## TODAY SPRINT

Item 1 - Text-message sign-in is live for everyone - Sign-in by text-message code is live for all dashboard users; each person turns it on in their own settings. It now gates every login rather than being optional.
Item 2 - Advisors pull any firm's reporting on the dashboard - The per-firm registry is built and connected: an advisor picks the account and that firm's reporting follows. No files move between us and the firms any more.
Item 3 - Pipeline migration is hours from V1 - The migration system and the new-client setup system are hours from a finished V1, so taking on a new client becomes a standard path instead of bespoke work.
Item 4 - Research APIs validated, three builds underway - The data APIs are validated, and three builds started on top of them: scoring functions, a foreign company filings channel, and alternative data enrichment.
Item 5 - Opal Gateway renovation is underway - Expanding who can reach what, the safety limits around it, and a better index. It comes back up after the renovation.
Item 6 - Model portfolios go first through the new remediation tool - Model portfolios are the first system through the new remediation tool, and water-testing has begun.
Item 7 - Mapping the Opal guidelines to real technology activity - Cross-referencing the guidelines against what our technology and AI actually do, then writing the discovery and remediation plan.

Volume: 457 commits across 30 agents since midnight Eastern (day still open), both machines.

## DIRECTIVES (all 15, worked or not -- the absence is the signal)

- **D0 Agent Infrastructure** - Steady background work keeping the agents on both machines running to plan.
- **D1 Model Portfolios**  _(no work today)_ - No work on this directive's own items today. The model-portfolio system is the first through the new remediation tool, and that work sits under Data Pipelines.
- **D2 Advisor Intelligence**  _(no work today)_ - No work today.
- **D3 Portfolio Analytics**  _(no work today)_ - No work today.
- **D4 Positioning**  _(no work today)_ - No work today.
- **D5 Asset Management** - The research app's data APIs are validated, and three builds started on top of them: scoring, foreign company filings, and alternative data.
- **D6 Opal AI**  _(no work today)_ - No work today. The register deliberately lists no projects here yet.
- **D7 Opal Ticketing**  _(no work today)_ - No work today.
- **D8 Data Pipelines** - Model portfolios are the first system into the new remediation tool, and water-testing has begun.
- **D9 Opal Workflows** - Client reporting's per-firm registry is built and connected, so advisors pick an account on the dashboard with no files moving. The gateway's entitlements, guardrails and index are expanding.
- **D10 Partner Implementations**  _(no work today)_ - No work today. The register lists no member projects for this one.
- **D11 Substrate & Tooling** - Light background work on shared tooling.
- **D12 Platform Operations** - Text-message sign-in went live for all dashboard users. Separately, the Opal guidelines are being cross-referenced against what our technology and AI actually do.
- **D13 Design**  _(no work today)_ - No work today.
- **D14 Platform Logic** - The migration and new-client setup systems are hours from a finished V1.

## PROCESS

- **D0 Agent Infrastructure** (Steady, ok) - Background upkeep, no new items.
- **D1 Model Portfolios** (Parked, idle) - No movement; the MDPF work runs under Data Pipelines.
- **D2 Advisor Intelligence** (Parked, idle) - No movement today.
- **D3 Portfolio Analytics** (Parked, idle) - No movement today.
- **D4 Positioning** (Parked, idle) - No movement today.
- **D5 Asset Management** (Building, act) - APIs validated; scoring and data builds underway.
- **D6 Opal AI** (Empty, idle) - No movement; no member projects by design.
- **D7 Opal Ticketing** (Parked, idle) - No movement today.
- **D8 Data Pipelines** (Water-testing, act) - MDPF first through the remediation tool.
- **D9 Opal Workflows** (Two fronts, act) - Reporting registry connected; gateway renovation underway.
- **D10 Partner Implementations** (Empty, idle) - No movement; no member projects yet.
- **D11 Substrate & Tooling** (Background, ok) - Minor tooling upkeep.
- **D12 Platform Operations** (Live + scoping, act) - MFA live; compliance cross-reference underway.
- **D13 Design** (Parked, idle) - No movement today.
- **D14 Platform Logic** (Near V1, act) - V1 hours away; migration and setup both built.

## BLOCKED

None.

SOURCE: daily-sprint packet 2026-09-18 21:17Z (comp-state self-test PASS 4/4; 671 commits / 38
authors, all refs, UTC day) + commit_census and project_census 2026-09-18 --window et to 5:27 PM
Eastern, both reading 457 commits / 30 agents on ONE population, each census's series summing to
that count. Both machines' commits read from the merged git history (git log --all). The seven
sprint items are authored directly from Andrew's own end-of-day list, each grounded against its
real project before writing: MFA (D12_PHONE_OTP_ALL_AWS) -- its enforcement measured INDEPENDENTLY,
another team's automated capture lost its authenticated session to mandatory MFA today (commit
111f9b4631); client reporting and the gateway under Opal Workflows (180 commits, IRPT_BCKEND round
4 closed and NFRA_OPLGTW); pipeline migration under Platform Logic (129 commits, LGIC_ENFORCE
rounds 8-10 and LGIC_LGCTFM); research APIs under Asset Management (52 commits, AMGT_RESAPP);
MDPF water-testing under Data Pipelines; technology compliance from today's two scoping records
(ANDREW_DIRECT_20260918_1836Z_COPM_PARSE_COMPLIANCE_POLICY.md and
ANDREW_DIRECT_20260918_19xxZ_COPM_ANALYSIS_SCOPE_TECHNOLOGY_AWS_PORTAL.md). Tech Compliance is D12
on Andrew's own correction this run. Directive rows are built BY SUBTRACTION from the register, so
all 15 appear worked or not. The day is still open; this is an evening edition, not a final count.
