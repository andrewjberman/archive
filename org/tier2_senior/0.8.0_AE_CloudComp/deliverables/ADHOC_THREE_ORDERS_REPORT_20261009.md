# Three ADHOC orders from `2.0.0_SA_COO~C` -- report

**Seat:** `0.8.0_AE_CloudComp`. **Date:** 2026-10-09. **Issuer:** `2.0.0_SA_COO~C`.
**GOs:** msg 107883 (@dcb75a5b07) for the two test fixes; msg 108129 (@75559abc7c) for the forwarder pair.
**Push state (MEASURED at write time, `git ls-remote`):** LOCAL -- local `box/laptop` @`2f17028e67`,
origin `box/laptop` @`738d9aceef`. Not pushed: `box/*` is pushed only by an MSTR or the scheduled
`box-sync`, never by this seat.

---

## 1. `ADHOC.comp-secrets-test-json-reveal-refused` -- COMPLETE @`51a7621b25`

**AC1** `python -m pytest -q .tools/tests/test_comp_secrets.py` -> **`8 passed`**

The CTO's patch
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/TEST_COMP_SECRETS_JSON_REVEAL_REFUSED_20261009.patch`)
applied with `git apply` after a clean `git apply --check` at HEAD. No hand edits.

| | |
|---|---|
| baseline before | `3 failed, 5 passed` |
| failing tests | `test_json_reveal_emits_value`, `test_new_modes_never_leak_to_stderr`, `test_binary_modes` |
| the assertion | all three on `assert 2 == 0` -- the live tool returns rc=2, the tests pinned rc=0 |
| after | `8 passed` |

Three tests now assert the refusal against the live tool: `rc == 2`, empty stdout, and the SENTINEL
absent from BOTH stdout and stderr. `test_json_reveal_emits_value` is renamed
`test_json_reveal_refused`. Tool code untouched -- the fix is the CTO's commit @`9e4730450c`.

**Adversary check (preflight asked for it).** Not weakened to pass: the refusal is LIVE and the
rc=2 in the baseline failure came from the tool itself, not from the patch. No secret value is read
-- the refusal is the point.

## 2. `ADHOC.safe-deploy-bd-gold-test-retired-rule` -- NEEDS NO WORK; SUPERSEDED AT HEAD

**Left `pending`.** `superseded` is the COO's or the issuer's flip, never the assignee's
(`org/ref/TASK_ORDER_PROTOCOL.md`). **This is the one item the issuer still owes an act on.**

The work was already done at HEAD by @`9bc3787bc9` (`0.9.0_WK_MDPF_SECCLASS~76`, "rewrite the two
gold deploy tests to the named-file rule"). The test named in the order,
`test_deploy_tool_ships_the_shared_modules_beside_the_gold_files`, no longer exists; it is
`test_deploy_tool_ships_only_the_files_it_names_and_a_named_shared_module_rides_with_its_tree`.

| measured now | |
|---|---|
| **AC1** `pytest -q data/black_diamond/scripts/gold/tests/test_etf_classifier_deployed_resolution.py` | **`7 passed`**, 0 failed |
| scope step 3, whole suite from `data/black_diamond/scripts/gold` | **`99 passed`**, 0 failed |
| working tree for that file | clean (`git status --porcelain` empty) |

The order's dell1 row `MDPF_SECCLASS-D1-S19` reported `1 failed, 96 passed`; the suite is now 99
passed. **I verified the rewrite asserts the current rule on BOTH arms rather than taking the green
at face value:**

- negative arm -- a gold thread file named alone plans exactly itself:
  `shipped_artifacts_for([thread]) == []` and no plan key contains `_shared`;
- positive arm -- a `_shared` member named with `--tree black_diamond` ships exactly to
  `opal-data-bd` under the gold layer's `lib/_shared/`;
- plus a silver-only deploy carrying nothing extra.

It also DISCRIMINATES: under the retired ship-everything rule `shipped_artifacts_for([thread])`
would return the three members, so `== []` would fail. The test is not vacuous.

## 3. `ADHOC.provision-shims-check-inbox-forwarder` -- COMPLETE @`44e9b4ebd5`

**AC1**
```
bash .tools/provision-path-shims.sh && command -v check-inbox && test -f ~/bin/check-inbox.cmd \
  && check-inbox 0.8.0_AE_CloudComp; echo rc=$?
-> /c/Users/AndrewBerman/bin/check-inbox
   [check-inbox] No pending messages for 0.8.0_AE_CloudComp
   rc=0
```
Run against **this seat's own serial only** -- `check-inbox` consumes the inbox it names.

Precondition confirmed landed before starting: `0.0.0_AB_MSTR`'s nested-lane fix @`fd8f6c6c9b`.

**What landed in `.tools/provision-path-shims.sh`:**

1. `~/bin/check-inbox` (bash) + `~/bin/check-inbox.cmd`, both forwarding to
   `org/mcp/check-inbox.sh` run by bash, in the `aws` special case's position and shape.
2. Caller-toplevel resolution, the comp-* forwarders' own rule: the CALLER's git toplevel first,
   the derived main-worktree path as a LOUD fallback, `--which` to print the target. No path typed.
3. The `.cmd` written CRLF through the existing `sed 's/$/\r/'` rule, with the `goto` form and the
   `[%1]` bracket comparison the twin's measured notes require.
4. `_GITBASH` **hoisted** to one definition near `BIN=` (it sat inside the derived-loop section) so
   the new twin and the comp-* loop share one source rather than a retyped literal. Verified
   byte-identical to the live, working `~/bin/comp-system.cmd` interpreter line.
5. Named non-comp set now ENUMERATED in the header comment and the run-time SCOPE line:
   `aws, check-inbox`. **No glob** -- a glob over `org/mcp/` would forward `inbox-watch.sh` and
   `agent-poller.py`, which consume an inbox and which no law names as a bare command.
6. Target test is `-r`, not the comp-* twin's `-x`: this forwarder runs the script as an ARGUMENT
   to bash, so readability is what decides whether the target answers. An `-x` test would send a
   readable-but-non-executable checkout to the baked path while the caller's own copy sat there.

**Exercised beyond AC1** (each adversary line in the preflight):

| check | result |
|---|---|
| no widened glob | confirmed; the only `org/mcp/*` in the file is the comment refusing it |
| caller-toplevel, inside the repo | `--which` -> the caller's own `org/mcp/check-inbox.sh` |
| caller-toplevel, outside any checkout | WARNs on stderr naming `git rc=128` + the baked path; never silent |
| LF `.cmd` hazard | `file(1)`: "DOS batch file, ASCII text, with CRLF line terminators" |
| the twin actually runs | by absolute path from PowerShell: `--which` rc=0, and a real run with an argument rc=0 |
| loop hazard (the `aws` pair's reason for existing) | cannot arise: `check-inbox.sh` carries no self-invocation at HEAD |

Run output: `wrote 105 tool(s) x2 forms` (104 before), `DACL inheritance intact -- protected 0 of 209`.

---

## Surfaced, not fixed -- `NFRA_TOOLARCH-S1`

`org/surprise_channel/NFRA_TOOLARCH/INVESTIGATION_v1.md` (channel opened; it had none).

The provisioner's foundational premise -- that `~/bin` is "a persistent Windows USER-level PATH
environment variable entry, inherited unconditionally by every child process on this machine" --
is **measured false on the PowerShell plane**. `~\bin` is absent from the 28-entry persistent user
PATH, and a fresh `powershell.exe -NoProfile` child reads `check-inbox` as NOT FOUND. So all 105
`.cmd` twins are unreachable by bare name from PowerShell, which the script's own comments call
"the primary shell on this box".

**Positive control, and it is what makes this a premise defect rather than a defect in the new
pair:** `comp-which` -- provisioned since July and in daily use -- is equally NOT FOUND there.
The bash plane resolves for an unrelated reason: Git Bash prepends `$HOME/bin` itself.

Why no probe catches it: `org/XXX.md` step 1b-A.3's PATH check runs in BASH, reads
"102 of 102 comp-tools resolve bare", and is structurally blind to the twin plane -- the same
anti-correlated-probe shape the script's own header warns about.

**Not this seat's act:** the remedy is a machine-level environment change outside the order's
`<paths>`, held by `0.0.0_AB_MSTR` with `1.0.0_SA_CTO` to rule whether it is the PATH entry, a
different reachable directory, or a correction to the premise comment. It does not block or weaken
the new pair, which is exactly as reachable as every other shim, and nothing in the order is left
undone on account of it.

## Compiler Tools

| tool | result |
|---|---|
| `comp-to` x3 | session TO_ID set per order |
| `comp-which` (startup exercise) | a forwarder RAN; `PATH: 102 of 102 comp-tools resolve bare` |
| `comp-pulse diff` (safe-commit risk reflex) | `PARTIAL_OR_BLIND` -- danger map 63.4h STALE, so it could not clear the diff. "Could not check" is not "checked clean"; recorded, not quoted as a pass |
| `commit-gate.sh` | clean on the `.py` edit; `bash -n` + `comp-shell` clean on the shell edit |
| `surprise-row-gate` | REFUSED my first row on two real violations (non-enum `disposition`, a `surfaced_by` carrying prose the committer-match could not read), then OK |
| `comp-schedule` / `comp-iam` | DECLARED-NOT-APPLICABLE per each order's preflight -- no schedule, no AWS call |

Gap worth naming: `client-data-check` WARNed on every commit -- the hashed account-id list is
ABSENT at `C:\Users\AndrewBerman\.opal\account_id_hashes.txt`, so these commits were NOT checked
for client account ids. Absent is not empty. Device-level, not an order item.
