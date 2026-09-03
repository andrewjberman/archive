TODAY SPRINT

* Two-factor sign-in is now on for every client, not just us. The rollout that started yesterday
  is finished.

* Opened our Azure account with LDT on it, so the people who run our IT can administer identity
  and devices directly.

* Specified how the portal, the website and the data service get defended at their own front
  doors, with suspicious traffic blocked on the spot and kept on file. Build starts this week.

* Ran a security review of everything we expose to the internet first, so the spec answers real
  findings rather than a checklist.

* Built out the workflow infrastructure and the schema design the agents run on: how work is
  registered, specified, decomposed and checked, in one shape end to end.

* Specified moving the data map into the cloud so it rebuilds itself overnight, and settled how
  the two machines divide work between them.

* A large pass over the internal tooling: what each tool is for, which ones earn their place, and
  repairs to the checks that had been reporting green while failing.

* Call with Canterbury next week on data infrastructure. I have opened a directive block for
  External Implementations to hold that class of work; the name is not final.

* 132 commits across 10 agents today.


PROJECTS

* Item 0 - Agent Infrastructure (Process Management)

  The busiest item today by a wide margin. Workflow infrastructure and schema design for how the
  agents operate, the cloud data map registered and specified, and a large pass over the internal
  tooling with the failing checks repaired.

* Item 1 - Model Portfolios: Asset-Category Views

  In production. No movement today.

* Item 2 - Advisor Intelligence

  Paused on my call. The nine briefs from yesterday are ready the moment it resumes.

* Item 3 - Account-Level Model Overlay

  No movement today.

* Item 4 - Satellites "Positioning" Variant

  The ETF product stays done. The coverage guardrail moved off this item to pipeline
  fortification, so this row is now clean.

* Item 5 - Alt Research

  Idle by design.

* Item 6 - Opal Analyst

  Idle, awaiting scope.

* Item 7 - Opal Ticketing

  Parked with planning complete. Resumes on the word.

* Item 8 - Model Portfolios Pipeline Fortification

  Picked up the ETF coverage guardrail and specified it through to a build plan: gaps in the
  monthly report get caught before it goes out, and anything that survives repair gets named.

* Item 9 - Tax SMA Ops + YCharts

  Four pieces active, none blocked. No movement today.

* Item 10 - Global Pipeline Structure

  No movement today. The overnight cloud rebuild specified today is registered under agent
  infrastructure.

* Item 11 - Substrate/Tooling Enhancements

  Tightened what counts as a finished record, and the tools now report their own usage so we can
  see which ones actually earn their place.

* Item 12 - Platform Ops

  Two-factor sign-in finished its rollout to every client. Separately, the security work is now
  specified end to end off a review of everything we expose, and the build starts this week.


PROCESS

* Item 0 - Agent Infrastructure (Process Management)
  **Timeline: Ongoing.**
  Status: Workflow and schema design built out; cloud data map registered; tooling pass done.

* Item 1 - Model Portfolios: Asset-Category Views
  **Timeline: Live.**
  Status: In production.

* Item 2 - Advisor Intelligence
  **Timeline: Paused on my call.**
  Status: Held. Nine briefs ready for the restart.

* Item 3 - Account-Level Model Overlay
  **Timeline: After the advisor work.**
  Status: No movement today.

* Item 4 - Satellites "Positioning" Variant
  **Timeline: Done. Taxonomy next.**
  Status: Product complete; guardrail rehoused to pipeline fortification.

* Item 5 - Alt Research
  **Timeline: Ongoing.**
  Status: Idle by design.

* Item 6 - Opal Analyst
  **Timeline: Ongoing.**
  Status: Idle, awaiting scope.

* Item 7 - Opal Ticketing
  **Timeline: On your word.**
  Status: Parked with planning complete.

* Item 8 - Model Portfolios Pipeline Fortification
  **Timeline: Build plan ready.**
  Status: ETF coverage guardrail specified end to end and registered here.

* Item 9 - Tax SMA Ops + YCharts
  **Timeline: This week.**
  Status: Four pieces active, nothing blocked.

* Item 10 - Global Pipeline Structure
  **Timeline: Ongoing.**
  Status: No movement today; the cloud rebuild is registered under agent infrastructure.

* Item 11 - Substrate/Tooling Enhancements
  **Timeline: Ongoing.**
  Status: Record standards tightened; tools now report their own usage.

* Item 12 - Platform Ops
  **Timeline: Security build starts this week.**
  Status: Two-factor rollout complete to all clients; endpoint protection specified end to end.


BLOCKED

* SmartX data channel - public keys

  Still waiting on Rodney's public keys. Nothing else stands between provisioning and live data.

* Sign-in for the dashboard link - IT

  One mistyped setting in an app registration only LDT can edit. The no-password link covers us.

* Domain renewal - registrar access

  opalinvest.dev expires 22 December. It is now both the portal's sign-in domain and the address our
  mail sends from, so it matters more than it did. Renewal needs registrar credentials.
