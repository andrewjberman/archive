# FWD-7 project-path overlaps (NFRA_CTLPLN.TO-CT-ay-1, cell CT-ay-1)

Project-path overlaps: 9 PROJECT-SAME-FILE line(s) name a shared file; they are listed per file below, and no fix is proposed (the CTO decides which become a cell).

Denominator: 62 OVERLAP line(s) read from `python .tools/placement-check.py` (rc=0; live projects 30; unplaced/unreadable 0). The read's own FINDINGS line counts 62 cross-box write overlap(s) (agrees).

Classes: CARRIER 40 | NOT-SAME-FILE 13 | PROJECT-SAME-FILE 9 | UNCLASSIFIED 0 | sum 62 | ok=True.

## PROJECT-SAME-FILE (9)

| # | project A (box) | project B (box) | path A | path B | shared file |
|---|---|---|---|---|---|
| 1 | AMGT_RESAPP (dell1) | NFRA_MCPORTAL (sitez) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 2 | AMGT_RESAPP (dell1) | IRPT_ANLREQ (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 3 | AMGT_RESAPP (dell1) | IRPT_DASHBD (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 4 | AMGT_RESAPP (dell1) | NFRA_MCPINDEX (sitez) | `infra/aws/lambda/ci/record-terraform-deploy.sh` | `infra/aws/lambda/ci/record-terraform-deploy.sh` | `infra/aws/lambda/ci/record-terraform-deploy.sh` |
| 5 | AMGT_RESAPP (dell1) | NFRA_OPLGTW (sitez) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 6 | NFRA_MCPORTAL (sitez) | IRPT_ANLREQ (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 7 | NFRA_MCPORTAL (sitez) | IRPT_DASHBD (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 8 | IRPT_ANLREQ (dell2) | NFRA_OPLGTW (sitez) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |
| 9 | IRPT_DASHBD (dell2) | NFRA_OPLGTW (sitez) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci/lambda-source-map.json` |

### Per shared file (which projects touch it; no fix proposed)

- `infra/aws/lambda/ci/lambda-source-map.json`: AMGT_RESAPP (dell1), IRPT_ANLREQ (dell2), IRPT_DASHBD (dell2), NFRA_MCPORTAL (sitez), NFRA_OPLGTW (sitez)
- `infra/aws/lambda/ci/record-terraform-deploy.sh`: AMGT_RESAPP (dell1), NFRA_MCPINDEX (sitez)

## NOT-SAME-FILE (13)

| # | project A (box) | project B (box) | path A | path B | relation |
|---|---|---|---|---|---|
| 1 | NFRA_CTLPLN (laptop) | IRPT_BCKEND (dell2) | `.tools/tests/test_crossbox_call.py` | `.tools/tests` | directory-prefix: .tools/tests is a directory claim over .tools/tests/test_crossbox_call.py |
| 2 | AMGT_RESAPP (dell1) | IRPT_BCKEND (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci` | directory-prefix: infra/aws/lambda/ci is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 3 | NFRA_MCPMSP (sitez) | ADVI_FIRMBKTS (dell1) | `infra/aws/lambda/layers/mcportal-grant-writer-deps/.build/mcportal-grant-writer-deps.zip` | `infra/aws/lambda` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/layers/mcportal-grant-writer-deps/.build/mcportal-grant-writer-deps.zip |
| 4 | NFRA_MCPORTAL (sitez) | ADVI_FIRMBKTS (dell1) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 5 | NFRA_MCPORTAL (sitez) | IRPT_BCKEND (dell2) | `infra/aws/lambda/ci/lambda-source-map.json` | `infra/aws/lambda/ci` | directory-prefix: infra/aws/lambda/ci is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 6 | ADVI_FIRMBKTS (dell1) | IRPT_ANLREQ (dell2) | `infra/aws/lambda` | `infra/aws/lambda/ci/lambda-source-map.json` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 7 | ADVI_FIRMBKTS (dell1) | IRPT_BCKEND (dell2) | `infra/aws/lambda` | `infra/aws/lambda/ci` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/ci |
| 8 | ADVI_FIRMBKTS (dell1) | IRPT_DASHBD (dell2) | `infra/aws/lambda` | `infra/aws/lambda/ci/lambda-source-map.json` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 9 | ADVI_FIRMBKTS (dell1) | NFRA_MCPINDEX (sitez) | `infra/aws/lambda` | `infra/aws/lambda/bd-pipeline/bd-asset-dim-trigger` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/bd-pipeline/bd-asset-dim-trigger |
| 10 | ADVI_FIRMBKTS (dell1) | NFRA_OPLGTW (sitez) | `infra/aws/lambda` | `infra/aws/lambda/ci/lambda-source-map.json` | directory-prefix: infra/aws/lambda is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |
| 11 | MDPF_SECCLASS (dell1) | IRPT_BCKEND (dell2) | `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | `data/assets/scripts/gold/investor_reporting` | directory-prefix: data/assets/scripts/gold/investor_reporting is a directory claim over data/assets/scripts/gold/investor_reporting/holdings_snapshot.py |
| 12 | IRPT_BCKEND (dell2) | NFRA_MCPINDEX (sitez) | `infra/aws/lambda/ci` | `infra/aws/lambda/ci/record-terraform-deploy.sh` | directory-prefix: infra/aws/lambda/ci is a directory claim over infra/aws/lambda/ci/record-terraform-deploy.sh |
| 13 | IRPT_BCKEND (dell2) | NFRA_OPLGTW (sitez) | `infra/aws/lambda/ci` | `infra/aws/lambda/ci/lambda-source-map.json` | directory-prefix: infra/aws/lambda/ci is a directory claim over infra/aws/lambda/ci/lambda-source-map.json |

Each NOT-SAME-FILE line is a directory claim over a path under it; it is classed here by the prefix rule the earlier table used (R5), which reads the two projects as changing different files. The relation column shows which path is the directory claim.

## CARRIER (40), counts by kind

- deploy-ledger-sentinel: 40
- audit-log: 0
- surprise-channel: 0
- open-calls: 0
- crossbox: 0
