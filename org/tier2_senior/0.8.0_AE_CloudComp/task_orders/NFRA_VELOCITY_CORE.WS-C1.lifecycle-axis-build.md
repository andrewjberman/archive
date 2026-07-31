<task_order>
<id>NFRA_VELOCITY_CORE.WS-C1.lifecycle-axis-build</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<status>pending</status>

<priority>P1 -- THE CRITICAL PATH. NFRA_VELOCITY is the EXCLUSIVE work regime (Andrew GO 2026-07-31 ~0225Z); WS-C1 is CORE's P1 first half and WS-C2 cannot start until this enum exists to validate.</priority>

<amendment date="20260731T0330Z" by="1.0.0_SA_CTO~Z">
**THE SPEC IS NOW REV 3 @691860493. HOLD RELEASED. BUILD FROM THE SPEC FILE, NOT FROM THIS TO's BODY.**

Everything below this block was written against spec rev 1 and IS STALE IN THREE PLACES. The spec file
is authoritative; where this TO and the spec disagree, THE SPEC WINS. Specifically superseded:

- **objective (a)'s enum list is WRONG.** It names `PERMANENT / ROLLING / TRANSIENT / EVENT_CREATED /
  SUPERSEDED / RETIRED / UNDECLARED`. The correct 7 are
  **`PERMANENT / TRANSIENT / EVENT_CREATED / DORMANT / LEGACY / RETIRED / UNDECLARED`**.
  `ROLLING` collapsed to a derivation (F-8); `SUPERSEDED` renamed `LEGACY` and the typed violation
  `ZOMBIE/ORPHAN` renamed `SILENT-RESIDENT` (F-1) -- **both old tokens are ALREADY OCCUPIED in ratified
  `variance.labels` and MUST NOT appear.** `DORMANT` added (your own catch).
- **objective (e) and acceptance item 5 name `ZOMBIE-ORPHAN`.** Use `SILENT-RESIDENT`, and the gate
  must name **BOTH** it and **`variance.Orphan`** as gated consumers -- that was the BLOCKING finding.
- **acceptance is now the spec's S.7 items 1-13**, not the 9 listed below. New requirements you did not
  have: `consumer`/`successor` EXERCISED not merely resolved (F-4); `max_dwell` BOUND to the consumer's
  D3 cadence (F-3); `revalidate_by` on EVERY declaration (S.3.1); an explicit `scope` per declaration
  (F-6); and **>=1 CONSUMER ACTUALLY GATED, which prose cannot discharge (F-7)**.

STILL BINDING AND UNCHANGED: every constraint (additive-only, `type_tuple` untouched, no name-pattern
inference, the held-out fence, no non-ASCII), the whole compiler-tools mandate, and the
cross-domain-coordination block. Re-run your phase-1 consumer enumeration against the rev-3 shape
before landing -- `DORMANT` and `scope` add fields the rev-1 shape did not have.
</amendment>

<amendment date="20260731T0345Z" by="1.0.0_SA_CTO~Z" subject="THE LAND PATH -- an omission in my original TO">
**THIS TO NAMED `0.8.0_AE_CloudComp~C` AS BUILDER OF AN ARTIFACT ITS LANE STRUCTURALLY CANNOT LAND,
AND NEVER STATED THE LAND PATH. That gap is mine, not the lane's, and it is corrected here.**

`org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` resolves to lane **`ANY_EXEC`**. Verified by me
directly against `.tools/owned-paths-validate.py`, with positive controls (two real refusals on paths
I do NOT own, so the instrument is discriminating, not permissive):

```
lane(NFRA_ONTOLOGY_RULE_BANK.yaml)            = ANY_EXEC
check_agent(1.0.0_SA_CTO~Z,       rulebank)   = True
check_agent(3.0.0_SA_CVO~Z,       rulebank)   = True
check_agent(0.8.0_AE_CloudComp~C, rulebank)   = False   <- the builder
check_agent(0.8.0_AE_CloudComp,   rulebank)   = False   <- base too; the tilde auto-permit does not rescue it
control: check_agent(1.0.0_SA_CTO~Z, org/tier0/ledger/LD-0001.md)  = False  [TIER0_MSTR]
control: check_agent(1.0.0_SA_CTO~Z, .../data_refresh/handler.py)  = False  [DATA_REFRESH_DEPLOY]
```

**CANONICAL LAND PATH FOR THIS TO AND EVERY WS-C1/WS-C2 RULE-BANK INCREMENT:**
> **BUILD + verify (`~C`) -> HAND OFF the content + commit message -> GATE + LAND (`1.0.0_SA_CTO~Z`),
> builder credited in the commit message -> signal `3.0.0_SA_CVO~Z` to verify.**

**A LANE-ADD WAS PROPOSED AND IS REJECTED -- on governance, not on speed.** `~C` correctly routed the
ask instead of self-landing (SoD: the grantee never lands its own grant) and reasonably suggested
widening the lane so future increments do not relay through me. Rejected because **the exec-lock is
deliberate** -- the rule bank's own header says *"Canonical placement (org/modules/graph, exec-locked)
routes through CTO -- like the census"* -- and it is the SINGLE vocabulary carrier for BOTH fabrics.

The decisive point: **the relay is not overhead, it IS the gate.** Acceptance already requires CTO~Z to
gate items 1-17 before CVO~Z verifies, so the artifact must pass through me regardless; landing it
myself is the same act, not an extra one. **Widening the lane would make it possible for an increment
to land WITHOUT passing that gate** -- converting a structural guarantee into a promise to wait. That
is the DESIRED-vs-APPLIED substitution acceptance item 10 exists to forbid, applied to the gate itself.
</amendment>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C1</ref>
  <ref type="design">org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C1_LIFECYCLE_DESIGN_SPEC.md @bab75bba5 -- THE SPEC YOU BUILD FROM. Read it in full before writing YAML.</ref>
  <ref type="target">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- meta.version "1.7" at spec authorship; additive section inside dynamic_rails.D3_contract_obligation</ref>
  <ref type="fence">MSTR~Z relay 20260729T233721Z -- the WS-C2 held-out set (ADVI_PERFORMANCE, MDPF_GLOBAL)</ref>
</references>

<objective>
Build the D3 LIFECYCLE AXIS into the rule bank, per the design spec. The rule bank today has D1/D2/D3
and ZERO lifecycle vocabulary; this is the additive subsection that closes it.

Scope is the spec's S.7 acceptance list, items 1-6. In brief:
(a) a `lifecycle` subsection under `dynamic_rails.D3_contract_obligation` carrying the 7-value
    `lifecycle_class` enum -- PERMANENT / ROLLING / TRANSIENT / EVENT_CREATED / SUPERSEDED / RETIRED /
    UNDECLARED -- with TRANSIENT explicit (the PRD's named vocabulary requirement).
(b) each value states its absent-at-rest AND present-at-rest polarity explicitly. The spec's S.2 table
    IS the content; do not compress it to a gloss. The polarity is the whole point of the axis.
(c) each value carries its S.3 required fields, and a missing/unresolvable required field renders
    UNKNOWN LOUD -- NOT a fallback to the declared value, NOT a fallback to PERMANENT.
(d) UNDECLARED as the default, scoped per S.4: it constrains what a tool may CLAIM, not what a tool
    may CHECK. State that bound IN the rule bank, not only in the spec.
(e) the S.5 derivations as derivations (debt / stranded / incomplete-decommission / frozen-vs-stale),
    and the S.5.1 ZOMBIE-ORPHAN lifecycle gate as a consumer contract.
(f) `meta.version` head advances; the changelog comment names the spec commit AND carries the S.0
    shaping-corpus declaration so a later reader can verify the held-out fence.

YOU ARE BUILDING A DECLARED VOCABULARY, NOT A DETECTOR. No tool is rewritten under this TO.
</objective>

<constraints>
1. ADDITIVE ONLY. The ratified C0-C3 vocabulary, the 14 roles, the 10 relations, and the variance +
   completeness axes are BYTE-IDENTICAL after your change. If you believe one must move, STOP and
   route to me -- that is the ratification chain, not this TO.
2. `type_tuple` IS NOT AMENDED. lifecycle_class is a D3 obligation FIELD, not a fifth tuple field.
   Amending type_tuple changes the canonical enum set base 0.8.0's registration invariant validates
   every comp-tool against -- a comp-tool STANDARD change that routes to MAIN CTO under the standing
   carve. If the build seems to require it, STOP and route to me. This is a seam, not a judgement call.
3. DO NOT INFER LIFECYCLE FROM NAME PATTERNS. Producer-asserted, never observer-inferred. Any
   implementation that derives lifecycle_class from key names, directory position, or observed absence
   has rebuilt the comp-legacywriter stopgap with more syntax, and I will reject it at gate.
4. HELD-OUT FENCE BINDING: do not use any ADVI_PERFORMANCE or MDPF_GLOBAL surface as a vocabulary
   example, and do not author a contract to make a rail look expressive. If you need an example, use
   one from the spec's S.0 declared corpus.
5. No emojis / non-ASCII anywhere (CLAUDE.md Code Quality; the commit gate will catch you, and it
   caught its own author on this device tonight).
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "what reads the ontology rule bank" -- then the routed tool (expect comp-kuzu / comp-estate class) to enumerate the rule bank's CONSUMERS</run>
      <expect>The set of readers that would be affected by a new D3 subsection, with a printed denominator. An additive section should have ZERO breaking consumers; if a consumer parses D3 strictly (fixed key set), that is a finding to report BEFORE writing, not after.</expect>
      <if_mismatch>If any consumer would break on an added key, STOP and report to me with the consumer named. Do not "fix" the consumer under this TO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>python -c "import yaml,sys; d=yaml.safe_load(open('org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml')); print(sorted(d['dynamic_rails']['D3_contract_obligation'].keys())); print(d['meta']['version'])"  # rail-checked: YAML structural parse of a specific known file; no comp-tool models rule-bank internal key structure</run>
      <expect>The lifecycle key present under D3; meta.version advanced past 1.7. Parses clean (a YAML syntax error in the rule bank breaks every consumer at once).</expect>
      <if_mismatch>Fix before commit. A rule bank that does not parse is worse than one without the axis.</if_mismatch>
    </step>
    <step>
      <run>git diff org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- inspect for any change OUTSIDE dynamic_rails.D3 + meta</run>
      <expect>ZERO hunks touching C0-C3 vocabulary, roles, relations, variance, completeness, or type_tuple. This is the constraint-1/2 self-check and it is mechanical.</expect>
      <if_mismatch>Revert the out-of-scope hunk. If it seemed necessary, that is a route-to-me, not an edit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the phase-1 consumer enumeration against the committed head</run>
      <expect>Every consumer still reads the rule bank without error; the added section is visible to whatever consumes D3.</expect>
      <if_mismatch>Report immediately -- an additive change that broke a consumer is a finding about the consumer's strictness and I want it.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. `dynamic_rails.D3_contract_obligation.lifecycle` exists carrying all 7 enum values, TRANSIENT
   explicit -- YAML-parse-provable, not prose-provable.
2. Every value carries both polarities (absent-at-rest, present-at-rest) AND its S.3 required fields.
3. A missing/unresolvable required field is documented as rendering UNKNOWN LOUD, with the explicit
   statement that it does NOT fall back to the declared value or to PERMANENT.
4. UNDECLARED is the documented default AND the claim-vs-check bound (S.4) is stated in the rule bank.
5. The four S.5 derivations present AS derivations; the ZOMBIE/ORPHAN lifecycle gate (S.5.1) present
   as a consumer contract naming `lifecycle_class NOT IN {TRANSIENT, EVENT_CREATED}` and the
   UNDECLARED-renders-UNKNOWN rule.
6. `meta.version` advanced; changelog comment cites the spec commit + carries the S.0 shaping-corpus
   declaration.
7. `git diff` shows ZERO hunks outside `dynamic_rails.D3_contract_obligation` and `meta`.
8. Session log with a Compiler Tools section reproducing each <run> vs <expect>.
9. Report to me (1.0.0_SA_CTO~Z) on land WITH the commit hash. I gate items 1-7 before CVO~Z verify.
</acceptance_criteria>

<cross_domain_coordination>
- `3.0.0_SA_CVO~Z` VERIFIES this and is already oriented on it (broker summary names WS-C1
  lifecycle/TRANSIENT + the held-out fence). Verify happens AFTER my gate, not in parallel -- do not
  ask CVO~Z to verify a build I have not gated.
- The rule bank is CROSS-DOMAIN by construction: it is the SINGLE vocabulary carrier for both fabrics
  (NFRA_VELOCITY_PROGRAM section 3c -- WORLDMODEL classes are proposals earning in by ratification;
  CORE vocabulary is cited, never imported). An edit here is visible to the main fabric. Additive-only
  is what keeps that safe.
- `type_tuple` is base `0.8.0_AE_CloudComp`'s registration-invariant surface. Constraint 2 exists so
  you do not silently widen a gate your own base serial enforces.
- `0.7.0_AE_CloudOps~Z` supplied the EVENT_CREATED evidence (the four-state partition of a 404). If
  you need the specimen detail, it is in the spec S.0 item 3 and their msgs 20260731T024616Z /
  024950Z. They are NOT on this TO and are not to be pulled onto it.
</cross_domain_coordination>

<notes>
WHY THE POLARITY TABLE IS THE DELIVERABLE AND NOT DECORATION: a detector that merely KNOWS about
TRANSIENT and skips it is a skip-list. Absence is HEALTHY on 2 of 7 rows and presence is a FINDING on
2 of 7, so a single-polarity existence detector is wrong on 3 of 7 -- and wrong in the direction that
proposes deleting live infrastructure. That is not hypothetical: a live pipeline trigger
(gold/trigger-pending.json class) reached a kill list's top tier on "no object found", and WS-E3's
>=2-CONFIRMED bar did not save it because a transient key independently reads absent AND dormant AND
reader-less -- two confirmed signals, both wrong. Confirmation across correlated instruments is not
independence.

WHY EVERY DECLARATION NEEDS A FALSIFIER: this axis SUPPRESSES findings. An unfalsifiable suppressor is
a silencer that now carries the authority of a type system. TRANSIENT requiring a D2-resolvable
consumer + max_dwell is what makes the declaration itself checkable -- and it recovers STRANDED
(written, never consumed = a dead pipeline leg), which no instrument in the estate can currently state
in either direction. Build the fields as REQUIRED, not as optional metadata.
</notes>
</task_order>
