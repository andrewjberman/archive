# TO ETFS_POSITIONING.TO-11-DE — the POSITIONING page defaults to `INT` for a FIRST-VISIT viewer

<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — `ETFS-f-2` (**the hardcoded `'UST'` model-list sites inside the plane**, DE-measured with exact `file:line`) and `ETFS-f-3` (**Models-mode BYTE-IDENTICAL**, cited as a CONSTRAINT). **NO new cell.**</decomp_ref>
<certification>Decomp CERTIFIED. No cell added. ⚠ **`ETFS-f-3` is cited on its stated ORACLE and not on a wider reading:** that cell's own premise oracle is *"byte-diff Models-mode **payload** pre/post"* — it constrains the **PAYLOAD**, not which book the UI pre-selects. **A default-selection change is therefore NOT a violation of `f-3`, and `AC5` makes that explicit rather than leaving it to a reader.**</certification>
<issued_to>0.4.0_DE_ClientPlatform~C</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>SEATED — **same project, same instance, Rule 27 satisfied.** That lane holds `ETFS_POSITIONING` (`TO-7` AC4/AC5), **is reading this exact page tree right now**, and located this TO's site at a cost of one grep. ⭐ It explicitly declined to act without a TO — *"I am NOT taking item 4 — no TO seats it to me and the cut is `2.0.0_SA_COO~Z`'s"* — which is correct and is why this exists.</seating_trigger>
<placement>SITE Z (Rule 26). `portal/` is a WORK-SITE. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T04:3xZ</issued>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_POSITIONING_TO7_TO11DE_CERTIFICATION_20260828.md` @`37a69dcdf7`, verdict **CERTIFIED -- 6 of 6**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**</status>
<priority>P1 — a sovereign add-on to the Positioning page, small and well-specified. **Below `ETFS_SATELLITES.TO-10-DE`, which is the D4 smoke-test distance.**</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~04:2xZ, VERBATIM** (relayed `1.0.0_SA_CTO~Z` 12753):

> *"Another rule i want to focus on is a simple add on for positioning page as a whole, the default when a user goes to  thatpage should be the \"INT\" Intermediate Term model being selected, not UST."*

**ANDREW-DIRECT ~04:3xZ, VERBATIM, ANSWERING THE SCOPE FORK** (relayed 12788):

> *"(a) new users first visit onluy"*
</authority>

---

## 1. THE SCOPE, SETTLED — AND WHAT IS NOT BEING TOUCHED

>> **NEW USERS / FIRST VISIT ONLY. A RETURNING VIEWER KEEPS THEIR REMEMBERED CHOICE.**

⛔ **HIS 2026-08-24 REMEMBERED-CHOICE RULING STANDS INTACT AND IS NOT REVERSED.** `defaultBook()`'s **LAYER 1 IS UNTOUCHED.** Nobody edits it, nobody weakens it, and **nobody treats persistence as a defect to be engineered around** — it is his product rule and it survives this change unchanged.

**The change is confined to the NO-REMEMBERED-CHOICE path.**

## 2. THE SITE, MEASURED

Located by `0.4.0_DE_ClientPlatform~C` (12767) and `0.4.0_DE_ClientPlatform~Z`:

```
portal/src/pages/Positioning/tabs/HoldingsTab.tsx:~694-699
  const bookStorageKey = `positioning:book:${bookMode}`
  const defaultBook = () => {
    const remembered = readPersistedToggle(bookStorageKey, books)          <- LAYER 1  remembered
    if (remembered && bookStatus[remembered] !== 'book_only') return remembered
    return books.find((b) => bookStatus[b] !== 'book_only') ?? books[0] ?? ''
                 ^ LAYER 2  first book that CARRIES ROWS      ^ LAYER 3  books[0]
  }
```

⭐ **THE DEFAULT IS NOT DECLARED ANYWHERE. IT FALLS OUT OF ARRAY ORDER** — `UST` is simply the first member of `MODEL_BOOKS` that carries rows. **Declaring a default is an improvement on the current state independently of which book he picked.**

## 3. ⛔ THREE TRAPS, EACH FOUND BY A DIFFERENT SEAT — DO NOT REDISCOVER THEM

**(A) DO NOT REORDER `MODEL_BOOKS`.** `bookSet.ts:78` — `['UST','ST','INT','LT','ULT']`. Moving `'INT'` to the front is the first thing a seat reaches for and **it SILENTLY MISALIGNS EVERY BLENDED CELL**: `customBlend.ts:27-41` builds each row against that array's order. ⛔ **Change the DEFAULT, never the ARRAY ORDER.**

**(B) A BARE `return 'INT'` REINTRODUCES A DEFECT SOMEONE DELIBERATELY FIXED.** The current default is **not** `books[0]` — it is *"the first book that CARRIES ROWS"*. **An unconditional `'INT'` would select a book that may hold no rows**, which is the exact condition Layer 2 exists to prevent.

**(C) ⛔ LAYER 2 SITS ABOVE `books[0]` AND CAN SHORT-CIRCUIT BEFORE `INT` IS EVER REACHED.** A default expressed only as a Layer-3 fallback **will not produce his outcome** — Layer 2 returns `UST` first whenever `UST` carries rows, which is the normal case. **The preference must be expressed at or above Layer 2, and it must still respect the carries-rows condition (B).**

## 4. ⛔ THE VERIFICATION TRAP — THE TEST PROVES NOTHING AGAINST A WARM BROWSER

```
  FALSE FAIL   storage holds UST -> viewer sees UST after a CORRECT fix -> reads broken,
               gets investigated, costs time.                                  RECOVERABLE.
  FALSE PASS   storage already holds INT -> viewer sees INT WHETHER OR NOT THE FIX LANDED
               -> reads as done, CLOSES THE ITEM, nobody looks again.          DANGEROUS.
```
>> ⭐ **A FALSE FAIL GETS INVESTIGATED. A FALSE PASS ENDS INQUIRY.** The persistent toggle makes the page **incapable of discriminating in either direction** against a warm profile.

## 5. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T11DE-AC1` | **A FIRST-VISIT VIEWER WITH NO STORED SELECTION LANDS ON `INT`.** ⛔ **Verified on a CLEARED profile (or a fresh/private one), and the report STATES the profile state.** *"Verified on a cleared profile"* is the evidence; a run against a warm browser is not evidence and must not be reported as a pass. | `ETFS-f-2` | |
| `T11DE-AC2` | ⛔ **A RETURNING VIEWER'S REMEMBERED CHOICE IS UNCHANGED.** Set a book, reload, get that book. **Layer 1 is byte-untouched** — cite it. **His 2026-08-24 remembered-choice ruling is not reversed by this TO and must be exhibited as still holding.** | `ETFS-f-2` | |
| `T11DE-AC3` | ⛔ **`MODEL_BOOKS` ORDER IS UNCHANGED.** `bookSet.ts:78` still reads `['UST','ST','INT','LT','ULT']`. **Show the array is byte-identical** — the blended-cell alignment in `customBlend.ts:27-41` depends on it and the misalignment would be SILENT. | `ETFS-f-2` | |
| `T11DE-AC4` | **THE CARRIES-ROWS CONDITION SURVIVES.** If `INT` holds no rows in a given mode, the viewer must NOT land on an empty book — the existing *"first book that carries rows"* behaviour still governs. **Name what happens in that case.** | `ETFS-f-2` | |
| `T11DE-AC5` | **MODELS-MODE PAYLOAD IS BYTE-IDENTICAL.** `ETFS-f-3`'s own oracle — *byte-diff Models-mode payload pre/post*. ⚠ **This TO changes which book is PRE-SELECTED, not what is served; exhibit that the payload did not move.** | `ETFS-f-3` | |
| `T11DE-AC6` | **RENDERED, NOT GREPPED.** Read screenshots: a cleared-profile first visit landing on `INT` · a returning profile keeping its remembered book. ⚠ **THE CANVAS IS SILVER.** | `ETFS-f-2` | |

## 6. NOT YOURS

- ⛔ **`MODEL_BOOKS` order** — see AC3. **Change the DEFAULT, never the ARRAY.**
- ⛔ **`defaultBook()` LAYER 1 / the persistence mechanism** — Andrew's standing ruling, untouched.
- ⛔ **`ETFS_SATELLITES.TO-10-DE`** (Satellite 98 hide, firm selector, colour gradient) — `0.4.0_DE_ClientPlatform~S`, different project. **Rule 27.**
- **The PROD promote** — DT lane, Rule 19, held at Andrew's word.

## 7. ⚠ A SCOPING CALL THIS OFFICE MADE, STATED SO IT CAN BE CHEAPLY OVERTURNED

Andrew said *"positioning page as a whole"*, which is **broader than the `ETFS_POSITIONING` project**. I have homed it here because `ETFS-f-2` is the cell that already owns the hardcoded `'UST'` sites in this plane, and because that keeps one lane on one page tree.

>> **`1.0.0_SA_CTO~Z`: if item 4 warrants its own directive registration rather than riding `ETFS_POSITIONING`, say so and this office re-homes it.** **The work is not held pending that answer** — the criteria do not change with the project label.

## 8. REPORTING

Deliverable + read screenshots + proof instance in this lane's `deliverables/`, via `.tools/safe-commit.sh --author "0.4.0_DE_ClientPlatform~C <0.4.0_DE_ClientPlatform~C@opal.agent>" -F <msgfile>` (message file by a **non-shell** writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt, then report.**

<proof_of_spec>
  <criterion id="T11DE-AC1" cell_refs="ETFS-f-2"/>
  <criterion id="T11DE-AC2" cell_refs="ETFS-f-2"/>
  <criterion id="T11DE-AC3" cell_refs="ETFS-f-2"/>
  <criterion id="T11DE-AC4" cell_refs="ETFS-f-2"/>
  <criterion id="T11DE-AC5" cell_refs="ETFS-f-3"/>
  <criterion id="T11DE-AC6" cell_refs="ETFS-f-2"/>
  <expected_criteria>T11DE-AC1,T11DE-AC2,T11DE-AC3,T11DE-AC4,T11DE-AC5,T11DE-AC6</expected_criteria>
  <alignment_denominators>cells declared: 2 (ETFS-f-2, ETFS-f-3); criteria: 6. FORWARD — 6 of 6 carry >=1 cell_ref. BACKWARD — 2 of 2 reachable (ETFS-f-2 from AC1/AC2/AC3/AC4/AC6, ETFS-f-3 from AC5). Unmapped 0; untraceable 0. NOTE: no cell is added. ETFS-f-3 is cited on its OWN stated oracle — byte-diff Models-mode PAYLOAD pre/post — and therefore as a CONSTRAINT that a default-selection change must not violate, NOT as a prohibition on changing the default: the cell governs what is served, not which book the UI pre-selects, and conflating the two would have read this TO as barred by its own decomp. AC4 exists because the current default is "first book that CARRIES ROWS" rather than books[0], so an unconditional INT would reintroduce a condition someone deliberately fixed.</alignment_denominators>
</proof_of_spec>
