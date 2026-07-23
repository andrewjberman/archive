# Cottonwood Daily Model-Allocation BACKFILL — Full BD-Surface Mechanism Campaign

**Author:** `4.0.0_SA_CRO` (Chief Research Officer) · **Home:** `org/tier1_exec/4.0.0_SA_CRO/` · **Date:** 2026-07-22
**Extends:** RCN-0001 (Black Diamond teardown) · **Recon linkage:** the BD half of the MDPF Cottonwood backfill question.
**Commissioned:** Andrew-direct, 2026-07-22 ~22:10Z, verbatim: *"hit the motherfuck (that means hit a lot and
everywhere) on BD to identify if there is some possible way of identifying a mechanism for backfill of daily
allocation count and value for each opal model."*
**Egress:** Andrew's explicit per-use word above authorizes **read-only cot-BD** probing. **Firm-sep binds — cot-BD
ONLY** (`blackdiamond/cot/session` + `opal-data-cot`); the BD platform serves 49F too and 49F stays untouched (COO
222937Z). **No production template is mutated; 0.6.2's `templates_enriched/` paths untouched.**
**Verdict authority (CTO v1.21 / COO 224310Z):** this campaign now carries the **full temporal-vs-current verdict**
that gates the Cottonwood backfill design — 0.6.2's second live probe is retired into it.
**Grades:** **[GROUNDED]** read at source · **[MEASURED]** live-tested (prior addenda) · **[HELD]** gated on live
execution (the qt5 window run, §7) · **[RULED OUT]** measured dead end · **[UNPROBED]** needs a call not yet made.

> **THE ANSWER, one paragraph.** I swept the entire BD estate — both surfaces, every date-bearing endpoint. **Exactly
> ONE surface can possibly deliver dated per-model allocation history, and it is DataMining's `qt5 allocations`
> template — which ALREADY selects the account→strategy assignment dimension and is date-windowed, so the decisive
> test needs no template change, just a past-window RUN.** Every other candidate is either measured-dead (the
> rebalancer ignores injected dates; its native dated surfaces are empty for Cottonwood) or unprobed-and-lower-odds
> (Surface-B account/audit/timeline). **The whole question therefore reduces to one probe with an unfalsifiable
> intrinsic control.** And whatever it returns, **nothing reaches before ~2026-05-28: the Opal models did not exist,
> so there is nothing to allocate to.**
>
> **EXECUTION GATE — CORRECTED 2026-07-22 ~23:0xZ (0.6.2 230359Z, production evidence).** My first draft said "blocked
> by a 16-day-stale session." **That was wrong for the DataMining path this probe uses.** The 401s I generalized from
> (Addenda 2/3) were the **Rebalancer product API** — a *different* auth surface. The DataMining path mints a working
> bearer off the current jar **right now**: holdings/transactions/realized silver landed **this morning** (07-22
> 02:03–02:04Z) off it. So the probe is **NOT auth-blocked, and no manual Andrew capture is needed.** The real gate is
> narrower and qt5-specific — see §7.

---

## 1. What "a backfill mechanism" must produce — the bar every candidate is graded against

For each past date `D` (D ≥ ~05-28), fabrication-free `model_aua[m,D]` and `account_count[m,D]` need **three vintages
each dated to D** (established in the enriched brief):

| Vintage | We have it dated? |
|---|---|
| **(c) VALUE** — per-account holdings MV | **YES** — cot silver holdings back to ~06-08 |
| **(a) ASSIGNMENT** — which strategy each account was on **on D** | **NO** (live-state roster, no date field) — this campaign hunts it |
| **(b) BLEND** — strategy→model weights **as of D** | **NO for history** — same hunt, composition axis |

**A mechanism is only as deep as it can date (a) and (b).** (c) is not the constraint. This campaign is the search
for a dated (a)/(b) source across every BD surface.

---

## 2. THE FULL SURFACE SWEEP — every BD endpoint that could carry dated assignment, graded

### Surface A — DataMining (the date-*windowed* query API; the live hope)

| # | Candidate | Dated? | Carries assignment? | Grade | Verdict |
|---|---|---|---|---|---|
| **A1** | **`qt5 allocations` (tid 226334) past-window run** | **YES** — `dateRangeType:Custom`, start/end | **YES — `accountRebalStrategyID`+`accountRebalStrategyName` ALREADY `isSelected:true`** (+ MV + account) | **[GROUNDED / HELD]** | **THE decisive probe. No re-persist. §3.** |
| A2 | `qt1 holdings` past-window | YES (windowed) | **UNKNOWN** — dims server-side, never dumped (0.6.2 dumps tonight) | [HELD] | If qt1 carries an assignment dim it is the *cleanest* source (native daily snapshot). Await 0.6.2's dump. |
| A3 | `qt2 transactions` (tid 226274) | YES — real dated events back to ~03-09 | Portfolio-level only (`portfolioRebalStrategyID/Name`); **no account-level**; also carries a **`backdatedDate`** restatement field | [GROUNDED] | **Guard, not source** — dates *when* composition changed (bounds trustworthy windows); cannot *name* the strategy (basket overlap). §4. |
| A4 | `v1/run` `asOfDate` parameter | YES (server-evaluated) | inherits the table's dims | [HELD] | Same temporal question at the run level — folded into A1's probe (the run body already carries the date). |
| A5 | `qt3/qt4 realized/unrealized` | YES (windowed) | account-rebal dims **available, unselected** (enriched brief §1) | [GROUNDED] | Lot-grained, not allocation-count; would need a re-persist. Lower value than A1, which is already selected. |

### Surface B — the product APIs (RCN-0001 capture; date-*bearing* fields observed)

| # | Candidate | What the capture proves | Grade | Verdict |
|---|---|---|---|---|
| B1 | **Account entity** `rebalancerAssignment` + `asOfDate` + `dataAsOfDate` + `performanceStartDate` | The account record **carries an assignment field and multiple as-of dates** — body retained current only | [UNPROBED] | Probe: `GET account/{id}` with `asOfDate` variants — does `rebalancerAssignment` move? **Second-highest odds after A1.** |
| B2 | `datamanagement/.../transactionbackdates/dataformat` + `reconstatus/summary` + `dashboard/audit/*` | BD **tracks restatements + backdates as first-class** (the `backdatedDate` field in A3 is its data-plane) | [UNPROBED] | If assignment changes are audited, the audit log IS a dated change-set. Restatement tracking, not assignment-specific — medium odds. |
| B3 | `includeHistoricalBenchmarkAssignments=true` (proven param on **benchmark** endpoints) | BD treats **historical assignment as a queryable concept** — proven for benchmarks | [UNPROBED] | Probe for a **model/strategy sibling** (`includeHistorical*` on `api/models/strategies/*`). Concept exists; a model twin is the hope. |
| B4 | `rebalancer` `api/sessions/*` + `trademanagement/blotter/search` | Natively dated (session = timestamped event; blotter = timeframe filter) | **[RULED OUT — MEASURED]** | **EMPTY for Cottonwood over a 19-month window** (Addendum 3, live). Coverage gap = migration, not shape. Dead for cot. |
| B5 | `relationship.reportingDates{historyStartDate,startDate,asOfDate}` | As-of semantics at relationship level | [UNPROBED] | Governs *reporting window*, not model assignment. Low odds it carries per-account strategy history. |
| B6 | `timeline` service (`api/v1/posts`, `tags`) | Inherently temporal client feed | [UNPROBED] | It is portal posts/tags, **not** model assignment. Lowest odds; swept for completeness, not expected to carry it. |
| B7 | `portfolioreporting/performanceSeries` | Daily arrays behind the chart | [UNPROBED] | Return series, not allocation-*count*; could carry per-class MV over time but not the *count* per model. Tangential. |

**Coverage statement (the denominator):** 2 DataMining surfaces × 5 query types + ~15 Surface-B services enumerated;
**every date-bearing endpoint in the RCN-0001 corpus is accounted for in the table above** — none silently dropped.
The two surfaces the campaign leans on (A1 live, B1/B2/B3 unprobed) are the only ones where a dated assignment could
survive; the rest are graded and set aside with the reason stated.

---

## 3. THE DECISIVE PROBE — A1, sharpened, with a WINDOW-INTEGRITY CONTROL (CTO v1.21, binding)

**The single question that gates the whole backfill design:** does `qt5 allocations`, run for a **past window**,
return the account→strategy assignment **that was in force then** (TEMPORAL → backfill is real) or **today's stamped
onto the past window** (CURRENT → the surface is closed)?

**Why it is the cheapest possible test:** the account-strategy dimension is **already selected in the production
template** (verified in `templates/allocations.json`: `accountRebalStrategyID` id 35392 + `accountRebalStrategyName`
id 35393, both `isSelected:true`, `isEnabled:true`). **No template re-persist. No mutation. A pure past-window RUN of
the template we already run daily.**

### The verdict logic — window-integrity FIRST (this is the CTO v1.21 requirement, not optional)

> **THE FAILURE MODE THAT MATTERS is window-IGNORING — the eclipse `--date`-is-a-filename class.** A query that
> silently returns CURRENT state for a past window yields a **false-CURRENT verdict that kills the backfill capability
> while looking like an honest negative.** 0.6.2 proved exactly this on eclipse today (8 date params → byte-identical
> sha256). My intrinsic control must catch in-run what a second instrument would otherwise catch.

**The model-creation timeline IS the window-integrity instrument** (from RCN-0001 Addendum A2, `rebalancer_model_detail`
`createdAt`): on a true **2026-06-15** window, Satellite 60 (created 06-23) and 30/40/70/98 (created 07-06) **cannot
exist**, and the roster is ~136–215 accounts, not today's 296. So:

```
RUN qt5 for window W_past = 2026-06-15 (+ a deeper W = 2026-05-15, pre-most-models)
  and W_recent = today, same template, only the dates differ.

STEP 0 — WINDOW-INTEGRITY GATE (must pass before any temporal/current verdict is legal):
  Does W_past return a roster STRICTLY REDUCED per the creation timeline
  (no Satellite 60; no 30/40/70/98; account count < today's 296; April window => "No Strategy" sentinels)?
    NO  (W_past returns today's full 296 + all strategies) -> WINDOW WAS IGNORED.
         => the surface is the eclipse class. Verdict = CURRENT-only, backfill CLOSED on A1. VALID because
            the same run PROVED the query reached (and was ignored by) the past window.
    YES (W_past returns the reduced, era-correct roster) -> WINDOW WAS HONORED. Proceed to Step 1.
    ZERO ROWS (W_past returns a 0-row shell) -> INSTRUMENT-BROKEN, NOT window-honored-empty. This is the
         07-09 qt5 allocations feed failure (0.6.2 230359Z: post-06-26 qt5 delivers 0-row shells with the
         full 56-col header). A genuine pre-model window still has 54-215 NON-Opal accounts; only a broken
         feed returns zero rows. HELD on the qt5 feed, never a CURRENT verdict.
    INCONCLUSIVE (cannot demonstrate honored either way) -> UNVERIFIABLE-INSTRUMENT, NOT a finding.
         => the pre-authorized self-evaluable escape (below).

STEP 1 — TEMPORAL DISCRIMINATION (only legal once Step 0 = HONORED):
  For the 15 churn-control accounts (0.6.2's set: Opal today, ABSENT from the 06-09 book):
    W_past returns them absent/unassigned  -> TEMPORAL. Backfill is real to the coverage horizon. Apply the B2
                                              model-weight rollup -> dated model_aua + account_count. GO LOUD to COO/CTO.
    W_past returns them carrying today's Opal strategy -> CURRENT-stamped at the dimension. Backfill CLOSED.
```

**Binding (COO 224310Z):** *a CURRENT-only verdict is VALID only if the same run demonstrates the window was honored.*
A CURRENT-only claim without Step-0=HONORED is `UNVERIFIABLE-INSTRUMENT`, reported as such, never as "the surface is
current-only." **Both controls are intrinsic and cannot false-positive:** the timeline control cannot be faked (BD
would have to invent pre-creation history); the churn control fails in both directions.

### The escape — PRE-AUTHORIZED + SELF-EVALUABLE (CTO finalized 224317Z; no round-trip)

> **CORRECTION 2026-07-22 ~23:0xZ (COO 225959Z):** an earlier draft of this section had the escape "routed back
> through COO to CTO." That is stale — CTO **finalized** it at 224317Z, *after* the relay this brief was first
> written against, as **pre-authorized and self-evaluable.** The corrected mechanics:

`0.6.2` evaluates a **machine condition himself** at the 02:00Z session window and runs his single re-persist
confirmation **IFF, by then, this campaign has NOT produced EITHER (a) a TEMPORAL verdict OR (b) a CURRENT-only
verdict with the window-integrity limb GREEN.** No COO→CTO round-trip; no explicit per-run GO.

- If this campaign lands a **sufficient verdict before 02:00Z** (TEMPORAL, or CURRENT-only with window-integrity
  green), 0.6.2 stays **retired** — he does not touch the surface.
- If this campaign is **still HELD / insufficient at 02:00Z**, 0.6.2 self-evaluates the condition and **may run
  in-session.** **The timeliness and strength of my window-integrity limb directly gate whether he touches BD at all.**
- If both are live in that window, **coordinate by timestamp — sequential, NEVER concurrent** (a second concurrent
  IP-bound DataMining session is the 401-manufacture risk v1.21 retired his probe to avoid).
- **Never off-window, never by default, never a concurrent session.**

---

## 4. A3 as a dated GUARD (not a source) — the one honest secondary use

`qt2 transactions` is dated back to ~03-09 and carries a `backdatedDate` restatement field. It **cannot name** a
strategy (the same basket cosine 0.62–0.98 that bans fingerprinting). But a rebalance produces a datable **cluster**
of trades → it dates *when* an account's composition changed, bounding the windows in which a carried-forward
assignment is trustworthy. **Sharp limit (CTO's symmetry): detected rotation → never carry across (sound); no rotation
detected → nothing licensed** (absence-of-signal cannot affirm stability where baskets overlap most). Use only as a
guard on A1's output, and to *manufacture* the churn positive control as the forward series accrues — never as the
assignment source.

---

## 5. RULED OUT — measured, not asserted

- **Holdings-basket fingerprinting** — strategy baskets cosine **0.62–0.98, mostly >0.90** (measured). Inference-from-
  similarity = the fabrication class. **Never propose.** (COO flagged this is exactly the temptation "identify a
  mechanism" invites; the run-level discriminator sidesteps it.)
- **Rebalancer date-injection** — **live-tested (Addendum 3):** 10 date shapes on `accounts/search`, 2 on `models/{id}`
  — **all ignored, positive control fired.** No hidden date parameter.
- **Rebalancer native-dated surfaces (sessions/blotter)** — **live-tested: EMPTY for Cottonwood over 19 months.**
- **Back-mapping today's assignment** — churn-wrong (models created 05-28→07-17; a quarter of the book on one day).

---

## 6. THE STRUCTURAL CEILING — restated because it bounds every branch

**No mechanism, live or not, reaches before ~2026-05-28.** The Opal models were *created* 05-28→07-17
(`rebalancer_model_detail.createdAt`, measured); only ~54/296 accounts (18%) are even allocatable before June. Backfill
best-case is Cottonwood joining the MDPF series from ~05-28 (a partial subset) growing to full ~07-06 — **a ~7-week
window against a 21-month chart, not the series start.** The honest deliverable is a short, self-extending, correctly-
labelled series; per the migration reframing (Andrew: *"do not get too indebted to what they have or don't have yet"*),
forward-only is already a correct answer, and A1-if-temporal only *widens* it, never completes it.

---

## 7. THE EXECUTION GATE — CORRECTED: it is qt5-specific, NOT session auth

**My first draft called this "held on a 16-day-stale session." 0.6.2's production evidence (230359Z) corrected it, and
the round-trip is why:** I over-generalized the Addendum-2/3 401s — those were the **Rebalancer product API**
(`/api/accounts/search`), a *different* auth surface with a short TTL. **My harness uses the DataMining path**
(`/datamining/auth/token` → qt5 run → export), and that path mints a working bearer off the **current** jar right now:
holdings/transactions/realized silver landed **this morning 07-22 02:03–02:04Z** off it (comp-freshness, 0.6.2). So:

- **Auth is NOT the gate, and no manual Andrew capture is needed.** The DataMining jar is functional. (My §9 note that
  the SM secret's `LastChanged`/`captured_at` reads 07-06 and session-fetch logs stop ~06-26 is a real WS-1
  feed-liveness question — but it does not block DataMining bearer minting, which is what this probe needs. 0.6.2/CTO's
  lane, not mine.)
- **The REAL gate is qt5-specific.** `qt5 allocations` silver has been **frozen since 2026-07-09** — the feed delivers
  **0-row shells** (full 56-col header, no rows) while the other qt tables land daily (0.6.2). **A past-window
  *explicit* run is a different call than the daily incremental and MAY clear it** — that is the unknown the probe
  itself tests. The hardened harness (§8) makes a 0-row result an explicit **`INSTRUMENT-BROKEN`**, never a
  window-honored-empty, so the qt5 failure cannot masquerade as a temporal finding.

**Execution (per the CTO/COO amendment, 225852Z):** on-box in the 02:00Z window, coordinated with 0.6.2, **sequential
never concurrent.** Two ways it fires, same harness: (i) as my **primary campaign** if run in that window; (ii) as the
**escape instrument** — if the pre-auth condition holds at 02:00Z, 0.6.2 runs *this harness* on the nightly session
(it strictly dominates his original re-persist, which stays fallback only).

**Possible clean outcomes, all honest, none a failure:** `TEMPORAL` (backfill real to ~05-28) · `CURRENT-only`
(window honored, backfill closed) · `INSTRUMENT-BROKEN` (qt5 0-row shell — the temporal question stays HELD on the
07-09 feed, a 0.6.2-lane fix, not a CRO finding) · `UNVERIFIABLE-INSTRUMENT` (window integrity undemonstrable → the
escape). The design, controls, and harness are complete; nothing waits on a manual capture.

---

## 8. Harness — ready to fire (`scripts/cot_qt5_temporal_probe.py`)

Self-contained, read-only: loads the SM session, mints the DataMining Bearer, runs `qt5 allocations` for
{2026-05-15, 2026-06-15, today}, downloads each xlsx, and **evaluates Step-0 window-integrity FIRST** (era-correct
roster per the model-creation timeline) then Step-1 temporal discrimination on the 15 churn accounts. Prints an
explicit `VERDICT=TEMPORAL | CURRENT-only(window-honored) | INSTRUMENT-BROKEN | UNVERIFIABLE-INSTRUMENT` line.
**Two binding guards** so a broken instrument never manufactures a verdict: (1) a token-mint / read HTTPError exits
`HELD` with no verdict; (2) a **today-baseline explicit-window run** must return the live 296 before any past window is
interpreted — a 0-row today means the 07-09 qt5 shell failure reaches my call pattern too, so the run exits
`INSTRUMENT-BROKEN`; and any past-window 0-row is classified `INSTRUMENT-BROKEN`, never window-honored-empty.

---

## 9. Grounding

**[GROUNDED]** qt5 template selects `accountRebalStrategyID/Name` (id 35392/35393, `isSelected:true`) +
`dateRangeType:Custom` (`data/cot/scripts/bronze/templates/allocations.json`, read this session) · qt2 carries
`portfolioRebalStrategyID/Name` + `backdatedDate`, no account-level (`transactions.json`, read) · gold
`dim_model_portfolio` computes the daily count+value (parquet read) · SM `blackdiamond/cot/session`
`captured_at=2026-07-06`, `LastChanged`≈07-06, session-fetch logs stop ~06-26 (SM + S3, read) — a WS-1 flag, NOT a
DataMining blocker · DataMining path works off the current jar: cot silver holdings/transactions/realized landed 07-22
02:03–02:04Z (0.6.2, comp-freshness) · qt5 allocations frozen since 07-09, 0-row shells (0.6.2) · model-creation
timeline + churn-control accounts (RCN-0001 Addendum A2; 0.6.2 B6 probe-prep, 15 accounts).
**[MEASURED]** rebalancer date-injection ignored + sessions/blotter empty (Addendum 3, live) · basket cosine 0.62–0.98.
**[UNPROBED]** B1/B2/B3/B5/B6/B7 Surface-B endpoints — enumerated, graded, not yet called. **[HELD]** A1/A2/A4 on the
qt5 window run (auth is live; the gate is the 07-09 qt5 feed, §7).

**One-line:** the entire BD estate offers exactly one live path to dated per-model allocation history — a past-window
run of the qt5 template we already own, whose auth is live NOW (DataMining path) — gated only on whether an explicit
past-window run clears the 07-09 qt5-shell failure; everything else is measured-dead or lower-odds-unprobed, and
nothing reaches before the ~05-28 model-creation floor.

---

# ADDENDUM — 2026-07-23 ~02:12Z: the probe RAN (02:00Z window). Verdict = HELD-ON-FEED (qt5 run-level 500), NOT a temporal finding.

**Execution:** my harness `cot_qt5_temporal_probe.py` ran once, on-box, python3.11, via 0.6.2's SSM
(cmd `a051ffc7-...`), ~02:11–02:12Z, sequential after 0.6.2's B5 dump, zero concurrent vendor calls. **Verbatim:**
```
=== cot qt5 temporal probe (read-only) ===
session captured_at=2026-07-06T02:02:47.724Z
token minted OK
HELD: baseline read HTTP 500 -- session not usable for DataMining, no verdict.
```

## The verdict, and why it is the CORRECT (not a disappointing) outcome

**VERDICT = HELD-ON-FEED. The temporal-vs-current question stays OPEN — it is NOT `CURRENT-only`, NOT
`backfill-closed`, NOT a temporal finding.** The harness's baseline gate fired exactly as designed: it refused to
emit any verdict because the instrument could not be shown to work. **A probe that returns "no verdict, and here is
why" beats one that returns a confident wrong answer** — the whole point of the window-integrity/baseline gate.

## Error-class discrimination (0.6.2 230942/021223Z — his window was pre-tasked to capture exactly this) **[SOURCE-CONFIRMED]**

The 500 is **table-specific and run-level**, not session/auth/call-pattern:
- **NOT auth** — the bearer minted (harness line 2); 0.6.2's `GET /template/{id}` succeeded ×4 minutes earlier off
  the same jar.
- **NOT the 0-row shell** my `INSTRUMENT-BROKEN` branch anticipated — the run died *earlier*, on a server-side 500 on
  the qt5 **run call itself** (before any rows).
- **qt1/qt2/qt3 RUNS SUCCEEDED tonight** (holdings/transactions/realized silver landed 02:03–04Z, same jar, same
  `v1/run` path). **So `v1/run` works per se; it 500s for qt5 specifically** (qt4 same family — both frozen 07-09).

**Conclusion (SOURCE-CONFIRMED): the 07-09 qt4/qt5 freeze is a TABLE-SPECIFIC RUN-LEVEL server failure** — not
session, not auth, not our call pattern. It lands in **0.6.2's WS-1 qt5 lane** as a feed defect to repair; the
temporal question re-opens the moment qt5 runs again. **My harness needs zero changes — it did its job one call deep.**

## The qt5-500 mechanism — hypothesis SHARPENED offline (my surface), 0.6.2's "newer-templateId" read partially FALSIFIED **[GROUNDED]**

I characterized the failing (qt4/qt5) vs working (qt1/qt2/qt3) templates from the persisted JSONs + git history:

| qt | table | templateId | last local change | ran tonight? |
|---|---|---|---|---|
| 1 | holdings | 226355 | 2026-06-22 (CurrentDay→Custom) | **OK** |
| 2 | transactions | 226274 | 2026-06-09 | **OK** |
| 3 | realized | *unprovisioned* (create-on-run) | 2026-06-12 | **OK** |
| 4 | unrealized | **237784** | **2026-06-30** (new id wired, "verify next") | **500 (frozen 07-09)** |
| 5 | allocations | **226334** | 2026-06-22 (CurrentDay→Custom, same edit qt1 got) | **500 (frozen 07-09)** |

- **0.6.2's "newer templateId 237784" hypothesis fits qt4 but does NOT extend to qt5** — qt5's `226334` is the *old*
  id-range (adjacent to working qt2's `226274`), and its last edit (06-22) is the *same* CurrentDay→Custom change qt1
  received and **survived.** So our template edits do not explain the qt5 500.
- **The 07-09 freeze ONSET aligns with NO local template change** (last touches: qt5 06-22, qt4 06-30) → this
  **strengthens the vendor-side-change (~07-08/09) axis** over the our-edit axis for the run-level 500.
- **Likely two distinct failure modes under one symptom:** qt4 = a possibly-unverified 06-30 template re-persist
  (`237784`, "verify next" that may never have completed); qt5 = a vendor-side run failure unrelated to our template.
- **Definitively discriminating them needs a vendor-side template-level probe** (modify the qt5 template, re-run,
  see if the 500 clears) — my campaign's surface, a **future vendor window**, not tonight. Recorded as the next
  actionable step for the qt5 half.
  > **GATE ON THAT FUTURE PROBE (CTO 021639Z):** the standing campaign egress covers *reads*, but this probe's
  > **template-MODIFICATION step gets its own look** — route the specific probe plan through CTO for the gate before
  > touching a production template. Do NOT fire it under the standing egress word alone. Co-design with 0.6.2 (agreed
  > 021634Z); repair-lane order (CTO): WS-1 cookie fix first at daylight, qt5 feed repair immediately behind, this
  > addendum as the diagnostic seed.

## Two other window results folded in

- **A2 CLOSED [GROUNDED]:** 0.6.2's first-ever `dump_enriched_templates.py` run landed qt1's dims — **15 dims / 4
  levels, and NO strategy/assignment dimension anywhere in qt1.** So the daily holdings snapshot cannot supply
  assignment; **qt5 is confirmed the ONLY date-windowed surface carrying account→strategy.** (qt3's 13 account-level
  dims are *selectable-but-unpersisted* — the template has no persisted id; A5 downgraded accordingly.)
- **WS-1 fires-without-writing CONFIRMED [MEASURED]:** SM `blackdiamond/cot/session` `LastChangedDate` held at
  ~07-06 across three reads tonight (02:02:07 / 02:02:54 / 02:08:36Z) while auth minted fine — **the nightly capture
  chain fires without rewriting the jar; a dead producer masked by surviving durable cookies.** My §9 grounding and
  0.6.2's observation now reconcile exactly. His WS-1 lane owns the repair.

## Net for Andrew's question

**A backfill mechanism EXISTS (qt5 past-window, one surface) — and tonight's run neither confirmed nor closed it.**
It is held on a **qt5-specific server-side run failure** (the 07-09 freeze), which is a *feed-repair* item, not a
*"no mechanism"* answer. The temporal-vs-current verdict re-opens the instant qt5 runs again — no manual capture, no
design change, just the qt5 feed repair (0.6.2/CTO) plus, if the vendor side is implicated, the template-level probe
on a future window (my surface). **Nothing reaches before ~05-28 regardless.**

---

# ADDENDUM 2 — 2026-07-23 ~04:2xZ: the probe COMPLETED (Andrew-egress vendor window). FINAL VERDICT = CURRENT-STAMPED, NOT temporal. Two mechanism corrections supersede Addendum 1.

**Andrew opened the vendor gate ("whoever needs egress ability has it / get it done now"). 0.6.2 ran a read-only R0–R3
pairing pass (his mechanics, my adjudication); I ruled on his retained raw exports + today's roster. Addendum 1's
HELD-ON-FEED read is superseded on three counts.**

## Correction 1 — my harness's 02:12Z HTTP 500 was a SELF-INFLICTED bug, not a vendor run failure **[SOURCE-CONFIRMED]**
`v1/run` requires a **wrapped** body `{"template": full, "asOfDate": endDate}` + normalization
(`cot_bronze_ingest.py:405-415`, comment *"omitting asOfDate 500s — this was the root cause"*). My `run_window` posted a
bare `dict(template)` — that alone 500s regardless of session/dates. So Addendum 1's *"table-specific server-side run
failure"* attribution was **wrong** — it was my instrument, caught by 0.6.2 reading the production source, not by my
care. Harness fixed to reuse `bi.run_query` (@7f2291783).

## Correction 2 — the qt5/qt4 freeze is DATA-AVAILABILITY (late materialization), not a run failure **[SOURCE-CONFIRMED]**
Daily qt5 runs **execute clean** and BD returns 0-data-row header-only exports — *"BD has no point-in-time snapshot for
this as-of date"* — because same-day snapshots aren't ready at the 02:00Z run and **materialize later**. Proven by the
bracket: 07-08/10/14, rejected 0-rows at their daily run, **return full exports now**. The frozen span 07-09..07-22 is
**recoverable today**; the daily chain's defect is our-side (asks once, never retries) — a catch-up sweep, 0.6.2's WS-1
lane. **No vendor conversation required.**

## THE VERDICT — CURRENT-STAMPED assignment, grounded THREE independent ways **[the careful negative]**
The fabric leaned TEMPORAL for ~an hour on genuinely suggestive evidence (differential windows 83→780→857→859→867→862;
churn controls 0/8→2/8→8/8 in migration order). **That evidence is real — but it proves temporal EXISTENCE + VALUE, not
temporal ASSIGNMENT.** The direct tests the parsimony read lacked:
1. **Direct assignment comparison:** across 778+ accounts present in a past window and matched to today's roster,
   **ZERO real Opal assignment changes** (the only 5 are `Moderate Income → DAF Income`, a non-Opal reclass). Every
   account carries its **exact today assignment** in every past window — current-stamped by definition.
2. **`createdAt` stability (falsifies the "re-save-stamp" rebuttal):** `createdAt` is **stable 22/22** across the 07-21
   and 07-22 partitions (a real birth date), while `updatedAt` moved for the 5 terminal models (the nightly
   revaluation — the field 0.6.2's B6 measured, generalized one field too far). So Sat-60 (06-23) and Sat-70/98 (07-06)
   genuinely did not exist at 05-15, yet appear in the 05-15 window = the current-stamp artifact.
3. **The window-integrity control's IGNORED flag was CORRECT**, not a misfire.

**A lesser process ships the exciting wrong answer tonight and a fabricated assignment history this week.** The
window-integrity control + independent verification + the direct test are exactly why it didn't.

## Consequences
- **qt5 is NOT an assignment-backfill source.** The interpolated 3F-BF1 build's **assignment leg STANDS as the only
  path**; there is nothing from qt5 to supersede it with (the earlier "upside path" framing is retired by evidence).
- **qt5 IS a real dated VALUE + existence source** back to ~05-15 — an **approved BF1 value-leg refinement** (extends
  the interpolator's floor below silver-holdings' 06-08); assignment stays interpolated. Spec detail to DS when the
  recovery sweep lands.
- **The recovery sweep** (07-09..07-22, CTO-GO'd, 0.6.2) recovers real **value** for the recent frozen daily dates with
  provenance **value-real / assignment-current-stamped / never-PIT-recovered** — it must never be read as PIT assignment.
- **Silver dropped `createdAt` (Rule-17 flag):** neither `fact_model_definition` nor `fact_model_roster` carries the
  creation date (roster's `last_update` is the revaluation timestamp, not creation) — per-model `createdAt` lives only
  in bronze `rebalancer_model_detail`. Routed to CTO for a silver passthrough on next touch; BF1 reads bronze meanwhile.

**Net for Andrew's question, FINAL:** there is **no historical model-assignment to recover** — qt5's assignment is
current-stamped, every other surface is measured-dead or lower-odds, and nothing reaches before ~05-28. **The honest
answer is the interpolated backfill: real dated VALUE, honestly-labelled interpolated ASSIGNMENT — which is exactly
what the yellow-dashed band exists to say.**
