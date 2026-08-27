<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-R3R10</id>
<title>Closure rows 3 + 10 — CONTRACT C3 (gold-row change → platinum publish, non-blocking, idempotent under stream fan-out) and THE SCHEDULED FLOOR (Door-6 retained as accelerator, deferral retries-or-records). Plus the manifest wiring.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. Rows 1–12 true = MDPF CLOSES.</workstream>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:32Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_CHANNEL_INDEPENDENCE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD @eaa8433547 §2.2/§2.3, §3a rows 3 + 10. Respawned by MSTR with a **mandatory handoff-read launch step** (Andrew-direct) — your prior session's operational judgement is why you are here rather than a fresh lane.</authorization>

<references>
  <ref type="prd">PRD §2.2 (C3), §2.3 (the scheduled floor), §3 (manifest — you wire it, `0.7.0~A` builds it), §3a rows 3 + 10</ref>
  <ref type="input">**YOUR OWN PRIOR SESSION, and it is why CTO argued to keep you:** the Door-6 topology, the AC5 behavioural self-shutdown exercise, and the **ListBucket absent-vs-forbidden classifier defect** — all C3-adjacent</ref>
</references>

<scope>
**ROW 3 — CONTRACT C3: fires on gold-row change, publishes WITHOUT BLOCKING ON ANY PARTNER, idempotent under
stream fan-out.**
*Verified by:* mutate ONE partner's row → artifacts republish, **and the OTHER PARTNERS' VALUES ARE
UNCHANGED.** That second clause is the whole point; a republish that silently moves another partner's number
is a worse outcome than not republishing.

**ROW 10 — MDPF HAS A SCHEDULED FLOOR. Door-6 retained as ACCELERATOR. Deferral RETRIES-OR-RECORDS.**
*Verified by:* **disable the event → the floor still publishes.**

>> **YOU MEASURED THE EXACT DEFECT THIS ROW EXISTS TO KILL, TODAY.** `mdpf-daily-refresh-trigger` has
   **`ScheduleExpression: None`** — it fires only on the INF pipeline's completion marker, and CTO enumerated
   every scheduled rule in the account: **not one for MDPF.** MDPF is a passenger on an unrelated pipeline.
   When INF broke on 07-18 it froze for six days **with perfectly fresh inputs sitting unused.**
   And you found the second half: **the trigger fired at 15:01:41Z, DEFERRED on stale 49F, and when the input
   was repaired ~50 minutes later NOTHING RETRIED.** A deferred event-driven dispatch has no retry path — the
   fix and the event missed each other and nothing anywhere reported it. **"Retries-or-records" is that
   finding turned into a requirement.**

**THE MANIFEST WIRING IS YOURS; THE MANIFEST ITSELF IS `0.7.0~A`'s (row 9).** Agree the schema with them
**before either side builds against it.** A schema agreed afterwards is two lanes discovering they measured
different objects — which happened twice today.
</scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **Row 3.** *Easiest pass:* mutate a partner's row, see artifacts republish, report PASS — **without checking
  the other partners' values.** The unchanged-others clause is the row; the republish alone is not.
- **Row 3 idempotency.** *Easiest pass:* fan-out delivers twice, no error, call it idempotent. **No error is
  not "unchanged."**
- **Row 10.** *Easiest pass:* add a schedule and never disable the event. **The row's own verification is
  "disable the event → the floor still publishes"** — if you do not disable it you have not tested the floor,
  you have tested the accelerator.
- **Row 10 retries-or-records.** *Easiest pass:* implement the retry and never construct a deferral.
  **Construct one and show it either retried or recorded.** A path nothing exercises is not a path.
- **THE ONE AIMED AT YOU SPECIFICALLY:** *cite your prior session's findings as evidence a row is now TRUE.*
  Your findings establish the DEFECTS. **They cannot establish the FIXES.**
**MISSING THIRD STATE:** `true | not-yet-true | TRUE-BUT-UNEXERCISED`.
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠⚠ **THE DEPLOY LEG IS BLOCKED — AND YOU ARE THE LANE MOST LIKELY TO HIT IT.** Actions is **billing-blocked
ORG-WIDE**; `lambda-deploy.yml` and `ec2-deploy.yml` are **REFUSED AT DISPATCH** (`steps=0`, `runner=""`, no
log — you know this signature, DT positive-controlled it against a real failure). Rule 1 makes Terraform the
only Lambda mechanism.
**BUILD AND VERIFY. DO NOT LAND.** **Do NOT improvise around CI** — no console, no `update-function-code`, no
manual deploy, no re-run loop. Only Andrew clears it.
**AND THE TRAP YOU ARE BEST PLACED TO FALL INTO:** you proved this morning that a runner can be **EXECUTING
41-day-old code** invisibly to S3-layer verification. **Do not use that knowledge to justify a
deploy-around-CI path** — the lesson was *verify at the instance*, not *deploy at the instance*.
</constraint_deploy_blocked>

<compiler_tools_mandate>
  <before_write>`comp-iam service <lambda>` after any new boto3 call — **NECESSARY NOT SUFFICIENT.** For a NEW table/stream/ARN use `aws iam simulate-principal-policy`, **ONE `--resource-arns` per call**, positive control run **SEPARATELY**, `--context-entries` for any conditioned statement (Rule 22a). `comp-blast` on infra before changes.</before_write>
  <before_commit>`comp-pipescript deployed`; deploy-completion ledger opened at start.</before_commit>
  <after_commit>Session log with `## Compiler Tools`; `org/compiler-tools-log.md` in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **Row 3:** one partner's row mutated → artifacts republish **AND other partners' values byte-unchanged**,
   both demonstrated. Fan-out duplicate → row unchanged.
2. **Row 10:** the event DISABLED and the floor shown to publish anyway. A deferral CONSTRUCTED and shown to
   retry or record.
3. **Per-row verdict** from the three-state set, with the exercise that produced it.
4. Manifest schema agreed with `0.7.0~A` **in writing, before building against it.**
5. Explicit-Z; denominators; NEVER#4; ledger open-at-start, closed-on-proof **or explicitly left open with
   the billing block named** — a legitimate close-out state today.
</acceptance_criteria>

<deliverables>
  - Report at `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/`, written for CVO.
  - To CTO (gate) + COO. **Commit; do NOT push — COO is push operator (Andrew ~1600Z).**
</deliverables>

<notes>
⚠ **ROW 4 (sever-a-channel) IS `3.0.0_SA_CVO`'s, NOT YOURS.** You build C3; you must not run the exercise
that proves channels are independent. No informal partial version of it either.
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE.**
Your AC5 leg B time-trigger for tomorrow still stands and is unaffected — though note `ec2-deploy.yml` is
among the refused workflows, so check before assuming that path is available.
</notes>
</task_order>
