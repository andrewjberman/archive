# LGIC_NAMING.TO-LN-e-2 -- namer B -- result

**Worker:** `0.9.0_WK_LGIC_NAMING~3` | **Branch:** `wk-lgic-naming-1-3` | **Base:** `6a5b276f8b382edca90673d1f425320a251ca0e5` (git rev-parse HEAD before the first commit) | **Cell:** `LN-e-2`

**Briefing read:** `org/standards/NAMING_SCHEMA.json` (v1.4), `infra/logic/05_IDENTITY_SPINE.md` (seed v0.1),
`.../2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json`. Not read: the PRD, the decomposition, `N3_KEY.json`, any other
exercise file, the other namer's order, and `check_ln.py`'s source. `check_ln.py` was only run.

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-namer-b.tsv`: 1 base line + 18 item lines,
LF endings, 18 tabs.

## Acceptance (verbatim outputs)

| id | invocation | output | verdict |
|---|---|---|---|
| E2-AC1 | `timeout 120 python .../fixed_inputs/check_ln.py e2-named` | `ITEMS: 18  NAMED: 18  MISSING: []` / `VERDICT: PASS-ALL-NAMED` rc=0 | PASS-by-output, 18 of 18 |
| E2-AC2 | `timeout 120 python .../fixed_inputs/check_ln.py e2-base` | `BASE: 6a5b276f8b382edca90673d1f425320a251ca0e5` / `VERDICT: PASS-BASE-RECORDED` rc=0 | PASS-by-output, 1 of 1 |

**Controls:** mutant 1 (remove the i18 line) gave `VERDICT: FAIL-UNNAMED` with `MISSING: ['i18']`. Mutant 2 (base set to 40 zeros)
gave `VERDICT: FAIL-NO-BASE`. The file was restored byte-identical. Both criteria produced the same output on two runs. The checker exits
rc=0 on FAIL as well, so its VERDICT line is the grade.

## The derivation rule applied to every item

- Resource: `{system}-{scope}-{function}[-{qualifier}]-{last}`. Scope SHORT, and omitted when the resource is shared. The last slot is the kind, or the cadence for EVENT_RULE/SCHEDULE.
- Function: the process noun the item names. If it names none, the item's main verb in base form. A tier word that the verb acts on is kept. Generic verbs and nouns are dropped, and the optional qualifier is omitted (row `LGIC_NAMING-W3-S2`).
- System: a product. The vendor is used only where the resource is the vendor integration (row `LGIC_NAMING-W3-S3`).
- Key: `{source}/{scope}/{tier}/{table}/{partition}`, scope LONG. A code key is `{source}/{scope}/code/{built_tier}/{file}`. A product-shared key takes the product as its scope (row `LGIC_NAMING-W3-S3`).
- Bucket: `opal-data-{scope}`, LONG.

## Items needing a row

- `i13` RAISE: `{entity}={id}` does not name which token fills `{entity}`. `advisor` and `advisor_id` both fit the item (row `LGIC_NAMING-W3-S1`).
- `i14`, `i11`, `i15`: scope and system slot choices, each resolved by a stated reading (row `LGIC_NAMING-W3-S3`).
- The 14 names that carry a function or purpose token (row `LGIC_NAMING-W3-S2`).

## Proof

`LGIC_NAMING.TO-LN-e-2.namer-b.proof_of_spec.json` beside this file, validated with
`python .tools/proof-of-spec-check.py <instance> E2-AC1,E2-AC2` before the `complete` flip.
