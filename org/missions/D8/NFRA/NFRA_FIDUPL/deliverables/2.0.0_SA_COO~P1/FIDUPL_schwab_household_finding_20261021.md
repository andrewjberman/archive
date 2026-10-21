# FIDUPL / NFRA_FIDSLVR -- how households exist on the Schwab side (read-only finding)

Author: read-only research subagent of 2.0.0_SA_COO~P1, 2026-10-21 ~17:15-17:45Z, dell1. Answers CRO msg 9179 (Andrew-direct, record
`org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261021_1535Z_GOLD_MASTER_CUSTODIAL_ATTRIBUTION_KEY.md`).
No account number, tax id, person, client or firm name, address or cell value appears here. Identifiers that are not S3 prefixes
are shown as sha256[:8]. Claim tags: MEASURED (read from bytes this session, source named), INFERRED, ABSENT (searched, denominator
given), REPORTED (another seat's measurement, not re-run).

## Answer in five lines

1. The premise is partly wrong. "No household table in bronze or silver" is true only of master 08242234. Master 08335338 carries `fam` (stale since 2026-08-10) and `slm` (live to 2026-10-20). The cottonwood folder carries `slm`. Both are the vendor's account-to-group registry (MEASURED).
2. FAM/SLM `col_6` is Schwab's household key. It equals the account's own TIN on 7,589 of 7,589 joinable accounts, so it is a per-taxpayer grouping that does not join spouses. `col_1` is a master-grouping (advisor-relationship) id: 20 values at 08335338 (MEASURED).
3. The Master Account Number (`mstracct_number`) is a per-file constant: 1 distinct value in each of 6 of 6 `fact_acc` files. It defines the advisor book, not a household, and one account can sit under several masters (08242234 and 08335338 share 7,589 accounts) (MEASURED).
4. `tcf`/`tcfx` are trade confirmations and `tnn` is the annual 1099 tax file. None of them carries a grouping or relationship field. `tnn` "Tax ID" equals the `fact_acc` TIN on 100% of joinable rows (MEASURED).
5. Households can be synthesized: 4,471 TIN households over 7,638 open 49F Schwab accounts, or about 3,432 with the CRO's address/name rule (REPORTED). The household is a SEPARATE dimension from the `(custodian, native_group_id) -> firm` attribution config, because 90 Schwab households span more than one `col_1` group.

## (1) Evidence per feed type and column

### Feed census (MEASURED, `.tools/aws s3 ls s3://opal-data-assets/schwab/<scope>/bronze/`, 2026-10-21)

| scope (S3 prefix) | bronze types | household-bearing type |
|---|---|---|
| `08242234` | acc rld rlu rlw rly rps rtu rty sec tcf tcfx tnn trn uln ult upn upt (17) | none (this is the list the CRO record quotes) |
| `08335338` | acc **fam** rld rlu rly rps rtu rty sec **slm** tcf tcfx tnn trn uln ult upn upt (18) | `fam` (526 partitions, 2024-07-08..2026-08-10), `slm` (572 partitions, 2024-07-12..2026-10-20) |
| `08403355` | 16 types, no fam, no slm (`conversion_manifest.MASTER_NOT_PUBLISHED = {"08403355": ("slm",)}`) | none, but its 30 accounts are all inside the 08335338 SLM |
| `49financial` | 16 types, no fam/slm | none |
| `cottonwood` | acc rld rps sec **slm** tcfx tnn trn uln ult upn upt (12) | `slm` (7 partitions, 2026-10-12..2026-10-20) |

Silver mirrors it: `schwab/08335338/silver/fact_fam/` (526 partitions, last `date=2026-08-10`), `fact_slm/` (572, last
`date=2026-10-20`), `schwab/cottonwood/silver/fact_slm/` (7). The firm buckets `opal-data-49financial` / `opal-data-cottonwood` hold only
`schwab/<firm>/state/` under `schwab/`.

### (a) Master Account Number: where it lives, cardinality

- **Columns:** `mstracct_number` + `master_account_name` + `custdian_id` are the first columns of 15 of the 17 pinned silver specs
  (`schwab_schemas.SPECS`; all except FAM/SLM). In bronze CRS files the master is also in H1 field 2 (`crs_reader._H1_RE`). In CS files
  (FAM/SLM) it appears only in the zip entry name `{master}.CS{MMDDYY}.{TYPE}.zip` (`cs_reader.identity_from_chain`). TCF names it
  `Master #`, TCFX `MstrAcct #`, and TNN `MstrAcct`.
- **Per file (MEASURED, `fact_acc` 2026-10-20):** `mstracct_number` distinct = 1 in each of 6 files (08242234 7,610 rows / 7,578 open;
  08335338 7,701 / 7,617; 08403355 30 / 30; cottonwood 08134043, 08480305, 08719286: 32 / 32 each). Accounts with no master: 0. Every row
  carries it.
- **Masters in the estate:** 7 S3 masters (3 in `silver_registry.DECLARED_SCHWAB_MASTERS` + 4 cottonwood in
  `conversion_manifest.FIRM_SILVER_MASTERS`). Firm grain: 08242234/08335338/08403355 -> 49financial; the 4 others -> cottonwood.
- **Many-to-many at account grain (MEASURED):** 08242234 & 08335338 share 7,589 accounts; all 30 08403355 accounts are in 08335338; the 3
  cottonwood `fact_acc` files carry the SAME 32 accounts (pairwise overlap 32/32). Distinct accounts across the 6 files: 7,754, against
  15,437 rows. Summing by master double-counts by 2x.
- **A finer master layer exists in SLM/FAM `col_1`** (7-digit, 100% populated). At 08335338 SLM 2026-10-20 it has 20 groups of sizes
  6,376 / 1,221 / 30 / 4 / 3 / 2 / 2 / then 13 singletons. The largest equals S3 prefix 08242234 and the 30-group equals 08403355; the
  1,221-group (hash `5fa30971`) is not an S3 master and is in none of the 95 `fact_acc` columns of 08242234 or 08335338. `col_1 -> col_2`
  and `col_1 -> col_3` are 1:1 (20 pairs each; col_2 8 distinct, col_3 8 distinct). In all 3 cottonwood SLM files `col_1` = 08719286 on
  32/32 rows, including the files of 08134043 and 08480305.

### (b) tcf, tcfx, tnn (MEASURED from one full object each, parsed by pipe; only header names printed)

| type | sample | record type / shape | what the columns hold | grouping / relationship / owner / tax id / address / linked-account field? |
|---|---|---|---|---|
| `tcf` | `08242234/bronze/tcf/20260818/` (24,660 D1 rows) | H1(7) + H2 + D1 (194 columns) + T1. 900 partitions 2023-01-18..2026-08-18 (08335338 also ends 2026-08-18) | trade confirmations: Bus Date, Master #, Account#, Trd/Settl date, Action, Cancel, Symbol, CUSIP, Quantity, Price, Principal, Total Amount, 12 fee columns, Accrued Int, State Tax, `Account Name/Address 1..6`, `Account Title 1..3`, `Account Type`, `Unused Field 4/5`, `MsgBreak`, `Message 1..150` | owner name/address lines and titles only. No group or relationship id |
| `tcfx` | `08242234/bronze/tcfx/20261020/` (498 D1 + 498 D2 rows) | record type `CONFRMX` v02.00. D1 = 45 columns, D2 = 210 columns. 253 partitions 2025-10-17..2026-10-20 | the extended successor of tcf: D1 = Custdian, MstrAcct #, Master Account Name, Bus Date, Account ID, `Message Reference Key` + the same trade, fee, name/address and title columns. D2 = the key columns + `Message 1..203` | same as tcf. `Message Reference Key` links D1 to D2 of one confirm, not accounts to each other |
| `tnn` | `08242234/bronze/tnn/20260211/` (52,320 lines); the 2026-10-12 object is header + trailer only | record type `BD1099DF`, tax year 2025. 8 sections, each with a 2-row header: DIV, INT, MISC(comp), B (`D9B`), OID, R, MISC(stnd), NEC | 1099 boxes per account. Every section starts Custdian, MstrAcct, Master Account (Name), Date (Prepared), Account ID, `Tax ID`, Tax (Year), Account Title 1..3 | **`Tax ID`**: 100% populated, and equal to `fact_acc.ssn_tin_number` on every joinable row (DIV 1,643/1,643; INT 1,134/1,134; B 45,285/45,285). Annual and sparse: 40 of 144 08242234 objects are over 600 bytes. No group id |

Converter status: `set_identity_guard.HOLE_TYPES = ("tcf","tcfx","tnn")`. All three are bronze-only "named holes" with no silver.

### (c) Other account-level fields (MEASURED)

- **Name census over all 17 pinned silver specs (1,048 columns):** 0 names contain house/relat/client/family/group/link/advis. The
  candidate-evidence columns sit in `fact_acc` only: `ssn_tin_number`, `taxpayer_first/middle/last_name`, `txpyr_title`,
  `organization_primary_name`, `primary_contact`, `alias_name`, `mailing_address_line_1..3`, `account_mailing_city`, `ac_st`,
  `acct_mail_zip`, `email_address`, `phone_nbr`, `mobile_phone_number`, `date_of_birth`, `acct_regis` (33 codes at 08242234),
  `custtype_code` (IND 7,115 / TRUST 281 / ORG 182 open), `schwab_br_cd` (286 distinct), `managed_account_money_manager` (2 distinct).
  `account_title_line_1..3` also appears in RPS s2 and TRN.
- **TIN is masked by master (MEASURED, 2026-10-20):** `ssn_tin_number` is populated on 7,610/7,610 (08242234; 4,495 distinct), 0/7,701
  (08335338), 0/30 (08403355), and 32/32 in each cottonwood file (23 distinct). So on 08335338 the only household key is SLM `col_6`.
- **FAM/SLM 6 positional columns** (`cs_reader`; names are PRESUMED, from `a01_dim_relationship.py:9-22`, because the vendor layout doc
  never arrived). col_1 is the master grouping id (7-digit). col_2 is the group name (8 distinct). col_3 is the rep name (8 distinct).
  col_4 is the account (FAM 8-digit space-padded, SLM 9-digit zero-padded). col_5 is the registration/holder name. col_6 is the
  household key (9-digit, all-digit).
- **col_6 is the TIN (MEASURED):** SLM 2026-10-20 joined to 08242234 `fact_acc` gives `col_6 == ssn_tin_number` (dash-stripped) on
  7,589/7,589. This matches the CRO's 2026-10-06 FAM measurement (7,067/7,067, `logs/2026-10-06/cro_h_household_count_research_1731-1824Z.md`).
- **FAM vs SLM at 2026-08-10 (MEASURED):** 7,202 = 7,202 keys, 0 one-sided. col_5 and col_6 are equal on 7,202/7,202; col_2 on 7,198;
  col_3 on 7,199. **col_1 differs on 1,146**: SLM moved 1,142 accounts out of the 08242234 group into the `5fa30971` group. In July
  the two files were content-identical (`OPAL_ASSETS_49METATABLES_D3_0833_GROUPA_ANALYSIS_20260714.md` headline 4).
- **Coverage:** SLM 08335338 2026-10-20 has 7,651 rows, of which 7,648 are in 08335338 `fact_acc` (53 acc rows have no SLM row) and
  7,589 are in 08242234 `fact_acc` (21 acc rows have none). 3 SLM rows have a blank col_6.

## (2) Synthesis options, with measured cardinalities

Universe: the 49F Schwab union, 08242234 + 08335338 + 08403355 `fact_acc` at 2026-10-20, deduplicated on account = 7,722 accounts
(7,638 open). Key order: SLM col_6, else the 08242234 TIN, else a self-household.

| option | definition | households (open) | accounts / household | status |
|---|---|---|---|---|
| S0 master | one household per `mstracct_number` | 1 per file | 7,610 / 1 | MEASURED. Not a household: the master is the advisor book |
| S1 col_1 group | one per SLM col_1 | 20 | -- | MEASURED. Advisor-relationship grain, not household |
| **S2 custodian-native TIN** | col_6 (= TIN), with fallback | **4,471** over 7,638 open (4,541 over 7,722 all) | 1.71 | MEASURED. Sources: slm_col6 7,616, tin 21, self 1 (open). Size histogram: 1: 2,426; 2: 1,298; 3: 546; 4: 150; 5: 31; 6: 11; 7: 5; 8-10: 3; one hub of 95 |
| S2' TIN only, 08242234 alone | distinct `ssn_tin_number` over open accounts | 4,459 over 7,578 | 1.70 | MEASURED |
| S3 TIN + address/name evidence | CRO rule T1: join TINs on same address + a second signal, or a joint-title co-owner; hub cap 6 | 3,432 over 7,474 (4,411 TINs) | 2.18 | REPORTED (CRO 2026-10-06, accepted by Andrew "that works"; not re-run here; the script is session-scratch only) |
| S4 vendor relationship | Black Diamond `Relationship ID` (multi-TIN) | 2,689 relationships over 5,277 joint accounts; fam households nest in them at 96.8% | -- | REPORTED (`4.0.0_SA_CRO~A/deliverables/FAM_FIELD_SEMANTICS_AND_BD_PLATFORM_OVERLAP_20260819.md`). Not a Schwab feed; 73.3% coverage |
| cottonwood S2 | SLM col_6 | 23 over 32 (1: 16, 2: 6, 4: 1) | 1.39 | MEASURED (each of the 3 files) |

Failure modes:
- Spouses with separate TINs become separate households. S2 over-counts against S3 by about 22% (REPORTED ratio).
- A joint account keys only to its primary TIN.
- Hubs: one col_6 holds 95 accounts in the union. It is an entity or plan TIN (INFERRED) and must not be read as one family.
- 80 S2 households mix IND with TRUST/ORG `custtype_code`.
- 90 S2 households span more than one col_1 group, so the household is not nested under the advisor grouping.
- Account-to-master is many-to-many. Deduplicate on account before any household or AUM roll-up, or the 2x double-count enters.
- 08335338 and 08403355 deliver the TIN masked, so S2 there depends on SLM.
- `a01_dim_relationship.py` reads `fact_fam` only, so it has been `fam-carried` at 2026-08-10. `fact_slm` carries an identical col_6 and is current (INFERRED repoint candidate; the owner is the 49F gold runner lane, and it is a one-producer-per-key change for the CTO).
- col_6 is a TIN. It is a grouping key only and is never emitted; the a01 pattern hashes the minimum account id of the group.

## (3) Cross-custodian design

Fidelity facts used here (REPORTED, not re-measured):
- 31 G numbers per login; each label names one firm.
- 0 of 5,007 accounts carry a G number in any export file, and `gnumberAssociations` is empty on 20 of 20 `verify.json` calls.
- The Accounts catalog has 141 columns with no G, group or firm column.
- 58 Groups come from `allGroups.json` (keys `groupId, groupName, groupType, maintDateTime, updateName, accessScope, accessible,
  groupNameDisp`; no members in the list). The wizard walk reads them as 5 system + 53 named; the CRO brief says 54 account-based + 4
  criteria-based. The two splits are not reconciled.
- Groups are the only account-scoping filter on an export.

Sources: `RESEARCH_20261019_NFRA_FIDUPL_G_NUMBERS.md` and `FIDUPL_9001_wizard_walk_record_20261021.md`.

The two custodians' "native group" ids are different things:

| | Schwab | Fidelity |
|---|---|---|
| advisor/firm book | `mstracct_number` (on every row) and SLM `col_1` (on every SLM row) | G Number (on no export row; scope label only) |
| household | SLM/FAM `col_6`: per TIN, vendor-computed, on every account | Group: user-curated collection, membership not in the files and not yet read |

**A. Attribution config, `(custodian, native_group_id) -> firm[, advisor]`, one intent (who services the account).** Proposed columns:
- `custodian`
- `native_group_type`, enum `schwab_master | schwab_slm_group | fidelity_g_number | fidelity_group | fidelity_export_profile`
- `native_group_id`
- `firm_scope` (an `infra/logic/registry/` scope, for example `49financial`, `cottonwood`)
- `advisor_id` (nullable)
- `precedence`
- `effective_from` / `effective_to`
- `claim` (`measured | held`)
- `source`

What it can hold:
- Schwab: firm attribution per master (7 rows; overlap collapses at firm grain because all overlapping masters map to one firm), and
  optionally advisor attribution per SLM `col_1` (20 rows).
- Fidelity: a G number cannot reach an account from the files, so account attribution must come from the export SCOPE: a per-firm
  export profile or a Group filter. The config row is then `(fidelity, export_profile|group) -> firm`, and the G number is held as
  documentation (`claim=held`).

Rules:
- Where one account maps to two firms through two masters, `precedence` decides and the conflict is reported, never silently picked.
- 17 of 31 G numbers have no registry firm, so their rows are `firm_scope=null`. Excluding them is an act Andrew decides.

**B. Household dimension, separate (who is one family), with its own Opal-minted key.**
- `dim_household`: `household_id` (hashed anchor, never a TIN), `grain` (`taxpayer | family`), `method`.
- `bridge_account_household`: `(custodian, account_id) -> household_id`, plus `evidence_class` enum
  `custodian_native_tin | custodian_native_group | rule_synthesized | vendor_relationship | manual | self`, `source_as_of`, `claim`.

What neither custodian gives natively:
1. A family-grain key on Schwab. Native is per-TIN, so the family grain needs S3/S4 or manual.
2. Fidelity Group MEMBERSHIP per account (not in the files; not read), and Group coverage of the book (unmeasured).
3. A cross-custodian link for one family holding accounts at both custodians. This needs a shared TIN or a rule; whether Fidelity
   exports a TIN is unmeasured.
4. A rule for which native grouping wins when Schwab-TIN and a Fidelity Group disagree.

Reconciliation:
- Fidelity Groups are advisor-curated families, like the BD relationship. Schwab col_6 is per-taxpayer and nests inside a family (96.8%
  measured against BD).
- So the consistent cross-custodian household is the FAMILY grain, with the Schwab TIN household as a child level (`grain=taxpayer`).
  Map a Fidelity Group to a family when its membership is read, and lift Schwab from TIN to family by S3 or S4.
- Keep A and B unjoined by design: 90 Schwab households cross col_1 groups.
- The Fidelity-to-Schwab silver alignment map in `RESEARCH_20261021_NFRA_FIDUPL_FULL_FACT_TABLE_CATALOG.md` (Tier A2) has no row for
  `fact_fam`/`fact_slm`. Its Fidelity analog would be a new group-membership table.

## Not measured

- The vendor FAM/SLM layout spec. Column semantics are PRESUMED from bytes.
- The meaning of the new SLM col_1 group `5fa30971`, and why SLM and FAM diverge on col_1 since July.
- Why the 3 cottonwood `fact_acc` files hold the same 32 accounts and their SLM col_1 is 08719286 in every file. This is INFERRED to be a
  surprise; the COO should file a row in the project surprise channel (this subagent may write only this file).
- 08165601 has an SLM file at 2026-10-20 but no `fact_acc` file that day.
- S3 (CRO T1) was not re-run at 2026-10-20.
- The BD relationship nesting was not re-measured.
- The Fidelity side: Group memberships and coverage, whether `account.txt` carries a TIN, and the 54/4 vs 5/53 split.
- TCF/TCFX name/address populated rates. Only one object per type was parsed.
- The current gold `dim_relationship` partition and its `identity_source`.

## Sources

- Code: `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/{schwab_schemas.py, cs_reader.py, crs_reader.py, set_identity_guard.py, conversion_manifest.py, silver_registry.py, schwab_projections.py}`, `data/assets/scripts/gold/runners_49f/a01_dim_relationship.py`
- S3, read-only (2026-10-21):
  - listings of `s3://opal-data-assets/schwab/{08242234,08335338,08403355,49financial,cottonwood}/{bronze,silver}/`
  - full objects: `08242234/bronze/{tcf/20260818,tcfx/20261020,tnn/20261012,tnn/20260211}/`, `08335338/bronze/{fam/20260810,slm/20260810,slm/20261020}/`, `cottonwood/bronze/slm/date=2026-10-20/` (3 files)
  - `fact_acc` parquet `date=2026-10-20` for 08242234, 08335338, `49financial/08403355`, and `cottonwood/{08134043,08480305,08719286}`
- Probes are counts-only, in session scratchpad (`probe2.py, measure.py, m2.py, m3.py, m4.py`); not in the repo. Downloaded copies are
  scratchpad-only.
- Prior records: `org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/OPAL_ASSETS_49METATABLES_D3_0833_GROUPA_ANALYSIS_20260714.md`, `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/FAM_FIELD_SEMANTICS_AND_BD_PLATFORM_OVERLAP_20260819.md`, `org/tier1_exec/4.0.0_SA_CRO/logs/2026-10-06/cro_h_household_count_research_1731-1824Z.md`, `org/tier1_exec/4.0.0_SA_CRO/deliverables/RESEARCH_20261019_NFRA_FIDUPL_G_NUMBERS.md`, `org/tier1_exec/4.0.0_SA_CRO/deliverables/RESEARCH_20261021_NFRA_FIDUPL_FULL_FACT_TABLE_CATALOG.md`, `org/missions/D8/NFRA/NFRA_FIDUPL/deliverables/2.0.0_SA_COO~P1/FIDUPL_9001_wizard_walk_record_20261021.md`
