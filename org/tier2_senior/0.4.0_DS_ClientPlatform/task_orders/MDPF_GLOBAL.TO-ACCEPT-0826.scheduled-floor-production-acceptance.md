# TO MDPF_GLOBAL.TO-ACCEPT-0826 — the 2026-08-26 SCHEDULED-FLOOR production acceptance for the clause-(vi) outage repair

<task_order id="MDPF_GLOBAL.TO-ACCEPT-0826" project="MDPF_GLOBAL">
<issued_to>DS-class, laptop. **DELIBERATELY SEATED TO A CLASS AND NOT TO A SESSION — see WHY THIS TO EXISTS.** Any DS lane free after 2026-08-26T13:50Z takes it; the first to ACK owns it.</issued_to>
<executor_class>DS-class</executor_class>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-25T21:4xZ</issued>
<status>ACTIVE — the READ opens 2026-08-26T13:50Z. Before that it is correctly dormant, NOT stale.</status>
<priority>P1 — this is the ONLY production evidence that tonight's repair works. Everything landed on 08-25 was ad-hoc.</priority>
<placement>LAPTOP (Rule 26).</placement>

<objective>
Read the SERVED payload after the 2026-08-26 `cron(30 13)` gold + `cron(50 13)` publish, and
determine whether the SCHEDULED chain — not a human, not an ad-hoc invoke — carried MDPF global
forward. Report PASS or FAIL with evidence. Change nothing.
</objective>

<proof_of_spec>
  <!-- Positional invocation, check the rc:
         python .tools/proof-of-spec-check.py <instance>.json ACC0826-AC1,ACC0826-AC2,ACC0826-AC3,ACC0826-AC4
       CHECK THE RC (0 VALID / 1 INVALID / 2 usage), never the output string. The 2-arg form returns
       rc=0 with COVERAGE UNCHECKED -- PASS THE IDS. (Measured tonight by 0.4.0_DS_ClientPlatform~G on
       OPAL_ADVIPOINTERS.P4-PINS-CERT-49F: bare run VALID rc=0 violations=0, criteria-fed run INVALID
       with 4 violations and 3 silent omissions. A coverage gap and a clean pass are BYTE-IDENTICAL to
       anyone who runs it the easy way.) -->
    <criterion id="ACC0826-AC1" cell_refs="ACC-a-1"/>
    <criterion id="ACC0826-AC2" cell_refs="ACC-a-2"/>
    <criterion id="ACC0826-AC3" cell_refs="ACC-b-1"/>
    <criterion id="ACC0826-AC4" cell_refs="ACC-c-1"/>
  <expected_criteria>ACC0826-AC1,ACC0826-AC2,ACC0826-AC3,ACC0826-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_GLOBAL.TO-ACCEPT-0826_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4; cells: 4; every criterion carries exactly 1 cell_ref; unmapped cells 0; untraceable criteria 0. ⛔ EACH CRITERION IS SINGLE-CELL AND SINGLE-LAYER BY CONSTRUCTION -- deliberate, per my own two-layer ruling (70416, and the candidate census at org/tier1_exec/2.0.0_SA_COO/deliverables/TWO_LAYER_CRITERION_CANDIDATE_CENSUS_20260825T2135Z.md). A bundled criterion here would score at its weakest layer and hide a satisfied check, which is exactly the defect I have now committed three times.</alignment_denominators>
</proof_of_spec>

<decomp_ref>⛔ NO DECOMP, DECLARED RATHER THAN OMITTED. This TO does not derive from an atom-decomp run: it discharges a NEVER#6-class acceptance obligation created by the 2026-08-25 clause-(vi) outage repair, whose deploy ledger is org/critical_paths/change_management/mdpf-global-coherence-clause-vi-domain-20260825.md (CLOSED @222fdf3042). The four ACC-* cell ids below are MINTED HERE for traceability and exist in NO decomp -- stated plainly so a reader does not hunt a run directory that does not exist, and so proof-of-spec alignment is checked against THIS declaration rather than against an absent artifact.
  ACC-a-1  served global `as_of_last` advanced by the SCHEDULED chain
  ACC-a-2  served global `_provenance.source_keys` names a 2026-08-25-or-later gold partition
  ACC-b-1  49financial / inflection / cottonwood move ONLY `_provenance.written_at` (leaf-field diff, denominators printed)
  ACC-c-1  the scheduled-vs-manual determination, WITH its instrument limitation stated (see the trigger.kind trap below)</decomp_ref>
</task_order>

## ⛔ WHY THIS TO EXISTS — read this before anything else

The 08-25 outage repair was verified on an **AD-HOC** invocation. **Ad-hoc artifacts are never
production evidence** (CLAUDE.md NEVER: *"An ad-hoc run is never the production path and its
artifacts are never production evidence."*). The acceptance is tomorrow's scheduled run.

That item was raised as UNOWNED **three times** on 2026-08-25 by
`0.4.0_DS_ClientPlatform~N` (71307, 71316) and `0.5.0_AE_OpalETL~B`. It was then assigned to
`1.0.0_SA_CTO`, who claimed it in 71350.

⛔ **AND THAT ASSIGNMENT WAS NOT DURABLE, WHICH `0.5.0_AE_OpalETL~B` NAMED AND WAS RIGHT ABOUT:**

> *"the 2026-08-26 13:30Z scheduled acceptance … needs a DURABLE assignment since no seat alive now
> will exist then."*

**A session cannot hold a 16-hour obligation.** Every seat that agreed to it — CTO included — will be
gone before the read opens. **The message scrolls; the artifact persists.** This TO is the carrier.
*Cost of the fix: one file. Cost of not fixing it: the single production proof of a five-day
client-facing outage repair silently goes unread.*

## THE READ — exact, so a fresh seat needs no context

**Opens 2026-08-26T13:50Z** (after `cron(50 13)` publish). Read the **SERVED** payload.

| # | Check | PASS condition |
|---|---|---|
| 1 | global `as_of_last` | `2026-08-25` **or later** |
| 2 | global `_provenance.source_keys` | names a gold partition of **2026-08-25 or later** |
| 3 | 49financial | only `_provenance.written_at` moves — no data-bearing field |
| 4 | inflection | only `_provenance.written_at` moves — no data-bearing field |
| 5 | cottonwood | only `_provenance.written_at` moves — no data-bearing field |

**Read the SERVED payload itself.** Not mtime, not object size, not `written_at`, not a producer's
self-report, not a log line saying it ran.

⛔ **CHECKS 3–5: USE A LEAF-FIELD DIFF, NEVER A RAW-BYTE `sha256`.** `1.0.0_SA_CTO` measured that a
byte compare reports a **FALSE FAILURE** on two healthy partners, because `_provenance.written_at`
legitimately moves every run. Prior-night denominators for calibration: 49financial 12,310 leaf
fields → 1 differing; inflection 12,375 → 1 differing. **Print your denominators.**

## ⛔ THE TRAP THAT WILL CATCH YOU — `trigger.kind` CANNOT ANSWER THIS QUESTION

The manifest carries a `trigger` block that **looks** like it attributes the run. **IT DOES NOT.**

```
kind = "scheduled" if event.get("source") == "aws.events" else (... "manual")
```

The classification is derived **entirely from caller-supplied payload**. Any invoker can claim any
kind — and **one already did**: the manifest under `_manifests/2026-08-24/` is stamped
`kind: scheduled` and was produced by `1.0.0_SA_CTO`'s **manual** invoke, which deliberately passed
the scheduled floor's exact production payload for fidelity. **A reader checking `trigger.kind` would
conclude the scheduled path ran on 08-25. It did not.** *(Found by `0.4.0_DS_ClientPlatform~N`, who
was one message from reporting the opposite of the truth off it.)*

⛔ **CloudTrail CANNOT SUPPLY IT EITHER.** Lambda `Invoke` is a **DATA event** and is not captured by
this trail: `0.5.0_AE_OpalETL~B` measured **0 events** with a **firing positive control of 1** on
`UpdateFunctionCode` in the same window. And every agent shares one AWS identity, so even captured
management events read `Andrew_Berman`.

**SO: THE ESTATE HAS NO SOUND INSTRUMENT FOR "WAS THIS RUN SCHEDULED OR MANUAL."** State that as a
limitation of your verdict rather than working around it.

**The one available discriminator is TIME:** if the object lands in the `13:30Z`–`13:50Z` window and
**no seat reports a manual invoke in that window**, scheduled delivery is the reasonable read.
**Ask on the broker whether anyone invoked it.** ⛔ **DO NOT INVOKE IT YOURSELF — a manual invoke in
the acceptance window destroys the only discriminator that exists.**

## WHAT EACH OUTCOME MEANS — the two failures are DIFFERENT DEFECTS

- **PASS** → the repair holds on the production path. Report it; close this TO.
- **FAIL, data did not advance** → ⛔ **the deployed fix works and the SCHEDULED PATH does not.** A
  different defect from the one closed on 08-25, and it means the repair was never actually load-bearing.
- **FAIL, a partner moved data-bearing fields** → a regression in the repair itself. Escalate loud.

**Do not remediate either.** Report to `2.0.0_SA_COO` (or the live COO/CTO), with evidence.

## GROUNDING — the state you are inheriting

- Fix deployed at hotfix pin `530ba66971`; **`D1_CATVIEWS` DELIBERATELY EXCLUDED** (`scopes_for = 0`
  in the shipped bytes, vs 5 at the fix pin — discriminating, verified on the downloaded package).
- ⛔ **`D1_CATVIEWS` IS NO-SHIP** and must not have landed before this read. It bricks the Lambda at
  import, and once un-bricked aborts all four scopes on a `$0.01` float comparison. If it HAS landed,
  **this acceptance is void** — say so and stop. (`0.4.0_DS_ClientPlatform~N` 71413/71442; COO 71450;
  CTO 71447.)
- Deploy-completion ledger for the repair: **CLOSED** `@222fdf3042`.
- The 08-25 restore act was `1.0.0_SA_CTO`'s Andrew-direct manual fire at ~19:42:5xZ — **not**
  `0.4.0_DS_ClientPlatform~N`'s 19:45:54Z run, which found byte-identical content and correctly no-op'd.
- Root cause: a coherence gate applying a test outside its domain. It refused correctly for five days
  on a signal that was real but did not mean what the gate said it meant.

## Surprise-channel posture (Andrew-direct 2026-08-25 ~20:24Z, verbatim)

> *"agents are expected to adhere to surprise-channel logic, they proceed with the task unless the
> task is untenable. if you do atom_decomp properly as you are supposed to that shouldnt be an issue."*

**The default is PROCEED.** OBSERVATION → one line to `3.0.0_SA_CVO`, cc the issuer, keep working.
BLOCKING → only if UNTENABLE. ARMED → disarm same-turn via a NAMED owner; DISARMED ≠ REMEDIATED.
**A FAIL verdict is not untenable — it is the deliverable.**
