# NEVER-WIDEN SIGN-OFF PACKET -- IB-rth-1: `_authz/loaders.py::load_ownership` recognises the
AccessDenied-masking wire shape as an absent ownership map, the same as NoSuchKey

**For:** the two halves required before this cell applies anything (CLAUDE.md never-widen: CTO + COO):
`1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.

**Prepared by:** `0.9.0_WK_IRPT_BCKEND~1` (`IRPT_BCKEND.TO-IB-rth-1`, first pass).

**Supersedes:** nothing. First packet on this cell.

**Executes:** the disposition of row `IRPT_BCKEND-S94` (REMEDIATION_v1.md, GRADUATED round 6, `ARMED`,
`disarm_owner: 2.0.0_SA_COO~B`) and its round-7 restatement `IRPT_BCKEND-W3-S50`. Both name the same
mechanism this packet fixes.

**NOTHING IS APPLIED BY THIS PACKET.** The source is committed on the branch. It is NOT built into the
Lambda build store and NOT deployed. No Terraform plan was taken against a changed artifact. No
change-management ledger is opened (none is owed until an apply is attempted).

A half signs the **blast radius**: what the key may touch, and the rollback. It does not sign an intention.

---

## 0. Why this is the only surviving B1 option (evidence, not judgment)

Two other rectifications of the EXISTING bucket (`opal-data-inf`, not the unrelated, genuinely-locked
`opal-data-inflection` -- see `IB-rth-1_investigation.md` section 1 and row `IRPT_BCKEND-W1-S46`) were
considered and ruled out on measured evidence:

1. **Grant `s3:ListBucket`** to the affected roles, restoring the informative 404. **BARRED**:
   `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_BCKEND_S90_OWNERSHIP_MAP_GRANT_20260919.md` --
   *"An OBJECT-SCOPED `s3:GetObject` per serving role on EXACTLY `arn:...ownership_map.json` ... Never
   `ListBucket`."* This worker does not re-open a standing ruling.
2. **Populate the object** via an existing producer path (the face's DELTA=0 carve-out). **Measured
   absent**: `data/inf/scripts/gold/` (full listing) carries no `ownership_map`-producing script, unlike
   cottonwood's/black_diamond's `D_00.portal_aggregates.py::build_advisor_ownership_artifact`;
   `data/assets/scripts/gold/investor_reporting/` carries only `directory_runner.py` and
   `holdings_snapshot.py`. Hand-authoring the object asserts a fact about inflection's advisor roster this
   worker has no standing to assert, and the prior packet's own author reached the same conclusion
   (`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md` s.8: "pitched to `1.0.0_SA_CTO`", never ruled). Also outside
   this order's `<paths>` grant.

**What remains: the CODE that receives S3's answer.** `_authz/loaders.py::load_ownership`'s own docstring
already declares the INTENT -- "An ABSENT map is an EMPTY map" -- and the existing exception handler already
implements that intent for ONE of the two wire shapes S3 can return for "absent" under the CTO-ruled,
`ListBucket`-free grant. This packet extends the recognised shape set; it changes no grant, no bucket
policy, no resource.

---

## 1. The measured mechanism (full derivation: `IB-rth-1_investigation.md` sections 2-4)

- The deployed role (`irpt-performance-adapter-role`, and by the same inline-policy shape every other
  serving role) holds `s3:GetObject` on exactly `arn:aws:s3:::opal-data-inf/platinum/inflection/
  ownership_map.json` -- read directly via `iam get-role-policy`, not inferred -- and **no**
  `s3:ListBucket` anywhere on `opal-data-inf` (`iam simulate-principal-policy` -> `implicitDeny`, and the
  role's own policy text, read above, has no such statement to miss).
- `platinum/inflection/ownership_map.json` does not exist (`head-object` -> 404 to an identity that DOES
  hold `ListBucket`).
- **The discriminating, live wire measurement**: a temporary, same-principal, reduced-privilege session
  (`sts get-federation-token`, not a new IAM principal, not an assumed role) scoped to EXACTLY the deployed
  role's own grant shape (`s3:GetObject` on that one ARN, nothing else) attempting `GetObject` on the same
  missing key returns:
  ```
  AccessDenied (HTTP 403): ... User: arn:aws:sts::313476888478:federated-user/ib-rth-1-wiretest2 is not
  authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::opal-data-inf" because no session policy
  allows the s3:ListBucket action
  ```
  This is S3's own existence-masking behaviour for a `GetObject`-only caller, not an explicit Deny and not
  `NoSuchKey`.
- `_authz/loaders.py::load_ownership`'s exception handler (pre-fix) matched only `NoSuchKey`-shaped
  exceptions and re-raised everything else, so this `AccessDenied` propagated out of `enforcer_for`
  uncaught, was classified `UNEXPECTED` by `served.py::handle()`, and (because `record_internal` is called
  with `sink=None`, `errors.py:191-192`) left **no trace in CloudWatch** -- matching exactly what round 7's
  live proof observed (HTTP 200, `class UNEXPECTED`, `START/END/REPORT` only, no ERROR line).

---

## 2. The fix, exactly

`infra/aws/lambda/investor-reporting/_authz/loaders.py::load_ownership`, the exception branch. Before:

```python
except Exception as exc:
    if exc.__class__.__name__ in ("NoSuchKey", "ClientError") and "NoSuchKey" in str(exc):
        artifact = {"schema_version": 1, "advisors": {}}
    elif exc.__class__.__name__ == "NoSuchKey":
        artifact = {"schema_version": 1, "advisors": {}}
    else:
        raise
```

After (committed this cell; full docstring reasoning in the file itself):

```python
except Exception as exc:
    code = None
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        code = (response.get("Error") or {}).get("Code")
    if code == "NoSuchKey" or (
        exc.__class__.__name__ in ("NoSuchKey", "ClientError") and "NoSuchKey" in str(exc)
    ):
        artifact = {"schema_version": 1, "advisors": {}}
    elif code == "AccessDenied" or exc.__class__.__name__ == "AccessDenied":
        artifact = {"schema_version": 1, "advisors": {}}
    else:
        raise
```

**One new branch.** The `NoSuchKey` branch is byte-identical to before (a redundant, dead `elif` beneath it
is also untouched). Everything else in the function, and every other function in the file, is unchanged.

COMMITTED-FILE-SHA256: `0c086052e6e65d2cb411f15362862b1656bad0b2320f9756be6a32444b665765` (9779 bytes;
this session, resuming after the reboot, refreshed the file's OWN `bucket_for` GENERATED-block
marker comment to the current registry hash via `lib/opal_naming.py generate` -- the naming gate
diffs the WHOLE FILE against a fresh regen and refuses on ANY stale marker in a file it grades,
unrelated to this cell's own edit; the regenerated `bucket_for` body is BYTE-IDENTICAL, only the
marker's cited registry hash changed, confirmed by diff before applying. This cell's actual fix
-- the `load_ownership` exception branch -- is unchanged from section 2 below).

---

## 3. Verification at rest (no deploy)

- `py -3.12 -m py_compile` -- clean.
- `.tools/ds-precommit-check.py` on the file -- rc=0.
- **Full existing `_authz` test suite**: `pytest infra/aws/lambda/investor-reporting/_authz/tests/ -q` --
  **141 of 141 passed**, 0 failures. No test in the estate's own suite exercises this exact branch (there is
  no `test_loaders.py`), so this is a NO-REGRESSION result, not a positive one for the fix itself.
- **The positive/negative result, in-process, over the REAL measured wire shapes** (never a fabricated
  exception class): `deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rth_1_code_verify.py`, output
  `IB-rth-1_code_verify_output.txt`, token `IB-RTH-1-LOADERS-FIX-VERIFIED`:
  1. `NoSuchKey` (the pre-existing case) -> empty map. **OK, unchanged.**
  2. `AccessDenied`, the EXACT live-measured message from section 1 -> empty map. **OK, the fix.**
  3. **NEGATIVE CONTROL**: a genuinely different failure (`InternalError`, HTTP 500) -> still **raises**.
     **OK -- the fix is narrow, not a blanket swallow of every S3 failure.**
  4. **POSITIVE CONTROL**: a present map reads through unchanged. **OK.**
  4 of 4 hold.

---

## 4. The blast radius, both branches

**BRANCH -- BUILT AND DEPLOYED** (not done by this packet; this section covers what an apply WOULD do):

- **Which functions are touched.** `_authz/loaders.py` is a SHARED module. Measured from
  `infra/aws/lambda/ci/lambda-source-map.json` (`files[]` per function), it is staged into **7 of 7** serving
  functions: `irpt-directory-search`, `irpt-status`, `irpt-holdings`, `irpt-narrative`,
  `irpt-export-render`, `irpt-performance-adapter`, `irpt-ycharts-generate`. It is NOT staged into
  `irpt-intake-poller` or `irpt-directory-refresh` (2 of 9 total lambda-source-map entries under this
  project, neither a serving function). **An apply of this fix means rebuilding and redeploying all 7**, not
  one.
- **What changes in served BEHAVIOUR, per firm.** For 49financial and cottonwood, whose ownership map
  objects EXIST today, `load_ownership` already succeeds with a 200 and never reaches this exception
  branch -- **no observable change for either firm today.** For inflection, a request that previously failed
  `UNEXPECTED` (an opaque outage label) now resolves with an EMPTY ownership map, the same served answer an
  advisor with zero grants already receives -- i.e. the request reaches `route_for`/the scope resolver and
  is answered `EMPTY_GRANT` or the appropriate policy code, never `UNEXPECTED`, for inflection specifically.
- **The cross-firm bound holds.** The fix touches only how ONE firm's `GetObject` failure is classified; it
  reads no new bucket, no new key, and the key is still resolved by the VERIFIED tenant
  (`bucket_for`/`OWNERSHIP_KEY_TEMPLATE`, unchanged). No firm becomes reachable from another firm's request.
- **What does NOT change.** No IAM grant. No bucket policy. No Terraform resource. No environment variable.
  `directory`, `policy` and every other loader function are untouched. The dead, redundant `elif` branch for
  `NoSuchKey` is left as-is (out of this cell's minimal-diff scope).
- **The residual risk, disclosed plainly.** If a genuine misconfiguration ever REMOVED the narrow
  `GetObject` grant for a firm whose map DOES exist, S3 would answer `AccessDenied` the same way, and this
  fix would now report that as an empty ownership map (silently) rather than as an outage. This is judged
  acceptable because: (a) the grant is a single, narrowly-scoped IAM statement per firm, unlikely to be
  partially removed without the whole statement vanishing; (b) a removed grant is visible on the existing
  IAM census arms (e.g. `battery_ib_rtf_10.py` arm (a)/(e), which `simulate-principal-policy` directly, not
  through this code path) independent of any served request; (c) the alternative -- leaving inflection
  permanently `UNEXPECTED` -- is the defect this cell exists to close. **This trade-off is exactly what the
  two signing halves are asked to weigh; it is not this worker's call to make unilaterally, which is why the
  packet stops here.**

**BRANCH -- NOT BUILT / NOT DEPLOYED (the current state, and the STOP if a half refuses):**

- Inflection stays `UNEXPECTED` on every scoped request that reaches `enforcer_for`, exactly as round 7
  measured. 49financial and cottonwood are unaffected either way.
- The committed source sits on the branch, verified at rest (section 3), until a build+apply follows a
  signed packet.

**ROLLBACK, if built and applied and later reverted:**

- Revert the commit (`git revert` or an equivalent), rebuild all 7 functions via
  `infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` from the reverted HEAD, and
  `.tools/safe-apply.sh` each of the 7 terraform roots that stage the module.
- **Pre-change `CodeSha256`, read this session, the rollback target for each of the 7 functions:**

  | function | pre-change `CodeSha256` |
  |---|---|
  | `irpt-directory-search` | `76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E=` |
  | `irpt-status` | `B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=` |
  | `irpt-holdings` | `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=` |
  | `irpt-narrative` | `o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=` |
  | `irpt-export-render` | `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=` |
  | `irpt-performance-adapter` | `W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=` |
  | `irpt-ycharts-generate` | `1L60sG1G9IaFfwe+LPNdE84DarlWCHKkdE8M5CyVI8o=` |

  These are the values a rollback must reproduce (via the build store's existing versions or a re-upload of
  the reverted bytes), never `update-function-code` (NEVER-9), never the manifest as a rollback source.
- **The served behaviour on rollback**: inflection returns `UNEXPECTED` again on every scoped request, the
  same state this packet found.

---

## 5. Writers of the touched property

| property | W | declared writers |
|---|---|---|
| `_authz/loaders.py` source | 1 (this commit) | this order's own `<paths>` grant is the only one with repo write access to `infra/aws/lambda/investor-reporting/_authz/`; no other project's `<paths>` names this path (measured: this project's own decomp is the sole owner of record for this subtree) |
| the 7 functions' `CodeSha256` (if built+applied later) | per-function, `infra/aws/lambda/ci/build-and-upload.sh` + Terraform's `module.irpt_*.aws_lambda_function.this`, exactly as every prior code change in this project (e.g. `IB-rtf-10`'s K-CODE) |

**The qualifier the count cannot remove** (carried from `IB-rtf-10`'s own half): a console or CLI write to
the build store or a function's code is physically possible and cannot be enumerated; banned by NEVER-9, and
a ban is not a census.

---

## 6. The identity line, per arm (the CTO's standing bar, `CTO_RULING_IRPT_BCKEND_S90...`)

| arm | claims a SERVED behaviour? | runs as |
|---|---|---|
| section 1 (the wire measurement) | **No.** A claim about what S3 answers to a REDUCED-PRIVILEGE session mirroring the role's grant shape -- not a claim about the deployed Lambda's own served path. | `arn:aws:sts::313476888478:federated-user/ib-rth-1-wiretest2` (a temporary session of `Andrew_Berman`, printed above) |
| section 3 (py_compile, ds-precommit, pytest, the in-process battery) | **No.** Code-at-rest and in-process claims, explicitly labelled as such. | the operator identity (`Andrew_Berman`) |
| a future arm (e), if built+applied | **YES**, and per the CTO's standing bar it must run as each function's OWN execution role via a real HTTP request, never in-process. Not run by this packet. | N/A -- not reached |

**No arm in this packet certifies a served path.** That is the explicit reason `R76-AC1` is recorded
`DISCLOSED-INCOMPLETE`, not `PASS`, by this cell.

---

## 7. What this packet does NOT cover

1. **The build and the apply.** Committed source only; the build store and all 7 live functions are
   untouched.
2. **Any other code in `_authz/`, `_ids/` or elsewhere.** One function, one new `elif` branch.
3. **The residual-risk trade-off named in section 4** -- disclosed for the signers to weigh, not resolved
   here.
4. **`W1-S43`, the 110-row disposition cell, or any other round-8 cell.** This packet is `IB-rth-1` only.

---

## 8. What the halves sign against

This file's committed blob, alongside the committed `_authz/loaders.py` at
`COMMITTED-FILE-SHA256: 0c086052e6e65d2cb411f15362862b1656bad0b2320f9756be6a32444b665765`. Each half names
this packet's own blob:
- `org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rth-1_*.md`;
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rth-1_*.md`.

If either half is ABSENT, this cell's STOP stands: no build, no apply, no arm (e), and `R76-AC1` stays
`DISCLOSED-INCOMPLETE` with this packet named as the carry.
