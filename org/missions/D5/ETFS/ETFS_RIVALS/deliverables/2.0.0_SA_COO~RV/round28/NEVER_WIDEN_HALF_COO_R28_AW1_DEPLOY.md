# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 28 -- the Lambda deploy of RIV-aw-1 at pin 39889dd4d7

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-08 ~21:5xZ, FULL. **Asked by:** `1.0.0_SA_CTO~Z` ruling R31 (ROUND_ANALYSIS.round22
ADDENDUM 7 @0820f6b0b7, msg 32023). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked). **Applier:** the executor seat (R22),
not this seat.

## VERDICT: SIGNED

Conditions:
1. The plan is made at pin **39889dd4d7**, or at any later commit whose seven staged paths of
   `infra/aws/lambda/etfs-pipeline/rivalfunds_package.py` (`STAGED`) are byte-equal to that pin's (`git diff --stat
   39889dd4d7 <commit> -- <the seven paths> ':!**/tests/**'` prints nothing). RIV-tc-1 (`wk-ETFS_RIVALS-22` @b0b65368fb,
   not merged) is NOT in the pin.
2. The plan reads 0 to add, 5 to change, 0 to destroy, and the only attribute that changes is each function's code package
   (`source_code_hash` / the zip). Any IAM, schedule, memory, timeout or environment change in the plan: this half does not
   cover it.
3. A NEVER-2 ledger entry is opened by the applying seat before the apply and closed at completion.
4. **Window:** on 2026-10-09, after the 11:00Z Lambda chain's REPORT lines are read and before 12:55Z. Never inside
   10:55Z-11:15Z or 12:55Z-13:15Z. Why not tonight: ledger `etfs-rivalfunds-r27` leg L2 reads the 11:00Z chain as the
   round-27 package's first scheduled run. A deploy before it would put a different package under that read. The
   sweep at 13:00Z is the first run of the new package and is aw-1's J1 read either way.
5. Every read below holds at the apply.

## Blast radius

- **What moves:** the code package of the five rivalfunds Lambdas (daily, fetch-holdings, build-silver,
  build-canonical-shape, publish-page). Nothing else.
- **What the package gains over the deployed pin 325bd4e0f8.** Read with `git diff --stat 325bd4e0f8 39889dd4d7` over
  the seven staged paths, tests left out: 9 files, +532 -55.
  - `data/etfs/scripts/rivalfunds/ai_accounts.py` +200 (RIV-aw-1). Changed top-level definitions: `PROMPT_VERSION`
    (`a1-chain/7`), `SYSTEM`, `P_ACTIVITY_30D`, `P_DIRECTION`, `fact_pack`, `run_chain`, `regrade_rows` and `_figures`.
    Ten are added (`PERIOD_WORDS`, `wording_check`, `period_windows`, `_uncited_figures`, `_correction_text` and
    others). `grounding_check`, `security_keys`, `reading_label`, `GRADER_VERSION` (`grounding_check/6`) and `TABLE`
    are unchanged.
  - Origin's changes, carried because the pin follows 0.0.0_AB_MSTR~Z's merges: `lib/opal_naming.py` +12 (the
    census's wide function-literal rule and a `--all-roots` CLI flag; neither is on the `address()`/`name()` path).
    `infra/logic/registry/` has seven files: `key_rulings.json` +236, `name_rulings.json` +38, `mail_parties.json` +33,
    `exemptions.json` +6 -30 (three dell1 rows become full rows), `event_rules.json` +18, `reporting_policies.json` +18
    and `root_map.json` 1 line.
  - `lib/trading_calendar.py`, `lib/research/identity`, `org/standards/NAMING_SCHEMA.json` and
    `etf_positioning_gold.py`: 0 lines.
- **Addresses do not move.** Every literal `address()` / `name()` call site of the package (29 harvested, 28 with
  literal arguments) was evaluated under each pin's `lib/opal_naming.py` + registry, each in a fresh interpreter.
  Results: 28 OK and 0 refusals at each pin; **0 of 28 differ**. The registry loads and validates at the new pin, the
  changed `exemptions.json` included. (`round28/addr_parity.py`, run `python -I addr_parity.py <repo> 325bd4e0f8 39889dd4d7`.)
- **What the deploy writes:** nothing in S3. The first writes are those of the next scheduled runs, below.

## The expected outcome, read from the producers' rules, both branches

Writers of the two served properties this code reaches:

- **The AI accounts** (`gold/research_hypotheses/date=<D>/`): 1 writer, the sweep's AI step. It is `sweep.py`
  `ai_stage.run_for_day`, gated on `RIVALFUNDS_AI_ENABLE == "1"` and a publish-page marker for the day, and it runs
  once per page day. `ai_accounts.write_rows` is append-only: one object per run, and an existing run object raises.
  `regrade_day` has no production caller.
- **The page** (`platinum/page/date=<D>/`): 1 writer, publish-page. The sweep's republish goes through the same runner.
  It puts a page only when the rendered bytes differ.

**The 11:00Z chain of 2026-10-09 (old package, under condition 4):** this deploy does not touch it.

**The publish-page render under the new package, for a day already served.** publish-page makes no AI call. It
rechecks every stored account with `grounding_check`, and only `_figures` changed beneath it: the three period phrases
are now removed before figures are counted. Measured on the served object
`research_hypotheses-20261008T130223Z-ai.parquet` (26 items, `a1-chain/6`, stored grounding PASS 25 / FAIL 1):
- items whose text holds a period phrase: 0;
- items whose figure list differs between the pins: 0;
- **items whose recheck verdict differs: 0 of 26.**

So a republish of 2026-10-08 under the new package renders the same badges (`round28/regrade_parity.py` over the object fetched read-only, the two pins' `ai_accounts.py` from `git show`).

**The 13:00Z sweep of 2026-10-09: the first run of the new package and the J1 read.**
- **Branch A, expected:** one new accounts object for 2026-10-09 written under `a1-chain/7`, and one republish of the
  page carrying it. J1 counts over its items: period codes (0 expected), items stating their two dates (all expected),
  FAIL items, and the sums of `attached_figures` and `corrections`.
- **Branch B, reachable:** the model still writes a code or an uncited figure. `run_chain` sends the item back once (at
  most 4 chats a fund). An item that still fails is stored and shown as grounding FAIL with a wording reason (row
  Z-W21-S2). That is a J1 NOT MET for the CVO: the round-29 cell (R31), not a rollback.
- **Branch C, reachable:** the extra chats push the AI step past its deadline. The step records FAILED or
  SKIPPED_TIME, and the page republishes with the attempt or not at all. The day's tables are untouched.
  - The 13:08Z sweep of 2026-10-08 ran 486.4 s. A REPORT over 720 s is BLOCKING, as for every sweep.
  - On C this seat reports the same turn. The remedy is a cell, not a rollback, unless the page itself failed to
    publish.

## One figure by hand (R14)

Not offered as new: no figure is computed differently. The fact values the accounts cite come from the same tables
(`fact_pack` changes only words: the period name and its two dates). The J1 read on the 13:00Z sweep includes one
account's cited figure checked by hand against its row.

## Rollback, per key

- **Lambdas:** apply a plan made at pin 325bd4e0f8 (deploy tree `C:/tmp/rv-r8` is detached there now), then 0576fb051f
  as before.
- **Objects:** the 2026-10-09 accounts object is additive and append-only, and the next day's sweep writes its own.
  Removing it is an S3 delete and needs a human's word. The page is re-rendered by any later publish.

## Not covered by this half

- RIV-tc-1's merge and the switch `RIVALFUNDS_HISTORY_OWED` (R31 acts 2 and 3, each under its own pair).
- A plan that is not 0/5/0 package-only (condition 2).
- The vehicle: it runs the working tree, and `ai_accounts.py` is not in `round27/vehicle_load_set.json`'s 18 modules
  (aw-1's merge was listed against it: 0 of 7 paths).
