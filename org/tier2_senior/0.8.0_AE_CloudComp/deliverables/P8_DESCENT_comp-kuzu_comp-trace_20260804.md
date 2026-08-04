# P8 INDEPENDENT DESCENT -- comp-kuzu + comp-trace (non-dialer cold use)

**Seat:** 0.8.0_AE_CloudComp~D (concurred non-dialer; adjacency = comp-pipescript, which I built
under F1/F9 -- NOT the dialed instruments). **TO:** ADHOC.p8-descent-kuzu-trace (COO GO 160454Z).
**Date:** 2026-08-04 ~1610-1650Z.

**INDEPENDENCE STATEMENT (required):** ZERO dial-record reads before Phase 2. Both descents ran
first (captures K0-K8, T1-T8b); `DIAL_RECORD_comp-kuzu_20260804.md` and
`DIAL_RECORD_comp-trace_20260804.md` were opened ONLY afterwards, for the Phase-2 diff. The
trace-leg gate was confirmed via CVO one-bit answer (trace dial CLOSED @a4581b96c; kuzu close
@395aaf053) with dial content explicitly withheld. The comp-pipescript dial record (a different
instrument) was read earlier for F9/F1 -- it is cited by this TO itself for the P8 class
definition and carries no kuzu/trace findings.

**Question derivation:** every question is something I actually needed this week (F9 watch-list
derivation, F1 consumer census, the io-discrimination fixture chain, the caller inventory,
deleted-module residue, mdpf trigger topology).

---

## Leg 1: comp-kuzu -- stumble table (10 captures)

| # | Question (real source) | Invocation | Result | Class |
|---|---|---|---|---|
| K0 | cold start: what is this tool? | bare `comp-kuzu` | Dialect primer: CloudNode/CloudEdge, node_type/edge_type are PROPERTIES, DO/DON'T examples, discovery queries | CLEAN (exemplary cold-start) |
| K0b/c | schema discovery | `RETURN DISTINCT n.node_type` / `e.edge_type` | Full lists + rich provenance header (DB vintage, per-table last-write, two-producer cohort note) | CLEAN |
| K1 | is pipeline_cli.py coupled to anything? (F9 watch list) | `WHERE n.node_id CONTAINS 'pipeline_cli'` | 0 rows | DEAD-END: **0 rows carries NO universe/scope statement** -- indistinguishable from "no coupling". Only my own census (K1b) revealed tool sources are out-of-universe |
| K1b | what IS modeled? | `RETURN n.node_type, count(*)` | 44+ classes incl. PipelineScript(133), PipelineFunction(1201) | CLEAN -- but this census was REQUIRED to interpret K1's 0 rows |
| K2 | accounts_dimension_latest.parquet lineage (fixture chain) | edges into/out of the key | A_00 WRITES_S3; 12+ bd readers; bucket CONTAINS/OWNED_BY | CLEAN, decision-useful |
| K3 | INF-side fixture chain (INF_A_00 -> INF_A_04) | scoped to the inf key | INF_A_00 WRITES_S3, INF_A_04 + 9 others READ_S3 | CLEAN -- independently corroborates the F1 fixture's chain |
| K4-K6 | gold_pipeline_deps.yaml / gold_dispatch.sh / adapter_audit_cli.py modeled? | CONTAINS probes | 0 rows all three | DEAD-END, same class as K1: config yamls, dispatch harnesses, tool/test sources out-of-universe, undisclosed at answer time |
| K7 | transitive downstream of A_00 (2-hop) | `(a)-[W]->(k)-[R]->(b)` | **0 rows, though K2 proved the data exists** | WRONG-FLAG-GUESS (mine, but instructive): READS_S3 points script->key, so BOTH edge types point INTO the key; naive flow-direction traversal silently returns empty. Direction convention stated nowhere in the primer |
| K7b | corrected | `(a)-[W]->(k)<-[R]-(b)` | 17 downstream readers | CLEAN post-correction |
| K8 | mdpf trigger topology (DOOR-6 standing concern) | TRIGGERS edges into mdpf lambdas | 3 edges incl. `mdpf-daily-refresh-trigger` EVENT_RULE -> `mdpf-daily-trigger` | CLEAN, decision-useful |

**Leg-1 verdict:** mechanically excellent where the question is in-universe (K2/K3/K7b/K8 are
fast, correct, corroborated). The cold-use hazard is concentrated in ONE class: **a 0-rows
answer is silent about scope and direction conventions** -- three of my eight real questions
(K1, K4-6, K7 pre-correction) produced 0 rows where the honest reading was out-of-universe or
wrong-pattern, not no-coupling, and nothing in the output discriminates.

## Leg 2: comp-trace -- stumble table (10 captures)

| # | Question | Invocation | Result | Class |
|---|---|---|---|---|
| T1 | cold start | bare `comp-trace` | `usage: cli.py {build,trace,blast,diff,xref} ... query required`; pipe-free rc=1 | MISLEADING (see T3) -- and note my FIRST rc read was corrupted by my own `\| head` (pipe-rc class; re-measured pipe-free per the law) |
| T1b | help | `--help` | Decent: direction/depth/json/all/check(0/2/1 rc semantics documented)/force | CLEAN |
| T2 | empty-query behavior | `comp-trace trace` (no query) | "Multiple matches for 'trace'" rc=0 -- the SUBCOMMAND WORD was consumed as the QUERY | MISLEADING: shim pre-supplies the subcommand; the usage text teaches a form the shim breaks |
| T3 | trace by taught form | `comp-trace trace A_00.accounts_dimension` | argparse error "unrecognized arguments" | MISLEADING (grounded): **the tool's own bare-call usage line teaches the underlying cli.py contract, not the shim's** -- the first thing a cold user sees misdirects them. Real form: `comp-trace <query>` |
| T3b | direct form | `comp-trace A_00.accounts_dimension` | Multi-match list (script + its functions) | CLEAN mechanics |
| T4 | exact-node trace | `comp-trace gold:A_00.accounts_dimension` | STALE_NODE_WARN (4 lambdas, `current=<missing>`) -> honest discard+rebuild 54s -> **STILL "Multiple matches"**: the EXACT canonical id cannot select itself because its function children share the prefix; no exact-match selector documented | DEAD-END (workaround guessing required) |
| T4b | bounded workaround | `--all --depth 1 --direction down` | Beautiful tree: WRITES_S3 key -> 12+ readers w/ file paths; matches kuzu K7b | CLEAN -- cross-instrument corroboration |
| T5 | rebuild-persistence discriminator | same call 3rd time | Warn = 1 NEW node (portal component, fresh shas), counts moved 2249/2940 -> 2250/2946; earlier warns did NOT recur | CLEAN (grounded): live concurrent churn, NOT a persistence defect; cost = ~51s rebuild per drift event on a moving estate |
| T6 | upstream of the $22M script | `build_canonical_prices_v2 --direction up --depth 2 --all` | Works; reveals `gold_dispatch (GOLD_SCRIPT) TRIGGERS` edge -- the dispatch harness IS in trace's universe (vs kuzu K5: absent) | CLEAN + one UNVERIFIED rendering note: WRITES_S3-labeled children appear under the TRIGGERS parent in the upstream tree; edge-label placement ambiguous to a cold reader. NOT claimed MISLEADING -- ungrounded, labeled INFERRED |
| T7 | cross-layer reach (D_04 -> portal) | `--direction down --depth 3 --all` | 22 platinum writes -> readers incl. `opal-partners-data` LAMBDA | CLEAN |
| T8/T8b | out-of-universe + typo messaging | `pipeline_cli` / `ZZZ_NO_SUCH_THING`, pipe-free rc | **"NOT-FOUND ... This is a NOT-FOUND, not a 'nothing-upstream/downstream' clear."** rc=3 | CLEAN -- exemplary; exactly the discrimination kuzu's raw 0-rows lacks |

**Leg-2 verdict:** the walker is mechanically strong (T4b/T6/T7 answered real questions with
file-path-grounded trees; NOT-FOUND semantics exemplary). Cold-use hazards concentrate at the
ENTRY: the bare-call usage text actively teaches a broken form (T1/T2/T3), and the exact-id
multi-match (T4) forces workaround guessing.

---

## Phase 2: two-direction diff vs the dial records

*(Records read AFTER both legs completed. Kuzu dial @395aaf053, trace dial @a4581b96c.)*

### Cold found that the dials did NOT flag

1. **[kuzu, the sharp one] 0-rows-without-universe is the kuzu instance of the trace dial's own
   T1 finding, unflagged in the kuzu dial.** Trace T1 (MED): "NOT-FOUND declares no universe, no
   denominator." comp-trace at least PRINTS a discriminating NOT-FOUND; raw comp-kuzu prints
   bare `(0 rows)`. The kuzu dial's P6 scored "honest-empty rc=0" as PASS -- true from the
   dialer's frame; from COLD USE, 3 of my 8 real questions returned 0 rows whose honest reading
   was out-of-universe/wrong-pattern, undiscriminated. Family-consistency remedy already named
   by the trace dial (comp-blast's repaired rc=3 prints universe + denominator): a one-line
   scope note on 0-rows, or unmodeled-class naming in the bare-call primer.
2. **[kuzu] Edge-direction convention undocumented (K7):** READS_S3 points script->key; both
   lineage edge types point INTO the key node, so naive flow traversal silently 0-rows. One
   primer line ("reads and writes both point AT the key; traverse lineage with `<-`") kills the
   class.
3. **[trace] The bare-call usage text teaches the underlying cli.py contract, not the shim's
   (T1/T2/T3, grounded by exercise).** Same CLASS as the dial's T4 (docstring teaches dead
   forms) but a sharper INSTANCE: the dial found it in the docstring; cold use hits it in the
   FIRST output a new user ever sees, and `comp-trace trace <q>` consuming "trace" as the query
   (T2) is actively confusing.
4. **[trace] Exact-id cannot self-select (T4):** `gold:A_00.accounts_dimension` -- the tool's own
   canonical id -- still multi-matches its function children; no exact-match flag documented.
   Adjacent to dial T2 (ambiguity semantics) but a distinct instance: this input is NOT
   ambiguous, it is the exact node id.
5. **[trace, datum not defect] 4 indexed lambda sources now `<missing>` on disk** (finbert,
   mdpf-manifest, schwab-bronze-freshness, security-sweep-daily) -- deletion-residue class,
   surfaced in T4's drift warn; the dial's probe saw 23 drifted nodes but the record does not
   name the missing-source subset. Also: the drift warn says "Rerun: comp-build" and then
   auto-rebuilds anyway -- the advice is redundant with the behavior that follows it.
6. **[cross-instrument, for the NAVIGATE consolidation] Scope asymmetry with no cross-pointer:**
   gold_dispatch is IN trace's universe (TRIGGERS edges, K5-answering) and ABSENT from kuzu's;
   kuzu carries AWS planes (buckets, IAM, event rules) at grains trace does not. A 0-rows/
   NOT-FOUND in one instrument is frequently answerable by the other, and neither points across.

### Dial found that cold use never hit

- **kuzu K1** (manifest canonical calls citing dead `id` property): unhittable -- repaired
  @e0d657799 BEFORE my descent, and the bare-call primer taught me `node_id` correctly. The
  repair held under cold use.
- **kuzu K3** (-full/-inc contracts), **K4** (stitch DB staleness), **K5** (bare pipescript
  alias), **P6 -inc labeled-stale skip**: my descent never left the default surface -- consistent
  with the dial's claim that the defect mass sits off the default path.
- **trace T0** (no output contract) and **T3** (built_at never printed): cold use CANNOT see an
  absent contract -- and tellingly, I never NOTICED the missing provenance header until reading
  the dial. That non-noticing is itself evidence for T3: the vintage axes are invisible exactly
  when nobody is looking for them.
- **trace T1's specific shape** (bare name WITH `.py` suffix -> NOT-FOUND on an existing node):
  my queries never used file suffixes; no collision, no contradiction.

### Convergences (independent confirmation, found blind)

- My T2 = dial T2 (ambiguity-at-rc=0, comp-blast family disagreement) -- found cold, verbatim.
- My T1/T3 class = dial T4 class (taught-form drift) -- different instances, same law.
- My T8 = dial P6 Q2 (honest NOT-FOUND) -- confirmed from cold.
- My K2/K3/K7b lineage answers corroborate the same chains comp-pipescript io traverses (and
  T4b corroborates K7b across instruments) -- where scopes overlap, the instruments agree.

## MISLEADING-claim grounding index (TO scope 2)

- T3 "usage teaches a broken form": grounded by the exercised triple (bare usage text; `trace`
  consumed as query at T2; direct form working at T3b). CONFIRMED.
- T6 upstream edge-label placement: NOT grounded -- labeled INFERRED, no classification beyond
  a rendering note.
- T5 rebuild-persistence suspicion: REFUTED by my own discriminator (drift warns never recur;
  counts move with live churn) -- recorded as CLEAN, cost note only.
- K7 0-rows: grounded (K2 had already proven the data; the corrected pattern K7b returns 17
  rows).

-- 0.8.0_AE_CloudComp~D, 2026-08-04
