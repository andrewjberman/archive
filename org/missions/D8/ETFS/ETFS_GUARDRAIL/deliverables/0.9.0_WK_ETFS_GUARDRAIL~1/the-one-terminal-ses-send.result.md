# EG-s-8 -- the ONE terminal SES send

**TO:** `ETFS_GUARDRAIL.TO-EG-s-8` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `c50c72f92a` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** wire.

**HEADLINE: the deploy did NOT land this session.** `S8-AC4`'s amended targeted-plan invocation, copied from `EG-s-7`'s working fix, does NOT isolate `aws_lambda_function.orchestrator` from the pre-existing `aws_instance.reporter` drift here -- a REAL Terraform dependency (`REPORTER_INSTANCE_ID = aws_instance.reporter.id`) pulls the instance into the targeted plan's closure. No apply was attempted (per this order's own bound), and the live invoke (`S8-AC7`) was deliberately NOT run because it would have hit the OLD, undeployed function and triggered a real production render. Filed `ETFS_GUARDRAIL-W1-S8` (BLOCKING/INERT). Code, tests and the ledger-open half are complete and committed; the apply/serve half is not.

## Code changes

`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`: added `_read_coverage_artifacts(month) -> dict` (best-effort read of `coverage_verdict.json`/`coverage_unresolved.json`/`coverage_egress_ask.json`, absence normal), `_build_terminal_email(month, unresolved, ask)` (shared build, never sends), `_send_terminal_unresolved(month, unresolved, ask)` (the third and only new send call site), enriched the `if status != "Success":` branch of `_run` to fold the coverage artifacts into the existing `_alert` and to call `_send_terminal_unresolved` exactly once when `coverage_unresolved.json` names at least one unresolved day, and added mode `terminal_qa` (send-free rehearsal, mirrors `email_qa`).

## 1. S8-AC1 -- the five-arm battery

**Invocation:**
```
python -m pytest infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py -q
```
**Output (rc=0):**
```
5 passed in 0.27s
```
Arms: (a) unresolved present -> exactly one `send_raw_email`, `Destinations == ["andrew@opalinvest.com"]`, body names every date/partner/provider; (b) unresolved absent -> zero sends, the ordinary render-failure alert text unchanged (no "Unresolved dates" section); (c) `terminal_qa` makes no SES call; (d) `absence_check` makes no SES call; (e) the mode table's only REAL sending mode besides the terminal path (reachable only from `_run`) is `send_correction` -- confirmed by parsing the handler's own source for any `if mode ==` block that calls a bare `_send_*` function by name.

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
**Output (rc=0):**
```
OK: pre-commit gate clean for 2 of 2 file(s)
```

## 4. S8-AC4 -- the TARGETED plan (FAIL by output -- a real dependency, not a coincidence)

**Terraform binary confirmed:** `.tools/terraform.exe version` -> `Terraform v1.9.8` (issuer-provisioned, per the hand-off). `init -input=false` run once (fresh worktree, no `.terraform/`): rc=0.

**Full (untargeted) plan first -- the honest state of the whole directory:**
```
terraform -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false

  # aws_instance.reporter will be updated in-place
      ~ user_data = "e47b615c4b7a16df31146d6834cb30ef1693c80f" -> "434774b5a5facfeb4931f837e1b93edc13bbec35"

  # aws_lambda_function.orchestrator will be updated in-place
      ~ source_code_hash = "7CIW8veDKFnk/rNKhXdInVVpp60dhXiZf5Lye9a0w3Q=" -> "YurQLInqu+YsVYIrQXcuFoMMeGS7GfDB4QvhAZbrm3Q="

Plan: 0 to add, 2 to change, 0 to destroy.
```

**Invocation (TARGETED, per the amended criterion):**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_lambda_function.orchestrator
```
**Output (rc=0):**
```
  # aws_instance.reporter will be updated in-place
      ~ user_data = "e47b615c4b7a16df31146d6834cb30ef1693c80f" -> "434774b5a5facfeb4931f837e1b93edc13bbec35"

  # aws_lambda_function.orchestrator will be updated in-place
      ~ source_code_hash = "7CIW8veDKFnk/rNKhXdInVVpp60dhXiZf5Lye9a0w3Q=" -> "YurQLInqu+YsVYIrQXcuFoMMeGS7GfDB4QvhAZbrm3Q="

Plan: 0 to add, 2 to change, 0 to destroy.
```

**S8-AC4 verdict: FAIL.** The targeted plan STILL shows both resources -- `-target` did not isolate the orchestrator here, unlike `EG-s-7`'s `aws_iam_role_policy.reporter`. **Root cause (not a repeat of the same finding): `infra/aws/terraform/etfs-reports/orchestrator.tf`'s `environment.variables` block sets `REPORTER_INSTANCE_ID = aws_instance.reporter.id` -- a real Terraform config dependency edge from the lambda to the instance.** Terraform's `-target` semantics include the target's full dependency closure (confirmed: no `-exclude` flag exists in this v1.9.8 binary's `plan -help` output), so any pending diff on `aws_instance.reporter` rides along with any targeted plan of `aws_lambda_function.orchestrator` no matter what. **No apply was attempted.** Filed `ETFS_GUARDRAIL-W1-S8` (BLOCKING/INERT).

## 5. S8-AC5 -- UNCOMPUTABLE-BY-CONSTRUCTION

The criterion is conditional on AC4's targeted plan reading exactly one resource; it read two. No apply, no ledger apply-leg, no 0-diff read. Rides the same later run `EG-s-7`'s `W1-S7` finding names (the pre-existing `aws_instance.reporter` drift dispositioned) OR a Terraform refactor decoupling `REPORTER_INSTANCE_ID` from a direct resource-attribute reference (out of this order's scope).

## 6. S8-AC6 -- served vs built (FAIL by output -- honest, expected)

**Invocation:**
```
python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/orchestrator_served_vs_built.py
```
**Output (rc=0):**
```
SERVED_CODE_SHA256: 7CIW8veDKFnk/rNKhXdInVVpp60dhXiZf5Lye9a0w3Q=
BUILT_ZIP_SHA256_B64: YurQLInqu+YsVYIrQXcuFoMMeGS7GfDB4QvhAZbrm3Q=
VERDICT: MISMATCH
```
Both hashes independently match the two hash values Terraform itself printed in section 4's plan (`source_code_hash = "..." -> "..."`) -- a second instrument (a local Python `hashlib`/`base64` computation vs Terraform's own provider-computed hash) agreeing with the first, corroborating that the script measures the right thing. `VERDICT: MISMATCH` is the correct, expected reading given `S8-AC4`'s block: nothing new has been deployed.

## 7. S8-AC7 -- NOT RUN (declared exclusion, not a FAIL)

**This worker deliberately did NOT run this criterion's live invoke.** The deployed function is still the PRE-this-order code (confirmed by `SERVED_CODE_SHA256` above matching the plan's OLD hash). That old `handler()`'s mode dispatch is `if mode=="absence_check" ...; if mode=="email_qa" ...; if mode=="send_correction_qa" ...; if mode=="send_correction" ...; _run(); return {"mode":"run","ok":True}` -- `"terminal_qa"` matches none of its branches, so invoking it live would fall through to `_run()`, the REAL production path: start the reporter EC2 instance, attempt a real SSM render, and (if it somehow succeeded) potentially a real SES send. Running this criterion against an undeployed function risks a genuine, expensive, unauthorized production side effect for the sake of a mechanical checkbox -- declined. Recorded as part of `ETFS_GUARDRAIL-W1-S8`.

**Local rehearsal evidence instead (send-free, no live invoke):** `test_terminal_qa_makes_no_ses_call` (S8-AC1 arm c) exercises the exact `terminal_qa` code path in-process against a stubbed month with one unresolved day, confirming `result["to"] == "andrew@opalinvest.com"`, `"URGENT" in result["subject"]`, and zero `ses` calls recorded on the stub.

## 8. S8-AC8 -- THE ANSWER (judgment; recorded, no verdict)

- **The send fires only from the terminal failure branch, exactly once, to andrew@ only:** `_send_terminal_unresolved` is called from exactly one place in the source -- inside `_run`'s `if status != "Success":` branch, gated additionally on `unresolved_days` being non-empty; test arm (a) confirms exactly one `send_raw_email` call with `Destinations == ["andrew@opalinvest.com"]`; test arm (b) confirms zero sends when `coverage_unresolved.json` is absent.
- **Dates/partner/provider are present without a follow-up question:** the email body's `date | partner | provider | class | reason` table (test arm (a) asserts every field appears in the raw MIME) plus the egress ask section when present.
- **No schedule, no topic, no alarm, no polling was added:** `NEW_TOPICS=0` (S8-AC2); the send is reachable only from `_run`'s existing refusal branch, which itself only fires from the existing EventBridge-scheduled `{"mode":"run"}` invocation already in place before this order (no new schedule resource touched, no new EventBridge rule, no CloudWatch alarm anywhere in this diff).
- **The carve-out's width is not exceeded:** compared against PRD s.0's STILL-BANNED list (new monitor, new alarm, new SNS topic, standing freshness service, any schedule-based send) -- none of these appear in the diff; the ONLY new resource-level Terraform change is `aws_lambda_function.orchestrator`'s `source_code_hash` (a code update to an EXISTING function on its EXISTING trigger).
- **FWD-7's EXERCISED grade needs a REAL terminal failure, which this order could not produce or should not simulate live:** the deploy did not land this session (S8-AC4/AC5), so even had it landed, this order would have offered only the REHEARSAL (`terminal_qa`, local + would-be-live) as evidence, never a live production failure -- by the PRD's own design ("the backfill strategy must be effective enough that it doesn't happen"), a REAL terminal failure is expected to be rare-to-never. RECORDED, not EXERCISED, honestly stated as such.

## 9. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
-> b000632f27e2e7462a8b666f15054a601b0324d1
```
