# Release plan r58 -- the enforcer_for refusals reach the wire (never-widen), workstream ~P

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-05 ~21:5x ET / 2026-10-06 ~01:5xZ | **For:** `1.0.0_SA_CTO` (CTO half, batch 271 asked for this packet)
**Code:** IB-pr-326 merged at `abf14e56ba` (LOCAL; origin CLOUD `01a47ac2e7`, ls-remote read). **Nothing below is built or deployed.**

## 0. Two findings that change the release shape (read first)

1. **The merged fix is in NO build yet.** `BUILD_ONLY=1 build-and-upload.sh investor-reporting <fn>` at HEAD returns the live sha for all four
   functions this seat owns (reporting-read `j5R1..`, directory-search `OmSw..`, holdings `skOq..`, export-render `QVZQ..`). Every function stages
   `_authz/served.py` from a per-member pin in `infra/aws/lambda/ci/lambda-source-map.json` (`staged_from[].pin` + `sha256`), so a source edit ships
   only when those pins move (the IB-pr-324 pattern). **The release therefore needs a re-pin cell, which is not cut yet.**
2. **One server fault would read as a client fault under the fix.** `_authz/loaders.py:204` is `_fetch_directory(bucket, pointer["key"], client)`. A
   `latest.json` pointer without `key` raises `KeyError`, which `errors.reason_for` maps by exact class name to `NOT_FOUND` (`errors.py:136`).
   Today it answers `UNEXPECTED`. Batch 271 item 2 says a server fault must not read as NOT_FOUND and gets a declared class in the same release.
   Proposed: `load_directory` raises `FirmArtifactIncomplete` (declared `NOT_READY`, the W124-S2 required-server-source-malformed class) when the
   pointer is not a dict or has no non-empty `key`. That is a `loaders.py` edit plus a test: a new cell (IB-pr-327).

## 1. The WHOLE delta (batch 271 item 1)

The edit (`served.py:1050-1054`): `AuthzError` keeps `FIRM_BINDING`; every other exception answers `self.public_reason_for(exc)`, which is
`errors.reason_for` (declared `public_reason_code` first, then the by-type table by EXACT class name, no MRO) then this function's own `self.reasons`
by MRO, then `UNEXPECTED` for anything outside `BOUNDARY_REASONS`. Every row of `errors.reason_for`'s by-type table, with the raise sites reachable
inside `enforcer_for` (census method in section 2):

| class (exact name) | answers today at this site | answers after | raise sites reachable inside `enforcer_for` | note |
|---|---|---|---|---|
| `AuthzError` | FIRM_BINDING | FIRM_BINDING (kept by the isinstance branch) | 3: `enforce.py:112`, `:164` and `:319` (a refusal-code constructor, FirmBinding, Enforcer) | unchanged |
| `BucketUnmapped` (declares FIRM_BINDING) | UNEXPECTED | **FIRM_BINDING** | 1: `loaders.py:66` (`bucket_for`) | the S260 intent |
| `FirmArtifactIncomplete` (declares NOT_READY) | UNEXPECTED | **NOT_READY** | 1: `loaders.py:218` (`opaque_firm_for`) | the W124-S2 intent |
| `KeyError` | UNEXPECTED | **NOT_FOUND** | 0 explicit; **1 implicit: `loaders.py:204` `pointer["key"]`** | finding 2: made `FirmArtifactIncomplete` by IB-pr-327 |
| bare `ValueError` | UNEXPECTED | **INVALID_INPUT** | 0 explicit (`bucket_for`'s `json.loads` ValueError is caught at `:63`); `JSONDecodeError`/`UnicodeDecodeError` are subclasses with other exact names and stay UNEXPECTED | recorded by a test |
| `KeyComponentRefused`/`KeyRefused`/`ArtifactRefused` -> KEY_REFUSED | UNEXPECTED | KEY_REFUSED | 0 inside `enforcer_for` (`KeyRefused` is raised at `enforce.py:849`, in `serve`, after the except block) | not reachable |
| `ScopeRefused` -> NOT_AUTHORIZED | UNEXPECTED | NOT_AUTHORIZED | 0 | not reachable |
| `NoSuchOperation` -> UNSUPPORTED_OPERATION | UNEXPECTED | UNSUPPORTED_OPERATION | 0 | not reachable |
| `EnvelopeRefused` -> INVALID_INPUT | UNEXPECTED | INVALID_INPUT | 0 | not reachable |
| `FileNotFoundError` -> NOT_FOUND | UNEXPECTED | NOT_FOUND | 0 explicit | boto3 raises `ClientError`, not this class |
| `TimeoutError` -> DEPENDENCY_TIMEOUT | UNEXPECTED | DEPENDENCY_TIMEOUT | 0 explicit | botocore raises `ReadTimeoutError`/`ConnectTimeoutError` (own names) |
| `ConnectionError` -> DEPENDENCY_UNAVAILABLE | UNEXPECTED | DEPENDENCY_UNAVAILABLE | 0 explicit | botocore raises `EndpointConnectionError` (own name) |
| `TransportUncertain`, `BackendUnavailable` -> DEPENDENCY_UNAVAILABLE | UNEXPECTED | DEPENDENCY_UNAVAILABLE | 0 | not reachable |
| `MaintainedSourceUnready` NOT_READY / `MaintainedSourceUnauthorized` NOT_AUTHORIZED / `MaintainedSourceInvalidInput` INVALID_INPUT | UNEXPECTED | their declared class | **0 on this path**: raised only under `_service_allowed_firms`, which catches everything and returns `[]` (`served.py:949-971`, r57 README section 1) | the broad census counts 27 sites by name collision; none is reachable |
| `ClientError`, `JSONDecodeError`, `IdRefused`, `AttributeError`, `IndexError`, `TypeError` and every other class | UNEXPECTED | UNEXPECTED | n/a | not in the table; unchanged |

**Net wire movement at this call site, for a real request:** a firm with no bucket (BucketUnmapped) FIRM_BINDING; a firm directory with no
`firm_id_opaque` (or, with IB-pr-327, a malformed pointer) NOT_READY. Nothing else moves, on the measured path.

## 2. Census method and its limits (batch 271 item 2)

`r58_census/enforcer_for_raise_sites.json`: static, name-based call-graph reachability from `Entry.enforcer_for` over `_authz/*.py` and
`_scope/*.py` (non-test): 56 of 254 functions reachable, 37 raise sites of by-type or declared classes. **It is an upper bound** (a callee shared
by name counts). The tight read is the direct path: `enforcer_for` calls `deps`, `opaque_firm_for`, `load_directory`, `load_ownership`,
`load_policy`, `FirmBinding`, `Enforcer.__init__`, `Context`, `self.id_projection(tenant)` (`_ids/ids.py:396`) and `self.render_ports(tenant)`;
depth 2 adds `_fetch_directory`, `_get_json`, `bucket_for`, `_s3` and the memo helpers. **Bare `ValueError` raise sites on that path: 0. Bare
`KeyError` raise sites: 0 explicit, 1 implicit subscript (`pointer["key"]`).** Not seen by this method: exceptions raised inside boto3, json
or the stdlib, subscripts on values other than the one named, and per-function `id_projection` / render-port objects beyond the two read
(`projection_for_firm` has no raise and no constant subscript; `render_ports_from_env` runs at build, not per request). A function's own `reasons`
map can also name a class for an exception raised on the path; no function here maps one of the two path classes differently.

## 3. Packages carrying `_authz/served.py`, anchors, rollback

From `lambda-source-map.json` `staged_from` (8 carriers), live `CodeSha256` read 2026-10-05 ~21:5xZ. The served.py pin differs by function, so a
re-pin to the merged blob moves everything between the old pin and HEAD for that member, not one line. **The changed-member census per function
is taken after the re-pin (the r57 pattern) and is NOT in this packet.**

| function | served.py pin | loaders.py pin | live CodeSha256 (the rollback anchor) | owner / state |
|---|---|---|---|---|
| irpt-49f-reporting-read-lambda | 0642c9d004 | 0642c9d004 | `j5R13Pnv+3+LdbjREHuuldudMS03N7G830VOoKlle7o=` (10-05 20:22Z) | ~P, ship |
| irpt-export-render | 0642c9d004 | 0642c9d004 | `QVZQo07b87PSYl61hobRF5yWGNZ+jckVsrwYxhdEmqE=` (10-05 20:30Z) | ~P, ship |
| irpt-directory-search | f9a00f732c | 0642c9d004 | `OmSwySstxlzs8Svf38u0Zyoc8ucHBHxJ99SOI6HVGlA=` (10-05 20:25Z) | ~P, ship |
| irpt-holdings | 21eca74f40 | 0642c9d004 | `skOqPofToy4zOzBj24FkCC55+SUKhgqcl691RpNZEvA=` (10-05 20:27Z) | ~P, ship |
| irpt-status | 0642c9d004 | 0642c9d004 | `jhGc2J4Q5EesJgnLq8EzdE5ErrZLbyqnJ8m00R7CgdE=` (10-05 04:18Z) | ~Y's deploy lane (batch 260) |
| irpt-ycharts-generate | 0642c9d004 | 0642c9d004 | `uFTONal/RhfoETes4rqJ4xRjJV4d2/nv3OlwuR9AXCQ=` (10-04 01:57Z) | HOLD (r57 row S337, riders) |
| irpt-performance-adapter | f9a00f732c | 0642c9d004 | `NU6YVERLJ0i6qmazBYWUF+1xVDPGHwdMKqQ5vgjmVc4=` (10-03 18:44Z) | HOLD (parity gate W127-S1, batch 270 item: nothing closes there on r57) |
| irpt-narrative | f6c6b56f40 | bc3727b3a3 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` (09-21 15:05Z) | not a ~P function; named so the set is complete |

Rollback per function: re-point the function at the r57 post-deploy S3 object version of `investor-reporting/<fn>.zip` (versioned bucket; the key
Terraform reads) with a targeted `safe-apply`, as r57. The r57 versions, which are r58's rollback targets (read from the r57 plans 2026-10-05):

| function | r57 object version (rollback target) |
|---|---|
| irpt-49f-reporting-read-lambda (key `irpt-reporting-read-lambda.zip`) | `gglDO8EVVhOJETgYbv4XArY2jYAmp0iH` |
| irpt-directory-search | `dUKEGHtxFxaBz_D_JUMQ2kTSsWvBHaZ5` |
| irpt-holdings | `LC5ia5OKXkAJj4E.eXXBf4Vs.RGiYgDd` |
| irpt-export-render | `jwtU6A2ctjdAPL5QCJ7VPfHGyDKrJfMy` |

**Hazard carried from r57:** `irpt-49f-reporting-read-lambda` is built to a key named after the function but Terraform reads
`irpt-reporting-read-lambda.zip`. r58's build for it must copy to the Terraform key (as r57 did) or the apply is a no-op. The other three
Terraform keys equal their function names.

## 4. Change and happy invokes (the r57 payloads, expectations flipped)

Payloads: `r57_invokes/` (all `*.change.json`, `*.happy.json`). The change payload (an unmapped `mockadv` principal) is the BucketUnmapped
probe. **Before r58 the wire answers `UNEXPECTED`; after, `FIRM_BINDING`** (the log's `classifier_code` already reads FIRM_BINDING since r57).
Happy payloads: byte-identical to the r57 post-deploy baselines (saved as `new_<fn>.<kind>.out` in the issuer's scratch; the sha of each is recorded
in the ledger at the invoke). `irpt-holdings` happy stays a baseline-equality read on a placeholder selection. For `irpt-export-render` also
`head-object` the receipt key before the happy invoke (batch 265 condition). A NOT_READY probe (an artifact with no `firm_id_opaque`) cannot be
invoked read-only against a real firm; it is covered by the offline test only, and said so.

## 5. Cells still to cut, and the order

1. **IB-pr-327** (`loaders.py`): a pointer that is not a dict or has no non-empty `key` raises `FirmArtifactIncomplete`; test with the S3 transport
   stubbed. Lands before the re-pin so the pinned loaders blob carries it.
2. **IB-pr-328** (`lambda-source-map.json`): move the `served.py` and `loaders.py` `staged_from` pins and sha256 for reporting-read, export-render,
   directory-search and holdings (and status, for ~Y, if it chooses) to the merged blobs.
3. Per function, as r57: census of changed members, build, plan 0/1/0 code hash only, targeted `safe-apply`, one change and one happy invoke.

## 6. The ask

Sign the CTO half on sections 1, 3 and 4 with the cells in section 5, or name what to change. Nothing is built until it is signed.
