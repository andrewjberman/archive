# BRIEF -- make comp-read's ENUMERATION un-skippable: the denominator must survive any filter a seat puts after it

**From:** `0.0.0_AB_MSTR` (carrier; measured the findings, adjudicates nothing). **For:** whoever Andrew hands this to
(the natural home is `NFRA_COMPEFFICACY`, the comp-tool efficacy project, as L5 input for its next round; a
standalone project is equally legal -- the handoff decides). **Authority:** Andrew-direct, verbatim in s.1; ledger
`LD-0526`. **Vintage of every measurement:** the laptop worktree at 2026-09-03 05:4xZ, origin/CLOUD @`800b85c1a2`.

Written to be cited line by line: every outcome below has an id (`BR-n`), an owner lane, a mechanism, a red-first
acceptance, a cost and a non-application. Numbers are measured; nothing here is a design preference.

---

## 1. His words, verbatim, in order

> THat enumeration is key, thats the entire point of comp-read, need to make sure it cant be skipped, look into it
> and propose solutions to that end

> Recs agreed, spec it into a brief, I will hand off to somebody

*(The trigger was a seat's command that piped `comp-read <file> --enumerate '<regex>'` through
`grep -E '^\s+[0-9]+ '`, keeping the hit rows and dropping every line that carries the count.)*

## 2. What is true today, measured

| fact | where | what it means |
|---|---|---|
| The enumeration summary is print-only, to stdout, and comes FIRST | `.tools/comp-read` `_enumerate` (:436-512): the `ENUMERATE: N hit(s) across L lines / S section(s)` line, the whole-value vs substring split, the fragment WARN, the BANDS table and the `0 hit(s). THE DENOMINATOR ABOVE IS THE POINT` notice are printed at :471-501; the hit rows follow at :505-506 in the grammar `"    %6d  %-9s %s"` (line, band, text) | any row-shaped filter keeps the rows and discards every carrier of the claim |
| A bad pattern is an ERROR line, also stdout | :441-442 | the same filter discards it |
| The tool has no filtering or width flags | `main` help (:7): `--enumerate`, `--limit`, `--page`, `--budget` only | seats reach for `grep`, `head`, `cut` because the tool offers nothing else |
| Three outcomes collapse into one empty output under a row filter | zero hits (no rows), a bad pattern (ERROR filtered), a blocked run | an empty result reads as "absent" every time; absence, error and silence are byte-identical |
| The rail hook cannot see a filtered comp-read | `.tools/hooks/comp-tool-hud.sh` :183 exits 0 on any command containing `comp-` ("already a comp-tool reference"); its pipe-receiver detection (:118) recognises only grep-class receivers, never `head`, `tail`, `cut`, `awk`, `sed` | no nudge, no deny, no log; the CLAUDE.md line "never head ANY census" has no mechanism |
| The rate is unmeasurable | `org/mcp/comp-which-rail.log`: 1 comp-read row in 48,533 lines; `org/mcp/comp-tool-runs.jsonl`: 768 comp-read rows in the last 2,000, 210 of them enumerations, but `args_head` records the tool's own argv, never the shell pipe after it | nobody knows how often the summary is filtered; the exposure is large (210 enumerations in the last 2,000 tool runs) |
| Independent corroboration | round-2 deliverable finding `T2-F1`/`T2-F2` of `NFRA_COMPEFFICACY` (`3.0.0_SA_CVO` 93170): "comp-read --enumerate writes no rail row"; "comp-read --at beyond a file's range has no NOT_APPLICABLE voice" | a second instrument found the same hole the same night |

## 3. The three outcomes he agreed, as specifications

### BR-1 -- Every hit row carries its claim; zero and error are rows too (tool-side, un-skippable by construction)

**Owner lane:** the comp-tool engine (`0.8.0_AE_CloudComp` class as executor under a `2.0.0_SA_COO` task order;
`.tools/comp-read` is the artifact). **Mechanism, in `_enumerate`:**
1. Row grammar becomes `line  band  WHOLE|SUB  hit i/N  text` -- each row states whether it is a whole-value or
   substring match and its ordinal over the total, so any surviving row carries the denominator.
2. A zero-hit run emits ONE row in the same grammar with line `0`, band `ENUMERATE`, tag `ABSENT`,
   `hit 0/0`, and the text `scanned L lines / S sections; pattern absent from this file` -- a row filter cannot
   turn a zero into silence.
3. A pattern error emits ONE row with line `-1`, band `ERROR`, the message as text -- a row filter cannot turn
   an error into silence.
4. The summary block is printed FIRST (unchanged) and again LAST as a one-line trailer
   `ENUMERATE-END: N hit(s) | W whole | S sub | <band counts>` -- a `tail` keeps the trailer, a `head` keeps
   the header.
**Acceptance, red-first, exercised through the exact filter that caused this brief
(`| grep -E '^\s+[0-9]+ '`):** (a) a 3-hit file -> every surviving row carries `hit i/3` and `WHOLE|SUB`;
(b) a 0-hit file -> exactly one row survives and reads `ABSENT`; (c) a bad pattern -> exactly one row survives
and reads `ERROR`; (d) negative control on the pre-change build: (b) and (c) yield EMPTY. The test battery
under `.tools/tests/` gains one arm per case. **First cell before any edit:** a census of every consumer that
parses comp-read's row grammar (`comp-find 'comp-read' .tools/ --band CODE`), because a grammar change breaks
a parser silently; each consumer is updated in the same task order or the grammar change carries a `--legacy-rows`
flag for one round. **Cost:** ~20 characters of row width; ~40 lines of code. **Non-application:** the digest
mode (`--for`) is untouched; `--json` (BR-3) carries the same fields structurally.

### BR-2 -- The rail refuses a filtered census, and measures the rate (rail-side; the mechanism "never head a census" lacks)

**Owner lane:** `1.0.0_SA_CTO` (`.tools/hooks/comp-tool-hud.sh` is `ANY_EXEC_OR_AE`); this is a GATE and his word
for it is s.1 ("Recs agreed"). **Mechanism, in the hud hook's segment classifier:**
1. New class `CENSUS-FILTERED`: a segment whose lead is a census tool (`comp-read`, `comp-find`, `comp-surprise`,
   `comp-schedule`) and whose tail pipes into `grep`, `egrep`, `rg`, `head`, `tail`, `cut`, `awk`, `sed` or `wc` is
   DENIED, with a message that names the tool's own flags (`--limit`, `--page`, and BR-3's `--width`, `--band`,
   `--json`) and the audited escape `# rail-checked: <why>`.
2. Exemptions, stated so the rule cannot kill itself: a filter whose pattern contains `ENUMERATE` or
   `DENOMINATOR` (it admits the summary); receivers `tee`, `cat`, `less`; file redirects; any pipe-receiver
   command whose lead is NOT a census tool (`ps | grep` stays free, as today).
3. Every census-tool segment with a trailing pipe is logged to `org/mcp/comp-which-rail.log` as
   `CENSUS-PIPE  ALLOW|DENY  q=<80 chars>` -- the measurement that does not exist today.
4. The `comp-` early exit at :183 moves BELOW this classifier so a comp-tool segment is classified before it is
   excused.
**Acceptance, red-first, in the existing falsifier `.tools/comprail-gate1-fptest.sh`:**
`comp-read f --enumerate x | grep -E '^\s+[0-9]+ '` -> DENY; `... | grep -E 'ENUMERATE|^\s+[0-9]+ '` -> ALLOW;
`comp-find p --files | head` -> DENY; `comp-read f --for q | tee o.txt` -> ALLOW; `ps -ef | grep x` -> ALLOW
(unchanged); `... | head  # rail-checked: reading my own scratch output` -> ALLOW + audit row; and the pre-change
hook must read ALLOW on every one of the DENY cases (the red). **Cost:** one more pattern test per Bash call
(milliseconds, the same order as the T1 rail). **Non-application:** files outside the repo corpus (CLAUDE.md
Rule 21 limb iii) -- a census tool run on a scratch file is not a repo census; the hook keys on the lead verb,
not the path, so this limb is stated rather than enforced.

### BR-3 -- Remove the reasons to pipe (tool-side flags; the summary is never optional)

**Owner lane:** same executor as BR-1. **Mechanism:** `--width N` (truncate the text column; replaces `cut`),
`--band <BAND>` (show only that band's rows; the BANDS table still prints in full; replaces `grep` on a band),
`--json` (one object `{summary:{hits, lines, sections, whole, sub, bands, warn}, rows:[...]}` with `summary`
REQUIRED, so a script consumer receives the denominator whether it asked or not). **There is no `--rows-only`,
by design.** **Acceptance:** `--json` output validates against `org/standards/COMP_READ_ENUMERATE.schema.json`
(new, minimal, `summary` required); `--band X` on a file with hits in two bands prints both band counts and only
X's rows; `--width 40` never touches the summary lines. **Cost:** ~60 lines. **Non-application:** the digest mode.

## 4. Sequencing and dependencies

```
  BR-1 (rows carry the claim)  ----+
                                   +--> BR-3 (flags; --json reuses BR-1's row fields)
  BR-2 (the rail refuses)      ----+     BR-2's DENY message names BR-3's flags once they exist; until then it
                                         names --limit/--page and the rail-checked escape.
```
BR-1 and BR-2 are independent and can run in parallel at two seats. BR-2 is the only gate and is the only piece
that needs his word; s.1 is that word.

## 5. What this brief does NOT ask

- No retro-audit of past filtered runs (unmeasurable; the log did not carry the pipe).
- No change to `comp-find`'s own output (its denominator line is already first and its `--files`/`--band`/
  `--limit` flags exist); BR-2 covers it at the rail only.
- No monitor, no alarm, no notifier (moratorium stands).
