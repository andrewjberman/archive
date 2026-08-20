# TO D7_TICKETING.TO-AC-SITEZ — DL discovery (TO-A) + the Analyst intake duty (TO-C) as ONE sitez workstream (the week's flagship; routes via MSTR -> MSTR~Z)

<task_order id="D7_TICKETING.TO-AC-SITEZ" project="OPAL_TICKETING">
<issued_to>SITEZ seat via 0.0.0_AB_MSTR -> MSTR~Z (converged split @a02f9ff5a4 adjustment A: TO-A rides WITH TO-C as one workstream at the box; cross-fabric issuance never-implicit — this TO file + MSTR's bus kickoff carrying (prd=D7_TICKETING_INTAKE_PRD.md, workstream=TO-AC, head_version=@36a7fbd70e) IS the kickoff package)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:15Z</issued>
<dated>TO-A: at seat assignment (hours of work; Andrew's Q3 one-liner is its gate-out). TO-C: on TO-B + U3/U4 closures. The 07:00-ET±30m window stays light (BBG pulls); WDAC clears 08-20 07:00 before any duty-config lands.</dated>
<status>staged -- activates at MSTR~Z's seat assignment; this TO is the durable contract, the bus message is the kickoff</status>
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
- **TO-C (on TO-B + U3/U4):** the 4.2 intake loop + SLA memory + buzz format (structured summary +
  link) as the named ticketing-center manager duty at the box-resident Analyst. **EXIT CRITERION
  INCLUDES THE PRODUCTION-TRIGGER DECISION: the v1 agent-loop is exercise-only; the chain is not
  production-reliable until a REAL SCHEDULE lands (box-native scheduled-task class — a schedule,
  never an alert).** Price that decision into the leg; the 2PM-ET config stamps ack wording.

## Acceptance criteria
- TAC-1 (TO-A): the Andrew one-liner sent with every fact pinned (addresses / mailbox-present /
  consent needs); the on-box permission state + capability grep delivered to AE+COO; the
  ticketing-thread confirmation or proposal recorded. Existence-check discipline: on-box reads are
  the evidence; R8's repo proxy is supporting only.
- TAC-2 (TO-C): one real DL mail -> ticket + buzz + link opens the board (the PRD's own acceptance);
  SLA triple derivable; duty config committed on-box per the register rules.
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
