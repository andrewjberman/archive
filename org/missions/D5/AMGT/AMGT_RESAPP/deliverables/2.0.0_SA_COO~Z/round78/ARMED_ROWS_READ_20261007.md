# AMGT_RESAPP -- the thirteen ARMED rows read one by one: hazard or not, as of 2026-10-07

**For:** `2.0.0_SA_COO~Z` (the round-77 analysis asked for "hazard-or-not per row"). **Read at:** shared tree, branch CLOUD, HEAD `e44a704705`.
**Nothing was changed.** No vendor call, no store write, no deploy. One store read was taken (the bb-1 check, reads only).

**Counts: HAZARD LIVE 0, NOT A HAZARD NOW 11, NEVER A HAZARD 2, CANNOT TELL 0. Sum 13.**

Where the rows live: nine are in `surprise-channel/investigations/INVESTIGATION_v1.md` (947 rows parsed, 0 blocks failed to parse).
The four `Z-C-*` ids are NOT rows of that file: they are the CVO's adjudication rows, in `adjudications/ADJUDICATION_v1.md`
(C-S2, C-S3), `ADJUDICATION_v5.md` (C-S35) and `ADJUDICATION_v24.md` (C-S372).

Every one of the thirteen still reads OPEN and ARMED on its remediation row (`remediations/REMEDIATION_v1/v13/v14/v15.md`), except
W289-S1 and W299-S1, which have no remediation row yet. Those clocks are the CVO's to move; this file is the evidence for moving them.

## Summary

| row | surfaced | verdict | the one deciding fact | who must act |
|---|---|---|---|---|
| Z-C-S2 | 2026-09-11 | NOT A HAZARD NOW | Six of seven members are fixed or sit in complete orders; the seventh (receiving-check grades one file at a time) was ruled NOT_A_DEFECT by the CTO @`4a89bef967` section D | `2.0.0_SA_COO~Z`: print "checked N of N" with the list in the round-78 drain-end packet. That line is what closes the row; the round-76 and round-77 packets do not carry it |
| Z-C-S3 | 2026-09-11 | NOT A HAZARD NOW | Three of four members fixed and re-measured today; on the fourth, comp-find now reports a provider binary as "BINARY, NOT searched" | `0.8.0_AE_CloudComp`: the ruled one-line add of `.terraform` to EPHEMERAL_DIRS has not landed (tidy-up, not a hazard) |
| Z-C-S372 | 2026-09-22 | NOT A HAZARD NOW | `harvest_serp` raises on `max_pages != 1` since `b1ba4f40a1` | nobody |
| Z-C-S35 | 2026-09-11 | NOT A HAZARD NOW | `lib/research/watchlist/tests/conftest.py` applies the socket block to every test (autouse) since `b1ba4f40a1` | nobody |
| Z-W4-S1 | 2026-09-11 | NOT A HAZARD NOW | The script is unchanged, but 0 of 3 open orders name it and the three orders that do are complete | nobody |
| Z-W2-S3 | 2026-09-11 | NOT A HAZARD NOW | Same fact as the fourth member of Z-C-S3; no round-77 or round-78 check uses `grep -r` | `0.8.0_AE_CloudComp` (same one line) |
| Z-W31-S2 | 2026-09-17 | NOT A HAZARD NOW | 0 of 3 open orders and 0 of 55 round-77/78 check scripts carry `npx tsc`; the ten orders that do are complete or superseded | nobody now; the device behaviour itself was NOT MEASURED |
| Z-W42-S5 | 2026-09-19 | NEVER A HAZARD | The row's own text: two bars missed on one sample for content reasons, graded FAIL honestly, nothing served wrong | nobody |
| Z-W88-S1 | 2026-09-22 | NOT A HAZARD NOW | Same fix as Z-C-S372 (`b1ba4f40a1`); the writer has no non-test caller | nobody |
| Z-W117-S5 | 2026-09-22 | NOT A HAZARD NOW | `dapi_check.py` still sends a live request, but 0 of 3 open orders and 0 of 55 check scripts name it | nobody now; the cut-time habit has no mechanism |
| Z-S242 | 2026-09-24 | NOT A HAZARD NOW | `etf-classifications.tf` re-committed with LF at `02a7be55d5`; the index reads `i/lf` | nobody |
| Z-W289-S1 | 2026-10-07 | NOT A HAZARD NOW | Two-pass object choice in `segment_table.py:136-144`; the check reads AMD from `20261007T115113Z` and SERVED: YES | `2.0.0_SA_COO~Z` to note one residual: the reader looks at the newest 5 objects only |
| Z-W299-S1 | 2026-10-07 | NEVER A HAZARD | Filed INERT; a stale constant in a check failed loudly; the check was amended in `9152a98bc5` and reads SERVED: YES | nobody |

## Per row

### Z-C-S2 (CVO adjudication row, 2026-09-11T03:05Z, BLOCKING, GRADUATED, disarm_owner "per row")
- **one_line:** seven criteria or instruments whose verdict cannot move with the build (W7-S1, W2-S2, W3-S4, W7-S5, W3-S2, W7-S2, S2).
- **spec_asserts:** a criterion's invocation demonstrates the cell's outcome. **world_is:** seven cannot.
- **Sibling files:** `REMEDIATION_v15.md` row Z-C-S2: six of seven fixed or in terminal orders; S2 still live; state OPEN, owner
  `1.0.0_SA_CTO~Z`. CTO ruling `ledger/CTO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md:52-57`: RULED-CLOSED, NOT_A_DEFECT, "the packet
  line is the mechanism". `ADJUDICATION_v92.md:24` (CVO, row C-S467): held OPEN because the round-76 packet has no such line.
- **Re-measured today:** orders s-2, s-6, s-7, s-9 last `<status>` complete (4 of 4 read). `e9d19be279` is an ancestor of HEAD.
  `.tools/receiving-check.py:87` still routes a task order as `lambda p: [p]` and `:183` still runs `run_one` per path.
  `round77/DRAIN_END_PACKET.md`: 0 lines match "checked", "receiving-check" or "N of N".
- **Verdict:** NOT A HAZARD NOW. The one live member fails loudly (it refuses, it does not pass wrongly) and is ruled not a defect.
  What is owed is the packet line, by `2.0.0_SA_COO~Z`, in the round-78 packet.

### Z-C-S3 (CVO adjudication row, 2026-09-11T03:05Z, OBSERVATION, GRADUATED, disarm_owner "per row", routed to the CTO)
- **one_line:** four instruments return a clean wrong answer on this device (W2-S4 shim, W2-S3 grep into a binary, W1-S3 gitignored
  `lib/`, W1-S4 empty `.gitmodules`).
- **Sibling files:** `REMEDIATION_v15.md` row Z-C-S3: three fixed, W2-S3 still live, OPEN. CTO ruling `:79`: re-owned to
  `0.8.0_AE_CloudComp`, add `.terraform` to EPHEMERAL_DIRS.
- **Re-measured today:**
  - W1-S3: `git check-ignore -v lib/research/newdir_probe/x.py` rc=1 (not ignored); positive control `node_modules/x` rc=0.
  - W1-S4: `.gitmodules` maps `portal`.
  - W2-S4: `~/bin/comp-routes` resolves the caller's own git toplevel first.
  - W2-S3: `.tools/_comprail.py:340-341` EPHEMERAL_DIRS still has no `.terraform`; 23 `.terraform` caches exist under
    `infra/aws/terraform/*/`. But `python .tools/comp-find "0\.0\.0\.0" infra/aws/terraform/bloomberg-tunnel --files` printed
    "0 hit(s) across 6 file(s) scanned ... 2 BINARY, NOT searched". The rail does not read the provider binary.
- **Verdict:** NOT A HAZARD NOW. Residual: text files inside a `.terraform` cache are still in the corpus, so the one-line add is
  still worth landing.

### Z-C-S372 (CVO adjudication row, 2026-09-22T07:35Z, GRADUATED, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** SERP records carry no page tag, so a multi-page harvest cannot give each silver row its exact bronze key.
- **spec_asserts:** every silver row carries the bronze key it came from. **world_is:** true for one page only.
- **Sibling files:** `REMEDIATION_v15.md` row: OPEN, "no refusal of max_pages > 1" (written before the repair). COO ruling
  `round76/COO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md:26`: refuse above 1. Cut as item 3 of order AMGT-ba-12.
- **Re-measured today:** `lib/research/harvest/bright_data_serp.py` `harvest_serp` (def at `:81`) opens with
  `if max_pages != 1: raise ValueError(...)`. Commit `b1ba4f40a1`, an ancestor of HEAD. Order ba-12 last status complete.
  `git grep "harvest_serp("`: 1 definition, 0 non-test callers, 2 calls in the check `r77_ba12.py`.
- **Verdict:** NOT A HAZARD NOW.

### Z-C-S35 (CVO adjudication row, 2026-09-11T21:39Z, GRADUATED, disarm_owner 2.0.0_SA_COO~ZZZ)
- **one_line:** the socket negative control did not guard the whole watchlist test suite (2 of 5 tests unguarded).
- **Sibling files:** `REMEDIATION_v15.md` row: OPEN (written before the repair). COO ruling `:23`: one conftest. Item 1 of ba-12.
- **Re-measured today:** `lib/research/watchlist/tests/conftest.py` exists with an `autouse=True` fixture that requests
  `block_all_sockets`. Commit `b1ba4f40a1`. `pytest lib/research/watchlist/tests lib/research/harvest/tests/test_bright_data_serp.py`:
  15 passed, 0 failed (the two files together; not split).
- **Verdict:** NOT A HAZARD NOW.

### Z-W4-S1 (2026-09-11T00:26Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~ZZZ)
- **one_line:** re-running `f6_remeasure.py` overwrites worker ~3's committed `f6_remeasure.json` in place.
- **spec_asserts:** AC1 treats the script as a read. **world_is:** it writes beside itself; only the two time fields move.
- **Sibling files:** `ADJUDICATION_v1.md` row C-S4 graduated it; `ADJUDICATION_v92.md:14` closed C-S4 as carried by its children.
  `REMEDIATION_v1.md` row Z-W4-S1: OPEN, ARMED.
- **Re-measured today:** `deliverables/0.9.0_WK_AMGT_RESAPP~3/f6_remeasure.py:65` still derives OUTPUT_PATH from `__file__` and
  `:234` still opens it "w". Orders naming the script: 3 of 416 (av-5, s-12, s-8), all complete. Open orders: 3 (bb-17 pending,
  bb-18 and bb-19 staged); 0 name it. `git status` on the folder: clean.
- **Verdict:** NOT A HAZARD NOW. The mechanism is still in the file, but nothing asks anyone to run it, the content it writes is
  identical, and a worker cannot commit the changed file outside its own paths.

### Z-W2-S3 (2026-09-11T00:47Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~ZZZ)
- **one_line:** a `grep -r` criterion counted a byte coincidence inside a gitignored terraform provider binary, reading 1 for 0.
- **Sibling files:** `ADJUDICATION_v1.md` row C-S3; `REMEDIATION_v14.md` row: OPEN; CTO ruling `:79` re-owned to
  `0.8.0_AE_CloudComp`.
- **Re-measured today:** as Z-C-S3 above. `infra/aws/terraform/research/.terraform` does not exist now. Check scripts using
  `grep -r`: 0 of 27 (round 77) and 0 of 28 (round 78). The rail hook `.tools/hooks/comp-tool-hud.sh` and its switch
  `org/mcp/comprail-gate1.enforce` are both present; the denial of a raw `grep -r` was not exercised here (forbidden in this read).
- **Verdict:** NOT A HAZARD NOW.

### Z-W31-S2 (2026-09-17T20:55Z, UNDER_INVESTIGATION, disarm_owner 0.4.0_DT_ClientPlatform)
- **one_line:** in a bun-only worktree `npx tsc -b` runs a decoy registry package and compiles nothing, exit 0.
- **Sibling files:** `ADJUDICATION_v13.md` row C-S315: graduated, INERT; both round-13 criteria were re-cut to the local binary
  (`5b767811e7`, `9074091db1`). `REMEDIATION_v13.md` row: OPEN, ARMED, owner `0.4.0_DT_ClientPlatform`.
- **Re-measured today:** orders carrying `npx tsc`: 10 of 416, all complete or superseded; 0 of the 3 open orders. Check scripts
  mentioning `tsc` at all: 0 across rounds 75-78. `portal/package.json` has `packageManager: bun@1.0.0` and
  `typecheck: tsc -b --noEmit`; `portal/.npmrc` still has `package-lock=false`.
- **Verdict:** NOT A HAZARD NOW: no live criterion is written that way. The device behaviour was not re-run (see NOT MEASURED).

### Z-W42-S5 (2026-09-19T11:10Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** on one live sample, blocks per citation read 1/1/2 against a bar of 1/1/1 and verbatim characters 57 of 67 (85.1%)
  against 0.90; both traced to the filing's content, not the code.
- **Sibling files:** `ADJUDICATION_v14.md` row C-S335: graduated as the class anchor ("a bar written without measuring the file"),
  INERT; the CTO ruled the remedy a habit, not a gate. `REMEDIATION_v14.md` row: OPEN, "a cutting habit with no mechanism".
- **Re-measured today:** order AMGT-rk-40 last status complete. Nothing else to measure: the row claims no wrong output.
- **Verdict:** NEVER A HAZARD. The row records a measured shortfall and an honest FAIL on AC4; no harm path is stated. The class
  it anchors (a bar tied to a state that can move) showed up twice today, as W289-S1 and W299-S1, and both were caught by the
  check failing loudly.

### Z-W88-S1 (2026-09-22T00:01Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** `harvest_serp` gives every row the LAST page's bronze key when more than one page is fetched.
- **Sibling files:** `ADJUDICATION_v24.md` row C-S372; `REMEDIATION_v14.md` row: OPEN (before the repair); item 3 of ba-12.
- **Re-measured today:** as Z-C-S372. A call with `max_pages=2` now raises; the last-page line is reachable only with one page,
  where it is exact.
- **Verdict:** NOT A HAZARD NOW.

### Z-W117-S5 (2026-09-22T21:31Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** AC0 named `dapi_check.py`, which sends a real Bloomberg request each run, inside a cell sized at 2 requests.
- **Sibling files:** `ADJUDICATION_v35.md` row C-S397: graduated, INERT, with the rule "a criterion that fires egress in a baseline
  step is refused at the cut". `REMEDIATION_v14.md` row: OPEN, no mechanism found.
- **Re-measured today:** `integrations/bloomberg/auth/dapi_check.py:41-44` still builds and sends a ReferenceDataRequest (last
  commit `75d44454fd`). Orders naming it: 4 of 416 (rk-113, rk-116, rk-117, s-1), all complete; 0 of the 3 open orders. Check
  scripts naming it: 0 of 55 (rounds 77 and 78).
- **Verdict:** NOT A HAZARD NOW. It returns only if a future order names the probe in a criterion; that is a habit at the cut.

### Z-S242 (2026-09-24T00:45Z, GRADUATED, disarm_owner 1.0.0_SA_CTO~Z to route)
- **one_line:** `etf-classifications.tf` was CRLF in the index against `eol=lf`, so `git status` could call identical bytes modified.
- **Sibling files:** `REMEDIATION_v14.md` row: OPEN, "the LF re-commit has not landed" (written before it did). CTO ruling `:78`:
  re-owned to `0.7.0_AE_CloudOps`, one LF re-commit. Cut as order AMGT-ba-26.
- **Re-measured today:** `git ls-files --eol`: `i/lf w/crlf attr/text eol=lf`. `git log` on the path: `02a7be55d5` (ba-26, AE~A)
  on top of `39810307ce`; an ancestor of HEAD. `git status --porcelain` on the path: empty. Class check: tracked files that are
  `i/crlf` under an `eol=lf` attribute: 0 of 62,269.
- **Verdict:** NOT A HAZARD NOW.

### Z-W289-S1 (2026-10-07T16:03Z, UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** AMD's newest stored segments object was a different-field pull with no revenue fields, and the literal rule chose it.
- **spec_asserts:** usable = no revenue error AND (carries a PG field OR has no field errors). **world_is:** the newest object
  passed that rule with no table, so AMD read no rows and C1 failed.
- **Sibling files:** none names it (0 hits in `adjudications/` and `remediations/`).
- **Re-measured today:** `lib/research/api/segment_table.py:105-107` `_carries_table`; `:136-139` first pass picks the newest
  object that carries a table; `:140-144` second pass falls back to the original rule. Commits `6cf8a0d403` (amendment 1) and
  merge `52daa06f53`, an ancestor of HEAD. Ran `r78_bb1.py --crit AC1 --where local` (store reads only, repo root on PYTHONPATH):
  C1 PASS "6 row(s); source 20261007T115113Z.json"; C4 PASS 85 of 85 (76 serving, 9 with a reason); SERVED: YES. AC2 SERVED: YES.
- **Verdict:** NOT A HAZARD NOW. One residual for the issuer: `MAX_READ = 5` (`:19`, `:130`), so five newer objects without a
  table in one name's folder would hide the table again. AMD has one such object today.
- **Side note:** run without the repo root on the import path, the check prints "FAIL C0 ... No module named 'lib.research'" and
  SERVED: NO. That is the caller's path, not the code.

### Z-W299-S1 (2026-10-07T16:34Z, UNDER_INVESTIGATION, hazard_standing INERT, disarm_owner 2.0.0_SA_COO~Z)
- **one_line:** AC3 of bb-14 read 95 other files and a different stamp than the 94 and stamp the check was cut with.
- **Sibling files:** none names it. Note this row is INERT in the file, not ARMED.
- **Re-measured today:** `round78/checks/r78_bb14.py:84-95` carries AMENDMENT 1: AC3 now grades the cell's own commits (the two
  files and no other) instead of the whole-folder stamp. Commit `9152a98bc5`. Ran `--crit AC3 --where local`: C1 PASS (2 paths),
  C2 PASS (0 other paths), SERVED: YES. `git ls-files integrations/bloomberg`: 97. The old STAMP constant is still at `:45` and
  is now read only by `--stamp`.
- **Verdict:** NEVER A HAZARD. A check's constant went stale when another project committed in the folder; it failed loudly and
  the product was untouched.

## NOT MEASURED

1. **Z-W31-S2, the device behaviour.** Whether `npx tsc -b` still resolves the decoy package in a fresh bun-only worktree was not
   run: `npx` may fetch from the registry, which this read was barred from. The shared tree's `portal/node_modules/.package-lock.json`
   exists, so the shared tree is not the case the row describes.
2. **Z-W2-S3 / Z-C-S3, the raw `grep -r` denial.** The hook and its switch are present; the denial was not exercised. A check
   script that walks the tree itself (not through comp-find) would not pass through the rail.
3. **Z-C-S2, five of the six fixed members.** Taken from `REMEDIATION_v15.md`'s evidence plus the four order statuses and one
   ancestry read; the amended criterion texts were not re-read line by line.
4. **Z-C-S35 and Z-C-S372 test counts.** The 15 passes are the two test files together; the per-file split was not printed.
5. **The eleven against the channel.** The investigation file holds 177 rows whose in-file `hazard_standing` is ARMED. This read
   covers the thirteen named rows only and says nothing about the other 164-plus.
