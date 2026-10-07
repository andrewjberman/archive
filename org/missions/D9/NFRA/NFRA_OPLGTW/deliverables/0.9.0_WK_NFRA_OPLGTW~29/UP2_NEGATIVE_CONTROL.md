# OG-up-2 negative control

With the signature restored to (name, size) only (and the hash-readable guard removed), run from
infra/aws/ec2/opal-gateway: `python -m pytest tests/test_opal_portal_dedupe_content.py -q`

    FAILED tests\test_opal_portal_dedupe_content.py::test_ogup2_ac01 - assert True is False
    FAILED tests\test_opal_portal_dedupe_content.py::test_ogup2_ac03 - assert True is False
    2 failed, 2 passed

test_ogup2_ac01 fails as the order requires (a corrected re-pull of equal size was dropped as already_triggered).
The code was then restored; up2.AC1 re-run: 4 of 4 PASS.
