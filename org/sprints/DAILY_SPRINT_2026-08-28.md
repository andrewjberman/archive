TODAY SPRINT

* Satellites is live for Cottonwood on the Positioning page: promoted to production overnight, smoke-tested on the real books, and now serving.

* Asset-Category Views is live on the Model Portfolios page: Models $1.80B and SMAs $22.79M broken down by category with drilldowns; drilldown values and frontend polish remain.

* ETFs on the Positioning page now carry a sub-sector classification, so the view reads by industry group and not only by ticker.

* This dashboard is the new home of the daily report: one link in Teams, and it picks the desktop or phone view for whoever opens it.

* The SmartX data channel is provisioned: a dedicated SFTP server stands ready and turns on the moment Rodney's public keys arrive.

* Insurance ingestion is proven end to end on the canonical data route; the only thing between it and per-advisor views is 49 Financial populating advisor keys.

* Built the internal timetable that tracks multi-period autonomous sprints, so a piece of work that runs across days reports where it stands without being asked.

* Codebase search now covers the live cloud too: raw searching is retired in favour of one tool that prints what it looked at, and it can scan every AWS resource by name.

* Opal's Azure subscription is set up and wired to our tenant; integration with LDT (Purview billing, app ownership, the sign-in fix) is scheduled for next week.

* 786 commits across 38 agents today.

PROJECTS

* Item 0 - Agent Infrastructure (Process Management)

  Three infrastructure wins. This dashboard: the daily report is rendered, published and served behind our sign-in with a device-aware view, and until IT fixes one setting the same report ships through a link that needs no password. The timetable: multi-period autonomous sprints now report progress on their own clock. The search rail: raw searching from the command line is retired, one tool answers every repo search with a printed denominator, and the same tool now scans the live AWS estate, where it surfaced 320 resources that exist in the cloud but are declared nowhere in the code.

* Item 1 - Model Portfolios: Asset-Category Views

  Live. Models $1.80B and SMAs $22.79M render by asset category with drilldowns on the Model Portfolios page, as of the 27th's data. Drilldown values and frontend polish remain; the demo follows the polish pass.

* Item 2 - Advisor Intelligence

  Insurance ingestion is proven end to end and I ruled where it lives: a function on the canonical Black Diamond data route, not a side channel. $51.8M across 102 accounts still cannot be attributed to an advisor because 49 Financial's advisor keys are empty; the capture is built and waits on that one field. The 533-day performance history rebuild continues on its checkpoints.

* Item 3 - Account-Level Model Overlay

  Foundation ready; folds in behind the Advisor Intelligence rebuild. No movement today.

* Item 4 - Satellites "Positioning" Variant

  Live. The multi-tenant Satellites view was promoted to production overnight and smoke-tested against the nine real books; Cottonwood sees its own scoped path and Opal keeps the full view. ETFs on the page now carry a sub-sector classification. The Satellites build is closed; what remains on Positioning is polish.

* Item 5 - Alt Research

  No movement today.

* Item 6 - Opal Analyst

  No movement today.

* Item 7 - Opal Ticketing

  No movement today; the weekly cadence with AJ stands.

* Item 8 - Model Portfolios Pipeline Fortification

  The SmartX data channel is provisioned: a dedicated SFTP server is up and waits only on Rodney's public keys to start receiving. Cottonwood served current again on the restored login.

* Item 9 - Tax SMA Ops + YCharts

  No movement today; tracking stays live on the expanded roster. YCharts later next week.

* Item 10 - Global Pipeline Structure

  Deliberately at rest until the product rollout completes.

* Item 11 - Substrate/Tooling Enhancements

  Opal's Azure subscription exists, is bound to our own tenant, and carries its resource group and budget; the items only IT can do (Purview billing linkage, billing ownership, app ownership, the sign-in setting) are on one list for LDT next week. The cloud inventory that powers the new AWS search is refreshed nightly with an event-driven incremental, and every result carries its own vintage.

PROCESS

* Item 0 - Agent Infrastructure (Process Management)
  **Timeline: Ongoing.**
  Status: Dashboard live; search rail live with its kill switch; timetable live.

* Item 1 - Model Portfolios: Asset-Category Views
  **Timeline: Live.**
  Status: Categorization live on Model Portfolios; drilldown values and frontend polish remain.

* Item 2 - Advisor Intelligence
  **Timeline: This week.**
  Status: Insurance ingestion proven; history rebuild running; attribution waits on advisor keys.

* Item 3 - Account-Level Model Overlay
  **Timeline: This week.**
  Status: Foundation ready; folds in behind the rebuild.

* Item 4 - Satellites "Positioning" Variant
  **Timeline: Live.**
  Status: In production for Cottonwood; sub-sector classification on ETFs; polish only.

* Item 5 - Alt Research
  **Timeline: Ongoing.**
  Status: Idle by design while current product priorities are completed.

* Item 6 - Opal Analyst
  **Timeline: Ongoing.**
  Status: Idle today.

* Item 7 - Opal Ticketing
  **Timeline: Weekly operating cadence.**
  Status: Idle today; the recurring meeting stands.

* Item 8 - Model Portfolios Pipeline Fortification
  **Timeline: On Rodney's keys.**
  Status: SmartX SFTP server provisioned; receiving starts when the public keys land.

* Item 9 - Tax SMA Ops + YCharts
  **Timeline: Later next week.**
  Status: Tracking live; YCharts held.

* Item 10 - Global Pipeline Structure
  **Timeline: After the current product rollout, Sep 2026.**
  Status: Deliberately resting.

* Item 11 - Substrate/Tooling Enhancements
  **Timeline: LDT next week.**
  Status: Azure wired on our side; IT list ready; AWS search live on the nightly inventory.

BLOCKED

* Advisor Intelligence - insurance attribution

  $51.8M of 49 Financial's insurance assets cannot be attributed to any advisor because no advisor key is populated in their Black Diamond. Ingestion is proven and idle. One question to Mike: teams or rep codes, populate whichever is theirs, and it flows with zero build.

* SmartX data channel - public keys

  The SFTP server is provisioned and waiting on Rodney's public keys. Nothing else stands between provisioning and live data.

* Sign-in for the dashboard link - IT

  The password-protected dashboard link fails on one mistyped setting in an app registration only LDT can edit. Fix is one character; scheduled with the Azure wiring next week. The no-password link covers the week.
