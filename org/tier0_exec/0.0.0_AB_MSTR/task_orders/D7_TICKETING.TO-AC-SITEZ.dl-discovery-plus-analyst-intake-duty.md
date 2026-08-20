# TO D7_TICKETING.TO-AC-SITEZ — DL discovery (TO-A) + the Analyst intake duty (TO-C) as ONE sitez workstream (the week's flagship; routes via MSTR -> MSTR~Z)

<task_order id="D7_TICKETING.TO-AC-SITEZ" project="OPAL_TICKETING">
<issued_to>SITEZ seat via 0.0.0_AB_MSTR -> MSTR~Z (converged split @a02f9ff5a4 adjustment A: TO-A rides WITH TO-C as one workstream at the box; cross-fabric issuance never-implicit — this TO file + MSTR's bus kickoff carrying (prd=D7_TICKETING_INTAKE_PRD.md, workstream=TO-AC, head_version=@36a7fbd70e) IS the kickoff package)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:15Z</issued>
<dated>TO-A: at seat assignment (hours of work; Andrew's Q3 one-liner is its gate-out). TO-C: on TO-B + U3/U4 closures. The 07:00-ET±30m window stays light (BBG pulls); WDAC clears 08-20 07:00 before any duty-config lands.</dated>
<status>complete -- ALL FOUR TAC ROWS SATISFIED, VALIDATED AND ACCEPTED, closed 2026-08-20 ~20:55Z by 2.0.0_SA_COO~Z (TAC-row holder) on 1.0.0_SA_CTO~Z's acceptance @c9459dfa2f (msg 2887: "TAC rows close at your hold on the above ... I am holding nothing on it").
  * TAC-1 COMPLETE 2026-08-19T1931Z (@69f5f82004): DLs 49@/inflection@ measured, Cottonwood none; CVO-P0-1 verdict TO-B does-not-collapse; one-liner AT ANDREW; capability read ferried.
  * TAC-2' PASS, **PRODUCER-SCOPED** (re-scoped by pivot @c7aa4bb03a, then narrowed pre-stamp by 1.0.0_SA_CTO~Z 2762): real PROD client form submission TCK-20260820-dcec0012 (created 20:18:09.873Z) -> the 5-min SCHEDULED runner fetched it unattended (20:19:46.16Z) -> buzz POSTED to "Opal Client Tickets" (post id 1787257189440 @20:19:49.44Z, author Opal Bloomberg, deep link carries ?ticket=) -> internal claim+complete 200/200, board back to 0 open. Filed-to-buzz 99.6s. FOUR independent readbacks concurred; THREE causal controls (BG's 20:04Z count=1, the runner's own 20:14:46Z fetched=0 pass, a complete channel census of 2). 1.0.0_SA_CTO~Z's own certifying check ran on a plane none of the four readbacks touched -- the Task's cadence boundaries match the fire EXACTLY, so it was a SCHEDULED PRODUCTION fire and not an ad-hoc QA read.
  * TAC-3 SCHEDULE LANDED (build @399df8444a): task OPAL_D7_ticket_intake registered 5-min/24x7/Limited, one real fire with the Analyst seat DOWN (LastTaskResult=0), negative controls exiting distinctly. VALIDATED at 2.0.0_SA_COO~Z's own instruments (Get-ScheduledTask + ScheduledTaskInfo + runner.log, concurring leg-for-leg).
  * TAC-4 VALID (@6e5670fed2): instance at the declared path, `proof-of-spec-check.py` POSITIONAL rc=0 (4 rows, 0 violations) -- run independently at BOTH the author's seat and 2.0.0_SA_COO~Z's, each with its OWN discriminating control (rc=1 on a criterion the instance lacks). The PASS is discriminated, not an instrument that cannot fail.
  ⛔ **SCOPE CARRIED FORWARD, DELIBERATELY: the ANSWERING LIMB IS A NAMED OPEN GAP** -- the agent HEARING channel posts has no mechanism (teams-watch is chat-grain by construction), demonstrated INSIDE the test (0.0.3_BG_BBGTerminal was NOT REGISTERED at post time; the correct buzz woke nobody). Fix in flight: the channel-leg P1 at 0.5.0_AE_OpalETL~Z. **NOBODY WRITES END-TO-END until that limb has its own exercised PASS.** Two evidence narrowings folded before the close: the ASCII check passed for a mechanism that DOES NOT EXIST (observation true, attribution struck), and a 200 from opalinvest.dev is a SPA catch-all DEFAULT -- the deep link is certified to CARRY the param, NOT to RESOLVE.</status>
<priority>P1 — D7 is the week's flagship per Andrew ("water through the pipes"); TO-A's one-liner unblocks TO-B's shape and Q3's closure</priority>
<authority>D7_TICKETING_INTAKE_PRD.md §TO-A/§TO-C at dispatch vintage @36a7fbd70e (CVO P0-1 folded: the on-box capability grep IS the §6 existence check — the gateway app is not repo-resident); Andrew's four positions (v1 INTERNAL-ONLY; Opal-Analyst-on-BBG-box placement FINAL; 2PM-ET interim cutoff STANDS for ack wording; bobby involved LATER — notification set proceeds without bobby@); DEVICE_SPLIT_DECISION @a02f9ff5a4.</authority>
</task_order>

## Objective
One box-resident workstream, two sequenced legs:
- **TO-A (first, hours):** enumerate candidate DLs via Graph (read-only; the DL ADDRESS SET is
  DISCOVERED not blocked — Andrew confirms the set as a one-liner); read the gateway app-permission
  state on-box via SSM (U2); confirm the ticketing-center thread (U3 — name the team/channel or
  propose the Analyst creating one); **PLUS the CVO-P0-1 command on the same SSM trip: grep the
  DEPLOYED gateway app for any existing group/shared-mailbox read path** — that read IS TO-B's
  existence check and decides its build-vs-collapse shape. Output: the one-liner to Andrew
  (addresses + mailbox-present? + consent needs) with each fact pinned, + the capability read to
  AE + COO.
- **TO-C — RE-SCOPED BY PIVOT 2026-08-20 ~00:5xZ (Andrew-direct @c7aa4bb03a: *"run this straight
  from the dashboard, no interaction with outlook emails coming in at all, we simply have a form
  fill out in the dashboard client-facing"*; CTO~Z gate act, full re-scope record:
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_D7_TOC_RESCOPE_DASHBOARD_FORM_20260820.md`):**
  the 4.2 intake loop + SLA memory + buzz format SURVIVE; the SOURCE becomes **CLIENT-FACING
  DASHBOARD-FORM SUBMISSIONS** (no Outlook interaction; TO-B stands down, dead as a gate); the
  buzz rides the APPROVED Ticketing Center channel (his part 3). **NEW GATE SET: §7.3 authz
  design (NAMED GATE — external submitters end the internal-only write boundary; §7.3 absorbs
  the 08-12 tenant-authz finding per @a2b93df332; the resolver floor stays up until it lands)
  + U3 (confirmed via TO-A) + the 08-20 07:00 WDAC acceptance.** U4 stands as-is as caller-shape
  law; the form backend's caller shape is a §7.3 design output. The form itself is a PORTAL build
  (color law + /frontend-dev render-check binding, client-facing surface). **EXIT CRITERION
  UNCHANGED: the production-trigger decision — a REAL SCHEDULE lands (box-native scheduled-task
  class — a schedule, never an alert).** Price that decision into the leg; the 2PM-ET config
  stamps ack wording.

## Acceptance criteria
- TAC-1 (TO-A): the Andrew one-liner sent with every fact pinned (addresses / mailbox-present /
  consent needs); the on-box permission state + capability grep delivered to AE+COO; the
  ticketing-thread confirmation or proposal recorded. Existence-check discipline: on-box reads are
  the evidence; R8's repo proxy is supporting only.
- TAC-2 (TO-C) — **CONTENT REPLACED BY PIVOT @c7aa4bb03a; the ID stays stable per the
  positional-citation rule (the expected-id set TAC-1..TAC-4 is unchanged; the CONTENT versions,
  the id never does — the enum stable-PK principle). Original text ("one real DL mail -> ...")
  tested a DEAD PATH; flagged wrong-by-pivot from the COO~Z validation lane 004728Z, replacement
  adopted at the CTO~Z gate:** one real CLIENT-FACING FORM SUBMISSION -> ticket + buzz + link
  opens the board; SLA triple derivable; duty config committed on-box per the register rules.
- TAC-3 (TO-C exit): the production-schedule decision made and recorded (schedule landed, or the
  explicit exercise-only state named with its owner) — never an implicit "the loop is running".
- TAC-4 proof instance VALID rc=0 positional: ids TAC-1,TAC-2,TAC-3,TAC-4; expected values cite
  MEASURED/RULED-class rows only per the protocol vocabulary.

<proof_of_spec>
  <expected_criteria>TAC-1,TAC-2,TAC-3,TAC-4</expected_criteria>
  <instance_path>org/tier0_exec/0.0.0_AB_MSTR/deliverables/D7_TICKETING.TO-AC_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- v1 stays INTERNAL-ONLY (Andrew's position). No bobby@ in the notification set until his word.
  No alert/monitor machinery — the TO-C exit is a SCHEDULE decision by law. Graph reads only on
  the standing gateway identities; no new consent grants without the one-liner's answer.

## Reporting
COO (cc CTO, AE for the capability read) at TO-A's one-liner-sent and at TO-C's acceptance; MSTR~Z
coordinates the seat. Surprise channel: one banked line to COO via the bus. Session log with
Compiler Tools section = deliverable.

---
## OWNERSHIP BOUNDARY -- RESOLVED 2026-08-19 ~21:16Z (CTO~Z + COO~Z CONCUR IN FULL @550b20ec5b; their trunk @e0de7ff9f4)

Converge complete; **no Andrew one-liner was needed.** Recorded here because it changes WHO RULES on
this package, not merely who executes it.

- **OWNERSHIP INCLUDING GATES for D7 / D9 / D6 / D8: `CTO~Z` RULES + `COO~Z` DECOMPOSES.**
- **Laptop legs are EXECUTION PLACEMENT** -- placement of work, not ownership of it.
- **Laptop CTO narrows to CROSS-FABRIC INTERFACES.** Their prior per-row rulings on this package
  (e.g. D7-U4, D8 TO-C) **stand as HANDOFF-INPUTS at the site-Z gate**, not as the gate itself.
- **ENVELOPE REFINEMENT CONCURRED:** applies stay under **laptop apply-time mechanics**; **item
  acceptance sits at `CTO~Z`.** So the apply leg and the acceptance leg are deliberately split --
  the fabric that can apply is not the fabric that accepts, and that is the intended shape.

**PRACTICAL READ FOR THE SEAT:** route rulings and acceptance to `CTO~Z` / `COO~Z`. Laptop COO
(me) continues to cut and to carry cross-fabric sequencing, and laptop CTO answers interface
questions -- but neither is your gate for this item any more.

---
## CHANNEL FOLD -- 2026-08-20 ~20:0xZ, 2.0.0_SA_COO~Z (per CTO~Z 2647/2658)

**The channel this TO's buzz rides is CREATED.** Andrew created it at his hand ~19:2xZ; CTO~Z
verified live from the BG identity (list_channels, denominator 3 channels in the one team):

- **Artifact name: "Opal Client Tickets"** -- NOT "Ticketing Center". The TOs/PRD/SCHEDULE_DECISION
  say "Ticketing Center" as the WORKING name at approval; **records follow the ARTIFACT's name**
  (the cma/philosophy precedent). Description: "Incoming client service requests.", standard
  membership.
- **team_id:** `9c4ab816-548f-47af-913c-ad5d5086f5ad` (Opal Capital team)
- **channel_id:** `19:2e189a40973d4d7091f4dbe2689282c7@thread.tacv2`
- The runner's config keys stay `team_id`/`channel_id` (ids, not names -- a rename can never break
  the send); refuse-if-unset honored until AE~Z's registration sitting sets them (msg 2738,
  in flight). dep-1 CLOSED both directions incl. BG's exercised send (CTO~Z 2680/2682).
- TAC-3 dependency state updated in `integrations/ticketing/intake/SCHEDULE_DECISION.md` DECISION
  block, same fold. Lifecycle-v2 decomposition W-A..W-D cut same window (this commit set):
  `org/tier2_senior/0.5.0_AE_OpalETL/task_orders/D7_TICKETING.W{A,B,C,D}-SITEZ.*.md`.
