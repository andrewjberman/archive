# ETFS_GUARDRAIL.TO-EG-s-27 -- THE LADDER SKIP RIDES THE FORCING

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~4` (L7 of `2.0.0_SA_COO`, round 3, cell `EG-s-27`)
**Branch:** `wk-etfs_guardrail-3-4` -- **LOCAL, never pushed**
**Face vintage:** the CORRECTED text at `d3a33a1189`, merged into this branch at `06925f8a6f`
**Deploy:** `org/critical_paths/change_management/20260910T1215Z_etfs-guardrail-eg-s-27-ladder-skip-rides-forcing_deploy_completion.md` -- **CLOSED, all 5 legs proven**

---

## 0. WHAT THIS SESSION IS, BECAUSE THE RECORD SHOULD NOT IMPLY ONE CONTINUOUS RUN

This is a **re-seat after a device crash**. My predecessor on this slot died at
`2026-09-10T06:43:35Z` when the device rebooted twice. It had already committed the CODE
(`e94ce02a92`) and left four deliverables untracked in the worktree, with `S27-AC1` recorded
**FAIL -- ordering-blocked**: `EG-s-26`'s renderer was not yet on the served key, and the face
forbids applying until it is.

**I did not trust any of that.** I committed the four artifacts unaltered first
(`d8b69b888c`) so the pre-correction text is attributable to its author, merged `CLOUD`
(`06925f8a6f`) to bring in the face correction, and then **re-measured every claim myself**.
The battery output file on disk was a text file a dead session wrote, not a run I observed;
I re-ran the invocation `S27-AC1` names and scored on its own output.

**The world had moved while the slot was dead.** `EG-s-26`'s renderer IS now served, so the
ordering condition is satisfied and the apply this cell was blocked on is now done.

---

## 1. THE SHAPE: COUPLED

```python
fixture = f" --fixture-remove {forcing} --no-ladder" if forcing else ""
```

`--no-ladder` is emitted **iff** a validated forcing spec is present, from a **single
expression**, and no event key can set it alone. The issuer offered this as a preference with
its reasoning rather than a prescription, and I took it. The reason is this slot's own row
`W4-S5` turned around: a second **independently-settable** switch on a served producer would be
a NEW REACHABLE STATE *and* a new writer to census, and it would let a caller silence the repair
ladder on a REAL month with nothing forced and nothing disclosed -- strictly worse than the
`month` injection `W4-S5` fenced, because that one could not silence a repair.

Coupled, the skip **cannot be reached without also forcing**, and forcing announces itself on
the artifact through `EG-s-25`'s and `EG-s-26`'s records. The dangerous combination is
self-disclosing. Because I took the coupled shape, the independent shape's bill (a full writer
census by subtraction on a NEW property, an adversarial arm, and the new state named in the
sign-off) is not owed on the *new property* -- **but I paid the writer census anyway on the
property that already has two writers**, because `W4-S5` proved it does. See §3.

---

## 2. WHY THE SKIP IS NEEDED AT ALL

With the ladder ON, `coverage_gate` **re-classifies from real S3** at
`render_month_end.py:999` and the in-memory forced hole is discarded, so a forced run returns
`COVERED` and the verdict is `PUBLISH`. **The forcing reached the classifier and never reached
the verdict.** That is what `EG-s-24` proved only half of, and it is why arm (d) exists.

With the ladder skipped, the first classify's result stands, the forced hole is class C, and
`REFUSE` is read from that.

---

## 3. `S27-AC1` -- SEVEN OF SEVEN ARMS HOLD

**Invocation:** `timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs27_skip_rides_the_forcing.py`
**Output:** `arms: 7 of 7 HOLD`, then `EGS27-SKIP-RIDES-FORCING-SCHEDULE-CLEAN`, **rc=0**.
Full verbatim transcript: `EG-s-27_S27-AC1_battery_output.txt` (206 lines).

**THE GRAIN MOVED SINCE THE PRE-CRASH RUN, AND THAT IS THE HEADLINE.** My predecessor's arms
spoke about the BUILD INPUT, because the apply was blocked. **Every arm now speaks about SERVED
BYTES**: the "after" is the zip member fetched from the function's own presigned
`Code.Location`, and the "before" is `git show ee7c70113f:<path>` -- which is not merely an
ancestor but is **content-resolved byte-equal** (47,075 B, `8d8cb2c23d7c00d9...`) to the member
the function served until 12:16:53Z, a sha256 I measured on the live function *before* applying.
Rule 22a: resolve a pin by CONTENT, never by `merge-base --is-ancestor`.

| arm | shape | result |
|---|---|---|
| (a) absence reproduces | premise check | **HOLD** -- 10 of 10 event shapes produce NO `--no-ladder` on the code that WAS RUNNING; the token sits in **0** executable string literals there (raw text 1 / literal 0 / **comment 1**) |
| (b) scheduled path unchanged | **INVARIANCE** | **HOLD** -- 5 of 5 marker-free shapes build a command **byte-identical** to the pre-change one |
| (c) skip not independently reachable | **CENSUS** | **HOLD** -- **0 of 20** adversarial payloads reach `--no-ladder` without a validated spec; **1 of 1** executable emitter, conditioned on `forcing` |
| (d) forcing reaches the verdict | **DIFFERENCE CONTROL** | **HOLD** -- ENGAGED `REFUSE` C=1; SAME run DISENGAGED `PUBLISH` C=0 |
| (e) disclosure present | single state + its own difference control | **HOLD** -- 2 of 2 forcing fields, 4 of 4 skip fields, in ONE object |
| (f) deploy real | **CENSUS** + negative control | **HOLD** -- 3 of 3 reads equal; member == `HEAD` blob; pre-fix blob does NOT match |
| (g) no send, no invoke | **CENSUS** + positive control | **HOLD** -- 0 START of 0 events, against 1 START of 4 in the control |

### Arm (d) is a DIFFERENCE control, and I corrected the word

The face at `d3a33a1189` corrected this and my predecessor's text had it wrong in three places
(the battery's printed prose, the commit message, the old proof instance). **Spine v3.13
qualifier 1: a POSITIVE control bounds UNDER-FIRING only** -- it shows the instrument *can*
fire -- **and never shows what CHANGES when the control is engaged, so it does not discharge
v3.12.** What the battery prints is the SAME run (same served orchestrator, same served
renderer, same month, same probe, same S3 stub) with the forcing engaged and disengaged, and
**the verdict moves between them**. The mechanism my predecessor built was right; the word was
wrong, and I fixed the word rather than let it read as conformance the arm had not earned.

```
ENGAGED    render_month_end.py --month 2026-08 --pdf --gate --s3-out s3://opal-data-etfs/platinum/reports/ --fixture-remove cottonwood:2026-08-04 --no-ladder
           spec='cottonwood:2026-08-04' no_ladder=True  -> VERDICT=REFUSE  C=1  holes=['2026-08-04']
DISENGAGED render_month_end.py --month 2026-08 --pdf --gate --s3-out s3://opal-data-etfs/platinum/reports/
           spec=''                     no_ladder=False -> VERDICT=PUBLISH C=0  holes=[]
```

### Arm (e): the ordering held, and the disclosure discriminates

`EG-s-26`'s renderer verified **by my own sha256**, not carried from any report: VersionId
`TkhI7NPt_hpJUaXYAlBnjZggJQDz.wBG`, 69,879 B, `LastModified 2026-09-10T06:40:10Z`, sha256
`9b9cdd9c39cbe92bbcb94c9550eebcf924b0f18744b81c61c3f66cfe75237a76`. **Negative control:** the
pre-`EG-s-26` baseline `b08a646d5755f501...` (66,756 B) does NOT match, so this is a moved
artifact and not a re-read of the old one.

The forced run's `coverage_verdict.json["forcing"]` carries **both records in one object**:

```json
{ "forced": true, "mechanism": "--fixture-remove",
  "fixture_remove_spec": "cottonwood:2026-08-04",
  "fixture_remove": {"cottonwood": ["2026-08-04"]}, "removed_slice_count": 1,
  "ladder_ran": false, "ladder_skip_mechanism": "--no-ladder",
  "rung3_stop_and_ask_reachable": false, "coverage_egress_ask_possible": false,
  "skip_note": "--no-ladder skips remediate_month entirely, so rungs 1-3 never run; rung 3 is
   the stop-and-ask and the SOLE writer of coverage_egress_ask.json, so that artifact is
   ABSENT BY CONSTRUCTION for this run -- not absent because nothing needed asking",
  "disclosure_version": "2" }
```

**I gave the disclosure its own difference control**, because a field that reads the same on
both branches discloses nothing: the UNFORCED run's record reads `forced:false`,
`ladder_ran:true`, `ladder_skip_mechanism:"none"`, `rung3_stop_and_ask_reachable:true`. The
record MOVES.

### A number my predecessor got wrong, corrected rather than carried

The old instance recorded arm (c) as **"0 of 27"**. That was arithmetic: it counted
`5 scheduled + 12 smuggles + 3 month-injections` and then added the scheduled set a second
time. The true denominator is **20**, and the battery now prints the breakdown beside it so the
sum is checkable on its face. The claim is unaffected -- 0 reached either way -- but a
denominator that cannot be re-derived from its own parts is not a denominator.

---

## 4. `S27-AC2` -- JUDGMENT, RECORDED FOR `3.0.0_SA_CVO` AT L9. NO VERDICT.

**(1) WHICH SHAPE AND WHY.** The COUPLED one; §1 above. One expression, no new writer, no
independently reachable state. I did not take the independent shape, so its bill is not owed;
I state the choice here so it is auditable rather than assumed.

**(2) WHAT A CALLER COULD STILL DO WRONG.** Four, named:
- **Name a partner or date that does not exist.** The renderer's `_apply_fixture_remove` is a
  silent no-op, so the run would REFUSE over nothing actually removed. `EG-s-26`'s
  `removed_slice_count` is exactly what exposes this -- it reads `1` on my run, and would read
  `0` on that mistake.
- **Force a month whose other holes are class D** and misread the D as driving the refusal when
  the forced C is doing the work.
- **Read a `--no-ladder` REFUSE as evidence the ladder TRIED AND FAILED.** It did not run at all.
- **Treat a driven REFUSE as a rehearsal of the organic terminal path.** It is not; see (4).

**(3) OTHER CALLERS OF `_render_command`, CENSUSED WITH A DENOMINATOR, NOT RECALLED.** On the
SERVED module (`git show HEAD:<path>`, byte-equal to the served zip member): an AST walk over
**237 `ast.Call` nodes** finds **1 definition** and **1 call site**, at `:682`
(`Parameters={"commands": _render_command(month, _forcing_spec(event))}`), with `forcing`
DEFAULTED so no caller is changed by its existence. Raw-text hits across the module: **3**,
banded **1 COMMENT (`:132`) / 1 DEF (`:424`) / 1 CODE (`:682`)** -- the band is what stops the
comment inflating the count. Repo-wide across `infra/`: **18 hits across 2 files**, of which
16 are the test module's own harness calls and 2 are the def+call above; **0 production callers
outside this module**. A pytest arm
(`test_render_command_has_exactly_one_caller_and_a_defaulted_parameter`) asserts both.
⚠ **INSTRUMENT NOTE:** `comp-find "_render_command" --scope all` returned
`0 hit(s) across 0 file(s) scanned` from this linked worktree. Per CLAUDE.md that is the
**OUT-OF-CORPUS** signal, not an absence -- the discriminator is the **0 scanned** count -- so I
did not convert it into a zero and re-took the census with the native (non-gated) instrument.

**(4) WHAT A DRIVEN RUN UNDER THIS SHAPE STILL DOES NOT EXERCISE, NAMED EXPLICITLY.**
**RUNG 3, THE STOP-AND-ASK, AND THEREFORE `coverage_egress_ask.json`.** `--no-ladder` bypasses
`remediate_month` entirely (`render_month_end.py:1030-1051`), so rungs 1-3 never run; **rung 3
is the SOLE writer of `coverage_egress_ask.json`**, so that artifact is **absent by
construction** on such a run rather than absent because nothing needed asking. It also skips
**rung 2's re-check**, the only thing allowed to declare a day `resolved`, and **rung 1's
producer re-invokes** (zero of them fire).

Per the issuer's corrected boundary, which I accept: what shape 1 removes is the **CO-PRESENCE
of the three artifacts in one run**, not any mechanism. Rung 3 itself was exercised by
`EG-s-15`'s real September run, whose egress ask sits at 1,017 B, `LastModified 01:20:20Z`,
beside its two siblings at the same second. So a driven refusal under this shape proves the
VERDICT path and does **not** rehearse the egress-ask path.

**VINTAGE.** Served orchestrator `CodeSha256 5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw=` at
`2026-09-10T12:16:53Z`; served renderer `9b9cdd9c39cbe92b...`; all reads 2026-09-10 12:0x-12:2xZ.

---

## 5. THE DEPLOY

Entry **OPENED 12:15Z, BEFORE the apply**; **CLOSED before the grading read**, all 5 legs proven.

| | |
|---|---|
| pre-state | `CodeSha256 rCrGrYPZNKgWQ4uX3NGFGqm7v1s+KcfQlJ7na+soz+g=`, `05:42:07Z`, 16,210 B; member 47,075 B `8d8cb2c23d7c00d9...` |
| post-state | `CodeSha256 5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw=`, `12:16:53Z`, 16,826 B; member 48,612 B `3266c6cced4940f0...` |
| plan predicted | `5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw=` -- **all three reads equal** |
| rollback | `git show ee7c70113f:<path>`, **content-resolved byte-equal to the running bytes**, re-applied by the same targeted `safe-apply` |
| 0-diff re-plan | rc=0, `No changes. Your infrastructure matches the configuration.` |

**I MEASURED FOR A REWIND BEFORE PLANNING ANYTHING.** The seating instruction was explicit that
a re-execute of an overtaken promote is a REWIND (NEVER-2). I read the orchestrator's own
served `CodeSha256` first: it was still `rCrGrY...` at `05:42:07Z` with the member **not**
equal to the build input and `--no-ladder` appearing once (a comment) rather than three times.
**My deploy had not landed**, so the apply was a first execution and not a repeat.

**NEVER-WIDEN SIGN-OFF** (full text in the entry): the act writes exactly ONE thing, the Lambda
function code, by a TARGETED plan on that one resource address -- no S3 key, no IAM, no
schedule, no topic, no environment variable, no image tag. **No run is fired by this order**,
so no served key moves on either branch of anything a later run could decide. **The new
reachable state in my own words:** a monthly run whose coverage repair ladder is turned off --
and I named the half that cuts the other way too, because a blast radius that lists only the
scary half is not a blast radius: such a run does **strictly less** (zero producer re-invokes,
zero rung-2 rechecks, rung 3 not reachable).

**AND I COUNTED THE WRITERS OF THE NAMED PROPERTY FIRST, WITH N PRINTED.** The property is
*"the built command string carries `--no-ladder`"*. Denominator **6** inputs reaching the built
command; **by subtraction**, 4 are Terraform-set module globals no event key maps to; **N = 2
invoker-writable writers**, and I read BOTH rules: writer 1 `forcing` (TEST_MARKER +
`FORCING_KEY` a top-level non-empty str + `FORCING_SPEC_RE`), writer 2 `month`
(`MONTH_RE=^\d{4}-(0[1-9]|1[0-2])$`, failing loud). Reading only writer 1's rule would have been
Rule 22's shared-dependency blindness moved up to the signature -- on the exact property `W4-S5`
already proved has two writers.

---

## 6. WHAT I DID NOT DO

- **NO SEND. NO ORCHESTRATOR INVOKE.** `EG-s-21`'s single permitted driven run is **UNSPENT**;
  it remains queued behind this order on my slot and I did not fire it. Measured, not merely
  asserted: 0 START RequestId over a 3 h window spanning the apply, against a non-zero control.
- **NO WRITE TO THE RENDERER.** `data/etfs/scripts/presentation/` is `EG-s-26`'s surface. I
  READ the served artifact and called its own parser and gate in-process; I wrote nothing there.
- **NO S3 WRITE OR DELETE, NO IAM, NO SCHEDULE CHANGE.**
- **NO PUSH.** Every commit is LOCAL on `wk-etfs_guardrail-3-4`.
- **NO ROW FILED.** Nothing I met was a spec-vs-world divergence: the ordering condition was
  satisfied rather than blocked; the session-serial write is the halt gate's own printed remedy
  at `halt-gate-check.sh:118` on a `.gitignore`'d path (`.gitignore:423`), already carried by
  this slot's rows `W4-S1`/`W4-S4`, and no commit crosses this order's `<paths>` boundary
  because of it.
