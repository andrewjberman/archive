TODAY SPRINT

* Twenty-one security changes shipped today and every one of them is closed and verified. This is
  defense in depth and SOC 2 preparation, not a patch job.

* Sign-in, two-factor and encrypted storage already stood in front of the platform. Today we built
  the layers around them.

* Finished by taking one of our own defenses out of service on purpose and driving a burst of failed
  logins at it, to prove the layer underneath caught it. It did, and everything went back.

* Nine more data endpoints now check for a signed-in session at the gateway itself, so the check
  happens at the door as well as inside the room. Sixty-nine of seventy-two.

* Traffic now enters through one controlled front door and the service verifies that is where it
  came from. One more layer between the internet and anything of ours.

* A firewall now stands at all three of our entrances - dashboard, data service and the marketing
  site - sharing one block list. Block an address once and it is blocked everywhere.

* Partner advisor records and the main user directory roll back to any point in the last month,
  cannot be deleted by accident, and the core tables now sit on encryption keys we own and can audit.

* Every access log lands in one private encrypted store, with alarms on repeated failed sign-ins.
  That is the audit trail an assessor asks for, in one place instead of six.

* Brought the older portal service under proper management so every change to it is reviewable.
  Change control is its own SOC 2 line item.

* Pending my call: who gets the alert when someone hammers a login. The alarms are live; the
  recipient is one name I have not given yet.

* Spent the day running the new agent workflow at full scale on the laptop. The testing is the
  result: the structure and the way work compiles are strong, the mechanics are not.

* That gap is what we are optimizing. The concepts hold; the execution around them is where the
  time goes, and we now have a full day of evidence on exactly where.

* 558 commits across 30 agents today.


PROJECTS

* Item 0 - Agent Infrastructure (Process Management)

  Ran the new workflow end to end, at full load, for a full day, and took notes the whole way. The
  verdict is worth more than any single build: the way work is structured and compiled is genuinely
  good, and the mechanics around it are not there yet. Six specific points of friction are written
  down with what each one cost, and two are already fixed. That is the list for this week, and it
  came from running the thing rather than reviewing it.

* Item 1 - Model Portfolios: Asset-Category Views

  In production. No movement today.

* Item 2 - Advisor Intelligence

  Paused on my call. The nine briefs stay ready for the restart.

* Item 3 - Account-Level Model Overlay

  No movement today.

* Item 4 - Satellites "Positioning" Variant

  Product complete. Asset-class taxonomy is queued behind the security work.

* Item 5 - Alt Research

  Idle by design.

* Item 6 - Opal Analyst

  Idle, awaiting scope.

* Item 7 - Opal Ticketing

  Parked with planning complete. Queued to pick up after the security work.

* Item 8 - Model Portfolios Pipeline Fortification

  No movement today. The ETF coverage guardrail is specified and waiting on a team.

* Item 9 - Tax SMA Ops + YCharts

  Four pieces active, none blocked. No movement today.

* Item 10 - Global Pipeline Structure

  No movement today.

* Item 11 - Substrate/Tooling Enhancements

  The reading tools got a real workout as part of today's testing, and two of them changed as a
  result: we found cases where a tool answered a slightly different question than the one asked and
  nothing in the output said so. Those are now caught at the tool rather than by the reader.

* Item 12 - Platform Ops

  Twenty-one security changes, every one closed and verified, in a single day. The shape of it is
  defense in depth. Sign-in, two-factor and encrypted storage were already in place; today added the
  layers around them. Data endpoints now check the session at the gateway as well as inside the
  service. Traffic enters through one controlled front door and the service verifies it came from
  there. A firewall stands at all three of our entrances sharing one block list, with the marketing
  site's edge built and waiting on a DNS move. Partner advisor records and the main user directory
  gained point-in-time recovery, delete protection and our own keys. Every access log lands in one
  private encrypted store, with alarms on the login path. The older portal service is under
  management, so its changes are reviewable. And we finished by taking one defense out of service on
  purpose to prove the layer beneath it held.


PROCESS

* Item 0 - Agent Infrastructure (Process Management)
  **Timeline: Optimizing this week.**
  Status: Workflow tested at full load; friction list written from the run, two items already fixed.

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
  **Timeline: Taxonomy queued.**
  Status: Product complete; next piece waits on the security work finishing.

* Item 5 - Alt Research
  **Timeline: Ongoing.**
  Status: Idle by design.

* Item 6 - Opal Analyst
  **Timeline: Ongoing.**
  Status: Idle, awaiting scope.

* Item 7 - Opal Ticketing
  **Timeline: Next up after security.**
  Status: Parked with planning complete.

* Item 8 - Model Portfolios Pipeline Fortification
  **Timeline: Waiting on a team.**
  Status: ETF coverage guardrail specified end to end; no movement today.

* Item 9 - Tax SMA Ops + YCharts
  **Timeline: This week.**
  Status: Four pieces active, nothing blocked.

* Item 10 - Global Pipeline Structure
  **Timeline: Ongoing.**
  Status: No movement today.

* Item 11 - Substrate/Tooling Enhancements
  **Timeline: Ongoing.**
  Status: Two reading tools corrected off findings from the day's testing.

* Item 12 - Platform Ops
  **Timeline: Build complete.**
  Status: Twenty-one changes shipped, all closed and verified. Alert recipient pending my call.


BLOCKED

* SmartX data channel - public keys

  Still waiting on Rodney's public keys. Nothing else stands between provisioning and live data.

* Sign-in for the dashboard link - IT

  One mistyped setting in an app registration only LDT can edit. The no-password link covers us.

* Domain renewal - registrar access

  opalinvest.dev expires 22 December. It is now both the portal's sign-in domain and the address our
  mail sends from, so it matters more than it did. Renewal needs registrar credentials.

* Text-message sign-in codes - carrier approval

  Waiting on the phone number registration to clear the carriers. One to three weeks from filing,
  and nothing on our side moves it.
