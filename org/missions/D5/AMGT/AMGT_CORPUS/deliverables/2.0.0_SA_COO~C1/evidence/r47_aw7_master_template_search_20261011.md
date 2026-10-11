# AMGT_CORPUS round 47 -- CRPS-aw-7: the master template search (FWD-12 master arm)

**Issuer:** `2.0.0_SA_COO~C1` (dell1), 2026-10-11 ~16:2xZ. **Instrument:** the gateway's `find_sharepoint_site`, `search_site_files`, `list_site_files`,
`get_site_item` (read-only Graph). **Question (round-46 analysis s.3 item 4):** is `FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx` anywhere
on the research SharePoint, a site-wide file search with the denominator printed.

## Result: FOUND, on one site of eight searched

| site (name, how found) | query `FactSet Based ONE PAGER TEMPLATE` |
|---|---|
| OpalCapital (`find_sharepoint_site "Opal"`) | 0 hits |
| OpalOCIO | 0 hits |
| OpalConsulting | 0 hits |
| OpalCIOOfficefor49Financial | 0 hits |
| 49Financial | 0 hits |
| OpalTradeSubmissionsandApprovals501 | 0 hits |
| **Shared** (`find_sharepoint_site "Shared"`; library path `Shared Documents/Asset Management/Research/`, the CRO's corpus root) | **20 hits, among them the master (below)** |
| ExternallyShared | 0 hits |

**The master:** site `Shared` (`opalinvest.sharepoint.com,9332c03f-2ad0-4b84-97fe-7bcd2c9cb90a,18b7f31c-c878-41ea-9b7e-0c103bcb5679`), item
`01L6LHKFRTYYYRWCI37VGLHJQPCL3KMJXN`, name `FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx`, 383839 bytes, modified 2026-07-24T13:04:50Z, quickXorHash
`pq+3UloI3tpTLuBsibGiTtR/yuo=`. Two older siblings of the same stem sit beside it: `..._v1.xlsx` (375488 bytes, 2026-04-02; 383776 bytes, 2026-05-04).

## Instrument controls and what this does NOT cover

- Positive control: the same search for `KDDI` on `Shared` returned the KDDI folder, its research pack and its workbook; on `OpalCapital` the
  `KDDI` search returned 0, which is correct (that name's folders are on `Shared`). The seven 0-hit sites therefore read as "not indexed there", not as a
  failure of the instrument.
- The result list was 20 rows with no next-page marker; a further copy elsewhere on `Shared` may exist and was not enumerated. The Graph item carries no
  parent path, so WHERE in the library the master sits is not read here (the library root listing is name folders plus `Formatting examples`).
- Sites the name queries did not surface (`research`, `Asset Management` returned none) were not searched; the denominator is the 8 sites found by the
  queries "Opal" and "Shared".

## What follows (the ingest is not the existing path as it stands)

`lib/research/corpus/library.py` derives the root `.../Shared - Documents/Asset Management/Research` and its ingest walks the immediate NAME folders,
storing each resolved folder's files under `security_key=<key>`. `team_sheet._master_reading` finds the master by basename anywhere under the bronze
`research-report` prefix, so one object with that basename under any partition would serve the 63 `master_absent` names. A file that is not inside a
name folder is not reached by `ingest --write`; landing it needs a stated bronze partition for a name-less file and a site-Z write under a
never-widen pair (the library is synced at site Z only). The partition is a naming call: `lib/opal_naming.py` (LGIC R1-R21) builds every address.
