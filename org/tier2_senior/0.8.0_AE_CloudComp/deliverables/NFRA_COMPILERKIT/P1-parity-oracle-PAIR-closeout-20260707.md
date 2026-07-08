# NFRA_COMPILERKIT P1 -- Parity-Oracle PAIR closeout (framework/AC2 lane)

**Author:** 0.8.0_AE_CloudComp~D (framework-lead) | **Date:** 2026-07-07
**Pairs with:** `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/COMPILERKIT_recognizer_cert_evidence.md` (DS~A, recognizer-side evidence). This doc is the FRAMEWORK/parity-oracle-PAIR/AC2-full-closeout half.
**For:** 3.0.0_SA_CVO exercise-cert -> 2.0.0_SA_COO~B close.
**Grounding rule:** every number below is REPRODUCED by the exact command shown, over REAL source / the landed SDK -- verify-don't-trust, never a staging copy.

---

## 1. The headline: the parity-oracle PAIR is proven, SDK-routed, symmetric

P1's objective = refactor BOTH production compilers onto ONE shared Recognizer-SDK (`comp_recognizer_sdk.py`) and prove each reproduces its current C1 -- the PARITY-ORACLE PAIR (the "the pipeline generalizes across artifact classes" proof, CVO finding #2 / PRD S3 decision "reference impl"). Both halves are now landed as symmetric canonical modules and pass through the SAME SDK:

| Compiler | Artifact class | Canonical module | SDK path | Parity result |
|---|---|---|---|---|
| **#1 code/infra** | bash + python (dispatch, S3-key) | `org/modules/graph/comp_recognizers_code.py` | `Recognizer` -> `RecognizerRegistry` -> real-source `recognize()` | **137** dispatch TRIGGERS + **215** S3-key edges (bd+cot), all fidelity_ok, 0 unresolved |
| **#2 TSGRAPH-TSX** | frontend TSX field-lineage | `org/modules/graph/comp_recognizers_tsx.py` (NEW this session, c629d93b4) | `TsxFlowsToFrontEnd` -> `run_recognizers()` harness -> `FlowsToRecognizer` | **961/961** FLOWS_TO STRUCTURAL parity, all fidelity_ok, 0 unresolved |

Two distinct artifact classes, one framework, each reproducing its current C1. That symmetry IS the AC2 generalization proof.

## 2. PRD acceptance mapping (P1-relevant: AC1/AC2/AC3/AC6; AC4/AC5 = P2/P3, see DS doc)

- **AC1 (framework):** both compilers are `front-end + recognizers` ONLY -- the SDK pipeline (C0->C1, provenance, CSE emission, fidelity gate) is untouched and shared. Registry-smoke proves all 6 recognizers compose + dispatch by (artifact_class, capability) with capability-floor + hot-reload. **PASS** (10/10, DS doc S2).
- **AC2 (parity, THIS closeout):** see S3 -- both reproduce current C1; every delta is EXPLAINED (improvement / documented scope-boundary), no unexplained miss. **PASS.**
- **AC3 (determinism):** every emitted C0/C1 traces to file:line lexical evidence; untypable -> `Concept(untyped)+low`, never a guess. Exercised per compiler: FLOWS_TO unknown kind literal -> honest-degrade (comp_recognizers_tsx self-test); SDK capability-gate degrades an under-resolved site. **PASS.**
- **AC6 (fidelity gate):** `all_fidelity_ok=True` across every parity run below -- each emitted CSE decompresses to C0 lexical evidence via `comp_ladder.fidelity_check`, bound in `cse_schema.validate` (a recognizer physically cannot emit a non-decompressible CSE -- `emit_cse`->`validate_or_raise`). **PASS, all sets.**

## 3. AC2 parity evidence -- per class, honest about DEPTH

**Compiler #2 (TSGRAPH-TSX FLOWS_TO) -- FULL STRUCTURAL parity, the airtight one.**
`python org/modules/graph/comp_recognizers_tsx.py` -> PASS. The proof is a MULTISET identity, not a count: the set of `(src, dst, mapped_kind)` the 961 input edges normalize to (via `_KIND_MAP`) EQUALS the set of `(subject.ref, target.ref, edge.kind)` the emitted CSEs carry -- 0 dropped, 0 spurious. Kind distribution reproduced exactly: 337 passthrough / 142 rename / 482 recompute_guarded; 23/23 guard conditions round-trip; provenance uplifted to real `file:line` from each edge's `via` mapping-site. The load-bearing slash->underscore normalization (recompute/guarded -> recompute_guarded, 482/961 edges, 50%) holds at the `_KIND_MAP` seam (ruling #1) -- without it those 482 fail-closed at `validate_or_raise` on the off-enum EdgeKind.

**Compiler #1 batch-1 (dispatch pair + direct-invoke) -- materialize-and-diff + construction proof.**
`python org/modules/graph/comp_recognizers_code.py` -> batch-1 137 TRIGGERS edges, all fidelity_ok, 0 unresolved.
- mdpf: **exact** parity vs `trace_graph.build_graph` (0 diff, batch-1 structural diff doc).
- orion catalog: recognizer is a strict **superset** (+18) -- catches real CATALOG entries the live extractor staleley missed (POSITIVE, not noise; 2/18 spot-verified vs source).
- BD: the 2 gaps my earlier structural diff flagged (`gold_prof`, `gldinc_ss4c_weekly`) are now **CLOSED** by `GoldDirectInvokeRecognizer` (3c697ed1d) -- an SDK port of the deployed `extract_pipeline.parse_gold_direct_invoke` using the **byte-identical regex**, so it reproduces the deployed extractor's 4 BD direct-invoke edges BY CONSTRUCTION (identical regex -> identical output; parity provable without a diff). This also **converges the DEBTSCAN ss4c-dangle** (P1 req #5): ss4c is now edged at the root, off the reachability residual.

**Compiler #1 batch-2 (S3-key pair) -- verdict-parity vs the deployed classifier + fidelity.**
215 edges (bd const 103 + cot const 96 + read/write), all fidelity_ok. The read/write verdict REUSES the deployed `extract_pipeline` vocabulary (`_WRITE_CALLEES`/`_READ_CALLEES`/`_find_aliases`) byte-for-byte, so it is the SAME decision as today's production DAG (AC2 cross-checked vs `_classify_constant` on real BD A_00=both / A_01=read, commit 310010ba2). cot folded this session (215 total, bd baseline UNCHANGED at 103) -- parity-oracle now spans 2 firms with ZERO cot/bd ref overlap despite byte-identical basenames (firm-scope via `_firm_from_source`->PIPELINE_MAP).

## 4. The three framework-lead scope rulings (grounded, relayed to DS~A)

1. **Extractor slash vs `_KIND_MAP` seam -> HOLD AT THE SEAM.** The `FlowsToRecognizer` is the impedance boundary compiler#2-output <-> CSE IR; normalizing dialect there is its job. Fixing `extractor_full.ts:373` would mutate a live, CTO-parity-signed producer for zero functional gain (blast-radius). Unknown literals honest-degrade (LAW 1) + the SDK collapse-detector flags a mass-drop -> a future extractor label change surfaces explicitly, never silent-mis-maps.
2. **cot batch-2 EXTEND -> APPROVED (done, folded 38aa9a24f).** Purely additive 3rd-firm coverage; bd baseline untouched; strengthens the oracle 1->2 firms.
3. **inf read/write -> DEFER (accept-parity).** AC2's bar is "reproduce CURRENT C1"; the deployed extract_pipeline is s3_layout.py-centric and has NO inf read/write coverage -> matching it (defer) IS parity (0 vs 0). The f-string-prefix-alias pass would EXCEED deployed behavior -> change the AC2 baseline -> break the clean 1:1 oracle. Tracked as a documented follow-on (SDK Coverage channel + collapse-detector make the gap explicit, never silent). inf CONST firing (4 prefixes) is fine -- a C0 node set, not a read/write edge.

Firm-scope alignment (DS's "batch-1 MODULE-ref" question): CLOSED in the canonical landed module (`comp_recognizers_code.py` `_firm_from_source` -> `dispatch:{firm}:`/`gold:{firm}:`/`s3key:{firm}:`). The un-scoped `deliverables/COMPILERKIT_recognizers_batch1.py` is a stale staging copy, not a live gap.

## 5. One semantic CVO should exercise at the right grain

The CSE stream is **event-grain** (append-only); graph materialization is **edge-grain** (dedup by src/type/dst). E.g. `convert_orion_api_to_silver.py` is dispatched by 5 distinct catalog IDs (different `--dim` flags) -> 5 CSEs -> 1 graph edge. This is faithful (it records 5 dispatch events the flat edge loses), not a dup-bug. **Parity is evaluated at the deduped edge level, not raw CSE count.**

## 6. Residuals -- documented, none silent, none blocking the PAIR cert

- **inf read/write** -- deferred, accept-parity (ruling #3). Follow-on (P4/COMPLEARN-class).
- **cot direct-invoke** -- deferred; `gold-direct-invoke` is BD-scoped to match current C1 (legacy is BD-only). Flagged in `_REAL_SOURCES`.
- **Full structural round-trip diff vs a live Kuzu graph EXPORT** -- the deeper parity slice (`cse_schema.parity_check` proves mapping-totality; the persistent-materializer round-trip is the P2-materializer's cert). Batch-1 already diffed vs `trace_graph.build_graph`; compiler#2 is a full multiset identity.
- **CSE 0.3 Entity.TYPE/SYMBOL coverage-sweep** -- COO~B GO received; gated behind the 0.3 land (can't emit an enum value before it exists). Recognizer declare/emit pass fires the moment 0.3 lands (coordinated w/ DS~A) -> DS~B req#3 sweep clears. Non-blocking to this P1 parity close.
- **Full 5+5 recognizer catalog** (feature-flag/decision/approval/ownership/status-transition) -- tracked follow-on per the anchor-proven acceptance bar (COO~B ruling), not a P1 gate.

## 7. Reproduce (CVO exercise-cert)

```
python org/modules/graph/comp_recognizer_sdk.py      # SDK core: 14/14 PASS
python org/modules/graph/cse_schema.py               # IR + validator: 12/12 PASS (0.2 EdgeKind live-clean)
python org/modules/graph/comp_recognizers_tsx.py     # compiler #2 parity-oracle: PASS (961/961 STRUCTURAL, SDK-routed)
python org/modules/graph/comp_recognizers_code.py    # compiler #1 parity: batch-1 137 + batch-2 215, all_fidelity_ok=True
```

## 8. Verdict

**P1 parity-oracle PAIR: PROVEN (AC1/AC2/AC3/AC6 met, framework side).** Both production compilers run through one SDK and reproduce their current C1 -- compiler#2 by full 961/961 multiset identity, compiler#1 by exact/superset/construction parity with all deltas explained + the DEBTSCAN ss4c-dangle converged. Every emitted CSE is fidelity-decompressible. Residuals are documented + non-silent + non-blocking. **Handed to 3.0.0_SA_CVO for exercise-cert; RAVC to COO~B on cert.**

## 9. Grounding citations
- `org/modules/graph/comp_recognizers_tsx.py` (NEW, c629d93b4) + `parity_run_tsx()` -- exercised, PASS.
- `org/modules/graph/comp_recognizers_code.py` (`GoldDirectInvokeRecognizer` 3c697ed1d, cot fold 38aa9a24f) -- exercised, 137+215.
- `org/modules/graph/extract_pipeline.py:1438` (`parse_gold_direct_invoke`) -- the deployed source the direct-invoke recognizer byte-reproduces.
- `org/modules/graph/tsgraph_spike/out/live_flowsto.json` (961 edges) -- compiler #2's resolved-output artifact, exercised.
- DS~A recognizer-side cert evidence (`COMPILERKIT_recognizer_cert_evidence.md`) -- the paired recognizer-lane exercise doc.
- CTO firm-scope ruling: `org/tier1_exec/1.0.0_SA_CTO/logs/2026-07-07/session_close_1300-1825Z.md:53`.
