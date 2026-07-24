<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-R9</id>
<title>Closure row 9 — THE MANIFEST. Written every run, `skipped` + `carried_forward` populated. It is the ONLY failure surface: no SES, no alarms. Data-as-of vs process-time is binding, and EVERY publish is kept, not the latest.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. Rows 1–12 true = MDPF CLOSES.</workstream>
<issued_to>0.7.0_AE_CloudOps~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:33Z</issued_at>
<status>pending</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD @eaa8433547 §3 / §3.1 / §3.2, §3a row 9. Fresh lane — **no context to preserve, biggest new build.**</authorization>

<references>
  <ref type="prd">PRD §3 (the manifest), §3.1 (data-as-of vs process time), §3.2 (every publish), §3a row 9</ref>
  <ref type="sovereign">Andrew ~1648Z: *"there needs to be a lambda that checks gold rows for the partners / aggregate / etc whatever else it needs to produce MDPF artifact(s) and it writes a manifest json somewhere colocated and thats what we check for failures. **I do not like alarms on SES and otherwise because too often they are miscalibrated and noisey, I do not trust them.** We just need audit log json manifest at that gold-reader/platinum-publisher lambda."*</ref>
</references>

<scope>
**ROW 9 — the manifest is WRITTEN EVERY RUN, with `skipped` and `carried_forward` POPULATED.**
*Verified by:* **read it — it must explain today's state WITHOUT A HUMAN TRACING S3.** That is the acceptance
bar, and it is a usability bar, not a schema bar.

>> **YOU ARE BUILDING THE ENTIRE OBSERVABILITY STORY. THERE IS NO FALLBACK.** Andrew ruled out SES and alarms
   explicitly and gave his reason: *"too often they are miscalibrated and noisey, I do not trust them."*
   **Today is the evidence for that ruling, not an exception to it** — every alarm-shaped thing the estate
   touched today misfired: a trigger that classified an ABSENT object as an IAM fault and would have alarmed
   loud on a config problem that does not exist; a deploy-ledger RED that is permanent and known-false by
   construction; and a render that nearly shipped alarm-yellow on a state that was correct.
   **So the manifest must be readable by someone who is NOT already suspicious.** A manifest that only makes
   sense to a reader who already knows what went wrong has failed row 9.

**§3.1 — DATA-AS-OF vs PROCESS TIME IS BINDING, AND THE PRD SAYS THIS IS WHERE TODAY'S FAILURES ACTUALLY
LIVED.** Carry both, separately, always. Today's proof: `0.4.0_DS~A` measured that `_latest_date()` resolves
roster and valuation partitions **independently**, so a stamped value's as-of is *"whenever the producer last
ran"*, not the axis date it lands on — **two clocks, unbounded skew, no convention.** A manifest that reports
only process time cannot express that, and a reader would see a fresh run over stale data and call it fresh.

**§3.2 — EVERY PUBLISH, NOT THE LATEST ONE.** Immutable per-publish history. **Today's whole diagnosis
depended on retained S3 object versions**; a latest-only manifest would have made the six-day freeze
invisible in exactly the way it already was.
</scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **THE PRIMARY TRAP:** write the manifest and validate it against **your own** understanding of today's
  state. **The acceptance is that it explains the state to someone who has NOT traced S3.** Hand it to a
  reader who was not in this thread — CVO, CTO — and have them tell you what happened from the manifest
  alone. If they need a second source, row 9 is not true.
- *Easiest pass 2:* populate `skipped` and `carried_forward` with **empty arrays** on a healthy run and call
  them populated. **Construct a run where something IS skipped and something IS carried, and show the fields
  carrying it.** Empty-on-healthy is correct; empty-on-everything is an unexercised field.
- *Easiest pass 3:* emit `process_time` and treat `data_as_of` as derivable from it. **They are two clocks
  with unbounded skew** — that is the §3.1 finding, measured today.
- *Easiest pass 4:* keep the latest manifest and call the history "available in S3 versions." **§3.2 requires
  per-publish history as a first-class output**, not a property of the bucket's configuration.
**MISSING THIRD STATE:** a run is not `succeeded | failed`. It is
`published | skipped-with-reason | CARRIED-FORWARD-WITH-BASIS-AND-AS-OF`. The third is the one that makes a
continuous series honest, and it is the one a two-state manifest destroys.
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠ **GitHub Actions is BILLING-BLOCKED ORG-WIDE** — `lambda-deploy.yml` refused at dispatch; Rule 1 makes
Terraform the only Lambda mechanism. **BUILD AND VERIFY. DO NOT LAND.** Build to the gate and STOP.
**Do not improvise around CI.** Only Andrew clears it. A fresh lane under a P0 clock is exactly the profile
that invents a route — do not.
</constraint_deploy_blocked>

<compiler_tools_mandate>
  <before_write>`comp-iam service <lambda>` for any new boto3 call — **NECESSARY NOT SUFFICIENT**; for a NEW bucket/key use `simulate-principal-policy`, ONE `--resource-arns` per call, positive control run SEPARATELY (Rule 22a). `comp-which` for any search you are unsure how to route.</before_write>
  <before_commit>`.tools/commit-gate.sh` (Rule 14); `comp-blast` before deleting anything.</before_commit>
  <after_commit>Session log with `## Compiler Tools`; `org/compiler-tools-log.md` in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **A manifest that a reader who has NOT traced S3 can use to explain the state** — demonstrated by an actual
   reader, named, not by your own assessment.
2. **`skipped` and `carried_forward` EXERCISED**: a run constructed where each is non-empty, and the field
   shown carrying it.
3. **`data_as_of` and `process_time` both present, separately, on every entry.**
4. **Per-publish history**, not latest-only.
5. **Interface agreed IN WRITING with `0.7.0_AE_CloudOps` (base)** who owns the manifest WIRING — before
   either side builds against it.
6. Explicit-Z; denominators; NEVER#4.
</acceptance_criteria>

<deliverables>
  - The manifest design + implementation, and the reader test from AC-1.
  - To CTO (gate) + COO. **Commit; do NOT push — COO is push operator (Andrew ~1600Z).**
</deliverables>

<notes>
Register as `0.7.0_AE_CloudOps~A` — FULL suffixed serial. The base `0.7.0` and `~B` are both LIVE on adjacent
rows; do not take their work.
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE** — not absorbed, not parked.
</notes>
</task_order>
