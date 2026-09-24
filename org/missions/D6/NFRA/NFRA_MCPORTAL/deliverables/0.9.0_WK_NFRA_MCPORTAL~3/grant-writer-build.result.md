# NFRA_MCPORTAL MP-t-2 -- grant-writer build, session log

**Worker:** `0.9.0_WK_NFRA_MCPORTAL~3`. **Worktree:** `C:/tmp/mp-3`, branch `wk-NFRA_MCPORTAL-3`, based at
`054bad6cc7`. **Commits:** `03c7f7f593` (the build) and `1a19d3c4cb` (a wording-only fix to two comments
that tripped AC3's own `sts:AssumeRole` scan; no behavior change).

## What was built

1. **Name.** `infra/logic/registry/systems.json` gains a `mcportal` row (`PRODUCT`, D6, `measured` from
   `org/missions/D6/NFRA/NFRA_MCPORTAL/project.json` and `org/missions/DIRECTIVES.yaml` D6 :278).
   `lib/opal_naming.py name('mcportal', None, 'grant-writer', 'lambda')` now resolves to
   `mcportal-grant-writer-lambda`; `python lib/opal_naming.py validate` still reports 0 refusals (47
   system rows, same 36 pre-existing WARNs, no new one).
2. **Source.** `infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/lambda_function.py`: the handler
   takes `{"action","tid","oid","candidate","owner_header"}`, verifies the ALB-signed `x-amzn-oidc-data`
   header itself (ES256 against the regional ELB key, reimplemented -- no import of `app/identity.py`),
   exact-matches the verified `oid` claim against `MCPORTAL_OWNER_OID` (its own env var), refuses a
   header whose `iat` is older than `HEADER_MAX_AGE_SECONDS` (120s), and refuses before any store call on
   all three (`NO-OWNER-HEADER`, `HEADER-UNVERIFIED`/`NOT-OWNER`, `HEADER-STALE`). On success it calls
   `ops/schwab_entitlement_admin.py`'s own `prepare`/`activate`/`revoke` so the grant revision and its
   `operator_audit` land in one `access_state.operator_transact` call. `infra/aws/lambda/ci/lambda-source-map.json`
   carries its entry (`source_dir`, `tf_file`, `tf_resource`, `iam_role`).
3. **Tests.** `infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/tests/test_grant_writer.py`: a
   `FakeStore` (records every call, no AWS) and a TEST ES256 keypair injected as `key_fetcher` (never the
   network). `test_refused_without_owner_header`, `test_refused_for_non_owner`, `test_refused_for_stale_header`
   each assert `store.calls == []`; `test_owner_write_lands_with_operator_audit` asserts the profile,
   grant and `operator_audit` land in ONE `operator_transact` call. `4 passed in <1s`, run repeatedly with
   an identical outcome.
4. **Terraform.** `infra/aws/terraform/opal-gateway/mcportal_grant_writer.tf`: the function named by the
   builder; its own execution role (`mcportal-grant-writer-role`) with a data-plane statement mirrored
   from `access_admin_policy` (GetItem on the table, PutItem/UpdateItem restricted to `POLICY#*` leading
   keys, no DeleteItem); ONE `lambda:InvokeFunction` grant for the Gateway role
   (`gateway-invoke-mcportal-grant-writer-policy`) on this function only; no assume-role grant added for
   the Gateway role anywhere in the file. `terraform fmt -check` is clean. `var.mcportal_owner_oid` carries
   no default -- the apply cell supplies it. Nothing is applied, planned or initialized (BOUNDS).

## The check-script defect (row `NFRA_MCPORTAL-Z-W3-S1`)

The round's own `t2.AC1.sh`/`t2.AC2.sh`/`t2.AC3.sh` all call `_root.sh`'s `mp_writer_entry()`, whose
embedded `python -c` one-liner is a `SyntaxError` (a list comprehension containing semicolon-separated
`print(...)` statements). The function's own `2>/dev/null` swallows the error, so every one of the three
checks reads an empty lookup and FAILs regardless of this cell's own state. Verified by re-running the
identical filter standalone (without the broken print clause): it returns exactly 1 matching entry, with
`source_dir` and `tf_file` both real paths in this worktree. Filed, grounded, ARMED (disarm_owner
`2.0.0_SA_COO~O`, since `_root.sh` is outside this cell's `<paths>` and is the issuer's own file). All
three literal invocations are recorded verbatim as FAIL in the proof-of-spec instance, per the worker rule
against repairing a criterion outside its `<paths>`.

## Independent verification of the three criteria's own claims (not the broken script's output)

- AC1: `name()` resolves; standalone re-run of the same source-map filter (without the syntax error)
  returns exactly 1 entry keyed `mcportal-grant-writer-lambda`, `source_dir` and `tf_file` both existing.
- AC2: `pytest .../tests/test_grant_writer.py -v` -> `4 passed`, the four named tests, 0 failed/errored.
- AC3: `terraform fmt -check` rc=0; the builder name literal appears 3 times; `lambda:InvokeFunction`
  appears 2 times; every `sts:AssumeRole` occurrence in the file sits inside the one Lambda trust policy
  naming `lambda.amazonaws.com` (0 outside it, after the wording fix in `1a19d3c4cb`).
