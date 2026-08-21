# C6-KERNEL Phase 1 -- S0 ground-read of the five named embryos

**TO:** `NFRA_EPISTEMY.C6-KERNEL.atomic-transaction-kernel` · **Activated** 2026-08-21T0309Z (COO GO 64235, C4-LEASE closed)
**Seat:** `0.7.0_AE_CloudOps` · **Phase 1 only.** No embryo was modified -- requirement 1 makes them precursors I READ.
**Fence:** build-staging. Nothing wired, no gate armed, no monitor built. Activation on any real mutation class is Andrew's worded act.

The TO asks, per embryo: **what does it BIND, and what does it NOT bind.** That framing is the whole
value of the phase, because four of the five bind something *adjacent to* the kernel's need and the
resemblance is what makes them dangerous to reuse unexamined.

---

## THE RESULT IN ONE TABLE

| # | embryo | binds | does NOT bind | kernel element it is an embryo OF |
|---|---|---|---|---|
| E1 | `safe-commit.sh:222-256` mutex | mutual exclusion between concurrent committers | **check-to-act** | isolation |
| E2 | `safe-apply.sh:50-54` -> HALTGT | a STOP signal to the last reversible moment | any fact about **state** | checkpoint *placement* |
| E3 | `.tools/deploy_ledger.py` (1,057 ln, 520 entries) | the half-landed-deploy class | **admissibility**, residue, priced debt | ledger *shape* |
| E4 | TF plan-vs-state-serial | a plan to the state it was computed against | anything outside Terraform | a token -- **not ours** |
| E5 | `precondition_token.py` (451 ln) | one S3 put to one live read | **anything multi-leg** | element D, atomic binding |

**Coverage verdict: the five embryos supply ISOLATION, CHECKPOINT-PLACEMENT, LEDGER-SHAPE, AN
EXTERNAL TOKEN and ATOMIC-BINDING. Not one of them supplies a residue vector, a recovery-capacity
function, priced rollback debt, prefix safety, or admissibility** -- i.e. every property K2/K3 turn on
is genuinely net-new, and the TO's "mostly WIRING EXISTING CONTROLS" (CTO 63768) is right about the
*binding* elements and not about the *pricing* ones.

---

## E1 -- `safe-commit.sh` mutex · **a MUTEX IS NOT A TOKEN**

`LOCK_DIR="${SAFE_COMMIT_LOCK_DIR:-$(git rev-parse --absolute-git-dir)/commit-queue.lock}"` (`:222`),
acquired by `while ! mkdir "$LOCK_DIR"` (`:226`) -- `mkdir` as an atomic test-and-set, which is the
correct primitive on a filesystem with no `flock` (Rule 16: `flock` is a Git-Bash absentee). PID
stamped at `:256`; stale-breaking on a dead holder (`:227-231`) and on a 60s timeout (`:238-243`).

**BINDS:** two agents cannot interleave a commit.
**DOES NOT BIND:** that the world is what the committer checked. Serialization and freshness are
different properties -- **two agents can serialize perfectly and the second still commits against a
premise the first invalidated.** The lock has no read-token, no ref comparison, no notion of "what did
you observe before you decided to write."
**AND IT IS NOT EVEN A DURABLE MUTEX:** `:238-243` **breaks the lock on a 60s timeout**, dispossessing
a *legitimate slow holder*. For the kernel that is a positive lesson, not a criticism: a timeout-broken
mutex is precisely the shape that must be inexpressible in a transaction kernel, because the
dispossessed holder receives no signal and proceeds believing it still holds.

## E2 -- HALTGT · **SHAPE WITHOUT SOUNDNESS, AND THE LAW ALREADY SAYS SO**

`safe-apply.sh:50-54` sources `halt-gate-check.sh` and fires `halt_gate_check "safe-apply"` immediately
before the irreversible apply. The *placement* is exactly right and is the pattern K2 wants: a
checkpoint at the last reversible moment.

**DOES NOT BIND:** anything. CLAUDE.md Rule 18 states it in the law file -- *"A HALTGT PASS IS NOT
EVIDENCE YOU WERE NOT HALTED"*: the checkpoint sees only *unread* files directly under
`inbox/<serial>/`, so **a live Monitor (which moves the message first) guarantees a silent empty-inbox
`exit 0`**, and a `~lane` agent is unhaltable regardless.
**Kernel consequence, stated so it is not re-learned:** I inherit HALTGT's *placement* and none of its
*evidence model*. A C6 checkpoint that concluded "no objection was raised, therefore proceed" would
reproduce this defect one layer up -- **absence-of-signal is not a safety verdict**, which is also the
S6 absence-semantics rule the TO puts on every nullable.

## E3 -- the deploy-completion ledger · **THE SHARPEST FINDING: THE CLOSEST EMBRYO IS BUILT ON THE MODEL K3 MUST FORBID**

Population: **520 entries** under `org/critical_paths/change_management/`. Reader/writer
`.tools/deploy_ledger.py`, **1,057 lines**. Real schema surface, and a good one:
`LEG_KINDS` is a **6-value closed set** (`:69` git · s3-prefix · activation · ec2-baked-asset · verify ·
tf-lambda), `APPLY_LEG_KINDS = LEG_KINDS - {"verify"}` (`:77`), `GATE_TYPES = {"sovereign","external"}`
(`:78`, explicitly *"the structured gate class -- NOT free prose"*), `TERMINAL_STATUS_TOKENS` (`:92`),
`HELD_STATUS` + `DEFAULT_HELD_STALE_DAYS` escalation (`:79-81`). It genuinely instruments NEVER#8.

⛔ **BUT EVERY ROW IS AN AGENT SELF-REPORT.** The write path is `cmd_open` (`:244`), `cmd_close_leg`
(`:292`), `cmd_close` (`:308`), `cmd_hold` (`:326`) -- **CLI subcommands an agent invokes to assert its
own state.** The ledger records what an agent SAYS it did.

PRD sec.2.7 declares, of the Cumulative_Residue_Ledger: **gateway-maintained -- AGENT SELF-REPORT IS
INADMISSIBLE.** So the estate's nearest ledger embryo is constructed on exactly the admissibility model
the kernel is required to make impossible. **This is not a defect in the deploy ledger** -- it is a
correct design for a *coordination record*, which is what it is. It is a defect only if inherited.

**Therefore K3 cannot be built by extending E3, and m4 is not a formality.** The kernel's ledger must
be written by the kernel from things it OBSERVED, and an agent-asserted row must be structurally
unrepresentable -- not rejected by validation, *inexpressible*, the same construction as C7's
hand-authored-row control and ~A's `known_negative: const "GENERATED"` (COO 64099: honesty enforced
where it cannot be skipped).

## E4 -- TF plan-vs-state-serial · **A REAL TOKEN, IN SOMEONE ELSE'S KERNEL. IT IS NOT OURS.**

The TO lists this among the estate's embryos ("TF plan staleness against the state serial (a partial
token)"). Measured, **our wrappers implement none of it**:

```
grep -rniE 'state.*serial|tfstate.*serial' .tools/   ->  1 hit
control: 'HALT_ACK' in .tools/                       -> 13 hits   (the grep discriminates)
```

The mechanism is **internal to the `terraform` binary** -- state serial/lineage checked at apply, an
apply refused when the plan was computed against a superseded serial. That IS a genuine check-to-act
token and it is the closest thing in the estate to what C6 needs.

**Two consequences, both worth stating rather than glossing:** (1) we *consume* it, we do not own it,
cannot extend it, and cannot make it emit an Observation_Record; (2) **it covers only TF-managed
mutations** -- which is precisely why the PRD names RAW S3 PUT as the naked spot. *I flag the TO's
framing: describing this as one of our partial tokens reads as though we hold a mechanism we do not.
Terraform holds it.*

## E5 -- `precondition_token.py` · **CORRECT AND SINGLE-ACT**

Mine, C10-PRECOND @82c3f36f24 + @cde3d4ba59, 451 lines. Binds a plain S3 put to a live-read precondition
via S3's own conditional write -- `If-Match` for update, `If-None-Match: *` for first-mint (`:13`).
`_request_hash` (`:173`) is the **normative digest home** (CTO 0.1.0: any other serialization is
NON-CONFORMANT even if the sha256 pattern matches). `StopAndSurface` (`:100`) on `ParamValidationError`
-- never a silent degrade. `DETAIL_ETAG_MISMATCH_412` (`:87`) is the discriminating rejection.

**BINDS:** one read to one write, atomically, at the store.
**DOES NOT BIND:** anything multi-leg. There is no transition, no checkpoint, no residue, no terminal,
no rollback. It is one token and one put. **That is element D doing its job, and the kernel's task is
to generalise the binding without inheriting the single-act assumption.**

---

## RULE-24 PRE-RECORD -- the terminal axis (the TO's question: is CONTAINED distinct from ROLLED_BACK?)

**Answer: YES, and collapsing them would hide the exact state NEVER#8 exists to catch.** Declared layer
= *the terminal states of one governed transition*. Candidate set, tested for MECE over that layer:

| terminal | the world after | recovery debt |
|---|---|---|
| `COMPLETED` | every leg landed; intent achieved | none |
| `ROLLED_BACK` | **no leg's effect survives**; pre-transition state restored | paid, and the payment is proven |
| `CONTAINED` | **some legs' effects SURVIVE**, bounded and declared; intent NOT achieved | **outstanding, priced, unpaid** |
| `ABANDONED_UNSAFE` | past a declared point of no return; neither restorable nor bounded | unpayable -- escalation, not a terminal the kernel may choose |

**CONTAINED vs ROLLED_BACK is the half-landed deploy.** A kernel with only ROLLED_BACK must report a
partially-landed transition as rolled back, which is **false in the direction that hides stranded
state** -- the 2026-06-11 stranded-layers class NEVER#8 was written for. `ABANDONED_UNSAFE` is the
uncovered member I went hunting for per the postulate-(i) CE half: it is the honest home for a
transition whose recovery requirement exceeded capacity *after* the point of no return, and without it
that case would be mis-filed as CONTAINED, which asserts a boundedness nobody established.

**Postulate check:** (i) MECE over the declared layer -- disjoint by "does any effect survive" x "is the
survival bounded"; (ii) same grain -- all four are whole-transition terminals, none is a leg outcome;
(iii) one intent -- terminal STATE only, no disposition/blame axis mixed in; (iv) state coherence --
**this one is worth naming: `ABANDONED_UNSAFE` does not move with the others.** The other three are
reachable by kernel logic; that one is reachable only by escalation, so a "build the terminal handler"
plan covers three of four. Declared rather than absorbed.

*This is a PRE-record. The axis routes through `4.0.0_SA_CRO` base as registry executor with a full
Rule-24 record + token census before `1.0.0_SA_CTO`'s arch gate -- cite-not-copy, never landed in-lane.*

---

## CARRIED INTO PHASE 2

- **m7 added** (beyond the TO's m1-m6), per COO 64235 note (b): a lease VALID at leg-open and EXPIRED by
  a later checkpoint, with the kernel proceeding, must **REFUSE at that checkpoint**. m5 catches a claim
  that asks for too much *at leg-open*; it cannot catch one that was honest then and expired at leg-3.
  Without m7 the kernel silently converts a lease into a lock -- the one thing sec.2.7 forbids by name.
  **This worktree generates the fixture on its own**: COO's own mint went VALID -> EXPIRED across a live
  commit window, and a peer commit mid-transition is the ordinary case on CLOUD, not an edge case.
- **K3 cannot extend E3.** The ledger must be kernel-written from observation; an agent-asserted row is
  to be inexpressible, not rejected.
- **No checkpoint may conclude from absence-of-signal** (the HALTGT lesson + S6 absence semantics).

## NOT DONE / LIMITS

- Phase 2 (battery) and Phase 3 (exercised multi-leg abort) not started.
- `halt-gate-check.sh` read at its call site only (`safe-apply.sh:50-54`), not line-by-line through its
  own 21,393 bytes; the Rule-18 evidence claim above is quoted from CLAUDE.md, not re-derived at source.
- The E4 conclusion rests on a `.tools/` grep with a firing control; I did **not** read terraform's own
  source to confirm the serial mechanism, and I have not claimed a line citation for it.
