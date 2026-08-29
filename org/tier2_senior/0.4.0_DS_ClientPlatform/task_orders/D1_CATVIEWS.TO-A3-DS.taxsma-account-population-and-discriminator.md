# TO D1_CATVIEWS.TO-A3-DS — MEASURE THE TAX SMA ACCOUNT POPULATION AND ITS DECLARED DISCRIMINATOR

<task_order>
<decomp_ref>workflows/atom_decomposition/runs/D1_CATVIEWS_INC3/20260829T032000Z/run.json — `INC3-A` (measure the Tax SMA account population at Schwab 0824 and its DECLARED discriminator; READ-ONLY; blocks `INC3-B` and `INC3-C`). **NO new cell.** ⛔ **RUN_CLASS is FOCUSED and the run is AUTHOR-MEASURED, NOT CERTIFIED** — the Rule 14(a)-(e) rectangle and sealed-mutant certification were OMITTED, with the boundary and its cost declared in-file by `1.0.0_SA_CTO~Z`. **Anything citing this cell inherits AUTHOR-MEASURED status and must say so.**</decomp_ref>
<issued_to>`0.4.0_DS_ClientPlatform~Z` — same project (`D1_CATVIEWS`), so no Rule 27 collision with the increment-2 faces already at that seat.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-29T03:2xZ</issued>
<status>CLOSED 2026-08-29 ~04:1xZ by `2.0.0_SA_COO~Z` (issuer) — **4 of 4 PASS, ZERO FAIL, ZERO UNCOMPUTABLE**. ⛔⛔ **CLOSED IS NOT CERTIFIED ON THIS FACE. AMENDED 2026-08-29 ~05:0xZ by the same issuer: the instance reads `proof-of-spec-check` rc=1 INVALID, 1 violation, and it CANNOT BE CLEARED BY ANY EDIT TO THE INSTANCE.** The cited cell `INC3-A` **EXISTS** in the decomp — but the estate's cell-id grammar is `PREFIX-<lowercase>-<digits>`, `INC3-A` is a bare uppercase suffix matching nothing, so the id space parses **EMPTY** and every `cell_ref` reports unknown (`3.0.0_SA_CVO~Z`, msg 16272). ⚠ **THE VIOLATION LINE SAYS "does NOT exist", WHICH IS WRONG AND IS THE HALF THAT TRAVELS** — the alignment FRAME carries the true diagnosis, `decomp id space = 0 distinct cell id(s)`. ⛔ **BLAST RADIUS: all five INC3 packages share the form, so EVERY INC3 instance is uncertifiable until the source is fixed.** ✅ **REMEDY (a) CHOSEN — the decomp declares cells in the conforming form and the TOs cite those; ONE edit at the source. OWNER: `1.0.0_SA_CTO~Z` as the decomp's author.** ⛔ **NOT a remedy: editing this instance, or widening `CELL_ID_RE` (that changes the id grammar for every project).** ✅ **THE CLOSURE STANDS ON THE SCORING, which is untouched by a citation-grammar defect: the roster rule cited at `taxsma_registry.py:144-149 @7d97a8bed2`, TWO negative controls in opposite directions, and the known-good account reconciled. THE FACE IS CLOSED; THE INSTANCE CERTIFIES ONLY AFTER THE SOURCE FIX LANDS.** ⚠ **AND THE ISSUER CLOSED THIS FACE WITHOUT RUNNING THE CHECKER — the defect was found by a certifier ~50 minutes later, not by the closure.** --- ORIGINAL CLOSURE TEXT FOLLOWS: instance `D1_CATVIEWS.TO-A3-DS_PROOF_OF_SPEC.json` 18,235 B. ⛔ **AND IT SCORED THE *AMENDED* BAR, NOT THE ONE IT WAS CUT WITH — CHECKED, BECAUSE THIS TO WAS AMENDED FIVE TIMES IN FORTY MINUTES:** `INC3A-AC1`'s `criterion_verbatim` carries the `AMENDED:` clause, so the Bump/Macy sizing requirement was scored, not the superseded wording. **A 4-of-4 against a superseded bar reads identically to this one, and only the verbatim distinguishes them.** ⭐ **THE CONTROLS ARE THE REASON THIS CLOSES RATHER THAN MERELY PASSING:** `AC2` cites the rule at `taxsma_registry.py:144-149 @7d97a8bed2` — `list_active()` filtering `status == "active"`, with the docstring stating a `pending_resolution` account is DELIBERATELY excluded — **a declared rule at file:line @ commit-ish, not a docstring inference**; `AC3` supplies **TWO negative controls in opposite directions** (5,374 of 5,375 xref ids absent from the roster, named exemplar `0010048935`; and `0035940058` Bump enrolled-but-status-gated), so the discriminator is shown REFUSING on both axes; `AC4` reconciles the one known-good account `0027265115` as 1 of 3 active and 1 of 5 enrolled without dropping it. ⭐ **ANDREW'S RULED FIVE AND THE ROSTER'S FIVE AGREE — the population is now `held` AND `measured`.** ⛔ **DO NOT SEAT; DO NOT RE-EXECUTE (NEVER#2).** ⚠ **WHAT THIS TO DID NOT DO, AND MUST NOT BE READ AS HAVING DONE:** it did not run `INC3-B`, did not touch a packaged member, and did not choose between the roster route (3 of 5 today) and the 0833 route (all 5, `$6,445,461.07`) — **that choice is AT ANDREW and nothing here pre-empts it.** --- PRIOR STATUS, PRESERVED: ~~pending — CUT AND CLEARED TO START. This is the ONLY increment-3 package with no interaction with the pending sovereign delete: it is READ-ONLY, it touches no packaged member, and it blocks `INC3-B` and `INC3-C`.~~</status>
<priority>P1 — it blocks two downstream packages, and Andrew's word on increment 3 is *"done tonight"*.</priority>
<expected_criteria>INC3A-AC1,INC3A-AC2,INC3A-AC3,INC3A-AC4</expected_criteria>
</task_order>

## 1. WHY THIS EXISTS — THE BLOCKER IS THE RUN, NOT THE DESIGN

`1.0.0_SA_CTO~Z` **retracted** their own earlier ruling that Tax SMA was *"structurally unbuildable"*.
They had audited the wrong artifact. Measured, and it is the whole finding:

```
  registry ALREADY declares  ("tax","tax","Tax-Managed SMA",True,"ALT Strategies")
  resolve_any ALREADY resolves it . the ALT bucket ALREADY sums
  consolidator:689 RAISES on an unresolved key -> a mis-keyed entry fails LOUD, never folds silently
  => ZERO consolidator edits are required to light up ALT Strategies.
```

⭐ **AND THE SMA TRACKING IS ALREADY CORRECT, PROVEN BY ARITHMETIC:** 49F `by_model` has 7 keys;
`opal_div_sma 18,783,379.81 + opal_growth_sma 4,011,386.44 = 22,794,766.25`, **exactly the served SMA
L1 total**. Andrew was right that we track SMA strategy values correctly. **`ALT Strategies` reads
`0.00` solely because no `tax` key ever enters** — the taxsma pipeline exists and is **six weeks stale
and single-account** (gold: 1 object, account `0027265115`, date `2026-07-17`).

## 2. THE WORK — READ-ONLY, AND IT ENDS AT A NUMBER WITH A RULE BESIDE IT

Establish **which Schwab 0824 accounts are Tax SMA accounts, and by what declared rule**.

⭐ **START HERE, from `1.0.0_SA_CTO~Z`'s adversary run — this is an ASSIGNMENT, not a finding:**
`data/assets/scripts/silver/bd49f_fact_allocation.py`. The taxsma gold groups `alloc_asset` by
`schwab_account_id` (`:142`), so **that allocation feed is very likely where the account population is
actually decided**, and it was never opened. Adjacent and also uncited: `schwab_conversion.py`,
`schwab_projections.py`, `bd49f_dim_conversion.py`, `conversion_manifest.py`.

## 3. ACCEPTANCE

<proof_of_spec>
  <criterion id="INC3A-AC1" cell_refs="INC3-A"/>
  <criterion id="INC3A-AC2" cell_refs="INC3-A"/>
  <criterion id="INC3A-AC3" cell_refs="INC3-A"/>
  <criterion id="INC3A-AC4" cell_refs="INC3-A"/>
  <expected_criteria>INC3A-AC1,INC3A-AC2,INC3A-AC3,INC3A-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-A3-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4, firm-tokened `INC3A-ACn`. Cells: 1 (`INC3-A`), from the FOCUSED run `workflows/atom_decomposition/runs/D1_CATVIEWS_INC3/20260829T032000Z/run.json`. FORWARD 4 of 4 carry a cell_ref; BACKWARD 1 of 1 reachable. ⛔ **THAT DECOMP IS AUTHOR-MEASURED, NOT CERTIFIED — no independent certifier signed a rectangle, and anything citing these cells INHERITS AUTHOR-MEASURED STATUS and must say so.**</alignment_denominators>
</proof_of_spec>

**`INC3A-AC1` — THE ACCOUNT SET, ENUMERATED, WITH ITS DENOMINATOR.**
Print the Tax SMA account set at Schwab 0824 **and the denominator it was drawn from** (accounts
considered, not just accounts matched). ⛔ **A bare list is not the deliverable — a list without its
denominator cannot distinguish "these are the Tax accounts" from "these are the ones my query found".**

**`INC3A-AC2` — THE MEMBERSHIP RULE, DECLARED AND CITED AT `file:line @ <commit-ish>`.**
State the rule that DEFINES membership, quoting the code that implements it. ⛔ **NOT a name match.
NOT an inference from an account appearing in the stale gold object.** If the rule turns out to be
implicit rather than declared anywhere, **say that** — an undeclared discriminator is itself the
finding, and it changes `INC3-B` from a re-run into a specification task.

**`INC3A-AC3` — A NEGATIVE CONTROL ON THE DISCRIMINATOR.**
Name an account the rule EXCLUDES and show it excluded. ⛔ **A rule that has never been observed
refusing anything has not been shown to discriminate**, and the single stale account
(`0027265115`) is not evidence of a working filter.

**`INC3A-AC4` — RECONCILE AGAINST THE ONE KNOWN-GOOD NUMBER.**
The current gold holds exactly one account at `2026-07-17`. State whether that account is IN the set
this TO derives, and if not, why not. ⛔ **A derived set that silently drops the only account we have
ever produced is a defect in the derivation, not a correction of the past.**

## 3a. ⛔⛔ AMENDED 2026-08-29 ~03:3xZ BY `2.0.0_SA_COO~Z` (issuer) — `AC2`'s ANSWER IS ALREADY LOCATED, AND THE REAL QUESTION MOVED

`1.0.0_SA_CTO~Z` measured the producer at source **two minutes after this TO was cut**:
```
  build_fact_taxsma_report.py
    :47  "Scope: Chiles-only for now (Bump/Macy need internal-accountId discovery --
          follow-on; the xref carries only the external form)."
    :43  "Chiles: z0822596361 -> 0027265115."
    :41  BRIDGE resolved via blackdiamond/49f/silver/dim_account_xref
    :44  an account that cannot bridge carries schwab_account_id=NULL +
          bridge_method='unresolved' (NEVER DROPPED -- Rule 17)
```
>> ⛔ **THE SINGLE GOLD ACCOUNT `0027265115` IS CHILES, AND IT IS ALONE BY *DECLARED SCOPE*, NOT
   BECAUSE THE PIPELINE STALLED. TWO DIFFERENT BLOCKERS WERE WEARING ONE SYMPTOM:** the six-week
   staleness is real AND separate; the single-account part has a named cause and a named follow-on
   (internal-accountId discovery). <<
⭐ **`AC2` IS THEREFORE ANSWERABLE IMMEDIATELY — the rule IS declared, in a docstring.** That is a
find, not a failure: this TO asked for the rule cited at `file:line`, and it exists.
⛔ **SO `AC1`/`AC3`/`AC4` GET *MORE* IMPORTANT, NOT LESS — the live question is no longer "what is the
rule" but "WHAT ARE WE OMITTING, AND HOW BIG IS IT."** Add, as part of `AC1`:
```
  MEASURE WHAT BUMP AND MACY HOLD -- the SIZE of the omission, not just its existence.
  "ALT is short two accounts" and "ALT is short two accounts worth $X" are different facts,
  and only the second lets anyone judge whether lighting ALT tonight is honest.
```
⚠ **BOUND, CARRIED VERBATIM FROM `1.0.0_SA_CTO~Z` AND NOT UPGRADED: the docstring names THREE
(Chiles, Bump, Macy). Whether THREE is the COMPLETE Tax SMA population is NOT established by that
read — it is the producer's scope note, not an account census. DO NOT CONVERT "three" INTO A
DENOMINATOR.** Establishing the true denominator is `AC1`'s job and remains open.

## 3b. ⛔ WHAT THIS FORCES ON ANY DOWNSTREAM `INC3-B`/`INC3-C`, RECORDED HERE BECAUSE NEITHER IS CUT YET

```
  INC3-B as proposed -- "run the existing taxsma silver+gold CURRENT across the FULL ACCOUNT SET"
  -> ⛔ CANNOT DELIVER AS WRITTEN. A run tonight REPRODUCES CHILES-ONLY. Bump and Macy are
     blocked on INTERNAL-ACCOUNTID DISCOVERY, which is a FOLLOW-ON BUILD, not a re-run.
     Cutting B as a re-run would produce a green run that silently ships a short population.
```
>> ⛔ **AND THE CONSEQUENCE IS THE 0.76%-VERSUS-MAPPING-GAP SHAPE, ONE NIGHT LATER: `ALT Strategies`
   CAN be lit tonight with CHILES ALONE — a REAL number over a STRUCTURALLY INCOMPLETE population, on
   an advisor-facing card, with NOTHING on the page saying it omits two accounts. Last night that
   class was caught by a denominator. Here we ALREADY KNOW the population is short.** <<
⛔ **RULING: IF `ALT Strategies` LIGHTS WITH A KNOWN-SHORT POPULATION, THE ARTIFACT MUST CARRY A
COVERAGE DECLARATION IN A FIELD A CONSUMER CAN REJECT ON.** This is not a new gate — it is CLAUDE.md's
standing *"a value must carry its claim"* applied at the point of use, and the consuming half is the
whole mechanism. **A number whose incompleteness is known to the producer and invisible to the reader
is the failure that law exists to prevent.**

## 3c. ⛔⛔ SOVEREIGN RULING — THE POPULATION IS **FIVE**, AND ALL FIVE ARE ATTAINABLE

> **Andrew, 2026-08-29 ~03:3xZ, VERBATIM (relayed same-turn by `1.0.0_SA_CTO~Z`, msg 15862):**
> ***"There are 5 accounts and we definitely can get all of them."***

```
  POPULATION           = 5   ANDREW-DIRECT, SOVEREIGN. This IS the denominator.
  producer docstring   = 3   (Chiles + Bump/Macy as follow-on)   -> INCOMPLETE
  gold artifact today  = 1   (Chiles, 0027265115)
  ATTAINABLE           = ALL FIVE.
```
>> ⛔ **THIS OVERTURNS §3a/§3b's LIKELY LANDING. The identity bridge is SOLVABLE, not a hard blocker.
   "Chiles-only tonight plus a coverage label" is NO LONGER THE EXPECTED OUTCOME — SOLVE THE
   BRIDGE.** <<
⭐ **AND THE BOUND IS WHAT MADE THIS LAND CLEANLY. §3a said *"the docstring names THREE ... DO NOT
CONVERT 'three' INTO A DENOMINATOR."* Andrew supplied FIVE. Had 3 been published as the denominator,
the whole item would have been sized against a number the sovereign knows is wrong — and every
downstream check would have AGREED with it, because they would all inherit the same wrong frame.**

**`AC1` IS RE-CUT BY THIS RULING — the discriminator moved:**
```
  NOT   "measure the population"  -- it is RULED at 5.
  NOW   ENUMERATE THE 5, and measure WHICH RESOLVE through
        blackdiamond/49f/silver/dim_account_xref TODAY and which do not.
        PRINT: RESOLVED / UNRESOLVED of 5.
```
⭐ **THE INSTRUMENT ALREADY EXISTS AND IT IS THE PRODUCER'S OWN RULE-17 BEHAVIOUR:** `:44` — an
account that cannot bridge carries `schwab_account_id=NULL` + `bridge_method='unresolved'` and is
**NEVER DROPPED**. **So unresolved accounts are VISIBLE, not silent — that is the progress meter
toward 5 of 5, and it needs nothing built.**
⭐ **AND THE GOLD NEEDS NO CHANGE TO HANDLE FIVE:** it already GROUPS BY `schwab_account_id`. **It
needs five BRIDGED INPUTS, not new code.** The real work is the XREF.

⛔ **THE ACCEPTANCE DENOMINATOR IS NOW 5, AND A `> 0` CRITERION IS BANNED:**
```
  BANNED     "ALT aum > 0"  -- a ONE-account ALT and a FIVE-account ALT BOTH satisfy it,
             and only one is the deliverable. A criterion both outcomes pass is not a criterion.
```
⛔⛔ **AND MY OWN FIRST FORM OF THE REQUIRED CRITERION WAS ALSO DEFECTIVE — CORRECTED HERE.** I wrote
*"ALT Strategies covers 5 of 5 Tax SMA accounts."* **That HARDCODES the denominator**, and
`3.0.0_SA_CVO~Z` named why it fails: **Andrew's `5` is HELD, not MEASURED — a sixth account later
makes a CORRECT BUILD FAIL A STALE LITERAL. It is the market-valued-literal defect wearing a
population's clothes**, and this estate has been burned by a control pinned to a constant the fix
would move.
```
  REQUIRED   coverage scored on the PRODUCER plane as  `resolved / declared`,
             with the DENOMINATOR'S SOURCE NAMED AND STAMPED:
                `held`     when a sovereign ruled it   (today: Andrew's 5)
                `measured` when an artifact enumerated it
  BANNED     a hardcoded integer denominator in the criterion text -- including "5".
  BANNED     "ALT aum > 0" as a DONE-criterion.  (LEGAL as render mechanics: describing
             when a row draws is a different claim from whether the item is complete.)
```
⭐ **THE DISTINCTION THAT KEEPS `> 0` USABLE WHERE IT IS HONEST IS `0.4.0_DE_ClientPlatform~Z`'s, and
they inoculated their own sentence against being lifted into a scoring criterion BEFORE anyone
lifted it.** That pre-emption is why it survives as mechanics rather than being withdrawn.
⛔ **THE §3b COVERAGE DECLARATION IS DEMOTED TO A FALLBACK, NOT THE PLAN.** It applies ONLY if the
bridge genuinely resists — **and if it does, that returns to ANDREW as a fork. It does not get
decided by whichever seat hits it first at 04:00Z.**

## 3d. ⛔⛔ WHERE THE `5 of 5` DENOMINATOR MAY BE READ — AND THE OBVIOUS INSTRUMENT IS THE BLIND ONE

`3.0.0_SA_CVO~Z` measured the collection rung (msg 15874) and it changes where this TO may read:
```
  XREF  build_schwab_bd_account_xref.py:44   unbridged -> schwab_account_id=NULL +
        bridge_method='unresolved', NEVER DROPPED (Rule 17).  UNRESOLVED ARE VISIBLE HERE.
  GOLD  build_dim_taxsma_report.py :142 / :252 / :289
        THREE BARE `groupby("schwab_account_id")` calls. NO `dropna=` anywhere.
        MEASURED on the installed pandas 3.0.3, that exact call shape:
          5 rows (2 real ids, 3 NULL) -> bare groupby = 2 groups, 2 rows. 3 SILENTLY DROPPED.
          dropna=False                -> 3 groups, 5 rows survive.
```
>> ⛔ **RULE 17's "NEVER DROPPED" HOLDS AT THE RUNG IT WAS WRITTEN FOR AND IS UNDONE ONE RUNG LATER
   BY A LIBRARY DEFAULT. The xref PRESERVES the unresolved accounts; the gold DELETES them.** <<
```
  AT THE GOLD ARTIFACT:
    "2 bridged, 3 unresolved"  -> 2 account= partitions
    "the population is 2"      -> 2 account= partitions
  BYTE-IDENTICAL. AN ABSENCE AND A TRUE-SMALL-POPULATION READ THE SAME.
```
⛔⛔ **AND THE NATURAL WAY TO ANSWER *"how many accounts does ALT cover?"* IS THE BLIND ONE:** counting
`account={schwab_account_id}/` partitions, or reading `:289`'s `by_acct`. **Both equal the RESOLVED
count and can NEVER reveal the shortfall.** A seat measuring coverage at the deliverable would report
**`2 of 2 = 100%` while three accounts are missing — WITH A DENOMINATOR PRINTED, which is exactly what
would make it convincing.**
>> ✅ **THEREFORE, BINDING ON `AC1` AND `AC4`: THE DENOMINATOR COMES FROM THE XREF, OR FROM ANDREW'S
   RULED 5. NEVER FROM THE GOLD PARTITIONS AND NEVER FROM `by_acct`.** The xref is not the *better*
   instrument here — **it is the ONLY one. No substitute exists.** <<

⚠ **PROVENANCE, PER *A VALUE MUST CARRY ITS CLAIM*: the `5` is ANDREW-RULED, therefore `held`, NOT
`measured`.** The instance must stamp it that way. **A sovereign ruling is excellent authority and it
is still not a measurement** — if the xref enumerates a different number, that is a FINDING to route
back to Andrew, **not a discrepancy to quietly reconcile toward either value.**

⚠ **A CHEAP FIX EXISTS AND IS DELIBERATELY NOT TAKEN TONIGHT:** `dropna=False` at `:142`/`:252`/`:289`
would make unresolved accounts visible at gold too. **`build_dim_taxsma_report.py` is NOT a packaged
member, so it carries no rebuild obligation — but it IS an `INC3-B` input, and changing collection
semantics mid-item is how a measurement stops comparing to its own baseline.** SURFACED, NOT CHASED;
owned by whoever cuts `INC3-B`. **Not this TO's act.**

## 3e. ⛔⛔ EXECUTED — AND IT CORRECTS §3d's BINDING INSTRUMENT. THE DISCRIMINATOR IS A **ROSTER**, NOT THE XREF AND NOT THE DOCSTRING

`0.4.0_DS_ClientPlatform~Z` executed `INC3-A` READ-ONLY (msg 15902). Zero S3 writes, no vendor egress.

**`AC2` ANSWERED — ONE PLANE OVER FROM WHERE *THREE SEATS* PLACED IT:**
```
  taxsma_registry.py:144      list_active() -> [a for a in accounts if a["status"]=="active"]
  lambda_function.py:252-273  discover_accounts() -- the roster is "the SINGLE source of truth
                              for which accounts the ETL pulls"; RAISES on 0 active
  ARTIFACT  s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json
            VersionId lNH3od2BprexiXQDjAxntCJjcNB_MK5t, LastModified 2026-08-27T22:48:18Z
```
>> ⛔ **THE `:47` DOCSTRING IS A SCOPE NOTE FROM 2026-07-17 AND IT IS STALE. Its very next sentence is
   the one that governs: *"This module processes EVERY ACCOUNT PRESENT IN THE BRONZE PARTITION."* THE
   PRODUCER APPLIES NO MEMBERSHIP FILTER AT ALL** — the population is decided UPSTREAM by the roster.
   **A DOCSTRING IS NOT A DISCRIMINATOR; `status` IS, AND IT IS A FIELD A CONSUMER CAN REJECT ON.** <<

**THE ROSTER, ENUMERATED — DENOMINATOR 5:**
```
  0027265115  Chiles                   active              bd 22596361  xref
  0035940058  Bump                     pending_resolution  -            -
  0091939812  Macy                     pending_resolution  -            -
  0084073310  Nixon, Matthew & Malita  active              bd 22659431  tier-3
  0076459710  Tracey, Shawn            active              bd 23221671  tier-3
```
⭐ **ANDREW SAID FIVE; THE ROSTER INDEPENDENTLY CARRIES FIVE. TWO INSTRUMENTS, ONE NUMBER — so the
population is no longer merely `held`, it is `held` AND corroborated `measured`.**

⛔⛔ **AND §3d's BINDING INSTRUMENT WAS WRONG. MEASURED, NOT ARGUED:**
```
  xref-resolved  1 of 5   (Chiles only)
  roster-active  3 of 5   (Chiles, Nixon, Tracey)
  Nixon and Tracey are ACTIVE, carry RESOLVED bd_internal_ids, and are ABSENT FROM THE XREF.
```
>> ⛔ **I RULED THE XREF WAS "NOT THE BETTER INSTRUMENT — THE ONLY ONE." IT UNDER-REPORTS BY TWO.**
   `3.0.0_SA_CVO~Z` proved GOLD was blind and I moved straight from *"gold is blind"* to
   *"therefore the xref"* **without testing the xref.** **ELIMINATING ONE BAD INSTRUMENT DOES NOT
   VALIDATE THE NEXT ONE YOU NAME** — and the xref is a BD-IDENTITY BRIDGE, not a membership roster,
   so it answers a different question and was never the discriminator. <<
```
  CORRECTED AND BINDING ON AC1/AC4:
    THE DISCRIMINATOR  = taxsma_roster.json `status == "active"`  (the ETL's own source of truth)
    THE DENOMINATOR    = the roster's full enrolment (5), corroborated by Andrew's ruling
    THE XREF           = evidence about BD-IDENTITY RESOLUTION ONLY. It is NOT a coverage meter
                         and must never be quoted as one.
    GOLD PARTITIONS / by_acct  = still BARRED (§3d) -- blind by NULL-key drop.
```
⚠ **SEPARATE FINDING, SURFACED NOT CHASED: the taxsma pull lambda has NO SCHEDULE ON EITHER
EventBridge PLANE.** That is a real gap and it is not this TO's act.
⚠ **AND IT COMPOSES WITH `1.0.0_SA_CTO~Z`'s 0833 RE-SCOPE:** the roster route reaches **3 of 5**
today (Bump and Macy sit at `pending_resolution`), while **all 5 carry balances in 0833
`dim_balance`** — which is precisely why the 0833 question is at Andrew. **Neither route is chosen
here.**

## 4. BOUNDS THAT BIND THIS TO

⛔ **READ-ONLY. NO WRITES, NO COMMITS TO ANY PACKAGED MEMBER, NO PRODUCER EDITS.** This TO exists to
make `INC3-B`/`INC3-C` specifiable; it must not begin them.
⛔ **DO NOT COMMIT TO ANY OF THE 22 PACKAGED MEMBERS WHILE THE RESERVED RELAND IS PENDING.** The gold
lambda is repinned to `73c2dea263` and Andrew's word is being sought AGAINST THAT BUILD; a member
commit in this window re-stales it and spends a reserved-category act on a superseded package.
⛔ **THE MEMBER LIST IS THE AUTHORITY, NEVER A PATH PREFIX OR A SUFFIX** — `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`, the `PACKAGE` literal. **ELEVEN of the 22 live OUTSIDE `data/mdpf/scripts/gold/`**, including `lib/trading_calendar.py` and a `.yaml` config (`route_bindings.yaml`).
⛔ **NO SHADOW PIPELINE** (Andrew veto) — Tax folds into the EXISTING scripts. **NO new monitor or alarm.**
⛔ **`muni` STAYS NULL AND THAT IS CORRECT.** Andrew: *"Muni to my knowledge does not exist yet"*,
*"Tax is the only ALT Strategy that is currently being traded."* **A criterion asserting
`ALT == tax + muni` is WRONG** — `1.0.0_SA_CTO~Z` flagged muni as an identical gap and Andrew corrected them.
⛔ **RESOLVE THE TRADING CALENDAR BEFORE ANY STALENESS CLAIM.** Counting six weeks is a claim about
trading days, not calendar days.
⛔ **`CLIENT_L1_HELD` IS NOT LIFTED.**

## 5. ⚠ A HAZARD ALREADY FOUND IN THE *DOWNSTREAM* PACKAGE — DO NOT INHERIT IT

`3.0.0_SA_CVO~Z` and `0.4.0_DE_ClientPlatform~Z` measured that **`by_model` EXISTS ON TWO PLANES WITH
DIFFERENT KEY SPACES**:
```
  GOLD    by_model keyed by `model_key`    7 entries, incl. opal_div_sma / opal_growth_sma
  SERVED  by_model keyed by `model_name`   5 entries, DISPLAY STRINGS, ZERO SMA keys
```
>> ⛔ **`INC3-C`'s wording — *"emit `tax` into 49F by_model, same shape as `opal_div_sma`"* — IS
   AMBIGUOUS ACROSS THOSE PLANES, AND THE ANALOGY CARRIES A GAP WITH IT: if `tax` follows
   `opal_div_sma` exactly, it lands on GOLD and NEVER REACHES THE SERVED PLANE, because
   `opal_div_sma` does not either.** <<
**This TO does not resolve that** — it is named here so `INC3-A`'s output is not written in a way that
assumes one plane. **When `INC3-C` is cut its acceptance must name, per row: WHICH ARTIFACT, WHICH
PLANE, WHICH KEY FIELD.** Whether the served array gains the entry at all is a SCOPE question the
PRD does not answer, and it is being routed separately.

## 6. NOT IN THIS TO

⛔ **`INC3-E` / PRD `I2` — GLOBAL CLIENT AGGREGATION — IS A SOVEREIGN FORK AND IS NOT CUT AS A BUILD
TO BY ANYONE.** `global`'s Client is 49F-only DELIBERATELY, holding basis B's P0 identity
`opal_aggregate == model_aua + non_model_aua`. It is with Andrew; `1.0.0_SA_CTO~Z` carries it.
