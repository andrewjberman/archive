# FEATURE RECEIPT -- AMGT-gr-7 (About this data reads the AI-fill input it renders)

## What the branch carries

- Branch: `cand/dell1/aifill-provenance` (portal repository, nested worktree `C:/dev/wk-resapp-456/portal`)
- Head: `31337460fcf771e46ab239429446b2e857041caf` (LOCAL, not pushed)
- Base: `7db035e448d9e6bbc202ef4264989f54d3d3dded` (PROD release, `merge feature cand/dell1/aifill-blocks-prod into release/20261014T034603Z`)
- Paths:
  - `src/pages/SecurityAnalysis/components/InputProvenance.tsx`
  - `src/pages/SecurityAnalysis/SecurityAnalysis.tsx`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent from the branch; `git diff 7db035e4 HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent from the branch; `git diff 7db035e4 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent from the branch; `git diff 7db035e4 HEAD -- src/lib/firmAccess.ts | wc -l` = 0

## How to look

1. `cd portal && bun run dev:live --port 5174`
2. Open `/security-analysis`, select a name, and open `About this data` under the tabs.
3. On a name whose AI fill is SERVED, the last row reads `AI-written blocks -- <date> -- <N> from a web search, <M> from Opal sources`.
