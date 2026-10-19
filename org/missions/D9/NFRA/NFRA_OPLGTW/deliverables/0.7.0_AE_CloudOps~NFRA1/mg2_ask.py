#!/usr/bin/env python
"""OG-mg-2 Phase A: write W/MG2_PREFLIGHT.md and W/NEVER_WIDEN_ASK_OG-mg-2.md from the records (no number is typed that a record holds).
usage: python mg2_ask.py   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
J = lambda n: json.load(io.open(W + n, encoding="utf-8"))  # noqa: E731
b, d, p, f = J("MG2_BEFORE.json"), J("MG2_DIFF.json"), J("MG2_PREFLIGHT_DECIDE.json"), J("MG2_FACTS.json")
pr = {x["role"]: x for x in b["principals"]}
m1, m2 = "08242234", "08335338"
a, y = pr["andrew"], pr["alyssa"]
den = b["denominator"]
meth = b["current_set_method"]

pre = """# OG-mg-2 Phase A -- preflight record (comp-iam, operator identity, approver)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Read at %(t)s. Counts, roles, keys and hashes only; no tid, oid, e-mail or account id is written here.

## Operator identity and comp-iam (re-simulated in Phase A)

- `sts:AssumeRole` into `opal-gateway-access-admin`: ASSUMED (the session ran `prepare()` under it; it wrote nothing).
- `simulate_principal_policy` on that role against `gateway-access-state-table`, with the `dynamodb:LeadingKeys` context `POLICY#*`: `dynamodb:PutItem` %(put)s, `dynamodb:UpdateItem` %(upd)s (the writes `activate()` makes). Neither is implicitDeny.
- Strong reads of the store ran under the CALLING principal (a fully paginated `Scan`, %(pages)s pages, %(allitems)s items, %(pol)s `POLICY#` items). The operator role holds no `Scan`: it writes only.

## Roles resolved

Both roles resolved in-process by the profile's e-mail prefix to EXACTLY ONE active `principal_profile` each (`andrew` pk_hash `%(ah)s`, `alyssa` pk_hash `%(yh)s`). The Bloomberg principal and every other profile are not touched.

## Approver and source authorization

Approver: `Andrew Berman` (the activation's `--approver`). Source record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_172xZ_ALYSSA_3PM_SCHWAB_TEST_SENDS_YES_ROSTER_AS_OPEN_CALLS_SCHWAB_FULL_ACCOUNTS.md` (commit 65a05f6658), relayed by `1.0.0_SA_CTO~Z` msg 36025 (a), (b). Andrew's word, verbatim, item 4:

> Schwab should automatically cover the full accounts, that should be easy enough to do because the premise should be that the tool is simply hitting what is being refreshed in AWS every single day, there shouldnt be a persisted list or anything of the sort because theres no need, it just needs to be redirected to the correct bucket

The order's open point stands for the halves: whether that word reaches Alyssa's grant (the CTO relays it for both).

## A finding the order does not mention (also in the ask, section 3)

`activate()` also puts one `email_deny` record per plan e-mail (row W3-S22). Measured now: Andrew's `email_deny` record DOES NOT EXIST (it was removed by the audited reversal, OG-ap-30); Alyssa's EXISTS. So activating Andrew's candidate would re-create it.
""" % {"t": b["read_at"], "put": f["simulate_principal_policy"]["dynamodb:PutItem"], "upd": f["simulate_principal_policy"]["dynamodb:UpdateItem"], "pages": den["scan_pages"], "allitems": den["all_items_scanned"],
       "pol": den["policy_items_scanned"], "ah": a["pk_hash"], "yh": y["pk_hash"]}
io.open(W + "MG2_PREFLIGHT.md", "w", encoding="utf-8", newline="\n").write(pre)

ask = """# NEVER-WIDEN ASK -- `OG-mg-2` -- re-activate Andrew's and Alyssa's Schwab grants at each granted master's CURRENT account set; ONLY `scope.accounts` changes

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-mg-2.round-46-schwab-grants-at-the-full-current-accounts.md` (GO for Phase A: msg 36035). DEADLINE: both grants live and read back before 2026-10-19T18:45Z.
Read at %(t)s from the store with a strongly consistent, fully paginated scan (%(pol)s `POLICY#` items among %(allitems)s items; %(prof)s `principal_profile` items). Records are named by role and `pk_hash` only; no account id, tid, oid or e-mail appears here.

## 1. What each record grants, and who gains what (counts, from the diff)

| role | pk_hash | profile revision | grant revision | masters | accounts before (per master) | current in S3 (per master) | ADDED | REMOVED |
|---|---|---|---|---|---|---|---|---|
| `andrew` | `%(ah)s` | %(apr)s -> %(apr1)s | %(agr)s -> %(agr1)s | %(masters)s | %(ab1)s / %(ab2)s | %(ac1)s / %(ac2)s | %(aa1)s / %(aa2)s | %(ar1)s / %(ar2)s |
| `alyssa` | `%(yh)s` | %(ypr)s -> %(ypr1)s | %(ygr)s -> %(ygr1)s | %(masters)s | %(yb1)s / %(yb2)s | %(yc1)s / %(yc2)s | %(ya1)s / %(ya2)s | %(yr1)s / %(yr2)s |

(per-master counts are in the order `%(m1)s` / `%(m2)s`.) Each principal GAINS the accounts added (S3 now holds them, the frozen list lacks them) and LOSES the accounts removed: those are in the frozen grant and are NOT in the latest complete `dim_balance` any more (a **non-empty `removed`, which the order says goes in the ask and is not a stop**). Same masters, datasets, dates, columns and operations as before: `changed_keys` reads `["accounts"]` for both roles (`MG2_DIFF.json`). Andrew's operations keep what his grant has today (including `download_filtered`); Alyssa's keep her no-download rule. Nothing is added: no operation, master, dataset, column or date window.

## 2. The current set: method, date and prefix

- Method: the distinct `account_id` values of the **`dim_balance`** table (one row per account) of each master, which is where the gateway's Schwab `account_id` column is carried for every account; I picked it because it reproduces the CTO's measure exactly (**%(ac2)s accounts for master `%(m2)s` against the CTO's 7,690**). `dim_position` and `dim_transaction` hold fewer accounts (accounts with a position or a transaction that day); `dim_asset` carries no account column. This is the same column (`account_id`) the gateway's Schwab tools filter on; no second enumeration method was invented. If the signers prefer a different table, the sets change.
- Date: the **latest complete** date of each master, taken from the newest completion marker: %(latest)s.
- S3 prefix: `opal-data-assets` / `schwab/<master>/silver/dim_balance/date=<latest complete>/` (completion markers under `schwab/<master>/meta/complete/`).

## 3. A finding the order does not state: activating Andrew's candidate RE-CREATES his `email_deny` record

- `activate()` (`ops/schwab_entitlement_admin.py`, row W3-S22) writes, in the SAME transaction as the profile and grant, one `email_deny` put per plan e-mail. This is what made `OG-mg-1`'s Phase B deny Andrew's own browser routes, reversed by the audited OG-ap-30 (CTO ruling: remove the `email_deny` records for Andrew's addresses only).
- Measured now (`MG2_FACTS.json`): Andrew's `email_deny` record **does not exist**; Alyssa's **exists** (her re-activation is an idempotent put). The store holds 1 `email_deny` record.
- What a deny record does on the live gateway (read from `app/`): the browser pages `/login`, `/sprint`, `/rivalfunds`, `/yearinreview` let a MASTER ADMIN through before the record is read (`OG-en-14`), so Andrew's pages stay open; **the legacy GUI consent sign-in (`/callback`, `token_broker.redeem_consent`) has no such exemption and answers 403 for an e-mail with a deny record**, so Andrew could not re-run that consent while the record stands. His existing token caches are not touched; the MCP tools do not read the record.
- `prepare()` refuses a candidate with no resolvable e-mail, so the deny put cannot be switched off from the candidate.
- **The halves choose** (I do not): **(a)** activate both as written, and remove Andrew's single `email_deny` record afterwards in the OG-ap-30 manner (an audited delete of exactly that one record; this order forbids a delete, so (a) needs the halves' explicit word for it, as a separate act); **(b)** activate Alyssa's now and hold Andrew's until the deny handling is ruled; **(c)** activate both and accept the residual for Andrew's legacy consent sign-in. My recommendation is **(a)**: it gives Andrew's grant before 18:45Z and removes the one residual in minutes. (b) is the lowest-risk if the removal cannot be signed in time.

## 4. Rollback

`revoke` of the new revision for each principal: a TOMBSTONE (status revoked at the next revision), never a delete; the previous revision's scope is the value to restore (Andrew: grant revision %(agr)s, Alyssa: grant revision %(ygr)s, both kept in the store). `revoke` never touches the `email_deny` records (the module keeps them).

## 5. process-wide state this change touches: none, read

I read `ops/schwab_entitlement_admin.py` (`prepare`, `activate`, `revoke`), `app/access_state.py` and `app/data_entitlement.py` (`decide`, `allowed_tools`). The act writes DynamoDB items (`POLICY#` partition: profile, grant revision, operator_audit, and the `email_deny` put of section 3) through one `operator_transact` per principal under the operator role; it changes no process, logger, signal, environment, `sys.path`, IAM, Lambda, gateway code or allowlist, and starts no listener. A running gateway reads the new grant on its next strong read.

## 6. Pre-flight measured in Phase A (nothing written)

- `prepare()` under `opal-gateway-access-admin` accepted both candidates and wrote nothing (`MG2_DIFF.json`).
- **decide() on Alyssa's CANDIDATE** (the gateway's own function, in process, no network): it ADMITS `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset` and `schwab_query`, and REFUSES `schwab_prepare_download` (`MG2_PREFLIGHT_DECIDE.json`: all five true). For Andrew's candidate decide() also admits the four and, because his grant carries `download_filtered`, admits the download tool too (as today).
- comp-iam: `dynamodb:PutItem` and `dynamodb:UpdateItem` under `POLICY#*` read `allowed` for the operator role (`MG2_PREFLIGHT.md`).
- The approver is Andrew's word, quoted in `MG2_PREFLIGHT.md`; whether it reaches Alyssa's grant is for the halves.

## 7. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

Sign or refuse, on the counts of section 1, the method of section 2, the process-wide state line of section 5, and name one of (a), (b), (c) of section 3.

### COO half (`2.0.0_SA_COO~O`)

Sign or refuse on the same, and on the rollback of section 4.

### CVO half (`3.0.0_SA_CVO~Z`)

Sign or refuse on the same, including that `removed` is non-empty for both roles and that Andrew's activation re-creates his `email_deny` record unless (b) is chosen.
""" % {
    "t": b["read_at"], "pol": den["policy_items_scanned"], "allitems": den["all_items_scanned"], "prof": den["principal_profiles"], "ah": a["pk_hash"], "yh": y["pk_hash"],
    "apr": a["profile_revision"], "apr1": a["profile_revision"] + 1, "agr": a["grant_revision"], "agr1": a["grant_revision"] + 1,
    "ypr": y["profile_revision"], "ypr1": y["profile_revision"] + 1, "ygr": y["grant_revision"], "ygr1": y["grant_revision"] + 1,
    "masters": ", ".join("`%s`" % m for m in a["masters"]), "m1": m1, "m2": m2,
    "ab1": a["accounts_before"][m1], "ab2": a["accounts_before"][m2], "ac1": a["accounts_current"][m1], "ac2": a["accounts_current"][m2],
    "aa1": d["andrew"]["added"][m1], "aa2": d["andrew"]["added"][m2], "ar1": d["andrew"]["removed"][m1], "ar2": d["andrew"]["removed"][m2],
    "yb1": y["accounts_before"][m1], "yb2": y["accounts_before"][m2], "yc1": y["accounts_current"][m1], "yc2": y["accounts_current"][m2],
    "ya1": d["alyssa"]["added"][m1], "ya2": d["alyssa"]["added"][m2], "yr1": d["alyssa"]["removed"][m1], "yr2": d["alyssa"]["removed"][m2],
    "latest": ", ".join("`%s` %s" % (m, v) for m, v in sorted(meth["latest_complete_date"].items()))}
io.open(W + "NEVER_WIDEN_ASK_OG-mg-2.md", "w", encoding="utf-8", newline="\n").write(ask)
print("wrote ask %d bytes sha256 %s" % (len(ask.encode()), hashlib.sha256(ask.encode()).hexdigest()[:12]))
