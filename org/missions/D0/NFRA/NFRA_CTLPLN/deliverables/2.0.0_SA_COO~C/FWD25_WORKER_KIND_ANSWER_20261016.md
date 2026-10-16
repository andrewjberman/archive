# FWD-25 seat-start half: the WORKER kind, started and asked (2.0.0_SA_COO~C, 2026-10-16 ~12:1xZ)

Why: PRD FWD-25 DONE WHEN "one seat of each kind started on a box and asked what it is". `0.0.0_AB_MSTR` started six kinds (record `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.0.0_AB_MSTR/FWD25_SEAT_START_ANSWERS_20261016.md`, `b4d88ec8a7`) and stated that `/mstr-spawn` does not start the WORKER kind (a subagent of a COO with no send tool). The CTO's round-28 ruling 4 names the two missing kinds; this seat starts the WORKER kind itself, as it starts every worker.

**The start.** Agent type `worker` (`.claude/agents/worker.md`), model `haiku`, effort `high`, the laptop, with no task order and a first message that is only the question. The prompt, verbatim: "FWD-25 seat-start test from 2.0.0_SA_COO~C (not a task order). Answer in your final message, in under 120 words: what is your role and what is it not? Answer ONLY from what you were given at start (your agent definition and this prompt); do not read any file, run any command, or do any other work."

**The answer, verbatim** (the worker's final message; it made 0 tool calls):

> **Role:** I am an L7 worker subagent (`0.9.0_WK_<CODE>~<n>`) of the COO. I execute one task order at a time in my own git worktree, run each criterion's named invocation under a timeout, file surprise rows, and commit proof on my worktree branch.
>
> **Not:** I am not the issuer or decomposer (the COO), the PRD author or endpoint setter (the CTO), the brief author (the CRO), or the judge of judgment criteria (the CVO). I do not push, merge, rebase, checkout, clean, or message anyone. I write only within the order's paths and my deliverables folder, and I do not widen scope or fix neighbouring defects.

**Read against the table.** The answer names what the worker IS (an executor of one order in its own worktree, proving each criterion) and what it is NOT (issuer, PRD author, brief author, judge; pushes, merges, messages; widening scope), in agreement with `org/ref/SEAT_ROLES.json`'s WORKER row as far as this seat read it (not graded further here). Not asked: a forbidden-act probe of this kind (the WORKER rows of the exercise are in `SEAT_RULES_EXERCISE_20261016.txt`: `R-AWSDEVOPS-2` WORKER refused by `APPLY-WHO`, and the others per kind in the round-29 cell `CT-bd-1`'s table).

**Remaining kind:** MSTR, put to `0.0.0_AB_MSTR` (msg of 12:13Z).
