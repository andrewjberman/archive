# METHOD_ROW_RULE24 -- the method rows of `dim_return_method` (IRPT_DASHBD TO-DB-b-102)

Schema adopted: the set of method rows `account_return_daily.py` METHOD_ROWS can write, keyed by `method_version`, plus the literal
`absent` for a source whose entry names none. Authored by 0.9.0_WK_IRPT_DASHBD~77 under ADDENDUM 13.2 (msg 3501).

## (i) MECE over a declared domain

Domain: the valuation class of a custody source's returns value V_t, as the source entry declares it in `valuation_source`.
Members and the row each maps to:

| class of the entry | row | rule |
|---|---|---|
| `valuation_source` = `custodian_reported` | 2 | custodian whole-account equity (batch 193) |
| `valuation_source` declared, anything else (positions-based) | 3 | value rebuilt from positions at the entry's `price_basis` |
| no `method_version` in the entry (any class) | `absent` | no row is claimed |

Subtraction from the printed denominator: the declaration holds 1 source entry (1 of 1 carries `method_version: 2`, class
`custodian_reported`); every entry falls in exactly one class by the producer's test (`method_version_of`), and a name that crosses
class (a positions-based entry naming 2, or a custodian entry naming 3) is refused rather than written, so no entry sits in two rows.
Scope of the census: this order read `method_version` in the producer module, `sources.json` and the `tests/` folder only (a sibling
producer, `account_class_daily.py`, also carries a `method_version` column and was not changed or censused here); the one custodian
entry is the only entry at this base. Cottonwood declares no entry here, so the row-3 population at this base is 0 of 1.

## (ii) Same grain

One row per method definition, one grain: the method of computing V_t for a whole source. Fee and price detail stay in the entry's
own `fee_treatment` and `price_basis` fields (ADDENDUM 13.1), not in the row, so the row does not restate a second axis.

## (iii) Intent coherence

One axis: which method produced the value. `absent` is the claim-carrying value for "this entry never said" (A_VALUE_MUST_CARRY_ITS_CLAIM),
so a consumer can reject on it; 2 is never the stand-in for it.

## (iv) State coherence

Naming a row does NOT move: the entry's `valuation_source`, `fee_treatment`, `price_basis` (separate fields), the flow convention and
the income basis. Row 3's dimension row inherits `flow_convention`, `income_basis` and `day_count` from the shared writer, which were
measured for the custodian channel only; a positions-based channel whose income or flow treatment differs needs its own measured
definition and, until then, those inherited fields are NOT claimed as measured for row 3. Remedy that moves only the row: adding a key
to METHOD_ROWS. Remedy that moves only the entry: setting its `method_version`.

## Word-boundary token census

Token `method_version` over the producer module and its tests, before and after this order: before, 4 producer sites (row frame,
manifest, dimension row, dimension address) all writing the constant; after, the three writing sites read the entry through
`method_version_of`, and the constant remains only as row 2's number and the legacy `src=None` dimension writer.
