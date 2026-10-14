<task_order id="NFRA_CTLPLN.TO-CT-ac-5.dell1-restart-mid-round-fwd11">
<to_id>NFRA_CTLPLN.TO-CT-ac-5.dell1-restart-mid-round-fwd11</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-13</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>EXERCISE</proof_genre>
<round>1</round>
<workstream>RESTART</workstream>

<title>NFRA_CTLPLN RESTART CT-ac-5 (FWD-11): record dell1's state before and after the deliberate restart window of Wed 2026-10-14 05:15-05:30Z, so the next person can say which round was where and that nothing was lost or redone -- the restart itself is the dell1 manager's act</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round13.md</decomp_doc>
<owned_cells>CT-ac-5</owned_cells>
<decomp_context>FWD-11 (PRD v0.30, card byte-unchanged): "A box can restart in the middle of a round and nothing is lost"; DONE WHEN "EXERCISED -- one box restarted mid-round, and the round finished"; ACCEPT "after any one box restarts, the next person to look can say which round was where, and the round finishes without work being redone or lost". Andrew, 2026-10-13 ~14:3xZ (record org/tier1_exec/2.0.0_SA_COO~C/deliverables/ANDREW_DIRECT_20261013_143xZ_NFRA_CTLPLN_ROUND12_CALLS_ANSWERED.md): "Yes sure" to one deliberate dell1 outage, at most 15 minutes, its manager parking the seats first, a time announced in advance. The window and the seat were named by 1.0.0_SA_CTO~DELL1 (msg 5262, relayed by 0.0.0_AB_MSTR msg 108944): this seat, re-seated for the FWD-11 and FWD-9 orders only; FWD-11 05:15-05:30Z; if it slips, the next quiet slot is 06:15-06:45Z. The window avoids dell1's fixed work (23:00Z BD fire, 02:30Z Yahoo run, 04:00Z fallback, 04:30Z read, 12:30Z RESAPP snapshot, 13:00Z site Z publish). 0.0.0_AB_MSTR~DELL1 announces at least an hour ahead, parks dell1's live seats first, performs the restart and re-seats you. You do NOT restart anything.</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-13 ~23:0xZ; gate limb: none graded this modification) -- THE WINDOW MOVED. The dell1 CTO (tick 4 on call 5263, relayed by 0.0.0_AB_MSTR msg 108977) CANCELLED the 05:15-05:30Z window: dell1 has no auto-logon and Andrew's console sign-in after each restart is his act (no auto-logon will be set). The FWD-11 window is now Wed 2026-10-14 14:30-14:45Z, after RESAPP's 12:30Z snapshot, the 13:00Z site Z publish and CANON's 13:30Z fire. 0.0.0_AB_MSTR~DELL1 announces by about 13:30Z and restarts ONLY if Andrew is at the box; if not, it slips to the next hour he is. Wherever this order says "05:15-05:30Z" read "the window the manager announces" (14:30-14:45Z as booked), and wherever it says "before 06:45Z" read "within 90 minutes after the restart". This seat stays UNSEATED until the manager seats it for this order. FWD-9's window is not an order of yours: the CTO ruled FWD-9 back to PARKED (no account held, no taker). Everything else in the order stands.
</amendment>

<amendment>
AMENDMENT 2 (booked by 2.0.0_SA_COO~C1 on the laptop's word, 2026-10-14 ~12:0xZ; gate limb: none graded this modification, no criterion changed) -- THE WINDOW REBOOKED. Andrew APPROVED the FWD-11 restart for 17:00 ET = 21:00Z today, Wed 2026-10-14, with him at the console: his express word for this ONE restart (Andrew-direct via 1.0.0_SA_CTO msg 109108, relayed by 0.0.0_AB_MSTR~DELL1 msg 5484 at 11:54Z; the laptop MSTR relay is the carrier, the 14:30-14:45Z booking of AMENDMENT 1 is superseded). Wherever this order or AMENDMENT 1 says "14:30-14:45Z" read "21:00Z, the window the manager announces". No restart before 21:00Z. The restart waits on one precondition the manager owns: the hardening read-back (AUOptions=3, Tailscale unattended) must reach cloud-local first; it is still owed, waiting on an admin paste. If the read-back is not in by 21:00Z the manager says so and the window slips; this seat's S0/S1 reads follow the manager's announcement, not the clock. S0 still comes BEFORE the seats are parked (the manager tells you), S1 within 90 minutes after the restart. Every other line of the order stands, including the bounds: this seat restarts nothing.
</amendment>

<amendment>
AMENDMENT 3 (booked by 2.0.0_SA_COO~C on the dell1 manager's relay, 2026-10-14 ~20:5xZ; gate limb: none graded this modification, no criterion changed) -- THE RESTART IS UNDATED. Andrew, verbatim at the 4.0.0_SA_CRO~DELL1 terminal ~20:49Z (relayed by 0.0.0_AB_MSTR~DELL1, MSTR msg 109244): "Dell1 Restart is being held til later, we have more work than expected that we need to get through". The 21:00Z window of AMENDMENT 2 is VOID: dell1 does not restart and parks no seats at 21:00Z. No restart without Andrew's express word, and the manager announces the new window at least an hour ahead. S0 as written at 20:15:08Z (commit 403fbe344e) is SUPERSEDED the moment a new window is set: write a FRESH S0 before the seats are parked for that window, and keep the 20:15Z file as it is. Everything else in the order stands, including the bounds: this seat restarts nothing.
</amendment>

<the_act>
1. Load `/cloud-ops`. Read this order whole. You act only on the two reads below; the restart is the manager's.
2. **S0, BEFORE the seats are parked (the manager tells you when; at the latest 5 minutes before the window opens).** Write `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-ac-5.s0.txt` holding, for dell1 only and from PUBLISHED artifacts first: (a) `git ls-remote origin box/dell1` and the local `git rev-parse HEAD`; (b) the count of local commits not on origin (`git rev-list --count origin/box/dell1..HEAD` after a `git fetch`) and the count of changed-but-uncommitted paths outside gitignored runtime files (`git status --porcelain`, count only); (c) every task order addressed to a seat that runs on dell1 whose `<status>` is not terminal, as `serial | order id | status`, read from the committed order files; (d) every open ledger entry (`org/critical_paths/.open_deploys/*.json` whose box is dell1) as names; (e) the live seats on dell1 (`python .tools/seat-liveness.py`, read-only). Commit the file and push `box/dell1` (publication is the point: a restart must lose none of it). Final line, exact form: `S0 at=<UTC> head=<10> unpublished=<n> uncommitted=<n> orders_open=<n> ledger_open=<n> seats_live=<n>`.
3. **S1, AFTER the manager has restarted and re-seated you (before 06:45Z).** Write `.../NFRA_CTLPLN.TO-CT-ac-5.s1.txt` with the same five reads. Then compute, from the two files and the committed order files: `lost` = the number of orders open at S0 that are absent at S1 with no completing commit (a missing order); `redone` = the number of orders whose id was issued or executed again after S0 (the same `issued_to` + order id appearing twice in new commits, or a ledger entry opened a second time under the same name); `unpublished_lost` = S0 unpublished commits that are not reachable after the restart (`git cat-file -e` each hash S0 listed; if S0 listed none, 0). Write `.../NFRA_CTLPLN.TO-CT-ac-5.restart-record.txt` ending with these lines, exact form: `S1 at=<UTC> head=<10> unpublished=<n> uncommitted=<n> orders_open=<n> ledger_open=<n> seats_live=<n>`, then `RESTART-RECORD window=<UTC>/<UTC> lost=<n> redone=<n> unpublished_lost=<n> uncommitted_s0=<n> uncommitted_s1=<n>`. An uncommitted path that did not survive the restart is a finding, not a failure: list the count and say so.
4. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1: the two final lines of each file and the record. Close your ledger entry if you opened one. Stand-down after the FWD-9 order, as the dell1 CTO ruled.
</the_act>

<bounds>
- Read-only except the files named above and `git push` of `box/dell1` carrying them (box/dell1 only, never CLOUD). No restart, no kill, no service stop or start, no seat spawn, no change to any variable, scheduled task or file outside the deliverables folder. If S0 cannot be written before the manager parks the seats, say so and do not backfill it from memory. Counts, names and hashes only; no secret value.
</bounds>

<proof_of_spec>
<criterion id="CTac5-AC1" cell_refs="CT-ac-5"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-ac-5.restart-record.txt</invocation><expect>lost=0 redone=0 unpublished_lost=0</expect></criterion>
<criterion id="CTac5-AC2" cell_refs="CT-ac-5" judgment="true"/>
</proof_of_spec>
<expected_criteria>CTac5-AC1,CTac5-AC2</expected_criteria>
`CTac5-AC2` (JUDGMENT, graded by `3.0.0_SA_CVO~L`, never self-graded; record it UNVERIFIABLE-BY-INSTRUMENT with a `status_reason` naming the CVO): reading only S0, S1 and the record, can the next person say which dell1 round was where before the restart and where it stands after, without asking anyone; and, read from git at the CVO's chosen later time, did an order open at S0 reach its next cell close without being redone?
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-ac-5.dell1-restart-mid-round-fwd11.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTac5-AC1,CTac5-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: RUN -- denominator dell1's fixed fires named in decomp_context (23:00Z BD, 02:30Z Yahoo, 04:00Z fallback, 04:30Z read, 12:30Z RESAPP, 13:00Z site Z); the window 05:15-05:30Z overlaps none; BLIND: a fire added after this order is cut (the manager's announcement re-checks).
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- an S0 written after the seats were parked (the bound: say so, never backfill); a `redone` count taken from memory instead of the committed order files; a restart done by this seat (forbidden); BLIND: work held only in a seat's context, which no file records (the record names it as outside the counts).
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, and the surprise channel.
</preflight>

Base checks: CTac5-AC1 base: FAIL as expected (the record does not exist); AC2 is a judgment.
Source: PRD v0.30 FWD-11; Andrew ~14:3xZ "Yes sure"; dell1 CTO msg 5262 via MSTR msg 108944.
</task_order>
