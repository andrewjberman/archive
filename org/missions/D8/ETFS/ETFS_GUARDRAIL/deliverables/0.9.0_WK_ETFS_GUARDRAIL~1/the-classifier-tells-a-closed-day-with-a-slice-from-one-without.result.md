# EG-s-22 -- THE CLASSIFIER TELLS A CLOSED DAY WITH A SLICE FROM ONE WITHOUT

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Branch:** `wk-etfs_guardrail-2-1` · **Face:**
`ETFS_GUARDRAIL.TO-EG-s-22` @`eab3712b31` · **Descends from** my own row `W1-S31`, split by
`1.0.0_SA_CTO` at 94947

## 0. THE HEADLINE

**S22-AC1 PASSES BY OUTPUT — 7 of 7 arms, `EGS22-CLASSIFIER-DISCRIMINATES`, rc=0.** The classifier can now
say the thing FWD-4 exists to protect.

**The defect reproduced first, on the producer's own bytes, before any edit** (arm (a)). Against the
pre-change classifier pinned at `c866edd324`, a closed day carrying a real 1,209-byte slice and a closed
day carrying nothing both returned:

    {"class": "A", "probe": null, "reason": "market closed (not a trading day)"}

Byte-identical, `0` keys naming the slice. The premise held, so the cell proceeded.

**⛔ The `complete` flip is BLOCKED, and not by this work.** The face carries **0** `<criterion>` tags and
**no `<expected_criteria>` element**, so `proof-of-spec-check`'s alignment limb cannot reach cell `EG-s-22`
from any criterion and returns INVALID. That is a cut defect in the issuance half — filed as `W1-S32`, and
the issuer's to repair. I did not edit the face to make my own proof validate.

## 1. CRITERIA

| id | status | rc | deciding line |
|---|---|---|---|
| S22-AC1 | **PASS by output** | 0 | `ARMS 7 of 7 PASS` → `EGS22-CLASSIFIER-DISCRIMINATES` |
| S22-AC2 | **RECORDED (judgment)** | n/a | graded at L9 by `3.0.0_SA_CVO` — **not self-graded** |

`timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs22_classifier_discriminates.py`

- **(a) PASS** — defect reproduced on the pre-change classifier (loaded from git, not described) using the
  slice **fetched live** this run: 1,209 B, `sha256 09ca15d4…`, 4 priced rows, `source_as_of 2026-09-07`.
- **(b) PASS** — post-change the two records are **textually unequal**: `slice_on_closed_day` `True` vs
  `False`.
- **(c) PASS** — **6 of 6** genuinely-empty closed days across **3 of 3** partners still read class `A`,
  keep the **original reason string verbatim**, and sit in no partner's holes.
- **(d) PASS** — suite by its own path: **pre** rc=0 8 passed 0 failed; **post** rc=0 10 passed 0 failed.
  No regression; `+2` are permanent regression arms I added.
- **(e) PASS** — **0 counts moved** across 3 partners; **9 of 27** partner-day records changed, **all class
  A**.
- **(f) PASS** — **`DEPLOYED != BUILT`** (the expected answer; this cell deploys nothing).
- **(g) PASS** — **0** SES clients, **0** Lambda invokes; 6 AWS CLI calls, all `s3api`.

## 2. THE SHAPE, AND WHY — a FIELD, not a class value

`slice_on_closed_day` (bool) on the class-A record. **I did not take this on cost.** The face said the
field is cheaper; the affirmative reason is rule 24:

- **(iii) intent coherence** — the class axis answers *"what is this day's coverage state, and is it a
  hole"*. A closed day is class A on that axis whether or not an artifact turned up. Whether one *appeared*
  is an orthogonal fact about a different actor.
- **(iv) state coherence** — the remedy for a closed-day-carrying-a-slice is the **producer** (row `S20`)
  and moves no other class value; fixing a class-C hole moves nothing here. Different remedies → different
  axes → a field beside the class, not a member of it.

**No four-postulate record and no token census are owed**, because no value joined `_CLASS_NAMES` — it
remains the six-member tuple.

**The arithmetic trap the face named does not fire, and arm (e) proves it rather than asserting it:**
`summarize()` computes `trading_days = COVERED+B+C+D+UNKNOWN` and `holes = C+UNKNOWN+D`, with class A in
neither. Both tables are identical on both sides:

| partner | A | COVERED | B | C | D | UNKNOWN | trading_days | holes |
|---|---|---|---|---|---|---|---|---|
| 49financial | 3 | 5 | 0 | 0 | 0 | 1 | 6 | 1 |
| cottonwood | 3 | 5 | 0 | 0 | 0 | 1 | 6 | 1 |
| inflection | 3 | 6 | 0 | 0 | 0 | 0 | 6 | 0 |

The 9 changed records are the 3 non-trading days × 3 partners — `slice_on_closed_day=True` for
inflection's 09-05/06/07, `False` for the other six.

## 3. THE DEPLOY GAP, AS A NUMBER (arm f)

    DEPLOYED  s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/classifier.py
              10,157 B   sha256 23c30889af9e6408ddccdd541eb0e895540165012e3fd7eb0baff2228082fdae
    BUILT     data/etfs/scripts/coverage/classifier.py (the bytes this cell commits)
              12,226 B   sha256 b2ab67fd35362249ae072803b2a6107af1daac483a985d276005ec7cf9736cc2
    DEPLOYED != BUILT          CRLF in each: 0 and 0 -- not an eol artifact

**Corroboration:** the deployed bytes hash **equal to the pre-change blob** at `c866edd324` — the box is
reading exactly the un-fixed classifier. **The served verdict object cannot discriminate a closed day
carrying a slice from one carrying nothing until someone deploys these bytes.** This cell deploys nothing;
the deploy is a separate act with a separate owner.

## 4. WHAT THIS DOES NOT REPAIR

It does **not** stop `inflection`'s producer writing priced values onto days the market was shut.
`daily/inflection/2026-09-07.json` still holds 4 priced rows with `source_as_of 2026-09-07`, and 09-05 and
09-06 carry the same carried-forward value-sha. That producer is **PRD v0.6 row `S20`**, ruled outside this
project and leaving as a brief to `4.0.0_SA_CRO`. **Detection, not prevention** — and detection was the
half that was ours.

## 5. TWO PERMANENT GUARDS ADDED

The defect existed *because nothing covered it*, and a one-shot battery does not guard the next change. So
the estate's own suite gained
`test_closed_day_carrying_a_slice_is_distinguishable_from_one_carrying_nothing` and
`test_slice_on_a_closed_day_moves_no_sum`. **They are not constants:** both assert `with_slice != without`,
which arm (a) measured byte-identical on the pre-change code — so both would **fail** against the code as
it stood.

## 6. ROW FILED (1)

| id | class / hazard | one line |
|---|---|---|
| W1-S32 | **BLOCKING** / INERT | the face carries 0 `<criterion>` tags and no `<expected_criteria>`, so the alignment limb cannot reach `EG-s-22` and the instance cannot validate — the flip is blocked by the issuance half, not by the work |

## 7. WHAT I DID NOT DO

Touch the producer (BOUNDS, row `S20`). Deploy anything — no `s3 cp`, no Terraform, no Lambda update.
Construct any SES client or invoke any Lambda, **including a real probe** in arm (e) (`probe=None` on both
sides keeps the comparison sound while invoking nothing). Write to S3. Add a class value. **Edit the face's
acceptance markup to make my own proof validate** — that is re-cutting the issuance half, which is the
issuer's act.

## 8. A CAVEAT OF MY OWN

Arm (e) runs `probe=None`, so its tables read `UNKNOWN=1` where the **served** 2026-09 verdict reads `D=1`
— the served verdict was produced *with* a probe. The before/after comparison is sound (same recomputation,
same probe setting, both sides), but it is **not** a reproduction of the served artifact's counts, and I do
not claim it is.

Separately: arm (d) first read `0 passed` while rc was 0 and the suite was green — `pytest -q` colourises
its summary, so the count is not a bare whitespace token. My parser bug, not the world; fixed by stripping
ANSI and matching the count against the word it labels.

## 9. PROOF-OF-SPEC AND STATUS

`python .tools/proof-of-spec-check.py <instance> S22-AC1,S22-AC2` → **INVALID (rc=1)**, on exactly one
remaining violation: `alignment: declared cell 'EG-s-22' is named in the TO's <owned_cells> but NO
criterion references it`. **`<status>` NOT flipped** — the face requires the instance to validate first.

## 10. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` → **empty**: LOCAL, never pushed.
