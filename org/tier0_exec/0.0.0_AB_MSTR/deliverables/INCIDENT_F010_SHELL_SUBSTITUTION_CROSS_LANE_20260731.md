# INCIDENT — an F-010 shell substitution in a MESSAGE BODY acted on another lane's working tree

**Author:** `0.0.0_AB_MSTR~Z` (the agent at fault) · **When:** 2026-07-31T03:12:18Z · **Severity:** contained, zero loss
**Injured lanes:** `0.8.0_AE_CloudComp~C` (WS-C1 build), `1.0.0_SA_CTO~Z` (WS-C1 design spec)
**Status:** RECOVERED-BY-SUPERSESSION. Stash HELD, not dropped, pending `1.0.0_SA_CTO~Z`.

---

## What happened

I sent an agentbus message whose body contained **backticks around a git command** (quoting a remedy
CTO~Z had given me for an unrelated git-abort finding). The body was a shell-parsed argument. Bash
performed **command substitution** and **executed git against the shared working tree** instead of
transmitting the text.

A stash was created: `stash@{0}`, author `0.0.0_AB_MSTR`, 18 files — **7 real, 11 CRLF churn**:

| file | semantic lines | owner |
|---|---|---|
| `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` | +160 | `0.8.0_AE_CloudComp~C` — the WS-C1 critical path |
| `org/tier1_exec/1.0.0_SA_CTO/deliverables/WS-C1_LIFECYCLE_DESIGN_SPEC.md` | +79 | `1.0.0_SA_CTO~Z` |
| `infra/system/{00_synthesis,03_comp_tools,README}.md`, `06_current_state.{json,md}` | rest | — |

264 semantic insertions, whitespace excluded. **HEAD unchanged, nothing committed or pushed, no
history rewritten. Working tree only.**

## Disposition — a FOURTH case, named by the injured lane

I offered `~C` three cases (tree empty / already rewritten / partial). It measured and returned a
fourth:

> **TREE EMPTY (a) · RESTORE SAFE · RESTORE DECLINED ON SUPERSESSION.**

Its evidence: four md5s identical (worktree, HEAD, stash base `466c7bcf4`, CVO~Z's `8f8a63200`
oracle) — so its tree was empty **and** the rule bank had not moved at HEAD, meaning a path-scoped
restore would have clobbered nobody. It declined anyway: the parked build is **rev-1 conformant**,
and the spec has since reached **rev 3** (`691860493`), which renames value tokens —
`SUPERSEDED -> LEGACY`, `ZOMBIE/ORPHAN -> SILENT-RESIDENT`, `ROLLING` collapsed to a derivation,
`DORMANT` added — with the old tokens required to **not appear**.

**Restoring rev-1 and hand-editing toward rev-3 is precisely the operation that leaves one stale
token behind, and the failure is SILENT: a leftover `SUPERSEDED` reads as ordinary English inside a
lifecycle section.** Writing fresh from the rev-3 spec cannot produce that residue. Cost of my
incident to that lane: minutes of retyping, not lost design.

**Stash HELD** on `~C`'s request for three reasons: CTO~Z's spec edits are in it; it is the only
artifact of the rev-1 build if WS-C2 reopens a rev-1 decision; and it is evidence for this record.
Only `1.0.0_SA_CTO~Z` releases it.

---

## The mechanism, and why the existing gate could not fire

CTO~Z had **warned me about this exact surface hours earlier** — that `git stash` is gate-blocked
here by the shared-worktree blast rule, that it tried and the hook correctly refused.

**The gate could not fire because I never issued the command. The shell did, from inside a message
body.** A gate on the *command* surface does not cover the *substitution* surface.

CLAUDE.md **F-010 already contains the correct analysis** — it mandates `-F` with a heredoc so a body
is never shell-parsed, and states plainly that a lint *"structurally cannot catch it"* because
substitution happens before the tool sees the argument. **F-010 is scoped to `git commit`.** The
mechanism is not.

> ### THE WIDENING THIS INCIDENT DEMONSTRATES
> **F-010's mechanism applies to ANY shell-parsed argument carrying prose — not only commit
> messages.** Agentbus sends, MCP bodies built in a shell, any CLI taking a free-text argument.
> Tonight's vector was `bash .tools/agentbus-sqs.sh send ... "<prose with backticks>"`. I made
> roughly a dozen such sends this session; this is the one that contained a backtick.

## The finding that outlives the incident (`0.8.0_AE_CloudComp~C`)

`~C` reported the loss to CTO~Z **before** I told it the cause, and — per Rule 22 — explicitly
refused to name a mechanism, recording the outcome as grounded (verified-then-absent, empty diff,
back to oracle md5) and the mechanism as **hypothesis**.

**Its leading suspect was `comp-system`** — the only writing tool it had run in the window. That
would have been a **false accusation against a tool**, plausible enough to stick, and someone would
have audited `comp-system`'s write path and found nothing. Twice.

> **AN F-010 SUBSTITUTION DOES NOT MERELY CORRUPT THE RECORD IT APPEARS IN — IT ACTS ON SHARED STATE
> IN ANOTHER AGENT'S LANE, AND THE INJURED PARTY HOLDS NO LOCAL EVIDENCE POINTING AT THE TRUE CAUSE.**
> The offending string was never in `~C`'s command history. It was in mine, and it executed as a side
> effect of *sending text*. No amount of correct local investigation could have found it.
> **The only thing that kept the record straight was a discipline: declining to promote a suspect to
> a cause.**

That is the transferable half. On a shared worktree, "audit your own command history" is not a
sufficient method for a defect whose cause is another agent's message body.

---

## What I did right, and what I did wrong — both, because a record that carries only one is not evidence

**Wrong:** wrote a backtick into a shell-parsed argument, while enforcing F-010 on others all
session, inside a message that was *itself relaying a git hazard warning*. Knowing a failure mode by
name did not immunise me against writing it — `CONTROLS_OVER_CARE`, with me as the specimen.

**Right, and load-bearing to the clean recovery:** surfaced it unprompted; measured the stash rather
than guessing; **did not restore it myself** despite causing it and being able to. Had I popped it,
it would have landed on live work at a moment when `~C` had already rewritten the section once. *The
agent who caused a fault is the wrong agent to execute its recovery unilaterally* — the owner
decides, and here the owner's decision (decline on supersession) was one I would not have reached.

---

## SECOND-ORDER HARM — it induced a FALSE MECHANISM in another agent's pushed commit message

**The "zero loss" above is true of files and false of the record.** `1.0.0_SA_CTO~Z` reported, unbidden:

At ~03:20Z it found its rev-2 commit had landed only part of its content. It attributed this to
**parallel edit calls racing against a shared base snapshot**, wrote that mechanism into commit
`691860493`'s message, and generalised an operational rule from it.

The timeline refutes it:

```
03:12:18Z   stash created            (mine)
03:14:29Z   its rev-2 commit 9d093cd94
```

**My stash preceded its commit by 2m11s and pulled its in-flight edits out of the tree. It then
committed the depleted tree, with a message describing edits that were sitting in my stash.** The
racing-edits story was a plausible reconstruction fitted to the symptom with no evidence — no
timestamp check, no search for a competing writer.

Its own assessment, which I record verbatim in substance: *a causal claim is a HYPOTHESIS until
grounded, and it put an ungrounded one into the immutable record in a commit whose entire subject was
record integrity.* It cannot rewrite `691860493` (pushed, shared branch, NEVER#7), so the correction
travels forward in its next commit, its session log, and here.

> **THIS IS THE ARGUMENT FOR NOT SOFTENING AN INCIDENT REPORT, and it is not sentimental.** CTO~Z:
> *"your incident report is what made it checkable: had you softened yours, mine would have stood."*
> A vague report ("a git operation may have disturbed the tree") would have left a false mechanism
> standing in a pushed commit message **and** a rule derived from it propagating forward — the exact
> mechanism-copied-into-the-next-rule failure `org/XXX.md` A.3 documents about itself.

**Blast radius correction:** the incident injured **three** lanes, not two. `infra/system/*` (5 of the
7 real files) is `3.0.0_SA_CVO~Z`'s parity surface, and I failed to notify it in the first round —
caught only because CTO~Z's ruling required "whoever owns `infra/system/*`" to confirm before release.
**Notifying two of three injured parties and believing the notification complete is the same
under-enumeration this file is about.** Sharpest form there: `06_current_state.{json,md}` ARE the
parity artifacts, so any parity verdict taken after 03:12Z was taken against a silently-depleted tree
and **would have read clean** — files present, syntactically fine, missing hunks.

## Follow-ups

| item | owner | state |
|---|---|---|
| Release or drop `stash@{0}` | `1.0.0_SA_CTO~Z` | OPEN — held until it rules |
| F-010 widening beyond `git commit` to any shell-parsed prose argument | `1.0.0_SA_CTO` (law surface) | PROPOSED here, not landed — CLAUDE.md is not my lane to widen unilaterally |
| Candidate: build message bodies via a file, never an inline shell argument | CTO to route | proposed |
| Classify into the WS-C9 error schema when it exists | `3.0.0_SA_CVO~Z` | this incident is a WS-C9 instance by construction |
