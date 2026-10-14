# NFRA_CTLPLN -- ARMED rows owned by 2.0.0_SA_COO~C, pass 2 of 2: the 23 not touched this session (issuer, 2026-10-14 ~03:2xZ)

For `3.0.0_SA_CVO~L` (REMEDIATION rows stay the CVO's). Pass 1 is `ARMED_ROWS_REMEDY_LANDED_20261014.md`. This pass was read by a read-only analyst subagent over the repository at HEAD (no test was run by it); the issuer re-read two findings (W73-S2: `.tools/thread-trace.py` `find_orders` reads `git ls-tree` on HEAD and origin/CLOUD with no glob; Z-S3: `lib/trading_calendar.py` fallback still covers 2010-2027 and its own text says regenerate before 2028). The 15 DISPOSED rows rest on the CVO's own adjudications and were not re-read.

Counts: LANDED 3, OPEN 5, DISPOSED 15, CANNOT-DETERMINE 0.

## Issuer's note on the two that matter most

- `W14-S2` (a Dell can rewrite a command document and the objects it runs): OPEN in the channel, but its premise is overtaken. By Andrew's rec (b) the Dell users are in the admin group (applied under pair 6, `CT-ab-2`), so the fence this row asked for was removed on his word; `dell_create_policy.json:26` still allows ssm Create/UpdateDocument, and the admin group allows it anyway. I recommend the CVO record it as overtaken by that ruling, not remediated.
- `W73-S2` (thread-trace globs the working tree) and `W6-S17`: the fix is landed; their remediation rows still read OPEN with no close row.

## The table (analyst's, unedited)

```
NFRA_CTLPLN-S1 | LANDED | Live read on this laptop 2026-10-13: the three enabled Remote Desktop inbound Allow rules (User Mode TCP-In, UDP-In, Shadow TCP-In) each read RemoteAddress 100.64.0.0/255.192.0.0; ADJUDICATION_v1.md C-S1 GRADUATED it and REMEDIATION_v1.md line 437 reads REMEDIATED/DISARMED (laptop only; site Z, dell1, dell2 not read).
NFRA_CTLPLN-W1-S1 | DISPOSED | NFRA_CTLPLN-C-S7 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: dell_iam_roles_policy.json AllowPassAnyRole allows iam:PassRole, a ruling overtook the row).
NFRA_CTLPLN-W3-S2 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: .tools/agentbus-consumer.py:73-82 checks the sender per the CVO's read).
NFRA_CTLPLN-W3-S3 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: refused mail is recorded and deleted, commit 221ee5b0b6).
NFRA_CTLPLN-W5-S1 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: gate no longer derives fabric from the Z- infix; PRD_HEADER.schema.json carries four fabrics).
NFRA_CTLPLN-W12-S1 | OPEN | Graduated by C-S8 (ADJUDICATION_v3.md) with REMEDIATION_v1.md row W12-S1 still OPEN (owner 2.0.0_SA_COO~C); at HEAD cmp shows all three infra/aws/lambda/{inf-pipeline/inf-etf-ownership-daily,bd-pipeline/bd-served-vintage-alarm,opal-assets-absence-check}/trading_calendar.py still differ from lib/trading_calendar.py (163 lines vs 304), and no later commit touched them.
NFRA_CTLPLN-W9-S1 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: both row schemas carry the four-fabric enum and the D1-/D2- id pattern).
NFRA_CTLPLN-W9-S2 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: adjudicates and disarms patterns admit the Dell infix).
NFRA_CTLPLN-W9-S3 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: proof-of-spec-check.py:1206 and surprise-watch.sh:85 admit the Dell infix).
NFRA_CTLPLN-W9-S4 | DISPOSED | NFRA_CTLPLN-C-S5 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: file_stop_row.py:13 carries the schema grammar).
NFRA_CTLPLN-W14-S2 | OPEN | Graduated by C-S8 with REMEDIATION_v1.md row W14-S2 still OPEN (owner 1.0.0_SA_CTO, no ruling row); infra/aws/terraform/nfra-ctlpln-identity/dell_create_policy.json:26 still allows ssm:CreateDocument/UpdateDocument/UpdateDocumentDefaultVersion, and commit 8ef2c65918 (TO-CT-ab-2) destroyed the routes Deny resource and put the Dells in an AdministratorAccess group, so the row's Deny remedy was not landed and the hazard is changed rather than closed.
NFRA_CTLPLN-W14-S3 | DISPOSED | NFRA_CTLPLN-C-S6 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: routes Deny rendered through modules/routes_policy, TO-CT-a-1 complete; module at infra/aws/terraform/nfra-ctlpln-identity/modules/routes_policy/main.tf).
NFRA_CTLPLN-S13 | DISPOSED | NFRA_CTLPLN-C-S6 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: TO-CT-k-2 AMENDMENT 5 measured the bun egress disarm, order complete).
NFRA_CTLPLN-W8-S7 | OPEN | Graduated by C-S8 with REMEDIATION_v1.md row W8-S7 still OPEN; infra/aws/terraform/shared-infra/tests/dell_fence_census.py:33 and :730 still default --out to tests/dell_fence_census.json, the file check_dell_fence_join.py:62 and check_fence_scoped_rows.py:753 read; last commit to the census is 248277c024, not separating the paths (not run).
NFRA_CTLPLN-W6-S17 | LANDED | org/devices/intake/intake_check.py:508-566 now tracks py_extra (wheel module absent from the installed RECORD) separately from py_missing (commit 5a8cfa0fb3, AMENDMENT 4) and org/devices/intake/test_intake_check.py:790-797 asserts such a wheel FAILS check 6 (REMEDIATION_v1.md row W6-S17 still reads OPEN; no close row filed; code read, tests not run).
NFRA_CTLPLN-S25 | DISPOSED | NFRA_CTLPLN-C-S6 (ADJUDICATION_v3.md, DISMISSED_WITH_REASON: the resource-policy ALLOW was later signed and applied as TO-APPLY-13, complete).
NFRA_CTLPLN-Z-S3 | OPEN | Graduated by C-S8 with REMEDIATION_v1.md row Z-S3 still OPEN (dated, before 2027-12-01); lib/trading_calendar.py:14,34,48 still reads the fallback as 2010-2027 with no "2028-" entries (grep count 0).
NFRA_CTLPLN-S9103 | OPEN | Graduated by C-S9 (ADJUDICATION_v3.md) with REMEDIATION_v1.md row S9103 still OPEN (owner 2.0.0_SA_COO~C); org/devices/kit_terraform_providers.py (no commit to it since 2026-10-09) shows no replace-not-merge step for the Dell mirror and no dell2 readback of it.
NFRA_CTLPLN-W56-S1 | DISPOSED | NFRA_CTLPLN-C-S13 (ADJUDICATION_v7.md, DISMISSED_WITH_REASON: CT-i-14 amendment 52713e9dbb wrapped the fake replies, agent suite ok=True).
NFRA_CTLPLN-W62-S1 | DISPOSED | NFRA_CTLPLN-C-S19 (ADJUDICATION_v8.md, DISMISSED_WITH_REASON: CTO ruling and PRD v0.25 FWD-28 keep the partner reads open and bind CT-u-7 to no-regression).
NFRA_CTLPLN-W61-S8 | DISPOSED | NFRA_CTLPLN-C-S18 (ADJUDICATION_v8.md, DISMISSED_WITH_REASON: .tools/ssh-tailnet-verify.py now reads the advertised methods).
NFRA_CTLPLN-W65-S4 | DISPOSED | NFRA_CTLPLN-C-S33 (ADJUDICATION_v10.md, DISMISSED_WITH_REASON: deploy.sh retired, commit 82ce6d8103).
NFRA_CTLPLN-W73-S2 | LANDED | .tools/thread-trace.py:239-259 find_orders now reads the order set by git ls-tree on HEAD and origin/CLOUD (no glob.glob remains in the file; docstring line 23), although C-S36 graduated it and REMEDIATION_v4.md row W73-S2 still reads OPEN with no close row (code read, planted-order test not run).
```
