# TO-AI-e32, the e32 AI leg: RUN 1 KILLED mid-act at 23:0xZ -- the measured state, and the call that is owed

**Author:** `0.7.0_AE_CloudOps~SC`, 2026-10-07 23:2xZ. **Ledger:** `secclass-e32-ai-leg-i-20261007`,
**OPEN**, entry
`org/critical_paths/change_management/20261007T2120Z_secclass-e32-ai-leg-i-20261007_deploy_completion.md`,
sentinel `org/critical_paths/.open_deploys/secclass-e32-ai-leg-i-20261007.json`, opened @`3c7b2ded06`.
**No leg is closed. The entry is deliberately left OPEN, which is the loud state.**

## What stopped it

The Claude Code harness killed the background process because the SYSTEM was critically low on
memory while the session was idle. Verbatim from the harness notice: "This is not a failure of the
command. Claude Code stopped it because the system was critically low on memory while the session was
idle, which says nothing about the command or its own memory use, so there is nothing in it to debug.
Do not start it again on your own, even if the work seems to need it: memory may still be short.
Report what was stopped and why, and start it again only when asked."

So this is NOT a STOP of the kind the order's step 3 anticipates. There was no contract breach, no
vendor refusal, no AWS error, and no traceback: the act's whole output is one `DIRECT planned=0` line,
one clean chunk line, and 63 `UNRESOLVED` lines. The process is confirmed DEAD (0 matching
`old_list_reclassify_write` processes). **This seat has NOT restarted it and will not without being
asked**; at the kill the box had 3.93 GB free of 31.7 GB (12.4 percent).

## The landed state, measured

Consistent paginated scan of `etf-classifications` (us-east-1) at 23:15Z, against the run's own
snapshot and the V3 set:

```
SNAPSHOT keys=8968 (taken 21:26Z, intact, 219,994 bytes)
PLANNED ai keys absent at snapshot=2291
LANDED of planned=187   STILL-ABSENT=2104
TABLE total=9155   delta_vs_snapshot=187
SNAPSHOT keys now missing (must be 0)=0
classified_by=model total=200   of which this run (updated_by=mdpf-secclass-model)=200
multi_asset rows=0
```

Chunk 1's self-report, independently corroborated three ways (the chunk line's own `written=187`; the
scan arithmetic 8,968 + 187 = 9,155 and 13 + 187 = 200; the output file's 63 `UNRESOLVED` lines =
250 - 187):

```
AI chunk 0-250: keys_sent=250 model_calls=251 landed_outside_contract=0 to_model=250 would_land=187 written=187
```

AI listing: `date=2026-10-07/index.json` holds `count=200`, equal to `model_rows`;
`date=2026-10-08/index.json` is ABSENT (`NoSuchKey`), as it should be at 23:1xZ.

**The partial state is BENIGN BY CONSTRUCTION, and that is the design working, not luck.** Every put
is `attribute_not_exists(ticker)`; nothing existing was touched; 0 snapshot keys are missing; the 187
landed rows all passed the contract 0.8.0 bound (`landed_outside_contract=0`) and carry
`classified_by=model` with `classification_confidence`. The halves state the property that makes this
safe: "the act is repeatable, since a present key is never touched."

## THE TRAP, and why step 4 was not executed

AC1, run exactly as the order names it, on this 8-percent-complete act:

```
AI-LEG-VERIFY act=e32 ok=True planned=2291 landed=187 unresolved=2104 problems=0 first=[] snapshot_keys_gone=0 multi_asset=0 model_rows=200 listing_count=200
AC1 rc=0
```

**`ok=True`, rc=0, on 187 of 2,291 keys.** `ai_leg_verify.py`'s `ok` is
`not probs and gone == 0 and ma == 0 and landed > 0 and lcount == model_rows`. The `landed > 0` term
is the preflight's guard against "an empty success" -- and it does catch an EMPTY act. It does not
catch a PARTIAL one: `unresolved` is printed but is NOT in the predicate, so every value from 1 to
2,291 landed reads identically as `ok=True`.

The order's step 4 is "Prove it (AC1) and close the entry with the `RECLASSIFY-WRITE` line and AC1's
output. Flip this order complete." Executed mechanically after this kill, that sequence would have
closed a NEVER-2 entry and flipped a WORLD-risk order to `complete` on an act that had sent 250 of
2,291 keys. **The only thing standing in the way is the `RECLASSIFY-WRITE` line, which the act never
printed** -- it is emitted after the chunk loop, so its ABSENCE is the real completeness oracle here,
and AC1 is not. Step 4 is therefore NOT executed, no leg is closed, and the order stays `pending`.

## The call that is owed, with this seat's recommendation

Two routes. Neither is this seat's to take: restarting is barred by the harness notice, and rolling
back is the issuer's act on this signature (CTO half condition 4 on the sibling order states the
rollback exercise stays the issuer's).

**(a) RESUME when the box has headroom -- RECOMMENDED.** Re-run the same `--write` invocation. It
cannot double-write: the 187 present keys are skipped by `attribute_not_exists`, and the planner's
`now_present` absorbs them. **The vendor ceiling is NOT breached by resuming, and this is the load-
bearing number:** the ceiling in both halves and in the writer (`VENDOR_KEY_CEILING = 8495`) is on
DISTINCT KEYS, and the distinct key set is unchanged at 2,291 whether this runs in one pass or two.
Call count across both attempts is about 251 + 2,104 = 2,355 plus retries, against the half's stated
"at most 4,582". The only waste is 63 re-sent keys -- chunk 1's unresolved, which are absent and so
re-enter the plan.
  - One blocker to name: the writer `raise SystemExit`s if the `--snapshot` path already exists. A
    resume must therefore either reuse `E32_AI_SNAPSHOT_20261007.json` (correct: it is the true
    pre-act key set and the rollback's only valid input) by a route the writer permits, or be given a
    second snapshot path -- in which case the ORIGINAL snapshot remains the rollback input for the 187
    already-landed rows, and that must be written into the ledger or the rollback silently narrows.
    This is a real edge the halves do not cover, because they did not contemplate a resumed act.

**(b) ROLL BACK.** The entry's command, per key, conditional delete of set keys absent from the
snapshot carrying this run's two `updated_by` values. It would delete exactly the 187 rows and
nothing else. **This seat does not recommend it:** it destroys 187 correct, contract-conformant rows
and the 251 vendor calls Andrew's word paid for, and a later redo spends 2,291 fresh calls against the
same ceiling -- all to reach a state that route (a) reaches without the deletion.

## What is NOT at risk either way

`bd-securities` was never written. No IAM changed. No other table, bucket or prefix was touched. The
blast radius stayed inside what both halves named: one table plus the one AI listing object.

## Next

Escalated loud to `1.0.0_SA_CTO` for relay to the issuer `2.0.0_SA_COO~M1` (dell1), which holds the
resume-or-roll-back call. The entry stays OPEN and will blare on the COO's `check --red` sweep until
it is dispositioned. Surprise row `MDPF_SECCLASS-S66` carries the AC1 partial-completeness gap.
