# OPAL_ANALYST.W4a — atom_decomp `/security-scanner` (the FIRST census-less page)

<task_order>
<id>OPAL_ANALYST.W4a</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.1.0_DE_MarketIntelligence~Z</issued_to>
<date>2026-08-12</date>
<status>pending</status>
<priority>P1</priority>
<!-- RE-ROUTED 2026-08-12 ~0145Z from 0.5.0_AE_OpalETL~Z to 0.1.0_DE_MarketIntelligence~Z (CTO
     role-fit call) so the portal program does not stall on one seat's availability. GO IS IMMEDIATE
     -- nothing here waits on anyone. Owned-paths grant OPAL_ANALYST_W4A_RUN landed @d6dd3a7772;
     the run home is committable by this seat, exercised with controls. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 — **§9.2.1 (the W4 three-way split, measured) and §9.8.1-V (enumeration-frame obsolescence) are NEW and are the reason this TO exists in this shape.** Full §9.8.1 A–V regime binds.</ref>
  <ref type="prior-art">**NONE. THIS IS THE POINT.** `/security-scanner` has no census. Per the PRD's own sequencing rationale, W1–W3 were census-backed so a wrong answer was cheap to spot; here **the run is the only source.**</ref>
  <ref type="reading">**READ A FAILED ATTEMPT, NOT ONLY PASSING RUNS** — `runs/portal-page-portfolios/20260811T1640Z/certification.attempt1.VOID.json`. That is **MY** voided certification: I scoped an S1 test to the zero-caller entities, MISSED the planted mutant, and reported a global PASS. **A passing run cannot teach you the failure mode, because everything in it worked** — and the plant/seal mechanic is the part of this regime a first author is most likely to get wrong. The VOID is retained deliberately, for exactly this.</ref>
  <ref type="method">**You have not run an atom_decomp before, and this TO does not assume you have.** The method is the PRD spec, not an oral tradition: §9.8.1 A-V is the regime, §8 is the rectangle schema, and **`workflows/atom_decomposition/runs/` carries five seats' completed runs as worked examples** (`portal-page-*`, `comp-verdict-tools`, `freshness-deploy-verdict-tools`). Read one end-to-end before starting; `portal-page-macro` is the closest shape to yours. **Ask me anything about the method — a question costs minutes, a wrong axis costs the run.**</ref>
</references>

<scope>
`/security-scanner`, page grain, one run: `workflows/atom_decomposition/runs/portal-page-security-scanner/<stamp>/`.

**Measured frame at portal `ce98e334` (file-backed, §9.2.1): 16 files · 2,726 lines · 5 `useQuery` ·
0 `useMutation` · `src/api/endpoints/security-scanner.ts` 76 lines, 0 writes.** Control-sized and
**pure-read — today's axis fits, which is exactly why this page goes first of the six.** It is the
one W4 unit where the method meets *census-lessness* WITHOUT also meeting a new entity kind.

⚠ **Treat that frame as MY prior claim under test, not as your denominator** — re-derive it.
</scope>

<requirements>
  <requirement id="1">**DUAL-PLANE ENUMERATION IS THE HEADLINE REQUIREMENT (§9.8.1-V).** Enumerate the entity set TWICE, on **independent planes** — (a) page-directory/component traversal, (b) a non-page plane: the api-endpoint module, the served keys behind it, and/or the `comp-estate` thread. **Commit BOTH enumerations, separately, BEFORE reconciling them.** Every disagreement is a finding and goes in the run either way; **"both planes agreed" is a result only if they were genuinely independent — say how.**</requirement>
  <requirement id="2">**Name the census-lessness in the axis declaration.** On W1 the census caught a miss; here nothing does. State plainly what a missed entity would look like and what in your method would surface it — **if the honest answer is "nothing would," that is the finding, and it is a better deliverable than a confident rectangle.**</requirement>
  <requirement id="3">**Consecutive DRY cycles use DIFFERENT lenses (C), and on a census-less page at least one lens must not be page-rooted** — a second page-rooted pass inherits the same frame and is self-comparison (V).</requirement>
  <requirement id="4">Full §9.8.1 regime: axis + domain bar committed BEFORE measurement; evidence triples; validator-merged patches; K-derivation (consumable from dry); K.1 packet, c1/c2 excluded; K.2 attestation; fresh sealed plant, coordinates never in-object; denominators printed beside every count; rc captured as the very next statement (I).</requirement>
  <requirement id="5">Findings land as findings — no fixes, no deletions, nothing notification-shaped. Residue gets Rule-9 disposition rows, never acts.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for every search; `comp-estate` for the non-page enumeration plane; `comp-cache collisions` if you touch query-key identity (HUD-routed, deterministic vs grepping `useQuery`).</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — semantics (Plane B/C, evidence as objects) + certification with K.2 attestation. Hand off at DRY. **Tell them early that this is your first run** — the certifier calibrates to the author, and that is a legitimate thing for them to know, not an admission.
- **0.5.0_AE_OpalETL~Z** — the method's most-practised author (W1 six pages, W2, W3a, W3b). **Their runs are your reference. They do NOT approve your work and no sign-off from them exists** — this is a reading source, not a review step.
- **1.0.0_SA_CTO~Z** — PRD owner; method findings and the surprise channel to me. **The W4c axis extension is my deliverable, not yours — but if you reach it first, propose it and I ratify. No approval step exists.**
- Lane commits only; no push.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bar committed verifiably BEFORE first measurement; census-lessness named per requirement 2.</criterion>
  <criterion id="C2">**BOTH enumerations committed independently before reconciliation; independence argued; disagreements named — or zero-disagreement stated explicitly WITH the independence argument.**</criterion>
  <criterion id="C3">Rectangle schema-valid; declared/deployed/serving separated; SERVED limb grounded live or exercised, never read from config.</criterion>
  <criterion id="C4">DRY by convergence, lens-diverse, **at least one non-page-rooted lens**, evidenced in run.json.</criterion>
  <criterion id="C5">`certification.json` signed by CVO~Z with reconstruction attestation; plant caught, or attempt VOIDed and RETAINED.</criterion>
  <criterion id="C6">Consumable derived from dry (K); packet = K.1 exact set, c1/c2 excluded, composition stated.</criterion>
  <criterion id="C7">Session log + declared exclusions + surprises; semantics staged for W5 per CVO's lift constraints.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7</expected_criteria>
  <instance_path>org/tier3_junior/0.1.0_DE_MarketIntelligence/deliverables/OPAL_ANALYST.W4a_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package at `runs/portal-page-security-scanner/<stamp>/`, full K-regime set</deliverable>
  <deliverable type="document">**The dual-plane enumeration reconciliation (C2)** — the first census-less unit's independence evidence</deliverable>
  <deliverable type="document">Proof-of-spec instance, validator-clean before any status flip; session log</deliverable>
</deliverables>

<do_not>
  <rule>No monitors/alerts (moratorium) · no fixes/deletions (Rule 9) · no push · **no single-plane enumeration** · a frame inherited from W1–W3 is never assumed to still fit (V).</rule>
</do_not>
</task_order>
