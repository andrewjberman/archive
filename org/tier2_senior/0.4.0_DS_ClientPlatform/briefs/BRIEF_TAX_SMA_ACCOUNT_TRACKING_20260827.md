# BRIEF — TAX SMA ACCOUNT TRACKING: the roster covers 3 of 12, and 2 TRADED accounts are unenrolled

**For:** `1.0.0_SA_CTO~Z` · **From:** `0.4.0_DS_ClientPlatform~Z` (D1_CATVIEWS DS lane)
**Requested by:** Andrew, 2026-08-27 ~20:3xZ, at this seat's terminal — *"I think there are more
accounts than that we need to track them through here, probably need some kind of pipeline strategy
to manage this... Check it out and write a brief on the subject for CTO~Z."*
**Status:** BRIEF / INPUT. Not a registration, not a self-assignment, not a proposal to build.
**Every figure below is measured; sources and vintages stated.**

---

## 1. THE TWO SOURCES, AND THEY DISAGREE

| | source | vintage | population |
|---|---|---|---|
| **A** | `s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json` | LastModified **2026-07-21**, 1,645 B | **3 entries** |
| **B** | SharePoint `Shared` › `Tax SMA Accounts.xlsx` (Andrew's link; sourcedoc `1FE3ACF5-…`) | LastModified **2026-08-26**, 15,750 B | **12 accounts, $30.91M** |

**A is the CONTROL ARTIFACT the production Lambda reads at runtime** — `taxsma_registry.py` is
imported by `opal-assets-bd49f-reporting-pull`'s `discover_accounts()`. **B is where the business
actually maintains the list.** They are 5 weeks apart and they do not reconcile.

---

## 2. THE RECONCILIATION — measured, keys normalised per `normalize_schwab()` (digits, zfill 10)

Of the **12** workbook rows: **8 carry an account number**, **4 do not** (*"awaiting account opening"*).
Of those **8**, the roster holds **3**.

| workbook account | name | strategy | traded | in roster? |
|---|---|---|---|---|
| …5115 | Chiles | SMA 145 | **Yes** | ✅ `active` |
| …0058 | Bump | SMA 145 | **Yes** | ⚠ `pending_resolution` |
| …9812 | Macy | SMA 145 | **Yes** | ⚠ `pending_resolution` |
| …3310 | Nixon | SMA 145 | **Yes** | ⛔ **ABSENT** |
| …9710 | Tracey | SMA 145 | **Yes** | ⛔ **ABSENT** |
| …4809 | Graff | SMA 200 | No | ⛔ ABSENT |
| …8743 | Draine | SMA 200 | No | ⛔ ABSENT |
| …4632 | Griffin | SMA 145 | No | ⛔ ABSENT |
| (none) ×4 | Lindsey, Ashok, Genender, TEPEYEC | — | No | n/a — no key exists yet |

> ⛔ **THE HEADLINE: 5 of 5 accounts that have actually TRADED are in the workbook; the roster knows
> 3 of them, and only 1 of those 3 is `active`.** **Nixon and Tracey are trading and enrolled
> nowhere.** Bump and Macy are enrolled but `bd_internal_id: null`, so they do not resolve to a BD id.

*(Accounts shown last-4 deliberately. ⛔ **Last-4 is NOT a key** — `normalize_schwab()` fails loud on
a fuzzy/last-4 input by design, PRD ss.2 "non-negotiable". The authoritative values are in the
workbook and the roster.)*

---

## 3. IT IS GROWING, AND THE SCHEMA IS DRIFTING WITH IT

A second workbook exists — `Tax SMA Accounts 20260805.xlsx`, titled **"Opal Tax SMA Pipeline"** —
i.e. **the business is already versioning this by filename.** Delta over 21 days:

```
2026-08-05   11 accounts   $27.71M   11 columns   account numbers MASKED (XXXX-5115)
2026-08-26   12 accounts   $30.91M   13 columns   account numbers UNMASKED (2726-5115)

  +1 account  TEPEYEC Ltd. ($3.20M)      -> and 27.71 + 3.20 = 30.91, reconciles to the cent
  +2 keys     Draine and Griffin gained account numbers (were blank on 08-05)
  +2 columns  "Divest Securities", "Instruction"
```

⭐ **The masking flip is the part worth noticing:** the 08-05 copy masked account numbers and the
current one does not. **A hand-maintained artifact changed its disclosure posture between versions**,
which is a governance fact, not a formatting one.

---

## 4. WHY THIS IS A PIPELINE PROBLEM AND NOT A DATA-ENTRY PROBLEM

1. **The control artifact is stale by construction.** Enrollment is a manual `/tax-newacc` act into
   an S3 JSON; the business list lives in SharePoint. **Nothing reconciles them, so the gap can only
   grow** — and it has, silently, to 5 of 8.
2. **The failure is invisible on the served surface.** An account absent from the roster is simply
   not discovered by `discover_accounts()`. **There is no error** — the ETL runs clean over a short
   list. *(This is the estate's recurring shape: absence that produces no signal.)*
3. **`pending_resolution` is not a queue.** Two accounts have sat unresolved while trading. Nothing
   retries the schwab# → BD-id xref, and nothing reports the backlog.
4. **Versioning by filename is the tell.** A dated copy beside a live copy is what people do when
   there is no system of record.

---

## 5. ~~A TAXONOMY DEFECT WORTH RULING ON — the roster collapses two strategies into one~~
## 5. ⛔ DISSOLVED — THERE WAS ONLY EVER ONE STRATEGY

> **ANDREW-DIRECT 2026-08-27 ~20:5xZ, VERBATIM:** *"They are all meant to be rolled up into tax, not
> two diff strategies or deeper drills/leaves."*

**Tax is ONE strategy.** `SMA 145` / `SMA 200` are a **LEVERAGE ATTRIBUTE** of it, not two
strategies, and *"deeper drills/leaves"* refuses any level beneath Tax. **The roster's single
`strategy` value is CORRECT**, D1's registry carrying `tax` as one L1 member is **CONFIRMED, not
changed**, and no migration exists to perform. The section below is preserved struck-through, because
a reader of the earlier draft should see the claim was **ANSWERED, not quietly dropped**.
*(No successor finding raised — see `1.0.0_SA_CTO~Z` 10046.)*

### ~~(struck) the original claim~~

```
WORKBOOK   "SMA 145"  (leverage 45%)   x7        <- two DISTINCT strategies
           "SMA 200"  (leverage 100%)  x5
ROSTER     strategy = "Opal Tax SMA 200/145"     <- ONE string, on all 3 entries
```

**The roster's `strategy` field carries one value where the source carries two, and the leverage
differs 45% vs 100%.** That is a **Rule 24(ii) SAME GRAIN** problem: the field's declared domain is
"strategy", and `"200/145"` is not a strategy — it is the *union of two*.

**Consequence for D1_CATVIEWS, which is why this reaches my lane:** the registry carries `tax` as a
**single** SMA L1 member (`SMA_MEMBERS`, `strategy_id='tax'`). Andrew's 08-26 layering names L1 SMAs
as **Tax · Muni · DIVZ · PFOE** — also one `Tax`. **So if SMA 145 and SMA 200 must ever be
distinguished on the page, neither the roster nor the registry can express it today.** I am not
asserting they must — **that is a taxonomy question for `1.0.0_SA_CTO~Z` and Andrew**, and it should
be answered before the SMA L1 node gains dollars under the scope-B contract change, not after.

---

## 6. WHAT I AM **NOT** CLAIMING

- **I have not traced whether D1's SMA `tax` dollars flow through this roster.** The registry resolves
  `tax` as a member; whether its AUM path consumes `taxsma_roster.json` is **UNMEASURED**.
- **I have not established that the workbook is authoritative.** It is where the business maintains
  the list; no ruling names it a system of record.
- **No egress was spent.** Andrew granted it (*"egress permitted"*); the roster came from our own S3
  and the workbook from our own M365 tenant via the Opal gateway. **The grant is unused.**
- ~~**I did not modify anything** — no enrollment, no roster write, no workbook edit.~~
  ⛔ **SUPERSEDED ~20:4xZ — TRUE WHEN WRITTEN, FALSE NOW.** Andrew subsequently instructed
  *"enroll nixon and tracey if they are listed as active in that sheet"*, and this seat **DID
  enroll both**: roster **3 → 5 entries**, 1,645 B → 3,027 B, `LastModified 2026-08-27T20:50:18Z`,
  verified by re-read from S3. Both landed `pending_resolution` (a named tier-3 egress block, not a
  failure — see `SPEC_TAXSMA_TRADING_ACTIVE_TRIGGER_20260827.md` §3). **The workbook was not
  touched.** Struck rather than edited in place so the brief's original state stays legible.

---

## 7. THE DECISION THIS BRIEF IS FOR

`1.0.0_SA_CTO~Z` owns whether this becomes a build. The shapes, stated neutrally:

| | shape | cost | what it does not fix |
|---|---|---|---|
| **(a)** | Reconciliation **report** only — diff workbook vs roster, surface the gap | small; read-only | does not enroll anything; gap persists until someone acts |
| **(b)** | **Ingest the workbook** as the upstream of record, roster becomes derived | medium; needs a Graph read in the pipeline + a resolution retry | makes a hand-edited spreadsheet load-bearing |
| **(c)** | Keep manual enrollment, add a **`pending_resolution` retry + backlog report** | small | does not close the 5 fully-absent accounts |

⚠ **(a) and (c) compose and neither requires ruling the workbook authoritative** — that is the
observation I would offer, not a recommendation. **The one thing I would flag against is doing
nothing about the two TRADED-but-unenrolled accounts**, which is a live gap rather than a design
question.

⛔ **And the moratorium binds:** a reconciliation report is a **monitor**, and CLAUDE.md forbids
building one *"unless Andrew explicitly asks."* He asked for a **brief**, not a monitor. **Any of the
three shapes above needs his word before it is built**, and this brief does not substitute for it.
