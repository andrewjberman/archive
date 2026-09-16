# LGIC_NAMING.TO-LN-e-1 -- namer A -- result

**Worker:** 0.9.0_WK_LGIC_NAMING~2 | **Branch:** wk-lgic-naming-1-2 | **Base:** 6a5b276f8b382edca90673d1f425320a251ca0e5 (HEAD before the first commit)

**Briefing read:** `org/standards/NAMING_SCHEMA.json` (v1.4), `infra/logic/05_IDENTITY_SPINE.md`, `N3_ITEMS.json`. Nothing else was read to name the items.

**Output:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-namer-a.tsv` -- 18 of 18 items named, 0 RAISE.

## Criteria (mechanical; graded by the checker's output)

| id | invocation | deciding output | rc |
|---|---|---|---|
| E1-AC1 | `timeout 120 python .../fixed_inputs/check_ln.py e1-named` | `ITEMS: 18  NAMED: 18  MISSING: []` / `VERDICT: PASS-ALL-NAMED` | 0 |
| E1-AC2 | `timeout 120 python .../fixed_inputs/check_ln.py e1-base` | `BASE: 6a5b276f8b382edca90673d1f425320a251ca0e5` / `VERDICT: PASS-BASE-RECORDED` | 0 |

## Places where Namer A chose between readings

The two briefing files do not close these, so each is filed as a row and none is answered RAISE:

- `LGIC_NAMING-W2-S1` -- the function / purpose slot is an open vocabulary (11 of 18 items turn on a chosen token).
- `LGIC_NAMING-W2-S2` -- i13 `{entity}` = `advisor` or `advisor_id` (wrote `advisor_id=A123`).
- `LGIC_NAMING-W2-S3` -- i14 all-firm scope under a product source = `global` or `mdpf` (wrote `global`).
- `LGIC_NAMING-W2-S4` -- i15 system for a vendor-named runner building a derived tier (wrote `orion`).

Whether the two namers agree is LN-e-3's measurement, not this worker's.
