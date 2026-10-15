# USE_CLASS_READ_RECORD (ADVI_COTBKF CB-ci-1, round 87)

The JSON beside this file is the machine record; its keys are the order's item 5 list.

- Module: `data/assets/scripts/silver/commonwealth_price_need.py` at HEAD blob 23fb24d68f39034537f5dc41788f96cc0fd177dc (commit 4ee1575acf).
- Change: a security in the active set V2 whose index `use_class` is `NOT_FOR_ACTIVE` stays uncovered. Outside the active set the rule is unchanged. A failed `use_class` read fails closed.
- Active set: 3368 distinct CUSIPs read from the pinned working-tree file (sha256 matches the pin). Account keys are not read into any value.
- Real index today: no `use_class` column (10 columns, footer read only). The NO_COLUMN branch is the live state, so every active-set security reads `NOT_FOR_ACTIVE` and stays uncovered until MDPF_DEMQUE lands the column.
- Tests: 5 new `use_class` tests; the 11 existing tests are unchanged (test-file diff: 66 added, 0 removed).
