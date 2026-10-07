# OG-al-2 negative control

With the new `opal_data_refresh_status` row (and its comment lines) removed from `identity_tool_allowlist.txt`
(the tracked file was restored byte-for-byte afterwards), `tests/test_identity_scope_status_row.py` read:

```
tests\test_identity_scope_status_row.py::test_ogal2_ac01 FAILED          [ 25%]
tests\test_identity_scope_status_row.py::test_ogal2_ac02 PASSED          [ 50%]
tests\test_identity_scope_status_row.py::test_ogal2_ac03 PASSED          [ 75%]
tests\test_identity_scope_status_row.py::test_ogal2_ac04 PASSED          [100%]
FAILED tests\test_identity_scope_status_row.py::test_ogal2_ac01 - assert "ide...
========================= 1 failed, 3 passed in 0.13s =========================
```

`test_ogal2_ac01` fails without the row and passes with it (4 of 4 with it).

## AMENDMENT 2 negative control (send path returns UNKNOWN on a bad id)

With `_read_status_once` restored to its pre-amendment body (it raises IntegrationError on a bad id; the file was
put back to the amended bytes afterwards), `pytest tests/test_opal_portal_status_id_shape.py -k test_ogal2_ac05` read:

    E   app.integrations.base.IntegrationError: execution_id must be 1-200 letters, digits, - _ or :
    FAILED tests\test_opal_portal_status_id_shape.py::test_ogal2_ac05 - app.integ...
    1 failed, 1 deselected in 0.77s

With the amended function the same test passes (AC3: named tests passed 2 of 2).
