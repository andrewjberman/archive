# NFRA_OPLGTW.TO-OG-a-3: the download browser's own OIDC login (as amended @6886ddd314)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3d` (worktree `/c/tmp/wk-oplgtw-1-3d`, cut from
`CLOUD` at `7459929520`, after OG-a-2 merged) | **Commits (LOCAL):**
- first run: `6a4e94d734` (the code, the test module and `BROWSER_PATHS.json`), `b2648343dc` (rows W3-S16 .. W3-S21),
  `06a9aec60d` (its completion);
- the issuer's amendment `6886ddd314` (status back to pending; ROUTE_CLASS granted; AC7 restated; AC8 .. AC10 added);
- this run: `9828b0e96e` (the ROUTE_CLASS entries, the superset AC7 and the AC8/AC10 probe), then the commit that
  carries this file, the proof instance and the `<status>` flip.

Nothing was pushed, merged or deployed.

## Read this first: 10 of 10 criteria pass by output

Every invocation ran verbatim at `9828b0e96e`:
- the eight pytest criteria read `1 passed` each (AC1 .. AC7) and `11 passed` (AC9), each with rc=0;
- the two probes print `VERDICT: PASS-OGA3-AC8` and `VERDICT: PASS-OGA3-AC10`, each with rc=0.

The first run's two route-table couplings are gone:
- `test_oga2_ac04` is green again (row W3-S16);
- AC7 now survives a later cell's new routes (row W3-S17).

## What this run changed

| path | what |
|---|---|
| `infra/aws/ec2/opal-gateway/tests/test_principal_cutover.py` | 2 lines added to `ROUTE_CLASS` (`:498`, `:499`), each `"public"`; nothing else |
| `infra/aws/ec2/opal-gateway/tests/test_browser_oidc.py` | `test_oga3_ac07` rewritten as a superset, plus 2 helpers (`_in_order`, `_declared_middleware`) |
| `deliverables/0.9.0_WK_NFRA_OPLGTW~3/probes/og_a3.py` (new) | the AC8 and AC10 probe |

`app/browser_oidc.py`, `app/server.py` and `BROWSER_PATHS.json` are unchanged since `6a4e94d734`, as the amendment
says ("Your AC1..AC6 code stands").

- **AC7, superset.** It checks five things:
  - every base route is still served, row for row (kind, path, methods, endpoint), in base order, each base path
    once;
  - both browser routes are served by `app.browser_oidc`;
  - the live middleware equals the base's `app.add_middleware` calls, reversed (read from the base git object);
  - `/login`, `/sprint` and `/sprint/archive` still refuse without the access-layer header;
  - the new login redirects to the upstream.

  It no longer asserts what HEAD adds, so the next cell's routes keep it green.
- **AC8, one-time record.** The probe reads three things:
  - `app/server.py`'s route declarations at the base and at HEAD, both from git objects by AST, comparing each
    declaration's whole structural dump;
  - `BROWSER_PATHS.json` at HEAD;
  - the served table of the app imported from the worktree. It refuses unless `app/` equals HEAD, and it imports
    under a no-egress guard.

  HEAD must equal the base plus exactly the listed rows.
- **AC10.** The probe reads the file at both vintages and the `-U0` diff:
  - 0 lines are removed;
  - every added line is inside `ROUTE_CLASS`, and together the added lines read as exactly the two entries;
  - the module with `ROUTE_CLASS` blanked is structurally identical at both vintages.

## Criteria (each invocation verbatim at `9828b0e96e`)

| id | verdict | deciding line |
|---|---|---|
| OGA3-AC1 | PASS-by-output | `BROWSER_PATHS.json lists 2 path(s) ...; all three sets equal; 4 of 4 (path, method) pairs answered` / `1 passed in 1.93s` |
| OGA3-AC2 | PASS-by-output | `refused 400 with no redirect and no session cookie on 4 of 4 arms ...; upstream redemptions for the 3 state arms [0, 0, 0]` / `1 passed in 1.84s` |
| OGA3-AC3 | PASS-by-output | `refused 400, no session cookie, on 3 of 3 arms, each by its own check` / `1 passed in 1.68s` |
| OGA3-AC4 | PASS-by-output | `2 of 2 cookies ... Secure + HttpOnly + SameSite=lax + Path=/schwab/download ...; 4 of 4 download URLs and 0 of 10 others` / `1 passed in 1.43s` |
| OGA3-AC5 | PASS-by-output | `MCP OAuth principal key == browser session principal key (True), tid equal True, oid equal True` / `1 passed in 1.81s` |
| OGA3-AC6 | PASS-by-output | `imports of app/identity.py and references to 4 ALB helper names or the ALB OIDC header 0` / `1 passed in 1.32s` |
| OGA3-AC7 | PASS-by-output | `base routes still served unchanged 27 of 27, in base order, each path once; browser routes served 2 of 2; middleware ... == the base's add_middleware calls reversed; ... 401 (3 of 3)` / `1 passed in 1.89s` |
| OGA3-AC8 | PASS-by-output | `declared routes: base 27 ..., HEAD 29`; `added 2; removed 0; changed 0; base order kept: yes`; `served routes ... 29; equal to the HEAD declarations row for row: yes; ... egress attempts during import 0` / `VERDICT: PASS-OGA3-AC8` |
| OGA3-AC9 | PASS-by-output | `OGA2-AC4: route declarations in app/server.py 29 ... == app.routes 29; ... public 10; ... the legacy bearer changes no status on 10 of 10` / `11 passed in 5.43s` |
| OGA3-AC10 | PASS-by-output | `ROUTE_CLASS entries: base 27, HEAD 29; gained {2, both public}; removed 0; re-classed 0`; `0 line(s) removed or changed, 2 added`; `module outside ROUTE_CLASS structurally identical: yes` / `VERDICT: PASS-OGA3-AC10` |

## Controls

- **AC7 mutants** (in-process, worktree untouched):
  - 2 extra routes injected (29 -> 31): `1 passed`. The superset holds where the first run's pinned AC7 would fail.
  - `/sprint/archive` removed: `1 failed`.
  - `/login` re-bound to POST only: `1 failed`.
- **Probe judges:** each verb runs its judge first on 6 synthetic cases, and 6 of 6 came out as expected on both AC8
  and AC10.
- **AC10 negative arm:** at the pre-edit HEAD `6886ddd314`, the probe printed `VERDICT: FAIL-OGA3-AC10 git diff ...
  rc=0 bytes=0`, rc=1.
- **AC9 negative arm:** the first run at `6a4e94d734` read `1 failed, 10 passed` on `test_oga2_ac04` (row W3-S16).
- **Determinism:** the pre-commit module runs (7 passed; 11 passed) agree with the verbatim runs, and the AC8
  counts are identical at `6886ddd314` and `9828b0e96e`.
- **Commit gate:** `OK: pre-commit gate clean for 3 of 3 file(s)`. It raised one advisory, not blocking, on
  `test_principal_cutover.py:527`, a line present at the cut base.

## Rows

This run filed no new row. The rows from the first run (`INVESTIGATION_v1.md` @ `b2648343dc`) are listed in the
proof's `surprises`:
- W3-S16 and W3-S17: both ARMED, disarm owner `2.0.0_SA_COO~O`. The amendment addresses both.
- W3-S18 .. W3-S21: INERT.

## Proof check

`py -3.12 .tools/proof-of-spec-check.py org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~3/NFRA_OPLGTW.TO-OG-a-3.browser-oidc.proof_of_spec.json OGA3-AC1,OGA3-AC2,OGA3-AC3,OGA3-AC4,OGA3-AC5,OGA3-AC6,OGA3-AC7,OGA3-AC8,OGA3-AC9,OGA3-AC10`:
the exit code is recorded in the final worker report and in the commit that carries this file.
