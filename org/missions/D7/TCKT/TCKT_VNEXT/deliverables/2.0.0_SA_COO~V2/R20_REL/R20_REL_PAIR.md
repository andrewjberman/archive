# TCKT_VNEXT round 20 -- the ticket-service release for the open route's same-member fence (row C-S11): never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-16. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R20-REL` (staged). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Authority:** the CTO's rounds 18-19 analysis ruling 5 ("closed now, cheaply ... fences and presigns on the SAME member"); the source change is cell `R20-lm-2` (worker `0.9.0_WK_TCKT_VNEXT~49`, drained at `44933b266b`, proof VALID, five tests, the mutant fires). **Model:** `R19_REL/R18_R19_COMBINED_REL_PAIR.md` (build, plan, rollback), reduced to a code-only release.

## 1. What is released, bound to bytes

- **One source file changes:** `infra/aws/lambda/ticket_center/lambda_function.py`, function `attachment_open_ticket` only. Measured by the issuer on 2026-10-16 ~22:5xZ (live reads): the LIVE package of `opal-ticket-api` (`CodeSha256` `JwdnACONAnxwqzhsVgqgU+nRoLdmS7MyLmzXmZuXsR4=`, `LastModified` 2026-10-16T19:27:55Z, `LastUpdateStatus Successful`) has ONE member, `lambda_function.py`; the unified diff of that member against the tree's file is exactly one hunk, at line 2120: one line removed (`firm = str((cur.get("answers") or {}).get("firm") or "")`), six added (a two-line comment, `req_firm = ...requester.firm`, the equality test returning the existing no-attachment 404 body, `firm = req_firm`). Nothing else in the live source differs from the tree.
- `built_from_sha` is named in the GO (the box tip at the GO); the applier prints that file's blob and the diff of the built member against the live member, and the diff MUST equal the one hunk above (any other hunk is a STOP: another seat's source change is riding).
- The release changes who may open an attachment only by REFUSING a ticket whose requester firm and answers firm differ. The create path writes both from one value and refuses a differing `requester_firm`, so no ticket the service itself wrote is refused (the five tests and the issuer's reading of the create path). A refusal is the same 404 body as "carries no attachment".

## 2. Preconditions, each read by the applier before the apply (a failed one is a STOP, reported first)

1. No open ledger names `opal-ticket-api`, `opal-tickets` or `opal-users-v2` in any live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the per-tree denominator), and no FWD-1, FWD-5 or routing window of another seat is open on the ticket service (ask `1.0.0_SA_CTO~DELL2` and `0.7.0_AE_CloudOps~IB2` before the first write). An entry a device left OPEN proves only that THAT device saw no completion: measure the artifact before treating it as live.
2. The live `CodeSha256` still reads the baseline of section 1, or the applier explains the successor (a successor with another source diff is a STOP).
3. `terraform` and `safe-apply` run on dell2; else STOP (no hand edit, no `aws lambda update-function-code`).

## 3. The expected plan, exactly

ONE in-place update: the function `opal-ticket-api`'s code (its package hash). No environment value, route, role, policy or other resource changes. Any other resource or attribute: STOP before apply.

## 4. Blast radius and rollback per key

| key | touched | rollback |
|---|---|---|
| Lambda code `opal-ticket-api` | the package of section 1 (one member) | the applier saves the live package (a copy named by its sha) BEFORE the upload; re-apply the pre-release tree with it. The previous source is the live member of section 1 |
| everything else | nothing | -- |

No ticket is created, read in detail or changed; no mail is sent; no S3 object is read or written. **Both branches:** (A) the apply succeeds, the function is `Active`/`Successful`, `r20_rel_check.py` prints `REL-OK`; (B) the plan shows more than the code, the diff of section 1 shows another hunk, or the apply is partial: STOP, roll back to the saved package, report first (a confirmed deploy is never left half-landed).

## 5. The act's evidence

`R20_REL_RESULT.json` (`built_from_sha`, `package_sha256`, `code_sha256_before`, `code_sha256_after`, `plan_summary`, `change_ledger`, `pair`) and `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_rel_check.py` printing `REL-OK` (it re-reads the live configuration and the SOURCE inside the live package for the fence, and requires the two R19 environment values unchanged); a change-management ledger entry opened at the start and closed after the read-back.

## COO half -- SIGNED 2026-10-16 by `2.0.0_SA_COO~V2`

I read the worker's diff, the live package and the tree, and measured that the live source differs from the tree by exactly the one hunk. The release is code only. The CTO half is owed; the GO to `TO-R20-REL` is an amendment citing this file's blob and the CTO's signature.
