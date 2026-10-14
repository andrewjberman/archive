# OPAL_BBGTML.TO-Z6-R6 -- report: portal_lookup.py quotes the DATA vintage, never the write time

**archetype:** IMPLEMENT
**secondary_archetypes:** VALIDATE

**Seat** `0.7.0_AE_CloudOps~ZS` | **issuer** `2.0.0_SA_COO~ZB` (@`80e4fc6c61`, GO msg 33859 acked) | **ruling** CTO msg 33851 | **risk** LOCAL
**Order** [OPAL_BBGTML.TO-Z6-R6.portal-lookup-quotes-data-vintage.md](file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R6.portal-lookup-quotes-data-vintage.md)
Ran 00:41Z -> 00:58Z, ahead of the HELD TO-Z6-R3. Nothing here releases R3.

## Verdict

**Both criteria PASS.** Two files changed, exactly the two named. One row filed (Z-S19) for the twin doc the order
barred me from editing. The override was used once, for the one commit, and its audit line is below.

## The defect, and what the fix does

`platinum/mdpf/*/aum-metrics.json` carries no `as_of_date`. The old fallback printed
`VINTAGE: field 'as_of_date' not present -- quote LastModified and say it is file-time, not data-time`, so the BG seat
quoted **2026-10-13** (the write time) when the data's true vintage was **2026-10-12** -- every MDPF answer off that
surface read one trading day too fresh.

The vintage order now applies to **every** channel, not just `mdpf-platinum`:

| order | branch | output |
|---|---|---|
| 1 | the channel's `date_field`, present in the doc | `VINTAGE (<field>): <value>  <- quote this with every figure` (unchanged) |
| 2 | else `_provenance.source_vintages`, one distinct date | `VINTAGE (_provenance.source_vintages): <date>` |
| 2b | else several distinct dates | each `<source>=<date>` printed, then `VINTAGE (_provenance.source_vintages, oldest of N): <date>` |
| 3 | else nothing | `VINTAGE: none in the object -- LastModified <ts> is the WRITE TIME (claim: inferred), never the data vintage; say so when quoting` |

The old `LAST-MODIFIED:` line is relabelled **`WRITE TIME (LastModified):`**, so no line in the output can be read as a
vintage. The string `quote LastModified` no longer appears anywhere in the file (verified on the post-edit bytes).

`refs/BUCKET_ALLOWLIST.yaml`: the `platinum/mdpf/` `vintage_field` carries that same three-step order in place of the
flat `as_of_date`. The file still parses (`yaml.safe_load`, against a bad-YAML control that raised `ParserError`), and a
full walk of the parsed tree confirms it is the **only** one of the three `vintage_field` values that changed.

`portal_lookup.py` `sha256 65c9dd2d...` -> `b7f5ab25...`, 389 -> 405 lines, LF throughout, 0 non-ASCII.
`py_compile` OK; `ruff --target-version py39` all checks passed.

## Criteria

### AC1 -- PASS, exit=0

```
expected vintage (the object's own _provenance.source_vintages): 2026-10-12
ARM 1: VINTAGE (_provenance.source_vintages): 2026-10-12  <- quote this with every figure
ARM 2: VINTAGE (data_as_of): 2026-10-12  <- quote this with every figure
ARM 1: PASS
ARM 2: PASS
R6: PASS
exit=0
```

ARM 1 names `_provenance.source_vintages` and the date the check read **from the object itself**, and no
`quote LastModified` line prints. ARM 2 (the control path, `json/macro/macro_data.json`) still names `data_as_of`. The
difference control -- the same check reading `ARM 1: FAIL / ARM 2: PASS` on the pre-edit bytes -- is recorded in the
issuance commit and was not re-run.

### AC2 -- PASS

`2 files changed, 21 insertions(+), 4 deletions(-)`, and `--name-only` over the whole commit lists only
`portal_lookup.py` and `BUCKET_ALLOWLIST.yaml`. Reported both ways: the literal `HEAD~1 HEAD` form agreed this time
because HEAD was still the R6 commit, and the pinned `b195dc14fe~1 b195dc14fe` read agrees with it. (On R2 the literal
form had returned empty because a peer commit moved HEAD, so it is worth stating which read was used.)

## Exercised beyond AC1 -- the multi-date arm, which no live object can reach

AC1's object carries exactly **one** source vintage, so AC1 cannot reach branch 2b at all. A read-only sweep of the four
`platinum/mdpf/{49financial,global,cottonwood,inflection}/aum-metrics.json` objects found **all four** with
`as_of_date=None`, 1 source, 1 distinct date (`2026-10-12`) -- so **no live object exercises the oldest-of-N logic**.
Rather than leave the riskiest branch unproven, seven shapes were driven through the **real** `cmd_get` in the deployed
file with only the S3 boundary (`fetch_object`) stubbed -- the vintage order, the sort and the oldest pick are the
shipped code, not a copy:

| arm | shape | result |
|---|---|---|
| A | 3 distinct dates | each source printed, `oldest of 3`, quoted `2026-10-09` |
| B | 2 sources sharing one date | single-date form, no per-source lines |
| C | nothing to go on | WRITE TIME wording, claim inferred |
| D | `as_of_date` **and** provenance both present | `VINTAGE (as_of_date)` -- date_field wins, correct precedence |
| E | `source_vintages` present, all values empty | falls through to WRITE TIME, **no IndexError** |
| F | `source_vintages` the wrong type (a list) | no crash -- the isinstance guard holds |
| **G** | lexically-first source holds the **newest** date | printed **`2026-10-07`**, the oldest |

**Arm G is the one that matters.** In arm A the oldest date and the lexically-first source name coincided, so A alone
could not distinguish "oldest date" from "first source" -- a passing arm that proves less than it appears to. G breaks
the tie: "first source" would have printed `2026-10-12`, and the code printed `2026-10-07`. The oldest semantic is
proven rather than coincidental.

**Still an evidence limit, stated plainly:** arms A-G stub the S3 boundary. They prove the shipped function's logic;
they do not prove that a real publisher ever writes multi-source provenance in this shape. ABSENT is not
EXERCISED-AGAINST -- the first real multi-source object is still the first live test of 2b.

## PORTAL_RETRIEVAL.md -- read, NOT edited, and why

Step 3 asked whether the twin states a vintage rule this edit contradicts. **It does not.** Line 13, rule 2 reads
`ANSWER FROM data_as_of (MDPF uses period / as_of_date -- same meaning: the data's as-of, never the run date)` -- R6
*implements* that rule; the rule is simply silent on what to do when the named field is absent, which is the gap R6
fills.

What **is** stale is its channel table: **line 43** still prints `as_of_date` as THE vintage field for `mdpf-platinum`,
a field absent from all four objects measured. `portal_lookup.py:46` calls that file the twin and says "keep in sync",
so the divergence is knowing. Filed as **Z-S19** (OBSERVATION / INERT) rather than edited -- the order caps the cell at
two files, and my override grant covered those two only. I did not stretch it to a third file.

Line 42 is the separate `mdpf` row (`period`) and is **not** this finding; the distinction was pinned by printing the
bytes of each line rather than grepping.

## The audited override

The order granted one `GIT_COMMIT_AUTHOR_OVERRIDE=TIER0_UTILITY` because lane `TIER0_UTILITY` refuses this seat.
`org/git-author-override-audit.sitez.log` went 3175 -> 3178 lines, and the three new lines are:

```
2026-10-14T00:51:02Z OVERRIDE  0.7.0_AE_CloudOps~ZS  2  (--author-override TIER0_UTILITY applied) act=8732e547cab1 paths=2:.../BUCKET_ALLOWLIST.yaml|.../portal_lookup.py
2026-10-14T00:51:05Z OVERRIDE  0.7.0_AE_CloudOps~ZS  2  (--author-override TIER0_UTILITY applied) act=8732e547cab1 paths=2:.../BUCKET_ALLOWLIST.yaml|.../portal_lookup.py
2026-10-14T00:51:16Z LANDED-2P  0.7.0_AE_CloudOps~ZS  b195dc14fe  paths=2  validate=16.99s  wait=0.17s  hold=3.59s  build=3.04s  ref=0.49s  post-commit=3.64s  attempt=1
```

**Two OVERRIDE lines, ONE act.** Both carry the same `act=8732e547cab1` and the same 2-path set, 3 seconds apart -- the
wrapper evaluates the override twice per act (validate, then commit). A reader counting OVERRIDE lines would score this
as two overrides against a one-override grant; counting distinct `act=` ids gives the true answer, 1. Recorded here so
the audit is not later misread. Commit author is `0.7.0_AE_CloudOps~ZS` and the lane override is what let it land.

## Push state -- MEASURED

`git ls-remote origin box/sitez` read `1fd96abebeda63d3ba0f49cbee7236d47b397173` at 00:58Z; containment tested against
that hash, not the local tracking ref, with both controls passing:

| commit | what | push state |
|---|---|---|
| `b195dc14fe` | **the two-file cell** | **on origin @`1fd96abebe`** |
| `ce59b6de56` | row Z-S19 | **LOCAL** -- pending this box's scheduled `box-sync` |

The deployed tool is live at `sha256 b7f5ab25...`, 405 lines -- it runs from the working tree whenever the BG seat
answers a question, so the next answer already uses the new order.

## Not done, and why

- **The `<status>` flip of TO-Z6-R6 is the issuer's**, per the report clause. Left alone.
- **TO-Z6-R3 stays HELD** -- unchanged by this order, which says so explicitly. Its worktree `C:/tmp/zs-z6-r3` remains
  locked with no R3 edits.
- **PORTAL_RETRIEVAL.md:43 not corrected** -- out of the write surface; Z-S19 carries it with suggested text.

## ADDENDUM, 01:06Z -- AMENDMENT 1 landed: `PORTAL_RETRIEVAL.md:43` now carries the vintage order

The issuer drained R6 (`b195dc14fe` on origin, AC1/AC2 PASS), reopened the order `in_progress` @`a8826454a8`, and
issued **AMENDMENT 1** on the very row this cell filed -- Z-S19 -- with the same one-commit override. GO msg 33870,
acked. Notes 1 (multi-date arm stub-only) and 2 (two override lines, one act) were taken to the round's drain-end
record, so neither is lost.

**Commit `31566aa49d`.** ONE table cell, one file, `refs/PORTAL_RETRIEVAL.md` line 43, the `mdpf-platinum` row's
vintage column:

| | value |
|---|---|
| before | `` `as_of_date` `` |
| after | `` `as_of_date` ``, else `` `_provenance.source_vintages` `` (oldest); LastModified is write time only |

That matches the allowlist and the tool, so the twin and `portal_lookup.py:46`'s "keep in sync" obligation agree again
-- which is exactly what Z-S19 named. **Row Z-S19's disarm remains the issuer's**, not this seat's; the remedy landing
is not the disarm.

**Nothing else moved**, and it was checked rather than assumed: the anchor string's count was asserted `== 1` before the
write (line 42, the separate `mdpf` row, untouched); the file keeps **79 lines**; row 43 keeps **5 table pipes**,
matching the header row; `sha256 06cb1ee8...` -> `eb559e8dca...`, 6670 -> 6748 bytes.

**Encoding, because this file is one of the mixed ones.** It already carried **26** non-ASCII characters (23 em-dashes,
2 `≈`, 1 `→`). The edit is binary with ASCII-only replacement text, so the count reads 26 before and 26 after and no
reader's encoding assumption changes -- CLAUDE.md's "all out, or every reader explicit" is not engaged by this edit
because the edit neither adds nor removes any. Worth flagging for whoever next touches the file: the naive detector
prints **52** here, and that is a BYTE delta (26 chars x 3 UTF-8 bytes, minus 26), never a character count.

`commit-gate` again reported `checked 0 of 1 file(s)` -- a `.md` is outside its set, the third suffix this session
(`.ps1`, `.yaml`, `.md`). The language-appropriate instrument was the structural read above: pipe count against the
header, line count, non-ASCII count, and the pre-write anchor assertion.

**The override audit, second observation.** `org/git-author-override-audit.sitez.log` 3213 -> 3216 lines:

```
2026-10-14T01:04:59Z OVERRIDE  0.7.0_AE_CloudOps~ZS  1  (--author-override TIER0_UTILITY applied) act=2b06380c0b36 paths=1:.../PORTAL_RETRIEVAL.md
2026-10-14T01:05:03Z OVERRIDE  0.7.0_AE_CloudOps~ZS  1  (--author-override TIER0_UTILITY applied) act=2b06380c0b36 paths=1:.../PORTAL_RETRIEVAL.md
2026-10-14T01:05:11Z LANDED-2P  0.7.0_AE_CloudOps~ZS  31566aa49d  paths=1  validate=14.76s  ...  attempt=1
```

Again **two OVERRIDE lines for one act** (`act=2b06380c0b36`, 4s apart). This is the second distinct act showing it, so
the pattern is **systematic, not a one-off coincidence** -- which strengthens the note sent at the drain: an auditor
counting OVERRIDE lines over-reports overrides by 2x, and the sound denominator is distinct `act=` ids. Two acts, two
grants, four OVERRIDE lines.

**Push state re-measured at 01:06Z** (`git ls-remote origin box/sitez` = `43bde59c58`, control passing):
`b195dc14fe`, `ce59b6de56`, `e9b1d65b70` **on origin**; `31566aa49d` **LOCAL**, pending `box-sync`. The deployed twin is
live at `sha256 eb559e8dca...`, 79 lines, 26 non-ASCII.

## Compiler Tools

| tool | result |
|---|---|
| `py_compile` on `portal_lookup.py` | PASS |
| `ruff check --target-version py39` | PASS, all checks passed |
| `yaml.safe_load` on `BUCKET_ALLOWLIST.yaml` + full tree walk | PASS -- parses; 1 of 3 `vintage_field` values changed, the right one, against a bad-YAML control that raised |
| real-`cmd_get` driver, S3 boundary stubbed (arms A-G) | PASS 7 of 7, G discriminating |
| read-only S3 GET x4 (`aum-metrics.json`) + x2 inside AC1 | PASS -- all four `as_of_date=None`, 1 distinct date each |
| `r6_vintage_check.sh` (AC1) | PASS, exit=0, both arms |
| `.tools/safe-commit.sh` x2 | `b195dc14fe` (override, 2 files), `ce59b6de56` (row). commit-gate clean for 1 of 2; naming-gate PASS 0 graded; surprise-row gate 1 new of 19 |
| `git ls-remote` + `merge-base --is-ancestor` with 2 controls | PASS |

**What worked.** Asserting `count == 1` on each replacement target before writing meant the one shape I got wrong
(nothing, this time) would have failed closed rather than half-applying -- the same guard that caught the CRLF mistake
on R2. Stubbing only `fetch_object` let the real shipped function be exercised against shapes S3 does not contain.

**What failed.** Nothing refused. One self-inflicted detour: my first YAML verification probe looked up
`d['buckets'][...]` when the top-level key is `allow`, printed `None`, and read as "the edit did not land". A full
recursive walk of every `vintage_field` resolved it in one call. A `None` from a hand-typed key path is a probe failure,
not a measurement.

**Gap found.** `commit-gate` reported `clean for 1 of 2 file(s)` -- it graded the `.py` and not the `.yaml`. Same shape
as the R2 gap (`.ps1` unexamined), and the same remedy: the gate names what it did not check, so the language-appropriate
instrument has to be run beside it. Here that was `yaml.safe_load` plus the tree walk. Not filed as a row -- it is
fabric tooling outside OPAL_BBGTML's channel and belongs to whoever owns `commit-gate.sh`.
