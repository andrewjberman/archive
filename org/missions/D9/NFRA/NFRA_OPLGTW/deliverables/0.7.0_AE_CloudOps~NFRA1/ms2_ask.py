#!/usr/bin/env python
"""OG-ms-2 Phase A: write W/MS2_PREFLIGHT.md and W/NEVER_WIDEN_ASK_OG-ms-2.md from the records. usage: python ms2_ask.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
J = lambda n: json.load(io.open(W + n, encoding="utf-8"))  # noqa: E731
b, d, p, f = J("MS2_BEFORE.json"), J("MS2_DIFF.json"), J("MS2_PREFLIGHT_DECIDE.json"), J("MS2_FACTS.json")
pr, den, al = b["principal"], b["denominator"], d["alyssa"]
m1, m2 = pr["masters"]
tabs = f["table_objects_at_latest_complete"]
V = {"t": b["read_at"], "pol": den["policy_items_scanned"], "allitems": den["all_items_scanned"], "prof": den["principal_profiles"], "pages": den["scan_pages"], "pk": pr["pk_hash"], "prev": pr["profile_revision"],
     "grev": pr["grant_revision"], "prev1": pr["profile_revision"] + 1, "grev1": pr["grant_revision"] + 1, "m1": m1, "m2": m2, "n1": pr["accounts_before"][m1], "n2": pr["accounts_before"][m2],
     "new": pr["new_master"], "nn": pr["new_master_accounts_current"], "date": pr["new_master_latest_complete_date"], "markers": f["completion_markers"], "nmaster": f["schwab_master_prefixes"],
     "tp": tabs["dim_position"], "tb": tabs["dim_balance"], "ta": tabs["dim_asset"], "tt": tabs["dim_transaction"], "put": f["simulate_principal_policy"]["dynamodb:PutItem"], "upd": f["simulate_principal_policy"]["dynamodb:UpdateItem"],
     "ndeny": f["email_deny_records_in_store"], "arev": f["andrew_grant_revision"]}

pre = """# OG-ms-2 Phase A -- preflight record (comp-iam, operator identity, approver)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Read at %(t)s. Counts, roles, keys and hashes only; no tid, oid, e-mail or account id is written here.

## Operator identity and comp-iam (re-simulated in Phase A)

- `sts:AssumeRole` into `opal-gateway-access-admin`: ASSUMED (the session ran `prepare()` under it; it wrote nothing).
- `simulate_principal_policy` on that role against `gateway-access-state-table`, with the `dynamodb:LeadingKeys` context `POLICY#*`: `dynamodb:PutItem` %(put)s, `dynamodb:UpdateItem` %(upd)s. Neither is implicitDeny.
- Strong reads of the store ran under the CALLING principal (a fully paginated `Scan`, %(pages)s pages, %(allitems)s items, %(pol)s `POLICY#` items, %(prof)s profiles).

## Role resolved

`alyssa` resolved in-process by the profile's e-mail prefix to EXACTLY ONE active `principal_profile` (pk_hash `%(pk)s`, profile revision %(prev)s, grant revision %(grev)s). Andrew's grant (revision %(arev)s) and every other profile are not touched.

## Approver and source authorization

Approver: `Andrew Berman`. Source record: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261019_195xZ_ALYSSA_SCHWAB_MASTER_0840_ADD_TO_ENTITLEMENTS.md`, relayed by `1.0.0_SA_CTO~Z` msg 36102 and sequenced by its ruling (B) msg 36104. Andrew's word, verbatim:

> we need to add 0840 to her search ability for schwab. she has the 0824 and 0833 accounts at schwab, the smartx and black diamond masters. she needs the 0840 master too added to her entitlements.

The record carries the mapping "0840" -> master `%(new)s` as INFERRED; Phase A confirms it against the bucket: `%(new)s` is the ONLY prefix beginning 0840 under `schwab/` (%(nmaster)s master prefixes in all).
""" % V
io.open(W + "MS2_PREFLIGHT.md", "w", encoding="utf-8", newline="\n").write(pre)

ask = """# NEVER-WIDEN ASK -- `OG-ms-2` -- add the Schwab master `%(new)s` ("0840") to ALYSSA's grant; ONLY `scope.masters` and `scope.accounts[%(new)s]` change

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ms-2.round-46-add-master-08403355-to-alyssas-schwab-grant.md` (GO for Phase A: msg 36116). Phase A writes NOTHING.
Read at %(t)s from the store with a strongly consistent, fully paginated scan (%(pol)s `POLICY#` items among %(allitems)s items). The record is named by role and `pk_hash` only; no account id, tid, oid or e-mail appears here.

## 1. What she gains (counts, from the diff)

- **One master:** `%(new)s`. Her grant today (profile revision %(prev)s, grant revision %(grev)s, pk_hash `%(pk)s`) names the masters `%(m1)s` and `%(m2)s`; the candidate (revisions %(prev1)s and %(grev1)s) names `%(m1)s`, `%(m2)s` and `%(new)s`.
- **Its accounts: %(nn)s** (the master's full CURRENT account set). The accounts of the two masters she already holds are **NOT touched** (%(n1)s and %(n2)s accounts before and after; `other_masters_accounts_unchanged` reads true in `MS2_DIFF.json`).
- **The same four datasets** her grant already names, **the same operations** (`list`, `describe`, `query`; her no-download rule stands, `download_filtered` is NOT granted), the same columns and the same rolling window. `changed_keys` of the candidate against the grant in force reads **`["accounts", "masters"]`** and nothing else.
- **ONE MASTER ONLY:** no other master, dataset, column, operation or date window is added, and no other principal is touched. Andrew's grant stays at revision %(arev)s (held by `OG-mg-2` option (b)); this order names Alyssa only.

## 2. The account set: method, date and prefix; what Phase A confirmed (read, not assumed)

- Method (the one `OG-mg-2` used and the CTO accepted): the distinct `account_id` values of the **`dim_balance`** table (one row per account) of the master at its latest complete date. Date: **%(date)s** (the newest `meta/complete/date=*.json` marker of %(markers)s). S3 prefix: `opal-data-assets` / `schwab/%(new)s/silver/dim_balance/date=%(date)s/`.
- (a) `%(new)s` is the **ONLY `0840` prefix** under `schwab/`. (b) `schwab/%(new)s/silver/` holds the four datasets with data at %(date)s: `dim_position` %(tp)s object, `dim_balance` %(tb)s, `dim_asset` %(ta)s, `dim_transaction` %(tt)s (objects per table, no values). (c) `prepare()` under `opal-gateway-access-admin` accepted the candidate and wrote nothing.
- Phase A ran on TRUNK code, where `OG-ms-1` already lists the master in `MASTERS`.

## 3. A fact the signers must read: the LIVE gateway does not know this master yet

The running gateway is the release before `OG-rz-2`'s batch15 and does not list `%(new)s` in its master registry. **A grant naming it would be rejected by the running code** (the strict scope parser), which would deny Alyssa's WHOLE Schwab access, not only the new master, until batch15 is live. That is why Phase B starts only after the batch15 ledger `nfra-oplgtw-gateway-resize-t4g-large` is CLOSED and the live marker is the batch15 sha; the activation is then harmless. **The reverse also holds:** rolling batch15 back after this activation would make the older code reject her grant, so the grant is reverted FIRST (the rollback below) before any tarball is redeployed.

## 4. Rollback

`revoke` of the new revision: a TOMBSTONE (status revoked at the next revision), never a delete. The previous revision's scope (grant revision %(grev)s, kept in the store) is the value to restore: it is re-activated as a new revision if she is to keep her two masters. `revoke` never touches the `email_deny` records.

## 5. The `email_deny` fact

Her `email_deny` record **already exists** (measured now: the store holds %(ndeny)s `email_deny` record, hers), so the activation's idempotent put changes nothing. Andrew's record is not touched, because his grant is not.

## 6. process-wide state this change touches: none, read

I read `ops/schwab_entitlement_admin.py` (`prepare`, `activate`, `revoke`), `app/access_state.py` and `app/data_entitlement.py` (`decide`, `check_scope`, `allowed_tools`). The act writes DynamoDB items in the `POLICY#` partition (her profile, the new grant revision, an `operator_audit` append and the idempotent `email_deny` put) through one `operator_transact` under the operator role; it changes no process, logger, signal, environment, `sys.path`, IAM, Lambda, gateway code, allowlist or listener. A running gateway that knows the master reads the new grant on its next strong read.

## 7. Pre-flight measured in Phase A (nothing written)

- **decide() on the CANDIDATE** (the gateway's own function, in process, no network): it ADMITS `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset` and `schwab_query`, and REFUSES `schwab_prepare_download`; for a request naming `%(new)s` every read operation is in scope on every dataset and `download_filtered` is refused by the scope; and the same answers for each of her two existing masters are **unchanged** (`MS2_PREFLIGHT_DECIDE.json`: all true).
- comp-iam: `dynamodb:PutItem` and `dynamodb:UpdateItem` under `POLICY#*` read `allowed` for the operator role (`MS2_PREFLIGHT.md`).
- The approver is Andrew's word, quoted in `MS2_PREFLIGHT.md`; the mapping from "0840" to `%(new)s` is confirmed in section 2 (a).

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

Sign or refuse, on the counts of section 1, the method and confirmations of section 2, the order of acts of section 3 and the process-wide state line of section 6.

### COO half (`2.0.0_SA_COO~O`)

Sign or refuse on the same, and on the rollback of section 4 (including that it comes before any batch15 rollback).

### CVO half (`3.0.0_SA_CVO~Z`)

Sign or refuse on the same, including that only Alyssa's grant changes, only one master is added and her no-download rule stands.
""" % V
io.open(W + "NEVER_WIDEN_ASK_OG-ms-2.md", "w", encoding="utf-8", newline="\n").write(ask)
print("wrote ask %d bytes sha256 %s; new master accounts %s" % (len(ask.encode()), hashlib.sha256(ask.encode()).hexdigest()[:12], V["nn"]))
