# validation_context_declaration -- comp-adversary v1
family: L0a boundary_report SIBLING (declaration + conformance + pins + denominators)
read-vintage: HEAD @749415b9a0 at 2026-09-11T01:40:40Z  [pin kind: read-vintage]
artifact: org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/IRPT_BCKEND.TO-IB-s-3.the-enforcement-library-reauthorize-before-serve.proof_of_spec.json
artifact-vintage: UNCOMMITTED (n/a)

## AUTHOR PROFILE (what the author's evidence context WAS)
pins found: 0 commits, 12 repo paths, 0 file:line cites, 3 tool mentions
tools cited: comp-adversary, comp-iam, comp-schedule
!! HEX RUNS PRESENT BUT ZERO PARSED AS PINS (3 run(s)): 62301f71e0, 749415b9a0, f61edc41fc
!! The pin parser saw NOTHING while the bytes carry commit-shaped hex. Either
!! these are digests/ETags/snapshot-ids (not pins -- fine), or the citation
!! form is one COMMIT_RE cannot read, in which case source 1's '0 attempted'
!! is a PARSER zero, not an evidence zero. They are byte-identical in output.
!! The runs are printed so this is inspectable rather than merely alarming.

## COMPLEMENT (what the validator should know the author may NOT have seen)

### source 1: cited-commit verification (0 attempted / 0 verified / 0 UNVERIFIABLE)

### source 2: cited-path vintage (12 attempted / 12 stable / 0 flagged)

### source 3: decomposition neighborhood (T11 admissibility -- the cell's graph, not the filesystem)
  owned cells: IB-s-3 | decomposition: org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md | project: org/missions/D9/IRPT/IRPT_BCKEND
  dependencies (ONE HOP): 0 -- decomp depends_on column: none | TO-declared read-dependencies: none
    in both carriers: none | decomp-only: none | TO-only: none
    IB-s-3 depends_on: (cell not found in a table carrying a depends_on column)
  members: 2 (proof instances found: 0)
  - org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md [decomposition] the rectangle the owned cells live in
  - org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md [prd] sections named by the artifact: FWD-2, s.1, s.2, s.6, s.8, s.9
  UNPROVEN dependencies: 0 of 0 -- none
  directory siblings: DEMOTED under T11 -- 38 uncited sibling(s) of cited paths NOT shown; filesystem adjacency is not admissible when the decomposition resolves (org/standards/ADMISSIBILITY_METHOD_T11.md)

### source 5: comp-read digests of the complement (THE PACKET -- stage 4)
  selection rule: ADVERSARIAL SALIENCE, one axis, first-match-wins over S1>S2>S3>S4 (MECE by construction; full record in the source header)
    S1 POSTDATES  changed after the artifact's vintage -- author could not have read this
    S2 KIN        shares a filename stem with a CITED path -- sibling-member/wrong-version class
    S3 DENSE      in a directory the author cited 2+ times -- demonstrably their working area
    S4 PERIPHERAL sibling of a directory the author cited once
  S1 NOTE: artifact has no commit vintage -- S1 is UNRESOLVABLE and reads empty
  domain: neighborhood members (the source-3 set)
  budget: 12 file(s) at <=2400 bytes each (raise with --digest-budget/--digest-bytes)
  selected: 2 of 2 neighborhood members
  class census: S1 0/0, S2 2/2, S3 0/0, S4 0/0
  NOT DIGESTED: 0 of 2 neighborhood members -- 0 beyond the budget, 0 non-text (comp-read is a text instrument; binaries stay in the denominator, never dropped)
  DEFERRED: 0 of 2 selected digest(s) did not return -- each names its reason below; for those files this packet is POINTERS ONLY
  WARN: THE PACKET IS A SELECTION, NOT A SURVEY. A file's ABSENCE from the digests below is a BUDGET fact, never an assessment that it did not matter.

  --- digest 1/2: org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md [class S2]
      digest basis: markdown-headings
  | comp-read: org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md
  |   241 lines | 50 section(s) via markdown-headings | question: (none given)
  | 
  |   SHAPE (all 50, never truncated):
  |         1-2     h1     IRPT_BCKEND -- L5 decomposition -- round 1 -- v0.1.1
  |         3-25    bold     v0.1.1
  |        26-29    bold     One carrier.
  |        30-53    h2     1. THE RECTANGLE -- nineteen cells
  |        54-55    bold     Outcome coverage, run not asserted: 10 of 10 `FWD-n` in the 
  |        56-61    bold     Placement axis:
  |        62-63    h2     2. WHAT L5 ADDS PER CELL (the PRD row carries everything els
  |        64-64    bold     `IB-s-18` is the ONE shared dependency beneath every other c
  |        65-65    bold     `IB-s-17` creates every tenant-scoped resource once
  |        66-66    bold     `IB-s-5` names the `FirmDestinationPolicy` OWNER: `0.7.0_AE_
  |        67-67    bold     `IB-s-6`'s reuse source is UNRESOLVED (PRD v0.3).
  |        68-68    bold     `IB-s-8` applies the host STOPPED.
  |        69-69    bold     `IB-s-9` proves the seven-step chain against a HAR-replay tr
  |        70-70    bold     `IB-s-10` cannot be certified against real PDFs because none
  |        71-73    bold     `IB-s-11` proves against the captured probe evidence
  |        74-74    bold     `IB-s-16` is late by construction:
  |        75-75    bold     `IB-s-15` includes the CloudFront behavior
  |        76-76    bold     `IB-sb-3` is the exercised proof of FWD-2
  |        77-80    bold     `IB-s-1` and `IB-s-12` are gold runners under CLAUDE.md rule
  |        81-107   h2     3. THE CHAIN READ -- computed from the edge set, not chosen
  |       108-111   bold     THE BINDING FACTS.
  |       112-131   h2     4. THE ROUND FENCE -- the dependency waves inside ONE issuan
  |       132-133   h2     5. SEATING AND THE FAN-OUT L6 WILL CARRY
  |       134-158   bold     All 19 cells are worker cells
  |       159-176   h2     6. TERRAFORM ROOTS, STATE AND THE DEPLOY DISCIPLINE
  |       177-195   h2     7. THE BATTERY -- run at L5, with each instrument's blindnes
  |       196-197   h2     8. BOUNDS THAT BIND EVERY ORDER, inlined at L6 where they to
  |       198-198   bold     NO LIVE VENDOR CALL
  |       199-199   bold     NO MONITOR, ALARM, SNS OR SES SEND
  |       200-200   bold     CROSS-FIRM, both shapes
  |       201-201   bold     Deploys
  |       202-202   bold     Andrew's four fixed constraints are not build choices:
  |       203-203   bold     No credential
  | ... DIGEST TRUNCATED at 2400 of 7437 bytes (per-file cap --digest-bytes; the FULL file is the territory, this was only ever an index into it)

  --- digest 2/2: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md [class S2]
      digest basis: markdown-headings
  | comp-read: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md
  |   304 lines | 10 section(s) via markdown-headings | question: (none given)
  | 
  |   SHAPE (all 10, never truncated):
  |         1-17    h1     IRPT_BCKEND -- Investor Reporting backend: ingestion, multi-
  |        18-102   h2     ENDPOINT (step 2, /endpoint --forward)
  |       103-127   h2     CELL CANDIDATES
  |       128-145   h2     CONTRACTS
  |       146-149   bold     v0.5 field additions from the supplement, no new browser con
  |       150-192   h2     PATHS
  |       193-204   h2     FIXTURES AND EVIDENCE
  |       205-250   h2     BRIEF COVERAGE
  |       251-285   h3     SUPPLEMENT COVERAGE (v0.5)
  |       286-304   h2     SURFACE MANIFEST
  | 
  |   SALIENT: (no --for question given; pass one to rank regions)
  | 
  |   QUALIFIERS: 63 in file | 63 near your regions (--all-quals for every one)
  |     ^ text that LIMITS / NEGATES / RETRACTS a nearby claim. This is where the
  |       right-file-wrong-conclusion lives: the claim gets read, this does not.
  |     !! 22: DONE WHEN  EXERCISED -- an advisor who has never used the workspace has searched, selected, and been shown the relationship and its permitted accounts
  |     !! 26: CONSTRAINT terminated clients STAY VISIBLE, marked terminated, access governed by entitlement; disappearance from search is never revocation
  |     !! 31: ...n suggestions, selected-account membership, report retrieval, job polling, cached results AND PDF download; a relationship containing an account outside the viewer's permitted population NEVER silentl...
  |        33: OWNER      IRPT_BCKEND.  CROSSES: IRPT_FNTEND handles the refusal -- no protected stale display, honest permission states, negative fixtures
  |     !! 34: ...last radius in the set: a defect is a CROSS-FIRM EXPOSURE; the estate's cross-firm rule is substrate-shaped, both shapes live (bucket-scoped Deny; key-prefix + IAM condition); graded on its own, never...
  |        40: ...ort, rendered view and PDF at one revision per partner and scope; relationship return uses a VENDOR CALCULATION for the exact selected account set -- summing or averaging account returns is not a subs...
  |        42: ...ry `calculated-performance.performance` is DECIMAL, daily breakdown `performance` is PERCENTAGE, daily `factor` links as product minus one; a normalizer treating both as one unit is wrong by 100x and ...
  |        50: ...Y REMOVED to obtain a successful report; clear inputs proceed PROGRA
  | ... DIGEST TRUNCATED at 2400 of 4224 bytes (per-file cap --digest-bytes; the FULL file is the territory, this was only ever an index into it)

  packet: 2 digest(s) delivered, 0 deferred, 5086 bytes total
  digest bases: markdown-headings x2
  ^ the BACKEND comp-read used per file. A change here changes this packet's CONTENT, so it is declared rather than left for a diff to discover. Extensionless python (the comp-* tools) reads via python-ast as of 2026-09-02; before that it fell to top-level-keys and enumerated UNBANDED.

### source 4: comp-state drift (raw excerpt -- validator reads full output)
  {
   "scanned_commits": 400,
   "records": 2825,
   "drift": [
    {
     "kind": "TO",
     "id": "NFRA_COMPUNIFY.S2.coverage-check-gate",
     "code": "NFRA_COMPUNIFY",
     "status": "?",
     "path": "org/projects/NFRA_COMPUNIFY/task_orders/NFRA_COMPUNIFY.S2.coverage-check-gate.md",
     "last": 1787682712,
     "verdict": "BEHIND",

## DECLARED EXCLUSIONS (sources the validator was NOT shown -- v1 contract)
  - toolgraph SHARES_SUBSTRATE independence : v1: toolgraph consumption not wired -- the independence oracle rides v2 (0.8.0 build)
  - comp-axes unexamined-axes (snapshot rows) : v1: snapshot-row consumption not wired (never live-render, per the 71.5s constraint)
  - comp-blast/comp-trace neighborhood expansion : v1: CODE-graph expansion (blast radius over the kuzu graph) not wired -- the neighborhood is the DECOMPOSITION graph under T11 when it resolves, else directory siblings; never a blast radius
  - comp-pulse warnings / comp-cochange diversity : v1: not wired
  - directory-sibling neighborhood (the pre-T11 source 3) : DEMOTED: the decomposition neighborhood resolved; 38 sibling(s) withheld

## DENOMINATORS
complement sources: 5 run / 0 deferred-with-reason / 5 declared-excluded
pin kinds: all pins in this declaration are READ-VINTAGE (declaration-vintage pins
appear only where the artifact itself recorded one -- trace-to-authority claims are
UNANSWERABLE from this declaration alone and are not implied).
