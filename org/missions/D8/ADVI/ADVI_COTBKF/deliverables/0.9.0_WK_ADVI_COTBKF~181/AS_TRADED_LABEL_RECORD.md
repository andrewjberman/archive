# CB-cm-1: the as-traded Yahoo close reaches the served use_class label

- Base: 5 of 5 `test_as_traded_*` tests passed on the unmodified modules. Production change: none.
- Tests: `data/assets/scripts/silver/tests/test_commonwealth_as_traded_use_class.py` (new; no existing test edited).
- Existing valuation and fwd3 tests: 3 files, 40 passed, rc 0.
- Readers of the three modules: 14 lines in the list (12 PRICE, 2 FACT). Unlabelled PRICE readers: 0.
- Record: `AS_TRADED_LABEL_RECORD.json` in this folder.

Not in the reader list, each stated in the record's `not_established`:
- `read_sechist` (dv L164-195, called at L1085 under `--sechist`) labels its rows `sechist`. Origin not established. Filed as `ADVI_COTBKF-D1-W181-S1`.
- The fwd3 index read (L783) reads labels, not prices.
- The cache digest for the run pin (dv L598-612) reads no value.

Not measured: the live label vocabulary and whether any V2-held ticker is in the Yahoo cache today.
