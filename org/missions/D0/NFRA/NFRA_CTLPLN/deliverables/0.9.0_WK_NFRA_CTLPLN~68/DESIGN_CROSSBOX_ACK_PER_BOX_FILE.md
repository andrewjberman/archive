# DESIGN-CROSSBOX-ACK -- the crossbox ack in a per-recipient-box file

**Order:** NFRA_CTLPLN.TO-CT-w-6 (round 8, cell CT-w-6, outcome FWD-8, FWD-3) | **Issued to:** 0.9.0_WK_NFRA_CTLPLN~68 by 2.0.0_SA_COO~C
**Reader:** 1.0.0_SA_CTO (decides the design) | **Judgment grader:** 3.0.0_SA_CVO (CTw6-AC2, L9)
**Base read:** worktree `C:/Users/AndrewBerman/Desktop/ajb_wk/ctlpln-68`, branch `wk-NFRA_CTLPLN-68`, HEAD `2fbb74e87d` (LOCAL).
**Scope:** a design only. No tool, hook, lane, crossbox file or `portal` gitlink was changed. No writing `crossbox-call.py` verb was run.
Citations are `path:line` at `2fbb74e87d`. Counts were measured on 2026-10-12 about 08:30Z to 08:45Z.

## 0. Premises checked against live state

| # | Premise in the order | Live state | Row |
|---|---|---|---|
| P1 | Worktree carries `org/` and `.tools/` | TREE-OK; branch `wk-NFRA_CTLPLN-68` | none |
| P2 | "the recipient's ack, receive and close edits land in that SAME file" | FALSE for receive. `receive` (`.tools/crossbox-call.py:476-519`) writes only the inbox file (`:518`). It never saves the crossbox JSON. | NFRA_CTLPLN-W68-S1 |
| P3 | Lane `NFRA_CTLPLN_FAST_C` says which paths a manager may commit | FALSE. `NFRA_CTLPLN_FAST_C` admits only `1.0.0_SA_CTO` and `2.0.0_SA_COO~C` (`.owned-paths.yaml:702-706`). The manager lane for crossbox is `DEVICES_CROSSBOX` (`:822-827`, path `:2944-2947`). | NFRA_CTLPLN-W68-S2 |
| P4 | "box-sync.sh's two known conflict classes" | `merge-resolve-known.py` header says "two" (`:1`) but enumerates four classes (`:7`, `:20`, `:24`, `:30`). The crossbox fold is class 4. | NFRA_CTLPLN-W68-S4 |
| P5 | The one-writer check governs crossbox files | FALSE. `APPEND_ONLY` (`.tools/git-hooks/one-writer-check.py:29-33`) has no crossbox pattern. | NFRA_CTLPLN-W68-S3 |
| P6 | Census: 36 of 1,894 merges, 69 path rows, 61 `RESOLVED-OTHER` | Confirmed by recount of the census body: 36 `MERGE` lines, 69 `PATH` lines, 61 `RESOLVED-OTHER` (all 61 crossbox), 6 `CHANNEL-UNION`, 2 `GENERATED-REGEN`. Header says "two" INVESTIGATION files; the body names three. | NFRA_CTLPLN-W68-S5 |
| P7 | `box-sync.sh` lines 48 and 265 read only `refs/remotes/origin/box/*` | Confirmed (`.tools/box-sync.sh:48`, `:265`, both `for-each-ref ... refs/remotes/origin/box/`). | none |

Also found (not a premise, a test gap): the crossbox selftest's "merge-folds" case calls the tool's own fold (`crossbox-call.py:905-906`, `:917`), not `git merge`. A real `git merge` of the same two copies conflicts (section 5, measured). NFRA_CTLPLN-W68-S6.

## 1. Who writes which field today

**Denominator: 13 verbs and 24 keys.** The verbs are the 13 subcommands of `crossbox-call.py` (docstring `:15-27`). Seven write the JSON directly (`open` `:265`, `sent` `:444`, `ack` `:558`, `acked` `:571`, `close` `:591`, `withdraw` `:607`, `merge` `:678`). Two write it through another verb (`issue` `:331` calls `open`; `send-pending` `:382` calls `sent` at `:438`). Four are read-only (`line` `:307`, `status` `:653`, `list` `:660`, `receive` `:476`, which writes only the inbox file at `:518`). The 24 keys are the 15 top-level keys (`KEYS`, `:61-62`) plus the 9 sub-keys of `sent` (2), `ack` (3) and `closed` (4) (`:63-65`).

Every save goes through `dump()` (`:200-203`), which recomputes `state` from the fields (`derive_state`, `:194-197`). So every writing verb rewrites `state`.

| field (key) | written by | verb (line) | example commit (history of the file) |
|---|---|---|---|
| schema, id, kind, call_id, from_device, to_device, from_serial, to_serial, subject, body_path, opened_at | sender box | `open` (`:292-296`, saved `:300`) | `9cb2a08f60` (COO~C creates `cb95`) |
| state | every writer (`dump`, `:201`) | all 7 direct writers | every commit above |
| sent.at, sent.bus_message_id | sender box | `sent` (`:451-452`), via `send-pending` (`:438`) | `2d870050d4` (MSTR records SENT on `cb95`) |
| ack.at, ack.by | **recipient** box | `ack` (`:565-566`, needs `to_device`, `:560`) | `8e872dbd49` (CT1 on dell1: "ack + close the TO half", `9ec5`) |
| ack.at, ack.by | **sender** box, when its copy has no ack | `acked` fallback (`:582`, saved `:587`) | `ae2e8d63bb` (MSTR on laptop: "record ACK on XB-9ec5", bus `41971e7f`) |
| ack.bus_message_id | sender box (the reply line's bus id) | `acked` (`:585`) | `bbb4e666f5` (MSTR on laptop: "record the ACK", `6c76`) |
| closed.from_at, closed.from_by | sender box | `close --side from` (`:602-603`, `need_box` `:595`) | `78cea2485b` (COO~C closes the from side, `9ec5`) |
| closed.to_at, closed.to_by | recipient box | `close --side to` (`:602-603`) | `8e872dbd49` (CT1, `9ec5`) |
| closed.to_at, closed.to_by | **sender** box, on a withdrawn ORDER | `withdraw` (`:630`, writes both sides) | `8a9e46efc5` (CTO, `a28e`, withdrawn 2026-10-11T06:55:38Z) |
| sent, ack, closed (all 9 sub-keys) | **any box that merges** the other copy | `merge` (`:692-705`, folds every sub-key) | `6245210c2f` (MSTR~DELL2: "dell2 sent/ack fields folded with CLOUD's closes", `c442`) |

**Fields with two writing boxes in the live tool:** `state` (all 7 writers), `ack.at` and `ack.by` (`:565` versus `:582`), `closed.to_at` and `closed.to_by` (`:602` versus `:630`), and, through `merge` (`:692-705`), all 9 sub-keys of `sent`, `ack` and `closed`. The commit `ae2e8d63bb` and the commit `8e872dbd49` both wrote `ack.at`/`ack.by` for the same ack of `9ec5`, one on each box. That is the census's conflict class.

**Conflict mechanism (measured in a raw-git simulation, section 5):** the single JSON is written with `indent=1` (`:203`). The `"ack"` line and the `"closed"` block sit on adjacent lines, so two boxes' edits fall in one hunk and git reports a conflict. The ordinary order conflicts too: the recipient's close and the sender's reply id and close sit on adjacent lines.

## 2. The proposed split

**Sender file** (writer: the `from_device` box only): `org/devices/crossbox/XB-<id>.json`, schema `crossbox/2`.
Keys: `schema`, `id`, `kind`, `call_id`, `from_device`, `to_device`, `from_serial`, `to_serial`, `subject`, `body_path`, `opened_at`, `sent` {`at`, `bus_message_id`}, `reply` null or {`bus_message_id`, `read_at`, `read_by`} (written by the sender's `acked`, copied from the reply line), `closed` null or {`at`, `by`} (sender's `close --side from`), `withdrawn` null or {`at`, `by`, `ruling`} (sender's `withdraw`, ORDER only, no recipient write).
`state` is no longer stored. A sender cannot store a value that depends on the recipient's file without reading it.

**Recipient file** (writer: the `to_device` box only): `org/devices/crossbox/ack/<to_device>/XB-<id>.json`, schema `crossbox/2-ack`.
Keys: `schema`, `id`, `to_device`, `to_serial`, `ack` null or {`at`, `by`} (`ack` verb), `closed` null or {`at`, `by`} (`close --side to`), and `delivered` null or {`at`} only if Q3 is approved.

**Why this path.** `<to_device>` is the canonical register name (`org/devices/DEVICES.json`: `laptop`, `sitez` with alias `Z`, `dell1`, `dell2`), so one path segment names one writing box. Top-level `glob("*.json")` readers keep seeing calls only (`crossbox-call.py:405`, `:662`; `crossbox-matrix.py:99`; `open-calls.py:923`; `crossbox-deploy-check.py:156`). The existing lane glob `org/devices/crossbox/**` (`.owned-paths.yaml:2944`) already covers the path. Rejected alternative: a per-box suffix `XB-<id>.<box>.json` in the same folder. It reuses the one-writer suffix logic, but every top-level reader would list ack files as calls, and the GS-f-4 regex (`owned-paths-validate.py:290`) would match them.

**Derived states (readers compute, from A = sender file and R = recipient file, null when absent in this tree):**

| state | rule (A, R) | today's equivalent |
|---|---|---|
| OPEN | A.sent.at null | `state` OPEN, `sent` null |
| SENT (status text only) | A.sent.at set, not ACKED | `status_of` `:649` "SENT, NOT ACKED" (today inside state OPEN) |
| ACKED | A.reply set, or R.ack set | state ACKED; matrix `ack=set`; `ack.bus_message_id` = A.reply.bus_message_id |
| HALF-CLOSED (status text only) | exactly one of A.closed, R.closed set | `status_of` `:643` (today inside whichever base state applies: ACKED when an ack exists, OPEN when it does not (the base state comes from the ack first)) |
| CLOSED-BOTH | A.closed and R.closed both set | state CLOSED-BOTH (`derive_state` `:195`) |
| CLOSED-BOTH, WITHDRAWN | A.withdrawn set (R absent) | `status_of` `:636` (today: from_by == to_by, no ack) |

The HALF-CLOSED wording correction is the CVO's note C-S31 (ADJUDICATION_v10); the derivation is unchanged, since `derive_state` still takes the base state from the ack first.

ACKED on A.reply keeps today's meaning: the sender's copy records the reply line, as `acked` (`:585`) does today. Withdrawn is derived from A alone, so the recipient's path is never written by the sender. DELIVERED is not in any file today. `receive` prints it (`:519`) and stores nothing, so it is not a git state (see S1, Q3).

**Who writes what in the split.** Sender box: `open`, `sent`, `acked` (reply only, no `ack.*`), `close --side from`, `withdraw`. Recipient box: `ack`, `close --side to`, and `delivered` if Q3. `merge` no longer folds: each copy holds disjoint paths, so `git merge` is clean and the verb is a read for v2 files only. The fallback at `:582` is removed: the sender never writes `ack.at` or `ack.by`.

## 3. Migration

- **Shape is fixed per call at open.** From the change on, `open` writes `crossbox/2`. A `crossbox/1` file is never rewritten. Its later verbs keep writing the single file exactly as today. Dispatch is on the sender file's `schema`.
- **Readers accept both shapes during the change.** `read()` (`:245-254`) branches on `schema`. The matrix `parse` (`crossbox-matrix.py:60-75`) accepts `crossbox/1` and `crossbox/2`, and joins `crossbox/2-ack` by id and by path segment.
- **In flight at the cut-over.** `list --open` measured 42 non-closed files of 140: 5 OPEN and 37 ACKED (`crossbox-call.py list --open`, rc 0). They finish on `crossbox/1`, and their conflicts recur until each closes. Q5 asks whether the CTO closes them by ruling instead.
- **Rollout order is mandatory:** (1) land the two-shape reader in all four boxes' trees; (2) only then let any writer emit `crossbox/2`. A `crossbox/1`-only reader meets `crossbox/2` and refuses (`check_call` `:164-165`: schema must be `crossbox/1`). That is loud, but it stops the box-sync cycle.
- **Two readers fail differently and must change in step 1.** `open-calls.py crossbox_closed_both` (`:920-945`) reads `state`; a v2 sender has none, so the CTO-ruling close gate refuses every v2 call (fail-closed). `crossbox-deploy-check.py` (`:163-166`) reads `state` and treats a missing one as "not live" and skips it, so a live v2 call would be cleared silently. That is a fail-open and it blocks the writer step. The fix is the shared derivation in item 9 of section 4.
- **No existing file is rewritten.** The 140 files are untouched. Test T8 (section 5) asserts that every v1 file reads the same.

## 4. What must change (files and functions; no patch)

1. **`.tools/crossbox-call.py`**: `KEYS`/`SCHEMA` (`:59-65`) and `check_call` (`:154-191`) accept `crossbox/1`, `crossbox/2`, `crossbox/2-ack`. `derive_state` (`:194-197`) and `dump` (`:200-203`) derive from two files for v2 and write no `state`. `open` (`:265-305`) writes `crossbox/2`. `ack` (`:558-569`) writes the R file under `<to_device>`, not the single file. `acked` (`:571-588`) writes `reply` only and drops the fallback at `:582`. `close` (`:591-605`) writes A.closed or R.closed. `withdraw` (`:607-632`) writes `withdrawn` only. `status_of` (`:634-651`) and `status` (`:653-658`) read both files. `listing` (`:660-676`) lists sender files and joins R. `merge` (`:678-706`) becomes a read for v2. Unchanged in v2: `line` (`:307`), `issue` (`:331`), `send-pending` (`:382`), `receive` (`:476`), `need_in_tree` (`:524`, identity read from A). Nine verbs change.
2. **`.tools/crossbox-matrix.py`**: `read_sources` (`:78-103`) lists the ack subfolder with `ls-tree -r` (`:81`) but reads the working tree with `glob("*.json")` (`:99`), an asymmetry to remove. `parse` (`:60-75`) requires `state` and would list every ack file UNREADABLE today, so the matrix must learn the new shapes before any ack file lands. `union` (`:106-126`) and `build` (`:150-172`) key by id, join A and R, and rank derived states, not stored ones. `counts` (`:175-183`) and `render` (`:186-209`) keep their formulas. Selftest (`:249-322`) gains the equivalence case.
3. **`.owned-paths.yaml`**: `DEVICES_CROSSBOX` (`:822-827`) already admits `0.0.0_AB_MSTR` and the path glob (`:2944-2947`) covers `ack/**`, so the box managers need no new entry. Add a lane entry for `lib/crossbox.py` (new, item 9). Add a seat entry only if Q1 says the recipient seat commits its own ack.
4. **`.tools/owned-paths-validate.py`**: `_XBOX_RE` (`:290`) matches only `org/devices/crossbox/XB-*.json`, so an ack path gets no receiving-lane admission under GS-f-4 (clause at `:381-384`). Extend the clause: admit `org/devices/crossbox/ack/<seg>/XB-*.json` when the agent equals the `to_serial` read from the sender file `XB-<id>.json` and `<seg>` equals that record's `to_device`. `_xbox_to_serial` (`:293-315`) reads the path's own file, so it needs the id-mapped sender path.
5. **`.tools/merge-resolve-known.py`**: `CROSSBOX_RE` (`:58`) and `fold_crossbox` (`:344-383`) stay for `crossbox/1` only. `fold_crossbox` must refuse any non-`crossbox/1` record, so a v2 record is never folded by v1 rules. A v2 conflict then falls to the default "not a known multi-writer class" (`:520`) and HOLDS. Those v2 paths should never conflict.
6. **`.tools/box-sync.sh`**: no code change. Lines 48 and 265 stay as they are; `resolve_known` (`:190-214`) delegates to item 5. Re-test only.
7. **`.tools/git-hooks/one-writer-check.py`**: `APPEND_ONLY` (`:29-33`) has no crossbox rule, and `decide` (`:53-66`) takes a path only. Add: `org/devices/crossbox/ack/<seg>/XB-*.json` is OK only when `<seg>` resolves through `lib/devices.py` to this box. A sender `XB-*.json` is OK only when its `from_device` is this box, which needs the staged content, so `decide` gains a content argument. A merge commit stays exempt (`:93-95`).
8. **`.tools/open-calls.py`**: `crossbox_closed_both` (`:920-945`) globs top-level files and reads `state`. It must derive from A and R through item 9, or the CTO-ruling close refuses every v2 call.
9. **`.tools/crossbox-deploy-check.py`**: OPEN-CALL (`:156-166`) reads `state` and skips a file with none. It must derive from A and R, or it fails open on v2 calls.
10. **`lib/crossbox.py` (NEW)**: the one derivation and join reader, used by items 1, 2, 8 and 9, following the `lib/devices.py` pattern. Needs a lane entry (item 3).

**Files to change: 9** (items 1 to 4 and 7 to 10: crossbox-call, crossbox-matrix, owned-paths.yaml, owned-paths-validate, merge-resolve-known, one-writer-check, open-calls, crossbox-deploy-check, lib/crossbox.py). `box-sync.sh` is 0 lines.
Test files, counted apart and not read by this worker, named by grep for crossbox use: `.tools/tests/test_crossbox_call.py`, `test_crossbox_deliver.py`, `test_open_calls.py`, `test_apply_who_and_crossbox.py`.

## 5. The test plan

| # | Case | Old shape (today) | New shape | Measured or planned |
|---|---|---|---|---|
| T1 | Two boxes, two temp repos plus origin, each commits its own side, one `git merge` | conflict, rc 1, `XB-SIM-0001.json` | rc 0, zero conflicts | **MEASURED** in raw git (`.scratch/xb_sim.py`, scratch only): V1 rc 1 conflicted `['org/devices/crossbox/XB-SIM-0001.json']`; V2 rc 0 conflicted `[]` |
| T1b | Ordinary order: ack merged, then the sender records the reply id and closes, the recipient closes | conflict, rc 1 | (split) | **MEASURED** V1b rc 1 conflicted the same file |
| T2 | Same sequence through the real verbs (`open`, `sent`, `ack`, `acked`, `close` from and to), then `git merge`, both sides read CLOSED-BOTH | fails (conflict) | passes | planned: the selftest harness, plus a `git merge` case |
| T3 | `receive` leaves the sender file byte-identical (sha before and after) | passes | passes | planned; pins P2 |
| T4 | `acked` with no recipient file writes no `ack.*` into the sender file | fails (`:582` writes an ack block) | passes | planned |
| T5 | `withdraw` changes no byte the recipient writes | fails (`:630` writes `closed.to_*` into the shared file) | passes | planned |
| T6 | Box dell1 commits `ack/dell2/XB-*.json` | no rule: passes silently | BLOCK (one-writer) | planned, new only |
| T7 | Lane: `0.0.0_AB_MSTR~DELL1` commits `ack/dell1/...` (admit) and `ack/dell2/...` (refuse) | no such path | admit and refuse | planned, new only |
| T8 | Equivalence: each of the 140 v1 files projected to a v2 pair (test-only converter); derived state, ack flag, ack bus id and status text equal the v1 file's `state` and today's `status_of` text | trivially equal | must equal | planned |
| T9 | Matrix: the live matrix (measured 12 pairs, with_file 12, acked 9, closed_both 5, none 0) is the same line when read from v1 files and from the v2 projection | state read as stored | derived | live baseline **MEASURED** `crossbox-matrix.py` rc 0 |
| T10 | One v1 and one v2 call on the same pair: newest by `opened_at` wins; counts unchanged | n/a | passes | planned |
| T11 | A `crossbox/1`-only reader meets a `crossbox/2` file | n/a | refuses, names the schema | planned; pins the rollout order |
| T12 | `open-calls` CTO close gate: v2 CLOSED-BOTH accepted; v2 half-closed refused | accepts v1 only | both | planned |
| T13 | `crossbox-deploy-check`: a live v2 ACKED call is flagged, not cleared | flagged (v1) | flagged | planned; a reader ignoring R is the mutant (fail-open) |
| T14 | Regression: the existing crossbox selftest (28 cases) and matrix selftest (7 cases) pass | passes: `CROSSBOX-SELFTEST cases=28/28 ok=True` (**MEASURED**, rc 0); `CROSSBOX-MATRIX-SELFTEST cases=7/7 ok=True` (**MEASURED**, rc 0) | unchanged | planned |
| T15 | The selftest's "merge-folds" case exercises `git merge` | no (`:905-906`, `:917`) | must | planned; S6 |

## 6. What the design does NOT fix

- **Surprise-channel INVESTIGATION files** are append-only shared files. The census shows 6 `CHANNEL-UNION` rows in 6 merges across **3** distinct files: `AMGT_HARVST` x3, `ADVI_FIRMBKTS` x2, `MDPF_DEMQUE` x1. Class 1 of `merge-resolve-known.py` (a section union, `:7-19`) already handles them. That is a different fix, outside this design.
- **Generated index rows:** 2 `GENERATED-REGEN` rows in 2 merges (`org/projects/ADVI_BILLING.json`, `org/projects/NFRA_OPSWKF.json`). Class 2. Not crossbox.
- **In-flight `crossbox/1` calls:** 42 non-closed files (5 OPEN, 37 ACKED) keep the single-file shape. Their conflicts recur until each closes (Q5).
- **Census scale:** 36 of 1,894 integrator merges conflicted (1.9%). 28 of those 36 (77.8%) touch a crossbox file, so 28 of 1,894 (1.5%) is the ceiling of what the split can remove. All 61 crossbox rows are `RESOLVED-OTHER`; the census does not say which resolver path landed each one.
- **The DELIVERED state** is not in git today and stays out unless Q3 is approved.
- **The write-authority gap:** `DEVICES_CROSSBOX` admits `0.0.0_AB_MSTR` for every box lane, so any box manager can commit any box's crossbox path until the item 7 rule lands.
- **The matrix BLIND arm:** a bus message with no file stays invisible to the matrix (`crossbox-matrix.py:18-19`), as it is today.

## 7. Open questions for the CTO

- **Q1.** May the recipient SEAT (for example `0.7.0_AE_CloudOps~CT1`, which wrote `8e872dbd49` under GS-f-4) commit its own ack file, or only its box manager? The answer sets item 3 and item 4.
- **Q2.** Is withdraw a sender-only `withdrawn` marker (no recipient write, section 2) approved?
- **Q3.** Should `receive` record DELIVERED in the recipient's file (one extra recipient commit per call), or should DELIVERED stay printed only?
- **Q4.** Is `state` dropped from `crossbox/2` and derived everywhere through `lib/crossbox.py` (item 9), or is a sender-side cache kept?
- **Q5.** Do the 42 in-flight `crossbox/1` calls finish on v1, or are they closed by a CTO ruling now?

DESIGN-CROSSBOX-ACK fields=24 verbs=13 files_to_change=9 questions=5
