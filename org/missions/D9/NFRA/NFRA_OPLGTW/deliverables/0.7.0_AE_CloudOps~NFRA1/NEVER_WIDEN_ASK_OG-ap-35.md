# NEVER-WIDEN ASK -- `OG-ap-35` -- narrow one client's live Schwab grant by ONE key, removing `download_filtered`

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-35.narrow-alyssa-no-download.md` (GO for Phase A: msg 35322).
Basis: the CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_BD68_ALYSSA_DOWNLOADS_ENFORCE_HIS_WORD_20261017_Z.md` (open call `sitez-20261016T111519Z-bd68`): Andrew's word of 2026-10-08, "no downloads needed yet", is enforced. Template: `OG-mg-1` (the same writer, role and ledger shape).
Phase A is READ ONLY: nothing is written to the store. Identifiers (tenant, object id, e-mail) appear in no repo file: they live only in `%LOCALAPPDATA%/opal/og-salt/ag1/`, outside the worktree. This file carries hashes (first 10 hex of sha256), roles, operation names and counts.

## 1. What changes, and for whom

- The client's principal (role `alyssa`, pk hash `2c61471b14`) loses ONE operation, `download_filtered`. Her other operations (`describe`, `list`, `query`) are unchanged. Nobody gains anything.
- Changed keys: operations only.
- Her current value (read live, strongly consistent, fully paginated, `AG1_BEFORE.json`): profile revision 4, grant revision 4, operations `describe, download_filtered, list, query`, scope-without-operations hash `5f95dcbca8`. The candidate is that scope with `operations` minus `download_filtered`; `prepare()` ran under the operator role, accepted it, and printed an 8-line diff whose only changed key is `operations` (`AG1_PREFLIGHT.md`). The grant would move to revision 5 (the profile to revision 5).
- The two other active principals are not touched; their grant hashes are recorded so the act can prove they did not move: Andrew `grant_hash` and the Bloomberg identity `grant_hash` in `AG1_BEFORE.json` (`others_hash`). Both hold the same four operations at grant revision 1.

## 2. Usage before the write (counts only; reported to the CTO for Andrew)

- **`download_filtered` calls by her principal since her grant's activation (2026-09-27T00:48:46Z; the operation was added to her grant at 2026-10-06T18:56:28Z): 0. Last use: none.**
- Source of record: the Schwab acknowledged audit prefix of the gateway audit lake (every Schwab release awaits its receipt there; events carry the principal as a hash and the operation as a fixed word). Window: 21 day partitions (2026-09-27 to 2026-10-17); 96 objects listed, 96 read, 0 read errors, 0 malformed. Her principal's hash appears in 5 events (3 distinct operations, none a download); some principal made 1 download event in the window.
- **Positive control:** the scan sees her 5 events and the 1 download event of another principal, so a zero is not an instrument that cannot see.
- **The general audit lake was also read and is NOT relied on:** 118433 records in 118433 objects, 0 errors, and none carries her principal (the control that it can see her failed). Its zero is reported, not used.
- Method: the census of `OG-bd-1` (row `Z-W57-S2`), her principal resolved in-process and never printed.

## 3. The writer, and what its transaction writes (the lesson of `OG-mg-1`: read the side-writes)

The writer is `infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py`: `prepare` then `activate`, one `operator_transact`, under the role `opal-gateway-access-admin`, with `--approver "Andrew Berman"` and `--source-authorization` naming the CTO ruling. **Writers of the property (a grant's `operations`): N = 1 module** (`activate()`; its callers are this CLI and the portal grant-writer Lambda, which stages the same module). `activate()` builds only Put operations and never deletes.

One transaction writes, read from the module and not assumed:
1. the `principal_profile` put (revision 4 to 5, `grant_revision` 4 to 5, status active, the stored e-mail unchanged, kind restricted);
2. the `data_entitlement` put (the new revision 5; revision 4 stays as history);
3. one `operator_audit` append (free text of one line naming this order and the ruling; no client name);
4. **one `email_deny` put for her stored e-mail**, conditioned `attribute_not_exists(pk) OR (tid = :tid AND oid = :oid)`. Her record exists today (present, status active, attribute names `oid, pk, record_type, sk, status, tid`), so the condition holds and the put re-writes the same tid, oid and status active. **Browser effect: none.** Her browser-route deny (contract C2; it was intended and stays) is not changed, and nobody else's is touched.

IAM preflight (`AG1_PREFLIGHT.md`, role assumed for real, then simulated with the `dynamodb:LeadingKeys` context `POLICY#*`): `GetItem` allowed, `PutItem` allowed, `UpdateItem` allowed; `PutItem` without the context implicitDeny (the condition mode, not a missing grant); `DeleteItem` and `Scan` implicitDeny (never used). No STOP, no widening.

**Blast radius:** four items of one principal's partition (profile, new grant revision, one audit record, the deny record). **What it may never touch:** any other principal's items (their hashes must read equal before and after), any other `email_deny` key, any IAM, policy, Lambda, gateway, allowlist or environment setting, any delete.

## 4. Both branches

- The base revisions still read profile 4 and grant 4 at the act: the transaction lands.
- Either moved since Phase A (a stale base): the writer's optimistic condition REFUSES, nothing is written, and Phase A is re-cut once.
- A failed read-back (the download is not refused, or another operation stops answering): restore at once (section 6), close the ledger ROLLED BACK, report.

## 5. Read-back (Phase B; the way `OG-ap-30` read the deny guard back)

Read-back: through the INSTALLED code on the host, the entitlement decision for her principal and the operation `download_filtered` is a REFUSAL, and for one other operation of hers (`list` or `describe`) it ANSWERS (allowed). The record `AG1_AFTER.json` carries her profile and grant revisions, the operations, the scope-without-operations hash (must equal the before hash), the two other principals' hashes (must equal the before hashes) and the two booleans. **No call is made as her. No message goes to her or her firm.**

## 6. Rollback

Rollback: restore. The next revision (6) is the before scope, written through the same `activate`, never a delete and never a tombstone; the before scope is saved off-repo with the candidate. Time to restore: one `activate` (seconds).

## 7. Conditions

- **No seat contacts the client or the firm.** No seat makes any call as her principal.
- Andrew can reverse the rule with one word, "Alyssa may download": the same writer then restores the operation (the restore above).
- No tenant, object id, e-mail, account id or grant value is written to the repo, a row, a message or a report: hashes, roles, operation names and counts only.
- The usage count is zero and does not gate the act (the ruling enforces Andrew's word either way); it is reported so Andrew sees it before Phase B.

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed against this ask's sha256. The ruling it rests on is the CTO's own.

### COO half (`2.0.0_SA_COO~O`)

To be signed against this ask's sha256.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed against this ask's sha256.
