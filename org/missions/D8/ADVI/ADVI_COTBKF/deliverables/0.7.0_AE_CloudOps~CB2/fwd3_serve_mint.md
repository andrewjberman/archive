# ADVI_COTBKF.TO-CB-ac-1 -- the SERVED mint of the three FWD-3 tables

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` (lane seated by MSTR msg 2264) | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 29 | **Cell:** `CB-ac-1`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @5efa02d5d9 (AMENDMENT 1 included)
**Criterion:** `CB29ac1-AC1` -- **PASS**
**Ledger:** `org/critical_paths/change_management/20261009T0743Z_advi-cotbkf-fwd3-serve-mint-cb-ac-1-20261009_deploy_completion.md`, opened @ad851387aa, CLOSED @476f970245, all 4 legs proven, sentinel removed.

---

## What was done

The three FWD-3 silver tables for Cottonwood were MINTED at their builder addresses and read back equal to
the local build. `FWD3-VERIFY tables=3 match=True`.

| table | key (all under `s3://opal-data-assets/commonwealth/cottonwood/silver/`) | rows | ETag | bytes |
|---|---|---|---|---|
| daily_returns | `daily_returns/date=2026-06-23/part-00000.parquet` | 1,691,729 | `c024c607273cfc65a2cce816b3965b43` | 1,646,994 |
| account_day_value | `account_day_value/date=2026-06-23/part-00000.parquet` | 21,102,041 | `365b2e8ef9092f6fee0335778fb4fbcb-7` | 58,027,322 |
| month_grades | `month_grades/date=2026-06-23/part-00000.parquet` | 82,593 | `88c025b57840efa8f92694b35cdbf481` | 428,972 |

Written 2026-10-09T08:09:26-28Z. The `-7` suffix on the middle ETag is a 7-part multipart upload, so that
ETag is **not** an MD5 of the object; it is recorded as an identity handle and never as a content oracle.
Content equality is carried by the hash comparison at AC1, over all 22,876,363 rows.

## The order of operations, and why

1. **Pair before any write.** Both halves exist and are GIVEN: CTO half with AMENDMENT 1 @478334e021
   (the 4 named account-months BLANKED, not valued) and COO half section 3. CTO condition 4 said to use
   `~DELL2` per CVO msg 1889 **unless** MSTR seated `~CB2` on a later word and the order cites it -- the
   order cites MSTR msg 2264, so the condition is met as written, by its own escape clause rather than by
   reading around it.
2. **Before-state, with a positive control.** All three target prefixes held 0 objects; the control
   `.../silver/transactions/date=2026-06-23/` read 14. An absence measured with no control is
   indistinguishable from a mangled prefix, so the control is what makes the three zeros mean absence.
   The act therefore MINTS and moves no served output -- the never-widen law's subject is untouched.
3. **Ledger opened before the write**, 4 legs declared up front (NEVER-2), then committed as each leg
   closed per the order's AMENDMENT 1.
4. **Rebuilt at this seat's own HEAD**, not trusted from the issuer's run. Re-grade rc 0, build rc 0,
   dry run rc 0.
5. **Apply, then read back**, then AC1.

## The equality that was required, and what was allowed to differ

The COO half fixes the row counts and lets the hashes move. Both held:

- **Row counts EQUAL** on all three tables (1,691,729 / 21,102,041 / 82,593).
- **Hashes differ**, and only as `run_commit` forces them to. `run_commit` is a column in all three
  schemas and `content_hash` covers the schema plus every row, so a different HEAD necessarily moves the
  hash. Mine: `54c5a152...` / `c7611556...` / `6ff13c60...` at `run_commit=e5371f3e395f`; the issuer's:
  `39e61705...` / `214f291e...` / `ba99ee87...` at `feeee0be4dec`. `manifest_hash_same=True` on all three
  proves the local files match the manifest written by this same build.
- **Addresses** byte-identical to the pair's three keys, `addresses_from_builder=True` -- rule 30 holds,
  nothing typed or stale.
- **`absent_months=4`**, `manifest_list_same=True`, and the four are exactly the pair's four: B3S728504
  2023-05 (22 days / 66 holding rows), B3S728504 2023-06 (21/63), B3S728506 2023-05 (22/66), B3S728506
  2023-06 (21/63), each `computed=ABSENT return=ABSENT verdict=ABSENT` with reason `REGRESSED_UNDER_R28`.
  That is CTO AMENDMENT 1 conditions 1 and 2. No fifth regression appeared, which is condition 3.

The re-grade also reproduced the drained CB-ab-1 numbers exactly: `months_before=3098/886/78609
months_after=3133/838/78622 control_same=True regressions=4 year_chain_same=True r22_named=25/25`, with
`REGRESSION-CAUSES n=4 by_cause={'cash_leg_difference': 4}` -- the 4 are a cash-leg difference only.

## Controls

- **Determinism.** `r28_out/month_grades_after.parquet`, `month_grades_before.parquet` and
  `sweep_regrade.md` came back at 312,561 / 313,841 / 145,340 bytes, identical to the issuer's run.
- **Independent corroboration.** The served `month_grades` was re-read and re-hashed *outside* the
  script's own verdict to `6ff13c60ebb5e84db6007f9c2d98e7672dd9a73ec257f42e3e7ae0c9fd779120` -- the hash
  the dry run printed for the local table *before* the write. Equality holds under a second instrument.
- **Sealed planted mutant.** AC1 rests on `content_hash` discriminating. One cell of the **served**
  `month_grades` was mutated in memory (row 0, `account`, `00074413503` -> `00074413503X`), nothing
  written anywhere, and the comparator moved to `16be57682ca8...` -- `FIRED-AS-EXPECTED`. Its control arm
  ran **first**: re-hashing the unmutated served bytes gave `rehash_same=True`, so the mutant's
  difference is the planted mutation and not instrument noise.
- **Negative arm, already on this instrument's record.** Before this apply the issuer's `--verify` read
  `served_rows=ABSENT match=False` on these same three addresses (behaviour added @61c911a8bf with a
  test, so it says so plainly rather than crashing). `match` flipped False -> True across the only act in
  between.

## Instrument limit found and recorded, not worked around

`aws iam simulate-principal-policy` is **non-discriminating for this principal**. `s3:PutObject` on the
target key read `allowed`; a **separate** invocation against `arn:aws:s3:::opal-data-assets-no-such-bucket-zzz9999/x.parquet`
*also* read `allowed`. That is the documented false-allow mode -- an `allowed` proves the pattern matches
the string typed, not that the resource exists or is the intended one -- so the simulation carries no
key-level information here and was **not** cited as the grant's proof. The Put itself was used as the
oracle, graded at leg A1. The preflight's own `comp-iam` line in the order declared this run at apply
time; it is recorded with its limit rather than as a pass.

## Surprise rows filed (two, both INERT, work continued)

- **`ADVI_COTBKF-D2-S42`** -- the order's step 3 still gates the mint on `regressions=0`, a precondition
  superseded before the order was cut (CTO AMENDMENT 1, the COO half, and CB-ab-1's own amended AC2 all
  say 4 NAMED and BLANKED). The order carries both readings at HEAD. Graded against the pair and the
  order's own later paragraph, which agree with each other and with the measured world. A seat reading
  step 3 alone would hold a SERVED act forever on a condition no build at the chain's default cash leg
  can meet.
- **`ADVI_COTBKF-D2-S43`** -- the refusal clause names the row id form `ADVI_COTBKF-D2-WCB2-S<k>`, which
  `proof-of-spec-check.py:1206` `SURPRISE_ID_RE` cannot parse (its lane arms are `[A-Z][0-9]*` and
  `W[0-9]+`/`C`), so a row filed exactly as instructed makes the instance INVALID and blocks the flip.
  Measured: `ADVI_COTBKF-D2-WCB2-S1` REJECTED, `ADVI_COTBKF-D2-S42` PARSES. Channel census with its
  denominator: 125 row ids for this project, 21 in the non-worker `D2-S<n>` form, max n = 41. Both rows
  use that existing namespace and S43 records the departure instead of silently renaming. Choosing
  between the clause and the regex is the issuer's call.

Both appended in the **shared** tree, not a worktree (CLAUDE.md 14b inverts for an append-only shared
file). Verified a pure append: the HEAD bytes are a byte prefix of the new file, 55 insertions, 0
deletions.

## Branch and rollback

**Branch A** of the pair fired. Nothing to roll back. `--apply` was run **without** `--overwrite`, so a
pre-existing object at any target would have aborted the run rather than replaced it. Per CTO half
condition 3 a branch-B deletion is a human-confirmed act; it stays unexecuted.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `deploy_ledger.py` | `open` / `close-leg` x4 / `close --slug advi-cotbkf-fwd3-serve-mint-cb-ac-1-20261009` | 4 legs declared before the write, each closed with proof, entry CLOSED, sentinel removed, nothing stranded |
| `proof-of-spec-check.py` | `<instance> CB29ac1-AC1` | **VALID (rc=0)**. First pass was INVALID on 9 violations -- `s3-object`/`SERVED` outside the schema's enums, an undeclared `controls.negative_arm`, and the WCB2 surprise id; all fixed, the last one by filing in the project's real namespace and recording the collision as D2-S43 |
| `owned-paths-validate.py` | `--check-agent 0.7.0_AE_CloudOps~CB2 .owned-paths.yaml`, 4 intended paths on stdin | rc 0, no VIOLATION lines -- the proof instance, this log, the order file and the ledger entry are all in this lane's write surface |
| `comp-to` | `comp-to ADVI_COTBKF.TO-CB-ac-1.fwd3-serve-mint` | session TO_ID set, race-free per seat+session |
| `aws s3api` | `list-objects-v2` on the three targets + the `transactions/` control, before; `head-object` on each key, after | before 0/0/0 with the control at 14; after all three present with ETags, sizes and LastModified |
| `aws iam simulate-principal-policy` | one `--resource-arns` per call; target key, then a separate out-of-grant control | **NON-DISCRIMINATING** -- both `allowed`; recorded with its limit, not cited as proof |
| `safe-commit.sh` | 3 commits under this seat's author line, `-F` message files written by a non-shell writer | @ad851387aa (ledger OPEN), @476f970245 (ledger CLOSED), @c2d3f143d3 (the two rows); surprise-row-gate OK on 2 new rows of 126 |

**What failed / gaps.** `comp-iam` was declared in the order's preflight for apply time; the live
simulator it rests on cannot see `(action, resource)` for this principal, so the declared control is
weaker than the order assumes -- the Put covered it. The first `grep -rn` for the reach-cap constant was
denied by the comp rail (F1, blind recursive search); the named-file `Grep` and the round-28 packet
answered it instead, and the answer is that the committed cap 0.5 is the DIFF-TRACE reach cap of the
read-only trace CB-ab-3, not a value in these three tables -- the packet's build line carries no cap and
the build takes no cap flag, so CTO condition 2 is satisfied without a forced 1.0.

## Push state

Measured at write time, not defaulted. See the final report line.
