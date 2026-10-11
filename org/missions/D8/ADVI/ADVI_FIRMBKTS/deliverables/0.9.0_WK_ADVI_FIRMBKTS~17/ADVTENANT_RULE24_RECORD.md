# ADVI_FIRMBKTS FB-f-7 -- the advTenant entitlement schema, Rule-24 record

Cell FB-f-7 (round 3, enrichment item 1; PRD F6; LD-0442's carried row). Built DORMANT: nothing is deployed. The field
is `advTenant` in the generated `FIRM_CONFIG` (`infra/aws/lambda-edge/_shared/firm-config.mjs`, emitted by
`lib/opal_naming.py` `_blk_firm_config`). The denominators below are read from that generated block at HEAD of this commit.

## (i) MECE over a declared domain

Declared domain: the generated `FIRM_CONFIG` firmIds (the served tenants of `scopes.json`, pseudo tenants excluded).
Denominator: 5 firmIds in the domain; 5 tenant directories; each firmId carries exactly one `advTenant` set.

| firmId | bucket (configured) | advTenant (generated) | role |
|---|---|---|---|
| 49financial | opal-data-bd | [49financial] | scope's own tenant |
| inflection | opal-data-inf | [inflection] | scope's own tenant |
| cottonwood | opal-data-cot | [cottonwood] | scope's own tenant |
| mockadv | opal-data-bd | [49financial] | alias tenant, DECLARED to the scope's own directory |
| demo | opal-data-demo | [demo] | scope's own tenant |

Subtraction over the domain: every tenant directory of the domain has at least one reader (uncovered directories: 0 of 5).
The cover is complete and NOT disjoint: one directory (49financial) has two declared readers, because the alias is declared
to it. The overlap is the declaration itself, never an inference from a shared bucket. Values one remedy does NOT move:
the five firmId keys, the five bucket values (no bucket is edited by this cell), the displayName values, and the
`platinum/advi/` path class with its 401 body and rule name.

## (ii) SAME GRAIN

The entitlement is at tenant-directory grain: the unit compared is the `{tenant}` segment of `platinum/advi/{tenant}/`
against the caller's `advTenant` set. The bucket is a storage grain and is no longer compared on this path class. Both
the router and the guard read the same field at the same grain, and the guard derives its membership independently from
the same generated config. Values one remedy does NOT move: the directory name strings themselves, the origin choice
(platinum tier constant), and the bucket grain on every non-platinum path (gold, views, satellites), which keeps its
bucket comparison unchanged in both functions.

## (iii) INTENT COHERENCE

One axis, one intent: `advTenant` answers one question, which tenant directories an identity may read. A declared alias
is an entitlement, not a bucket accident. Residual, declared not hidden: the opal-capital staff proxy names a BUCKET slug
(`?firm=<slug>` -> `opal-data-<slug>`), so its set is derived by grouping firmIds on the bucket field. That is a second
axis that a later cell may replace with a tenant-named proxy; this cell does not change the query grammar. Values one
remedy does NOT move: the `?firm=` slug grammar, and the staff identity that is allowed to use it.

## (iv) STATE COHERENCE

Standing cases and the set each resolves to (generated values, registry at HEAD):

- The mockadv alias: resolves to [49financial]. It is admitted on the 49financial directory and refused on every other
  directory, its own included. Under the old bucket comparison it was also admitted on its own directory (both firms
  share opal-data-bd); that is the one decision this remedy moves for a declared pair (see the exception below).
- The opal-capital staff proxy with ?firm=bd: resolves to the union of the sets of the firms whose bucket is opal-data-bd,
  which is [49financial]. With ?firm=inf it is [inflection], with ?firm=cot [cottonwood], with ?firm=demo [demo].
- A firm that shares a bucket with another: 49financial shares opal-data-bd with mockadv. Its set is [49financial]; the
  shared bucket grants it nothing extra. The old bucket comparison let it read the mockadv directory by accident.

Dormancy, measured: over the router grid (firmId x tenant directory x path x ?firm slug) 85 of 88 decisions are identical
to HEAD. The 3 that differ are all on platinum/advi/mockadv/: 49financial, mockadv, and opal-capital with ?firm=bd. The
guard grid shows the same three pairs (each across the served buckets). Every other decision, and every decision on a
non-platinum path, is identical. The exception is the declared alias's own directory: the spec's ALIAS control requires
refusal on every other tenant directory, and the staff proxy follows the declared sets. A later ruling may keep the
mockadv directory readable for the staff proxy; this record states the present behaviour and does not hide it.

Values one remedy does NOT move: the bucket values of FIRM_CONFIG, the FIRM_BUCKET_MAP derivation, the origin bucket of
platinum/advi/ requests (still the canonical tier constant set on the router's tenant branch), the satellites branch,
the 401 "Firm scope mismatch" body and its rule name, and the guard's 502 body and its firm_isolation_guard event.

## Controls and the mutation that fails each (cell 1a.5)

Each control is a test in a NEW spec file per package (`tenant-grain.spec.mjs`). Each mutation below was applied to the
build, the spec run, the arm count read, and the build restored byte for byte:

- SHARED BUCKET. Mutation router-shared: the router's entitlement test replaced by bucket equality (FIRM_BUCKET_MAP of the
  path tenant equals the caller's bucket, the base rule). Router spec: 4 of 12 fail, including the refusal of one firm
  reading another firm's directory on the shared bucket. Mutation guard-shared: the guard's platinum branch replaced by the
  base bucket comparison. Guard spec: 5 of 10 fail, including the 502 on the cross-firm directory.
- ALIAS. Mutation router-alias: the caller's set inferred from the firms that share its bucket, with no declaration. Router
  spec: 3 of 12 fail (admission on the declared directory under the cutover double, refusal on every other directory, and
  the shared-bucket refusal). Mutation guard-alias: the same inference in the guard. Guard spec: 4 of 10 fail.
- STAFF PROXY. Mutation router-staff: the ?firm= set widened to every tenant directory. Router spec: 3 of 12 fail (exact
  admission, refusal on another bucket's tenant, refusal of an unknown slug). Mutation guard-staff: the same widening in the
  guard. Guard spec: 1 of 10 fails (the exact pass-or-trip arm).
- NO FIRM LITERALS is a commit-time gate, not a mutation control: `python .tools/naming-gate.py --diff .scratch/f7.diff
  --enforce` reads NAMING-GATE: PASS on the final diff.
