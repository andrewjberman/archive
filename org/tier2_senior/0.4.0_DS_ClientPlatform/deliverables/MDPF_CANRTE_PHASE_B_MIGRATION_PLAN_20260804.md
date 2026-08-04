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

## 3. W-2 — Model-B spine builder, build-alongside (staging writes only)

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

## 4. W-3 — Derived producers parameterized (metrics / distribution / pair fold-in)

- **WHAT LANDS:** the same binding parameterization for `dim_mdpf_aum_metrics`,
  `dim_mdpf_account_distribution`, and the cottonwood pair's derived outputs (the pair already
  imports the dim machinery [pair:63-65] — the consolidation is half-done in the dependency
  direction). Includes the global meta-provenance one-hunk so every derived artifact carries the
  uniform meta block (source_spine / as_of_basis / firm_id). Same shadow → 3-green → swap
  idiom as W-2.
- **PARITY GATE:** DELTA=0 per derived artifact per scope; PLUS the derived-vs-spine tie law
  (the water-test class: per-model tie to the cent) asserted by the harness, not by rc.
- **ROLLBACK:** dispatch-step revert, incumbents stay deployed.
- **SERVE EXPOSURE:** zero (staging + the accrual's dated tree read the same content by parity).

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
- **Instrument:** a small read-only comparator (Phase-C build item, DS lane) that prints the
  denominator (files compared, fields stripped) per run.
- **Its own control:** before first gating use, a MUTANT run (perturb one series value in a
  copy) must FAIL — a comparator that cannot fail is not a control. Exercised, not assumed.
- **Cycle rule:** parity is only ever read on SCHEDULED cycles (never an ad-hoc build — ad-hoc
  artifacts are never production evidence, NEVER#4).

## 8. What this plan deliberately does NOT do

- No alarms, monitors, or freshness checkers anywhere (moratorium; the parity harness is a
  gate on a migration step, not a standing monitor — it retires with the migration).
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

Phase-C work items implied by this plan (builder, comparator, config, moves) get their own TOs
at Phase-C seating — none are begun by this document.
