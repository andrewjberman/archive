# Task Order: NFRA_PROMOTE P2 -- the four materializers (write validated promotions back into the substrate, reversibly)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-promote-p2</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~Z (GOV-B producer + recognizer/compiler-rule materializer share -- arch-ratified design 4d0886493; REDIRECTED 2026-07-14 from the dead 0.8.0~D lane [respawn never happened, idle 6d] per SOVEREIGN REDIRECT @ 14c2aeeba + AMENDMENT-1 @ 552667ccd) + 0.4.0_DS_ClientPlatform~B (CSE-schema / graph / router materializers -- NOT moved by the redirect table; reallocated from the down DS~A) + 1.0.0_SA_CTO (ratify owner, cross-plane -- UNCHANGED)</issued_to>
    <date>2026-07-07</date>
    <status>staged -- GO on PROMOTE-P1 landing. REDIRECT-ACK FOLD (per CVO~Z 072211Z fold-duty, 2026-07-14): agent-side ACK landed 071744Z (orphan pid 3636301 had stolen the original handoff; recovered from read/); 22b caveat CLOSED. STATE NOTE (0.8.0~Z first-touch survey): ~D landed the GOV-B recognizer-materializer share BEFORE dying (f9d9926f2 + a0528032d, comp_promote_materializer.py, self-test 16/16) -- my share is verify + integrate against the P1 lifecycle now landing, not greenfield. PRIOR: ~D respawn requested (GOV-B arch-ratified = instant-build); DS materializers reallocated DS~A->DS~B.</status>
    <prd_ref>docs/architecture/NFRA_PROMOTE_PRD.md (P2, S4.1) + docs/architecture/NFRA_SEMCTL_PRD.md (GOV-B seam)</prd_ref>
    <dispatch_state>STAGED -- GO at Wave-4, AFTER NFRA_PROMOTE.P1 (contract/lifecycle). Authored by COO~B on the NFRA full-program completion drive. PROMOTE is LAST -- the only plane that writes back.</dispatch_state>
    <gate_note>Gated on PROMOTE-P1. The recognizer/compiler-rule materializer CLOSES SEMCTL GOV-B (the hot-registration seam producer side -- the RecognizerRegistry consumer half is already landed in comp_recognizer_sdk.py).</gate_note>
  </metadata>

  <objective>Build the four materializers (PROMOTE PRD S4.1) that turn a validated regularity into explicit structure, each writing back into its target plane and each REVERSIBLE + emitting a CSE: (a) a compiler-rule/new-recognizer -> NFRA_COMPILERKIT (via the RecognizerRegistry hot-registration seam); (b) a new algebra primitive -> a governed NFRA_CSE schema migration; (c) a routing/retrieval directive -> the router (explicit, NOT a latent affinity weight); (d) a first-class knowledge node -> the graph.</objective>

  <requirements>
    <requirement id="1">All four materializers implemented; each writes back into the correct target plane (COMPILERKIT / CSE-schema / router / graph).</requirement>
    <requirement id="2">Each materialization is REVERSIBLE (carries a demotion path -- wired in PROMOTE-P3) + emits a CSE (promotion is itself organizational evolution, feeds its own observation).</requirement>
    <requirement id="3">HUMAN-RATIFY structural (AC2): each materializer runs only after a typed-commission ratify -- ZERO auto-mutation of the substrate. Generalize the TH-C clause-A dispatch pattern.</requirement>
    <requirement id="4">CLOSE GOV-B: the recognizer/compiler-rule materializer wires the PROMOTE producer side into the live RecognizerRegistry (comp_recognizer_sdk.py PROMOTE_SEAM) + binds on_register to the live comp-surface-check watcher -> a promoted recognizer registers LIVE without a redeploy, end-to-end.</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_PROMOTE.P1: the typed-commission contract + lifecycle this materializes from. HARD PREREQUISITE.
    - NFRA_SEMCTL.GOV-B: the recognizer materializer closes its producer half (consumer half landed 6004a91c0).
    - NFRA_COMPILERKIT (comp_recognizer_sdk.py RecognizerRegistry): the hot-registration target.
    - NFRA_CSE (cse_schema.py): the algebra-primitive migration target (governed schema bump).
    - NFRA_COMPROUTE (comp_route.py): the routing-directive target (explicit heuristic, not latent w_h).
    - 1.0.0_SA_CTO: the ratify owner for cross-plane promotions.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Each of the 4 materializers demonstrated end-to-end: candidate -> ratify -> materialize into its plane -> emits a CSE.
    2. GOV-B closed: a promoted recognizer registers LIVE into the RecognizerRegistry without redeploy, exercised (not config-read); on_register bound to comp-surface-check.
    3. Zero auto-mutation proven (a promotion without ratify does NOT mutate -- grep-proof + exercise).
    4. Ground on live substrate writes (Rule 22/22a: desired+applied+exercised). RAVC COO~B + CC CTO; CVO independently verifies each materializer + the anti-auto-mutation gate.
  </acceptance_criteria>
</task_order>
```
