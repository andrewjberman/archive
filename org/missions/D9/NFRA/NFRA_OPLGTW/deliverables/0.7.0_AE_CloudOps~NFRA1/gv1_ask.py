#!/usr/bin/env python
"""OG-gv-1 Phase A: write W/NEVER_WIDEN_ASK_OG-gv-1.md from the records. usage: python gv1_ask.py   (repository root, after gv1_phasea.py)"""
from __future__ import annotations

import io
import json

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
b = json.load(io.open(W + "GV1_BEFORE.json", encoding="utf-8"))
d = json.load(io.open(W + "GV1_DIFF.json", encoding="utf-8"))["andrew"]
p = json.load(io.open(W + "GV1_PREFLIGHT_DECIDE.json", encoding="utf-8"))["andrew"]
n = json.load(io.open(W + "GV1_DENY.json", encoding="utf-8"))
pr = b["principal"]
counts = pr["accounts_before_counts"]
masters = sorted(counts)
opts = "\n".join("%d. %s" % (i + 1, o) for i, o in enumerate(n["options"]))
ask = """# NEVER-WIDEN ASK -- `OG-gv-1` -- Andrew's own Schwab grant moves from its HELD stored account lists to the MASTER-WIDE scope (`accounts[master] = ["*"]` for each of his two masters); ONE record, ONE new revision; only `accounts` changes; his download operation is UNCHANGED

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-gv-1.round-47-andrews-schwab-grant-moves-to-the-master-wide-scope.md` (GO for Phase A: msg 36187; amended per the issuer's ruling on row Z-S431, msg 36199). Source: the CTO's round-46 analysis rank 6 ("then Andrew's own grant moves to it"), and Andrew-direct 2026-10-19 ~17:2xZ ("Schwab should automatically cover the full accounts ... there shouldn't be a persisted list"; record `ANDREW_DIRECT_20261019_172xZ_ALYSSA_3PM_SCHWAB_TEST_SENDS_YES_ROSTER_AS_OPEN_CALLS_SCHWAB_FULL_ACCOUNTS.md` @65a05f6658).
**Phase A writes NOTHING and activates nothing in any form.** `prepare()` ran in process on trunk's `ops/schwab_entitlement_admin.py` (it writes nothing); `decide()` ran in process on trunk code. Read %(read_at)s from the store with a strongly consistent, fully paginated scan (%(pol)d `POLICY#` items). The principal is named by role and `pk_hash` (`%(pkh)s`) only; no account id, tid, oid or e-mail appears here or in any record.
Records: `W/GV1_BEFORE.json`, `W/GV1_DIFF.json`, `W/GV1_PREFLIGHT_DECIDE.json`, `W/GV1_DENY.json`, `W/gv1_phasea.py`, `W/gv1_ask.py`; the candidate (which holds the tid and oid) is off-repo.

## 1. The diff

His active grant (profile revision %(prev)d, grant revision %(grev)d, the held revision of `OG-mg-2` option (b)) has a STORED account list per master (%(c1)d accounts under `%(m1)s`, %(c2)d under `%(m2)s`). The NEW revision keeps his `masters` (the same two), `datasets`, `columns`, `dates` and `operations` byte-equal and replaces ONLY `accounts`: for each master, `["*"]`. `changed_keys` of the candidate against the grant in force read `%(keys)s`; the rest of his scope (everything except `accounts` and `masters`) hashes the same before and after (`rest_of_scope_matches_template` %(rest)s). `prepare()` accepted the candidate. Nothing is added: no master, no dataset, no operation, no column, no date window.
**His download operation is unchanged.** His held scope carries `download_filtered` (stored operations include it: %(sdl)s); `decide()` on the candidate leaves `schwab_prepare_download` exactly as his stored operations say (admitted before and after: %(adm)s), because only `accounts` changes and this order does not narrow his operations (the issuer's ruling on row Z-S431).

## 2. The widening, stated plainly

The principal's reach grows from the stored account list to EVERY CURRENT ACCOUNT of each master he already holds, and to accounts created later, with no grant write: `["*"]` is resolved at read time by `OG-rt-1`'s code (the account set is read from the master's silver data on each call, never stored). No new master (`08403355` was Andrew's word for Alyssa alone), no new dataset, no new operation. His tools stay the same: `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query` admitted on the candidate (`decide()` pre-flight, in process), and `schwab_prepare_download` as before. The master-wide helper builds its own `dim_position` policy check, so a master-wide grant that lacks `dim_position` is refused fail-closed; his datasets include it (ruled in `OG-rl-18`'s ask).

## 3. The release-order condition

**`OG-rl-18` (ledger `nfra-oplgtw-gateway-release-batch17`) must be CLOSED and live on the host before the activation:** an OLD gateway reads a stored sentinel `["*"]` as `Malformed` and would deny the principal's WHOLE Schwab access. Phase B starts only when the live marker on the host equals `OG-rl-18`'s release sha. A batch17 rollback after the activation reverts THIS grant FIRST (section 6).

## 4. The `email_deny` finding (facts; the CTO half names the handling)

- Present now: %(dpresent)s. `activate()` writes (or re-writes) one `email_deny` record per plan e-mail: %(dwrites)s (%(demails)d e-mail in the plan).
- Effect: %(effect)s
- Options, none a delete:
%(opts)s
- **Request: the CTO half names the handling (an option above, or another that is not a delete).** The order forbids a delete of any kind; Phase B handles the record exactly as the CTO half names.

## 5. Order of acts (Phase B, on a GO that names all three halves signed, `OG-rl-18` CLOSED and the live marker equal to its release)

1. Ledger `nfra-oplgtw-gv1-andrew-masterwide`, entry AND sentinel first; print the live marker and Andrew's grant revision (a revision different from the before-record re-cuts Phase A once).
2. `activate` for the one record under `opal-gateway-access-admin`, `--approver "Andrew Berman"`, with the `email_deny` handling as named.
3. Read back against the DEPLOYED tree: `decide()` on his LIVE grant in a guarded fresh process (admits the four read tools; `prepare_download` as his stored operations say); as Andrew through the served gateway, `schwab_get_access` reports `account_count` `"all"` per master and ONE bounded `schwab_query` answers at least one row.
4. Close the ledger, proof instance, `gv1.AC2`, report, send the COO the CLOSED time.

## 6. Both branches and rollback

- **Read-back passes:** the grant stands. **Read-back fails** (any decision differs, or the served read does not answer): `revoke` the new revision (a tombstone, never a delete), re-activate the held revision-1 scope as a NEW revision at once, close the ledger ROLLED BACK, tell the COO the same turn.
- **Rollback of `OG-rl-18` after this activation:** revoke this revision and re-activate the held revision-1 scope FIRST, then roll the release back; otherwise the older gateway denies his whole Schwab access.

## 7. Triggers

The live marker not equal to `OG-rl-18`'s release sha; his grant revision different from the before-record; `prepare()` refusing the candidate; `decide()` on the live grant differing from this ask's pre-flight (any of the four tools refused, `prepare_download` changed); `schwab_get_access` not reporting `"all"`; the bounded `schwab_query` answering no row; any write to a principal other than his.

## 8. Gate lines

process-wide state this change touches: none (one grant record; no process, logger, signal, environment or global config), read.

I read `ops/schwab_entitlement_admin.py` (`prepare`, `activate`, `_deny_put_op`), `app/data_entitlement.py` (`decide`, the master-wide parser, `email_denial`), `app/token_broker.py`'s `EmailDenied` and the legacy `/callback` branch, and `OG-mg-2`'s records. No code, IAM, Terraform, deploy or env change.

## 9. The three halves (sign ONCE, on this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed with the widening (section 2), the `email_deny` finding and the handling it names (section 4), and the release-order condition (section 3) read.

### COO half (`2.0.0_SA_COO~O`)

To be signed with the diff (section 1), the order of acts and rollback (sections 5 and 6) and the triggers (section 7) read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed with the process-wide state line (the verdict 35844; section 8), the widening (section 2) and the statement that his download operation is unchanged (section 1) read.
""" % {
    "read_at": b["read_at"], "pol": b["denominator"]["policy_items_scanned"], "pkh": pr["pk_hash"], "prev": pr["profile_revision"], "grev": pr["grant_revision"], "c1": counts[masters[0]], "m1": masters[0], "c2": counts[masters[1]], "m2": masters[1],
    "keys": d["changed_keys"], "rest": d["rest_of_scope_matches_template"], "sdl": p["download"]["stored_operations_include_download_filtered"], "adm": p["download"]["prepare_download_admitted"],
    "dpresent": n["deny_record_present_before"], "dwrites": n["activate_writes_deny"], "demails": n["deny_emails_in_plan"], "effect": n["effect"], "opts": opts}
io.open(W + "NEVER_WIDEN_ASK_OG-gv-1.md", "w", encoding="utf-8", newline="\n").write(ask)
print("wrote the ask, %d bytes" % len(ask.encode("utf-8")))
