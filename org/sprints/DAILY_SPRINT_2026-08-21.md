Today Sprint:
A single way of running every project was agreed, written into law and used the same day: register it, define its purpose, map what it touches, then task it — no building ahead of a defined task.
ETF Positioning went through that process end to end in one session: registered, defined, mapped, independently certified, and now being built by three teams in parallel.
The daily Bloomberg ETF data pull is live on the other device; first unattended run tomorrow at 7am.
The 49F advisor dashboard switch was stopped an hour before go-live: it would have cut chart history from six years to two and collapsed the state and office breakdowns. Nothing shipped; the current dashboard is untouched.
A second reason to stop, found separately: the refresh job for the new data was deliberately left off pending its activation step, so the switch would have frozen on day one. Andrew held the switch until both are fixed.
An infrastructure hazard caught before it fired: a live read permission for the advisor route was missing from code, so the next routine deployment would have broken it. Deployments to that bucket are frozen until it is written back in — one change, already specified.
Ticketing on the other device: the three approved changes went live (ticket queue and client leg, richer Teams notifications, escalation wiring) and client ticket pages were generated for all four firms.
A provenance clean-up thread was cancelled outright as not worth the effort; it restarts only as a properly defined project applied identically across all four firms.
Fabric: 462 commits by 26 agents across both devices; 10 direct decisions from Andrew recorded; one infrastructure freeze in place; no external engineering blockers.

Projects:
Item 0 – Infrastructure – New project process in law and in use; deployments now run on the device that owns the work; a live-permission drift caught and frozen before it fired; the proof-of-knowledge program passed its first 65-item gate and opened its review.
Item 1 – Model Portfolios – No movement today; waiting its turn behind the live work.
Item 2 – Advisor Intelligence – Switch held by Andrew on two conditions: close the data gaps (history, geography, office, leaderboard) and activate the refresh. Activation is fully specified and ready; geography turns out to be buildable from data we already hold. Nothing shipped.
Item 3 – Account-Level Model Overlay – No movement today; starts when 1 and 2 clear.
Item 4 – ETF "Positioning" variant – Made the session's priority. Registered, defined, mapped, certified and tasked the same day; three teams building (data producer, serving route, page flip). Ships two full ETF books now; the other two fill in automatically once the TrueShares holdings capture is approved.
Item 5 – Alt Research – No movement today.
Item 6 – Opal Analyst – No shipped change today; the other device is being put on the new process, starting with a clean register of what is actually open there (Andrew's order).
Item 7 – Opal Ticketing – Three approved changes live; client ticket pages for all four firms; escalations route to the internal ops channel; no firm sees the merged Ticket Center until rollout. Automatic replies on the thread still to come.
Item 8 – "Philosophy"/modal edits – DONE, in production, retired.
Item 9 – Tax SMA Ops – No movement today; still waiting on the Yang/Alyssa meeting.

Process:
Item 0 – Ongoing – Unblocked; one deployment freeze on the shared serving bucket until the missing permission is written back into code (same change as the ETF route).
Item 1 – ~2 weeks – Unblocked; idle today.
Item 2 – Held – Both conditions are specified engineering work; restarts on Andrew's word.
Item 3 – ~6–7 weeks – Sequenced behind 1 and 2.
Item 4 – Priority – Three teams building; first unattended data run tomorrow 7am; the serving route needs one wording amendment, then a single deployment.
Item 5 – Ongoing – Idle today.
Item 6 – Continuing – Other device; register clean-up first.
Item 7 – This week – Live; replies on the thread next.
Item 8 – DONE – Retired.
Item 9 – Assess then build – Waiting on the meeting.

Blocks:
One external: the Schwab feed on their side — affects only 49F's parity dates; unchanged today.
One for Andrew: approve the standing daily capture of TrueShares' published holdings sheet (same publisher we already read daily). It fills the two empty ETF books, and every uncaptured day is lost for good.
One for Andrew: create the ticketing email distribution list — an admin act, still outstanding.
One for Andrew, no rush: whether insurance assets get their own tracking for advisors or stay folded in with alternatives. The work is the same either way; the answer only changes what advisors see.
