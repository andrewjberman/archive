# NEVER-WIDEN SIGNOFF PACKET v3 -- IRPT_BCKEND IB-pr-532, FULL PIN MINT, WITH THE LIVE-AGAINST-PIN DIFFERENTIAL (round 195, workstream ~P)

Order: IRPT_BCKEND.TO-IB-pr-539 (issued by 2.0.0_SA_COO~P2; CTO round-195 analysis item 1: the live-against-pin differential of the holdings producer, then packet v3). Worker: 0.9.0_WK_IRPT_BCKEND~384. Packet v3 is packet v2 (copied, its change set and blast radius updated) plus section 13, the differential as the signed scope.
Record: IB194-1_packet_v2_record.json (same folder). Predecessor: the v1 packet (deliverables/0.9.0_WK_IRPT_BCKEND~379/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532.md), whose counts this packet re-measures and whose mint route it replaces.
Scope: READ ONLY. Nothing was minted, invoked, written to AWS, uploaded, applied, deployed, signed or sent by this order (the only AWS calls were get-object by version id on the three live bundles and the harness's get and list reads). The only AWS calls were get-object by version id on the three live bundles and the re-measure harness's own read calls.

Base commit (worker HEAD before the first commit): 54b77779e4547ad9366a7b7cafb13d7366ae253e. Pin: 49467335d288d5c0012fe339c4cafcb74bd43fb5 (the release pin of the producer, blob 3a19dcf5912798f7d94e9756ae04f64dd2ce7ea0 for holdings_snapshot.py). Base commit for v3 (worker HEAD before the first commit of IB-pr-539): 69f54375235de6778f7d33e02fefb8f0306ea654.

## 1. Change set

Change 1, the IR cash rule on both layers, as signed in v1: the canonical branch (commit ec20f73ff8, IB-pr-527) and the bd-securities fallback branch (commit 9e41657727, IB-pr-529). Both call apply_cash_rule on the return of classify_security; the rule changes asset_class only, to cash, where sub_asset_class trimmed and lower-cased equals cash.

Change 2, the publish-gate exemption repair, as signed in v1: commit f3a42b2ab8 (IB-pr-530). directory_marks_no_closures ignores carried-forward entries, so a lost account is listed rather than refused where the firm's own source marks every entry UNKNOWN.

The full pin mint is not the two changes alone. Each firm's bundle moves by the members in section 2: changed by content, changed by line endings only, and one added member (opal_strategy_matcher.py). The live holdings_snapshot.py copies also predate producer commits that are on the pin (the account_id member, the keyed publish-gate summary, the CUSIP fallback and the multi_asset line, for the cottonwood and inflection copies); each is characterised in its effect line and listed as a moved member, not hidden behind the two signed changes.

Change 3, measured by section 13 and not in the two signed changes: on cottonwood, 291 changed nodes beyond the signed cash rule move through the holdings_snapshot.py member swap (asset_class 4 fixed_income to cash, asset_class_basis 236, sub_asset_class 51); on the other two firms the differential is the signed cash rule alone. The v2 reading that the full mint is the two signed changes plus the listed members is kept, and section 13 names the scope of the non-rule moves per firm.

## 2. Moved-member tables (one per firm, one line per member)

Every path below is a moved member of that firm's bundle, the set the stop evidence (IB193-1_digest_gate_stop.json) names and this worker recomputed from the downloaded live bundle against the pin closure. Columns: path, state, live commit, pin commit, class, effect. The live commit is the newest commit whose blob, CRLF folded, hashes to the live member's folded sha256; null means no commit matches.

### 49financial -- changed by content 19, changed by line endings only 4, added 1

| path | state | live commit | pin commit | class | effect |
|---|---|---|---|---|---|
| data/assets/scripts/gold/build_cottonwood_mdpf_slice.py | changed | 9efbec3c2f | 0c72f3be00 | behaviour | Not reached by the 49financial run: holdings_snapshot.py imports this module only inside the COT taxonomy helper (_cot_taxonomy_rules), which only the cottonwood builder calls. The change (commits 58772c1e86 and 0c72f3be00) adds the SMA sleeve overlap and the unidentified-strategy list to build_slice and build_composed, which the producer does not call, so the 49financial served output is unchanged. |
| data/assets/scripts/gold/investor_reporting/holdings_inf.py | changed | 9efbec3c2f | aa5778d962 | behaviour | Not reached by the 49financial run: the inflection builder is called only for inflection. The change (commit aa5778d962, amendment 1 of IB-pr-496) removes the local Eclipse capture temp file when a write fails, and leaves the served output unchanged. |
| data/assets/scripts/gold/investor_reporting/holdings_snapshot.py | changed | null | 1464de48be | behaviour | The live copy matches no commit in the history of this file. Against it the pin adds the signed IR cash rule on both classify layers (IB-pr-527 and IB-pr-529: a sub_asset_class of cash serves asset_class cash), the signed exemption repair (IB-pr-530: directory_marks_no_closures ignores carried-forward entries), and the registry header comment; the 49financial served asset classes and the publish-gate outcome are re-measured in the remeasure block, and no other 49financial behaviour differs between the two copies. |
| data/assets/scripts/gold/investor_reporting/schwab_account_codes.json | changed | b47987ae49 | b47987ae49 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| data/assets/scripts/silver/opal_strategy_matcher.py | added | null | 099632f46c | behaviour | New module loaded at import time by rebalancer_schemas.py (the cottonwood run only) and read by build_cottonwood_mdpf_slice.py inside a function; rebalancer_schemas.py imports it at module level, so the bundle must carry it or the cottonwood import fails. It reads the shared strategy config from S3 on first call, and the 49financial and inflection runs do not import it. |
| data/assets/scripts/silver/rebalancer_schemas.py | changed | 9efbec3c2f | 2727ad0214 | behaviour | Not reached by the 49financial run: rebalancer_schemas is imported only inside the COT taxonomy helper and by the slice and dim-model builders. The change moves opal_sma_member_of onto the shared StrategyMatcher and adds a module-level import of opal_strategy_matcher (commits 2727ad0214 and 099632f46c); is_opal_name is unchanged. |
| data/firm_registry.json | changed | 8e9ed1b539 | 69679b90e3 | data | The only changed line is the _generated provenance string (registry revision ffa41913 to 9f1cc0a3, commits 6c962b0a52 and 69679b90e3); no firm row, alias or bucket value in the file differs, so the firm set the producer reads is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_account_distribution.py | changed | e20899bce7 | 94ff221642 | behaviour | Not reached by the producer's run: this module is imported only by build_cottonwood_mdpf_pair, which only the cottonwood COT taxonomy helper imports, and the producer calls none of its functions. The change (commits 94ff221642 and ed1c20d805) folds the Cottonwood model keys into one other_models line in the MDPF Global distribution. |
| data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py | changed | 85dd7adc26 | ed1c20d805 | docs | Comments and docstrings only: the parse tree with docstrings removed is identical to the pin's, so the code the producer runs is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py | changed | 1e5e13d223 | 94ff221642 | behaviour | Not reached by the producer's run: imported only by build_cottonwood_mdpf_pair, and the producer calls none of its functions. The change (commits a85ecada1f and 94ff221642) adds the other_models line and an SMA additive component to the MDPF Global composition, which the producer does not compute. |
| data/mdpf/scripts/gold/mdpf_category_registry.py | changed | 46d04eb7b6 | fab599bcea | behaviour | Adds the SMA basis tables, sma_global_basis_of and a per-firm population rule for the MDPF Global views (commits 93de0c2336 and fab599bcea) and a signature change to build_category_views. The producer reads only VIEW_TREE and resolve from this module (taxonomy_path); neither is in a changed hunk and build_category_views is not called by the producer, so the served taxonomy paths are unchanged. |
| data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py | changed | 85dd7adc26 | 94ff221642 | behaviour | Adds an id-less other_models CANONICAL_MODELS row (commit 94ff221642, CN-f-1). The producer resolves a model's key only through resolve_model_id and resolve_eclipse_id, which key on a SmartX or Eclipse id, and the new row carries no id, so the served model_key of each model leaf is unchanged. |
| docs/contracts/investor-reporting/v1/CurrencyAuthorities.json | changed | 98b4416105 | 98b4416105 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json | changed | 506096fc9a | 506096fc9a | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| infra/aws/lambda/investor-reporting/_ids/ids.py | changed | 47f21dab95 | 11ba48fdc7 | behaviour | The change sits inside projection_with_seam, which the holdings producer does not call (its callers are the irpt_custody readers and the tests, by grep of the pin); the producer imports this module only for the id normalizer, which the diff leaves unchanged, so no served field moves (commits e962a5cb81 and 11ba48fdc7). |
| infra/logic/registry/exemptions.json | changed | 8b4c15c6ba | 61cc536c29 | data | Adds fence and exemption rows that opal_naming reads at run time (commits 2a809c975e through 61cc536c29); the holdings producer does not read exemptions.json, and the write addresses are equal, so no holdings output moves. |
| infra/logic/registry/remediations.json | changed | fd3b3b7bf2 | fd3b3b7bf2 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| infra/logic/registry/reporting_policies.json | changed | f60e6f1d2a | 103902e75d | data | Activates the irpt-custody-x10 and irpt-anlreq-x10 policy rows and widens the research-policy firm list (commits 0798635fec through 103902e75d); the holdings producer does not read reporting_policies.json (no reference in holdings_snapshot.py) and its write addresses are equal, so no holdings page moves. |
| infra/logic/registry/resources.json | changed | f185873e6b | 17ae4222c7 | data | Removes the openpyxl-layer library row (commit 17ae4222c7); the producer's write addresses are built by address() and are equal under the live and pin trees, so no served address moves. |
| infra/logic/registry/scopes.json | changed | 0146e0c954 | 69679b90e3 | data | Adds tenant pages, an inflection MASTER row, a restricted-prefix host and transitional tier_live and product_live rows, and flips the 49financial opal-data-bd alias routed flag to false (commits 5f962296ae, a15fb36a4c, 69679b90e3); the firm_bucket_map body generated into holdings_snapshot.py is unchanged and the write addresses are equal, so no firm write moves. |
| infra/logic/registry/systems.json | changed | 4201d79857 | 826364c980 | data | Adds the commonwealth and yahoo VENDOR rows and re-states owner claims (commits 8e39143feb, 530ef17ff8, 826364c980); holdings_snapshot.py source_vendor_keys matches VENDOR keys word-bounded against each builder's source text, and no firm's source text names either added key, so the served source vendor keys are unchanged. |
| lib/opal_naming.py | changed | b77e2af4d5 | 6ae365f583 | behaviour | The builder gains the firm_pages.json reader and the portal firm-matrix generator (commits a99d7e584c, c5d1415676, 6ae365f583) and the ownership and fence helpers (commits 7d0f46fe7c through b81373cbcc); address() and lookup() return the same strings for the producer's seven write shapes under the live and the pin trees (write_addresses equal for every firm), so no write address moves. |
| lib/trading_calendar.py | changed | 0cbb0ad174 | b2b7488660 | data | Under the fallback a year outside 2010 to 2027 now raises CalendarCoverageError instead of answering, and the fallback announces once on stderr (commits 4b766e4e2d and b2b7488660); the holiday set and the T-1 answers for the producer's window are equal (calendar block), so no served business date moves. |
| org/standards/NAMING_SCHEMA.json | changed | aa2b5a42ff | eb29bf7f37 | data | The naming schema that opal_naming reads at run time gains the user and group kinds, the fifo suffix rule, the fourth verdict and the cadence rules (commits 01c56eda2b, 1ea925a095, 19b61836e4, f701d5da50, eb29bf7f37); the producer's write addresses are equal under both trees, so no served address moves. |

### cottonwood -- changed by content 21, changed by line endings only 3, added 1

| path | state | live commit | pin commit | class | effect |
|---|---|---|---|---|---|
| data/assets/scripts/gold/build_cottonwood_mdpf_slice.py | changed | 9efbec3c2f | 0c72f3be00 | behaviour | Reached by the cottonwood run through the COT taxonomy helper, which reads only _norm, _CANONICAL_BY_NORM and is_auto_custom; none of these is in a changed hunk, so the cottonwood taxonomy answers are unchanged. The new SMA overlap and unidentified-strategy functions (commits 58772c1e86 and 0c72f3be00) run only in build_slice and build_composed, which the producer does not call. |
| data/assets/scripts/gold/investor_reporting/holdings_49f.py | changed | 0b7d3c77a1 | 135fc3509e | behaviour | Not reached by the cottonwood run: holdings_snapshot.py calls only the builder of the firm it runs (BUILDERS[firm_id]), and build_cot does not call holdings_49f. The change (commits 9b7256a99f, dfa9b72cc9, 7ace854890, 135fc3509e) leaves the cottonwood served output unchanged. |
| data/assets/scripts/gold/investor_reporting/holdings_inf.py | changed | 9efbec3c2f | aa5778d962 | behaviour | Not reached by the cottonwood run: the inflection builder is called only for inflection. The change (commit aa5778d962) removes a local capture temp file on a failed write and leaves the served output unchanged. |
| data/assets/scripts/gold/investor_reporting/holdings_snapshot.py | changed | null | 1464de48be | behaviour | The live copy matches no commit in the history of this file. Against it the pin adds the signed IR cash rule on both classify layers (IB-pr-527 and IB-pr-529), the signed exemption repair (IB-pr-530), the publish-gate keyed summary (IB-pr-414), a CUSIP fallback for canonical lookups after a symbol miss (SC-e-56), the multi_asset line of the six-class rule (SC-e-56), and the additive account_id member, which is written only when a caller passes one; the cottonwood served asset classes and the gate outcome are re-measured in the remeasure block. |
| data/assets/scripts/gold/investor_reporting/schwab_account_codes.json | changed | b47987ae49 | b47987ae49 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| data/assets/scripts/silver/opal_strategy_matcher.py | added | null | 099632f46c | behaviour | New module loaded at import time by rebalancer_schemas.py (the cottonwood run only) and read by build_cottonwood_mdpf_slice.py inside a function; rebalancer_schemas.py imports it at module level, so the bundle must carry it or the cottonwood import fails. It reads the shared strategy config from S3 on first call, and the 49financial and inflection runs do not import it. |
| data/assets/scripts/silver/rebalancer_schemas.py | changed | 9efbec3c2f | 2727ad0214 | behaviour | Reached by the cottonwood run through the COT taxonomy helper, which calls is_opal_name; that function's hunk is a comment only, so the Models-versus-Client placement is unchanged. The new effect on this run is the import-time load of opal_strategy_matcher (commit 099632f46c), which must resolve before any taxonomy call; opal_sma_member_of, which now reads the shared S3 config on first use and raises when it is unreadable, is not called on the producer's path. |
| data/firm_registry.json | changed | 8e9ed1b539 | 69679b90e3 | data | The only changed line is the _generated provenance string (registry revision ffa41913 to 9f1cc0a3, commits 6c962b0a52 and 69679b90e3); no firm row, alias or bucket value in the file differs, so the firm set the producer reads is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_account_distribution.py | changed | e20899bce7 | 94ff221642 | behaviour | Not reached by the producer's run: this module is imported only by build_cottonwood_mdpf_pair, which only the cottonwood COT taxonomy helper imports, and the producer calls none of its functions. The change (commits 94ff221642 and ed1c20d805) folds the Cottonwood model keys into one other_models line in the MDPF Global distribution. |
| data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py | changed | 85dd7adc26 | ed1c20d805 | docs | Comments and docstrings only: the parse tree with docstrings removed is identical to the pin's, so the code the producer runs is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py | changed | 1e5e13d223 | 94ff221642 | behaviour | Not reached by the producer's run: imported only by build_cottonwood_mdpf_pair, and the producer calls none of its functions. The change (commits a85ecada1f and 94ff221642) adds the other_models line and an SMA additive component to the MDPF Global composition, which the producer does not compute. |
| data/mdpf/scripts/gold/mdpf_category_registry.py | changed | 46d04eb7b6 | fab599bcea | behaviour | Adds the SMA basis tables, sma_global_basis_of and a per-firm population rule for the MDPF Global views (commits 93de0c2336 and fab599bcea) and a signature change to build_category_views. The producer reads only VIEW_TREE and resolve from this module (taxonomy_path); neither is in a changed hunk and build_category_views is not called by the producer, so the served taxonomy paths are unchanged. |
| data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py | changed | 85dd7adc26 | 94ff221642 | behaviour | Adds an id-less other_models CANONICAL_MODELS row (commit 94ff221642, CN-f-1). The producer resolves a model's key only through resolve_model_id and resolve_eclipse_id, which key on a SmartX or Eclipse id, and the new row carries no id, so the served model_key of each model leaf is unchanged. |
| docs/contracts/investor-reporting/v1/CurrencyAuthorities.json | changed | 98b4416105 | 98b4416105 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json | changed | 9e58503be1 | 506096fc9a | data | Adds the optional ACCOUNT-node account_id member (commit 7ace854890, IB-pr-493). The member is written only when a caller passes an account id, so the cottonwood and inflection nodes carry no new member, and the schema change is additive for every firm. |
| infra/aws/lambda/investor-reporting/_ids/ids.py | changed | 47f21dab95 | 11ba48fdc7 | behaviour | The change sits inside projection_with_seam, which the holdings producer does not call (its callers are the irpt_custody readers and the tests, by grep of the pin); the producer imports this module only for the id normalizer, which the diff leaves unchanged, so no served field moves (commits e962a5cb81 and 11ba48fdc7). |
| infra/logic/registry/exemptions.json | changed | 8b4c15c6ba | 61cc536c29 | data | Adds fence and exemption rows that opal_naming reads at run time (commits 2a809c975e through 61cc536c29); the holdings producer does not read exemptions.json, and the write addresses are equal, so no holdings output moves. |
| infra/logic/registry/remediations.json | changed | fd3b3b7bf2 | fd3b3b7bf2 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| infra/logic/registry/reporting_policies.json | changed | f60e6f1d2a | 103902e75d | data | Activates the irpt-custody-x10 and irpt-anlreq-x10 policy rows and widens the research-policy firm list (commits 0798635fec through 103902e75d); the holdings producer does not read reporting_policies.json (no reference in holdings_snapshot.py) and its write addresses are equal, so no holdings page moves. |
| infra/logic/registry/resources.json | changed | f185873e6b | 17ae4222c7 | data | Removes the openpyxl-layer library row (commit 17ae4222c7); the producer's write addresses are built by address() and are equal under the live and pin trees, so no served address moves. |
| infra/logic/registry/scopes.json | changed | 0146e0c954 | 69679b90e3 | data | Adds tenant pages, an inflection MASTER row, a restricted-prefix host and transitional tier_live and product_live rows, and flips the 49financial opal-data-bd alias routed flag to false (commits 5f962296ae, a15fb36a4c, 69679b90e3); the firm_bucket_map body generated into holdings_snapshot.py is unchanged and the write addresses are equal, so no firm write moves. |
| infra/logic/registry/systems.json | changed | 4201d79857 | 826364c980 | data | Adds the commonwealth and yahoo VENDOR rows and re-states owner claims (commits 8e39143feb, 530ef17ff8, 826364c980); holdings_snapshot.py source_vendor_keys matches VENDOR keys word-bounded against each builder's source text, and no firm's source text names either added key, so the served source vendor keys are unchanged. |
| lib/opal_naming.py | changed | b77e2af4d5 | 6ae365f583 | behaviour | The builder gains the firm_pages.json reader and the portal firm-matrix generator (commits a99d7e584c, c5d1415676, 6ae365f583) and the ownership and fence helpers (commits 7d0f46fe7c through b81373cbcc); address() and lookup() return the same strings for the producer's seven write shapes under the live and the pin trees (write_addresses equal for every firm), so no write address moves. |
| lib/trading_calendar.py | changed | 0cbb0ad174 | b2b7488660 | data | Under the fallback a year outside 2010 to 2027 now raises CalendarCoverageError instead of answering, and the fallback announces once on stderr (commits 4b766e4e2d and b2b7488660); the holiday set and the T-1 answers for the producer's window are equal (calendar block), so no served business date moves. |
| org/standards/NAMING_SCHEMA.json | changed | aa2b5a42ff | eb29bf7f37 | data | The naming schema that opal_naming reads at run time gains the user and group kinds, the fifo suffix rule, the fourth verdict and the cadence rules (commits 01c56eda2b, 1ea925a095, 19b61836e4, f701d5da50, eb29bf7f37); the producer's write addresses are equal under both trees, so no served address moves. |

### inflection -- changed by content 20, changed by line endings only 3, added 1

| path | state | live commit | pin commit | class | effect |
|---|---|---|---|---|---|
| data/assets/scripts/gold/build_cottonwood_mdpf_slice.py | changed | 9efbec3c2f | 0c72f3be00 | behaviour | Not reached by the inflection run: this module is imported only inside the COT taxonomy helper, which only the cottonwood builder calls. The change (commits 58772c1e86 and 0c72f3be00) adds functions that only build_slice and build_composed run, and the producer calls neither. |
| data/assets/scripts/gold/investor_reporting/holdings_49f.py | changed | 0b7d3c77a1 | 135fc3509e | behaviour | Not reached by the inflection run: holdings_snapshot.py calls only BUILDERS[firm_id], which for inflection is build_inf_meshed, and that builder does not call holdings_49f. The change (commits 9b7256a99f, dfa9b72cc9, 7ace854890, 135fc3509e) leaves the inflection served output unchanged. |
| data/assets/scripts/gold/investor_reporting/holdings_snapshot.py | changed | null | 1464de48be | behaviour | The live copy matches no commit in the history of this file. Against it the pin adds the signed IR cash rule on both classify layers (IB-pr-527 and IB-pr-529), the signed exemption repair (IB-pr-530), the publish-gate keyed summary (IB-pr-414), a CUSIP fallback for canonical lookups after a symbol miss (SC-e-56), the multi_asset line of the six-class rule (SC-e-56), and the additive account_id member, which is written only when a caller passes one; the inflection served asset classes and the gate outcome are re-measured in the remeasure block. |
| data/assets/scripts/gold/investor_reporting/schwab_account_codes.json | changed | b47987ae49 | b47987ae49 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| data/assets/scripts/silver/opal_strategy_matcher.py | added | null | 099632f46c | behaviour | New module loaded at import time by rebalancer_schemas.py (the cottonwood run only) and read by build_cottonwood_mdpf_slice.py inside a function; rebalancer_schemas.py imports it at module level, so the bundle must carry it or the cottonwood import fails. It reads the shared strategy config from S3 on first call, and the 49financial and inflection runs do not import it. |
| data/assets/scripts/silver/rebalancer_schemas.py | changed | 9efbec3c2f | 2727ad0214 | behaviour | Not reached by the inflection run: rebalancer_schemas is imported only inside the COT taxonomy helper and by the slice and dim-model builders, and the inflection builder calls none of them. The change (commits 2727ad0214 and 099632f46c) moves opal_sma_member_of onto the shared StrategyMatcher; is_opal_name is unchanged. |
| data/firm_registry.json | changed | 8e9ed1b539 | 69679b90e3 | data | The only changed line is the _generated provenance string (registry revision ffa41913 to 9f1cc0a3, commits 6c962b0a52 and 69679b90e3); no firm row, alias or bucket value in the file differs, so the firm set the producer reads is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_account_distribution.py | changed | e20899bce7 | 94ff221642 | behaviour | Not reached by the producer's run: this module is imported only by build_cottonwood_mdpf_pair, which only the cottonwood COT taxonomy helper imports, and the producer calls none of its functions. The change (commits 94ff221642 and ed1c20d805) folds the Cottonwood model keys into one other_models line in the MDPF Global distribution. |
| data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py | changed | 85dd7adc26 | ed1c20d805 | docs | Comments and docstrings only: the parse tree with docstrings removed is identical to the pin's, so the code the producer runs is unchanged. |
| data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py | changed | 1e5e13d223 | 94ff221642 | behaviour | Not reached by the producer's run: imported only by build_cottonwood_mdpf_pair, and the producer calls none of its functions. The change (commits a85ecada1f and 94ff221642) adds the other_models line and an SMA additive component to the MDPF Global composition, which the producer does not compute. |
| data/mdpf/scripts/gold/mdpf_category_registry.py | changed | 46d04eb7b6 | fab599bcea | behaviour | Adds the SMA basis tables, sma_global_basis_of and a per-firm population rule for the MDPF Global views (commits 93de0c2336 and fab599bcea) and a signature change to build_category_views. The producer reads only VIEW_TREE and resolve from this module (taxonomy_path); neither is in a changed hunk and build_category_views is not called by the producer, so the served taxonomy paths are unchanged. |
| data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py | changed | 85dd7adc26 | 94ff221642 | behaviour | Adds an id-less other_models CANONICAL_MODELS row (commit 94ff221642, CN-f-1). The producer resolves a model's key only through resolve_model_id and resolve_eclipse_id, which key on a SmartX or Eclipse id, and the new row carries no id, so the served model_key of each model leaf is unchanged. |
| docs/contracts/investor-reporting/v1/CurrencyAuthorities.json | changed | 98b4416105 | 98b4416105 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json | changed | 9e58503be1 | 506096fc9a | data | Adds the optional ACCOUNT-node account_id member (commit 7ace854890, IB-pr-493). The member is written only when a caller passes an account id, so the cottonwood and inflection nodes carry no new member, and the schema change is additive for every firm. |
| infra/aws/lambda/investor-reporting/_ids/ids.py | changed | 47f21dab95 | 11ba48fdc7 | behaviour | The change sits inside projection_with_seam, which the holdings producer does not call (its callers are the irpt_custody readers and the tests, by grep of the pin); the producer imports this module only for the id normalizer, which the diff leaves unchanged, so no served field moves (commits e962a5cb81 and 11ba48fdc7). |
| infra/logic/registry/exemptions.json | changed | 8b4c15c6ba | 61cc536c29 | data | Adds fence and exemption rows that opal_naming reads at run time (commits 2a809c975e through 61cc536c29); the holdings producer does not read exemptions.json, and the write addresses are equal, so no holdings output moves. |
| infra/logic/registry/remediations.json | changed | fd3b3b7bf2 | fd3b3b7bf2 | line_endings | Line endings only: the folded contents are equal to the pin's, so no served output can change from this member. |
| infra/logic/registry/reporting_policies.json | changed | f60e6f1d2a | 103902e75d | data | Activates the irpt-custody-x10 and irpt-anlreq-x10 policy rows and widens the research-policy firm list (commits 0798635fec through 103902e75d); the holdings producer does not read reporting_policies.json (no reference in holdings_snapshot.py) and its write addresses are equal, so no holdings page moves. |
| infra/logic/registry/resources.json | changed | f185873e6b | 17ae4222c7 | data | Removes the openpyxl-layer library row (commit 17ae4222c7); the producer's write addresses are built by address() and are equal under the live and pin trees, so no served address moves. |
| infra/logic/registry/scopes.json | changed | 0146e0c954 | 69679b90e3 | data | Adds tenant pages, an inflection MASTER row, a restricted-prefix host and transitional tier_live and product_live rows, and flips the 49financial opal-data-bd alias routed flag to false (commits 5f962296ae, a15fb36a4c, 69679b90e3); the firm_bucket_map body generated into holdings_snapshot.py is unchanged and the write addresses are equal, so no firm write moves. |
| infra/logic/registry/systems.json | changed | 224058ea3f | 826364c980 | data | Adds the commonwealth and yahoo VENDOR rows and re-states owner claims (commits 8e39143feb, 530ef17ff8, 826364c980); holdings_snapshot.py source_vendor_keys matches VENDOR keys word-bounded against each builder's source text, and no firm's source text names either added key, so the served source vendor keys are unchanged. |
| lib/opal_naming.py | changed | b77e2af4d5 | 6ae365f583 | behaviour | The builder gains the firm_pages.json reader and the portal firm-matrix generator (commits a99d7e584c, c5d1415676, 6ae365f583) and the ownership and fence helpers (commits 7d0f46fe7c through b81373cbcc); address() and lookup() return the same strings for the producer's seven write shapes under the live and the pin trees (write_addresses equal for every firm), so no write address moves. |
| lib/trading_calendar.py | changed | 0cbb0ad174 | b2b7488660 | data | Under the fallback a year outside 2010 to 2027 now raises CalendarCoverageError instead of answering, and the fallback announces once on stderr (commits 4b766e4e2d and b2b7488660); the holiday set and the T-1 answers for the producer's window are equal (calendar block), so no served business date moves. |
| org/standards/NAMING_SCHEMA.json | changed | aa2b5a42ff | eb29bf7f37 | data | The naming schema that opal_naming reads at run time gains the user and group kinds, the fifo suffix rule, the fourth verdict and the cadence rules (commits 01c56eda2b, 1ea925a095, 19b61836e4, f701d5da50, eb29bf7f37); the producer's write addresses are equal under both trees, so no served address moves. |

Folded sha256 values, per member, are in the record (IB194-1_packet_v2_record.json, members block). Digests are not repeated here.

Section 6 reads inflection PUBLISHED before and after. The differential in section 13 measures inflection REFUSED on source_frontier_older on both codes at pin 2026-10-13; the table above is not re-cut here, and section 13 records the measured gate.

## 3. Trading calendar: holiday delta and T-1, old against new

The trading calendar member (lib/trading_calendar.py) has live commit 0cbb0ad174d4786879466662b1f9a7c5f3d75b14 and pin commit b2b748866020370ebbef91fc5f4378b4cafb5f58. Both were loaded from their committed blobs as two modules; each answers from its NYSE fallback holiday set in this environment (pandas_market_calendars is absent, so the module's own WARN line prints on import). Neither module carries an early-close table.

Window 2026-10-01 to 2027-12-31. Holidays added in the window: none. Holidays removed in the window: none.

The next three scheduled fire dates and their T-1 under each module:

| fire date | T-1 old | T-1 new | differs |
|---|---|---|---|
| 2026-10-14 | 2026-10-13 | 2026-10-13 | no |
| 2026-10-15 | 2026-10-14 | 2026-10-14 | no |
| 2026-10-16 | 2026-10-15 | 2026-10-15 | no |

The calendar effect on the three fires is nil. The fallback change (a year outside 2010 to 2027 now raises CalendarCoverageError, and the fallback announces once on stderr) lies outside the window and does not move a T-1 answer.

## 4. Write addresses the producer writes, old against new

Each firm's addresses were produced by calling lib/opal_naming.py address() once under the live bundle (the untarred live bundle as the repository root, its own registries) and once under the pin tree, with the same arguments the publication code uses: the gold holdings revision object, the platinum revision and its header, part and manifest objects, current/manifest.json and current/publish_refusal.json. The date is normalised to date=* and the revision to <revision>.

- 49financial: equal = true; seven shapes old and new. Old: s3://opal-data-49financial/irpt/49financial/gold/holdings/date=*/<revision>.parquet; s3://opal-data-49financial/irpt/49financial/platinum/holdings/date=*/<revision>.json; s3://opal-data-49financial/irpt/49financial/platinum/holdings/date=*/<revision>.header.json; s3://opal-data-49financial/irpt/49financial/platinum/holdings/date=*/<revision>.part00001.json; s3://opal-data-49financial/irpt/49financial/platinum/holdings/date=*/<revision>.manifest.json; s3://opal-data-49financial/irpt/49financial/platinum/holdings/current/manifest.json; s3://opal-data-49financial/irpt/49financial/platinum/holdings/current/publish_refusal.json
- cottonwood: equal = true; seven shapes old and new. Old: s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings/date=*/<revision>.parquet; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/date=*/<revision>.json; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/date=*/<revision>.header.json; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/date=*/<revision>.part00001.json; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/date=*/<revision>.manifest.json; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/current/manifest.json; s3://opal-data-cottonwood/irpt/cottonwood/platinum/holdings/current/publish_refusal.json
- inflection: equal = true; seven shapes old and new. Old: s3://opal-data-inflection/irpt/inflection/gold/holdings/date=*/<revision>.parquet; s3://opal-data-inflection/irpt/inflection/platinum/holdings/date=*/<revision>.json; s3://opal-data-inflection/irpt/inflection/platinum/holdings/date=*/<revision>.header.json; s3://opal-data-inflection/irpt/inflection/platinum/holdings/date=*/<revision>.part00001.json; s3://opal-data-inflection/irpt/inflection/platinum/holdings/date=*/<revision>.manifest.json; s3://opal-data-inflection/irpt/inflection/platinum/holdings/current/manifest.json; s3://opal-data-inflection/irpt/inflection/platinum/holdings/current/publish_refusal.json

A difference in any write address would be a STOP and a separate pair. None was found: the old and new lists are equal for every firm. The QA table (holdings_qa) is not written by the production publication and was not enumerated.

## 5. The added matcher: opal_strategy_matcher

The added member data/assets/scripts/silver/opal_strategy_matcher.py has importer data/assets/scripts/silver/rebalancer_schemas.py (module-level import, its line 42; the importer is inside the pin closure and is reached by the cottonwood run through the COT taxonomy helper). build_cottonwood_mdpf_slice.py also imports it, inside a function. The member is not dropped: without it the cottonwood import of rebalancer_schemas.py fails, so the mint must carry it. The 49financial and inflection runs do not import it.

## 6. Re-measure against the signed counts

The committed harness (deliverables/0.9.0_WK_IRPT_BCKEND~380/release_count_harness.py) ran from this worktree with the pin tree as its repository root, --as-of 2026-10-12,inflection=2026-10-13, read only. Its output is the remeasure block of the record.

| firm | canonical movers | fallback movers | gate before | gate after | lost accounts listed | matches v1 |
|---|---|---|---|---|---|---|
| 49financial | 32 | 0 | PUBLISHED | PUBLISHED | 0 | yes |
| cottonwood | 38 | 211 | REFUSED | PUBLISHED | 1 | yes |
| inflection | 774 | 67 | PUBLISHED | PUBLISHED | 0 | yes |

Pins: 49financial 2026-10-12, cottonwood 2026-10-12, inflection 2026-10-13. A difference from the signed counts would be a measurement, and the release stops at the stop rule (section 10).

Section 13 adds one module to this check: data/assets/scripts/silver/opal_unidentified.py is imported by the pin's cottonwood builder and is absent from the cottonwood table, so the cottonwood digest gate below cannot see it. The issuer amends the table before any mint.

## 7. Branch A: the three mints (NOT run in this order)

Branch A is the FULL pin mint, from a worktree at the pin 49467335d288d5c0012fe339c4cafcb74bd43fb5, one firm per mint: bash .tools/safe-deploy.sh --mint-bundle irpt_holdings_49f, then irpt_holdings_cot, then irpt_holdings_inf, one session between fires. The mint opens no change-management ledger; the releasing seat opens its own (section 11).

Digest gate of v2, per built bundle: the changed members of each built bundle must equal exactly the paths of that firm's table in section 2 plus SHA256SUMS, and each pin blob's folded sha256 must equal the table's pin_folded_sha256. Any other member, or any other hash, STOPS the release. The built bundle must hold the 46 closure members of the pin (45 plus SHA256SUMS).

## 8. Branch B: rollback, and the manifest anchors

Prior bundle version, per firm, by version id (the rollback target, restored by copy-object with CopySource VersionId over the same key): 49financial UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD (last modified 2026-10-13T13:35:24Z); cottonwood oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_ (2026-10-09T10:29:07Z); inflection PzhCs97qVBXkZcIjaOklHmzWiFsOFafM (2026-10-13T13:36:08Z).

Manifest anchors (the recorded page anchors, carried from v1 and not re-read in this order): 49financial daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh; cottonwood lQMhNnImgj0ikICMdhFeasBGJKSbl55s; inflection MLSPlfHHsZa7mSnXEzorRkR9zgs2Q68u. A manifest version newer than the anchor is admitted only as the only newer one, written by that firm's scheduled fire of the day and dated T-1 by lib/trading_calendar.py.

Per-firm business-date rule: a firm's fire stamps the business date T-1 by lib/trading_calendar.py, with a T-1 partition under it; or it holds by name on an absent T-1 partition with the served frontier unchanged. A wrong stamp is a STOP. A late firm never rolls the other two back.

## 9. Blast radius, per firm and per change

Every other date is untouched: the release writes only the business date of each firm's own fire, and the served index history before that fire is not rewritten. The 49financial 2026-10-08 gap stays absent, as v1 recorded.

Cash rule: 49financial moves 32 canonical and 0 fallback nodes; cottonwood 38 canonical and 211 fallback; inflection 774 canonical and 67 fallback (the re-measure above). Exemption repair: cottonwood's REFUSED candidate becomes PUBLISHED with one lost account listed (a count only); no gate outcome changes for 49financial or inflection.

Calendar effect: nil for the three fire dates and for the window (section 3). Write addresses: unchanged (section 4). Added members per section 2 carry their own effect lines; for cottonwood and inflection the account_id member is written only when a caller passes one, so no node of theirs gains a member from it.

Rollback per key: Branch B. Restoring the bundle restores the code for the next scheduled fire; what cannot be undone is any fire already published, which stays in the bucket as its own revision, and any reader that already fetched a page.

Section 13 gives the per-firm totals of the cash rule (49financial 32, cottonwood 249, inflection 841: the same totals as the canonical and fallback movers above) and the 236 non-rule Cottonwood nodes that this section did not carry. Write addresses and the calendar are unchanged by the differential.

## 10. Stop rule (both branches)

The release stops, and this packet is re-cut, unless at the release the counts match this packet: the per-firm canonical and fallback movers, the lost-account count, and the gate outcome and conditions before and after. A differing count means a different candidate. Any digest-gate mismatch of Branch A, any changed write address, and any moved member outside section 2 also stops the release.

## 11. The releasing seat's own NEVER-2 ledger

The releasing seat opens its own change-management entry at the start of the release, under org/critical_paths/change_management/, naming every leg:

1. the mint of irpt_holdings_49f, irpt_holdings_cot and irpt_holdings_inf (each a leg);
2. the first scheduled fire's after-read per firm: each firm's current/manifest.json latest business date after the fire, and for cottonwood a business date past 2026-10-08 with its lost account listed (count 1 at this measurement);
3. the rule's after-read: FDRXX and the other Cash-sub holdings read Cash in the published page;
4. the 49financial 2026-10-08 gap, unchanged after the release;
5. one read-only kernel-log count after the first fire while the host is Online (added to v1's four legs).

The after-read states what to read; the value is measured then, not predicted here.

## 12. What this packet does not measure

The current manifest versions beyond the recorded anchors; the bundle sha256 values of the new mints; the first fire's outcome; the calendar's pandas_market_calendars path (the fallback answered in this environment); any holding value, account identifier or holding name (none is written here); the producer under the scheduler. The check defect that stops AC1 of the order is a channel row, not a packet fact.

## 13. The live-against-pin differential (the signed scope)

### 13.1 Scope and method

This section is the differential of the holdings-producer release, measured on the same pinned source receipts for both codes: the code the live bundles serve now (the live-against-pin side) against the code at the pin 49467335d288 (the pin side). The live bundle version ids are those of section 8, and the bytes downloaded by those version ids are the build input. The candidate of each code is built for the custody pin of its firm (49financial 2026-10-12, cottonwood 2026-10-12, inflection 2026-10-13); the business date built is 2026-10-12 on both codes for every firm, so the candidate is dated one trading day before its custody pin on each. Read only: the harness makes get and list calls with the worker's identity and refuses every other S3 operation. Harness: deliverables/0.9.0_WK_IRPT_BCKEND~384/live_pin_differential.py. Record: deliverables/0.9.0_WK_IRPT_BCKEND~384/IB195-1_differential_record.json. Nothing is minted, uploaded, applied, deployed, signed or sent.

Attribution rules. A changed node is attributed to the signed cash rule (attributed by identity-patch) when the pin, rebuilt with apply_cash_rule replaced by the identity function inside the harness, differs from the pin's asset_class and the live asset_class equals the identity value. Every other changed field is attributed to the member whose swap alone reproduces it (attributed by member-swap): the live tree with that one member replaced by the pin bytes, built on the same receipts. A field no single member reproduces, or whose commits do not name account_id, the keyed gate, the CUSIP fallback or multi_asset, is UNATTRIBUTED, and an UNATTRIBUTED node is a stop. The count of UNATTRIBUTED nodes is 0 on every firm (section 13.2).

The signed scope. The signed scope of packet v3 is the differential in section 13.2: per firm, every difference group with its node count, its attribution, its members and its commits. A sign-off of v3 covers these groups and no others. The release reproduces them on the three bundles, and any other group, any unattributed node, any gate difference other than the signed exemption repair, or any moved member outside section 2 and the one named module in section 13.3 stops the release (section 10).

### 13.2 The differential, per firm

Signed cash rule counts: 49financial 32, cottonwood 249, inflection 841; the identity-patch measurement equals each signed count. Cottonwood carries 291 further changed nodes that the signed rule does not explain (see 13.3).

### 13.2.1 49financial (custody pin 2026-10-12)

| node kind | live | pin |
|---|---|---|
| ACCOUNT | 7640 | 7640 |
| CASH | 9226 | 9226 |
| CATEGORY | 7640 | 7640 |
| MODEL_LEAF | 7567 | 7567 |
| SECURITY | 124431 | 124431 |

Account set (ACCOUNT nodes): only on live 0, only on pin 0, on both 7640.
Changed values (absolute tolerance 0.01): nodes with a changed numeric value 0; largest absolute delta 0.0, field none.
Gate on the live code: PUBLISHED (no condition). Gate on the pin code: PUBLISHED (no condition). Gate attribution: same.
Changed nodes: total 32; attributed 32; UNATTRIBUTED 0 (distinct nodes).

| difference group | nodes | attribution | attributed by | members (v2 table) | commits |
|---|---|---|---|---|---|
| asset_class: fixed_income -> cash | 32 | signed_cash_rule | identity-patch | none | none |

Digests (sha256 of the canonical comparison result): run 1 55921f975706ca61c576b76781b022a94c9351dc4d85909206985ba3775233c7; run 2 55921f975706ca61c576b76781b022a94c9351dc4d85909206985ba3775233c7. The two runs are equal: one digest per firm.
Planted mutant: one asset_class value changed in the pin signature; flagged true; changed nodes with the mutant 33 (the unmutated count is 32, so the mutant raised the count by exactly one).

### 13.2.2 cottonwood (custody pin 2026-10-12)

| node kind | live | pin |
|---|---|---|
| ACCOUNT | 867 | 867 |
| CATEGORY | 871 | 871 |
| MODEL_LEAF | 557 | 557 |
| SECURITY | 15558 | 15558 |
| SLEEVE | 113 | 113 |

Account set (ACCOUNT nodes): only on live 0, only on pin 0, on both 867.
Changed values (absolute tolerance 0.01): nodes with a changed numeric value 0; largest absolute delta 0.0, field none.
Gate on the live code: REFUSED (account_lost). Gate on the pin code: PUBLISHED (no condition). Gate attribution: signed_exemption_repair.
Changed nodes: total 485; attributed 485; UNATTRIBUTED 0 (distinct nodes).

| difference group | nodes | attribution | attributed by | members (v2 table) | commits |
|---|---|---|---|---|---|
| asset_class: fixed_income -> cash | 4 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| asset_class: fixed_income -> cash | 249 | signed_cash_rule | identity-patch | none | none |
| asset_class_basis: NAME_ALIAS -> TABLE | 234 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| asset_class_basis: NAME_PATTERN -> TABLE | 2 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Cash -> (absent) | 2 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Cash -> Money Market | 4 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Intermediate -> (absent) | 12 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Investment Grade -> (absent) | 29 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Investment Grade -> Municipal | 2 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: Municipal -> (absent) | 1 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |
| sub_asset_class: US Small Cap -> (absent) | 1 | W383-S2:holdings_snapshot | member-swap | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | 3f2bdda5784ec1c71eaeb78ffb218daafe517d29, 4cc72587d6336809adbb3a46b119a304ef0a6dff, 7ace8548905d66ef98358c384cb320f12c2683e4, 9efbec3c2fd8867151f6f903dad796716ae2c577, f3a42b2ab81d080c317bb1177c04b556d775a4dd |

Digests (sha256 of the canonical comparison result): run 1 4ab73be7139900da521ee98f0043efe5b2065c7e946adb7d45afeee77669b886; run 2 4ab73be7139900da521ee98f0043efe5b2065c7e946adb7d45afeee77669b886. The two runs are equal: one digest per firm.
Planted mutant: one asset_class value changed in the pin signature; flagged true; changed nodes with the mutant 486 (the unmutated count is 485, so the mutant raised the count by exactly one).

### 13.2.3 inflection (custody pin 2026-10-13)

| node kind | live | pin |
|---|---|---|
| ACCOUNT | 863 | 863 |
| CATEGORY | 940 | 940 |
| MODEL_LEAF | 626 | 626 |
| SECURITY | 34273 | 34273 |

Account set (ACCOUNT nodes): only on live 0, only on pin 0, on both 863.
Changed values (absolute tolerance 0.01): nodes with a changed numeric value 0; largest absolute delta 0.0, field none.
Gate on the live code: REFUSED (source_frontier_older). Gate on the pin code: REFUSED (source_frontier_older). Gate attribution: same.
Changed nodes: total 841; attributed 841; UNATTRIBUTED 0 (distinct nodes).

| difference group | nodes | attribution | attributed by | members (v2 table) | commits |
|---|---|---|---|---|---|
| asset_class: fixed_income -> cash | 841 | signed_cash_rule | identity-patch | none | none |

Digests (sha256 of the canonical comparison result): run 1 3d97a0451cd13b0888f9330453c8a25602343eb6b03c5cbddb5a28fa03515624; run 2 3d97a0451cd13b0888f9330453c8a25602343eb6b03c5cbddb5a28fa03515624. The two runs are equal: one digest per firm.
Planted mutant: one asset_class value changed in the pin signature; flagged true; changed nodes with the mutant 842 (the unmutated count is 841, so the mutant raised the count by exactly one).

Difference group labels in this section, every firm: asset_class: fixed_income -> cash; asset_class_basis: NAME_ALIAS -> TABLE; asset_class_basis: NAME_PATTERN -> TABLE; sub_asset_class: Cash -> (absent); sub_asset_class: Cash -> Money Market; sub_asset_class: Intermediate -> (absent); sub_asset_class: Investment Grade -> (absent); sub_asset_class: Investment Grade -> Municipal; sub_asset_class: Municipal -> (absent); sub_asset_class: US Small Cap -> (absent).

### 13.3 What the differential adds to the release, and what it names

1. The moved members named by the attributions are holdings_snapshot.py (cottonwood only, for the 291 non-rule nodes) and, for the signed rule, the pin's holdings_snapshot.py as a whole. No other section 2 member reproduces any node of any group. Section 2 stays the table of members; this section adds no member to it.
2. Four cottonwood nodes move fixed_income to cash on the pin without the rule: their identity-patch value is already cash. Their move is a non-rule holdings_snapshot.py change, named as the group asset_class: fixed_income -> cash under the member attribution, separate from the 249 signed nodes. The sub-cause inside holdings_snapshot.py (keyed gate, CUSIP fallback, multi_asset line, account_id, exemption repair) is not separated by this measurement; the member is the unit of attribution.
3. The cottonwood publish gate changes only as the signed exemption repair: the live code refuses on account_lost and the pin publishes. 49financial publishes on both codes. Inflection refuses on both codes on source_frontier_older, so its gate is the same on both codes, but it is REFUSED, not PUBLISHED as section 6 reads; section 6 is not re-cut here, and this section records the measured gate.
4. Named, not in section 2: data/assets/scripts/silver/opal_unidentified.py (pin bytes). The pin's cottonwood builder imports it (build_cottonwood_mdpf_slice.py), no live bundle holds it, and section 2 does not list it, so a hybrid of that member built only on the live tree fails to import. The measurement copied that one pin file into that hybrid alone and recorded it. The closure the Branch A digest gate expects is therefore one module short for cottonwood. The issuer amends the section 2 table before any mint; this packet does not add it to section 2.
5. Branch A (the three mints) cannot run on the section 2 table as written: the cottonwood digest gate of section 7 would pass a bundle that cannot import its cottonwood taxonomy path. Branch B (rollback by version id) and the manifest anchors of section 8 are unchanged: the differential does not read the current manifests, and the anchors are carried as recorded. The per-firm business date rule of section 8 is unchanged; the candidate's business date is 2026-10-12 on both codes for every firm.

### 13.4 Why the two runs and the mutant

Run 2 rebuilt the pin candidate, the identity candidate and the live candidate on the run-1 receipts; receipts, gate results and comparison results equal run 1 on every firm. The hybrid signatures were built once and reused by both comparisons. The planted mutant changed one pin asset_class value in memory and raised the changed-node count by exactly one on every firm, so the comparison discriminates.

### 13.5 Measured limits

Numeric leaves were compared with an absolute tolerance of 0.01 and none differed on any firm, so the largest absolute delta is 0.0 with no field. The snapshot-level clocks were not compared node by node. No account id, node id, position quantity or holding name is in this packet or its record; the per-node signatures and receipts are outside the repository.

## 14. Signatures

COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes.

CTO half: 1.0.0_SA_CTO -- UNSIGNED at these packet bytes.

The packet's own sha256 is left for the signers and is not computed here. Both halves are signed at these packet bytes before Branch A may run, and a signature covers the signed scope of section 13 as written.

