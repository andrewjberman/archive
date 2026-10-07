# Row Z-W28-S24 -- did the 16:55Z `bun install` of the r27 deploy fetch from the registry?

By: `2.0.0_SA_COO~O`, 2026-10-07 17:38Z. For `1.0.0_SA_CTO~Z` msg 31228. Read-only; nothing fetched, nothing run through
bun, no file changed.

## Verdict: CACHE-ONLY for package content. A metadata request is not ruled out by this instrument.

## What ran

`infra/aws/ec2/opal-gateway/deploy-to-ec2.sh:206`: `( cd "$MCPORTAL_DIR" && bun install --frozen-lockfile && bun run build )`.
Lines 39-62: on one branch the script builds in a fresh detached mcportal worktree under a temp directory and removes it
on exit. Which branch the 16:55Z run took, and whether its build directory already held `node_modules`, was not read. The deploy output (`deliverables/0.9.0_WK_NFRA_OPLGTW~28/r27_phaseB_deploy.out`
lines 265-279) reads `bun install v1.3.14`, ten top-level names and `77 packages installed [11.65s]`. It prints no
"downloaded" or "resolved" count.

## The read that decides it: bun's install cache on this box, at 17:38Z (13:38 local, UTC-4)

Directory `%USERPROFILE%/.bun/install/cache`; `BUN_INSTALL_CACHE_DIR` is unset, so this is the cache bun used.

| read | result |
|---|---|
| entries, top level (denominator) | 948 |
| entries to depth 2 (denominator) | 6,441 |
| created 16:50Z-17:00Z today | 0 |
| modified 16:50Z-17:00Z today | 0 |
| created at any time today | 0 |
| modified at any time today | 0 |
| newest entry in the whole cache | created 2026-10-06 15:55 local |
| the deploy's named versions already in the cache | 7 of 7 checked: `vite@7.3.6`, `react@19.3.0`, `react-dom@19.3.0`, `react-router-dom@7.18.4`, `@types/node@24.13.6`, `@vitejs/plugin-react@5.2.0` created 2026-09-24; `typescript@5.9.3` created 2026-08-06 |

A package fetched from the registry is written into this cache before it is linked. Nothing was written to it today, on
either timestamp, so no package tarball was fetched by the 16:55Z install, by r26's 14:02Z install, or by anything else
on this box today. The 77 packages were linked from entries cached on or before 2026-10-06.

## Limits

- **Network was not observed.** A cache read cannot show a request that wrote nothing. With `--frozen-lockfile` and every
  package cached, bun should need no registry request, but that is its documented behaviour as this seat knows it, not
  a measurement. Hence "a metadata request is not ruled out".
- **Seven names were checked by name, not 77.** The cache-wide zero covers the other 70.
- **The hazard stands.** The line fetches whenever the lockfile names a version the cache lacks: the first deploy after
  an mcportal dependency change, or any deploy from a box with an empty cache. The newest cache entries (2026-10-06
  15:52-15:55 local) were written by something yesterday; that was not this project's deploy window and is not traced
  here.

## What would close the row

A deploy that cannot fetch: the dashboard bundle built on the box allowed to fetch and shipped as an artifact, or the
install run offline so a cache miss fails the deploy. Either is a change to `deploy-to-ec2.sh`; the choice is the
CTO's with NFRA_CTLPLN's download tiers.
