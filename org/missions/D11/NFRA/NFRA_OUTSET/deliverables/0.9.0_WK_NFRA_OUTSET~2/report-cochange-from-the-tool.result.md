# TO-OS-s-9 result -- the report's co-change stratum reads the tool's artifact, and declares itself when it cannot

**TO:** `NFRA_OUTSET.TO-OS-s-9` (`.../task-orders/NFRA_OUTSET.TO-OS-s-9.report-cochange-from-the-tool.md` @`8c231d47bf`)
**Cell:** `OS-s-9` - **outcome_ref:** FWD-3, FWD-6 - **verb:** fix - **depends_on:** OS-s-10 (`508d4ce31d`)
**Executed by:** `0.9.0_WK_NFRA_OUTSET~2` in worktree `C:/tmp/wk-OUTSET-2`, branch `wk-OUTSET-2`, base HEAD `8c231d47bf`
Both addressing limbs read `~2` at HEAD before I started; no carry step.

> **HEADLINE, and it changes the shape of the fix: the cell's premise is half true. `_stratum_cochange` really is host-computed with 0 tool calls -- but there is NO TOOL TO RETIRE IT IN FAVOUR OF.** It pairs *resource / pipeline-chain* labels; the estate's co-change tool `comp-cochange` answers *agent-type* co-movement. Same word, different axis. So the fix is not a substitution: the stratum now **reads the OS-s-10 seam artifact when one is published**, and when none is, the host copy stays and **declares what it stands in for** -- which is exactly the branch `O9-AC2` and FWD-6 anticipate. Row `NFRA_OUTSET-W2-S14`.

---

## 1. WHAT I MEASURED FIRST

| | grain | evidence |
|---|---|---|
| **the host stratum** (`estate_report_runner.py:1308-1345` @`8c231d47bf`) | **resource / pipeline chain** | walks commits, calls `attribute_path(p, maps)` (`:903`) and keeps only `kind == "chain"` labels -- lambda/EC2 producers resolved to threads via `maps["prod_to_thread"]`. Rows are `{"pair": "<chain> <-> <chain>", "co_commits": n, "each_total": [...]}` |
| **the tool** `.tools/comp-cochange` | **agent type / serial** | live run, `rc 0` in 1.3 s: `grain: "type"`, `active_tags: [AB, AE, BG, DE, DS, DT, SA, WK]`, `pairs` = `["AE","SA"]`, `["AB","SA"]`, `["AE","DT"]` ... 14 pairs, **0** resource labels. Its own header: *"which agent TYPES change the same files together"*; its only grain flag is `--grain {type,serial}` |

The router corroborates that no resource-grain co-change tool exists (`comp-which` asked three ways: `comp-blast 1.50` once, `NO CURATED RULE MATCHED` twice) -- offered as corroboration only, since I filed `W2-S11` recording that this fabric's router is in lexical fallback.

**Smaller premise correction:** the stratum's own path makes **one** git subprocess call (`commits_in_window`, `:282`); the runner as a whole has 8 distinct `"git"` argv sites. The "16 git calls" is a runner-wide figure. The **"0 tool calls"** half is true and is the load-bearing half.

## 2. WHAT I CHANGED -- `infra/aws/ec2/estate-report-runner/estate_report_runner.py` only

| Change | Where (after) | What |
|---|---|---|
| seam branch | `:1327-1336` | When `ESTATE_OUTSET_SEAM_PREFIX` is set, read `<prefix>/comp_cochange.json` through **`_outset_read` unchanged** and render the tool's rows, vintage, answer-state and denominators. **No second reader** -- OS-s-10's contract *is* the reader, and all its arms (ABSENT / UNREADABLE / STALE / FUTURE-DATED / unmapped-state) apply for free. |
| `OUTSET_COCHANGE_KEY` | `:1463` | The artifact key, beside the seam's other constants so every key this host consumes is visible in one place. |
| `COCHANGE_STANDS_IN_FOR` | `:1509` | **FWD-6's declaration**, carrying the measurement behind it: which tool, which grain, why it is not a drop-in, and where the retirement path actually is. |
| declaration on **both** host exits | `:1355` (computed) and `:1318` (git-FAILED) | It travels in the **rendered denominator and vintage**, not a comment. `claim=host-computed`. |

**Production is byte-unchanged:** `ESTATE_OUTSET_SEAM_PREFIX` is unset by default (OS-s-10's decision, not mine), so every production run still takes the host branch -- now declaring itself.

**The gap my own battery caught in my own change:** the first version put the declaration only on the *computed* exit. Arm D2 failed with `vintage=repo @PIN` -- the **git-FAILED early return** rendered without it. That matters: a reader seeing `GROUP B INSTRUMENT_FAILED` would conclude *a tool failed*, when no tool was ever called. Fixed at `:1318`.

## 3. ACCEPTANCE

### O9-AC1 -- PASS by output

`timeout 120 python .tools/tests/test_os9_cochange_source.py` - expect `PASS` - **rc 0**

```
=== test_os9_cochange_source: PASS (16/16) ===
```

**Denominator: 16 of 16 arms.** Also at the second required grain: `python -m pytest -q` -> `1 passed in 4.10s`.

| arm | what it proves |
|---|---|
| A1-A3 | with a prefix configured, the rows **are** the artifact's rows (a `OS9-SENTINEL-PAIR-NOT-FROM-GIT` sentinel makes provenance *falsifiable*, not merely plausible), the vintage names the **tool**, and the denominator carries the **tool's** denominators |
| **B2 RED MUTANT** | the criterion's named mutant, **executed**: the seam branch deleted from a temp copy of the runner restores the host-git path -> the sentinel cannot appear (`sentinel_present=False`) |
| C x6 | a failed publish reads **FAILED, never a clean empty**: ABSENT, not-JSON, foreign seam tag, STALE, FUTURE-DATED, unmapped `answer_state` -- each a non-OK stratum with `rows == []`, `row_count is None`, and its own reason |
| D1, D2a, D2b | FWD-6's declaration names the tool + grain + seam key, and reaches the **rendered** stratum on **both** host exits |
| **D3 RED MUTANT** | the declaration emptied *at its definition* breaks D2a **and** D2b |
| E1 | the grain claim is **re-measured live**, not asserted: `grain='type'`, agent tags, no resource label |

No AWS, no network. Arm E runs the co-change **engine** directly under `sys.executable` -- never a bash launcher -- which sidesteps both host hazards at once (a bare `subprocess.run(["bash", ...])` reaches the WSL stub; `timeout=` does not bound a shell launcher because the grandchild holds the stdout pipe).

**Regression:** `.tools/tests/test_os10_seam.py` -> `OS10-SEAM BATTERY: 12/12 PASS`, rc 0 -- the contract between the two seam halves still holds after I added a consumer to it.

### O9-AC2 -- JUDGMENT (`judgment="true"`) -- EVIDENCE ONLY, NO VERDICT

**A citation note first** (row `W2-S16`): at HEAD `:1308` is correct, but **`:1996` is a bare `#`** inside a comment block -- the wiring is at **`:2149`**. I quote both the cited line and the line the citation means, labelled.

**BEFORE**, `git show HEAD:...` @`8c231d47bf`:
```
1308: def _stratum_cochange(repo_dir: str, end, maps: dict, pin: str) -> dict:
1996: #                                     <- the cited line; a comment-block filler
2149:             "B": _stratum_cochange(repo, end_local, maps, pin),      <- the actual wiring
```

**AFTER** (worktree):
```
1308: def _stratum_cochange(repo_dir: str, end, maps: dict, pin: str, prefix=..., loader=None,
1327:     prefix = OUTSET_SEAM_PREFIX if prefix is ... else prefix
1328:     if prefix:
1332:         src = prefix.rstrip("/") + "/" + OUTSET_COCHANGE_KEY
1333:         r = _outset_read(src, loader or _outset_loader, ...)
1334-1336:   return _stratum("B_relationships", ..., status=r["status"], error=r["error"])
2221:             "B": _stratum_cochange(repo, end_local, maps, pin),      <- wiring, unchanged
```
The wiring is **deliberately unchanged**: the call site passes no prefix, so the default `prefix=...` resolves to the module-level `OUTSET_SEAM_PREFIX` at call time. Injection is for the battery; production reads its own env.

**THE HOST COPY STAYS, AND HERE IS ITS DECLARATION** (`:1509`, rendered into the denominator of every host-path stratum):

> STAND-IN DECLARATION (FWD-6): these rows are computed on this HOST from git metadata, not by a tool. They stand in for a RESOURCE-GRAIN co-change answer published through the OS-s-10 seam as `<ESTATE_OUTSET_SEAM_PREFIX>/comp_cochange.json`; when that artifact exists this stratum reads it and stops computing. THE NAMED TOOL IS NOT A DROP-IN AND THAT IS MEASURED, NOT ASSUMED: `.tools/comp-cochange` answers AGENT-TYPE/SERIAL co-movement (`--grain {type,serial}`; a live matrix run yields agent tags, not resource labels), while these rows pair pipeline-chain labels from `attribute_path()`. Same word, different axis -- substituting it would answer a different question under the same heading. `claim=host-computed`.

Rendered vintage on the host path: `host git history @<pin>, trailing 14d -- STAND-IN, not a tool answer (claim=host-computed)`.

**What I did not do, and why:** I did not point the stratum at `comp-cochange` (it would fill a resource-co-change heading with agent-co-movement rows and *look* like a completed retirement); I did not add a `--grain resource` mode to the tool (a second implementation, and out of `<paths>`); I did not delete the host copy (that removes the measurement outright).

## 4. THE HONEST LIMIT OF O9-AC1

Row `W2-S15`. **Nothing publishes `comp_cochange.json`.** `outset_seam.py:243-250` registers exactly two producers, both comp-heat, and that file is not in my `<paths>`. Even once registered, the runner's applied role grants `s3:GetObject` on `opal-estate-report/{daily/*,code/*,manifest/*}` plus one exact key and **nothing on the globgrph bucket** (`estate_report_runner.py:1440-1447`; `W1-S19`). So O9-AC1 is satisfiable as a **contract test against an injected artifact** -- which is what the battery is, and what OS-10's own battery is, for the same reason -- and **never as a live end-to-end read on this fabric**. 16 green arms are not a live seam, and I say so rather than letting the count imply it.

## 5. GATES

| Gate | Result |
|---|---|
| `bash .tools/commit-gate.sh <runner> <battery>` | `OK: pre-commit gate clean for 2 of 2 file(s)`, rc 0 |
| non-ASCII introduced by this cell | **0** (3 pre-existing lines are a unicode-punctuation transliteration map, non-ASCII by purpose) |
| `comp-system --gate --changed` (both arms) | `NOT_APPLICABLE ... gate open`, rc 0 on **both** -- this cell's pathspec matches none of the comp-system triggers, so the `06_current_state` pair is untouched and was correctly **not** granted here |

## 6. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W2-S14` | OBSERVATION / **ARMED** | no tool exists at this grain; a later "completion" that swaps in `comp-cochange` would answer a different question under the same heading |
| `W2-S15` | OBSERVATION / **ARMED** | the seam branch is dormant: no producer (out of `<paths>`) and no IAM grant (`W1-S19`) |
| `W2-S16` | OBSERVATION / INERT | `:1996` is not the wiring; a bare line number is a pointer into a moving file |
| `W2-S17` | OBSERVATION / INERT | **self-reported**: my first declaration mutant left a second live carrier, so it passed while measuring nothing |

## 7. DECLARED NON-APPLICATIONS

- **`org/modules/heatmap/outset_seam.py` not edited** -- registering a resource-grain producer is the real retirement path and that file is outside `<paths>`. Row `W2-S15`, not a workaround.
- **No IAM change** -- the runner's grant covers no seam prefix; this cell adds a second key under the same prefix and widens nothing. `W1-S19` already carries it.
- **No default for `ESTATE_OUTSET_SEAM_PREFIX`** -- a default would point the runner at a prefix nobody publishes to and convert a quiet `INSTRUMENT_UNAVAILABLE` into a daily `INSTRUMENT_FAILED`.
- **No monitor, alarm or freshness-checker; no delete verb; no new dependency; no second implementation** (the reader is OS-s-10's, reused).
