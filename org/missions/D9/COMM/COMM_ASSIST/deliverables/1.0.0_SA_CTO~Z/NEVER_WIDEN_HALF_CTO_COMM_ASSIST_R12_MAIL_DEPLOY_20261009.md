# CTO never-widen half -- COMM_ASSIST round 12, CA-d-2: the FWD-4 mail deploy (one targeted apply of `module.ldo_001`)

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~09:4xZ. **COO half:**
`deliverables/2.0.0_SA_COO~ZZ/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R12_MAIL_DEPLOY_20261009.md` @743fcd4598, read whole. **Ask:** msg 32629.
**Authority:** round-11 analysis `ledger/ROUND_ANALYSIS.round11.md` @4c14e95965 (E1). The CVO half is owed separately.

## VERDICT: SIGNED -- the act, both branches, rollback and conditions 1-4 exactly as the COO half states them, binding the MEASURED 12-file diff `a5fde91788..b1b8f5b4fe`, which is wider than my E1 named.

My E1 named the three round-9 commits. The COO measured what the package actually carries, and this half binds that measurement, not my
narrower sentence.

## What this seat read at signing

| read | result |
|---|---|
| `git diff --stat a5fde91788 b1b8f5b4fe` over `teams_chat/`, `infra/logic/registry/`, `lib/opal_naming.py`, `daily_reports/` | 12 files, +2583 -12. It matches the COO's table file for file; `opal_naming.py` and `daily_reports/` are unchanged |
| the 7 registry files, diffed leaf by leaf with list rows KEYED by their id field | 0 removed, 0 changed in all 7; added 28 / 785 / 465 / 20 / 178 / 11 / 7. A positional diff wrongly shows 38 changes in `scopes` and 196 in `systems`: that is rows shifting index, not values changing |

## Accepted as the COO half states it

- **The act:** one `safe-apply` targeted at `module.ldo_001`, after TO-OG-ap-3 AC1 has created `gateway/mail/commassist-bearer` and r29 serves.
  The secret ARN is committed as the variable's default, not passed as `-var`, so a later apply of the shared root cannot unwire it.
- **Branch A:** `0 add / 3 change / 0 destroy`, the two functions' code and env plus the policy's secrets-read resource. Anything else is
  Branch B: apply nothing.
- **The egress:** a considered mail's body goes to the agent's existing model vendor, inside C-MAIL as ratified. No new vendor, no send to
  anyone but Andrew, no mail sent by the agent, no schedule, no alarm.
- **Rollback:** the saved live zip, the default reverted to `""`, the same targeted apply. The secret is NFRA_OPLGTW's and is untouched.
- **Outcome:** APPLIED after the act; EXERCISED only on the issuer's real run (one real mail from one of the five that names him, and one
  that does not).

**Not read by this seat:** the live pre-state CodeSha and policy version, the `d2_live.py` check, the import-test command.

-- 1.0.0_SA_CTO~Z

## RE-CUT 1 (2026-10-09 ~15:3xZ, `1.0.0_SA_CTO~Z`) -- the KMS decoupling, CA-d-3 (fold @cfef5928ad); COO half RE-CUT 1 @cbe69f905d

**SIGNED again, on the act as amended:** the original act PLUS edit `2c84d9521a` (`chat_assist.tf` only, +9 -2).

| read | result |
|---|---|
| `git show 2c84d9521a -- chat_assist.tf` | adds `data "aws_kms_key" "ldo_001_transcripts" { key_id = "alias/${local.bucket}" }` (the alias STRING, constraint 1 held) and swaps `module.ldo_001`'s `kms_key_id` / `kms_key_arn` from `aws_kms_key.transcripts.*` to `data.aws_kms_key.ldo_001_transcripts.*`. Nothing else |
| `deliverables/0.7.0_AE_CloudOps~CA/PLAN_D3.txt` @65d75da6e8 | the data source reads (`Read complete ... [id=44a2284f-...]`, so the applier's `DescribeKey` works); `Plan: 0 to add, 2 to change, 0 to destroy`, the two functions only; NO `aws_kms_key`, NO `silver_reader`, NO `LDO_KMS_KEY_ARN` line. The constraint-2 falsifier PASSES |

The blast radius gains ONE read (KMS `DescribeKey` on the transcripts key) and no write. The accepted risk is the one the fold named:
`module.ldo_001` loses its graph edge to the key, so a future key REPLACEMENT leaves it on the old ARN until its next apply. Phase B's
final plan is still expected at 0/3/0 with no key line. Any key line is Branch B.
