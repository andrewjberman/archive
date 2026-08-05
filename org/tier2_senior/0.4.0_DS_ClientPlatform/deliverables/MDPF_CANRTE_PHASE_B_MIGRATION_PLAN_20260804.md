# MDPF_CANRTE Phase B — Migration Plan (DESIGN)

**Status:** PHASE-B DELIVERABLE v1.0 — submitted for CTO+COO plan acceptance (the Phase-C gate).
**Author:** 0.4.0_DS_ClientPlatform (same seat per the scope phase table; DT/AE read-only consults).
**Governing inputs:** TIGHT SCOPE v0.1 @86f52bdfb · Phase-A design @ab2d2f167 (citations @e0d657799)
· **CTO FORK RULINGS** `org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_CANRTE_FORK_RULINGS_20260804.md`
(F-1 = shape-uniform/source-parameterized, C-1 preserved-by-binding, ETFS boundary ratified;
F-2 = uniformity binds at the spine, L1 = declared vendor-necessity rows only; F-3 = MODEL-B,
C-2 rider BINDING pre-Phase-C; §2.1 contract canonized; §2.2 grammar ratified) · COO Phase-B
open 164231Z.
**Walls unchanged:** design-only at this phase — zero code, zero serve contact, zero `data/`
commits. Phase-C seating happens only on CTO+COO acceptance of THIS plan + Andrew's word on any
serve-touching step. Downstream tail untouched throughout.

---

## 0. Shape of the plan

Five waves. Each wave states: WHAT LANDS · PARITY GATE · ROLLBACK · SERVE EXPOSURE. The
invariant across all of them: **nothing serve-facing moves before Phase C, every wave is
reversible by a single revert, and nothing is deleted until the terminal step of the last
wave.** Build-alongside → parity → swap is the only cutover idiom used (it is the idiom the
revamp itself proved).

The DELTA=0 parity class used everywhere (§5) is defined once and exercised with a mutant
control before first use.

---

## 1. W-0 — Preconditions (already authorized elsewhere; sequenced here, not re-opened)

- **C-2 instrument fix** (comp-pipescript: assets-tree addressability, trio/legacy-agg
  visibility, write-attribution) — BINDING before Phase-C cutover per F-3. Owner: graph stream,
  routed through CTO (partition-legal). This plan's W-4/W-5 explicitly WAIT on it (§4, §5).
- The two authorized post-Leg-4 one-hunks at my seat (WS-C roll-forward resolver; global
  meta-provenance extension — the latter folds into W-3 so the derived contract is uniform).
- No other precondition. W-1/W-2 do not wait on W-0.

## 2. W-1 — Binding config lands (pure-add, zero behavior)

- **WHAT LANDS:** `data/mdpf/config/route_bindings.yaml` — the Phase-A §3 table as declared
  config: per-firm model/custody/non-model source rows (49f custody = the Andrew-canonical DDB
  cohort VERBATIM per F-1/C-1), **L1 row present ONLY with its vendor-grain reason** (F-2:
  cottonwood: value_date re-key + blend explosion + relationship-grain collapse; 49f/inflection:
  ABSENT — the reference shape), model-key sets, launch seams/depths, carry windows
  (roster-derived, unchanged), and the CARRY-IMPORT declaration (§6). A sibling of
  `partner_roster.json`, same one-committed-authority/two-locations pattern
  ([dim:1718-1746] @e0d657799) — deliberately NOT a roster extension, so gate-policy semantics
  stay untouched.
- **PARITY GATE:** a read-only tie-out validator asserting every binding row == the constant it
  replaces, cited to the live module constants ([dim:66-131], slice/pair constants). Run once at
  land; re-run in W-2's harness. (Pure-add needs no behavioral parity.)
- **ROLLBACK:** delete the file — nothing consumes it yet.
- **SERVE EXPOSURE:** zero.

## 3. W-2 — Model-B spine builder ~~build-alongside (staging writes only)~~

> **⚠ HISTORICAL — DO NOT EXECUTE THIS SECTION AS WRITTEN. W-2 IS DONE, AND IT WAS NOT DONE THIS
> WAY.** The shadow prefix below was **deleted pre-first-emission** and the comparator
> **deleted + deprecated** under Andrew's 2026-08-04 complete veto; the port then ran as W2R
> (build-correctness + ad-hoc QA + direct swap, incumbents deleted same-window), and the
> 3-consecutive-green gate was collapsed as a shadow-era artifact.
> **The text is preserved unedited as the record of what was PLANNED** — the veto landed mid-wave
> and that sequence is part of the history. **It is not an instruction and nothing should be
> derived from it.** For the method that actually applies to any remaining wave, see §4's
> METHOD bullet.

- **WHAT LANDS:** ONE firm-parameterized spine builder (F-3) consuming W-1 bindings, emitting
  the canonized §2.1 contract per firm + the existing global fold mechanism. It writes to a
  SHADOW staging prefix (`gold/mdpf_canrte_shadow/{firm}/aggregate_aua_timeseries.json`) on the
  same schedule, alongside the incumbent producers — the revamp's own build-alongside idiom.
- **PARITY GATE (DELTA=0, §5):** shadow vs incumbent staged artifact, per firm + global, on
  **3 consecutive green scheduled cycles** (observed-green-run doctrine — never accepted on the
  authoring run). Only then: the dispatch re-points its stage steps (6a/6d step (3)) to the
  consolidated builder writing the CANONICAL staging keys — one dispatch-script change.
- **ROLLBACK:** revert the dispatch step; incumbent builders remain deployed and runnable until
  W-4 retires their homes (never deleted before that).
- **SERVE EXPOSURE:** zero — staging keys only; accrual/publisher continue reading unchanged
  content (that is what the parity gate proves).
- Note: the cottonwood L1 dim + its vocabulary/composition gates are UNTOUCHED (declared
  vendor-necessity per F-2; today's Moderate-Income arc is live proof those gates are
  load-bearing).

## 4. W-3 — Derived producers parameterized — **AMENDED 2026-08-05, TWICE. READ THE BOX FIRST.**

> ### ⛔ AMENDMENT A — THIS SECTION PRESCRIBED A VETOED MECHANISM FOR ~30 HOURS
>
> **It said, verbatim: *"Same shadow → 3-green → swap idiom as W-2."* BOTH HALVES ARE DEAD.**
>
> - **SHADOW — Andrew-direct COMPLETE VETO, 2026-08-04:** *"We do not do all these extra paths,
>   these things never ever get decommissioned and they become debt and fuck us up forever… we
>   simply do something correctly the first time and port over, not making a million backdoor
>   shadow channels… The comparator is also a HORRIBLE idea."* W-2's shadow prefix was deleted
>   pre-first-emission and its comparator deleted + deprecated.
> - **3-GREEN — collapsed** by Andrew's W2R word as *a shadow-era artifact* (COO, relayed).
>
> **I WROTE THIS PLAN ON 08-04, THE SAME DAY THE VETO LANDED, AND IT SAT AS THE SEATING DOCUMENT
> FOR AN UNSTARTED WAVE.** Executing my own plan would have built a shadow channel under a
> standing veto **while citing an approved design document.** The next reader's diligence —
> following the plan — is what would have produced the violation.
>
> **A STALE PLAN IS WORSE THAN A STALE FACT, BECAUSE A PLAN IS AN INSTRUCTION.** A stale fact gets
> checked when someone relies on it; a stale plan gets EXECUTED, and the more approved the
> document, the more faithfully. Amended rather than quietly deviated from — a deviation leaves
> the bad instruction in place for the next reader.
> *(COO confirmed the method 2026-08-05T1955Z and directed this amendment as its own commit ahead
> of any W-3 code. Doctrine candidate they are carrying to CTO: **when a ruling lands, the sweep is
> not only over records of FACT — it is over PRESCRIPTIVE documents, which are the ones that will
> be acted on.**)*

> ### ⚠ AMENDMENT B — THE SCOPE WAS THREE LEGS AND IT IS FOUR
>
> This section named *"metrics, distribution, and the cottonwood pair"*. The program label in the
> registry is **"derived-producer consolidation (6b/6c/6e)"** — three letters that map neatly onto
> those three components. **That neatness is a coincidence, and acting on it would have built the
> wrong scope.**
>
> `6a`–`6e` are **dispatch stage-6 steps**, ground-truthed in
> `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh` (@HEAD, `:521`–`:615`):
>
> | step | what it runs | status |
> |---|---|---|
> | **6a** | THE COLLECTIVE SPINE (`build_mdpf_spine.py`) | DONE — W-2/W2R swap |
> | **6b** | `account_distribution` per firm | **W-3** |
> | **6c** | `non_model` (`dim_mdpf_non_model_assets`) — MUST follow 6a | **W-3** |
> | **6d** | COTTONWOOD legs (dim + pair + slice + global re-stage) | **W-3** |
> | **6e** | `aum_metrics` — runs LAST, sees 6d's output | **W-3** |
>
> **The three-letter label SILENTLY DROPPED 6d (cottonwood), and my own prose had named the
> cottonwood PAIR while OMITTING 6c (non_model_assets) entirely.** Two errors that cancelled in
> count and not in content. **W-3 IS FOUR LEGS: 6b / 6c / 6d / 6e.**
> *(COO propagated the three-letter label from CTO without resolving it and said so; I declined to
> guess the mapping because the letters skip 6d. The dispatch is the authority, not the label.)*

- **WHAT LANDS:** binding parameterization for the FOUR derived-producer legs above —
  `dim_mdpf_account_distribution` (6b), `dim_mdpf_non_model_assets` (6c), the cottonwood legs
  (6d — dim + pair + slice + global re-stage; the pair already imports the dim machinery
  [pair:63-65], so the consolidation is half-done in the dependency direction), and
  `dim_mdpf_aum_metrics` (6e). Includes the global meta-provenance one-hunk so every derived
  artifact carries the uniform meta block (source_spine / as_of_basis / firm_id).
- **METHOD (REPLACES the shadow idiom) — Andrew's own, verbatim: DO IT CORRECTLY THE FIRST TIME
  AND PORT OVER.** Build-time correctness: tests, exercised tie-outs, and an **AD-HOC QA
  comparison run (run-and-read, nothing left standing)**. Then a **DIRECT port on the production
  schedule with same-window rollback.** No shadow prefix. No parallel emitter. No standing
  comparator. **Nothing that survives the port.**
- **PARITY GATE — AMENDED:** DELTA=0 per derived artifact per scope, plus the derived-vs-spine tie
  law (per-model tie to the cent), **read on an AD-HOC QA run before the port and asserted by the
  test, not by rc.** ⛔ The prior wording — *"asserted by the harness"* — implied a STANDING parity
  harness, which is the comparator shape in softer form and is vetoed. An ad-hoc run-and-read is
  sanctioned; a standing second instrument is not.
- **ROLLBACK:** dispatch-step revert, same window; incumbents stay deployed.
- **SERVE EXPOSURE:** zero (staging + the accrual's dated tree read the same content by parity).
- **⚠ SEQUENCING DEPENDENCY, open at Andrew (recorded, not resolved):** CTO's HEAD note on
  `MDPF_CANRTE.json` identifies a redundant promotion hop — the spine writes
  `gold/mdpf_revamp/` (underscore, undated) and 40 minutes later the same bytes are promoted to
  `portal/gold/mdpf/` (hyphen, date-partitioned). *"IF THE SPINE WROTE THE CANONICAL GRAMMAR
  DIRECTLY, THE PROMOTION HOP DISAPPEARS."* It is **carried to Andrew as part of the W-3 appetite
  question and NOT authorized as work.** Relevance here: **if he rules the hop away, W-3's
  meta-provenance one-hunk lands in a DIFFERENT output grammar than the one this plan builds to.**
  Do not start the meta-provenance leg without checking that ruling's state.

## 5. W-4 — Home migrations (the ratified grammar's one-builder-home rule)

- **WHAT LANDS:** `git mv` of the NON-serve-facing off-home builders into
  `data/mdpf/scripts/gold/` — slice + pair (assets tree), per-firm distribution (smartx tree) —
  with dispatch/SSM path re-points and deployed-prefix sync. Moves, not edits: content identical
  by construction.
- **SEQUENCING RULE:** W-4 does NOT start until the W-0 C-2 fix is landed — a home migration the
  drift instrument cannot see would recreate the exact blindness this program exists to close.
- **PARITY GATE:** `comp-pipescript deployed` MATCH on every moved script (post-C-2-fix, the
  instrument can now say so) + one green scheduled cycle + DELTA=0 on the wave's artifacts.
- **ROLLBACK:** revert the mv commit + re-point; prior deployed copies remain on their prefixes
  until the wave closes green.
- **SERVE EXPOSURE:** zero. **The serve-facing off-home writers — the platinum rollup writer
  (backfill home) and any legacy-key writer — are EXCLUDED from W-4 by design; they move only
  inside W-5's gates.**

## 6. W-5 — Phase-C serve cutover (every serve-touching step, gated)

**ENTRY GATES (all four, hard):** C-2 fix landed + W-2/W-3 parity green + CTO+COO acceptance of
this plan + **Andrew's word on the serve-touching steps** (scope phase table). Phase-C seating
is COO's then.

Ordered steps, each with its own freeze window + DELTA=0 + single-step rollback:

1. **Serve repoints** (DE/DT lanes): the legacy `json/portfolios/aum-metrics.json` read
   re-points to the canonical serve keys ([metrics:61-63] — "alive until DE re-points" becomes
   a dated step, not an open-ended residue); the per-firm `json/mdpf/*` LIVE bells stay
   as-served (their producer migrates home in step 2; the hyphenated account-distribution key
   remains LIVE — standing memory rule, re-affirmed).
2. **Serve-facing writer home moves:** the platinum-rollup writer leaves the `backfill/` home
   (its write folds into the scheduled route or re-derives at the bridge — the ruled grammar:
   the bridge-publisher is the ONE rename boundary and the publisher never renames); the
   smartx-tree per-firm distribution writer's serve write follows its W-4-moved home.
3. **Legacy chain retirement:** feeders + `mdpf_aggregate_aua` + legacy platinum names retire —
   LAST, only after every repoint has run green through at least one full scheduled cycle.
   Nothing is deleted before this step; retirement itself is a deploy-prefix + dispatch change
   with the legacy code still in git (recoverable by revert).
4. **Carry-import post-cutover form (the §6.2 decision Phase B owes):** RECOMMEND **KEEP as a
   declared CARRY-IMPORT binding row** reading the served count carry — its post-cutover
   self-reference is already engineered (the W-7 frontier-stamp guard [dim:589-603]) and the
   declared-row form makes the serve-read visible in the binding table rather than buried in a
   loader. Alternative (re-derive counts from account_dist history) adds a derivation with no
   consumer demanding it — not recommended.

**SERVE-FREEZE WINDOWS:** each W-5 step executes in the daily quiet window **~17:30Z → 11:30Z
next day** — after the day's full chain (trigger ~13:0xZ fire, accrual cron 15:45Z, publisher
fires observed 14:59Z/15:44Z, post-17:15Z emitter bundle) and before the next day's board —
with the freeze = no serve-key writes during the step (each step is minutes; the window is
~18 hours). A step that cannot complete + verify inside its window rolls back the same window
(the half-landed-deploy NEVER rule is the law here; the change-management ledger entry opens at
step start and closes at verify).

**DELTA=0 AT SERVE:** per-firm served-artifact parity pre/post every repoint (publisher-output
comparison under the §5 normalization). Any diff = the step rolls back, no exceptions — a
wanted content change is by definition NOT part of this migration (never-widen).

---

## 7. §5 The DELTA=0 parity class (defined once)

- **Normalization:** strip exactly the volatile stamp fields — `generated_at`, `last_updated`,
  `_provenance.written_at` — then require BYTE EQUALITY. No numeric tolerance: the trio's own
  idempotency contract ("generated_at stamps differ; series bytes do not" [trio:19-20]) is the
  precedent that everything else must tie exactly.
- **Instrument — AMENDED 2026-08-05:** an **AD-HOC, RUN-AND-READ** comparison, executed by hand
  before the port and **left standing nowhere**, that prints the denominator (files compared,
  fields stripped) per run.
  ⛔ **The prior wording — *"a small read-only comparator (Phase-C build item, DS lane)"* — is
  VETOED and is struck.** Scheduling a comparator as a build item creates exactly the standing
  second instrument Andrew's 2026-08-04 veto names: *"The comparator is also a HORRIBLE idea
  because it just muddies the water even further… Delete all of that and mark it all as
  deprecated."* **A comparator that never dies is the debt; the comparison itself is fine.**
- **Its own control (UNCHANGED and still mandatory):** before first gating use, a MUTANT run
  (perturb one series value in a copy) must FAIL — **a comparator that cannot fail is not a
  control.** Exercised, not assumed. *(This survives the veto intact: it is a property of the
  ad-hoc run, not a standing process.)*
- **Cycle rule — CLARIFIED, because the two halves read as contradictory:** **production EVIDENCE
  comes only from SCHEDULED cycles** (an ad-hoc artifact is never production evidence, NEVER#4).
  **The ad-hoc QA comparison above is a QA INSTRUMENT, not production evidence** — it establishes
  build-time correctness before the port; the scheduled cycle after the port is the acceptance.
  Both statements are true and neither licenses the other: **run-and-read to decide whether to
  port; scheduled-run to accept what was ported.**

## 8. What this plan deliberately does NOT do

- No alarms, monitors, or freshness checkers anywhere (moratorium).
  ⛔ **AMENDED 2026-08-05 — the original justification is struck:** it read *"the parity harness is
  a gate on a migration step, not a standing monitor — it retires with the migration."* **That
  argument is exactly the one the 08-04 veto rejects.** "It retires with the migration" is what
  every shadow path and standing comparator has claimed, and Andrew's own words are that *"they
  never ever get decommissioned."* **There is no parity harness in this plan any more** (§7): the
  comparison is ad-hoc and leaves nothing behind, so the moratorium question does not arise
  rather than being argued around.
- No re-litigation of ruled forks; no ETFS-CANON contact (the 49f custody binding carries the
  sovereign ruling verbatim; a future ETFS ruling flips one row, zero route change — ratified).
- No `mdpf-daily-trigger` scheduling redesign: the convergence-gate/no-schedule class (the
  08-03 silent gap) is REAL but OUT OF SCOPE here — named as adjacent debt for CTO routing,
  not smuggled into this program.
- No touch of today's in-flight water-test/supersede stream artifacts.

## 9. Acceptance criteria for THIS deliverable (plan-level)

1. Every wave carries the four fields (lands/parity/rollback/serve-exposure) — §§1-6.
2. Serve-touching steps are ALL inside W-5 behind the four entry gates incl. Andrew's word.
3. The DELTA=0 class is defined with a normalization contract + mutant control (§7).
4. C-1/C-2 dispositions carried forward: C-1 verbatim in the W-1 binding row; C-2 as a hard
   W-4/W-5 precondition (§1, §5 sequencing rule).
5. The §6.2 carry-import decision is made (§6 step 4) with the alternative stated.

Phase-C work items implied by this plan (builder, config, moves — **NOT a comparator; struck
2026-08-05 per the 08-04 veto, see §4/§7**) get their own TOs
at Phase-C seating — none are begun by this document.
