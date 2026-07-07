# NFRA_COMPILERKIT -- Recognizer-Side Cert Evidence (P1/P2/P3)

**author:** 0.4.0_DS_ClientPlatform~A (recognizer lane) | **date:** 2026-07-07 | **for:** 3.0.0_SA_CVO cert packet (assembled by 0.8.0_AE_CloudComp~D, framework/closeout lane)
**scope:** the RECOGNIZER half of NFRA_COMPILERKIT. Framework/parity-oracle-pair/AC2-full-closeout is ~D's lane; this doc is the recognizer-side exercise-cert evidence CVO folds in.
**grounding rule:** every result below was RE-RUN post-fabric-restart 2026-07-07 against REAL source (verify-don't-trust); each is reproducible by the exact command shown. All harnesses import the LANDED SDK (`comp_recognizer_sdk.py`) + landed recognizers, not staging copies.

---

## 1. Recognizer inventory (6 sets, 3 compilers + 2 non-code classes)

| Recognizer | Compiler / class | Landed in | Commit |
|---|---|---|---|
| DispatchCatalogRecognizer + MdpfDispatchRecognizer | #1 code (batch-1, dispatch pair) | `org/modules/graph/comp_recognizers_code.py` | a4f3d302e (wired) / eb466b90e |
| S3KeyConstRecognizer + S3KeyReadWriteRecognizer | #1 code (batch-2, S3-key pair) | `org/modules/graph/comp_recognizers_code.py` | 9863962a9 / 564eea218 |
| FlowsToRecognizer | #2 TSGRAPH-TSX (anchor, field-grain lineage) | `deliverables/COMPILERKIT_recognizer_flowsto.py` (wiring into canonical `comp_recognizers_tsx.py` = ~D this session) | cc983b78a |
| ConfigS3RefRecognizer + EnvSecretRefRecognizer | P2 config (non-code class #1) | `deliverables/COMPILERKIT_recognizers_P2_config.py` | 66f7bcd14 |
| TicketRequirementImplementsRecognizer | P3 ticket (non-code class #2, cross-plane) | `org/modules/graph/comp_recognizers_ticket.py` | 6789fe028 |

---

## 2. PRD acceptance-criteria -> recognizer evidence map

**Acceptance bar RULED anchor-proven** (COO~B 2026-07-07, ruling adopted): each compiler is proven by its characteristic edge class per the PRD's GENERALIZE-NOT-BUILD / parity-oracle thesis; the full 5+5 recognizer catalog (feature-flag/service-endpoint/decision/approval/ownership/status-transition) is a **tracked follow-on, not a gate**.

| PRD AC | Requirement | Recognizer evidence | Result |
|---|---|---|---|
| **AC1** framework | new class added by writing ONLY front-end + recognizers; pipeline untouched | all 6 recognizers compose in the live `RecognizerRegistry` + dispatch by (artifact_class, capability) with capability-floor + hot-reload | **10/10 PASS** (registry smoke) |
| **AC2** parity | code compiler reproduces current code C1 (no regression) | batch-1 reproduces dispatcher->TRIGGERS->script C1 (133 edges); batch-2 reproduces S3-key read/write. *Full structural diff vs live extract_pipeline = ~D framework closeout.* | 133 + (bd 115 + cot 100) edges, all fidelity_ok |
| **AC3** determinism | every C0/C1 traces to lexical evidence; untypable -> confidence:low + Concept(untyped) + coverage-gap, never a guess | LAW-1 honest-degrade EXERCISED per recognizer: P2 malformed SECRET value -> Concept(untyped)+low; FLOWS_TO unknown kind literal -> degrade (not reject); ticket requirement naming no real path -> Requirement entity alone (edges=[]), coverage-channel records unresolved | exercised + PASS in every harness |
| **AC4** config->consumer | config compiler emits config->consumer edges into C1 (a dimension the code-only graph lacked) | ConfigS3RefRecognizer (config -> S3 bucket refs, YAML) + EnvSecretRefRecognizer (config -> secret-id pointers, env) | **11/11 PASS** vs real yaml/env |
| **AC5** cross-plane | ticket compiler emits >=1 cross-plane edge class (org Requirement implements a code Component) | TicketRequirementImplementsRecognizer: 5 Requirement-IMPLEMENTS-Component edges over 188 real requirements / 59 real TO files; each Component end is a `os.path.isfile`-CONFIRMED real path (never guessed) | **PASS** (>=1 met; 5 emitted) |
| **AC6** FIDELITY GATE | every recognizer C0/C1 PASSES comp-ladder `fidelity_check` -- each node decompresses to lexical evidence | `all_fidelity_ok=True` across EVERY parity run below (headline recognizer-side cert) | **PASS, all sets** |

---

## 3. Reproducible parity results (post-restart re-run, REAL source)

```
# P1 compiler #1 -- batch-1 dispatch pair (TRIGGERS edges)
$ python org/modules/graph/comp_recognizers_code.py
  batch-1: TOTAL 133 edges; all_fidelity_ok=True  (orion 67 + bd 28 + cot 27 catalog + mdpf 11)
  batch-2 (bd): const 103 + read/write 12 = 115 edges; all_fidelity_ok=True

# P1 compiler #1 -- batch-2 S3-key cot EXTENSION (additive 3rd firm; ruled APPROVED by COO~B + ~D)
$ python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/COMPILERKIT_batch2_cot_extension_probe.py
  cot: const 96 + read/write 4 = 100 edges; all_fidelity_ok=True
  10/10 PASS -- cot firm-resolves via PIPELINE_MAP; ZERO cot/bd ref+target overlap despite
  byte-identical A_00/A_01 basenames; bd baseline UNCHANGED (no perturbation)

# P1 compiler #2 anchor -- FLOWS_TO (field-grain lineage + EdgeKind discriminator)
$ python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/COMPILERKIT_recognizer_flowsto.py
  9/9 PASS vs REAL 961-edge live_flowsto.json; 961/961 resolve; 482 recompute_guarded normalize (not reject)

# P2 config compiler
$ python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/COMPILERKIT_recognizers_P2_config.py
  11/11 PASS vs REAL gold_freshness_config.yaml (bd+cot scope-tagged) + real secret-ids.env; LAW-1 degrade exercised

# P3 ticket compiler (cross-plane)
$ python org/modules/graph/comp_recognizers_ticket.py
  AC5 PASS -- 5 Requirement-IMPLEMENTS-Component edges / 188 requirements / 59 TO files; all_fidelity_ok=True

# AC1 framework -- all recognizers compose in the live SDK
$ python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/COMPILERKIT_recognizer_registry_smoke.py
  10/10 PASS -- register + (artifact_class,capability) dispatch + capability-floor + hot-reload
```

---

## 4. Documented scope boundaries (honest, not silent -- SDK coverage-channel tracked)

- **inf read/write S3 edges: DEFERRED** (accept-parity, ~D ruling #3). Deployed `extract_pipeline` is `s3_layout.py`-centric with 0 inf read/write coverage; matching it (0-vs-0) IS parity. The f-string-prefix-alias enhancement would EXCEED deployed behavior -> net-new edges -> change the AC2 baseline. Tracked follow-on (post-cert, P4/COMPLEARN-class). inf CONST firing (4 inline prefixes) is a C0 node set, not a read/write edge -> does not touch the parity baseline.
- **extractor slash-form normalization: held at the `_KIND_MAP` seam** (FlowsToRecognizer), NOT fixed at `extractor_full.ts:373` (~D ruling #1) -- the recognizer IS the impedance boundary; mutating a live CTO-parity-signed producer = live blast-radius for zero functional gain.
- **Full 5+5 recognizer catalog: tracked follow-on** (COO~B ruling), not the P1/P2/P3 gate.

## 5. Open items for the lane close (NOT recognizer-side)
- Compiler #2 full SDK migration (`comp_recognizers_tsx.py` + TsxFlowsToFrontEnd + SDK-routed `parity_run_tsx()`) + full AC2 structural parity diff -- **0.8.0~D this session**.
- cot scope-dict fold into canonical `parity_run_batch2` (2-line addition validated by the cot probe) -- handed to ~D (wiring lane).
- CVO exercise-cert of this recognizer-side evidence + ~D's framework/parity evidence -> COMPILERKIT close.
