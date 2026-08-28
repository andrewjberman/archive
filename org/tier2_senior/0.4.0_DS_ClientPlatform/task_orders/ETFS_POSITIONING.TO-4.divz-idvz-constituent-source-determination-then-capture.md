# TO ETFS_POSITIONING.TO-4 — DIVZ/IDVZ constituents: **DETERMINE THE SOURCE FIRST**, then capture

<task_order id="ETFS_POSITIONING.TO-4" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cell ETFS-c-1 (issuer-capture plane); reads ETFS-a-1, ETFS-a-3</decomp_ref>
<certification>Decomp **CERTIFIED** by `3.0.0_SA_CVO` @59f2c95115 (§6 refused, rewritten @f7c719b56d, refusal discharged). ⛔ Note the difference from TO-1/2/3: **this TO is NOT "uncertified on face"** — it is cut after certification.</certification>
<issued_to>DS-class. Seated: `0.4.0_DS_ClientPlatform` — owns the ETFS_SETUP DS-contract lane (`config/etf_universe.json`'s own owner field).</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED — but ⛔ **SEQUENCED BEHIND `ETFS_POSITIONING.TO-1`. DO NOT INTERLEAVE.** See the sequencing block.</seating_trigger>
<placement>LAPTOP (Rule 26).</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T20:50Z</issued>
<status>superseded — ⛔ **LEAD WORD ADDED 2026-08-28 ~02:5xZ: `to-check.py:_classify_status` reads the FIRST WORD ONLY, and my disposition led with an emoji, so the index read this face as ACTIVE for ~50 minutes while the ruling said SUPERSEDED. The tool is right and my formatting was wrong — this is NOT the instrument-changes case.** ⛔ **SUPERSEDED — NOT COMPLETE, AND THE DISTINCTION IS LOAD-BEARING.** ⚠ **`COMPLETE` would imply the TrueShares BRONZE CAPTURE shipped. IT DID NOT, and a future reader hunting that tree would find nothing and reopen this** (`1.0.0_SA_CTO~Z`'s own caution, adopted). **THE OBJECTIVE IS DISCHARGED BY A DIFFERENT VEHICLE, ON ANDREW'S OWN RULING** — 2026-08-24 ~15:2xZ, VERBATIM: *"This needs to be handled via Bloomberg pipeline structure. We should be accruing all data in same shape via daily bloomberg /terminal-upload schedule with a scoped additional script for this purpose, with that data accruing in correct structure in a relevant opal-data-etfs subfolder."* **He MOVED the capture's vehicle.** Measured: `bbg/2026-08-26/constituents/constituents_issuer_fill.csv`, **DENOMINATOR 187 data rows — PFDE 90 · IDVZ 44 · DIVZ 29 · PFOE 24, ALL FOUR FUNDS**, header carrying `vendor_trueshares_*` + `fill_source`. ⭐ **THE ABSENCE OF `trueshares/` IS COMPLIANCE, NOT A GAP** — and it was established with a DENOMINATOR (the 8 actual top-level prefixes on `opal-data-etfs`; neither `bronze/` nor `trueshares/` among them), **because a guessed prefix returning empty reads identical to a wrong one.** ⛔ **DISPOSITION SET BY THE ISSUING OFFICE 2026-08-28 ~02:0xZ on `1.0.0_SA_CTO~Z`'s per-face measurements (11743), CARRIED AS THEIRS AND LABELLED — I did not re-run them, and re-running the same instrument would be REPETITION, not corroboration.** ⚠ **THIS IS NOT AN AC-LEVEL CERTIFICATION:** the OBJECTIVE is met in the world; whether every acceptance criterion is discharged has NOT been taken by anyone and is `3.0.0_SA_CVO~Z`'s act. **What is settled is that this face is NOT WAITING ON A SEAT** — which is the claim that was manufacturing false dispatches all night.</status>
<priority>P2. ⛔ **BELOW TO-1 DELIBERATELY, AND THE REASON IS ANDREW'S OWN RULING** — see sequencing.</priority>
<authority>**ANDREW-DIRECT 2026-08-21T20:45Z, VERBATIM: *"egreess is allowed, other stuff doesnt really matter at this point just carry it"*** — record `org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20260821_2045Z_EGRESS_ALLOWED_CARRY_THE_REST.md` @d3c0c9c1d2. This fires the sovereign start condition on `ETFS-c-1`. Plus PRD s.10.2 (issuer sheet YES, capture-forward only) and s.10.4 (the ship shape).</authority>
</task_order>

## ⛔ SEQUENCING — WHY THIS IS P2 AND NOT P1

The egress grant makes this cell **actionable**. It does **not** make it urgent, and the distinction is
Andrew's own prior ruling, not my preference.

**PRD s.10.4 — the ship shape is TWO FULL BOOKS (PFDE/PFOE) + TWO SHELLS (DIVZ/IDVZ) UPGRADING FORWARD.
THE PAGE SHIPS ON THAT SHAPE AND DOES NOT WAIT FOR THESE ROWS.** `ETFS_POSITIONING.TO-1`'s
`ETFS-TO1-AC3` already requires the producer to pick up constituent rows **with no code change** when
they land. So this TO **adds a lane; it does not sit on the critical path.**

⛔ **THE THING HE ASKED TO BE DONE RIGHT NOW IS THE RENDERED PAGE.** A newly-unblocked lane that slows
the producer would trade the thing he asked for against a thing he explicitly said could arrive later.
**Finish TO-1, then start here.** If you believe the two can genuinely run in parallel at your seat
without slowing TO-1, say so and I will re-rule — **do not decide it silently in either direction.**

## ⛔ HALF 1 GATES HALF 2 — AND IT MAY MAKE HALF 2 UNNECESSARY

**READ-ONLY. CHEAP. DO IT FIRST.** MSTR relayed a site-Z finding (65770) with an explicit open cell that
is yours to close:

> ***"NOT MEASURED: whether a filepoint feed for DIVZ/IDVZ exists and is simply unwired, or does not
> exist at all. Those take OPPOSITE remedies."***

**DETERMINE WHICH, BEFORE BUILDING ANYTHING.** You already measured (65577) that `silver/holdings`
source distribution is **filepoint 114 of 114** for PFDE/PFOE. The question is whether the same feed
carries DIVZ/IDVZ and is merely unwired.

| outcome | remedy | egress needed? |
|---|---|---|
| **(a) A filepoint feed EXISTS and is unwired** | **WIRE IT.** No capture, no scraping, no vendor egress | **NO** |
| **(b) No feed exists** | Half 2 — the TrueShares issuer-sheet capture | Yes (granted) |

⛔ **BUILD-LADDER RUNG 2 IS THE WHOLE POINT: IF (a) IS TRUE, HALF 2 IS A DUPLICATE OF SOMETHING THE
ESTATE ALREADY HAS, AND BUILDING IT WOULD BE THE EXPENSIVE WRONG ANSWER TO A CHEAP QUESTION.** An
egress grant is permission, not instruction — *availability is not authorization's mirror image:
authorization is not obligation.*

**Report Half 1's answer before starting Half 2.** One line to me is enough.

## ⛔ THE THREE TRAPS — carried VERBATIM from site Z, because a re-derivation hits them first

**1. A COUNT IS NOT A LIST.** `TOTAL_NUMBER_OF_HOLDINGS_IN_PORT` returns **DIVZ=30, IDVZ=46**.
**Bloomberg knows HOW MANY and will not enumerate WHICH.** ⛔ *"That field reads exactly like partial
coverage and is not — anyone re-deriving this will hit it first and conclude the data is there."*
**If you find yourself concluding the constituents exist because a count came back, stop: that is this
trap firing.**

**2. ZERO `NOT_AUTHORIZED` on the Bloomberg side. THIS IS NOT AN ENTITLEMENT GAP, SO IT CANNOT BE
BOUGHT OUT OF.** Forecloses the obvious remedy before someone spends a week on it. **Do not propose a
Bloomberg entitlement purchase.**

**3. PRE-EMPTING A FALSE GAP REPORT (unrelated but adjacent):** the dividend-yield field is **80/109 =
73.4%**, and the 29 blanks are AMD, AMZN, ANET, BA, DECK, CIEN, IDXX and similar — **genuine
non-dividend-payers. A CORRECT ECONOMIC FACT.** A naive coverage read files that as a 27% hole. **It is
not a defect and it is not yours to fix.**

## Half 2 — the TrueShares capture (**ONLY IF Half 1 returns (b)**)

**The cause is ALREADY DIAGNOSED. DO NOT SIZE THIS AS AN INVESTIGATION.**
`infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:381` defines
`TS_HOLDINGS_ENABLED`; `:420` defines `fetch_trueshares_holdings`. **CTO source-confirmed the flag is
never branched on and the function is never called.** `DIVZ 0 / IDVZ 0` is a **missing call site** — not
a vendor problem, not a data-availability unknown.

**LAW THAT BINDS THE CAPTURE — the egress grant does NOT touch any of it:**
- ⛔ **CAPTURE-FORWARD ONLY. THERE IS NO TRUESHARES BACKFILL** (PRD s.10.2). **The load-bearing check is
  `distinct`, NOT row count** — a row count grows on re-capture of the same day and proves nothing.
- **PRODUCTION = SCHEDULED.** An ad-hoc capture run is a **QA instrument**; its artifacts are **never**
  production evidence.
- **No shadow path, no parallel emitter, no standing comparator** (Andrew, complete veto, twice).
- **ALERT/MONITOR MORATORIUM** — the run manifest and log ARE the record. Build no checker.
- **Rule 15** (`from __future__ import annotations`), **no non-ASCII** in anything running on AWS.

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO4-AC1** | ⭐ **Half 1 ANSWERED: (a) unwired-feed or (b) no-feed, stated with its denominator and the trees searched.** An ABSENCE verdict names every tree it enumerated | `ETFS-c-1` | APPLIED |
| **ETFS-TO4-AC2** | If **(a)**: the feed is wired and DIVZ/IDVZ rows appear in `silver/holdings` on a **SCHEDULED** run. If **(b)**: `ETFS-TO4-AC2` is **N/A, declared**, and AC3–AC4 carry the work | `ETFS-c-1` | EXERCISED |
| **ETFS-TO4-AC3** | If **(b)**: the capture call site exists and is **exercised** — `fetch_trueshares_holdings` actually called, flag actually branched on | `ETFS-c-1` | EXERCISED |
| **ETFS-TO4-AC4** | If **(b)**: capture runs on a **SCHEDULE**; **`distinct` day-count grows across runs** (never a row count) | `ETFS-c-1` | EXERCISED |
| **ETFS-TO4-AC5** | ⛔ **The shells UPGRADE with NO producer code change** — rows land, `ETFS-TO1-AC3`'s path picks them up. **If a code edit is needed, AC5 FAILS and the producer is wrong, not the capture** | `ETFS-c-1`, `ETFS-d-1` | EXERCISED |

<proof_of_spec>
  <!-- ISSUANCE half (COO). Ids firm-tokened; cell_refs are the join for CVO's bidirectional alignment.
       A criterion without cell_refs is REFUSED, never retrofitted.
       INVOCATION IS POSITIONAL -- no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO4-AC1,ETFS-TO4-AC2,ETFS-TO4-AC3,ETFS-TO4-AC4,ETFS-TO4-AC5
       CHECK THE RC, NEVER THE OUTPUT STRING -- the usage banner contains the vocabulary of BOTH
       verdicts, and the 2-arg form returns a clean rc=0 that says COVERAGE UNCHECKED. -->
    <criterion id="ETFS-TO4-AC1" cell_refs="ETFS-c-1"/>
    <criterion id="ETFS-TO4-AC2" cell_refs="ETFS-c-1"/>
    <criterion id="ETFS-TO4-AC3" cell_refs="ETFS-c-1"/>
    <criterion id="ETFS-TO4-AC4" cell_refs="ETFS-c-1"/>
    <criterion id="ETFS-TO4-AC5" cell_refs="ETFS-c-1, ETFS-d-1"/>
  <expected_criteria>ETFS-TO4-AC1,ETFS-TO4-AC2,ETFS-TO4-AC3,ETFS-TO4-AC4,ETFS-TO4-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Scope guard · surprise channel · reporting

⛔ **Andrew's DS scope-lift still binds and the burden is MINE as tasker:** this TO qualifies **exactly**
the work above and nothing else. **It does NOT re-open any other held item at your seat.**

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts**; **BLOCKING** routes same-turn to me,
cc CVO; **ARMED** needs a named disarm owner same-turn; **DISARMED ≠ REMEDIATED.** Mid-round the spec is
**FROZEN** — route, do not adjudicate.

**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN.** **EVERY COMMIT REPORT STATES ITS PUSH STATE** — never
bare "landed."
