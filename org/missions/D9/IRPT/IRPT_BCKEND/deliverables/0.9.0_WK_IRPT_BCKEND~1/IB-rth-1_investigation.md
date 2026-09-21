# IB-rth-1 INVESTIGATION -- the inflection serving route, rectified within Andrew's terms

**Worker:** `0.9.0_WK_IRPT_BCKEND~1`. **Cell:** `IB-rth-1` (round 8). **Date:** 2026-09-21.

All commands run `timeout`-bounded from worktree `/c/tmp/wk-irpt-8-1` (branch `wk-irpt_bckend-8-1`), as
`arn:aws:iam::313476888478:user/Andrew_Berman` unless stated otherwise.

---

## 1. THE FACE'S OWN PREMISE IS PARTLY STALE -- MEASURED, NOT ASSUMED

The face (and round-7's `W3-S50`) both name **`opal-data-inflection`** as "the locked bucket (FWD-11)."
**Measured: that is a DIFFERENT bucket from the one the serving path actually reads.**

- `data/firm_registry.json` (HEAD): `inflection -> bucket "opal-data-inf"` (three-letter legacy code,
  same shape as `49financial -> opal-data-bd`, `cottonwood -> opal-data-cot`).
- Live deployed env var, `irpt-performance-adapter`: `IRPT_DIRECTORY_BUCKET_MAP =
  {"49financial":"opal-data-bd","cottonwood":"opal-data-cot","inflection":"opal-data-inf"}` -- **EQUAL** to
  the registry.
- `opal-data-inflection` and `opal-data-cottonwood` are a SEPARATE pair of buckets
  (`aws s3api list-buckets`: both `CreationDate 2026-09-18T20:05:17Z`, same second, one apply -- the D14
  full-name migration per box memory `project_legacy_firm_buckets_are_the_active_channels_until_the_d14...`),
  carrying an **explicit Deny** resource policy (`get-bucket-policy --bucket opal-data-inflection` ->
  `AccessDenied ... with an explicit deny in a resource-based policy`, even for `Andrew_Berman` --
  row `IRPT_BCKEND-S107`-adjacent evidence, INVESTIGATION_v1.md:7178). **Nothing in the live serving path
  reads `opal-data-inflection` at all.**
- `opal-data-inf`'s own bucket policy (`get-bucket-policy --bucket opal-data-inf`, this session): two `Allow`
  statements for a CloudFront OAI and a CloudFront distribution on `gold/*` -- **no Deny statement, and
  Andrew_Berman can read the policy at all** (unlike `opal-data-inflection`). **`opal-data-inf` is not
  locked.**

**So FWD-11's "locked bucket" is real, but it is a DIFFERENT bucket than the one blocking this route.** The
live blocker is entirely inside `opal-data-inf`, which is open, active, and already the one the code reads.
This correction is filed as a surprise row (S111, below) rather than edited into the face.

---

## 2. (a)(i) -- REPRODUCE THE LIVE FAILURE

Round-7's own live proof (`IB-rtg-3_arm_e_live_proof_output.txt`, already committed) already reproduced it
under the deployed role via a real HTTP request: inflection's scoped performance request -> HTTP 200,
`class UNEXPECTED code UNEXPECTED firm_id ABSENT route None`, while 49financial and cottonwood both resolved
SERVED with `coverage.route` populated. CloudWatch for that invocation carries `START/END/REPORT` only, no
`ERROR`/traceback line -- consistent with `served.py:601-630 handle()`'s `except Exception` classifying any
unhandled exception `UNEXPECTED` and calling `_errors.record_internal(None, cid, operation, exc)` with
**`sink=None`**, which (measured, `errors.py:191-192`: `if sink is not None: sink(record)`) means the
record dict is built and **discarded, never logged anywhere** -- so the exception's class/message is
genuinely unobservable from CloudWatch, by design of the current code. This investigation does not re-run a
live HTTP request (arm (a) is READ-ONLY); it reproduces the WIRE CONDITION directly (section 3) and confirms
the code path independently (section 5).

---

## 3. (a)(ii)+(iii) -- WHERE THE MAP IS EXPECTED, WHETHER IT EXISTS, AND THE EXACT WIRE ERROR

**Bucket + keys, measured directly (`.tools/aws s3api head-object`, this session, as Andrew_Berman):**

| object | bucket | key | result |
|---|---|---|---|
| directory pointer | `opal-data-inf` | `investor-reporting/directory/latest.json` | 270 bytes, `LastModified 2026-09-18T09:02:14Z` -- **PRESENT** |
| directory artifact | `opal-data-inf` | `investor-reporting/directory/2026-09-17/directory.json` (from the pointer's `key`) | 447976 bytes -- **PRESENT** |
| **ownership map** | `opal-data-inf` | `platinum/inflection/ownership_map.json` | **404 Not Found (HeadObject)** |

So `enforcer_for`'s `load_directory(tenant)` call (`served.py:574`) succeeds cleanly for inflection; the
directory artifact and its `firm_id_opaque` are readable. **The failure is isolated to `load_ownership`.**

**THE EXACT WIRE ERROR, three separate measurements, not a constructed stub:**

1. **My own identity's `GetObject`** (broad permissions, includes `ListBucket` elsewhere) on the missing key:
   `boto3 s3.get_object(Bucket='opal-data-inf', Key='platinum/inflection/ownership_map.json')` ->
   `NoSuchKey`, class name `NoSuchKey`, message *"An error occurred (NoSuchKey) when calling the GetObject
   operation: The specified key does not exist."* -- `response.Error.Code = NoSuchKey`.
2. **The deployed role's actual IAM shape, read directly (not inferred):** `iam get-role-policy
   --role-name irpt-performance-adapter-role --policy-name irpt-performance-adapter-ownership-map-read-policy`
   -> `{"Action":["s3:GetObject"],"Effect":"Allow","Resource":["arn:aws:s3:::opal-data-bd/platinum/
   49financial/ownership_map.json","arn:aws:s3:::opal-data-inf/platinum/inflection/ownership_map.json",
   "arn:aws:s3:::opal-data-cot/platinum/cottonwood/ownership_map.json"]}` -- **`s3:GetObject` only, on the
   exact key, per the CTO's S90 ruling ("Never `ListBucket`")**. `iam simulate-principal-policy` for
   `s3:ListBucket` on `opal-data-inf` for this role -> **`implicitDeny`** (confirmed against the role's own
   policy text above, so this is not a simulate-without-resource-policy false-negative: there is no
   `ListBucket` statement to miss).
3. **The discriminating wire call: a session scoped to EXACTLY this role's grant shape** (`sts
   get-federation-token` under the SAME identity, `Policy={"Effect":"Allow","Action":"s3:GetObject",
   "Resource":"arn:aws:s3:::opal-data-inf/platinum/inflection/ownership_map.json"}` -- a temporary,
   same-principal, reduced-privilege session, NOT a new IAM principal and NOT an assumed role) attempting
   `GetObject` on the same missing key:
   ```
   AccessDenied (HTTP 403): An error occurred (AccessDenied) when calling the GetObject operation: User:
   arn:aws:sts::313476888478:federated-user/ib-rth-1-wiretest2 is not authorized to perform: s3:ListBucket
   on resource: "arn:aws:s3:::opal-data-inf" because no session policy allows the s3:ListBucket action
   ```
   **This is the EXACT wire shape the deployed role sees**, because the deployed role's policy is the SAME
   `GetObject`-only, no-`ListBucket` shape (measurement 2). `sts:AssumeRole` on the role itself was tried
   first and refused (`AccessDenied: User: .../Andrew_Berman is not authorized to perform: sts:AssumeRole`),
   confirming the root-console/impersonation door is genuinely closed, consistent with Andrew's own terms --
   the federation-token route was used instead because it mints no new principal and reuses the existing
   identity's session only.

**VERDICT: 403 AccessDenied, not 404 NoSuchKey, not an explicit bucket-level Deny.** S3 masks the existence
of a key from a caller holding `GetObject` but not `ListBucket` on that resource -- documented AWS S3
behaviour, now measured directly rather than assumed.

---

## 4. (a)(iii) -- THE DISCRIMINATING CALL: read the CODE that receives this error

`infra/aws/lambda/investor-reporting/_authz/loaders.py::load_ownership` (HEAD, before this cell's edit):

```python
try:
    artifact = _get_json(bucket, key, s3)
except Exception as exc:
    if exc.__class__.__name__ in ("NoSuchKey", "ClientError") and "NoSuchKey" in str(exc):
        artifact = {"schema_version": 1, "advisors": {}}
    elif exc.__class__.__name__ == "NoSuchKey":
        artifact = {"schema_version": 1, "advisors": {}}
    else:
        raise
```

Both branches match only `NoSuchKey`-shaped exceptions. An `AccessDenied` exception (class name
`AccessDenied`, `"NoSuchKey"` NOT a substring of its message) matches neither branch and is **re-raised**,
propagating out of `enforcer_for` uncaught, caught by `served.py::handle()`'s `except Exception`
(`:626-630`), classified `UNEXPECTED` because it is not an `_enforce.AuthzError`. **This is the entire
mechanism**, and it matches row `IRPT_BCKEND-S94`'s mechanism exactly (REMEDIATION_v1.md:3868, filed by
`0.7.0_AE_CloudOps~V` at round 6, GRADUATED, `disarm_owner: 2.0.0_SA_COO~B`, still `ARMED`).

**The object CANNOT be produced/read on the existing bucket via a code-side fix alone with certainty about
existence** -- S3's masking is deliberate and by design (it exists precisely so a `GetObject`-only caller
cannot learn whether a key exists). What CAN be established, and is: **the caller's policy is scoped to
exactly one ARN**, so an `AccessDenied` on that exact key, given that policy, is either (i) the key is
absent, or (ii) the one-statement grant was itself removed (an infra defect the census arms, not this
loader, are the control for). This is the basis for the rectification below.

---

## 5. BRANCH: B1, code-only, a NEVER-WIDEN act -- PACKET PRODUCED, STOP BEFORE APPLY

**Two other B1 sub-branches were considered and ruled out, on evidence, before landing here:**

1. **Grant `s3:ListBucket`** to the serving roles (restoring the informative 404). **BARRED by existing
   ruling**: `CTO_RULING_IRPT_BCKEND_S90_OWNERSHIP_MAP_GRANT_20260919.md` -- *"An OBJECT-SCOPED
   `s3:GetObject` per serving role on EXACTLY `arn:...ownership_map.json` ... Never `ListBucket`."* This
   worker does not re-open a standing CTO ruling.
2. **Populate `platinum/inflection/ownership_map.json`** (even an empty map) via "the estate's existing
   producer path" (the face's own DELTA=0 carve-out). **Measured: no such producer exists.** `data/inf/`'s
   gold pipeline (`data/inf/scripts/gold/*.py`, full listing read) has no `ownership_map`-producing script,
   unlike cottonwood/black_diamond's `D_00.portal_aggregates.py::build_advisor_ownership_artifact`.
   `data/assets/scripts/gold/investor_reporting/` carries only `directory_runner.py` and
   `holdings_snapshot.py` -- no ownership-map producer there either. Hand-authoring the object's content
   would assert a FACT about inflection's advisor roster this worker has no standing to assert (the prior
   packet's own author reached the same conclusion: `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md` s.8, "the
   recommendation that the producer publish an empty map ... is pitched to `1.0.0_SA_CTO`" -- never ruled).
   This path is also outside this order's `<paths>` grant (`data/inf/` is not listed). **Not this branch.**

**LANDED: a minimal, scoped code fix in `_authz/loaders.py::load_ownership`**, extending the existing,
already-designed "absent map is an empty map" behaviour to recognise the SECOND wire shape S3 actually
returns under the CTO-ruled, `ListBucket`-free grant. Full diff and reasoning: the committed file itself
(section 6) and the packet (`NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md`, this deliverables folder).

**This changes a SERVED property** (the live authorization boundary's behaviour on an `AccessDenied`
response) and is treated as a never-widen act per the face's own bound: **the source is committed, verified
in-process against the REAL measured wire shapes (section 3) and the FULL existing `_authz` test suite (141
of 141 passed, no regression), but NOT built into the Lambda build store and NOT deployed.** No Terraform
plan was taken against a changed artifact; no `safe-apply` was run; no change-management ledger was opened
(none is owed yet -- the bound only requires one "opened before any apply," and no apply has been attempted).

**STOPPING HERE.** The subtraction gate, the build/deploy, arm (d) (halves-at-HEAD check) and arm (e) (the
live proof under deployed bytes) are **not run** by this cell. `R76-AC1` cannot PASS -- it needs the deployed
role + bytes, and nothing is deployed. It is recorded `DISCLOSED-INCOMPLETE` with this carry named.

---

## 6. WHAT WAS COMMITTED

- `infra/aws/lambda/investor-reporting/_authz/loaders.py` -- the fix (section 4/5). Compiles
  (`py_compile`), passes `ds-precommit-check.py` (rc=0), and the full `_authz/tests/` suite: **141 of 141
  passed**, no failures, no regressions (`pytest infra/aws/lambda/investor-reporting/_authz/tests/ -q`).
- `battery_ib_rth_1_code_verify.py` (this deliverables folder) -- an in-process verification over the REAL
  measured wire shapes from section 3 (never a fabricated exception class): (1) `NoSuchKey` still resolves
  empty (the pre-existing case, unchanged); (2) `AccessDenied` with the EXACT live-measured message now
  resolves empty (the fix); (3) a NEGATIVE CONTROL, a genuinely different failure (`InternalError`, 500),
  **still raises** -- the fix is narrow, not a blanket swallow; (4) a POSITIVE CONTROL, a present map, reads
  through unchanged. **4 of 4 PASS**, token `IB-RTH-1-LOADERS-FIX-VERIFIED`, output
  `IB-rth-1_code_verify_output.txt`.
- `NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md` (this deliverables folder) -- the packet for `1.0.0_SA_CTO` +
  `2.0.0_SA_COO~B`. Nothing built, nothing applied.

## 7. SURPRISE ROW FILED

`IRPT_BCKEND-W1-S46` (INVESTIGATION_v1.md; this section previously misstated the id as `S111` --
corrected on resume-and-verify by the same worker slot, `0.9.0_WK_IRPT_BCKEND~1`, before commit;
the FILED row's id was always `S46`, confirmed the true next-unused id: 43 rows at this worker's
committed HEAD, max existing number 45): the face's premise names `opal-data-inflection` as the
locked bucket; the live serving path reads `opal-data-inf`, which is not locked -- see section 1.
`ARMED`, `disarm_owner: 2.0.0_SA_COO~B` (the face's own issuer, same pattern as `W3-S50`/`S94`).

## 8. WHAT ROUND 8 STILL OWES

1. `1.0.0_SA_CTO` + `2.0.0_SA_COO~B` sign the two packet halves at this commit's blob (or refuse/amend).
2. On signature: build `_authz/loaders.py` into the 7 serving functions' zips that stage it (measured,
   `infra/aws/lambda/ci/lambda-source-map.json`: `irpt-performance-adapter`, `irpt-directory-search`,
   `irpt-narrative`, `irpt-ycharts-generate`, `irpt-export-render`, `irpt-holdings`, `irpt-status` -- **7 of
   7**; `irpt-intake-poller` and `irpt-directory-refresh` do NOT stage it), open a change-management ledger,
   `safe-apply` per root, then run `battery_ib_rth_1.py` (arm (e), the deployed-role live proof) for
   `R76-AC1`.
