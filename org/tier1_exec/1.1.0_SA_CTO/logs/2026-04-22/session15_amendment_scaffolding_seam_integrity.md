# Session 15 — Wave 3 PRD amendment scaffolding (seam integrity + cross-lane definitions)

**Date:** 2026-04-22
**Agent:** 1.1.0_SA_CTO
**Principal:** Andrew
**Predecessor:** session14 (.039 + .045 Stage 2 activation); immediately prior — `.048` Lane A integrity invalidation (DS commit df168552) + `.050` Lane B worktree contamination (DS 1.4.0 stopped, COO reset at 36367765f).
**Trigger:** /loop COMP_LEARNS while blocked on Andrew A/B/C scope call. Productive CTO-lane work available: scope-invariant PRD amendment scaffolding.

---

## Objective

Draft the scope-invariant portions of the Wave 3 PRD amendment so that when Andrew's scope call lands (A = full pause, B = split-Wave-3a, C = Lane B only), I can integrate the lane-specific dispositions and ship the amendment as a single commit rather than authoring from zero under time pressure.

**What is scope-invariant** (applies under A, B, and C):
- Seam Integrity requirement class (meta-section Andrew approved)
- Cross-lane "clean" definition
- Lane B (§3) additions — Lane B is active in all three scopes

**What is scope-dependent** (authored after A/B/C lands):
- Lane A (§2) disposition — rebuilt (A, B) or scoped-out (C)
- Transition narrative in §1 about wave structure changes
- Updated JSON `phase` + `blocking` text (COO's lane per `.053`)

This log is DRAFT content. No commits this session until Andrew picks scope.

---

## §0 — Seam Integrity (new meta-section, ~30 lines as authorized)

**Proposed placement:** between existing §0 (Design Center) and §1 (Wave Structure), as a new `## §0.5 Seam Integrity Requirement Class`.

### Proposed text

```markdown
## §0.5 Seam Integrity Requirement Class

Two Wave 3a runs (`.048` dev-4 and `.050` Case 3 unaided) produced integrity findings
on 2026-04-22 that share a structural pattern: both failures occurred at seams between
human setup and harness automation. This wave formalizes the pattern as a requirement
class.

**Definition.** A "seam" is any control-flow transition between human (agent or
operator) work and harness-automated work. Examples:

- Bundle authored manually → dev-loop consumed automatically (`.048` failure mode)
- Aided run ended manually → unaided run started manually with shared repo state (`.050` failure mode)
- Runner provisioning completed → DS agent began navigation (future failure surface)
- Compiler mutation committed → bundle author scored the mutation (conflict-of-interest surface)

**Requirement.** Every seam must be gated by a packet-level hygiene check that fails
closed. The gate must:

1. Be declared in the task packet's `compiler_tools_mandate` phase 0 (before any
   measurement activity)
2. Execute before the downstream automation touches any state
3. Produce a machine-verifiable pass/fail (exit code 0 or non-zero)
4. Block the run when it fails — no flag, no caveat, no "contaminated:true" opt-in

**Explicitly out of scope for this amendment:** replacing all manual setup with
runner-driven automation. Manual-first per AUTOMATION_V1 §6 remains valid for first-pass
cases. The requirement is that manual setups must end with the same hygiene guarantees
that runner-driven setups provide.

**Why this is a class, not a list.** Spec'ing every future seam individually produces
uncovered gaps. Naming the class allows future TOs to identify new seams and apply the
same gating discipline without amending the PRD again. The cost is a small amount of
up-front abstraction; the benefit is closing the "unnamed seam" discovery failure mode
that caused `.048` and `.050`.
```

**Status:** ready to commit verbatim once scope lands.

---

## Cross-lane "clean" definition (new subsection, ~15 lines)

**Proposed placement:** §0.5 paragraph or a short §0.6 immediately after Seam Integrity.

### Proposed text

```markdown
## §0.6 "Clean" Definition (applies to all lanes)

"Clean" state for any Wave 3 run means ALL of the following, verified before any DS
agent navigation or loop iteration begins:

1. **No uncommitted diffs** — `git -C <target> diff --quiet` exits 0
2. **No staged changes** — `git -C <target> diff --cached --quiet` exits 0
3. **No untracked files** in target path — `git -C <target> status --porcelain` empty
   (exceptions must be declared in packet's `ignored_paths` list)
4. **No stale bundles** for the current `task_id` — `comp/dev-bundles/<task_id>/` absent
   or emptied (dev-mode only)
5. **No dirty submodules** — submodule HEAD matches pinned commit
6. **For dev mode:** canonical source present at `comp/targets/<task>/_repo/` checked
   out at `baseline_commit` (not a temp tree authored at runtime)

Violation of any item is a hard-stop. The gate returns non-zero and the orchestrator
aborts the run before DS agent context engages with the target.
```

**Status:** ready to commit verbatim once scope lands.

---

## Lane B additions (scope-invariant — Lane B active in A, B, and C)

**Proposed placement:** new `§3.8 Preflight Gates` subsection after `§3.7 Claim Scope`.

### Proposed text

```markdown
### 3.8 Preflight Gates (mandatory)

Every Case 3 run (aided and unaided, all conditions) must pass these gates before DS
agent navigation begins. Gates are declared in the task packet's
`compiler_tools_mandate` phase 0.

| # | Gate | Fail response |
|---|------|---------------|
| 1 | `comp/targets/sphinx/_repo/` exists and HEAD is `baseline_commit` | Abort; provisioning skipped or misconfigured |
| 2 | §0.6 "clean" definition satisfied in `_repo/` | Abort; run `git reset --hard HEAD` then retry; if persistent, escalate to CTO |
| 3 | No DS agent has touched `_repo/` in the current session (first-touch invariant) | Abort; fresh DS session required |
| 4 | Task packet `task_id` matches directory provisioned | Abort; cross-condition contamination risk |

Gate 3 is enforced by fresh-session semantics: the unaided condition's DS session and
the aided condition's DS session must be distinct terminals. Claude sessions carry no
cross-session context, so spawning a new session for the second condition is sufficient
provided the gate 2 worktree reset separates the two.

Between condition transitions (aided → unaided or vice versa), the operator MUST
execute `git -C comp/targets/<target>/_repo reset --hard <baseline_commit>` before
dispatching the next condition's DS. This is the harness-enforceable substitute for
provisioning automation until comp-wave-runner covers first-pass setups.
```

**Status:** ready to commit verbatim once scope lands.

---

## Lane A additions (scope-dependent — drafted for A/B; scoped-out under C)

**Proposed placement (A/B only):** new `§2.0 Preconditions` subsection before `§2.1
Target formula`.

### Proposed text (A/B version — Lane A continues)

```markdown
### 2.0 Preconditions (MANDATORY — added 2026-04-22 per .048 integrity finding)

Every dev-4 (or any future dev-N) lane run must satisfy these preconditions at
iteration 0, BEFORE the loop invokes the compiler or consumes any bundle.

**Precondition 1 — Canonical source present.**
`comp/targets/<target>/_repo/` must exist and be checked out at
`task_packet.baseline_commit`. The compiler MUST be invoked against this canonical
source. Representative or temp-tree sources are INVALID for measurement purposes.

**Precondition 2 — Scorer-author role separation.**
The agent that authored the compiler mutation under measurement MUST NOT be the agent
that authored the bundle consumed by the loop. Scorer-author separation is enforced
by MCP attribution: bundle metadata MUST include `scored_by: <serial>` where the serial
differs from the `compiler_sha`'s authoring agent. The loop MUST reject bundles that
violate this invariant.

**Precondition 3 — No self-authored bundles.**
A bundle is "self-authored" if its `evaluation_notes`, `scoring_rubric`, or any
`primary_metric`-contributing field was written by the compiler mutation author. Dev-loop
runs MUST consume only bundles that pass scorer-author separation. Bundle origin is
validated in task packet phase-0 gate; violation aborts the run.

**Precondition 4 — Packet-declared scorer.**
Each task packet MUST declare a scorer in the format:
    scorer:
      serial: <agent_serial>
      mode: human | scorer_agent | independent_judge
      artifact_location: <path>
Absence of this field disqualifies the packet from dev-mode runs.

These preconditions are direct remediations of the `.048` integrity finding
(`comp/results/dev-4/integrity_invalidation.md`). They close the compiler-author-scores-
themselves failure mode at the task-packet schema level rather than as an operator
convention.
```

**Status (A/B version):** ready. **Under scope C,** this section is deleted and
replaced with a one-line note: `§2 removed — dev-4 lane scoped out of Wave 3; see
<successor PRD> for dev-mode rework`.

---

## Integration checklist (execute when scope lands)

1. Integrate §0.5 Seam Integrity (verbatim above)
2. Integrate §0.6 Clean Definition (verbatim above)
3. Integrate §3.8 Preflight Gates (verbatim above)
4. **If A or B:** integrate §2.0 Preconditions (verbatim above); bump PRD version to rev5
5. **If C:** replace §2 with scope-out note; bump to rev5; note supersession
6. Bump change-log section with entry citing `.048` commit `df168552` + `.050` reset `36367765f`
7. Commit under `--author=1.1.0_SA_CTO` with `--only docs/architecture/COMP_LEARNS_WAVE3_V1.md`
8. MCP `2.1.0_SA_COO` with amendment ready + expected TO re-decomposition surface
9. MCP `1.1.0_DS_CompLearns` + `1.4.0_DS_CompLearns` confirming Lane A/Lane B restart preconditions
10. Post to Andrew: amendment committed + decomposition ball with COO

---

## Blockers

**External (waiting on Andrew):**
- A/B/C scope call for Wave 3 amendment final shape
- (Separate track, lower priority) direction on whether to draft COMP_LEARNS path→lane YAML for future owned-paths pre-commit hook

**Internal:** none. All in-lane preparation work that can be done without scope call is drafted above.

---

## Decisions + non-decisions this session

**Decision: draft scaffolding in advance of scope call.** Under /loop COMP_LEARNS while
blocked on an escalation, the productive move is scope-invariant authoring in my lane.
No commits, no dispatch, no prejudice on Andrew's scope call.

**Non-decision: whether to pre-author Lane A preconditions.** Drafted verbatim for A/B;
noted how they would be replaced under C. Under scope C the preconditions aren't
deleted — they'd belong to a successor compiler-infrastructure-hardening PRD. Drafting
them here costs nothing and saves time under any scope.

**Non-decision: whether to draft the path→lane YAML.** Asked Andrew explicitly; no
answer. /loop COMP_LEARNS implies "keep at the project"; the YAML is a workspace-wide
deliverable that crosses my lane into `1.0.0_SA_CTO` territory. Not drafting until
Andrew confirms.

---

## Next steps

1. **[Andrew]** A/B/C scope call
2. **[Self, on Andrew's call]** Execute integration checklist above (single commit, under 30 min)
3. **[Self, in parallel standby]** Monitor inbox-watch for any new DS/COO MCP
4. **[Self, optional if Andrew signals "keep driving"]** Draft COMP_LEARNS path→lane YAML as separate CTO-drafted-infra-config work-product (saved as a draft under `docs/architecture/`, not committed)

---

## Compiler Tools

Read-only session — no `comp-*` invocations required. Edits are to drafting-only PRD text; `comp-build` / `comp-blast` not needed until the amendment actually commits.
