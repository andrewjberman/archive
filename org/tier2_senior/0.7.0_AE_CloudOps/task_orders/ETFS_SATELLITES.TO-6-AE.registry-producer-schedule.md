# TO ETFS_SATELLITES.TO-6-AE — the SCHEDULE for the satellites registry producer (`T5DS-AC6`, lifted to its own lane)

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — cell `SAT-a-4` (delivery form / the served block), INFRA HALF. The producer half is discharged under `ETFS_SATELLITES.TO-5-DS`.</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). This TO carries NO new cell — it lifts an existing criterion (`T5DS-AC6`) out of a DS-lane TO into the lane Rule 13 assigns it to. No re-certification is sought because no cell is added.</certification>
<issued_to>0.7.0_AE_CloudOps~S</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED 2026-08-28 ~01:0xZ by `0.0.0_AB_MSTR~Z` (pre-flight 1pt CLEAR / 1c 7-of-16 / 1d 0 open TOs). ⛔ **GATED ON `ETFS_SATELLITES.TO-5-DS` AC2** — there is nothing to schedule until a producer exists and has written once. Do NOT build the trigger against an absent producer.</seating_trigger>
<placement>SITE Z — D4 is SITEZ-placed until the project is done (Andrew-direct 2026-08-24, VERBATIM: *"keep D4 on sitez until the project is done"*).</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:0xZ</issued>
<status>ACTIVE — gated on TO-5-DS AC2, which is RULED OPEN (`cooZ_ETFS_SATELLITES_TO5DS_AC2_RULING_20260828.md` @674501d4b4).</status>
<priority>P1 — `T5DS-AC6` is one of the six criteria on D4's critical-path TO, and it is the ONLY one no DS lane can discharge.</priority>
<authority>CLAUDE.md Rule 13 (infra / PROD triggers are the AE/DT lane, not DS) · CLAUDE.md §5 (*"Ad-hoc gold runs are PERMITTED FOR QA; production pipelines MUST be scheduled — success-of-upstream as the only trigger is a defect"*) · NEVER#9 (`safe-apply`, never bare `terraform apply`; Terraform is the only Lambda deploy mechanism).</authority>

---

## WHY THIS TO EXISTS AT ALL

`T5DS-AC6` was written as the sixth criterion of `ETFS_SATELLITES.TO-5-DS`, a **DS-lane** TO. It says:

> **The trigger is a SCHEDULE.** Success-of-upstream as the only trigger is a defect, and an ad-hoc
> run is permitted for QA and is NEVER the acceptance.

⛔ **A DS lane cannot discharge it.** Rule 13 puts PROD triggers in the DT/AE lane. `1.0.0_SA_CTO~Z`
named this in the handoff @`9728617de3` as *"the real gap — it has no lane at all."* This TO gives it
one. **Nothing about the criterion is changed; only its lane.**

## THE OBJECTIVE

Give the satellites registry producer built under `TO-5-DS` a **scheduled trigger**, applied through
Terraform, and demonstrate it fired **on its own schedule**.

## WHAT YOU ARE SCHEDULING

The producer that writes `platinum/satellites/registry.json` into the **firm's** bucket —
`opal-data-cot` for Cottonwood. ⛔ **NO firm segment in the key: the firm IS the bucket.**

## ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T6AE-AC1` | **The trigger EXISTS as a SCHEDULE, in Terraform.** ⛔ **`DESIRED ≠ APPLIED ≠ EXERCISED`** — a committed `.tf` block is DESIRED and nothing more. Cite the resource by `file:line @ <commit-ish>`. ⛔ **NEVER bare `terraform apply` — `safe-apply` only.** | `SAT-a-4` | |
| `T6AE-AC2` | **APPLIED — read back from the live plane, not from the plan.** ⛔ **EventBridge Rules and Scheduler are TWO PLANES and `list-rules` structurally cannot see a Scheduler schedule.** Census **BOTH** APIs and **PRINT BOTH DENOMINATORS**; name which plane carries this trigger. | `SAT-a-4` | |
| `T6AE-AC3` | **EXERCISED — it FIRED ON ITS OWN SCHEDULE.** ⛔ **An ad-hoc invocation does NOT discharge this, and neither does a successful apply.** Evidence must distinguish a scheduled fire from a manual one — the artifact's `LastModified` (UTC, `s3api`) aligned to the schedule, plus the invocation record. ⛔ **The QA write authorized under AC2 of `TO-5-DS` carries `provenance: ad-hoc-QA` and is EXPLICITLY NOT evidence here.** | `SAT-a-4` | |
| `T6AE-AC4` | **Success-of-upstream is NOT the only trigger.** If the design chains off an upstream success, state the independent schedule that also fires it. *A pipeline whose only trigger is another pipeline's success is the named defect, not a design.* | `SAT-a-4` | |
| `T6AE-AC5` | ⛔ **THE EMPTY PUBLISH SURVIVES THE SCHEDULE.** `TO-5-DS` `AC3` ruled **PUBLISH THE EMPTY, NEVER DELETE THE KEY** — zero members is a steady state, not day one. Show the scheduled path does **not** skip, delete, or 404 on an empty member set. ⚠ **This is load-bearing, not belt-and-braces:** the edge synthesis was REMOVED @`24a8435642`, so a missing key now stays a **403** — indistinguishable from a refusal — all the way to the consumer. | `SAT-b-2` | |

## WHAT IS **NOT** YOURS

- ⛔ **The producer itself.** That is `TO-5-DS` at `0.4.0_DS_ClientPlatform~L`. Do not write, re-write,
  or "fix" it. If it is wrong, report — do not repair across a lane boundary.
- ⛔ **The first QA write.** Ruled and authorized separately (see `status`). It is DS's act, once.
- ⛔ **The `POSN_TENANCY.TO-4-AE` apply hold** and the **ETFS_SATELLITES PROD promote** — both HELD,
  neither is lifted by this TO.
- ⛔ **`D1_CATVIEWS` D1-i-2** (the Lambda re-pin + TF apply) is a **different project** and is seated at
  `0.7.0_AE_CloudOps~Z`. **Rule 27: one instance, one project.** Do not pick it up.

## STANDING CONSTRAINTS THAT RIDE THIS TO

- ⛔ **NO ad-hoc `mdpf` gold run before 2026-08-28 13:30Z** — it destroys `D1_CATVIEWS.TO-P1-AE` AC1's
  discriminator. Unrelated pipeline, same box; stated because the window is live.
- **NEVER** `aws lambda update-function-code` — Terraform is the only Lambda deploy mechanism.
- **NEVER** reference another firm's data from a pipeline tree — **BUCKET *or* KEY-PREFIX**.
- Open a ledger entry in `org/critical_paths/change_management/` at the start of any apply and close it
  at completion. **A confirmed deploy is never left half-landed.**

## REPORTING

Deliverable + proof instance in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~S <0.7.0_AE_CloudOps~S@opal.agent>" -F <msgfile>`
(message file written by a **non-shell** writer). Report to `2.0.0_SA_COO~Z` (issuer) with evidence;
`3.0.0_SA_CVO~Z` certifies. **Silent receipt and silent completion are both RAVC violations** — ACK on
receipt, then report.

<proof_of_spec>
  <criterion id="T6AE-AC1" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC2" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC3" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC4" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC5" cell_refs="SAT-b-2"/>
  <expected_criteria>T6AE-AC1,T6AE-AC2,T6AE-AC3,T6AE-AC4,T6AE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 2 (SAT-a-4, SAT-b-2); criteria: 5. FORWARD — 5 of 5 criteria carry >=1 cell_ref. BACKWARD — 2 of 2 declared cells reachable (SAT-a-4 from AC1/AC2/AC3/AC4, SAT-b-2 from AC5). Unmapped 0; untraceable 0. NOTE: this TO adds NO cell to the decomp — `T5DS-AC6` is lifted verbatim in substance from `ETFS_SATELLITES.TO-5-DS` into the lane Rule 13 assigns it, and AC5 restates that TO's ruled AC3 as a survival condition on the scheduled path rather than as a new requirement.</alignment_denominators>
</proof_of_spec>
