# NEVER-WIDEN ASK -- `OG-ms-2` -- add the Schwab master `08403355` ("0840") to ALYSSA's grant; ONLY `scope.masters` and `scope.accounts[08403355]` change

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ms-2.round-46-add-master-08403355-to-alyssas-schwab-grant.md` (GO for Phase A: msg 36116). Phase A writes NOTHING.
Read at 2026-10-19T21:25:20Z from the store with a strongly consistent, fully paginated scan (27 `POLICY#` items among 2104 items). The record is named by role and `pk_hash` only; no account id, tid, oid or e-mail appears here.

## 1. What she gains (counts, from the diff)

- **One master:** `08403355`. Her grant today (profile revision 6, grant revision 6, pk_hash `2c61471b14`) names the masters `08242234` and `08335338`; the candidate (revisions 7 and 7) names `08242234`, `08335338` and `08403355`.
- **Its accounts: 30** (the master's full CURRENT account set). The accounts of the two masters she already holds are **NOT touched** (7599 and 7690 accounts before and after; `other_masters_accounts_unchanged` reads true in `MS2_DIFF.json`).
- **The same four datasets** her grant already names, **the same operations** (`list`, `describe`, `query`; her no-download rule stands, `download_filtered` is NOT granted), the same columns and the same rolling window. `changed_keys` of the candidate against the grant in force reads **`["accounts", "masters"]`** and nothing else.
- **ONE MASTER ONLY:** no other master, dataset, column, operation or date window is added, and no other principal is touched. Andrew's grant stays at revision 1 (held by `OG-mg-2` option (b)); this order names Alyssa only.

## 2. The account set: method, date and prefix; what Phase A confirmed (read, not assumed)

- Method (the one `OG-mg-2` used and the CTO accepted): the distinct `account_id` values of the **`dim_balance`** table (one row per account) of the master at its latest complete date. Date: **2026-10-16** (the newest `meta/complete/date=*.json` marker of 764). S3 prefix: `opal-data-assets` / `schwab/08403355/silver/dim_balance/date=2026-10-16/`.
- (a) `08403355` is the **ONLY `0840` prefix** under `schwab/`. (b) `schwab/08403355/silver/` holds the four datasets with data at 2026-10-16: `dim_position` 1 object, `dim_balance` 1, `dim_asset` 1, `dim_transaction` 1 (objects per table, no values). (c) `prepare()` under `opal-gateway-access-admin` accepted the candidate and wrote nothing.
- Phase A ran on TRUNK code, where `OG-ms-1` already lists the master in `MASTERS`.

## 3. A fact the signers must read: the LIVE gateway does not know this master yet

The running gateway is the release before `OG-rz-2`'s batch15 and does not list `08403355` in its master registry. **A grant naming it would be rejected by the running code** (the strict scope parser), which would deny Alyssa's WHOLE Schwab access, not only the new master, until batch15 is live. That is why Phase B starts only after the batch15 ledger `nfra-oplgtw-gateway-resize-t4g-large` is CLOSED and the live marker is the batch15 sha; the activation is then harmless. **The reverse also holds:** rolling batch15 back after this activation would make the older code reject her grant, so the grant is reverted FIRST (the rollback below) before any tarball is redeployed.

## 4. Rollback

`revoke` of the new revision: a TOMBSTONE (status revoked at the next revision), never a delete. The previous revision's scope (grant revision 6, kept in the store) is the value to restore: it is re-activated as a new revision if she is to keep her two masters. `revoke` never touches the `email_deny` records.

## 5. The `email_deny` fact

Her `email_deny` record **already exists** (measured now: the store holds 1 `email_deny` record, hers), so the activation's idempotent put changes nothing. Andrew's record is not touched, because his grant is not.

## 6. process-wide state this change touches: none, read

I read `ops/schwab_entitlement_admin.py` (`prepare`, `activate`, `revoke`), `app/access_state.py` and `app/data_entitlement.py` (`decide`, `check_scope`, `allowed_tools`). The act writes DynamoDB items in the `POLICY#` partition (her profile, the new grant revision, an `operator_audit` append and the idempotent `email_deny` put) through one `operator_transact` under the operator role; it changes no process, logger, signal, environment, `sys.path`, IAM, Lambda, gateway code, allowlist or listener. A running gateway that knows the master reads the new grant on its next strong read.

## 7. Pre-flight measured in Phase A (nothing written)

- **decide() on the CANDIDATE** (the gateway's own function, in process, no network): it ADMITS `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset` and `schwab_query`, and REFUSES `schwab_prepare_download`; for a request naming `08403355` every read operation is in scope on every dataset and `download_filtered` is refused by the scope; and the same answers for each of her two existing masters are **unchanged** (`MS2_PREFLIGHT_DECIDE.json`: all true).
- comp-iam: `dynamodb:PutItem` and `dynamodb:UpdateItem` under `POLICY#*` read `allowed` for the operator role (`MS2_PREFLIGHT.md`).
- The approver is Andrew's word, quoted in `MS2_PREFLIGHT.md`; the mapping from "0840" to `08403355` is confirmed in section 2 (a).

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

Sign or refuse, on the counts of section 1, the method and confirmations of section 2, the order of acts of section 3 and the process-wide state line of section 6.

### COO half (`2.0.0_SA_COO~O`)

Sign or refuse on the same, and on the rollback of section 4 (including that it comes before any batch15 rollback).

### CVO half (`3.0.0_SA_CVO~Z`)

Sign or refuse on the same, including that only Alyssa's grant changes, only one master is added and her no-download rule stands.
