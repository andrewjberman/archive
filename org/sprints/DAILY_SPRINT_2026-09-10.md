# DAILY SPRINT - Thursday, September 10, 2026

GENERATED FROM daily_reports/data/DAILY_REPORT_2026-09-10.json, so this text and the
published page cannot disagree. The PAGE is the deliverable (Andrew-direct 2026-08-26);
this file is the text record of it.

**Spam defence is live on the website, and Investor Reporting became two funded builds in an afternoon.**

Three programs closed out, every cloud access role in the company got measured for the first time, and the research application found the pattern it needed.

## TODAY SPRINT

Item 1 - Spam submissions blocked at the website - Junk submissions were reaching the inbox. They now stop at the edge. Measuring the traffic also showed the volume was smaller than we thought, so the number is now known rather than guessed.
Item 2 - The estate change report is serving - Changes used to be reconstructed by hand after the fact. The report now states them. The first edition read thin and the content fix is in flight tonight.
Item 3 - Every cloud access role measured, first time ever - You cannot tighten access you have not measured. This is the baseline the tightening works from, and the work closed out on all three of its goals today.
Item 4 - The company data map finished its move to the cloud - Andrew called this one finished today. It rebuilds in the cloud, on schedule, with one writer.
Item 5 - The fund-screening guardrail closed out - A goal nobody exercised is not a goal that passed. Saying so is what makes the other seven mean something.
Item 6 - Investor Reporting is now two builds, both specified - Full-stack development starts now on both halves, and neither waits on the other to begin.
Item 7 - Fundamental research gets its own application - The research source we wanted was reachable all along; its credential had simply lapsed. Nothing needed inventing.

Volume: 601 commits from 46 workers, since 00:00 ET.

## DIRECTIVES

- **D0 Agent Infrastructure** - The company data map finished its move to the cloud on Andrew's word. The duplicate-key fault underneath it was settled and closed at the writer rather than patched downstream, and the settle found five colliding pairs where one had been assumed. Three older pieces of work closed out.
- **D1 Model Portfolios** - One commit. Name discovery closed; nothing else moved.
- **D5 Alternative Research** - Andrew ruled that this directive holds all of the research and analysis work, settling a scope question directly. The authenticated sign-in pattern the research application needs was found already proven twice elsewhere in the estate, so nothing needs inventing. Its credential has lapsed.
- **D8 Data Pipelines** - The fund-screening guardrail closed. Seven goals met; the two whose test run was never spent are named UNTESTED rather than quietly passed.
- **D9 Opal Workflows** - Investor Reporting was cut from one idea into two full-stack projects with a hard boundary between what the advisor sees and the machinery underneath. Both were registered and both written specs landed the same evening. Twelve outcomes between them.
- **D11 Substrate & Tooling** - The drift measure was ruled continuous rather than hand-triggered, and the reasoning behind an earlier over-broad ruling was narrowed in place rather than left standing.
- **D12 Platform Operations** - The biggest surface of the day. Every one of the 219 cloud access roles was measured against 90 days of real use, finding two thirds of granted permissions never observed in use at all; that work closed on all three of its goals. The website's spam trap went live at 11:36. The estate change report deployed and is serving, though its first edition read thin on Andrew's own read.

## PROCESS

- **D0 Agent Infrastructure** (Finished, ok) - Called finished by Andrew. One review round stays open on paperwork, not on the build.
- **D1 Model Portfolios** (Quiet, idle) - One commit, a close. No open work moved today.
- **D5 Alternative Research** (Scoping, act) - Scope settled by Andrew today. The build starts on a renewed credential.
- **D8 Data Pipelines** (Closed, ok) - Closed with two goals named untested. Saying so is what makes the other seven mean something.
- **D9 Opal Workflows** (Specs landed, act) - Both projects registered and specified today; the two build lanes are being seated now.
- **D11 Substrate & Tooling** (Running, act) - Continuous drift measurement issued; the cell was cut without waiting on a question that turned out not to gate it.
- **D12 Platform Operations** (Three fronts, act) - Access measurement closed. Spam trap armed and soaking. Change report live, content being widened tonight.

## BLOCKED

- **SmartX data channel - their keys** - Still waiting on Rodney's connection details and public key. Nothing else stands between provisioning and live data.
- **Research source credential** - The fundamental-research source needs a working sign-in. The pattern is proven; the credential itself has lapsed and needs renewing.

SOURCE: daily-sprint packet 2026-09-10 (comp-state self-test PASS 4/4; 888 commits / 52 authors all refs, both fabrics) + commit_census and project_census 2026-09-10 --window et, 601 commits / 46 workers, both censuses agreeing on the denominator
