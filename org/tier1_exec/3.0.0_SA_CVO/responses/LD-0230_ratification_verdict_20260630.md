# CVO Independent Constitutional Ratification — LD-0230 (size-invariant granularity) + GRAPHDEPTH substrate-model confirm

**archetype:** VALIDATE
**Verifier:** 3.0.0_SA_CVO~B (NFRA_COMP* verification lane, Andrew-direct via CTO 214112Z)
**Authority:** Constitution Art. XIV independent ratification — ACCEPTED-CVO (independent; NOT as MSTR subordinate, per `org/XXX.md` Tier-0 §CVO-independence)
**Date:** 2026-06-30
**Inputs:** `org/tier0/ledger/LD-0230.md` (commit `6c8cc636d`) · `docs/architecture/NFRA_GRAPHDEPTH_PRD.md` (operative instantiation) · grounded source `org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.size-invariant-granularity-principle.md` (`34d8c138b`, rollup-corrected `047ce51d0`) · CTO arch-assessment 210236Z (the 3 boundary conditions)

---

## VERDICT

**(1) LD-0230 — RATIFIED (ACCEPTED-CVO).** The principle is sound, the four invariants are well-formed and mutually consistent, and the three boundary conditions correctly and near-completely bound it. One forward scope-clarification recorded (P2, NOT a redline) — see SN-1.

**(2) GRAPHDEPTH substrate model — CONFIRMED.** The depth axis, the 5 invariants, the two-regime/file-pivot model (§2a), and the `referenceable`-target gate rule are sound and internally coherent. One parallel forward scope-note (P2) — see SN-2.

Neither note gates ratification or P1 population. Both are recorded extension points, not defects in the current type set.

---

## Soundness analysis (the independent check, not a rubber-stamp)

**Core principle — SOUND.** Orthogonalizing TYPE (semantic) from LEVEL (a declared coordinate on a stable `CONTAINS` ladder) is the correct decomposition for scale-free cognition. It is the same self-similar-schema pattern TSGRAPH already demonstrates live (`MS_FOLDER -CONTAINS-> MS_FILE`, `Module -DECLARES-> Component`; PRD §5) — so the principle is demonstrated, not aspirational. The failure mode it forecloses (diving deeper forks the one graph into per-level schemas/tools, re-creating multi-graph incoherence on the depth axis) is real and is exactly what the program exists to kill.

**Invariant 1 ("deeper dive ADDS levels within FIXED types") vs Boundary A ("the type SET grows by SEMANTIC, never by depth") — COHERENT, not contradictory.** I specifically stress-tested this apparent tension. They reconcile cleanly: depth alone never forks a type (a finer `CALLS` is still `CALLS` + a deeper `level`); but a genuinely new *semantic* surfaced by zooming (statement-grain control-flow branch/loop ≠ a deeper `CALLS`) mints a new scale-stable type. Boundary A is **load-bearing** — it is precisely what stops invariant 1 from being misread as "the type set is frozen." Ratifying A as the declared scope is correct; without it the principle would be unsound-as-absolute (the risk LD-0230 risk_summary itself names).

**Invariant 3 (existential rollup; defects UNSUPPORTED / COARSE-INCOMPLETE) — SOUND and COMPLETE *for the relational edge model*.** OR-rollup ("a coarse edge EXISTS iff ≥1 fine edge rolls up") is the right semantics for existence/reachability relations, and the rejection of 1:1 equality (`047ce51d0`) is correct — 1:1 would false-flag legitimate coarse edges. The two defect classes are the complete failure set for an existential mapping: a coarse claim with no fine basis (UNSUPPORTED, a phantom) and a fine reality with no coarse parent (COARSE-INCOMPLETE, a gap). For the current edge set (`CALLS`/`READS_S3`/`WRITES_S3`/`CONTAINS`/`OWNED_BY`/`RUNS` — all relational/existence) this is sound and gate-checkable. **The verifiability being built into the principle (invariant 3 is a checkable COMPDRIFT seam, not a slogan) is the strongest part of the design** — it makes scale-invariance falsifiable.

**Boundary B (logic vs materialization) — NECESSARY and correctly stated.** Without it the principle implies eager estate-wide statement/row materialization = combinatorial fan-out. "Stable types WHERE materialized, not every level materialized" is the right contract.

**Boundary C (type-specific drilldown) — SOUND.** Correctly forecloses the "infinite drilldown" misread; different types bottom at different levels.

**General-law vs operative-instantiation separation — NO DRIFT.** LD-0230 carries 4 invariants (the general law); GRAPHDEPTH PRD carries 5 (the 5th = two-regime + `referenceable`, the graph-specific §2a application). This is consistent with the LD-0230-is-general / LD-0229+GRAPHDEPTH-is-operative split the artifact and CTO both assert — the 5th invariant is correctly scoped to the substrate layer, not back-propagated into the general law. Boundary conditions A/B/C match verbatim between the LD and PRD §4(a-c). No map-vs-territory gap between the two records.

**Two-regime model (§2a) — SOUND, internally coherent.** I checked the `S3_BUCKET = MS_FOLDER = Module` "same tier" claim: it holds at the CONTAINER tier (each is "the thing that contains files") with the file-equivalent (`MS_FILE` / `S3Key` / portal file) as the pivot and the recursive archetype below it (object data-schema / function-and-statement tree / component tree). The equivalence is a ladder-POSITION claim (comparability by tier-position), not an ontology claim — sound as long as tools treat tier-position as the `(breadth, depth)` comparability axis, which §3 supports.

**`referenceable`-target rule (invariant 5) — SOUND.** "Breadth edges may target only `referenceable` nodes, never terminal members" is the rule that makes breadth compose with depth correctly, and it is gate-checkable (a breadth edge landing on a `Statement`/`Field`/`Prop` = a finding). Correct for the enumerated breadth-edge set.

---

## Scope-clarifications recorded (P2 — forward extension points, NOT redlines)

**SN-1 (rollup-semantics dimension — completes the boundary set).** Boundary conditions A/B/C bound the TYPE dimension of scale-invariance (semantic-shift / materialization / grain-meaningfulness). There is a 4th latent dimension they do not address: the **rollup SEMANTICS**. Invariant 3's existential (OR) rollup is correct for relational/existence edges, but a future `edge_type` carrying a QUANTITATIVE attribute that must aggregate across grain (a weight, a call-count, bytes-transferred) would need a **companion value-rollup rule** — existential-only checking would pass a coarse edge that EXISTS but whose aggregate MAGNITUDE is wrong (the same class of "present but semantically wrong" defect the CVO SEMANTIC axis exists to catch). No current edge_type is weighted, so this is latent, not live. **Recommend** MSTR/CTO record it as a known extension point in the LD/PRD so a future weighted edge_type does not silently inherit existential-only rollup. This does not weaken the ratification — it strengthens boundary-condition completeness.

**SN-2 (`referenceable` is currently node-intrinsic).** `referenceable` is modeled as a node-level attribute (a node is or isn't a valid breadth-edge target, full stop). This is correct and simpler for the current breadth-edge set. But the property is in principle EDGE-TYPE-relative: a `Statement` is not a valid `CALLS` target, yet could be a valid target of a future statement-grain `DATA_FLOW`/`TAINTS` edge (a security/data-flow lens). If such a semantic is ever minted (legal under Boundary A), the gate must decide whether `Statement` becomes `referenceable` for that edge_type or whether the edge targets the containing referenceable unit. **Recommend** ~C/~D note this as the extension point when invariant 5 is encoded — keep `referenceable` checks keyed so they can become edge-type-relative without a schema fork.

---

## What you should have asked but did not

Whether the **existential rollup invariant (3) and the `referenceable` rule (5) need a regression fixture of their OWN before P1 population freezes the gate's behavior.** The P0-CVO no-regression fixture (which I now own from zero) is currently scoped to the four structure-TOOLS' answers (comp-blast/trace/xref/platinum set-equality pre- vs post-re-point). But the GATE itself (`comp-coverage-check` rules 7-9 + the incoming referenceable-target rule) is also changing behavior as ~C folds rules and ~D populates — and an existential-rollup checker that silently flips from OR-rollup toward 1:1 (the `047ce51d0` regression class) would not be caught by a TOOL-answer fixture. I will scope the P0-CVO fixture to capture BOTH (a) the four tools' pre-delta answers AND (b) a representative gate-verdict fixture (a known-GREEN and a known-RED grain case the rollup/referenceable checkers must continue to classify identically post-fold) — so the no-regression gate covers the governance layer, not only the tool layer. Flagging now because it widens the fixture I am about to freeze, and the fixture must be captured while the current caches/gate are still authoritative.

---

— 3.0.0_SA_CVO~B
