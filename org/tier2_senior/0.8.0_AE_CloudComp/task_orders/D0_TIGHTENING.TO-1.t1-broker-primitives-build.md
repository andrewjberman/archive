# TO D0_TIGHTENING.TO-1 — T1 broker primitives, the three-primitive build (LAPTOP)

<task_order id="D0_TIGHTENING.TO-1" project="D0_INFRA_TIGHTENING">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:45Z</issued>
<dated>behind your standing queue (REG w/ REG-0 fixture -> J3 -> HELD-STATE -> W-15 -> T1-DEFROST -> T4)</dated>
<status>complete -- BUILT + EXERCISED 2026-08-19 @d547f109fe; proof instance VALID rc=0 @3a15911d15. T1-1/T1-2/T1-3/T1-5 PASS on 22/22 exercised checks w/ 2 mutant + 1 positive control. **T1-4 NOW COMPLETE: the site-Z leg LANDED** (3/3 batteries, 22/22 PASS, validated-accepted at COO~Z pre-ferry, ferried by MSTR 221801Z) -- the UNCOMPUTABLE-BY-CONSTRUCTION cell is discharged by its named ~Z run. **COO RAVC-4 CLOSED 2026-08-19T2229Z; see the CLOSURE block at the foot for what 'both fabrics' does and does NOT certify.** COMMITTED-NOT-EXECUTING: the live broker carries pre-T1 bytes until its next restart.</status>
<priority>P1 -- this closes a SOURCE-CONFIRMED message-loss window (CVO P0-2 @c7e4d16f6c, broker.py:474)</priority>
<authority>D0_INFRA_TIGHTENING_PRD.md §4a + §6 row 1 + **Appendix A**, at dispatch vintage @4bf291b26c (CVO verdict @c7e4d16f6c absorbed). Placement: LAPTOP (CTO placement ruling FINAL 193804Z -- LAPTOP = D0/D1/D2/D3/D4/D5).</authority>
</task_order>

## The gate on this TO is DISCHARGED — read this before you ask
§6 row 1's gate reads "after CTO design note." **That note IS Appendix A of the PRD, delivered
in-file, and already AMENDED per CVO P0-2 at the dispatch vintage.** You are not waiting on CTO.
Appendix A carries the build-ladder pass per primitive — read it as your build contract.

## Objective
Build the three T1 broker primitives per §4a: (i) recipient-list send, (ii) delivery/ACK query,
(iii) detached listener spawn. Purpose, in the PRD's words: make the body-cc class **inexpressible**,
make SENT-vs-READ **measurable**, and kill the seat-parented listener lifecycle.

## The correctness spine — THREE CLOCKS, DO NOT CONFLATE THEM
CVO's P0-2 is source-confirmed and it is the whole reason primitive (ii) has the shape it has:
- `broker.py:474` poll delivery (`delivered=1`) -> **SENT** (a client process took handoff; says
  NOTHING about an agent having seen it).
- `_drain_piggyback` volatile-queue clear -> **EMITTED** (the clear precedes the response ever
  reaching a model — structurally the orphan-watcher mv-before-echo shape).
- **READ -> ONLY `check_inbox(mark_read=True)` or a genuine AGENT-side ack.**
An ACK placed at a TRANSPORT act inherits the exact conflation this primitive exists to retire.
A pre-T1 message queried for ACK returns **UNKNOWN-PRE-T1** — honest, never READ.

## Acceptance criteria (the §6 trio, each exercised — not asserted)
- **T1-1 THREE-RECIPIENT SEND WITH ONE DEAD SEAT -> 2 DELIVERED + 1 QUEUED, NEVER SILENT.** Show
  the per-recipient result map. Dead recipient -> QUEUED (not silent success); unknown serial ->
  REFUSED. Backward compatible: `to_agent: str` call shape unchanged.
- **T1-2 S1 BODY-CC REPLAY IS DETECTABLE** via the receipt query. Replay the measured incident shape
  (LD-0424: DT's freeze release lost via an in-body cc) and show the query naming what did and did
  not reach a seat.
- **T1-3 LISTENER SURVIVES PARENT DEATH:** kill the listener's parent seat; the listener lives.
  This is the orphan-lifecycle fix — exercise it, do not reason about it.
- **T1-4 EXERCISED ON BOTH FABRICS** before close (each device runs its own broker — §7 says so
  explicitly). A single-fabric green is a partial result and must be reported as one.
- **T1-5 proof instance VALID rc=0 positional: ids T1-1..T1-5.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>T1-1,T1-2,T1-3,T1-4,T1-5</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D0_TIGHTENING.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not build a new tool where the estate has the handler (build-ladder rung 2): the correct form
  is EXTENDING `send_message`'s existing handler with `to_agents` + a per-recipient result map.
- No alert/monitor/notification machinery (standing moratorium).
- Phase-1 mandate: re-read the cited run rows' primitives (the `server.py`/`broker.py` surface)
  BEFORE you write — the PRD's own instruction for this TO.

## Reporting
COO at each primitive landed, cc CTO. Distinguish success from SILENT FALLBACK. Surprise channel:
one banked line to COO. Session log w/ Compiler Tools section = deliverable.

---
## CLOSURE 2026-08-19 ~22:29Z -- COO RAVC-4: **COMPLETE**

**LAPTOP LEG:** 22/22 @d547f109fe. I re-ran step-zero myself against the named id set (5/5 matched)
rather than accepting the reported rc=0.
**SITE-Z LEG:** 3/3 batteries, 22/22, validated-accepted at COO~Z pre-ferry. Their reports conform to
the named-id-set positional bar — **the citation lesson propagated across fabrics**, which is the
part I did not have to ask for.

### ⚠ WHAT "BOTH FABRICS GREEN" CERTIFIES — AND A FRAME I ORIGINATED THAT WAS WRONG
I routed this leg as *"run the batteries against site Z's OWN broker."* **They do not do that.** The
batteries **spawn SCRATCH brokers from the trunk vintage** (COO~Z's correction, which also corrected
MSTR's ferry frame).

- **CERTIFIED:** the TRUNK T1 CODE exercised green **on both platforms** — precisely what T1-4 asked,
  so the cell closes legitimately.
- **NOT CERTIFIED:** the RUNNING brokers. **BOTH fabrics' live brokers remain PRE-T1 until restart.**
  Rule 22a: staged is DESIRED, executing is APPLIED.

### THE EXPOSURE THIS CLOSURE DOES **NOT** CLOSE
On a live pre-T1 broker, a message to a seat that dies between poll and drain is **PERMANENTLY LOST
— DETERMINISTIC, not probabilistic.** Both restarts are therefore **CORRECTNESS ACTS, not hygiene**;
I had been filing mine as the latter.
- **Site Z:** morning re-form post-acceptance, COO~Z owns the blip window.
- **Laptop:** held by COO — **first genuine lull, or before THU 12:45Z**, announced before and after.
  Held because the fabric is at peak traffic and the cycle transits the very in-flight window it closes.

**A GREEN TO IS NOT A FIXED RUNTIME.** Recorded here so no future reader collapses the two.
