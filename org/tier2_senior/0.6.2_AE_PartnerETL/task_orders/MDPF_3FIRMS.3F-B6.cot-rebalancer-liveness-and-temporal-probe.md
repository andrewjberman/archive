<task_order>
<id>MDPF_3FIRMS.3F-B6</id>
<title>COT/BD-rebalancer bronze leg — feed-level LIVENESS signal + the TEMPORAL-vs-CURRENT probe (positive control mandatory)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:23Z</issued_at>
<status>staged</status>
<advisory>4.0.0_SA_CRO (probe spec author — consult, do not re-derive)</advisory>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z (explicit: "The 3F-B6 TEMPORAL-vs-CURRENT probe EXECUTES -- it is evidence-gathering, in scope, positive control mandatory").</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §2.2 (COT-model row); §4 WS-B row 3F-B6; §5 ruling 10 (backfill = developing subject, COTTONWOOD-ONLY); §8.2</ref>
  <ref type="brief">CRO lookback brief @eb9edc1dc + addendum @d0287966d (CTO-reviewed, PRD v1.2)</ref>
</references>

<scope>
Two deliverables. Both are EVIDENCE-GATHERING; neither executes a backfill.

**(a) A FEED-LEVEL LIVENESS SIGNAL — and understand precisely why the obvious check fails.**
The 07-21 and 07-22 rebalancer pulls are BYTE-IDENTICAL. **A stable roster and a frozen feed are
INDISTINGUISHABLE FROM STORAGE ALONE** (CRO §7.4). Therefore **"assignment unchanged" must NEVER be
read as "feed confirmed live."** Name a signal that can actually discriminate — something that would
differ if the feed were dead. A diff is not a liveness signal.

**(b) THE TEMPORAL-vs-CURRENT PROBE** on the DataMining ACCOUNT-level assignment dims, per CRO's spec.
The decisive unknown for all Cottonwood history: does BD expose DATED `(account, strategy)` state, or
only current state stamped with whatever date you ask for?

⛔ **POSITIVE CONTROL IS MANDATORY AND IT IS THE WHOLE POINT.** The probe MUST include an account whose
assignment is KNOWN to have changed between the two windows. **Without it, "identical" cannot fail** —
and an instrument that cannot fail is not an instrument. CRO measured the churn that makes this
constructible: back-mapping today's roster onto 06-08 holdings joins 291/296 and mis-states every
churned account; models were created 2026-05-28..07-17; a quarter of the book sits on models created on
one day (07-06); 5 of today's accounts did not exist on 06-08.

**BACKFILL DESIGN CONTEXT — carry these, do not re-litigate them (CTO-reviewed, PRD v1.2):**
- **(i) HOLDINGS-BASKET FINGERPRINTING IS BANNED, BY MEASUREMENT** — not by preference. Strategy baskets
  are the same ~15 ETFs at different weights; pairwise cosine 0.62-0.98, mostly >0.90 (Sat 50v60 =
  0.969, 80v70 = 0.981). A past date's strategy is NOT recoverable from holdings alone. Inference-from-
  similarity is the fabrication class.
- **(ii) The temporal DataMining dimension is the SINGLE REAL UNLOCK.** If the probe returns TEMPORAL,
  dated `(account, strategy, date)` x composition weights -> dated model-level AUM.
- **(iii) TRANSACTIONS-AS-CHANGE-EVENTS ARE A GUARD, NOT A LICENSE.** A detected rotation cluster means
  NEVER carry an assignment across it. **But absence-of-signal does NOT affirm stability** — the same
  basket similarity that kills fingerprinting caps this detector's sensitivity: a 0.97-cosine
  reassignment produces a near-invisible trade cluster. Calibration path: the forward window accrues
  ground truth free (daily roster diffs yield dated observed reassignments) — score each against its
  transaction signature to MEASURE hit-rate before anyone leans on it.
- **(iv) TWO CTO BINDINGS:** **COMPOSITION VINTAGE** — a dated backfill needs blend weights AS OF that
  date, not today's (a June 80/20 served with today's 75/25 fabricates at the composition layer even
  with perfect temporal assignment); so the probe scope EXTENDS to whether `model_detail` history is
  dated. **STRUCTURAL DEPTH CEILING** — Opal model definitions were created 2026-05-28..07-17, so **no
  Opal-model series can exist before the models did (~05-28), REGARDLESS of probe outcome.**

⛔ **NOTHING IS BACKFILLED INSIDE THIS TO.** Forward-only stands until a CTO-gated backfill design.
Cottonwood backfill remains the DEVELOPING SUBJECT (Andrew's hold is Cottonwood-scoped — this leg IS
the held firm). The probe is evidence; the design is CTO's; the execution is neither.
⛔ The BD Rebalancer endpoint returns LIVE STATE — never a backfill instrument, same law as the eclipse
`--date` filename ban.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run># rail-checked: applied-truth schedule read
aws events describe-rule --name cot-rebalancer-runner-daily</run>
      <expect>ENABLED; cron(0 6). Cite verbatim.</expect>
      <if_mismatch>STOP; report to COO.</if_mismatch>
    </step>
    <step>
      <run>Read CRO's probe spec (@eb9edc1dc + @d0287966d) BEFORE designing anything</run>
      <expect>Probe design matches CRO's spec; you consult rather than re-derive.</expect>
      <if_mismatch>If you believe the spec is wrong, MCP CRO — do not silently substitute your own design.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Identify the POSITIVE-CONTROL account (assignment KNOWN changed between the two probe windows) BEFORE running the probe</run>
      <expect>A named account with documented evidence its assignment changed. CRO's churn data supports construction.</expect>
      <if_mismatch>⛔ HARD STOP. Do NOT run the probe without the control. An "identical" result with no control is uninterpretable and MUST NOT be recorded as a verdict. This is the single most important gate in this TO.</if_mismatch>
    </step>
    <step>
      <run>Execute the temporal-vs-current probe, control account INCLUDED, on account-level assignment dims AND on model_detail (composition vintage)</run>
      <expect>A TEMPORAL or CURRENT-ONLY verdict for BOTH axes, with raw evidence retained. The control returns DIFFERENT across windows if the surface is temporal.</expect>
      <if_mismatch>If the control returns identical, the surface is current-only OR the control is invalid — distinguish these two before recording anything.</if_mismatch>
    </step>
    <step>
      <run>Name the feed-level liveness signal and demonstrate it discriminates</run>
      <expect>A signal that would differ if the feed were dead — NOT a roster diff.</expect>
      <if_mismatch>A signal that cannot distinguish a frozen feed from a stable roster does not satisfy this step. State it as unresolved rather than substituting a diff.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-confirm bronze rebalancer partitions with denominators printed</run>
      <expect>07-21, 07-22 present; series is 2 days old because it STARTED 07-21 — that is not a gap.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Probe + liveness characterization only. No converter or producer is patched and
  NO backfill is executed. Any backfill design arising from a TEMPORAL verdict lands as a CTO-gated PRD
  amendment with its own reprocess scope.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="rebalancer bronze + fact_model_assignment" shared_with="0.4.0_DS_ClientPlatform (3F-G3)">
    G3 wires the Cottonwood gold slice and is WS-G-GATED. Your probe verdict determines whether any
    historical series is even possible. Hand the verdict; do not build the slice.
  </resource>
  <resource path="probe spec + churn measurements" shared_with="4.0.0_SA_CRO">
    CRO authored the spec and holds the measured churn context. Consult on request; CRO is advisory on
    this TO, not an executor.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="none">Independent of the other B legs.</dependency></dependencies>

<acceptance_criteria>
1. Probe EXECUTED with a POSITIVE CONTROL that could have failed, covering BOTH assignment temporality
   AND composition (`model_detail`) temporality. **A verdict without a control is not accepted.**
2. A TEMPORAL or CURRENT-ONLY verdict recorded with RAW EVIDENCE retained.
3. A feed-level LIVENESS SIGNAL named — explicitly not a roster diff — with its discriminating power
   demonstrated, or recorded as unresolved.
4. The fingerprint BAN is carried forward in the deliverable (measured, cosine 0.62-0.98).
5. The ~05-28 structural depth ceiling is stated as binding REGARDLESS of probe outcome.
6. Forward-only stands; **zero backfill executed inside this TO**; any design routed to CTO.
7. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; CTO gates any backfill design. Escalate immediately on a TEMPORAL verdict — it
materially changes what Cottonwood history is possible and feeds a developing subject Andrew is holding.
</escalation>
</task_order>
