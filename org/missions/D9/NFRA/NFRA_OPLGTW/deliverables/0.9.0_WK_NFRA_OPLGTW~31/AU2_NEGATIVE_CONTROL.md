# OG-au-2 negative control

Run from `infra/aws/ec2/opal-gateway`: `python -m pytest tests/test_audit_rivalfunds_args.py -v -p no:cacheprovider`.

With the one line `"rivalfunds_view": {"day", "route", "fund"},` removed from `_ARGS_ALLOWLIST` in `app/audit.py`
(restored afterwards; `git diff` shows the entry present):

```
test_ogau2_ac01 FAILED   (record args == {'_omitted': 'args fail-closed (tool not in R8-PRIV allowlist)'}, want day/route/fund)
test_ogau2_ac02 FAILED
test_ogau2_ac03 PASSED   (bytes is a separate log_call argument, independent of the allowlist)
test_ogau2_ac04 FAILED
3 failed, 1 passed
```

With the entry present: 4 passed.
