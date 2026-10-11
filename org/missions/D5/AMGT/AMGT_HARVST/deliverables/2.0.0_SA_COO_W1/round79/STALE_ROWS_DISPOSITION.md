# AMGT_HARVST -- the 18 stale remediation rows, dispositioned (round 79 packet)

**Issuer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~18:1xZ. **Authority:** `ledger/ROUND_ANALYSIS.round78.md` item 4 (`1.0.0_SA_CTO~DELL1` msg
2937): "A row is closed with the commit that resolved it, or carried with its named owner and the condition that clears it. No row
stays open with no owner for a third round."

**Census:** every `REMEDIATION_v*.md` under `surprise-channel/remediations/`, 13 files, 168 row ids, latest version per id. 21 rows
are open. 3 are round 78's new rows (D1-S3, D1-S4, D1-W133-S2, all in v13 and owned by this seat). The other **18** are the stale
rows below. Census script: `round79/remediation_census.py`.

Owner note: `2.0.0_SA_COO~H` was site Z's issuer of AMGT_HARVST before the move to dell1. Its rows pass to this seat, the
project's issuer (handover `deliverables/1.0.0_SA_CTO~Z/HANDOVER_TO_DELL1_20261009.md`). `1.0.0_SA_CTO~Z`'s endpoint rows pass to
`1.0.0_SA_CTO~DELL1`, the project's CTO on dell1.

## CLOSED (5 rows)

| row | from | resolved by | read at disposition |
|---|---|---|---|
| Z-S19 | v1 | the r75 list @52be31ddc2 | `HAL_US_Equity` company `Halliburton`, aliases `['Halliburton', 'Haliburton']`. The correct name is stored, and the misspelt folder form is kept as an alias. |
| Z-S20 | v1 | the r75 list @52be31ddc2 | same read as Z-S19 (the OneDrive folder spelling is carried as an alias, not as the name) |
| Z-S21 | v1 | the r75 list @52be31ddc2 | the identity path for the 40 folders is the list's own security_key, not EDGAR name enrichment; Halliburton reads correctly |
| Z-W108-S2 | v11 | HVST-bh-8 @f9d664f996 ("a Seeking Alpha job record's finished_at is the job's own end, not the run's") | `lib/opal_data_harvest/test_bh8_job_finished_at.py` present |
| Z-C-S63 (barrons half) | v5 | HVST-al-1 @5b33a747e3 (the job row reads `listing_empty_200`) | its request_kind half is CARRIED with Z-W90-S14 below |

## CARRIED (13 rows)

| row(s) | from | owner | the condition that clears it |
|---|---|---|---|
| Z-W87-S1, Z-W90-S6, Z-S56, Z-W92-S17, Z-W92-S18, Z-W92-S19, Z-S66, Z-W92-S20, Z-W90-S21, Z-C-S62 (10, the ft sign-in limb) | v5 | `2.0.0_SA_COO~W1` | The FT is out of FWD-18's publisher list (PRD v0.22: "the FT is not run"), and the ft limb is a QUALIFIED WAIT (round-37 ruling 2). Each clears when: the HVST-RECHECK-OCILAR-1 re-check on **2026-11-01** shows a working unattended ft sign-in that holds a session, or Andrew's word puts the FT back on the list (then cut as a cell). Re-dispositioned at 2026-11-01. |
| Z-W90-S14, plus Z-C-S63's request_kind half | v5 | `2.0.0_SA_COO~W1` | Measured at disposition: `lib/opal_data_harvest/transport.py:163` still returns `listing` for any path holding `/news`, so a bbg article GET (`/news/articles/...`) is labelled `listing`. Clears when an article GET is recorded as `article` (a one-function fix plus a test). It is cut in the first round whose list admits a repair cell. |
| Z-C-S72 | v5 | `1.0.0_SA_CTO~DELL1` | A company-level key (a populated composite_figi or an issuer id) so cross-security counts collapse listings. This is an endpoint/contract choice; it clears on the CTO's ruling plus a cell. |
| Z-W110-S5 | v12 | `2.0.0_SA_COO~W1` | Measured at disposition: the r75 list still holds `ICT_US_Equity` as `International Container Termin` (cut at 30 characters), and the TTE listings are spelt `Total Energies` and `TotalEnergies SE`. Clears when the issuer groups them by one of two routes: a registry identity record for the second listing (the lei limb links them), or a name match that survives the cut, or ICT_US_Equity leaves the list. Cut with the next list move. |

Every open row now names an owner and a clearing condition. None is ownerless.
