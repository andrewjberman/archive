# G-C evidence -- the controlled identity's verified tid/oid and its one approved synthetic grant

**Order:** `NFRA_OPLGTW.TO-OG-g-1` | **Cell:** `OG-g-1` | **Gate:** `G-C` (decomposition s.6; ADDENDUM R2-E.3)
**Seat:** `0.7.0_AE_CloudOps~OG` (the identity administrator, Andrew-direct 2026-09-20 ~18:0xZ, record @`768e6df290`)
**Branch:** `ae-og-g1` cut from `CLOUD` @`6d1a12f475` | **PRD:** v1.1 @`c80b5c85b6` | **Contract:** v1.3
**Written:** 2026-09-29

> ⛔ **THIS FILE DOES NOT CLOSE `G-C`.** It is the evidence `1.0.0_SA_CTO~O` writes the gate record from.
> ⛔ **THE IDENTITY HALF OF `G-C` IS BLOCKED ON A TENANT-ADMINISTRATOR ACT.** No controlled identity exists
> in the Opal Capital tenant, and this order's own clause forbids improvising one. The grant half is derived,
> bounded and validated as far as an absent principal allows. **No live write was performed**, so no
> deploy-ledger entry was opened. The precise human ask is section 6.

---

## 1. The controlled identity -- ABSENT, and why

- **controlled_tid:** `6810043e-d171-4adc-9975-068b35e179da`
- **controlled_oid:** `<<ABSENT -- no controlled identity exists in the tenant; see section 2>>`
- **controlled_upn:** `<<ABSENT -- no controlled identity exists in the tenant; see section 2>>`
- **instrument:** `az account list` and `az ad user list` / `az ad user show` (Azure CLI against Microsoft Entra, tenant Opal Capital), run 2026-09-29 under the operator's signed-in Azure session

The **tenant** half is verified and is a canonical GUID. The **principal** half does not exist to be read.
`controlled_tid` alone is not an identity: the Gateway's principal key is `(tid, oid)` together
(`org/standards/NFRA_OPLGTW_CONTRACT.json` `principal_key`), so `GCG1-AC1` FAILS on the absent `oid`, correctly.

### INSTRUMENT OUTPUT, VERBATIM

```
$ az account list --output json
[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "6810043e-d171-4adc-9975-068b35e179da",
    "id": "1e594a38-9247-4744-a33d-eb2b29dd64e6",
    "isDefault": true,
    "name": "Opal Capital",
    "state": "Enabled",
    "tenantDefaultDomain": "opalinvest.com",
    "tenantDisplayName": "Opal Capital",
    "tenantId": "6810043e-d171-4adc-9975-068b35e179da",
    "user": { "name": "Andrew@opalinvest.com", "type": "user" }
  }
]
```

---

## 2. Why no identity in this tenant qualifies -- by subtraction from a printed denominator

`az ad user list` returned **85 user objects**: **47** external guests (`#EXT#`) and **38** internal. Rule 24(i)
subtraction over the 38 internal accounts, against this order's three prohibitions (never a master-admin address,
never Andrew's own account, never a real person's account) and `GCG1-AC2` (no match on either live roster):

| class | count | disposition |
|---|---|---|
| real named employees (Adam, AJ, Alyssa, Andrew, Austin, bobby, Chris, Craig, Jai, Jay, Jeanette, Jim, Keith, Lauren, Manav, menachem, Toni, Wade, Wayne, William, Yang) | 21 | **REFUSED** -- a real person's account. `Andrew@` is additionally the sole `MASTER_ADMIN_EMAILS` entry; `Alyssa@` is on `WRITE_CAPABLE_EMAILS`; `menachem@` is the **pilot** identity reserved for `G-E`, not the controlled one |
| admin / break-glass (`AzureAdmin@`, `LDTAdmin@`, `PurviewAccess@`, `breakglass@`) | 4 | **REFUSED** -- privileged by construction; the walkthrough must exercise refusal paths |
| live shared business mailboxes (`billing@`, `info@`, `operations@`, `trading@`, `Analytics@`, `Cottonwood@`, `info@pathfinderetfs.com`) | 7 | **REFUSED** -- real operational mailboxes real staff sign into; granting Schwab data to one is a live access decision, not a test fixture |
| room / resource objects (`ConferenceRoom@`, `CONFERENCEROOM2@`, `ConferenceRoom1@`) | 3 | **REFUSED** -- cannot perform A1's interactive work-account sign-in |
| `opalbloomberg@` | 1 | **REFUSED** -- on `WRITE_CAPABLE_EMAILS`; `GCG1-AC2` grades a match either way a FAIL |
| security/system (`report-phishing-checkpoint@`, `G476b089da38b4adb9f6e9740a7528923@`) | 2 | **REFUSED** -- not a usable interactive principal |
| **purpose-built controlled / test principal** | **0** | **the uncovered member: it does not exist** |

38 of 38 accounted for; **0 qualify**.

**The UI walker is not a candidate, for a structural reason.** `/ui-walk`'s dormant account is
`opal-ui-walker@opal.test` in the portal's own `opal-users-v2` DynamoDB store
(`.claude/skills/ui-walk/SKILL.md:29`). It is not an Entra principal and has no `tid`/`oid` at all, so it cannot
key a Gateway principal. Different identity plane, not a narrower one.

**Creating one is outside this order.** This order's authorized live write is exactly one principal's `POLICY#`
records in AWS and "⛔ NOTHING ELSE IN AWS"; it authorizes no Entra write at all. A new tenant identity is an
outward-facing, licence-consuming directory object. Per the order's own clause, that is the answer.

### What the live table says, and why it does not help

A strong scan of `POLICY#` (10 items, `ScannedCount` 213, no `LastEvaluatedKey`, so complete) holds **4 distinct
principals**: 3 are `probe-og-i1-*` test keys from `OG-i-1`'s probe, and exactly **1** is a real Entra-keyed
principal -- `POLICY#6810043e-d171-4adc-9975-068b35e179da#ad037ea5-fee8-412e-9da9-15c6cf2a4fbc`. That `oid`
resolves through `az ad user list` to **`Alyssa@opalinvest.com`**, who is on the deployed `WRITE_CAPABLE_EMAILS`.
Her profile is `profile_kind restricted`, `status active`, `grant_revision 1`, and her grant is **portal-only**
(`portal_channels` of 10 channels; `masters`, `datasets`, `columns` all empty; `operations` `["query"]`) from
project `NFRA_OPALAI` cell `OA-g-3`, approved by `andrew@opalinvest.com` 2026-09-27T00:48:46Z.

Three consequences: **no Schwab data grant exists for anyone**; the one real principal is a privileged real
employee, so `GCG1-AC2` would FAIL on her; and the order forbids widening an existing grant. She is not reusable.

---

## 3. The privilege rosters, read from the DEPLOYED host (not from the deploy script)

Read on `i-07dccb1615503ac99` (`opal-gateway`, running, `opal-gateway.service` **active**) from
`/opt/opal-gateway/.env`, 27 keys total, via SSM. Only the roster keys were extracted; the secret-bearing lines in
that file were never read. Positive control `AWS_REGION=us-east-1` returned, so an empty roster would be a real
empty and not a failed read.

| key | deployed value | entries |
|---|---|---|
| `MASTER_ADMIN_EMAILS` | `andrew@opalinvest.com` | 1 |
| `WRITE_CAPABLE_EMAILS` | `alyssa@opalinvest.com,opalbloomberg@opalinvest.com` | 2 |
| `MASTER_ADMIN_PRINCIPALS` | `<<ABSENT FROM DEPLOYED ENV>>` | 0 |
| `WRITE_CAPABLE_PRINCIPALS` | `<<ABSENT FROM DEPLOYED ENV>>` | 0 |

**Denominator: 3 roster entries across 2 present rosters.** The two `*_PRINCIPALS` rosters are absent, which
**confirms row `NFRA_OPLGTW-S61` on the live plane**: `OG-t-1` re-keyed the person tier on `tid`/`oid` in code
(@`3c58463f8c`) but its release `OG-t-2` is held, so the deployed gateway still decides the person tier by exact
email match. A controlled identity whose address landed on either roster would be privileged today regardless of
its grant -- which is why `GCG1-AC2` reads the deployed rosters and not the Terraform or the deploy script.

`ENABLED_INTEGRATIONS` reads `ycharts opal_portal globgrph opal_discover portal_index` -- **`schwab` is absent**,
so the switch is OFF exactly as the order states. A grant written now serves nobody, which is what makes writing
it first safe.

---

## 4. The grant -- derived line by line, narrowest that serves the walkthrough

Recorded as data in `grant_candidate_scope.json` beside this file. Derivation, per dimension:

### masters -- `08242234`, `08335338`
From `SEALED_EXPECTED_V2.json` at HEAD: `08335338` is named by RQ2-1, -2, -3, -5, -6, -7; `08242234` by RQ2-4
and RQ2-6. Both are required; the contract admits only these two.

### datasets -- `dim_balance`, `dim_position`, `dim_asset`
`dim_balance` by RQ2-2 .. RQ2-6; `dim_position` by RQ2-1 and RQ2-7; `dim_asset` by the order's named describe
journey. All three of the contract's datasets, and each is load-bearing.

> **`dim_position` must be INSIDE the grant even though RQ2-1 and RQ2-7 expect a refusal.** Both carry
> `expected_class C3_REFUSAL` in the seal, because the declared source grain collides on the date asked
> (`duplicate_source_grain` / `paging_refused_no_unique_grain`, protocol s.4). If `dim_position` were outside the
> grant the refusal would be a *grant* denial, and the walkthrough would pass for the wrong reason -- the exact
> failure the order warns against. The grant must admit the request so the C3 rules under test produce the refusal.

### dates -- `fixed_dates`, exactly `2026-09-24` and `2026-09-25`
Every sealed question names literal `2026-09-25`; RQ2-4 and RQ2-5 also name `2026-09-24`. The seal's own dates
block is `D_NEW = 2026-09-25`, `D_PREV = 2026-09-24`. Ruling R-OG-12 fixed these as literals *"so a newer
qualified closure at ask time does not change what was sealed"*.

`fixed_dates` is chosen over `rolling_complete_window` for two measured reasons:

1. **It is narrower.** `rolling_complete_window` is the latest qualified date and the previous 29 calendar days
   (`data_entitlement.py:74` `ROLLING_WINDOW_DAYS = 30`) -- roughly 30 dates where 2 are needed.
2. **It preserves the date-dimension refusal.** A qualified closure marker exists for `2026-09-23` (measured: 19
   markers per master), so under `fixed_dates` a request for that real date is refused as outside the grant. Under
   a rolling window it would be granted and that discriminator would not exist.

**A7 step 4's no-date ask is inside a `fixed_dates` grant -- measured, not assumed.** `check_scope`
(`data_entitlement.py:482`) documents that *"an omitted optional dimension means 'the granted set'"*, and its date
limb runs only `if dates is not None`. A request carrying no business date therefore skips the date check entirely.

> ⚠ **NAMED RESIDUAL RISK, not a grant defect.** The newest qualified marker for both masters is today
> `date=2026-09-25` (19 markers each; nothing later exists), so A7 step 4's expected observation -- *"a latest
> qualified date equal to the newest qualified closure marker for that master at ask time"* -- holds right now. The
> last marker landed 2026-09-26 and the producer writes daily (~10:16Z / ~09:46Z), so a marker for a later business
> date is likely to land before the walkthrough runs. Under a `fixed_dates` grant the returned latest qualified date
> is bounded by the grant at `2026-09-25` and would then not equal the newest marker. This is an interaction between
> the grant's date mode and A7 step 4's expectation that belongs to `OG-v-7`'s grading, not to the grant's width.
> Filed as row `NFRA_OPLGTW-Z-S11`.

### columns -- 7 of 9, 5 of 11, 3 of 9
Only the fields the sealed questions and the describe journey name:

| dataset | granted | from | withheld (real catalog fields, deliberately outside) |
|---|---|---|---|
| `dim_balance` | `account_ref`, `business_date`, `mkt_value_long`, `mkt_value_short`, `net_mv_positions`, `cash_balance_settled_only`, `net_mv_plus_cash` | RQ2-2 (`mkt_value_long`, `mkt_value_short`, and `account_ref` for *"how many accounts hold a negative value"*), RQ2-3 (three fields reported separately), RQ2-4 (`net_mv_plus_cash`), RQ2-5 (`cash_balance_settled_only`), RQ2-6 (`net_mv_positions`), `business_date` to pin the date | `bank_cash`, `bank_sweep_ibf` |
| `dim_position` | `business_date`, `cusip`, `l_s`, `quantity_settled_unsettled`, `market_value_settled_unsettled` | RQ2-1 (groups by `cusip`, `l_s`; sums the two named fields), RQ2-7 (the paged row read) | `ticker_symbol`, `quantity_settled`, `quantity_unsettled_long`, `quantity_unsettled_short`, `closing_price` |
| `dim_asset` | `cusip`, `ticker_symbol`, `security_description_line_1` | the describe journey; `security_description_line_1` is where the protocol's prompt-like and formula-like text is carried | `security_description_line_2`, `security_description_line_3`, `closing_price`, `maturity_date`, `prod_code`, `prodcatg_code` |

No `forbidden_field_classes` member (`raw_account_id`, `account_title`, `tax_identifier`, `mailing_address`,
`hidden_*_operand`) is named anywhere in the grant.

### operations -- all four the contract allows, each load-bearing
`query` (RQ2-1 .. RQ2-7), `download_filtered` (A7 step 3's full authorized CSV), `list` (A7 step 4's available
dates), `describe` (the `dim_asset` journey and RQ2-1/RQ2-2's *"what unit or scale does the dataset description
give"*). `download_original` and `write` are contract-disabled and are never requested.

### accounts -- RULED, then MEASURED under amendment A3

Row `NFRA_OPLGTW-Z-S10` reported that `parse_scope` requires `scope.accounts` to name every granted master's
accounts and `_strings` (`data_entitlement.py:204-206`) **refuses an empty list**, so a runnable Schwab grant
structurally contains raw account identifiers -- colliding with `GCG1-AC6`. That finding is **confirmed on the
code**, not merely inferred: `app/account_ref.py:3` states it outright -- *"Accounts are raw Schwab ids INSIDE
the Gateway only: the data_entitlement grant's `scope.accounts` and the source rows."* The `account_ref` a
principal sees is a keyed HMAC over the raw id and never appears in a grant.

`1.0.0_SA_CTO~O` ruled it @`8bf2bf37c6` (msg 26461) and the issuer carried it as **A2**: **AC6 wins** -- the
scope diff is committed with every account identifier redacted, plus the SHA-256 of the unredacted diff; the
candidate names its accounts only off-repo. The grant's accounts are **exactly the set
`SEALED_EXPECTED_V2.json` was computed over, per master; record the COUNT, never an identifier.**

**A3's measurement** (the read it granted: `GetObject` by pinned VersionId on those 5 objects only, decoded with
pyarrow, counts only). Instrument: `probes/og_g1_accounts.py`.

| master | dataset | business date | rows | distinct accounts in object | VersionId |
|---|---|---|---|---|---|
| `08242234` | `dim_balance` | 2026-09-25 | 7460 | 7460 | `5PRG5E6r7Y0ouiB7XOK1Ab7bQGCCEyNd` |
| `08242234` | `dim_balance` | 2026-09-24 | 7452 | 7452 | `UKusT2qymyztVSohx_i3JvHcJRedvdtK` |
| `08335338` | `dim_balance` | 2026-09-25 | 7548 | 7548 | `l902TpDGeJ.P.AF0Ru8kiW87B6EpUXTq` |
| `08335338` | `dim_position` | 2026-09-25 | 106835 | 6347 | `MTChLz7Qh4xR9ySWrFxSBRxRktUmLwa3` |
| `08335338` | `dim_balance` | 2026-09-24 | 7540 | 7540 | `ccnYjRNxXDSlvEuZLv.TlRR8NA5PkQQq` |

Keys are `schwab/<master>/silver/<dataset>/date=<date>/data.parquet`. **Denominator: 5 of 5 pinned objects read.**

**THE GRANT'S ACCOUNT COUNT, per master:** `08242234` -> **7460**; `08335338` -> **7548**.

Feasibility, measured rather than assumed: every id is exactly 10 characters, so `scope.accounts` serialises to
about **195,102 bytes -- 47.6% of DynamoDB's 400 KB item limit**. The ruled grant is writable in one item.

> ⛔ **THIS IS EVERY ACCOUNT IN BOTH MASTERS, AND THAT IS CORRECT -- BUT IT CONTRADICTS THIS ORDER'S OWN
> "bounded subset" CLAUSE.** The order says *"The accounts and columns stay a bounded subset"* because a grant
> wide enough to answer everything destroys the refusal evidence. The **columns** are a bounded subset (15 of 29).
> The **accounts cannot be**: RQ2-2 .. RQ2-6 are aggregates over the objects -- sums of `mkt_value_long`,
> `net_mv_positions`, `cash_balance_settled_only`, and *"how many accounts hold a negative value"* -- so any
> account subset changes the answer and breaks the hash match against `OG-v-6`'s seal. The seal FORCES an
> all-accounts grant. Ruling (1) is therefore not just permissible, it is the only value that lets the sealed
> answers verify. **The cost, stated plainly: the account dimension yields NO refusal discriminator.** Every
> refusal `OG-v-7` grades must come from the column or date dimension -- which is what the pair below does.
> Filed as row `NFRA_OPLGTW-Z-S13`.

### The AC3 artifacts under amendment A2 -- the off-repo candidate and the diff hash

- **offrepo_candidate:** `%LOCALAPPDATA%/opal/og-salt/og_g1_candidate.json`
- **unredacted_diff_sha256:** `<<ABSENT -- the candidate is keyed by the controlled identity's tid/oid, which does not exist; see section 1>>`

The candidate lives outside the repository, on the same route `WALKTHROUGH_PROTOCOL.md` section 2 already uses
for real-data answers (`%LOCALAPPDATA%/opal/og-salt/`). It is the only place the 15,008 account identifiers
appear; nothing about them enters git but their **count**. Retention: it is deleted once `G-C` closes and the
grant is active, since from then on the authoritative copy is the `data_entitlement` record itself.

Both fields are ABSENT for one reason, not two: without a `tid`/`oid` there is no candidate to validate and
therefore no diff to hash. The probe's AC3 arm is fully implemented against A2's mechanism and will grade the
moment the identity exists -- it calls `validate_candidate`, recomputes the unredacted diff, compares this
SHA-256, and separately scans this committed file for any account identifier of the candidate.

### The discriminator pair (`GCG1-J1`)

| | request | why it is a discriminator |
|---|---|---|
| **MUST SUCCEED** | `08335338`, `dim_balance`, `2026-09-25`, columns `net_mv_positions` + `cash_balance_settled_only` + `net_mv_plus_cash`, `query` (= RQ2-3) | every dimension inside the grant; the seal gives it `expected_class VALUE`, so a refusal here is a real defect |
| **MUST BE REFUSED** | `08335338`, `dim_balance`, `2026-09-25`, column `bank_cash`, `query` | identical on master, dataset, date and operation -- **only the column differs**, so the refusal can be caused by nothing but the grant's column dimension. `bank_cash` is a real `dim_balance` field in the contract catalog, so this is an out-of-scope refusal and not an unknown-field error |

A second axis: `2026-09-23` (a real qualified date) with an otherwise in-scope request isolates the date dimension.

---

## 5. Criterion verdicts, each with its measurement

| id | verdict | measurement |
|---|---|---|
| `GCG1-AC1` | **FAIL** | 3 of 4 required identity fields present; `controlled_oid` and `controlled_upn` ABSENT -- no controlled identity exists (38 of 38 internal accounts accounted for, 0 qualify). `controlled_tid` is verified and GUID-shaped |
| `GCG1-AC2` | **FAIL** | the instrument was exercised and its reading recorded: 3 deployed roster entries across 2 present rosters, 2 `*_PRINCIPALS` rosters ABSENT, positive control returned. The comparison cannot be made against an absent identity -- **and an absent identity is not a non-privileged one** |
| `GCG1-AC3` | **FAIL** | two independent causes. (a) no `tid`/`oid` to validate, so `validate_candidate` refuses at `make_principal`. (b) the committed candidate redacts `accounts` under AC6, so what validates is not what a run would activate. The **scope half parses** under `de.parse_scope` with a substituted account list. Separately, the CLI has **no `prepare` subcommand** (row `NFRA_OPLGTW-Z-S9`) |
| `GCG1-AC4` | **FAIL** | no live write was performed, correctly -- the identity that would key it does not exist. `POLICY#<tid>#<oid>` is not constructible. The strong-read instrument was exercised against the table (10 `POLICY#` items, complete) |
| `GCG1-AC5` | **PASS** | 7 of 7 sealed questions inside the grant (masters, dataset and business dates each checked, read from the seal at HEAD); A7 step 4 no-date asks 2 of 2; A7 step 3 `download_filtered` 1 of 1 |
| `GCG1-AC6` | **PASS** | 4 files scanned, 0 with a finding |
| `GCG1-J1` | `UNVERIFIABLE-BY-INSTRUMENT` | graded by `3.0.0_SA_CVO~O` at L9. RECORD; NO VERDICT |

`<status>` is **not** flipped to `complete`: the order admits that flip only when every mechanical criterion
passes by output.

---

## 6. What a human must do -- one paragraph, non-technical

**Someone with Microsoft 365 administrator rights needs to create one new test user in the Opal Capital
directory, and tell this seat its sign-in address.** Call it something obviously non-human such as
`og-controlled@opalinvest.com`. It must be a brand-new account, not a copy of anyone's, and its address must not
be added to any admin or write-capable list. It needs a normal work mailbox licence so it can sign in to Claude in
a browser and complete the sign-in prompt like an ordinary employee would, because the test it exists for is a
person clicking through the connector. It needs no special permissions of any kind -- the whole point is that it
starts with nothing, so the test can prove the system correctly refuses it. Whoever creates it should also say
which Schwab accounts, of the two firms `08242234` (SmartX) and `08335338` (BlackDiamond), this test identity is
allowed to see, since the data grant cannot be written without that list and it must stay a small subset rather
than everything. Once the address exists, this seat reads its permanent identity numbers from the directory,
writes the one bounded grant through the committed operator command, reads it back, and the gate's evidence is
complete. Nothing else is waiting on anyone.

**Also owed by a seat, not by Andrew:** the disposition of rows `NFRA_OPLGTW-Z-S9` through `-S12`
(`2.0.0_SA_COO~O` is `disarm_owner` on the two ARMED ones, `-S10` and `-S11`) -- the missing `prepare`
subcommand in `GCG1-AC3`'s text, the AC3-verbatim / AC6-no-raw-account-id conflict, the `fixed_dates` / A7
step 4 interaction, and the row-id shape the order mandates that both gates reject. **`-S10` blocks
`GCG1-AC3` from ever passing as written, even once the identity exists.**

> ⛔ **Row ids: the order asks for `NFRA_OPLGTW-Z-OG-S<k>`, and both gates reject that shape.**
> `surprise-row-gate.py:104` and `proof-of-spec-check.py:1127` are anchored patterns admitting only `Z-`,
> `W<n>-` or `C-` before `S<k>`; 0 of the channel's 191 rows carry a `-OG-` segment. Filed under the order's
> literal ids, the commit would have been refused and these findings would have read as unfiled. They carry
> the admitted seat-row shape `NFRA_OPLGTW-Z-S9..S12` instead, continuing the existing `Z-S1..Z-S8` series.
> Recorded as row `-S12` so the renumbering is not later read as a seat inventing its own ids.
