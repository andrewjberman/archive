# DOCTRINE_RATCHET.A1 — is the post-cut growth REDUNDANT or ADDITIVE? (analysis only; no deletions)

<task_order>
<id>DOCTRINE_RATCHET.A1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>3.0.0_SA_CVO~Z</issued_to>
<date>2026-08-12</date>
<status>complete -- delivered 2026-08-12 @f7b23a05f8 (DOCTRINE_RATCHET_A1_CVO_ANALYSIS_20260812.md + PROOF_OF_SPEC VALID rc=0 C1-C5, re-run 2026-08-20 at this seat); status flipped 2026-08-20 by the assignee (3.0.0_SA_CVO~Z) at Step-2b reconciliation -- the TO read pending for 8 days after its deliverable landed</status>
<priority>P3 — IDLE-CAPACITY WORK, EXPLICITLY PREEMPTIBLE</priority>

<!-- ⛔ DROP THIS THE INSTANT A W4a PACKET LANDS. Certification is your standing duty and outranks
     this without discussion. This exists because you are idle BY CONSTRUCTION (awaiting a packet
     that cannot exist until a seal happens elsewhere), not because it is important. -->

<scope>
`docs/doctrine/CONTROLS_OVER_CARE.md` (GENCHI GENBUTSU). **ANALYSIS ONLY. YOU DELETE NOTHING.**

**MEASURED DRIFT (my numbers, re-derive them — they are a prior claim under test):**

```
4defd7ff3e  08-05  4.0.0_SA_CRO   +195 -1245   THE CUT (1,289 -> ~200), Andrew-DIRECTED
  b51513a69b 08-05 4.0.0_SA_CRO   +20          post-cut
  e9d89a997b 08-05 4.0.0_SA_CRO   +21          post-cut
  dfc66d4dbf 08-06 4.0.0_SA_CRO   +24          post-cut
  8b7b303908 08-06 1.0.0_SA_CTO~Z +6  -1       post-cut
  27b57247b1 08-11 1.0.0_SA_CTO~Z +33          post-cut  <- MINE, tonight, section 5
                                  ----
                          net    +103 from 2 seats; file now 342
```

**THE SHAPE, named so you can test it rather than assume it: A RATCHET EACH STEP OF WHICH JUSTIFIES
LOCALLY.** Every addition — including both of mine — was argued as *"this one fills a real gap."*
**Three of the five post-cut additions are the CUTTER'S OWN, within 36 hours of their own cut**,
which is the strongest available evidence that the local argument is persuasive to anyone standing
in it. **A ratchet that justifies locally at every step never reverses on its own.**
</scope>

<requirements>
  <requirement id="1">**THE ONE QUESTION: is each post-cut addition ADDITIVE (a mechanism the file did not carry) or REDUNDANT (a restatement of something already present in different words)?** Per addition, a verdict with a citation to the text it duplicates if redundant.</requirement>
  <requirement id="2">**Judge `27b57247b1` §5 — MINE — first and hardest.** I argued it fills a gap (the four modes explain why you failed to SEE; nothing explained why nobody SENT IT BACK). **That argument is exactly the shape every other contributor used.** If §5 restates §4/§4b/§4c in new clothing, say so plainly; I will remove it myself.</requirement>
  <requirement id="3">**Apply the file's own editing test to each addition:** is the principle ACTIONABLE WITHOUT ITS INCIDENT? An addition that cannot be stated without retelling what happened is an incident wearing a principle's clothes and belongs in `docs/references/`.</requirement>
  <requirement id="4">**Report whether the ~200 target is still the right target.** It was an Andrew-DIRECTED outcome executed by CRO, not a hand-edit — so the number may be a proxy for "only mechanisms, no incidents" rather than a line budget. **If the file is 342 lines of pure mechanism, that is a different finding from 342 lines with 140 of restatement**, and the remedy differs.</requirement>
  <requirement id="5">**No deletions, no edits, no proposals-as-acts.** The output is a verdict table. **Removal is the file owner's call and, for the ~200 ruling itself, arguably Andrew's** — this TO exists to make that decision cheap, not to pre-empt it.</requirement>
</requirements>

<acceptance_criteria>
  <criterion id="C1">Drift table re-derived independently; disagreement with my numbers named (or zero-disagreement stated explicitly).</criterion>
  <criterion id="C2">Per-addition verdict: ADDITIVE / REDUNDANT (with the duplicated text cited) / INCIDENT-SHAPED.</criterion>
  <criterion id="C3">§5 judged explicitly and by name, with its author's argument quoted and tested rather than paraphrased.</criterion>
  <criterion id="C4">A recommendation on the ~200 target per requirement 4 — line budget vs mechanism-purity proxy.</criterion>
  <criterion id="C5">Zero file modifications to the doctrine file. The deliverable is the analysis.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5</expected_criteria>
  <instance_path>org/tier1_exec/3.0.0_SA_CVO/deliverables/DOCTRINE_RATCHET.A1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
  <before_write>`comp-which` for any search; `comp-find` if a raw repo search is needed.</before_write>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5   # POSITIONAL argv[2]; read rc via ${PIPESTATUS[0]} if you pipe it</after_commit>
</compiler_tools_mandate>

<deliverables>
  <deliverable type="document">`org/tier1_exec/3.0.0_SA_CVO/deliverables/DOCTRINE_RATCHET_A1_ANALYSIS.md` — the verdict table</deliverable>
  <deliverable type="document">`DOCTRINE_RATCHET.A1_PROOF_OF_SPEC.json`, validator-clean</deliverable>
</deliverables>

<do_not>
  <rule>⛔ **PREEMPTED BY ANY W4a CERTIFICATION PACKET — drop this immediately, no handoff needed.**</rule>
  <rule>No deletions. No edits to the doctrine file. No new doctrine authored while analysing doctrine growth.</rule>
  <rule>No push (lane commit; MSTR~Z integrates).</rule>
</do_not>
</task_order>
