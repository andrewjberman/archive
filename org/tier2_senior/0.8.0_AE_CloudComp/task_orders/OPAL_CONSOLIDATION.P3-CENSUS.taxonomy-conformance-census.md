<task_order>
<to_id>OPAL_CONSOLIDATION.P3-CENSUS</to_id>
<title>Consolidation taxonomy CONFORMANCE CENSUS — measure every consolidation-associated resource against OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md; per-resource conform/deviate table with each deviation NAMED</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<!-- RE-TARGETED 2026-07-17 ~17:36Z per Andrew-direct via MSTR 173531Z: base 0.8.0 is RESERVED
     (Andrew-launched research session, dc4207c7c asks); fabric census work goes to the ~C lane.
     The 172809Z GO to base 0.8.0 is MOOT (MSTR sends the stand-down); the shared-Phase-1
     composition note becomes a COORDINATION seam between ~C's census enumeration and base's
     heat/dups research -- ~C reads base's deliverables when published, never tasks base. -->

<date>2026-07-17</date>
<status>staged</status>
<priority>P3 (Andrew-ratified standing allocation order, CTO relay 171739Z — behind P1 INF chain + P2 GLDRNS/re-key; parallelizable, dedicated instrument-builder)</priority>

<authority>
Andrew-direct ~17:1xZ (CTO terminal), VERBATIM: "we want to establish how we name things and stay
consistent in that naming in all aws resources associated with the consolidation and migration. that
means consistent bucket structure, consistent local repo data/assets/~ structure, consistent ec2
runner structure and specs (size may vary), consistent implementation (using our architectural docs
like how we use lambda_chunking or ec2_autostart) and device OS and IAMS, we want to make sure that
we are running a very tight ship here and that starts by being organized."
Division (CTO 171739Z): CTO authors the STANDARD (docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md,
citing existing canon, not re-deriving); THIS TO is the MEASUREMENT against it. Gates come AFTER the
census names the real deviation classes — gate-what-you-measured, no speculative lint.
</authority>

<scope>
MEASURE (read-only; zero remediation in this TO) every consolidation-associated resource against the
standard's axes, one row per resource:
  A. S3 buckets + prefix grammar (opal-data-assets {source}/{scope}/{layer}/{type|feed}/{date} as
     already-law; every consolidation bucket incl. telemetry/logging buckets)
  B. Local repo data/assets/~ tree structure
  C. EC2 runner structure + specs (shape/spec baseline conformance; size MAY vary by design — a size
     delta is NOT a deviation unless the standard says so)
  D. Implementation-pattern conformance: lambda_chunking, ec2_autostart, telemetry-at-provision,
     absence-twin, EventBridge Scheduler grammar {unit}-{function}-{cadence} (per OPAL_STNDRD ratified axes)
  E. Device OS + IAM baseline (role naming, scoped-grant shape; DESIRED from TF + APPLIED from live reads)
OUTPUT: docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_CENSUS.md — per-resource table:
resource | axis | CONFORM/DEVIATE | the deviation NAMED (exact, quotable) | evidence (comp-tool output or live-read id)
plus a DEVIATION-CLASS rollup (the input to CTO's gate design) with denominators printed per axis.
</scope>

<dependencies>
  <dependency doc="docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md" status="CTO authoring this hour — GO fires when it lands"/>
</dependencies>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-aws (bucket + lambda + scheduler census views) and comp-iam service per consolidation lambda</run>
      <expect>Every resource the census will row-ify appears in a comp-tool view OR is explicitly listed as comp-invisible with a live-read fallback (aws ls/describe, operational). Denominator printed: N resources enumerated, source per resource.</expect>
      <if_mismatch>STOP. A census whose denominator is not enumerated at run time is the axis-error class (verification law 6). Surface the enumeration gap to COO before writing rows.</if_mismatch>
    </step>
    <step>
      <run>Read the STANDARD doc end-to-end; extract its axes into the census column schema BEFORE measuring</run>
      <expect>Every axis in the standard has a census column; no census column exists without a standard clause to cite.</expect>
      <if_mismatch>STOP. A measured-but-unstandardized column is speculative lint — the thing CTO's division explicitly excludes. Route the missing clause to CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Positive + currency control (AMENDED per CTO 172321Z): run the census against ONE known-conform resource (opal-data-assets grammar row) AND the us-east-2 telemetry bucket — the STANDARD's sec A now blesses dedicated telemetry buckets, so that row MUST read CONFORM-BY-AMENDMENT citing sec A. A census reading it DEVIATE is reading a CACHED DRAFT of the standard, not the current doc @cc1cd96dd.</run>
      <expect>Conform control reads CONFORM; telemetry bucket reads CONFORM-BY-AMENDMENT with the sec-A cite. Either misread = the instrument fails its currency test. An instrument that cannot fail is not an instrument.</expect>
      <if_mismatch>STOP. Fix the instrument (re-read the standard at HEAD), not the row. Do not commit a census whose controls did not discriminate.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-state --project OPAL_CONSOLIDATION</run>
      <expect>Census landing reflected; no BEHIND introduced by this TO's own records.</expect>
      <if_mismatch>Reconcile the record in the same session; surface to COO if the drift is not yours.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Shared surfaces: opal-data-assets + opal-data-schwab (0.5.0 WP8 D4 zero-reader window LIVE — the census
READS but must not write/probe schwab objects: a census GetObject against opal-data-schwab during the
window would pollute the zero-reader evidence. Coordinate timing with 0.5.0 BEFORE any schwab-bucket
live read; TF/IAM DESIRED reads are always safe). INF chain boxes are P1-owned by 0.7.0 — read-only
census there too, and no SSM commands to the inf box while the nightly re-dispatch is in flight.
</cross_domain_coordination>

<acceptance_criteria>
1. Census doc landed with per-resource rows, per-axis denominators, and the deviation-class rollup.
2. BOTH controls (conform + known-deviate) reproduced in the session log's Compiler Tools section with
   observed output and explicit pass/fail vs expect — missing rows = REWORK.
3. Every DEVIATE row names the deviation exactly (quotable into a gate spec) and cites its evidence
   (comp-tool output or live-read request-id). "Nonstandard" without the named delta = REWORK.
4. Zero writes to any measured resource; zero schwab-bucket live reads without 0.5.0's timing ack.
5. Session log Compiler Tools section reproduces each mandate run + observed result + pass/fail vs expect.
</acceptance_criteria>

<references>
  <ref type="standard">docs/architecture/OPAL_CONSOLIDATION_TAXONOMY_STANDARD.md (CTO, landing ~this hour)</ref>
  <ref type="prd">docs/architecture/OPAL_CONSOLIDATION_PRD.md (v0.2 RATIFIED)</ref>
  <ref type="ratified-axes">OPAL_STNDRD registry row (scheduler grammar, absence-twin, telemetry-at-provision)</ref>
  <ref type="ruling">CTO 171739Z (Andrew verbatim + division: standard=CTO, census=this TO, gates AFTER)</ref>
</references>
</task_order>
