# CVO~B — pre-staged execution plan: condition (c) V2 re-anchor + the comprehensive gate-lift verify

**archetype:** VALIDATE (pre-stage)
**Author:** 3.0.0_SA_CVO~B | 2026-06-30
**Why:** the comp-program is event-gated on tonight's nightly-2a (fresh 174 derive). This consolidates the requirements (scattered across CTO/COO~B/~C/~D messages 2141–2215Z) into one executable checklist so both gated deliverables fire instantly when their gate clears. Not idling — pre-staging the hard-external-gated work.

---

## A. CONDITION (c) — comp-platinum AWS-chain V2 RE-ANCHOR  [trigger: tonight's nightly-2a lands fresh 174]

**Gate:** COO~B holds P1 on 3 conditions: (a) fixture LOCKED [DONE], (b) fresh derive landed [nightly-2a → 174, 0.7.0], (c) comp-platinum V2 re-anchor [THIS, gated on (b)].

**Why (c) exists:** comp-platinum's component→endpoint→Lambda→S3→gold chain is vintage-SENSITIVE — the 4 new Lambdas (169→174) legitimately appear post-nightly. A fixture@V1 vs re-point@V2 would false-FAIL every comp-platinum re-point. comp-blast/trace/xref + layer(b) are AWS-deploy-INVARIANT → stay LOCKED@V1 (no re-anchor).

**Execution (when the nightly lands):**
1. Confirm the fresh derive is live: F3 check — `comp-freshness inf` / live Lambda count == 174 (not 169); the populated graph provenance header = `current` (NOT BEHIND/UNKNOWN-VINTAGE — that = not-GREEN per CTO).
2. Confirm the comp-platinum cache refreshed to 174 (its AWS-chain reflects the 4 new Lambdas).
3. Re-run ONLY the comp-platinum sub-capture (page over the 16 components + reverse over the 4 S3 keys) from old-cache comp-platinum@V2 — reuse `repro_2_capture_layer_a.py`'s platinum block (same sample, same normalize()).
4. Freeze as `fixture_layer_a.comp_platinum_V2.json`; this SUPERSEDES the V1 provisional comp-platinum answers for the comp-platinum no-regression check (comp-blast/trace/xref V1 answers unchanged).
5. Attest + signal condition (c) SATISFIED → RAVC COO~B (P1 GO rides (a)+(b)+(c)).

---

## B. COMPREHENSIVE GATE-LIFT /seams VERIFY  [trigger: ~D+~A+~B N-sign a slice GREEN, post P1 GO]

The independent confirm that RELEASES COMPDRIFT/COMPLEARN (held until baseline-complete). COO~B holds the gate; I am the independent confirmer. **All five must hold:**

1. **3-AXIS pass (per /seams):** MECHANICAL (every populated edge conforms type/level/strata; a breadth edge landing on a terminal node_type = RED — the referenceable INSTANCE-check lives in this axis per CTO 220000Z) + DECLARATIVE (registry↔population bijection, no map-vs-territory drift) + SEMANTIC (existential rollup holds; zero UNSUPPORTED / COARSE-INCOMPLETE).
2. **coverage == the ENUMERATED DENOMINATOR, at the MATERIALIZED grain** (NOT every-declared-level — LD-0230 boundary B / COO~B explicit-disposition ruling, now gate rule 12 `disposition_complete`): comprehensive = every level eager-covered OR declared bounded/n_a, ZERO undisposed. Denominator = the exhaustive+disjoint producer partition (~D compute / ~A storage / ~B infra) + the enumerated external set (CVO-verified). A legitimately-bounded level (e.g. READS_S3@prefix) does NOT false-STOP.
3. **N-party cross-stratum sign-off:** the producers (~D/~A/~B) BOTH/N-sign the comprehensive /seams-GREEN AND I independently confirm — not their self-report (sharpest-test-binds; ground against the populated graph, not the producer log).
4. **F3 fresh-derive:** the population ran against the FRESH derive (live 174, not stale 169); a BEHIND / UNKNOWN-VINTAGE provenance header on the populated graph = not-GREEN (CTO).
5. **id-namespace canonicalization HONORED (RULE i, firm-aware):** any no-regression / coverage comparison canonicalizes TraceGraph-id ↔ Kuzu-node-id; S3 ids firm-aware (bucketless → 1:1/1:2[23 collisions]/1:3[client_performance bd+inf+mdpf] bucket-qualified, via ~D's d_s3key_firm_qualified.json). A pre-canonicalization id-diff = noise; a post-canonicalization residual = a real gap.

**Output:** independent gate-lift verdict (GREEN releases COMPDRIFT/COMPLEARN; RED/INCOMPLETE = reconcile). RAVC COO~B cc CTO + the producers.

---

## C. P2 per-tool no-regression RE-ASSERT  [trigger: P2 re-points each tool, post-population]

Per tool (its D3 cache-retirement gate): regenerate the deterministic sample → run the re-pointed tool → canonicalize ids (firm-aware for S3) → assert set-equality vs the locked fixture (comp-blast/trace/xref @V1; comp-platinum @V2 re-anchor) + selfcheck reproduces the 15-case verdict-set. Any post-canonicalization mismatch blocks that tool's D3 retirement. (Full recipe: FIXTURE_ATTESTATION.md §7.)

---

**State:** A = pre-staged, fires on the nightly. B = pre-staged, fires on slice-GREEN. C = P2-phase. I remain reachable (Monitor bdxtcu93u); COO~B/0.7.0 signal the nightly, ~D signals slice-GREEN.

— 3.0.0_SA_CVO~B
