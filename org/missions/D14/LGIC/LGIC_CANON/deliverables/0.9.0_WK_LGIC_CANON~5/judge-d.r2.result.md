# TO LGIC_CANON.CN-j-5-r2 -- result (judge D, cell CN-j-5, round 2)

**Worker:** `0.9.0_WK_LGIC_CANON~5` · **Worktree:** `.worktrees/wk-lgic-canon-2-5` on branch `wk-lgic-canon-2-5`,
cut from CLOUD at `49b4a5b74a`. **Artifact commit:** `19c9d7d930426ae1e8710332952b95e70970f8a2`.

## What this cell did

Judged all 13 planes named in `CN_TREE_INFLECTION.md` (the INFLECTION tree) on the canon's five axes
(A1 INGESTION, A2 BUCKET STRUCTURE, A3 NAMING, A4 COMPUTE, A5 FORMAT), from `infra/logic/02_DOCTRINE.md`
**alone**, per `CN_SEVERITY.md`'s vocabulary. Wrote
`org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-d.tsv` (header + 13 rows, 9 columns:
plane, A1-A5, rules, reach, why).

## Method

For each plane, the deciding rule per axis was taken from the canon's own rule blocks in `02_DOCTRINE.md`
section 3, preferring an EXACT match against the canon's own printed census lines (object counts and
`VIOLATED-LIVE` / `VIOLATED-DEAD` / `CONFORMANT` tags) over an independent re-derivation, since several of
this tree's planes are the literal objects those census lines describe (matched by exact object count:
opal-data-inf/platinum 8,673 = R6's census line; opal-data-inf/gold 22,836 (221 json residual) -> R11;
opal-data-inf/silver 16,757 (3,066 json) = R4's and R10's census lines; opal-data-inf/bronze 28,614 (4,802
parquet) = R4's and R9's census lines; opal-data-inf/backup/gold_canonical_PRE_REDERIVE 8,805 =
R17's census line; opal-data-inf/_pre_rebuild_backup/.../silver 6,060 = R17's census line;
opal-data-inf/_toolprobe_scratch 1 = R17's census line). Where the tree gave only a plane-level count and
no key-level grain (A3 naming inside the legacy bucket), or where R13's threshold is deferred by Andrew's
word and the canon's own R13 non-application names "the existing EC2 gold runners (49f, inf) ... UNCLASSIFIED"
directly, the verdict is `UNDETERMINED` rather than a guessed `CONFORMS`/`VIOLATES`.

The two monolith silver planes (`orion/inflection/silver/`, `eclipse/inflection/silver/`) are named in the
tree as the destination of `opal-data-inf/silver/`'s migration, "whose canonical twins already exist," both
dated 09-12 (LIVE). This is the shape R18 forbids (a standing shadow/dual-write path) but R18's own worked
census example turns on DURATION ("live status 31d") which this tree does not give for the silver pair, so
A1 on all three silver rows (the legacy plane and its two canonical twins) reads `UNDETERMINED` citing R18,
rather than `VIOLATES` -- the canon's own test (standing vs. migration-in-flight, R19's territory) cannot be
settled from the given facts.

## A-13 seven-rule reach

Per-row `reach` columns plus the last row's tree-wide summary: **REACHED (3 of 7): R14, R17, R19.**
**NOT REACHED (4 of 7): R3, R8, R15, R21** -- R3 needs two MASTERS of one VENDOR (orion and eclipse are two
different vendors/sources for one firm, not two masters of one vendor); R8 needs a GENERAL,
non-firm-attributable plane and every plane in this tree is inflection firm-attributable data; R15 needs a
source served raw AND separately consumed by a derived plane, and no raw-serve route is named for inflection
anywhere in this tree; R21 is unreachable by this tree's own design, per `CN_SEVEN_RULES.json`'s own `_about`
note -- no conformant `state/` plane exists anywhere in the estate, and this tree's backup/scratch/probe
prefixes are R17's territory, not R21's (none of them are `_state/`, `_parity/`, `*_watermark.json`,
`manifests/` or `otp/state.json`-shaped).

**Instrument note, filed as `LGIC_CANON-W5-S2`:** `check_canon_r2.py`'s `j5-reach` subcommand does a
whole-file `\bR<n>\b` regex over every column of every row, so it cannot distinguish a rule this file names
as REACHED from one it names while explaining it is NOT reached -- because my last row's why-text spells out
all four not-reached ids to explain why, the checker's own stdout reads `REACHED (7)` even though this file's
own determination is 3 of 7. The criterion (J5-AC3) still PASSES either way (it only needs `reached`
non-empty), so this is not a criterion failure -- it is the checker's summary line disagreeing with the file
it just scanned. See the row for the full grounding; `3.0.0_SA_CVO` is named as disarm owner because L9 is
where this file's actual content, not the checker's blob-scan line, should be read.

## Blindness

I did not read `judge-c.tsv`, `judge-e.tsv`, `judge-compare-r2.md`, or any other judge's file or output. My
file does not name `judge-c` or `judge-e`. I judged independently from the tree, the canon, `CN_SEVERITY.md`
and `CN_SEVEN_RULES.json` only, per the order's own point: "Agreement you reach by guessing what another
judge would say measures nothing."

## Mutant control (see proof_of_spec.json `controls.mutant` for the full record)

Copied the committed `judge-d.tsv` to `.scratch/judge-d.orig.tsv`, then in place: blanked row 1's A3 cell
(breaks `j5-axes`), replaced every `R<n>` token in row 2's rules/reach/why cells with `XX` (breaks
`j5-cites`), and replaced every A-13 seven-rule token (`R3,R8,R14,R15,R17,R19,R21`) across every row with `XX`
(breaks `j5-reach`). All three criteria read FAIL on the doctored file. The original was copied back; `git
status --porcelain` and `git diff --stat` on the path both read clean/empty (byte-identical restore). All
three criteria then read PASS again, identical to the pre-mutation run.

## What I read (per the order's "Read" list)

`CN_TREE_INFLECTION.md`, `infra/logic/02_DOCTRINE.md`, `CN_SEVERITY.md`, `CN_SEVEN_RULES.json`. The
preloaded workspace CLAUDE.md and auto-memory were in context per every worker's baseline, but no verdict
here cites them -- every citation is to the four files above.

## Surprise filed

`LGIC_CANON-W5-S2` (OBSERVATION, ARMED, disarm_owner `3.0.0_SA_CVO`): `check_canon_r2.py`'s `j5-reach` (and
the identically-shaped `j4-reach`/`j6-reach`) blob-scans the whole row set for `\bR<n>\b`, so it cannot tell
a rule cited as reached from one cited while explaining it is not reached; the checker's own printed
`REACHED (7)` line disagrees with this file's actual 3-of-7 determination. Does not block J5-AC1..AC3 (all
three PASS regardless, since the criterion only needs `reached` non-empty); filed so L9 and the CN-j-7
compiler read the file itself rather than the checker's summary line.
