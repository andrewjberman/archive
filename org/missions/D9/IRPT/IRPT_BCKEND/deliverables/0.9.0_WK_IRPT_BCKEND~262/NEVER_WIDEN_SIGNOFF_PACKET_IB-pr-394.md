# Never-widen sign-off packet -- IB-pr-394: the two hosts IB-pr-390 held out -- irpt-narrative (TypeError on the served error path) and irpt-holdings (ADHC_DRIFTD.002 parity gate)

Prepared by 0.9.0_WK_IRPT_BCKEND~262 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 2690 via ~V2 msg 2691; rows `IRPT_BCKEND-D2-W201-S5`, `-S6`). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. Files beside this packet: `IB99-1_release_census.json`, `IB99-1_release_replay.json`, `replay/` (the scripts). Model: `0.9.0_WK_IRPT_BCKEND~201/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md`.

**READ THIS FIRST.**

1. **Unlike IB-pr-390, the artifacts below are built at the REAL source map** (`infra/aws/lambda/ci/lambda-source-map.json` at the pin, no `BAU_SOURCE_MAP_OVERRIDE`): both hosts' `served.py` rows are restaged in this cell, so a build at HEAD carries the change. Compare the printed sha256 to the table before any upload.
2. **irpt-holdings is a small release** (2 changed members: `served.py` and the registered `holdings_publication_port.py`). **irpt-narrative is a wide one** (22 changed members, 8 of them added; live runs a boundary 28 `served.py` commits old). The release of narrative also **adds internal firm selection to a function whose live boundary does not honour it** (replay arm below, row `IRPT_BCKEND-D2-W262-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2). The signer can sign holdings alone: the two functions release independently.

## Root cause and fix, per host

- **irpt-narrative (row W201-S6).** The shared `_authz/served.py` calls `errors.public_line(..., admitted=BOUNDARY_REASONS)` in `_record`, at every error site. The `admitted` keyword exists in `_authz/errors.py` from `4fffe13f01`; narrative staged `errors.py` at `bc3727b3a3` (blob `784ee313ed70`), which does not take it, so every refusal that records an internal error raised TypeError. **Fix: restage narrative's `errors.py` row to `c18b5fec74` (blob `b60f25ccaa70`, the current one) and its `served.py` row to the same pin (blob `87d9ecc49747`, IB-pr-390's).** The smaller change: two staged rows of ONE function, against editing the shared `served.py` (which moves the bytes of all 8 hosts, 6 of them already restaged and released under IB-pr-390) or restaging all 21 members. No other host's bytes move: every other function's `errors.py` row is untouched (holdings' is already the current blob). Tests: `narrative/tests/test_served_error_path.py`, 4 tests (`-k served_error_path`): an internal caller and a service caller each reach the error site of the real `entry.ENTRY` in a flat `python -I` tree built the way the builder builds it (staged blobs read at their pin, sha256-verified) and each get the staged `errors.py` public line and a refusal envelope, no TypeError; the staged `errors.py` takes `admitted`; and a negative control puts the old blob back and must see TypeError.
- **irpt-holdings (row W201-S5).** `holdings/holdings_publication_port.py` (added by `73075a9048`, IB-m35-351) is in `source_dir` and not in `files[]`, so the ADHC_DRIFTD.002 parity gate refused every BUILD_ONLY. **Fix: `holdings_publication_port.py` added to holdings' `files[]` (owned by `73075a9048`),** and holdings' `served.py` row restaged to `c18b5fec74` (blob `87d9ecc49747`). The member is then in the zip, as it is in `irpt-ycharts-generate`'s, which already registers it.

## The pin and the builds

- **Release pin P: `c18b5fec743eef161ce1bc7ee444c7653e90865e`** (branch `wk-IRPT_BCKEND-262`): the commit that holds both restages, the `files[]` member and the narrative tests. `served.py` at P is blob `87d9ecc49747` (IB-pr-390's code commit `74a62fb46c`).
- Census: `infra/aws/lambda/ci/release-census.py <function> --pin P` for each of the two functions, live zip read from AWS (read only), diffed by member and sha256.
- BUILD_ONLY from a clean tree (porcelain 0 lines before and after every build), each function built twice, byte-identical: **YES** (2 of 2 built). Command: `TMPDIR=<scratch> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>  (the REAL source map, no override)`. Zips kept only in scratch; nothing uploaded; source map untouched.

| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |
|---|---|---|---|---|---|---|
| `irpt-narrative` | `NbzUcWz1clj8Be8IqNjdBbjmUpcfCcxr6iGGtJqh+Vc=` | `35bcd4716cf57258`... | 214053 | `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=` | 22 | `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` |
| `irpt-holdings` | `CKpZUMD5RVWyY/2oyo8zZwN7Ss8J2FbkeNFr2XYbXD8=` | `08aa5950c0f94555`... | 298954 | `SRANzIGzWj0cR9dl4YOuLVOECV9dt9omPQZ80uzoR5g=` | 2 | `GbQOO4bhv7LjZ0kiUVyc5V4TSDK85GNZ` |

`live_before` = `aws lambda get-function-configuration` CodeSha256, read 2026-10-09; each equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip` (checked: irpt-narrative yes, irpt-holdings yes), which is the rollback version in the last column.

## Changed members and their owners (every one owned)

**`irpt-narrative`** -- function=irpt-narrative pin=c18b5fec74 built_members=27 live_members=19; changed_members=22
- changed `enforce.py` (built `18f04af84b9c`, live `d1c8e7e09467`): e9311289b1, 4bca50737e
- changed `entry.py` (built `231560f57ed4`, live `ca9d9d47eec8`): 630de21b95
- changed `errors.py` (built `b60f25ccaa70`, live `784ee313ed70`): 4fffe13f01
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
- changed `served.py` (built `87d9ecc49747`, live `ba0cea6d4246`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e, cd9a61bb0c +22
- added `canonical_profile_reads.py` (built `0ec4a717f2aa`, live `-`): 2704705672
- added `custody.py` (built `23cda6b0e3dd`, live `-`): 4911c398d9
- added `keys.py` (built `56ee3cc22e80`, live `-`): 48313e9c0e
- added `maintained_sources.py` (built `774eca9bde60`, live `-`): 15b9f85eb3
- added `owner_reads.py` (built `f9e1f5d3274e`, live `-`): 4911c398d9
- added `prospect.py` (built `b7e5c9335caa`, live `-`): a85e7d6329
- added `selection.py` (built `7ba910b85e2f`, live `-`): a176e4bc11
- added `selection_store.py` (built `583507a70e3a`, live `-`): 33e630885f

**`irpt-holdings`** -- function=irpt-holdings pin=c18b5fec74 built_members=36 live_members=35; changed_members=2
- changed `served.py` (built `87d9ecc49747`, live `a8eb91e7d4c5`): 74a62fb46c, b4b544fb15, 7e0bfc3222, fff1b0395a, db8161f46e
- added `holdings_publication_port.py` (built `9ebf475e43c3`, live `-`): 73075a9048

Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). `served.py`'s owner list is IB-pr-390's code commit `74a62fb46c` first; the rest are the earlier `served.py` commits live narrative predates (28) / live holdings predates (5), including IB-pr-385/387 (the svc subject and the profile-row narrowing), IB-pr-366 and IB-pr-357. Narrative's `errors.py` is owned by `4fffe13f01`; holdings' `holdings_publication_port.py` by `73075a9048`. Narrative's other 20 members are the map's existing staged pins and source files, which no cell of this order changes; they release with it because live narrative was last built 2026-09-21.

## Writers of the changed property

- **The firm an internal caller's request is bound to (the property narrative's release widens: from the caller's own firm to a firm it selects).** Writers of the bound firm in `served.py`: **N=2**, both read: `verified = header(headers, 'X-Firm-Id')` (the edge-verified claim, unchanged) and `verified = selected` after the selection checks (internal caller only; `bucket_for(selected)` must accept it; a service principal needs its row's `allowedFirmIds`; an internal caller is narrowed by its profile row, and a bare `ALL` never admits, CTO msg 2569). Both branches are covered in the replay: with a row, narrowed; with NO row, any registered firm (the IB-pr-387 "no row = unchanged" rule) -- and on narrative that is NEW, because the live boundary never honoured `selected_tenant`.
- **The Opal roster handed to `enforcer_for`:** 3 writers (N=3: `Entry.handle` and the two custody paths), only `Entry.handle` is in these zips and it is unchanged by this cell.

## Every route of the two hosts: admitted and another-firm-refused

Route set: `docs/contracts/investor-reporting/v1/routes.json` at P, handlers `irpt-narrative` and `irpt-holdings`: 2 routes (1 each). Columns -- **U-own** a plain firm user (x-firm-id cottonwood) with no selection: admitted for its own firm; **U-other** the same user selecting inflection: refused; **U-claim** the same user restating firm_id=inflection: refused; **A** an Opal internal caller with profile row `[cottonwood]` selecting cottonwood: admitted; **B** that caller selecting inflection: refused; **C** an unrelated Opal internal caller with no row, selecting inflection (built / live); **S** svc-custody-statement on the route's operation.

| route | operation | handler | U-own | U-other (refused) | U-claim (refused) | A (built / live) | B (built / live) | C (built / live) | S |
|---|---|---|---|---|---|---|---|---|---|
| GET /api/scoped/investor-reporting/narrative/{reportId} | narrative-packet | `irpt-narrative` | admitted (cottonwood) | refused FIRM_BINDING (live: bound cottonwood) | refused FIRM_BINDING | admitted cottonwood / bound opal-capital | refused FIRM_BINDING / bound opal-capital | bound inflection / bound opal-capital | not on roster (UNEXPECTED) |
| GET /api/scoped/investor-reporting/holdings/{accountSetId} | holdings-snapshot | `irpt-holdings` | admitted (cottonwood) | refused FIRM_BINDING (live: FIRM_BINDING) | refused FIRM_BINDING | admitted cottonwood / bound cottonwood | refused FIRM_BINDING / bound inflection | bound inflection / bound inflection | not on roster (NOT_AUTHORIZED) |

Reading: for a plain firm user both functions admit the user's own firm and never reach another (narrative's LIVE boundary ignores the selection and stays on the caller's firm; the built one refuses it). For an Opal internal caller, **holdings is unchanged except where a profile row narrows** (C identical, B newly refused); **narrative changes in C**: live binds an internal caller to `opal-capital` whatever it selects, built binds it to the selected firm with the Opal roster. Tests cited as the second cover: `_authz/tests/test_allowed_firm_ids.py`, `_authz/tests/test_svc_custody_statement.py`, and the four `served_error_path` tests.

## The replay (offline; live versus built artifacts; `IB99-1_release_replay.json`)

The replay drives the real `served.Entry.handle` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer `irpt-common:5` extracted beside it), profile row injected and `enforcer_for` stubbed to raise, so EVERY admitted case also crosses `served._record` (the error path under repair). **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the roster; **refused** = a FIRM_BINDING / NOT_AUTHORIZED reply. `UNEXPECTED` in a record is the stub's own stop after admission, now answered through the staged `errors.py` instead of TypeError.

| arm | verdict | negative control | detail |
|---|---|---|---|
| plain firm user (x-firm-id cottonwood), no selection: bound to its OWN firm through the built zip, same (firm, code) as the live zip | identical | no | 2 of 2 routes |
| plain firm user selecting inflection: refused FIRM_BINDING through the built zip; the live zip never reaches inflection either (another firm is refused) | expected-diff | yes | 2 of 2 routes refused FIRM_BINDING on built and never reached inflection on live; 1 of 2 identical built vs live (irpt-narrative live=cottonwood/UNEXPECTED; irpt-holdings live=None/FIRM_BINDING) |
| plain firm user restating firm_id=inflection in the query: refused FIRM_BINDING through the built zip, same as the live zip | identical | yes | 2 of 2 routes |
| internal caller, profile row allowedFirmIds [cottonwood], selecting cottonwood: admitted (bound to cottonwood) through the built zip | admitted | no | 2 of 2 routes; live admitted on 1 (live zips: irpt-narrative=opal-capital, irpt-holdings=cottonwood) |
| internal caller, row [cottonwood], selecting inflection: refused FIRM_BINDING through the built zip (live: see detail) | expected-diff | yes | 2 of 2 routes refused on built; live bound to inflection on 1 (irpt-narrative live=opal-capital/UNEXPECTED, irpt-holdings live=inflection/UNEXPECTED) |
| unrelated Opal internal caller with NO profile row, selecting inflection: through both zips | WIDENS irpt-narrative | no | 1 of 2 routes identical (firm, roster, code); a WIDENS verdict means the live boundary does not honour the selection: irpt-narrative built=inflection/UNEXPECTED live=opal-capital/UNEXPECTED; irpt-holdings built=inflection/UNEXPECTED live=inflection/UNEXPECTED |
| error path: no case through the built zips raises (no HARNESS_* code), i.e. served._record meets the staged errors.py without TypeError | identical | no | 2 routes x 7 cases each; HARNESS_* codes on built: none; on live: none |
| NEGATIVE CONTROL: the same built trees with errors.py put back to the pre-IB-pr-394 narrative blob (bc3727b3a3) raise TypeError on the error path | expected-diff | yes | 2 of 2 routes answer HARNESS_TypeError in all three probed cases |
| NEGATIVE CONTROL: svc-custody-statement (cottonwood) on these hosts' operations is never on the Opal roster through the built zip | identical | yes | 2 of 2 routes: built code irpt-narrative=UNEXPECTED, irpt-holdings=NOT_AUTHORIZED |

Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in with `served.py`; neither route is a create route); a live token of svc-custody-statement (none exists until its mint pair is applied; neither host serves one of its three operations).

## Branch A (released)

For each function in the signed set (narrative and holdings are independent; sign either alone):

1. From a clean tree at P (or a descendant whose `lambda-source-map.json`, the host trees and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip`).
2. The Terraform deploy path of the function's module: `irpt-narrative` (`infra/aws/terraform/investor-reporting/narrative/lambda.tf`); `irpt-holdings` (`infra/aws/terraform/investor-reporting/holdings/lambda.tf`); no IAM, route, schedule, layer or environment change. Effect on served bytes: the two functions answer through `served.py` `74a62fb46c`'s boundary; holdings gains `holdings_publication_port.py`; narrative gains the members listed above and honours internal firm selection (row W262-S1).
3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.

## Branch B (rolled back)

- `irpt-narrative`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ` (its CodeSha256 is the `live_before` value `es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest.
- `irpt-holdings`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `GbQOO4bhv7LjZ0kiUVyc5V4TSDK85GNZ` (its CodeSha256 is the `live_before` value `SRANzIGzWj0cR9dl4YOuLVOECV9dt9omPQZ80uzoR5g=`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest.

The source-map restage reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).

## The replay arm for the applier (rerun before the ledger)

From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> P <out.json>` (reads the live zips and the layer from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if the negative control does not raise TypeError (the harness then is not reaching the error site). A `WIDENS` verdict is expected for irpt-narrative only. Delete the scratch directory afterwards.

## The after-read

1. **holdings.** One `GET /api/scoped/investor-reporting/holdings/{accountSetId}` as a plain firm user: expected the same answer as before (the member `holdings_publication_port.py` is not on this route's path); CloudWatch shows no `TypeError`.
2. **narrative.** One refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line with the public reason code and no `TypeError` in the function's log group; an Opal internal caller selecting a firm now binds to it (the widening, row W262-S1). Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.

## Rows

`IRPT_BCKEND-D2-W262-S1` (OBSERVATION, ARMED: narrative's release is wide and adds internal firm selection). Closes by this cell: `IRPT_BCKEND-D2-W201-S5` and `-S6` (the code and restage; the release itself stays with the signed pair).
