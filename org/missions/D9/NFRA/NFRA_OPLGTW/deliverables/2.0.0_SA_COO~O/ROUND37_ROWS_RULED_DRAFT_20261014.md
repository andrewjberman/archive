# NFRA_OPLGTW round 37 -- rows ruled ahead of the terminal packet (2.0.0_SA_COO~O, 2026-10-14 ~03:4xZ, DRAFT)

Work-ahead on an empty drive tick, around the gateway block (r30 waits on NFRA_MCPINDEX's catalog v2 or the 10:00Z
fallback). This file folds into `ROUND37_TERMINAL_<date>.md` at the drain. Every row below is owned by 2.0.0_SA_COO~O.

## Ruled -- issuer defects at the cut (4), each already remedied by an amendment

| row | what | remedy | carried to the cut template |
|---|---|---|---|
| Z-W65-S4 (BLOCKING) | cd1.AC2's `\S+` could not match a cron with spaces | OG-cd-1 A1 @a35d44604e | plant a green arm from a LIVE read, never a typed value |
| Z-S103 (OBSERVATION) | mg-1's preflight named `dynamodb:TransactWriteItems`, not an IAM action | OG-mg-1 A1 @402cea2cbc | name only real actions (`accessanalyzer validate-policy`), with the policy's condition context |
| Z-S104 (BLOCKING) | mg-1 offered the halves a choice the template made vacuous | OG-mg-1 A3 @024c9cb27c | read the template's fields before offering a branch |
| Z-W67-S1 (BLOCKING) | bd-2's ac03 pinned the rule the CTO reversed; the file was not in `<paths>` | OG-bd-3 A1 @989f3e4c38 | before running a sibling suite as a control, read what it asserts against the new rule |

## Ruled -- worker observations

- **Z-W61-S1, Z-W61-S2:** ACCEPT (ruled in the round-36 packet).
- **Z-W63-S1:** ACCEPT the plane (round-36 packet).
- **Z-W64-S2 (OBSERVATION):** ACCEPT, disclosed in OG-hv-2's pair.
  - `tools._run` requires a delegated Graph token the harvest tools do not use, so an Opal user without Graph consent
    gets `needs_login`.
  - Each call writes two audit records, and the key or prefix rides in `detail` (not secret).
  - No order changes.
- **Z-W64-S3 (OBSERVATION):** ACCEPT. 31% of audit-lake rows carry an empty user, so the census's 8 is a floor. Named
  as a floor in OG-hv-1's census.
- **Z-W65-S1 (OBSERVATION):** ACCEPT for the off-host read. The channel-to-family link is by entity-id token, because
  the catalog holds no `s3://` roots, and it over-links `blackdiamond_fees`. Carried to NFRA_MCPINDEX: a catalog
  `s3_root` per dataset would make the link exact.
- **Z-W65-S2 (OBSERVATION):** ACCEPT. `backfill_status_keys` is a plain list of URIs, a key list rather than a value.
- **Z-W65-S3 (OBSERVATION):** ACCEPT. The naming gate refuses scope names, so scopes are discovered live, and two
  families on one source read `inferred`. `local.family_depth_sources` holds 8 typed source prefixes; that is a rule-30
  question for OG-ap-16's pair.
- **Z-W66-S1 (OBSERVATION):** ACCEPT and CARRY.
  - 5 test ids fail standing alone, plus 1 acceptance test, and 5 more fail only when run in one process. All are
    pre-existing at base.
  - Carry to the round-37 analysis as ONE repair cell, the batched-repair rule.
- **Z-W66-S2 (OBSERVATION):** CARRY. The lake reads `ok` for the one `schwab_query` the acknowledged sink recorded as
  INVALID_REQUEST. Two audit planes disagree on one outcome, and that is FWD-8's support story; it belongs in the
  analysis.
- **Z-W66-S3 (OBSERVATION):** CARRY. `ops/schwab_status.py` raises `RoleConfigError` off-host (`SCHWAB_READER_ROLE_ARN`
  unset). It is FWD-8's runbook arm, owed on-host; a clear error is the repair.
- **Z-S102 (BLOCKING):** ANSWERED in the world. Route (a) drain-only builds pass LGIC_ENFORCE; full-source convergence
  is route (b), its own migration. Disposition is the CVO's at the slug.

## Open at the drain (not rows)

- Call `sitez-20261013T215753Z-232a`: Andrew names one asset manager (OG-hv-2 AC3, graded PARTIAL on the stand-in until
  then).
- For the round-37 analysis, from the OG-cp-1 draft: tier records are named in C-PERSON but carry no rule, and the
  `person_access` record type is hand-named (the builder has no record-type kind).
