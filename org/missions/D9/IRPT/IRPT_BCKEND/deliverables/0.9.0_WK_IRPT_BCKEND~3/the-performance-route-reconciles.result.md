# Result -- IRPT_BCKEND.TO-IB-rtg-3: the performance route reconciles to the bound id space

**Assignee:** `0.9.0_WK_IRPT_BCKEND~3` | **Pass:** first | **Outcome:** clean reconciliation,
committed and built; STOPPED before apply (both never-widen halves ABSENT at HEAD, the expected
first-pass outcome per the order's own status line).

---

## Arm (a) -- MEASURE FIRST

Confirmed W2-S27: `performance/tenants.py:81,91,101` (pre-fix) keyed `ROUTES` on
`F-49F`/`F-COT`/`F-INF`; `_authz/enforce.py:Enforcer.resolve_now:277-278` overwrites
`headers["x-firm-id"]` with the directory's declared opaque id (`FirmBinding.opaque_firm_id`,
`fir_...`) before `_scope.resolve` runs; `handler.py:79-80` then hands
`scope["verified_request_firm_id"]` (the opaque id) straight to `tenants.route_for`, which raised
`UnknownTenant` -> `DEPENDENCY_UNAVAILABLE` (`entry.py:117`) on every real request.

The estate's ONE id-space normalizer, `_ids/ids.py`, exposes `opaque_firm(firm_id)` -- the exact
grammar the directory artifacts' own `firm_id_opaque` field is minted with (module docstring:
"THE GRAMMAR IS UNCHANGED FROM ROUND 1").

**Firm count re-derived LIVE this pass** (never inherited from the round-6 analysis):
`_ids.firm_ids()` against `data/firm_registry.json` at HEAD returns 3 enabled client firms --
`('49financial', 'cottonwood', 'inflection')` (battery output, line 4).

## Arm (b) -- the reconciliation

**Clean reconciliation was possible; the STOP-and-ROW (new-mapping) branch did NOT fire.**
`performance/tenants.py`'s `ROUTES` dict is now keyed on the opaque id computed via
`_ids.opaque_firm(canonical_firm_id)` for each of the 3 registry client firms, using the estate's
existing normalizer -- no fourth firm-token mapping was minted. The retired short spelling
survives only as a readability alias (`tenants._LEGACY_SHORT_ID`), never read by `route_for`.

The edit is confined to `performance/tenants.py` (no `_ids/` edit was needed -- it already exposed
`opaque_firm`). Source committed `eee9094d47`. Built and uploaded:
`bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter`, rc=0,
`artifact_sha256 W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=` (`lambda-source-map.json`, committed
`60e232e9b2`). Served-byte delta verified exactly `tenants.py` (23 of 23 members, 1 differs;
NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-3.md section 3). Change-management ledger
`irpt-bckend-ib-rtg-3-k-code-build` opened, its one leg proven, and CLOSED
(`org/critical_paths/change_management/20260920T1550Z_irpt-bckend-ib-rtg-3-k-code-build_deploy_completion.md`,
committed `6d1bf6761a`) -- build-store only, no function touched.

**Battery** (`battery_ib_rtg_3.py`, R74-AC1): all 3 registry firms resolve a `TenantRoute` via
their real opaque id, the retired short tokens correctly refuse (`UnknownTenant`), and every
`ROUTES` key is an ISSUED firm id (0 fourth-id-space literals). PASS:
`IBR74-PERFORMANCE-ROUTE-RESOLVES-EACH-FIRM`. Output:
`IB-rtg-3_R74-AC1_battery_output.txt`, committed `eee9094d47`.

## Arm (c) -- the never-widen packet

`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-3.md` written and committed `712b75db26`, blob
`1a1b7b2709f44c03c37a52325623208fe5652cd6`. Read for both halves at HEAD:

- `org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtg-3_*.md`
  -- **ABSENT**.
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtg-3_*.md`
  -- **ABSENT**.

**STOP HERE, per the order's own status line ("ABSENT -> STOP, VALID instance, REPORT (expected
first pass)").** Arms (d) (apply) and (e) (live proof) do NOT run this pass. No apply. The live
`irpt-performance-adapter` function is unchanged (`CodeSha256 IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=`,
confirmed live, unchanged since before this order).

## A related, out-of-bound finding (not fixed, filed)

Row `IRPT_BCKEND-W3-S48`: `handler.py`'s own `RECORDED_LABELS` dict is ALSO keyed on the retired
`F-49F`/`F-INF` spelling this order reconciles in `tenants.py`. Reconciling ONLY `tenants.py` (this
order's explicit bound) leaves `RECORDED_LABELS` unreachable by any real opaque firm id, so a
served request under the function's DEFAULT transport mode (`recorded`) now returns a NO-CAPTURE
absence rather than DEPENDENCY_UNAVAILABLE. This order's own criterion (route resolution, no
DEPENDENCY_UNAVAILABLE) is unaffected. Not fixed here -- fixing it would touch `handler.py`,
outside the "confined to `performance/tenants.py`" bound -- filed and routed to
`2.0.0_SA_COO~B` (the issuer). 5 of 28 pre-existing unit tests in
`performance/tests/test_performance_adapters.py` now fail for this reason (all 5 failures are
`RECORDED_LABELS` misses producing `report: None`/NO-CAPTURE, never an `UnknownTenant` or a route
failure) -- measured, not hidden.
