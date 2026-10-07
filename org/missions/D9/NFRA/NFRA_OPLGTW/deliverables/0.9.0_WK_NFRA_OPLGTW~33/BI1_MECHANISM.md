# OG-bi-1 -- mechanism chosen

By 0.9.0_WK_NFRA_OPLGTW~33. Read: `bun --version` = 1.3.14; `bun install --help` (both local).

## (a) A no-network installer mode of this bun: NONE EXISTS

`bun install --help` on 1.3.14 lists no `--offline`, `--prefer-offline` or `--frozen-cache` flag. The cache flags it has
are `--cache-dir` (a location) and `--no-cache` (ignore the manifest cache: more fetching, not less). `--registry`
only re-points the registry; `--dry-run` is not stated to avoid the registry. No flag in the help refuses the network.

## (b) CHOSEN: the pre-check `infra/aws/ec2/opal-gateway/ops/bun_cache_precheck.py`

It reads the lockfile's `packages` section and checks that each registry entry's directory
`<cache>/<name>@<version>@@@1` exists in bun's install cache (cache default: `BUN_INSTALL_CACHE_DIR`, else
`BUN_INSTALL/install/cache`, else `~/.bun/install/cache`). It prints `<present> of <total>` then the missing
`name@version` lines; exit 0 only if nothing is missing. It never runs bun and never opens a socket. In
`deploy-to-ec2.sh` it runs inside the same subshell as `bun install --frozen-lockfile`, joined with `&&`, so a miss
exits the subshell before `bun install`.

Two rules the real lockfile forced (found by the first read, 75 of 127 before they were added):
- os/cpu: an entry whose `os`/`cpu` field excludes the host is not installed by bun and is not counted (the lockfile
  names every platform's esbuild and rollup binary; 50 of the 127 are other platforms').
- prerelease: bun stores `gensync@1.0.0-beta.2` as `gensync@1.0.0-<16 hex>@@@1`. The hash function was not reproduced,
  so a prerelease counts as present when ANY `<name>@<x.y.z>-<hash>@@@1` directory exists. This is weaker than an exact
  match: the check cannot tell `beta.2` from another prerelease of the same x.y.z. 2 of 77 entries are prereleases.

## Can the script's install line send a metadata request when every package is cached?

UNDETERMINED. The mode the script uses is (b) plus the existing `bun install --frozen-lockfile`; no offline mode exists
to add. What was read: `bun install --help` (no flag that forbids or confirms it) and the earlier source read
`S24_BUN_INSTALL_SOURCE_READ_20261007.md` (bun should need no registry request with a frozen lockfile and a full cache,
but that is documented behaviour, not a measurement). A yes/no needs a network observation or reading bun's source,
neither of which this cell may do. What (b) guarantees: no TARBALL can be fetched, because a missing one stops the
deploy first. It does not guarantee that no metadata request is sent.
