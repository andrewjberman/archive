# OG-q-8 negative control (0.9.0_WK_NFRA_OPLGTW~22)

Old line restored in `infra/aws/ec2/opal-gateway/app/integrations/schwab/integration.py`
(`position_cusips = frozenset(row[0] for row in pos_rows)`, bytes from `git show HEAD:`), then
`python -m pytest tests/test_schwab_q8_blank_cusip.py -q` from `infra/aws/ec2/opal-gateway`:

    FAILED test_ogq8_ac01  -- AssertionError: ['', 'SYN000001']; assert [''] == []   (query admits the blank-cusip dim_asset row)
    FAILED test_ogq8_ac02  -- AssertionError: ['', 'SYN000001']; assert [''] == []   (download admits it too)
    FAILED test_ogq8_ac03  -- internal_error:TypeError (None in the held set)
    FAILED test_ogq8_ac04  -- internal_error:TypeError instead of asset_read_denied_unqualified
    4 failed

ac01 and ac02 fail as the order requires. ac03 and ac04 also fail on the old line. The fix was then restored
(4 passed).
