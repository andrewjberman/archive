# ADVI_FIRMBKTS FB-f-7 -- the advTenant entitlement schema, Rule-24 record

Cell FB-f-7 (round 3, enrichment item 1; PRD F6; LD-0442's carried row). Built DORMANT: nothing is deployed. The field
is `advTenant` in the generated `FIRM_CONFIG` (`infra/aws/lambda-edge/_shared/firm-config.mjs`, emitted by
`lib/opal_naming.py` `_blk_firm_config` through `_adv_tenant`). The denominators below are read from that generated block
at the commit that carries this record. The entitlement unit is one scope's EQUIVALENCE CLASS: the scope's own tenant and
each alias tenant of that scope, every member listing every member (the PRD's tenant-assertion contract resolves the
path's firm segment "aliases included, to one firm").

## (i) MECE over a declared domain

Declared domain: the generated `FIRM_CONFIG` firmIds (the served tenants of `scopes.json`, pseudo tenants excluded).
Denominator: 5 firmIds in the domain; 5 tenant directories; 7 (firmId, tenant directory) entitlement pairs.

| firmId | bucket (configured) | advTenant (generated) | role |
|---|---|---|---|
| 49financial | opal-data-bd | [49financial, mockadv] | scope's own tenant; class of scope 49financial |
| inflection | opal-data-inf | [inflection] | scope's own tenant; no alias |
| cottonwood | opal-data-cot | [cottonwood] | scope's own tenant; no alias |
| mockadv | opal-data-bd | [49financial, mockadv] | alias tenant; the same class as its scope |
| demo | opal-data-demo | [demo] | scope's own tenant; no alias |

Subtraction over the domain: every tenant directory of the domain has at least one reader (uncovered directories: 0 of 5).
The cover is complete and NOT disjoint by design: the two directories of the 49financial class (49financial and mockadv)
each have two declared readers, both members of the class. The overlap is the declaration itself, never an inference from
a shared bucket. Values one remedy does NOT move: the five firmId keys, the five bucket values (no bucket is edited by this
cell), the displayName values, and the `platinum/advi/` path class with its 401 body and rule name.

## (ii) SAME GRAIN

The entitlement is at tenant-directory grain: the unit compared is the `{tenant}` segment of `platinum/advi/{tenant}/`
against the caller's `advTenant` set. The bucket is a storage grain and is no longer compared on this path class. Both
the router and the guard read the same field at the same grain, and the guard derives its membership independently from
the same generated config. Values one remedy does NOT move: the directory name strings themselves, the origin choice
(platinum tier constant, set after the assertion as at base), and the bucket grain on every non-platinum path (gold,
views, satellites), which keeps its bucket comparison unchanged in both functions.

## (iii) INTENT COHERENCE

One axis, one intent: `advTenant` answers one question, which tenant directories an identity may read. A scope and its
aliases are one class by declaration: any member reads every directory of the class, and no class is inferred from a
shared bucket. Residual, declared not hidden: the opal-capital staff proxy names a BUCKET slug (`?firm=<slug>` ->
`opal-data-<slug>`), so its set is derived by grouping firmIds on the bucket field. That is a second axis that a later
cell may replace with a tenant-named proxy; this cell does not change the query grammar. Values one remedy does NOT move:
the `?firm=` slug grammar, and the staff identity that is allowed to use it.

## (iv) STATE COHERENCE

Standing cases and the set each resolves to (generated values, registry as it stands):

- The mockadv alias: resolves to [49financial, mockadv]. It is admitted on its own directory and on the 49financial
  directory, and refused on the other three directories. Under the old bucket comparison it was admitted on every
  directory of its bucket; the declared class replaces that inference with a declaration that yields the same set.
- The opal-capital staff proxy with ?firm=bd: resolves to the union of the sets of the firms whose bucket is
  opal-data-bd, which is [49financial, mockadv]. With ?firm=inf it is [inflection], with ?firm=cot [cottonwood], with
  ?firm=demo [demo].
- A firm that shares a bucket with another: 49financial shares opal-data-bd with mockadv. Its set is the class,
  [49financial, mockadv], and the reason is the declaration, not the shared bucket: the mockadv directory is admitted
  because it is in the declared class.

Dormancy, measured by `evidence/dormancy_grid.mjs` (base 576e574de4 built by git show into .scratch/base): router grid
(firmId x tenant directory x path x ?firm slug) 88 of 88 decisions identical to base; guard grid (firmId x tenant
directory x ?firm x served bucket) 396 of 396 identical; DORMANCY: router differing 0, guard differing 0. The class
reproduces exactly today's boundary: no firm reads a directory outside its bucket's class, and every decision that base
admitted by the shared bucket is now admitted by declaration. An earlier build that listed the alias alone (the
single-entry alias set) left one decision, 49financial on the mockadv directory, differing from base; the class closes it
and is the issuer's ruling for row ADVI_FIRMBKTS-D1-W17-S5.

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
- ALIAS (one equivalence class, the cutover double with the scope's own tenant in its own bucket). Mutation r_alias: every
  member's set reduced to its own directory (the class declaration dropped). Router spec: 2 of 12 fail (the shipped-handler
  admission of each member on each class directory, and the admission of the alias on the scope's directory under the
  cutover double). Mutation g_alias: the same reduction in the guard. Guard spec: 2 of 11 fail (the same two arms). Mutation
  r_alias_inferred: the caller's set inferred from the names of the firms sharing its bucket, with no declaration. Router
  spec: 2 of 12 fail (the shared-bucket refusal, and the alias's admission on the scope's directory under the cutover double).
  Mutation g_alias_inferred: the same inference in the guard. Guard spec: 2 of 11 fail (the 502 on the shared-bucket firm,
  and the alias's pass on the scope's directory under the cutover double).
- STAFF PROXY. Mutation r_staff: the ?firm= set widened to every tenant directory. Router spec: 3 of 12 fail (exact
  admission against the bucket's declared set, refusal on another bucket's tenant, refusal of an unknown slug). Mutation
  g_staff: the same widening in the guard. Guard spec: 1 of 11 fails (the exact pass-or-trip arm).
- NO FIRM LITERALS is a commit-time gate, not a mutation control: `python .tools/naming-gate.py --diff .scratch/f7.diff
  --enforce` is run on the final diff and its verdict line is carried in the worker report.
