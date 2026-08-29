# TO ETFS_POSITIONING.TO-13-DS — STOP THE UPSTREAM COERCION STRIPPING LEADING ZEROS OFF CUSIPs

<id>ETFS_POSITIONING.TO-13-DS.identifier-coercion-strips-leading-zeros</id>
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md -- cells ETFS-a-1, ETFS-a-5, ETFS-d-1</decomp_ref>
⛔ **THE FIRST CUT OF THIS FACE CLAIMED "NO CELL CLAIMED -- NO HONEST CELL REFERENCE EXISTS" AND THAT WAS FALSE. Corrected by the issuer before the face landed; recorded because the reasoning was plausible and wrong.** I reasoned that a 2026-08-21 round-1 decomp could not cover a defect measured on 2026-08-29, copied the disclosure pattern from `ETFS_INGEST.TO-9-DS`, and never opened the decomp. **`safe-commit` refused the commit and its refusal text said the thing I needed to hear: *"If no decomp exists yet, that is a PIPELINE FAILURE TO SURFACE to COO/CTO, not a reason to cut the TO without one."* I had asserted the antecedent without checking it.**
⭐ **THE CELLS ARE REAL AND THEY ARE EXACT.** `ETFS-a-1` IS `silver/holdings/{date}.parquet` — *"the WEIGHTS, already ours"*, DS-class — **which is the very artifact carrying `cusip=2824100`.** `ETFS-a-5` is `bbg/{date}/`, the L1 landing prefix whose `history_topup` lost the ABT row. `ETFS-d-1` is the producer, *"BUILT against the bbg/{date}/ CONTRACT"* (DECOMP §3.1), which is what emits the served gold. **A cell names an OPERATIVE SURFACE, not a date — an eight-day-old decomp covers a defect found today whenever the defect lives on a surface it enumerated.** That is what I got wrong, and it is the general form.
⚠ **A DECOMP-REF ARMS ALIGNMENT ENFORCE in `proof-of-spec-check.py:24,161`. THAT IS CORRECT HERE AND IS WHY `ETFS_INGEST.TO-9-DS` IS NOT A PRECEDENT FOR THIS FACE:** that TO had genuinely no cell, so its element was absent by necessity and its enforcement would have been vacuous. **This face has three real cells, so enforcement is a feature.** ⛔ **NEVER fabricate `cell_refs` to satisfy the gate — that yields a VALID-READING INSTANCE THAT LIES. The remedy for a missing cell is to SURFACE the pipeline gap, never to invent a reference or to reach for the override.**

<issued_to>(unassigned -- UNSEATED BY DESIGN AT CUT TIME; see section 0 for the seating note and why no serial belongs in this field yet)</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-29T12:4xZ</issued>
<status>**PENDING — CUT WITH THE DEFECT FULLY CHARACTERIZED AND ONE LINK DELIBERATELY UNEXERCISED.** The finding, the mechanism, the blast radius and both rival explanations are all MEASURED and recorded in `org/projects/ETFS_POSITIONING.json` `blocking` (the NAMED PRIMARY CARRIER; commits `9ebcd31a3a`, `6bac9a3680`, `dc57db85c5`, `0d5f5a8e2e`). ⛔ **WHAT IS NOT MEASURED AND MUST NOT BE MEASURED BY THIS FACE: `/sedol/2824100` has NOT been run against Bloomberg. That is a VENDOR CALL and needs Andrew's explicit per-use word, which nobody has asked for and which this TO does NOT request — the scheduled pull exercises it for free.** So "the sedol query returns nothing for ABT" is **STRONGLY EVIDENCED AND UNEXERCISED**, and is deliberately NOT called a root cause under Rule 22. ⚠ **A SEAT PICKING THIS UP MUST NOT UPGRADE THAT LANGUAGE WITHOUT EITHER THE SOVEREIGN WORD OR A SCHEDULED-RUN OBSERVATION.**</status>
<priority>P2 — a real served defect on a real position, bounded to one holding by enumeration, and not urgent enough to spend a vendor call on. **It is wrong-valued, not wrong-looking** (contrast `ETFS_INGEST.TO-9-DS`), which is why it is not P3; it is one row of 187, which is why it is not P1.</priority>

<authority>
No sovereign word. Cut by `2.0.0_SA_COO~Z` under the **D1+D4 scoped `/drive` arm** (Andrew-direct
2026-08-28 ~02:3xZ at the COO~Z terminal, VERBATIM: *"you just need to keep the fabric discipined
and proceed through D1 and D4 TO completion. No distractions, pure execution, if there are issues
they go to surprise-channel and CVO investigates."*).

⚠ **THIS IS AN ISSUE THAT WENT TO INVESTIGATION AND CAME BACK RESOLVED**, which is the arm working
as written: `3.0.0_SA_CVO~Z` and `0.4.0_DS_ClientPlatform~Z` characterized it across msgs 16710 /
16712 / 16715 / 16718 / 16721 / 16723 / 16726 / 16728 / 16744, **both correctly declined the remedy
under Rule 27**, and handed it to whoever holds `ETFS_POSITIONING`. This face is that hand-off
landing. **Neither of those lanes carries this further.**
</authority>

## 0. SEATING -- UNSEATED BY DESIGN, AND THE `issued_to` FIELD IS DELIBERATELY SERIAL-FREE

⛔ **THIS FACE IS UNSEATED AT CUT TIME, 2026-08-29 ~12:4xZ. That is not an oversight.** Every
existing Tier-2 lane is Rule-27 encumbered:

```
  0.4.0_DS_ClientPlatform~Z   holds D1_CATVIEWS TO-M1-DS + TO-N1-DS      LIVE, encumbered
  0.7.0_AE_CloudOps~Z         holds D1_CATVIEWS TO-P1-AE                 LIVE, encumbered
  0.4.0_DS_ClientPlatform~Q   holds ETFS_INGEST.TO-9-DS                  DEAD (INFERRED), encumbered
  0.7.0_AE_CloudOps~I         holds ETFS_INGEST.TO-10-AE                 DEAD (INFERRED), encumbered
```

**One instance is one project, so this face needs a FRESH DS-class lane.** The issuer
(`2.0.0_SA_COO~Z`) holds spawn/seat authority per Andrew 2026-08-28 15:32Z and is batching one
seating pass at ~13:0xZ covering this face plus the two ETFS_INGEST faces, rather than running three
pre-flights separately.

⚠ **THIS WORK IS FIRE-INDEPENDENT.** Unlike the two ETFS_INGEST faces it does **not** wait on the
13:00Z `etf-positioning-producer-daily` run — the defect is already measured and the fix is in code.
It is unseated for batching, not because anything gates it.

⛔ **AND THE FIELD IS SERIAL-FREE ON PURPOSE — THE FIRST VERSION OF IT WAS NOT, AND THAT WAS A
DEFECT THE ISSUER CAUGHT ON ITS OWN FACE.** The seating note originally lived inside `<issued_to>`;
`to-check` renders the FIRST serial-shaped token it finds there, so the face rendered
**`-> SA_COO~Z`** — the issuer, as executor. **A face that renders the COO as its own assignee is a
lane violation on its face, and it is WORSE than one rendering `(unassigned)`**, because
`(unassigned)` announces itself and a plausible-but-wrong serial does not. Same class as
`ETFS_INGEST.TO-7` carrying an executor CLASS and no instance for three days while every other field
looked complete. **Prose about seats goes in a SECTION; only the assignee goes in the field.**

## 1. THE DEFECT, ON THE SERVED PLANE

`gold/holding/date=2026-08-27/holding.parquet` — the newest gold partition (`gold/book/` and
`gold/holding/` both stop at 08-27), 45,692 bytes, size matched against `s3api` before read.

```
  189 rows . 169 distinct ticker . 31 columns
  NON-NULL WINDOW COUNT, DENOMINATOR 189 ROWS -- BIMODAL AND EMPTY BETWEEN:
     8 of 8 non-null : 183 rows
     0 of 8 non-null :   6 rows      NOTHING PARTIAL
```

**Every one of the six, enumerated — this IS the population, not a sample:**

```
  ABT       Abbott Laboratories       DIVZ  w=2.36   is_cash=False  price=114.1
  CASH      Cash & Cash Equivalents   DIVZ  w=0.23   is_cash=True
  CASH      Cash & Cash Equivalents   IDVZ  w=0.53   is_cash=True
  CASH      Cash & Cash Equivalents   PFDE  w=0.03   is_cash=True
  CASH      Cash & Cash Equivalents   PFOE  w=-0.02  is_cash=True
  2602335D  TPG Inc                   PFDE  w=0.00   is_cash=False  price=0.0
```

>> ⛔ **FOUR OF THE SIX ARE CASH AND ONE IS A ZERO-WEIGHT ZERO-PRICE PLACEHOLDER. ABT IS THE ONLY
REAL PRICED HOLDING IN THE ESTATE WITH ALL EIGHT RETURN WINDOWS NULL — 2.36% of DIVZ, priced 114.1.** <<

## 2. THE MECHANISM — MEASURED AT SOURCE, AND THE BUCKET IS STRUCTURALLY AMBIGUOUS

`silver/holdings/2026-08-28.parquet`, 187 rows: **ABT's stored `cusip` is `2824100` — SEVEN
characters. Abbott Laboratories' CUSIP is `002824100`. TWO leading zeros stripped by numeric
coercion upstream.**

`integrations/bloomberg/pipeline/etf_daily_pull.py:96-102` @`6bac9a3680` routes by LENGTH:

```
  len(c) == 9   ->  "/cusip/" + c
  len(c) == 8   ->  "/cusip/0" + c     # pads ONE zero -- "leading zero stripped upstream"
  len(c) == 7   ->  "/sedol/" + c      # <-- ABT LANDS HERE
```

**THE WHOLE 7-CHAR BUCKET, ENUMERATED, DENOMINATOR 187:**

```
  DIVZ  ABT  2824100   digits_only=True    a CUSIP MINUS TWO ZEROS. MIS-ROUTED.
  IDVZ  ICT  6455819   digits_only=True    a GENUINE SEDOL
  IDVZ  MER  B247XZ6   digits_only=False   a GENUINE SEDOL
```

>> ⛔⛔ **THE SAME 2026-08-25 SWITCH TO IDENTIFIER-QUERY ADDED ICT AND MER AND DROPPED ABT, OUT OF
ONE LENGTH BUCKET, BY ONE RULE.** ICT and MER are the function's OWN docstring examples, verified on
the live terminal 2026-08-25 (`/sedol/6455819` -> INTL CONTAINER TERM SVCS px 949; `/sedol/B247XZ6`
-> MANILA ELECTRIC px 479). **The change was RIGHT for two of the three and wrong for the third.** <<

⛔ **`isdigit()` DOES NOT SEPARATE THEM** — ABT `2824100` and ICT `6455819` are both all-digits.
**THERE IS NO PURELY LEXICAL FIX INSIDE THE 7-CHAR BUCKET.** The docstring already calls fixing the
coercion at source *"a separate, better fix"*; this measurement makes it the **only** sound one.

⭐ **AND THE PAD MECHANISM IS NOT BROKEN — the 8-char bucket is four rows and all four are correct:**
`AEP 25537101 . AIG 26874784 . ATO 49560105 . BP 55622104`, each a CUSIP minus ONE zero, each padded
right. **ABT is the SINGLE row in 187 where stripping went one digit further than the pad
anticipates.** Blast radius bounded BY ENUMERATION, not estimate.

## 3. THE DATA WAS CONSTANT; THE CODE MOVED

`silver/holdings/{date}.parquet` cusip LENGTH histogram, denominator per date:

```
  2026-08-21   114 rows   {9:111, 10:2, 12:1}              <- NO 7-char, NO 8-char rows
  2026-08-24   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-25   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-26   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-27   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
  2026-08-28   187 rows   {7:3, 8:4, 9:177, 10:2, 12:1}
```

**IDENTICAL FROM 08-24 ONWARD. ABT's cusip was 7-char THE DAY IT FIRST APPEARED and was never
9-char — the coercion defect PREDATES the 08-25 change, which merely walked into it.**
**CORROBORATED ON A SECOND PLANE:** ABT HAD a `history_topup` row on 08-24 (return `0.0257`) with the
7-char cusip ALREADY stored. On 08-24 the fetch did not depend on that identifier; on 08-25 it did.

⛔ **BOTH BENIGN EXPLANATIONS ARE DEAD BY MEASUREMENT, and each was hunted deliberately:**
`0.4.0_DS_ClientPlatform~Z` killed *"it was sold"* (ABT present in `constituents_issuer_fill` on
08-24 AND 08-28); `3.0.0_SA_CVO~Z` killed *"it left and returned"* (present on all five dates
08-24..08-28, no interruption). **THE RETURN FETCH STOPPED THE DAY AFTER ABT ENTERED THE PORTFOLIO,
NOT WHEN IT LEFT.**

## 4. ⭐ AND THE CODE PREDICTED THIS EXACT SHAPE, ABOUT A DIFFERENT TICKER

`etf_daily_pull.py:150-153`, on FXFXX: *"Excluding it meant its history NEVER ADVANCED — it renders
returns today only because the FROZEN backfill happens to reach the current as-of, and **IT WOULD
HAVE GONE BLANK THE MOMENT THE FRONTIER MOVED PAST IT.**"*
>> **That is ABT's shape verbatim, written days before ABT exhibited it. The author reasoned the
CLASS correctly while fixing one instance, and the 7-char limb created a NEW INSTANCE OF THE SAME
CLASS IN THE SAME COMMIT.** Read that comment before designing the fix — it is the best statement of
the failure mode in the tree. <<

## 5. THE WORK

**Fix the numeric coercion that strips leading zeros from `cusip` BEFORE it reaches
`silver/holdings/`.** The identifier must arrive as a 9-character CUSIP string.

⛔ **DO NOT "FIX" THIS IN `bbg_security()` BY WIDENING THE LENGTH HEURISTIC.** §2 measures why: a
7-char all-digit value is genuinely ambiguous between a doubly-stripped CUSIP and a real SEDOL, and
ICT is a live counter-example sitting in the same partition. **A heuristic that rescues ABT breaks
ICT.** The `len==8` pad stays as it is — it is correct for all four of its cases and is not in scope
to remove.
⚠ **The 8-char pad becomes DEAD CODE if the coercion is fixed at source. LEAVE IT.** It is a
defence against the same class recurring from a different producer, and removing it is a separate
decision with its own evidence.

## 6. ACCEPTANCE CRITERIA

**AC1 — THE STORED IDENTIFIER IS REPAIRED AT SOURCE.** `silver/holdings/{next}.parquet` carries
`ABT` with a **9-character** `cusip` (`002824100`). Score by reading the row, not the writer's log.
**Print the length histogram with its denominator** — the whole-partition shape is the control, and
the 7-char bucket must drop from 3 rows to 2 (ICT and MER, which are correct and must SURVIVE).

**AC2 — ICT AND MER ARE NOT COLLATERAL DAMAGE.** Both still resolve and both still carry non-null
returns after the change. ⛔ **This criterion exists because the obvious fix breaks them**; a change
that repairs ABT and silently drops a Philippine holding has traded one blank row for another.

**AC3 — THE SERVED ARTIFACT CARRIES ABT'S RETURNS.** In a `gold/holding/date={d}/holding.parquet`
produced by a **SCHEDULED** fire after the fix lands, `ABT` carries **8 of 8** non-null return
windows. **Report the 0-of-8 population with its denominator**, which should then be the four CASH
rows plus `2602335D` — **five, not six.**
⚠ **`2602335D` (TPG Inc, w=0.00, price 0.0) IS NOT IN SCOPE and MUST NOT be "fixed" as part of this.**
It is a zero-weight CVR whose Bloomberg ticker is numeric; per the docstring's RBGLD note that class
has no `PX_LAST` so no history can accrue. **Leave it null and say so.**

**AC4 — THE FIX IS EXERCISED BY A SCHEDULED RUN, NOT AN AD-HOC ONE.** An ad-hoc QA run is legitimate
for testing (CLAUDE.md permits it) but **is not the acceptance**. Name the scheduled fire by DATE.

⚠ **DO NOT SCORE AC1-AC4 AGAINST A WEEKEND FIRE WITHOUT RESOLVING THE TRADING CALENDAR FIRST.**
Today is **Saturday 2026-08-29**. `etf_positioning_gold.py:497` and `:1672` anchor on
`tcal.expected_last_trading_day(now)`, which is a DIFFERENT mechanism from the MDPF content-derived
`derive_as_of()` — **do not carry an MDPF frontier result across that boundary** (`3.0.0_SA_CVO~Z`
fenced exactly this, msg 16732). AFTER == BEFORE on a non-advancing day is the EXPECTED outcome, not
a regression.

## 7. BOUNDS THIS FACE CARRIES RATHER THAN DROPS

- **`/sedol/2824100` is UNEXERCISED** (§`<status>`). Not a root cause under Rule 22.
- **20 of 171 backfill objects were read** for the depth/date-range work, size-rank selected, not a
  census. The two-run conclusion is **STRONG AND SHORT OF A CENSUS**.
- **One gold partition (08-27) was read.** Whether ABT was null in the 08-25/08-26 gold is INFERRED
  from the input timeline, not measured on the output.
- **`3.0.0_SA_CVO~Z`'s first probe printed ABT ABSENT ON EVERY DATE** — it selected the first
  `*tick*` column, which is `fund_ticker` (DIVZ/IDVZ), not `holding_ticker`. **A failed retrieval
  returning a VALUE.** What caught it was a histogram printed for an unrelated reason. **If a probe
  here says ABT is absent, suspect the column before the world.**
- **The `bbg/{date}/constituents/` prefix also holds `derived_*` and a `run_manifest.json`** — a
  whole-prefix sweep into a CSV reader dies on the manifest. The constituent rows are
  `constituents_issuer_fill` ONLY.


<proof_of_spec>
  <!-- ISSUANCE half (2.0.0_SA_COO~Z). POSITIONAL -- no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json POS-TO13-AC1,POS-TO13-AC2,POS-TO13-AC3,POS-TO13-AC4
       CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE (a pipe resets $?).
       Coverage diff is BIDIRECTIONAL -- an extra filed criterion fails as loudly as a missing one.
       ⛔ A PLACEHOLDER ROW PASSES THIS CHECKER: rc=0 VALID has been measured on a criterion that
       never ran. rc=0 means the CONTRACT is well-formed, NOT that the work happened. Score the
       ARTIFACT for each AC, then file.
       CELL MAPPING, and the surfaces are what the cells name:
         AC1/AC2 -> ETFS-a-1  the silver/holdings identifier itself
         AC3     -> ETFS-d-1  the producer emitting the served gold
         AC4     -> ETFS-d-1 + ETFS-a-5   the scheduled fire landing under bbg/{date}/
       ⚠ The cells name OPERATIVE SURFACES. The exact code location of the coercion is NOT fixed by
       this contract and is the executor's to determine -- section 5 bounds what must NOT change. -->
  <criterion id="POS-TO13-AC1" cell_refs="ETFS-a-1"/>
  <criterion id="POS-TO13-AC2" cell_refs="ETFS-a-1"/>
  <criterion id="POS-TO13-AC3" cell_refs="ETFS-d-1"/>
  <criterion id="POS-TO13-AC4" cell_refs="ETFS-d-1, ETFS-a-5"/>
  <expected_criteria>POS-TO13-AC1,POS-TO13-AC2,POS-TO13-AC3,POS-TO13-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-13-DS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
