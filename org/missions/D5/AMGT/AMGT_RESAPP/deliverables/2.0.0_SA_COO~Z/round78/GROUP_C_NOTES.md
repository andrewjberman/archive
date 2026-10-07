# AMGT_RESAPP round 78 -- GROUP C: six drafted cells (bb-5, bb-6, bb-7, bb-12, bb-14, bb-15)

Drafted for `2.0.0_SA_COO~Z` on 2026-10-07, about 14:10Z to 14:45Z. Nothing is committed, nothing under `lib/`,
`integrations/`, `infra/` or `portal/` was edited, no store was written, no vendor was called.

**The base.** The shared tree on `CLOUD`. HEAD read `be3481c83e` when the reads began and `94b13244ed` at the last
dry-run; other seats were committing throughout, and the shared index holds an AMGT_HARVST drain in progress
(`lib/research/harvest/universe_securities.py` and three test files staged). The deployed function is
`opal-amgt-scoped-api`, read with GET-shaped direct invokes only. Python is the shell default, 3.14.

**Files.**
- checks: `round78/checks/r78_bb5.py`, `r78_bb6.py`, `r78_bb7.py`, `r78_bb12.py`, `r78_bb14.py`, `r78_bb15.py`. Each passes
  `bash .tools/commit-gate.sh <file>` ("pre-commit gate clean for 1 of 1 file(s)").
- today's reads and the literal base outputs: `round78/reads/` (the two tables, the plant record, one output file per check).

**The write sets are disjoint, and no cell edits `lib/research/api/scoped_amgt.py`.**

| cell | product files it writes |
|---|---|
| bb-5, bb-6, bb-12 | none (the worker's own deliverables folder only) |
| bb-7 | `lib/research/api/name_search.py`, `lib/research/api/_company_names.py` (new), `lib/research/api/tests/test_name_search.py` |
| bb-14 | `integrations/bloomberg/research/research_pulls.py`, `integrations/bloomberg/research/tests/test_research_pulls.py` |
| bb-15 | `lib/research/lists/rot.py`, `lib/research/freshness/build_view.py`, `lib/research/lists/data/rot_signal.json` (new), `lib/research/freshness/tests/test_rot_home.py` (new) |

Every invocation below is the literal line; in an order's XML each `&&` becomes `&amp;&amp;`.

---

## C1 -- `AMGT-bb-5` -- READ: why a driver chart is served for 1 covered name of 95 (ruling 2)

### 1. Measured at the base

Read: `r78_bb5.py --crit AC1 --where deployed`, run 2026-10-07 about 14:25Z. It makes one `/thesis` invoke per covered name
and one S3 LIST per name under `filings/v1/<name>/` in `opal-data-harvest`. The covered list is
`lib.research.coverage.covered_universe.covered_security_keys()`: 95 names; 95 of 95 `/thesis` answered 200.

| class | names | what it means |
|---|---|---|
| NO_FILING_ANALYSIS | 83 | no object ending `.analysis.json` is stored under `filings/v1/<name>/` |
| NO_USABLE_TABLE | 10 | an analysis is stored and the drafted notes name a driver, but 0 of its points were located in the filing text (2 are needed) |
| HOLDS_A_TABLE | 2 | the driver has 2 or more located points: 1 SERVED (BA_US_Equity), 1 REFUSED by round-76 ruling 7 (ASML_NA_Equity) |
| sum | 95 of 95 | 0 unclassified |

- **The refusal removed 1 name, not 94.** `lib/research/filings/table_class.py driver_refusal` is reached only after a driver
  has 2 located points (`scoped_amgt.thesis_driver_chart`, the second branch). 93 names never reach it.
- **The 83.** Each also reads `drafting_status: ABSENT` (83 of 83). The page's own stated reason splits them 41 / 42:
  41 read "filing_identity.source is 'none': no cik and expected form to fetch by" (20 with a US ticker, 21 without);
  42 read "no drafted document at s3://opal-data-harvest/drafting/v1/<name>.json: NoSuchKey ..." (13 US, 29 not).
  The 20 US names with no company number on file: AMD, BZLFY, CPA, GOOGL, IDXX, ISRG, LLY, MA, MELI, MNST, NFLX, NOW, QXO,
  SPOT, TSM, UBER, UNH, UNVGY, V, WDAY.
- **The 10.** BABA, COST, HAL, HD, INTU, KMB, NU, PBR, SAP GY, VLO. Each has drafted notes served and a named driver (for
  example COST: "Total company comparable sales growth excluding foreign-currency and gasoline price impacts"), and each
  driver has 0 points located in the filing text.
- **Where the chart is built.** `lib/research/api/scoped_amgt.py thesis_driver_chart()` (called from `read_thesis_bundle`),
  from the drafted notes' `thesis_driver`. It is served as `thesis_driver_chart` on `GET /security/<name>/thesis`.
- **Controls, all three held:** BA_US_Equity HOLDS_A_TABLE / SERVED; ASML_NA_Equity HOLDS_A_TABLE / REFUSED; AMD_US_Equity
  NO_FILING_ANALYSIS, its segment reason opening "No filing analysis is stored for this name yet".
- The full table with the 95 names per class: `round78/reads/DRIVER_CHART_COVERAGE.md` and `.json`.

**Is the read already done? Yes.** The three counts and the name lists above are today's, from the deployed function. The
worker's run adds a second, independent run and a committed table under a worker folder. If the issuer wants no worker
spent, the table in `round78/reads/` can be committed as it is and the cell closed as an issuer act.

### 2. The act (worker face text)

CTO round-77 ruling 2: one read, no build. Per covered name: is a filing analysis stored, does it hold a table a driver
could be drawn from, and did round-76 ruling 7's refusal remove it. Three counts summing to 95, and the names per class.

1. Run the read script once, writing the table into your own deliverables folder:
   `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb5.py" --crit AC1 --where deployed --write "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<your serial>/"`
   It reads the deployed function `opal-amgt-scoped-api` (one GET-shaped invoke of `/api/scoped/amgt/security/<name>/thesis`
   per covered name) and lists `filings/v1/<name>/` in `opal-data-harvest`. It writes `DRIVER_CHART_COVERAGE.json` and
   `DRIVER_CHART_COVERAGE.md`.
2. The classes are the script's (its docstring states them): NO_FILING_ANALYSIS, NO_USABLE_TABLE, HOLDS_A_TABLE, the last
   split into SERVED and REFUSED. Do not change the rule. If a name prints as UNCLASSIFIED, file a surprise row and commit
   the table as it came out.
3. The issuer's run of 2026-10-07 read 83 / 10 / 2 (BA_US_Equity served, ASML_NA_Equity refused). If your counts differ,
   say which names moved; do not make them agree.
4. Read the 10 NO_USABLE_TABLE names in your table and add ONE paragraph to the `.md`, in plain words: for each, the
   driver the drafted notes name (`driver_series`) and whether the filing text kept for it holds any figure for that
   driver. That paragraph is what the next cell is cut from.
5. You edit no file under `lib/`, `infra/`, `integrations/` or `portal/`. No deploy, no store write, no vendor, SEC or
   model call. One run of the script, and one more only if the first did not complete.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb5.py" --crit AC1 --where deployed; echo "exit=$?"`
  Expect: 95 covered names, every `/thesis` 200; the three counts printed and summing to 95 with 0 unclassified; BA_US_Equity
  SERVED, ASML_NA_Equity REFUSED, AMD_US_Equity NO_FILING_ANALYSIS; `R78 BB5 AC1 READ: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb5.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: exactly one committed `DRIVER_CHART_COVERAGE.json` under a worker folder, its three counts summing to its covered
  count, each covered name listed once, the three controls in their classes; `R78 BB5 AC2 READ: YES`; and exit=0.

### 4. The base dry-run

AC1, PASSED as expected (a read that prints its counts). Literal, the 83-name line shortened here and whole in
`round78/reads/bb5_AC1_base_output.txt`:

```
PASS C1 the covered names are read and every /thesis answers 200 95 covered
   covered names 95; /thesis not 200: 0
   NO_FILING_ANALYSIS   83
   NO_USABLE_TABLE      10
   HOLDS_A_TABLE         2
      of HOLDS_A_TABLE: SERVED 1 ['BA_US_Equity']; REFUSED 1 ['ASML_NA_Equity']
   sum 95 of 95; unclassified 0 []
      NO_USABLE_TABLE because the driver has 0 located point(s); 2 are needed: 10
      NO_FILING_ANALYSIS, the page's stated reason 'no drafted document is stored for the name (the served text names the store address)': 42
      NO_FILING_ANALYSIS, the page's stated reason "filing_identity.source is 'none': no cik and expected form to fetch by": 41
   NO_FILING_ANALYSIS: 1299_HK_Equity, 2317_TT_Equity, 8035_JP_Equity, 8306_JP_Equity, 8316_JP_Equity, 8766_JP_Equity, 939_HK_Equity, 9433_JP_Equity, 992_HK_Equity, ADBE_US_Equity, AI_FP_Equity, AMD_US_Equity, AMXB_MM_Equity, AZN_LN_Equity, BATS_LN_Equity, BBSE3_BZ_Equity, BNP_FP_Equity, BP/_LN_Equity, BZLFY_US_Equity, CDNS_US_E ... [line shortened; whole in reads/bb5_AC1_base_output.txt]
   NO_USABLE_TABLE: BABA_US_Equity, COST_US_Equity, HAL_US_Equity, HD_US_Equity, INTU_US_Equity, KMB_US_Equity, NU_US_Equity, PBR_US_Equity, SAP_GY_Equity, VLO_US_Equity
   HOLDS_A_TABLE: ASML_NA_Equity, BA_US_Equity
PASS C2 the three counts sum to the covered count 83 + 10 + 2 = 95 of 95
   control BA_US_Equity: class HOLDS_A_TABLE split SERVED
   control ASML_NA_Equity: class HOLDS_A_TABLE split REFUSED
   control AMD_US_Equity: class NO_FILING_ANALYSIS split None
PASS C3 the three controls sit in their classes 
   wrote DRIVER_CHART_COVERAGE.json and .md to org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/reads
R78 BB5 AC1 READ: YES
exit=0
```

AC2, FAILED as expected (no worker has committed a table):

```
FAIL C1 exactly one committed table 0 found []
R78 BB5 AC2 READ: NO
exit=1
```

### 5. Paths

```
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light` (no product line).

### 7. Edges

None. The cell that builds on it (ruling 2: "the cell that follows is cut from that table") waits for it.

### 8. Not measured, and questions for the issuer

- **Rule the partition.** The ruling asks three counts summing to 95. I put the one served name inside the third class
  (HOLDS_A_TABLE = 1 served + 1 refused). If the three were meant as "no analysis / no table / refused", they sum to 94 and
  the served name is the 95th.
- "A filing analysis is stored" is read as an object under `filings/v1/<name>/` ending `.analysis.json`, the same listing
  `read_segment_breakdown` makes. A drafted document with no analysis object would still read NO_FILING_ANALYSIS; today
  that case is empty (83 of 83 have neither).
- NOT measured: whether the kept filing text of the 10 holds the driver's figures at all (step 4 asks the worker), and why
  20 US names have no company number on file.

---

## C2 -- `AMGT-bb-6` -- READ: the Recommendation cards (ruling 8)

### 1. Measured at the base

Read: `r78_bb6.py --crit AC1 --where deployed`, run 2026-10-07 about 14:27Z; 95 of 95 `/thesis` answered 200.

**The two labels are page text, not served fields.** Both are in
`portal/src/pages/SecurityAnalysis/components/ThesisCards.tsx`, function `CardLead`:
- "The research team's Base case leads, as written in the team's pack" shows when `model.team_cases.base.status` is
  `"SERVED"` and its `table` is a non-empty object (`isServed(teamCaseOf(bundle, 'base'))`).
- "A machine draft, not the research team's view" shows when `drafted_sections` holds the section with
  `section_id: "recommendation"` and 1 or more sentences.

| label state | names |
|---|---|
| BOTH labels | 3 (ASML_NA_Equity, INTU_US_Equity, SAP_GY_Equity) |
| machine draft only | 9 (BABA, BA, COST, HAL, HD, KMB, NU, PBR, VLO) |
| Base case leads only (the card then reads "Recommendation is not in this pack yet") | 31 |
| neither | 52 |
| sum | 95 of 95 |

**The sentence rule.** The card's face shows the first sentence of the recommendation section. A sentence IS a
recommendation only when it carries a recommendation word: buy, sell, hold, overweight, underweight, outperform,
underperform, accumulate, recommend, rating, rated, price target, upside, downside, attractive, valuation, undervalued,
overvalued, own the shares, add to, trim, conviction (`RECOMMENDATION_WORDS` in the script).

- Cards with a drafted sentence: 12 of 95.
- Face sentence is not a recommendation: **12 of 12**.
- Cards where no sentence at all carries a recommendation word: 12 of 12; **0 of 63 sentences** carry one.
- Of the 12 face sentences, 9 are a forward-looking statement lifted from the filing (expects, plans, will ...). 3 carry no
  forward-looking word either: ASML_NA_Equity (the governance-code sentence), NU_US_Equity, SAP_GY_Equity. That second word
  list is coarse: NU's sentence says "could" and SAP's says "guided", so read those two by eye before calling them ASML's
  kind.

**So ASML is one of a class of three for the two labels, and one of twelve for the sentence.** Every served Recommendation
card is a list of filing statements; none states a recommendation. The table: `round78/reads/RECOMMENDATION_CARDS.md`.

**Is the read already done? Yes**, on the same terms as C1.

### 2. The act (worker face text)

CTO round-77 ruling 8: one read, no build. Over the covered names' Recommendation cards: how many carry both labels, and
how many carry a sentence that is not a recommendation.

1. Run the read script once, writing the table into your own deliverables folder:
   `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb6.py" --crit AC1 --where deployed --write "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<your serial>/"`
   It writes `RECOMMENDATION_CARDS.json` and `RECOMMENDATION_CARDS.md`.
2. The label rule and the sentence rule are the script's (its docstring states both). Do not change them.
3. Read every face sentence in your table by eye (there were 12 on 2026-10-07) and add one line per card to the `.md`:
   does the sentence tell a reader to do anything with the shares, yes or no, in your own reading. Where your reading and
   the word rule disagree, say so on that line.
4. Open `portal/src/pages/SecurityAnalysis/components/ThesisCards.tsx` (read only) and confirm in one sentence that the two
   labels are still switched by the two fields the script's docstring names. If they are not, file a surprise row.
5. You edit no file under `lib/`, `infra/`, `integrations/` or `portal/`. No deploy, no store write, no vendor, SEC or
   model call.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb6.py" --crit AC1 --where deployed; echo "exit=$?"`
  Expect: 95 covered names, every `/thesis` 200; the four label states summing to 95; the count of face sentences that are
  not a recommendation printed with their names; ASML_NA_Equity in BOTH with a face sentence that is not a recommendation;
  `R78 BB6 AC1 READ: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb6.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: exactly one committed `RECOMMENDATION_CARDS.json` under a worker folder, its four states summing to its covered
  count with each name once, ASML_NA_Equity in BOTH; `R78 BB6 AC2 READ: YES`; and exit=0.

### 4. The base dry-run

AC1, PASSED as expected (a read that prints its counts). Literal:

```
PASS C1 the covered names are read and every /thesis answers 200 95 covered
   covered names 95; /thesis not 200: 0
   BOTH                  3  ASML_NA_Equity, INTU_US_Equity, SAP_GY_Equity
   MACHINE_DRAFT_ONLY    9  BABA_US_Equity, BA_US_Equity, COST_US_Equity, HAL_US_Equity, HD_US_Equity, KMB_US_Equity, NU_US_Equity, PBR_US_Equity, VLO_US_Equity
   BASE_CASE_ONLY       31  8035_JP_Equity, ADBE_US_Equity, AZN_LN_Equity, BP/_LN_Equity, BZLFY_US_Equity, CDNS_US_Equity, CELH_US_Equity, CPA_US_Equity, HEI_US_Equity, IDXX_US_Equity, ISRG_US_Equity, MA_US_Equity, MELI_US_Equity, ML_FP_Equity, MNST_US_Equity, MSCI_US_Equity, NFLX_US_Equity, NKE_US_Equity, NOW_US_Equity, ORA_FP_ ... [line shortened; whole in reads/bb6_AC1_base_output.txt]
   NEITHER              52  1299_HK_Equity, 2317_TT_Equity, 8306_JP_Equity, 8316_JP_Equity, 8766_JP_Equity, 939_HK_Equity, 9433_JP_Equity, 992_HK_Equity, AI_FP_Equity, AMD_US_Equity, AMXB_MM_Equity, BATS_LN_Equity, BBSE3_BZ_Equity, BNP_FP_Equity, CLX_US_Equity, CNR_CN_Equity, ENEL_IM_Equity, GOOGL_US_Equity, GPN_US_Equity, GSK_L ... [line shortened; whole in reads/bb6_AC1_base_output.txt]
   sum 95 of 95
   cards with a drafted sentence 12 of 95
   face sentence is NOT a recommendation (no recommendation word): 12 of 12
      of those, no forward-looking word either: 3  ASML_NA_Equity, NU_US_Equity, SAP_GY_Equity
   cards where NO sentence carries a recommendation word: 12 of 12
   sentences with a recommendation word: 0 of 63 sentences
   ASML_NA_Equity   BOTH               NEITHER_WORD         1 sentence(s) words [] | The updated Dutch Corporate Governance Code 2025 applies to financial years starting on or after January 1, 20
   BABA_US_Equity   MACHINE_DRAFT_ONLY OUTLOOK_ONLY         9 sentence(s) words [] | The company expects continued margin pressure, stating "As we continue with our significant investments into o
   BA_US_Equity     MACHINE_DRAFT_ONLY OUTLOOK_ONLY         9 sentence(s) words [] | The 737 program plans to increase the production rate from 42 to 47 per month in 2026 "with the concurrence of
   COST_US_Equity   MACHINE_DRAFT_ONLY OUTLOOK_ONLY         4 sentence(s) words [] | Management plans to open up to 35 new warehouses, including five relocations, in 2026.
   HAL_US_Equity    MACHINE_DRAFT_ONLY OUTLOOK_ONLY         3 sentence(s) words [] | Management says that despite this reduction from 2025, this level of spending will enable continued investment
   HD_US_Equity     MACHINE_DRAFT_ONLY OUTLOOK_ONLY         3 sentence(s) words [] | The company plans to invest approximately $4 billion back into the business in capital expenditures in fiscal 
   INTU_US_Equity   BOTH               OUTLOOK_ONLY        10 sentence(s) words [] | The company expects total service revenue as a percentage of total revenue to grow over the long term, after s
   KMB_US_Equity    MACHINE_DRAFT_ONLY OUTLOOK_ONLY         7 sentence(s) words [] | Management expects 2026 net input costs, including tariffs, "to be broadly in line with fiscal 2025, including
   NU_US_Equity     MACHINE_DRAFT_ONLY NEITHER_WORD         1 sentence(s) words [] | Management notes ongoing Brazilian discussions to update risk-weighted asset methodology "which could positive
   PBR_US_Equity    MACHINE_DRAFT_ONLY OUTLOOK_ONLY         6 sentence(s) words [] | The company believes it should not be treated as a PFIC for the 2025 or 2024 taxable years and does not antici
   SAP_GY_Equity    BOTH               NEITHER_WORD         5 sentence(s) words [] | SAP guided "To steadily decrease carbon emissions across the relevant value chain", and emissions fell to 6.3 
   VLO_US_Equity    MACHINE_DRAFT_ONLY OUTLOOK_ONLY         5 sentence(s) words [] | Management states global demand for gasoline, diesel and jet fuel "continues to rise, with growth in demand fo
PASS C2 the four label states sum to the covered count 95 of 95
   named case ASML_NA_Equity: state BOTH; face kind NEITHER_WORD
PASS C3 the named case carries both labels over a sentence that is not a recommendation 
   wrote RECOMMENDATION_CARDS.json and .md to org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/reads
R78 BB6 AC1 READ: YES
exit=0
```

AC2, FAILED as expected:

```
FAIL C1 exactly one committed table 0 found []
R78 BB6 AC2 READ: NO
exit=1
```

### 5. Paths

```
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light`.

### 7. Edges

None. The producer cell of ruling 8 (one provenance label; a drafted sentence that states no recommendation is refused)
is cut from this table.

### 8. Not measured, and questions for the issuer

- **The labels are the page's.** The producer serves no label. "A card carries ONE provenance label" is therefore either a
  DSGN_AMGTV1 page cell, or a producer cell that serves one field the page prints. Rule which.
- **If the producer refuses every drafted sentence with no recommendation word, all 12 served cards go empty.** 0 of 63
  sentences pass the word rule. Rule the refusal's test before the producer cell is cut.
- NOT measured: the rendered page. The labels were read from the page's source and the fields from the served body; no
  browser was opened.

---

## C3 -- `AMGT-bb-7` -- name search by company name (row AMGT_RESAPP-Z-W275-S1)

### 1. Measured at the base

Read: `r78_bb7.py --crit READ --where deployed` and `--crit AC1 --where local`, 2026-10-07 about 14:29Z.

- The stored name list is `s3://opal-data-harvest/crosswalk/v1/2026-10-07.json`: 243 records, 243 distinct names.
- Records carrying a name the search can read: **100 of 243** by field (a research folder name on 96, a registered name
  on 68, either on 100); **99 of 243** by behaviour (one record's stored name is only its ticker's first word). 143 / 144
  carry none.
- `resolve_query("apple")`: `none`, "no company we cover matches 'apple'". `resolve_query("microsoft")`: `none`.
  `resolve_query("airbnb")`: `candidates`, ABNB_US_Equity "AIRBNB INC-CLASS A" (it has a registered name from today's
  first pull). The deployed route answers the same three, each 200.
- **What AMGT_HARVST joined.** Its cells `HVST-bc-1` (round 56) and `HVST-be-1` (round 58, today) take each company's legal
  name from the collector's own record:
  `org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_identity_20261005.json`, 234 records,
  234 names (`company.value`), 0 not ASCII, read by `lib.research.harvest.universe_securities.load_legal_names()` through
  the path in `lib/opal_data_harvest/config.json` (`symbol_resolution_source`). `HVST-az-1` is the alias set per name that
  record came from.
- **Are those names readable by name search today? No.** They were joined into the collector's list of companies to match
  articles against. Nothing wrote them into the stored name list, and `lib/research/api/name_search.py` reads only
  `source_row.folder` and `identity.name` of that list. No names file exists under `lib/research/`.
- **What a join would reach.** The 234 legal names hold 139 of the 144 nameless records. After a join 238 of 243 carry a
  name; 5 still do not: BE_US_Equity, DG_US_Equity, ED_US_Equity, GEV_US_Equity, MRNA_US_Equity.
- Simulated in memory (no file edited): with the legal names as a third source, "apple" lists AAPL_US_Equity "Apple Inc",
  "microsoft" lists MSFT_US_Equity "Microsoft Corp", "coca" lists 3 companies, "lenovo" and "airbnb" answer as today.

### 2. The act (worker face text)

Row AMGT_RESAPP-Z-W275-S1: typing a company name lists nothing for 144 of the 243 companies we hold, because their stored
record carries no name. "apple" and "microsoft" both answer "no company we cover matches". Another project already holds
the legal names. Make the search read them.

Build, in this order:

1. **A new module `lib/research/api/_company_names.py`** holding ONE constant, `NAMES`: a dict of company key to legal
   name, sorted by key, and a header comment that names its source file and the date you copied it. Generate it, do not
   type it: read the names with `lib.research.harvest.universe_securities.load_legal_names()` (no argument), pass each
   value through `universe_securities.clean_legal_name(value)[0]`, and write the dict out as Python source, ASCII only.
   On 2026-10-07 that is 234 names. It is a `.py` file on purpose: every `.py` under `lib/research/api/` is carried into
   the deployed package, and a `.json` would not be.
2. **`lib/research/api/name_search.py`.** `_stored_names(record)` gains a third name, after the two it reads today:
   `_company_names.NAMES.get(record["security_key"])`, added only when it is not already there (compare case-insensitively).
   Nothing else in the matching changes. A record with no folder name and no registered name now shows its legal name as
   the candidate's `name`.
3. `name_search.py` must NOT import `lib.research.harvest` and must NOT open any file under `org/`. The generator in
   step 1 is a one-off you run; it is not left in `name_search.py`.
4. **Tests** in `lib/research/api/tests/test_name_search.py`: add `test_a_legal_name_lists_its_company` ("apple" and "Apple"
   list AAPL_US_Equity with the name "Apple Inc"; a company with a folder name still lists under that folder name; a
   company with no name anywhere still lists by its ticker's first word only). Keep the eight tests there passing.

Rules:
1. The search still never guesses: an exact stored form answers `exact` as today, and a typed company name is never
   answered as `exact`.
2. You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/identity/crosswalk.py`, the build script under
   `infra/`, or anything under `lib/research/harvest/` or `org/missions/D5/AMGT/AMGT_HARVST/`.
3. Any sentence the search serves stays in plain words. Do not use: identity, unresolved, security key, crosswalk,
   dossier, landed, model block, estate, stage, input ledger, bronze.
4. No deploy, no store write, no vendor, SEC or model call.

Report: how many records carry a name before and after, the names of those that still carry none, and what "apple",
"microsoft" and "airbnb" answer.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: "apple" lists AAPL_US_Equity and "microsoft" lists MSFT_US_Equity by company name; 238 or more of the stored
  records carry a readable name, the rest printed; `_company_names.NAMES` holds 230 or more names, each equal to the
  cleaned legal name for its key; C1-C3 PASS; `R78 BB7 AC1 SERVED: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: `test_name_search.py` holds `test_a_legal_name_lists_its_company` and the whole file passes;
  `R78 BB7 AC2 SERVED: YES`; and exit=0.
- **AC3** (bound) `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: every stored key still passes through as exact (N of N); "apple", "microsoft", "lenovo" and "airbnb" are never
  answered as exact; "lenovo" and "airbnb" still list their companies; no match still reads a plain reason;
  `R78 BB7 AC3 SERVED: YES`; and exit=0.

### 4. The base dry-run

Literal (lines cut at 400 characters), `round78/reads/bb7_base_output.txt`. READ on the deployed route, then AC1 FAILED as
expected (build), AC2 FAILED as expected (build), AC3 PASSED as expected (bound):

```
### READ --where deployed
   stored name list as_of 2026-10-07; records 243
   records carrying a readable name 99 of 243; without 144
   AMGT_HARVST legal names: 234 loaded from org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_identity_20261005.json
   of the 144 without a name, the legal names hold 139; still without 5 ['BE_US_Equity', 'DG_US_Equity', 'ED_US_Equity', 'GEV_US_Equity', 'MRNA_US_Equity']
   legal names not ASCII: 0
   deployed, status code 200:
   'apple': status none candidates [] reason "no company we cover matches 'apple'"
   deployed, status code 200:
   'microsoft': status none candidates [] reason "no company we cover matches 'microsoft'"
   deployed, status code 200:
   'airbnb': status candidates candidates [('ABNB_US_Equity', 'AIRBNB INC-CLASS A')] reason None
R78 BB7 READ: DONE
exit=0
### AC1 --where local
   stored name list as_of 2026-10-07; records 243
   records carrying a readable name 99 of 243; without 144
   AMGT_HARVST legal names: 234 loaded from org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_identity_20261005.json
   of the 144 without a name, the legal names hold 139; still without 5 ['BE_US_Equity', 'DG_US_Equity', 'ED_US_Equity', 'GEV_US_Equity', 'MRNA_US_Equity']
   legal names not ASCII: 0
   'apple': status none candidates [] reason "no company we cover matches 'apple'"
   'microsoft': status none candidates [] reason "no company we cover matches 'microsoft'"
   'airbnb': status candidates candidates [('ABNB_US_Equity', 'AIRBNB INC-CLASS A')] reason None
FAIL C1 apple and microsoft list their companies by company name 
FAIL C2 238 or more records carry a readable name 99 of 243; without ['2602335D_US_Equity', 'AAPL_US_Equity', 'ABBV_US_Equity', 'ABT_US_Equity', 'ADM_US_Equity', 'AEP_US_Equity', 'AIG_US_Equity', 'AIZ_US_Equity', 'AMAT_US_Equity', 'AMP_US_Equity', 'AMX_US_Equity', 'AMZN_US_Equity']
FAIL C3 lib.research.api._company_names imports cannot import name '_company_names' from 'lib.research.api' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\api\__init__.py)
R78 BB7 AC1 SERVED: NO
exit=1
### AC2 --where local
FAIL C1 the test file holds test_a_legal_name_lists_its_company 
   8 passed in 0.29s
PASS C2 every case in the file passes rc=0
R78 BB7 AC2 SERVED: NO
exit=1
### AC3 --where local
PASS C1 every stored key passes through as exact 243 of 243
PASS C2 a typed company name is never answered as exact {'apple': 'none', 'microsoft': 'none', 'lenovo': 'candidates', 'airbnb': 'candidates'}
PASS C3 the names that listed before still list, and no match still reads a plain reason 
R78 BB7 AC3 SERVED: YES
exit=0
```

### 5. Paths

```
lib/research/api/name_search.py
lib/research/api/_company_names.py
lib/research/api/tests/test_name_search.py
lib/research/harvest/universe_securities.py            (read only)
lib/opal_data_harvest/config.json                      (read only)
org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_identity_20261005.json   (read only)
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light`: about 10 changed lines in `name_search.py`; the new module is 234 generated lines of data.

### 7. Edges

None before it. After it: the page shows the result only once the round's redeploy cell has drained (the redeploy is not
this cell's). AC1's C3 reads AMGT_HARVST's record at check time; if AMGT_HARVST re-mints that record between the worker's
copy and the drain, C3 reads the difference.

### 8. Not measured, and questions for the issuer

- **This cell copies another project's data.** The names are AMGT_HARVST's (a file in its deliverables folder, dated
  2026-10-05). A copy under `lib/research/api/` goes stale when AMGT_HARVST re-mints. The other route is that the stored
  name list itself carries each legal name at its next mint (`lib/research/identity/crosswalk.py`, which round 77 bound
  as read-only for the search cell). Rule which. The copy is the small build; the mint is the one home.
- 5 names stay nameless either way (BE, DG, ED, GEV, MRNA): they are in neither record. A name for them needs a source
  nobody has named.
- NOT exercised: that the build script carries `_company_names.py`. It is inferred from
  `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh` (`SEED_PKG_DIRS` holds `lib/research/api`); the redeploy
  cell's own check should read "apple" on the deployed route (`r78_bb7.py --crit READ --where deployed` prints it).
- NOT measured: how the page's search box shows a candidate whose name is in capitals ("AIRBNB INC-CLASS A").

---

## C4 -- `AMGT-bb-12` -- the planted FWD-14 lapse (ruling 6)

### 1. Measured at the base

Read: `r78_bb12.py --crit AC1 --where local` and `--crit ORGANIC --where deployed`, 2026-10-07 14:30Z.

- The two list files are packaged at `lib/research/lists/data/publishers.json` (2 entries, owner "Andrew", reviewed
  2026-09-10T22:42Z, every 90 days) and `social_accounts.json` (267 entries, owner "Andrew", reviewed 2026-09-10T22:42Z,
  every 30 days). Read: the two files' own top-level fields.
- The route `GET /api/scoped/amgt/freshness?view=page` serves
  `page_body.page_view(view, annotate=..., lists=owner_line.lists_statement(read_list_register()))`
  (`scoped_amgt.py`, the `freshness` branch). `lists_statement` is a pure function of the register and the clock.
- The deployed page today: "Andrew owns the publisher list and the social account list." and "The publisher list is in
  date: reviewed 2026-09-10, next review due 2026-12-09. The social account list is in date: reviewed 2026-09-10, next
  review due 2026-10-10."
- **Provable today with no build: YES.** `read_list_register()` takes no path; it reads the `data` folder beside
  `lib.research.lists.rot`'s module file. The check copies both files to a temporary folder, sets the review date in the
  COPY of the social list to 2026-08-01T00:00Z, points that module's `__file__` at the temporary folder for one call in
  its own process, and calls the real handler. Result: "The social account list is out of date: its review fell due on
  2026-08-31." beside "Andrew owns the publisher list and the social account list."; the unchanged publisher list still
  reads in date; the unchanged-copy control reads in date; the packaged files' SHA-256 did not move.
- **The clean seam would be a path argument on `read_list_register`, and that function is in `scoped_amgt.py`, which no
  cell of this group edits.** So the cell is a READ cell that commits the plant's record; no seam is built.
- **The organic arm falls due at 2026-10-10T22:42Z, not at the start of that day.** `lists_statement` compares the due
  moment (review time plus 30 days) with the clock. A read at any time on 2026-10-10 before 22:42Z will still say "in
  date ... next review due 2026-10-10". Read it after 22:42Z.

### 2. The act (worker face text)

CTO round-77 ruling 6: "A planted lapse, stated as planted: on a copy of one list, the review date set in the past; the
page says the list is out of date and names its owner. The social list's real review date of 2026-10-10 is kept as the
organic arm and read that day. No alert is built."

1. Run the plant once, writing its record into your own deliverables folder:
   `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb12.py" --crit AC1 --where local --write "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<your serial>/"`
   It copies the two packaged list files to a temporary folder, changes ONE field in the COPY of the social account list
   (`reviewed_at`, to 2026-08-01T00:00Z), and calls the page route's own handler on the copies. It writes
   `PLANTED_LAPSE.json`: what was planted, the page's words for the planted copy, the page's words for an unchanged copy,
   and the packaged files' SHA-256 before and after.
2. Beside it write `PLANTED_LAPSE.md`, in plain words, opening with the sentence "This is a plant: a copy of the social
   account list with its review date set in the past. The real list has not lapsed." Then the two sentences the page
   said for the plant (the out-of-date sentence and the owner sentence), the sentence it said for the unchanged copy, and
   the moment the real list falls due (the record's `real_due_utc`).
3. You never open `lib/research/lists/data/publishers.json` or `social_accounts.json` for writing, and you edit no file
   under `lib/`, `infra/`, `integrations/` or `portal/`. No deploy: the deployed page must go on saying what is true.
4. You build no alert, alarm, message, schedule or monitor. The page saying it when a person opens it is the whole act.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb12.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: on the planted copy the page says "The social account list is out of date: its review fell due on 2026-08-31."
  and "Andrew owns the publisher list and the social account list."; the publisher list reads in date beside it; the
  unchanged copy reads in date (or out of date only if the real due moment has passed); the packaged files did not move;
  C1-C5 PASS; `R78 BB12 AC1 SERVED: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb12.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: exactly one committed `PLANTED_LAPSE.json` under a worker folder that says it is a plant and carries the same
  five clauses; `R78 BB12 AC2 SERVED: YES`; and exit=0.

The organic arm is the issuer's own read, not a worker criterion (a worker cannot wait three days):
`cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb12.py" --crit ORGANIC --where deployed; echo "exit=$?"`
run after 2026-10-10T22:42Z. Expect then: the deployed page says the social account list is out of date and names Andrew.

### 4. The base dry-run

Literal (lines cut at 420 characters), `round78/reads/bb12_base_output.txt`. AC1 PASSED as expected (the outcome is
provable today); AC2 FAILED as expected (no committed record); ORGANIC reads NO as expected today (not yet due):

```
### AC1 --where local --write org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/reads
   planted: owner line 'Andrew owns the publisher list and the social account list.'
   planted: 'The publisher list is in date: reviewed 2026-09-10, next review due 2026-12-09. The social account list is out of date: its review fell due on 2026-08-31.'
   control: 'The publisher list is in date: reviewed 2026-09-10, next review due 2026-12-09. The social account list is in date: reviewed 2026-09-10, next review due 2026-10-10.'
PASS C1 planted: the page says the social account list is out of date, with its due date The social account list is out of date: its review fell due on 2026-08-31.
PASS C2 it names the owner owner 'Andrew'
PASS C3 the unchanged publisher list still reads in date beside it 
PASS C4 the control: the unchanged copy reads what the packaged file implies today real due 2026-10-10T22:42Z; read at 2026-10-07T14:30:26Z; expected out of date False
PASS C5 the packaged files did not move and the copies were the files read sha256 social 892533d76c773d5a
   wrote PLANTED_LAPSE.json to org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/reads
R78 BB12 AC1 SERVED: YES
exit=0
### AC2 --where local
FAIL C0 exactly one committed record 0 found []
R78 BB12 AC2 SERVED: NO
exit=1
### ORGANIC --where deployed
   deployed owner line: 'Andrew owns the publisher list and the social account list.'
   deployed: 'The publisher list is in date: reviewed 2026-09-10, next review due 2026-12-09. The social account list is in date: reviewed 2026-09-10, next review due 2026-10-10.'
   the packaged social account list falls due at 2026-10-10T22:42Z; now 2026-10-07T14:30Z
FAIL C1 the deployed page says the social account list is out of date and names its owner out_of_date False owner 'Andrew'
R78 BB12 ORGANIC SERVED: NO
exit=1
```

### 5. Paths

```
lib/research/lists/data/publishers.json                (read only)
lib/research/lists/data/social_accounts.json           (read only)
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light`.

### 7. Edges

None. If bb-15 (below) drains first it adds a third file to `lib/research/lists/data/`; the plant copies two files by name
and is not affected.

### 8. Not measured, and questions for the issuer

- **The plant is proved on the route's handler in a local process, never on the deployed page.** Showing it on the deployed
  page would mean deploying a false list file. The CVO must say whether the local handler read grades FWD-14's planted arm.
- The check redirects one module attribute in its own process to stand in for a path argument. If the CTO wants a real
  seam (`read_list_register(data_dir=None)`), that is one line in `scoped_amgt.py` and belongs to whichever round-78 cell
  owns that file.
- The page's words carry the due DATE and no time, while the lapse turns on the due MOMENT (22:42Z). On 2026-10-10 the page
  will say "in date ... next review due 2026-10-10" for 22 hours 42 minutes. Seen, no verdict; a surprise row is the
  issuer's to file.
- When the real list does lapse, somebody has to review it or the page says "out of date" from then on. The ruling names
  no act for that.

---

## C5 -- `AMGT-bb-14` -- the pull driver gives a missing library its own stop word (row AMGT_RESAPP-Z-S366)

### 1. Measured at the base

- `integrations/bloomberg/research/research_pulls.py` (271 lines): `EXIT = {"OK": 0, "CAPACITY": 3, "VEHICLE_NOT_RUN": 4,
  "TERMINAL_DOWN": 5}`; `terminal_healthy()` is `try: return bool(_load_blp_client().health().get("ok"))` /
  `except Exception: return False`; `run()` checks `vehicle_ran()` then `health()`; `main()` returns
  `EXIT[result["stopped"] or "OK"]`. Read: the file.
- The shell's default Python is 3.14 and has no `blpapi` (row Z-S366, the issuer's read of 2026-10-07 as the row records it; not re-run here:
  re-running would invoke the driver).
- `integrations/bloomberg/research/tests/test_research_pulls.py`: 20 tests pass under Python 3.14 (`20 passed in 0.34s`).
- `integrations/bloomberg/` holds 96 tracked files; 94 are not this cell's. Their stamp (SHA-256 over `git ls-files -s`)
  is `002e8c2034aba7d6...`, and nothing there is modified or untracked. Last commit touching the folder: `fad25b1527`,
  2026-10-07T13:45Z. Read: `r78_bb14.py --stamp` and `--crit AC3`.

### 2. The act (worker face text)

Row AMGT_RESAPP-Z-S366. The driver for the one-time Bloomberg research pulls reports `TERMINAL_DOWN` (exit 5) when the
Python it runs under simply has no Bloomberg library: `terminal_healthy()` returns False on any exception. A missing
library and a Terminal that is not answering read the same, and the driver does not say which Python it ran under. Give
the missing library its own stop word and exit code, decided before any other read.

Edit `integrations/bloomberg/research/research_pulls.py`:

1. `EXIT` gains `"NO_BLOOMBERG_LIBRARY": 6`. The four older codes do not change. Update the `EXIT = ...` line in the module
   docstring and add one docstring line stating the new condition.
2. Add `library_importable(module="blpapi")`: True when that module can be found by this interpreter, False when it cannot.
   Use `importlib.util.find_spec` inside a `try` that treats `ImportError` and `ValueError` as False. It imports nothing
   and opens no session.
3. `run(kind, names, blp, write, vehicle_ran, health, library=None)`: when `library` is given and `library()` is false,
   return at once with `stopped: "NO_BLOOMBERG_LIBRARY"`, 0 calls, nothing pulled, BEFORE `vehicle_ran()` and before
   `health()` are called. `library=None` means the question is not asked, so every existing caller and test behaves as
   today.
4. `main()` passes `library=library_importable`, looked up on the module when `main` runs (not bound as a default
   argument). When the run stops on the new word, `main` also prints one line that names the interpreter, in plain words,
   for example: `REFUSED: this Python (<sys.executable>, <version>) cannot import the Bloomberg library blpapi; run the
   pull with the Python the 7:00 AM pull uses`. It returns 6.
5. `terminal_healthy()` keeps its behaviour. `TERMINAL_DOWN` now means only what it says.

Edit `integrations/bloomberg/research/tests/test_research_pulls.py` (fakes only, as the file already does):

6. Add `test_missing_library_stops_before_any_call`: `rp.run(..., library=lambda: False)` stops `NO_BLOOMBERG_LIBRARY`, the
   fake client has 0 calls, 0 writes, and neither the vehicle read nor the health read ran.
7. Add a control test: `library=lambda: True` pulls every name; and a test that `library_importable` answers False for a
   module name that does not exist.
8. Update `test_exit_codes_are_the_stated_ones` and `test_cli_maps_a_stop_to_its_exit_code` for the fifth word.

Rules:
1. **You edit those two files and no other file under `integrations/bloomberg/`.** Andrew's no-modify order covers
   everything there except `research/`. Do not touch `integrations/bloomberg/mcp/blp_client.py`.
2. **You make no Bloomberg call and you do not run the driver's `run` command.** Not `--probe`, not once. Every proof is on
   fakes. `plan` is also not needed.
3. No sign-in script is named or imported (the existing test `test_source_names_no_sign_in_script` must keep passing).
4. No deploy, no store write.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb14.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: `EXIT` holds NO_BLOOMBERG_LIBRARY = 6 beside the four older codes; a missing library stops the run before the
  vehicle read and the health read, with 0 calls; with the library present the run pulls; a silent Terminal is still
  TERMINAL_DOWN; the command line returns 6 and names the interpreter; C1-C5 PASS; `R78 BB14 AC1 SERVED: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb14.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the test file holds `test_missing_library_stops_before_any_call` and the whole file passes;
  `R78 BB14 AC2 SERVED: YES`; and exit=0.
- **AC3** (bound) `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb14.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: every other tracked file under `integrations/bloomberg/` is the one at the cut (94 files, the stamp equal) and
  nothing else there is modified or untracked; `R78 BB14 AC3 SERVED: YES`; and exit=0.

### 4. The base dry-run

Literal, `round78/reads/bb14_base_output.txt`. AC1 FAILED as expected (build), AC2 FAILED as expected (build), AC3 PASSED as
expected (bound; re-run at HEAD `94b13244ed`, still PASS):

```
### AC1
FAIL C1 EXIT holds the new word at 6 and the four older codes {'OK': 0, 'CAPACITY': 3, 'VEHICLE_NOT_RUN': 4, 'TERMINAL_DOWN': 5}
FAIL C2 library_importable exists absent
R78 BB14 AC1 SERVED: NO
exit=1
### AC2
FAIL C1 the test file holds test_missing_library_stops_before_any_call 
   20 passed in 0.34s
PASS C2 every case in the file passes rc=0
R78 BB14 AC2 SERVED: NO
exit=1
### AC3
PASS C1 every other tracked file under integrations/bloomberg is the one at the cut 94 files; stamp 002e8c2034aba7d6
PASS C2 nothing else there is modified or untracked 0 other path(s) []
R78 BB14 AC3 SERVED: YES
exit=0
```

### 5. Paths

```
integrations/bloomberg/research/research_pulls.py
integrations/bloomberg/research/tests/test_research_pulls.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light` (about 25 product lines, about 30 test lines).

### 7. Edges

**It drains before the ABNB pull cell (ruling 7) if that cell uses this driver**, so the pull runs with the new word. If
any round-78 cell commits under `integrations/bloomberg/` before the issuance commit, AC3's stamp must be re-taken at the
cut: `python .../r78_bb14.py --stamp` prints it, and the constant `STAMP` in the check is replaced by that value.

### 8. Not measured, and questions for the issuer

- NOT measured: whether any caller other than this seat runs the driver under the default Python (the row says the same).
- NOT measured: the driver under the pull's own Python 3.11. The checks ran under 3.14 on fakes.
- **Rule the order.** I put the library question FIRST, before the vehicle read, so that a wrong Python is named even on a
  day the 7:00 AM pull has not run. If the vehicle condition must stay the first refusal, swap them and change clause C3.
- The word and the code (`NO_BLOOMBERG_LIBRARY`, 6) are my choice; exit 2 is already the wrong-call-count refusal.

---

## C6 -- `AMGT-bb-15` -- the rot signal gets a home its own module owns (row AMGT_RESAPP-Z-W279-S2)

### 1. Measured at the base

- **What the glob matches today: 1 file.** `ROT_SIGNAL_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/**/rot_signal.json"`
  matches `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/rot_signal.json` and nothing else.
  Read: `glob.glob(..., recursive=True)` in the shared tree, and a whole-repo file search for `rot_signal.json` (1 file).
  It is tracked. Its `computed_at` is 2026-09-10T22:57Z.
- **Who writes a `rot_signal.json`: one writer.** `lib/research/lists/rot.py main()` writes `<folder>/rot_signal.json`
  beside the two list files it was pointed at, when a person runs `python -m lib.research.lists.rot <folder>`. Read: a
  search of every `.py`, `.sh`, `.json`, `.tf`, `.yaml`, `.ts` and `.tsx` in the repo for the name (24 files name it; one
  writes it). `scoped_amgt.read_list_register` states that it never calls `main()`.
- **What `build_view` does with it.** `find_rot_signal_path()` takes the first match; `build()` loads it, renders ONE line
  with `render_rot_signal()`, and puts that same line on every row as `rot`, plus `rot_signal_path` on the result.
  `build()` is reached only from `build_view.main()` (the by-hand generator) and one test
  (`lib/research/identity/tests/test_slash_safe_key_sites.py`, which replaces `find_rot_signal_path` with a stub).
- **The served route does not use the glob.** `scoped_amgt.read_coverage_freshness` imports `render_rot_signal` and feeds
  it the register computed in memory (`render_rot_signal({"lists": register.get("lists")})`); it never calls
  `find_rot_signal_path` or `build`. Read: every import of `build_view` under `lib/` (three import lines in `scoped_amgt.py`, naming `NEVER`,
  `VENDOR_INPUTS`, `security_key_for` and `render_rot_signal`).
- **Does the deployed package carry it?** The package carries `build_view.py` (the build script's own comment records the
  closure line) and the two list files (`DATA_MEMBERS`). It carries no `org/missions/.../deliverables/` path and no
  `rot_signal.json` (neither is in `DATA_MEMBERS`). INFERRED from
  `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`; the deployed zip was not opened.
- The line the view renders from the stored file today:
  `publishers: not stale (0/2 stale, reviewed 2026-09-10T22:42Z) | social_accounts: not stale (0/267 stale, reviewed 2026-09-10T22:42Z)`.
  The served route's in-memory line is the same text today.

### 2. The act (worker face text)

Row AMGT_RESAPP-Z-W279-S2. `lib/research/freshness/build_view.py` finds the lists' rot signal with a glob over every
worker's deliverables folder (`ROT_SIGNAL_GLOB`). Production code must not read a worker's folder. Give the signal ONE
home, owned by the module that computes it, and make `build_view` read only that home.

1. **Copy, never move.** Copy
   `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/rot_signal.json` byte for byte to
   `lib/research/lists/data/rot_signal.json`. The original stays where it is, unchanged.
2. **`lib/research/lists/rot.py`** gains `SIGNAL_HOME`: the path `data/rot_signal.json` beside the module's own file,
   worked out from `__file__` (no absolute path typed, no device path). Add one docstring line saying this is the
   signal's one home and that `python -m lib.research.lists.rot lib/research/lists/data` writes it there. Nothing else in
   `rot.py` changes: `main()` still writes beside the folder it is given, and you do not run it.
3. **`lib/research/freshness/build_view.py`:** remove `ROT_SIGNAL_GLOB`, its comment block and `import glob`.
   `find_rot_signal_path()` keeps its name and its return type and now answers `Path(rot.SIGNAL_HOME)` when that file
   exists, else `None`. It reads `rot.SIGNAL_HOME` each time it is called (through the module, not a copy taken at import).
   Import `lib.research.lists.rot` at the top of the module; it imports only the standard library. `load_rot_data`,
   `render_rot_signal`, `build` and `main` do not change. Correct the two docstring passages that describe the glob.
4. **A new test file `lib/research/freshness/tests/test_rot_home.py`** with `test_the_view_reads_the_signal_from_its_home`
   (the path found is `rot.SIGNAL_HOME`; with `rot.SIGNAL_HOME` set to a missing file, the path is `None` and the line is
   `build_view.NO_ROT_SIGNAL`) and one test that no line of `build_view.py` names a deliverables folder.

Rules:
1. You do NOT edit `lib/research/api/scoped_amgt.py`, the build script under `infra/`, or
   `lib/research/identity/tests/test_slash_safe_key_sites.py` (it must keep passing: it stubs `find_rot_signal_path` by
   that name).
2. You do not run `rot.main()` or `python -m lib.research.lists.rot`: it looks up every publisher domain, which is a
   network act nobody asked for. The copy in step 1 is the whole content change.
3. The line the view renders must not change (AC3).
4. No deploy, no store write, no vendor call. You do not delete or edit anything under a worker's deliverables folder.

### 3. The criteria

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb15.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: `build_view` names no worker folder for the signal; `rot.SIGNAL_HOME` is inside `lib/research/lists/`, holds a
  byte-equal copy, and the worker folder's file is still there; the view finds the signal at its home; an absent signal
  reads as no signal; C1-C4 PASS; `R78 BB15 AC1 SERVED: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb15.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: `test_rot_home.py` holds `test_the_view_reads_the_signal_from_its_home`, and it and
  `lib/research/lists/tests/test_rot.py` pass; `R78 BB15 AC2 SERVED: YES`; and exit=0.
- **AC3** (bound) `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb15.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the view renders the same line as at the cut; `R78 BB15 AC3 SERVED: YES`; and exit=0.

### 4. The base dry-run

Literal (lines cut at 400 characters), `round78/reads/bb15_base_output.txt`. AC1 FAILED as expected (build), AC2 FAILED as
expected (build), AC3 PASSED as expected (bound):

```
### AC1
FAIL C1 build_view names no worker folder for the signal ROT_SIGNAL_GLOB True; glob call True; lines ['# (deliverables/<slot>/lists/rot_signal.json, not deliverables/<slot>/', 'ROT_SIGNAL_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/**/rot_signal.json"']
FAIL C2 rot.SIGNAL_HOME exists absent
R78 BB15 AC1 SERVED: NO
exit=1
### AC2
FAIL C1 the test file holds test_the_view_reads_the_signal_from_its_home lib/research/freshness/tests/test_rot_home.py
R78 BB15 AC2 SERVED: NO
exit=1
### AC3
   read from org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/rot_signal.json
   publishers: not stale (0/2 stale, reviewed 2026-09-10T22:42Z) | social_accounts: not stale (0/267 stale, reviewed 2026-09-10T22:42Z)
PASS C1 the view renders the same line as at the cut 
R78 BB15 AC3 SERVED: YES
exit=0
```

### 5. Paths

```
lib/research/lists/rot.py
lib/research/lists/data/rot_signal.json
lib/research/freshness/build_view.py
lib/research/freshness/tests/test_rot_home.py
lib/research/lists/tests/test_rot.py                   (read only; it must keep passing)
lib/research/identity/tests/test_slash_safe_key_sites.py   (read only; it must keep passing)
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~5/lists/rot_signal.json   (read only)
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

LOCAL. `worker-light` (about 15 product lines).

### 7. Edges

None inside this group. `build_view.py` rides in the deployed package, so the change reaches the function at the round's
redeploy; there it changes nothing a route runs (no route calls `find_rot_signal_path`). If another round-78 cell edits
`lib/research/freshness/build_view.py` or `lib/research/lists/rot.py`, the two must be chained.

### 8. Not measured, and questions for the issuer

- **The signal being given a home is a month old and will soon be wrong.** It was computed 2026-09-10 and says the social
  list is "not stale". After 2026-10-10T22:42Z the served route (which computes in memory) will say stale and this stored
  file will still say not stale. The ruling asks for a home, and "copying and never moving" is what the cell does. Whether
  the by-hand view should instead compute the signal from the two list files when it runs, as the served route does, and
  keep no stored signal at all, is a ruling. Refreshing the stored file needs `rot.main()`, which looks up publisher
  domains.
- NOT measured: the deployed zip's contents (see section 1); and whether anyone has run `build_view.main()` since
  September.
- AC3's line is a constant taken from the stored file today. If the issuer rules that the signal be refreshed in this
  cell, AC3 is recut.
