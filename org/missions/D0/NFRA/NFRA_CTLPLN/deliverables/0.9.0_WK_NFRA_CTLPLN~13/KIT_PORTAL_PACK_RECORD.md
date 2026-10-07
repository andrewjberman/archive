# KIT_PORTAL_PACK_RECORD -- NFRA_CTLPLN.TO-CT-k-2 AMENDMENT 3

Worker `0.9.0_WK_NFRA_CTLPLN~13`, 2026-10-07 (install and pack ran 2026-10-07 ~10:55Z to 11:09Z, UTC). Branch `wk-NFRA_CTLPLN-13`.
No stop point fired. Nothing was sent anywhere; the pack is not committed.

## Where

- `<base>` = `C:/Users/AndrewBerman/Desktop/ajb_workspace` (first entry of `git worktree list --porcelain`)
- `<portal>` = `<base>/portal` (a nested git repo, branch DEV)

## BEFORE (step 1)

- Portal HEAD `481b3bcc5f22312bdc4c75768e4e50915e4bda56`, branch `DEV`.
- `bun.lock` SHA-256 `9be0dbee0ba1e6ff2a09f298f11ac66b4c38e4030427abadea5be7d4008dd2a4` (raw bytes; the tool's CRLF-folded form is `b32cb20e3d31...`)
- `package.json` SHA-256 `507a9901bc3400710a1647eb7c71747e6457c8f5fe325ea425282566f75bc867`
- `bun --version` 1.3.9; `node --version` v26.10.0
- `git -C <portal> status --porcelain`: 18 modified tracked files, all under
  `src/pages/InvestorReporting/contracts/wire/` (AnalysisReport, AnalysisRequest, AnalysisSubmissionRequest,
  AnalysisUploadResult, BoundaryRefusal, DirectoryContext, DirectoryEntry, DirectoryPage, NarrativePacket,
  OwnedAnalysisRequestHistory, PerformanceReport, PublicStatusEnvelope, RenderPackage, RequestComposition,
  ResolvedScope, SelectedAccounts, SelectionRequest, StatusEnvelope; another seat's work, untouched) plus 17
  untracked entries. Full listing kept in `.scratch/portal_status_before.txt` (worktree scratch).
- `describe` last line:
  `PORTAL-TREE head=481b3bcc5f22312bdc4c75768e4e50915e4bda56 lockfile=bun.lock lock_sha256=b32cb20e3d31 equals_dev=True bun=1.3.9 node=v26.10.0 packages=487 present=409 absent=6 files=41952 bytes=447989421 ok=False`

## READ 1 -- port 5174 (step 2): NOTHING LISTENING

- Python socket connect to 127.0.0.1:5174: `ConnectionRefusedError [WinError 10061] ... actively refused it`
- `netstat -ano | findstr ":5174"`: no output, filter rc=1 (control: `netstat -ano` itself returned 343 lines)

## Process read (step 3): NONE NAMES THE PORTAL

`Get-CimInstance Win32_Process` for `node`/`bun`: 16 processes, all `node.exe`, all `npx -y @playwright/mcp@0.0.75 --headless
--config .tools/playwright-mcp-config.json` launchers and their `.../npm-cache/_npx/.../@playwright/mcp/cli.js` children
(8 pairs). No command line names the portal directory; no bun process.

## The install (step 4)

`cd <portal> && timeout 600 bun install --frozen-lockfile`, run once. EXIT=0. Last lines:

```
$ node scripts/preinstall.js
Package manager check passed: Bun detected

+ xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz

7 packages installed [347.32s]
```

(The package's own `preinstall` script ran as part of the install command; it prints the Bun check. No "lockfile would change" message.)

## READ 2 -- AFTER (step 5): UNCHANGED

- `git status --porcelain` AFTER vs BEFORE: byte-identical (`diff` rc 0).
- `bun.lock` SHA-256 after: `9be0dbee0ba1e6ff2a09f298f11ac66b4c38e4030427abadea5be7d4008dd2a4` (same)
- `package.json` SHA-256 after: `507a9901bc3400710a1647eb7c71747e6457c8f5fe325ea425282566f75bc867` (same)
- Portal HEAD after: `481b3bcc5f22312bdc4c75768e4e50915e4bda56` (same)

## The six packages, version on disk before then after (lock pins the "after")

| package | before | after |
|---|---|---|
| @types/d3-array | 3.0.3 | 3.2.2 |
| @types/d3-interpolate | 3.0.1 | 3.0.4 |
| baseline-browser-mapping | 2.11.22 | 2.10.0 |
| caniuse-lite | 1.0.30001810 | 1.0.30001775 |
| d3-format | 1.4.5 | 3.1.0 |
| d3-time-format | 3.0.0 | 4.1.0 |

## describe AFTER (step 6)

`PORTAL-TREE head=481b3bcc5f22312bdc4c75768e4e50915e4bda56 lockfile=bun.lock lock_sha256=b32cb20e3d31 equals_dev=True bun=1.3.9 node=v26.10.0 packages=487 present=415 absent=0 files=41860 bytes=448802404 ok=True`

## The pack (step 7)

- Path: `C:/tmp/kit-portal-pack-20261007/` (outside every git tree; holds `portal_node_modules.tar.gz` and `MANIFEST.json`)
- Archive format: `tar+gzip-1` (gzip level 1)
- Archive SHA-256: `27c916158ef2f763844a3847049975848c16b9affc7f58ffadd91b1f22d54d21`
- Archive size: 100,052,760 bytes (about 95.4 MiB); unpacked 448,802,404 bytes
- File count: 41,860 files packed; links 0; unrepresented 0; platform-specific packages 5 (all win32/x64)
- Manifest: lockfile `bun.lock` folded-SHA `b32cb20e3d31d35fd6e4e0026585eca4a159e881f0ecebfa2a884340593ff4c6`, portal HEAD 481b3bcc..., bun 1.3.9, node v26.10.0, platform win32/x64
- `sha256sum` of the archive on disk matches the manifest.
- Self-check, `verify --from C:/tmp/kit-portal-pack-20261007 --portal <portal>` (no `--extract`):
  `PORTAL-VERIFY archive=ok lockfile=ok bun=ok node=ok platform=ok extracted=- ok=True`
- The portal's `git status` after the pack is still identical to BEFORE.
- Not sent, not committed. The typecheck was NOT run in the base checkout (step 8).

## What a Dell runs (after the pack arrives by Taildrop at `<dir>`; `<portal>` is its portal checkout at DEV with `bun.lock` equal to the laptop's)

The Dell must have bun 1.3.9 and node v26.10.0 (verify refuses otherwise), and Windows x64.

```
python org/devices/kit_portal_tree.py verify --from <dir> --portal <portal>
python org/devices/kit_portal_tree.py verify --from <dir> --portal <portal> --extract
python org/devices/kit_portal_tree.py typecheck --portal <portal>
```

(`--replace` is needed on the second line only if `<portal>/node_modules` already exists and is non-empty.) The portal's own
script, as `package.json` names it, is `typecheck`: `tsc -b --noEmit`. Each of these makes no network call and no install.
