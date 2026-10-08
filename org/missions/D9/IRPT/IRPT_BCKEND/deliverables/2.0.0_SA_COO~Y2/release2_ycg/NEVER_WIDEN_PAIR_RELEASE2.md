# irpt-ycharts-generate RELEASE 2 -- never-widen pair DRAFT (TCKT_VNEXT X-1, both halves)

**VOID** (1.0.0_SA_CTO~DELL2 ADDENDUM 2 @b227133904, msg 1364): row IRPT_BCKEND-D2-W156-S2 showed the live guard never
reaches the on-behalf branch. ~P2 recuts the guard (E5); after E5 drains ~Y2 re-pins and a NEW release-2 pair is signed.
Do not apply from this pair. Run record: `ledger/IRPT_BCKEND_ROUND65_Y_L8_COMPILE.md`.

**Deployer:** `2.0.0_SA_COO~Y2`, the function's lane. **Ruling:** `1.0.0_SA_CTO~DELL2` msg 1089 ("Release 2 (later): X-1's
repin cell plus the smoke test, under its own pair. It also waits on the filer entitlement"); msgs 925/944 (ONE pair for
both X-1 halves). Derived from `../x1_release/NEVER_WIDEN_PAIR_DRAFT.md` @f0056a55a4. DRAFT: no half is signed and nothing
has been deployed.

## Pin and artifact

- **Pin:** dell2 CLOUD `f7a9d0b34f` (the IB-yr-641 drain). LOCAL on dell2 when drafted; origin CLOUD read `838362db08`
  (ls-remote). The pin must be on origin before signing.
- **Built artifact (BUILD_ONLY at f7a9d0b34f, gates passed, run by this seat 2026-10-08 ~17:2xZ):**
  `798Lgqw25X1am7uCjdgYdTSOY90saT2k3n8H01eOBJ0=` (100 members; import-closure OK, 63 .py).
- **Live now / ROLLBACK:** `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=` (release 1, LastModified 2026-10-08T10:06:18Z).

## Every changed member (`release-census.py irpt-ycharts-generate --pin f7a9d0b34f`; changed_members=3; `CENSUS_f7a9d0b34f.txt`)

| member | built / live | owner / half | what it does |
|---|---|---|---|
| `uploads.py` | 47f89e0b4660 / f88bdb902789 | Y (IB-yr-631 @b7dc881c10) | an OPAL_GLOBAL filer, home opal-capital, whose `allowedFirmIds` names the owner firm may create an upload for that firm; the record gains `acting_principal_id` |
| `interactive_access.py` | c28d9a74c9af / bba07a3f4eeb | ~P (IB-pr-354 @c101699a71) | `current()` adds `allowedFirmIds` to an OPAL_GLOBAL row only, from the injected profile reader (row email must equal the subject; trimmed, sorted, "ALL" dropped); absent / empty / ALL-only / failed read / no reader = no field (fail closed); stripped from every retained owner. `authorize_current`'s admission rule is UNCHANGED; the on-behalf admit is uploads.py's, reading this field |
| `generate_installed.py` | d878d10731f4 / f761837e870f | ~P (IB-pr-358 @c246d6a180) | `compose_upload` passes `ports["get_user"]` as `profile_reader`, cached once per subject per request; a failed read re-raises (fail closed); no new client |

**P half CONFIRMED as shipped:** `2.0.0_SA_COO~P2` msg 1322 (diff `3f29017cfc..f7a9d0b34f`: interactive_access.py +32/-2,
generate_installed.py +20/-1).

No other member changes, so release 1's riders (E-Y4, the ~G2 members, IB-pr-357) are already live and do not ride here.

## The route and the principal classes it changes

**Route:** the Analysis upload creation path, the POST that reaches `intake/uploads.py` `create`, served by
`irpt-ycharts-generate`.

| principal class | before | after |
|---|---|---|
| OPAL_GLOBAL, home opal-capital, `allowedFirmIds` lists the owner firm | refused (UPLOAD_CREATOR_MUST_BE_CURRENT_ACTOR / UPLOAD_ACTOR_ATTRIBUTION) | **ADMITTED**; the record names the actor and the owner firm |
| OPAL_GLOBAL, the firm not listed, or `allowedFirmIds` = "ALL" or absent | refused | refused (same code) |
| non-internal principal, another firm | refused | refused (same code) |
| any principal, owner firm opal-capital or global | refused (INPUT_ACCESS_DENIED) | refused (same code) |
| a principal filing for its own firm (the ordinary case) | admitted | admitted, unchanged |

Exactly one class widens. **Moves:** one function, `irpt-ycharts-generate` (`irpt-status`, `irpt-export-render` and
`irpt-performance-adapter` do not package the new `interactive_access.py` blob, ~P2 msg 1021). **Does not move:** the
resident host and every other function.

## Write set and rollback, per key

Ruled by `1.0.0_SA_CTO~DELL2` msg 1320 (msg 944 (2)): after-read 1 runs with a TEST filer, so the test principal is part of
this act's write set.

| key | written by | rollback |
|---|---|---|
| Lambda `irpt-ycharts-generate` code | the release (`798Lgqw2...`) | `ZspX0qD2...` |
| ONE test user profile in `opal-users-v2` (`SK = PROFILE`; email a dedicated test address; `userType`/home making it OPAL_GLOBAL, home opal-capital; `allowedFirmIds` = a list of exactly ONE partner firm). Created only after the code equality read (after-read 7). Its exact item is written to `TEST_FILER_ITEM.json` beside this file before the put. | this seat, one `put-item` | `delete-item` on the same `PK`/`SK`, always run after the reads, pass or fail; a `get-item` reading NOT FOUND closes the leg |
| the upload record(s) the admit read creates for that firm | the admit after-read | deleted with the test user; their keys are recorded in `RELEASE2_AFTER_READS.md` before deletion |

The test principal's `allowedFirmIds` never holds "ALL", never names opal-capital, and never names more than one firm.
No real person's row is written or changed. Which real person files for which firms stays Andrew's grant, on the act list,
and does not hold this release.

## After-reads (each branch named)

1. **Admit:** the TEST OPAL_GLOBAL filer above, whose `allowedFirmIds` explicitly lists one partner firm, creates an upload for
   that firm. The stored record shows `acting_principal_id` = the filer and `owner.firm_id` = the firm.
2. **Refuse (a):** the same filer, for a firm NOT on its list, is refused with its existing code.
3. **Refuse (b):** an ordinary advisor filing for another firm is refused, as before.
4. **Refuse (c):** any filer naming owner opal-capital is refused, as before.
5. **No regression:** an ordinary principal filing for its own firm is admitted as before, and one ordinary authorized
   Analysis request answers as before (READY path, no new refusal).
6. **Import closure:** one direct IAM invoke of `{"irpt_import_census": true}` returns `failed: {}`.
7. **Equality:** the deployed CodeSha256 equals the built `798Lgqw2...`; then the source map is recorded at that hash.

If any of 1-7 fails, roll back to `ZspX0qD2...` in the same session. The test user and its upload records are removed in
every branch.

## Still owed before signing

- **Andrew (not holding this release, msg 1320):** the real filer entitlement, meaning which person files for which firms.
- **~P2:** DONE (msg 1322), recorded above.
- **Pin on origin:** DONE -- `f7a9d0b34f` is an ancestor of origin CLOUD `4adc60e32f` (fetch + is-ancestor, ~17:2xZ).
- **The CTO's signature.**
