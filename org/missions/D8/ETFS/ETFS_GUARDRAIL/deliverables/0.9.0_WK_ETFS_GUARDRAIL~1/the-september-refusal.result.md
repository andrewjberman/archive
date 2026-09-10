# EG-s-15 -- THE SEPTEMBER-TO-DATE REFUSAL: criteria verbatim, with rc and denominator

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` (RE-SEATED; the predecessor session died at ~01:33Z on an API
session limit, not a defect of the work) · **Branch:** `wk-etfs_guardrail-2-1` · **Face:** the RE-CUT
`ETFS_GUARDRAIL.TO-EG-s-15` @`dc99d82c4d` (the ONE re-cut `1.0.0_SA_CTO` authorised at 94877)

## 0. THE HEADLINE

**The deploy is LANDED AND CORRECT. There was no refusal to observe. The run instead proved something
worth more than the pass it replaced.**

September-to-date *is* incomplete, but the gate's refusal axis is the coverage **CLASS**, not the month's
completeness: it refuses on class **C**, and a missing upstream partition inside an OPEN month is class
**D**. `C = 0` for 3 of 3 partners, so the verdict is **PUBLISH** and the refusal branch cannot be entered
by this data. That premise was the issuer's, ruled so, and arm (c) is re-cut to read the producer's own
rule instead of asserting an outcome.

**What the run proved (rows `W1-S25`, `W1-S29`) — FWD-7's terminal send is UNREACHABLE IN PRODUCTION:**
the deployed guard reads a key the renderer never writes.

    DEPLOYED  lambda_function.py:435 @bd0e384890  (zip sha256 dc05ea90c94dc41e..., 28,504 B)
      unresolved_days = (unresolved_doc or {}).get("unresolved") or []

    SERVED    coverage_unresolved.json top-level keys : ['49financial', 'cottonwood']
    FIXTURE   test_terminal_send.py:118 top-level keys: ['unresolved']          -> DISAGREE

Evaluated live against the served document the guard returns `[]` — falsy — so
`_send_terminal_unresolved` is skipped **even on a genuine REFUSE**. Round-1's EG-s-8 proof passed only
because its fixture was built to the docstring's shape. A **second site at `:516`** (the `terminal_qa`
rehearsal) reads the same way, so the send-free rehearsal is blind to it too.

**Nothing was re-fired.** The activation completed at 01:19:02Z→01:20:28Z; both re-runs are reads against
that same run. Andrew's standing constraint (no test mail to aj@) is satisfied here **by construction**.

## 1. CRITERIA — 4 of 4 MECHANICAL PASS BY OUTPUT

| id | status | rc | deciding line |
|---|---|---|---|
| S15-AC1 | **PASS** | 0 | `7 passed in 0.22s` |
| S15-AC2 | **PASS** | 0 | `PLAN-GATE-HELD` (three limbs) |
| S15-AC3 | **PASS** | 0 | `VERDICT: MATCH` |
| S15-AC4 | **PASS** | 0 | `ARMS 9 of 9 PASS` → `EGS15-REFUSAL-LADDER-RAN` |
| S15-AC5 | **RECORDED (judgment)** | n/a | graded by `3.0.0_SA_CVO` at L9 — **no worker verdict** |

### S15-AC1 — PASS
`timeout 120 python -m pytest .../test_terminal_send.py -q` → rc=0, `7 passed in 0.22s`.
**Denominator: 7 of 7**; round-1 count 5, so the bar (`>= round-1 + 2`) is met exactly. Re-run after the
CLOUD merge.

### S15-AC2 — PASS, `PLAN-GATE-HELD`
The transcript **exists** (this worker's own session captured it in this worktree), so
`PLAN-GATE-UNRECORDED` does not apply. Because `.scratch/` is not committed and the pre-apply plan is not
reproducible after the apply, it is preserved whole at `egs15_plan_gate_transcript.md`.

- **(i)** Pre-apply plan, mtime **2026-09-10T01:14:13Z**: action list contains
  `# aws_lambda_function.orchestrator will be updated in-place` with
  `~ source_code_hash "CvFmg9Zm…" -> "M5Dopbky…"`, `# (27 unchanged attributes hidden)`, and
  `Plan: 0 to add, 1 to change, 0 to destroy.` **That is the only resource in the action list** — every
  other resource appears solely as `Refreshing state...`, a read, not a change.
- **(ii)** The apply at **01:16:19Z** (after 01:14:13Z), through `safe-apply.sh` (its own gate banner heads
  the transcript): `aws_lambda_function.orchestrator: Modifications complete after 6s` and
  `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`
- **(iii)** The same targeted plan re-run now with `-detailed-exitcode` → **rc 0**,
  `No changes. Your infrastructure matches the configuration.`

(i) and (iii) now **agree instead of contradicting** — (iii) is the post-state S15-AC3 also requires.

### S15-AC3 — PASS
`VERDICT: MATCH`, rc=0, `SERVED_CODE_SHA256 == BUILT_ZIP_SHA256_B64 == M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80=`.
**Third instrument this session:** the deployed zip fetched from `get-function`'s presigned location hashes
`dc05ea90c94dc41e…`, 28,504 B, **byte-equal** to the worktree file at `bd0e384890` — and equal to the
issuer's independent read. **3 instruments in agreement.**

### S15-AC4 — PASS, 9 of 9 arms
Re-run **once** against the same run. Arms (c), (d), (e) re-cut.

- **(c)** The producer's rule quoted *first*, then the table read against it:
  `classifier.py:146-148 @c866edd324` class **D** = `upstream partition missing (genuinely absent)`;
  `classifier.py:160-163 @c866edd324` class **C** = `upstream present and priced > 0, no slice`;
  `render_month_end.py:957-963 @4b85a9ae68` — `if summary["C"] > 0: any_c = True` then
  `verdict = "REFUSE" if any_c else "PUBLISH"`. Verdict **accepted as given**: `PUBLISH`. Class C across
  **3 of 3** partners = **0**. 2 unresolved dates, **2 of 2** carrying rung 1's verbatim raised error.
  Branch **PUBLISH** → pair read for *that* branch: publish keys `[200, 200]`, **3 of 3** served CSVs carry
  the coverage line.
- **(d)** Branch PUBLISH: `etfs-reports-alerts` publishes in the run window = **0**, beside the **positive
  control** from the 23:14:43Z failed fire's window = **1** over 1 datapoint. A zero with a control is a
  reading.
- **(e)** The **defect proven** (see §0), plus `SES-PLANE-UNREAD` (SendRawEmail 0 across **2 of 2** trails,
  beside a live positive control) and `NO-APPLICATION-LOG-LINE` (**4 of 4** window events
  runtime-generated) — **neither graded**. The ordinary send that *did* fire is cited from the issuer's
  gateway: `Opal ETF Ownership -- Month-End Report (2026-09)`, 2026-09-10T01:21:28Z, to aj@ **and** andrew@.
- **(a)(b)(f)(g)(h)(i)** unchanged and passing: ledger opened before plan and invoke; `START RequestId` 1 of
  1 with scheduler-role AssumeRole 0 of 35; ask names date+provider 1 of 1; egress 0 of 173 attributable in
  a 5,626-event window; run-id in 3 log lines; box `stopped`.

**Every key the run wrote, with its causing rung** (the BOUNDS' served-slice line, re-cut on `W1-S24`):

| key | size | UTC | caused by |
|---|---|---|---|
| `daily/inflection/2026-09-09.json` | 1,209 | 01:20:16Z | **RUNG 1** (re-run the producer) |
| `coverage_{egress_ask,unresolved,verdict}.json` | 1,017 / 1,414 / 2,705 | 01:20:20Z | the gate/ladder |
| `etf_ownership.html` / `.pdf` | 33,793 / 173,126 | 01:20:23Z | the renderer, PUBLISH branch |
| 3 × `opaletfs_*_202609.csv` | 584 / 552 / 552 | 01:20:23Z | the renderer, PUBLISH branch |

`daily/` denominator **273** keys, **1** written in the window. **The worker's own hand wrote 0 of 273
under `daily/` and 0 of 8 under `platinum/reports/2026-09/`.**

### S15-AC5 — RECORDED (judgment), NO VERDICT
Full evidence with vintages is in the instance's `S15-AC5` row: the ladder rung by rung with verbatim
producer errors, why there is no refusal text, which send fired and which could not, the unchanged
scheduled path, and the six things this order could not see.

## 2. ROWS FILED (10): `W1-S20` .. `W1-S29`

| id | class / hazard | disposition by the issuer |
|---|---|---|
| W1-S20 | OBSERVATION / INERT | form only |
| W1-S21 | OBSERVATION / ARMED | **issuer owns it** — a hand-off defect of its own spawn procedure |
| W1-S22 | BLOCKING / ARMED | premise was the issuer's → **arm (c) re-cut** |
| W1-S23 | BLOCKING / ARMED | CTO: a RECORD breach, not a world breach; the September keys **stay** |
| W1-S24 | OBSERVATION / ARMED | **BOUNDS re-cut** — the ladder may write; the worker's hand may not |
| W1-S25 | BLOCKING / ARMED | **arm (e) re-cut to prove it**; repair escalated to the CTO as its own cell |
| W1-S26 | OBSERVATION / ARMED | folded into arm (e) as two printed, ungraded oracles |
| W1-S27 | OBSERVATION / ARMED | escalated as a code cell |
| W1-S28 | OBSERVATION / INERT | **S15-AC2 re-cut** to `PLAN-GATE-HELD` |
| W1-S29 | OBSERVATION / ARMED | **NEW** — the guard is at `:435`, not `:439`; second site at `:516` |

`W1-S29` is a correction to **my own** row `W1-S25`, whose `:439` the re-cut face inherited. Reading the
deployed bytes as arm (e) requires is what surfaced it. The channel is append-only, so the correction is a
new row and `W1-S25` stands as written; the battery prints the discrepancy inline.

Row gate: `1 new row(s) of 54 total checked (53 pre-existing, NOT re-graded)`, rc=0 — the union the issuer
drained is intact, none lost. Corpus baseline clean (4 known, 0 new, 0 resolved).

## 3. THE NEVER-2 LEDGER — CLOSED

Opened 2026-09-10T01:12:30Z, window 4.0h, 8 legs. L1–L3 by the predecessor; **L4–L8 closed from measured
world state**; entry **CLOSED ~01:47Z inside the window**, sentinel removed, all 8 legs proven. The NEVER-2
detail was appended **last**, after the final mutation, per `W1-S16`. Committed at `8f7229e9f2`.

## 4. WHAT I DID NOT DO

Re-fire the invoke or apply anything a second time (the issuer's ruling and Andrew's standing constraint
both forbid it; every re-run here is a read). Change any code — `lambda_function.py` is READ-ONLY and the
`:435`/`:516` repair is the issuer's cell. Delete the September keys or the daily slice. Add any trail,
alarm, monitor, topic, schedule or env var. Send anything. Read any inbox. Edit an existing surprise row.
Re-word a criterion — every divergence went to a row and the issuer re-cut.

## 5. PROOF-OF-SPEC AND STATUS

`proof-of-spec-check ... S15-AC1,S15-AC2,S15-AC3,S15-AC4,S15-AC5` → **`VALID (rc=0)`**,
`surprises-frame: 10 entries; 10 open with a row id; 10 resolve to a channel row`.

**`<status>` FLIPPED to `complete`** — rc 0 **and** every mechanical criterion PASSES by output.

## 6. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` → **empty**: LOCAL, never pushed.
