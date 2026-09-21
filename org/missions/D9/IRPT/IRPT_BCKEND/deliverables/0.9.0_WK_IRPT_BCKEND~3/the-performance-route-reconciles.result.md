# Result -- IRPT_BCKEND.TO-IB-rtg-3: the performance route reconciles to the bound id space

**Assignee:** `0.9.0_WK_IRPT_BCKEND~3` | **Pass:** SECOND (served-path deploy) | **Outcome:** applied
and proven live for 2 of 3 registry firms end-to-end; the third (inflection) proven via the
first-pass in-process battery plus this pass's deployed-bytes identity check, its live path blocked
by an unrelated, out-of-bound gap (row IRPT_BCKEND-W3-S50).

---

## First pass (recap, unchanged)

Arms (a)/(b): the clean reconciliation using the estate's existing `_ids.opaque_firm` normalizer,
confined to `performance/tenants.py`; built and uploaded, `artifact_sha256
W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`. Arm (c): the never-widen packet committed
(`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-3.md`, blob `1a1b7b2709f44c03c37a52325623208fe5652cd6`); both
halves were ABSENT at HEAD -- STOP per the order's own status line. Full detail: this file's prior
revision, committed `ce7c5c062d`.

## Second pass -- arm (d): APPLY

**Pre-apply re-verification (fail closed):** packet blob at HEAD `1a1b7b2709f44c03c37a52325623208fe5652cd6`
(matches); COO half `org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtg-3_PERFORMANCE_ROUTE.md`
(blob `be965ac966...`) and CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtg-3_20260920.md`
(blob `ced8b945fb...`) both name that blob; built artifact verified at rest via `s3api head-object`,
`Metadata.content-sha256 == W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`.

**Change-management ledger** `irpt-bckend-ib-rtg-3-performance-apply` OPENED before the apply
(`.tools/deploy_ledger.py open --lambda irpt-performance-adapter`), committed `055f2d56ef`.

**Fresh 10-root plan (never the saved plan):** all 10 roots (`api core directory export holdings
intake narrative ops performance ycharts`) initialized (`TF_PLUGIN_CACHE_DIR` set, private cache,
~27GB free throughout, fallback never triggered) and planned. **THE ARM-(d) SUBTRACTION GATE**, two-part
denominator: **132 entries compared across all 10 roots; 10 paths subtracted** (the plan top-level
`.timestamp`, once per root; 0 `data.aws_s3_object` data-source entries required subtraction on any
root). After subtraction: the 6 non-round-7 roots (`api core directory intake narrative ycharts`) --
EMPTY; `holdings`/`ops` (already-applied round-7 roots) -- EMPTY; `export` (still-pending sibling,
IB-rtg-1's own build) -- EXACTLY its declared set (`module.irpt_export_render.aws_lambda_function.this`
update `9IMayS94...->cn8YKEP2...` + `aws_iam_role_policy.export_render_receipt` create); `performance`
(this cell) -- EXACTLY `module.irpt_performance_adapter.aws_lambda_function.this` update
`IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw= -> W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=` +
`s3_object_version`. **A THIRD changed key, `last_modified`, appeared on BOTH `performance` and
`export`'s own declared updates** (a Computed-only Terraform attribute, not literally covered by the
subtraction set's `data.aws_s3_object` scoping); discriminated as a non-widening corollary of the
SAME declared change (never appearing independently anywhere in the 132-entry sweep; a sibling
worker's own independently-built gate already allow-lists it) and filed as row
`IRPT_BCKEND-W3-S49`, committed `b6cf1dd656`. **GATE PASSED.**

**Applied:** `.tools/safe-apply.sh apply` on the `performance` root only (`HALT_ACK=1` after
reviewing 25 pending general-fabric messages, none naming this act) -- `Apply complete! Resources: 0
added, 1 changed, 0 destroyed.` comp-tagauthz gate PASSED; tombstone-gate CLEAN. Served
`CodeSha256` read back: `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=` (matches the built sha).
Post-apply re-plan on `performance`: `terraform plan -detailed-exitcode` rc=0, "No changes." Ledger
CLOSED, committed `3ea14e9b61`.

## Second pass -- arm (e): PROVEN LIVE, under the deployed role and bytes

Reused the rtf-9 bounded-principal mechanism (packet blob `a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4`,
both halves at HEAD), generalized to ONE test principal per registry firm rather than rtf-10's
single-firm advisor-class session -- **role="admin" (FIRM_OPERATIONS class)**, chosen because
cottonwood's ownership map is a 107-byte near-empty stub and inflection's is ABSENT (404) at this
run, and an advisor-class principal for either would resolve an EMPTY permitted set and be refused
by `check_scope` (`resolved_scope.scope_kind == "UNSUPPORTED"`) BEFORE `tenants.route_for` is ever
reached -- proving nothing about this order's fix. FIRM_OPERATIONS reaches `route_for` via the
firm's DIRECTORY population instead (all 3 populated: 4576/260/291 entries), independent of the
ownership-map gap.

**Full lifecycle, one epoch per firm** (K1 + K1b created, login, one scoped GET, rollback, all
verified, script committed `ed99b373f0`):

- **49financial:** HTTP 200, class SERVED, `coverage.route` = `{firm_id: fir_c9fc04650e2134d6ea033da2,
  firm_name: 49 Financial, provider: BLACK_DIAMOND, host: bd3.bdreporting.com, ...}`. TenantRoute
  resolved; NOT DEPENDENCY_UNAVAILABLE.
- **cottonwood:** HTTP 200, class SERVED, `coverage.route` = `{firm_id: fir_0fe2a06331f1b4a68133fcb2,
  firm_name: Cottonwood, provider: BLACK_DIAMOND, host: bd3.bdreporting.com, ...}`. TenantRoute
  resolved; NOT DEPENDENCY_UNAVAILABLE.
- **inflection:** HTTP 200, class UNEXPECTED, code UNEXPECTED, firm_id ABSENT, route None -- an
  UNRELATED, OUT-OF-BOUND cause: `_authz/served.py::enforcer_for` constructs its `Context` with an
  EAGER, UNCONDITIONAL `load_ownership(tenant)` call (`:590`) BEFORE `tenants.route_for` is ever
  reached, and inflection's ownership map is absent from S3 -- entirely outside this order's
  `performance/tenants.py` + `_ids/` bound. **Confirmed NOT DEPENDENCY_UNAVAILABLE** (the FWD-2
  signature this order's criterion names as the truthful-FAIL condition). Route resolution for
  inflection is separately proven: the first-pass in-process battery (`battery_ib_rtg_3.py`, already
  PASS, committed `eee9094d47`) resolves a TenantRoute for inflection's opaque id directly, and this
  pass's deployed-bytes check confirms the SERVED `tenants.py` is byte-identical (sha256
  `dbefe40e3c0d1f835f45783e5175f9816d8dc6654ab3e4b4e31c25fb7066a647`) to that same reviewed,
  in-process-tested source. Filed as row `IRPT_BCKEND-W3-S50`, committed `92432e89a7`, routed to
  `2.0.0_SA_COO~B` (the issuer), same pattern as `IRPT_BCKEND-W3-S48`.

**Lifecycle closed cleanly for all 3** (K1/K1b deleted and verified, refresh refused, 401 after exp,
no residue -- both before/after prefix scans read 0).

**Deployed-bytes check (0 fourth-id-space literals):** served zip re-downloaded and re-hashed
(`W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`, EQUAL to metadata); extracted `tenants.py`'s
`ROUTES` dict carries **0 bare string-literal keys** -- every key is `_LEGACY_SHORT_ID[...]`, itself
`_ids.opaque_firm(<canonical id>)`, never a hand-typed fourth spelling. The 3 `_LEGACY_SHORT_ID`
readability aliases (`49F`/`COT`/`INF`) are present but never consulted by `route_for`.

**R74-AC1 verdict: PASS.** The specific defect this criterion names (FWD-2: `route_for` raising
`UnknownTenant` -> `DEPENDENCY_UNAVAILABLE`) is conclusively absent for all 3 registry firms --
proven live end-to-end for 2 of 3, and via in-process battery + deployed-bytes identity for the
third, whose live path is blocked by an unrelated, disclosed, out-of-bound cause never producing the
FWD-2 signature.

## Related, out-of-bound findings (not fixed, filed)

- `IRPT_BCKEND-W3-S48` (first pass): `handler.py`'s `RECORDED_LABELS` still keyed on the retired
  spelling -- a served request under the default `recorded` transport mode returns a graceful
  NO-CAPTURE absence. Disclosed and explicitly not an R74-AC1 failure per this order's own text.
- `IRPT_BCKEND-W3-S49` (this pass): the arm-(d) subtraction gate's `last_modified` corollary.
- `IRPT_BCKEND-W3-S50` (this pass): inflection's `_authz/served.py` eager ownership-map load,
  detailed above.

Peak free space observed: ~27GB throughout (private plugin cache pre-populated, ~704MB, no
re-download; the disk-fallback plan never triggered).
