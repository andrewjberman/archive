# Session log -- `0.9.0_WK_AMGT_RESAPP~49` on `AMGT-rk-47`

Worktree `/c/tmp/wk-amgt-14-49`, branch `wk-amgt-14-49`, cut from SITEZ HEAD `79173538aa`.

## What was built

1. **`lib/research/management/bloomberg_fallback.py`** (NEW) -- `pull_exec_officers(security, blp=None,
   s3=None, write_raw=False)`. One `ReferenceDataRequest` on `[security]` for `NAME` +
   `COMPANY_EXEC_OFFICERS` through `blp_client.reference_data` (loaded by path, same convention as
   `model_block_pull.py::_load_blp_client`). Parses each `"<name>,  <title>"` row on the FIRST `,  `
   (two spaces), folds both halves through `roster.asciify`. `status` OK / EMPTY / FAILED per the
   order's own discipline (FAILED never EMPTY). Lands the full per-security response, untouched, at
   `raw/bloomberg/<security_key>/<stamp>/exec_officers.json`, put-if-absent, when `write_raw=True`.

2. **`lib/research/management/enrich.py`** -- `apply_bloomberg_fallback(document, security_key, blp=None,
   s3=None, write_raw=False)`, called from `build_document` right after `roster_module.build_roster`.
   RESOLVED filing -> `roster_source FILING`, fallback never called (call count 0, planted control in
   AC1/test 1). Non-RESOLVED filing -> the fallback pull; OK with officers -> `roster_source
   BLOOMBERG_FALLBACK`, officers rebuilt as `{name, role, role_start: null, role_start_basis: "absent",
   tenure_years: null, source: "bloomberg", confirmed: true, enrichment: "NOT-ATTEMPTED", ...}`,
   `avg_tenure_years: null`, a `fallback` block with the page label; EMPTY/FAILED -> `officers: []`,
   `roster_source: null`, the `fallback` block carrying the status/reason. The FILING side
   (`roster_status`, `roster_reason`, `source_accession`, `source_key`, `source_item`, `parse_strategy`,
   `absence_reason_class`/`evidence`) is never touched by this function -- the filing's own failure
   travels with the fallback exactly as ratified. Also: `--skip-pool` on `main()` (guards the
   `compute_pool`/`write_pool_object` calls only when `--write-pool` is given; no effect on a dry run);
   `write_raw=args.write_pool` (raw never lands on a dry run); two new print lines (`ROSTER-SOURCE`,
   `BLOOMBERG-FALLBACK`).

3. **`lib/research/management/management.schema.json`** -- `roster_source` (REQUIRED, enum FILING /
   BLOOMBERG_FALLBACK / null) and `fallback` (REQUIRED, new `definitions.fallback`, `additionalProperties:
   false`, same contact-field `not` clauses) added at top level; `officer.source` widened from
   `const: "filing"` to `enum: ["filing", "bloomberg"]`; `officer.confirmed` re-described.

4. **`integrations/bloomberg/research/management_posture_batch.py`** -- `cmd_report` gains
   `_newest_management_object()` and the `MANAGEMENT CONTENT: FILING a BLOOMBERG_FALLBACK b zero-officer c
   of N served object(s)` line, read over EVERY served name (not just the filing ceiling) so a
   Bloomberg-fallback-only name is counted. `filed_names`/`cmd_management`'s own targeting is untouched.

5. **Tests** -- `lib/research/management/tests/test_bloomberg_fallback.py` (NEW, 7 tests: RESOLVED/no-call,
   UNRESOLVED+3-officer-fallback-with-filing-reason-preserved, EMPTY, FAILED via field-error, FAILED via
   transport exception (never EMPTY), two-space/nickname parse verbatim, `validate()` clean on both
   branches with 0 contact fields). `lib/research/management/tests/test_management.py` -- one existing
   test (`test_the_schema_forbids_a_contact_field`) updated to carry the now-required `roster_source`/
   `fallback` fields on its RESOLVED fixture (a direct consequence of the schema change; all 47
   pre-existing tests still pass).

## Live results (AC2/AC3/AC4)

Bloomberg terminal signed in (`health() -> ok: True`). All three validation names returned `status OK`
(CAT 44 entries, CSL 14, 6861/Keyence 1 -- "President", no CEO title, matches the surprise candidate the
order names for `rk-48`). Live write: CAT's filing had RESOLVED by spawn time (rk-38's battery landed it)
so it wrote `roster_source FILING`, fallback `NOT-CALLED`, call count 0; CSL and 6861 wrote
`roster_source BLOOMBERG_FALLBACK` with their own filing's `roster_reason` preserved on the object. Pool
object ETag identical before/after (`--skip-pool` held). Change-management ledger opened before the first
write, 3 legs (one per validation name) closed with pre/post proof, entry CLOSED.

## Surprise filed

`AMGT_RESAPP-Z-W49-S1` -- AC4's `<expect>` assumed the three validation keys are NOT in the crosswalk;
measured at spawn, all three are already `MEASURED` crosswalk records (rk-31 landed them earlier this
round). Does not affect AC4's PASS (read-only, a+b+c=N holds); filed for the record.

## Declared exclusions

- `AMGT-rk-48` (the CEO search) -- handed to this slot next as a continuation; not started here.
- No fleet run, no re-run of the 33 -- only the three validation names were ever targeted by a
  `--write-pool` invocation in this order, per BOUNDS.
