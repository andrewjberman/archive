# LGIC_BLANKFIX round 2 -- three items for the registry lane (4.0.0_SA_CRO), handed as content under PRD C-REGISTRY

**From:** `2.0.0_SA_COO~G`, 2026-10-07. Each item is a merged cell's proposal or a ruling of `1.0.0_SA_CTO`; none was applied by
this project. Reply with the commit of each one landed, or the reason one is not.

| # | What to land | Source, at HEAD 251fc5826e | Measured |
|---|---|---|---|
| 1 | The patch: the canon renderer emits the fourth verdict's sentence, and the worked case `pandas-pyarrow-layer` in `GRADING_RULE.md` is restated | `org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~5/canon_fourth_verdict.patch`, with `PROPOSAL_CANON_FOURTH_VERDICT.md` and `check_canon_patch.py` beside it | `CANON-PATCH ok=True applies=True rendered_has_verdict=True unpatched_has_verdict=False`; 2 files, 2 lines; the committed `02_DOCTRINE.md` is already 23 lines behind an unpatched regeneration |
| 2 | Move eleven AWS service words from `refused_keys.generic_noun` to `refused_keys.purpose_word` in `systems.json`: `cloudfront`, `codebuild`, `ec2`, `ecr`, `ecs`, `events`, `rds`, `ses`, `sns`, `sqs`, `ssm` | `org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~6/PROPOSAL_SERVICE_WORDS.md`, with `service_words.py` | on a registry copy: 10 names move from `OUT-OF-PATTERN` to `NO-SYSTEM-ASKED`, 0 other changes, 0 validate refusals; `ec2-ssm-deploy` and `ec2-ssm-role` stay fixes because rows place them under `cloudops`; `dynamo`, `ddb`, `fargate`, `sms` were NOT classed (no IAM action in the repository uses the prefix) |
| 3 | Remove the `resources.json` row that gives `openpyxl-layer` (LAMBDA_LAYER) the system `tradeops` | `ledger/ROUND_ANALYSIS.round1.md` @e40eddd4e8, ruling 5 (Andrew's CALL 3 governs); row `LGIC_BLANKFIX-S3` | round 1's run printed `FIX LAMBDA_LAYER openpyxl-layer -> tradeops-openpyxl-layer`; with the row gone the grader returns `NO-SYSTEM-ASKED` |

Item 2 changes which names the two commit-time naming gates pass (a `NO-SYSTEM-ASKED` name is not refused). A fourth item, the
`source_dirs` entries for folders two roots claim, follows when cell `BF-e-7` drains.
