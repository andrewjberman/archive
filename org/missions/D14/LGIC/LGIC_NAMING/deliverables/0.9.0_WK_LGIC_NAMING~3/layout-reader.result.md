# LGIC_NAMING.TO-LN-l-2-r2 -- the cross-bucket reader, in a clean-context seat -- result

**Worker:** `0.9.0_WK_LGIC_NAMING~3` | **Branch:** `wk-lgic-naming-2-3` | **Base:** `619dec559fe82915c6a2c325a0f9f718270b08d0` | **Cell:** `LN-l-2` (round 2)

**Act:** `python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/blind_seat.py run l2`, run ONCE from the
worktree root with a 600000 ms Bash bound. Printed line, verbatim:

```
SEAT: OK cell=l2 rows=7 session=07de665f-d708-416a-9f2c-7710b2e3380e base=619dec559f Q1='unknown' Q2='unknown'
rc=0
```

No ERROR occurred, so the seat was not run a second time. No seat file was written or edited by hand.

## What the seat wrote

- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n5-reader.tsv`: `# base 619dec559f...`, `# seat 07de665f-...`, then 7 rows.
  a1, a2, a4, a5 and a6 read `bucket,source,scope,tier,table,partition,object`, a3 reads `bucket,source,scope,tier,table,partition`, and a7 reads `DOES-NOT-FIT`.
  A wrong label is the outcome's evidence, not a defect. This worker grades no label.
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/seats/l2.{seat.json,prompt.txt,raw.json,answer.txt,canary.txt}`.
  `l2.canary.txt` reads `Q1: unknown` / `Q2: unknown`.
- Seat record (`l2.seat.json`):
  - folder: `C:/Users/AndrewBerman/AppData/Local/Temp/opal_blindseat_l2_85bk6voz`, outside the workspace and in no git repository;
  - folder state: 0 files before and after, and `claude_md_in_parent_chain: []`;
  - invocation: argv `claude.EXE -p --tools "" --output-format json`, rc 0, `is_error false`, `num_turns 1`, prompt 4054 bytes;
  - `models: ["claude-haiku-4-5-20251001", "claude-opus-5[1m]"]` is recorded as the session reported it, with no verdict.

## Acceptance (verbatim outputs)

| id | invocation | deciding output | verdict |
|---|---|---|---|
| L2R-AC1 | `cd <WS> && timeout 120 python .../fixed_inputs/r2/check_ln_r2.py l2-seat` | `SEAT CONDITIONS: 10  HELD: 10  NOT HELD: []` / `VERDICT: PASS-CLEAN-SEAT` rc=0 | PASS-by-output, 10 of 10 |
| L2R-AC2 | `cd <WS> && timeout 120 python .../fixed_inputs/r2/check_ln_r2.py l2-canary` | `CANARY ANSWERS: 2 of 2  WORKSPACE-ONLY FACTS IN THE REPLY: 0 of 2` / `VERDICT: PASS-CANARY-BLIND` rc=0 | PASS-by-output, 2 of 2 |
| L2R-AC3 | `cd <WS> && timeout 120 python .../fixed_inputs/r2/check_ln_r2.py l2-labeled` | `ADDRESSES: 7  LABELED: 7  MISSING: []` / `VERDICT: PASS-ALL-LABELED` rc=0 | PASS-by-output, 7 of 7 |

`<WS>` = `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-3`.

**Controls:**
- **Determinism:** every criterion was run twice on unchanged files, with identical deciding lines both times.
- **No file mutant:** the order forbids hand edits to the prompt, reply and answer file.
- **In-memory mutant:** the checker's `:133-136` comparisons were re-typed and run on the files as written (all True), then on in-memory CRLF renderings of `l2.prompt.txt` and `l2.answer.txt` (all False). The files were not touched.

## Surprise

`LGIC_NAMING-W3-S4` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~G`): the seat files are LF with no `eol` attribute on a
`core.autocrlf=true` box. `check_ln_r2.py` reads the prompt and reply with `exact=True` and hashes them. So a checkout other than this worktree renders them CRLF, and `l2-seat` and `l2-canary` would re-grade FAIL there on a clean seat.

## Proof

`LGIC_NAMING.TO-LN-l-2-r2.layout-reader.proof_of_spec.json` beside this file, validated with
`python .tools/proof-of-spec-check.py <instance> L2R-AC1,L2R-AC2,L2R-AC3` before the `complete` flip.
