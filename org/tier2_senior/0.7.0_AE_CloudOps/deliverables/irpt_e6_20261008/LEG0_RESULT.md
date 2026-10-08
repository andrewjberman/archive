# IRPT_BCKEND E6 laptop leg 0

Seat: 0.7.0_AE_CloudOps
Date: 2026-10-08
Table: irpt-requests, us-east-1
Caller: arn:aws:iam::313476888478:user/Andrew_Berman
Schema: tenant (HASH, S), request_revision (RANGE, S)
Key: tenant=__IRPT_E6_NONEXISTENT_DRY_PROBE_20261008_0_7_0__; request_revision=__NEVER_CREATED__1cfcc7b5-d8c7-48ce-8325-77c38d351e2c
Condition: attribute_exists(tenant)
Response: An error occurred (ConditionalCheckFailedException) when calling the DeleteItem operation: The conditional request failed
AWS CLI exit: 255 (expected service rejection)
Result: expected condition failure; no row deleted. Conditional prerequisite for leg 1 satisfied.
Push state: LOCAL; origin CLOUD a8689cb2595050a7c40427160113abd8fd5e4e8c (git ls-remote).