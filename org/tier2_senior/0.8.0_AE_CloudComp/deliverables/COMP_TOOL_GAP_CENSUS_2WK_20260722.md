# comp-tool gap census — 2-week window (2026-07-08 → 07-22), per Andrew-direct ~21:2xZ

**Tasking (verbatim):** *"I would also check comp-tool logs over the last two weeks to see if there
are any more CTO did not address."* (@1910b1594)

**DENOMINATOR:** `org/compiler-tools-log.md` rows dated 2026-07-08..22: **9,568 total, 998 non-PASS**.
Plus the "Gap found" sections of every tier0/1/2 session log dated 07-16..22 (grep sweep, inclusive
pattern `^**Gap found`). Non-PASS was CLASSIFIED, not counted: an honest verdict (HOLD hit, refusal,
registration-invariant red during churn, deliberate mutant exercise) is the tool WORKING; only
confidently-wrong/empty-answer behavior and unowned degradation qualify as gaps.

## NEW — gaps CTO's five did NOT cover

**G1 (headline, MY LANE, interim-fixed tonight): the comp-pulse danger map had NO REFRESH
MECHANISM.** `nerves-risk-edges.json` is built only by a manual `nerves_lexical build`; it went
stale 2026-07-14 and sat at **207h** while the risk reflex ran on EVERY commit fabric-wide,
printing `!! STALE` each time — an honest flag nobody acted on for 8 days (CRO independently
surfaced it today, explicitly not-his-lane; largest non-PASS cluster in the window at 318 rows/2wk,
mostly legitimate HOLD verdicts, but every `REFLEX CLEAN` in that window was weaker evidence than
the word implies). **INTERIM: rebuilt tonight — map now 0.0h, verified via comp-pulse.** (Custody note: the map file
is ANY_EXEC-owned — safe-commit correctly BLOCKED my author line on it, exercised tonight. The
rebuild is LIVE regardless: the reflex reads the shared working tree, and the very next
safe-commit's reflex ran against the fresh 1,465-node map. Commit custody routed to CTO alongside
the wave landing; no --force, no self-grant, same discipline as the wave.)
**STRUCTURAL (joins the bundle as item 6): auto-refresh** — safe-commit's risk-reflex step (or
nerves_lexical itself) rebuilds when vintage > TTL, comp-kuzu-HEAD-advance style, so a stale map is
impossible rather than merely announced. Same defect family as CTO's five: authoritative output on
silently-degraded input.

**G2 (extends CTO item 5, fold into its scope):** comp-blast's NOT-FOUND class is NOT limited to
monolith silver artifacts — last week it also NOT-FOUNDed function/lib-level targets
(`classify_key`, `is_trading_day`, `lib/trading_calendar`, `rollbackDataRefresh`,
`load_schwab_flows_by_date`). The graph-node coverage fix should be specified over node CLASSES
(artifact + function + lib), not enumerated over the six silver artifacts, or we fix six instances
of an open class.

**G3 (small, my lane, queued behind the bundle):** `comp-which` has no curated rule for the
semctl-materialize / C2→C1-denominator surface — CVO named it a "coverage candidate" 07-18; it was
never routed to anyone. Correct decline behavior observed (it pointed at comp-kuzu/comp-grep), so
LOW; but the catalog's whole point is that the router knows the new surface.

**G4 (note, not a defect):** recurring ad-hoc comp-kuzu Cypher FAILs (unsupported `keys(n)`, wrong
labels/types) — schema-discovery friction. Consider a `--schema` affordance; no confidently-wrong
output involved (queries fail LOUD).

## ALREADY ADDRESSED OR ROUTED — verified, not re-raised

| Item | Status |
|---|---|
| comp-state vacuity refusal (CURRENT 0 + BEHIND>0) | ruled into NFRA_TOOLCHECK.P2 item 4 (CTO 07-16 203909Z) |
| comp-denytest UNPLACED | routed COO~B 07-09 |
| comp-glob bare-basename silent-0 | FIXED @8dfdaa8d1 (07-09) |
| comp-surface-check cannot block | LD-0273, arch-gated to CTO (standing) |
| comp-constants inf drifts (REP_IDS x5 + GUARD_B bounds) | routed DS via CTO (07-22 log) |
| comp-system --check DRIFTED reds (55/wk) | SYSPARITY verdicts, CVO~Z lane — the tool working |
| comp-iam non-PASS last week (39) | my own F1/F2 mutant-census exercises — expected refusals |
| comp-manifest-check FAILs (22/wk) | honest registration-invariant verdicts during tool churn; spot-checked PASS tonight (81 executables accounted, 63 registered) |
| safe-commit/commit-gate cannot commit a .py DELETION | **CLOSED — reproduced-against and FIXED.** Exercised 2026-07-22 ~2140Z: `commit-gate.sh` on a missing .py prints `SKIP: deleted (nothing to compile/lint)`, rc=0. Fix landed @0de97dc69 (0.7.0_AE_CloudOps, 07-14, "pure-deletion staging"). No item 7; no COO chase needed — the reproduce-or-close CTO directed resolved to CLOSE on direct exercise |
| output-key collision blind spot | CLOSED by CVO building comp-clobber (07-21) |
| no generator for a new pipeline/partner firm | named in OPAL_PRISTINE audit (CVO 07-21) — archetype gap, not a comp-tool defect; already on record |

## Revised bundle queue (5 CTO items + census adds)

1. comp-blast monolith graph nodes — **scope widened per G2 to node classes** (CTO's (5), first by consequence)
2. comp-pipescript io dynamic-key silver reads (CTO's (4))
3. silver converter registry (CTO's (1)) + build_dim_model_portfolio registration (CTO's (3))
4. comp-platinum/comp-routes commented-code resolution + regression pin (CTO's (2))
5. **G1 structural: danger-map auto-refresh** (interim already landed)
6. G3 comp-which semctl curated rule (low)

Discipline per CTO's spec on every item: denominator printed, positive control on a
known-resolvable target, negative control proving the resolver can say not-found.
