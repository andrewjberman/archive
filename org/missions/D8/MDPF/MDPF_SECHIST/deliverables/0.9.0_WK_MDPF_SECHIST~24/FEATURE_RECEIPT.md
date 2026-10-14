# FEATURE RECEIPT -- cand/dell1/sechist-frontier-label (MDPF_SECHIST SH-t-25, FWD-9)

## What the branch carries

- Branch: `cand/dell1/sechist-frontier-label` (LOCAL in the nested portal worktree; not pushed)
- Head commit: `c77f23624df0a400273da28063813930d7e63afb` (c77f2362, LOCAL)
- Base: `6a5926fc11` (portal PROD)
- Changed paths (portal-root relative, `git diff --name-only 6a5926fc11 HEAD`):
  - `src/api/portal-proxy.ts`
  - `src/pages/Positioning/shared/etfAdapter.ts`
  - `src/pages/Positioning/tabs/HoldingsTab.tsx`
  - `src/pages/Positioning/tabs/ReturnsFrontier.tsx` (new)
  - `src/pages/Positioning/__harness__/frontierLabel.harness.cjs` (new)
  - `src/pages/Positioning/__harness__/frontierFixture.json` (new)
  - `src/pages/Positioning/__harness__/frontierNoCarry.golden.json` (new)

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Positioning | /positioning | client-facing | firm-gated (infra/logic/registry/firm_pages.json lists /positioning) |

## Shared files

- portal/src/api/portal-proxy.ts (types only: four optional fields)

## Not carried

- package.json: absent; `git diff 6a5926fc11 HEAD -- package.json | wc -l` = 0
- bun.lock: absent; `git diff 6a5926fc11 HEAD -- bun.lock | wc -l` = 0
- src/lib/firmAccess.ts: absent; `git diff 6a5926fc11 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- src/App.tsx: absent; `git diff 6a5926fc11 HEAD -- src/App.tsx | wc -l` = 0

## How to look

`cd portal && bun run dev:live --port 5174`, then the page `/positioning`, Performance view, books DIVZ and IDVZ. The label shows only against the NEW served keys (`returns_frontier`, `returns_frontier_holdings`); until the producer serves them, the fixture `frontierFixture.json` in `portal/src/pages/Positioning/__harness__/` is the way to see it.
