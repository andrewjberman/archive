# EG-s-8 -- the ONE terminal SES send

**TO:** `ETFS_GUARDRAIL.TO-EG-s-8` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `c50c72f92a` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** wire.

**HEADLINE (final): the deploy landed.** `S8-AC4`'s FIRST reading was a FALSE drift: a CRLF-vs-LF checkout artifact on this `core.autocrlf=true` worktree (no `*.tf` eol rule in `.gitattributes`), not a real config change on `aws_instance.reporter`. The issuer normalized the `.tf` tree to LF (row `ETFS_GUARDRAIL-S2`) and ADDED one line to this order's own deliverable -- `_render_command` now passes `--gate` to the renderer, the seam between this Lambda and `EG-s-6`'s pre-publish coverage gate (row `ETFS_GUARDRAIL-S3`, minted `S8-AC9`). After both, the targeted plan read exactly one resource, the apply landed, and the live rehearsal ran safely. Filed `ETFS_GUARDRAIL-W1-S8` (BLOCKING/INERT, dispositioned by rows S2/S3) for the first, false-drift reading and the correctly-declined live invoke against the pre-deploy function.

## Code changes

`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`:
1. `_read_coverage_artifacts(month) -> dict` -- best-effort read of `coverage_verdict.json`/`coverage_unresolved.json`/`coverage_egress_ask.json`, absence normal.
2. `_build_terminal_email(month, unresolved, ask)` -- shared build, never sends.
3. `_send_terminal_unresolved(month, unresolved, ask)` -- the third and only new send call site.
4. `_run`'s existing `if status != "Success":` branch enriched: folds the coverage artifacts into the existing `_alert`, and calls `_send_terminal_unresolved` exactly once when `coverage_unresolved.json` names at least one unresolved day.
5. Mode `terminal_qa` -- send-free rehearsal, mirrors `email_qa`.
6. (ADDED BY THE ISSUER, row `ETFS_GUARDRAIL-S3`) `_render_command` now passes `--gate`: `python3 render_month_end.py --month {month} --pdf --gate --s3-out {out}` -- the seam that runs `EG-s-6`'s pre-publish gate on the scheduled fire.

Reuses the existing SES grant (`ses:SendRawEmail` from `*@opalinvest.dev`, already applied) and the existing `platinum/reports/*` read grant -- no new IAM.

## 1. S8-AC1 -- the five-arm battery

**Invocation:**
```
python -m pytest infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py -q
```
**Output (rc=0, re-run after the `--gate` edit, unaffected):**
```
5 passed in 0.32s
```
Arms: (a) unresolved present -> exactly one `send_raw_email`, `Destinations == ["andrew@opalinvest.com"]`, body names every date/partner/provider; (b) unresolved absent -> zero sends, the ordinary render-failure alert text unchanged; (c) `terminal_qa` makes no SES call; (d) `absence_check` makes no SES call; (e) the only real-sending mode besides the terminal path is `send_correction`.

## 2. S8-AC2 -- exactly three send call sites, no new topic

**Invocation:**
```
python -c "import re; s=open('infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py').read(); print('SEND_CALL_SITES=%d NEW_TOPICS=%d' % (len(re.findall(r'send_raw_email\(', s)), len(re.findall(r'create_topic\(', s))))"
```
**Output (rc=0):**
```
SEND_CALL_SITES=3 NEW_TOPICS=0
```

## 3. S8-AC3 -- commit gate clean

**Invocation:**
```
bash .tools/commit-gate.sh infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py
```
**Output (rc=0, re-run after the `--gate` edit):**
```
OK: pre-commit gate clean for 2 of 2 file(s)
```

## 4. S8-AC4 -- the TARGETED plan (PASS, after the false-drift correction)

**The false drift (row `ETFS_GUARDRAIL-S2`), confirmed:** `file infra/aws/terraform/etfs-reports/instance.tf` -> `ASCII text` (no CRLF, after the issuer's normalization); `git diff --ignore-cr-at-eol infra/aws/terraform/etfs-reports/instance.tf` -> 0 lines (an eol-only change, no content difference). The live reporter instance's `user_data` (sha1 `e47b615c`) was always byte-identical to the LF rendering of the heredoc; the earlier "new" hash `434774b5` was the CRLF rendering Terraform hashed from this worktree's (pre-normalization) checkout.

**Full (untargeted) plan, post-normalization:**
```
terraform -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false

  # aws_lambda_function.orchestrator will be updated in-place
      ~ source_code_hash = "7CIW8veDKFnk/rNKhXdInVVpp60dhXiZf5Lye9a0w3Q=" -> "stq9kk/+gatkLr7F/ldLzduW+i03aUCrx1ZG91wJWgY="

Plan: 0 to add, 1 to change, 0 to destroy.
```
`aws_instance.reporter` shows NO change -- confirms row S2's finding directly.

**Invocation (TARGETED):**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_lambda_function.orchestrator
```
**Output (rc=0):**
```
Plan: 0 to add, 1 to change, 0 to destroy.
```
**S8-AC4 verdict: PASS.**

## 5. S8-AC5 -- the ledger, the targeted apply, the targeted 0-diff (PASS)

**Ledger:** opened before the apply -- `python .tools/deploy_ledger.py open --slug etfs-guardrail-eg-s-8-orchestrator-terminal-send --title "EG-s-8: the ONE terminal SES send + --gate flag, etfs-reports-orchestrator (targeted: aws_lambda_function.orchestrator only)" --author 0.9.0_WK_ETFS_GUARDRAIL~1 --leg "code|activation|etfs-reports-orchestrator|..."` -> `org/critical_paths/change_management/20260905T0550Z_etfs-guardrail-eg-s-8-orchestrator-terminal-send_deploy_completion.md`. Entry + sentinel COMMITTED (`d0edf02b28`) before the apply, alongside the `--gate` source edit.

**Apply, BY TARGET:**
```
HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/etfs-reports apply -input=false -auto-approve -target=aws_lambda_function.orchestrator
```
**Output (rc=0):**
```
comp-tagauthz gate PASSED. tombstone-gate CLEAN.
Plan: 0 to add, 1 to change, 0 to destroy.
aws_lambda_function.orchestrator: Modifications complete after 6s
Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

**Targeted 0-diff:**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -detailed-exitcode -target=aws_lambda_function.orchestrator; echo rc=$?
-> "No changes. Your infrastructure matches the configuration." rc=0
```

**`record-terraform-deploy.sh`:**
```
bash infra/aws/lambda/ci/record-terraform-deploy.sh etfs-reports --function etfs-reports-orchestrator --author "0.9.0_WK_ETFS_GUARDRAIL~1 <0.9.0_WK_ETFS_GUARDRAIL~1@opal.agent>"
-> stamped 1 of 1 rows under etfs-reports: etfs-reports-orchestrator; CHANGELOG.json updated
-> commit ee6e7e0580 "ci: record deploy etfs-reports @ d0edf02b [skip ci]" -- exactly 2 files: infra/aws/lambda/ci/lambda-source-map.json, infra/aws/terraform/etfs-reports/CHANGELOG.json (both in-grant; confirmed via `git show --stat`)
```

**Ledger close:**
```
python .tools/deploy_ledger.py close-leg --slug etfs-guardrail-eg-s-8-orchestrator-terminal-send --leg-id code --proof "..."
-> OK: leg code closed. Remaining open: NONE
python .tools/deploy_ledger.py close --slug etfs-guardrail-eg-s-8-orchestrator-terminal-send
-> OK: CLOSED ... all 1 legs proven; sentinel removed
```
**S8-AC5 verdict: PASS.**

## 6. S8-AC6 -- served vs built (PASS)

**Invocation:**
```
python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/orchestrator_served_vs_built.py
```
**Output (rc=0):**
```
SERVED_CODE_SHA256: stq9kk/+gatkLr7F/ldLzduW+i03aUCrx1ZG91wJWgY=
BUILT_ZIP_SHA256_B64: stq9kk/+gatkLr7F/ldLzduW+i03aUCrx1ZG91wJWgY=
VERDICT: MATCH
```

## 7. S8-AC7 -- the live rehearsal (PASS, safe now the deploy landed)

**Invocation attempted exactly as named:**
```
.tools/aws lambda invoke --function-name etfs-reports-orchestrator --cli-binary-format raw-in-base64-out --payload "{\"mode\":\"terminal_qa\",\"month\":\"2026-08\"}" /dev/stdout
```
**Output: refused, as the criterion's own fallback anticipated:**
```
Unknown options: --cli-binary-format, /proc/.../fd/pipe:[...]
```
**Form that ran (flag dropped, payload as plain JSON string, per the criterion's own bound):**
```
.tools/aws lambda invoke --function-name etfs-reports-orchestrator --payload "{\"mode\":\"terminal_qa\",\"month\":\"2026-08\"}" .scratch/terminal_qa_invoke_out.json
```
**Output (rc=0, StatusCode 200):**
```json
{"mode": "terminal_qa", "month": "2026-08", "subject": "URGENT: ETF month-end 2026-08 -- 0 date(s) unresolved after remediation", "to": "andrew@opalinvest.com", "body_head": "The ETF ownership coverage ladder for 2026-08 could not resolve 0 date(s) after every rung ran (probe, re-run the producer, re-check).", "ok": true}
```
`"mode": "terminal_qa"` present; no email sent (August 2026 has no `coverage_unresolved.json` yet -- `holes=0`, matching `EG-s-4`'s own live read -- so the rehearsal correctly shows 0 unresolved dates while still exercising the full build path end to end).

## 8. S8-AC9 -- MINTED (row `ETFS_GUARDRAIL-S3`): `--gate` in `_render_command`

**Invocation:**
```
python -c "s=open('infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py').read(); i=s.find('def _render_command'); j=s.find('return [', i); print('GATE_FLAG_IN_RENDER_COMMAND=%s' % ('--gate' in s[i:j]))"
```
**Output (rc=0):**
```
GATE_FLAG_IN_RENDER_COMMAND=True
```

## 9. S8-AC8 -- THE ANSWER (judgment; recorded, no verdict)

- **The send fires only from the terminal failure branch, exactly once, to andrew@ only:** `_send_terminal_unresolved` is called from exactly one place -- inside `_run`'s `if status != "Success":` branch, gated on a non-empty unresolved list; test arms (a)/(b) confirm exactly-once and zero-when-absent.
- **Dates/partner/provider are present without a follow-up question:** the email body's `date | partner | provider | class | reason` table (arm (a)) plus the egress ask section when present; confirmed again live via the `terminal_qa` rehearsal's `subject`/`body_head` fields (section 7).
- **No schedule, no topic, no alarm, no polling was added:** `NEW_TOPICS=0`; the ONLY Terraform change applied is `aws_lambda_function.orchestrator`'s `source_code_hash` on its EXISTING trigger; the `--gate` flag (S8-AC9) changes what the EXISTING scheduled render command passes to the EXISTING renderer, adding no new resource of any kind.
- **The carve-out's width is not exceeded:** checked against PRD s.0's STILL-BANNED list (new monitor/alarm/topic/freshness-service/schedule-based send) -- none appear.
- **FWD-7's EXERCISED grade needs a REAL terminal failure:** not claimed here. The deploy landed and the rehearsal ran LIVE (section 7), which is the strongest evidence available without a real ladder failure -- by the PRD's own design, a real terminal failure should be rare-to-never. RECORDED, not EXERCISED, honestly.

## 10. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
```
