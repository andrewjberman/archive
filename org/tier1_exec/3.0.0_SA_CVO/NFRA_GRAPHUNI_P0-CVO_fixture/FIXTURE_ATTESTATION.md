# NFRA_GRAPHUNI P0-CVO — no-regression PRE-DELTA FIXTURE — CVO ATTESTATION + FIXTURE-LOCKED

**archetype:** VALIDATE
**Owner / attestor:** 3.0.0_SA_CVO~B (NFRA_COMP* verification lane)
**TO:** `org/projects/NFRA_GRAPHUNI/task_orders/NFRA_GRAPHUNI.P0-CVO.no-regression-fixture.md`
**Date:** 2026-06-30
**Status:** **FIXTURE-LOCKED** — both layers frozen against authoritative pre-delta state; this is the HARD GATE that releases NFRA_GRAPHUNI/GRAPHDEPTH P1 population (COO~B GOes P1 on this lock).

---

## 1. What this fixture is (the no-regression contract)

The PRIMARY GRAPHUNI risk (MSTR-named, PRD §4 + CTO Ruling R3): a re-pointed `comp-blast`/`comp-trace`/`comp-xref`/`comp-platinum` — once P2 re-points it off its local cache onto the unified Kuzu graph @ marker head — MUST return the SAME answers it returns today. This fixture freezes "today's answers" while the local caches + the gate are still authoritative, so P2 can prove no-regression by set-equality. Per CTO 214806Z it is **two layers**:

- **Layer (a) — the 4 structure-tools' pre-delta ANSWERS** (`fixture_layer_a.tool_answers.json`). Pins the OUTPUT.
- **Layer (b) — ~C's frozen `comp-coverage-check selfcheck` per-rule VERDICT-SET** (`fixture_layer_b.selfcheck_verdicts.json`). Pins the CHECKER. Caught from my unknown-unknown: a tool-answer-only fixture pins output but not the gate logic, which is mutating as ~C folds rules while ~D populates — a checker drift (existential-rollup sliding to 1:1 = the `047ce51d0` class, or referenceable-target weakening) would pass a layer-(a)-only fixture invisibly.

Both captured BEFORE any P1 graph mutation. Capturing after a mutation corrupts the baseline — hence ordered FIRST.

## 2. Integrity proof (why this baseline is trustworthy)

- **Pre-delta source (layer a):** the `TraceGraph` cache `.comp-graph/graph.json` (feeds comp-blast/trace/xref) + the platinum caches (feed comp-platinum). Pinned copy: `graph.json.pinned_predelta`. **content_sha256 = `39f002859e8b815d…`** (`PROVENANCE.txt`), 2,152 nodes / 2,772 edges.
- **Stability across a rebuild — VERIFIED.** The cache `built_at` moved `2026-06-30T21:48:43Z → 21:53:43Z` during capture (a content-stable HEAD-advance refresh from the fleet's commits — node/edge type counts byte-identical across the bump). I did not assume count-equality is sufficient: I **re-ran the full capture and diffed all 65 per-answer SHAs — 0 mismatches**, byte-identical across two runs spanning the rebuild. The fixture is a deterministic function of stable pre-delta content, not a snapshot of a moving target.
- **Before P1 mutation:** the unified Kuzu graph still holds 0 gold-pipeline nodes / 0 CALLS edges (gap-list §1); P1 is gated on THIS lock, so no derive has run. Confirmed pre-delta.

## 2a. Vintage model + the 3-condition P1 gate (CTO ruling 220955Z / COO~B 221205Z)

This fixture is condition (a) of a **3-condition P1 gate** (COO~B holds the GO). The fixture is NOT mono-vintage — a naive single-vintage lock would false-FAIL every comp-platinum re-point, because comp-platinum's AWS-resource chain is vintage-SENSITIVE (today's 4 new Lambdas, live count 169→174). CTO's scoped-hybrid vintage ruling:

- **comp-blast / comp-trace / comp-xref + layer (b) — LOCKED@V1, FINAL.** These are code-structure / gate-logic, AWS-deploy-INVARIANT. The pre-mutation integrity proof (§2) holds; strict set-equality at V1. This is what is locked NOW.
- **comp-platinum AWS-chain — RE-ANCHORED@V2 (condition c SATISFIED 2026-06-30 ~2252Z).** Baseline = `fixture_layer_a.comp_platinum_V2.json` (SUPERSEDES the V1-provisional comp-platinum answers in `fixture_layer_a.tool_answers.json` for the comp-platinum no-regression check ONLY). V2 vintage = marker HEAD `7647070038814948852` @22:27:32Z, Lambda 174, workspace `91cf62212` / portal `ad97d915`. Mechanism grounded (Rule 22): comp-platinum builds routing/dag/dataflows from WORKSPACE source under a 5-min-TTL freshness contract — a first naive re-run left `dataflows` stale (mixed-vintage, CAUGHT) → redone with a consistent **`gc.Freshness.FORCE` rebuild of all 5 caches** then re-captured. Result: **14/16 components + 4/4 reverse IDENTICAL V1==V2; 2 real post-174 vintage-drifts** (AdvisorsTab cosmetic line-shift; PartnerAnalytics `getHeaderMetricsFresh→getHeaderMetrics`, confirmed against current committed source line 154 = V2 is truth). So the re-anchor was NECESSARY — a V1-vs-repoint@V2 compare would have false-FAILed PartnerAnalytics. comp-blast/trace/xref + layer(b) stay LOCKED@V1.

**The 3-condition P1 gate — ALL SATISFIED:** (a) fixture LOCKED [✓ `9d5765b82`] + (b) fresh derive landed [✓ ~B/COO~B-verified, marker 7647070038814948852, Lambda 174] + (c) comp-platinum AWS-chain re-anchored@V2 [✓ this artifact]. → COO~B GOes P1.

## 3. The deterministic, reproducible sample (so P2 regenerates it identically)

Sample selection (`repro_1_select_sample.py` → `sample.deterministic.json`) is **rule-based, not hand-picked** — top-K by degree per pipeline/class, id-ascending tie-break — so P2 regenerates the IDENTICAL sample and the comparison is a clean set-equality, not a sample-drift artifact.

| Tool | Sample | Selection rule |
|---|---|---|
| comp-blast | 28 targets: 8 bd-fn + 8 inf-fn (hot paths) + 6 script-level + 6 S3 artifacts | top-K by CALLS-degree (fn) / S3-IO-degree (script,S3) |
| comp-trace | 8 nodes (top fn both pipelines + scripts + S3) | up + down, separate runs (set-form per direction) |
| comp-xref | 9 symbols spanning fn-name / file-path / S3-key / lambda / endpoint | derived from the blast/S3 sample heads |
| comp-platinum | 16 component `page` chains + 4 `reverse` on top S3 keys | the full platinum `summary` component set |

## 4. Coverage attestation (representative + hot-path-covering — AC3)

- **Hot paths:** the top gold functions by CALLS-degree are in the blast sample — incl. `D_01.partner_analytics:generate_header_metrics` (the served-AUA-header builder, blast radius 39), `B_01.holdings_lots:build_holdings_lots_snapshot`, `B_00.canonical_holdings:main`, `INF_D_00.portal_aggregates:main`, `INF_D_02.advisor_client_detail:{build_client_details,build_advisor_books}`. A regression is most likely to surface on a large radius — **blast radius sizes: min 14 / median 132 / max 216 ids, 0 empty.**
- **Both pipelines:** bd (723 gold) + inf (606 gold) both represented in blast/trace/xref/platinum.
- **Node classes exercised:** GOLD_SCRIPT (function + script level), S3_ARTIFACT (top-IO), COMPONENT + ENDPOINT (via platinum), LAMBDA + EVENTBRIDGE (via xref/sample). 
- **Edge classes exercised:** CALLS (blast/trace over functions), READS_S3 / WRITES_S3 (blast over scripts + S3 artifacts), FETCHES (platinum chains), TRIGGERS (sampled).
- **comp-platinum:** all 16 component chains non-empty (min 4 / median 28 / max 123 lines); 4 reverse non-empty.
- **comp-xref:** all 9 symbols matched ≥1 node (node_count min 1 / median 7 / max 110 — the `main` multi-match case included).

## 5. DOCUMENTED SOFT-SPOTS (honest scope of the regression signal — not hidden)

The fixture is a valid no-regression baseline everywhere, but two case-classes are weaker DETECTORS and I mark them non-binding so a future reader does not over-trust them:

- **2 script-level trace cases are empty-both-ways** (`gold:D_04.client_portal_summary`, `gold:INF_D_04.client_portal_summary`). comp-trace walks the CALLS (fn→fn) graph; a script-level node has no CALLS edges (those live on its `:function` children), so up=down=∅. A valid baseline (P2 must reproduce ∅) but a WEAK detector (a re-pointed tool returning ∅ for a different reason still "matches"). **The trace regression signal is carried by the function-level cases** (down median 45, max 157) — those bind.
- **3 xref symbols have edge_count=0** (matched-node set present). Per gap-list §3, comp-xref is a LENS over the same TraceGraph substrate comp-blast uses (definition site = the function node; reference sites = its CALLS/READS_S3/WRITES_S3 edges) — there is no separate xref index. So **xref's edge-set no-regression guarantee RIDES ON comp-blast's edge-set fixture** (shared substrate); layer-(a) xref captures the matched-node set + counts as xref's independent signal, and the deeper edge guarantee is entailed by comp-blast's. This is by design, not a gap.

## 6. Layer (b) — the frozen gate-verdict baseline

Source: ~C `comp-coverage-check selfcheck --json` (commit `8ad43b6dc`), frozen at the **stable 14-case point** (~C confirmed: NOT 12 — the referenceable-target rule (gate rule 11 = my LD-0230 EP-2 / invariant 5) was the LAST LD-0230 invariant, just folded; all 5 LD-0230 invariants are now gate rules). `all_ok:true`, 11 gate_rules, ledger_version 1.

The frozen `{id → (kind, expected)}` map (14 cases) is in `fixture_layer_b.selfcheck_verdicts.json`. The load-bearing per-rule discriminators:
- `rollup_1to1_semantics → FAIL` + `rollup_defects_existential → holds` — pins the existential OR-rollup vs the `047ce51d0` 1:1 regression class.
- `breadth_terminal_allowed_target → FAIL` + `seam_breadth_terminal_instance → holds` — pins the referenceable-target rule (EP-2).
- `grain_retyping → FAIL` (split-by-depth), `unattributed_edge_type → FAIL`, `no_checker_rule → UNVERIFIABLE`, `clean_passes → PASS`.

**~C's commitment (binding):** no EXISTING case's expected verdict will change (a changed existing verdict IS the regression this catches); new rules are ADDITIVE-only, with a ping to me to extend the fixture additively. The case list is 1:1-guarded (a metadata/append mismatch self-fails UNVERIFIABLE — the map cannot silently drift from the cases).

## 7. P2 RE-ASSERT recipe (how each re-pointed tool is gated on this fixture)

**Layer (a) — per tool, per its D3-retirement gate (PRD R3, never strand a tool on a deleted cache):**
1. Regenerate the sample with `repro_1_select_sample.py` (deterministic — identical top-K).
2. Run the RE-POINTED tool (reading Kuzu @ marker head) over the same sample; compute the same set-form answers (`repro_2_capture_layer_a.py`, repointed).
3. Assert per-target SHA equality vs `fixture_layer_a.tool_answers.json`. Any mismatch = a coverage regression for that tool → **blocks that tool's D3 cache-retirement** until reconciled.

**RE-ASSERT PRECONDITION (CVO finding — the comparison is only meaningful if id-namespaces match; CTO RULE (i) 220713Z = a hard P2 prerequisite + P2 deliverable):** the fixture answers are in the TraceGraph id namespace (`gold:…`, `s3:…`, `lambda:…`, `endpoint:…`). The no-regression diff tests SEMANTIC equality (same node SET / same blast-radius), NOT id-string equality. So P2 MUST canonicalize BOTH sides to a common id namespace BEFORE the set-compare, OR a 100%-correct re-point false-FAILs on id-form alone (constant false-reds → the gate is unusable). A residual id-diff AFTER canonicalization = a REAL gap; a pre-canonicalization id-diff = noise.

**S3 ids must be canonicalized FIRM-AWARE, not by naive string (per ~D 220752Z — strengthens RULE (i)):** the frozen pre-delta S3 ids are **BUCKETLESS** (`s3:gold/…`); the unified-graph S3Key ids are **BUCKET-QUALIFIED** (`opal-data-{firm}/gold/…`, per ~C's convention `02286234a`). A bucketless pre-delta id maps to bucket-qualified post-delta ids. **LANDED (byte-exact) mapping — `org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-D.bucketless_to_qualified.json`, derived from the landed Phase-A producer (HEAD `3316621630930459138`):** 146 bucketless keys → 169 bucket-qualified `opal-data-{firm}/…` ids; cardinality **123 × 1:1 (single-firm) + 23 × 1:2 (the bd+inf collisions)**. **RECONCILIATION (landed vs projected):** the earlier `1:3` for `gold/timeseries/client_performance.parquet` (bd+inf+mdpf) was the *structural projection*; in the LANDED graph the mdpf leg was an UNRESOLVED read (surfaced, not landed) → it is **1:2 (bd+inf)** in the actual graph. So max cardinality in the landed reality is 1:2, not 1:3. P2 expands each bucketless pre-delta id to its firm-qualified set FIRST, then diffs vs the post-delta ids — a pre-delta id with 0 post-delta matches = a REAL regression; the 1:2 expansions are EXPECTED. `gold:`/`lambda:`/`endpoint:` ids have no bucket dimension. Bucket spelling grounded `opal-data-{bd,inf,cot,mdpf}` vs live S3_BUCKET nodes. So P2's S3 set-equality MUST diff in the firm-qualified space (or expand each bucketless pre-delta id to its firm-qualified set first) using ~D's producer-firm mapping `NFRA_GRAPHUNI.P1.d_s3key_firm_qualified.json` (key → writer_firms/reader_firms → bucket); ~D hands the explicit bucketless↔bucket-qualified table as P2-prep at populate-time. `gold:`/`lambda:`/`endpoint:` ids have no bucket dimension and are unaffected. A naive string compare would false-mismatch EVERY S3 id. **P2 owns the firm-aware canonicalization map before running the diff** — it is also the reusable map that lets comp-blast/platinum traverse across the re-pointed substrate.

**Layer (b) — post-fold / post-population:**
1. Run `comp-coverage-check selfcheck --json`.
2. Assert every case's `(kind, expected)` matches the frozen map AND `passed:true`. A checker drift (existential→1:1, referenceable weakening) flips a case → caught. New additive cases are allowed (≥14, the 14 unchanged); a CHANGED existing verdict is a regression.

## 8. CVO ATTESTATION (AC3)

I attest, as the independent NFRA_COMP* verifier, that this fixture is **representative and sufficient to detect a real per-tool coverage regression in P2**: it covers the hot paths (top-degree gold functions, both pipelines), every node/edge class the four tools traverse, with substantive non-empty answers (blast radius median 132); it pins BOTH the tool outputs (layer a) AND the gate checker discriminators (layer b); it is integrity-proven (content_sha stable, 65/65 answers deterministic across a rebuild); and it is captured pre-mutation. The two documented soft-spots (§5) and the re-assert id-namespace precondition (§7) are scoped and assigned, not hidden. **FIXTURE-LOCKED.**

## 9. Artifacts (this directory)

| File | Role |
|---|---|
| `fixture_layer_a.tool_answers.json` | layer (a): 65 set-form tool answers + per-answer SHA |
| `fixture_layer_b.selfcheck_verdicts.json` | layer (b): the frozen 14-case gate-verdict map |
| `sample.deterministic.json` | the rule-selected sample (reproducible) |
| `graph.json.pinned_predelta` + `PROVENANCE.txt` | the pinned pre-delta TraceGraph + content_sha256 |
| `repro_1_select_sample.py` / `repro_2_capture_layer_a.py` | the deterministic reproduction harness (P2 re-runs these against the re-pointed graph) |

— 3.0.0_SA_CVO~B
