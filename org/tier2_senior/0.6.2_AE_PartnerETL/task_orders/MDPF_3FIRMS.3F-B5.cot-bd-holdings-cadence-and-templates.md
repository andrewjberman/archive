<task_order>
<id>MDPF_3FIRMS.3F-B5</id>
<title>COT/BD-holdings bronze leg — verify tonight's 07-21 landing, document the D+1 delivery cadence as the freshness contract, dump the enriched template catalog</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:23Z</issued_at>
<status>staged</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §2.2 (COT-AUA row); §2.2 zero-overlap resolution; §4 WS-B row 3F-B5; §8.1 (migration constraint)</ref>
  <ref type="brief">CRO briefs @eb9edc1dc + @cab5e1748 (RF-14) — account-level vs portfolio-level template selection</ref>
</references>

<scope>
**THIS IS A VERIFICATION TO, NOT A REPAIR TO — read why, because the framing was corrected once
already.** DS measured that `fact_holdings` (06-09..07-20) and `fact_model_assignment` (07-21, 07-22)
share ZERO dates, so `non_model = total - model` was computable for no date, and correctly declined to
guess why. **The mechanism is the D+1 ~03:30Z holdings delivery cadence: the two series are ADJACENT,
NOT DISJOINT.** First overlap = 07-21, landing tonight on the standing schedule. Nothing is broken.

Deliverables:
(a) **Verify tonight's `HOLDINGS_DAILY_2026-07-21.xlsx`** (~03:30Z) lands and converts through the BD
    silver sweep (cron(0 5)) into `fact_holdings_s2` date=2026-07-21.
(b) **Document the D+1 delivery cadence as this leg's FRESHNESS CONTRACT** — measured from bronze object
    stamps, not assumed. This is what stops the next agent reading a correct D+1 lag as staleness.
(c) **Run `dump_enriched_templates.py`** — it exists, is gate-clean, and has NEVER BEEN RUN; qt1 dims
    are unseen. Read-only, on-box. Dump the full server-side dimension catalog including qt1 holdings.
(d) **Vendor-depth statement under the migration constraint.**

⚠ **THE MIGRATION CONSTRAINT IS BINDING AND COUNTER-INTUITIVE (§8.1):** Cottonwood is MID-MIGRATION into
Black Diamond. Our 06-09 floor is **OUR INGEST START, NOT THE VENDOR FLOOR**, and vendor-side depth is a
MOVING TARGET — more history is expected to arrive on its own. Therefore: **NO HARDCODED SERIES START,
no synthesized rows, no frozen backfill.** The sweep must pick up newly-arrived older dates
AUTOMATICALLY. Anything that writes a value where real data will later appear is a future contradiction
we authored ourselves.

⚠ **RF-14, and it is the cautionary tale for this whole leg:** BD DataMining templates carry
ACCOUNT-level assignment dims (13 each in qt3/qt4, none selected) while our template selects the
PORTFOLIO level — producing `portfolio_strategy_id` 100% null across 13,303 rows. **That looked exactly
like a vendor gap for four months and it was OUR SELECTION.** Never conclude data doesn't exist from the
shape of our own template.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run># rail-checked: applied-truth schedule read
aws events describe-rule --name cot-bd-session-daily
aws events describe-rule --name opal-assets-silver-blackdiamond-sweep-daily</run>
      <expect>Both ENABLED; cron(0 2) and cron(0 5). Cite verbatim.</expect>
      <if_mismatch>STOP; report to COO before proceeding.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 on the Cottonwood bronze holdings prefix (explicit-Z LastModified)</run>
      <expect>Object stamps confirming the D+1 ~03:30Z cadence across several prior deliveries.</expect>
      <if_mismatch>If the cadence is not D+1, the freshness contract changes — report the measured cadence, do not assert the documented one.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Verify fact_holdings_s2 date=2026-07-21 present after the scheduled sweep (s3api, explicit-Z)</run>
      <expect>Partition present by 06:00Z 2026-07-23.</expect>
      <if_mismatch>If the scheduled pass has not run: BLOCKED-ON-SCHEDULE, report and wait. ⛔ Do NOT hand-fire the sweep or any gold run.</if_mismatch>
    </step>
    <step>
      <run>python dump_enriched_templates.py  (read-only, on-box; never run before)</run>
      <expect>Full dimension catalog dumped to s3://opal-data-cot/code/bronze/templates_enriched/, INCLUDING qt1 holdings dims. Read the output.</expect>
      <if_mismatch>If it errors, that is a finding (a gate-clean never-run script). Report; do not patch it inside this TO.</if_mismatch>
    </step>
    <step>
      <run>Backwards-extension exercise: confirm a newly-landed OLDER date converts without intervention</run>
      <expect>Either an exercised demonstration or documented evidence that the sweep is date-agnostic.</expect>
      <if_mismatch>If the sweep cannot pick up back-arriving history automatically, that DIRECTLY violates §8.1 and is a P1 design finding — escalate, do not work around it.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-list the partitions with denominators printed</run>
      <expect>07-21 present; weekend absences (07-18/19) correctly explained, not flagged.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>No converter logic is modified. `dump_enriched_templates.py` is read-only and
  writes only a template catalog to a code/ prefix — no data-layer write, no reprocess implication.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="blackdiamond/cottonwood/silver/fact_holdings_s2/" shared_with="0.4.0_DS_ClientPlatform (3F-S3, 3F-G3)">
    3F-S3 determines whether `fact_holdings` or `fact_holdings_s2` is canonical for the AUA total — an
    OPEN S4 question, not silently either. Your cadence contract feeds it. MCP DS before publishing.
  </resource>
  <resource path="template catalog" shared_with="4.0.0_SA_CRO">
    CRO authored the RF-14 finding; route the qt1 dims to CRO for read.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency type="schedule" name="BD holdings delivery ~03:30Z 07-23 + sweep cron(0 5)" status="pending">
    A scheduled gate. BLOCKED-ON-SCHEDULE is a valid interim report.
  </dependency>
</dependencies>

<acceptance_criteria>
1. `fact_holdings_s2` date=2026-07-21 present by 06:00Z 2026-07-23, evidenced via s3api explicit-Z.
2. The D+1 delivery cadence is committed as this leg's freshness contract, MEASURED from bronze object
   stamps (not asserted from documentation).
3. Template catalog dumped to `s3://opal-data-cot/code/bronze/templates_enriched/` **and read**, with
   the qt1 dims explicitly enumerated.
4. Backwards-extension exercised or evidenced — a newly-landed older date converts with no intervention.
5. Vendor-depth statement written under §8.1 (depth is a moving target; our floor is our ingest start;
   NO hardcoded series start).
6. Weekend/holiday absences explained via the trading calendar, never reported as gaps (NEVER#1).
7. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO. Escalate immediately if the sweep CANNOT auto-pick-up back-arriving history —
that is a §8.1 design violation with consequences well beyond this leg.
</escalation>
</task_order>
