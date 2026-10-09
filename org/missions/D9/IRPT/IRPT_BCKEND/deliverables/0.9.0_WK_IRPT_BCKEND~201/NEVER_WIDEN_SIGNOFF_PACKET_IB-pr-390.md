# Never-widen sign-off packet -- IB-pr-390: release of IB-pr-385 + IB-pr-387 (`_authz/served.py` hosts) -- svc-custody-statement admitted on three routes, internal callers narrowed by their profile row

Prepared by 0.9.0_WK_IRPT_BCKEND~201 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. Files beside this packet: `IB97-3_release_census.json`, `IB97-3_release_replay.json`, `replay/` (the scripts). `lambda-source-map.candidate.json` and `amendment1_ALL_never_admits.patch` are SUPERSEDED history of the pre-amendment packet (the patch is now committed; the real map is restaged; no candidate map is used). Model: `0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`.

**READ THIS FIRST -- this packet is AMENDMENT 1 (issuer 2.0.0_SA_COO~P2, CTO msg 2569) and releases 6 of the 8 `served.py` hosts.**

1. **ALL never admits an internal caller, and it is in this pin.** A profile `allowedFirmIds` equal to the string `ALL`, or a list holding `ALL`, is refused FIRM_BINDING at the internal narrowing step (code commit `74a62fb46c`, `_authz` suite 304 passed). Measured live 2026-10-09 (the pre-amendment packet): of 83 `opal-users-v2` profile rows, 2 carry `allowedFirmIds` -- one internal `Dev` row with a LIST of six ids that covers all four firms, and one service row `cottonwood`; **0 internal rows hold `ALL`**, so the change refuses no live caller today.
2. **The real source map carries the change.** `served.py`'s staged row of each released host pins `74a62fb46c` (restage commit `c2bb612234`); the artifacts below are built at the REAL `lambda-source-map.json`, no candidate map, no override.
3. **HELD OUT, not in this pair: `irpt-holdings` (row S5) and `irpt-narrative` (row S6); their source-map rows are NOT restaged.** Every route they serve is **NOT YET NARROWED** -- see the section below, which names the follow-up cell.

## The pin and the builds

- **Release pin P (census pin): `71e9aacf27ab99a7c59475976fda063d57e46cc7`** (branch `wk-IRPT_BCKEND-201`). **Code pin `74a62fb46c`** (the commit that adds ALL-never-admits to `served.py`; it sits on IB-pr-385 `7e0bfc3222` and IB-pr-387 `b4b544fb15`). P is two commits on: the restage `c2bb612234` and the routes.json denominator `71e9aacf27`. `served.py` at the code pin is blob `87d9ecc49747`.
- **Census: the 6 RELEASED hosts of the 8 that package `_authz/served.py`** (a token census of `served.py` in `files[]` and `staged_from` over all 229 functions found 8; the layer map carries no copy): `irpt-49f-reporting-read-lambda`, `irpt-directory-search`, `irpt-export-render`, `irpt-performance-adapter`, `irpt-status`, `irpt-ycharts-generate`. Held out, with their rows: `irpt-holdings` -- row IRPT_BCKEND-D2-W201-S5 (parity gate refuses BUILD_ONLY at the real map); `irpt-narrative` -- row IRPT_BCKEND-D2-W201-S6 (new served.py raises TypeError against its staged errors.py). The layer map carries no copy (0 hits).
- BUILD_ONLY from a clean tree (porcelain 0 lines before and after every build), each function built twice, byte-identical: **YES** (6 of 6 built). Command: `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>  (TMPDIR outside the worktree; real lambda-source-map.json)`. Zips kept only in scratch, removed; nothing uploaded; source map untouched.

| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |
|---|---|---|---|---|---|---|
| `irpt-49f-reporting-read-lambda` | `8ySmTtYXTqZgnpFY/cnFKnbsGGO/qm6qLCxGLXhIVCI=` | `f324a64ed6174ea6`... | 280560 | `cou/Td9ydDrn9rQPT4hfa1n04eb54VXqnWaq4+N4FTI=` | 1 | `fvLqMaaeFSi6ZarBY7IjcfEWWmVllVX8` |
| `irpt-directory-search` | `RwgwXI5+xiss9h7OmVPqk6EujzQalXYCciQkvTBGj+c=` | `4708305c8e7ec62b`... | 193302 | `IV7P2AL43cGo9VfyY2ku0zEFAhQWq9BPxge754UynM8=` | 1 | `7L6kC0.B6Z2viqOJPKYrX86pVYngSWTn` |
| `irpt-export-render` | `c7jOyysB/zo6OjtzCNdUZiu0o4fxNE9XeCM1FxXIHhk=` | `73b8cecb2b01ff3a`... | 418286 | `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=` | 1 | `QK8IR0k6Ek7HmbMvA.GqjpfTGNKmDKdi` |
| `irpt-performance-adapter` | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` | `a3feb8dea5440b1e`... | 441258 | `NU6YVERLJ0i6qmazBYWUF+1xVDPGHwdMKqQ5vgjmVc4=` | 3 | `5nyq8P6vP8ZC7tceMqvLoKTl4F.1MvRP` |
| `irpt-status` | `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=` | `13b54abe183713d0`... | 353051 | `jhGc2J4Q5EesJgnLq8EzdE5ErrZLbyqnJ8m00R7CgdE=` | 4 | `Ji6C92YJzsOWQtvO0fJkTV2yYhqfE2bx` |
| `irpt-ycharts-generate` | `ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8=` | `640d102795adffb2`... | 614290 | `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=` | 6 | `VWdbar2YhmyNzR1BT0VkLo1c.nc2E3Gf` |

`live_before` = `aws lambda get-function-configuration` CodeSha256, read 2026-10-09; each equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip`, which is the rollback version in the last column.

## Changed members and their owners (every one owned)

**`irpt-49f-reporting-read-lambda`** -- function=irpt-49f-reporting-read-lambda pin=71e9aacf27 built_members=31 live_members=31; changed_members=1
- changed `served.py` (built `87d9ecc49747`, live `a8eb91e7d4c5`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-directory-search`** -- function=irpt-directory-search pin=71e9aacf27 built_members=24 live_members=24; changed_members=1
- changed `served.py` (built `87d9ecc49747`, live `a8eb91e7d4c5`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-export-render`** -- function=irpt-export-render pin=71e9aacf27 built_members=66 live_members=66; changed_members=1
- changed `served.py` (built `87d9ecc49747`, live `a8eb91e7d4c5`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-performance-adapter`** -- function=irpt-performance-adapter pin=71e9aacf27 built_members=71 live_members=71; changed_members=3
- changed `holdings_gold.py` (built `d41e861212a7`, live `cc04dd3332ea`): cd41c4e24f
- changed `loaders.py` (built `93f2f02a1bd4`, live `763f0a0d4445`): 8540c9dd8f, 8e6011bda1
- changed `served.py` (built `87d9ecc49747`, live `455cd77ea46e`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c +4

**`irpt-status`** -- function=irpt-status pin=71e9aacf27 built_members=49 live_members=49; changed_members=4
- changed `canonical_profile_reads.py` (built `30c8a05ad674`, live `0ec4a717f2aa`): 8540c9dd8f
- changed `loaders.py` (built `93f2f02a1bd4`, live `763f0a0d4445`): 8540c9dd8f, 8e6011bda1
- changed `maintained_sources.py` (built `29c35dbfba72`, live `585950a53879`): 8e6011bda1
- changed `served.py` (built `87d9ecc49747`, live `4a9d374c9806`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c +1

**`irpt-ycharts-generate`** -- function=irpt-ycharts-generate pin=71e9aacf27 built_members=104 live_members=100; changed_members=6
- changed `generate_installed.py` (built `fc67f9ad9965`, live `d878d10731f4`): 0ee21c796f
- changed `served.py` (built `87d9ecc49747`, live `570f79caa35d`): 74a62fb46c, b4b544fb15, 7e0bfc3222
- added `custody_interpreter.py` (built `60337babd76b`, live `-`): b398d27731
- added `custody_ports.py` (built `a19a0509c590`, live `-`): 4ee5392232
- added `holdings_publication.py` (built `ca49ec495cb5`, live `-`): 200ba442f5
- added `holdings_publication_port.py` (built `9ebf475e43c3`, live `-`): 73075a9048

`served.py` is owned by `74a62fb46c` (ALL never admits, this amendment), `b4b544fb15` (IB-pr-387) and `7e0bfc3222` (IB-pr-385); in 49f-reporting-read and directory-search and export-render the live blob also predates `fff1b0395a` (IB-pr-366, the served CREATE guard) and `db8161f46e` (IB-pr-357), which ride in (row S7). Grouping for the signer: **clean (served.py only):** 49f-reporting-read, directory-search, export-render. **Carry other unreleased cells:** performance-adapter (`holdings_gold.py`, `loaders.py`), status (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`), ycharts-generate (`generate_installed.py` IB-yr-761 and four added custody/holdings members). **The svc subject needs export-render (custody-report-persist, submit-export) AND ycharts-generate (analysis-requests).**

## What the release does

- **IB-pr-385.** `verified_internal_subject` admits ONE firm-bound service subject, `svc-custody-statement` (sub, `userType` service, edge-verified, not renderer, verified `x-firm-id` == `lookup('cottonwood')['long']` from `lib/opal_naming.py`). `Entry.handle` keeps it out of the any-firm selection and `global`, puts it on the Opal roster for its own firm only, and refuses it NOT_AUTHORIZED on every operation but `custody-report-persist`, `analysis-requests`, `submit-export`. A zip without the registry refuses it (fail closed).
- **IB-pr-387.** An internal caller selecting another firm is narrowed by its profile row's `allowedFirmIds`: a non-empty list narrows; no row, no attribute or an empty list is unchanged; a non-list value or any read error is FIRM_BINDING. **Amendment 1: `ALL` (the string, or a list member) is a FIRM_BINDING refusal, never an unrestricted spelling.**

## Writers of each changed property

- **Admission of `svc-custody-statement` on the Opal roster (the property IB-pr-385 widens, for ONE named subject and ONE firm).** Writers of a request's Opal roster: 3 code sites (N=3, all read): `served.py` `Entry.handle` (`principals = frozenset([email]) if subject is not None`, the ONLY one this release changes), `_scope/custody.py:74` and `reports/generate_installed.py:158` (each rosters the verified custody principal for its own path; unchanged). Its inputs: the verified claims written by the edge authorizer (`portal-authorizer`, a signed token; the token itself is minted by the applier under the K2 mint pair `NEVER_WIDEN_PAIR_SVC_CUSTODY_STATEMENT_MINT.md`, DRAFT, not signed -- so no live token of this subject exists to admit). Both branches covered: cottonwood claim admitted, any other firm claim not admitted (replay arms below).
- **A caller's selectable firms (the property IB-pr-387 narrows).** Writers of `allowedFirmIds` on a profile row: 0 code writers found in non-test code (17 files mention it; the authorizer and readers derive or read it; the rows are maintained data, not written by a Lambda in this repo) -- the rule that reads it is `Entry._internal_allowed_firms` (1 rule, read). Live rows: 83 scanned, 2 carry the attribute (above). Blast radius of the narrowing today: 0 internal callers lose a firm.

## Every route this change admits (pair of admitted and another-firm-refused)

Source of the route set: `docs/contracts/investor-reporting/v1/routes.json` at P -- 23 routes (21 DECLARED + 2 ROUTED_ELSEWHERE); its `_denominator` now reads declared 21, routed_elsewhere 2, total 23 (row S2 fixed, `71e9aacf27`, no route changed). **21 of the 23 are replayed below (the 6 released hosts); the other 2 are the held-out hosts' and are listed as NOT YET NARROWED.** The narrowing applies on every route, because every route runs `Entry.handle` and the narrowing fires when a caller selects a firm other than its verified one. Each route below is replayed through its HANDLER's built zip. Columns: **A** = internal row `[cottonwood]` selecting cottonwood (admitted); **B** = the same caller selecting inflection (refused FIRM_BINDING built; the live zip admitted it); **C** = no-row Opal caller selecting inflection (identical built and live); **ALL** = internal caller whose row is the string `ALL` / a list holding `ALL`, selecting inflection (refused FIRM_BINDING built). svc rows: **S1** svc cottonwood claim (admitted on built, not on live); **S2** svc inflection and 49financial claims (not admitted, built and live identical); **S3** svc cottonwood selecting inflection (FIRM_BINDING).

| route | operation | handler | A | B (built / live) | C | ALL (str / list, built) | svc S1 / S2 / S3 |
|---|---|---|---|---|---|---|---|
| POST /api/scoped/investor-reporting/selections | selection-create | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/directory/browse | directory-browse | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/directory/search | directory-search | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: UNEXPECTED) |
| POST /api/scoped/investor-reporting/directory/resolve | resolve-scope | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/performance/{accountSetId} | performance-report | `irpt-performance-adapter` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/analysis | analysis-requests | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| GET /api/scoped/investor-reporting/analysis/{jobId}/sections | analysis-report | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/status | status-summary | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/status/{jobId} | status-job | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/export | submit-export | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| GET /api/scoped/investor-reporting/export/{exportId} | export-receipt | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/export/{exportId}/download | export-download | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/custody-report/{reportId} | custody-report-read | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/custody-report | custody-report-persist | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| POST /api/scoped/investor-reporting/analysis/inputs | analysis-input-upload | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests | analysis-request-history | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/comparisons | comparison-catalogue | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests/{requestId} | analysis-request-read | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests/{requestId}/pdf | analysis-request-pdf | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/reporting/{account_id}/{which} | reporting-read | `irpt-49f-reporting-read-lambda` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/reporting/client/{client_id}/summary | reporting-summary-read | `irpt-49f-reporting-read-lambda` | admitted | FIRM_BINDING / admitted | identical | FIRM_BINDING / FIRM_BINDING | n/a (svc: NOT_AUTHORIZED) |

The non-svc `svc: UNEXPECTED` entries for `irpt-directory-search` mean the subject is not recognised at all there (its tree has no `lib/opal_naming.py`), so it is an ordinary service principal with an empty Opal roster; elsewhere it is NOT_AUTHORIZED. Tests cited as the second cover of each pair: `_authz/tests/test_svc_custody_statement.py` (23, incl. `test_svc_custody_statement_cottonwood_admitted_on_each_route`, `..._other_firm_claim_refused`) and `_authz/tests/test_allowed_firm_ids.py` (12: listed firm admitted, unlisted firm refused).

## NOT YET NARROWED -- the routes of the two held-out hosts

`irpt-holdings` and `irpt-narrative` are NOT in this release (their source-map rows are not restaged, nothing here builds or replays them). **Until they are released, an internal caller selecting another firm on these routes is NOT narrowed by its profile row and the svc subject is not admitted there:**

| route | operation | handler | status | why held out |
|---|---|---|---|---|
| GET /api/scoped/investor-reporting/narrative/{reportId} | narrative-packet | `irpt-narrative` | **NOT YET NARROWED** | row IRPT_BCKEND-D2-W201-S6 (new served.py raises TypeError against its staged errors.py) |
| GET /api/scoped/investor-reporting/holdings/{accountSetId} | holdings-snapshot | `irpt-holdings` | **NOT YET NARROWED** | row IRPT_BCKEND-D2-W201-S5 (parity gate refuses BUILD_ONLY at the real map) |

**Follow-up cell: none is cut at this pin** (decomposition section 90 carries IB-pr-390 and IB-pr-391 only). It is for the issuer 2.0.0_SA_COO~P2 to cut, one cell for both hosts or one per host: (a) `irpt-holdings` -- clear the ADHC_DRIFTD.002 parity gate (`holdings_publication_port.py` is in `source_dir` and not in `files[]`), then restage `served.py` at the code pin and build/replay/sign; (b) `irpt-narrative` -- restage its `errors.py` to one carrying `public_line(admitted=)` (and its 27 `served.py` commits of drift), then the same. Rows `IRPT_BCKEND-D2-W201-S5` and `-S6` are the evidence.

## The replay (offline; live versus built artifacts; `IB97-3_release_replay.json`)

The replay drives the real `served.Entry.handle` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layers extracted beside it), with the profile row injected and `enforcer_for` stubbed: **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the Opal roster; **refused** = a FIRM_BINDING / NOT_AUTHORIZED reply, or the subject absent from the roster (the real enforcer and the persist writer then refuse a non-Opal principal; the stub does not run them). `UNEXPECTED` in a record is the stub's own stop after admission.

| arm | verdict | negative control | detail |
|---|---|---|---|
| svc-custody-statement admitted on custody-report-persist, analysis-requests, submit-export with a cottonwood claim through the built zip; refused through the live zip | expected-diff | no | 3 of 3 svc routes: built reached the firm check bound to cottonwood with svc-custody-statement on the Opal roster; live did not put it on the roster. Routes: POST /api/scoped/investor-reporting/analysis (irpt-ycharts-generate), POST /api/scoped/investor-reporting/export (irpt-export-render), POST /api/scoped/investor-reporting/custody-report (irpt-export-render) |
| internal caller, profile row allowedFirmIds [cottonwood], selecting inflection: refused (FIRM_BINDING) through the built zip, admitted through the live zip | expected-diff | no | 21 of 21 routes (the routes of the 6 released hosts, each through its handler's built zip) |
| internal caller, profile row [cottonwood], selecting cottonwood (the admitted half of each narrowing pair): admitted through both zips | identical | no | 21 of 21 routes |
| AMENDMENT 1 (CTO msg 2569): internal caller whose profile row is the string ALL, or a list holding ALL, selecting inflection: refused FIRM_BINDING through the built zip (never an unrestricted spelling) | expected-diff | no | 21 of 21 routes, both forms; the live zip's outcome for the same caller is recorded per route in routes[] |
| unrelated Opal internal caller with no profile row, selecting inflection: identical through both zips (any-firm reach unchanged) | identical | no | 21 of 21 routes, same (firm, roster, code) built and live, bound to inflection |
| NEGATIVE CONTROL: svc-custody-statement with an inflection or 49financial claim is never admitted on the three svc routes, built or live | identical | yes | 3 of 3 svc routes: svcInf and svc49 identical built vs live and neither on the Opal roster |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) selecting inflection is refused FIRM_BINDING through the built zip (no any-firm selection) | expected-diff | yes | 3 of 3 svc routes |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) on an operation outside its three is refused NOT_AUTHORIZED through the built zip | expected-diff | yes | 18 of 18 non-svc routes |
| NEGATIVE CONTROL: each svc host built tree (export-render, ycharts-generate) with infra/logic/registry removed does not admit svc-custody-statement on any of its three svc routes | expected-diff | yes | 3 of 3 svc routes (export-render x2, ycharts-generate x1) not admitted with the registry absent (fail closed) |
| lib/opal_naming.py lookup('cottonwood') resolves from the built zip (row D2-S26) | expected-diff | no | resolved from 5 of 6 built trees: irpt-49f-reporting-read-lambda, irpt-export-render, irpt-performance-adapter, irpt-status, irpt-ycharts-generate; the svc host zips are irpt-export-render, irpt-ycharts-generate; trees that do not resolve: irpt-directory-search |

`lib/opal_naming.py` `lookup('cottonwood')` (row D2-S26): resolves from the built tree of 5 of the 6 released functions, including both svc hosts (`irpt-export-render`, `irpt-ycharts-generate`); `irpt-directory-search` carries no `lib/opal_naming.py`, so the subject is simply not recognised there (fail closed, and it hosts no svc route). Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in, row S7); the two held-out hosts' routes; a live token of the subject (none exists until the mint pair is applied).

## Branch A (released)

Precondition: none to restage -- the real map already pins `74a62fb46c` for the 6 released hosts (commit `c2bb612234`); the applier does not restage. Build from a clean tree at P or a descendant. For each of the 6 functions in the signed set (`irpt-holdings` and `irpt-narrative` are NOT in it):

1. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<key>.zip`, `<key>` = the function name, except 49f-reporting-read = `irpt-reporting-read-lambda`).
2. The Terraform deploy path of the function's module (`infra/aws/terraform/investor-reporting/<tf file>`: `49f-reporting-read-lambda` reporting-read/lambda.tf; `directory-search` directory/lambda.tf; `export-render` export/lambda.tf; `performance-adapter` performance/lambda.tf; `status` ops/lambda.tf; `ycharts-generate` ycharts/generate.tf); no IAM, route, schedule or environment change. Effect on served bytes: svc-custody-statement becomes admissible on the three routes for a cottonwood token (none exists yet); internal callers with a list row are narrowed and an `ALL` row is refused (0 such rows today); `served.py`'s IB-pr-366/357 changes also land.
3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.

## Branch B (rolled back)

Per function, redeploy the prior artifact through the same Terraform path (never a console edit): the S3 object version in the table's last column (its CodeSha256 is the `live_before` value). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest. The restage of the source map reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).

## The replay arm for the applier (rerun before the ledger)

From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> <pin> <out.json>` (reads the live zips and layers from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`; if the svc arm is not `expected-diff` on all 3 routes; if arm B or the ALL arm is not refused on every counted route; if the no-row arm is not identical; or if the no-registry negative control admits the subject. Delete the scratch directory afterwards.

## The after-read

One live `svc-custody-statement` persist read, and one internal caller's narrowed read, after the apply:

1. **svc persist (refusal-or-admission).** The applier, holding the minted token (K2 mint pair; not yet applied), POSTs `/api/scoped/investor-reporting/custody-report` once with a cottonwood-bound body. Expected: admitted to the writer (status per the writer's contract); a body bound to another firm: refused. If the token does not exist yet, this read is UNEXERCISED -- say so; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.
2. **Internal caller, narrowed.** Use an existing internal caller whose profile row carries a non-empty list and select a firm outside it: expected FIRM_BINDING. Measured today: the only internal row with a list covers all four firms, so no such caller exists; the read is then the unrestricted arm (the same caller selecting a listed firm still reads through) and the narrowing stays UNEXERCISED live. Do not write a profile row to make one: that is a WORLD write this packet does not ask for.

## Rows

Dispositioned by AMENDMENT 1: `IRPT_BCKEND-D2-W201-S1` (amendment code committed, `74a62fb46c`), `-S2` (routes.json denominator fixed, `71e9aacf27`), `-S3` (svc test fixture re-pointed to a no-row caller, same code commit), `-S4` (source map restaged, `c2bb612234`). Still open and ARMED: `-S5` (irpt-holdings parity gate) and `-S6` (irpt-narrative errors.py) -- both held out; `-S7` (IB-pr-366/357 ride in).
