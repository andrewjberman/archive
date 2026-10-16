# NEVER-WIDEN ASK -- OG-mg-1: the two r30 grant writes, Andrew's profile and the Bloomberg mirror

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z`. From: `0.7.0_AE_CloudOps~Z`.
Phase A of `NFRA_OPLGTW.TO-OG-mg-1`, under amendments A1 (the IAM preflight), A2 (the deny-email
sources) and A3 (route (i): the `operations` branch is struck). **NO WRITE RAN.** `prepare()` writes
nothing and `activate()` was never called.

**RE-ISSUED 2026-10-16** (msg 34916) at the live release `3d5c9c8bf1`; the first issue was at `189bbbb8d2`
on r30. The COO half of 2026-10-14 refused because a restricted profile ended master_admin's access to
`blackdiamond_list_fees`. That ground is gone: `OG-bd-3` is live in `3d5c9c8bf1`, and section 1b shows it on
the live bytes. The store and the mirror were read again (section 0); nothing in them moved. **Any write
waits for all three halves to sign at THIS hash.**

Records: `MG1_BEFORE.json`, `MG1_PREFLIGHT.md`, `MG1_CANDIDATES.json`, `MG1_FEE_ACCESS.txt`. Instruments: `mg1_before.py`,
`mg1_candidates.py`. **No address appears in this file** -- identifiers live only in
`%LOCALAPPDATA%/opal/og-salt/mg1/`, asserted at run time to resolve outside the worktree, and the
repo carries each one's source, `sha256(lower(...))[:10]` and domain.

## 0. What is being asked, in one line each

**Sign or refuse R1 and R2, each on its own.** Both are CREATES. Both are built from the store's only
contract-maximal grant, with identity replaced and nothing else changed -- which is A3's route (i).

| record | principal | pk_hash | profile now | grant now | what it creates |
|---|---|---|---|---|---|
| **R1** | Andrew's master-admin | `a18b74486b` | **NONE** | **NONE** | profile revision 1, grant revision 1, `restricted` |
| **R2** | the Bloomberg concierge | `3c1d2597c9` | **NONE** | **NONE** | the same, the mirror |

Denominator for those "NONE"s, **read again 2026-10-16**: a strongly consistent, fully paginated scan --
**1714 items over 1 page, 17 POLICY# partitions, 4 `principal_profile`, 4 `data_entitlement`**. (The first
issue read 1510 items; the 17, the 4 and the 4 are unchanged, so the table grew in other partitions only.)
Exactly one profile is active and it is Alyssa's (`2c61471b14`, revision 4, grant_revision 4,
`restricted`), unchanged. The candidates were rebuilt: `prepare()` accepts R1, R2 and the struck-branch candidate (kept for the record), each
with `base_profile_revision` and `base_grant_revision` `None`, the template diff against Alyssa's
revision-4 scope changes **no key**, and R2's scope equals R1's with **zero** differing keys. DynamoDB's own
`ItemCount` was not used: it refreshes about every six hours and read 1493 against a live 1504.

## 1. What each record grants, and who gains what

**R1 -- Andrew's principal gains the Schwab data-grant family and the full approved width for 13
calendar months.** Concretely, the scope is Alyssa's revision-4 scope with identity replaced:
masters 2, datasets 4, accounts 2, columns 4, portal_channels 10, operations 4, and
`dates = {mode: rolling_complete_window, calendar_months: 13}`.

That width is **contract-maximal, not arbitrary**: `load_contract` approves exactly 2 masters
(`08242234`, `08335338`), 4 datasets (`dim_asset`, `dim_balance`, `dim_position`,
`dim_transaction`) and 4 operations (`describe`, `download_filtered`, `list`, `query`). R1 takes all
of each. There is no wider grant this contract admits, so R1 cannot be widened further without
changing the contract.

**Who gains:** Andrew's principal, from no profile and no grant at all, to the full approved width.
Under OG-pf-1 (live since r30; the r30 ledger `nfra-oplgtw-gateway-release-r30` is CLOSED) a `restricted`
profile confines only the data-grant family, so this grant is what admits the Schwab tools while leaving
every non-data tool to its own gate.

**R2 -- the Bloomberg concierge principal gains the same, as the mirror** (PRD v2.3 item 1,
Andrew-direct 2026-10-09). Measured: R2's scope is **equal to R1's with zero differing keys**,
identity aside. Its Teams surface stays under the Opal-users-only gate that OG-tg-1 shipped in r30,
which is the condition v2.3 item 4 sets -- item 2 ships with item 1 or neither ships. **That coupling
matters here:** r30 also unscopes that principal's tool set to Andrew's, so the Opal-users-only gate
is what bounds who can drive it. r30 is landed and its ledger CLOSED (2026-10-14T11:40:46Z), so the
condition that R2 not land before r30 is met.

## 1b. The master_admin caller's fee access is KEPT (the ground of the COO refusal, answered)

The refusal read: a restricted profile ended master_admin's access to `blackdiamond_list_fees`. At the
release the refusal was made against (r30, OG-bd-2) that was true: a profile confined a master_admin
exactly as it confines anyone, and the tier test applied only to an unprofiled principal. **`OG-bd-3`
(CTO ruling msg 33941, route (a)) changed it, and it is live in `3d5c9c8bf1`** (the data_entitlement
module's bytes on the host equal the release's: the OG-ap-23 md5 walk read 141 of 141). Read on those
bytes, offline, in `MG1_FEE_ACCESS.txt` (11 of 11 tests pass):

- **`test_ogbd3_ac01`:** a master_admin with an ACTIVE restricted profile whose grant does not name
  `blackdiamond_list_fees` is **allowed it**; with the profile REVOKED it is still allowed it and is still
  denied a non-tier tool. `tool_denial` and `visible_tools` agree.
- **`test_ogbd3_ac03`:** a profiled master_admin still needs the grant for a **Schwab** tool, so R1's
  grant is what admits Andrew to those, as section 1 says.
- **`test_ogad1_ac04`:** the same holds for the five `client_*` tools: with an active profile whose grant
  omits the tool, master_admin passes 5 of 5 and a standard employee is denied 5 of 5.
- **`test_ogbd3_ac02`:** a profiled principal at tier standard or unknown is denied the fee tool, so the
  tier, not the profile, is what keeps it.

**So R1 changes nothing about Andrew's fee access: it was admitted by tier before the write and is admitted
by tier after it.** R2 is not master_admin, so R2 holds no fee access before or after (an unprofiled
non-admin was already denied it since OG-bd-2); R2's profile adds the Schwab family only. The writer-count
claim of section 4 and the rollback of section 2 are unchanged.

**Who loses: nobody.** Neither record removes anything from anyone, and Alyssa's record is not read
for writing or touched -- AC2 checks it is unchanged.

## 2. The current value, and the rollback per record

**Current value: NONE, for both.** Neither principal holds a profile or a grant, so there is no prior
revision to restore and no prior scope to diff against. `prepare()` confirmed it on the live store:
`base_profile_revision` and `base_grant_revision` are both `None` for R1 and R2, which is why
`activate()` will compute revision 1 for each.

**Rollback per record: `revoke`, under the same operator role.** It writes a **tombstone, never a
delete** -- the module states "Never a DeleteItem", and the role holds no `dynamodb:DeleteItem`, so a
destructive rollback is not merely avoided by discipline but unavailable to this seat. Revocation
also deliberately **keeps** the `email_deny` records (ruled). So the rollback leaves a readable
history rather than restoring an absence, and that asymmetry is the thing to sign knowingly: after a
revoke the store shows "revoked at revision 1", not "never granted".

## 3. The measurement A3 asks for in place of the struck branch

A3 struck step 4's `operations` branch because it was vacuous, and asked instead: **where does PRD
v2.2 item 4's no-download rule actually live, and do R1 and R2 inherit it from being built from
Alyssa's record?**

**Measured answer: it does not live on her record at all, and there is nothing per-principal to
inherit. What IS in force from item 4 is a CONTRACT-level field prohibition that binds every
principal identically.** Four surfaces were checked and three are empty:

| candidate surface | measured |
|---|---|
| her `operations` field | `['describe', 'download_filtered', 'list', 'query']` -- `download_filtered` IS present, and that set is contract-maximal |
| a profile-level field on her record | her `principal_profile` carries exactly `status`, `revision`, `grant_revision`, `tid`, `oid`. **No such field** |
| the contract's `portal_only_schwab_tools` | **`[]`** -- empty, so no tool is portal-only |
| the contract's "hidden classes" | **IN FORCE**: `forbidden_field_classes` = `raw_account_id`, `account_title`, `tax_identifier`, `mailing_address`, `hidden_filter_operand`, `hidden_group_operand`, `hidden_sort_operand` |

The contract's other download keys are **transport** rules, not permissions:
`download_artifacts_per_ticket` 1, `download_metadata`, `download_ticket_transport`. They govern how
a download is delivered, never whether a principal may ask for one.

So the forbidden field classes are "never requestable by name", enforced in `validate_candidate`'s
own cross-check (`CandidateRejected` when a scope names one) -- at the **contract** level, uniformly.
**R1 and R2 are bound by them exactly as Alyssa is, and not because they were copied from her
record**: every candidate is validated against the same contract. Building them from her scope
neither adds nor removes that protection. The proof that her columns name none of those classes is
that `prepare()` ACCEPTED R1, which carries her column set unchanged.

**The consequence the halves should see plainly: there is no per-principal no-download restriction on
Alyssa to decline to copy.** If v2.2 item 4 was understood to confine her downloads specifically,
that reading is not what the store and the contract hold today. Naming it changes nothing here -- A3
asked for the outcome, not an act -- but it is the kind of belief that silently widens a later grant,
because "we copied the restricted template" would be read as carrying a restriction that is not
there.

## 4. The writer of the property: N = 1 module, read

**One module, one entry point, and it was read rather than assumed.** Every POLICY# write goes
through `ops/schwab_entitlement_admin.py` (`prepare` then `activate`, one
`access_state.operator_transact`). `activate()` (:377-394) builds
`ops = [profile_put_op(profile_item, base_profile_revision), grant_put_op(grant_item), audit_op]`
plus one deny put per alias -- **every member a Put**, with the optimistic staleness check riding the
Put's own `ConditionExpression`, not a separate `ConditionCheck` item.

The MC Portal grant writer (`mcportal-grant-writer-lambda`) imports the same module but refuses
without Andrew's verified owner token, so **this seat cannot drive that path**. No other path writes
a grant.

**Authorization, from the role's policy rather than the preflight's prose** (A1, after row
`Z-S103`): the role allows `dynamodb:GetItem` unconditioned and `dynamodb:PutItem` /
`dynamodb:UpdateItem` conditioned on `dynamodb:LeadingKeys = POLICY#*`. Every record written sits in
a `POLICY#<tid>#<oid>` partition, so the condition admits exactly these writes and would refuse a
non-POLICY# item in the same table. `dynamodb:TransactWriteItems` is **not an IAM action** --
`accessanalyzer validate-policy` returns `INVALID_ACTION` -- which is why simulating it read
`implicitDeny` and would have manufactured a STOP on this order's central write.

Three writes per record, one transaction: the `principal_profile`, the new `data_entitlement`
revision, and the `operator_audit` append, plus one `email_deny` put per alias. **Deny email count
measured: 1 per record.** Sources, per A2: R1's is the single alias in the live host
`MASTER_ADMIN_EMAILS` (exactly one, or STOP with a BLOCKING row), `sha10` `7b1bca22c9`, opalinvest.com
domain; R2's is the code-pinned Bloomberg identity named by `identity_scope`'s `OPAL_USERS_ONLY`,
`sha10` `f39c9b2025`, same domain.

## 5. The positive arm this enables (AC3)

After r30 **and** these two writes, `0.0.3_BG_BBGTerminal` re-runs its own capability exercise on the
**8** gateway data tools it previously measured DENIED -- `opal_discover`, `mdpf_get_aum_metrics`,
`mdpf_get_aggregate_aua`, `mdpf_get_account_distribution`, `mdpf_get_model_benchmarks`,
`etfs_get_positioning`, `gateway_query_catalog`, `ycharts_freshness` -- the same way it read them,
and should read **8 of 8 ALLOWED**.

That act is owed by `0.0.3_BG_BBGTerminal`, not by this seat, so AC3 is recorded
UNVERIFIABLE-BY-INSTRUMENT naming `3.0.0_SA_CVO~Z` and that act. **Denied after both is a BLOCKING
row, not a pass** -- which is the right asymmetry: this ask's whole point is that the grant is what
makes those 8 reachable, so a denial after both would mean the premise is wrong rather than the
exercise.

## 6. What Phase B will do on the GO, and its two refusal conditions

Only on the issuer's GO naming all three halves signed at this hash. OG-ap-14's ledger
`nfra-oplgtw-gateway-release-r30` is already CLOSED, so the writes are no longer inert-before-served. The
operator role's policy was re-read on 2026-10-16 and is as `MG1_PREFLIGHT.md` records it (two inline
policies, no attached ones; `GetItem` unconditioned; `PutItem` and `UpdateItem` conditioned on
`LeadingKeys` `POLICY#*`); the 2026-10-14 simulations were not re-run. Ledger
`nfra-oplgtw-r30-grant-writes`, entry and sentinel first; `activate()` under the operator role with
`--approver` and `--source-authorization` naming the preflight's records; then a live read-back of
both, and the mirror check that R2's scope equals R1's.

**Two conditions refuse rather than proceed**, both already exercised in Phase A: a deny-email source
that resolves to anything other than exactly one value is a STOP with a BLOCKING row (A2); and a
STALE base -- the record moved or came into existence between `prepare()` and `activate()` --
raises `acs.ConditionFailed` and writes nothing, by the optimistic condition rather than by my
checking.
