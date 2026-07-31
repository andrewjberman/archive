<task_order>
<id>NFRA_VELOCITY_CORE.WS-C8.doctrine-collapse</id>
<project>NFRA_VELOCITY_CORE</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.1.0_SA_COO</issued_by>
<status>staged</status>

<priority>DISPATCH-FIRST. C8 is PARALLEL-from-P1 and is the workstream FURTHEST from its own acceptance
while producing the most output. You are the warm seat with zero WIP. Composed by COO; gated by
1.0.0_SA_CTO~Z; CVO~Z reviews the TO itself.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_CORE_PRD.md -- WS-C8</ref>
  <ref type="upstream">org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C8_STAGING_LAWS_DERIVED_20260731.md -- staged L-ids (L-1..L-16 and counting)</ref>
  <ref type="target">docs/doctrine/MECHANISM_LAWS.md -- DOES NOT EXIST. Creating it is this TO.</ref>
  <ref type="corpus">INCIDENT_TAXONOMY -- the 14 mechanism-laws + the 210-row instance table</ref>
  <ref type="context">docs/doctrine/CONTROLS_OVER_CARE.md (95578 B, 1270 lines; section III at :175, III-a..III-g)
    -- **NOT a collapse-source. THE PRD'S "section-III family collapsed into the M-classes" DIRECTION IS
    IMPOSSIBLE BY WS-C2 STEP 0**: the M-taxonomy types WHERE AN ASSERTION SITS; section III types HOW AN
    INSTRUMENT LIES. They are different axes, so one cannot absorb the other. Read III for context; do NOT
    collapse it into artifact 1. **The PRD text carries the same impossible direction and that is a
    PRD-LEVEL correction for CTO~Z, not something to resolve inside this TO.**</ref>
  <ref type="fence">org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- dynamic_rails.held_out_fence (binds you)</ref>
</references>

<objective>
Execute the PREVENTION ruling: turn a growing pile of STAGED laws into a LANDED, collapsed doctrine head.

**FIRST ARTIFACT -- the ONLY thing this GO authorizes you to produce:**

  `docs/doctrine/MECHANISM_LAWS.md` as a SKELETON carrying the **14 taxonomy mechanism-laws ONLY**, each
  in the PRD's four-part form: {law <=2 lines | the exposing question | the gate-or-test that absorbs it |
  instance rows}. The gate-or-test cell is REQUIRED and may be `NO GATE POSSIBLE -- <reason>`, but it may
  NOT be blank.

Nothing else. Not the staged L-ids, not the M15 adjudication, not the CONTROLS_OVER_CARE collapse. Those
are artifacts 2, 3 and 4 and are NOT authorized by this GO. Report artifact 1 and stop.

**WHY THE SCOPE IS THIS NARROW -- it is the finding that produced this TO.** C8's acceptance says
*doctrine byte-count FALLS.* Measured 2026-07-31: staged laws went 7 -> 16 in about two hours,
`MECHANISM_LAWS.md` does not exist, and `docs/doctrine/` is byte-for-byte unchanged. The workstream is
running opposite to its own acceptance criterion. CTO~Z already booked "law-count inflation" as a residual
@3c6a1ffbd, then declined to mint L-17 for exactly this reason @0e1ea5e7c, and the staged set's own L-15 is
*flooding-hides-defects-while-looking-thorough.* **The corrective is not another law. It is landing the
collapse.** *(Scoped by CVO~Z's measurement: the staged laws are mostly NOT redundant -- see constraint 3. The collapse-not-started fact is what drives this TO, not law-count alone.)*
</objective>

<constraints>
1. **DO NOT AUTHOR A NEW LAW UNDER THIS TO.** If the collapse exposes a genuine new mechanism, STOP and
   route it to CTO~Z. A new law found during a collapse is a WS-C9 Route-C event, not a free write.
   CTO~Z has already set this precedent by recording an instance under L-1 instead of minting L-17.
2. **NOTHING DELETED.** Instances become rows. Dated material moves to `docs/references/`. Nothing Andrew
   called good is cut without his word. The collapse diff must show ZERO lost instances.
3. **THE STAGED L-IDS ARE NOT IN ARTIFACT 1** -- and the reason is now MEASURED, not assumed. CVO~Z
   mapped all 13 staged L-ids against the 14 M-mechanisms at source: **~10 of 13 are NOT in the
   M-taxonomy** (L-1, L-3, L-4, L-6, L-7, L-8, L-9, L-10, L-12, L-13); **~3 are genuinely close**
   (L-2 ~ M1, L-5 ~ M11, L-11 ~ M14). **The dedup pass is warranted for THREE, not for the set.**
   **AND THE TEN ARE NOT NOISE -- they are the residual CTO~Z's own WS-C2 step 0 named:** the M-taxonomy
   types WHERE AN ASSERTION SITS and **does not type INSTRUMENT FALLIBILITY, by construction.** The ten
   uncovered laws are predominantly **control-design laws** -- that gap being written down.
   **THIS RAISES A SCOPE QUESTION THAT IS CTO~Z's, NOT YOURS: `MECHANISM_LAWS.md` may need a second
   section, or the control-design laws a separate home, because they are not members of the corpus this
   file collapses.** Surface it; do not resolve it inside artifact 1.
   *(CVO~Z declared a conflict -- it authored several of the laws it judged -- so the split is marked
   UNVALIDATED-REUSE pending a non-author seat. Working figure with that caveat, not a settled one.)*
   **UPDATE, CVO~Z A18 @46ba560b9 -- the scope question has a MEASURED answer and it is neither of the two
   proposed.** CTO~Z ruled the ten already have a home in CONTROLS_OVER_CARE section III. Two of three of
   that ruling verify to the byte (95578 B, 1270 lines, III-a..III-g all present). **The COVERAGE claim
   fails**: section III is entirely about an INSTRUMENT or a MEASUREMENT lying, and **L-7 (property-not-
   event -> how a RULE is drafted), L-8 (actorless step -> how a PROCEDURE is drafted), L-9 (non-owner
   first exercise -> how a ROLE is constituted) are not instrument laws at all.** Containment scan over
   the full file, positive-controlled (the word "control" = 92 hits, so the scan works): `"names no
   actor"` 0, `"actorless"` 0, `"non-owner"` 0, `"role whose first"` 0, `"property, never the event"` 0,
   `"pre-commitment"` 0 -- **six zeros, real absence.**
   **So: MECHANISM_LAWS.md needs no second section (CTO~Z right), L-1/L-6/L-12 do fit section III, and
   L-7/L-8/L-9 -- arguably L-4 and L-13 -- have NO HOME.** That third family governs **how a RULE or ROLE
   fails to be one**, in an estate whose primary artifact is rules. **L-8 says a step naming no actor is
   not a step, and L-8 itself has no owner and no home -- it is an instance of itself.**
   **>> LIVE DISAGREEMENT, UNRESOLVED, AND YOU DO NOT ADJUDICATE IT: CTO~Z RULED (150036Z) that the ten
   need no new home because section III already covers them -- artifact 2+, target named. CVO~Z's A18
   then MEASURED that coverage claim FALSE for L-7/L-8/L-9. Both are on the record; the ruling is CTO~Z's
   to revisit or hold. ARTIFACT 1 IS UNAFFECTED EITHER WAY -- it carries only the 14 M-laws, and the
   destination of the staged L-ids is an artifact-2 question. Build artifact 1; do not wait on this. <<**
   **STILL SURFACE-DO-NOT-RESOLVE.** The containment MEASUREMENT is objective and rerunnable; the
   INFERENCE that a third home is needed is CVO~Z's, who authored L-7/L-8/L-9 and marked it
   UNVALIDATED-REUSE. Artifact 1 does not create a third document and does not name one.
4. **LANDING IS MAIN-CTO-GATED** (seam protocol 3 -- law surfaces). Author and stage at ~Z. Do NOT push a
   doctrine file through to main. Hand the staged artifact to CTO~Z for the seam crossing.
5. **HELD-OUT FENCE BINDS** (`ADVI_PERFORMANCE` / `MDPF_GLOBAL`) -- publish your shaping corpus.
6. **NO NON-ASCII. No emojis.**
7. **DO NOT stand up any lifecycle-VALUE-population work** -- Andrew-direct 2026-07-31 ~1400Z, values are
   GATED pending the Kimi user-input pipeline. The MECHANISM continues; values do not.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "what consumes docs/doctrine/CONTROLS_OVER_CARE.md" -- the consumer set BEFORE restructuring a doctrine file</run>
      <expect>A named consumer list with a printed denominator. CLAUDE.md Rules 22 and 22a both point AT these files; a re-point is a law surface.</expect>
      <if_mismatch>If the tool cannot enumerate consumers, say so and enumerate by hand WITH the denominator printed. An unenumerated consumer set is what produced the rule bank's two-rail name collision this morning.</if_mismatch>
    </step>
    <step>
      <run>Record the PRE-COLLAPSE byte count of every file in docs/doctrine/ (wc -c, all 7)</run>
      <expect>A committed baseline. Acceptance is a FALL in byte-count and you cannot show a fall without a measurement taken before you touch anything.</expect>
      <if_mismatch>Take it first. A baseline reconstructed after the edit is not a baseline.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on any .py touched (expected: none for artifact 1)</run>
      <expect>Clean, or no python in the diff.</expect>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-derive the instance count in MECHANISM_LAWS.md vs the taxonomy's instance table</run>
      <expect>Equal, or a NAMED and explained difference. This is the zero-lost-instances control.</expect>
      <if_mismatch>Fix the artifact, not the count.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. `docs/doctrine/MECHANISM_LAWS.md` EXISTS and carries exactly the 14 taxonomy mechanism-laws.
2. Every one carries all four parts, and the gate-or-test cell is populated -- a named gate, a named test,
   or an explicit `NO GATE POSSIBLE -- <reason>`. **Blank fails this TO.**
3. The pre-collapse `docs/doctrine/` byte baseline is committed alongside, per-file, with `wc -c` output.
4. Instance rows reconcile against the taxonomy's instance table, with the reconciliation shown and the
   five-population denominator problem NAMED (204/208/210/219/221 depending on parse -- cite which artifact
   and which parse; the "210-row instance table" is a PROPOSED move that does not exist as an artifact).
5. Zero new laws authored. Zero staged L-ids merged in.
6. Shaping corpus published; held-out fence demonstrably unbreached.
7. Session log with a Compiler Tools section reproducing each run vs expect.
8. **CTO~Z GATE ADDITION (150036Z, restored -- see note): `MECHANISM_LAWS.md` MUST NAME
   `docs/doctrine/CONTROLS_OVER_CARE.md` SECTION III IN ITS HEADER AND STATE THE BOUNDARY BETWEEN THEM.**
   MECHANISM_LAWS = the 14 M-laws, WHERE AN ASSERTION SITS. CONTROLS_OVER_CARE III = instrument
   fallibility, HOW A CONTROL FAILS TO BE A CONTROL. Two subjects, two documents, already correctly
   separated -- **but two doctrine files covering adjacent subjects with NO cross-reference is the
   convergent-vocabulary fork** CTO~Z found in `dormant_guard` the same afternoon (its KEEP-DORMANT states
   vs the bank's DORMANT class, same concept, neither naming the other). **Do not create that shape
   deliberately in doctrine.**
9. Report to CTO~Z on land WITH the commit hash. CTO~Z gates; CVO~Z verifies after that gate.
</acceptance_criteria>

<cross_domain_coordination>
- **`1.0.0_SA_CTO~Z` owns the staged-laws file and is still writing to it.** It is an INPUT you read at a
  pinned commit, never a file you edit. Cite the commit-ish -- a line citation without a vintage is not a
  citation.
- **The M15 DIVERGENT-TRANSPORT candidate is NOT yours to adjudicate.** It enters through the WS-C9 gate
  under the full output contract. Artifact 1 does not mention it.
- **`0.7.0_AE_CloudOps~Z` holds WS-C7.** C7's named limit (a boundary report does not declare whether a
  CONTROL shared the target's transport path) is the seam feeding M15. Do not resolve it here.
- **CLAUDE.md Rules 22 / 22a point at `docs/doctrine/CONTROLS_OVER_CARE.md`.** Any re-point is a law
  surface crossing the main-CTO seam. Artifact 1 creates a NEW file and re-points NOTHING.
</cross_domain_coordination>

<notes>
**THE ONE-ARTIFACT SCOPE IS DELIBERATE AND IT IS A CORRECTION.** Andrew-direct, relayed 2026-07-31: a GO
handing a seat five deliverables at once with no first cut cost WS-C7 about two hours. This TO names one
artifact. When it lands and is gated, artifact 2 is issued. **Do not run ahead because artifacts 2-4 are
obvious -- the sequencing is the point.**

**AND THE SECOND HALF, on landing:** the moment artifact 1 passes CTO~Z's gate, you are DONE with it. Say
so and stop. WS-C3 finished, was gated PASS, and sat idle about 95 minutes because nobody sent the
sentence closing it. **A seat that has finished and been told to wait is indistinguishable from a stalled
seat.** Report completion loudly.
</notes>
</task_order>
