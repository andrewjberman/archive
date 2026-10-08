# Fresh-seat run, round 7 (TO LGIC_BLANKFIX.TO-BF-v-2) -- 0.9.0_WK_LGIC_BLANKFIX~5

Worktree `C:/tmp/wk-blankfix-5`, branch `wk-LGIC_BLANKFIX-5`, a fresh copy of the trunk. Python on this box is 3.12.10 (the README asks for 3.9 or later).

## Instructions found

Files and tools read, in order, to find the written instructions:

1. `README.md` (root) -- read lines 1-40 and searched it for "logic", "lgic", "naming". The only hit is line 279, "Follow naming: `opal-{content-type}-{purpose}`" (a convention, not a command). It names no naming check and no `infra/logic/`. Not followed.
2. `AGENTS.md` (root, 54 lines) -- read whole. It is the Codex seat startup; no mention of a naming check. Not followed.
3. `CLAUDE.md` (root; already in my context) -- rule 30 ("EVERY NEW PIPELINE IS BUILT TO LGIC") names `infra/logic/02_DOCTRINE.md` and `lib/opal_naming.py address()`/`name()`, and says "the commit-time naming gate grades names". It gives no command that runs the check across the repository.
4. `comp-which "how do I run the naming check that grades every Terraform name"` -- "NO CURATED RULE MATCHED"; candidates were comp-schedule, comp-similar, comp-transform. Not useful.
5. `ls infra/logic` -- 14 files including `README.md`. I chose it from the folder name `logic` (CLAUDE.md rule 30 had pointed at that folder).
6. `infra/logic/README.md` (157 lines) -- read whole. The section **"Run the naming check"** is the instructions I followed. Passage: "The check that grades every Terraform name in the repository against the canon is one command. Run it from the repository root: `python lib/opal_naming.py census --all-roots`", followed by "(`python lib/opal_naming_rootcheck.py all --map infra/logic/registry/root_map.json` is the same run.)", then "What the output is, line by line", "The last line, field by field", and "What `ok=True` means, and what it does not".

How I got to file 6 depended on CLAUDE.md rule 30 and the folder name; neither root document (README.md, AGENTS.md) leads there.

## Steps run

All commands run from the worktree root. Nothing asked for AWS or the network; no step is SKIPPED-LIVE. The README says the run "reads the repository only".

1. `python --version` -> `Python 3.12.10`. Passage: "Python 3.9 or later is all it needs."
2. `python lib/opal_naming.py census --all-roots > <file>` (passage: "Run the naming check" and "Save it with ..."). Output captured to a file in the worktree root, then read. Exit code 0, wall time 13.8 s (README: "about 15 seconds"). stderr empty. 166 lines (README: "about 170"). First line `ROOTS total=87 mapped=13 unmapped=74`. Last three lines:
   ```
   TOTALS completed=13 stopped=0 right=141 fix=271 not_asked=32 pattern=8 carded=0 refused=0 hole=1
   HOLE-CLASSES carded=0 source_bucket=0 event_rule=0 unknown_word=0 other=1
   OTHER-HOLE investor-reporting/intake || SCHEDULE irpt-intake-poll -> partial form irpt-intake-poll-{cadence}; could not fill {cadence}: no cadence row for this name  [infra/aws/terraform/investor-reporting/intake/main.tf:122]
   ALL-ROOTS ok=True roots_total=87 mapped=13 unmapped=74 completed=13 stopped=0 items=453 right=141 fix=271 not_asked=32 pattern=8 carded=0 refused=0 hole=1 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=0 other_holes=1 stale_hints=0 uncounted=301
   ```
   (The saved file was then deleted, see "Written for the run".)
3. `python lib/opal_naming_rootcheck.py all --map infra/logic/registry/root_map.json | tail -2` (passage: "is the same run") -> last line identical to step 2; exit code of python 0.
4. `python lib/opal_naming.py census --all-roots | tail -1` -> the same last line; exit code of python 0 (passage: "Exit code: 0 when the last line reads `ok=True`").

Reading the last line against the README's field table: `ok=True`, `stopped=0`, so every mapped root completed; 13 of 87 roots are graded, 74 are UNMAPPED and not graded; `hole=1`, `uncounted=301` are names not settled, and per the README "The check is done for a root only when that root is mapped, `stopped` is 0, and its `hole` and `uncounted` are 0" -- so the check ran to its totals, and the repository is not done by that test.

## Final output

```
ALL-ROOTS ok=True roots_total=87 mapped=13 unmapped=74 completed=13 stopped=0 items=453 right=141 fix=271 not_asked=32 pattern=8 carded=0 refused=0 hole=1 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=0 other_holes=1 stale_hints=0 uncounted=301
```

## Written for the run

Nothing was written for the run as the order means it: no skip list, card, configuration or registry file; no file edited outside the deliverables folder except this order's own `<status>` flip. Disclosures:

- In step 2 I redirected the output to two files in the worktree root (`.scratch_run.txt`, `.scratch_err.txt`) to read it. They were my own redirect targets, not anything the check needs (steps 3 and 4 ran with a pipe and wrote no file). I deleted both before writing this record; `git status --porcelain` afterwards showed only the order's status flip.
- The runs created ignored files only (`lib/__pycache__/`, `.tools/__pycache__/`, `org/modules/graph/__pycache__/`, `.comp-graph/`, and comp-which logs under `org/mcp/` from my one `comp-which` call). They are gitignored and not part of `git status --porcelain`.

## Where the instructions fell short

1. **Finding them.** Neither root document (`README.md`, `AGENTS.md`) mentions `infra/logic/` or the naming check; `comp-which` does not know it. A newcomer reaches `infra/logic/README.md` only through CLAUDE.md rule 30's pointer to `infra/logic/02_DOCTRINE.md` or by guessing the folder name `logic`. Rule 30 itself names no command. What was needed: one line in root `README.md` (or in CLAUDE.md rule 30) giving `python lib/opal_naming.py census --all-roots` or pointing to `infra/logic/README.md#run-the-naming-check`.
2. **Python version.** The README says "Python 3.9 or later"; this box has 3.12.10. It ran. A seat with 3.9 was not tried.
3. **"Save it" invites a write.** The README says to save the output with `> <file>`, but gives no place for the file; a newcomer choosing a path inside the worktree creates an untracked file (I did, then deleted it). Saying "or pipe to `tail -1`; save only outside the repository" would keep the repository clean.
4. **Count of lines.** README says "about 170 lines"; measured 166. Within "about".
5. **The result is not "done".** The README states `ok=True` is soundness only; with `fix=271`, `hole=1`, `uncounted=301` and 74 unmapped roots, the run reaches its totals but the estate is not clean. The README is explicit about this, so it is not a shortfall, only recorded.
6. The run did not stop anywhere; nothing was written to get past a stop.
