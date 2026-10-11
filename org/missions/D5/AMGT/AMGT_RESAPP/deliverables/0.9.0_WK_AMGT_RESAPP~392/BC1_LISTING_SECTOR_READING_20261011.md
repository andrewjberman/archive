# AMGT-bc-1 -- listing-sector reading (round 96), 2026-10-11

Question: does the STORED Bloomberg-fed data for the listings SAN_FP_Equity (SAN FP) and CSL_AU_Equity (CSL AU) already carry a sector value, so a classification could be served from an exchange-qualified source? Read-only. Control listing: BA_US_Equity (BA US), served with a sector today.

## Sources

- derived/model_block SAN_FP_Equity: s3://opal-data-harvest/derived/model_block/SAN_FP_Equity/20261011T130935Z/model_block.json, newest of 17, figures[3] vintage 2026-10-11T13:09:35Z, n=12618 fields scanned (1729 mnemonic records)
- derived/model_block CSL_AU_Equity: s3://opal-data-harvest/derived/model_block/CSL_AU_Equity/20260930T093804Z/model_block.json, newest of 6 (the last object is dated 2026-09-30), figures[3] vintage 2026-09-30T09:38:04Z, n=3629 fields scanned (533 mnemonic records)
- derived/model_block BA_US_Equity (control): s3://opal-data-harvest/derived/model_block/BA_US_Equity/20261011T130241Z/model_block.json, newest of 31, figures[3] vintage 2026-10-11T13:02:40Z, n=11212 fields scanned (1521 mnemonic records)
- bronze refdata SAN_FP_Equity: s3://opal-data-harvest/bloomberg/harvest/bronze/refdata/security_key=SAN_FP_Equity/20261011T130928Z.json, newest of 11, dict key "SAN FP Equity", n=368 fields scanned
- bronze refdata CSL_AU_Equity: s3://opal-data-harvest/bloomberg/harvest/bronze/refdata/security_key=CSL_AU_Equity/20260919T152121Z.json, newest of 3 (all dated 2026-09-19), dict key "CSL AU Equity", n=22 fields scanned
- bronze refdata BA_US_Equity (control): s3://opal-data-harvest/bloomberg/harvest/bronze/refdata/security_key=BA_US_Equity/20261011T130233Z.json, dict key "BA US Equity", n=428 fields scanned
- identity crosswalk: s3://opal-data-harvest/crosswalk/v1/2026-10-09.json (newest of 3), records for the three keys, n=9200 fields scanned over the whole object (243 records)
- classifications table etf-classifications (DynamoDB GetItem, all attributes): keys SAN, CSL, BA (control), SAN FP, CSL AU; last_updated SAN 2026-09-29T14:02:59Z, CSL 2026-09-30T02:23:47Z, BA 2026-08-25T17:48:57Z; n=24 attributes across the three rows found
- integrations/bloomberg/research/model_block_pull.py HEADER_FIELDS, n=25 names; integrations/bloomberg/research/field_map.json, n=122 distinct mnemonics swept

## Listings

SAN_FP_Equity (Bloomberg ticker: SAN FP)
FIELDS: GICS_SECTOR_NAME=Health Care (derived/model_block figures[3], vintage 2026-10-11T13:09:35Z; bronze refdata key "SAN FP Equity", same value)
SOURCE: derived/model_block/SAN_FP_Equity/20261011T130935Z/model_block.json, figures[3] (mnemonic GICS_SECTOR_NAME, field value), source bloomberg-dapi

CSL_AU_Equity (Bloomberg ticker: CSL AU)
FIELDS: GICS_SECTOR_NAME=Health Care (derived/model_block figures[3], vintage 2026-09-30T09:38:04Z; bronze refdata key "CSL AU Equity", vintage 2026-09-19T15:21:21Z, same value)
SOURCE: derived/model_block/CSL_AU_Equity/20260930T093804Z/model_block.json, figures[3] (mnemonic GICS_SECTOR_NAME, field value), source bloomberg-dapi

## Census

fields scanned n=37477 across the seven landed objects (3 model blocks n=27459, 3 refdata n=818, 1 crosswalk n=9200); matched n=9 (each model block matches its GICS_SECTOR_NAME record and that record's basis copy, 2 per block, 6 in all; each refdata object matches its GICS_SECTOR_NAME key, 3 in all; the crosswalk matches 0).
Sweep plane: a name matches sector, industr, gics, bics or SIC, tested on dict KEYS and on the `mnemonic` VALUE of each record. The model block stores each Bloomberg field as a record {mnemonic, value}, so a key-only sweep is blind to it. The first run swept keys only and read the BA control as matched 0; that run was discarded, and every figure in this section is from the corrected run.
Dictionary census: HEADER_FIELDS sector-class n=1 (GICS_SECTOR_NAME of 25); field_map.json sector-class n=1 (GICS_SECTOR_NAME of 122 distinct mnemonics). No GICS_INDUSTRY_*, BICS or INDUSTRY_SECTOR mnemonic is in either dictionary.
Classifications table: the sweep matched 0 of 24 attributes by name. The table's sector is not a named field: scoped_amgt.py _with_served_sector (line 647) derives it from sub_asset_class when that value is one of the 11 GICS sectors, so a name sweep of this surface is blind by construction.

## Control

CONTROL: BA_US_Equity FIELDS: GICS_SECTOR_NAME=Industrials (derived/model_block figures[3], vintage 2026-10-11T13:02:40Z; bronze refdata key "BA US Equity", same value); sub_asset_class=Industrials (classifications table row BA; not name-matched by the sweep, served by _with_served_sector)

## Surfaces

- READ: derived/model_block, newest object for each of SAN_FP_Equity, CSL_AU_Equity and BA_US_Equity (3 of 3 present), the GICS_SECTOR_NAME record of each.
- READ: bloomberg/harvest/bronze/refdata, newest object per key (3 of 3 present).
- READ: etf-classifications DynamoDB, GetItem on SAN, CSL, BA, SAN FP and CSL AU. The two listing-form keys SAN FP and CSL AU hold no item. The table holds 11361 items; no full scan was made.
- READ: crosswalk/v1, newest object. SAN_FP_Equity's source row names its folder "Sanofi SAN FP"; the table row SAN names "Banco Santander S.A. ADR". The crosswalk carries no sector field.
- READ: integrations/bloomberg/research/model_block_pull.py (HEADER_FIELDS) and integrations/bloomberg/research/field_map.json (the field dictionary).
- NOT READ: bloomberg/harvest/bronze/bestdata, bronze/segments, bronze/identity, bronze/exec_officers, bronze/histdata, silver/listing_hit, the other derived/ prefixes, and any equity reference table under opal-data-assets silver or gold. These were not reached, so no SECTOR-ABSENT claim is made from them.

## Outcome

OUTCOME: SECTOR-SERVED
SERVE-FROM: derived/model_block/<newest model_block.json>, figures[] record with mnemonic GICS_SECTOR_NAME, field value (source bloomberg-dapi); both listings. The same field is on the same listing in bronze refdata.
Read as stored, not verified against the vendor. The SAN FP value (Health Care) agrees with the crosswalk folder naming the issuer "Sanofi SAN FP". The bare-ticker table row SAN names a different issuer ("Banco Santander S.A. ADR") and carries sub_asset_class Health Care. The code withholds a table row whose name disagrees with the registered security name (scoped_amgt.py, AMGT_RESAPP-aa-2), which is the page's "classification not available" state. The CSL AU stored objects are older (model block 2026-09-30, refdata 2026-09-19) than SAN FP and BA US (2026-10-11); the CSL AU objects stop there. No serve is cut here: AMGT-bc-2 is conditional on this reading.

## Not changed

WRITES: none
BLOOMBERG CALLS: none
Reads only: S3 GET and LIST on opal-data-harvest, DynamoDB GetItem and DescribeTable on etf-classifications, local file reads. Scratch copies and the sweep scripts sit under .scratch/r96 of the worktree.
