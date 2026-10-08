## E1 -- `AMGT-cc-5` -- THE TWO BUILD-SIDE REPAIRS OF THE SCOPED FUNCTION: THE STALE GENERATED STAMP, AND THE READ GRANT ON THE COLLECTOR'S JOB-RECORD PREFIX (TEXT ONLY, NOTHING APPLIED)

### 1. MEASURED AT THE BASE

Base `c08ddaf71f` (CLOUD), 2026-10-08T10:30Z to 10:50Z. HEAD moved to `6b9d3118c6` during the measuring; none of the four
files of this cell changed between the two (AC3 at the base, section 4). Repo reads, one scratch copy outside the repo, and
four AWS READS (the role's inline policy, its policy lists, the function's configuration, two store listings). Nothing written
to the repo but this file and the check. One side effect, named: the naming gate was run once on a scratch diff and appended
its verdict lines to its own gitignored log `org/mcp/naming-gate-verdicts.log`.

**THREE THINGS THE BRIEF ASSUMED THAT THE REPO DOES NOT HOLD. Read these first.**

1. **There is no generated tfvars file.** `gen_harvest_prefixes.py` writes ONE file, `lib/research/api/_harvest_prefixes.py`
   (its `OUT_REL`, line 46). The folder `infra/aws/terraform/harvest/` holds no `.tfvars` and no `.auto.tfvars.json`
   (21 tracked files, listed by `git ls-files`; the `.tfplan` files are gitignored).
2. **The terraform takes no prefix from a variable.** `scoped-amgt-api.tf` grants every store prefix from ONE local list,
   `scoped_amgt_pool_prefixes` (lines 118 to 288, 33 entries, each a quoted string written in the file). The list is read
   twice: line 322 builds the `s3:GetObject` resources, line 330 builds the `s3:ListBucket` prefix condition. So ONE list
   entry grants both limbs. The filing-attempt state prefix is granted exactly that way (one entry, line 190). The smallest
   correct change is therefore ONE added list entry: no new variable and no statement edit.
3. **The naming gate does not refuse the builder's prefix written in that list.** `org/mcp/naming-gate.enforce` is present
   (the gate enforces). Run on a scratch diff carrying this cell's seven added lines it printed
   `NAMING CONFORMANT infra/aws/terraform/harvest/scoped-amgt-api.tf:289 seeking-alpha/harvest/state/job_record/` (and the
   same for the generated module's line), `NAMING-GATE: PASS 2 graded`, exit 0. What ties the written entry to the builder
   is AC2 clause T1, which computes the builder's value and compares.

**Repair 1: what a regeneration changes. THE HASH ONLY. No prefix value changes.**

`PYTHONPATH="$(pwd)" python infra/aws/terraform/harvest/gen_harvest_prefixes.py --check` exits 1. The generator's own functions,
called from a scratch script, give this line diff of the regenerated module against the committed one:

| line | committed | regenerated |
|---|---|---|
| 2 (header comment) | `... at generation time: 0b67ab695620558cd2c626e7f007915ac67713df4f72c6d3b12e39f05cbebf99` | `... at generation time: fff9a273a59bc232addcd45968cfaca55832266e74e288512d5c61817d7c225e` |
| 11 `REGISTRY_HASH` | `'0b67ab69...05cbebf99'` | `'fff9a273...7d7c225e'` |

| constant | committed | regenerated | |
|---|---|---|---|
| `BLOOMBERG_BRONZE_PREFIX` | `bloomberg/harvest/bronze/` | `bloomberg/harvest/bronze/` | EQUAL |
| `BRIGHT_DATA_SERP_BRONZE_PREFIX` | `bright-data/harvest/bronze/serp/` | `bright-data/harvest/bronze/serp/` | EQUAL |
| `FILING_ATTEMPT_STATE_PREFIX` | `amgt/harvest/state/filing_attempt/` | `amgt/harvest/state/filing_attempt/` | EQUAL |
| `SEEKING_ALPHA_BRONZE_PREFIX` | `seeking-alpha/harvest/bronze/` | `seeking-alpha/harvest/bronze/` | EQUAL |

4 of 4 values equal. No served address moves.

- **What the hash covers.** `scoped_registry_hash()` hashes four rows of `infra/logic/registry/systems.json` (keys `amgt`,
  `bloomberg`, `bright-data`, `seeking-alpha`) and the one `scopes.json` row `lookup("harvest")` resolves to, with sorted keys.
- **Which commit moved it: ONE, `c09b1ad769`** (4.0.0_SA_CRO, 2026-10-07T18:48Z). The scoped hash computed from the registry
  at `c09b1ad769~1`, `11f54fba67~1`, `8e39143feb~1`, `4201d79857~1` and `bd15c7410d` is `0b67ab69...` at all five; at HEAD it
  is `fff9a273...`. The fields that differ, old against new: `owner_claim` (`inferred` to `measured`) and `owner_basis` (the
  sentence now opens with Andrew's confirmation) on the three rows `bloomberg`, `bright-data`, `seeking-alpha`. The `amgt` row
  and the scope row are unchanged. No `key`, `long` or `class` field changed, which is why no prefix value moved.
  (`662cbb0be5` and `914bb833ca`, named in the brief, did not move the scoped hash.)
- **The test.** `lib/research/api/tests/test_harvest_prefixes.py`: 5 passed, 1 failed
  (`test_ii_registry_hash_matches`, the same two hashes). 6 tests in the file.
- **The build.** `build-and-upload-scoped-amgt.sh` line 127 runs `--check` under `set -euo pipefail`, before anything else, so
  the next build stops there.
- **The stamp will go stale again** whenever any field of those five rows is edited, including a prose field. See section 8, Q4.

**Repair 2: the prefix, the registry, the grant.**

- **The builder's output, computed, never typed.**
  `lib.opal_naming.address("seeking-alpha", lookup("harvest")["long"], "state", "job_record", "date=1970-01-01")` printed
  `s3://opal-data-harvest/seeking-alpha/harvest/state/job_record/date=1970-01-01`. With the partition cut:
  `seeking-alpha/harvest/state/job_record/`. With the table cut as well (the tier root): `seeking-alpha/harvest/state/`.
- **The registry: the builder does NOT refuse, and no row is missing.** `key()` needs the source in `systems.json` (the
  `seeking-alpha` row is there, class VENDOR), the scope (`harvest`) and the tier (`state`); it asks nothing of the table.
  The token `job_record` appears 0 times across the 11 files of `infra/logic/registry/` (denominator printed per file, 0 in
  each). So the schema's sentence "its registry row lands with the collector cell's commit" names a row the builder never
  needed: there is no such row and none is owed. This cell adds nothing to the registry.
- **The reader does not use the generated module.** `AMGT-cc-3` (GROUP_B section 2, rule 1) calls the builder inside the
  function at request time. The new constant in the generated module is therefore a build-side carrier with no runtime reader
  at this cut (section 8, Q2).
- **The role and its policy** (from the file): role `opal-amgt-scoped-api-role` (`aws_iam_role.scoped_amgt_api`), ONE inline
  policy `opal-amgt-scoped-api-grants` (`aws_iam_role_policy.scoped_amgt_api_grants`), one attached managed policy
  `AWSLambdaBasicExecutionRole`. Statement `ReadThePoolPrefixesTheAdapterReads` (line 315) is the object read; statement
  `ListOnlyThePoolPrefixesTheAdapterReads` (line 325) is the list with the prefix condition.
- **The live policy equals the file today** (read 10:37Z, section 8): 7 statements; 33 object-read resources and 33 list
  prefixes, each equal, in order, to the file's 33 entries with `*` appended. No live line names `job_record`. The only live
  line under any `state/` tier is `amgt/harvest/state/filing_attempt/*`.
- **Narrow against wide.** The CTO's text names `seeking-alpha/harvest/state/`. The reader lists
  `seeking-alpha/harvest/state/job_record/`. The builder supports both (the first is its tier root, the second its table
  prefix). Measured in the store at 10:48Z: `seeking-alpha/harvest/state/` holds exactly ONE child, `job_record/`, and no
  object of its own, so today the two grants reach the same objects. They differ only for a table a later writer adds under
  that tier. This cell is drafted for the NARROW one, the table prefix, which is what the reader needs and how
  `filing_attempt` is granted.

### 2. THE ACT (worker face text)

The scoped research function is built by a script that first checks one generated file against the address builder. That
check fails today, so the next build would stop. Separately, the function is about to read a new folder of small records
(one per finished Seeking Alpha collection job) and its role has no read grant on that folder. You make both repairs IN TEXT
ONLY. You run no `terraform` command of any kind, no `safe-apply`, no `aws` command that writes, no build script
(`build-and-upload-scoped-amgt.sh` is NOT run), and you install and download nothing. Another order applies the grant.

Work from the repo root: `cd "$(git rev-parse --show-toplevel)"`. Every command below is run there.

Read first, whole: `infra/aws/terraform/harvest/gen_harvest_prefixes.py` and
`lib/research/api/tests/test_harvest_prefixes.py`. In `infra/aws/terraform/harvest/scoped-amgt-api.tf` read lines 94 to 120,
lines 184 to 190 (how the filing-attempt state prefix is granted: one list entry) and lines 256 to 332.

1. **The generator.** In `infra/aws/terraform/harvest/gen_harvest_prefixes.py`, function `compute()`, add ONE entry after the
   `BRIGHT_DATA_SERP_BRONZE_PREFIX` line:
   `"SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX": _table_prefix("seeking-alpha", _SCOPE, "state", "job_record"),`
   Do not change `_SOURCES` (it already holds `seeking-alpha`), `scoped_registry_hash`, `main` or the two helper functions.
   Where the file's text says "the four constants" (the module docstring, the `scoped_registry_hash` docstring, and the header
   line inside `render`), write "the constants". Change nothing else in `render`.
2. **Regenerate. Never edit the generated file by hand.** Run
   `PYTHONPATH="$(pwd)" python infra/aws/terraform/harvest/gen_harvest_prefixes.py --write`
   then
   `PYTHONPATH="$(pwd)" python infra/aws/terraform/harvest/gen_harvest_prefixes.py --check; echo "exit=$?"`
   The second must print `OK:` and `exit=0`. Open `lib/research/api/_harvest_prefixes.py` and confirm: `REGISTRY_HASH`
   changed, the four old constants read exactly as before (`bloomberg/harvest/bronze/`, `bright-data/harvest/bronze/serp/`,
   `amgt/harvest/state/filing_attempt/`, `seeking-alpha/harvest/bronze/`), and the one new constant is there. If any of the
   four old values differs, STOP, change nothing further, and report it: that would move a served address.
3. **The test.** In `lib/research/api/tests/test_harvest_prefixes.py`, function `_fresh_constants`, add ONE entry after the
   `BRIGHT_DATA_SERP_BRONZE_PREFIX` line:
   `"SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX": _table_root("seeking-alpha", "harvest", "state", "job_record"),`
   Where the file's docstring says "four constants", write "constants". Leave `test_ii_b` alone: its set of four SOURCES is
   still right. Run `PYTHONPATH="$(pwd)" python -m pytest lib/research/api/tests/test_harvest_prefixes.py -q -p no:cacheprovider`
   and see 6 passed.
4. **The grant.** Print the prefix from the generated file, do not compose it yourself:
   `PYTHONPATH="$(pwd)" python -c "from lib.research.api import _harvest_prefixes as h; print(h.SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX)"`
   In `infra/aws/terraform/harvest/scoped-amgt-api.tf`, in the list `scoped_amgt_pool_prefixes`, add ONE entry as the LAST
   entry of the list, after the line `"issuer-site/harvest/silver/filing_source/",` and before the closing `]`: the printed
   value in double quotes followed by a comma, on its own line, indented four spaces like its neighbours. It ends in a slash.
   Above it write a comment of a few lines, each starting `#`, that says: AMGT_RESAPP round 79, cell AMGT-cc-5; the freshness
   view's reader of the Seeking Alpha collector's job records lists this prefix and then reads its objects; one entry grants
   both limbs because the list is read twice below; the spelling is the generated constant
   `SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX`, which is the address builder's output; the trailing slash is mandatory; READ ONLY,
   the collector writes these records and this role never does; the grant is this table and not the whole state tier. Write
   the comment in plain ASCII and do not write the prefix itself inside the comment.
5. **Change nothing else in that file.** No new statement, no new variable, no new action, no edit to lines 322 or 330, no
   edit to any other list entry or comment. Do not edit `build-and-upload-scoped-amgt.sh`, any other `.tf`, anything under
   `infra/logic/registry/`, `lib/opal_naming.py`, or any file under `lib/` other than the two named above.
6. Run the three criteria below. Your report states: the old and new `REGISTRY_HASH`; the four old values, each "unchanged";
   the new constant's value; the line number of the new list entry; and that you ran no terraform, no apply, no build and no
   AWS write.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc5.py" --crit AC1; echo "exit=$?"`
  Expect: the generator's own check exits 0, its test file passes whole (6 or more passed, 0 failed), the four prefix values of the cut are byte-equal to the cut, and the new job-record constant is in the generated module and in the generator and equals the address builder's output; G1-G5 PASS; R79 CC5 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc5.py" --crit AC2; echo "exit=$?"`
  Expect: read as text with no terraform run, the prefix list is the cut's 33 entries in order plus exactly the builder's job-record prefix, the whole state tier is not granted, the one object-read expression and the one list-condition expression are the cut's, no action was added or removed, and no other code line changed; T0-T5 PASS; R79 CC5 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc5.py" --crit AC3; echo "exit=$?"`
  Expect: from the base commit to HEAD and in the working tree, nothing under the harvest terraform folder or the generated files changed except the cell's four files; B0-B2 PASS; R79 CC5 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN

At HEAD `6b9d3118c6` (the check's pinned base is `c08ddaf71f`), 2026-10-08 ~10:45Z. AC1 and AC2 FAIL for the right reasons
(the stamp is stale; the constant and the list entry do not exist yet); AC3 PASSES.

```
--- BASE AC1
FAIL G1 the generator's --check exits 0 exit 1; FAIL: lib/research/api/_harvest_prefixes.py DRIFTS from fresh lib.opal_naming output (registry hash fff9a273a59bc232addcd45968cfaca55832266e74e288512d
FAIL G2 the generator's test file passes whole exit 1; passed 5 (at the cut 6 tests); failed 1 ['lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches']
   BLOOMBERG_BRONZE_PREFIX at the cut 'bloomberg/harvest/bronze/' now 'bloomberg/harvest/bronze/' EQUAL
   BRIGHT_DATA_SERP_BRONZE_PREFIX at the cut 'bright-data/harvest/bronze/serp/' now 'bright-data/harvest/bronze/serp/' EQUAL
   FILING_ATTEMPT_STATE_PREFIX at the cut 'amgt/harvest/state/filing_attempt/' now 'amgt/harvest/state/filing_attempt/' EQUAL
   SEEKING_ALPHA_BRONZE_PREFIX at the cut 'seeking-alpha/harvest/bronze/' now 'seeking-alpha/harvest/bronze/' EQUAL
PASS G3 the prefix values of the cut are byte-equal to the cut 4 of 4 equal; changed []
FAIL G4 the generated module carries the builder's job-record prefix and no other new constant SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX is None; builder 'seeking-alpha/harvest/state/job_record/'; constants 4; unexpected []
FAIL G5 the generator computes the same prefix, and its constants are the module's compute() gives None; builder 'seeking-alpha/harvest/state/job_record/'; names 4
R79 CC5 AC1 SERVED: NO
exit=1
--- BASE AC2
PASS T0 the prefix list is found at the cut and now at the cut 33 entries (expected 33); now 33
FAIL T1 the list is the cut's list in the cut's order plus exactly the builder's job-record prefix entries 33 (at the cut 33); added []; removed []; builder 'seeking-alpha/harvest/state/job_record/'
PASS T2 the added entry ends in a slash and the whole state tier is not granted tier root 'seeking-alpha/harvest/state/' in the list: False
PASS T3 one object-read expression and one list-condition expression read the list, as at the cut expressions at the cut 2; each present once now True; code lines naming the list 3 (expected 3)
PASS T4 no action was added or removed anywhere in the file action tokens 15 (at the cut 15); added []; removed []
PASS T5 apart from the one list entry the file's code is the cut's; no other line names the new prefix code lines 197 (at the cut 197); other lines naming it 0
R79 CC5 AC2 SERVED: NO
exit=1
--- BASE AC3
PASS B0 the base commit is known to this repository c08ddaf71f87 rc=0
PASS B1 from the base to HEAD only the cell's four files changed under the harvest folder and the generated files base c08ddaf71f HEAD 6b9d3118c6; changed []; outside the cell []
PASS B2 the working tree holds no uncommitted change outside the cell's four files in those places uncommitted []; outside the cell []
   not graded: files changed from the base to HEAD under the naming registry and its builder: 0 []
R79 CC5 AC3 SERVED: YES
exit=0
```

Reachability: the same check against a scratch copy OUTSIDE the repo (`git archive HEAD` of `lib`, `infra/logic/registry`,
`org/standards` and the harvest folder, with the act's seven added lines laid over it; `git status --porcelain` on the repo's
harvest folder, `lib/research/api` and `infra/logic` is empty after it):

```
--- SCRATCH AC1
PASS G1 the generator's --check exits 0 exit 0; OK: lib/research/api/_harvest_prefixes.py matches fresh lib.opal_naming output byte for byte (registry hash fff9a273a59bc232addcd45968cfaca55832266e74
PASS G2 the generator's test file passes whole exit 0; passed 6 (at the cut 6 tests); failed 0 []
   BLOOMBERG_BRONZE_PREFIX at the cut 'bloomberg/harvest/bronze/' now 'bloomberg/harvest/bronze/' EQUAL
   BRIGHT_DATA_SERP_BRONZE_PREFIX at the cut 'bright-data/harvest/bronze/serp/' now 'bright-data/harvest/bronze/serp/' EQUAL
   FILING_ATTEMPT_STATE_PREFIX at the cut 'amgt/harvest/state/filing_attempt/' now 'amgt/harvest/state/filing_attempt/' EQUAL
   SEEKING_ALPHA_BRONZE_PREFIX at the cut 'seeking-alpha/harvest/bronze/' now 'seeking-alpha/harvest/bronze/' EQUAL
PASS G3 the prefix values of the cut are byte-equal to the cut 4 of 4 equal; changed []
PASS G4 the generated module carries the builder's job-record prefix and no other new constant SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX is 'seeking-alpha/harvest/state/job_record/'; builder 'seeking-alpha/harvest/state/job_record/'; constants 5; unexpected []
PASS G5 the generator computes the same prefix, and its constants are the module's compute() gives 'seeking-alpha/harvest/state/job_record/'; builder 'seeking-alpha/harvest/state/job_record/'; names 5
R79 CC5 AC1 SERVED: YES
scratch exit=0
--- SCRATCH AC2
PASS T0 the prefix list is found at the cut and now at the cut 33 entries (expected 33); now 34
PASS T1 the list is the cut's list in the cut's order plus exactly the builder's job-record prefix entries 34 (at the cut 33); added ['seeking-alpha/harvest/state/job_record/']; removed []; builder 'seeking-alpha/harvest/state/job_record/'
PASS T2 the added entry ends in a slash and the whole state tier is not granted tier root 'seeking-alpha/harvest/state/' in the list: False
PASS T3 one object-read expression and one list-condition expression read the list, as at the cut expressions at the cut 2; each present once now True; code lines naming the list 3 (expected 3)
PASS T4 no action was added or removed anywhere in the file action tokens 15 (at the cut 15); added []; removed []
PASS T5 apart from the one list entry the file's code is the cut's; no other line names the new prefix code lines 198 (at the cut 197); other lines naming it 0
R79 CC5 AC2 SERVED: YES
scratch exit=0
```

The bound's negative arm, with an older base (`--base b71bf46c74~1`): B1 FAILS and names 9 files outside the cell (the build
scripts, `content_diff.py`, `freshness-snapshot-schedule.tf` and others), `R79 CC5 AC3 SERVED: NO`, exit=1.

`bash .tools/commit-gate.sh` on the check file: `OK: pre-commit gate clean for 1 of 1 file(s)`, exit 0.

### 5. `<paths>`

```
infra/aws/terraform/harvest/gen_harvest_prefixes.py
infra/aws/terraform/harvest/scoped-amgt-api.tf
lib/research/api/_harvest_prefixes.py
lib/research/api/tests/test_harvest_prefixes.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class

- `<risk>`: LOCAL. Four text files; seven added lines of code plus comments and three wording edits. Nothing is applied,
  built, uploaded or deployed by this cell, and no store or AWS resource is written. Egress class NONE.
- The cell's text becomes SERVED only at the redeploy order's apply, under that order's own never-widen pair. The grant
  entry is a WIDENING of the role (read only, one table prefix); the stamp repair moves no served value (4 of 4 equal).
- `<worker_class>`: `worker-light`. The whole act is under 20 changed lines and the reference edit was made and run in
  scratch.

### 7. Edges

- **AC2 clause T5 is strict about the entry's form.** The new entry must be a line that reads, stripped, exactly the quoted
  prefix followed by a comma. An entry without the trailing comma, or with a comment on the same line, fails T5.
- **T1 wants the cut's order kept and the new entry added.** It does not require the new entry to be last; the act asks for
  last so the file reads in round order.
- **Comments are not graded by AC2** (lines starting `#` are skipped). A comment that names the prefix would not fail AC2,
  and would be graded by the naming gate as a comment (not graded). The act still forbids it, so one text search for the
  prefix finds exactly one grant.
- **The base pin.** AC1 and AC2 read the cut's files from commit `c08ddaf71f` by `git show`; an unreadable base is a FAIL of
  the clause, never an empty file. AC3's `--base` defaults to the same commit. A worker worktree cut from a later CLOUD HEAD
  is fine so long as no commit between touched the harvest folder or the two `lib` files (0 at `6b9d3118c6`). If the issuer
  cuts from a HEAD where another commit has touched them, pass `--base <that HEAD>` to AC3.
- **AC1 does not pin the hash value.** It grades the generator's own `--check`. If the CRO edits one of the five registry
  rows between the worker's `--write` and the grading, G1 and G2 fail again for the same cause as today: re-run `--write`,
  do not edit the check.
- **G2 needs the test's imports.** The test imports `lib.research.api.scoped_amgt`; a cell that breaks that import breaks
  G2. `AMGT-cc-4` edits that file in this round; at the drain run AC1 on the merged tree.
- **`AMGT-cc-4`'s check lists this test as a known base failure** (`r79_cc4.py` line 66). After this cell lands the failure
  is gone; cc-4's AC3 accepts that (it allows the failure, it does not require it).
- **The naming gate enforces at the commit.** Measured PASS on this act's diff (section 1, item 3). The gate also refuses a
  hand edit to a generated file; step 2's `--write` is what keeps the worker clear of that.
- `R79_CC5_TREE` reads the four files from another tree; it exists for the scratch run above and is not in any criterion.

### 8. Not measured, and questions for the issuer

**FOR THE REDEPLOY ORDER'S NEVER-WIDEN PAIR (the grant leg; this cell applies nothing).**

- **What a plan should then show, named.** In the root `infra/aws/terraform/harvest/`:
  1. `aws_iam_role_policy.scoped_amgt_api_grants` (inline policy `opal-amgt-scoped-api-grants` on role
     `opal-amgt-scoped-api-role`): update in place, exactly two added lines in the policy document: one resource in statement
     `ReadThePoolPrefixesTheAdapterReads` and one `s3:prefix` value in statement `ListOnlyThePoolPrefixesTheAdapterReads`.
  2. `module.scoped_amgt_api.aws_lambda_function.this` (function `opal-amgt-scoped-api`): update in place, `source_code_hash`
     and `s3_object_version` only, and only after the new artifact is uploaded (the module reads the artifact object's
     `content-sha256`, `modules/yang-lambda/main.tf` lines 38 to 39).
  Nothing else. Any other resource in the plan is not this round's and stops the apply. Order (GROUP_B H7, and the CTO's
  standing grant condition): the policy is applied and re-read BEFORE the code leg.
- **The one read that gives BEFORE** (run at 2026-10-08T10:37Z, read only):
  `.tools/aws iam get-role-policy --role-name opal-amgt-scoped-api-role --policy-name opal-amgt-scoped-api-grants --output json`
  The role holds exactly one inline policy (`list-role-policies`) and one attached managed policy,
  `AWSLambdaBasicExecutionRole` (`list-attached-role-policies`). BEFORE reads:
  - 7 statements: `ReadRankedAxesAndPoints`, `ReadThePoolPrefixesTheAdapterReads`, `ListOnlyThePoolPrefixesTheAdapterReads`,
    `WriteOnlyTheFirmsOwnStarMarkers`, `ReadTheServedEtfClassificationLabels`,
    `ReadTheScannerSp500UniverseForCoveredNoBlock`, `ReadAndWriteTheFreshnessSnapshotObjectOnly`.
  - `ReadThePoolPrefixesTheAdapterReads`: action `s3:GetObject`, 33 resources. Those naming Seeking Alpha (3):
    `arn:aws:s3:::opal-data-harvest/seeking-alpha/harvest/bronze/*`,
    `arn:aws:s3:::opal-data-harvest/seeking-alpha/harvest/silver/*`,
    `arn:aws:s3:::opal-data-harvest/seeking-alpha/harvest/silver/article/*`.
  - `ListOnlyThePoolPrefixesTheAdapterReads`: action `s3:ListBucket` on the bucket, 33 `s3:prefix` values. Those naming
    Seeking Alpha (3): `seeking-alpha/harvest/bronze/*`, `seeking-alpha/harvest/silver/*`,
    `seeking-alpha/harvest/silver/article/*`.
  - Lines under any `state/` tier: one in each limb, `amgt/harvest/state/filing_attempt/*`. `job_record` appears 0 times.
  - Both limbs equal the file's 33 entries with `*` appended, in order (live equals desired).
  - sha256 of the document with sorted keys and compact separators:
    `6270e453570b8ea923b9a4471bbcf4d0660e73fabe8ffe920502be4442c64adb`.
  - The function at the same read: `CodeSha256` `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=`, last modified
    2026-10-08T07:19:32Z.
- **What AFTER should read** (the same command): 7 statements, the same seven Sids and the same actions; 34 resources in the
  object-read statement and 34 prefixes in the list statement; the one added line in each is
  `arn:aws:s3:::opal-data-harvest/seeking-alpha/harvest/state/job_record/*` and `seeking-alpha/harvest/state/job_record/*`;
  the other 33 of each byte-equal to BEFORE and in the same order; the five other statements byte-equal; the attached
  policy list unchanged. The pair's control arms, by `simulate-principal-policy` one resource per call: `s3:GetObject` on a
  key under the job-record prefix and `s3:ListBucket` with that `s3:prefix` move from implicitDeny to allowed;
  `s3:PutObject` and `s3:DeleteObject` on the same key stay implicitDeny; `s3:GetObject` on a sibling key under
  `seeking-alpha/harvest/state/` that is NOT under `job_record/` stays implicitDeny (the arm that tells narrow from wide).

**Questions for the issuer.**

- **Q1 (CTO). Narrow or wide.** The ruling's words are "the exact prefix seeking-alpha/harvest/state/"; the reader needs
  `seeking-alpha/harvest/state/job_record/`. Both are builder output. Today they reach the same objects (the tier holds one
  child and no object of its own). The cell is drafted NARROW. If the wide one is ruled, three things change: the generator
  entry becomes `"SEEKING_ALPHA_STATE_PREFIX": _tier_root_prefix("seeking-alpha", _SCOPE, "state")` (and the test's entry
  `_tier_root`); the list entry is the tier root; and the check's `NEW_NAME`, clause T1's expected value and clause T2 (which
  today REFUSES the tier root) are edited to match. The pair's last control arm above then has no deny to show.
- **Q2 (issuer). Is the generator constant wanted at all?** The brief's premise was that the terraform reads generated
  values. It does not. The grant itself is one list line; the constant adds two files' worth of edits and has no runtime
  reader (cc-3 calls the builder). It is kept in the draft because the brief asked for it and because it gives the worker a
  printed value to copy. Dropping it removes steps 1 and 3 of the act and clauses G4 and G5; repair 1 is then step 2 alone.
- **Q3 (CTO). Rule 30 against this file's shape.** All 33 existing entries are strings written in the `.tf`. The gate grades
  a conforming one CONFORMANT and passes it. If the CTO reads rule 30 as requiring the list to be GENERATED, that is a
  migration of 34 entries and a new generated file, not a rider on this cell.
- **Q4 (CTO or the generator's owner). The stamp is brittle by design.** It hashes whole registry rows, so a prose edit to
  `owner_basis` turned the build red with no prefix moved. Hashing only the fields `key()` reads (`key`, `long`, `class`
  and the scope row's address fields) would stop that. Not in this cell: it changes what the gate guards.
- **Q5 (issuer). Whether this is a surprise row.** A registry commit by another project broke this project's build gate and
  nothing told either seat; found only because cc-4's base run listed a failing test. Not filed by this seat.

**Not measured.**
- No `terraform plan` was run, so "nothing else in the plan" above is the expectation, not a reading. Standing drift in this
  root, if any, is unknown.
- The live grant was read, not simulated: no `simulate-principal-policy` call was made for the job-record prefix.
- The worker's wording edits ("the four constants" to "the constants") were not in the scratch run; they change the generated
  header line, and `--write` followed by `--check` is consistent by construction.
- The full api test folder was not run with the act laid over it; only `test_harvest_prefixes.py` (6 passed in scratch).
- Whether the deployed package's `lib/opal_naming` resolves this source and tier inside the function (GROUP_B's open item)
  is untouched by this cell.
- The build script was not run, with or without `--build-only`.
- The worker's deliverables folder is not in section 5: the slot number is the issuer's, and the generator adds it.
