# BATTERY `IB-rt-2` -- RESULT

**Run:** `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`
**Vintage:** branch `wk-irpt_bckend-2-2b`, after amendment 6 and the THIRD and final deploy.
**Verbatim stdout:** `battery_ib_rt_2.result.txt` beside this file. This document QUOTES that run.

> **`15 of 15 ARMS PASS. THE TOKEN IBRT2-SIX-GUARDED IS PRINTED.`**
> **THE VINTAGE IS CLEAN:** `0 subject file(s) differ from HEAD: every byte above is IN THE RECORD.`
> **NO ROOT IS HELD:** all SEVEN functions are applied and verified on their SERVED bytes, over three
> acts, one root at a time. **THE ORDER IS TERMINAL** -- and two of its fifteen arms are
> HUMAN-GATED rather than measured, printed under their own verb so neither can be read as a
> measurement.

---

## WHAT MOVED SINCE THE `15 of 15 over uncommitted bytes` RUN

| arm | was | is | why |
|---|---|---|---|
| vintage | 4 files at no commit | **0** | amendment 5 E1 put the holdings paths in `<paths>`; the lane gate had been right and the grant was prose. |
| `a1` in lane | `0 of 11` | `0 of 12` | holdings is in lane and guarded, so in-lane IS the published file. |
| `e` deployed | 6 of 6 | **7 of 7** | the second deploy applied six roots; holdings' handler moved; all seven re-verified on served bytes. |
| `g1`/`g3` | 11 of 11, 1 excluded | **12 of 12, 0 excluded** | the holdings route's guarded handler is live, so nothing is excluded any more. |

---

## ARM (a) -- ZERO OF N, AND THE CONTROL

```
denominator: 12 published route(s) = 12 with a declared handler + 0 without
IN LANE (the 7 functions this order may open): 0 of 12 unguarded
WHOLE FILE                                   : 0 of 12 unguarded
[PASS] a1 | [PASS] a2 | [PASS] a3  -- control 3 of 3 victims moved the verdict to `1 of 12`
2 basename match(es): 2 declared vendored copy(ies), 0 true collision(s)   [PASS] a4
```

`irpt-holdings` earned the mark; **the instrument did not move.** `is_guarded` still tests the one
thing `guard()` sets. The handler moved under it, and **nothing a caller reaches widened** -- its
`Entry` composes the same grant-nothing ownership triple that surface already used, because wiring
the shared loaders would have turned a route that serves nothing into one that serves real holdings,
and that is IB-rt-7's decision.

---

## ARMS (b) (c) (d) AND (d3)

```
(b) 36 of 36 swaps over the SIX the face names; difference control 6 of 6
    W1-S16's seventh negative 6 of 6, with ITS control 6 of 6
(c) 6 of 6 / 6 of 6      (d) 6 of 6 / 6 of 6      [PASS] x4
(d3) denominator READ FROM THE CONTRACT: 9 states; 5 ANSWER-BEARING; 4 NO-ANSWER [9 MINUS 5]
     the boundary's own three sets agree with the contract's, member for member: True
     6 of 6 POST-READ refusals carry business_date; 6 of 6 PRE-READ omit it; 0 of 12 null
     an ANSWER-BEARING state with no business_date RAISES at the boundary: True   [PASS] x2
```

**The state set is a SUBTRACTION from the contract's own nine, not a forward list.** My first cut was
pre-read vs post-read -- a distinction about *refusals* -- and QUEUED and RUNNING are not refusals,
so both would have kept failing. The issuer caught that and it is the load-bearing correction here.

---

## ARM (e) -- DEPLOYED AND VERIFIED -- 7 of 7

```
7 of 7: declared artifact_sha256 == live CodeSha256 | handler is the guarded entry | Active/Successful
IMPORT-OK 7 of 7 | negative control FIRES 7 of 7 | VERIFIED 7 of 7
ledger: 2 entry(ies), sentinel removed=True, post-apply plans reading `No changes`: 12
HELD ROOT, named: ycharts -- its plan NOW reads `0 to add, 0 to change, 2 to destroy`
```

Six roots in this act, one at a time, each verified on its **served bytes** before the next was
touched. Every applied root planned only `s3_object_version` + `source_code_hash`, and holdings
alone also the handler.

⛔ **A VERIFY READ RED BEFORE IT READ GREEN, AND THE INSTRUMENT WAS WRONG.** holdings' first verify
said `IMPORT-FAIL: No module named 'keys'` on a sound zip, because this verifier kept **its own**
hand-maintained list of which functions attach the layer, beside the packager's -- and the two
diverged the moment holdings was granted. **That is the fourth time in this cell that two
hand-maintained copies of one fact disagreed.** Each time the fix was to delete a copy:

| copy | where it diverged | fix |
|---|---|---|
| two in-lane test sets | `irpt-status` added to one | both now read from their owner |
| the battery reading the wrong one | holdings granted -> 42 expected, 36 run | each arm reads the set that owns it |
| the verifier's layer list | holdings granted -> probed with no `/opt/python` | **deleted**; read from the live function |
| the battery's `DEPLOYED` list | holdings deployed -> arm (e) said 6 of 7 | **deleted**; imported from the packager |

Two further defects surfaced in that same read and are fixed: `join(',', Layers[].Arn)` **raises**
on a function with no layers (three of six), and `--output text` renders an empty last field that
`strip()` removes, so unpacking five values got four. **A one-function probe would have looked clean.**

⛔ **AND A POST-APPLY `No changes` IS A PERISHABLE CLAIM.** The ycharts root read `No changes` after
this cell's first apply and now reads **`0 to add, 0 to change, 2 to destroy`**: a LIVE secret
(`ycharts/session/research-20260911`, `DeletedDate null`) and a log group that IB-rt-9 removed from
the configuration at `f83f73ce6c` without applying. **Any apply of that root by any cell now destroys
them.** Row `W2-S42`, ARMED. Found only because this arm re-read the plan instead of trusting the
recorded one.

---

## ARMS (f) AND (g2) -- HUMAN-GATED

```
[HUMAN-GATED] f  -- 9 of 9 record elements, 0 secret values
[HUMAN-GATED] g2 -- 10 of 10 record elements, 0 secret values, 0 of 12 success responses MEASURED
```

A third verb, because `PASS` would claim something unexercised and `BLOCKED` would report a met rule
as unmet. Both are graded by READING their record for the elements the rule names. **The wrong way to
close g2 is the easy one:** a fabricated advisor id returns a REFUSAL, which cannot validate against
a response contract at all.

---

## ARM (g) -- ENVELOPE CONFORMANCE, SERVED -- 12 of 12, NOTHING EXCLUDED

```
denominator: 12 route(s) whose guarded handler is DEPLOYED at this HEAD; 0 excluded
a mismatched X-Contract-Version is refused CONTRACT_VERSION on the DEPLOYED function: 12 of 12
the refusal validates against v1 StatusEnvelope: 12 of 12        [PASS] g1 | [PASS] g3
```

**"Is it deployed" is now a MEASUREMENT, not a membership:** the arm reads each function's live
`Handler` and includes the route when it equals the guarded entry. A list cannot tell you whether an
apply landed; the function can.

---

## THE ORDER IS TERMINAL -- WHAT CLOSED IT, AND WHAT IT DOES NOT CLAIM

The last root applied in a third act and **no root is held**: all seven functions this order owns
are live on the guarded entry and verified on their **served** bytes, and that final apply is what
**disarmed row `W2-S39`** -- the cache-lifetime defect this cell introduced is no longer served
anywhere, and the v0.14 envelope and the post-read `business_date` are on every function.

**Amendment 6 F2 asked for a restore and none was needed, because my own row had the cause wrong.**
`W2-S42` said IB-rt-9 removed two declarations; `git show --stat` on that commit shows it ADDED 28
lines to `iam.tf` and removed nothing. The declarations were **added** at `244d3a968d` in
`research_absorbed.tf`, and my worktree predated them while the shared state already held the
imports. Row `W2-S43` corrects it. **`git log -- <path>` answers what last TOUCHED a path, never what
CHANGED a thing** -- its top entry is a neighbour, not a cause. The observed fact was real, the
secret is preserved and untouched, and no act was taken on the wrong attribution.

⛔ **AND A PASSING ARM WAS PRINTING THAT FALSE SENTENCE FOR ONE RUN.** Arm (e) carried a hardcoded
"HELD ROOT ... not applicable by anyone right now" paragraph after both halves had become false. It
is a measurement now, not a paragraph. A green arm is not licence for the prose beside it.

### What this order still does NOT claim

* **Two arms are HUMAN-GATED, not measured.** `f` and `g2` wait on one principal a worker may not
  mint. Each is graded by READING its record (9 of 9 and 10 of 10 elements, 0 secret values).
  **0 of 12 success responses are measured and none is claimed.**
* **The test principal was never minted**, so how it would differ from a real advisor's claims is
  UNANSWERED BY MEASUREMENT -- and arm `g2` inherits exactly that gap.
* **What the in-process swaps cannot show** is what `IB-rtb-1` must add: that the EDGE VALIDATOR
  injects the headers the boundary trusts, for a token the AUTHORIZER accepted, end to end through
  CloudFront.
* **The holdings zip is internally skewed by design** -- IB-rt-7's pinned `enforce` beside the tree's
  `served` -- so that cell's `STAGE_MANIFEST` claims stay true. The one behavioural delta is measured
  unreachable for that function, but only against today's call graph.
* **Whether the two research resources should ever be retired is not this round's question.** They
  are preserved; that is the whole of what this record says about them.

### The pattern this cell is worth remembering for

Five times one fact was kept in two places and the copies diverged, and **every divergence surfaced
the moment a function was GRANTED**: the two in-lane test sets, the battery reading the wrong one of
them, the verifier's own layer list, the battery's `DEPLOYED` list -- and finally a duplicated
**VIEW** rather than duplicated data, when a stale worktree over a shared state produced a plan that
read exactly like a configuration-versus-world disagreement. Each of the first four was fixed by
**deleting a copy rather than syncing it**. The fifth is why a post-apply `No changes` is perishable
in **two** directions, and only one of them is somebody else's commit.
