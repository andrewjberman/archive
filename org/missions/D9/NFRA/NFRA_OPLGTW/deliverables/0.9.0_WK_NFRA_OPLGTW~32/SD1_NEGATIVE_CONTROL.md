# SD1 negative control

With "generated_at" removed from the candidate tuple in _manifest_date (all else unchanged), run from
infra/aws/ec2/opal-gateway: `python -m pytest tests/test_opal_portal_status_displayed_date.py -q -p no:cacheprovider -k ac01`

Result: `FAILED test_ogsd1_ac01 - AssertionError: assert None == '2026-10-07T03:41:12Z'` ; `1 failed, 2 deselected`.

The key was then restored; with it, the three tests pass (3 passed).

Neighbouring files, each in its own process, with the change in place:
- tests/test_opal_portal_send_split.py: 5 passed
- tests/test_opal_portal_status_id_shape.py: 2 passed
- tests/test_opal_portal_dedupe_content.py: 4 passed
