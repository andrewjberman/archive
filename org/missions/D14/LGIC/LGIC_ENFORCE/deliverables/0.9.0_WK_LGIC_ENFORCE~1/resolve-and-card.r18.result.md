# resolve-and-card.r18.result -- LGIC_ENFORCE.TO-EN-t-1-r18 (EN-t-1), 0.9.0_WK_LGIC_ENFORCE~1

**Built at commit `659dca28f3` (the record), worktree `wk-lgic-enforce-18-1`, base `021d1947bb` (cut from
round-18 issuance, `1.0.0_SA_CTO`'s ruling `4a5b0cafa8`, on `W2-S13`).**

## The cell

`R-38`'s SECOND half over `EN-t-1`: resolve the measured rows of the re-derived 1303-row placeholder
population, card the rest, print `resolved + carded == population`. Not re-opening round 13; the
population is re-derived at THIS cut's own write time, never treated as an inherited constant.

## The pin, and how the population was re-derived

Source declared: `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r13.md`
-- its ONE fenced JSON object's `rows[]`, read directly (never the retired `count_report()` / rendered
table, which round 14 escaped and round 15 retired for it). `judged_rows = len(rows) = 3264`. Population =
every `row_index` whose RAW `canonical` field carries a literal `{token}` (regex `\{([a-z_]+)\}`): **1303**.
**NO DRIFT against the inherited 1303** -- this cut's own re-derivation reproduces the round-13 number
exactly (3264 judged, 1303 carrying a token).

**The population is a multiset, keyed by `row_index`.** Measured directly from the census: 1303 rows, 630
distinct `current` names, 1200 distinct whole rows -- consistent with the order's own warning that this
round's checker shipped a name-keyed defect for one revision, caught by its own self-test disagreeing with
an independent read. Every row in the record carries its `row_index`.

**Tokens carried: nine, not three.** `{system}` 1119, `{scope}` 122, `{cadence}` 108, `{source}` 85,
`{snap}` 7, `{dim_name}` 5, `{firm}` 1, `{d}` 1, `{dc}` 1 (token-instances; a row may carry more than one,
so these do not sum to 1303). `R-38` names only `{system}`/`{scope}`/`{cadence}`; the six unnamed tokens
are not silently dropped -- they land in `CARDED` with the same reasoning as the rest, because `CARDED` is
`POPULATION MINUS RESOLVED`, a subtraction over the re-derived population, never a token-list domain.

## The disposition: 0 RESOLVED, 1303 CARDED

**What a RESOLVED row requires:** the substitution MEASURED FROM A DECLARED SOURCE, named in
`measured_from`. `infra/logic/registry/resources.json` is the ONE registry file (of the six under
`infra/logic/registry/`: `systems.json`, `resources.json`, `scopes.json`, `tiers.json`, `exemptions.json`,
`remediations.json`) keyed by exact resource identity -- `(name, type)` -- the same key `grade()`'s own
registry lookup reads (`lib/opal_naming.py` `_slots`, `v.resources.get((nm, typ))`, confirmed by reading
the function directly, not assumed from its `_about`). It carries 91 rows.

**Joined all 1303 population rows against resources.json's 91 rows by exact `(current, type)`: 0 matches.**
One row (index 2833, `current='cot-rebalancer-runner'`, census `type='EC2_INSTANCE'`) matches resources.json
by NAME ONLY -- the registry's row for that name is `type='LAMBDA'` (its `evidence` field cites
`infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf` and the sibling `cot-rebalancer-runner-role`,
already `system=mdpf`). The type disagreement means this is not the key `grade()`'s own lookup would hit
for THIS census entry, so it is **CARDED**, not asserted RESOLVED on a name coincidence -- per the order's
own bar, "a row wrongly marked RESOLVED is worse -- it asserts a measurement that was never taken."

The other five registry files carry no per-resource `(name, type)` index at all (`systems.json` lists
system KEYS a `{system}` slot may take, not which resource takes which; `scopes.json`/`tiers.json` are
tenancy/home rules; `exemptions.json`/`remediations.json` are fence-exemption and remediation-project rows).
None of them can be joined against an arbitrary resource name without guessing, which the order forbids.

**So the population's own registry coverage is the measured fact this record reports: 0 of 1303 rows have
a declared source that names their substitution.** Every row is CARDED, `owner: "1.0.0_SA_CTO"` (the
registry's own ruling authority -- `resources.json`'s `_about` cites `1.0.0_SA_CTO` ruling 97177 as the
authority that admitted its 91 rows), each with a reason grounded in this measurement: the type-mismatch
reason for row 2833, and for the other 1302 a reason naming the six registries checked and that resolving
each would require the same per-resource Terraform-citation investigation `resources.json`'s own 91 rows
demonstrate (30 of them, for example, cited in `RESOURCE_ROWS.md` from `EN-r-4`), which this round's scope
is dispositioning the population against a declared source, not conducting fresh per-resource research
(BOUNDS: "Repair nothing in the registry or the builders").

**An entirely-CARDED record is the outcome the order and its fixed input both name, in terms, as a valid,
non-failure disposition of R-38** ("carding is a disposition R-38 asks for by name, not a failure ... a
correct record may be entirely CARDED").

## Mechanical result

`T1R18-AC1` PASS (`t1-resolution`), `T1R18-AC2` PASS (`r18-vintage-field`, 2/2 fixed inputs named and
resolvable at `021d1947bb`), `T1R18-AC3` PASS (`r18-stale-proofs`, guard-shaped: 1 commit since `cut_pin`
`d180c2077f` touching the watched `fixed_inputs/r18` path -- the round-18 mint itself, `021d1947bb` --
0 proofs at risk at that commit's parent, 0 named re-run, set equality holds). `T1R18-AC4` recorded for
`3.0.0_SA_CVO` at L9 with the bytes cited in the proof-of-spec instance, not asserted here.

## Controls

**Mutant (FIRED-AS-EXPECTED), run against the committed record and the REAL `t1-resolution` arm, restored
byte-identical (`diff` clean, `git status --porcelain` clean against the committed blob):** the last row
(`row_index` 3258) dropped from `rows[]`, `carded` decremented to 1302 to keep the disposition arithmetic
self-consistent, `population` left at 1303 -- `FAIL-T1-RESOLUTION`, naming `NOT DISPOSITIONED (1 in the
population, absent from the record): [3258]`. Set equality on `row_index` caught the omission even though
the row-count arithmetic (1302 rows, 0+1302) closed on its own.

**Determinism (STABLE):** `t1-resolution`, `r18-vintage-field` and `r18-stale-proofs` run twice in sequence
against the restored, committed record -- `cmp` reports the two capture files IDENTICAL, 3 `VERDICT:` lines
each run, same verdicts and `rc=0` both times.

## The cut-time bar, checked

"Can a CORRECT artifact FROM THIS CELL ALONE satisfy this criterion?" For AC1-AC3: yes, demonstrated by
this run -- a record built from an honest re-derivation and an honest registry join passes cleanly. For
AC4: explicitly routed to L9 and carries no verdict from this cell, which is the criterion's own design.
No cut-time-unsatisfiable criterion was found in this cell; none filed.

## What this cell does and does not move

Repairs nothing in the registry or the builders (round 13's `no_repair` stands; dispositioning the
population, not changing what the estate emits, is this round's owed half). Does not touch
`NAMING_CENSUS_REPORT.r13.md` or `check_en_r13.py` -- read-only, not one byte. Does not touch
`LGIC_CANON-W3-S2` -- another project's routed defect, not this cell's.
