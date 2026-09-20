# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtg-3: the performance route reconciles to the bound id space

**For:** the two halves required before IB-rtg-3 applies anything (CLAUDE.md never-widen: CTO +
COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.

**Prepared by:** `0.9.0_WK_IRPT_BCKEND~3` (`IRPT_BCKEND.TO-IB-rtg-3`, first pass, face status line
and `<paths>` @8ba74b3130423f6d1ca7ce4e5f2b24bb82dc8664).

**Supersedes:** nothing. First packet for this cell.

**Executes:** the order's own bound -- reconcile `performance/tenants.py`'s `route_for` to the id
space the boundary binds on, using the estate's existing `_ids` normalizer, confined to
`performance/tenants.py` (no new lookup table minted -- the STOP-and-ROW branch did not fire).

**NOTHING IS APPLIED BY THIS PACKET.** The source edit is committed on this worker's branch
(`wk-irpt_bckend-7-3`) and the rebuilt artifact is uploaded to the artifact store; no Terraform
apply has run and the live `irpt-performance-adapter` function is UNCHANGED. Line citations are
at `@60e232e9b2ef79e2ebe23913a85ac4d1d28bed4b` unless another vintage is given.

A half signs the **blast radius** of the act: what each key may touch, and the rollback for each
key. It does not sign an intention.

---

## 0. comp-iam and the never-widen scope

This order's own preflight: `comp-iam: DECLARED-NOT-APPLICABLE -- a source reconciliation under
the function's existing role; no grant change (if the fix needs a new firm-token mapping the
order STOPs and ROWs for the CTO, and no deploy runs).` The fix did NOT need a new mapping (arm
(a)/(b) below), so there is **no K-OM / K-DIR / K-ENV key in this packet** -- only **K-CODE**, the
one function's rebuilt bytes. The function's role (`irpt-performance-adapter-role`), environment
and every other Terraform resource are untouched by this edit.

---

## 1. The registry vintage (arm (a): re-derived LIVE, never inherited from round 6)

The grant is derived from `data/firm_registry.json` at HEAD (`60e232e9b2`); the ORIGINAL W2-S27
finding named `F-49F`/`F-COT`/`F-INF` as a third, hand-invented spelling. Re-run this pass,
`_ids.firm_ids()` (the registry read, `kind == "client" && enabled`) returns:

REGISTRY-FIRM-COUNT: 3 -> ('49financial', 'cottonwood', 'inflection')

This is the SAME 3 the round-6 finding named, MEASURED LIVE this pass (battery output line 4,
cited in section 9), not carried forward from the round-6 analysis.

---

## 2. The defect and the fix (arms (a)/(b))

- **Cause, confirmed:** `performance/tenants.py:81,91,101` (pre-fix) keyed `ROUTES` on
  `F-49F`/`F-COT`/`F-INF`; `_authz/enforce.py:Enforcer.resolve_now` (`:277-278`) overwrites
  `headers["x-firm-id"]` with `FirmBinding.opaque_firm_id` (the directory's declared `fir_...`
  id) BEFORE `_scope.resolve` runs, so `handler.py:79-80`'s `route_for(firm_id)` always received
  the OPAQUE id and raised `UnknownTenant` -> `DEPENDENCY_UNAVAILABLE` (`entry.py:117`) on every
  real request. FWD-2, row IRPT_BCKEND-W2-S27.
- **The fix, confined to `performance/tenants.py`:** `ROUTES` is now keyed on the SAME opaque id,
  computed via the estate's ONE normalizer `_ids.opaque_firm(canonical_firm_id)` for each of the
  3 registry client firm ids (section 1) -- never a new, hand-typed fourth spelling. The retired
  short labels (`F-49F`/`F-COT`/`F-INF`) survive only as `tenants._LEGACY_SHORT_ID`, a readability
  alias this module's own tests use; `route_for` never reads it.
- **The STOP-and-ROW branch did NOT fire.** A clean reconciliation was possible with the existing
  normalizer, so no row was filed under the FirmBinding/W2-S9 axis for a missing mapping.
- **A related, OUT-OF-BOUND finding WAS filed** (row `IRPT_BCKEND-W3-S48`): `handler.py`'s own
  `RECORDED_LABELS` dict is ALSO keyed on the retired spelling, and reconciling only `tenants.py`
  (per this order's bound) leaves that lookup unreachable by any real opaque firm id -- a served
  request under the DEFAULT `recorded` transport mode now returns a NO-CAPTURE absence rather
  than DEPENDENCY_UNAVAILABLE. **This packet's own criterion (R74-AC1, route resolution, no
  DEPENDENCY_UNAVAILABLE) is unaffected** -- the finding is about a DIFFERENT, downstream outcome
  (whether captured evidence is found), filed rather than fixed because fixing it would touch
  `handler.py`, outside this order's "confined to tenants.py" bound.

---

## 3. K-CODE: `irpt-performance-adapter` rebuilt from HEAD (1 function) -- BUILT, NOT APPLIED

- **What it is.** The `tenants.py` reconciliation (section 2), deployed by rebuilding
  `irpt-performance-adapter`.
- **The prior LIVE state, read before the build (the ROLLBACK SOURCE):**
  `CodeSha256 IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=` (169955 bytes), held in the artifact
  store at `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-performance-adapter.zip`
  version `38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF` (uploaded 2026-09-19T15:58:45Z). Confirmed by
  `head-object` on that exact version: `content-sha256` metadata equals the live `CodeSha256`
  exactly (`aws lambda get-function-configuration` read live, 2026-09-20).
- **The build:**
  - command: `bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter`,
    from worktree HEAD `eee9094d47` (the source-edit commit; `infra/aws/lambda/` was clean before
    the build per the script's own gate);
  - result: rc=0, import-closure gate passed, no ADVISORY beyond the pre-existing undeclared
    `keys` layer dependency (unrelated to this edit, no `BUILD_MANIFEST.json` on this function).
  - BUILT-SHA256: `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`
  - BUILT-VERSION: `M0E32HJhwg54I6jcU4g2e58Ktthey_51` (171542 bytes, uploaded
    2026-09-20T15:27:03Z).
- **Verified at rest:**
  - `head-object` (no version pinned) reads the LATEST version id == `M0E32HJhwg54I6jcU4g2e58Ktthey_51`,
    `content-sha256` metadata == `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`;
  - the object was RE-DOWNLOADED and re-hashed independently of the metadata claim:
    `openssl dgst -sha256 -binary <downloaded> | base64` == `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`
    (matches both the metadata and `lambda-source-map.json`'s updated `artifact_sha256`, committed
    @60e232e9b2);
  - **the served-byte delta is EXACTLY the edit.** The prior live zip (version
    `38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF`) and the newly built zip were both downloaded and
    extracted: **23 of 23 members present in both; exactly 1 member differs, `tenants.py`**
    (prior sha256 `1238f6701b8aae45727194342e00e8a5c3f7793de10436d0f0b20a67e5f5ba90`, new sha256
    `dbefe40e3c0d1f835f45783e5175f9816d8dc6654ab3e4b4e31c25fb7066a647`). The new zip's
    `tenants.py` hashes IDENTICALLY to the worktree's committed `tenants.py` at HEAD
    (`dbefe40e...`, same command run on both), so what shipped is what was reviewed. Every other
    member (`handler.py`, `entry.py`, `served.py`, `enforce.py`, `errors.py`, `resolve.py`,
    `loaders.py`, `ids.py`, `firm_registry.json`, `raw_keys.json`,
    `data/custodian_key_seam.json`, `bd_adapter.py`, `normalize.py`, `orion_adapter.py`,
    `transport.py`, `units.py`, the 5 `fixtures/*` files) is byte-identical between the two zips.
- **No new IAM name, no environment change, no other function's bytes.** Section 0.

PACKET-KEYS: K-CODE 1 (K-OM 0; K-DIR 0; K-ENV 0)

---

## 4. Writers of each named property (the declared plane)

| property | W | declared writers |
|---|---|---|
| `irpt-performance-adapter` served code | 1 | `module.irpt_performance_adapter` (the performance root), which reads the artifact store's latest version and its `content-sha256` |
| `lambda-source-map.json` `artifact_sha256` for this function | 2 | `build-and-upload.sh` (pre-apply, the built sha -- this commit) and `record-terraform-deploy.sh:748-768` (post-apply, via `comp-lambdamap reconcile-deployed`, reconciled to the deployed `CodeSha256`). Neither is a rollback source; the rollback source is the artifact store's versioned object (section 3) |
| `irpt-performance-adapter-role` | 0 (unchanged) | this order makes no IAM change (section 0) |

**The qualifier the count cannot remove** (the estate's standing bar): a console or CLI write to
the function's configuration or the build store is physically possible and cannot be enumerated.
It is banned by NEVER-9, and a ban is not a census. `W` counts the declared plane; the rollback's
own re-read (section 3) covers the rest.

---

## 5. The plan, taken and NOT applied

`terraform plan -refresh=false` on `infra/aws/terraform/investor-reporting/performance`
(init'd fresh in this worktree, 2026-09-20):

```
module.irpt_performance_adapter.aws_lambda_function.this will be updated in-place
  ~ s3_object_version   = "38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF" -> "M0E32HJhwg54I6jcU4g2e58Ktthey_51"
  ~ source_code_hash    = "IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=" -> "W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA="
Plan: 0 to add, 1 to change, 0 to destroy.
```

PLAN-ROOTS: 1 of 1 planned (the performance root; no other root reads this function's artifact
key, so no other root is touched by construction); destroy 0 of 1; changes 1.
PLAN-CODE-CHANGE-ADDRESS: `module.irpt_performance_adapter.aws_lambda_function.this`
`IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=` -> `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`

The plan file was saved OUT OF THE REPO (`/tmp/ib_rtg3.plan` on this device) and is NOT applied by
this packet. Any different plan at the apply -- a different digest, a second address, or any
`to destroy` -- is a STOP and a re-cut, never an apply.

---

## 6. The blast radius, both branches

**BRANCH -- APPLIED (K-CODE only):**
- `irpt-performance-adapter`'s served bytes move to the built zip; the ONLY functional change is
  `route_for`'s key space (section 2). Every other module in the zip is byte-identical (section
  3), so `check_scope`, the BD/Orion adapters, `normalize`, `transport` and the `_authz`/`_scope`
  boundary behave exactly as before.
- **What becomes reachable:** an authorized, scope-resolved request for each of the 3 registry
  firms resolves a `TenantRoute` instead of raising `UnknownTenant` -- the FWD-2 defect closes.
- **What does NOT become reachable:** no new IAM grant, no new bucket, no new route, no other
  function's bytes (section 0, section 3's byte-identical members).
- **The related NO-CAPTURE consequence (row W3-S48):** under the default `recorded` transport
  mode, a served request for any of the 3 firms returns a NO-CAPTURE absence rather than the
  captured-evidence replay OR DEPENDENCY_UNAVAILABLE, because `RECORDED_LABELS` (`handler.py`,
  untouched by this edit) cannot match the opaque id. This is a WEAKER failure mode than the
  order's own target defect (a graceful absence with a stated reason, never an exception, never a
  cross-firm read) and it is disclosed, not hidden.

**BRANCH -- NOT APPLIED (this packet's actual current state):**
- The live function keeps serving `CodeSha256 IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=`; FWD-2
  (`UnknownTenant`/`DEPENDENCY_UNAVAILABLE` on every real performance request) stands unchanged.
- The built artifact and this packet sit ready for the next pass.

**ROLLBACK, per key:**
- **K-CODE:** re-publish the prior live `CodeSha256 IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=`
  through Terraform. Its bytes are at artifact-store version
  `38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF`, verified present and equal (section 3). Re-point the
  artifact-store object's latest pointer (or reference the version explicitly) and
  `.tools/safe-apply.sh` the performance root. Never `update-function-code`. Verify
  `get-function-configuration` `CodeSha256 == IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=`
  afterward.
- **The served behaviour on rollback:** `route_for` raises `UnknownTenant` again on a real
  request's opaque id -- the pre-fix FWD-2 state, not a NEW hazard.

---

## 7. The identity line, per arm (the standing bar)

| arm | claims a SERVED behaviour? | runs as |
|---|---|---|
| (a) measure, (b) source edit + build, (c) packet, (d)'s plan-take (not applied) | **No.** A registry read, a source edit, a build, an artifact-store read and a plan are claims about configuration and an artifact at rest, never about a served path. | the operator identity this worker's session holds (`aws sts get-caller-identity`, `arn:aws:iam::313476888478:user/Andrew_Berman`, the same identity every AWS read in this packet ran as) |
| (e) the live proof | Not reached this pass (halves ABSENT, section 8). | would run as the function's own execution role once applied |

**No arm in this packet certifies a served path.** The battery (section 9) exercises the real
`tenants`/`_ids`/`_scope`/`_authz.enforce` modules IN-PROCESS, never a copy, but that is still not
a served-path claim.

---

## 8. What this packet does NOT cover

1. **Row `IRPT_BCKEND-W3-S48`'s remedy** (reconciling `handler.py`'s `RECORDED_LABELS`), routed to
   `2.0.0_SA_COO~B` as this order's issuer.
2. **Any code other than `tenants.py`:** every other member of the zip is byte-identical
   (section 3); no `_authz/`, `_scope/`, `_keys/` or `_ids/` change; no other function rebuilt.
3. **Any IAM, environment or route change** (section 0).
4. **The apply itself** -- section 5's plan is TAKEN and NOT applied.

---

## 9. What the halves sign against

This file's blob. Each half names that blob:
- `NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtg-3_*.md` (`org/tier1_exec/2.0.0_SA_COO~B/deliverables/`);
- `NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtg-3_*.md` (`org/tier1_exec/1.0.0_SA_CTO/deliverables/`).

**Battery cited:**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-rtg-3_R74-AC1_battery_output.txt`
(`battery_ib_rtg_3.py`, this run, PASS: `IBR74-PERFORMANCE-ROUTE-RESOLVES-EACH-FIRM`).

If either half is ABSENT, arm (d) STOPS; that is the EXPECTED first-pass outcome (this order's
own status line). The next pass runs (d)/(e).

**At the apply, (e) re-verifies BEFORE any `safe-apply`:**
- the registry blob EQUAL to section 1's read;
- the built sha EQUAL to section 3's (`W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=`) at the
  artifact store's latest version for this key;
- the plan's canonical shape EQUAL to section 5 (0 add, 1 change, 0 destroy, this one address).

Any difference is a STOP and a re-cut, never an apply.
