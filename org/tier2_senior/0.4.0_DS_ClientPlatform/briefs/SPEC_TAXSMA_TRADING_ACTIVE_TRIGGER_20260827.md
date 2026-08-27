# SPEC INPUT — the TRADING-ACTIVE trigger derived from the Tax SMA sheet (D9 / OPAL_TAXSMA)

**For:** `1.0.0_SA_CTO~Z` (D9 registration owner) · **From:** `0.4.0_DS_ClientPlatform~Z`
**Andrew-direct, 2026-08-27 ~20:4xZ, at this seat's terminal — VERBATIM:**

> *"enroll nixon and tracey if they are listed as active in that sheet, there needs to be some kind
> of "trigger" derived from that sheet for actively being traded, assess the sheet and see if you can
> find it and accordingly make a rule based on it, that is what would be part of the spec as well
> that you send to 1.0.0_SA_CTO~Z"*

**Source:** SharePoint `Shared` › `Tax SMA Accounts.xlsx`, sourcedoc `1FE3ACF5-…`, **LastModified
2026-08-26**, read via the Opal gateway 2026-08-27 ~20:3xZ. 12 rows, $30.91M.

---

## 1. THE SHEET HAS NO "ACTIVE" COLUMN — THE TRIGGER IS DERIVED

Columns: `Index · Account Number · Name · Advisor Contact · Strategy · Leverage · AUM (Mn) ·
Divest Securities · Inception Date · Last Trade Date · Traded · Instruction · Comment`.

**MEASURED — three columns coincide EXACTLY on the same five rows:**

```
Traded == "Yes"            -> 5   Chiles · Nixon · Bump · Tracey · Macy
Last Trade Date non-empty  -> 5   THE SAME FIVE  (all 8/5/2026)
Inception Date non-empty   -> 5   THE SAME FIVE
Account Number non-empty   -> 8   A SUPERSET (adds Graff, Draine, Griffin)
```

**The three agree 5/5 and the fourth is deliberately wider.** That separation is the whole design:
*having a key* and *being traded* are different facts, and the sheet distinguishes them.

---

## 2. THE RULE

```
TRADING-ACTIVE(row)  ⟺  row.Traded == "Yes"
                     ∧  row["Last Trade Date"]  is non-empty
                     ∧  row["Inception Date"]   is non-empty

ENROLLABLE(row)      ⟺  TRADING-ACTIVE(row) ∧ row["Account Number"] is non-empty
```

### ⛔ THE REFUSAL ARMS — this is what makes it a control rather than a filter

```
R1  the three TRADING-ACTIVE limbs DISAGREE
      -> REFUSE the row, SURFACE it. Never enroll, never skip silently.
         A Traded="Yes" with no Last Trade Date is a STALE FLAG; the inverse is an
         UNRECORDED TRADE. Both are sheet defects and both must be visible.

R2  TRADING-ACTIVE ∧ Account Number EMPTY
      -> REFUSE. There is no key. `normalize_schwab()` fails loud on fuzzy/last-4 by
         design (PRD ss.2, "non-negotiable"), so a name match is not a fallback.
```

**WHY THREE LIMBS AND NOT ONE.** `Traded` is a human-maintained boolean — an *assertion*.
`Last Trade Date` is a *date* — evidence that can be checked. **Requiring agreement makes the
sheet's own internal consistency the control**; a single-column trigger cannot detect a flag that
went stale, and would enroll or skip on it silently.

### VALIDATION AGAINST THE WORLD

Applying `ENROLLABLE` to the 2026-08-26 workbook yields **exactly 5** rows — and the roster now
holds **exactly those 5** (§3). **Rule output == artifact state, 5 of 5.**

⚠ **BOTH REFUSAL ARMS ARE EMPTY TODAY (R1: 0 rows, R2: 0 rows).** Stated plainly because **a rule
whose refusal arm has never fired is untested** — the first violation would also be its first
exercise. A build should ship with a planted-row fixture for each arm.

---

## 3. WHAT I EXECUTED ON HIS WORD

His condition was *"if they are listed as active in that sheet."* Both satisfy `TRADING-ACTIVE`
(Traded=Yes, Last Trade 8/5/2026, Inception 8/5/2026) and carry account numbers. **Enrolled.**

```
roster BEFORE  1,645 B  2026-07-21  3 accounts
roster AFTER   3,027 B  2026-08-27T20:50:18Z  5 accounts   (verified by re-read from S3,
                                                            not from the tool's self-report)
  0027265115  Chiles   bd=22596361  active              (unchanged)
  0035940058  Bump     bd=None      pending_resolution  (unchanged)
  0091939812  Macy     bd=None      pending_resolution  (unchanged)
  0084073310  Nixon    bd=None      pending_resolution  <- NEW, enrolled_by /tax-newacc
  0076459710  Tracey   bd=None      pending_resolution  <- NEW, enrolled_by /tax-newacc
```

### ⛔ THEY ARE `pending_resolution`, NOT `active`, AND THAT IS A NAMED EGRESS BLOCK

Dry-run first, per the skill's own mandate. Both returned `resolution_gated`:

> *"not in `dim_account_xref` (zero-egress tier-1 exhausted); tier-2 sanctioned surface **PROVEN
> masked-last-4/no-exact-filter** 2026-07-21; the exact full number is ONLY on `account-api/*`
> (tier-3, **NEW egress**) -> needs Andrew's **account-api egress-word extension (PRD D3)**"*

**POSITIVE CONTROL:** the same command on Chiles returns `would_enroll_active`, `resolved EXACT
(tier=xref) bd_internal_id=22596361`. **The resolver works; Nixon and Tracey are genuinely absent
from the xref.**

⛔ **I did NOT spend an egress word.** Andrew's earlier *"(egress permitted)"* was scoped to finding
the tax accounts — which needed no egress at all. **Activating these two needs a DIFFERENT, named
grant (`account-api`, tier-3, PRD D3), and stretching one grant to cover another surface is exactly
what "availability is not authorization" forbids.** That is an ask for him, not an inference.

---

## 4. FOR THE SPEC — WHAT THE TRIGGER IMPLIES ABOUT THE PIPELINE

1. **It must be RE-EVALUATED, not run once.** Measured between the `20260805` snapshot and the
   current sheet: **Draine and Griffin gained account numbers** that were blank before. **Rows cross
   the ENROLLABLE boundary over time** — a one-shot import would have missed both.
2. **The 4 keyless rows are the inflow, not noise.** Lindsey, Ashok, Genender, TEPEYEC are
   `awaiting account opening`. R2 refuses them correctly *today*; they are the population the
   re-evaluation exists to catch.
3. ⚠ **ENROLLMENT IS NOT YET FLOW.** The skill states the ETL includes an enrolled account *"once
   the WS-R3 registry-read producer is deployed."* **I have not verified WS-R3's deploy state.**
   So Nixon and Tracey are now *recorded*, which is strictly better than invisible — but **do not
   read this as "they are in the pipeline."**
4. ~~**The strategy grain defect stands and should be settled in the same spec** — the sheet carries
   SMA 145 (45% leverage) and SMA 200 (100%); the roster carries the single string
   `"Opal Tax SMA 200/145"` on every entry... Rule 24(ii).~~
   ⛔ **DISSOLVED 2026-08-27 ~20:5xZ BY ANDREW-DIRECT, VERBATIM:** *"They are all meant to be rolled
   up into tax, not two diff strategies or deeper drills/leaves."* **THERE WAS ONLY EVER ONE
   STRATEGY.** The workbook's `SMA 145` / `SMA 200` are a **LEVERAGE ATTRIBUTE of one strategy**, not
   two strategies, and *"deeper drills/leaves"* explicitly refuses a level beneath Tax.
   **The roster's single `strategy` value is CORRECT AS IT STANDS.** No split, no row migration, and
   `taxsma_newacc.py:23`'s `DEFAULT_STRATEGY` needs no change on grain grounds.
   ⛔ **A trigger reading `Strategy` therefore surfaces ONE value into a field that holds one** —
   the opposite of what this item claimed. **Struck rather than deleted so a reader of the earlier
   draft sees it was ANSWERED, not dropped.**
   *(No successor finding is raised. The `Leverage` column exists and the roster does not carry it;
   manufacturing a new finding out of a dissolved one is its own defect — `1.0.0_SA_CTO~Z`, 10046.)*

---

## 5. BOUNDS AND LANE

- **Sheet vintage 2026-08-26.** A live spreadsheet can change under this rule; the coincidence in §1
  is measured at that vintage and is not eternal.
- **`Traded` semantics are inferred from co-occurrence, not from a data dictionary.** No document
  defines the column. The three-limb agreement is what makes the inference safe, not certainty about
  the author's intent.
- ⚠ **RULE 27 / LANE:** this seat is seated **D1_CATVIEWS ONLY**. The enrollment and this spec are
  **D9 / OPAL_TAXSMA** work, executed on **Andrew's direct instruction at this terminal**, which is
  sovereign and overrides seating. **Surfaced, not adjudicated** — `2.0.0_SA_COO~Z` holds seating and
  `1.0.0_SA_CTO~Z` holds D9 registration, and neither was asked by me before acting on his word.
