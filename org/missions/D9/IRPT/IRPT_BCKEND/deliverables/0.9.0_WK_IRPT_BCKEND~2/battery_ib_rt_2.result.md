# BATTERY `IB-rt-2` -- RESULT

**Run:** `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`
**Vintage:** branch `wk-irpt_bckend-2-2b` @ `36e4c5f70b`, after amendment 5 and the second deploy.
**Verbatim stdout:** `battery_ib_rt_2.result.txt` beside this file. This document QUOTES that run.

> **`15 of 15 ARMS PASS. THE TOKEN IBRT2-SIX-GUARDED IS PRINTED.`**
> **AND THE VINTAGE IS CLEAN:** `0 subject file(s) differ from HEAD: every byte above is IN THE
> RECORD.` The previous run printed the same token over four uncommitted files; this one does not.
> **`<status>` IS STILL NOT FLIPPED, for one reason that is not bookkeeping -- see the last section.**

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

## WHY `<status>` IS STILL OPEN -- ONE REASON, AND IT IS NOT BOOKKEEPING

Every criterion passes by output and the vintage is clean. **One of the seven functions this cell
owns is still serving code without this cell's own fix.** `irpt-ycharts-generate` keeps the previous
`served.py`, so it alone lacks the v0.14 state-conditional envelope and the post-read
`business_date` -- and **row `W2-S39`'s cache-lifetime defect, which this cell INTRODUCED, remains
ARMED on it.**

It cannot be fixed by this cell right now, and the reason is not a preference:

* **`W2-S38`** -- amendment 5 E3 instructs a STOP if that zip carries `settings.json` without
  `fixtures/holdings/security_mapping.json`, or either without `parse.py`. Re-measured at HEAD the
  literal condition is TRUE (`parse.py` is declared by **0 of 214** functions). The issuer's call.
* **`W2-S42`** -- and independently, **no cell can apply that root at all** without destroying a live
  secret another cell removed from configuration.

**A terminal flip would retire the `<paths>` grant this cell needs for that last apply**, and it
would assert the work is complete while a defect this cell introduced is still served. So the order
stays open on two rows whose owners are named, `IB-rt-6` and `IB-rtb-1` wait on one ruling, and the
flip is the last act -- not the act that frees anyone to finish.
