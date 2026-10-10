# ADHOC four approved AWS deletes -- receipt

**archetype:** DEPLOY
**seat:** 0.7.0_AE_CloudOps~CTL | **issuer:** 2.0.0_SA_COO~C | **risk:** WORLD | **date:** 2026-10-10
**order:** `ADHOC.delete-retired-tfstate-orphan-loggroup-stray-demand-state-20261010`

## Authority, verified at the pin before anything was read or touched

`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261010_133xZ_FIFTEEN_OPEN_ITEMS_ANSWERED.md`
@`d02b5d81e1`, printed with `git show` **at that commit** rather than grepped for the quote. Andrew,
verbatim: **"8) agreed 9) delete 10) delete"**. The record's own item map names exactly these four targets
and routes deletes 8-10 to a laptop cloud-operations seat.

**Control on the authority read:** a bogus path at the same pin was refused, so the bytes printed are
really from `d02b5d81e1`. Item 12's "yes delete" is a dell2-local folder and is **not** in this order's
scope; nothing outside the four was touched.

## Summary

| id | target | before | delete | after | recoverable |
|---|---|---|---|---|---|
| T1 | `s3://opal-313476888478-terraform-state/canonical-schwab-si2-schedule/tfstate` | 343 B | DeleteMarker `TgO5MDjUks0JO5z2NMOxzLFjfjVMUI5Q` | 404 | **yes** -- version survives |
| T2 | `s3://opal-313476888478-terraform-state/opal-assets-absence/tfstate` | 180 B | DeleteMarker `BJQ2WUsgASOjJu.vT0pjbMd4u9YYl6iK` | 404 | **yes** |
| T3 | log group `/aws/lambda/opal-assets-absence-check` | 4,811 stored B | `delete-log-group` | describe 0 | **no** -- see below |
| T4 | `s3://opal-data-assets/bloomberg/global/silver/demand_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json` | 335 B | DeleteMarker `8CTvcswZ_LxVAl64825iWi0sHxjx27I.` | 404 | **yes** |

Deletes ran 13:56:18Z - 13:56:25Z. Four exact keys/names; no prefix delete, no wildcard, no `--recursive`.
**Both buckets are versioning ENABLED**, so T1/T2/T4 left delete markers and the object versions survive --
those three are reversible by deleting the marker. **T3 is not**: a log group carries no versioning, so its
4,811 bytes of events are gone for good. Andrew's word covered it explicitly, and the saved metadata is the
only remaining record.

## T1 -- `canonical-schwab-si2-schedule/tfstate`

- **BEFORE:** 343 B, LastModified `2026-08-04T05:12:30Z`, ETag `770ce732eb14e046a26b10b78e4f9150`,
  VersionId `G1Hy9VgQTCK_PCTJYWhQQ0eDwLx.ReWR`.
- **MATCHES:** `resources` is an **empty list** (count 0, types `[]`) -- no live infrastructure tracked.
  `version` 4, `serial` 5. Counts and types only; no values printed.
- **NO READER:** `comp-find 'canonical-schwab-si2-schedule/tfstate' infra` -> **0 hits over 12,923 files
  scanned**, denominator printed. **Positive control on the same instrument and scope:** `comp-find
  'tfstate' infra` -> **289 hits**, including the `"key": "<root>/tfstate"` backend lines of live roots, so
  the instrument demonstrably finds backend keys of exactly this shape.
- **Why the zero, read rather than inferred:** `infra/aws/terraform/canonical-schwab-si2-schedule/` holds
  **no `.tf` file at all** -- only an `org/` subdir. The directory survives as a husk; the configuration
  does not, so no backend block can name the key. (A bare `test -d` says "root present", which is literally
  true and would have been misleading on its own.)
- **SAVED:** `T1_canonical-schwab-si2-schedule_tfstate.json`, 343 B, sha256
  `e28da884cb622ed986b986cb950c42d9e81f97a5a4c84490881732ea22058a6a`.
- **AFTER:** `head-object` **404**. Control: `bd-pipeline/tfstate` in the same bucket still **200**
  (430,417 B).

## T2 -- `opal-assets-absence/tfstate`

- **BEFORE:** 180 B, LastModified `2026-07-18T01:17:42Z`, ETag `527390f6d9eba1127d6a156de8382913`,
  VersionId `Dm9SuGZIxfEG3z7WpyX3eAQk8Gm3CUlt`.
- **MATCHES:** `resources` **empty** (count 0, types `[]`); `version` 4, `serial` 3.
- **NO READER:** 0 hits for `opal-assets-absence/tfstate` over the same 12,923 files, same working control.
  The root holds no `.tf` file either -- only `.build`, a `.terraform.lock.hcl`, a stale
  `frontier-token.tfplan` and `org/`.
- **SAVED:** `T2_opal-assets-absence_tfstate.json`, 180 B, sha256
  `148b62c425737c24b48e7b75b6a5eea84d8ae4e5c0a9c4756b219d97dac4624e`.
- **AFTER:** **404**; same-bucket control **200**.

## T3 -- log group `/aws/lambda/opal-assets-absence-check`

- **BEFORE:** exact-name match, `storedBytes` 4,811, `creationTime` 1784181606310, `retentionInDays` null.
- **MATCHES (the order's STOP condition):** `lambda get-function opal-assets-absence-check` ->
  **ResourceNotFoundException**, so the group is an orphan. **Control on the same instrument:**
  `get-function` on `teams-global-chat-assist-handler-lambda` returned a name, so the not-found is a real
  absence and not a broken call.
- **SAVED:** `T3_loggroup_metadata.json`, metadata only, **no log events read**, 539 B, sha256
  `1161a2e307f26104c32c3734841fc643b9e93f891218b481a260dcada977a6d2`.
- **AFTER:** exact-name describe **0**; sibling log group describe **1**.
- **Irreversibility, stated plainly:** unlike the three S3 objects this one cannot be restored from AWS.

## T4 -- the stray `demand_state` object

- **BEFORE:** 335 B, LastModified `2026-10-09T05:10:13Z`, ETag `5c491d3e1c448dbd19e70315639238ce`,
  VersionId `3PwINNYZavmgXnRupsDK1JzKIg8PQHTk`.
- **NO READER, and the evidence is stronger than a census.** The request's own definition,
  `org/missions/D8/MDPF/MDPF_DEMQUE/requests/ETFS_RIVALS-HISTORY-OWED-DAILY.json:28`, declares
  `state_address` under **`request_state/`**, not `demand_state/`, citing MDPF_DEMQUE PRD ADDENDUM v0.4.
  The canonical object at `request_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json` is **live**
  (191 B, `2026-10-09T09:38:34Z` -- four hours *later* than the stray). So the live producer and any
  consumer read a different key, and the deleted object was a pre-canonicalization stray.
- `comp-find -i 'ETFS_RIVALS-HISTORY-OWED-DAILY'` -> 35 hits over **245,998** files scanned; none is a
  reader of the `demand_state/` key.
- A `list-objects-v2` of the whole `demand_state/` prefix returned **exactly one object** -- the target.
- **SAVED:** `T4_demand_state_ETFS_RIVALS-HISTORY-OWED-DAILY_state.json`, 335 B, sha256
  `801d5252c0f2f2fb1676cb68d5c5d3d62277c0b94b24680d7161f0e1336ae704`.
- **AFTER:** **404**. Control: the canonical `request_state/` key still **200**, which is the control that
  matters -- it proves the live request is unaffected. **No same-prefix sibling exists**: `demand_state/` is
  now empty, so the order's "a sibling in the same prefix still reads 200" could not be run as written and
  the same-bucket canonical key was used instead.

## Rules honoured

Only these four targets. No secret value read or printed; the two state files were saved without printing
their contents, and only `resources` counts and types were read from them. No log events read. A STOP on one
target would not have blocked the others -- none was reached.

## Ledger

`org/critical_paths/change_management/20261010T1340Z_adhoc-four-approved-deletes-laptop-20261010_deploy_completion.md`
-- opened 13:40Z **before any act** with the four targets as four legs, each closed with its own proof, entry
**CLOSED** 13:58:50Z, sentinel removed.

## AC1

`AC1` is judgment and the issuer's to grade from this receipt plus a live re-read. All four targets are
absent with a positive control on the same instrument; none was STOPPED.
