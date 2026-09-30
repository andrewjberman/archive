# AMGT_RESAPP round 50 -- `AMGT-yy-5` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~00:3xZ

**The act (ONE, CTO round-49 ruling 2):** redeploy `opal-amgt-scoped-api` carrying yy-2 (/thesis `dossier_fields`), yy-3 (the management
pass-through of the NEO label) and yy-4 (the base case's owner label), AND create two M-1 objects through
`python -m lib.research.management.proxy_officers --persist --security-key <K>` for INTU_US_Equity and HAL_US_Equity. Executor
`0.7.0_AE_CloudOps~A`, order `task-orders/AMGT_RESAPP.TO-AMGT-yy-5.the-one-build.md`. Build commit: CLOUD at or after `50cc86edd6`
(yy-3's drain) with `lib/` unchanged from it.

**The base, read live at signing:** CodeSha256 `Um3BOJ+jcVc3B79VuFCn4RyD5VYu+IzCpe3BQOP/p7A=`, LastModified 22:29:10Z (xx-4); artifact
VersionId `uq53Z5kcYgit49CPcBxZCHIhCgqaPhc2`, built from CLOUD `ccf2a27c6b`. No AMGT sentinel open at signing. **The executor re-reads
the base immediately before the build; a moved base is a STOP and a re-sign.**

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

| act | what it MAY touch | rollback |
|---|---|---|
| ONE artifact upload + ONE safe-apply | the function's CODE only (no IAM, no prefix) | re-apply VersionId `uq53Z5kc...` |
| TWO M-1 creates | `management/v1/INTU_US_Equity/2026-09-29.json`, `management/v1/HAL_US_Equity/2026-09-29.json` (builder output: `enrich.management_key`) -- both ABSENT at signing (each name holds only `2026-09-18.json`, untouched) | delete the two created objects (the 09-18 objects then serve again) -- a delete, so Andrew's confirmation is owed if it is ever needed |

## EXPECTED OUTCOME, read from the landed rules at signing (both branches)

- **/thesis** (`read_thesis_bundle`, one `read_dossier`): every name gains `dossier_fields`. For a dossier whose `thesis_pillars` is a
  LIST, the pillars verbatim with `terms` (13 over AZN_LN / IMB_LN / ADBE_US / AMD_US: 5 + 6 + 2 + 0); for an ABSENT pillars field
  (AMD_US), `thesis_pillars: []` + `thesis_pillars_absent` ABSENT with the dossier's reason. `management`, `fund_of_record`,
  `last_stated_position`: SERVED with the dossier's value and citation, or ABSENT with its reason. An unreadable dossier: `READ_FAILED`.
  No pre-existing /thesis key moves.
- **The base case label** reads `Opal's historical-multiple reference` wherever the base case is present; formula, `formula_words`,
  value and status unchanged.
- **Management:** INTU and HAL read the new objects -- `officer_set` "named_executive_officers", the label, `source_form` "DEF 14A",
  5 officers each, accessions INTU `000089687825000057`, HAL `000004501226000033` (the dry-runs at yy-3's drain; the executor records
  the live values). Every other name's payload gains `officer_set`, `officer_set_label`, `source_form` as null and nothing else.
- **Everything else served: UNCHANGED** -- `/timeline`, `/timeline/day`, `/print`, `/lead-panel/rankings`, `/lead-panel/timeseries`.

## THE CLOSURE -- what the build may carry

`git diff --name-only ccf2a27c6b 50cc86edd6 -- lib/` (non-test), measured: **9 files.**
- **Moving (RESAPP, this pair):** `lib/research/api/scoped_amgt.py` (yy-2, yy-3), `lib/research/api/case_rule.py` (yy-4).
- **INERT riders, verified by the issuer at signing:**
  - `lib/research/identity/crosswalk.py` (yy-6): only `build_crosswalk`'s union and `main` changed; the request path resolves through
    `load_crosswalk` / `resolve`, unchanged.
  - `lib/research/management/management.schema.json` (yy-3): read only by `enrich.validate`, never on the request path.
  - `lib/research/management/proxy_officers.py` (yy-3): not imported by `scoped_amgt` or any request-path module (it imports `fetch`,
    i.e. EDGAR -- a request-path import of it is a STOP).
  - `lib/research/harvest/publication_gold.py` (AMGT_HARVST k-1, l-1): `event_rows` / `_is_guarded` are called only by the offline
    `build_event` (`:1253`) and the CLI; the scoped API reads stored parts (COO~H msg 26807).
  - `lib/research/harvest/timeline_api.py` (AMGT_HARVST j-1): the hunks are the module docstring, the ROUTE-3 comment and
    `get_timeline_event`, which is UNMOUNTED (referenced in `scoped_amgt.py:4163` only in a comment; CTO hold, msg 26760);
    `get_timeline` and `get_timeline_day` unchanged.
  - `lib/research/corpus/induction_scheduled.py`, `schedule_induction.ps1` (AMGT_CORPUS r-1): a CLI and a Windows scheduler script,
    imported by no request-path module.
- **Landed after `50cc86edd6`, NOT packaged:** `lib/opal_naming.py` (1.0.0_SA_CTO @`01646908e1`, DSGN_IRPTV1's FIRM_DISPLAY_NAMES
  view target). `scoped_amgt.py:120/:193/:2087` record that `lib.opal_naming` sits OUTSIDE the adapter's vendored closure and is never
  imported at runtime; the content diff at the build confirms it is absent from the package. Any OTHER `lib/` file landing after this
  signing is limb 2.
- The CTO's ruling `ledger/CTO_RULING_YY5_CLOSURE_HARVST_INERT_20260930.md` (msg 26809) rules the HARVST riders INERT, no HARVST half.

## THE LANE STOPS on any of seven limbs

1. The base moved (re-read immediately before the build).
2. The content diff against artifact `uq53Z5kc...` names a packaged file beyond the nine above, or a request-path import of
   `proxy_officers`, `induction_scheduled` or `get_timeline_event`.
3. In `scoped_amgt.py`, a changed function beyond `read_thesis_bundle`, `_read_dossier_document`, `_dossier_fields`, `_team_cases`
   (its optional `dossier_read` argument), `read_management`'s pass-through.
4. The plan moves anything beyond the function's code.
5. A persist refuses, or its object fails `enrich.validate` (management.schema.json), or its key is not the builder's.
6. The served `/print` pdf OUTPUT or `/timeline` OUTPUT moves on AMD, BA, GOOGL, 1299 HK (captured before, byte-equal after; an
   AMD/BA/GOOGL timeline move is attributed against any AMGT_HARVST data write after the capture before it is a ROLLBACK).
7. The served `/lead-panel/rankings/trending/chatter` rows or `/lead-panel/timeseries` series move (`generated_at` excepted).

## THE FALSIFIERS

`yy-5` AC1 (base moved), AC2 (`yy_thesis.py --plane served --what fields`), AC3 (`--what label`), AC4 (`yy_neo.py --plane served`) --
each FAILS at the base (measured at the cut). Any criterion failing after the act is the ROLLBACK trigger.

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
