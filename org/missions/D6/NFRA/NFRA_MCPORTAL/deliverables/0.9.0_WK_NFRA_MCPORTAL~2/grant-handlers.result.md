# NFRA_MCPORTAL.TO-MP-t-4 -- grant handlers -- result

Assignee 0.9.0_WK_NFRA_MCPORTAL~2, worktree C:/tmp/mp-2, branch wk-NFRA_MCPORTAL-2, base a2b89be579
(stacked on MP-t-1, merged into this branch, UNMERGED into CLOUD -- chain B merges once at its end).

## What was built

- `app/admin_grants.py` (new): `read_grant_state(tid, oid, table=None) -> "NO-PROFILE" |
  "PROFILED" | "STORE-UNAVAILABLE"`, through `access_state.AccessState.get` on the
  `principal_profile` key (the EXISTING strong-read path, never a new one). `GET
  /grants/{tid}/{oid}`: the principal's profile + active data grant via
  `data_entitlement.current_access`. `POST /grants/{tid}/{oid}/narrow|widen`:
  `invoke_grant_writer()` calls a boto3 Lambda client (`GRANT_WRITER_FUNCTION_NAME` env; unset or
  any invoke failure/malformed response answers `REFUSED` with a reason, never a crash) with the
  candidate and the REQUEST's own `x-amzn-oidc-data` header forwarded verbatim as `owner_header`,
  and relays the writer's verdict unmodified. `GET /changes`: the writer's `operator_audit` rows
  for one principal (required `tid`/`oid` query params), newest first, each record passed through
  exactly as the writer stored it (including whatever `before`/`after` fields it wrote).
  Every handler here is `owner_only`-decorated in this module; none calls
  `access_state`'s write API (`put_runtime`/`update_runtime`/`delete_runtime`/`transact_runtime`/
  `operator_transact`) -- `test_gateway_never_writes_policy` traps all five.
- `app/admin_api.py`: registers the four new routes onto the existing `/api/admin/*` router
  (handlers stay decorated in `admin_grants.py`; this file only wires them, per this cell's own
  chain-B amendment -- no second writer touches this file).
- `app/server.py` (drain amendment): `GET /assets/{path:path}` serves
  `DASHBOARD_BUNDLE_DIR/assets/*` behind the SAME owner gate as `"/"` (path-traversal-safe: the
  resolved target must stay inside the assets dir). Added between the `/api/admin` `Mount` and the
  `"/"` `Route`; an exact, non-overlapping prefix that shadows nothing above or below it. Without
  this, `"/"` served `index.html` but nothing served the Vite bundle's assets, so the dashboard
  would load blank.
- `tests/test_admin_grants.py` (new): the four AC1-named tests
  (`test_get_grant_reads_store`, `test_narrow_invokes_writer_with_forwarded_header`,
  `test_gateway_never_writes_policy`, `test_changes_newest_first`) plus the amendment's own
  `test_assets_served_to_owner_only`. All offline (no network, no moto): the ALB header
  verification is stubbed exactly as `tests/test_owner_gate.py` stubs it; `access_state` calls are
  stubbed at the class/module level.

## Interpretation surfaced (see the surprise row)

The task order's literal `GET /api/admin/changes` names no `tid`/`oid`, implying a global feed, but
the existing store's `operator_audit` records live under a per-principal `POLICY#<tid>#<oid>`
partition with no cross-tenant index -- there is no read this box's existing read path can make
that lists every principal's changes in one call. Implemented scoped by required `tid`/`oid` query
parameters; a true global feed needs a new index, out of this cell's `<paths>`.

## Commit

`17b7e01c0f0234724cb7177d231b0b4cafee4a84` on branch `wk-NFRA_MCPORTAL-2` (LOCAL; not pushed).

## Controls

- Mutant: `probes/mp_t4_mutant.py` monkeypatches `access_state.AccessState.get` in-process (no
  tracked file touched) to swallow a `DependencyUnavailable` as "no record". Real:
  `read_grant_state` distinguishes NO-PROFILE (live, never-profiled principal) from
  STORE-UNAVAILABLE (a nonexistent table). Mutant: both answer NO-PROFILE (the distinction AC2
  exists to catch disappears). `VERDICT: PASS-MP-T4-MUTANT`.
- Determinism: `tests/test_admin_grants.py`, `t4.AC1.sh` and `t4.AC2.sh` were each run twice;
  identical pass counts and deciding output both times (AC2 is a live AWS read; both runs answered
  `NO-PROFILE`/`STORE-UNAVAILABLE` identically).

## Bounds honoured

Nothing deployed. No push, no install, no vendor call beyond the declared read-only AWS DynamoDB
`get_item` (AC2's own invocation) and the stubbed Lambda invoke in tests (never real). No AWS write
of any kind. `app/owner_gate.py`, `app/access_state.py`, `app/data_entitlement.py`, `app/config.py`,
`ops/schwab_entitlement_admin.py` read only, never edited.
