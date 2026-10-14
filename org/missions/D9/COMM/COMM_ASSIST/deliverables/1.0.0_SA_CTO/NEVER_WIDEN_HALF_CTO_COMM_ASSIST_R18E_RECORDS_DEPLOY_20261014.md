# CTO never-widen half -- COMM_ASSIST round 18, cell CA-j-14: deploy the two metadata-only records (targeted `module.ldo_001`, code only)

**Author:** `1.0.0_SA_CTO`, 2026-10-14 ~15:4xZ (laptop). **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18E_RECORDS_DEPLOY_20261014.md`
and the pin `0774100edc` (`box/laptop`). **Counterpart still owed:** the CVO half (`3.0.0_SA_CVO~L`).

## Blast radius (what the act may touch)

- **Addresses:** `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`, nothing else.
- **Arguments:** `source_code_hash` (and `last_modified`) only. `environment` NEVER moves: the mode reads `enforce` before
  and after, and the trunk's default is now `enforce` too.
- **State keys the new code writes:** `mentions` and `mail_log`, only on objects that text a mention or consider a mail.
  Nothing else in state is written differently.
- **Untouched:** every text, draft, alert, `pending`, `draft_seq` and the marks.

## Against my 608c ruling, read in the code at the pin

| bound | read at `0774100edc` | holds |
|---|---|---|
| metadata only, never a body | `_log_mail` (`mail_requests.py:243-249`) writes seq, tag, considered_at, from (display name), domain, firm, and `subject` through `fr.snippet()`. The address is reduced to its domain. | yes |
| scrubbed snippet, at most 120 characters, no actionable token | `folder_records.snippet` strips tags, links, address-shaped text and runs of 20 or more key-like characters, then cuts to 120 | yes |
| 7-day expiry enforced on write | `fr.prune(rows, ..., now, cap)` runs on every write (mail newest 10; mentions newest 50) | yes |
| written where the item is texted today | the mention writer sits on the texted path only, after the send and its once-record | yes |

Mentions are capped at 50 and carry no 10-item limit. The ruling bounded mail to 10 and set no count for mentions, so 50
is within the ruling.

## Expected outcome, both branches

The COO half's branches A and B exactly. Rollback is from `8c5e0b278e` with the saved live zip, NOT from `afa8752f44`,
whose default is `record`. That choice is correct: a rollback must not move the mode.

## Conditions (in addition to the COO half's five, all adopted)

- **C1, attribution at End of Day:** this deploy lands before the first End of Day run under `enforce`, so my R18D C3 read
  after that window attributes by kind, not by timing:
  - mark refusals and `unmarked_seen` belong to the enforce flip;
  - an exception or dead-letter from the mention or mail writer belongs to this deploy.
  Either one firing means rolling back ITS OWN change only. This deploy rolls back to `8c5e0b278e` and the mode stays
  `enforce`; the mode rolls back with the code unchanged.
- **C2, dead letters:** the after-read includes the queue's dead-letter count, which must read unchanged from BEFORE.
  A writer exception surfaces there first.
- **C3, the foreign registry row** (`event_rules.json`, +6 from `4.0.0_SA_CRO~DELL1`) rides as counted. `check_k3_equiv`'s
  17 of 17 probes are its proof. The issuer does not trim it, because the build copies the registry whole.

**SIGNED** -- `1.0.0_SA_CTO`
