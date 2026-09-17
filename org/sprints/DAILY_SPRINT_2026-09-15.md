# DAILY SPRINT - Tuesday, September 15, 2026

Written from daily_reports/data/DAILY_REPORT_2026-09-15.json, regenerated 2026-09-17 after the
CLOUD<->SITEZ merge landed, so this text and the published page now count both machines' commits
from the merged git history instead of one side's own report. The PAGE is the deliverable
(Andrew-direct 2026-08-26).

**Both machines closed real work: Investor Reporting went live, and two Positioning projects closed on the second machine.**

Platform Logic's naming rules finished, MFA/OTP and opal-gateway work advanced, and Cottonwood's frozen views were fixed.

## TODAY SPRINT

Item 1 - New screens live before 9 AM Eastern - The release went live at 8:12 AM, ahead of the 9 AM target: Investor Reporting for Opal staff only, the redesigned pages, and complete asset-class figures on Positioning. Checked three ways, and on my phone.
Item 2 - Platform Logic closed two rounds today - Naming closed round three with 5 of 6 goals met, enforcement closed round one with 3 of 7, and the canon build reached 9 of 12 pieces.
Item 3 - Research app: 11 of 13 pieces in round eleven - Nearly done, and a standard score was designed for three tabs: robustness, peer valuation and model divergence.
Item 4 - Cottonwood's frozen views are current again - The category views had been stuck on September 10. A rounding check was fixed, and all four views show the latest day.
Item 5 - Agents can no longer go silent from one crash - One agent's check-in crashed and its messages were refused for about 50 minutes. It now recovers on its own.
Item 6 - Tax SMA pipeline planned to Platform Logic rules - Every storage location passed 7 of 7, live accounts key off the Traded column, and the work is planned in 27 pieces.
Item 7 - Positioning's Opal-wide book is being restored - Eight goals set and the first four orders issued on the second machine within hours. Two older Positioning projects, asset-class taxonomy and an aggregation fix opened the same day, both closed this window on the second machine. Opal staff only.
Item 8 - Every new pipeline now follows one rulebook - Approved today. Tax SMA is the first pipeline built this way; the advisor data redesign is next.

Volume: 790 commits across 66 agents since midnight Eastern, both machines, counted from the merged history.

## DIRECTIVES (all 15, worked or not -- the absence is the signal)

- **D0 Agent Infrastructure** - An agent check-in crash was fixed, and both machines' agents now work to written goals.
- **D1 Model Portfolios**  _(no work today)_ - No work today.
- **D2 Advisor Intelligence** - The advisor data redesign was written up as its own project, built to the new rules.
- **D3 Portfolio Analytics**  _(no work today)_ - No work today.
- **D4 Positioning** - The asset-class breakdown went live this morning; two Positioning projects (asset-class taxonomy, an aggregation fix opened same-day) closed on the second machine, and a new project to restore the Opal-wide book set its goals.
- **D5 Asset Management** - Round eleven of the research application reached 11 of 13 pieces, and each tab's standard score was designed. The single busiest project of the day on the second machine.
- **D6 Opal AI**  _(no work today)_ - No work today.
- **D7 Opal Ticketing**  _(no work today)_ - No work today.
- **D8 Data Pipelines** - Cottonwood's frozen category views were fixed, and the Tax SMA pipeline passed the new rules and was planned in 27 pieces.
- **D9 Opal Workflows** - Investor Reporting went live for Opal staff only, its round eight closed, and the gateway sign-in work moved forward. Opal-gateway's Schwab read-access extension and the SharePoint monthly-workbook automation both moved forward.
- **D10 Partner Implementations**  _(no work today)_ - No work today. The register lists no member projects for this one.
- **D11 Substrate & Tooling**  _(no work today)_ - No work today.
- **D12 Platform Operations** - Text-message MFA/OTP work for phone sign-in started on the second machine.
- **D13 Design** - The redesigned pages went live in this morning's release.
- **D14 Platform Logic** - Naming round three and enforcement round one closed, the canon build reached 9 of 12, and every new pipeline now follows these rules. Naming is now complete; enforcement and the canon build continue.

## PROCESS

- **D0 Agent Infrastructure** (Goals set, ok) - Agents work to written goals; crash fixed.
- **D1 Model Portfolios** (Parked, idle) - No movement today.
- **D2 Advisor Intelligence** (Brief written, ok) - Advisor data redesign scoped.
- **D3 Portfolio Analytics** (Parked, idle) - No movement today.
- **D4 Positioning** (Two projects, act) - Two Positioning projects closed; Opal-wide book started.
- **D5 Asset Management** (Round eleven, act) - 11 of 13 pieces; round twelve designed.
- **D6 Opal AI** (Parked, idle) - No movement today.
- **D7 Opal Ticketing** (Parked, idle) - No movement today.
- **D8 Data Pipelines** (Planned, act) - Tax SMA plan waits on its last sign-off.
- **D9 Opal Workflows** (Live, ok) - Investor Reporting live; round eight closed.
- **D10 Partner Implementations** (Empty, idle) - No movement today. No member projects yet.
- **D11 Substrate & Tooling** (Parked, idle) - No movement today.
- **D12 Platform Operations** (Started, act) - MFA/OTP for phone sign-in under way.
- **D13 Design** (Shipped, ok) - Redesign live in this morning's release.
- **D14 Platform Logic** (Next rounds, act) - Two rounds closed; next rounds under way.

## BLOCKED

None.

SOURCE: daily-sprint packet 2026-09-15, regenerated 2026-09-17 21:19Z (comp-state self-test PASS
4/4; 1032 commits / 71 authors, all refs, UTC day) + commit_census and project_census 2026-09-15
--window et, 790 commits / 66 agents, both censuses agreeing on the denominator and cross-checked
against each other (attributed-by-project + unattributed = total, per bin and overall). Both
machines' commits are read from the merged git history (git log --all) after the CLOUD<->SITEZ
merge (LD-0579), not from either side's own report -- the prior edition's "second machine's commits
count at the next merge" note is resolved; this is that next count.
