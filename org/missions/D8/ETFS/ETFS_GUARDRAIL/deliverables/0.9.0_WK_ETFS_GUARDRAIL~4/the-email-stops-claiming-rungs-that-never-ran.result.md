# ETFS_GUARDRAIL.TO-EG-s-30 -- RESULT

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` · **Branch:** `wk-etfs_guardrail-3-30` (cut at `a6cbb6f3c3`)
· **Cell:** `EG-s-30` · **outcome_ref:** FWD-9, FWD-10

`S30-AC1` **PASSES BY OUTPUT** -- rc 0, `arms: 6 of 6 HOLD`, token
`EGS30-EMAIL-TELLS-THE-TRUTH-ON-BOTH-BRANCHES`. Full transcript:
`EG-s-30_S30-AC1_battery_output.txt`. `S30-AC2` is **RECORDED BELOW WITH NO VERDICT** for
`3.0.0_SA_CVO` at L9.

---

## 1. WHAT CHANGED, IN ONE PARAGRAPH

`_build_terminal_email` now takes the month's `coverage_verdict.json` (defaulted, so no caller
broke), reduces its `forcing` block through a TRI-STATE read, and emits a five-line **RUN SHAPE**
block as the FIRST thing in the body, above the count and above the per-date table, with an
explicit value on every branch. The claim sentence that used to say "after every rung ran" now
says what actually happened; the subject's "after remediation" tail is corrected on the same
evidence and gains a `[DRIVEN TEST -- NOT A REAL ALERT]` prefix on a forced run. The organic
branch's subject is byte-identical to today's and every body line today's bytes emit survives
byte-identical and in order.

**THE TWO DEFECTS STAYED APART ALL THE WAY THROUGH, INCLUDING IN THE MUTANT.** Arm (a) measured
them separately (a presence count for the false claim; a 0-of-12 token census with a 5-of-5
positive control for the missing disclosure). The mutant control put the false claim BACK while
leaving the disclosure intact, and the battery failed arm (b) alone while arm (d) kept holding --
which is the evidence that fixing one does not launder the other.

---

## 2. `S30-AC2` -- JUDGMENT, RECORDED, NOT SELF-GRADED

### (i) Could a person reading the forced message still mistake it for an organic one, and what remains of that risk?

**What a reader gets, quoted.** Subject:
`[DRIVEN TEST -- NOT A REAL ALERT] URGENT: ETF month-end 2026-08 -- 1 date(s) unresolved with the repair ladder SKIPPED (--no-ladder)`.
Body line 0, character offset 0:
`RUN SHAPE: DRIVEN TEST RUN -- THIS ALERT WAS MANUFACTURED ON PURPOSE AND IS NOT A REAL COVERAGE EMERGENCY. THE REPAIR LADDER DID NOT RUN.`
The organic message at the same two positions reads an unprefixed `URGENT: ...after remediation`
and `RUN SHAPE: ORGANIC -- nothing was forced and the full repair ladder ran. This is a real
coverage failure.` The two differ in the first token of the subject and the first token of the
body, so a reader who reads NOTHING BUT the preview pane is discriminated.

**What remains, stated rather than dismissed.**

1. **The word `URGENT` survives on a driven run.** It sits *after* the disclosure prefix, so the
   subject reads "not a real alert ... URGENT", but a reader who pattern-matches on `URGENT:` --
   which is what a person trained by five months of real alerts does -- can act before reading
   left-to-right. I did not remove it: the bound is "do not change what the message reports, only
   what it claims", and `URGENT` is a routing signal EG-s-8 chose, not a claim this cell owns.
2. **The disclosure is TEXT, not structure.** A mail client that renders only a plain-text
   preview shows it; one that a reader has configured to hide previews shows only the subject,
   where the marker is 33 characters that a narrow window can clip (see (iii)).
3. **THE DEEPEST RESIDUAL, AND IT IS NOT ABOUT WORDING: the disclosure is only as true as
   `coverage_verdict.json`.** The email reports what the ARTIFACT says, and if a run wrote no
   verdict, or a renderer older than EG-s-25 wrote it, the message falls to `[RUN SHAPE NOT
   STATED]`. That is the honest branch and it never reads as organic -- but it is also the branch
   a reader has the least experience with, and "NOT STATED" is a weaker signal than "DRIVEN".
   A forced run whose verdict write FAILED would present as NOT STATED, not as DRIVEN.
4. **A second reader-class exists and this cell did not serve it: the SNS alert.** `_alert` fires
   on the same refusal branch with the raw `Coverage verdict: {...}` JSON folded in, so the
   forcing record IS present there -- but as unformatted JSON in a 100-character-subject SNS
   message, not as a disclosure. I did not touch it (out of this cell's subject).

### (ii) Does any OTHER sentence assert something a shape-1 run did not do? CENSUSED, not recalled.

**Denominator, by subtraction from the printed line count** rather than by listing what I thought
of: 1 subject + 12 body lines = **13 text units** on a shape-1 run (`--fixture-remove` +
`--no-ladder`, no ask). Subtract 3 blank separators (indices 05, 07, 10), 1 table header (08) and
1 data row (09) -- data, not assertion -- leaving **8 assertion-bearing units**. Each was read
against what a shape-1 run actually does:

| # | unit | asserts | true of a shape-1 run? |
|---|---|---|---|
| 1 | SUBJECT | driven test; N unresolved; ladder skipped via `--no-ladder` | **yes**, except the residual `URGENT` in (i) |
| 2 | `[00]` RUN SHAPE headline | manufactured, not a real emergency, ladder did not run | yes |
| 3 | `[01]` `forced:` | `--fixture-remove <spec>`, N slices dropped IN MEMORY, nothing on S3 changed | yes -- the renderer's `--fixture-remove` drops from the loaded series and touches no key |
| 4 | `[02]` `ladder ran:` | `remediate_month` never called, 0 of rungs 1-3 ran, rung 3 is the sole writer of `coverage_egress_ask.json`, so that artifact is absent by construction | yes -- **with one qualifier, below** |
| 5 | `[03]` `run id:` | the id and its source | yes, and it repeats the record's own `run_id_source` verbatim rather than characterising it. **Honest limit inherited from the producer: this is NOT the SSM `CommandId`** -- the orchestrator holds that and does not pass it to the renderer |
| 6 | `[04]` `read from:` | the object and field the disclosure came from | yes |
| 7 | `[06]` claim sentence | no rung attempted; unresolved as FIRST CLASSIFIED, not after repair | yes |
| 8 | `[11]` signature | nothing | n/a |

**THE ONE QUALIFIER, AND IT IS THE FINDING OF THIS CENSUS.** Unit 4 is literally true and can
still mislead. `EG-s-29` writes a rung-3-EQUIVALENT ask on the ladder-skipped branch, under its
OWN key `coverage_egress_ask_ladder_skipped.json` (`render_month_end.py`
`LADDER_SKIPPED_ASK_BASENAME`, @`a6cbb6f3c3`) -- deliberately not rung 3's key, so that EG-s-26's
"absent by construction" statement stays true. But the orchestrator's `_read_coverage_artifacts`
reads exactly three basenames and that is not one of them, so **on a shape-1 run the equivalent
ask EXISTS on S3 and the EMAIL carries no ask block at all**, while the per-date table's
`provider` column renders `(not stated)`. A reader of unit 4 can reasonably conclude "nothing was
asked"; what is true is "rung 3's document was not written, and a different document was". This
is the same surface `R-EG-7`/`EG-s-28` is already cut on ("the terminal alert names NO provider
in ANY run"), so I name it here rather than filing a duplicate row against a live owner -- and I
did NOT fix it, because adding the equivalent ask would change what the message REPORTS, which
this order's bounds forbid.

**With an ask present (a ladder-RAN run) the denominator is 17 body lines**, adding 3
assertion-bearing units -- the `Egress ask (per-use only -- nothing above has been executed
automatically)` header, the per-ask row, and `Authorization: ...`. All three are EG-s-20's/
EG-sb-7's and are unchanged by this cell; none of them can appear on a shape-1 run today.

### (iii) Does the placement survive the way mail clients truncate?

**Measured, not asserted** (battery arm (e)): headline at body line index **0 of 12**, character
offset **0**; per-date table header at index **8**; **7 lines between them**. So the disclosure
cannot be pushed below the fold by the number of unresolved dates -- the one variable that grows
without bound in this message -- which is the specific failure mode "buried below the per-date
table" names.

**Where it is exposed anyway:**

- **Subject truncation is the real risk and it is the reason the marker is a PREFIX.** Gmail's
  web list truncates the subject to the column width; iOS Mail shows roughly 35-40 characters at
  default text size. `[DRIVEN TEST -- NOT A REAL ALERT] ` is **33 characters**, so it survives a
  35-character clip by 2 characters and is CLIPPED at 30. That is a thin margin and I am naming
  it rather than claiming the placement is safe: a shorter marker (`[TEST] `, 7 characters) would
  survive any clip, at the cost of the words "NOT A REAL ALERT" that carry the meaning.
- **Preview-pane truncation favours the body block.** Every client that shows a snippet shows the
  FIRST line, which is the headline -- and the headline is a complete sentence that ends with
  "IS NOT A REAL COVERAGE EMERGENCY." within its first 128 characters, so a snippet clip at 100
  characters still delivers "DRIVEN TEST RUN -- THIS ALERT WAS MANUFACTURED ON PURPOSE".
- **The labelled fields are indented two spaces and are NOT re-flow-proof.** A client that
  re-wraps plain text at a narrow width will break the long `ladder ran:` value across lines and
  lose the column alignment. The VALUES survive; the table shape does not. That is cosmetic
  here, but it would not be if a later cell made the block machine-parsed.

---

## 3. THE DEPLOY

Entry `20260910T1741Z_etfs-guardrail-eg-s-30-email-run-shape-disclosure_deploy_completion.md`,
**OPENED 17:41:03Z, before the plan (17:42:01Z) and the apply (17:44:50Z)**; **CLOSED
17:51:46Z, before the grading read**; all 5 legs proven.

| | |
|---|---|
| supersede check FIRST | my HEAD bytes (`9337c58c...`, 59,843 B) were NOT the served member (`3266c6cc...`, 48,612 B) -> a FIRST execution, not a rewind |
| pre-state | `CodeSha256 5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw=`, `12:16:53Z`, 16,826 B |
| post-state | `CodeSha256 njvsszkhJI4d+Xj9SOmWZy4Q0NAYKQvHTvBglbd2i5U=`, `17:44:50Z`, 20,596 B; member 59,843 B `9337c58c...` |
| three reads | served == built zip == plan-predicted, all `njvsszkh...` |
| grain deeper than the zip | member BYTE-EQUAL to `git show HEAD:<path>` |
| negative control | `git show a6cbb6f3c3:<path>` retrievable, 48,612 B `3266c6cc...`, does NOT match |
| rollback | that same blob -- CONTENT-RESOLVED against the running bytes, measured at 13:16Z before any apply |
| 0-diff re-plan | rc=0, `No changes. Your infrastructure matches the configuration.` |

**NEVER-9 throughout:** `.tools/terraform.exe` **v1.9.8**, copied into this fresh worktree
because the binary is `.gitignore`d and ABSENT here, and verified before use -- never the PATH
`terraform` (v1.14.5 on this box, which would re-pin remote state), never a bare `terraform
apply`, never `aws lambda update-function-code`.

---

## 4. WHAT I DID NOT DO

- **NO SEND. NO ORCHESTRATOR INVOKE.** `EG-s-21`'s single permitted driven run is **UNSPENT**.
  Measured on two planes with a non-zero control, and bounded by the oracle that is sound for
  the claim -- an ast call-site census showing all 3 `_ses` sites sit in functions reachable only
  from `handler`, and 0 START RequestId over a 6 h window spanning the apply.
- **NO WRITE TO THE RENDERER.** `data/etfs/scripts/presentation/` is `EG-s-29`'s terminal
  surface; I read it and cited it and wrote nothing there.
- **NO CHANGE TO WHAT THE MESSAGE REPORTS** -- the per-date table, the recipients, the routing,
  the envelope resolution and the send path are `EG-s-20`'s and are byte-untouched.
- **NO S3 WRITE OR DELETE, NO IAM, NO SCHEDULE CHANGE. NO PUSH.**

## 5. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W4-S13` | OBSERVATION / INERT | arm (c) and arm (d)+the BOUND are jointly unsatisfiable; I built to the BOUND and printed the literal form as FALSE |
| `W4-S14` | OBSERVATION / **ARMED** (`2.0.0_SA_COO`) | a pre-existing red arm at the branch base: the renderer emits `provider`, the committed S3 fixture does not |
| `W4-S15` | OBSERVATION / INERT | I amended `EG-s-27`'s terminal arm 4, from a line count to an ast reachability census -- strictly stronger |
| `W4-S16` | OBSERVATION / INERT | `ses:GetSendStatistics` re-keys its buckets every call, so a bucket-diff is not a change measurement; and it is account-wide |
