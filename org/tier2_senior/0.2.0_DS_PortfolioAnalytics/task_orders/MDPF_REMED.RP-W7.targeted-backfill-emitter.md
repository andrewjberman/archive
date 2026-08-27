# TO MDPF_REMED.RP-W7 — TARGETED BACKFILL (the emitter as strategic infrastructure) ⛔ STAGED: AFTER the pipeline is functional

<task_order id="MDPF_REMED.RP-W7" project="MDPF_REMED">
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "MDPF_REMED" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>Sequenced LAST by Andrew's word: "after the remediation is complete and the pipeline is
functional moving forward, we will want to explore a robust targeted solution for backfill — which
is the point of that emitter." GO comes from COO only after the plan-§5 completion bar reads true
(12/12 A4 objects on one unattended scheduled cycle) — not before.</priority>

<dependencies>
  <dependency agent="2.0.0_SA_COO" task="plan §5 completion bar adjudicated (scheduled cycle 12/12)" status="pending"/>
</dependencies>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W7, §4)</ref>
</references>

## SCOPE
The emitter is strategic infrastructure, not a one-off for 08-05. Reconstruction prefix RATIFIED by
CTO with binding conditions:
`s3://opal-data-assets/eclipse/inflection/reconstructed/vintage=2026-08-05/reconstruction.json` —
distinct medallion slot, self-naming, opt-in by construction (0 read paths glob it, measured),
grammar-conformant. `vintage=` not `date=` is deliberate: no `date=`-globbing consumer can pick it
up by accident.

**CONDITION 1 — labels live in the ARTIFACT BODY, not only the gate:** `point_class:
"reconstructed"`, method version, tie-out error, fwd/bwd residual travel WITH the data. A consumer
reading the object without the gate must still learn it is derived.

**CONDITION 2 — DO NOT FREEZE GATE THRESHOLDS ON THE CALIBRATION DAY:** calibrate on one known day,
VALIDATE ON A DIFFERENT ONE. Freezing from the calibrated run and measuring against it is fitting
the test to the data (Andrew 2026-08-06: "a fix only your test set can see is a tune, not a fix").

**UNCHANGED:** the 136bp `opal_long_term_conservative` cell must come under the bar or THE GATE
FAILS AND THAT IS A FINDING, not a threshold to relax (your own words, ratified). ⛔ NOTHING SERVES
from this prefix without a separate ruling.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-find "reconstructed" data + comp-platinum reverse &lt;any new field emitted&gt;</run>
      <expect>0 existing read paths glob the reconstructed prefix (re-confirm the opt-in property at your HEAD); consumer set of any new field enumerated BEFORE the producer ships.</expect>
      <if_mismatch>STOP — a consumer already globbing it breaks the opt-in premise; surface to CTO via COO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate &lt;emitter script&gt; --artifact &lt;reconstruction.json QA output&gt;</run>
      <expect>PASS/WAIVED; body carries point_class/method-version/tie-out/residual (Condition 1 exercised by reading the artifact).</expect>
      <if_mismatch>STOP until clean; NO_CONFIG = build the config, this artifact class must not ship unvalidated.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>calibration/validation split demonstrated: thresholds set on day A, validated on day B (different day)</run>
      <expect>Validation-day tie-out under the bar WITHOUT re-tuning. 136bp cell under the bar or reported as a gate FAILURE finding.</expect>
      <if_mismatch>Report the failure as a finding; do not relax thresholds; do not serve.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Writes ONLY under the ratified reconstructed/ prefix — never platinum, never the medallion tiers it
sits beside. Serving requires a separate ruling (NEVER#3 territory if it moves served output). No
coordination with the RP-W1..W5 executors needed while staged; re-check with COO at GO.
</cross_domain_coordination>

<acceptance_criteria>
1. Artifact body carries the Condition-1 labels (shown by reading the served-candidate object).
2. Calibrate/validate day split shown (Condition 2), no threshold motion between them.
3. 136bp cell disposition explicit: under bar, or gate-FAIL finding filed.
4. Nothing serves; 0 read paths outside the prefix touched.
5. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail.
</acceptance_criteria>
</task_order>

---

## DISPOSITION: SUPERSEDED-BY-EXECUTION (2.0.0_SA_COO, 2026-08-14 ~17:2xZ)

This TO's scope was ABSORBED by Andrew's direct employment order at the 4.0.0_SA_CRO terminal
(~1517Z, record `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260814_EMITTER_EMPLOY_AND_REFRESH_SKILL.md`)
and executed to completion at that seat the same day: emitter @80b7bf651f (D4 gate PASS), 7
reconstruction artifacts on the ratified prefix, builder opt-in consume @5b00923c11 deployed
(comp-pipescript MATCH), dated-key re-land under Andrew's explicit "recs approved" @9b816615f1,
publish 17:16Z serving all 7 former holes (COO independent tie-out read PASS). The sequencing gate
this TO sat behind was discharged-by-sovereign-direct. **DO NOT FIRE this TO** — its work is done;
DS's D3 spec + executed steps 1-2 were reused with attribution. Routing record: COO→DS inbox
20260814T154034Z. Disposition per CRO's 171822Z handback ("the TO disposition is yours").
