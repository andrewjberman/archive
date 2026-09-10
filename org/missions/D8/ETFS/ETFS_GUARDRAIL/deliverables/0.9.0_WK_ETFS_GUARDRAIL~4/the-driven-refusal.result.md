# ETFS_GUARDRAIL.TO-EG-s-21 -- THE DRIVEN REFUSAL: STILL BLOCKED, AND STILL NOT INVOKED

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` · **Branch:** `wk-etfs_guardrail-3-4`
**Outcome:** `S21-AC1` **FAIL**. `<status>` NOT flipped. **The single permitted run is UNSPENT.**
**Row:** `ETFS_GUARDRAIL-W4-S6` -- BLOCKING / ARMED.

> **NOTHING WAS INVOKED.** No orchestrator invoke, no producer invoke, no SES send, no S3 write,
> no S3 delete. Every AWS call is a read; the renderer was executed only in-process with
> `remediate` and `s3` replaced by stubs.

---

## 1. THE PRECONDITION HOLDS -- and it needed re-taking, because the bytes changed

The coordinator was right that my 04:35Z read was stale: **`EG-s-24` redeployed the function at
05:42:07Z**, so that read was about different bytes.

| | |
|---|---|
| read at | **2026-09-10T06:09:59Z** (and again in the battery) |
| served `CodeSha256` | `rCrGrYPZNKgWQ4uX3NGFGqm7v1s+KcfQlJ7na+soz+g=` |
| zip member | 47,075 B, sha256 `8d8cb2c23d7c00d943a985d381e45b96315f7dcf6047fe1bc3cc2234854d801f` |
| result | **aj@opalinvest.com in 0 of 18** resolved test-invocation lists; scheduled path still `['aj@opalinvest.com','andrew@opalinvest.com']` |

This also serves as a regression check on my own `EG-s-24` change: the recipient path survived it.

**So the block is not the recipient bound. That one passes.**

## 2. THE FORCING IS DEFEATED BY THE LADDER

`--fixture-remove` mutates the in-memory series that `coverage_gate` uses for its **first**
classify. With `ladder=True` -- the only path the orchestrator's fixed `--gate` command takes --
the gate then **re-classifies from real current S3**:

```
render_month_end.py:991   classes = classifier.classify_month(p, month, series=series, probe=probe)
render_month_end.py:999   classes = classifier.classify_month(p, month, s3=s3, probe=probe)
                          # "re-classify from REAL current S3 state, never the in-memory series"
```

`_apply_fixture_remove` call sites on the served renderer: **3** (`:441` def, `:455` HTML path,
`:1116` in `main` before the gate) -- **none inside `coverage_gate`**, which receives
`fixture_remove` only to *record* it in the `forcing` field.

**Measured hermetically on the served bytes** (66,756 B, sha256 `b08a646d5755f501…`), identical
fixture / month / probe, the only difference being the ladder:

| | verdict | C | holes | ladder asked to fix |
|---|---|---|---|---|
| `ladder=False` | **REFUSE** | 1 | `['2026-08-04']` | *skipped* |
| `ladder=True` | **PUBLISH** | 0 | `[]` | `('cottonwood', ['2026-08-04'])` |

And `--no-ladder` is **not threaded** -- the deployed command a forced invoke would send is
`… --month 2026-08 --pdf --gate --s3-out … --fixture-remove cottonwood:2026-08-04`, with no way to
select the only mode in which the forcing works.

**The second harm is worse than the first.** On the ladder path the first classify *does* yield C,
so rung 1 invokes the producer for that date -- a real invoke that would **rewrite a served
`daily/<partner>/<date>.json` slice**. That is exactly the unintended served write round 1 rowed as
`W1-S24`.

**And there is no organic C to fall back on:** 2026-08 reads PUBLISH, holes 0, C = 0 of 3 partners
(21 of 21 trading days covered); 2026-09 reads PUBLISH, holes 2, C = 0 of 3.

So a driven run today would **publish rather than refuse, rewrite a served daily slice, and consume
the single permitted act** -- proving nothing about FWD-9 or FWD-10.

## 3. WHY MY OWN `EG-s-24` DID NOT CATCH THIS

`EG-s-24`'s bar was that the forcing spec **reaches** the classifier and that the scheduled path
cannot reach it. Both are true and remain true -- the spec does reach the renderer's real code path
and is applied at `:1116`. What no arm asked was whether reaching the classifier **changes the
verdict**, which is a property of the gate's control flow, not of the seam.

**A seam proved to deliver its input is not a seam proved to have an effect.** That is mine, and it
is the same family as `W4-S4` and `W4-S5`: I keep proving the thing I built rather than the property
it was built to establish.

## 4. WHAT A RE-CUT NEEDS -- two shapes, different fidelity, both outside this order

1. **Thread `--no-ladder` beside the forcing** in `_render_command` (one line, `EG-s-24`'s file,
   already deployed and out of this order's NO-CODE-CHANGE bound). Yields a genuine class-C REFUSE
   -- measured above -- but the ladder never runs, so `coverage_unresolved.json` rows read
   `"ladder skipped (--no-ladder)"` with rungs all zero, and arm (d), which wants **the ladder's
   outputs** on the refusal branch, gets a degenerate answer.
2. **Apply the fixture to the re-classify** inside `coverage_gate` (renderer, `EG-s-25`'s surface).
   The ladder runs for real, rung 1 fires, and the re-classify still sees the date removed, so the
   verdict is REFUSE **with real ladder output** -- the faithful analogue of the organic case, at
   the cost of a renderer change and a forced date unresolvable by construction.

I did not choose between them: `EG-s-21` binds **NO CODE CHANGE** and both live outside its grant.

## 5. THE CRITERIA

### `S21-AC1` -- FAIL

```
$ timeout 900 python org/.../test_egs21_driven_refusal.py
ARM (a) PRECONDITION : HOLDS -- 0 of 18 reach aj@
ARMS (c)-(g)         : NOT REACHABLE -- no refusal can be produced.
    BLOCKING: the forcing does not change the verdict on the ladder path
    BLOCKING: --no-ladder is not reachable from any event
NOTHING WAS INVOKED. NO SEND. NO S3 WRITE OR DELETE. EG-s-21's ONE RUN IS UNSPENT.
EGS21-BLOCKED-FORCING-DEFEATED-BY-LADDER      rc=2
```

Expected `EGS21-REFUSAL-DRIVEN-AND-SENT`; no match, so **FAIL**. The battery has no branch that can
print the success token.

### `S21-AC2` -- RECORDED, judgment, NO VERDICT

Three of the four limbs still have no object, because no refusal exists. What is recordable:

- **The disclosure limb is now ANSWERED, and it answers well.** `EG-s-25` landed and I exercised it:
  every `coverage_gate` return now carries
  `{"forced": true, "mechanism": "--fixture-remove", "fixture_remove_spec": "cottonwood:2026-08-04",
  "removed_slice_count": 1, "run_id": …, "run_id_source": …, "disclosure_version": "1"}`.
  It is written on **both** branches -- my `ladder=True` run PUBLISHED and still recorded
  `forced: true`, which is the honest and useful direction: a forced run that fails to force still
  says it was forced.
- **Faithfulness of the analogue, sharpened.** Shape 1 (`--no-ladder`) is *not* a faithful analogue:
  it skips the very rungs FWD-9's refusal is supposed to have exhausted. Shape 2 is faithful. The
  choice between them is a fidelity decision, not a convenience one, and it belongs to the cut.
- **Emission vs delivery:** unchanged. The `MessageId` line at the terminal send is an emission
  oracle only, and nothing here moves it.

**Vintage:** orchestrator `LastModified 2026-09-10T05:42:07Z`, member `8d8cb2c23d7c00d9…`; served
renderer `b08a646d5755f501…`; served verdicts read 2026-09-10 ~06:1xZ; code `@c1e2d3acd9`.

## 6. WHAT I DID NOT DO

No invoke of any kind, no send, no S3 write or delete, no code change, no override, no `<status>`
flip. No NEVER-2 entry was opened -- the face requires one *before the act*, and there was no act;
an entry for a run that never happened would put a false event in the change-management record.
