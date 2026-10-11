# ADVI_FIRMBKTS FB-f-7 -- the advTenant entitlement schema, Rule-24 record

Cell FB-f-7 (round 3, enrichment item 1; PRD F6; LD-0442's carried row). Built DORMANT: nothing is deployed. The field
is `advTenant` in the generated `FIRM_CONFIG` (`infra/aws/lambda-edge/_shared/firm-config.mjs`, emitted by
`lib/opal_naming.py` `_blk_firm_config`). The denominators below are read from that generated block at the commit that
carries this record (registry at HEAD of the worktree, generator as amended by the issuer's 1a.1).

## (i) MECE over a declared domain

Declared domain: the generated `FIRM_CONFIG` firmIds (the served tenants of `scopes.json`, pseudo tenants excluded).
Denominator: 5 firmIds in the domain; 5 tenant directories; 6 (firmId, tenant directory) entitlement pairs.

| firmId | bucket (configured) | advTenant (generated) | role |
|---|---|---|---|
| 49financial | opal-data-bd | [49financial] | scope's own tenant |
| inflection | opal-data-inf | [inflection] | scope's own tenant |
| cottonwood | opal-data-cot | [cottonwood] | scope's own tenant |
| mockadv | opal-data-bd | [mockadv, 49financial] | alias tenant: its own directory and the scope's directory, both declared |
| demo | opal-data-demo | [demo] | scope's own tenant |

Subtraction over the domain: every tenant directory of the domain has at least one reader (uncovered directories: 0 of 5).
The cover is complete and NOT disjoint: the 49financial directory has two declared readers (49financial itself and the
alias mockadv), because the alias is declared to it. The overlap is the declaration itself, never an inference from a
shared bucket. Values one remedy does NOT move: the five firmId keys, the five bucket values (no bucket is edited by this
cell), the displayName values, and the `platinum/advi/` path class with its 401 body and rule name.

## (ii) SAME GRAIN

The entitlement is at tenant-directory grain: the unit compared is the `{tenant}` segment of `platinum/advi/{tenant}/`
against the caller's `advTenant` set. The bucket is a storage grain and is no longer compared on this path class. Both
the router and the guard read the same field at the same grain, and the guard derives its membership independently from
the same generated config. Values one remedy does NOT move: the directory name strings themselves, the origin choice
(platinum tier constant, set after the assertion as at base), and the bucket grain on every non-platinum path (gold,
views, satellites), which keeps its bucket comparison unchanged in both functions.

## (iii) INTENT COHERENCE

One axis, one intent: `advTenant` answers one question, which tenant directories an identity may read. A declared alias
is an entitlement, not a bucket accident: mockadv reads its own directory and the directory its declaration names. The
remaining residual, declared not hidden: the opal-capital staff proxy names a BUCKET slug (`?firm=<slug>` ->
`opal-data-<slug>`), so its set is derived by grouping firmIds on the bucket field. That is a second axis that a later
cell may replace with a tenant-named proxy; this cell does not change the query grammar. Values one remedy does NOT move:
the `?firm=` slug grammar, and the staff identity that is allowed to use it.

## (iv) STATE COHERENCE

Standing cases and the set each resolves to (generated values, registry as it stands):

- The mockadv alias: resolves to [mockadv, 49financial]. It is admitted on its own directory and on the 49financial
  directory, and refused on the other three directories. Under the old bucket comparison it was admitted on every
  directory of its bucket; the declared set replaces that inference.
- The opal-capital staff proxy with ?firm=bd: resolves to the union of the sets of the firms whose bucket is
  opal-data-bd, which is [49financial, mockadv]. With ?firm=inf it is [inflection], with ?firm=cot [cottonwood], with
  ?firm=demo [demo].
- A firm that shares a bucket with another: 49financial shares opal-data-bd with mockadv. Its set is [49financial]; the
  shared bucket grants it nothing extra. The old bucket comparison let it read the mockadv directory by accident. This is
  the one decision the remedy moves that the registry as it stands does not declare (see the residual below).

Dormancy, measured by `evidence/dormancy_grid.mjs` (base 576e574de4 built by git show into .scratch/base): router grid
(firmId x tenant directory x path x ?firm slug) 87 of 88 decisions identical to base; guard grid (firmId x tenant
directory x ?firm x served bucket) 393 of 396 identical. The residual is one pair, 49financial on
platinum/advi/mockadv/: base admitted it by the shared bucket (origin opal-data-portal-v2), the declared sets refuse it with
the 401 (router: one decision; guard: three served-bucket cases). Every other decision, and every decision on a
non-platinum path, is identical. A declaration of 49financial's read of the mockadv directory would restore base; it is a
widening of an entitlement the registry does not declare, so it is not made here. A ruling is owed before any cutover
(surprise row ADVI_FIRMBKTS-D1-W17-S5).

Values one remedy does NOT move: the bucket values of FIRM_CONFIG, the FIRM_BUCKET_MAP derivation, the origin bucket of
platinum/advi/ requests (still the canonical tier constant set on the router's tenant branch), the satellites branch,
the 401 "Firm scope mismatch" body and its rule name, and the guard's 502 body and its firm_isolation_guard event.

## Controls and the mutation that fails each (cell 1a.5)

Each control is a test in a NEW spec file per package (`tenant-grain.spec.mjs`). Each mutation below was applied to the
build by a named break, the new spec run alone, the failing arm count read, and the build restored byte for byte
(sha-256 compared). Router spec: 12 arms. Guard spec: 11 arms. Each row names the failing arms by their assertion.

- SHARED BUCKET. Mutation r_shared: the router's caller set replaced by the union of the declared sets of every firm
  sharing the caller's bucket (the bucket grain, declarations attached). Router spec: 1 of 12 fails, the refusal of one
  firm reading another firm's directory on the shared bucket. Mutation g_shared: the same replacement in the guard.
  Guard spec: 1 of 11 fails, the 502 on the cross-firm directory served from the canonical tier.
- ALIAS. Mutation r_alias: the alias's declared set reduced to its own directory (the declaration of the scope's
  directory dropped). Router spec: 2 of 12 fail (the shipped-handler admission on the declared directory, and the
  admission on the declared directory under the cutover double). Mutation g_alias: the same reduction in the guard.
  Guard spec: 2 of 11 fail (the same two arms). Mutation r_alias_inferred: the caller's set inferred from the names of the
  firms sharing its bucket, with no declaration. Router spec: 2 of 12 fail (the shared-bucket refusal, and the
  declared-directory admission under the cutover double). Mutation g_alias_inferred: the same inference in the guard.
  Guard spec: 2 of 11 fail (the 502 on the shared-bucket firm, and the declared-directory pass under the cutover double).
- STAFF PROXY. Mutation r_staff: the ?firm= set widened to every tenant directory. Router spec: 3 of 12 fail (exact
  admission against the bucket's declared set, refusal on another bucket's tenant, refusal of an unknown slug). Mutation
  g_staff: the same widening in the guard. Guard spec: 1 of 11 fails (the exact pass-or-trip arm).
- NO FIRM LITERALS is a commit-time gate, not a mutation control: `python .tools/naming-gate.py --diff .scratch/f7.diff
  --enforce` is run on the final diff and its verdict line is carried in the worker report.
