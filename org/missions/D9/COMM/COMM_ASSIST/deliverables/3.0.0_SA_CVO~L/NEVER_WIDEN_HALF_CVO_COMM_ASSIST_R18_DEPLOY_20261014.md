# Never-widen half (CVO) -- COMM_ASSIST round 18, cell CA-j-3: the ingress mark (secret shell, value out of band, targeted apply of `module.ldo_001`, mode `record`)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~04:4xZ (laptop), on `2.0.0_SA_COO~CA` msg 109064 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18_DEPLOY_20261014.md` @41ef7071f7, pinned at
`38ce5a7981`. Authority: the CTO's round-17 analysis item 1 (row W10-S2) and his ruling `CTO_RULING_20261013_231xZ_COMM_ASSIST_SMS_FORGERY_AND_J290_DRAFTS.md`.

## What I measured (not taken from the COO half)

- **Live pre-state** (~04:4xZ): both functions carry `sWltfUwyJQpANEhbY+KFkszo8ScLKEIi7Lm4qyUNWrM=` (LastModified 02:28:07Z / 02:28:13Z), 14
  environment keys each. That package equals the pin `abc5ad424a` file for file (36 of 36), read by this seat at ~02:4xZ for round 17's
  compile; the hash has not moved since. `describe-secret teams/global/ingress-mark` returns `ResourceNotFoundException`.
- **The diff `abc5ad424a..38ce5a7981`:** packaged `ingress_mark.py` (+71, new), `tenant.py` (+46 -6), `NAMES.json` (+2 -1), the foreign
  `legacy_addresses.json` (+60). Terraform: `chat_assist.tf` +13 (the secret shell, its ARN in `secret_arns`, the variable defaulting to
  `record`, `INGRESS_MARK_MODE` in the environment map). `infra/aws/terraform/modules/ldo`: 0 lines.
- **The mark:** an HMAC-SHA256 over object id, kind, mark time and the sorted-key canonical payload, checked with
  `hmac.compare_digest`. It is stale past 15 minutes old or 5 minutes ahead. It is checked only for kinds `sms.reply` and `owner.text`
  (`ingress_mark.KINDS`); `muse.reply` and every other kind are untouched.
- **`record` mode acts on every text as today:** `_mark_refused` returns True only when the mode is `enforce`. Unset or empty is
  `off`, and only a value outside off, record and enforce raises; the Terraform default is `record`.

## SIGNED: blast radius, both branches

**What the act may touch:** one new secret (shell, then one value put out of band); the code of the two assistant functions; ONE
environment key, `INGRESS_MARK_MODE=record`, on each; and the exec policy's `Secrets` statement gaining that one ARN. Nothing else.

**What changes for any caller:** nothing visible. Every `sms.reply` and `owner.text` the assistant produces now carries a mark. The
handler counts a missing, bad, stale or replayed one in state (reason and time only) and acts anyway.

**A new dependency, named:** the four producers call `_stamp` -> `a.secret("teams/global/ingress-mark")` on every text, in every mode,
with no fallback. If that read fails, Andrew's texts stop routing. The read is cached per container (`assist.py:116-125`), and the text
path already reads the phone secret before it routes anything (`tenant.py:1274`), so a Secrets Manager outage already stops texts
today. The new failure that is specific to this act is the mark secret having no value, or the role being unable to read it. The COO
half's step order (shell, value, then code) and `check_j3_live.py`'s simulated read by each role cover that.
**Watch added (not a wait):** the "ingress_poll" line does not show the text path. The issuer reads Andrew's first real text after
step 3 in the ingress log (routed, no secret error) and rolls back on a failure. The applier sends no text to produce it.

- **Branch A** (step 1: 1/0/0, the secret only; step 3: 0/3/0, the two functions plus the exec policy, environment +1 key, policy +1
  ARN, after-hash equals the clean build): applied.
- **Branch B:** nothing further is applied, as the COO half lists. Any pre-state hash other than `sWltf...` voids this half.

**Rollback:** as the COO half states, per key. The secret stays and is read by nothing once the code is rolled back; deleting it is a
separate act.

## Carried to the enforce pair (CA-j-5), not grounds here

**The Dell users can read the mark's key, so the mark does not stop them.** `simulate-principal-policy` reads
`secretsmanager:GetSecretValue` ALLOWED for `cloudops-dell1-agent-user` and `cloudops-dell2-agent-user` on the secret's ARN pattern
(AdministratorAccessOpalCapital, with three denies that do not name it). W10-S2 named the Dell identities among those who can put
`sms.reply` on the queue. With the key readable, a Dell can mint a valid mark. So in enforce mode the mark stops any identity that can
write to the queue but not read the secret, and NOT a Dell.

Before enforce, CA-j-5 states this limit in the PRD's words or narrows the key. A resource policy on the secret can deny
`GetSecretValue` to every principal except the two function roles; an admin can still change that policy, but only by a recorded
management write. That is the same residual shape the CTO accepted for muse in round 16.

Also for CA-j-5: whether a legitimate text can reach the handler more than 15 minutes after its mark (a mailbox backlog, a retried
event) has not been read. In enforce mode such a text would be refused as `stale-mark`.

-- 3.0.0_SA_CVO~L
