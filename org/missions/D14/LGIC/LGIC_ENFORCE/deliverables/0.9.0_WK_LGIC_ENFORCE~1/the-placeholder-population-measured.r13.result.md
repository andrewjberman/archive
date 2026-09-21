# the-placeholder-population-measured.r13.result -- LGIC_ENFORCE.TO-EN-p-37-r13

Worker `0.9.0_WK_LGIC_ENFORCE~1`, worktree `wk-lgic-enforce-13-1`, branch `wk-lgic-enforce-13-1`.

## What ran

1. `selftest-arms` -- `PASS-ARMS-DISCRIMINATE`, 27 arms (11 POSITIVE-SATISFIABILITY, 16 mutant/other),
   run BEFORE any write. No arm found unsatisfiable by a correct record; no BLOCKING row owed on this
   axis.
2. Extracted the `not_judged` list (462 entries, owner cards) from the round-8 census report's own
   fenced json (`NAMING_CENSUS_REPORT.r8.md`) and wrote it to `NOT_JUDGED_R13.json`, this cell's own
   deliverables folder -- reused rather than re-derived, since the owner-resolution research those cards
   carry (which token has no declared source / would touch a generated policy) has not gone stale between
   round 8 and this cut.
3. Ran the REAL live census: `python lib/opal_naming.py census --live --repo --budget 600 --not-judged
   .../NOT_JUDGED_R13.json --report .../NAMING_CENSUS_REPORT.r13.md`. rc=0, `CENSUS: COMPLETE 3264
   judged + 463 carded (live 1711+131 of 1842 nameable, repo 1553+332 of 1885)`; both planes `stopped:
   null`. Registry@`9f4a569d7a54b53c` over all 6 registry file(s); estate vintage `Built from the estate
   as of 2026-09-19 05:56:38 UTC ... manifest: e6c4aee2deef`.
4. Parsed the fresh report's fenced json `rows` list (3264 items) and measured, over the `canonical`
   field only (R-38's own scope -- "rows whose `canonical` holds a literal placeholder brace", not
   `current`): **1303 of 3264** rows match `\{[a-z_]+\}`. Cross-checked: 15 judged rows carry a
   placeholder-shaped brace in `current` too (pre-existing template variables such as `{snap}`), proving
   the population must be read off `canonical` specifically or the two classes would be conflated.
5. Built `PLACEHOLDER_POPULATION_TABLE_R13.md` -- one markdown table row per judged item (`current`
   escaped `{`/`}` -> `(`/`)` so only the `canonical` cell carries live brace bytes, `canonical` verbatim,
   verdict/type/plane/where), 3264 data lines, header and separator lines deliberately NOT starting with
   `|` so the arm's own row filter (`ln.startswith("|")`) counts data rows only. This is `population.
   report_path`, the artifact `check_en_r13.py`'s `count_report()` re-counts.
6. Verified the arm's own instrument directly (not merely inferred): called `check_en_r13.count_report()`
   against (a) the standard `NAMING_CENSUS_REPORT.r13.md` -- returns `rows=50, with_ph=0` (the SUMMARY
   "Totals by type" table only, exactly the trap the order's own probe named for round 8's report), and
   (b) `PLACEHOLDER_POPULATION_TABLE_R13.md` -- returns `rows=3264, with_ph=1303, 9 distinct tokens`,
   matching my own hand count exactly.
7. Traced each of the 9 distinct tokens to a producer by READING source, not inferring from the token's
   name: `{system}` (lib/opal_naming.py:1187, `_slots()`), `{scope}` (:1489 and :1507, `_grade_key()`),
   `{cadence}` (:1229, `_cadence_slot()`), `{source}` (:1487, `_grade_key()`) are the naming grader's OWN
   substitution-slot synthesis, each the ONLY code site in the file that assigns that literal string
   (corroborated per-token with `comp-find '"{token}"' lib/opal_naming.py`, separating executable
   assignment lines from comment/docstring mentions of the same string). `{snap}`, `{dim_name}`,
   `{firm}`, `{d}`, `{dc}` are a DIFFERENT producer class: literal `str.format()`-style template
   variables already present in the OBSERVED name, written by 4 application source files (5 sites, each
   read directly) and never touched by `_grade_key()`'s tail-passthrough (:1476/:1491) -- proven by 5
   rows verdict CONFORMANT with `current == canonical` while a `{dim_name}` brace still stands in both,
   which is only possible if grade() never emitted that brace itself.
8. Answered the cause question as a measurement: **SEVERAL**, on two kinds of evidence -- (i) two
   structurally different producer classes exist (grader-synthesis vs pre-existing source-code template
   text), proven above by direct code reads, not inference; (ii) the classes do not always co-occur (5 of
   15 class-B rows carry NO class-A token), so class B is not a byproduct of class A firing; (iii) even
   within class A, the four slots are gated on independent vocabulary lookups. `UNDETERMINED` was
   considered and rejected as the honest answer here because the evidence discriminates cleanly, not
   because a decisive-sounding verdict was wanted.
9. Delta against the inherited figure: inherited 1411 of 3237 (round-4 census, `LGIC_ENFORCE-W2-S13`,
   `0.9.0_WK_LGIC_ENFORCE~2`, 2026-09-17T18:30Z, registry@4f192e91bd64ee70) vs now 1303 of 3264 (this
   cell, 2026-09-19T07:33:40Z, registry@9f4a569d7a54b53c). Direction: **SHRANK**. Both vintages named in
   the record; the round-6 placeholder campaign's own disarm evidence (`LGIC_ENFORCE-S64`) accounts for
   part of the drop (41 of 1411 minted/resolved by round 6), the remainder is population drift across
   rounds 5-12 (live nodes and repo names both changed net between vintages, per each report's own
   `denominators` block).
10. `no_repair`: `git log --format="%h %an %s" 44fc14c183..HEAD -- infra/logic/registry/
    lib/opal_naming.py` returns EMPTY -- 0 commits by this cell (or anyone) touch either NO-REPAIR path
    since the cut. Neither file was edited this round.
11. `fixed_inputs_at_pin`: both `check_en_r13.py` and `R13_BASE.json` resolve to
    `c2865743ed47c79f26ad3565bac6d66aa34c43da` (`git log -1 --format=%H -- <path>`, both files, same
    commit -- the L6 issuance itself).
12. `stale_proofs`: `git log 44fc14c183..HEAD -- <fixed_inputs/r13 dir>` returns exactly 1 commit
    (`c2865743ed`, the L6 issuance that created the fixed inputs). `proofs_at_risk()` over that commit's
    PARENT lists 0 round-13-shaped `proof_of_spec.json` files under the project root (none existed before
    the issuance -- this is the first and only cell of round 13). `proofs_re_run: []` matches the empty
    at-risk set exactly.

## Final arms (real run, not selftest)

```
PASS-P37-POPULATION        report rows re-counted: 3264 ; with placeholder, re-counted: 1303 ; record claims 1303 of 3264
PASS-P37-TOKENS            distinct tokens re-counted: 9 ; record names 9 (distinct=9)
PASS-P37-PRODUCERS         producers named: 5 (record states 5) ; tokens attributed: 9 ; unattributed: 0 ; silent: 0
PASS-P37-CAUSE             verdict: SEVERAL ; evidence length: 1505
PASS-P37-NO-REPAIR         registry/builder commits since the cut: 0 by this cell, 0 elsewhere
PASS-R13-VINTAGE-FIELD     fixed inputs named at pin: 2 ['R13_BASE.json', 'check_en_r13.py'] ; each commit resolvable: True
PASS-R13-STALE-PROOFS      fixed-input commits since the cut: 1 (informational) ; proofs at risk: 0 ; record enumerates: 0
```

## Files written (this cell's deliverables folder only, per BOUNDS)

- `NOT_JUDGED_R13.json` -- the 462-card not-judged input, extracted from round 8's own report.
- `NAMING_CENSUS_REPORT.r13.md` -- the real live+repo census run, this cell's write time.
- `PLACEHOLDER_POPULATION_TABLE_R13.md` -- the arm-readable per-row table, `population.report_path`.
- `PLACEHOLDER_POPULATION_R13.json` -- the record, per `R13_BASE.json`'s `record_shape`.

## What this cell explicitly did NOT do

No registry or `lib/opal_naming.py` edit; no mint, no card written to `infra/logic/registry/`; no
remedy proposed for a single row. The cause question is answered as a measurement, not resolved into one
recommended fix. `NAMING_SCHEMA.json` was read, never edited.

## AC8 (judgment, for `3.0.0_SA_CVO`)

Not self-graded. Material for that read: the census's own `stopped: null` on both planes (no early
stop, the RAISE population was carded not skipped-past), the registry vintage printed with the report,
and the per-token producer citations above, each naming the exact file:line read and the instrument
(`comp-find` count + direct Read) used to attribute it -- not an inference from the token's name alone.
