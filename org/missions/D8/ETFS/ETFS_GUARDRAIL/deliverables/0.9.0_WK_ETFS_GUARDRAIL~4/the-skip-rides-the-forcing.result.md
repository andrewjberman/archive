# ETFS_GUARDRAIL.TO-EG-s-27 -- THE LADDER SKIP RIDES THE FORCING: built, proven to have an EFFECT, and NOT APPLIED

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` · **Face:** `676bb96933` · **Branch:** `wk-etfs_guardrail-3-4`
**Outcome:** `S27-AC1` **FAIL** — 5 of 7 arms HOLD; **(e) and (f) BLOCKED by the ordering condition**, which is the branch the face declares. `<status>` NOT flipped.
**Rows:** none filed this turn — the block is the face's own declared path, not a spec-vs-world divergence.

> **NO SEND, NO ORCHESTRATOR INVOKE, NO APPLY, NO S3 WRITE OR DELETE.** `EG-s-21`'s single
> permitted run remains **unspent**.

---

## 1. THE SHAPE I TOOK, AND WHY

**I took the COUPLED shape** — `--no-ladder` is emitted **iff** a validated forcing spec is
present, from a single expression:

```python
fixture = f" --fixture-remove {forcing} --no-ladder" if forcing else ""
```

Your reasoning is the reason, and it is my own `W4-S5` turned around: an independently-settable
switch would be a **new reachable state** letting a caller silence the repair ladder on a **real**
month with **nothing forced and nothing disclosed** — strictly worse than the `month` injection I
fenced four hours earlier, because that one could not silence a repair.

Coupled, the skip:
- **adds no new writer to census** — it rides the forcing property whose writers I already
  censused by subtraction (denominator 6, 4 excluded, 2 invoker-writable, both fenced);
- **inherits every fence the forcing has** — `TEST_MARKER`, `FORCING_KEY` as a top-level non-empty
  `str`, and `FORCING_SPEC_RE`;
- **cannot be reached without also forcing**, and forcing announces itself on the artifact
  (`EG-s-25`'s `forcing` record, `EG-s-26`'s skip record), so the dangerous combination is
  self-disclosing.

I did not take the independent shape, so I did not need to pay its bill.

## 2. ARM (d) — THE ONE THAT EXISTS BECAUSE OF THE EG-s-24 DEFECT — HOLDS

Driven **through this cell's own command**, against the **served** renderer, using the renderer's
own `_parse_fixture_remove` / `_apply_fixture_remove` / `coverage_gate`:

```
FORCED    … --gate --s3-out s3://opal-data-etfs/platinum/reports/ --fixture-remove cottonwood:2026-08-04 --no-ladder
          spec='cottonwood:2026-08-04' no_ladder=True  -> VERDICT=REFUSE  C=1  holes=['2026-08-04']
UNFORCED  … --gate --s3-out s3://opal-data-etfs/platinum/reports/
          spec=''                      no_ladder=False -> VERDICT=PUBLISH C=0  holes=[]
```

Same code, same month, same probe, same served renderer — **only the forcing differs, and it flips
the verdict.** The unforced arm is the arm's own positive control. That is the second half spine
v3.12 names: the seam is now proved to have an **effect**, not merely to deliver its input.

## 3. WHY (e) AND (f) ARE BLOCKED

**`EG-s-26` is not on the served key.** Verified by my own sha256, twice:

| | |
|---|---|
| served renderer now | 66,756 B, sha256 `b08a646d5755f501f10b0b3c8d0512702c20b38e02263dc3b33a2f963d71020f`, `LastModified 05:19:37Z` |
| my own EG-s-25 baseline | **byte-identical** |
| EG-s-26 skip tokens (`ladder_skipped`, `egress_ask_absent`, `rung3`, `rung_3`, `skip_record`) | **0 of 5** |
| EG-s-25 controls (`forcing`, `forced`, `run_id`, `fixture_remove`) | **4 of 4 non-zero** |

The controls are what make the zeros an absence rather than a dead read. So a ladder-skipped run
could not yet record that it skipped, and arm (e) has no object. **I did not apply, and I did not
wait in a loop** — the face's declared branch is STOP and report, and that is what this is.

## 4. THE CRITERIA

### `S27-AC1` -- FAIL (5 of 7 HOLD)

```
$ timeout 600 python org/.../test_egs27_skip_rides_the_forcing.py
arms: 5 of 7 HOLD
  a-absence-reproduced  HOLD   b-scheduled-bit-for-bit  HOLD   c-not-independently-reachable HOLD
  d-forcing-reaches-the-verdict HOLD   e-disclosure-present BLOCKED   f-deploy-real BLOCKED
  g-no-send-no-invoke   HOLD
EGS27-BLOCKED-ORDERING-EG-S-26-NOT-SERVED     rc=2
```

- **(a)** deployed code produces `--no-ladder` in **0 of 10** event shapes, and **0** executable
  string literals contain it (its 1 raw-text hit is a comment — mine, from `W4-S5`).
- **(b)** **5 of 5** marker-free shapes build a command **byte-identical** to the deployed one.
- **(c)** **0 of 27** payloads reach `--no-ladder` without a validated forcing spec — including
  through `month`, which `W4-S5` proved is a writer — and there is exactly **1** executable emitter,
  conditioned on `forcing`.
- **(d)** as above.
- **(g)** **0** START RequestId in my window against **1 of 4** in a positive-control window.

### `S27-AC2` -- RECORDED, judgment, NO VERDICT

- **Which shape and why:** the coupled one, for the reasons in §1. It is the shape that adds no new
  writer and no independently-reachable state.
- **What a caller could still do wrong:** name a partner or date that does not exist (the
  renderer's `_apply_fixture_remove` is a silent no-op, so the run would refuse over *nothing
  removed* — `EG-s-26`'s `removed_slice_count` is what exposes that); force a month whose only
  holes are class D and expect the D to drive the refusal when the forced C is doing the work;
  or read a `--no-ladder` REFUSE as evidence the ladder *tried and failed*, which it did not.
- **Other callers of `_render_command`, censused:** AST walk -> **1** call site, with `forcing`
  defaulted; a pytest arm asserts both.
- **What a driven run under this shape still does NOT exercise — explicitly:** **rung 3, the
  stop-and-ask, and therefore `coverage_egress_ask.json`.** `--no-ladder` skips `remediate_month`
  entirely (`render_month_end.py:1000-1008`), and rung 3 fires only from inside it
  (`remediate.py:283-284`), being the sole writer of that key (`:188-194`). It also skips rung 2's
  re-check, the only thing allowed to declare a day *resolved*. Per your corrected boundary, what
  shape 1 removes is the **co-presence of the three artifacts in one run**, not any mechanism —
  rung 3 itself was exercised by `EG-s-15`'s real September run, whose egress ask sits at 1,017 B,
  `LastModified 01:20:20Z`, beside its two siblings at the same second.

**Vintage:** deployed orchestrator `CodeSha256 rCrGrYPZNKgWQ4uX3NGFGqm7v1s+KcfQlJ7na+soz+g=` /
05:42:07Z; served renderer `b08a646d5755f501…`; all reads 2026-09-10 ~06:4xZ; code `@<this commit>`.

## 5. WHAT I DID NOT DO

No apply, no invoke, no send, no S3 write or delete, no `<status>` flip, no override. **No NEVER-2
entry was opened** — the face requires one before the apply and there was no apply; an entry for a
deploy that never started would put a false event in the change-management record. No edit to
`data/etfs/scripts/presentation/` (`EG-s-26`, `~5`) or `data/etfs/scripts/coverage/` (`EG-s-23`,
`~1`).

**One probe of mine was wrong and I caught it pre-record:** arm (a)'s second conjunct was a
raw-text check that hit my own `W4-S5` **comment** at `:145` and reported the premise broken. It is
now AST-scoped and prints the raw / string-literal / comment split side by side. That is the third
time this shape has bitten me tonight, and it is the reason every census I write now bands its hits.
