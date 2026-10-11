# NEVER-WIDEN ASK -- NFRA_OPLGTW OG-gw-1 (round 34, E2, row W42-S1): redeploy `mcportal-grant-writer-lambda` from the live gateway release

From: `0.9.0_WK_NFRA_OPLGTW~56`. To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. Phase A only: nothing is applied, uploaded or written.
Blast radius: ONE Lambda function's code. Its role, policies, layer, environment and tags are unchanged (the plan proves it).

## 1. The one Terraform change

Plan: `W/gw1_plan.txt`, exit code `W/gw1_plan.rc` = 0. Command (from a detached worktree `C:/tmp/og-tf-gw1` at box/sitez
HEAD `6f523f89c9`, `infra/aws/terraform/opal-gateway`): `terraform plan -target=aws_lambda_function.mcportal_grant_writer
-input=false -lock=false -no-color`. Summary line: `Plan: 0 to add, 1 to change, 0 to destroy.`

```
# aws_lambda_function.mcportal_grant_writer will be updated in-place
  ~ last_modified    = "2026-10-03T20:07:55.000+0000" -> (known after apply)
  ~ source_code_hash = "ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI=" -> "894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck="
```

The "from" hash equals the live function's CodeSha256 (`get-function`, read at this time: `ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI=`).
No other attribute changes. The owner key claim and key (environment) show no diff; no secret value appears in the plan.
The plan reads the build at plan time (`data.external` -> `build_gw_stage.py` -> `build_package.py`, from
`EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` = `c3af8687e44a1e641259b37f992033ae02cdce3d`).

Order premise that did not hold (filed as a row): the order says `mcportal_owner_key_claim` and `mcportal_owner_key` are required
Terraform variables supplied by `TF_VAR_`. At box/sitez HEAD neither is a declared variable: both are read inside the
configuration from `gateway/principals/rosters` (`data.aws_secretsmanager_secret_version.mcportal_owner_config`), so no `TF_VAR_`
was needed and none was set.

## 2. The code delta (live pin -> c3af8687e4), by member

Method: live code downloaded with `get-function` (read) and compared member by member with `git show`; the live
`data_entitlement.py`, `ops/schwab_entitlement_admin.py` and `NFRA_OPLGTW_CONTRACT.json` are byte-equal to the blobs at
`adc979b13b8b256aa32dea4cb57a34ae7b090333` (the old pin, 2026-10-01); live `app/config.py` is byte-equal to the blob at
`db92656c72` (a release-branch commit, not an ancestor of c3af8687e4). 11 members: 7 identical, 4 differ.

| member | live (bytes) | rebuilt (bytes) | change |
|---|---|---|---|
| `app/data_entitlement.py` | 32133 | 35626 | +62/-4 vs adc979b13b: `calendar_months` (1 to 13) parsed and validated, `calendar_days` only the contract 30, exactly one of the two; `Scope` gains both fields; `months_before` / `window_first`; `_allowed_dates` uses them |
| `ops/schwab_entitlement_admin.py` | 27887 | 29030 | +22/-1: a candidate with `calendar_months` is refused unless the contract has `rolling_window` carrying it; the old/new window enters the audit diff; the value is written into the grant's `dates` only when carried |
| `org/standards/NFRA_OPLGTW_CONTRACT.json` | 9189 | 10747 | +25/-2: adds the `rolling_window` rule and `calendar_months` meaning (13 months of 2026-03-31 is 2025-02-28) |
| `app/config.py` | 29788 | 30925 | +12 vs the live blob: two gateway settings (`YEARINREVIEW_VIEW_ALLOWED_EMAILS`, `MAIL_SENDER_DOMAIN_TABLE`), read from the environment, unused by the grant path; they ride in because the closure imports `app.config` |

Identical members: `app/__init__.py`, `app/access_state.py`, `app/context.py`, `app/graphql_plumbing/__init__.py`,
`app/graphql_plumbing/catalog_gate.py`, `ops/__init__.py`, `lambda_function.py`. No member added or removed.

## 3. Both branches of a grant write

- Refused (live now): a rolling grant whose `dates` carries `calendar_months` is rejected -- the live parser admits only `{"mode"}` for
  `rolling_complete_window` ("a rolling_complete_window grant carries only its mode"), so the write returns a refusal and no
  `POLICY#` item changes.
- Written (after the rebuild): the same grant with `calendar_months` 1 to 13 is accepted and stored with its month window; a
  grant carrying neither keeps the 30-day window and its prior shape; `calendar_months` 14 or 0, a non-integer, or both
  `calendar_days` and `calendar_months` still refuse (`Malformed`), before any store call.

The AC1 test `test_grant_writer_stages_the_contract_only_from_the_standard` passes against the rebuilt package source (pytest rc=0).

## 4. Rollback

Redeploy the prior code: `CodeSha256` `ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI=` (live now). Restore by rebuilding the old
members from the commits above (adc979b13b: `data_entitlement.py`, `schwab_entitlement_admin.py`, contract; db92656c72:
`config.py`; `lambda_function.py` and the other members unchanged) and uploading that zip, or, if the applier saves the live
zip first (`get-function` Code.Location, a read), re-uploading it byte-for-byte. The check is the function's CodeSha256 returning to
the value above. The rollback is a code redeploy: no data to undo, since the grant table holds no write from this act except the
read-back grant below.

## 5. The read-back (the applier's step, after the apply)

One 13-month grant written through the rebuilt function, then read back: a `widen` for a named test principal in the
owner's own tenant with `scope.dates = {"mode":"rolling_complete_window","calendar_months":13}`, sent with the owner's
ALB-signed header (the function accepts only the owner), then read the `POLICY#<tid>#<oid>` item and the
`mcportal-grant-changes-table` row to see `calendar_months` 13 stored and the window diff in the audit record. Named
gap: the owner header is Andrew's session, so this step needs the owner path (his sign-in) -- the applier order must name
who drives it. A revoke (a tombstone) of the test principal follows.

## 6. What the pair signs

That an apply of exactly the one change in section 1 may run: `aws_lambda_function.mcportal_grant_writer` code, nothing else, by `-target`
and by a fresh plan at the time of apply that reads the same single-row summary. No upload and no grant is written by this order.
