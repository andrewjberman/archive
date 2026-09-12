# SESSION LOG -- `IRPT_BCKEND.TO-IB-rt-10`, worker `0.9.0_WK_IRPT_BCKEND~4`

**Worktree** `/c/tmp/wk-irpt-2-4b` on branch `wk-irpt_bckend-2-4b`, cut from CLOUD at `a296eac0f4`.
**Cold start**, per the issuer amendment of 2026-09-11 ~22:5xZ: no prior context, no WIP hand-off, and none
was hunted for. Everything below was built from the task-order face, the PRD row it quotes, the CTO's
round-1 ruling and the decomposition cell.

## 1. FIRST ACTS

```
$ git rev-parse --abbrev-ref HEAD
wk-irpt_bckend-2-4b
$ test -d org && test -d .tools && echo TREE-OK
TREE-OK
```

Session serial written to `org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial` before any other act.
No `safe-apply` was run in this cell (the order carries no deploy), but the file was written anyway because
the amendment says to write it before you need it.

## 2. RE-GROUNDING THE PREMISES AGAINST LIVE STATE

Every premise the face states was checked before any code was written. What was found:

| premise | state |
|---|---|
| `ycharts/extract/{extract.py,certify.py}` exist from round 1 | PRESENT, 685 + 294 lines |
| the three retained vendor PDFs are readable from Opal's own S3 | FETCHED and hash-verified, 3 of 3, into `.scratch/vendor_pdf/` |
| pages 23 / 31 / 35 | CONFIRMED, and 23+31+35 = the face's 89 |
| the codes are 45 / 45 / 46 | CONFIRMED |
| `Comparison undated 34 of 81, Multi 51 of 108` | REPRODUCED exactly, by re-deriving round 1's rule over this run's rows |
| `_contracts/AnalysisReport.schema.json` and the v1 artifact | BOTH present; **not byte-equal to each other, by design** -- the published copy carries its own `$id` and a `contract_version` const |

The vendor read is an **Opal S3 read, never a vendor call** (bound 1): `s3api get-object` against
`opal-data-ycharts`, verified against `pdf_validation.json` before use.

## 3. WHAT WAS BUILT, AND THE DECISIONS INSIDE IT

### 3.1 `fonts.py` -- and the bug in its own first version

The module asks each document's OWN resources in order (ToUnicode CMap, Encoding/Differences, the embedded
font program's `cmap` and `post` tables) and records the exhaustion when none answers.

**The first version resolved a code through whichever of the document's fonts mapped it. That was wrong and
the measurement is what caught it:** in the overview specimen, code 45 belongs to
`QXFAAA+RobotoCondensed-Regular` and is mapped by `QHGAAA+RobotoCondensed-Bold` to the digit `8`. A
document-scoped resolver would have returned a confident wrong digit. The unit is the FONT RESOURCE, and
`cross_font_control` now prints what the relaxed rule would have said (U+0038 / U+004D / U+0044 across the
three documents) as a standing negative control.

### 3.2 The date rule, and the round-1 defect it replaces

`date_claim` is SECTION / REPORT / NONE, decided per LOCATED VALUE rather than per page. Round 1 took the
page's first `Data as of` line and, failing that, the field census's date -- another document's statement.
Measured on the overview specimen: **15 of 61 rows sit on a page printing two different dates** (page 2:
2026-09-09 and 2026-09-11; page 6: 2026-08-31 and 2026-09-11). Filed as channel row `IRPT_BCKEND-W4-S28`.

### 3.3 Certification's fourth leg

L4 re-reads the date out of the document at the coordinates the row's provenance names, and refuses on two
distinct verdicts with two distinct remedies -- `DATE_NOT_STATED_AT_PROVENANCE` (wrong date) and
`DATE_TAKEN_FROM_A_NEIGHBOURING_BLOCK` (right date, wrong block). Two mutants exercise the two.

### 3.4 Three defects found in this cell's own work, by measurement

| what | how it was caught | what changed |
|---|---|---|
| `extra_attrs=["fontname"]` on `extract_words` silently RE-SEGMENTS the page and cost **3 of 61** located rows | the vendor row count dropped from 61 to 58 | the font scope is recovered from `page.chars` instead; word segmentation is byte-for-byte round 1's |
| a 2pt VERTICAL pad on a date-line crop pulled in the line above and pdfplumber interleaved them into `PSereppteamrebde fro 1r 1S,y 2n0th2e6t` -- **5 correct rows failed** | the first full certification run | no vertical padding on a date crop; horizontal slack only |
| the fixture PDF was pure ASCII, so **git detected it as TEXT** and an autocrlf checkout would have moved every byte after line 1 and invalidated its own xref offsets | the `safe-commit` warning `LF will be replaced by CRLF` | the generator now writes the standard PDF binary marker |

### 3.5 The unmapped-glyph fixture

A hand-built two-page PDF whose ToUnicode CMap has a deliberate hole. The withheld character is CHOSEN at
generation time as one the breaking value carries and the surviving value does not -- **the first attempt
withheld a character both values shared, which broke the positive control silently.** Every number comes
from the field census; the pair of fields is chosen by subtraction over the census's own rows, never named
from memory.

## 4. THE CONTRACT EDIT, AND THE CHECKER IT TRIPPED

`date_claim` was added to BOTH published copies of `AnalysisReport` as an OPTIONAL enum, written once and
inserted into both so byte-equality is a property of the edit rather than something checked afterwards.

**`battery_ib_s_18.py` arm (a) refused the first draft**: it treats every double-quoted span in a contract
property description as a claim to quote the PRD CONTRACTS section verbatim, and the description wrote the
PDF's own heading as `"Data as of:"`. It was the 1 of 386 quotes that did not resolve. The prose was
re-worded; **the checker was not touched.** After the fix: `TOTAL: 385 of 385 description quote(s) resolve
VERBATIM in the CONTRACTS section at 62301f71e0`.

That same battery then **crashes** in arm (c) on the path register's own data -- filed as
`IRPT_BCKEND-W4-S29`, not repaired here: it is `0.9.0_WK_IRPT_BCKEND~1`'s deliverable and outside this
order's paths.

## 5. TWO THINGS I HAD TO UNDO

- **A whole-file rewrite of `PATH_MANIFEST.json`.** `json.load` / `json.dump` produced a 6,579-insertion /
  6,518-deletion diff for a five-entry append. The register was restored to its HEAD bytes (via
  `git cat-file blob` and a write, **not** `git checkout --`, which this worker may not run), the restore was
  GRADED with `git diff --stat` until it read empty, and the append was redone TEXTUALLY: 67 insertions,
  1 deletion, with the parsed arrays compared before and after to prove no existing entry moved.
- **An LF write to the surprise channel**, which would have re-rendered ~1,900 CRLF lines as modified and
  guaranteed a conflict with every other seat appending to the same file. The appender now preserves the
  file's own line endings; the five rows land as a clean 218-line insertion across two commits.

## 6. BOUNDS OBSERVED

No vendor call. No monitor, alarm, SNS or SES. No deploy, no Terraform, no `safe-apply`, no change-management
ledger opened (the cell carries no deploy, and NEVER-2 forbids opening one without the room to close it).
No served output touched. No credential in any artifact. Nothing written outside the order's `<paths>` and
this deliverables folder. The spec was not widened and no neighbouring defect was repaired -- two were
found and both were filed as rows.

## 7. RUNS

| command | rc | result |
|---|---|---|
| `timeout 600 python .../battery_ib_rt_10.py` | 0 | `IBRT10-GLYPHS-DATES-PROVENANCED`, arms 4 of 4 |
| the same, a second time | 0 | byte-identical, 17,926 bytes, sha256 `292d854078120020` |
| `timeout 1200 python .../tests/run_offline_suite.py` | 0 | 6 specimens, all certified |
| `timeout 600 python .../battery_ib_s_18.py` (regression) | 1 | arm (a) 385 of 385; arm (c) crashes on pre-existing data (row W4-S29) |

## 8. THE STANDING PROOF GAP

Every specimen is real vendor output on SYNTHETIC HOLDINGS, or census-generated, or hand-built. **No
representative real-client PDF exists, none was manufactured, and nothing in this cell is a certification
against real client input** (FWD-4, FWD-8).
