# Row AMGT_RESAPP-Z-S369 -- the read for ruling R4 (`ICT_US_Equity`)

1. **What the pool row is and where it came from.** `ICT_US_Equity` is the key the holdings join minted on 2026-09-16
   for the IDVZ holding "International Container Termin" (ticker ICT, identifier 6455819), from the stored Bloomberg row
   `ICT US Equity`. On the pool of 2026-10-06 that same holding failed to join (the day's Bloomberg file held no ICT row
   and the holding row had no country), so the key was carried in from the name list as a nameless "coverage" entry and
   the holding sits beside it unresolved.
2. **Can a name be filled from stored data alone? YES.** From `s3://opal-data-etfs/bbg/2026-10-06/characteristics.parquet`,
   the row whose `security` is `ICT US Equity`: `NAME` = `INTL CONTAINER TERM SVCS INC`, `CNTRY_OF_DOMICILE` = `PH`. The
   same name is stored on that row in 27 of the 33 daily files. It is Bloomberg's name for exactly this key, already
   stored; no new call is needed.
3. **Not needed for the name. What stored data does NOT settle** is whether `ICT_US_Equity` and `ICT_PM_Equity` are to be
   kept as two keys or merged into one: no ISIN, FIGI or exchange code is stored for the US key. That would take one
   Bloomberg identity read of `ICT US Equity` (ID_ISIN, ID_SEDOL1, ID_BB_GLOBAL, EXCH_CODE), which is Andrew's word.
   Until then the row should say: "ICT_US_Equity is named INTL CONTAINER TERM SVCS INC from the stored Bloomberg row;
   the IDVZ holding is the same security by its stored identifier; whether it stays a key apart from ICT_PM_Equity is
   not decided."

Read by a drafting subagent for `2.0.0_SA_COO~Z`, 2026-10-08 about 10:05Z to 10:20Z. Read-only: S3 GETs and LISTs on
`opal-data-harvest` and `opal-data-etfs`, and repo files. No Bloomberg call, no write, no name guessed. Every record
below is printed as stored.

## 1. The row

`org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`, id `AMGT_RESAPP-Z-S369` (1 of 958
rows parsed from the file's one fenced JSON array): ARMED, UNDER_INVESTIGATION, disarm owner `2.0.0_SA_COO~Z`, surfaced
by `2.0.0_SA_COO~H` at 2026-10-08T01:46:40Z. Its `one_line` ends "no field shows the two keys as one issuer". Section 5
below reads that sentence against the stored fields.

## 2. What is stored, by object and date

Listings: `crosswalk/v1/` holds 7 objects (2026-09-15 to 2026-10-07); `universe/v1/` holds 3 (2026-09-15, 2026-09-16,
2026-10-06). Count of the text `ICT_US_Equity` per object:

| object | `ICT_US_Equity` | `ICT_PM_Equity` |
|---|---|---|
| `universe/v1/2026-09-15.json` | 0 | 0 |
| `universe/v1/2026-09-16.json` | 1 | 0 |
| `crosswalk/v1/2026-09-15.json`, `-09-19`, `-09-22` | 0 | 0 |
| `crosswalk/v1/2026-09-24.json`, `-09-25`, `-09-29` | 4 | 6 |
| `universe/v1/2026-10-06.json` | 2 | 3 |
| `crosswalk/v1/2026-10-07.json` | 5 | 7 |

So the key first exists in `universe/v1/2026-09-16.json` and first enters the name list on 2026-09-24.

### 2a. The newest name list: `s3://opal-data-harvest/crosswalk/v1/2026-10-07.json` (243 records)

Record 158, `ICT_US_Equity`, every field:

```
security_key      ICT_US_Equity
model_key         ICT_US_Equity
bloomberg         ICT US
display_ticker    ICT US
raw_identifier    ICT US
exchange          US
share_class       null
resolution        MEASURED
association_keys  ["ICT_US", "ICT_US_Equity"]
legal_name        {"value": "International Container Termin", "status": "MEASURED",
                   "evidence": "s3://opal-data-harvest/universe/v1/2026-09-16.json :: names[] entry with source 'holding', its name"}
source_row        {"coverage_source": "s3://opal-data-harvest/universe/v1/2026-10-06.json", "folder": null, "one_pager_files": [],
                   "bloomberg_ticker": {"value": "ICT US", "status": "MEASURED", "resolved_at": "2026-10-06", "evidence": <the text below>}}
provenance.source_row       s3://opal-data-harvest/universe/v1/2026-10-06.json :: names[] key ICT_US_Equity
provenance.raw_identifier   the retained universe row's ticker, preserved verbatim
provenance.association_keys explicit canonical key and measured <ROOT>_<CC> pack convention; no bare-root alias
provenance.resolution       MEASURED through the Positioning chain (AMGT-rk-4, never a bare-ticker join): Bloomberg security
                            'ICT US Equity' MEASURED on bbg/<date>/characteristics for ticker root 'ICT'; compiled stable_id
                            '6455819_PH' (SEDOL '6455819' + domicile 'PH', check digit validated (precedence rung 3)); domicile
                            'PH'.; filing identity: the SEC ticker-to-CIK table (10422 rows, retrieved 2026-09-15T07:54:10Z)
                            carries no ticker 'ICT'; filing identity: the SEC ticker-to-CIK table (10459 rows, retrieved
                            2026-09-22T20:15:07Z) carries no ticker 'ICT'
```

The record has NO `identity` block: no ISIN, no FIGI, no SEDOL field of its own, no Bloomberg exchange code. Its
`exchange: US` is the second word of the ticker, not a Bloomberg field. Note that this record DOES carry a name,
`legal_name.value` "International Container Termin" (30 characters, cut), taken from the holding. The nameless entry is
the pool row in 2b, not this one.

Record 31, `ICT_PM_Equity`, every field:

```
security_key      ICT_PM_Equity
model_key         ICT_PM_Equity
bloomberg         ICT PM
display_ticker    ICT PM
raw_identifier    ICT PM
exchange          PM
share_class       null
resolution        MEASURED
legal_name        {"value": "INTL CONTAINER TERM SVCS INC", "status": "MEASURED",
                   "evidence": "the record's own identity.name (the Bloomberg NAME of its registration pull)"}
identity          bloomberg_security ICT PM Equity; name INTL CONTAINER TERM SVCS INC; exchange PM;
                  isin PHY411571011; sedol 6455819; figi BBG000BL67C5; composite_figi BBG000BL6726;
                  lei 254900FU1MWK0I0Q4J61; cik 1656958; sec_id 0001656958; website www.ictsi.com;
                  registered_at 2026-09-24T11:10Z; field_errors {};
                  source bloomberg/harvest/bronze/identity/security_key=ICT_PM_Equity/20260924T111046Z.json
source_row        folder "International Container Terminals"; coverage_source lib/research/identity/registrations.json;
                  bloomberg_ticker {"value": "ICT PM", "status": "MEASURED", "resolved_at": "2026-09-24T11:10Z",
                  "evidence": "registrations.json entry, registered_at 2026-09-24T11:10Z"}
provenance.resolution   registered via ONE Bloomberg reference_data call (C-INSTANTIATION-ENTRY), landed at
                        bloomberg/harvest/bronze/identity/security_key=ICT_PM_Equity/20260924T111046Z.json
provenance.exchange     the second token of the registration's bloomberg field ('ICT PM'); Bloomberg's own EXCH_CODE ('PM')
                        is carried separately on identity.exchange -- AGREES: id token 'PM' == Bloomberg EXCH_CODE 'PM'
provenance.resolves_coverage_record   this registration RESOLVES the UNRESOLVED coverage record for folder 'International
                        Container Terminals' (lib/research/identity/data/universe.json) in place
```

The same list's `identity_universe.refusals[26]` (60 refusals):

```
raw_identifier  ICT
security_key    null
reason          the form 'ICT' matches no persisted or measured identifier form in crosswalk/v1 (as_of 2026-09-29, 237
                records) -- it is NOT guessed The ETF plane's producer-side identifier contract is NOT established
                (C-ETF-PLANE-READ), so this raw identifier is kept UNRESOLVED rather than guessed. Root-equal canonical
                candidate(s) NAMED, NOT merged: ['ICT_PM_Equity', 'ICT_US_Equity']. Positioning-chain evidence: no valid
                CUSIP/FIGI/SEDOL shape (raw identifier '6455819') and no BBG-characteristics row confirms a Bloomberg
                security for ticker root 'ICT' -- UNRESOLVED, never guessed
```

### 2b. The pool: `s3://opal-data-harvest/universe/v1/2026-10-06.json`

Top level: `as_of` 2026-10-06, `snapshot_date` 2026-10-05, 302 names, holdings read from
`gold/holding/date=2026-10-02/holding.parquet` for all four books; denominators coverage 237, holdings 167, union 302,
resolved 242, unresolved 60. Three entries mention ICT as a whole word:

```
names[116]  security_key ICT_PM_Equity   ticker "ICT PM"   name "International Container Terminals"
            source coverage   resolution MEASURED   books []   weight_by_book {}   cik null
            filing_identity {cik null, form_expected none, source none}
            resolution_reason: registered via ONE Bloomberg reference_data call (C-INSTANTIATION-ENTRY), landed at
              bloomberg/harvest/bronze/identity/security_key=ICT_PM_Equity/20260924T111046Z.json; filing identity: the SEC
              ticker-to-CIK table (10459 rows, retrieved 2026-09-22T20:15:07Z) carries no ticker 'ICT'

names[117]  security_key ICT_US_Equity   ticker "ICT US"   name null            <-- the row in question
            source coverage   resolution MEASURED   books []   weight_by_book {}   cik null
            filing_identity {cik null, form_expected none, source none}
            resolution_reason: MEASURED through the Positioning chain (AMGT-rk-4, never a bare-ticker join): Bloomberg
              security 'ICT US Equity' MEASURED on bbg/<date>/characteristics for ticker root 'ICT'; compiled stable_id
              '6455819_PH' (SEDOL '6455819' + domicile 'PH', check digit validated (precedence rung 3)); domicile 'PH'.;
              filing identity: [the two SEC table sentences as in 2a]

names[268]  security_key null   ticker "ICT"   name "International Container Termin"   <-- the unresolved holding
            source holding   resolution UNRESOLVED   books ["IDVZ"]   weight_by_book {"IDVZ": 1.63}   cik null
            filing_identity {cik null, form_expected none, source none}
            resolution_reason: [the same text as refusals[26] in 2a]
```

### 2c. The two older pools

`universe/v1/2026-09-15.json` (256 names, holdings of 2026-09-11): no `ICT_US_Equity`. Two entries: `names[53]`, the
research folder "International Container Terminals", source coverage, UNRESOLVED, no key, no ticker ("the coverage
row's bloomberg_ticker status is 'UNRESOLVED' ... NOT guessed from the folder name"); and `names[164]`, the holding, ticker
"ICT", IDVZ 1.72, UNRESOLVED, candidates "none".

`universe/v1/2026-09-16.json` (250 names, holdings of 2026-09-14): **the key's first appearance.**

```
names[88]   security_key ICT_US_Equity   ticker "ICT US Equity"   name "International Container Termin"
            source holding   resolution MEASURED   books ["IDVZ"]   weight_by_book {"IDVZ": 1.7}
            resolution_reason: MEASURED through the Positioning chain (AMGT-rk-4, never a bare-ticker join): Bloomberg
              security 'ICT US Equity' MEASURED on bbg/<date>/characteristics for ticker root 'ICT'; compiled stable_id
              '6455819_PH' (SEDOL '6455819' + domicile 'PH', check digit validated (precedence rung 3)); domicile 'PH'.;
              filing identity: the SEC ticker-to-CIK table (10422 rows, retrieved 2026-09-15T07:54:10Z) carries no ticker 'ICT'
names[211]  the research folder "International Container Terminals", source coverage, UNRESOLVED, no key (as on 09-15)
```

### 2d. The repo's own files

- `lib/research/identity/registrations.json` lines 336 to 360: ONE entry mentions ICT, folder "International Container
  Terminals", `bloomberg` "ICT PM", `security_key` `ICT_PM_Equity`, the identity block of 2a (ISIN PHY411571011, SEDOL
  6455819, name INTL CONTAINER TERM SVCS INC), registered 2026-09-24T11:10Z. There is no entry for `ICT US`.
- `lib/research/identity/data/universe.json` lines 1025 to 1041 (the research-folder list): folder "International
  Container Terminals", `bloomberg_ticker` null, UNRESOLVED, "no *ONE PAGER*.xlsx workbook found in this folder",
  2026-09-10T23:18Z. No `ICT US` there either.
- `lib/research/identity/positioning_chain.py` lines 41 to 43 name this very holding as the one case of its third rule:
  "the SEDOL + domicile, when the raw value is 7-char SEDOL-shaped with a valid check digit (1 -- International Container
  Terminal Services Inc, domicile PH)".

So `ICT_US_Equity` was never put on a coverage list by a person. No research folder, no registration and no pull names
it. Its one source is the holdings join.

## 3. The holding and the Bloomberg row it joined (bucket `opal-data-etfs`, read-only)

The holding, `gold/holding/date=<D>/holding.parquet`, the one row whose ticker is `ICT`:

| date | book | ticker | name | `cusip` column | domicile | weight |
|---|---|---|---|---|---|---|
| 2026-09-14 | IDVZ | ICT | International Container Termin | 6455819 | PH | 1.70 |
| 2026-10-02 | IDVZ | ICT | International Container Termin | 6455819 | (empty) | 1.63 |
| 2026-10-06 | IDVZ | ICT | International Container Termin | 6455819 | PH | 1.62 |

The Bloomberg row, `bbg/<D>/characteristics.parquet`, the one row whose `security` begins `ICT `, over all 33 daily
files (33 of 33 read):

| dates | rows in the file | the ICT row |
|---|---|---|
| 2026-08-20 | 109 | none |
| 2026-08-21, 2026-08-24 | 170 | `ICT US Equity`, NAME empty, domicile empty |
| 2026-08-25 to 2026-09-30 (26 files) | 171 or 172 | `ICT US Equity`, NAME `INTL CONTAINER TERM SVCS INC`, domicile `PH` |
| 2026-10-01, 2026-10-02, 2026-10-05 | 114 | none |
| 2026-10-06 | 172 | `ICT US Equity`, NAME `INTL CONTAINER TERM SVCS INC`, domicile `PH` |

On 2026-10-06 the row also carries GICS sector Industrials, industry group Transportation. The file's columns hold no
ISIN, SEDOL, FIGI or exchange code.

**Why the pool of 2026-10-06 reads as it does.** It was built from the holdings of 2026-10-02. On that date the
Bloomberg file had 114 rows and no ICT row, and the holding row's domicile was empty. The join's third rule needs both
(a Bloomberg-confirmed security, and the SEDOL with the domicile), so the holding fell to UNRESOLVED. The key minted on
2026-09-16 was still in the name list, so the build carried it in as a "coverage" entry with no books and no name
(the name had lived on the holding entry). One holding became two entries. The reason text on the holding, "no valid
CUSIP/FIGI/SEDOL shape (raw identifier '6455819')", is not what the identifier shows: 6455819 is 7 characters and its
SEDOL check digit validates (weighted sum 91, check digit 9, last digit 9; computed here).

## 4. The two candidate keys, side by side

| | `ICT_PM_Equity` | `ICT_US_Equity` |
|---|---|---|
| how it was minted | one Bloomberg identity pull, 2026-09-24T11:10Z, for the research folder | the holdings join, 2026-09-16, from the IDVZ holding |
| Bloomberg security | `ICT PM Equity` | `ICT US Equity` |
| Bloomberg NAME (stored) | INTL CONTAINER TERM SVCS INC (registration) | INTL CONTAINER TERM SVCS INC (daily file, 27 of 33 days) |
| exchange code | PM, and Bloomberg's own EXCH_CODE PM, stored | "US" from the ticker's second word only; no Bloomberg exchange code stored |
| ISIN | PHY411571011 | not stored |
| SEDOL | 6455819 (Bloomberg, registration) | 6455819 (the holding's identifier, from the fund's own holdings file) |
| FIGI / composite FIGI | BBG000BL67C5 / BBG000BL6726 | not stored |
| country of domicile | not a field of the registration (the ISIN opens PH) | PH (Bloomberg daily file, and the holding row) |
| company number (CIK) | 1656958 | not stored; the SEC ticker table carries no ticker ICT |
| held in a book | no (books empty) | yes through the holding: IDVZ 1.62 to 1.72 |

## 5. What the stored fields show, and what they do not

**They show one issuer.** Three stored fields agree, each on a different plane:
- the Bloomberg NAME is the same string on both securities (`INTL CONTAINER TERM SVCS INC`);
- the SEDOL Bloomberg returned for `ICT PM Equity` (6455819) is the identifier the fund's holdings file carries for the
  holding that `ICT_US_Equity` was minted from;
- the domicile is PH on the US row, and the PM key's ISIN opens PH.

So the row's sentence "no field shows the two keys as one issuer" does not hold against the stored data: the SEDOL and
the name do. The earlier read (AMGT_HARVST order HVST-bh-6, `BH6_ICT_US_EQUITY.md`) saw the
shared SEDOL and set it aside as "in the pool reason text only, not a registry field". The registry does carry it
(`lib/research/identity/registrations.json` line 351, `"sedol": "6455819"`). That read did not open the daily Bloomberg
file (its two files mention `characteristics` 0 times), so it did not see the name stored for `ICT US Equity`.

**They show more than that: the IDVZ holding IS the Manila line.** A SEDOL names one listing. The fund holds the
security whose SEDOL is 6455819, and Bloomberg gave that SEDOL for `ICT PM Equity`.

**They do not show** what `ICT US Equity` is as a Bloomberg security of its own: whether Bloomberg treats it as a
separate US-quoted line of the same company with its own ISIN, SEDOL and FIGI, or as another way of reaching the same
line. No ISIN, SEDOL, FIGI or exchange code was ever pulled for it. That is the only thing a new identity read would add,
and it bears on ONE question: keep two keys, or merge the US key into the PM key. It does not bear on the name.

## 6. What the disarm can do from stored data, and what waits

From stored data, with no vendor call:
1. **Name the pool row.** `ICT_US_Equity`: `INTL CONTAINER TERM SVCS INC`, source
   `s3://opal-data-etfs/bbg/2026-10-06/characteristics.parquet`, row `ICT US Equity`. (The name list already carries the
   holding's cut name "International Container Termin" for this key; the Bloomberg NAME is the fuller stored one.)
2. **Resolve the holding.** A pool build over a holdings date on which the Bloomberg file carries the ICT row and the
   holding carries its domicile (2026-10-06 does; 2026-10-02 did not) joins the holding to `ICT_US_Equity` again by the
   existing rule, as it did on 2026-09-16. No rule change is needed for that. The two entries become one.

Waits on Andrew's word (a Bloomberg identity read) or on a ruling:
3. **One key or two.** Whether `ICT_US_Equity` is merged into `ICT_PM_Equity` (so the holding, the research folder and
   the registration sit under one key). The stored SEDOL says the holding is the PM line; a merge is a change to what
   is served and to AMGT_HARVST's list, so it is the CTO's to rule, with or without the new read.

## 7. Not measured

- The raw Bloomberg pull for `ICT PM Equity` (`bloomberg/harvest/bronze/identity/security_key=ICT_PM_Equity/20260924T111046Z.json`)
  was not opened; its fields are read from the registration and the name list, which quote it.
- Why the Bloomberg daily file fell to 114 rows on 2026-10-01, 2026-10-02 and 2026-10-05, and why the holding's domicile
  was empty on 2026-10-02. Those are the ETF plane's, not this project's.
- Whether any other holding was split the same way by the 2026-10-06 build (60 names are unresolved there; one was read).
- The DynamoDB tables the join can also read (`etf-classifications`, `trade-security-identifiers`) were not read.
- No pool build was run and nothing was written.
