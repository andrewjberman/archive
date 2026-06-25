<to_id>ETFS_SETUP.W1</to_id>
<project>ETFS_SETUP</project>
<title>ETFS_SETUP W1 (AE) -- opal-data-etfs bucket + write-out IAM + ETF-universe config + daily-artifact contract + Inflection daily-ownership producer (the provable-now foundation)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<!-- ETFS lane = base 0.7.0_AE_CloudOps (Andrew-direct 2026-06-23: base AE is FREE post-go-live -> take ETFS W1/W2/W3 directly; the ~B spawn was stood down). -->>
<consult>0.4.0_DS_ClientPlatform (daily-artifact contract shape -- DS's AVGCAP compute reads it; agree the schema before the producer writes)</consult>
<issued_by>2.0.0_SA_COO (ETFS_SETUP decomposition; CTO PRD 1e3db994b + Andrew decisions fd41dc052)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete</status>
<!-- GO 2026-06-22 151x Z: AE signaled capacity. Non-DS-dependent parts startable now; the daily-artifact contract step loops DS (AE proposes, DS confirms async). No-rush overall (full June ~early-July). -->
<!-- COMPLETE 2026-06-25 (COO flip per ETFS-TO-status convention; AE RAVC2 131248Z + DS corroboration): W1 LANDED+LIVE+verified-on-served -- ledger d2dd0d5d6 CLOSED (13-add/0/0, tagged inf-pipeline-v1.7.74 + shared-infra-v1.31.0), comp-iam CLEAN (548904bbd), served slice opal-data-etfs/daily/inflection/2026-06-23.json comp-freshness=PASS, 4 ETFs sum ~$82.2M ties DS $82.14M/476-accts + PRD ~$82M anchor, reuse-bucket version. NOTE: the forward producer is W1's verified deliverable; the HISTORICAL BACKFILL needed for ETFS_AVGCAP.AC#2 (monthly-avg) is a SEPARATE follow-on leg dispatched to AE 0.7.0 (2026-06-25), NOT a W1 reopen. -->
<!-- SCOPE-CORRECTION 2026-06-23 (CTO Andrew-direct, COO-amended): the opal-data-etfs bucket ALREADY EXISTS -- shared-infra/s3.tf:164 (Terraform-managed, ETFS_NETAST-created 05-22, ~296 net-assets objects; also mdpf-pipeline/main.tf:58 ref). REUSE it, do NOT create (a safe-apply 'create' = duplicate-resource/state collision). The real W1 infra delta = the write-out IAM + the daily/{partner}/ prefix-contract + the Inflection producer, NOT the bucket. Objective/the_fix#1/safe-apply-phase/AC1 amended below. -->

<objective>
Stand up the ETFS aggregation foundation using the WRITE-OUT model (CTO-ruled, comp-iam-grounded): each per-firm producer reads ONLY its own firm bucket (already IAM-allowed) + WRITES a small daily ETF-ownership slice to the EXISTING shared opal-data-etfs bucket (REUSE -- already NETAST-managed, see scope-correction note; do NOT create); ETFS_AVGCAP reads opal-data-etfs ONLY (zero firm-bucket grants). This never fights the firm-bucket Deny statements (Deny-on-own-ARN) -> NEVER#1 (no cross-firm-bucket) holds BY CONSTRUCTION. W1 delivers the foundation + the FIRST producer (Inflection, the live-daily provable-now source).
</objective>

<the_fix>
1. opal-data-etfs BUCKET -- REUSE the EXISTING shared bucket (CTO 2026-06-23 source-confirmed: shared-infra/s3.tf:164, Terraform-managed, ETFS_NETAST-created 05-22, ~296 net-assets objects). DO NOT create it (duplicate-resource/state collision). The real W1 infra delta = (a) the daily/{partner}/ prefix structure under the existing bucket + (b) prefix-scoped co-tenancy with the existing net-assets series (NETAST lives under its OWN prefix -- ZERO-touch it). Scoped IAM in #2.
2. WRITE-OUT IAM: grant the Inflection producer role read opal-data-inf (already allowed) + write opal-data-etfs/inflection/. comp-iam-verify the new grants don't widen any firm-bucket Deny.
3. ETF-UNIVERSE CONFIG (shared, one source not hardcoded x3): {DIVZ, IDVZ, PFDE, PFOE}. One config the 3 producers + AVGCAP all read.
4. DAILY-ARTIFACT CONTRACT: define the per-firm daily ETF-ownership slice schema (partner, ETF-ticker, date, sum(market_value) across the partner's accounts holding the ETF, account_count, source_as_of). Agree with DS (consumer) before the producer writes. This is the contract AVGCAP averages.
5. INFLECTION DAILY PRODUCER (lambda): reads opal-data-inf gold/holdings/{date}.parquet -> filters to the 4 ETF universe -> aggregates per-ETF market_value -> writes the daily slice to opal-data-etfs/inflection/{date}.json per the contract. Clock = 2026-05-15 (Andrew D3; May-partial 05-15..). source_as_of label (Andrew D6). Inflection is live-daily (Orion REST), so this is provable NOW.
</the_fix>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam gaps + comp-iam service (the new Inflection producer role + AVGCAP read role vs opal-data-etfs + opal-data-inf)</run>
      <expect>The write-out grants (producer: read-inf + write-etfs/inflection; AVGCAP: read-etfs-only) introduce NO firm-bucket-Deny widening + NO cross-firm read. Confirm the firm-bucket Deny-on-own-ARN is untouched.</expect>
      <if_mismatch>STOP; re-scope the IAM so no firm-bucket grant is widened (the whole point of write-out is to avoid cross-firm reads).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>.tools/safe-apply.sh (TF: write-out IAM only -- the bucket already exists)</run>
      <expect>Plan = ONLY the new scoped write-out IAM (0-diff on the EXISTING opal-data-etfs bucket). A 'create opal-data-etfs bucket' diff = STOP (duplicate-resource/state collision; it's NETAST-managed at shared-infra/s3.tf:164). HALTGT clean. Open a deploy-completion ledger.</expect>
      <if_mismatch>STOP; do not apply. A bucket-create diff = the reuse wasn't wired -> re-point at the existing resource (don't create).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>verify the Inflection producer writes a valid daily slice (read-back opal-data-etfs/inflection/{date}.json vs the contract) + comp-freshness</run>
      <expect>Daily slice present, schema-valid per the DS-agreed contract, 4 ETFs, source_as_of labeled, market_value sane (Inflection ~$82M-area). Close the ledger.</expect>
      <if_mismatch>Fix the producer before signaling DS for AVGCAP-W1.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
opal-data-etfs is a NEW shared cross-partner aggregation bucket (the audited write-out target). The daily-artifact contract is shared with DS (ETFS_AVGCAP consumer) -- agree the schema with DS before the producer writes (avoid a producer/consumer shape mismatch). No firm-bucket sharing (write-out model, NEVER#1 by construction).
</cross_domain_coordination>

<acceptance_criteria>
1. opal-data-etfs bucket REUSED (already-live, NETAST-managed -- W1 plan shows 0-diff on the bucket itself, NOT recreated) + the new scoped write-out IAM is the only infra add (safe-apply 0-diff-except-the-IAM, deploy-ledger opened+closed; comp-iam-verified: no firm-bucket-Deny widening, no cross-firm read) + the daily/{partner}/ prefix co-tenants cleanly with NETAST's net-assets prefix (zero-touch).
2. ETF-universe config (one shared source, {DIVZ,IDVZ,PFDE,PFOE}) + daily-artifact contract (DS-agreed schema) committed.
3. Inflection daily producer deployed + writing opal-data-etfs/inflection/{date}.json (schema-valid, 4 ETFs, source_as_of, clock=05-15) -- verified on the served slice (validate-on-served).
4. Session-log Compiler Tools section reproduces every <run> + result + pass/fail.
5. Signals DS that the Inflection daily series is live -> unblocks AVGCAP-W1 (Inflection methodology + May-partial + June-MTD).
</acceptance_criteria>
