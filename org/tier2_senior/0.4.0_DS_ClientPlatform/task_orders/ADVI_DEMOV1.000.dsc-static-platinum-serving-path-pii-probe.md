<task_order>
  <metadata>
    <id>2.0.0_SA_COO~C-2026-05-21-demov1-phase0-probe</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <!-- RAVC2-accepted by 2.0.0_SA_COO~C 2026-05-21: brief
    docs/briefs/advi-demov1-phase0-serving-path-pii-probe-20260521.md (commits
    5ecfa2ceb, a15ffd67a verified on origin/CLOUD); all 8 acceptance criteria
    met; §3.2 linchpin definitively resolved; compiler tools logged. Four
    Phase-0 deltas folded into TO-2/TO-3 amendments + relayed to CTO. -->
    <project_code>ADVI_DEMOV1</project_code>
  </metadata>

  <objective>
    Phase 0 of ADVI_DEMOV1 — a READ-ONLY verification probe. Close the single
    unknown that gates all downstream infra: the exact mechanism by which the
    static-platinum `?firm=` fetch path selects an S3 origin bucket. Produce an
    independent per-file-type PII field inventory reconciled against (not
    inherited from) the ADVI_ANONYM field map, confirm the serving-path topology,
    and audit firm-specific code branches a new `demo` firm could trip. This TO
    ships NO code and creates NO infrastructure — its sole deliverable is a probe
    brief that feeds the CTO's PRD risk section and unblocks Phase 1.
  </objective>

  <context>
    ADVI_DEMOV1 is ratified (Andrew-direct, 2026-05-21; CTO base architectural
    authority). Goal: clone s3://opal-data-bd/platinum/** (22,253 objects, 168
    advisors / 2,962 clients / 6,548 accounts) into a new opal-data-demo bucket
    with every client/advisor/account/firm identity replaced by realistic fake
    data, served to a demo Cognito login with zero real-PII exposure.

    You authored the source proposal:
    docs/proposals/advisor-intelligence-demo-dataset-20260521.md. This TO is
    proposal §7 row 0 + §8. Read §3.2, §3.3, §4, §6 (the ANONYM-map caveat), and
    §8 risks #1/#3/#4/#6 before starting.

    Project JSON: org/projects/ADVI_DEMOV1.json. The CTO is authoring the full
    PRD (docs/architecture/ADVI_DEMOV1.md) in parallel — your probe findings feed
    its risk section. Phases 1-4 are gated on PRD ship + COO~C decomposition;
    they are NOT yours to start.

    Org lane: 1.0.0_SA_CTO (base, architecture) <- 2.0.0_SA_COO~C (administration)
    <- 0.4.0_DS_ClientPlatform~C (you). RAVC your completion to 2.0.0_SA_COO~C.

    Why §3.2 is the linchpin: the dynamic API (opal-partners-data Lambda) is
    already firm-agnostic — it resolves the bucket from DynamoDB
    opal-users-v2 FIRM#{id}.s3Bucket, so a `demo` firm needs no Lambda change.
    But the static-platinum routes (PLATINUM_BASE = '/api/scoped/advisor-
    intelligence/platinum', e.g. firm/dashboard.json, advisors/{id}/timeseries.json)
    are NOT in the partners-api Terraform route table — they are CloudFront -> S3
    static fetches where `?firm={suffix}` selects the bucket. The exact mechanism
    (a per-firm CloudFront behavior vs an origin-request Lambda@Edge reading a map
    vs a §3.3-style dedicated static adapter) determines whether Phase 1 infra is
    a new CF behavior, a one-line edge-map entry, or a new adapter route. Phase 1
    cannot be scoped until this is a fact, not a guess.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before investigation (orientation baseline):
      <run>comp-routes trace {platinum static-fetch fn}</run>
      <expect>Full CloudFront -> auth -> S3 key path for a PLATINUM_BASE route
      (e.g. the function fetching platinum/firm/dashboard.json in
      portal/src/api/endpoints/advisor-intelligence.ts). The trace should reveal
      the CF distribution + behavior and whether an edge function sits in the
      path.</expect>
      <if_mismatch>If comp-routes cannot resolve the static path (these routes
      are not in the partners-api route table), fall back to direct inspection of
      the CloudFront Terraform (infra/aws/terraform/**, comp-routes behaviors for
      the custom-error/behavior table) + the live distribution config via AWS
      CLI. Document the gap; the answer is still required.</if_mismatch>

      <run>comp-blast opal-partners-data</run>
      <expect>Downstream blast radius of the dynamic serving Lambda — record the
      node/consumer count as the baseline.</expect>
      <if_mismatch>None expected for a read-only probe; record whatever blast
      radius the tool returns.</if_mismatch>

    Phase 2 — before finalizing/committing the probe brief:
      <run>comp-pii audit</run>
      <expect>The pseudonymized-vs-cleartext field audit. Use it as ONE input to
      the independent per-file-type PII inventory — cross-reference, do not
      substitute it for the file-tree walk.</expect>
      <if_mismatch>If comp-pii audit covers only serve-time fields (likely — it
      reflects the Lambda pseudonymizer scope), that is exactly the §6 caveat:
      the brief's inventory must still independently walk the full platinum tree.
      Note the divergence explicitly in the reconciliation table.</if_mismatch>

    Phase 3 — after committing the probe brief:
      <run>comp-blast opal-partners-data</run>
      <expect>Blast radius identical to the Phase 1 baseline — this is a
      read-only probe, nothing changed.</expect>
      <if_mismatch>If the blast radius differs, something non-probe was touched —
      stop and flag to 2.0.0_SA_COO~C immediately.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Phase 0 is read-only: it reads S3 listings, portal source, Terraform,
    Lambda source, and DynamoDB metadata, and writes only a new probe brief under
    docs/briefs/. It touches no file or S3 key owned by another active TO.
    Phases 1-4 will carry cross_domain_coordination blocks; this one does not. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Probe brief committed to docs/briefs/ (suggested:
       advi-demov1-phase0-serving-path-pii-probe-20260521.md) on CLOUD, authored
       under your serial.
    2. The brief gives a DEFINITIVE answer to the §3.2 unknown: it names the
       concrete mechanism — the CloudFront distribution + behavior(s), and/or the
       origin-request Lambda@Edge function and the map it reads, and/or a §3.3
       dedicated static adapter — by which `?firm={suffix}` selects an origin
       bucket. "Likely" / "probably" is not acceptable; cite the Terraform
       resource, edge-function source, or live AWS CLI config that proves it.
    3. The brief states an explicit go/no-go on the static serving path for a new
       `demo` firm, and a recommended Phase-1 routing approach (new CF behavior |
       edge-map entry | dedicated static adapter) with the rationale.
    4. The brief contains a per-file-type PII field inventory table covering all
       four platinum file scopes (firm-level, per-advisor, per-client,
       per-account files), every PII-bearing field named, with a reconciliation
       column versus the ADVI_ANONYM map: MATCH (in both) | ANONYM-ONLY |
       DEMOV1-ONLY (field the full-tree walk found that the serve-time path never
       returned). Every DEMOV1-ONLY field is the §6 belt-and-suspenders payoff —
       call each out explicitly.
    5. The brief confirms, with evidence, whether opal-partners-data is the ONLY
       dynamic server and whether the portal is platinum-only — specifically
       whether any portal surface still triggers an on-demand gold/ read
       (risk #6: bd-client-detail reads gold/clients/{id}.json with INPUT_BUCKET
       hardcoded to opal-data-bd). State whether platinum fully supersedes it.
    6. The brief lists every firm-specific code branch found (firmId === / firm
       === / bucketSuffix / ROUTER_FIRM_SUFFIX / Inflection observability
       sentinels / the §3.3 static-adapter override) with a demo-firm-trips-it
       Y/N assessment for each, and notes any portal/Lambda change a `demo` firm
       would require.
    7. The brief includes a current live platinum file manifest (per-prefix
       object counts + the per-scope file lists) — refreshing the proposal §2.2
       numbers as of probe time.
    8. Session log committed with a Compiler Tools section: comp-routes trace,
       comp-pii audit, comp-blast opal-partners-data — each with the command,
       result, and what it showed (or why a fallback was needed).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">docs/briefs/advi-demov1-phase0-serving-path-pii-probe-20260521.md</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-21/advi_demov1_phase0_probe~C.md</file>
      <file action="reference">docs/proposals/advisor-intelligence-demo-dataset-20260521.md</file>
      <file action="reference">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="reference">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/</file>
      <file action="reference">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/pseudonymizer.py</file>
      <file action="reference">docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md</file>
      <file action="reference">docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Resolve the §3.2 static-platinum serving mechanism to a
    concrete, evidenced fact: which CloudFront distribution serves PLATINUM_BASE
    routes, what behavior(s) it carries, whether an origin-request Lambda@Edge is
    in the path, and exactly how `?firm={suffix}` is translated to an origin
    bucket. Inspect the portal fetch code, the CloudFront Terraform, the edge
    function source if present, and live AWS config as needed.</requirement>
    <requirement id="2">Perform an INDEPENDENT per-file-type PII field inventory
    by walking the real structure of each platinum file scope (firm / advisor /
    client / account). Do not inherit the ADVI_ANONYM field map — reconcile
    against it. Every field that carries a real firm name, advisor name, client
    name, account name/number, or a z-prefixed BD id (in content OR in an S3 key
    slug) must be enumerated.</requirement>
    <requirement id="3">Confirm the dynamic-serving topology: opal-partners-data
    is the only dynamic server; characterize whether the portal is strictly
    platinum-only or whether any surface triggers an on-demand gold/ read.
    Inspect bd-client-detail's INPUT_BUCKET specifically.</requirement>
    <requirement id="4">Audit firm-specific code branches (firmId/firm equality
    checks, bucketSuffix/ROUTER_FIRM_SUFFIX translation, the inflection
    static-adapter override, observability sentinels) for any path a new `demo`
    firm would fall into incorrectly or fail to be recognized by.</requirement>
    <requirement id="5">Confirm whether the Lambda pseudonymizer's own-firm
    exemption skips hashing when a demo user views the demo firm as its own firm
    (proposal §4 open item) — state the behavior so Phase 2/4 can rely on it.</requirement>
    <requirement id="6">Deliver all findings as a single probe brief structured
    to drop directly into the CTO PRD's risk section. RAVC completion to
    2.0.0_SA_COO~C.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">docs/briefs/advi-demov1-phase0-serving-path-pii-probe-20260521.md — the probe brief satisfying acceptance criteria 2-7</deliverable>
    <deliverable type="commit">Brief + session log committed to CLOUD under your serial via .tools/safe-commit.sh</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT create the opal-data-demo bucket, write any Terraform, register
    any DynamoDB firm record, or create any Cognito user. Phase 0 ships nothing —
    those are Phases 1 and 3.</rule>
    <rule>Do NOT build or run the transform engine, or write to any S3 bucket.
    This probe is strictly read-only against existing infrastructure.</rule>
    <rule>Do NOT inherit the ADVI_ANONYM PII field map as the answer. It is vetted
    for the serve-time response path only; the demo walks the full platinum tree.
    Reconcile against it — independent inventory is the entire point of this
    probe per the §6 caveat.</rule>
    <rule>Do NOT start Phases 1-4. They are gated on the CTO PRD ship and COO~C
    decomposition. If Phase 0 surfaces something that changes the phase plan,
    flag it to 2.0.0_SA_COO~C — do not act on it unilaterally.</rule>
    <rule>Do NOT settle for a "likely" / "probably" answer on the §3.2 mechanism.
    If a tool cannot resolve it, escalate the gap to 2.0.0_SA_COO~C rather than
    closing the TO with the linchpin unknown still open.</rule>
  </do_not>
</task_order>
