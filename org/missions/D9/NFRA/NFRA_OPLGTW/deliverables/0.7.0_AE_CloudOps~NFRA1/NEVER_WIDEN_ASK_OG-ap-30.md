# NEVER-WIDEN ASK -- `OG-ap-30` -- delete two `email_deny` records (the OG-mg-1 browser side effect)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-30.reverse-email-deny-side-effect.md`.
Basis: CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_EMAIL_DENY_SIDE_EFFECT_OF_OG_MG_1_20261016_Z.md` (shape b; its CTO half covers exactly this two-key write set); CVO half `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/3.0.0_SA_CVO~Z/NEVER_WIDEN_HALF_CVO_EMAIL_DENY_REVERSAL_20261016.md` @c39c415178 (it re-reads this ask).
Phase A is READ ONLY: this file, `DENY_BEFORE_OG-ap-30.json` and a git-excluded rollback file are the only things written. Nothing in the table has been written.

## 1. The diff

Table `gateway-access-state-table` (us-east-1), items keyed `pk` = `POLICY#EMAILDENY#` + sha256hex(`og-email-deny/v1|` + lowercased e-mail), `sk` = `email_deny`.

- DELETE the record for `andrew@opalinvest.com`.
- DELETE the record for `opalbloomberg@opalinvest.com`.
- CONDITION CHECK (no write) on the record for `alyssa@opalinvest.com`.

Nothing else: no put, no update, no scan-and-delete, no loop, no other table, no code, no deploy, no IAM change. The write set is a literal two-key list.

## 2. The widening

A NARROWING reversal. It RE-OPENS the four email-only browser routes (`/login`, `/sprint*`, `/rivalfunds*`, `/yearinreview*`) to the two Opal owner e-mails, which were open before 11:22Z on 2026-10-16. No data scope changes. The `principal_profile` and `data_entitlement` records and the grants of `OG-mg-1` R1 and R2 stay exactly as signed, so both owner principals remain RESTRICTED on the MCP surface. No `operator_audit` record is touched.

`alyssa@opalinvest.com` is UNTOUCHED: her deny (restricted since 2026-09-27) is intended and stays active.

## 3. Both branches

One `TransactWriteItems` (us-east-1, the applier's own audited identity; the gateway operator role holds no DeleteItem by design and is NOT used). Each delete carries `attribute_exists(pk) AND #s = :a` (`#s` = `status`, `:a` = `active`); the check on the alyssa record carries the same condition, so the whole transaction fails closed if her record moved.

- Branch 1, both records present and active, each item's sha256 equal to the one recorded in `DENY_BEFORE_OG-ap-30.json`: the transaction lands; both records are deleted.
- Branch 2, a record absent or changed since the read (sha256 or status differs, or the count is no longer 3): NO key is written. The applier STOPS, files a BLOCKING row and reports. The transaction is all-or-nothing, so there is no partial landing.
- Identity denied the write: STOP and report; nothing is widened to get past it.

Measured before the act (Phase A, strongly consistent): all three records present and `active`; the `email_deny` count is 3. Permission simulation for the applier's identity on the table: DeleteItem, ConditionCheckItem, PutItem and GetItem all allowed (read-only simulation, nothing written).

## 4. Blast radius and what it may never touch

May touch: two items in one table (the andrew@ and opalbloomberg@ `email_deny` records), read-checked on a third.
May never touch: alyssa's record; any other `email_deny` key; any `principal_profile`, `data_entitlement` or `operator_audit` record; the MCP tool surface; the deploy scripts; any IAM, Terraform or other resource.

## 5. Rollback, per key

The full original items (every attribute, DynamoDB typed form) are saved in `DENY_ROLLBACK_ITEMS.json` in this folder. It holds principal identifiers, so it is git-excluded: never committed, imaged or mailed.

- andrew@ record: `PutItem` the saved item back from `DENY_ROLLBACK_ITEMS.json`, or `deny-backfill` for that e-mail.
- opalbloomberg@ record: the same, for that key.
- Read back after a rollback: the record is present and `active`, and the `email_deny` count is 3.
- The rollback is two single-item puts of known items, so the measured rollback time is seconds; it is recorded in the Phase B report.

## 6. Read-backs (strongly consistent, after the transaction)

- `ap30.AC2`: andrew@ record present NO; opalbloomberg@ record present NO; alyssa present YES and active YES; `email_deny` total 1 (before 3, minus 2); the rollback file is present and tracked by git 0.
- `DENY_AFTER_OG-ap-30.json`: counts and booleans only.
- The issuer's close run (the applier cannot drive it, because the ALB e-mail comes from the Entra sign-in): the owner account opens `/sprint` and `/rivalfunds` once each through MC Portal and reads what each answered.

Failure branches in words both halves repeat: if the read-back differs from the lines above, grade FAIL as measured, restore the saved item for any key that should still exist, open a row, and the issuer decides. Do not repair a criterion.

## 7. The three halves

The CTO half is signed in the ruling named above. The CVO half is signed at `c39c415178` and re-reads this ask. The COO half is the issuer's. The issuer's GO names this file's sha256 and all three halves.

### CTO half

Signed in the ruling named above for exactly the two-key write set in section 1. Pending the issuer's GO naming this ask's sha256.

### COO half

To be signed by `2.0.0_SA_COO~O` against this ask's sha256.

### CVO half

Signed at `c39c415178`; to re-read this ask at its sha256.
