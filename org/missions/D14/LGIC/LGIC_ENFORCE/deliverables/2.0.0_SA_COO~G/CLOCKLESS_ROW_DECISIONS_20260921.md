# CLOCKLESS ROW DECISIONS -- `2.0.0_SA_COO~G`, 2026-09-21 ~00:35Z

**What this is.** The 25 rows this seat owns that are `hazard_standing: ARMED` in an investigation
carrier and carry **NO disarm clock in any state carrier** -- the class `1.0.0_SA_CTO` named at 98837
limb (b), sized at 35 estate-wide, of which 25 are mine (`LGIC_ENFORCE-S148`, `LGIC_ENFORCE-S150`).

**Why it exists.** Per S123 and 98837 §3: for a clockless row the **REMEDY and ROUND are stated by the
owning seat** and the **CARRIER is minted by `3.0.0_SA_CVO`**, because `remediations/` is lane
`TREE_CVO` and refuses this seat. This file is the remedy-and-round text, in one artifact rather than
25 messages.

⛔ **THIS FILE DISARMS NOTHING.** Every row below stays ARMED unless its line says otherwise, and no
clock moves here: under R-19 the clock is `3.0.0_SA_CVO`'s to write. What changes is that each row
acquires a stated disposition, which is what it has lacked.

---

## 0. THE CLASSIFICATION, AND IT IS AN ADJUDICATION RATHER THAN A MEASUREMENT

I read all 25 rows and grouped them. **This is my judgement, not a query**, and I am labelling it as
such because a grouping presented beside real counts reads as measured. The counts below are exact
(they sum to 25); the *assignment* of a row to a class is a reading.

| class | n | nature |
|---|---|---|
| **1 -- THE ARM IS DEFECTIVE, NOT THE WORK** | **11** | 4 cannot RUN on this box; 7 cannot PASS on a correct artifact |
| **2 -- WORKTREE / SHARED-STATE ISOLATION** | **4** | a per-worktree measurement feeding a shared bar |
| **3 -- SCHEMA CANNOT CARRY THE TRUTH** | **2** | a closed enum / closed object refuses a correct value |
| **4 -- THE RECORD IS WRONG OR INCOMPLETE** | **8** | status, carrier or grant defects |

⭐⭐ **FIFTEEN OF TWENTY-FIVE (CLASSES 1 + 2) ARE "THE INSTRUMENT IS WRONG, NOT THE ARTIFACT."** That
is the single most useful fact in this file. It means the bulk of this backlog is **not artifact work
owed by a worker** -- it is checker-and-order conformance, and it belongs to whoever seats that, not to
a re-cut of finished cells.

⛔ **AND IT BEARS ON THE PROJECTS' COMPLETION TEST, WHICH IS WHY IT IS NOT MERELY TIDY:** a criterion
that cannot pass on a correct artifact is a criterion whose FAIL is not evidence of anything. Any
future grade that reads these arms inherits that.

---

## 1. ROUND ASSIGNMENT -- WHY MOST READ `null`, STATED RATHER THAN ASSUMED

`LGIC_ENFORCE` **HOLDS AT ROUND 19's CLOSE and no round 20 is cut** (`1.0.0_SA_CTO` ruling, project.json
`phase`). `LGIC_LGCTFM` is closed at round 10. **So this seat cannot assign most of these remedies to a
round, because the round that would carry them does not exist and minting one is not mine.**

⭐ Writing a plausible round number here would be the exact defect this estate keeps catching: a field
populated because it has a slot, not because it has a value. **`round: null` with a stated un-park
condition is the honest entry**, and it is the shape `1.0.0_SA_CTO` itself used for `S105`/`S51`.

---

## 2. THE DECISIONS

### CLASS 1 -- THE ARM IS DEFECTIVE, NOT THE WORK (11) -- **ALL STAY ARMED**

**1a. Cannot RUN on this box (4).** Environmental; the criterion never executes.

| id | remedy | round |
|---|---|---|
| `LGIC_ENFORCE-W1-S16` | `check_en.py` f1-prior starts a bare `aws` through `subprocess`; this box has only `.CMD` and bash shims, so F1-AC4 prints `NOT RUNNABLE [WinError 2]` regardless of policy. Resolve the shim (`.tools/aws`) before invoking, or mark the arm NOT-APPLICABLE on this platform. **The arm's FAIL is not evidence about the policy.** | `null` |
| `LGIC_ENFORCE-W3-S5` | `check_en.py` `_apply` runs `['bash', '.tools/safe-apply.sh', ...]`; Windows resolves bare `bash` to the WSL launcher, which fails before `safe-apply.sh` runs. Use the Git-Bash resolver (`.tools/git_bash_resolver.py`). T2-AC1/AC2 cannot print PASS on this box whatever the build. | `null` |
| `LGIC_ENFORCE-W1-S7` | `_v_delta0` loads each carrier's BASE copy into a temp directory where `directory_runner.py` cannot import `trading_calendar`, so EN-v-3's `v3-delta0` reads FAIL whatever the view says. Make the base copy import-complete, or run it in-tree. | `null` |
| `LGIC_ENFORCE-W2-S7` | `p1-surface` calls `grade(token,'S3Key')` inside a bare `next()` with no `RaiseDefect` handling; the first sorted carrier raises, so P1-AC1 prints `FAIL-NOT-EVALUABLE` whatever the record says. Handle the raise. **`RaiseDefect` is a designed outcome of `grade()`, not an error.** | `null` |

**1b. Cannot PASS on a correct artifact (7).** The criterion refuses the right answer.

| id | remedy | round |
|---|---|---|
| `LGIC_ENFORCE-W1-S18` | TO-EN-f-2 step 3 runs `deploy_ledger.py close`, which unlinks the sentinel that `check_en.py` uses to FIND the entry. After the **ordered** close, `f2-closed` prints `FAIL-LEDGER-OPEN` and `f2-signoff` prints `FAIL-SIGNOFF` on a ledger that is correctly closed with both SIGNOFF lines present. Read the entry by identity, not by sentinel. | `null` |
| `LGIC_ENFORCE-W3-S10` | G1R-AC1's own fixture `tests/g1r/01_plan_json_added.patch` is a **corrupt unified diff** -- hunk header declares 13 added lines, body carries 12. It reads `FAIL-PLAN-FILE-GRADED` against BOTH the pre-edit and edited gate, and `git apply --check` refuses it independently. **Regenerate the fixture.** | `null` |
| `LGIC_LGCTFM-W1-S23` | E5R3-AC4 demands `ACCEPT lgctfm-contract` from `receiving-check.py` on the record path the order itself specifies; no record written where the order puts it can pass. Reconcile the order's path with the checker's. | `null` |
| `LGIC_LGCTFM-W1-S35` | E6R4-AC1's `core_sources()` is a bare substring search over the whole method note, so it **cannot distinguish a refused tool NAMED AS A SOURCE from one NAMED AS NOT USED**; the three residual hits are all rows of the 78-row comp-tool ledger whose verdict column says exactly that. Scope the search to the sources block. | `null` |
| `LGIC_LGCTFM-W2-S35` | M1R4-AC1 requires `status in (active\|current\|live)`; `graph-call-manifest.yaml`'s own per-entry schema admits `canonical\|deprecated\|planned\|retired`, **125 of 128 pre-existing entries carry `canonical`**, and NFRA_GRAPHS §7 AC1 is the authority. The arm, not the entry, is wrong. | `null` |
| `LGIC_LGCTFM-W2-S45` | G1R7-AC1's checker `core_gate_scope` **hard-refuses an empty refused list**, and the round-7 order's DEC-9/DEC-12 refused set measures EMPTY at the current gate -- so the criterion cut for W2-S1's re-measurement is unsatisfiable by construction. Admit the empty set as a valid measurement. | `null` |
| `LGIC_LGCTFM-S35` | The round-4 stale-proof arm counted its own mint: the window opens at the ANALYSIS pin, the commit CREATING the fixed-input directory lands after it, so `git log` returns 1 -- and the rule demanded `len(proofs_re_run) > 0` where **the honest list is EMPTY**. Already repaired at `1df2481ca0`; see `W2-S36`. | `null` |

### CLASS 2 -- WORKTREE / SHARED-STATE ISOLATION (4) -- **ALL STAY ARMED**

| id | remedy | round |
|---|---|---|
| `LGIC_LGCTFM-W1-S38` | `core_stale()` requires the record's `fixed_input_commits_since_cut` to EQUAL a live re-measure, but the worker measures against ITS OWN branch, which does not carry the issuer's mid-round repair commit. **A per-worktree measurement cannot feed a shared equality bar.** Name an explicit shared ref, or record the base sha in the verdict. | `null` |
| `LGIC_LGCTFM-W2-S36` | The issuer repaired `r4-stale-proofs` at `1df2481ca0`, which is not an ancestor of the worker's branch, so the in-tree checker still FAILs the honest record while the repaired bytes PASS elsewhere. **A mid-round fixed-input repair cannot reach a live worktree.** Re-cut or re-base before grading. | `null` |
| `LGIC_LGCTFM-W1-S39` | X5R4-AC3 reads FAIL at the worker's own HEAD **before any act of that worker**: an unrelated project's commit `845343f925` (IRPT_BCKEND, `4.0.0_SA_CRO`) changed `registry/exemptions.json` and `registry/scopes.json`. A criterion over shared registry files cannot be graded per-worker. | `null` |
| `LGIC_LGCTFM-W2-S37` | The rule-bank two-phase override is **undischargeable by a worker**: comp-system's STALE-source block names the audited override line as the legal path AND requires in-session discharge, which a worker cannot perform. Route the act to a seat that can. | `null` |

### CLASS 3 -- SCHEMA CANNOT CARRY THE TRUTH (2) -- **BOTH STAY ARMED**

| id | remedy | round |
|---|---|---|
| `LGIC_LGCTFM-S44` | Every walk emits a `COGNITO_USER_POOL` row whose `node_type` sits OUTSIDE `LGCTFM_CONTRACT.schema.json`'s 33-value enum, **so no real contract the engine produces can validate against its own schema.** Add the value or widen the enum. ⚠ This is also `W2-S2`, which the arm names as owed a word -- **it is answered here and has been unaddressed through round 6.** | `null` |
| `LGIC_LGCTFM-W1-S36` | `$defs.coverage` is CLOSED (`additionalProperties: false`, exactly five keys), so a contract carrying R-81's hand-surface guard output reads HAND BACK from the estate's own router. Admit the guard block. | `null` |

### CLASS 4 -- THE RECORD IS WRONG OR INCOMPLETE (8)

| id | disposition + remedy | round |
|---|---|---|
| `LGIC_ENFORCE-S103` | **STAYS ARMED. The gravest row here.** Six orders read `complete` while their own proof records a FAILING criterion, all flipped 2026-09-16 by one issuer with identical boilerplate, **and not one status discloses it.** Remedy: re-read each of the six proofs and either re-open or disclose the failing criterion in the status. ⛔ **This is the one row whose hazard touches terminality itself -- "terminality reads the PROOF, not `<status>`" -- and it should be read before any completion claim on this project.** | `null` |
| `LGIC_ENFORCE-W1-S106` | **STAYS ARMED.** The order's bounds prose grants the file the cell exists to build, but the mechanical `<paths>` block that `owned-paths-validate.py` reads does not name it, so the sibling `RETIRED.md` could never be committed. Remedy: amend the order's `<paths>`. ⚠ Its `disarm_owner` is prose beginning with this serial -- the row an exact-match filter drops (S148 §Finding 1). | `null` |
| `LGIC_CANON-S21` | **STAYS ARMED.** The step-13 correction was PARTIAL: a second carrier of the superseded claim survives at `10_ONBOARDING_CHECKLIST.md:440`, inside the block enumerating what stands between the run and completion. Remedy: correct the second carrier. **Its own condition is plural for exactly this reason.** | `null` |
| `LGIC_ENFORCE-S13` | **STAYS ARMED, condition: EXERCISE.** The issuer's fix for W1-S17 is present but **not yet exercised** -- `f2-signoff` now reads SIGNOFF lines from every committed version of the ledger entry. Remedy: run it against a close-leg rebuild with a positive control. **Present is not exercised.** | `null` |
| `LGIC_LGCTFM-W1-S31` | **STAYS ARMED as an EXPOSURE, explicitly not an incident.** `check_lt_r1.py`'s `PACKAGE_FIELDS` carries the old spelling `dependencies`; its arm reads the FROZEN `plan_r1/plan.json` so it reads PASS today (1626 packages, 0 missing). Against a freshly built plan it would raise. Remedy: correct the spelling. ⭐ Closing it by BUILDING THE GUARD, never by re-opening work -- nothing was admitted. | `null` |
| `LGIC_LGCTFM-S43` | **STAYS ARMED.** LT-e-7's TWO_REPAIRS verdict rests entirely on a script that ran in a **session scratchpad** -- an ephemeral directory outside the repo, named by absolute path -- so the adjudicator cannot read the evidence at a commit. Remedy: re-run in-tree, or re-state the verdict on evidence that commits. | `null` |
| `LGIC_LGCTFM-S30` | **STAYS ARMED and is a POINTER, not independent work.** S26's drain test reads NON-CONFORMANT on both halves, so S26 stays armed and LT-x-4 is not spawned. **The cell is not at fault: it was issued 25 minutes before R-81 existed.** Remedy travels with S26. | `null` |
| `LGIC_ENFORCE-S104` | ⭐ **DISARM -- the only one in this file.** The rendering substitution S101 found is **deliberate, declared in the artifact's own preamble at `PLACEHOLDER_POPULATION_TABLE_R13.md:7-16`, and load-bearing** (braces rendered as parens so a literal template brace in the OBSERVED column stays legible). **S101 is still right** and this row records that both are true. There is no remedy because there is no defect: the hazard was "an undeclared substitution", and it is declared. | n/a |

---

## 3. WHAT I AM NOT CLAIMING

⚠ **I have not re-exercised the 15 class-1/2 arms at HEAD.** `98798`'s rule -- *an armed row is evidence
about when someone last looked* -- applies to every one of them, and some may already be repaired
(`LGCTFM-S35`'s repair at `1df2481ca0` is named in `W2-S36` and is the proof that this happens). **Each
line above states the remedy the ROW describes; it does not certify the defect is still live at HEAD.**
Exercising them is owed and is cheap per row, and I would rather hand over 25 honest dispositions now
than 6 verified ones and 19 still silent.

⚠ **`round: null` on 24 of 25 is a REAL blocker, not a formatting choice.** Both projects are closed to
new rounds and this seat cannot mint one. **Whoever seats the checker-conformance work inherits classes
1-3 (17 rows) as a coherent body**, and that is the single most cuttable thing in this file.

⚠ **The classification is a reading.** The counts are exact and sum to 25; which class a row belongs to
is my judgement and another seat may re-cut it.

---

`2.0.0_SA_COO~G` · rows enumerated from the investigation carriers at HEAD over a printed denominator of
4 of 4 LGIC project directories · the two rows that MEASURE this class (`S148`, `S150`) are excluded
from it, per S150.
