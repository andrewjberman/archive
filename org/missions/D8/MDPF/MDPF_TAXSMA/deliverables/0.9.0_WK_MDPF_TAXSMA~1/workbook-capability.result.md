# MDPF_TAXSMA.TO-TX-g-1 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~1` · **cell** `TX-g-1` (PRD surface S01, FWD-7) · **branch** `wk-mdpf_taxsma-1-1`
in `C:/tmp/wk-taxsma-1` · **cut base** `fd2f1e4b31` · **commits** `6abf60e5d5` (build) and `8dce9aeb0b`
(instrument fixes), both LOCAL. **Spec:** the PRD @671925aecc and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json`
v0.5.0, whose enumerations are the only vocabulary used.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `infra/aws/ec2/opal-gateway/app/taxsma_workbook.py` (new, 533 lines) | the `GET /ms/taxsma-workbook` capability: its own guard, the fixed-resource read, the projection and the audit record | `git show --stat 6abf60e5d5`, 2026-09-15T23:0xZ |
| `infra/aws/ec2/opal-gateway/app/server.py` (+5 lines) | one import and one `Route(...)`, before every generic `/ms/*` route | same |
| `infra/aws/ec2/opal-gateway/app/config.py` (+10 lines) | `TAXSMA_WORKBOOK_BEARER`, `TAXSMA_WORKBOOK_IDENTITY`, neither in `validate()` | same |
| `infra/aws/ec2/opal-gateway/tests/test_taxsma_workbook.py` (new, 1161 lines) | `test_txg1_ac01 .. ac21`, one per criterion | same, amended at `8dce9aeb0b` |
| `infra/aws/ec2/opal-gateway/tests/test_principal_cutover.py` (+1 line) | the one `ROUTE_CLASS` entry the amended grant admits | same (1 insertion, 0 deletions) |
| `deliverables/.../probes/tx_g_1.py`, `probes/ac22_before.json` | the criterion probe and AC22's before arm | same |

**The guard order as built** (contract `capability.guard_order`), every step before a delegated-token fetch or a
Graph call: exact method; the route-only bearer, constant-time and refused when its value is also another route's
credential; no caller-supplied identity; no caller-supplied selector; the configured `<tid>/<oid>` bound to a
broker-held cache that a VALIDATED sign-in wrote for exactly that pair; current revocation.

## 2. Criteria -- 23 of 23 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-1 && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~1/probes/tx_g_1.py AC<n>`,
run at HEAD `8dce9aeb0b` with 0 of the 5 files under test dirty, 2026-09-15T23:29Z-23:35Z. Each run prints its
measurement, its denominator and exactly one `VERDICT:` line; rc 0 on all 23.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | 200; response fields 13 of 13, 0 extra, 0 missing, same order | module constants equal the contract on 17 of 17 checks |
| AC2 | 7 of 7 rows carry exactly the 7 projected + 3 metadata fields | 49 of 49 projected cells passed through unchanged |
| AC3 | 10 of 10 bearer arms 401 UNAUTHORIZED_CAPABILITY; correct bearer 200 | 5 other-route credentials accepted by their own gates, 5 of 5 |
| AC4 | 7 of 7 non-GET methods 405 `Allow: GET`, one audit record each | 0 token fetches, 0 Graph requests |
| AC5 | 31 of 31 enumerated selectors refused | 7 of 7 selector kinds; 0 reached Graph |
| AC6 | 18 of 18 credential-refusing routes refuse it; 11 of 11 open routes unchanged | 29 other routes of 30, probed twice each |
| AC7 | identity unset -> 503 AUTH_REQUIRED, 0 Graph calls | 2 of 2 unset forms |
| AC8 | tid alone differs -> 503, 0 fetches, 0 Graph; configured pair -> 200 | 3 of 3 engaged arms, same email throughout |
| AC9 | oid alone differs -> 503, 0 fetches, 0 Graph; configured pair -> 200 | 3 of 3 engaged arms, same email throughout |
| AC10 | 14 of 14 missing/malformed/unvalidated/caller-supplied arms -> 503 before any fetch | 3 classes, each enumerated |
| AC11 | 5 of 5 generic credentials 401, including an MCP token of the designated principal | audit label `unrecognized`, nothing bound |
| AC12 | 4 of 4 requests start at `taxsma_workbook.guard`; 5 generic `/ms/*` steps called 0 times | route 16 of 30, before the first generic `/ms/*` at 17 |
| AC13 | `delegated_identity_ref` = `{principal: <tid>/<oid>, display_email: ...}` | email in 0 of the record's other 10 fields |
| AC14 | 10 of 10 refusal arms 503 AUTH_REQUIRED, no rows | cutoff BEFORE the grant -> 200 with 7 rows |
| AC15 | Graph 403 -> one code, SOURCE_UNAVAILABLE, at `source_read` | disjoint from both guard refusals at `capability_guard` |
| AC16 | ETag changing every read -> SOURCE_CHANGED after 3 attempts | 1 + `etag_change_retries` 2, read from the contract |
| AC17 | 10001 rows -> SOURCE_TOO_LARGE with the observed extent, 0 value reads | 3 over-limit arms; boundary 10000 -> 200, complete true |
| AC18 | 7 of 7 header defects -> SOURCE_SCHEMA_INVALID | control: outer whitespace -> 200 |
| AC19 | 4 of 4 unrecognized rows returned, 0 dropped | two `Total` rows -> both UNRECOGNIZED, TOTAL 0 |
| AC20 | 0 prohibited occurrences across every test case | 21 cases, 210 calls, 210 bodies, 153 audit records; 10 of 10 prohibited fields enumerated |
| AC21 | 151 of 151 calls wrote exactly one record with exactly the 11 audit_fields, in order | 9 of 9 outcome classes; all 5 exclusions read 0 |
| AC22 | 87 of 87 previously passing tests still pass; 0 new failures | 14 modules before, 15 after; 4 NOT-EVALUATED |
| AC23 | 0 third-party names new to the Gateway; moto and msal refused, 21 passed | 63 base import names over 65 files; requirements unchanged |

**Controls.** MUTANT: removing the broker-record check from the binding (a scratch plugin, no file changed) gave
`5 failed, 16 passed`, rc=1 -- AC8, AC9, AC10, AC13 and AC14 fired. DETERMINISM: AC1, AC13 and AC21 re-run
verbatim are byte-identical after normalising the vintage line, durations and the corpus pid, 3 of 3.

## 3. Interpretations this cell had to make, stated

1. **`TAXSMA_WORKBOOK_IDENTITY` is `<tid>/<oid>`** and binds through the token broker's principal-keyed cache
   (`principal:<tid>/<oid>`), which only `verify_upstream_id_token` writes. That is what makes "a validated Entra
   principal context" checkable at request time without a token fetch, as AC8/AC9 require.
2. **A `TOTAL` row is the ONE row** whose single `Total` marker has no account number and no traded status; two
   such rows are both UNRECOGNIZED rather than an error, because the contract returns unrecognized rows and never
   drops them (AC19). A sheet with no Total row is not refused: the contract enumerates no error for it.
3. **Statuses:** UNAUTHORIZED_CAPABILITY 401 (405 for a method, 400 for a selector), AUTH_REQUIRED 503 as the
   machine routes already answer a missing delegated identity, SOURCE_* 502.
4. **`schema_version`** is the contract version, `0.5.0`.
5. **Cell scalars ship as Graph returned them.** A consequence worth naming for the consumer (S02/S19/S03): the
   projection carries values only, so a date cell arrives as its Excel serial with no number format beside it;
   the contract's date decoding happens downstream.

## 4. Surprise rows filed (3)

`MDPF_TAXSMA-W1-S1` (the AC22 population: four moto modules, not two, and two already-failing tests) ·
`MDPF_TAXSMA-W1-S2` (running the suite appends to the tracked `audit.jsonl`; restored to blob `3c69355bcd`, and
the probe now redirects `AUDIT_PATH`) · `MDPF_TAXSMA-W1-S3` (the load-sensitive `test_ogq1_ac02` reads FAILED in
the before-record). All three OBSERVATION and INERT; all three cited in the proof instance.

## 5. What this cell does NOT claim

No deploy, no live Graph or SharePoint call, no read of the real workbook, and no activation: EGRESS-ATTEMPTS 0
in 21 of 21 tests, and the first controlled live read remains TX-r-3's after G-A. The capability is unusable
until both configuration keys are set, which is TX-i-3's secret and the release cells' work. `ROUTE_CLASS`'s
assertion could not be executed here (moto absent); it was read statically instead, 30 of 30 routes named.
