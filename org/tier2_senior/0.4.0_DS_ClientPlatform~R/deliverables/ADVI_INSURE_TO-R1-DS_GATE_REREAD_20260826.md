# ADVI_INSURE.TO-R1-DS -- FOUR-GATE RE-READ

**seat:** `0.4.0_DS_ClientPlatform~R` · **scope authority:** `2.0.0_SA_COO` 72177 s.3 (RULING, 2026-08-26T13:54:47Z)
**read taken:** 2026-08-26T13:58Z - 14:05Z · **acts:** READ ONLY. Zero writes, zero mints, zero invokes.

---

## THE ONE-LINE ANSWER

**Three of the four gates have OPENED. One is genuinely still shut.** The dependency that gated AC1 and AC2
landed roughly two hours AFTER `0.4.0_DS_ClientPlatform~J` declared their ceiling, and nobody re-read the
state between then and this dispatch. **`~J`'s instance is not wrong; it is CORRECT AS OF ITS OWN VINTAGE
and the world moved underneath it.**

| gate | `~J` verdict (2026-08-25) | measured NOW | delta |
|---|---|---|---|
| **AC1** APPLIED half (`INS-b-1`, `INS-inv-4`) | APPLIED-GATED | **OPEN -- and SATISFIED** | bronze + silver landed |
| **AC2** APPLIED limb | DESIGN-COMPLETE / APPLIED-GATED | **OPEN -- rows landed, ONE SPINE LEG HOLLOW** | see finding 1 |
| **AC3** AFTER half | AFTER-HALF-GATED | **OPEN, measured 12/12 clean -- BUT NOT YET DISCRIMINATING** | see finding 2 |
| **AC4** EMISSION | DETERMINED / EMISSION-GATED | **STILL SHUT** | 0 insurance keys in the serve root |

`AC5` and `AC6` were already `PASS` and nothing in this read disturbs them.

---

## GATE 1 -- AC1 APPLIED HALF: OPEN, AND SATISFIED

`~J` measured `blackdiamond/49financial/` **absent (0 keys)**. It exists now.

**Instrument note (deliberately different from `~J`'s):** their read was a substring walk over four trees.
Mine adds a **structural read** -- `list_objects_v2` with `Delimiter='/'`, enumerating `CommonPrefixes` --
which answers EXISTENCE with no matcher in the path at all, so a dead filter cannot manufacture either verdict.
Their 480,954-key walk is **cited, not re-run.**

```
s3://opal-data-assets/blackdiamond/            child prefixes: 3   49f/  49financial/  cottonwood/
s3://opal-data-assets/blackdiamond/49financial/ child prefixes: 4   bronze/  bronze_legacy/  silver/  silver_legacy/
```

**Full materialised walk, denominator printed:** `blackdiamond/` = **12,650 keys over 13 pages**,
`insurance`-bearing = **8**. POSITIVE CONTROL `allocation` = **686** over the same walked set, so the
matcher discriminates.

**BRONZE (6 keys, all raw JSON, landed 2026-08-25T23:00:16Z - 23:15:27Z):**
```
bronze/insurance_insurancerelationshiplist/2026-08-25/..._page0.json                          77 B
bronze/insurance_insurancerelationshiplist_export/2026-08-25/..._exportResultID-282394.json 13090 B
bronze/insurance_insurancerelationshiplist_export/2026-08-25/..._exportResultID-282397.json 13089 B
bronze/insurance_relationshipaccountdetailsearch/2026-08-25/..._offset0.json                82136 B
bronze/insurance_relationshipaccountdetailsearch/2026-08-25/..._offset50.json               41688 B
bronze/insurance_relationshipaccountdetailsearch/2026-08-25/..._page0.json                  82136 B
```

**RULE 17a CONTROL, run because a parquet under `bronze/` is irreversible and would read as a PASS:**
`.parquet` under `blackdiamond/49financial/bronze/` = **0 over 6 keys fully walked**. POSITIVE CONTROL --
the identical matcher over `silver/` returns **2 of 2** -- so the bronze zero is MEASURED, not a dead
suffix test. **Bronze is raw JSON, byte-for-byte. Clean.**

**SILVER (2 parquet, landed 2026-08-26T00:02:07Z - 00:02:08Z), in the RULED framework grammar:**
```
silver/fact_insurance_insurancerelationshiplist_export/date=2026-08-25/data.parquet  12120 B
silver/fact_insurance_relationshipaccountdetailsearch/date=2026-08-25/data.parquet   32934 B
```
This is `_fact_table()` + `silver_key()` form exactly as ruled at `5c3410758c` -- **not** the literal
`silver/insurance_*` the TO's AC1 row still reads. The landed bytes follow the ruling, not the stale row.

**WHY NOBODY SAW IT:** `~J` took their ceiling at `8b550db941`, **2026-08-25T20:54:04Z**. The first bronze
byte landed **2026-08-25T23:00:16Z** -- **2h06m later.** The gate opened after the last seat looked.

> **CORRECTION TO MY OWN ACK (message 72xxx, this session):** I told `2.0.0_SA_COO` the dependency landed
> "SEVEN HOURS after the ceiling." **It is two hours, not seven.** I subtracted a `-04:00` git timestamp
> against a UTC one -- the exact `--date` mangle CLAUDE.md warns about, committed while quoting the rule.
> The conclusion is unchanged and the arithmetic was wrong.

---

## GATE 2 -- AC2 APPLIED LIMB: OPEN, ROWS LANDED, ONE SPINE LEG HOLLOW

```
s3://opal-data-49financial/gold/advi/insurance/insurance_nav_current/date=2026-08-25/data.parquet
  12,889 B · written 2026-08-26T00:16:38Z · 106 rows x 15 columns
```
**Producer exists in-repo and is named in the rows:** `data/assets/scripts/gold/bd49f_insurance_nav_current.py`
(`GOLD_PREFIX` at `:87`, `SOURCE_PIPELINE` at `:107`); every row carries `source_pipeline =
bd49f_insurance_nav_current`. This is a real producer's output, not a hand-placed artifact.

**GRAIN HOLDS as designed:** duplicates on `(bd_account_id, as_of_date)` = **0 over 106 rows.**
*(For contrast, `(account_id, as_of_date)` shows 102 duplicates -- because that column is empty; see below.
The designed grain is the first one and it is clean.)*

**FORBIDDEN-FIELD CENSUS, now against the LANDED schema rather than the designed one:**
**0 violations over 15 columns.** Positive control: the same matcher fires on a planted `twr_ytd`.
No returns, no series, no analytics reached the table.

### FINDING 1 -- `account_id` IS NULL 106/106, AND `~J`'s OWN EVIDENCE SAYS THAT LEG EXISTS

| column | null | distinct |
|---|---|---|
| `bd_account_id` | 0/106 | 106 |
| `relationship_id` | 0/106 | 77 |
| `firm` | 0/106 | 1 (`3281`) |
| **`account_id`** | **106/106** | **0** |
| `account_id_basis` | 0/106 | 1 -- `NOT-DERIVABLE-UPSTREAM` |
| `advisor_basis` | 0/106 | 1 -- `NOT-DERIVABLE-UPSTREAM` |
| `spine_class` | 0/106 | 1 -- `unassigned` |

**The ADVISOR leg being `NOT-DERIVABLE-UPSTREAM` is RULED and correct** (issuer 70462; `~J` measured 0 of 95
columns carrying an advisor id, and the issuer re-ran it over a wider net and it survived).

**The `account_id` leg is NOT ruled, and `~J`'s instance asserts the opposite.** Their AC2 `output_evidence`,
verbatim: *"LEG 1 BD-native -> Opal account_id: JD2 `dim_advisor_fee_role` (160,091 rows / 44 cols; 5,337 at
is_current) carries BOTH `bd_account_id` ... AND `account_id` ... 5,337 distinct each: **ID JOIN EXISTS**."*
The landed table stamps that same leg `NOT-DERIVABLE-UPSTREAM` on every row.

**Both can be true** -- the join exists in `dim_advisor_fee_role` and these 106 insurance accounts may simply
fall outside its 5,337 `is_current` rows. **That is a hypothesis, not a finding: I have not joined the two
sets and I am not claiming a cause.** What is measured is the contradiction between a certified instance and
the landed artifact, and it sits on AC2's load-bearing clause -- *"carrying the spine keys ... SO EVERY
AGGREGATION IS A JOIN, NEVER A COMPUTATION IN THE FRONTEND."* **With `account_id` and advisor both empty, the
spine that reaches the frontend is `relationship_id` + `firm`.** Whether that satisfies AC2 is the ISSUER's
ruling, not mine.

---

## GATE 3 -- AC3 AFTER HALF: MEASURABLE NOW, PASSES 12/12, AND NOT YET DISCRIMINATING

Method identical to the baseline **by necessity** -- a two-point comparison requires one method; this is not
a same-command re-run of a peer's claim, it is the second point of `~J`'s own control.
`sha256` over the **full GET body** (never ETag), plus `last_modified` + `etag` per key so the read can tell
*"the publisher re-ran"* from *"insurance moved an AM figure."*

```
BEFORE  12 keys captured 2026-08-25T12:43:52Z by 0.4.0_DS_ClientPlatform~J (commit 4d40f0d1c8)
AFTER   12 keys read     2026-08-26T14:01:53Z by 0.4.0_DS_ClientPlatform~R
  keys ADDED 0 · keys REMOVED 0
  identical 12/12 · moved-in-place 0 · republished 0
```
**No existing 49F AM served figure moved by one byte. The TO's designated falsifier did NOT trip.**

### FINDING 2 -- THE PASS IS CURRENTLY TRIVIAL, AND REPORTING IT AS A CLEAN PASS WOULD MISLEAD

All 12 objects still carry `last_modified` **2026-08-21T15:03-15:04Z**. **The publisher has not re-run at any
point between the BEFORE and the AFTER.** So run the discrimination question the estate's own evidence law
demands -- *could this evidence have come out differently if the claim were false?* **No.** Had the insurance
plane blended straight into an AM figure, these bytes would still be identical, because nothing re-emitted
them. **A control that cannot fail is not evidence yet.**

**AC3's AFTER half acquires its discriminating power only when the publisher next runs -- which is AC4's
emission, still shut.** It should be re-taken AT emission and the current 12/12 treated as a
**NULL-CHANGE BASELINE EXTENSION**, not as the control discharged. `~J` declared this coupling correctly
("the AFTER half cannot exist until something changes"); what is new is that a *partial* change landed
(bronze/silver/gold) which does **not** touch the serve root, so the control now reads GREEN for a reason
unrelated to its subject.

### FINDING 3 -- THE CONTROL IS ONE FIGURE WEAKER THAN DECLARED: 10 INDEPENDENT DIGESTS, NOT 11

`~J` declared *"at most 11 independent figures, not 12"*, collapsing the byte-identical
`timeseries_chart.json` / `timeseries_chart_full.json` pair. **There is a second, undeclared collapse:**
`_manifests/2026-08-20/933dfc1bf6b1.json` and `_manifests/latest.json` are also byte-identical
(`sha256` `bcee438a8f4e80c4`), which is expected -- `latest.json` is a pointer copy.
**12 objects, 10 distinct digests.** Quote **10**. The error is small and runs in the direction that matters:
it makes the control *weaker* than its author believed, and an over-counted denominator is exactly the
defect this project has been catching all week.

---

## GATE 4 -- AC4 EMISSION: GENUINELY STILL SHUT

```
s3://opal-data-portal-v2/platinum/advi/  DENOMINATOR: 12 keys fully walked, 1 page
  insurance-bearing: 0
  child prefixes: platinum/advi/49financial/  (only)
```
**The insurance leaf has not been emitted.** The serve root holds the same 12 AM keys as the baseline.
`~J`'s one-producer determination stands unchanged and needs no re-measurement: `SERVE_BUCKET` /
`SERVE_ROOT` pinned at `d_publisher_port.py:61-62`, every write built as `f'{SERVE_ROOT}/{row[leaf]}'`
at `:466`, and `:530-533` refusing unknown keys -- the writer **cannot** address a foreign key, so a second
producer is unreachable through that path rather than merely discouraged.

**FREEZE HELD:** `2.0.0_SA_COO` 72166 binding 1 froze the MDPF path and forbade invoking the portal
publisher. **I invoked nothing** -- no `d_publisher_port.py`, no dry-run, no nudge. This gate is reported
from **served-key state plus source**, which is exactly what a freeze leaves available. A GET on
`platinum/advi/` is a read and destroys no time-of-day evidence; it is also a different tree from MDPF.

---

## WHAT I DID NOT DO

- **No build.** No bronze/silver landing rebuilt (it exists and is clean).
- **No second producer** -- NEVER#5. A gold producer already exists and is named in the rows.
- **No TO `<status>` edit.** That is the issuer's record fix per 72177 s.4.
- **No instance amendment.** A criterion's status is the ISSUER's ruling; rewriting it at the executing
  seat is scope adjudication in the widening direction, which is the thing `~J` was right to refuse.
- **No emission, no invoke of any publisher.**

## WHAT I RECOMMEND, FOR THE ISSUER'S RE-CUT

1. **AC1 -- close it.** The APPLIED half is satisfied at APPLIED and Rule 17a is controlled clean.
   The TO's AC1 row still names the pre-ruling `silver/insurance_*` grammar; the landed keys follow the
   `5c3410758c` framework ruling. **Row text vs ruling, issuer's call.**
2. **AC2 -- rule on the hollow `account_id` leg before closing.** Rows, grain and forbidden-field census all
   hold. Whether a spine of `relationship_id` + `firm` alone satisfies "every aggregation is a join" is a
   ruling, and `~J`'s certified instance says that leg exists.
3. **AC3 -- do not close on today's 12/12.** Re-take AT emission. Quote 10 independent figures.
4. **AC4 -- still shut,** and it is the only remaining build. It is also frozen-adjacent; I will not touch
   it without both a re-cut and an explicit freeze release.

**Standing by for the re-cut. I have not proceeded past this read.**

-- `0.4.0_DS_ClientPlatform~R`, 2026-08-26
