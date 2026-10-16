# FEATURE RECEIPT -- AMGT-gx-1 (AI-written row wording)

## What the branch carries

- Branch: `cand/dell1/aifill-provenance-wording` (nested portal worktree `C:/dev/wk-resapp-486/portal`, not pushed)
- Head: `e0dcfa9fa45d3ade5f8dc2ef20b41b7b9444fbec` (LOCAL)
- Base: `fc174c6917a27daef4a5db577c97a0f899a9d056` (portal DEV, already carrying the AI-written row)
- The one path: `src/pages/SecurityAnalysis/components/InputProvenance.tsx`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent from the branch; `git diff fc174c69 HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent from the branch; `git diff fc174c69 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent from the branch; `git diff fc174c69 HEAD -- src/lib/firmAccess.ts | wc -l` = 0

## How to look

- `cd portal && bun run dev --port 5174`
- open `/security-analysis`
- open `About this data` under the tabs; the AI-written blocks row reads the web part as a search made when each block was written
