# TO-OS-s-3 result -- a plain-English freshness/archive question routes to comp-heat

**TO:** `NFRA_OUTSET.TO-OS-s-3` (`org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-3.router-rule-for-a-heat-question.md` @`c3449745ec`)
**Cell:** `OS-s-3` · **outcome_ref:** FWD-1 · **verb:** wire · **depends_on:** OS-s-1, OS-s-2
**Executed by:** `0.9.0_WK_NFRA_OUTSET~2` in worktree `C:/tmp/wk-OUTSET-2`, branch `wk-OUTSET-2`, base HEAD `22e38e7963`
**Both addressing limbs were correct at seating** (`<issued_to>` = `~2`, deliverables folder = `~2`), so no carry step was needed. Verified at branch HEAD, not from a checkout.

> **HEADLINE: two of three criteria PASS. `O3-AC3` FAILS and I did not bend anything to change that.** Its own invocation cannot produce its own `<expect>` under the order's own mandatory bound, by a factor of at least 6.4x, and it could not before this cell touched anything. Rows `NFRA_OUTSET-W2-S7` (BLOCKING) and `-W2-S8` (a second, independent limb). **`<status>` is NOT flipped.**

---

## 1. WHAT I MEASURED FIRST

`comp-which` scores a question two ways: a curated `RULES` list (`comp-which:89`, `_score_rule` at `:1259` -- substring phrases +3, single tokens +2, vetted band `>= 1.0`) and a small set of forced-score regexes that beat a co-occurring search verb (`HEAT_RX` at `:1210`). Below the vetted band the tool prints `NO CURATED RULE MATCHED`; if nothing routes at all it RUNS `comp-find` as a never-dead-end (`_run_primitive`, `:1632`).

Measured on the committed router at `22e38e7963`, each question via its own CLI invocation:

| question | PRE |
|---|---|
| `what is stale and safe to archive` (**O3-AC1**) | `1. score 2.00  comp-heat freshness [path]` -- **already routed** |
| `what have I not touched in months` (**O3-AC2**) | **RAN comp-find** -- a content search for `touched`, 8371 hits across 28886 files |
| `files I haven't touched since June` | RAN comp-find (8388 hits) |
| `which paths have not been touched in a long time` | RAN comp-find (8395 hits) |
| `when was this last touched` | RAN comp-find (8378 hits) |
| `show me untouched directories` | `1. score 0.28  comp-adversary` (sub-vetted fuzzy guess) |
| `what went cold in the repo` | `1. score 1.50  comp-iam-usage role-cold` -- a **confident curated-band answer to a different question** |

**1 of 7.** The gap is a real vocabulary gap: comp-heat's curated rule covered `stale files`, `safe to archive`, `cold subtrees`, `uncommitted` -- and had **nothing at all** for the *last-touched / write-age* phrasing of the same question, which is the most natural way to ask it. The last row is the worst shape: not an absence but a confident mis-route to IAM role coldness.

## 2. WHAT I CHANGED -- `.tools/comp-which`, two places, 20 insertions

| Change | Where | What |
|---|---|---|
| curated vocabulary | comp-heat's `RULES` entry, `:791` onward | The last-touched / write-age family: `not touched`, `not been touched`, `havent/haven't touched`, `hasnt/hasn't been touched`, `never touched`, `untouched`, `nobody has touched`, `no one has touched`, `last touched`, `when did i last touch`, `gone cold`, `went cold`. |
| forced-score override | `HEAT_RX`, `:1214` | The same intent, above a co-occurring search verb. **Necessary because AC2's measured failure was not a tie** -- the never-dead-end primitive won outright, so keywords alone would have been scored and then bypassed. This is exactly why the existing estate-hygiene phrasings already sit in `HEAT_RX`. |

**Why this is comp-heat's question and not a string to satisfy a test:** `comp-heat freshness` bands paths by *age vs barriers* (`hot<=7d, warm<=30d, cold>30d`) and ranks the coldest. "What have I not touched in months" is that computation stated in English. The addition is the same move this file documents dozens of times in its own comments ("*had NO curated rule at all... Add the actual vocabulary*").

**Deliberately time-scoped so it steals nothing.** The estate already has WHO-touched routes -- `node touching a symbol` -> comp-xref (`:164`), `who touched the bucket` (`:1026`), `touching a gold script` (`:766`). Those ask *which agent* touched a thing; mine ask *when it was last written*. None of them carries a negation or a `last`/`never` qualifier, and none of my keywords matches them. Verified, not argued -- see §4.

## 3. ACCEPTANCE

### O3-AC1 -- PASS by output

`timeout 120 .tools/comp-which "what is stale and safe to archive"` -- **rc 0**

```
comp-which -- candidates for: "what is stale and safe to archive"
  MATCHES (top 3 of 79 -- score is overlap, NOT a confidence):
  1. score 2.00   comp-heat freshness [path]
```
`<expect>` `comp-heat` present at rank 1; no `NO CURATED RULE MATCHED` banner. **Denominator: 1 of 1 invocation matches.**
**Disclosed honestly: this criterion passed BEFORE the change too** (§1). Its PASS is not evidence of work -- row `NFRA_OUTSET-W2-S9`.

### O3-AC2 -- PASS by output

`timeout 120 .tools/comp-which "what have I not touched in months"` -- **rc 0**

```
comp-which -- candidates for: "what have I not touched in months"
  MATCHES (top 3 of 79 -- score is overlap, NOT a confidence):
  1. score 2.00   comp-heat freshness [path]
  2. score 0.06   comp-pipescript dag --pipeline <tree> [--json]
```
**Denominator: 1 of 1.** This is the criterion that was genuinely red: PRE it produced no route at all and ran a content search instead.

### O3-AC3 -- **FAIL**, and the recorded output is a timeout

`timeout 120 python .tools/comp-which-routing-test.py` -- **the bound expired; no verdict line produced** (152 lines of output, `grep -c -E "^\s*(PASS|FAIL)\b"` = **0**).

Measured **three times**, two of them on the committed router *before* this cell changed anything:

| run | form | bound | result |
|---|---|---|---|
| 1 | literal (as the criterion writes it) | 120 s | bound expired, no verdict |
| 2 | `--out <scratch>` (the tool's own regression form) | 120 s | bound expired, no verdict |
| 3 | `--out <scratch>` | **600 s** | rc 124 at 600 s (05:46:25Z -> 05:56:27Z), no verdict |

**The reason is architectural, measured, not inferred.** `.tools/comp-which-routing-test.py:284` runs `subprocess.run([sys.executable, COMP_WHICH, q])` -- **one comp-which subprocess per cohort question** -- with further subprocess sites at `:606` and `:996`. Cohort sizes from the harness's own frozen artifact: `cohort_R_raw` **562**, `cohort_R_strict` **556**, `cohort_C` **87**, plus `self_route_verdicts` over ~69 tools and ~45 instrument controls. One comp-which subprocess costs a measured **1.01 s** (3 consecutive calls, 3.03 s). So **>= 763 invocations >= ~770 s**, at least **6.4x** the criterion's own mandatory bound. A bracket, not a point -- the second `measure()` pass only widens it.

**A second, independent limb** (`NFRA_OUTSET-W2-S8`): the criterion's literal form carries no `--out`, and the harness's default output is `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline.json` -- **another seat's tree, outside this order's `<paths>`** -- which the tool's own `--help` calls a clobber hazard that has fired once before. Nothing was clobbered here (`git status --porcelain -- org/tier2_senior/` empty after every run) only because no run reached the write. **Raising the bound without adding `--out` would convert that latent hazard into a live one.**

**What I refused to do:** substitute a cheaper battery of my own and grade AC3 against it (a different instrument answers a different question, and the order says a mechanical criterion's pass is decided by *the match*); raise the bound and call the result PASS; edit the harness or the criterion.

**What I did instead, as evidence rather than as a verdict:** ran `python org/modules/graph/tests/test_compwhich_toolpass_rules.py` -- a routing-rank battery, run-only, not edited -- against **both** routers:

```
committed router : 1 failed, 26 passed, 1 xpassed  in 26.95s   rc=1
changed router   : 1 failed, 26 passed, 1 xpassed  in 26.95s   rc=1
```
Identical. The single failure is `Touching MP/benchmarks/ADVI backend -> comp-surface-check`, a **pre-existing** case naming the tool CLAUDE.md Rule 20 records as RETIRED. **Denominator: 28 of 28 outcomes unchanged by this cell.** That is the regression assurance AC3 exists to give; it is offered as evidence and AC3 stays FAIL.

## 4. THE HONESTY CHECK -- does the router *answer the question*, or did I just make the string appear?

The issuer's warning on this cut was that the criterion cannot tell those apart. So the criteria are not my evidence.

**Held-out phrasings** (none is a criterion sentence; none is a literal keyword for two of them), PRE and POST on the faithful instrument:

| held-out question | PRE | POST |
|---|---|---|
| `files I haven't touched since June` | RAN comp-find | **2.00 comp-heat** |
| `when was this last touched` | RAN comp-find | **2.00 comp-heat** |
| `show me untouched directories` | 0.28 comp-adversary | **2.00 comp-heat** |
| `what went cold in the repo` | 1.50 comp-iam-usage | **2.00 comp-heat** |
| `which paths have not been touched in a long time` | RAN comp-find | **2.00 comp-heat** |

**Negative controls -- must NOT move:**

| question | PRE | POST |
|---|---|---|
| `who touched the bucket` | 1.50 comp-whoread | 1.50 comp-whoread |
| `every graph node touching a symbol` | 2.00 comp-xref | 2.00 comp-xref |
| `which agent types change the same files` | 1.50 comp-cochange | 1.50 comp-cochange |
| `is the gold data fresh enough to run the chain` | 1.83 comp-freshness | 1.83 comp-freshness |
| `am I touching a held or frozen file` | 1.50 comp-pulse | 1.50 comp-pulse |
| `cold roles and unused permissions` | -- | 1.67 comp-iam-usage role-cold (**not stolen**, though `what went cold in the repo` correctly moved away from it) |

**5 of 5 held-out route; 6 of 6 controls keep their routes; 1 of 7 heat-intent phrasings routed before, 7 of 7 after.**

## 5. THE INSTRUMENT TRAP I HIT, REPORTED AGAINST MY OWN FIRST TWO ANSWERS

Row `NFRA_OUTSET-W2-S10`. Both cheap ways of measuring the PRE router were **wrong, in opposite directions, and both looked clean**:

- a copy of the committed `comp-which` run from `.scratch/` reported **0 of 7** routing PRE. Cause: `comp-which:33` sets `WS = dirname(dirname(abspath(__file__)))`, so a copy out of place resolves the wrong workspace, finds no manifest, and **fails soft** to the never-dead-end primitive for every query. There is no workspace env override to fix it with.
- an in-process `exec` of the same PRE source reported **7 of 7** routing PRE.

The faithful instrument -- committed bytes restored to the **real path**, invoked exactly as the criteria invoke them, then the changed bytes restored and proved byte-identical (`cmp -s`) -- says **1 of 7**.

**What caught it was not a control but a contradiction:** the first proxy disagreed with a direct measurement already taken on the real binary. Had I not measured before editing, "0 of 7 before, 7 of 7 after" would have been reported as a clean result that **overstates this cell's own effect**. This is the same false-clean family as `NFRA_OUTSET-W2-S1`, arriving in the *verification* rather than in the tool.

## 6. A CAVEAT ON EVERY ROUTING NUMBER ABOVE

Row `NFRA_OUTSET-W2-S11`. Every `comp-which` invocation on this fabric prints:

```
ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance
(ValueError: POTION hash-mismatch on tokenizer.json: manifest=e67e803f... vendored=0a1168df... (FAIL-CLOSED))
```

The router is running **lexical-only**. My two mechanisms (`_score_rule` substring/token matching, and a regex) are unaffected by the embedder, but the ranking they compete in is not. Every number here is sound for the lexical path and **unmeasured for the semantic one**. The vendored asset is outside this order's `<paths>` and was not touched; a FAIL-CLOSED hash guard is not something a passer-by works around.

## 7. GATES

| Gate | Result |
|---|---|
| `bash .tools/commit-gate.sh .tools/comp-which` | `OK: pre-commit gate clean for 1 of 1 file(s)`, rc 0 |
| `python -m py_compile .tools/comp-which` | clean |
| non-ASCII check on the edit | 0 lines (the file declares itself ASCII-only) |
| `comp-system --gate --changed .tools/comp-which` (**PATH shim** -- the arm safe-commit reaches) | `SYSTEM CURRENT (no genuine drift) -- gate open.` rc 0 |
| `bash .tools/comp-system --gate --changed .tools/comp-which` (**worktree-local**) | `SYSTEM BLOCKED-ON-PEER-LANDING: genuine drift ... rc 2` |

**The two arms disagree, in the permissive direction** -- row `NFRA_OUTSET-W2-S12`, the load-bearing instance of the hazard `W2-S5` could only show latently on OS-s-8. The commit-time gate opens on drift it did not grade, because the PATH shim pins `WORKSPACE` to the main tree. So I regenerated `infra/system/06_current_state.{json,md}` with the **worktree-local** arm -- the one that can see the change -- and committed the pair, because the drift is real, not because a gate forced it.

## 8. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W2-S7` | **BLOCKING** / ARMED | O3-AC3's invocation cannot produce PASS under the order's own `timeout 120`; >= 763 subprocesses, >= ~770 s; pre-existing |
| `W2-S8` | OBSERVATION / ARMED | O3-AC3's literal form writes an out-of-grant baseline the tool's own help calls a clobber hazard |
| `W2-S9` | OBSERVATION / INERT | the cell's premise, AC1 and AC2 are three different questions; AC1 was already green |
| `W2-S10` | OBSERVATION / ARMED | two cheap PRE/POST proxies both returned confident wrong numbers, in opposite directions |
| `W2-S11` | OBSERVATION / ARMED | every routing measurement here is against a lexical-fallback router (POTION FAIL-CLOSED) |
| `W2-S12` | OBSERVATION / ARMED | the comp-system arms disagree on a real `_SOURCE`; the commit-time gate fails open |

## 9. DECLARED NON-APPLICATIONS

- **No new battery in `.tools/tests/`.** The order's acceptance names three invocations and none asks for one; inventing one would have read as a substitute for the AC3 I could not pass. The regression evidence I *could* produce under a bound came from an existing battery, run-only.
- **`.tools/comp-which-routing-test.py` not edited** -- outside `<paths>`; it is AC3's subject, and editing the instrument that grades you is not a repair.
- **`what is comp-heat` still does not route** (top score 0.61, still `NO CURATED RULE MATCHED`). That is a DESCRIBE-the-tool intent, a different question from the two criteria, and out of this cell's scope -- recorded in `W2-S9`, not silently fixed.
- **No monitor, alarm or freshness-checker; no delete verb; no new dependency; no second implementation.**
