# NFRA_OPLGTW.TO-OG-z-2 -- result (0.9.0_WK_NFRA_OPLGTW~3)

**Outcome: 9 of 9 mechanical criteria PASS by output.** Branch `wk-nfra_oplgtw-1-3e`, worktree
`/c/tmp/wk-oplgtw-1-3e`, cut from CLOUD at `404fe87155` with `OG-z-1`, `OG-z-3`, `OG-i-1`, `OG-i-2` and
`OG-k-1` merged. Cold start: `.venv-og` built fresh this run (py -3.12, `--system-site-packages`,
`requirements.txt` + `msal moto pytest`; mcp 1.28.0, moto 5.2.3, boto3 1.42.54/botocore 1.42.97).

## What was built

`infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py` (new, 376 lines) -- the operator's
entitlement administration command. It is a repository/release-operated script, never an MCP tool
(nothing in `app/tools.py` or `app/integrations/**` imports it or the POLICY-write primitives it uses --
`OGZ2-AC8`). It never touches a live table in this cell.

- `check_operator_identity(sts_client)` -- reads `sts_client.get_caller_identity()` and matches the
  ARN's ROLE NAME (either `role/<name>` or `assumed-role/<name>/<session>` form) against
  `opal-gateway-access-admin` (the operator role created by `OG-i-1`,
  `arn:aws:iam::313476888478:role/opal-gateway-access-admin`); every other identity, INCLUDING the
  Gateway runtime role `opal-gateway-role`, is refused (`IdentityRefused`).
- `validate_candidate(raw, contract)` -- `context.make_principal` for the candidate's own tid/oid
  (empty/unknown -> `CandidateRejected`); `data_entitlement.parse_scope` for the scope shape
  (malformed dates, an account named for a master outside the candidate's own granted masters, an
  unknown master/dataset/operation -> `CandidateRejected`); then this command's own cross-check of the
  contract's `fields` catalog and `forbidden_field_classes` per dataset, and `grant_date_modes` /
  `operations` / `disabled_operations` against the contract data (not hand-typed constants) -- the five
  contract keys the hand-off named.
- `prepare(store, raw_candidate, contract)` -- validates, strongly reads the current profile/grant
  (`current_state`), computes the exact per-dimension `scope_diff` and PRINTS it, and returns a `Plan`
  carrying the base profile/grant revision that read produced. Nothing is written here.
- `activate(store, plan, approver=, source_authorization=, at=, summary=)` -- conditionally activates
  `plan` against `plan.base_profile_revision` (`data_entitlement.profile_put_op`'s optimistic condition):
  a STALE base (the record moved, or now exists, since `prepare()` read it) raises
  `access_state.ConditionFailed`; the CURRENT base succeeds. ONE `access_state.operator_transact` call
  writes the `principal_profile` put, the new `data_entitlement` revision put and the
  `operator_audit` append together (`OGZ2-AC6`).
- `revoke(store, tid, oid, approver=, source_authorization=, at=, summary=)` -- the tombstone: profile
  status -> `revoked` at the next revision, appended with its audit in ONE transaction; never a
  `DeleteItem` (`OGZ2-AC7`; and `access_state.operator_transact` independently refuses any `delete`
  action before any AWS call, so a mutant that tried to sneak one in via `revoke()` raised
  `AccessStateRefused` instead of succeeding -- see Controls).
- A CLI (`activate`/`revoke` subcommands, `argparse`) for real operator use, wired through the same
  functions; `sts_client`/`store`/`out` are all injectable so nothing in it forces a real AWS call.

`infra/aws/ec2/opal-gateway/tests/test_entitlement_admin.py` (new, 369 lines) -- `test_ogz2_ac01` ..
`test_ogz2_ac09`, offline, on `tests/test_access_state.py`'s moto harness (fake credentials, an
in-process DynamoDB table, a `Spy` client that records every call). AC9 drives a fake STS client with
both ARNs directly; AC8 is a static census over the source files backing every currently REGISTERED
MCP tool (native `app/tools.py` plus the three integrations `registry.available_ids()` actually
constructs -- `ycharts`, `opal_portal`, `globgrph`; the five Schwab tool names are classified in
`data_entitlement.TOOL_CLASSES` but registered on no factory yet, confirmed live by
`available_ids()`, so they are outside this census's file set by construction, not by omission).

## Criteria (each run individually under `timeout 120`, then the whole file together, then twice more
for determinism)

| id | verdict | deciding output |
|---|---|---|
| OGZ2-AC1 | 1 passed | "3 of 3 empty/unknown-identity candidates refused" (empty tid, missing oid, non-GUID tid) |
| OGZ2-AC2 | 1 passed | "2 of 2 (unapproved account, unapproved field) candidates refused" |
| OGZ2-AC3 | 1 passed | "2 of 2 malformed-date candidates refused" (invalid calendar date, wrong shape) |
| OGZ2-AC4 | 1 passed | "diff printed by prepare() (6 dimension lines) precedes the activate() call"; `plan.diff` compared equal to an independently computed `scope_diff(None, plan.scope)` |
| OGZ2-AC5 | 1 passed | "stale base (None, now superseded) refused with ConditionFailed; current base (revision 1) activated to revision 2" |
| OGZ2-AC6 | 1 passed | "1 transact_write_items call, 3 puts (profile+grant+audit), audit carries approver='andrew@opalinvest.com' source_authorization='IT-TICKET-42' at='2026-09-16T01:02:03Z'" |
| OGZ2-AC7 | 1 passed | "revoke() -> 1 transact_write_items call, 0 Delete items, 0 delete_item calls; profile still readable, status=revoked revision=2; a direct delete Op is refused before any AWS call" |
| OGZ2-AC8 | 1 passed | "DENOMINATOR 44 registered tool(s) (35 native + 9 integration across ['globgrph', 'opal_portal', 'ycharts']) backed by 10 file(s) scanned -- 0 hit(s)" |
| OGZ2-AC9 | 1 passed | "operator role ARN accepted (role+assumed-role form); runtime role ARN 'arn:aws:iam::313476888478:role/opal-gateway-role' refused (role+assumed-role form)" |

Whole-module run: `9 passed in 1.58s`, rc=0. Repeated: `9 passed in 1.47s`, rc=0 -- diff of the two logs
is empty except the timing line (determinism).

## Controls: mutants (7), one process each, `.scratch/ogz2_mutants.py` (uncommitted, loaded with
`-p ogz2_mutants` / `PYTHONPATH=.scratch`), monkeypatching the running module only -- the committed bytes
untouched

| mutant | targets | observed |
|---|---|---|
| `identity_off` (`check_operator_identity` never refuses) | AC9 | `1 failed` -- `assert 'MUTATED-NO-CHECK' == 'arn:...access-admin'` |
| `permissive_identity` (`context.make_principal` never refuses) | AC1 | `1 failed` -- `Failed: DID NOT RAISE CandidateRejected` |
| `permissive_scope` (`de.parse_scope` never refuses a malformed shape/date/account) | AC2, AC3 | `2 failed` -- both `DID NOT RAISE CandidateRejected` |
| `stale_reread` (`activate()` re-reads the current revision instead of trusting the plan's base) | AC5 | `1 failed` -- `Failed: DID NOT RAISE ConditionFailed` (recreates the exact race the two-step `prepare`/`activate` design exists to close) |
| `audit_clobber` (`operator_audit_op` always records `approver='MUTATED'`) | AC6 | `1 failed` -- `assert 'MUTATED' == 'andrew@opalinvest.com'` |
| `no_diff_print` (`prepare()` computes the diff but never prints it) | AC4 | `1 failed` -- `assert 'SCOPE DIFF:' in ''` |
| `revoke_via_delete` (`revoke()` appends a `Delete` transaction item) | AC7 | `1 failed` -- `access_state.AccessStateRefused: POLICY records are never deleted` (raised by `access_state.operator_transact`'s own independent guard, before any AWS call) |

Supplementary, not a pytest run: AC8's static census, widened to include the common token `"def "` in
its primitive list, flags 7 of the same 10 files (vs 0 with the real primitive list) -- the census is
sensitive, not vacuously passing. 7 of 7 mutants fired as expected; every mutant broke exactly the
criteria it targeted and none of the others were run under it.

## Interpreter

`.venv-og` built this run: `py -3.12 -m venv --system-site-packages .venv-og` then
`pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest`. Python 3.12, boto3
1.42.54, botocore 1.42.97, mcp 1.28.0, moto 5.2.3, pytest 9.0.2 (pip's own dependency-resolver warnings
about `awscli`/`mitmproxy`'s outer-environment pins are pre-existing and orthogonal to this venv).

## Command usage (operator-facing; not activated here)

```
.venv-og/Scripts/python infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py activate \
  --candidate candidate.json --approver <name> --source-authorization <ref>
.venv-og/Scripts/python infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py revoke \
  --tid <tid> --oid <oid> --approver <name> --source-authorization <ref>
```
Both subcommands check the caller's AWS identity first (real `boto3.client("sts")` unless a test injects
one) and refuse before touching the store if it is not the operator role.

## Rows filed this run

None. Nothing the order did not say, and nothing it said that could not be done as written: the two-step
`prepare`/`activate` split, the contract-derived field/date/operation cross-checks and the ARN-role-name
match were all implementation choices within this cell's own grant, not deviations from it.

## commit-gate

`bash .tools/commit-gate.sh infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py
infra/aws/ec2/opal-gateway/tests/test_entitlement_admin.py` -> `OK: pre-commit gate clean for 2 of 2
file(s)`.
