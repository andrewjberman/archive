# LGIC_ENFORCE.TO-EN-s-41-r9 -- percent-style-scope -- result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Branch:** `wk-lgic-enforce-9-2` | **Cut from CLOUD at** `a6476ef28f`

## Decision: WIDEN

The template rule is RUNTIME SUBSTITUTION; the brace is one syntax of it. `key.template_detection.rule` at v1.11
already names its object as "the producer's own runtime substitution field", and `silver/%s/` is that object in
another syntax (`SILVER_PREFIX_FMT` in both freshness probes, a format string by its own name).

## Population, counted before deciding

| corpus | denominator | %-style |
|---|---|---|
| `NAMING_CENSUS_REPORT.r8.md` rows fence (the census) | 3254 rows | 2 (`silver/%s/` x2, S3Key, repo) |
| `PLACEHOLDER_CAMPAIGN_R6.json` | 1370 rows | 2 (the same) |
| tracked `.py`, key-shaped literals, tier-prefixed (unscoped) | 6498 files | 44 literals in 33 files; 42 not census rows; 11 files first-party producers |

## The bound (NAMING_SCHEMA v1.12, `key.template_detection`)

`percent_field_regex` = `%(?:[(][A-Za-z_][A-Za-z0-9_]*[)][sd]|0[1-9][0-9]?d|s|d(?![0-9A-Fa-f]))`, searched after
`%%` pairs are removed. Four forms: `%s`; `%d` not before a hex digit; `%(name)s|%(name)d`; `%0Nd` (N 1-99).
`percent_field_excludes` names what stays out. The `scope` field states that it takes precedence over the brace-only `test`,
which is left byte-identical as EN-m-39's record.

## Negative arm (what WIDEN excludes)

3273 of 3273 ORDINARY: 3237 ordinary census rows, 16 exemplars (literal percent, URL bytes incl. the `%dc`
collision, `%5s %f %x %r %i`, strftime other than `%d`, `{}`, `$NAME`), and 20 genuine URL-encoded key-shaped
literals from tracked source. Positive control: 21 of 21 TEMPLATE. Repo: 44 of 44 tier-prefixed %-literals
selected. The broad printf predicate misreads 11 real literals (`a%20secret` as width-20 `%s`, `%5ESPX`); the bound
leaves all 11 ORDINARY.

## Criteria

| id | verdict | deciding line |
|---|---|---|
| S41R9-AC1 | PASS | `VERDICT: PASS-S41-DECISION` |
| S41R9-AC2 | PASS | `rows carrying a %-style field: 2`, own denominator 3254 |
| S41R9-AC3 | PASS | `negative arm: rejected 3273 of 3273 tested` |
| S41R9-AC4 | PASS | `NOT GRADED 8 of 8`, `ROUTED 7 of 7`, moved `[]` |
| S41R9-AC5 | JUDGMENT | for `3.0.0_SA_CVO` at L9 |

`grades_moved` 0: no code reads `key.template_detection`. The re-grade (2 rows) is a later round's cut. The W3-S17
disarm belongs to `2.0.0_SA_COO~G`; this cell supplies the evidence only.

Rows filed: `LGIC_ENFORCE-W2-S14` (face/instrument record-shape mismatch, OBSERVATION, INERT),
`LGIC_ENFORCE-W2-S15` (census admits 2 of 44 %-style key literals, OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~G`).

Commits: `0aebbac8a2` (schema, record, instrument, rows); the proof commit carries this file and the status flip.
