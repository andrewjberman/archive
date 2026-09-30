# Session log -- 0.9.0_WK_AMGT_RESAPP~171 on AMGT-ww-2

Built `_classification_for_ticker` and `_join_classification` in lib/research/api/scoped_amgt.py; 7 tests in lib/research/api/tests/test_list_rows_classification.py.
AC1 PASS (2 live rows read). AC2 FAIL as an instrument absence: with infra/logic in the cone (issuer ruling), api-suite.sh reads 287 passed, 5 failed, 23 errors, all FileNotFoundError on
infra/aws/terraform/harvest and portal/ fixtures outside the cone. Rows Z-W171-S1 and Z-W171-S2. DynamoDB action called: dynamodb:GetItem on etf-classifications.
