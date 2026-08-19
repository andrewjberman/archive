# TO D9_TAXSMA.TO-A-SITEZ — the Tax SMA Ops STATE ASSESSMENT (SITEZ whole-item; recon-class, one seat)

<task_order id="D9_TAXSMA.TO-A-SITEZ" project="D9_TAX_SMA_OPS">
<issued_to>site Z, seat assigned by 0.0.0_AB_MSTR~Z (recon-class, ONE seat)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:00Z</issued>
<dated>START-NOW eligible -- gates on nothing</dated>
<status>pending -- flipped by 0.4.0_DS_ClientPlatform~Z on kickoff receipt 2026-08-19T20:03Z (kickoff ferried via 0.0.0_AB_MSTR -> MSTR~Z, carrying (prd, workstream, head_version) explicitly. NEVER IMPLICIT.)</status>
<priority>P1-program. CVO's dispatch-order note names this the STRONGEST whole-item sitez candidate in the D-set: self-contained, read-only, multi-day, ZERO coupling to the 49F Friday spine.</priority>
<authority>D9_TAX_SMA_OPS_PRD.md §4.1 + §6 item 1 at dispatch vintage @fac13ccc3a (CVO verdict @3ae19879fb absorbed + the guardrail DONE-bar hardening). Placement: SITEZ, Andrew-RATIFIED ~19:3xZ ("I am find with them having D7 D9 D6") and confirmed FINAL by CTO 193804Z.</authority>
</task_order>

## KICKOFF TRIPLE (explicit, per the never-implicit law)
- **prd:** `docs/architecture/D9_TAX_SMA_OPS_PRD.md`
- **workstream:** (a) STATE ASSESSMENT — §4.1, TO-A only. NOT (b), NOT (c).
- **head_version:** `@fac13ccc3a`

## Objective — Andrew's words: "know what we've done thus far"
This is the **pre-read for the Yang/Alyssa meeting.** It is an ASSESSMENT, and its value is in being
honest about the gap between what our records claim and what is actually live.

## ⛔ EXPLICITLY NOT IN THIS TO
**No build. No migration. No AWS mutation.** Read-only throughout: repo + records + live AWS reads +
m365 SharePoint reads. If you find something broken, it is a FINDING, not a fix.

## The 7-part output contract (one document + one machine table)
1. **LIVE-TRUTH TABLE over run rows B1-B3** — per recorded claim, a deployed/exercised verdict
   (deployed bytes, last run, freshness), **with the Rule 22a layer NAMED PER ROW** (desired /
   applied / exercised). A claim verified at the wrong layer is not verified.
2. **WORKFLOW-AS-DESIGNED MAP** (intake -> generate -> human execute), **with the guardrail marked.**
3. **BUCKET/PREFIX CONFORMANCE MAP vs the 17b grammar** (run F2) — **FINDINGS ONLY, NO MOVES.** A
   non-conforming tree is not a violation and not a warrant to move anything; moving a served key is
   NEVER#3.
4. **SHAREPOINT SYNC REVIEW** — locate the Yang+Alyssa doc set (`search_site_files` /
   `read_site_file`), produce the doc-vs-built drift list.
5. **HOLE LIST + REMAINING-WORK REGISTER** (WS-remainders B2/B3 + anything new).
6. **SEAT-OR-SUPERSEDE RECOMMENDATION for TOs #42 and #48** — see the dedicated section below; this
   part has a sovereign ask attached and is not routine.
7. **THE YANG/ALYSSA MEETING AGENDA** — one page.

## ERROR CASES — both are named because both have a silent failure mode
- **m365 gateway unreachable -> the SharePoint leg is reported BLOCKED WITH THE PROBE OUTPUT, never
  silently skipped.** Reach from sitez is an OPEN capability question; if it fails, that failure is
  itself a reportable result and the leg falls back to a laptop split-leg. **Do not let an
  unreachable gateway render as an empty drift list** — an empty answer from a broken retrieval is
  the single most expensive shape in this estate.
- **A record-vs-live contradiction is RECORDED AS A FINDING (map-vs-territory), never "fixed"
  in-pass.**

## PHASE-1 MANDATE (before any writing)
`comp-estate` on the taxsma thread if it is named, else a `comp-find` census; `comp-pipescript
deployed` for the chain scripts; and a **TRIGGER CENSUS on the producer** — you must discriminate
**NEVER-LAUNCHED from STOPPED.** Build-day artifacts mimic a dead feed, and failure-vs-stopped is a
false fork; the trigger census plus a lifecycle check is what tells them apart.

⚠ **Treat every `comp-estate` topology or served-name claim as a PRIOR UNDER TEST** and ground it on
the live primitive. Its `served:` field mixes live-derived detail with snapshot prose and carries no
marker separating them.

⚠ **PRINT DENOMINATORS.** Every count you reason from carries the count of what you scanned beside
it. An ABSENCE verdict over a firm-partitioned estate must NAME THE TREE IT SEARCHED — a 404 in the
wrong bucket is not evidence of absence, it is the wrong question asked cleanly.

## PART 6 IN DETAIL — TO #42 CARRIES A SOVEREIGN ASK
**TO #42 ("TAXSMA + Opal Ticket System scoping") is an ANDREW-DIRECT that has sat PENDING 36 DAYS at
the DEAD seat `0.5.0_AE_OpalETL~A`.** All three projects + 2 stalled TOs sit at that seat.

CVO measured the trap and it is worth stating so your recommendation does not repeat it: **D9 §1
scoped out "the ticketing half (owned by D7)" while D7's PRD and run contained ZERO mentions of
TAXSMA or #42. A handoff declared in your own document does not create ownership in someone else's.**
**That half is now closed** — CTO added an explicit #42 ticketing-half acceptance to D7 at
`@fac13ccc3a`, which is your dispatch vintage.

**What remains, and what your recommendation feeds:** the DISPOSITION — *supersede-by-D7+D9* vs
*re-seat* — **is a sovereign call that goes to Andrew WITH this act.** Recommend; do not decide.
For the seat half, §7-Q3's expectation is that the assessment seat inherits, or a fresh 0.5.0-class
respawn takes it. **Execution of any re-seat routes through COO** — recommend the shape, and I
execute it.

## Acceptance criteria
- **D9A-1 ALL 7 OUTPUT-CONTRACT PARTS DELIVERED** (document + machine table).
- **D9A-2 EVERY B-ROW VERDICTED** with its Rule-22a layer named.
- **D9A-3 DENOMINATORS PRINTED** on every census/count in the deliverable.
- **D9A-4 THE SHAREPOINT LEG IS EITHER DELIVERED OR REPORTED BLOCKED WITH ITS PROBE OUTPUT** — never
  absent without explanation.
- **D9A-5 TRIGGER CENSUS DISCRIMINATES never-launched vs stopped** on the producer.
- **D9A-6 PART-6 RECOMMENDATION STATED** for #42 and #48, with the disposition ask framed for Andrew
  and the seat recommendation routed to COO.
- **D9A-7 proof instance VALID rc=0 positional: ids D9A-1..D9A-7.** Expected values cite only
  MEASURED/RULED-class run rows; INFERRED-class rows are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D9A-1,D9A-2,D9A-3,D9A-4,D9A-5,D9A-6,D9A-7</expected_criteria>
  <instance_path>(sitez trunk) deliverables/D9_TAXSMA.TO-A_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not cut or start the (c1)-(c5) build TOs. They wait for the Yang/Alyssa meeting unless Andrew
  explicitly waives (§7-Q2). **Note for when they DO cut: the (c1) daily-unattended leg now GATES on
  the guardrail test set** (deployed-bytes credential-absence + non-reachability + handoff naming)
  per CTO's D9 hardening — priced at that TO, not this one.
- No alert/monitor/notification machinery (standing moratorium).

## Reporting
COO via the MSTR ferry, at the halfway read and at delivery. Surprise channel: one banked line.
Session log with a Compiler Tools section = deliverable.
