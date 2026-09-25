# NFRA_MCPORTAL.TO-MP-t-1 -- owner gate and serving -- result

Assignee 0.9.0_WK_NFRA_MCPORTAL~2, worktree C:/tmp/mp-2, branch wk-NFRA_MCPORTAL-2, base 48ee4eebfc.

## What was built

- `app/owner_gate.py` (new): `DASHBOARD_OWNER_EMAILS`-backed owner gate. Identity comes ONLY from
  `identity._alb_oidc_identity` (ES256-verified `x-amzn-oidc-data`). `require_owner()` returns the
  verified owner email or raises `OwnerGateError` (401 = no identity established at all -- missing
  header or a failed/forged verification; 403 = a verified identity that is not on the roster).
  `validate_owner_emails()` is the boot-time refusal: any roster entry other than
  `andrew@opalinvest.com` raises `RuntimeError`; unset/empty does not raise (the dashboard just
  fail-closes every request instead, since an empty roster matches no email).
- `app/admin_api.py` (new): the `/api/admin/*` Starlette router, mounted under `owner_gate.owner_only`.
  First route: `GET /whoami`.
- `app/server.py`: calls `owner_gate.validate_owner_emails(_cfg)` at boot beside `_cfg.validate()`;
  mounts `Mount("/api/admin", app=admin_api.admin_app)` and adds `Route("/", dashboard_root)` serving
  `DASHBOARD_BUNDLE_DIR/index.html` behind the gate (missing bundle -> plain 503, never a crash). Both
  are appended after the `/sprint/{day}` route and before `Mount("/mcp", ...)`. Route-order safety: the
  admin mount is a brand-new, non-overlapping URL prefix (`/api/admin`), and `"/"` is an exact-path
  `Route` -- Starlette's `Route` only prefix-matches when it declares path params, so a bare `"/"` Route
  matches ONLY the literal root and cannot shadow `/sprint*`, `/mcp`, the OAuth/well-known paths,
  `/health` or anything else; none of those routes moved or changed.
- `app/config.py`: `DASHBOARD_OWNER_EMAILS` (parsed like `MASTER_ADMIN_EMAILS`/`WRITE_CAPABLE_EMAILS`,
  but its own distinct env var and purpose) and `DASHBOARD_BUNDLE_DIR` (default `dashboard/` beside `app/`).
- `tests/test_owner_gate.py` (new): the five named tests. The ALB header verification is stubbed at
  BOTH call sites that reach it -- `owner_gate._alb_oidc_identity` (owner_gate's own import, used by
  `require_owner`) and `identity._PROVIDERS['alb_oidc']` (the dict `get_user_email` -- and therefore
  `sprint_view._viewer` and `GuardMiddleware`'s `/sprint`+`/login` branch -- looks up AT CALL TIME, so
  patching the dict entry in place reaches every caller regardless of which module imported the name).
  sprint_view's S3 reads are stubbed the same way (never the network); this cell does not own
  `sprint_view.py` or `identity.py`.

## Commit

`98ad7e253fbe8bc176c3d69c5f955824917a04bb` on branch `wk-NFRA_MCPORTAL-2` (LOCAL; not pushed).

## Controls

- Mutant: `probes/mp_t1_mutant.py` monkeypatches `owner_gate.is_owner` to always return `True`
  in-process (no tracked file touched) and re-runs `require_owner()` for Andrew and a verified
  non-owner. Real: Andrew ALLOWED, non-owner DENIED-403. Mutant: Andrew ALLOWED, non-owner ALLOWED
  (the bug the mutant re-creates) -- `git status --porcelain` identical before/after.
  `VERDICT: PASS-MP-T1-MUTANT`.
- Determinism: `tests/test_owner_gate.py` and the two AC check scripts were each run twice; identical
  pass counts and output both times.

## Bounds honoured

Nothing deployed (`deploy-to-ec2.sh` untouched); `moto` not installed and not touched;
`app/identity.py`, `app/sprint_view.py`, `app/tier.py`, `app/guard.py`, `tests/conftest.py` read only,
never edited. `tests/test_identity_scope.py::test_scoped_deny_by_default` remains the one pre-existing
red test at the cut (5 of 6 passed, same as BOUNDS #2 states); nothing in this cell touches
`app/identity_scope.py`.
