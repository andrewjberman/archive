# BATTERY `IB-rt-2` -- RESULT

**Run:** `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`
**Vintage:** branch `wk-irpt_bckend-2-2b`, after amendments 3 and 4 and the six-root deploy.
**Verbatim stdout:** `battery_ib_rt_2.result.txt` beside this file. This document QUOTES that run.

> **`15 of 15 ARMS PASS. THE TOKEN IBRT2-SIX-GUARDED IS PRINTED.`**
> **AND THE ORDER IS DELIBERATELY NOT FLIPPED TERMINAL.** Four subject files are at NO COMMIT,
> the run says so above its own token, and the `<paths>` grant that would let them be committed is
> live ONLY while this order is non-terminal -- so flipping it would permanently orphan them.

**THIS SUPERSEDES the `10 of 13` vintage of this file.** New run, not a correction.

---

## WHAT CHANGED SINCE THE `10 of 13` RUN, AND WHY EACH ARM MOVED

| arm | was | is | why |
|---|---|---|---|
| `a2` whole file | `1 of 12` BLOCKED | `0 of 12` PASS | amendment 3 C1 granted the holdings paths and the handler moved under the mark. **The census was NOT loosened.** |
| `g3` refusal validates | `0 of 11` BLOCKED | `11 of 11` PASS | the CTO ruled the contract (PRD v0.14 @`b8e98d5a4d`): `business_date` is state-conditional. Not a workaround here. |
| `g2` success responses | BLOCKED | **HUMAN-GATED** | ruled by the issuer as the face's own rule applied to a dependent arm; graded by READING its record, 10 of 10 elements. |
| `d3` (new) | -- | PASS x2 | the post-read obligation the contract deliberately stopped carrying, plus its negative control. |
| `f` the principal | PASS | **HUMAN-GATED** | same verdict, now under a verb that cannot be mistaken for a measurement. |

---

## ARM (a) -- ZERO OF N, AND THE CONTROL

```
denominator: 12 published route(s) = 12 with a declared handler + 0 without
IN LANE (the 7 functions this order may open): 0 of 12 unguarded
WHOLE FILE                                   : 0 of 12 unguarded
[PASS] a1 zero in lane | [PASS] a2 zero over the whole file | [PASS] a3 the control fires
  the control, on a THROWAWAY copy of the TABLE (never of a handler): 3 of 3 victim(s)
2 basename match(es) across 8 function directory(ies) x 7 shared module(s):
  2 declared vendored copy(ies), 0 true collision(s)          [PASS] a4
```

**`irpt-holdings` EARNED THE MARK; THE INSTRUMENT DID NOT MOVE.** `is_guarded` still tests the one
thing `guard()` sets. Row `W2-S31` established that this was a MARK gap and not a live cross-firm
hole -- the handler enforced the same `FirmBinding` inline -- and the issuer and the CTO both ruled
that an inline enforcement the instrument cannot see should stay VISIBLE rather than be absorbed.
So `holdings/entry.py` puts the boundary in front and the Terraform root names it.

⛔ **AND NOTHING A CALLER REACHES WIDENED, WHICH TOOK A DECISION RATHER THAN A DEFAULT.**
`make_holdings_enforcer` defaults the ownership map to `_no_grant` and the deployed handler never
supplied a real one, so every `FIRM_ADVISOR` resolves to an EMPTY permitted set today. Handing
`Entry` the shared `_loaders.deps` -- what the other six do -- would have turned a route that
serves nothing into one that serves real holdings. **That is IB-rt-7's decision, not this cell's**,
so `entry.py` composes the SAME triple that surface already used.

**THIS FILE HAS NOW ASSERTED THE CURRENT GAP TWICE AND BEEN RIGHT TWICE:** `3 of 11` for
`irpt-status` before `W2-S19`, then `1 of 12` for `irpt-holdings` before `W2-S30`. Each time the
assertion's own failure was the notice that the gap had closed.

---

## ARMS (b) (c) (d) -- THROUGH THE REAL ENTRY POINTS

```
(b) six swaps x 6 dispatched function(s) ........................... 36 of 36
    the swap census covers 6 function(s); irpt-holdings carries the C1 MARK and is NOT in the
    swap set -- its deploy is HELD (rows W2-S38, W2-S41), named here and counted in neither direction
    difference control -- the authorized request is NOT refused .....  6 of 6
    ROW W1-S16, the seventh negative: an ADMIN principal addressing an advisor
    outside the verified firm is refused ...........................  6 of 6
    and its difference control -- an IN-FIRM advisor is NOT refused OBJECT_NOT_COVERED  6 of 6
(c) 6 of 6 and 6 of 6   (d) 6 of 6 and 6 of 6   [PASS] x4 including the envelope key set
```

**`36 of 36` is the face's bar over the SIX the face names.** Three arms briefly went red in an
earlier run of this battery for a reason that had nothing to do with them: the battery was reading
the ROUTE census's in-lane set as the SWAP census's denominator, so when amendment 3 granted
holdings the expected count became `7 x 6 = 42` while the suite ran 36. **Each arm now reads the
set from the module that OWNS it.** That is the two-separate-lists trap the wind-down hand-off
named, arriving from the other side.

---

## ARM (d3) -- THE BUSINESS DATE, WHERE THE SCHEMA CANNOT REACH

```
denominator, READ FROM THE CONTRACT not from this file: 9 state(s) in the enum
  ANSWER-BEARING (business_date REQUIRED): 5 -- READY, PARTIAL, STALE, NEEDS_CORRECTION, UNCERTAIN
  NO-ANSWER  (may be ABSENT, never null) : 4 -- QUEUED, RUNNING, UNAVAILABLE, FAILED  [9 MINUS 5]
the boundary's own three sets agree with the contract's, member for member: True
  6 of 6 POST-READ refusals carry business_date = 2026-09-10 (from the ARTIFACT)
  6 of 6 PRE-READ refusals omit it -- ABSENT, and 0 of 12 envelopes carry it as NULL
an ANSWER-BEARING state built with no business_date raises at the boundary: True
[PASS] d3 the post-read business date | [PASS] d3 an answer-bearing state cannot ship dateless
```

**THE STATE SET IS A SUBTRACTION FROM THE CONTRACT'S OWN NINE, NOT A FORWARD LIST.** My first cut
of this rule was PRE-READ vs POST-READ -- a distinction about REFUSALS -- and **QUEUED and RUNNING
are not refusals at all**, so both would have gone on failing validation exactly as before. The
issuer caught it and said so plainly; the subtraction cannot lose a member without the count
disagreeing.

**THE OBLIGATION IS HONOURED WHERE THE SCHEMA GAVE UP.** The contract's own `allOf` `$comment`
records that it can no longer catch a post-read refusal that omits a date it HAS. A post-read
refusal has an artifact and now states it. **And the arm has a negative control**: without the
raise, "the date is present" could be satisfied by a boundary that never checks.

---

## ARM (e) -- DEPLOYED AND VERIFIED -- 6 of 6

```
declared artifact_sha256 == live CodeSha256: 6 of 6; handler is the guarded entry: 6 of 6;
Active/Successful: 6 of 6
IMPORT-OK 6 of 6 | negative control FIRES 6 of 6 | VERIFIED 6 of 6
ledger: entry present=True, sentinel removed=True, post-apply `No changes`: 6 of 6
```

Six roots, one at a time, each verified on its SERVED bytes before the next was touched. **Two
runtime-only defects meant none of the six could have served a production event before this order**
-- the package roots derived from the parent of `/var/task`, and `operation_of` resolving the
operation by READING `routes.json` on exactly the event shape the API delivers
(`integrations.tf:57`, `payload_format_version = "2.0"`, no request template). **A guard that cannot
import is not a guard, and three matching hashes say nothing about either.**

⛔ **AND A DEFECT THIS CELL INTRODUCED AND REMOVED -- row `W2-S39`.** `served.Entry` held ONE cache
dict for the MODULE'S lifetime. Found by accident: a holdings test refused a bad snapshot alone and
**SERVED** it when a valid request ran first. Authorization was never at risk (both branches
reauthorize; the key carries tenant and scope fingerprint). Freshness was. **A better key cannot
fix it** -- the key is built from what the BOUNDARY sees and a compute reads artifacts the boundary
never sees -- so the cache is now PER-REQUEST unless explicitly shared, which is what the
pre-existing holdings path did. ⚠ Still ARMED in the world until the next deploy ships it.

---

## ARMS (f) AND (g2) -- HUMAN-GATED, UNDER A VERB THAT IS NEITHER PASS NOR BLOCKED

```
[HUMAN-GATED] f the principal  -- 9 of 9 required elements, 0 secret values
[HUMAN-GATED] g2 success responses validate, SERVED -- 10 of 10 elements, 0 secret values,
              0 of 11 success responses MEASURED and none claimed
```

**A THIRD VERB WAS NEEDED.** `PASS` would claim something unexercised; `BLOCKED` would report a met
rule as unmet. Both arms are graded by READING their record for the elements the rule names, as
literal strings, so a reworded record fails rather than being read charitably.

**AND THE WRONG WAY TO CLOSE g2 IS THE EASY ONE:** invoking a deployed function with a FABRICATED
advisor id returns a REFUSAL, which cannot validate against a response contract at all (row
`W2-S25`). Counting that would record the opposite of what the arm asks. The record names the
operator's act as **step 3b of arm (f)'s same bounded run**, with the two ENQUEUEING routes
excluded on their own line under bounds 1 and 2.

---

## ARM (g) -- ENVELOPE CONFORMANCE, SERVED

```
denominator: 11 route(s) whose guarded handler is DEPLOYED at this HEAD; 1 excluded and named:
  EXCLUDED, neither a pass nor a fail: GET .../holdings/{accountSetId} -- irpt-holdings
  (guarded in the TREE at this commit, apply HELD: rows W2-S38 and W2-S41)
a mismatched X-Contract-Version is refused CONTRACT_VERSION on the DEPLOYED function: 11 of 11
the refusal validates against v1 StatusEnvelope: 11 of 11
[PASS] g1 the version check is SERVED | [PASS] g3 the refusal validates against StatusEnvelope
```

**`g1`'s denominator is "routes whose guarded handler is DEPLOYED", which is NOT "routes this order
may open".** Counting the twelfth would have reported another cell's deployed behaviour as this
arm's failure; omitting it silently would have overstated the sweep. It is named.

---

## THE VINTAGE -- WHY THE TOKEN IS NOT A TERMINAL ORDER

```
HEAD: 0562ba4708
4 subject file(s) are NOT at HEAD:
   M _authz/tests/test_unguarded_census.py      M terraform/investor-reporting/holdings/lambda.tf
  ?? holdings/entry.py                          ?? holdings/tests/test_entry_guarded.py
```

Amendment 3 C1 grants the holdings paths in **PROSE**; the `<paths>` block does not name them, and
the lane gate refuses them. **The gate is right** -- it reads the machine-readable grant -- and an
author override is the one escape `ADHC_OWNPTH.005` forbids. Row `W2-S41`, **ARMED**, because the
work exists only on this device's filesystem.

⛔ **AND THIS IS WHY THE `<status>` STAYS OPEN.** The `<paths>` grant is live **only while the order
is NON-TERMINAL**. Flipping to `complete` would retire the grant and permanently orphan C1's
work -- a terminal order whose deliverables exist at no commit is not a record. **One line of
`<paths>` turns this disclosure into a record and this order terminal.**
