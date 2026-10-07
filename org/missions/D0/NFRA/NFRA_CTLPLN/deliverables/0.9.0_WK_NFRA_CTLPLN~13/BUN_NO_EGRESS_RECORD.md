# BUN_NO_EGRESS_RECORD -- NFRA_CTLPLN.TO-CT-k-2 AMENDMENT 5 (row NFRA_CTLPLN-S13)

Worker `0.9.0_WK_NFRA_CTLPLN~13`, 2026-10-07 (UTC ~12:35Z to 13:15Z), branch `wk-NFRA_CTLPLN-13`. bun on this machine: **1.3.9** (Windows x64).
Tools: `org/devices/kit_bun_no_egress.py` (measure, wrap, selfcheck), `org/devices/test_kit_bun_no_egress.py`,
`.tools/wk-provision.sh`, `.tools/tests/test_wk_provision_no_registry.py`. No `bun install`, `add`, `bunx`, `create` or `update` was run anywhere.

## The harness (what makes the test safe)

Every bun process the tool starts runs with TWO independent redirects to loopback:
A, the registry (`BUN_CONFIG_REGISTRY` / `NPM_CONFIG_REGISTRY` and a project `bunfig.toml` `registry =`, all pointing at a
Python stdlib listener on `127.0.0.1:<ephemeral>` that logs method + path and answers 404); B, the proxy (`HTTP_PROXY`,
`HTTPS_PROXY`, `http_proxy`, `https_proxy` at a second loopback listener that logs every request line, `CONNECT` included, and
answers 502; `NO_PROXY` / `no_proxy` empty). The probe imports `@opal-no-such-scope-<16 hex per run>/probe`. Each arm has its own
directory (outside every git tree; every ancestor checked for `node_modules`, `package.json`, `.git`, `bunfig.toml`), its own
`BUN_INSTALL_CACHE_DIR`, and its own `HOME`/`USERPROFILE`/`XDG_*`/`APPDATA`/`TEMP`, passed as an env dictionary to the child only.
The system temporary directory is REJECTED on this box (`C:\Users\AndrewBerman` holds a `node_modules` and a `package.json`), so
the tool falls back to `<drive root>\tmp`.

## ORDER OF PROOF, as run

| step | registry listener | proxy listener | rc |
|---|---|---|---|
| before any bun: Python-made requests to both listeners (CONNECT, absolute-URI GET, registry GET) | logged 1 | logged 2 | -- |
| 0 `bun --version`, both listeners up | 0 | 0 | 0 |
| 0b (ADDITION, row W13-S12) `bun run` of a script that fetches a LOOPBACK URL, proxy variables set | 0 | 1 (GET http://127.0.0.1:port/... answered 502; bun printed `fetch-status 502`) | 0 |
| 1 proxy proof: `bun --no-install run probe.js`, registry default | 0 | 0 | 1 (resolution error) |
| 2 positive, no disarm, all three forms of Redirect A + proxy | 0 | 6 (all naming `127.0.0.1:<port>`, none a public host) | 1 |
| 2 positive, form `BUN_CONFIG_REGISTRY` alone / `NPM_CONFIG_REGISTRY` alone / project `bunfig.toml` alone | 0 / 0 / 0 | 6 / 6 / 6 (all naming loopback) | 1 |

bun routes even the loopback registry through the proxy variable when `NO_PROXY` is empty, so the positive arm's requests are
counted on the proxy listener (a loopback listener), naming the loopback registry; the registry listener itself saw no request
in any arm. All three forms of Redirect A are effective on their own. `bun --version` made no request (step 0: 0 and 0).

## Every arm (this machine's bun 1.3.9; the candidates carry the effective redirects of step 2)

```
version                                    --version                        reg=0 prx=0 rc=0
proxy-honor-check                          run fetchcheck.js                reg=0 prx=1 rc=0
proxy-proof                                --no-install run probe.js        reg=0 prx=0 rc=1  (redirect B only)
positive-all-forms / positive-alone x3 / positive-final   run probe.js      reg=0 prx=6 rc=1  (each)
CANDIDATES
flag:--no-install                          --no-install run probe.js        reg=0 prx=0 rc=1  PASS
flag-after-subcommand:--no-install         run --no-install probe.js        reg=0 prx=0 rc=1  PASS
project-bunfig  ([install] auto="disable") run probe.js                     reg=0 prx=0 rc=1  PASS
user-bunfig     ([install] auto="disable") run probe.js                     reg=0 prx=6 rc=1  FAIL (same count as the positive arm)
env:BUN_CONFIG_SKIP_INSTALL_PACKAGES=1                                      reg=0 prx=6 rc=1  FAIL
env:BUN_FEATURE_FLAG_DISABLE_INSTALL_INDEX=1                                reg=0 prx=6 rc=1  FAIL
env:BUN_FEATURE_FLAG_DISABLE_REDIS_AUTO_PIPELINING=1                        reg=0 prx=6 rc=1  FAIL
env:BUN_FEATURE_FLAG_DISABLE_SQL_AUTO_PIPELINING=1                          reg=0 prx=6 rc=1  FAIL
structural (empty node_modules + package.json beside the probe)             reg=0 prx=0 rc=1  PASS
CONTROL (no network by construction)
control:user-bunfig-is-read-by-run  (malformed user file in HOME and XDG_CONFIG_HOME, --no-install)   reg=0 prx=0 rc=1
```

LAST line: `BUN-NO-EGRESS bun=1.3.9 positive_requests=6 candidates=9 passing=4 leaked_public=0 form=flag:--no-install ok=True`

A candidate passes only with zero requests on both listeners, no timeout, bun's output naming the probe package (so a flag-syntax error
is not a pass), and the same run's positive arm non-zero. Every arm's `cache_files` was 0. Environment variables searched: the
binary names 90 `BUN_*` strings, 13 of them `BUN_CONFIG_*` (list in the JSON); the four whose name reads as an install / auto
switch were tried (rows above). `bun --help` and `bun run --help` document `--no-install` ("Disable auto install in the Bun runtime"),
`--install=<val>` (auto, fallback, force) and `-i` (= `--install=fallback`); no documented setting disables it by environment.

## The passing form and how the wrapper applies it

Form carried: **`flag:--no-install`** (the command-line flag, placed before the subcommand). `wrap -- <bun args>` inserts it:
`wrap -- run x.js` runs `bun --no-install run x.js`. Preference order for the form when several pass: flag, flag-after-subcommand,
environment, project bunfig, user bunfig, structural. `wrap` refuses `install`, `i`, `add`, `a`, `x`, `bunx`, `create`, `c`, `update`,
`upgrade`, `outdated`, `audit`, `info`, `publish`, `remove`, `rm`, `pm view`, `pm info` (rc 2, a line naming link or none) unless
`--allow-registry <reason>` is given (printed loudly), and refuses an `--install` / `-i` flag. A bare info flag (`--version`, `--help`) is
run bare. The wrapper default is the form measured on this bun; a box with another bun runs `measure --out` and passes `wrap --from <json>`.

User-level setting on this version: it does **not** work, and the control shows why. A malformed user-level `.bunfig.toml` (in `HOME` and in
`XDG_CONFIG_HOME`) is never read by `bun run`: bun reported the probe's resolution error, not a config error. The valid file with
`auto = "disable"` made 6 requests, equal to the positive arm. Whether `bun install` / `bunx` read the user-level file was not measured.

## What stays unproven

- A request that bypassed BOTH listeners cannot be seen by this tool. It is bounded by: the proxy being proven honoured by this
  bun's HTTP client (step 0b, and six requests in each positive arm landing on the proxy listener); `cache_files=0` in every arm; and
  bun's own error text in every arm, a module-resolution error ("Cannot find module '@opal-no-such-scope-...'") that never names a
  registry host. The package name cannot exist, so a leak would have retrieved nothing.
- Row W13-S10: the worker's first control arm (a user-level `registry=` line) sent 6 requests toward the PUBLIC registry host in each
  of two runs; the proxy listener caught each (`CONNECT registry.npmjs.org:443`, answered 502). That arm is replaced by the
  no-network control above.
- Row W13-S13: the earlier criterion's AC5 test ran one `bun run --no-install typecheck` (script `echo typecheck-ok`) in a synthetic
  portal outside the harness. The bare `bun --version` run by this seat at the start is likewise outside the harness.
- bun 1.4.2 on a Dell is not measured here; the same script measures it (below).

## Earlier pass of this order (row NFRA_CTLPLN-S13)

The frozen-lockfile install run on this machine at about 10:55Z (`KIT_PORTAL_PACK_RECORD.md`, same folder): `bun install --frozen-lockfile`
in the base portal, exit 0, output "**7 packages installed** [347.32s]" including `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`
(a non-registry tarball URL on cdn.sheetjs.com). The record's table names six packages brought to the DEV lockfile's versions
(`@types/d3-array`, `@types/d3-interpolate`, `baseline-browser-mapping`, `caniuse-lite`, `d3-format`, `d3-time-format`); the other
install line is the `xlsx` tarball. That install ran on the registry path with no redirect and no listener, so what it contacted
(the public registry and the tarball host) is by the same reading a fetch from public hosts. It was not re-run.

## Commands another machine runs to measure its own bun

```
python org/devices/kit_bun_no_egress.py selfcheck                       (no bun process: the two listeners log Python-made requests)
python org/devices/kit_bun_no_egress.py measure --out <result.json>     (last line BUN-NO-EGRESS ...; ok=True needs a passing form)
python org/devices/kit_bun_no_egress.py wrap --from <result.json> -- run <file>
python org/devices/test_kit_bun_no_egress.py                            (BUN-KIT-TEST cases=7/7 ok=True)
```

## wk-provision.sh

`.tools/wk-provision.sh`: 44 insertions, 2 deletions (`git diff --numstat`; the two deleted lines are usage lines reworded). The `install` mode (and `provision` / `portal` arguments naming it) refuses with
rc 2 BEFORE any worktree is created, unless every registry redirect present (`BUN_CONFIG_REGISTRY`, `NPM_CONFIG_REGISTRY`,
`npm_config_registry`, a `registry =` line in the portal's `bunfig.toml`) names a non-public host and at least one is present. Refusal line:
`REFUSED: --node-modules install runs bun install, which contacts the package registry, and no request may leave this machine; use --node-modules link (the default) or --node-modules none`.
Default: link (it already was, with `none` where the main tree has no `node_modules` to link to; row W13-S9). The test ran a full `provision` on
scratch repositories with a fake `bun` first on PATH: install refused (no redirect, public redirect), install allowed with a loopback
redirect (fake bun recorded `install --frozen-lockfile`), default / link / none print the same lines as the script before the change
(`69288c8ca0`), zero requests on either listener: `WK-PROVISION-REGISTRY install_refused=True requests=0 default=link ok=True`.
