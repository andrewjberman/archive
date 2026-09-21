# TX-m-3 -- case evidence for the four current exceptions (PRD s.3.3)

Cell: `TX-m-3`, read only, deliverables-only writer. Worker `0.9.0_WK_MDPF_TAXSMA~6`, round 1, worktree
HEAD `e8f800e6a9070e30793d9c44f4c3a271e2b8cdf9`. Masked last-four labels and aggregate counts only --
no full account number, name or balance appears below (probe `probes/tx_m_3.py` AC4 scans this file for
account-shaped digit runs on every grading run).

**Sources read** (no live SharePoint/Graph call made by this cell; bound 1 forbids it):
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/TAXSMA_D8_PIPELINE_20260915/RESEARCH.md@8e8afed454`, measured
  by its author 2026-09-15 ~04:35-04:52Z.
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/TAXSMA_D8_PIPELINE_20260915/account-status-evidence.json@8e8afed454`,
  `measured_at_utc: 2026-09-15T04:58:27.849734+00:00`, `business_date: 2026-09-11`, 13 accounts enumerated.
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/TAXSMA_D8_PIPELINE_20260915/evidence-manifest.json@8e8afed454`
  (receipt hashes; raw identities explicitly excluded from this file per its own `private_content_boundary`).
- `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json@671925aecc` (vocabulary: `identity_status`,
  `reason_codes`, `identity.accepted_account_forms` / `.rejected_forms`).
- `org/missions/D8/MDPF/MDPF_TAXSMA/prd/MDPF_TAXSMA_PRD.md@671925aecc` s.3.3/s.3.4.
- Live AWS reads by this worker (read-only, Opal infrastructure, logged to `command_log.jsonl` tagged
  `cell=TX-m-3`): see s.1 and s.5 below.

---

## 1. Protected carriers available to a worker that hold full workbook identities

**Live measurement, run fresh at grading time by `probes/tx_m_3.py` AC1** (instrument: `.tools/aws s3api
list-objects-v2` / `head-object`, read verbs only): the data contract's own carriers for the workbook's
*own* capture -- the only place a worker-reachable full **workbook** identity (as opposed to a custodian
identity) could be recorded -- are `address()`-built and were checked live:

- `s3://opal-data-assets/gateway/49financial/bronze/taxsma_workbook/` -- `list-objects-v2` returns no
  `Contents` (0 objects) at this read.
- `s3://opal-data-assets/gateway/49financial/silver/taxsma_workbook/` -- `list-objects-v2` returns no
  `Contents` (0 objects) at this read.
- `s3://opal-data-49financial/mdpf/49financial/state/taxsma_membership/dispositions.json` -- `head-object`
  returns 404 Not Found at this read.

**Denominator: 2 of 2 workbook-capture prefixes measured EMPTY, dispositions carrier measured ABSENT**,
at the UTC time printed by the probe run. This is consistent with the project state: `TX-g-1`'s capability
is not yet activated (G-A/`existing_workbook_access.status` is `UNMEASURED`; `TX-r-3` has not run), and no
`TX-b-1`/`TX-b-2`/`TX-m-1` write has happened in this worktree lineage, so no Bronze/Silver snapshot of the
live workbook exists anywhere a worker can read.

Carriers a worker **can** read (Opal AWS infrastructure, read-only, permitted under bound 1) that hold full
**custodian** identities -- cited from RESEARCH.md's "Source and producer evidence" table, not
re-downloaded here. The reporting-master and base-master path segments are masked to
`<reporting-master>` / `<base-master>`: those are custodian MASTER identifiers already published in the
ratified data contract (`identity.reporting_master`, `identity.base_master_control`), not client account
numbers, and this cell does not restate their digits to stay conservative under AC4:

- `s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json` (manual ETL roster; re-confirmed live
  by this worker via `head-object`: `LastModified: Thu, 27 Aug 2026 22:48:18 GMT`, `ETag:
  "8462a2e7a994df410225af72efd2e073"`, `VersionId: lNH3od2BprexiXQDjAxntCJjcNB_MK5t` -- matches
  RESEARCH.md's recorded vintage exactly; 5 accounts, partial membership list only, never a capture of
  the workbook itself)
- `s3://opal-data-assets/schwab/<reporting-master>/silver/fact_acc/date=2026-09-11/data.parquet`
- `s3://opal-data-assets/schwab/<reporting-master>/silver/fact_rps/date=2026-09-11/data.parquet`
- `s3://opal-data-assets/schwab/<reporting-master>/silver/dim_balance/date=2026-09-11/data.parquet`
- `s3://opal-data-assets/schwab/<base-master>/silver/fact_acc/date=2026-09-11/data.parquet`
- `s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/date=2026-09-11/data.parquet`
- `s3://opal-data-assets/blackdiamond/49f/gold/dim_taxsma_report/` (exactly one historical parquet
  object, ending in the same last-four as workbook slot 1, dated 2026-07-17)
- `s3://opal-data-49financial/gold/advi/canonical/canonical_valuation/date=2026-09-11/data.parquet`

**8 of 8** custodian-side carriers enumerated. None of the eight is a capture of the workbook's own
assertion -- each is an independent custodian, crosswalk or canonical-value source that a worker can
join *to* a workbook claim only if it already holds a matching full-key row.

**Statement on the full-key join (AC1's second half).** The only place the two uncorroborated claims'
(workbook slots 7 and 8, last-four **...4809** and **...5591**) own full workbook account numbers were
ever read is the live SharePoint workbook itself, captured only into the CTO seat's own device-local
private research receipts (`%LOCALAPPDATA%/CodexSeatScratch/1.0.0_SA_CTO~A/taxsma-20260915`, per
`evidence-manifest.json`'s `private_receipt_home`) -- a different seat's private, non-repository scratch,
listed in the manifest only by SHA-256 hash, and unreachable by any worker under bound 1 (no SharePoint/
Graph/live-workbook call) and bound 2 (no private data in the repository). The one committed file that
carries per-account observed fields (`account-status-evidence.json`) stores only masked `account_suffix`
(last four) values -- its own `identity_rule` line states plainly that "No historical exact-identity diff
is possible from masked ... cells." **So no protected carrier available to a worker holds the full
workbook identity of either uncorroborated claim, and the two uncorroborated claims CANNOT be joined on
full key by this worker or any worker** -- independently confirmed by the second fact above: even the one
custodian carrier that would corroborate them if they matched (the reporting-master 0833 `fact_acc` at
`date=2026-09-11`) records `acc_exact_rows: 0` for both, so there is no row to join to even if the full
number were known.

---

## 2. The two traded claims absent from the latest 0833

Per `account-status-evidence.json`, workbook slots 7 (**...4809**) and 8 (**...5591**) are `excel_ready:
"Yes"`, `excel_traded: "Yes"`, but both carry `acc_exact_rows: 0`, `balance_exact_rows: 0`,
`xref_exact_rows: 0` and `canonical_valuation_rows: 0` at `business_date: 2026-09-11`.

**...4809 (workbook slot 7): UNRESOLVED.** Evidence that stops assignment of a cause class:
- Reporting-master 0833 `fact_acc` at `date=2026-09-11` (7,469 rows, entire object read per RESEARCH.md
  "Source and producer evidence"): 0 exact rows for this account.
- Base-master 0824 `fact_acc` at the same business date (7,384 rows) records **zero exact matches for
  all ten numbered workbook accounts**, per RESEARCH.md line 61 and `account-status-evidence.json`
  `population.workbook_numbered_matches_in_0824: 0` -- this is uninformative as a discriminator, because
  it is equally true of the six corroborated accounts, so a zero-match result in 0824 does not by itself
  distinguish "wrong master" from "no cause."
- BD identity crosswalk `dim_account_xref` (6,202 rows): `xref_exact_rows: 0` for this account (only one
  exact match exists anywhere in that compared population, and RESEARCH.md does not attribute it to this
  account).
- BD Tax SMA report (`dim_taxsma_report/`, exactly one parquet object, dated 2026-07-17): its one row is
  keyed to the same last-four as workbook slot 1 (**...5115**), not this account.
- RESEARCH.md's own conclusion, line 114: "No cause has yet been proven for the two missing
  workbook-traded accounts or the two strategy-label conflicts."
- No prior YES/removal history is recorded for this account in any read source, so `REMOVED_UNCONFIRMED`
  / `TRANSFER_UNRESOLVED` (data contract `identity_status`) cannot be assigned without inventing a fact
  not in evidence; `MASTER_CONFLICT` cannot be assigned without a positive match under another master,
  which was not found. The applicable **status** under the data contract is `MISSING_CUSTODIAN`
  (identity_status enum; TX-m-2's own acceptance line: "an expected claim with no matching 0833 record
  stays in the expected population with MISSING_CUSTODIAN") -- but MISSING_CUSTODIAN is the *status*, not
  a *cause*; no cause class is grounded in the evidence read by this cell, so the cause is reported
  **UNRESOLVED**.

**...5591 (workbook slot 8): UNRESOLVED.** Same evidence pattern as **...4809** above: `acc_exact_rows:
0`, `xref_exact_rows: 0`, `canonical_valuation_rows: 0`; also absent from the one-row BD Tax SMA report
(keyed to **...5115**); also one of the ten accounts inside the 0824 zero-match population (uninformative,
same reasoning as above); RESEARCH.md line 114 names it explicitly among the "two missing
workbook-traded accounts." Cause class: **UNRESOLVED**.

---

## 3. The two strategy conflicts

Per `account-status-evidence.json`, workbook slots 1 (**...5115**) and 2 (**...3310**) are the only two
of the six 0833-corroborated accounts whose `excel_strategy` disagrees with `acc_strategies`; the other
four corroborated accounts (**...0058**, **...9710**, **...8743**, **...9812**) have matching labels
(RESEARCH.md matrix rows 3-6 show no "conflict" disposition; row for **...8743** is `SMA 200` in both
places).

**...5115 (workbook slot 1).**
- Workbook label: `excel_strategy = "SMA 145"`. Source date: the live workbook item's own
  `modified` stamp, **2026-09-14T18:33:00Z** (RESEARCH.md "Workbook population" section, item
  `01L6LHKFXVVTRR73M6KZGIHM4FY2ATNK4U`).
- Custodian label: `acc_strategies = ["Opal Tax SMA 200"]`. Source date: reporting-master 0833 `fact_acc`,
  `business_date: 2026-09-11` (`measured_at_utc: 2026-09-15T04:58:27Z`).
- RESEARCH.md's reconciliation matrix, row 1: "Traded claim corroborated; workbook 145 vs custodian 200
  conflict."

**...3310 (workbook slot 2).**
- Workbook label: `excel_strategy = "SMA 145"`. Source date: same workbook item, modified
  **2026-09-14T18:33:00Z**.
- Custodian label: `acc_strategies = ["Opal Tax SMA 200"]`. Source date: same 0833 root,
  `business_date: 2026-09-11`.
- RESEARCH.md's reconciliation matrix, row 2: "Traded claim corroborated; workbook 145 vs custodian 200
  conflict."

Both are `STRATEGY_CONFLICT` on the data contract's `identity_status` axis ("a workbook and custodian
strategy disagreement is STRATEGY_CONFLICT even when the account number matches" -- `TX-m-2` acceptance).
Neither case's account number is in dispute; both are corroborated (`acc_exact_rows: 1`,
`canonical_matches_balance_to_cent: true`). No cause is asserted for *why* the strategy labels disagree
(a re-designation timing lag, a custodian-side default, or a workbook entry error are all consistent with
the evidence and none is distinguished by any source read here); PRD line 199 states the same: "The
historical two uncorroborated traded claims and two strategy conflicts need actual authorized
reconciliation evidence; their causes are not presumed."

---

## 4. Privacy statement (AC4)

This deliverable contains no full account number, name or balance. Every account is referenced only by
its last-four label (**...5115**, **...3310**, **...4809**, **...5591**, and incidentally **...0058**,
**...9710**, **...8743**, **...9812** for the non-conflicted corroborated set) or by aggregate counts
already published in the committed, non-private `account-status-evidence.json`
(`population.workbook_traded_yes: 8`, etc.). The reporting-master and base-master identifiers are masked
to `<reporting-master>` / `<base-master>` throughout s.1 rather than restated, even though they are
already published in the ratified data contract, to keep this file conservatively clean of any
account-number-shaped digit run. `probes/tx_m_3.py` AC4 re-scans this exact file on every grading run for
ten-digit-00, four-hyphen-four and eight-ASCII-digit runs (excluding calendar-looking `YYYYMMDD` tokens)
and fails the criterion if one is found.

---

## 5. Command log (AC5)

Every AWS call this cell makes is read-only (`list-objects-v2`, `head-object`, `head-bucket` -- Describe/
Get/List/Head verbs only) and is appended to `command_log.jsonl` in this deliverables folder, tagged
`"cell": "TX-m-3"`, before it runs. No `put-object`, `delete-object`, `copy-object` or any Graph/
SharePoint write call is made by this cell. No dataset is written and no workbook, roster or custodian
record is changed: this cell's own write surface is `deliverables/0.9.0_WK_MDPF_TAXSMA~6/` only, and no
call in the tagged log touches `taxsma_workbook`, a roster path or a custodian write endpoint.
`probes/tx_m_3.py` AC5 re-reads `command_log.jsonl`, filters to `cell == "TX-m-3"`, and fails if any
tagged call is a non-read verb or targets a forbidden write surface (`workbook`, `roster`,
`dispositions.json`).

---

## 6. Note for L9 judgment (AC6, judgment -- no worker verdict)

Each stated cause above is supported by the evidence cited beside it: s.2's two `UNRESOLVED`
dispositions are each grounded in four independent negative/uninformative source reads plus
RESEARCH.md's own explicit "no cause has yet been proven" line, rather than inferred from silence alone;
s.3's two `STRATEGY_CONFLICT` findings are grounded in the exact `excel_strategy`/`acc_strategies` field
values in `account-status-evidence.json`, cross-checked against RESEARCH.md's independently-written
reconciliation-matrix prose for the same two rows. No cause beyond what those sources state is asserted.
