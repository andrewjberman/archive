# TO MDPF_REMED.RP-W4 — MIRROR FIRM SELECTOR, THEN THE RENAME (Andrew ruled route (b))

<task_order id="MDPF_REMED.RP-W4" project="MDPF_REMED">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>pending</status>
<priority>P1. Unblocked by Andrew's ruling ~2334Z ("Agree with your recs for all open calls", Call 2
= route (b); record: CTO relay 234031Z). Two steps IN ORDER — the rename is only TRUE after the
selector exists. Sequence relative to RP-W5 (your running TO) and the RP-W1/W2/W3 atomic window per
COO GO.</priority>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W4)</ref>
</references>

## SCOPE — two steps, strictly ordered
**Step (i) — ADD THE FIRM SELECTOR.** `opal-assets-ingest-mirror` currently iterates every MAP row
on every invocation (`lambda_function.py:353`; `event` is NEVER read in 469 deployed lines) and both
schedules have been observed writing the other firm's tree. Give the handler a firm/row selector
driven by the invocation payload; both existing invokers currently pass empty payloads — default
behavior with no selector present must be explicit (all-rows, unchanged) so nothing breaks before
the schedules are re-pointed.
**Step (ii) — THE RENAME.** Apply Andrew's `opal-assets-ingest-mirror-{firm}-{channel}-daily` naming
to the schedules, each passing its firm selector — the names are only then true rather than
decorative. ⇒ This also serves RP-W3: per-firm selection is what lets firms be re-timed
independently.

⚠ Do NOT fold the D-16 guard narrowing into this TO (that is RP-W5's, running). Do not move any
schedule TIME here (that is RP-W3's, atomic-gated) — this TO changes selection and naming only.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast opal-assets-ingest-mirror</run>
      <expect>Known radius (10 event rules incl. mdpf-daily-refresh-trigger, 36 IAM policies). No new consumers vs issue-date.</expect>
      <if_mismatch>STOP; surface to COO.</if_mismatch>
    </step>
    <step>
      <run>read infra/aws/terraform/opal-assets/mirror.tf directly (comp-trigger is blind to interpolated names like "${local.mirror_name}-cot-daily-et")</run>
      <expect>Both schedule resources + their input payloads enumerated at your HEAD.</expect>
      <if_mismatch>Never conclude console drift from comp-trigger on this estate; the .tf file is the ground.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>safe-commit then .tools/safe-apply.sh; Terraform only (a schedule rename may be destroy+create — state the cutover-gap plan: no skipped/double business day)</run>
      <expect>Plan scoped to selector + naming only; 0-diff post-apply; tag + push --follow-tags.</expect>
      <if_mismatch>STOP on dirty plan.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>EXERCISE: invoke with firm selector A (QA-safe) — ONLY A's rows run; invoke with no selector — explicit default behavior observed; next scheduled fire per renamed schedule writes ONLY its own firm's tree (verify by key census, the discriminator that caught the original defect)</run>
      <expect>Selection provably discriminates (positive + negative control per firm); no cross-firm writes.</expect>
      <if_mismatch>Roll back in-window; a schedule observed writing the other firm's tree post-rename is the original defect wearing the new name.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same function as RP-W5 (guard) and same schedules as RP-W3 (times) — all your lane; keep the three
changes in separate commits/applies so each is attributable and separately rollback-able, and
coordinate order with COO (selector ideally lands before or with the RP-W3 atomic window).
</cross_domain_coordination>

<acceptance_criteria>
1. Step order proven: selector commit precedes rename apply.
2. Phase-3 exercises shown with positive AND negative controls per firm; key-grammar census shows no
   cross-firm write on the first scheduled fire post-rename.
3. Names match Andrew's ordered form and are TRUE (each schedule's payload selects the named firm).
4. Cutover-gap plan stated pre-apply; post-apply shows no skipped/double day.
5. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail.
</acceptance_criteria>
</task_order>
