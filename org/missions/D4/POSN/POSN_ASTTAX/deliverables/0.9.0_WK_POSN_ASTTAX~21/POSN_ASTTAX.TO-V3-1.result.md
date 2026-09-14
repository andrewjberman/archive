# POSN_ASTTAX.TO-V3-1 -- RESULT

**Cell `AT5-s-3` (B3, FWD-5 durability) / round 5 / `0.9.0_WK_POSN_ASTTAX~21` / branch
`wk-posn_asttax-5-21` / worktree `C:/tmp/wk-posn-5-21`.**
Worktree HEAD at start: `2a882703db`. The task-order file's bytes were compared against the face
delivered in the spawn prompt and **agree exactly** (8744 bytes, last touched by `2a882703db`, the
amendment that repaired V3-AC5's invocation).

**Outcome: 6 of 6 mechanical criteria PASS by output; V3-AC7 RECORDED (judgment, graded by
`3.0.0_SA_CVO~Z` at L9). Four surprise rows filed. The live table was never written.**

---

## 1. WHAT THIS CELL DID

Round 4's `TO-U3-1` measured the defect and wrote the fix but could not apply it -- its `<paths>`
grant excluded `data/black_diamond/**`. This order's grant **is** the file, so this cell applied
round 4's diff verbatim, gated it, proved it on a scratch copy of the table, and committed it.

The change, in one sentence: the Yang (`etf-classifications`) limb of `seed()` now **pre-reads the
live row** and refuses to overwrite a value the table already serves and the seeder disagrees with,
exiting 1 without writing, with `--force` the single override -- and **a first mint still mints**.

The mechanism is the sibling writer's, not a second pattern:
`infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py` `merge_item():72-120`.

**Commits (both LOCAL on `wk-posn_asttax-5-21`, never pushed):**

| commit | what |
|---|---|
| `8cad052620` | the patched `seed_canonical_securities.py` (+57/-2) |
| (second) | this result, the proof instance, the harnesses and outputs, the four surprise rows, and the `<status>` flip to `complete` |

---

## 2. PER CRITERION -- INVOCATION, VERBATIM OUTPUT, rc, DENOMINATOR

### `V3-AC1` -- THE PATCH APPLIES, AND THE CHECK DISCRIMINATES. **PASS**

Grain first: the working-tree file hashed **identically to HEAD's blob and to round 4's recorded
subject** before anything was touched -- `fbbc7165d33198789d3a7788a557ed3f5ce75614`, 296 lines,
15000 bytes.

```
$ timeout 60 git apply --check org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~16/u3_proposed_patch.diff
RC=0                                    <- no output; rc is the verdict
```

NEGATIVE CONTROL, run **before** applying, on a copy of the same diff with one context line
corrupted (line 40 of 95; length-preserving, so the hunk headers stay valid; 4299 -> 4320 bytes):

```
$ timeout 60 git apply --check .scratch/u3_patch_MUTATED_context.diff
error: patch failed: data/black_diamond/scripts/classification/seed_canonical_securities.py:212
error: data/black_diamond/scripts/classification/seed_canonical_securities.py: patch does not apply
RC=1                                    <- THE CHECK DISCRIMINATES
```

Then the apply and the diffstat:

```
$ timeout 60 git apply <the same diff>            RC=0
$ timeout 60 git diff --stat -- data/black_diamond/scripts/classification/seed_canonical_securities.py
 .../classification/seed_canonical_securities.py    | 59 +++++++++++++++++++++-
 1 file changed, 57 insertions(+), 2 deletions(-)
$ git diff --numstat -- <the file>
57      2       data/black_diamond/scripts/classification/seed_canonical_securities.py
```

The figure the patch itself carries, printed as `<expect>` requires: **+57/-2** over 95 diff lines
-- equal to the measured 57/2.

**A second axis on the same claim (grain):** the applied bytes are **byte-identical** to the bytes
round 4's `U3-AC3` exercised -- both 17700 bytes, sha256 `dde708491f6fa73d`. So "the patch applied"
and "the patch applied *is the reviewed one*" are separately evidenced.

*Denominator:* 1 of 1 patch; 95 of 95 diff lines; 2 of 2 check arms; 1 of 1 tracked path modified.

### `V3-AC2` -- THE GATE ON THE CHANGED `.py`. **PASS** (and see `W21-S2`)

The criterion's invocation takes its subjects from argv and is given none. Run exactly as written:

```
$ timeout 180 bash .tools/commit-gate.sh
WARN: commit-gate checked 0 of 0 file(s) -- NOTHING WAS CHECKED.
      This line is NOT evidence of a clean gate. ...
RC=0
```

The gate says the quiet part itself. Its own exit-code table documents that `rc=0` covers *"nothing
was dispatched at all"*, so the exit code cannot separate the arms -- only the printed denominator
can. The arm whose subject is the one `<expect>` names ("the CHANGED file ... and nothing else"):

```
$ timeout 180 bash .tools/commit-gate.sh data/black_diamond/scripts/classification/seed_canonical_securities.py
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 1 of 1 file(s)
RC=0
```

The denominator moves `0 of 0` -> `1 of 1`, which is the entire difference. A **third, in-band**
exercise: the same gate ran inside the commit that landed the file (`8cad052620`) on the same single
path, printing the identical `1 of 1` line. And the instrument **fires** when given a bad subject --
a planted `def broken(:` returns `BLOCKED: py_compile failed`, `rc=1`.

**Both ASCII limbs, read and named:**

- **Limb 1 -- staged-`.py` content, WARN-ONLY, never blocks.** `commit_gate_runner.py:405-461`
  `_nonascii_lint_one`, whose docstring says *"Always returns 0"*. **Its scope is `infra/**` and
  `.tools/**` only** (`:429-431`). The subject is `data/black_diamond/**`, so **this limb returned 0
  without reading a byte of it** -- it contributed nothing to the clean reading, which is exactly why
  `V3-AC3` exists as a separate instrument.
- **Limb 2 -- commit message, BLOCKING.** `.tools/git-hooks/commit-msg-ascii-check.sh`, installed as
  the live `.git/hooks/commit-msg` in the shared git-common-dir (`core.hooksPath` unset). Header:
  *"This gate reads the COMMIT MESSAGE ONLY. It does NOT inspect file contents."* It passed; both
  message files were verified pure ASCII before their commits.

*Denominator:* 1 of 1 changed `.py` on the subject-bearing arm; 3 of 3 gate instruments; 2 of 2 ASCII
limbs; 3 exercises plus 1 negative control.

### `V3-AC3` -- ASCII, BY AN INSTRUMENT THAT SELECTS THE FILE AND CAN FIRE. **PASS**

```
$ timeout 60 python -c "... p='data/black_diamond/scripts/classification/seed_canonical_securities.py' ..."
data/black_diamond/scripts/classification/seed_canonical_securities.py 0
$ timeout 60 python -c "... p='CLAUDE.md' ..."
CLAUDE.md 427
```

427 > 0, so the instrument is capable of a nonzero reading and the 0 is a measurement, not a constant.

**The unit is part of the claim:** this expression returns `len(bytes) - len(decoded characters)` --
the count of **extra bytes** contributed by multi-byte characters, *not* a count of non-ASCII
characters. CLAUDE.md's 213 non-ASCII characters read 427 here because they are three-byte
characters. On a pure-ASCII file the two lengths are equal and the result is exactly 0.

*Denominator:* 1 of 1 subject over all 17700 of its bytes; 2 of 2 arms.

### `V3-AC4` / `V3-AC5` -- THE TWO ARMS, SIDE BY SIDE. **PASS / PASS**

One bounded run produced both arms: `timeout 600 python .scratch/v3_mutant_control_re.py`, rc=0.
It is round 4's control **re-run against the APPLIED REPO FILE** -- the one thing round 4 could not
do. Round 4's machinery (`u3_ac1_before_control.py`: the scratch table, the fake boto3, the retag
set, the baseline builder, the mint probe) is imported **unmodified**, with its sha256
`ae72cab7dfbeb62f` asserted at import, so the two rounds' numbers are comparable rather than merely
similar.

| | `V3-AC5` pre-patch arm | `V3-AC4` applied arm | override arm |
|---|---|---|---|
| subject blob | `fbbc7165d331` (15000 B) | `803721e2c154` (17700 B) | `803721e2c154` |
| VXX | Structured -> equity **CLOBBERED** | Structured -> Structured **SURVIVED** | CLOBBERED |
| UVXY | Structured -> equity **CLOBBERED** | Structured -> Structured **SURVIVED** | CLOBBERED |
| QBER | Structured -> fixed_income **CLOBBERED** | Structured -> Structured **SURVIVED** | CLOBBERED |
| PDBC | Commodities -> equity **CLOBBERED** | Commodities -> Commodities **SURVIVED** | CLOBBERED |
| tally | SURVIVED **0 of 4**, rc=`None` | SURVIVED **4 of 4**, rc=**1** | CLOBBERED 4 of 4, rc=0 |
| mint control | `CASH_USD` MINTED, **53** rows | `CASH_USD` MINTED, **53** rows | MINTED, 53 |
| yang get_item | 0 | 57 | 57 |

**THE TWO ARMS DIFFER on identical input**, and the mint control fires in **both** -- so "CLOBBERED"
is a property of the seeder's write rule and not of the instrument, and the guard is not simply a
script that refuses everything. The applied arm printed 8 `[PRESERVED]` lines and:

```
REFUSED 4 etf-classifications row(s): the table serves a value this seeder disagrees with.
Nothing was reverted. Re-run with --force to overwrite them.
  [PRESERVED] QBER       asset_class: table serves 'Structured', seeder asserts 'fixed_income' -- table wins, pass --force to override
  [PRESERVED] VXX        asset_class: table serves 'Structured', seeder asserts 'equity' -- table wins, pass --force to override
  ...
```

**The scratch target, named.** Every table above is an in-process dict. `boto3` is replaced in
`sys.modules` **before any seeder byte executes**, and `boto3.client()` **raises**, so no network
client exists in the process; each interception prints the table name it caught. `--upload` was never
passed to a real table because no real table exists there.

**Subject resolution for `V3-AC5`, by CONTENT and not by ref name.** The patch was applied but not
yet committed when this arm ran, so HEAD still carried the pre-patch blob. All three candidate
sources resolve to one object and the harness asserts it before running:

```
HEAD                 : fbbc7165d33198789d3a7788a557ed3f5ce75614
HEAD~1               : fbbc7165d33198789d3a7788a557ed3f5ce75614
U3 scratch head copy : fbbc7165d33198789d3a7788a557ed3f5ce75614
```

So the order's literal `HEAD~1` form and the form used are **the same object**; no deviation arises.

*Denominators:* 4 of 4 carried five-class members (of an 11-member retag set, against the seeder's
57-row list); 53 of 53 absent rows minted; 8 `[PRESERVED]` lines over 4 tickers x 2 conflicting
fields; 2 of 2 table names intercepted.

### `V3-AC6` -- THE LIVE TABLE, UNTOUCHED. **PASS**

The identical command, run twice, bracketing the whole exercise.

| | BEFORE `18:45:19Z` (pre-`V3-AC4`) | AFTER `18:55:31Z` (post-`V3-AC4`/`AC5`) |
|---|---|---|
| QBER | `fixed_income` / `Volatility` | `fixed_income` / `Volatility` |
| UVXY | `equity` / `Volatility` | `equity` / `Volatility` |
| VXX | `equity` / `Volatility` | `equity` / `Volatility` |
| PDBC | `equity` / `Commodities` | `equity` / `Commodities` |
| frame | Count **4**, ScannedCount **285**, no `LastEvaluatedKey` | Count **4**, ScannedCount **285**, no `LastEvaluatedKey` |

**ALL FOUR ROWS IDENTICAL BEFORE vs AFTER: True.** Neither response carries a `LastEvaluatedKey`, so
the Count is the whole filtered result and not a page of it -- the trap `--no-paginate` carries.
The table could not have moved: no write API was called at any point in this cell.

*Denominator:* 4 of 4 rows x 3 attributes across 2 reads; Count 4 of ScannedCount 285 both.

### `V3-AC7` -- JUDGMENT. **RECORDED, NO VERDICT.** Graded by `3.0.0_SA_CVO~Z` at L9.

Eight readings are recorded in the proof instance. The load-bearing ones:

| | fields |
|---|---|
| the guard OWNS (`YANG_OWNED_FIELDS`, `:207-211`) | `asset_class`, `sub_asset_class`, `name` |
| the seeder WRITES to Yang (`UpdateExpression`, `:306-317`) | `asset_class`, `sub_asset_class`, `name`, `last_updated`, `updated_by` |
| R1 / `AT5-s-8` WRITES (decomp `:190-208` @`6c7e292c93`) | `asset_class`, `sub_asset_class`, + `management_style` (VNQ only) |

Intersection 2 (`asset_class`, `sub_asset_class`); R1 writes but the guard does not own
`management_style` (1, VNQ) -- **which the seeder never writes at all**, so no re-seed can revert it
by any path; the guard owns but R1 does not write `name` (1).

**The per-field probe** -- the guard exercised one field at a time, the live row agreeing on every
other owned field:

```
FIELD PROBED       IN TUPLE  rc   OUTCOME
asset_class        YES       1    REFUSED, 4 [PRESERVED] line(s)
sub_asset_class    YES       1    REFUSED, 4 [PRESERVED] line(s)
name               YES       1    REFUSED, 4 [PRESERVED] line(s)
last_updated       no        0    WROTE THROUGH, no conflict raised
sector             no        0    WROTE THROUGH, no conflict raised
```

**The `name` asymmetry, measured rather than assumed.** The guard owns `name` and R1 does not write
it, so the guard could in principle refuse for a reason the retag never caused. The mutant control's
fixture sets `name=<ticker>` and therefore *shows* name conflicts -- but that is the fixture, not the
world. Read live: `name` **AGREES on 4 of 4** (VXX `iPath Series B S&P 500 VIX Short-Term Futures
ETN`, UVXY, QBER, PDBC all exact), so no spurious refusal arises for these members and the fixture's
name conflicts are an artifact.

**What the guard protects is what the table serves AT RE-SEED TIME**, not a value compiled in: the
four members' live `asset_class` today is `equity`/`equity`/`equity`/`fixed_income`, i.e. R1's retag
has not yet run, so at this instant seeder and table AGREE and no `asset_class` conflict would be
raised at all. The guard becomes load-bearing for these rows only **after** R1 writes.

---

## 3. SURPRISE ROWS FILED (4)

All appended to `org/missions/D4/POSN/POSN_ASTTAX/surprise-channel/investigations/INVESTIGATION_v1.md`
(97 -> 101 row ids, 45 -> 49 fenced blocks, every block re-parsed after the write, pure ASCII, 0 CR).

| id | one line | class / hazard |
|---|---|---|
| `POSN_ASTTAX-Z-W21-S1` | **The downstream cell's acceptance instrument cannot fail.** `AT5-s-8` is recorded as reading this guard by a DRY RUN expecting `0 PRESERVED`; the guard computes conflicts at `:295` only `if upload`, so a dry run makes **0 `get_item` calls** and `0 PRESERVED` / rc=0 is the only value that path can emit. Measured: a dry run over a store that would lose 4 of 4 five-class values reads **identically** to one with nothing to lose. | OBSERVATION / **ARMED**, disarm `2.0.0_SA_COO~Z` |
| `POSN_ASTTAX-Z-W21-S2` | **`V3-AC2`'s invocation, run as written, checks nothing** -- 0 of 0 files, rc=0, while its `<expect>` names the changed `.py` as subject. Both arms run and recorded. | OBSERVATION / **ARMED**, disarm `2.0.0_SA_COO~Z` |
| `POSN_ASTTAX-Z-W21-S3` | **A third read-only scan where the preflight declares two**, to ground `V3-AC7`'s `name` question on a live value rather than the fixture's synthetic one. Read-only, no write, same IAM posture; settled it favourably. | OBSERVATION / INERT |
| `POSN_ASTTAX-Z-W21-S4` | **The module docstring now contradicts its own exit contract** -- `:13-19` still promises "Idempotent ... Safe to re-run at any time" with no `--force` in Usage, while the code refuses and exits 1. Not edited, deliberately. | OBSERVATION / INERT |

`W21-S1` is the one a reader should look at first: it is about **another cell's** acceptance reading,
it is invisible from inside that cell, and every failure mode of the dry run points toward "pass".

---

## 4. WHAT WAS DELIBERATELY NOT DONE

- **The seeder was never run against the live table.** `--upload` was never passed in this cell.
- **`V3-AC2`'s invocation was not repaired** and **the guard's dry-run path was not changed** -- the
  REFUSAL CLAUSE forbids repairing a criterion; both are rows for their owners.
- **The module docstring was not aligned** even though the `<paths>` grant covers the file: extra
  bytes would make the applied file differ from the bytes round 4 measured, and their byte-identity
  is itself a `V3-AC1` corroboration.
- **Nothing outside the four granted paths was touched** -- no decomposition, no `AT5-s-8`, no
  neighbouring defect.
- **Round 4's measurement was not re-derived** -- the `<decomp_ref>` names it a READ-dependency.

---

## 5. RE-RUNNING THE CONTROLS

`v3_mutant_control_re.py` and `v3_dryrun_inertness_probe.py` in this directory are **byte-identical
copies of the scratch files that produced the recorded output**. To re-run, place them plus
`u3_ac1_before_control.py.ROUND4COPY.txt` (renamed back to `u3_ac1_before_control.py`) in a
`.scratch/` directory at the root of a worktree carrying the patched file, and run from that root.
The harness asserts the machinery's sha256 and the pre-patch blob before doing anything, so a wrong
input fails loudly rather than producing a plausible number.
