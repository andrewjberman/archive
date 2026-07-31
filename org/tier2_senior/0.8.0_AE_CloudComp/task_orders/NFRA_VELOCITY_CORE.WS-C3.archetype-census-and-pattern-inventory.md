<task_order>
<id>NFRA_VELOCITY_CORE.WS-C3.archetype-census-and-pattern-inventory</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<status>pending</status>

<priority>P2 -- OPEN AS OF 2026-07-31. P1 (C1+C2) closed; P2 = C3 + C7. WS-C7 is with 0.7.0_AE_CloudOps~Z; THIS is the other half. NFRA_VELOCITY remains the EXCLUSIVE work regime.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C3</ref>
  <ref type="upstream">org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C2_STEP2_MSBEFF_BY_CLASS.md -- the 718 are ALREADY class-typed; do not re-derive</ref>
  <ref type="upstream">org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C2_STEP1_INSTANCE_CROSSTAB.md -- the incident cross-tab and its five-population denominator problem</ref>
  <ref type="target">the census + inventory are DELIVERABLES in your lane; the rule bank is NOT touched by this TO</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (LANDED, binds you)</ref>
</references>

<objective>
Produce WS-C3's two artifacts:

**(a) THE ARCHETYPE CENSUS** -- per-plane motif frequency **with printed denominators**, starting from
the tick-29 uncovered-edge gap already recorded in the rule bank (`c1_frontend_adapter`): 11 live edge
types carrying flow/grain with no ratified relation binding, 3912 edges, of which RENDERS 2447 +
PROP_PASSES 1382 = 97.9% are frontend flow. Also the declared-but-zero-live tokens.

**(b) THE PATTERN INVENTORY** -- pattern -> archetype -> instantiating tools -> gaps, seeded from the
registered comp-tool population, the MSBEFF 718 (ALREADY CLASS-TYPED -- consume step 2's table, do not
re-type items), the rail-override intents, and **the debt shapes as named first-class patterns**
(LEGACY-WRITER, CLOBBER, SILENT-RESIDENT, TRIGGER-MISSEQUENCE).

**THE COMPRESSION RATIO IS ITSELF A FINDING.** The PRD expects the inventory to be far smaller than the
tool count. Report the ratio; do not smooth it.

**ENDS WITH: the ranked tool-gap list** -- the generative "what tool is missing" answer the estate
cannot currently produce.
</objective>

<constraints>
1. **THE RULE BANK IS NOT TOUCHED BY THIS TO.** WS-C3 is a census and an inventory. If the census
   implies a vocabulary change, **STOP and route it to me** -- that is WS-C1 round 2, not this.
2. **HELD-OUT FENCE BINDS.** `ADVI_PERFORMANCE` / `MDPF_GLOBAL` must not shape anything, and
   **PUBLISH YOUR SHAPING CORPUS** -- an unnamed one is indistinguishable from a breached one. The
   fence is now IN the rule bank at `dynamic_rails.held_out_fence`; read it before you start. Note its
   `scope_note`: the DECOMPOSITION precondition on those projects was released; **THE FENCE WAS NOT.**
3. **DO NOT HAND-COUNT WHAT A GATE MAINTAINS.** The tool population is `comp-manifest-check`'s, not a
   `ls .tools/comp-*`. My own `ls` returns 94 against the PRD's "~96" -- **cite the gate, and if the
   gate and the PRD disagree, the gate is right and the disagreement is a finding.**
4. **NO NON-ASCII. No emojis.**
5. Standard: additive, no unilateral schema moves, report before deciding on anything that looks like
   it needs a ruling.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-manifest-check completeness (or its registration-invariant count) -- the AUTHORITATIVE tool population</run>
      <expect>A gate-maintained count. Record it AS the gate's number with the gate named. If it differs from the PRD's "~96", report the delta rather than reconciling silently.</expect>
      <if_mismatch>The gate is the authority. A PRD prose count that has drifted IS a finding for the census.</if_mismatch>
    </step>
    <step>
      <run>comp-kuzu (or comp-which -> the routed tool) for live edge-type frequencies per plane</run>
      <expect>Per-plane motif/edge counts with a PRINTED DENOMINATOR -- never a bare top-N. Read the provenance header: a projection is a vintage.</expect>
      <if_mismatch>If the graph cannot supply a per-plane denominator, that is a coverage finding for the census, not a reason to estimate one.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-derive the compression ratio from the committed artifacts</run>
      <expect>inventory size / tool count, both from their cited sources, reproducible by a reader.</expect>
      <if_mismatch>Fix the artifact, not the ratio.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The archetype census exists, **per-plane, with printed denominators on every count** -- no bare
   top-N anywhere.
2. The tick-29 uncovered-edge gap is carried forward with its numbers (11 live types / 3912 edges /
   the 97.9% frontend concentration) and the declared-but-zero-live tokens are enumerated.
3. The pattern inventory exists as **pattern -> archetype -> instantiating tools -> gaps**, with the
   four debt shapes present as first-class patterns.
4. **THE COMPRESSION RATIO IS PUBLISHED** with both of its inputs cited to their sources.
5. **THE RANKED TOOL-GAP LIST** exists and is ordered by a stated criterion, not by impression.
6. Every population count cites the instrument that produced it. **A count with no named source is not
   a measurement.**
7. Shaping corpus published; held-out fence demonstrably unbreached.
8. Session log with a Compiler Tools section reproducing each run vs expect.
9. Report to me on land WITH the commit hash. I gate; CVO~Z verifies after my gate.
</acceptance_criteria>

<cross_domain_coordination>
- **`0.7.0_AE_CloudOps~Z` holds WS-C7** (the recall standard), P2's other half. **WS-C3's ranked
  tool-gap list and WS-C7's recall declarations will meet** -- a tool that cannot state what it could
  not have found is a different gap from a tool that does not exist. **Do not build C7's contract
  inside C3.** If they collide, route to me.
- **`3.0.0_SA_CVO~Z` verifies after my gate**, and is under self-imposed exposure bindings: it authors
  no vocabulary and recuses from scope-shaped amendments. **The census is measurement, so it is
  verifiable within those bindings** -- but do not ask it to rule on vocabulary.
- MSBEFF's 718 are **already class-typed** in WS-C2 step 2 (RECALL 50.6% / not-a-defect 22.6% /
  tuple-typed 6.4%). **Consume that table. Re-typing them would re-derive an existing classification**,
  which is the same trap step 2 avoided.
</cross_domain_coordination>

<notes>
**A DENOMINATOR TRAP IS ALREADY WAITING FOR YOU, AND I HIT IT AN HOUR AGO.** The PRD says "187
rail-override intents." `org/mcp/comp-which-rail.log` on this device reads **261 lines** -- and per
**LD-0362's caveat, that log is DEVICE-LOCAL** (`.gitignore:68`), so the laptop's half is not in it and
neither number is a fabric count. **If you cite rail-override volume, label it PER-DEVICE.** A count
from a device-local artifact reported as an estate figure is the exact class MSTR~Z has now measured
four times tonight.

**AND THE HARDER ONE, FROM MY OWN WS-C2 WALK:** the incident taxonomy has **five populations and no
canonical artifact** -- 204/208/210/219/221 depending on the parse, because the "210-row instance
table" is a *proposed move* that does not exist. **MSBEFF, by contrast, has `findings_merged.jsonl` and
every published figure reproduces off it exactly.** When you cite either corpus, **cite which artifact
and which parse.** The lesson is cheap to state and I paid for it three times: **a self-chosen
denominator cannot refute the instrument that chose it -- prefer a denominator you did not construct.**
</notes>
</task_order>
