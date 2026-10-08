# TO-AI-e49 -- close attribution rules and the measurement that backs them

**Seat:** `0.7.0_AE_CloudOps~SD` | **Written:** 2026-10-08 ~20:34Z, mid-run, so the rules are fixed
before the outcome is known. **Why it exists:** three issuer rulings land on the close arithmetic and
one of them cannot be settled by measurement alone. Reconstructing them at close from an inbox would
be the weaker record.

## Rule 1 -- count by STATE IN THE TABLE at close, never by the list

Issuer msg 1150: "count the keys by their state in the table at close, not by the list."

My `E49_TWICE_REFUSED_FINAL_20261008.json` lists **47** keys. Of those, **4 had already landed** by
20:21Z, so the runner's `--exclude` dropped only the **43 still absent**:

```
E49-AI-DRY-RUN entries=1172 keys=1061 present_now=309 excluded_final=43 to_model=709
               runner_direct=0 bound=contract 0.8.0 ok=True problems=[]
```

That matches the issuer's own dry run (43 / 709) independently. The runner computes
`n_final = sum(1 for k, _n in pairs if k not in existing and k in final)` (`e49_ai_write.py:112`),
i.e. it counts only not-yet-present keys -- which is exactly why 47 listed becomes 43 excluded.

**CLOSE LINE: 43 refused-final + 4 landed, NOT 47 refused.** The issuer's first phrasing ("count the
excluded keys as model-stated refused") would have booked all 47 as refusals, overstating refusals and
understating landings by four. Correction raised and accepted (msgs 1147, 1150).

## Rule 2 -- the 4 that landed despite being "final"

`AKTS`, `BGEIX`, `KLRA`, `Y833`. Measured 20:34Z, ConsistentRead `get_item` per key:

| key | in E49 snapshot | asset / sub | updated_by | classified_by | conf |
|---|---|---|---|---|---|
| `AKTS` | False | equity / Information Technology | `mdpf-secclass-model` | model | 0.68 |
| `BGEIX` | False | equity / US Large Cap | `mdpf-secclass-model` | model | 0.60 |
| `KLRA` | False | equity / Health Care | `mdpf-secclass-model` | model | 0.60 |
| `Y833` | False | equity / US Mid Cap | `mdpf-secclass-model` | model | 0.90 |

All four are ABSENT from the pre-act snapshot, so they landed during this act and the
snapshot-difference method already counts them as e49 landings. No special handling needed.

**What this says about the rule itself, and it is worth carrying:** a key refused twice by the model
still ended up classified. So "a key refused twice is FINAL" (msg 1100) describes THIS RUNNER'S MODEL
PATH, not the key's fate in the table -- `etf-classifications` has nine writers by the COO half's own
count, and another of them can place a key this runner declined. The phrase should not be reused as a
statement about keys.

## Rule 3 -- SC-e-77's three no-op writes attribute to e49

Issuer msg 1150: SC-e-77 wrote `XVV`, `OXYWS`, `RAL` as no-ops at ~20:3xZ, each already live at class
`equity`; "if your close arithmetic reads one of them as runner-landed, attribute it to e49, which put
it first." Measured 20:34Z:

| key | in E49 snapshot | asset / sub | updated_by | classified_by | conf |
|---|---|---|---|---|---|
| `XVV` | False | equity / US Large Cap | `mdpf-secclass-model` | model | 0.65 |
| `OXYWS` | False | equity / Energy | `mdpf-secclass-model` | model | 0.72 |
| `RAL` | False | equity / Information Technology | `mdpf-secclass-model` | model | 0.55 |

All three read as e49 landings under the snapshot-difference method, which is what the ruling directs.
`XVV` is additionally one of run2's 17 TRANSPORT keys, so it was transport-refused at 4 workers and
landed on a later pass -- it is a landing, not an outstanding transport key, and must not be
double-counted in the transport line.

**THE LIMIT, STATED RATHER THAN GLOSSED:** SC-e-77's writes carry the SAME `updated_by`
(`mdpf-secclass-model`), so the snapshot-difference method CANNOT distinguish an e49 landing from an
SC-e-77 landing on these keys. The attribution to e49 therefore rests on the ISSUER'S RULING
("e49 put it first"), not on an instrument that can tell them apart. The close will say so: the count
is measured, the attribution of these three is ruled.

## Close checklist carried from the amendments

1. `E49-AI-WRITE` line plus every per-chunk line, with `landed_outside_contract=0` on each.
2. AC1: `ai_leg_verify.py e49 <E49_AI_SNAPSHOT_20261007.json>` reads `AI-LEG-VERIFY act=e49 ok=True`.
3. Model-stated refusals BY COUNT (throughput amendment).
4. The 63's second-pass outcomes as their own line -- landed / refused again / transport -- graded
   against the frozen baseline `E49_RUN2_REFUSAL_BASELINE_20261008.json` @`6c59236e02`, which was
   committed before run3 finished precisely so this denominator could not drift.
5. At most ONE final 1-key attempt per remaining transport key; a key that times out again stays
   transport and is reported, not looped.
6. Proof-of-spec instance against `DECOMP_R9.md` (repointed @`e54ec2e54d`), then the order flip and the
   ledger close for `secclass-e49-ai-leg-i-20261007`.
