# Never-widen sign-off packet -- IB-pr-390: release of IB-pr-385 + IB-pr-387 (`_authz/served.py` hosts) -- svc-custody-statement admitted on three routes, internal callers narrowed by their profile row

Prepared by 0.9.0_WK_IRPT_BCKEND~201 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. Files beside this packet: `IB97-3_release_census.json`, `IB97-3_release_replay.json`, `lambda-source-map.candidate.json`, `amendment1_ALL_never_admits.patch`, `replay/` (the scripts). Model: `0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`.

**READ THIS FIRST -- this packet is PRE-AMENDMENT and the order is left OPEN.**

1. **Amendment 1 (ALL never admits an internal caller, CTO msg 2569) is NOT in this pin.** The lane gate refused the code commit (row `IRPT_BCKEND-D2-W201-S1`, BLOCKING): `served.py` and two test files are in no order's `<paths>` until the drain. The change is written, tested and saved as `amendment1_ALL_never_admits.patch` (_authz suite: 303 passed, 1 failed -- row S3: `test_svc_custody_statement.py` is outside the grant). At this pin an internal caller whose row is the string `ALL` is still treated as unrestricted. Measured live: of 83 `opal-users-v2` profile rows, 2 carry `allowedFirmIds` -- one internal `Dev` row with a LIST of six ids that covers all four firms, and one service row `cottonwood`; **0 internal rows hold `ALL`**, so the amendment changes no live caller today. Do not sign the final pair on this pin: re-run `replay/make_census.py`, `replay/run_replay.py`, `replay/make_packet.py` at the amendment's commit.
2. **A build at the real source map does not carry this change** (row S4, ARMED). All 8 functions pin `served.py` at older blobs. The artifacts below are built from `lambda-source-map.candidate.json` (8 `staged_from` rows differ) through `BAU_SOURCE_MAP_OVERRIDE`. The applier must land that restage in `lambda-source-map.json` first, or the release is a no-op that reads green.
3. **`irpt-narrative` must stay OUT of the pair** (row S6, ARMED): the new `served.py` raises `TypeError` on its error path against that function's staged `errors.py`, and its live boundary is 27 `served.py` commits behind. **`irpt-holdings` has no built artifact** (row S5): the builder refuses on a parity gate that fails at the real map too.

## The pin and the builds

- **Release pin P: `389b61b2227d51f164ab393bf1386684014b4e18`** (branch `wk-IRPT_BCKEND-201`). Code pin `dea0f53252` (box/dell2 HEAD as the worktree carries it) holds IB-pr-385 `7e0bfc3222` and IB-pr-387 `b4b544fb15`; P is the next commit, which adds the candidate map. `served.py` at P is blob `e1db29d5eb5b`.
- **Census of EVERY function that packages `_authz/served.py`: 8 of 8** in `lambda-source-map.json` (a token census of `served.py` in `files[]` and `staged_from` over all 229 functions): `irpt-49f-reporting-read-lambda`, `irpt-directory-search`, `irpt-export-render`, `irpt-holdings`, `irpt-narrative`, `irpt-performance-adapter`, `irpt-status`, `irpt-ycharts-generate`. The layer map carries no copy (0 hits).
- BUILD_ONLY from a clean tree (porcelain 0 lines before and after every build), each function built twice, byte-identical: **YES** (7 of 7 built). Command: `BUILD_ONLY=1 BAU_SOURCE_MAP_OVERRIDE=<candidate map> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>`. Zips kept only in scratch, removed; nothing uploaded; source map untouched.

| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |
|---|---|---|---|---|---|---|
| `irpt-49f-reporting-read-lambda` | `EaSFFxBMmWQrfHGOd39wKFEAmWzZW0yQEYA2tzJ4EmU=` | `11a48517104c9964`... | 280517 | `cou/Td9ydDrn9rQPT4hfa1n04eb54VXqnWaq4+N4FTI=` | 1 | `fvLqMaaeFSi6ZarBY7IjcfEWWmVllVX8` |
| `irpt-directory-search` | `vInWBtDaMzvRPOJUWAqFdsd1yqADl8WOs2EoGVaHiWM=` | `bc89d606d0da333b`... | 193259 | `IV7P2AL43cGo9VfyY2ku0zEFAhQWq9BPxge754UynM8=` | 1 | `7L6kC0.B6Z2viqOJPKYrX86pVYngSWTn` |
| `irpt-export-render` | `tv4e9ioBpF4s19GRCJSgjUrhfl6pQ0kFjvlE6zxy/EE=` | `b6fe1ef62a01a45e`... | 418243 | `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=` | 1 | `QK8IR0k6Ek7HmbMvA.GqjpfTGNKmDKdi` |
| `irpt-narrative` | `8OaQQOZONXC8fcTmkHTinnFvb78PNq1Yqocx6VvY304=` | `f0e69040e64e3570`... | 213747 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` | 21 | `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` |
| `irpt-performance-adapter` | `Fdu45UBmHipDZ31mqbLz6bk4bNV42UQcy73LQqZHBLk=` | `15dbb8e540661e2a`... | 441215 | `NU6YVERLJ0i6qmazBYWUF+1xVDPGHwdMKqQ5vgjmVc4=` | 3 | `5nyq8P6vP8ZC7tceMqvLoKTl4F.1MvRP` |
| `irpt-status` | `+bDinT0AcIIHpCLPdCZO0yHWmqP7aen2/nmHF2rvrnk=` | `f9b0e29d3d007082`... | 353008 | `jhGc2J4Q5EesJgnLq8EzdE5ErrZLbyqnJ8m00R7CgdE=` | 4 | `Ji6C92YJzsOWQtvO0fJkTV2yYhqfE2bx` |
| `irpt-ycharts-generate` | `1DK6HKMO4hzJm7DXNEOWrExzZb+7DmaqjBTZYnyeOio=` | `d432ba1ca30ee21c`... | 614247 | `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=` | 6 | `VWdbar2YhmyNzR1BT0VkLo1c.nc2E3Gf` |
| `irpt-holdings` | NOT BUILT (row S5) | - | - | `SRANzIGzWj0cR9dl4YOuLVOECV9dt9omPQZ80uzoR5g=` | 1 | `GbQOO4bhv7LjZ0kiUVyc5V4TSDK85GNZ` |

`live_before` = `aws lambda get-function-configuration` CodeSha256, read 2026-10-09; each equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip`, which is the rollback version in the last column.

## Changed members and their owners (every one owned)

**`irpt-49f-reporting-read-lambda`** -- function=irpt-49f-reporting-read-lambda pin=389b61b222 built_members=31 live_members=31; changed_members=1
- changed `served.py` (built `e1db29d5eb5b`, live `a8eb91e7d4c5`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-directory-search`** -- function=irpt-directory-search pin=389b61b222 built_members=24 live_members=24; changed_members=1
- changed `served.py` (built `e1db29d5eb5b`, live `a8eb91e7d4c5`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-export-render`** -- function=irpt-export-render pin=389b61b222 built_members=66 live_members=66; changed_members=1
- changed `served.py` (built `e1db29d5eb5b`, live `a8eb91e7d4c5`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

**`irpt-narrative`** -- function=irpt-narrative pin=389b61b222 built_members=27 live_members=19; changed_members=21
- changed `enforce.py` (built `18f04af84b9c`, live `d1c8e7e09467`): e9311289b1, 4bca50737e
- changed `entry.py` (built `231560f57ed4`, live `ca9d9d47eec8`): 630de21b95
- changed `event_policy.json` (built `346e626bad4e`, live `d60745bedcb2`): a12b0df4e7
- changed `evidence.py` (built `6a3064cc866f`, live `fe7a41c46df0`): ac4eb443b3
- changed `fixtures/FIXTURE_MANIFEST.json` (built `f04956460562`, live `0d7ee782eb64`): a12b0df4e7
- changed `fixtures/performance_report_inf.json` (built `753e3cc6cb07`, live `f9fe05d6bcf5`): a12b0df4e7
- changed `fixtures/topics_predating.json` (built `835800678898`, live `dfb1bacca07f`): a12b0df4e7
- changed `fixtures/topics_window.json` (built `9d7473e24dfc`, live `8a4290315e78`): a12b0df4e7
- changed `handler.py` (built `8deb7938ee7f`, live `f04a619fd0cb`): ac4eb443b3
- changed `loaders.py` (built `b84bb2918fc1`, live `0c086052e6e6`): 79c4d64a0c, ffbffcac50, 81785d9ae3
- changed `prose.py` (built `6a3df88e25ee`, live `171c3898e971`): 118612b599, ac4eb443b3
- changed `resolve.py` (built `24b407fa00ff`, live `086a55a7d9d4`): 81785d9ae3, a0967bb920, 4bca50737e
- changed `served.py` (built `e1db29d5eb5b`, live `ba0cea6d4246`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c, cd41c4e24f +21
- added `canonical_profile_reads.py` (built `0ec4a717f2aa`, live `-`): 2704705672
- added `custody.py` (built `23cda6b0e3dd`, live `-`): 4911c398d9
- added `keys.py` (built `56ee3cc22e80`, live `-`): 48313e9c0e
- added `maintained_sources.py` (built `774eca9bde60`, live `-`): 15b9f85eb3
- added `owner_reads.py` (built `f9e1f5d3274e`, live `-`): 4911c398d9
- added `prospect.py` (built `b7e5c9335caa`, live `-`): a85e7d6329
- added `selection.py` (built `7ba910b85e2f`, live `-`): a176e4bc11
- added `selection_store.py` (built `583507a70e3a`, live `-`): 33e630885f

**`irpt-performance-adapter`** -- function=irpt-performance-adapter pin=389b61b222 built_members=71 live_members=71; changed_members=3
- changed `holdings_gold.py` (built `d41e861212a7`, live `cc04dd3332ea`): cd41c4e24f
- changed `loaders.py` (built `93f2f02a1bd4`, live `763f0a0d4445`): 8540c9dd8f, 8e6011bda1
- changed `served.py` (built `e1db29d5eb5b`, live `455cd77ea46e`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c, cd41c4e24f +3

**`irpt-status`** -- function=irpt-status pin=389b61b222 built_members=49 live_members=49; changed_members=4
- changed `canonical_profile_reads.py` (built `30c8a05ad674`, live `0ec4a717f2aa`): 8540c9dd8f
- changed `loaders.py` (built `93f2f02a1bd4`, live `763f0a0d4445`): 8540c9dd8f, 8e6011bda1
- changed `maintained_sources.py` (built `29c35dbfba72`, live `585950a53879`): 8e6011bda1
- changed `served.py` (built `e1db29d5eb5b`, live `4a9d374c9806`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c, cd41c4e24f

**`irpt-ycharts-generate`** -- function=irpt-ycharts-generate pin=389b61b222 built_members=104 live_members=100; changed_members=6
- changed `generate_installed.py` (built `fc67f9ad9965`, live `d878d10731f4`): 0ee21c796f
- changed `served.py` (built `e1db29d5eb5b`, live `570f79caa35d`): b4b544fb15, 7e0bfc3222
- added `custody_interpreter.py` (built `60337babd76b`, live `-`): b398d27731
- added `custody_ports.py` (built `a19a0509c590`, live `-`): 4ee5392232
- added `holdings_publication.py` (built `ca49ec495cb5`, live `-`): 200ba442f5
- added `holdings_publication_port.py` (built `9ebf475e43c3`, live `-`): 73075a9048

**`irpt-holdings`** -- function=irpt-holdings pin=389b61b222 built_members=35 live_members=35; changed_members=1
- changed `served.py` (built `e1db29d5eb5b`, live `a8eb91e7d4c5`): b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e

`served.py` is owned by `b4b544fb15` (IB-pr-387) and `7e0bfc3222` (IB-pr-385); in 49f-reporting-read, directory-search, export-render and holdings the live blob also predates `fff1b0395a` (IB-pr-366, the served CREATE guard) and `db8161f46e` (IB-pr-357), which ride in (row S7). Grouping for the signer: **clean (served.py only):** 49f-reporting-read, directory-search, export-render. **Carry other unreleased cells:** performance-adapter (`holdings_gold.py`, `loaders.py`), status (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`), ycharts-generate (`generate_installed.py` IB-yr-761 and four added custody/holdings members). **The svc subject needs export-render (custody-report-persist, submit-export) AND ycharts-generate (analysis-requests).**

## What the release does

- **IB-pr-385.** `verified_internal_subject` admits ONE firm-bound service subject, `svc-custody-statement` (sub, `userType` service, edge-verified, not renderer, verified `x-firm-id` == `lookup('cottonwood')['long']` from `lib/opal_naming.py`). `Entry.handle` keeps it out of the any-firm selection and `global`, puts it on the Opal roster for its own firm only, and refuses it NOT_AUTHORIZED on every operation but `custody-report-persist`, `analysis-requests`, `submit-export`. A zip without the registry refuses it (fail closed).
- **IB-pr-387.** An internal caller selecting another firm is narrowed by its profile row's `allowedFirmIds`: a non-empty list narrows; no row, no attribute or an empty list is unchanged; a non-list value or any read error is FIRM_BINDING. (At this pin a bare `ALL` is still unchanged: amendment 1, row S1.)

## Writers of each changed property

- **Admission of `svc-custody-statement` on the Opal roster (the property IB-pr-385 widens, for ONE named subject and ONE firm).** Writers of a request's Opal roster: 3 code sites (N=3, all read): `served.py` `Entry.handle` (`principals = frozenset([email]) if subject is not None`, the ONLY one this release changes), `_scope/custody.py:74` and `reports/generate_installed.py:158` (each rosters the verified custody principal for its own path; unchanged). Its inputs: the verified claims written by the edge authorizer (`portal-authorizer`, a signed token; the token itself is minted by the applier under the K2 mint pair `NEVER_WIDEN_PAIR_SVC_CUSTODY_STATEMENT_MINT.md`, DRAFT, not signed -- so no live token of this subject exists to admit). Both branches covered: cottonwood claim admitted, any other firm claim not admitted (replay arms below).
- **A caller's selectable firms (the property IB-pr-387 narrows).** Writers of `allowedFirmIds` on a profile row: 0 code writers found in non-test code (17 files mention it; the authorizer and readers derive or read it; the rows are maintained data, not written by a Lambda in this repo) -- the rule that reads it is `Entry._internal_allowed_firms` (1 rule, read). Live rows: 83 scanned, 2 carry the attribute (above). Blast radius of the narrowing today: 0 internal callers lose a firm.

## Every route this change admits (pair of admitted and another-firm-refused)

Source of the route set: `docs/contracts/investor-reporting/v1/routes.json` at P -- 23 routes (21 DECLARED + 2 ROUTED_ELSEWHERE); its own `_denominator` is stale (row S2). The narrowing applies on every route, because every route runs `Entry.handle` and the narrowing fires when a caller selects a firm other than its verified one. Each route below is replayed through its HANDLER's built zip (holdings: the would-be zip). Columns: **A** = internal row `[cottonwood]` selecting cottonwood (admitted); **B** = the same caller selecting inflection (refused FIRM_BINDING built; the live zip admitted it); **C** = no-row Opal caller selecting inflection (identical built and live). svc rows: **S1** svc cottonwood claim (admitted on built, not on live); **S2** svc inflection and 49financial claims (not admitted, built and live identical); **S3** svc cottonwood selecting inflection (FIRM_BINDING).

| route | operation | handler | A | B (built / live) | C | svc S1 / S2 / S3 |
|---|---|---|---|---|---|---|
| POST /api/scoped/investor-reporting/selections | selection-create | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/directory/browse | directory-browse | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/directory/search | directory-search | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: UNEXPECTED) |
| POST /api/scoped/investor-reporting/directory/resolve | resolve-scope | `irpt-directory-search` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: UNEXPECTED) |
| GET /api/scoped/investor-reporting/performance/{accountSetId} | performance-report | `irpt-performance-adapter` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/analysis | analysis-requests | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| GET /api/scoped/investor-reporting/analysis/{jobId}/sections | analysis-report | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/narrative/{reportId} | narrative-packet | `irpt-narrative` | EXCLUDED | EXCLUDED | EXCLUDED | - (row S6: built TypeError on the error path) |
| GET /api/scoped/investor-reporting/status | status-summary | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/status/{jobId} | status-job | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/export | submit-export | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| GET /api/scoped/investor-reporting/export/{exportId} | export-receipt | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/export/{exportId}/download | export-download | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/custody-report/{reportId} | custody-report-read | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/custody-report | custody-report-persist | `irpt-export-render` | admitted | FIRM_BINDING / admitted | identical | S1 built admitted/live refused; S2 not admitted (equal built/live); S3 FIRM_BINDING |
| GET /api/scoped/investor-reporting/holdings/{accountSetId} | holdings-snapshot | `irpt-holdings` (would-be) | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| POST /api/scoped/investor-reporting/analysis/inputs | analysis-input-upload | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests | analysis-request-history | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/comparisons | comparison-catalogue | `irpt-ycharts-generate` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests/{requestId} | analysis-request-read | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/analysis/requests/{requestId}/pdf | analysis-request-pdf | `irpt-status` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/reporting/{account_id}/{which} | reporting-read | `irpt-49f-reporting-read-lambda` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |
| GET /api/scoped/investor-reporting/reporting/client/{client_id}/summary | reporting-summary-read | `irpt-49f-reporting-read-lambda` | admitted | FIRM_BINDING / admitted | identical | n/a (svc: NOT_AUTHORIZED) |

The non-svc `svc: UNEXPECTED` entries for `irpt-directory-search` mean the subject is not recognised at all there (its tree has no `lib/opal_naming.py`), so it is an ordinary service principal with an empty Opal roster; elsewhere it is NOT_AUTHORIZED. Tests cited as the second cover of each pair: `_authz/tests/test_svc_custody_statement.py` (23, incl. `test_svc_custody_statement_cottonwood_admitted_on_each_route`, `..._other_firm_claim_refused`) and `_authz/tests/test_allowed_firm_ids.py` (12: listed firm admitted, unlisted firm refused).

## The replay (offline; live versus built artifacts; `IB97-3_release_replay.json`)

The replay drives the real `served.Entry.handle` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layers extracted beside it), with the profile row injected and `enforcer_for` stubbed: **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the Opal roster; **refused** = a FIRM_BINDING / NOT_AUTHORIZED reply, or the subject absent from the roster (the real enforcer and the persist writer then refuse a non-Opal principal; the stub does not run them). `UNEXPECTED` in a record is the stub's own stop after admission.

| arm | verdict | negative control | detail |
|---|---|---|---|
| svc-custody-statement admitted on custody-report-persist, analysis-requests, submit-export with a cottonwood claim through the built zip; refused through the live zip | expected-diff | no | 3 of 3 svc routes: built reached the firm check bound to cottonwood with svc-custody-statement on the Opal roster; live did not put it on the roster. Routes: POST /api/scoped/investor-reporting/analysis (irpt-ycharts-generate), POST /api/scoped/investor-reporting/export (irpt-export-render), POST /api/scoped/investor-reporting/custody-report (irpt-export-render) |
| internal caller, profile row allowedFirmIds [cottonwood], selecting inflection: refused (FIRM_BINDING) through the built zip, admitted through the live zip | expected-diff | no | 22 of 22 routes (every route of docs/contracts/investor-reporting/v1/routes.json except irpt-narrative's 1, through its handler's zip; irpt-holdings through the WOULD-BE zip) |
| internal caller, profile row [cottonwood], selecting cottonwood (the admitted half of each narrowing pair): admitted through both zips | identical | no | 22 of 22 routes |
| unrelated Opal internal caller with no profile row, selecting inflection: identical through both zips (any-firm reach unchanged) | identical | no | 22 of 22 routes, same (firm, roster, code) built and live, bound to inflection |
| NEGATIVE CONTROL: svc-custody-statement with an inflection or 49financial claim is never admitted on the three svc routes, built or live | identical | yes | 3 of 3 svc routes: svcInf and svc49 identical built vs live and neither on the Opal roster |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) selecting inflection is refused FIRM_BINDING through the built zip (no any-firm selection) | expected-diff | yes | 3 of 3 svc routes |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) on an operation outside its three is refused NOT_AUTHORIZED through the built zip | expected-diff | yes | 19 of 19 non-svc routes |
| NEGATIVE CONTROL: each svc host built tree (export-render, ycharts-generate) with infra/logic/registry removed does not admit svc-custody-statement on any of its three svc routes | expected-diff | yes | 3 of 3 svc routes (export-render x2, ycharts-generate x1) not admitted with the registry absent (fail closed) |
| lib/opal_naming.py lookup('cottonwood') resolves from the built zip (row D2-S26) | expected-diff | no | resolved from 6 of 8 built trees: irpt-49f-reporting-read-lambda, irpt-export-render, irpt-holdings, irpt-performance-adapter, irpt-status, irpt-ycharts-generate; the svc host zips are irpt-export-render, irpt-ycharts-generate; trees that do not resolve: irpt-directory-search, irpt-narrative |

`lib/opal_naming.py` `lookup('cottonwood')` (row D2-S26): resolves from the built tree of 6 of 8 functions, including both svc hosts (`irpt-export-render`, `irpt-ycharts-generate`); `irpt-directory-search` and `irpt-narrative` carry no `lib/opal_naming.py`, so the subject is simply not recognised there (fail closed, and neither hosts a svc route). Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in, row S7); the narrative route (row S6); a live token of the subject (none exists until the mint pair is applied).

## Branch A (released)

Precondition (row S4): the applier lands the candidate restage in `infra/aws/lambda/ci/lambda-source-map.json` (8 `staged_from` rows: pin `b4b544fb15...`, sha256 `e1db29d5...`; or the amendment's commit), commits, then builds from a clean tree. For each function in the signed set (recommended: every one but `irpt-narrative`; `irpt-holdings` only after the parity gate is cleared, row S5):

1. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<key>.zip`, `<key>` = the function name, except 49f-reporting-read = `irpt-reporting-read-lambda`).
2. The Terraform deploy path of the function's module (`infra/aws/terraform/investor-reporting/<tf file>`: `49f-reporting-read-lambda` reporting-read/lambda.tf; `directory-search` directory/lambda.tf; `export-render` export/lambda.tf; `holdings` holdings/lambda.tf; `narrative` narrative/lambda.tf; `performance-adapter` performance/lambda.tf; `status` ops/lambda.tf; `ycharts-generate` ycharts/generate.tf); no IAM, route, schedule or environment change. Effect on served bytes: svc-custody-statement becomes admissible on the three routes for a cottonwood token (none exists yet); internal callers with a list row are narrowed (0 today); `served.py`'s IB-pr-366/357 changes also land.
3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.

## Branch B (rolled back)

Per function, redeploy the prior artifact through the same Terraform path (never a console edit): the S3 object version in the table's last column (its CodeSha256 is the `live_before` value). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest. The restage of the source map reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).

## The replay arm for the applier (rerun before the ledger)

From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> <pin> <out.json>` (reads the live zips and layers from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`; if the svc arm is not `expected-diff` on all 3 routes; if arm B is not refused on every counted route; if the no-row arm is not identical; or if the no-registry negative control admits the subject. Delete the scratch directory afterwards.

## The after-read

One live `svc-custody-statement` persist read, and one internal caller's narrowed read, after the apply:

1. **svc persist (refusal-or-admission).** The applier, holding the minted token (K2 mint pair; not yet applied), POSTs `/api/scoped/investor-reporting/custody-report` once with a cottonwood-bound body. Expected: admitted to the writer (status per the writer's contract); a body bound to another firm: refused. If the token does not exist yet, this read is UNEXERCISED -- say so; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.
2. **Internal caller, narrowed.** Use an existing internal caller whose profile row carries a non-empty list and select a firm outside it: expected FIRM_BINDING. Measured today: the only internal row with a list covers all four firms, so no such caller exists; the read is then the unrestricted arm (the same caller selecting a listed firm still reads through) and the narrowing stays UNEXERCISED live. Do not write a profile row to make one: that is a WORLD write this packet does not ask for.

## Rows

`IRPT_BCKEND-D2-W201-S1` (BLOCKING: amendment 1 cannot be committed), `-S2` (the stale `_denominator` is in the contract file, not the granted path), `-S3` (BLOCKING: IB-pr-385's test collides with amendment 1), `-S4` (BLOCKING, ARMED: source map pins), `-S5` (BLOCKING: irpt-holdings parity gate), `-S6` (BLOCKING, ARMED: irpt-narrative), `-S7` (IB-pr-366/357 ride in).
