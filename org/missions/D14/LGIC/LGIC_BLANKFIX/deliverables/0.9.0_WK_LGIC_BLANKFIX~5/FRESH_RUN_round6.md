# FRESH RUN round 6 -- 0.9.0_WK_LGIC_BLANKFIX~5 on LGIC_BLANKFIX.TO-BF-u-7

Worktree C:/tmp/wk-blankfix-5, branch wk-LGIC_BLANKFIX-5, fresh copy of the trunk. Repository plane only. Python on this
machine is 3.12.10 (the order says 3.9). Raw outputs kept in this folder: `run1.out`, `run4.out`, `run5.out`
(`run2.out` and `run3.out` were 108 KB each and byte-identical to each other; deleted, their tails are quoted below).

## Instructions found

Files read to find the instructions, in order:

1. The task order's WORKER FACE (given): it names `lib` nowhere; it says "the check" without a command.
2. `CLAUDE.md` (loaded with the session): no run command for a naming check.
3. `README.md` (repo root), searched for logic / lgic / naming / check: no hit about the naming check.
4. `infra/logic/README.md` (read whole, 65 lines): describes the folder; gives NO command for running the check. Its line 40
   says the onboarding contract "is not pre-built here", which is stale (see the last section).
5. `AGENTS.md` and `lib/README.md`, searched for naming / check: no hit.
6. `comp-which "run the naming check that grades every declared name"`: "NO CURATED RULE MATCHED"; no useful candidate.
7. `python lib/opal_naming.py --help`, then `python lib/opal_naming.py census --help`: the `census` subcommand and its options
   (`--live --repo --report --budget --not-judged --root --map --all-roots`), one-line help each, no instruction on which to use.
8. `comp-find "opal_naming.py census"` (DOC band, outside `org/missions` and `org/audit`) surfaced two documents:
   - `infra/logic/10_ONBOARDING_CHECKLIST.md` (lines 1-40 and 336-366 read). The passage followed is STEP 13, line 344:
     "`python lib/opal_naming.py census --repo --live --report <path>`", and line 350: the census "STOPS at its first RAISE".
   - `docs/briefs/d14-naming-check-blank-fixes-brief-20261007.md` (lines 10-22, 55-66, 175-190, 232-260 read). The passage
     followed is line 15: "The check: `python lib/opal_naming.py census --live --repo`", line 57-60 ("O4 ... on a clean
     checkout and it finishes ... Today the run stops twelve times"), and line 240: "`census --live --repo --budget 600
     --not-judged <cards> --report <file>` with `<cards>` = `NOT_JUDGED_R13.json` (462 cards) plus the 12 scratch cards of F5".
9. After the stop, to find the skip list the brief names by file name only: `git ls-files` filtered for `not_judged`
   (three files, all under `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/`). And, to read the stop, `lib/opal_naming.py`
   lines 1-60 and 2781-2825, and PRD lines 59-64 and 100-104 (named by the order).

## Steps run

Every command run from the worktree root. `--live` is in both documented commands and would pull the live plane (AWS graph);
it was not run: `SKIPPED-LIVE` (checklist line 344 and brief lines 15 and 240 ask for it). `--report <path>` was left off (the
check prints its totals to the screen; a report file is optional in the help text).

| # | command (exactly as run) | passage | rc | last printed line |
|---|---|---|---|---|
| 0 | `python lib/opal_naming.py --help` ; `python lib/opal_naming.py census --help` | help text | 0 | option list |
| 1 | `python lib/opal_naming.py census --repo` | checklist STEP 13 line 344 / brief line 15, minus `--live` (SKIPPED-LIVE) | 3 | `CENSUS: STOPPED on the first RAISE after 2 judged (0 carded): repo IAM_POLICY 'F49ServedAndSourceRead'` |
| 2 | `python lib/opal_naming.py census --repo --not-judged org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R13.json` | brief line 240 (`NOT_JUDGED_R13.json`, 462 cards), repo-held skip list | 3 | `CENSUS: STOPPED on the first RAISE after 1006 judged (75 carded): repo IAM_POLICY 'restricted-prefix-get-put-list'` |
| 3 | same with `.../0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R4.json` | the second repo-held skip list | 3 | identical to step 2 (output byte-identical) |
| 4 | same with `.../0.9.0_WK_LGIC_ENFORCE~4/NOT_JUDGED_S6.r3.json` | the third repo-held skip list | 3 | `CENSUS: STOPPED on the first RAISE ...` after 2 judged, same stop as step 1 |
| 5 | `python lib/opal_naming.py census --all-roots` | `census --help` text only; in neither written document | 0 | the `ALL-ROOTS ok=True ...` line in Final output |

Step 1 stop, verbatim: `CENSUS RAISE repo IAM_POLICY infra/aws/terraform/49f-value-parity/49f_value_parity.tf:67
F49ServedAndSourceRead -- R1.f: 'f49' is in no vocabulary; no registry row resolves it`.
Step 2 stop, verbatim: `CENSUS RAISE repo IAM_POLICY infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:262
restricted-prefix-get-put-list -- R1.f: 'restricted' is in no vocabulary; no registry row resolves it`. Nothing was written to
get past either stop. The check takes one skip list per run, so the three repo-held lists cannot be combined without writing
a new file, which the order forbids. The brief (line 240) says the full run needs R13 plus 12 scratch cards that are not in
the repository.

Step 5 is a different grain: it grades the Terraform names root by root and covers 13 of 87 roots (74 unmapped, 412 items), so
it is not the whole-estate check the two documents describe.

## Final output

```
CENSUS: STOPPED on the first RAISE after 1006 judged (75 carded): repo IAM_POLICY 'restricted-prefix-get-put-list'
ALL-ROOTS ok=True roots_total=87 mapped=13 unmapped=74 completed=13 stopped=0 items=412 right=124 fix=248 not_asked=32 pattern=8 carded=0 refused=0 hole=0 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=0 other_holes=0
```

The first line is the last printed line of the best documented-command run (step 2, the repo-held skip list that gets
furthest); the second is the last printed line of the run that reached totals (step 5, partial grain). The documented
whole-estate command did not finish.

finished: no

## Written for the run

Nothing: no skip list, card, configuration or report file. The run used the repo-held skip lists named in steps 2-4 (read
only). The only files created are the run outputs and this record in this deliverables folder. Python wrote
`lib/__pycache__/` while importing, which is gitignored (`.gitignore:36`) and does not appear in `git status --porcelain`.
`comp-which` wrote a ranking file under `.comp-graph/`, also not shown by `git status --porcelain`.

## Where the instructions fell short

1. `infra/logic/README.md`, the first document a newcomer opens for the naming check, names no command. The command is found
   only through `comp-find` (checklist STEP 13, a firm-onboarding document; or a brief). Its line 40 says the onboarding
   contract "is not pre-built here" while `10_ONBOARDING_CHECKLIST.md` sits in the same folder.
2. The checklist's command (line 344) and the brief's command (line 15) both carry `--live`, which needs the live plane. The
   instructions do not say what to run when only the repository plane is available.
3. The run stops at its first unreadable name even on the documented command: first at `F49ServedAndSourceRead`, and with the
   repo-held list `NOT_JUDGED_R13.json` at `restricted-prefix-get-put-list`. The instructions needed to say either that the
   repository's skip list covers every name in the repository (it does not: R13 stops at the name above), or that a run on a
   fresh copy ends at the stop and what the stop means. The checklist (line 350) says the stop exists and tells the reader to
   fix the row "at its own row", which a person who may write nothing cannot do.
4. The brief names `NOT_JUDGED_R13.json` by file name only; the path (`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/
   0.9.0_WK_LGIC_ENFORCE~1/`) had to be found with `git ls-files`. Three skip lists exist (R13, R4, S6.r3) with no statement
   of which is current, and the check accepts one list per run.
5. `--all-roots`, the one mode that ended with totals, appears only in the help text and covers 13 of 87 roots; no document
   says how it relates to the whole-estate check.
6. The order says Python 3.9; the machine ran 3.12.10.
