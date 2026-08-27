# ADVI_INSURE `INS-a-2` — THE FIELD→CALL MAP, PRINTED

**TO:** `ADVI_INSURE.TO-A1-AE` (`@f4884fb367`) · **cell:** `INS-a-2` · **criterion:** `INSA1AE-AC2`
**Executor:** `0.6.0_AE_PartnerETL` · **Issued by:** `2.0.0_SA_COO` · **Produced:** 2026-08-25T2232Z
**Decomp:** `workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md` (CVO cert `@7397dfd83e`)
**Repo HEAD at production:** `214bba9960`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`** (ADVI_INSURE PRD s.3, Andrew ~16:1xZ) — binds this document at every relay.

**ZERO VENDOR CALLS WERE MADE TO PRODUCE THIS.** Derived entirely from captured payload bytes already
in the estate, the committed API catalogue, and the vehicle source. The 49F principal was not touched.

---

> # ⛔ SUPERSEDED IN PART — READ §9 FIRST (v2, 2026-08-25T2315Z)
> **Andrew granted vendor egress at 22:48:48Z and the surfaces have now been EXERCISED live on the
> 49F principal.** Three verdicts below are overturned by measurement — including my own headline
> claim that `carrier` and `product` are supplied by no call. **They are supplied.** §1–§8 are
> preserved verbatim as the pre-egress record; **§9 is the current answer.**

## 0. THE HEADLINE — three things that change the build

1. ⛔ **`carrier` and `product` — the two fields Ruling 6 puts in v1 — are supplied by NO call for which
   this estate holds any evidence.** They are *presumed* to live inside `insuranceCharacteristics`, an
   object that has been observed exactly once, **empty (`{}`)**. The v1 field list rests on a container
   whose populated shape has never been seen. `INS-a-2`'s own decomp row predicted this: *"v1's
   `carrier/product` (s.11 #6) **may not be where the ruling assumes**."* **Confirmed, independently.**
2. ⛔ **There are TWO DIFFERENT `AccountDetailSearch` ENDPOINTS ON TWO DIFFERENT SURFACES, and the
   sanctioned one MASKS the join key.** Ruling 2 joins the two source modes **"on account number."** The
   `/portfolioreporting/*` variant — the surface already inside the vehicle's egress envelope — returns
   **`XXXX5115`, a masked last-4, and accepts no exact-number filter** (Andrew-authorized live probe,
   2026-07-21). The full unmasked number lives only on `/account-api/*`, **a separate gated egress
   surface.** The v1 join key is therefore not obtainable on the currently-sanctioned surface.
3. ⛔ **The estate's own catalogue mis-names its primary evidence file.** `account_detail_search.json`
   does **not** contain an `accountdetailsearch` response; its captured `url` is
   `RelationshipAccountDetailSearch`. **0 of 3 captured payloads hold an `/account-api/*` response.**
   Anyone resolving that payload by filename gets a different endpoint's projection and will not error.

---

## 1. THE DOMAIN, NAMED (Rule 24-i — the set this map claims to cover)

The v1 gold row for `insurance_nav_current`, fixed by `ADVI_INSURE_PRD.md` **s.11 Rulings 2, 3 and 6**
(`@5194584763`). **DENOMINATOR = 10 fields.** Riders / death benefit / cash value are **DEFERRED by
Ruling 6** and are therefore *out of this domain*, not gaps in it.

| # | v1 field | fixed by |
|---|---|---|
| 1 | `bd_account_id` (gold key) | Ruling 3 |
| 2 | account number (the **join key** between the two source modes) | Ruling 2 |
| 3 | `carrier` | Ruling 6 |
| 4 | `product` | Ruling 6 |
| 5 | `currentEmv` | Ruling 6 |
| 6 | `asOfDate` | Ruling 6 |
| 7 | `insuranceCharacteristics` (the container the above two are presumed to sit in) | Ruling 6 / TO |
| 8 | cohort membership (which accounts ARE the insurance cohort) | Ruling 2 |
| 9 | spine key: account → relationship | Ruling 3 |
| 10 | spine keys: relationship → advisor → firm | Ruling 3 |

---

## 2. THE CALLS, AND WHAT EACH IS GROUNDED ON

**Provenance is a separate field from the claim** (CLAUDE.md §4). No surface below is described without one.

| id | call | provenance of our knowledge | 49F principal |
|---|---|---|---|
| **S1** | `POST /request/api/offline/insurancerelationshiplist` (async: run → `resultGuid` → download) | **PROSE-ONLY** — `DATA_BDINSURANCE_PRD.md:137 @47a0a1e7e6`, from HAR-2. **No payload capture, no response shape, no field list in the estate.** | **UNEXERCISED** |
| **S2** | `POST /account-api/query/accountdetailsearch` | **PROSE-ONLY** — `DOMAIN.md @70e4741e83` prose block. **0 captured payloads.** | **UNEXERCISED** · gated egress (tier-3) |
| **S3** | `POST /relationship/request/query/RelationshipAccountDetailSearch` | ⭐ **CAPTURED BYTES** — 2 payload files, `status 200`, 50 rows, `total: 226` | **UNEXERCISED** (capture is Cottonwood) |
| **S4** | `GET /relationship/request/relationship/{id}` | ⭐ **CAPTURED BYTES** — 1 payload file, `status 200` | **UNEXERCISED** (capture is Cottonwood) |
| **S5** | `POST /portfolioreporting/api/…AccountDetailSearch` | **LIVE-PROBE MEASURED** — `taxsma_resolver.py:10-14 @0ac99a72cb`, Andrew-authorized probe 2026-07-21, positive-controlled on Chiles `internalId 22596361` | **IN ENVELOPE** (vehicle's sanctioned surface) |
| **S6** | DataMining qt6 (`Account × Month`) | catalogued | **PARITY LEG ONLY** — Ruling 2 forbids it as an ingest source |

⚠ **S3/S4's captured rows carry `teams: ["Cottonwood Capital Advisors"]`.** Every byte of directly-observed
insurance evidence in this estate is **Cottonwood's**. This corroborates the decomp's L-1 by a different
instrument (payload parse, not the decomp's census).

---

## 3. ⭐ THE MAP

**Legend — `MEASURED` = read from captured response bytes · `RECORDED` = stated in a committed doc, no
payload behind it · `ABSENT` = no call in the estate's evidence supplies it.**

| # | v1 field | SUPPLIED BY | grounding | status |
|---|---|---|---|---|
| 1 | `bd_account_id` | **S3** `accounts[].id` = `"z0927266711"` | **MEASURED** | ✅ |
| 2 | **account number (join key)** | **S3** `accounts[].accountNumber` = `"19007481-3"` **UNMASKED** | **MEASURED** | ✅ |
| 2b | ↳ same field on **S5** | `XXXX5115` **MASKED last-4; no exact-number filter accepted** | **LIVE-PROBE MEASURED** | ⛔ **UNUSABLE for the Ruling-2 join** |
| 2c | ↳ same field on **S2** | full unmasked — *"the ONLY exact full-number source"* | **RECORDED** (`taxsma_resolver.py:15-19`) | ⚠ gated egress |
| 3 | **`carrier`** | **no call** — presumed inside `insuranceCharacteristics`, never observed populated | **ABSENT** | ⛔ **GAP** |
| 4 | **`product`** | **no call** — same container, same absence | **ABSENT** | ⛔ **GAP** |
| 5 | `currentEmv` | **S3** `accounts[].currentEmv` = `{"emv": 500000.0, "asOf": "2026-07-07T00:00:00"}` | **MEASURED** | ✅ |
| 5b | ↳ also on **S2** | `currentEmv` listed in the `include` block | **RECORDED** | ✅ |
| 6 | `asOfDate` | **S3** `accounts[].asOfDate` = `"2026-07-07T00:00:00"` (also `dataAsOfDate`, `startDate`, `modifiedDate`) | **MEASURED** | ✅ ⚠ see §5 |
| 7 | `insuranceCharacteristics` | **S2 only** — the field name does **not exist** on S3's 27-field projection | **RECORDED**, observed once as `{}` | ⛔ **SHAPE UNKNOWN** |
| 8 | cohort membership | **S1** (the export's own list, Ruling 2) — *and nothing else* | **ABSENT** (no capture) | ⛔ **GAP** |
| 9 | account → relationship | **S3** — the account is nested under its relationship row (`z09305723` / `"Bass, Christa"`) | **MEASURED** | ✅ |
| 10 | relationship → advisor → firm | **S4** `financialTeam[]`; **S3** `teams[]` = `{"id":"z096714","name":"Cottonwood Capital Advisors"}` | **MEASURED** | ✅ |

### COVERAGE, PRINTED
```
DOMAIN                       10 fields  (ADVI_INSURE_PRD s.11 Rulings 2/3/6 @5194584763)
  SUPPLIED, measured on bytes  6   (#1, #2, #5, #6, #9, #10)
  SUPPLIED, recorded only      1   (#7 -- name only; populated shape never observed)
  ABSENT / GAP                 3   (#3 carrier, #4 product, #8 cohort membership)
UNMAPPED DOMAIN MEMBERS        0
CALLS ENUMERATED               6   (S1..S6)   -- NO ELLIPSIS
```

---

## 4. ⛔ THE ELLIPSIS, CLOSED

`DATA_BDINSURANCE_PRD.md:139-141 @47a0a1e7e6` presents the account schema as a list ending in a literal
`…` — a partial enumeration presented as whole. `0.4.0_DS_ClientPlatform~J` measured that; the TO
instructed me not to inherit it. **I did not. Here is the complete enumeration from the bytes.**

**S3 `accounts[]` — the CAPTURED projection. EXACTLY 27 FIELDS, no ellipsis:**
```
accountDisplayNumber  accountNumber  accountRegistrationType  asOfDate  closedBy  closedDate
closedWhen  correlation  createDate  currentEmv  custodialAccountNumber  custodian  custodianID
dataAsOfDate  dataFormatID  displayName  firmID  id  internalId  modifiedBy  modifiedDate  name
ordinal  relationshipID  repCodes  startDate  taxStatus
```

**S2 record — the PROSE projection (`DOMAIN.md @70e4741e83`). 18 fields.** No payload capture exists;
this set is transcribed from the doc and is **RECORDED, not MEASURED.**

### ⛔ THE TWO PROJECTIONS ARE NOT THE SAME SHAPE — 9 fields in common, out of 27 and 18

| | fields |
|---|---|
| **in both (9)** | `accountNumber` `asOfDate` `createDate` `currentEmv` `dataAsOfDate` `displayName` `id` `name` `taxStatus` |
| **only S3 (18)** | `accountDisplayNumber` `accountRegistrationType` `closedBy` `closedDate` `closedWhen` `correlation` `custodialAccountNumber` `custodian` `custodianID` `dataFormatID` `firmID` `internalId` `modifiedBy` `modifiedDate` `ordinal` `relationshipID` `repCodes` `startDate` |
| **only S2 (9)** | `accountSubCategoryId` `custodianId` `dataFormatId` **`insuranceCharacteristics`** **`insuranceCharacteristicsRiders`** `outsideIdentifiers` `positionOnly` `registrationTypeId` `taxLotMethod` |

**This is the direct answer to the cell's instruction — *"do not assume one call covers both."* It does
not. The same account (`z0927266711` / `19007481-3`) returns two different field sets from two calls.**

---

## 5. ⛔ THREE COLLISION HAZARDS FOR THE ETL — measured, not anticipated

**(a) CASE-VARIANT KEYS ACROSS THE TWO CALLS.** The same logical field is spelled differently per surface:

| logical field | S3 (captured) | S2 (recorded) |
|---|---|---|
| data format id | **`dataFormatID`** | **`dataFormatId`** |
| custodian id | **`custodianID`** | **`custodianId`** |

A parser keyed on one spelling returns `None` against the other and **does not raise**. This is the
silent-failure class, in the join Ruling 2 mandates.

**(b) TYPE DIVERGENCE ON A SHARED KEY.** `taxStatus` is **`1` (int)** on S3 and **`"Taxable"` (string)**
on S2 — same key name, different type, same account. A dtype-standardising silver step (Rule 17) will
be handed both.

**(c) `asOfDate` IS FOUR DIFFERENT DATES ON ONE RECORD.** The captured account carries
`asOfDate 2026-07-07`, `dataAsOfDate 2026-06-23`, `startDate 2026-06-23`, `modifiedDate 2026-07-08`.
Ruling 7 advances a gold row **only when `asOfDate` advances** and Ruling 5 prints *"statement as of
MM/DD"* to the client. **Which of these four is the statement date is NOT determined by any evidence in
this estate** — and `currentEmv` carries its own independent `asOf`. Picking wrong changes both the
cadence trigger and a client-facing string.

---

## 6. ⛔ THE FILENAME DEFECT — resolve payloads by `url`, never by name

| filename | ACTUAL captured `url` |
|---|---|
| `account_detail_search.json` | `POST /relationship/request/query/**RelationshipAccountDetailSearch**` |
| `relationship_search.json` | `POST /relationship/request/query/RelationshipAccountDetailSearch` *(same endpoint)* |
| `relationship_detail.json` | `GET /relationship/request/relationship/z09305726` ✅ |

`data/black_diamond/API/domains/insurance/endpoints/README.md @70e4741e83` describes three calls and calls
`/account-api/query/accountdetailsearch` *"**The insurance-relevant endpoint**."* **The estate holds no
capture of it.** Two of the three payload files are the *same* endpoint; the third is the relationship
detail. Token census across all three payload files:

```
insuranceCharacteristics  0 occurrences   currentEmv  1 occurrence (response-side, S3 nested account)
account-api               0 occurrences
```

**This is Rule 22a's "NEVER by filename" generalised past code: the name and the content disagree, and
resolving by name returns a clean, well-formed, 200-status response to a question you did not ask.**

---

## 7. WHAT THIS UNBLOCKS, AND WHAT IT DOES NOT

**UNBLOCKS —** `0.4.0_DS_ClientPlatform~J` declined the gold builder on exactly this: *"nobody has
answered which call supplies `currentEmv` vs `insuranceCharacteristics`."* **Answered:**

> **`currentEmv` comes from S3 (and S2). `insuranceCharacteristics` comes from S2 ONLY — the field name
> does not exist on S3's projection — and its populated shape has never been observed by anyone.**

The builder can be specified against 6 measured fields plus the spine joins. It **cannot** be specified
against `carrier`/`product` without either a populated specimen or a Ruling-6 amendment.

**DOES NOT UNBLOCK —** three gaps stand, and each names its dependency rather than being generalised
into "insurance data is unavailable" (`INS-a-3` discipline, applied here):

| gap | the dependency, named |
|---|---|
| `carrier`, `product` | one populated `insuranceCharacteristics` specimen — needs an S2 call, which needs the vendor-egress word |
| cohort membership | one S1 export run — same dependency |
| which of 4 dates is the statement date | resolvable from an S1/S2 response, or by a Ruling-7 clarification |

---

## 8. EVIDENCE LEDGER (Rule 22 — `file:line @ commit-ish`)

| claim | grounding | layer |
|---|---|---|
| S3 27-field projection; `accountNumber` unmasked; `currentEmv`; nesting under relationship | `data/black_diamond/API/domains/insurance/endpoints/payloads/account_detail_search.json @70e4741e83`, parsed | **MEASURED** |
| 50 rows this page, `total: 226` | same file, `responseBody.total` | **MEASURED** |
| `insuranceCharacteristics` 0 occurrences across all 3 payloads | token census over the 3 files | **MEASURED** |
| S2's 18-field set; `insuranceCharacteristics == {}` | `data/black_diamond/API/domains/insurance/DOMAIN.md @70e4741e83` | **RECORDED** |
| S5 returns masked last-4, no exact filter; S2 is the only full-number source; `/account-api/*` gated | `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_resolver.py:10-19 @0ac99a72cb` | **LIVE-PROBE MEASURED** (Andrew-authorized, 2026-07-21) |
| S1 shape; `/session/token` distinct authority | `docs/architecture/DATA_BDINSURANCE_PRD.md:137,155-160 @47a0a1e7e6` | **RECORDED** |
| v1 field domain (Rulings 2/3/6) | `docs/architecture/ADVI_INSURE_PRD.md:151-156 @5194584763` | **RECORDED** (ruling) |
| the ellipsis | `docs/architecture/DATA_BDINSURANCE_PRD.md:139-141 @47a0a1e7e6` | **MEASURED** |

**Instrument-independence:** the decomp reached `INS-a-2`'s hazard by a **census**; I reached it by
**parsing the payload bytes and diffing the two field sets**. Different instruments, same conclusion —
corroboration, not repetition. Findings in §5 and §6 are **NOT in the decomp** and are first-to-claim here.

**Not verified by me:** every `RECORDED` row above. I did not re-run any peer's method (TO posture), and
I made no vendor call.

---

# 9. ⭐ v2 — THE MAP AFTER LIVE EXERCISE (2026-08-25T2315Z)

**Authority:** Andrew-direct 2026-08-25T224848Z *"Youhave vendor egress"* (`@a1e9fbcca7`);
`2.0.0_SA_COO` 71632 lifting the DRY-only constraint. **Leg:** `insurance_leg.py @d7583e51b2`.
**Exercised on the 49F principal** — the first live 200s on this surface for this principal, which
discharges the decomp's **L-1** (*"49F principal UNEXERCISED"*).

## 9.1 WHAT I GOT WRONG IN §0–§3, AND WHY IT WAS WRONG THE RIGHT WAY

| §3 said | v2 measured | why the v1 verdict happened |
|---|---|---|
| `carrier` **ABSENT** — no call supplies it | **SUPPLIED** by `accounts[].custodian.name` | true of the *estate's evidence*, false of the *vendor*. Nobody had ever run the call. |
| `product` **ABSENT** | **SUPPLIED** by `accounts[].accountRegistrationType.identifier` | same |
| cohort membership **ABSENT** | **SUPPLIED** — 77 relationships, 106 accounts | same |

⛔ **The v1 map was a faithful report of a corpus, and a corpus is not a vendor.** Every `ABSENT`
carried the qualifier *"no call **for which this estate holds evidence**"* — that qualifier was
load-bearing and it is the only reason the verdict was honest rather than wrong.

## 9.2 THE MAP — all v1 fields, ONE sanctioned call, ACCOUNT grain

**Source: `POST /relationship/request/query/RelationshipAccountDetailSearch`** (S3), which returns
account records nested under their relationship row.

| # | v1 field | JSON path | measured value (specimen) |
|---|---|---|---|
| 1 | `bd_account_id` | `accounts[].id` | `"z0814328741"` |
| 2 | **account number (join key)** | `accounts[].accountNumber` | `"12266924"` — **UNMASKED, 106 of 106** |
| 3 | **`carrier`** | `accounts[].custodian.name` | `"Brighthouse Financial - Financial Professional"` |
| 4 | **`product`** | `accounts[].accountRegistrationType.identifier` | `"INSURANCE_OTHER"` |
| 5 | `currentEmv` | `accounts[].currentEmv.emv` | `382471.75` |
| 6 | `asOfDate` | `accounts[].currentEmv.asOf` | `"2026-08-24T00:00:00"` |
| 9 | account → relationship | parent row `.id` | `"z08117302"` |
| 10 | relationship → advisor/firm | parent row `.teams[]` | team objects |

```
DOMAIN 10 | SUPPLIED-MEASURED 8 | ABSENT 0 | on GATED surfaces 0 | unmapped 0
COHORT: 77 of 77 relationships materialised (paginated to the server total, NOT a page)
        106 account records | accountNumber unmasked 106/106
```

## 9.3 ⛔ THE FINDING THAT MATTERS MOST — THE EXPORT IS THE WRONG GRAIN FOR carrier/product

The bulk export **does** carry `Issuer` and `Product Type`, which makes it the tempting source.
**It is at RELATIONSHIP grain and CONCATENATES** every carrier in the relationship into one cell:

> `"Allianz Life, Brighthouse Financial - Financial Professional"`
> `"INSURANCE_ANNUITY, INSURANCE_LIFEINSURANCE, INSURANCE_OTHER"`

Ruling 6 asks for **account-level** fields. Measured over the full cohort:

```
account records whose relationship appears in the export : 106
  export Issuer == account custodian.name                :  93
  export Issuer != account custodian.name                :  13
  of those 13, export cell contains a comma              :  13   <- ALL of them
  residual mismatches NOT explained by concatenation     :   0
```

**Sourcing an account-level field from the export mis-attributes 12.3% of accounts to a
multi-carrier string** — and it would look correct on the 87% you spot-check. Rule 24(ii)
same-grain, violated inside the vendor's own artifact.

⚠ **AND THE NEAR-MISS BESIDE IT:** `custodian.dataFormatName` is `"ByAllAccounts"` — the data
**aggregator**. `custodian.name` is the **carrier**. Same object, adjacent keys, and the aggregator
is the one that reads like a system field you should ignore.

## 9.4 CORRECTIONS TO THE PROJECT'S OWN PREMISES

1. **`/account-api/*` IS NOT REQUIRED FOR v1.** Its unique contribution is
   `insuranceCharacteristics` / riders — which **Ruling 6 already DEFERS**. Carrier, product, value,
   date, key and spine all come from a sanctioned surface. **The narrow question now with Andrew is
   not load-bearing for v1.**
2. **The masked-key finding stands but belongs to a THIRD surface.** `XXXX`-masking is real on
   `/portfolioreporting/*` (`taxsma_resolver.py:10-19 @0ac99a72cb`). `/relationship/*` returns the
   number **unmasked**. My §0 item 2 implied the unmasked key lived only on `/account-api/*` —
   **wrong; it also lives on `/relationship/*`.**
3. **The two token authorities are BYTE-IDENTICAL on the 49F principal** —
   `sha256[:16]=e3c20170eedbafd3`, `len=66` both. `AUTHENTICATION.md` recorded interchangeability as
   *"untested"*; it is now tested. **AC1's "shown to be distinct" is measured FALSE here.** The
   routing was deliberately **not** collapsed onto that result — see `insurance_leg.py` header.
4. **Download is keyed on `exportResultID` (int), NOT `resultGuid`.** The guid 404s on every path.
5. **The export is ASYNC and answers HTTP 400 — not 404 — while building.** No status endpoint
   exists (`status/{id}` → 404), so readiness is polled on the download itself.
6. **A 200 is not a payload.** `/Api/Offline/ExportResults/{guid}` returns **200 with 5.5KB of
   HTML**. A `status==200 and len>100` check lands a login page in bronze as data. Validate on
   **magic bytes**.

## 9.5 WHAT REMAINS OPEN

| item | state |
|---|---|
| which of the record's **four dates** Ruling 5's client-facing *"statement as of MM/DD"* prints | **a RULING, not a measurement.** `currentEmv.asOf` is paired with the value it stamps and is the honest NAV vintage; the client-facing string is Andrew's call. |
| `insuranceCharacteristics` populated shape | **unread — `/account-api/*` still held and mechanically refused.** No longer on the v1 critical path. |
| riders / death benefit / cash value | **DEFERRED by Ruling 6** — outside v1, not a gap. |

## 9.6 EVIDENCE

Bronze landed RAW (Rule 17a), verified by live `ListObjectsV2` — never a producer self-report:
```
blackdiamond/49financial/bronze/insurance_relationshipaccountdetailsearch/2026-08-25/...   82,136 B
blackdiamond/49financial/bronze/insurance_insurancerelationshiplist/2026-08-25/...             77 B
blackdiamond/49financial/bronze/insurance_insurancerelationshiplist_export/2026-08-25/...  13,090 B
```
**Negative controls, all FIRED:** held surface refuses · unlisted surface refuses · firm-separation
aborts on a `cot` prefix. **0 calls made to `/account-api/*`.**
