# NFRA_COMPREG -- Registration-Gap Audit (2026-07-18)

**Deliverable 2** of NFRA_COMPREG (Andrew-direct: *"scan all the comp-tools and establish if there are
any that are not properly registered and make sure they get registered through that canonical flow"*).
**Author:** 0.8.0_AE_CloudComp~B. **Method:** `registration_audit.py` (colocated), reproducing the exact
registries `comp-manifest-check`'s registration-invariant (member 5) reads. Cross-checked against the live
gate: `comp-manifest-check completeness` -> `registration-invariant PASS`.

## Result: CLEAN -- 0 registration gaps across 77 tracked comp-* executables

**Denominator (printed, per CTO gate point 3 -- a sweep that cannot name what it did not cover is the
silent-truncation class):**

```
universe = 77 tracked .tools/comp-* launchers (git ls-files, extensionless, member-5 filter)
  tools_index   = 59   (routable routing targets)
  excluded      = 15   (excluded_not_graph_use_cases, each with a reason)
  entries-tools = 64   (distinct entries[].tool -- has an agent-phrasing use_case row)
  coverage-map  = 80   (union tools[]=35, meta_tools[]=45 -- the posterior router's ledger)
unaccounted (in NEITHER tools_index NOR excluded NOR any entries row) = NONE
unledgered  (absent from comp-coverage-map union)                     = NONE
```

Every one of the 77 executables is accounted (tools_index OR excluded-with-reason OR an entries `tool:`)
AND ledgered in the coverage map. This is expected: NFRA_COMPCLOSE landed the registration-invariant as a
ramp-exempt commit-time gate on 2026-07-14, so no unregistered comp-tool has been committable since. The
audit CONFIRMS the estate is gap-free and gives the per-tool denominator on the record.

## Disposition breakdown (the three registration outcomes the canonical flow decides between)

Counts are over the **77-tool comp-* universe** (the member-5 filter: tracked, extensionless, `comp-`
prefix). They differ from the raw registry sizes in the denominator because two registry rows name entities
outside that universe -- `tools_index` carries `pipescript` (the non-`comp-` human entry point) and
`excluded_not_graph_use_cases` carries `comp-v5-composite-test` (the `.sh` regression test). Both are
correctly accounted; neither is in the 77.

| Disposition | Count | Meaning |
|---|---|---|
| REGISTERED (routable) | 58 | tools_index=Y + coverage-map home + entries row -- a first-class comp-which routing target |
| REGISTERED (entries-only) | 5 | tools_index=N but has a coverage-map home + entries row -- a subcommand-variant, a split sibling, or the router itself: comp-describe, comp-kuzu-full, comp-kuzu-inc, comp-state, comp-which |
| EXCLUDED (with reason) | 14 | in excluded_not_graph_use_cases -- NOT a graph-query use-case: enforcement gates, worklist producers, graph producers, on-rails search/inspection primitives, context setters |

(58 + 5 + 14 = 77. Raw registry denominators: tools_index 59 = 58 comp-* + pipescript; excluded 15 = 14
comp-* + comp-v5-composite-test.)

## Per-tool verdict table

```
TOOL                     TI  CM     EXC ENT  VERDICT
----------------------------------------------------------------------
comp-adapter-audit       Y   tools  .   Y    REGISTERED
comp-assets              Y   tools  .   Y    REGISTERED
comp-aws                 Y   tools  .   Y    REGISTERED
comp-axes                Y   meta   .   Y    REGISTERED
comp-blast               Y   tools  .   Y    REGISTERED
comp-build               Y   meta   .   Y    REGISTERED
comp-cache               Y   tools  .   Y    REGISTERED
comp-canon-motif         .   meta   Y   .    EXCLUDED
comp-chainrun            Y   tools  .   Y    REGISTERED
comp-cluster             Y   tools  .   Y    REGISTERED
comp-constants           Y   tools  .   Y    REGISTERED
comp-coverage            Y   meta   .   Y    REGISTERED
comp-coverage-check      .   meta   Y   .    EXCLUDED
comp-deadgrant           Y   meta   .   Y    REGISTERED
comp-debris              Y   meta   .   Y    REGISTERED
comp-denytest            Y   meta   .   Y    REGISTERED
comp-depth               Y   tools  .   Y    REGISTERED
comp-describe            .   meta   .   Y    REGISTERED (entries-only)
comp-diff                Y   tools  .   Y    REGISTERED
comp-dispatch            Y   tools  .   Y    REGISTERED
comp-drift               Y   meta   .   Y    REGISTERED
comp-dups                Y   tools  .   Y    REGISTERED
comp-fedobs              Y   meta   .   Y    REGISTERED
comp-firmsep-sweep       Y   meta   .   Y    REGISTERED
comp-freshness           Y   tools  .   Y    REGISTERED
comp-gitdrill            Y   meta   .   Y    REGISTERED
comp-glob                .   meta   Y   .    EXCLUDED
comp-graph               Y   tools  .   Y    REGISTERED
comp-grep                .   meta   Y   .    EXCLUDED
comp-heat                Y   tools  .   Y    REGISTERED
comp-honesty             Y   tools  .   Y    REGISTERED
comp-iam                 Y   tools  .   Y    REGISTERED
comp-iam-usage           Y   meta   .   Y    REGISTERED   (DECOMTOOL exemplar: CREATE)
comp-icedrill            Y   meta   .   Y    REGISTERED
comp-imgread             .   meta   Y   .    EXCLUDED
comp-incrparity          Y   tools  .   Y    REGISTERED
comp-kit-striplist-gate  .   meta   Y   .    EXCLUDED
comp-kuzu                Y   tools  .   Y    REGISTERED
comp-kuzu-full           .   meta   .   Y    REGISTERED (entries-only)  (KUZUSPLIT exemplar)
comp-kuzu-inc            .   meta   .   Y    REGISTERED (entries-only)  (KUZUSPLIT exemplar)
comp-lambdamap           Y   tools  .   Y    REGISTERED
comp-learns-score        Y   meta   .   Y    REGISTERED
comp-learns-status       Y   meta   .   Y    REGISTERED
comp-manifest-check      .   meta   Y   .    EXCLUDED
comp-parity              Y   tools  .   Y    REGISTERED
comp-passcraft           .   meta   Y   .    EXCLUDED
comp-perf                .   meta   Y   .    EXCLUDED
comp-pii                 Y   tools  .   Y    REGISTERED
comp-pipescript          Y   tools  .   Y    REGISTERED
comp-platinum            Y   tools  .   Y    REGISTERED
comp-pulse               Y   meta   .   Y    REGISTERED
comp-pydeps              Y   meta   .   Y    REGISTERED
comp-registry            Y   meta   .   Y    REGISTERED
comp-routable-check      .   meta   Y   .    EXCLUDED
comp-routes              Y   tools  .   Y    REGISTERED
comp-secrets             Y   tools  .   Y    REGISTERED
comp-shell               Y   tools  .   Y    REGISTERED
comp-state               .   meta   .   Y    REGISTERED (entries-only)
comp-stitch-refresh      .   meta   Y   .    EXCLUDED
comp-surface-check       .   meta   Y   .    EXCLUDED
comp-symbols             Y   tools  .   Y    REGISTERED
comp-system              Y   meta   .   Y    REGISTERED
comp-tagauthz            Y   meta   .   Y    REGISTERED
comp-to                  .   meta   Y   .    EXCLUDED
comp-tool-health         Y   meta   .   Y    REGISTERED
comp-tool-health-gate    .   meta   Y   .    EXCLUDED
comp-toolgraph           Y   meta   .   Y    REGISTERED
comp-tooltip             Y   tools  .   Y    REGISTERED
comp-trace               Y   tools  .   Y    REGISTERED
comp-transform           Y   tools  .   Y    REGISTERED
comp-trigger             Y   tools  .   Y    REGISTERED
comp-types               Y   tools  .   Y    REGISTERED
comp-validate            Y   tools  .   Y    REGISTERED
comp-which               .   meta   .   Y    REGISTERED (entries-only -- the router itself)
comp-whoread             Y   meta   .   Y    REGISTERED
comp-xray                Y   tools  .   Y    REGISTERED
comp-xref                Y   tools  .   Y    REGISTERED
----------------------------------------------------------------------
GAPS: unaccounted=NONE | unledgered=NONE
RESULT: CLEAN -- 0 registration gaps across 77 tools
```

(`pipescript` -- the non-`comp-` human entry point -- is registered in tools_index + entries + coverage-map
but sits outside member 5's `comp-*` universe filter by design; it is accounted, not a gap.)

## Secondary finding (non-blocking, NOT a registration gap): self-route NEARTIE

`comp-manifest-check completeness` reports 57 self-route **NEARTIE WARNs** ("surfaces only inside
comp-which's near-tie list, never rank-1"). These are threshold-shaped (member 3 hard-blocks only on a
MISS -- a tool comp-which returns *nothing* for; NEARTIE means it *does* surface, just not rank-1) and so
are reporting-only, not gaps. They indicate routing-precision headroom (many tools cluster near-tie for
their own use_case), which is a NFRA_COMPROUTE/curated-vocabulary concern, not a NFRA_COMPREG registration
concern. Recorded here so the audit names it rather than silently dropping it; no closure action under this
project.

## Reproducibility

`python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPREG/registration_audit.py`
Ground-truth gate (authoritative): `comp-manifest-check completeness`.
