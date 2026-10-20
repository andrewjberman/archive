# FEATURE RECEIPT -- AMGT-ch-1 (round 126): the posture cite misses print plain words

Serial `0.9.0_WK_AMGT_RESAPP~532`, order `AMGT_RESAPP.TO-AMGT-ch-1.the-page-prints-plain-words-for-the-posture-cite-status`, issued by `2.0.0_SA_COO~R1`.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-status-words` (nested portal worktree `C:/dev/wk-resapp-532/portal`).
- Head commit: `ebd7b447` (LOCAL on the branch; not pushed; the product change is `1a6cfd48`, the census wording fix is `ebd7b447`). Push state: unread by this worker. Merge check: `postureCites.ts` is unchanged between base `facddeb6` and `origin/DEV` (f6f1fe5b), so the branch merges onto DEV without a conflict in that file.
- Base: `facddeb6` (PROD). The outer worktree branch `wk-AMGT_RESAPP-532` carries this receipt and the instance.
- Changed paths (`git diff --name-only facddeb6 HEAD`, all under `src/pages/SecurityAnalysis/`):
  - `src/pages/SecurityAnalysis/postureCites.ts` (modified: one import; the management-block miss; the model-block miss)
  - `src/pages/SecurityAnalysis/statusWords.ts` (new: `blockStateWords(status)`)
  - `src/pages/SecurityAnalysis/__harness__/statusWords.harness.cjs` (new: 23 checks)
  - `src/pages/SecurityAnalysis/__harness__/statusWordsPageCensus.json` (new: the census)
- Sparse set: the nested worktree is not sparse (`git sparse-checkout list` returned "not sparse"); no sparse change was made.
- `GenerationCaption.tsx` is not edited (CTO ruling: `generationCaptionText` reaches the page only through the `data-generation-detail` attribute).

## Census

Pattern (native Grep, glob `*.{ts,tsx}`, under `portal/src/pages/SecurityAnalysis`): `\.status|_status|ranking_status|point_status|management_status|model_status|toLowerCase\(\)|ABSENT|READ_FAILED|EMPTY|REFUSED|INVALID|UNMAPPED`. Denominator: 263 hits in 36 files. The whole folder (all types) is 1187 hits in 113 files; the 924 hits in the 77 harness and fixture files are class HARNESS by folder and are not classed line by line.

| class | count | what |
|---|---|---|
| VISIBLE, status-bearing, edited | 2 | `postureCites.ts:343` (management block), `postureCites.ts:372` (model block) |
| VISIBLE, status-bearing, deferred | 5 | `refusalPresentation.ts:42`, `components/PrintExportAction.tsx:135` and `:165` (the `[REFUSED: ...]` markers, changed under cg-2 on `origin/DEV`), `components/CheckFaceBadge.tsx:42` (REFUSED label, still on DEV), `tabs/PeersTab.tsx:408` (`(read <status>)`, changed under cg-2 on `origin/DEV`); rows S1, S2 and S5 |
| VISIBLE, not a status | 7 | `postureCites.ts:216`, `:232` (mnemonic and unit words); `tabs/ModelTab.tsx:338`, `:351`, `:352` (unit words); `components/AiFillBlock.tsx:178`, `:180` (fixed plain words) |
| ATTRIBUTE | 31 + 2 hand-added = 33 rows | `data-*` only; the raw value stays on the attribute (design law) |
| COMMENT | 78 | |
| LOGIC | 139 | includes the helper `reasonWords.ts:116-117`, which turns codes into words |
| HARNESS | 1 | `__rendercheck__/renderCheck.tsx:311` |
| check | 263 = 14 + 31 + 78 + 139 + 1 | |

Hand-added (not caught by the pattern, no `.status` or `_status` token): `components/GenerationCaption.tsx:45` (ATTRIBUTE, inside `generationCaptionText`) and `:104` (ATTRIBUTE, the consumer).

`generationCaptionText` consumers (all `edited: false`): `components/GenerationCaption.tsx:104` (call, ATTRIBUTE); `components/LeadPanel.tsx:117` imports only `generationCaptionWords` and `generationDetailWords`; `__harness__/leadPanelPattern.harness.cjs:217` (binding, no call); comments at `leadPanelPattern.harness.cjs:215` and `tabs.harness.cjs:585`.

The census file lists the rows with `file`, `line` (base PROD numbering), `class`, `prints`, `plain_after` and `edited`. After the edit `postureCites.ts` moves one line down because of the import.

## Pins

Search: native Grep over `portal/src/pages/SecurityAnalysis/__harness__` (96 entries) for `management block|\(the model|\(model |unrecorded|block is (read|absent|ABSENT|READ)|model is (read|absent)`.

- Pinned assertions of the old words in pre-existing harnesses: none. The only pre-existing hits are `changedListFixture.RIO_LN_Equity.json:16714` (a source string, "model block only") and `dateSites.fixture.json:29` (a site list). Neither pins a cite-miss sentence.
- Assertions near the cite-miss path, unchanged and still correct: `posture.harness.cjs:517` counts `Citation not resolved -- ` (the prefix this branch keeps); `posturePattern.harness.cjs:333-339` counts `data-cite-resolved` and the warning icon.
- Re-scope: none needed. The new pins are this branch's own `statusWords.harness.cjs` (T2 and T3 sentences) and its census.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

No other page changed.

## Shared files

- none

## Not carried

Each path absent from this branch, with `git diff facddeb6 HEAD -- <path> | wc -l` = 0:

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0
- `src/pages/SecurityAnalysis/reasonWords.ts`: 0 (cg-2's file; not edited here)

## Harness runs

Unchanged page (before any product edit; `node src/pages/SecurityAnalysis/__harness__/statusWords.harness.cjs`): `STATUS WORDS PAGE HARNESS: NO (7 of 23 checks)`, exit 1. Failing: T1 (8 checks; `statusWords.ts` absent), T2 READ_FAILED, T2 ABSENT, T2 no-raw-status (the old text printed `this name's management block is read_failed` and `... is absent`), T3 (3 checks; the old text printed `(model read_failed)` and `(model absent)`), T5 census edit claim (`blockStateWords(` absent from `postureCites.ts`), T6. Passing: T2 no-management-object (the old text `is not carried` is kept), T4 (3), T5 (3).

Base hit sentences, recorded from the unchanged `postureCites.ts` before any edit (T4 asserts them literally):

- F: `a figure the analysis built for this name calls rev: 12.5 mm`
- E: `the company's filing, p. 3: "Revenue rose."`
- O: `officer: Jane Doe, CEO, 4 year(s) in role`

After the edit: `STATUS WORDS PAGE HARNESS: YES (23 of 23 checks)`, exit 0. The rendered miss sentences read once from the PASS lines:

- `this name's management block could not be read`
- `this name's management block is not on file`
- `this name's management block is not carried`
- `... served thesis (the model could not be read)`
- `... served thesis (the model is not on file)`
- `... served thesis (the model is not recorded)`

The harness is a function-level instrument (transpiled `postureCites.ts` and `statusWords.ts`, called directly). It renders no HTML and no browser was used.

Commit-gate note: `.tools/commit-gate.sh` reported "checked 0 of 4 file(s)" for this frontend commit, so it is not evidence of validation. The validation is AC2 (typecheck and lint, below).

## Surprise rows

Filed to `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (appended as five fenced rows, S1 to S5; `disarm_owner` `2.0.0_SA_COO~R1` on each):

- `AMGT_RESAPP-D1-W532-S1`: the PROD Peers line `(read <status>)` is raw; left unedited (cg-2 already changed it on `origin/DEV`, line 410). class OBSERVATION, hazard ARMED on PROD until the next promote.
- `AMGT_RESAPP-D1-W532-S2`: the verdict word REFUSED: the PROD sites are changed on `origin/DEV` by cg-2 except the CheckFaceBadge label, which DEV still shows; the order's phrasing covers block states only. class OBSERVATION, hazard ARMED.
- `AMGT_RESAPP-D1-W532-S3`: the premise "cg-2 is now on DEV" was recorded as false. SUPERSEDED by S5: the reading used a stale local DEV ref. class OBSERVATION, hazard INERT.
- `AMGT_RESAPP-D1-W532-S4`: `org/surprise_channel/` is tracked at HEAD but absent from this worktree's disk. class OBSERVATION, hazard INERT.
- `AMGT_RESAPP-D1-W532-S5`: correction. After `git fetch origin DEV`, `c8cd2da0` IS in `origin/DEV` (f6f1fe5b), so the "now on DEV" premise holds; S3 and the "not on DEV" statements in S1 and S2 are wrong. class OBSERVATION, hazard INERT.

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174` (dev builds use port 5174 only).
- Open `/security-analysis`, pick a name whose posture cite misses (a management block that is READ_FAILED or ABSENT, or a model block with no figure the cite names), and open the Posture tab.
- Expected: the miss reads `... management block could not be read` / `... is not on file` / `... is not carried`, and `(the model could not be read)` / `(the model is not on file)` / `(the model is not recorded)`. No raw status word appears in the sentence.
- Not verified live: this worker did not run a browser or HTTP.
