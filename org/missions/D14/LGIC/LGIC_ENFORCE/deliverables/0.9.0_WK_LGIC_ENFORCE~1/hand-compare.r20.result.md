# hand-compare.r20.result -- the hand ranking against the round-20 census (LGIC_ENFORCE EN-z-2, FWD-5 clause 3)

Written by `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/build_hand_compare_r20.py` from `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/HAND_REMEASURE_R19.json`; the facts each explanation cites are read from git objects at build time.

- Census compared against: `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r20.md`
- Census vintage: Built from the estate as of 2026-10-09 12:52:02 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z.  manifest: afb76c769ceb (registry f936f6350cc5c404; grade() at HEAD reads the same registry hash)
- Hand side: round 19's re-measured hand verdicts and figures, read as written, never re-graded (vintage commit `54659987c0bd95069d57ab78e425b28678dc32fb`).
- Positive control passed: the comparator over the round-8 machine side reproduces round 19's {"compared": 143, "agree": 140, "disagree": 3}.

## Totals

| surface | compared | agree (r20) | disagree (r20) | round 19: agree | round 19: disagree | machine side read from |
|---|---|---|---|---|---|---|
| grading_rule_worked_cases | 45 | 39 | 6 | 45 | 0 | grade_at_head_not_in_r20 11, r20_row 34 |
| n6_grader_rows | 88 | 72 | 16 | 86 | 2 | grade_at_head_carded 9, grade_at_head_not_in_r20 21, r20_row 58 |
| tension_ranking_surfaces | 10 | 6 | 4 | 9 | 1 | iv7_over_r20_report 10 |
| **total** | **143** | **117** | **26** | **140** | **3** | |

The round-19 hand re-measure agreed with the round-8 census on 140 of 143 keys; against the round-20 census it agrees on 117 of 143. Every one of the 26 differences below carries an explanation read at the bytes. 24 of them are the estate or the grading rule moving between the round-8 and round-20 readings (registry rows, system keys, the fourth verdict, or the estate itself); 2 (rank-5, the instrument gap, and ExecIncrParityFailure, the machine-side departure from GRADING_RULE.md N2) were already open in round 9 and round 19.

## Differences, with the cause class counted

- ESTATE_MOVED: 3
- FOURTH_VERDICT: 2
- INSTRUMENT_GAP: 1
- RESOURCE_ROW_ADDED: 14
- RESOURCE_ROW_REPOINTED: 2
- SYSTEM_KEY_ADDED: 2
- TOKEN_RESOLVED: 1
- WRITTEN_RULE_DEPARTURE_PLUS_ROW: 1

## grading_rule_worked_cases -- 45 compared, 39 agree, 6 disagree

### LAMBDA::inf-silver-chain  [RESOURCE_ROW_REPOINTED]

- hand: OUT-OF-PATTERN advi-inf-silver-chain-lambda
- machine: OUT-OF-PATTERN orion-inf-silver-chain-lambda  (r20 report row (live plane, 1 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form leads with 'advi', the system the resources.json row (inf-silver-chain, LAMBDA) carried at the census commit 54659987c0. At HEAD the same row names 'orion' (re-pointed at b282500581 (2026-09-21, 4.0.0_SA_CRO)). Its evidence: "RE-POINTED advi -> orion (Andrew-direct 2026-09-21 at the 4.0.0_SA_CRO terminal ~18:4xZ, 'recs approved'; its job reads ONLY orion (inf-silver-chain); SY1 first clause). ". The r20 run reads the re-pointed row and leads with 'orion'; every other token is byte-equal.

### API_GW::opal-portal-data-proxy-api  [SYSTEM_KEY_ADDED]

- hand: CONFORMANT opal-portal-data-proxy-api
- machine: OUT-OF-PATTERN portal-data-proxy-api  (r20 report row (live+repo plane, 2 row(s)); differs in verdict)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. At the census commit 54659987c0 systems.json holds no row with key 'portal' and none with long form 'opal-portal', so 'opal-portal-data-proxy-api' read as the reserved opal prefix plus a name and the hand rule (applied at that vintage in round 19) rules it CONFORMANT. At HEAD systems.json carries the row {key: portal, class: PLATFORM_SUBSYSTEM, long: opal-portal}, first added at 6c07797a9c (2026-09-21, 4.0.0_SA_CRO); the name now leads with that system's long form, the system slot takes the key, and the canonical form becomes portal-data-proxy-api, so the name is OUT-OF-PATTERN. The r20 run (registry f936f6350cc5c404) reads the HEAD registry.

### CW_ALARM::Inflection-SilverChain-DimConversionFailure  [RESOURCE_ROW_REPOINTED]

- hand: OUT-OF-PATTERN advi-inf-silver-chain-dim-conversion-failure-alarm
- machine: OUT-OF-PATTERN orion-inf-silver-chain-dim-conversion-failure-alarm  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form leads with 'advi', the system the resources.json row (Inflection-SilverChain-DimConversionFailure, CW_ALARM) carried at the census commit 54659987c0. At HEAD the same row names 'orion' (re-pointed at f185873e6b (2026-09-21, 4.0.0_SA_CRO)). Its evidence: 'RE-POINTED advi -> orion (4.0.0_SA_CRO 2026-09-21 ~21:2xZ): declared in inf-silver-chain.tf, the job that reads ONLY orion; its Lambda, role, rule and policy were re-poin'. The r20 run reads the re-pointed row and leads with 'orion'; every other token is byte-equal.

### LAMBDA_LAYER::pandas-pyarrow-layer  [FOURTH_VERDICT]

- hand: OUT-OF-PATTERN {system}-pandas-pyarrow-layer
- machine: NO-SYSTEM-ASKED pandas-pyarrow-layer  (r20 report row (live plane, 1 row(s)); differs in verdict)
- explanation: THE GRADING RULE MOVED between the two readings; neither side is wrong. The hand verdict is the hand rule's own (three verdicts: lib/opal_naming.py at the census commit 54659987c0 has no NO-SYSTEM-ASKED and NAMING_SCHEMA.json grade.verdicts there lists 3). At HEAD grade.verdicts lists 4 and lib/opal_naming.py carries _NO_SYSTEM_ASKED (landed at 19b61836e4 (2026-10-07, 0.9.0_WK_LGIC_BLANKFIX~2)): a library layer / purpose-word-led policy name with no resolved system takes the fourth verdict and a canonical form with no system slot. For (pandas-pyarrow-layer, LAMBDA_LAYER) the r20 run reads NO-SYSTEM-ASKED with canonical pandas-pyarrow-layer; the hand form differs only in the '{system}-' blank the rule no longer owes.

### SCHEDULE::wsb-49f-model-aua-pull-daily  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-49f-wsb-model-aua-pull-daily
- machine: OUT-OF-PATTERN mdpf-49f-wsb-model-aua-pull-daily  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (wsb-49f-model-aua-pull-daily, SCHEDULE) (91 rows there). At HEAD (464 rows) the row (wsb-49f-model-aua-pull-daily, SCHEDULE) -> mdpf is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F14 -- a5 family F14, leading token 'wsb' (census row 'wsb-49f-model-aua-pull-daily', LGIC placeholder recount @0f1caafb1d; Andrew-direct 2026-0". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: mdpf-49f-wsb-model-aua-pull-daily. Every other token of the canonical form is byte-equal to the hand's.

### SECRET::inf/otp-relay/token  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}/inf/otp-relay/token
- machine: OUT-OF-PATTERN portal/inf/otp-relay/token  (r20 report row (live+repo plane, 3 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (inf/otp-relay/token, SECRET) (91 rows there). At HEAD (464 rows) the row (inf/otp-relay/token, SECRET) -> portal is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). The row was later RE-POINTED to this system at 6c07797a9c (2026-09-21, 4.0.0_SA_CRO). Its evidence: "RE-POINTED gateway -> portal (Andrew-direct 2026-09-21 ~19:0xZ 'yes agreed on both'; 'gateway' is the Opal Gateway, NFRA_OPLGTW, which 4.0.0_SA_CRO ha". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: portal/inf/otp-relay/token. Every other token of the canonical form is byte-equal to the hand's.

## n6_grader_rows -- 88 compared, 72 agree, 16 disagree

### CODEBUILD_PROJECT::semantic-clustering-lambda-build  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-semantic-clustering-lambda-build
- machine: OUT-OF-PATTERN news-semantic-clustering-lambda-build  (r20 report row (live plane, 1 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (semantic-clustering-lambda-build, CODEBUILD_PROJECT) (91 rows there). At HEAD (464 rows) the row (semantic-clustering-lambda-build, CODEBUILD_PROJECT) -> news is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F03 -- a5 family F03, leading token 'semantic' (census row '/aws/codebuild/semantic-clustering-lambda-build', LGIC placeholder recount @0f1caafb". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: news-semantic-clustering-lambda-build. Every other token of the canonical form is byte-equal to the hand's.

### CW_ALARM::ExecIncrParityFailure  [WRITTEN_RULE_DEPARTURE_PLUS_ROW]

- hand: OUT-OF-PATTERN {system}-exec-incr-parity-failure-alarm
- machine: OUT-OF-PATTERN globgrph-exec-incrparity-failure-alarm  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: TWO DIFFERENCES, ONE STANDING SINCE ROUND 9. (1) ESTATE MOVED: the hand's '{system}' blank is filled by the resources.json row (ExecIncrParityFailure, CW_ALARM) -> globgrph, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO) (absent at the census commit 54659987c0). (2) UNMOVED, the machine side departs from the written rule: GRADING_RULE.md N2 (read at HEAD) says 'Split before each capital that follows a lowercase letter or a digit ... Then lowercase each piece' and states no re-join, so the hand form is 'exec-incr-parity-failure'; grade() re-joins the pieces of one original segment whose concatenation is a vocabulary word and 'incrparity' is a token in systems.json at the census commit and at HEAD, so grade() writes 'exec-incrparity-failure'. The hand follows the rule as written; the departure is the machine's, it is the same one round 9 recorded, and no ruling has settled whether N2 lacks a re-join clause or grade() carries one it should not.

### CW_ALARM::exec-summary-advisors-processed-ceiling  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-exec-summary-advisors-processed-ceiling-alarm
- machine: OUT-OF-PATTERN advi-exec-summary-advisors-processed-ceiling-alarm  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (exec-summary-advisors-processed-ceiling, CW_ALARM) (91 rows there). At HEAD (464 rows) the row (exec-summary-advisors-processed-ceiling, CW_ALARM) -> advi is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F10 -- a5 family F10, leading token 'exec' (census row 'exec-summary-advisors-processed-ceiling', LGIC placeholder recount @0f1caafb1d; Andrew-d". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: advi-exec-summary-advisors-processed-ceiling-alarm. Every other token of the canonical form is byte-equal to the hand's.

### CW_ALARM::wsd-49f-partner-held-etf-daily-errors  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-49f-wsd-partner-held-etf-daily-errors-alarm
- machine: OUT-OF-PATTERN mdpf-49f-wsd-partner-held-etf-daily-errors-alarm  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (wsd-49f-partner-held-etf-daily-errors, CW_ALARM) (91 rows there). At HEAD (464 rows) the row (wsd-49f-partner-held-etf-daily-errors, CW_ALARM) -> mdpf is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F14 -- a5 family F14, leading token 'wsd' (census row 'wsd-49f-partner-held-etf-daily-errors', LGIC placeholder recount @0f1caafb1d; Andrew-dire". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: mdpf-49f-wsd-partner-held-etf-daily-errors-alarm. Every other token of the canonical form is byte-equal to the hand's.

### DYNAMODB_TABLE::bd-securities  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-49f-securities-table
- machine: OUT-OF-PATTERN advi-49f-securities-table  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (bd-securities, DYNAMODB_TABLE) (91 rows there). At HEAD (464 rows) the row (bd-securities, DYNAMODB_TABLE) -> advi is present, first added at b282500581 (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL1 SY1 -- PRODUCT (ROOT): infra/aws/terraform/shared-infra/main.tf:363 (header 'ADVI_CLSUNI: bd-securities DynamoDB Table'); Andrew-direct 2026-09-". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: advi-49f-securities-table. Every other token of the canonical form is byte-equal to the hand's.

### DYNAMODB_TABLE::user-permissions  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-user-permissions-table
- machine: OUT-OF-PATTERN portal-user-permissions-table  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (user-permissions, DYNAMODB_TABLE) (91 rows there). At HEAD (464 rows) the row (user-permissions, DYNAMODB_TABLE) -> portal is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). The row was later RE-POINTED to this system at 6c07797a9c (2026-09-21, 4.0.0_SA_CRO). Its evidence: "RE-POINTED gateway -> portal (Andrew-direct 2026-09-21 ~19:0xZ 'yes agreed on both'; 'gateway' is the Opal Gateway, NFRA_OPLGTW, which 4.0.0_SA_CRO ha". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: portal-user-permissions-table. Every other token of the canonical form is byte-equal to the hand's.

### IAM_POLICY::invoke-trending-publisher  [FOURTH_VERDICT]

- hand: OUT-OF-PATTERN {system}-invoke-trending-publisher-policy
- machine: NO-SYSTEM-ASKED invoke-trending-publisher-policy  (r20 report row (live+repo plane, 2 row(s)); differs in verdict)
- explanation: THE GRADING RULE MOVED between the two readings; neither side is wrong. The hand verdict is the hand rule's own (three verdicts: lib/opal_naming.py at the census commit 54659987c0 has no NO-SYSTEM-ASKED and NAMING_SCHEMA.json grade.verdicts there lists 3). At HEAD grade.verdicts lists 4 and lib/opal_naming.py carries _NO_SYSTEM_ASKED (landed at 19b61836e4 (2026-10-07, 0.9.0_WK_LGIC_BLANKFIX~2)): a library layer / purpose-word-led policy name with no resolved system takes the fourth verdict and a canonical form with no system slot. For (invoke-trending-publisher, IAM_POLICY) the r20 run reads NO-SYSTEM-ASKED with canonical invoke-trending-publisher-policy; the hand form differs only in the '{system}-' blank the rule no longer owes.

### IAM_POLICY::yield-curve-artifact-write  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-yield-curve-artifact-write-policy
- machine: OUT-OF-PATTERN marketdata-yield-curve-artifact-write-policy  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (yield-curve-artifact-write, IAM_POLICY) (91 rows there). At HEAD (464 rows) the row (yield-curve-artifact-write, IAM_POLICY) -> marketdata is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F04 -- a5 family F04, leading token 'yield' (census row 'yield-curve-artifact-write', LGIC placeholder recount @0f1caafb1d; Andrew-direct 2026-0". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: marketdata-yield-curve-artifact-write-policy. Every other token of the canonical form is byte-equal to the hand's.

### INSTANCE_PROFILE::inf-exporter-profile  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-inf-exporter-profile
- machine: OUT-OF-PATTERN advi-inf-exporter-profile  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (inf-exporter-profile, INSTANCE_PROFILE) (91 rows there). At HEAD (464 rows) the row (inf-exporter-profile, INSTANCE_PROFILE) -> advi is present, first added at b282500581 (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL1 SY1 -- PRODUCT (SIBLING): registered sibling(s) 'inf-exporter*' -> advi (resources.json, inf-pipeline root); Andrew-direct 2026-09-21 ~18:0xZ (S". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: advi-inf-exporter-profile. Every other token of the canonical form is byte-equal to the hand's.

### LAMBDA::access-anomaly-scanner  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-access-anomaly-scanner-lambda
- machine: OUT-OF-PATTERN secops-access-anomaly-scanner-lambda  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (access-anomaly-scanner, LAMBDA) (91 rows there). At HEAD (464 rows) the row (access-anomaly-scanner, LAMBDA) -> secops is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F06 -- a5 family F06, leading token 'access' (census row '/aws/lambda/access-anomaly-scanner', LGIC placeholder recount @0f1caafb1d; Andrew-dire". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: secops-access-anomaly-scanner-lambda. Every other token of the canonical form is byte-equal to the hand's.

### LAMBDA_LAYER::anthropic-sdk-deps  [SYSTEM_KEY_ADDED]

- hand: OUT-OF-PATTERN {system}-anthropic-sdk-deps-layer
- machine: OUT-OF-PATTERN anthropic-sdk-deps-layer  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. At the census commit 54659987c0 'anthropic' is not a systems.json key, so the hand (R1.d) leaves the blank: '{system}-anthropic-sdk-deps-layer'. At HEAD systems.json carries the row {key: anthropic, class: VENDOR}, first added at b282500581 (2026-09-21, 4.0.0_SA_CRO); the name's first token is now itself the system, so no blank is owed and the canonical form is anthropic-sdk-deps-layer (the name plus the layer kind suffix). The r20 run reads the HEAD registry (f936f6350cc5c404).

### LAMBDA_LAYER::yfinance-dependencies  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-yfinance-dependencies-layer
- machine: OUT-OF-PATTERN marketdata-yfinance-dependencies-layer  (r20 report row (live plane, 1 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (yfinance-dependencies, LAMBDA_LAYER) (91 rows there). At HEAD (464 rows) the row (yfinance-dependencies, LAMBDA_LAYER) -> marketdata is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F04 -- a5 family F04, leading token 'yfinance' (census row 'yfinance-dependencies', LGIC placeholder recount @0f1caafb1d; Andrew-direct 2026-09-". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: marketdata-yfinance-dependencies-layer. Every other token of the canonical form is byte-equal to the hand's.

### S3_BUCKET::opal-data-news-av  [TOKEN_RESOLVED]

- hand: RAISE None
- machine: OUT-OF-PATTERN opal-data-news  (no r20 row: carded NOT-JUDGED (R-29) in the r20 run; grade() at HEAD; differs in verdict)
- explanation: THE ESTATE MOVED between the two readings; the hand is not wrong at its vintage. At the census commit 54659987c0 'news' sits in systems.json 'unresolved' (V2), so B2 raises on 'opal-data-news-av' and the hand RAISE is right. At HEAD 'news' is a PRODUCT key (long news-intelligence), first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO), and grade() at HEAD returns OUT-OF-PATTERN opal-data-news. NOTE: the r20 run holds NO verdict row for this name: it is CARDED NOT-JUDGED (R-29) with a card that still reads B2 / V2, so the machine verdict recorded here is grade() at HEAD, not a r20 row; see this order's surprise row on the stale cards.

### SCHEDULE::wsd-49f-partner-held-etf-pull-daily  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-49f-wsd-partner-held-etf-pull-daily
- machine: OUT-OF-PATTERN mdpf-49f-wsd-partner-held-etf-pull-daily  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (wsd-49f-partner-held-etf-pull-daily, SCHEDULE) (91 rows there). At HEAD (464 rows) the row (wsd-49f-partner-held-etf-pull-daily, SCHEDULE) -> mdpf is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F14 -- a5 family F14, leading token 'wsd' (census row 'wsd-49f-partner-held-etf-pull-daily', LGIC placeholder recount @0f1caafb1d; Andrew-direct". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: mdpf-49f-wsd-partner-held-etf-pull-daily. Every other token of the canonical form is byte-equal to the hand's.

### SNS_TOPIC::inf-otp-alert  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-inf-otp-alert-topic
- machine: OUT-OF-PATTERN portal-inf-otp-alert-topic  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (inf-otp-alert, SNS_TOPIC) (91 rows there). At HEAD (464 rows) the row (inf-otp-alert, SNS_TOPIC) -> portal is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). The row was later RE-POINTED to this system at 6c07797a9c (2026-09-21, 4.0.0_SA_CRO). Its evidence: "RE-POINTED gateway -> portal (Andrew-direct 2026-09-21 ~19:0xZ 'yes agreed on both'; 'gateway' is the Opal Gateway, NFRA_OPLGTW, which 4.0.0_SA_CRO ha". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: portal-inf-otp-alert-topic. Every other token of the canonical form is byte-equal to the hand's.

### SQS_QUEUE::partner-etl-ops-queue  [RESOURCE_ROW_ADDED]

- hand: OUT-OF-PATTERN {system}-partner-etl-ops-queue
- machine: OUT-OF-PATTERN advi-partner-etl-ops-queue  (r20 report row (live+repo plane, 2 row(s)); differs in canonical form)
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit 54659987c0 holds no row for (partner-etl-ops-queue, SQS_QUEUE) (91 rows there). At HEAD (464 rows) the row (partner-etl-ops-queue, SQS_QUEUE) -> advi is present, first added at 93790c036e (2026-09-21, 4.0.0_SA_CRO). Its evidence: "CALL2 F15 -- a5 family F15, leading token 'partner' (census row 'partner-etl-ops-queue', LGIC placeholder recount @0f1caafb1d; Andrew-direct 2026-09-2". The r20 run (registry f936f6350cc5c404) reads that row and fills the blank: advi-partner-etl-ops-queue. Every other token of the canonical form is byte-equal to the hand's.

## tension_ranking_surfaces -- 10 compared, 6 agree, 4 disagree

### rank-1  [ESTATE_MOVED]

- hand: WITHIN-TOLERANCE; machine: OUTSIDE-TOLERANCE (1 of 10 figures)
  - 49f anywhere (hand's grain undeclared; census s.2 per-type sums are any-position): hand 68, r8 68, r20 92, tolerance 10.2
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure '49f anywhere' is round 19's re-quote of the r8 census (2026-09-18 12:17:28 UTC), 68; the same instrument (compare_hand_r9.iv7: live judged + carded names, tokens split on - / _ . # : and camel humps, a LOG_GROUP tokenised on its resource part) over the r20 census (2026-10-09 12:52:02 UTC) reads 92, outside the declared tolerance 10.2. Measured on the two reports' live rows: 24 (name, type) pairs carrying the token 49f are in r20 and not in r8 (e.g. LOG_GROUP:/aws/lambda/irpt-49f-reporting-gold-lambda, LOG_GROUP:/aws/lambda/irpt-49f-reporting-publish-lambda, LOG_GROUP:/aws/lambda/irpt-49f-reporting-read-lambda, IAM_POLICY:irpt-49f-directory-read-policy, IAM_ROLE:irpt-49f-directory-read-role, IAM_POLICY:irpt-49f-holdings-performance-policy ...), and none is in r8 and not in r20. The other 9 of 10 figures of this surface stay within tolerance.

### rank-4  [ESTATE_MOVED]

- hand: WITHIN-TOLERANCE; machine: OUTSIDE-TOLERANCE (1 of 5 figures)
  - customer-managed IAM policies: hand 515, r8 515, r20 598, tolerance 51.5
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure 'customer-managed IAM policies' is round 19's re-quote of the r8 census (2026-09-18 12:17:28 UTC), 515; the same instrument over the r20 census (2026-10-09 12:52:02 UTC) reads 598, outside the declared tolerance 51.5. Measured on the two reports' live rows: 83 IAM_POLICY (name, type) entries are in r20 and not in r8 (e.g. IAM_POLICY:amgt-global-freshness-snapshot-scheduler-policy, IAM_POLICY:cottonwood-recovery-policy, IAM_POLICY:etfs-rivalfunds-daily-policy, IAM_POLICY:etfs-rivalfunds-fetch-holdings-policy, IAM_POLICY:etfs-rivalfunds-scheduler-policy, IAM_POLICY:gateway-assume-blackdiamond-reader-policy ...), and none is in r8 and not in r20. The other 4 of 5 figures of this surface stay within tolerance.

### rank-5  [INSTRUMENT_GAP]

- hand: OUTSIDE-TOLERANCE (r19, unrevised); machine: OUTSIDE-TOLERANCE (6 of 6 figures)
  - live names with no same (name,type) on the census repo plane: hand 339, r8 669, r20 793, tolerance 33.9
  - LAMBDA: hand 15, r8 158, r20 144, tolerance 2.0
  - IAM_ROLE: hand 16, r8 56, r20 90, tolerance 2.0
  - EVENT_RULE: hand 10, r8 26, r20 35, tolerance 2.0
  - LOG_GROUP: hand 68, r8 199, r20 215, tolerance 6.8
  - IAM_POLICY: hand 36, r8 93, r20 138, tolerance 3.6
- explanation: NEITHER SIDE IS SHOWN WRONG; THE TWO SIDES COME FROM DIFFERENT INSTRUMENTS, and the gap is the one round 9 recorded and round 19 left unrevised. The hand figures (339 in all; LAMBDA 15, IAM_ROLE 16, EVENT_RULE 10, LOG_GROUP 68, IAM_POLICY 36) are comp-estate's drift_class LIVE-no-DECLARED; the census has no drift class, and the figure it can produce is live (name, type) minus repo (name, type), where the repo plane reads only literal Terraform name attributes and source literals. All 6 figures are outside tolerance at r8 (2026-09-18 12:17:28 UTC) and at r20 (2026-10-09 12:52:02 UTC): live names with no same (name,type r8 669 -> r20 793 (hand 339, tolerance 33.9); LAMBDA r8 158 -> r20 144 (hand 15, tolerance 2.0); IAM_ROLE r8 56 -> r20 90 (hand 16, tolerance 2.0); EVENT_RULE r8 26 -> r20 35 (hand 10, tolerance 2.0); LOG_GROUP r8 199 -> r20 215 (hand 68, tolerance 6.8); IAM_POLICY r8 93 -> r20 138 (hand 36, tolerance 3.6). Re-reading the census at a newer vintage cannot close an instrument gap.

### rank-9  [ESTATE_MOVED]

- hand: WITHIN-TOLERANCE; machine: OUTSIDE-TOLERANCE (1 of 2 figures)
  - secrets: hand 99, r8 99, r20 115, tolerance 9.9
- explanation: THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure 'secrets' is round 19's re-quote of the r8 census (2026-09-18 12:17:28 UTC), 99; the same instrument over the r20 census (2026-10-09 12:52:02 UTC) reads 115, outside the declared tolerance 9.9. Measured on the two reports' live rows: 16 SECRET names are in r20 and not in r8 (e.g. SECRET:dowjones/barrons/session, SECRET:dowjones/wsj/session, SECRET:gateway/global/taxsma-workbook-token, SECRET:gateway/mail/bearer, SECRET:gateway/principals/rosters, SECRET:gateway/teams/bearer ...), and none is in r8 and not in r20. The other 1 of 2 figures of this surface stay within tolerance.

