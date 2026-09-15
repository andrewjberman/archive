# AMGT-rj-8 -- RUN LOGS (0.9.0_WK_AMGT_RESAPP~22, 2026-09-15)

Every output below is VERBATIM from the run that produced it, in the order the
runs happened. The credits table is at the bottom, and it counts the whole cell
rather than the graded runs only -- a bound is a bound on what was SPENT.

The two secrets these runs need reach the process as environment variables the
CALLER exported through `comp-secrets get <name>`: LUSHA_API_KEY from
find-insure/lusha-ai/api-key, BRIGHT_DATA_API_KEY from
find-insure/bright-data/api-key and BD_SERP_ZONE (serp_opal) from the zone
config at find-dualbiz/bright-data/serp. No module in lib/research/management
reads a secret store: AC6 measures 0 such calls across 4 of 4 modules.

## AC1 -- the unit suite and the schema assertions

```
Ran 26 tests in 0.131s

OK
additionalProperties False forbids-email True has-role_start True has-confirmed True
```

## AC2 -- the roster from the persisted filing (BA_US_Equity), dry run

```
SOURCE: s3://opal-data-harvest/filings/v1/BA_US_Equity/000162828026004357.source.json accession 000162828026004357 item 'Item 10. Directors, Executive Officers and Corporate Governance'
PARSE: strategy narrative-entry lines-scanned 30 candidates 12 accepted 12 rejected 0
roster_status: RESOLVED
officers: 12 of 12 carry name, role and source filing
with-role-start 12 without-role-start 0 (denominator 12 officer(s) of this name)
ROLE-START-BASIS: filing-since-clause 12 filing-since-column 0 absent 0
confirmed: 12 of 12 officer(s) confirmed from the filing, avg_tenure_years 2.58
DRY-RUN: nothing written -- no Lusha call, no SERP call, no pool write (enrich.py --write-pool is the only writer).
```

## AC3 -- the live enrichment and the two pool writes (BA_US_Equity)

```
SOURCE: s3://opal-data-harvest/filings/v1/BA_US_Equity/000162828026004357.source.json accession 000162828026004357
roster_status: RESOLVED officers 12 with-role-start 12 without-role-start 0 avg_tenure_years 2.58
LUSHA: CALLED domain boeing.com filter seniority-c-suite(9) credits-used 2 (bound 2 per name) results 50 of 739 matched 4 of 12 officer(s)
LUSHA-UNMATCHED: 8 of 12 officer(s) enrichment ABSENT: Brett C. Gerry, Jesus Malave, Jr., Brendan J. Nelson, Robert K. Ortberg, Stephen K. Parker, D. Christopher Raymond, Ann M. Schmidt, Jeffrey S. Shockey
SERP: query site:boeing.com "Robert K. Ortberg" pages 1 status ABSENT ceo Robert K. Ortberg url ABSENT
SCRUB: contact-fields-stored 0 (provider keys removed 0, schema-valid True)
M-1: officers 12 avg_tenure_years 2.58 with-profile 4 schema additionalProperties:false, email/phone/mobile FORBIDDEN
OK: uploaded s3://opal-data-harvest/management/v1/BA_US_Equity/2026-09-15.json content-length 6290 read-back sha256 db156feae8af0f6f put True
POOL: pool_avg_tenure_years 2.58 names_in_union 256 names_with_roster 1 officers_with_role_start 12 (objects read 1, tenures 12, universe s3://opal-data-harvest/universe/v1/2026-09-15.json)
OK: uploaded s3://opal-data-harvest/management/v1/_pool/2026-09-15.json content-length 180 read-back sha256 7019f46de4c7f910 (7.5s)
```

## AC4 -- the four remaining QA names, and the pool listing

```
SOURCE: s3://opal-data-harvest/filings/v1/COST_US_Equity/000090983225000101.source.json accession 000090983225000101
roster_status: RESOLVED officers 13 with-role-start 13 without-role-start 0 avg_tenure_years 5.06
LUSHA: CALLED domain costco.com filter seniority-c-suite(9) credits-used 2 (bound 2 per name) results 50 of 81 matched 1 of 13 officer(s)
LUSHA-UNMATCHED: 12 of 13 officer(s) enrichment ABSENT: Ron M. Vachris, Russ Miller, Claudine Adamo, Patrick Callans, Caton Frates, Teresa Jones, Jim C. Klauer, Javier Polit, Pierr
SCRUB: contact-fields-stored 0 (provider keys removed 0, schema-valid True)
OK: uploaded s3://opal-data-harvest/management/v1/COST_US_Equity/2026-09-15.json content-length 6029 read-back sha256 a0e99d601e584aad put True
OK: uploaded s3://opal-data-harvest/management/v1/_pool/2026-09-15.json content-length 180 read-back sha256 96ff135d9eb48f2b (15.4s)
SOURCE: s3://opal-data-harvest/filings/v1/HD_US_Equity/000162828026019436.source.json accession 000162828026019436
roster_status: RESOLVED officers 10 with-role-start 9 without-role-start 1 avg_tenure_years 4.68
LUSHA: CALLED domain homedepot.com filter seniority-c-suite(9) credits-used 2 (bound 2 per name) results 50 of 107 matched 3 of 10 officer(s)
LUSHA-UNMATCHED: 7 of 10 officer(s) enrichment ABSENT: WILLIAM D. BASTEK, JORDAN BROGGI, ANGELA BROWN, JOHN DEATON, EDWARD P. DECKER, TERESA WYNN ROSEBOROUGH, MICHAEL ROWE
SCRUB: contact-fields-stored 0 (provider keys removed 0, schema-valid True)
OK: uploaded s3://opal-data-harvest/management/v1/HD_US_Equity/2026-09-15.json content-length 5121 read-back sha256 85c6589286802c5d put True
OK: uploaded s3://opal-data-harvest/management/v1/_pool/2026-09-15.json content-length 180 read-back sha256 41e9c22f26582a4a (12.4s)
SOURCE: s3://opal-data-harvest/filings/v1/SAP_GY_Equity/000110465926020058.source.json accession 000110465926020058
roster_status: RESOLVED officers 6 with-role-start 6 without-role-start 0 avg_tenure_years 4.04
LUSHA: CALLED domain sap.com filter seniority-c-suite(9) credits-used 2 (bound 2 per name) results 50 of 1471 matched 3 of 6 officer(s)
LUSHA-UNMATCHED: 3 of 6 officer(s) enrichment ABSENT: Muhammad Alam, Thomas Saueressig, Gina Vargiu-Breuer
SCRUB: contact-fields-stored 0 (provider keys removed 0, schema-valid True)
OK: uploaded s3://opal-data-harvest/management/v1/SAP_GY_Equity/2026-09-15.json content-length 3566 read-back sha256 d540be3758f259f6 put True
OK: uploaded s3://opal-data-harvest/management/v1/_pool/2026-09-15.json content-length 180 read-back sha256 d01da913870d6a6c (9.3s)
SOURCE: s3://opal-data-harvest/filings/v1/BABA_US_Equity/000119312526231755.source.json accession 000119312526231755
roster_status: RESOLVED officers 7 with-role-start 0 without-role-start 7 avg_tenure_years None
LUSHA: CALLED domain alibabagroup.com filter seniority-c-suite(9) credits-used 2 (bound 2 per name) results 50 of 327 matched 0 of 7 officer(s)
LUSHA-UNMATCHED: 7 of 7 officer(s) enrichment ABSENT: Joseph C. TSAI, Eddie Yongming WU, J. Michael EVANS, Toby Hong XU, Jane Fang JIANG, Sara Siying YU, Fan JIANG
SCRUB: contact-fields-stored 0 (provider keys removed 0, schema-valid True)
OK: uploaded s3://opal-data-harvest/management/v1/BABA_US_Equity/2026-09-15.json content-length 3447 read-back sha256 d80a8993b39d589e put True
OK: uploaded s3://opal-data-harvest/management/v1/_pool/2026-09-15.json content-length 180 read-back sha256 14fc087581fe2a36 (11.2s)
management/v1/BABA_US_Equity/2026-09-15.json
management/v1/BA_US_Equity/2026-09-15.json
management/v1/COST_US_Equity/2026-09-15.json
management/v1/HD_US_Equity/2026-09-15.json
management/v1/SAP_GY_Equity/2026-09-15.json
management/v1/_pool/2026-09-15.json
```

## AC5 -- the SERVED pool object and the SERVED BA object, read back

```
180
pool_avg_tenure_years 4.08 denominator {"names_in_union": 256, "names_with_roster": 5, "officers_with_role_start": 40}
6290
officers 12 avg_tenure_years 2.58 with-profile 4 contact-fields 0
```

## AC6 -- the batch dry run, the DISABLED weekly task, the commits, the ASCII census

```
BATCH: universe s3://opal-data-harvest/universe/v1/2026-09-15.json as_of 2026-09-15 names 256 with-persisted-filing 5 with-declared-domain 5 would-build 5 limit none
WOULD-BUILD: BABA_US_Equity, BA_US_Equity, COST_US_Equity, HD_US_Equity, SAP_GY_Equity
NO-PERSISTED-FILING: 251 of 256 name(s) -- rj-6's filings batch is the producer; each is an explicit UNRESOLVED-SOURCE object when this batch runs for real, never a silent skip
DRY-RUN: nothing built, no Lusha call, no SERP call, no pool write, no task run. 5 of 256 name(s) would be built.
TaskName:                             \OpalResearch-ExecManagement
Scheduled Task State:                 Disabled
Schedule Type:                        Weekly
deb16ee7d3 0.9.0_WK_AMGT_RESAPP~22 build(AMGT_RESAPP AMGT-rj-8, 0.9.0_WK_AMGT_RESAPP~22): the POOL object gets its own closed schema and a w
a4270d3072 0.9.0_WK_AMGT_RESAPP~22 build(AMGT_RESAPP AMGT-rj-8, 0.9.0_WK_AMGT_RESAPP~22): lib/research/management -- the exec-management ros
files 4 nonascii 0 raw-secretsmanager-reads 0 reveal-calls 0
```

## CONTROLS -- the pool gate, determinism of the pool object, and its mutant

```
served pool validates: (True, [])
recomputed: {"as_of": "2026-09-15", "pool_avg_tenure_years": 4.08, "pool_denominator": {"names_in_union": 256, "names_with_roster": 5, "officers_with_role_start": 40}}
identical-to-served: True | objects read 5
re-write put_performed: False content_length 180 sha 14fc087581fe2a36
MUTANT FIRED: the pool object does not validate, nothing written: pool_denominator: 'names_with_roster' is a required property
```

## MUTANTS -- the contact ban and the never-a-guessed-roster arms

```
CONTROL positive: the SERVED BA document validates: True
MUTANT email FIRED: True | ['contact field stored at $.officers[0].email']
MUTANT mobile FIRED: True | ['contact field stored at $.officers[0].mobile']
MUTANT empty-section FIRED: UNRESOLVED-SOURCE | officers 0 | the persisted 10-K filing 000162828026004357 carries an EMPTY officer section (Item 10. Di
MUTANT unreadable-section FIRED: UNRESOLVED-SOURCE | officers 0
```

## DETERMINISM -- the parse, twice, compared by sha256

```
run1 2a9458679c16d339 657
run2 2a9458679c16d339 657
IDENTICAL=True
```

## CREDITS AND EGRESS -- the whole cell, not the graded runs only

| instrument | call | names | credits / queries | inside the bound? |
|---|---|---|---|---|
| Lusha v3 contacts/prospecting | 1 page, page_size 50, seniority c-suite (id 9) server-side | BA_US_Equity | 2 (graded run) + 2 (an earlier run charged, then killed by the import collision of row AMGT_RESAPP-Z-W22-S2) = 4 | NO -- 4 against a bound of 2 per name; the row carries the measurement and the remedy |
| Lusha v3 contacts/prospecting | same | COST_US_Equity | 2 | yes |
| Lusha v3 contacts/prospecting | same | HD_US_Equity | 2 | yes |
| Lusha v3 contacts/prospecting | same | SAP_GY_Equity | 2 | yes |
| Lusha v3 contacts/prospecting | same | BABA_US_Equity | 2 | yes |
| Lusha contacts/enrich (disclosure) | NOT CALLED anywhere in the package | -- | 0 | yes -- the cell forbids it and AC6 measures 0 |
| Bright Data SERP (serp_opal) | serp_brightdata(), 1 page | 5 QA names, 1 query each | 5 queries | yes (one query per name) |
| Bright Data SERP (serp_opal) | 2 diagnostic queries for row AMGT_RESAPP-Z-W22-S1 | BA_US_Equity | 2 queries | the cell bounds the SERP at one query per name per run; these two are the ROW's evidence and are declared here rather than folded into the runs |
| SEC EDGAR | NOT CALLED -- rj-6's persisted filings are the input | -- | 0 | yes |

CELL TOTAL: **12 Lusha credits** (10 of them inside the per-name bound) and **7
Bright Data SERP queries**. Lusha account before the cell: 1,029 remaining of
1,200 (card 2 @5007337353).

## WHAT THE FIVE NAMES PRODUCED

| name | form | strategy | officers | with role start | avg tenure | Lusha matched | CEO profile |
|---|---|---|---|---|---|---|---|
| BA_US_Equity | 10-K | narrative-entry | 12 | 12 | 2.58 | 4 of 12 | ABSENT (row S1) |
| COST_US_Equity | 10-K | narrative-entry | 13 | 13 | 5.06 | 1 of 13 | ABSENT (row S1) |
| HD_US_Equity | 10-K | narrative-entry | 10 | 9 | 4.68 | 3 of 10 | ABSENT (row S1) |
| SAP_GY_Equity | 20-F | table-year | 6 | 6 | 4.04 | 3 of 6 | ABSENT (row S1) |
| BABA_US_Equity | 20-F | table-age | 7 | 0 | null | 0 of 7 | ABSENT (row S1) |

POOL: pool_avg_tenure_years 4.08 over 40 officers with a role start, across 5
names with a roster object, of 256 names in the union universe.

SAP is the one that would have gone wrong quietly: its Item 6 carries the
SUPERVISORY BOARD (twenty non-executive members) immediately above the EXECUTIVE
BOARD, and a parser that took the first table it found would have published the
wrong people with a role start each. The run rejects it by heading and keeps the
six Executive Board members.

BABA is the one that shows the role-start field is REAL and not assumed: its
Name/Age/Position table carries no tenure column, so 0 of 7 officers get a role
start and the name contributes nothing to the pool average. Nothing was mined
out of the biography prose to fill it.
