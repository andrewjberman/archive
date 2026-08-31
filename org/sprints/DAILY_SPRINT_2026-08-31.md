TODAY SPRINT

* A strategy day. Three new workstreams scoped, a new partner conversation opened, and the build work
  running behind them.

* Scoped a user management and MFA system for the client portal: one-time codes at login, remembered
  devices, and partner firms able to add their own users. New workstream.

* Scoped the ticketing expansion: attachments on a ticket, live chat with the client against that ticket,
  and notifications on both sides.

* Scoped one asset-class taxonomy — Fixed Income, Cash, Equity, Structured, Commodities, Alternatives —
  to be implemented across Positioning and Capital Market Assumptions.

* Opening conversations with Canterbury on data infrastructure solutions engineering and implementation.

* Expanded the substrate's stable-keying rules: a field that was never measured can no longer claim it
  was, and the fix was made at the producer rather than card by card.

* Cottonwood lost a day of model data when a vendor login expired. Recovery is authorised, and the real
  gap — nothing re-runs once the login heals itself — is now its own workstream.

* Insurance access: two permissions were declared but never applied. Found and fixed.

* 49 Financial's Monday run graded clean and matched byte for byte.

* 98 commits across 16 agents today.


PROJECTS

* Item 0 - Agent Infrastructure (Process Management)

  Two gates that were quietly wrong are now right: one was judging work against the wrong repository, the
  other was writing its own audit trail into repositories it does not own. Both repaired and proven on a
  live case. Built a mail filter that surfaces only the messages that actually need me.

* Item 1 - Model Portfolios: Asset-Category Views

  In production. No movement today.

* Item 2 - Advisor Intelligence

  49 Financial's Monday run graded clean, matching byte for byte on every account checked. A half-applied
  set of insurance permissions was caught and fixed. The Black Diamond parity run is cleared to go again
  now that the login it failed on has refreshed.

* Item 3 - Account-Level Model Overlay

  No movement today.

* Item 4 - Satellites "Positioning" Variant

  Scoped the asset-class taxonomy that becomes this item's next major body of work: one canonical order
  and colour set, defined once and consumed by Positioning and Capital Market Assumptions rather than
  each page inventing its own.

* Item 5 - Alt Research

  Idle by design while current priorities are completed.

* Item 6 - Opal Analyst

  Idle today.

* Item 7 - Opal Ticketing

  Scoped the next version: attachments stored against a ticket, chat between our team and the client saved
  to that ticket, notifications when a ticket is filed, accepted and completed, and a cleaner view of what
  is new, in progress and done. First step is a read of what we already have before anything is built.

* Item 8 - Model Portfolios Pipeline Fortification

  Cottonwood's rebalancer lost a full day when its vendor login expired mid-run. The login repaired itself
  hours later and nothing re-ran, so the day simply never existed while every check downstream read
  healthy. Recovery of that day is authorised and the underlying gap is now a named workstream.

* Item 9 - Tax SMA Ops + YCharts

  Three account-registry and roster workstreams that were running unattached are now formally under this
  item.

* Item 10 - Global Pipeline Structure

  Opened the global alarm consolidation: one assessment of every serving layer, producing a single unified
  alarm schedule instead of per-surface decisions. All new alarms hold until that plan exists.

* Item 11 - Substrate/Tooling Enhancements

  Tightened the keying rules so a value recorded as "not measured" can no longer carry a claim that it was.
  Twelve records were affected and the repair was made at the producer, not one card at a time.

* Item 12 - Platform Ops

  New. User management and MFA for the client portal is the first workstream: one-time codes by email or
  text at login, remembered devices so people are not challenged every time, a proper admin screen for
  adding users, and partner firms able to add their own people under our controls.


PROCESS

* Item 0 - Agent Infrastructure (Process Management)
  **Timeline: Ongoing.**
  Status: Two gate repairs proven on live cases; mail filter shipped.

* Item 1 - Model Portfolios: Asset-Category Views
  **Timeline: Live.**
  Status: In production.

* Item 2 - Advisor Intelligence
  **Timeline: This week.**
  Status: Monday run graded clean; insurance permissions fixed; parity run cleared to re-fire.

* Item 3 - Account-Level Model Overlay
  **Timeline: This week.**
  Status: No movement today.

* Item 4 - Satellites "Positioning" Variant
  **Timeline: Taxonomy next, after current closure.**
  Status: Asset-class taxonomy scoped; becomes the next primary series once current work closes out.

* Item 5 - Alt Research
  **Timeline: Ongoing.**
  Status: Idle by design.

* Item 6 - Opal Analyst
  **Timeline: Ongoing.**
  Status: Idle today.

* Item 7 - Opal Ticketing
  **Timeline: Scoped, starting with an architecture read.**
  Status: Next version scoped; nothing built yet, by design.

* Item 8 - Model Portfolios Pipeline Fortification
  **Timeline: This week.**
  Status: Missing day authorised for recovery; the re-run gap is a named workstream.

* Item 9 - Tax SMA Ops + YCharts
  **Timeline: Later this week.**
  Status: Three registry workstreams formally attached.

* Item 10 - Global Pipeline Structure
  **Timeline: Plan first, then a schedule.**
  Status: Alarm consolidation opened; all new alarms held until the plan exists.

* Item 11 - Substrate/Tooling Enhancements
  **Timeline: Ongoing.**
  Status: Keying rules tightened and closed at the producer.

* Item 12 - Platform Ops
  **Timeline: Scoped, ownership to be assigned.**
  Status: New item. User management and MFA scoped; which device owns it is decided after the current
  project review.


BLOCKED

* SmartX data channel - public keys

  The server is provisioned and waiting on Rodney's public keys. Nothing else stands between provisioning
  and live data.

* Sign-in for the dashboard link - IT

  The password-protected dashboard link fails on one mistyped setting in an app registration only LDT can
  edit. The no-password link covers us in the meantime.

* Positioning promote - cleared, waiting on the second site

  I signed off the condition that could not be met as written. The second site is back online after a
  restart today, so the promote can proceed there.
