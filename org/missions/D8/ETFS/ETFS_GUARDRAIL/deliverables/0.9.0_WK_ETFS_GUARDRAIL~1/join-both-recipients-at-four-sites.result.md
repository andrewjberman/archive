# EG-s-9 -- JOIN both recipients at four sites, plus the variable

**TO:** `ETFS_GUARDRAIL.TO-EG-s-9` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `df14ecd5f1` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** wire. **Last order of the round.**

## Code changes

`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`:
1. `EMAIL_RECIPIENTS = [a.strip() for a in EMAIL_RECIPIENT.split(",") if a.strip()]` derived once at module level. `EMAIL_RECIPIENT` itself stays the joined string from the environment (unchanged definition) -- both headers (`_build_report_email`, `_build_correction_email`) keep `msg["To"] = EMAIL_RECIPIENT` UNCHANGED, since it already renders correctly once the Terraform variable holds the joined value.
2. `_email_report` and `_send_correction_email`'s envelopes: `Destinations=[EMAIL_RECIPIENT]` -> `Destinations=EMAIL_RECIPIENTS`.
3. `EG-s-8`'s terminal path DECOUPLED: a new `TERMINAL_RECIPIENT = "andrew@opalinvest.com"` constant; `_build_terminal_email`'s header and `_send_terminal_unresolved`'s envelope both use it instead of the shared variable, so the JOIN never silently widens the urgent internal alert to AJ.
4. Module-level and send-path docstrings updated from "to Andrew" to "the recipients (Andrew AND AJ, JOINED)".
5. `email_qa`'s return now includes `"to": msg["To"]`, mirroring `terminal_qa`'s shape, so the rehearsal's To header is directly observable without a send (deliverable item 4's own requirement).

`infra/aws/terraform/etfs-reports/orchestrator.tf`: `EMAIL_RECIPIENT = "aj@opalinvest.com,andrew@opalinvest.com"` -- the one Terraform change besides the code hash.

## 1. S9-AC1 -- the five-arm battery

**Invocation:**
```
python -m pytest infra/aws/lambda/etfs-reports-orchestrator/test_recipients_join.py -q
```
**Output (rc=0):**
```
5 passed in 0.39s
```
Arms: (a) two-address join -> both headers contain both addresses, both envelopes are a 2-element list in order; (b) one address -> a 1-element list, header unchanged in meaning; (c) whitespace around commas tolerated; (d) the terminal send stays `["andrew@opalinvest.com"]` alone even with the joined env var; (e) `email_qa` stays send-free. The pre-existing `test_terminal_send.py` battery (5 arms) also re-run clean (10/10 total across both files).

## 2. S9-AC2 -- the four-site fix as a property of the bytes (AMENDED, PASS)

**Invocation:**
```
python -c "import re; s=open('infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py').read(); print('ENVELOPE_LIST_SITES=%d HEADER_SITES=%d SINGLE_ELEMENT_ENVELOPES=%d' % (len(re.findall(r'Destinations=EMAIL_RECIPIENTS', s)), len(re.findall(r'msg\[\"To\"\]\s*=', s)), len(re.findall(r'Destinations=\[EMAIL_RECIPIENT\]', s))))"
```
**Output (rc=0):**
```
ENVELOPE_LIST_SITES=2 HEADER_SITES=3 SINGLE_ELEMENT_ENVELOPES=0
```
**Row filed and dispositioned same-turn:** measured BEFORE any envelope edit that `HEADER_SITES` was already 3 (report, correction, AND `EG-s-8`'s terminal header), because the PRD's four-site table predates `EG-s-8`. Filed `ETFS_GUARDRAIL-W1-S9`; the issuer AMENDED the criterion's `expect` to `HEADER_SITES=3` (row disposition = the amendment itself). **S9-AC2 verdict: PASS** against the amended expect.

## 3. S9-AC3 -- SES delivery-capability, read BEFORE the deploy

**Invocation:**
```
.tools/aws sesv2 get-account --query ProductionAccessEnabled --output text
```
**Output (rc=0):**
```
True
```
Full account read: `SendingEnabled=true`, `EnforcementStatus=HEALTHY`, `ReviewDetails.Status=GRANTED` (case `178727932800843`). Out of the sandbox -- an unverified recipient (`aj@opalinvest.com`) does not fail silently at delivery.

## 4. S9-AC4 -- commit gate clean

**Invocation:**
```
bash .tools/commit-gate.sh infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py infra/aws/lambda/etfs-reports-orchestrator/test_recipients_join.py
```
**Output (rc=0):**
```
OK: pre-commit gate clean for 2 of 2 file(s)
```

## 5. S9-AC5 -- the TARGETED plan, apply, ledger

**Full (untargeted) plan, before the apply:**
```
  # aws_lambda_function.orchestrator will be updated in-place
      ~ source_code_hash = "stq9kk/+gatkLr7F/ldLzduW+i03aUCrx1ZG91wJWgY=" -> "AVvA9lPQAj3tns5JSJ7Awg+crucGgIAfr5dHtScATXw="
      ~ environment { variables = { ~ "EMAIL_RECIPIENT" = "andrew@opalinvest.com" -> "aj@opalinvest.com,andrew@opalinvest.com" } }

Plan: 0 to add, 1 to change, 0 to destroy.
```
`aws_instance.reporter` shows NO change (row `ETFS_GUARDRAIL-S2`'s LF-normalization fix holds).

**Invocation (TARGETED):**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_lambda_function.orchestrator
```
**Output (rc=0):** `Plan: 0 to add, 1 to change, 0 to destroy.` **S9-AC5 verdict: PASS.**

**Ledger + apply:** opened `etfs-guardrail-eg-s-9-orchestrator-join-recipients` (commit `1d7c53e6eb`, before the apply) -> `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/etfs-reports apply -input=false -auto-approve -target=aws_lambda_function.orchestrator` -> `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` -> targeted 0-diff `-detailed-exitcode` rc=0 -> `record-terraform-deploy.sh` (commit `19b11f082b`) -> ledger closed.

**Supplementary apply (deliverable item 4's own requirement surfaced a gap -- see row `ETFS_GUARDRAIL-W1-S10`):** `email_qa` did not return a `"to"` field at all, so the live rehearsal could not show the To header as this deliverable requires. Added `"to": msg["To"]` to its return (mirrors `terminal_qa`); re-ran both test batteries (10/10 green) and the commit gate (clean); re-ran the targeted plan (`1 to change`) and applied again (`1 changed`); confirmed a second targeted 0-diff and `record-terraform-deploy.sh` (commit `c6ddc5d6c4`). **This second apply ran WITHOUT a ledger entry open at the time** (the first ledger was already closed) -- filed `ETFS_GUARDRAIL-W1-S10` and remediated same-turn by opening and closing a supplementary ledger entry (`etfs-guardrail-eg-s-9-orchestrator-emailqa-to`) with proof from the post-fix measurements below.

**Final full (untargeted) plan, after both applies:** `No changes. Your infrastructure matches the configuration.` -- zero drift anywhere in the directory.

## 6. S9-AC6 -- the applied variable

**Invocation:**
```
.tools/aws lambda get-function-configuration --function-name etfs-reports-orchestrator --query Environment.Variables.EMAIL_RECIPIENT --output text
```
**Output (rc=0, re-read after the final apply):**
```
aj@opalinvest.com,andrew@opalinvest.com
```

## 7. S9-AC7 -- served vs built

**Invocation:**
```
python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/orchestrator_served_vs_built.py
```
**Output (rc=0, final, post both applies):**
```
SERVED_CODE_SHA256: CvFmg9ZmBrSMZSSlplJGd7BWp99FXn5+ODaRbKTe/QI=
BUILT_ZIP_SHA256_B64: CvFmg9ZmBrSMZSSlplJGd7BWp99FXn5+ODaRbKTe/QI=
VERDICT: MATCH
```

## 8. S9-AC8 -- THE ANSWER (judgment; recorded, no verdict)

**Live `email_qa` rehearsal, 2026-08 (send-free), showing the To header:**
```
.tools/aws lambda invoke --function-name etfs-reports-orchestrator --payload "{\"mode\":\"email_qa\",\"month\":\"2026-08\"}" .scratch/email_qa_invoke_out2.json
-> StatusCode 200
{"mode": "email_qa", "month": "2026-08", "to": "aj@opalinvest.com,andrew@opalinvest.com", "attachments": ["opal_etf_ownership_2026-08.pdf", "opaletfs_49financial_202608.csv", "opaletfs_cottonwood_202608.csv", "opaletfs_inflection_202608.csv"], "ok": true}
```
**Live `terminal_qa` rehearsal, same month, confirming the terminal path is unaffected:**
```
{"mode": "terminal_qa", "month": "2026-08", "subject": "URGENT: ETF month-end 2026-08 -- 0 date(s) unresolved after remediation", "to": "andrew@opalinvest.com", "body_head": "...", "ok": true}
```

- **JOIN not replace, at all four sites:** the report/correction headers now render `"aj@opalinvest.com,andrew@opalinvest.com"` (measured live above), and their envelopes pass both as a 2-element list (test arm (a)); Andrew is never dropped in either shape.
- **The variable is the carrier for a future recipient:** `EMAIL_RECIPIENTS` is derived once from `EMAIL_RECIPIENT`; adding a third address is a Terraform variable edit, not a code change (test arms (b)/(c) already exercise 1-address and whitespace-tolerant parsing).
- **FWD-5's EXERCISED grade ("both people have actually received one") is NOT claimed here.** This order does not send a report to AJ ahead of the scheduled fire (`etfs-reports-monthly-run`, `cron(0 10 1 * ? *)` America/New_York) -- an outward-facing send on a report the alignment has only just landed would be exactly the kind of ad-hoc, unauthorized act this project's carve-outs forbid elsewhere. The next scheduled fire is the first opportunity for FWD-5 to become EXERCISED, read as delivery at both inboxes.
- **No live send of any kind occurred in this order:** every measurement above is either a live READ (`get-function-configuration`, `sesv2 get-account`, `terraform plan`) or a live INVOKE of a send-free rehearsal mode (`email_qa`, `terminal_qa`); `run` and `send_correction` were never invoked.

## 9. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
-> cb82020ab1337cdfbebbfeb1371534a80f6b5cb5
```
