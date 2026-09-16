# naming-compare -- LGIC_CANON round 1, cell CN-n-3 (0.9.0_WK_LGIC_CANON~7)

Compared: `naming-a.tsv` @69f406a696 (worker A) and `naming-b.tsv` @885831971e (worker B), both `# base f95470f384`,
against `2.0.0_SA_COO~G/fixed_inputs/r1/CN_NAMING_KEY.json` @4058a56606, slot-aware, with the refused tokens of
`org/standards/NAMING_SCHEMA.json` @2f554182b6 (`bd`, `mockadv`) and the forms of `infra/logic/registry/scopes.json`
@a925c8a642 row `49financial` (long `49financial`, short `49f`, bucket `opal-data-49financial`). 6 of 6 items; both
answers equal the canonical value on every item, with the LONG form in every bucket and key scope slot and the SHORT
form in every resource scope slot, and no refused token in any slot. n6 (the refused-token trap) reads
`blackdiamond-49f-session-runner-role` in both: vendor `blackdiamond` in the system slot, `49f` in the scope slot.

ITEM n1: PASS
ITEM n2: PASS
ITEM n3: PASS
ITEM n4: PASS
ITEM n5: PASS
ITEM n6: PASS
