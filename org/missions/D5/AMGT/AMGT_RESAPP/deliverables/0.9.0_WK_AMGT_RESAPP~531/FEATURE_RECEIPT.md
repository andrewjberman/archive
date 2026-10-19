# FEATURE RECEIPT -- AMGT_RESAPP AMGT-cg-2 (round 125): the Security Analysis page prints reader words in plain words

Worker `0.9.0_WK_AMGT_RESAPP~531`, task order `AMGT_RESAPP.TO-AMGT-cg-2`, issuer `2.0.0_SA_COO~R1`.

## What the branch carries

- **Branch:** `cand/dell1/amgt-sa-reader-words` (nested portal worktree `C:/dev/wk-resapp-531/portal`), cut from PROD `facddeb6`.
- **Head commit:** `c8cd2da0ebbb3cb8b27c4b34d161118a2913083c` (LOCAL on the branch; not pushed; no DEV or PROD write).
- **Base:** `facddeb6` (PROD).
- **Changed paths (15, all under `src/pages/SecurityAnalysis/`):**
  - `src/pages/SecurityAnalysis/reasonWords.ts` (+13): `peerReadWords(status)`.
  - `src/pages/SecurityAnalysis/tabs/PeersTab.tsx` (read suffix and file comment).
  - `src/pages/SecurityAnalysis/components/PrintExportAction.tsx` (two sentences, no bracket).
  - `src/pages/SecurityAnalysis/refusalPresentation.ts` (`displayValue` refusal prints `Not available -- <reason>`; doc comment).
  - `src/pages/SecurityAnalysis/__harness__/readerWords.harness.cjs` (new, 9 checks).
  - `src/pages/SecurityAnalysis/__harness__/readerWordsPageCensus.json` (new, the census rows).
  - `src/pages/SecurityAnalysis/__harness__/richBA.old.md` and `richBA.new.md` (new; the old is the r123 export copy, the new differs on one line).
  - `src/pages/SecurityAnalysis/__harness__/richCases.old.md` and `richCases.new.md` (new; a Model Cases pair in each vintage).
  - `src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs` (vintage rule for the three line kinds; loader stubs brought to this vintage).
  - `src/pages/SecurityAnalysis/__harness__/peersReadFailed.harness.cjs`, `peersPattern.harness.cjs`, `join.harness.mjs`, `dateBypass.harness.cjs` (re-scoped pins, see `## Pins`).

## Census

Method. Native Grep over `portal/src/pages/SecurityAnalysis` for `ABSENT|REFUSED|READ_FAILED|SERVED|UNMAPPED|INVALID`, and over `*.ts`/`*.tsx` for `(read ` and the status interpolation shape. Denominator: 782 distinct hit lines (228 outside `__harness__`, 554 inside it). Each hit is classed by a line rule (comment marker, `data-*=` attribute, otherwise LOGIC); the VISIBLE set was read by hand against the page source. The classifier was a throwaway script, not committed.

| class | hit lines | meaning |
|---|---|---|
| VISIBLE | 10 | JSX text or a template that reaches the reader |
| ATTRIBUTE | 36 | a `data-*` attribute value |
| COMMENT | 91 | a comment line |
| LOGIC | 91 | comparisons, lookups, constant and type definitions, imports, identifiers containing a token (e.g. `NOT_SERVED_WORDS`) |
| HARNESS | 554 | any hit under `__harness__` (pins and fixtures) |

VISIBLE rows (12 rows: 10 hit lines plus 2 consumers of the `displayValue` helper, which prints the token without containing it):

| file:line | prints (before) | after | edited |
|---|---|---|---|
| `tabs/PeersTab.tsx:408` | ` (read READ_FAILED)` | ` (read failed)` | yes |
| `components/PrintExportAction.tsx:135` | `[REFUSED: <richError>]` | `The document could not be made: <richError>` | yes |
| `components/PrintExportAction.tsx:165` | `[REFUSED: <error ?? 'print render failed'>]` | `The pack could not be printed: <error ?? 'print render failed'>` | yes |
| `refusalPresentation.ts:42` | `[REFUSED: <reason>]` | `Not available -- <reason>` | yes |
| `components/ProvenanceLine.tsx:54` (via helper) | the helper's bracket token | the helper's new output | yes |
| `tabs/ModelTab.tsx:155` (via helper) | the helper's bracket token | the helper's new output | yes |
| `components/CheckFaceBadge.tsx:42` | `REFUSED` badge label | unchanged | no (a verdict label, not a sentence; surprise `AMGT_RESAPP-D1-W531-S2`) |
| `components/GenerationCaption.tsx:38` | `generation: none -- <status>` | unchanged | no (census P3, system-fact caption; put to the CTO) |
| `components/GenerationCaption.tsx:45` | `read <status>` | unchanged | no (census P3) |
| `components/InputProvenance.tsx:81` | ` -- <status>` | unchanged | no (census P4) |
| `postureCites.ts:343` | `... is <status, lowercased>` | unchanged | no (census P5, lowercase in a sentence) |
| `postureCites.ts:372` | `(model <status, lowercased>)` | unchanged | no (census P5) |

The machine-readable rows are in `readerWordsPageCensus.json`.

## Pins

Assertions that pinned today's words, each with its old and new form:

1. `peersReadFailed.harness.cjs:97` -- old `assert.ok(html.READ_FAILED.includes('(read READ_FAILED)'), ...)`; new `includes(' (read failed)')`.
2. `peersReadFailed.harness.cjs:98` -- old `!html.READ_FAILED.includes('(read ABSENT)')`; new `!includes(' (read absent)')`.
3. `peersPattern.harness.cjs:197` -- old `armHtml.READ_FAILED.includes('(read READ_FAILED)')`; new `includes(' (read failed)')`.
4. `peersPattern.harness.cjs:198` -- old `!armHtml.READ_FAILED.includes('(read ABSENT)')`; new `!includes(' (read absent)')`.
5. `join.harness.mjs:248` -- old `rendered.startsWith('[REFUSED:')`; new `rendered.startsWith('Not available -- ')`.
6. `dateBypass.harness.cjs:354` (`refusedOf`, the D8e site) -- old `/\[REFUSED: [^\]]*\]/g`; new `/Not available -- [^<]*/g`.

Not pins, checked and unchanged: `peersReadFailed.harness.cjs:102` (ABSENT never says READ_FAILED) and `:105` (UNRESOLVED has no `(read `); `peersCarry.harness.cjs` (no word pin); `modelPattern.harness.cjs:150` (computes its expected text through `displayValue`, no literal); `drafting.harness.cjs:261` and `thesisLadder.harness.cjs:302` (pin `>REFUSED</span>`, the CheckFaceBadge label, unchanged).

`exportCompare.harness.cjs`: no pin changed. Additions: the rich parser reads `Not available -- <reason>` for the y/y note, the estimate-years note and the Model Cases absent line (`notAvailableReaderLine`), and the case reader accepts a served case with no state word (`artifactCases`). Loader repair: the stub set was copied from `tabs.harness.cjs` (`@/ui/components/PageEnd`, `@/lib/dateUtils`, `@/ui/components/graphic/GraphicCard`, `@tanstack/react-query`, `@/api/api-client`, and the hook stubs `useModelVersions`, `useModelCompare`, `useInputLedger`, `useCollectedChatter`) because the harness aborted at load before reading any artifact. Its comment at about line 257 still names `[REFUSED: ...]` (a stale comment, left as is).

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

No other page is changed.

## Shared files

- none

## Not carried

Each path absent from this branch, with `git diff facddeb6 HEAD -- <path> | wc -l` = 0:

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174` (port 5174 only). The page is `/security-analysis`.
- Peers tab: pick a name whose peer read is not `SERVED`. A `READ_FAILED` read shows `... (read failed)` under the reason; an `ABSENT` read shows the designed empty state ("No peer set for this name yet.") with no suffix.
- Print and export buttons: the failed sentences show only on a failed request or render (`The document could not be made: ...`, `The pack could not be printed: ...`).
