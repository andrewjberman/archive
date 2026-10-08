# Proposal: how a reviewed addition and a regeneration of requirements.txt stop overwriting each other

**Author:** `0.9.0_WK_NFRA_CTLPLN~13`, task order `NFRA_CTLPLN.TO-CT-e-1`, 2026-10-07. **For:** `1.0.0_SA_CTO`, who rules.
**Scope of my act:** I changed neither `requirements.txt` nor its generator. `git status --porcelain -- requirements.txt` read
empty after every run below.

## 1. What generates the file (measured)

- The file's own header names it: `org/tier1_exec/3.0.0_SA_CVO/deliverables/REQUIREMENTS_CENSUS/build_requirements.py`,
  fed by `import_census.py` in the same folder.
- `import_census.py <repo root> <out.json>` lists the git-tracked `.py` files, parses each with `ast`, collects third-party
  import names, and maps each to an installed distribution and version with `importlib.metadata` on the box it runs on.
  `build_requirements.py <census.json> <out file>` turns that JSON into the file. Both take the output path as an argument,
  so each has a scratch mode by construction; I used it and never let either touch the real file.
- The builder reads no existing `requirements.txt`. Its hand-curated inputs are constants inside the script (`TOOLS`,
  `UNPINNED`, `WINDOWS_ONLY`, `RULED_*`, `NOT_INSTALLED_NOTES`). Everything else comes from the census JSON.
- I found no scheduled or hooked caller: `git grep` for the script's name outside its own folder and the missions tree
  returns only the file's header, one brief and one Andrew-direct record. Whether a person runs it from a shell is UNREAD.

## 2. Does a regeneration reproduce the committed file today? (measured, all outputs under `.scratch/regen/`)

| Run | Inputs | Result |
|---|---|---|
| A | builder, the committed `import_census_20261007.json` | `cmp` reports no difference: the same 8,480 bytes, same sha256 |
| C | `import_census.py` over this worktree today (62,085 tracked files; 9,874 `.py`), then builder | the 67 active lines, their names and pins are the same; the line-4 count and the "N files" comments differ (9,765 to 9,874 tracked `.py`; boto3 1,853 to 1,870; pandas 953 to 974) |

So the builder is deterministic from a given census, and a fresh census changes only comment numbers while the package set is
unchanged. A regeneration at a later date produces a diff in many comment lines even when no package changed.

## 3. What happens to a line added by hand? (measured)

I copied `requirements.txt` to scratch, appended `frozendict==2.4.7  # hand-added, reviewed`, and ran the builder into a second
scratch file. The regenerated file is byte-identical to run A: **the hand-added line is gone** (`grep -c frozendict` = 0). The
builder writes the whole output from the census and never reads the old file, so any hand edit is lost on the next run with no
warning. This is the overwrite the CTO named, and it is why the header says "do not hand-edit".

## 4. Recommendation (five lines)

1. **A second, reviewed input file**, `org/devices/intake/approved_additions.txt` (one `name==version` per line, each with a
   trailing comment naming the CRO assessment and the CTO decision it rests on). A human edits only this file; its commit is the
   review record (C-INTAKE clause 7). The CTO owns it.
2. **The generator merges it, never reads the old output.** `build_requirements.py` gains one step: after its own sections it
   appends a `# --- 6. Reviewed additions ---` section from that file, and exits non-zero if a reviewed name is already generated
   with a different pin. `requirements.txt` stays generated, so its "do not hand-edit" header stays true. This is the one change
   to the CVO's script, for the CTO to rule on.
3. **The closure is a generated lock beside it, never hand-written.** `intake_closure.py closure` already writes
   `closure_cp314_win_amd64.json` (162 members at today's measure); the same tool can print it as `name==version` lines in a lock
   file. The checked route fetches from the lock, so a dependency can never be missed because someone forgot to list it.
4. **Order of operations:** regenerate `requirements.txt` (census plus reviewed file), then recompute the closure from it, then
   re-derive the fetch list. Each step is a script run to a stated output path; none is edited by hand.
5. **A reviewed addition's survival is testable:** run the builder on a scratch copy with one reviewed line and `grep` for it
   in the output; run it again with the line removed and expect it gone. (My run B is the negative arm, measured above.)

## 5. What this does not settle

- The pins in the generated file are the versions installed on the laptop. The closure inherits them: two specifier conflicts
  stand on `botocore` (see the closure file), because the laptop's own set is inconsistent.
- Whether a Python 3.14 file exists on the index for any name in the fetch list is UNREAD.
- A commit-time check that the committed file equals a regeneration is possible and is NOT proposed here: it would be an
  approval gate nobody asked for.
