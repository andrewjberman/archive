# EN-aa-3 scope test result (0.9.0_WK_LGIC_ENFORCE~3)

Commit 3ef12f2fe3 changes lib/tests/test_opal_naming_scope.py only.

Old: any(i["current"] == "etfs-rivalfunds-daily-role" and i["where"].endswith(".tfvars.json:11") for i in res)
New: the line is derived from infra/aws/terraform/etfs-rivalfunds/generated.auto.tfvars.json (the one line holding the role name), and the same check asserts the name is counted at ".tfvars.json:<that line>".

Criterion AA3R21-AC1: check_en_r21.py scope -> rc=0, "scope: rc=0 SCOPE-TEST ok=True assertions=826", last line PASS-R21-SCOPE.
