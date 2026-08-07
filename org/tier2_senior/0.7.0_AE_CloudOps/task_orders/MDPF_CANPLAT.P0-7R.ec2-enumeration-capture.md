<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-07-canplat-p0-7r</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>MDPF_CANRTE.P0-7 (body ADOPTED @a6ae64326). Criterion 1 (pre-enumeration EBS snapshot) is ALREADY DISCHARGED: snap-0fa2186f01fbc3785, 100%, StartTime 2026-08-06T20:48:38.684Z, vol-071d4d9e2d169bbb9 — AE~Z live-primitive re-confirmed 2026-08-07 ~0001Z. Do not re-snapshot; the open half is the ENUMERATION only.</supersedes>
    <governing>PRD @24d3eb2f8 · CONTRACT @a3106d585 (this capture is a PRECONDITION of the deferred EC2 teardown; the teardown itself remains NOT AUTHORIZED)</governing>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0 BINDS (verbatim §0 carried in your P0-2R/P2-1/P3-1 set @f123fbf6e — same force here):
    BUILD WHAT IS DESCRIBED, DO NOT HUNT ERRORS. A number that surprises you is not a finding. Anything
    that looks wrong: ONE LINE to 2.0.0_SA_COO~Z, subject `SURPRISE:`, then continue. This TO is
    EVIDENCE CAPTURE, not investigation — what you capture is recorded, not analyzed.
  </standing_instruction>

  <objective>
    Complete the OPEN HALF of the adopted P0-7: the on-disk code + dependency ENUMERATION of the MDPF
    EC2 (i-02448edb624a7a7cf), executed during the chain's OWN production-initiated window (the 09:00 ET
    2026-08-07 scheduled cycle) per the adopted body's amended criteria @a6ae64326 — so the capture sees
    the real runtime state, before this program's port changes what runs on that box.
  </objective>

  <sequencing>
    Tomorrow morning, in order, one block: (1) P0-2R Orion probe inside 08:05–08:40 ET; (2) this
    enumeration during the 09:00 ET production-initiated window. They do not contend — the probe is
    vendor-side read-only; this is box-side read-only. If the 09:00 ET cycle does not fire, that is a
    NOT-RUN report, not a re-trigger — ad-hoc gold runs are QA instruments and this capture's whole
    point is the PRODUCTION window (adopted P0-7 amendment: "enumerate during the chain's OWN start").
  </sequencing>

  <acceptance_criteria>
    The adopted P0-7 criteria @a6ae64326 stand for the enumeration half (incl. "a manifest is not a
    control" — the capture is evidence, its integrity shown by hashes, not by a manifest asserting
    itself; and the second runtime pip-install finding's UNPINNED capture requirement). Plus:
    1. Capture executed via the S3-pull pattern (Rule 12: local → S3 → EC2 pulls → execute; never
       inline code in SSM).
    2. Evidence: enumeration artifact keys + content hashes reported to COO~Z same day, with the
       denominator printed (files enumerated / dirs walked).
    3. Criterion-1 NOT re-run: the existing snapshot stands as the rollback baseline; state its ID in
       the deliverable rather than minting a new one.
    4. NO termination, NO teardown, NO schedule change — the teardown remains unauthorized under this
       decomposition (deferred list, MDPF_CANPLAT_DECOMPOSITION_20260806.md).
  </acceptance_criteria>

  <do_not>
    <rule>DO NOT terminate, stop, resize, or de-schedule anything. Evidence capture only.</rule>
    <rule>DO NOT re-trigger the production chain if it does not fire — report NOT-RUN.</rule>
    <rule>DO NOT let this displace the P0-2R probe window — the probe holds the 08:05–08:40 ET slot.</rule>
    <rule>NO error-hunting (§0). What the enumeration finds is RECORDED, not investigated.</rule>
    <rule>Commit to your lane on SITEZ; push is MSTR~Z's (:55–:00); never rebase.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">Enumeration evidence (S3 keys + hashes + denominators) to COO~Z</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
