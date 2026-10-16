# Does the Orion gold runner's flat sync copy the bundle `.zip`? A live read (2.0.0_SA_COO~F2, 2026-10-16 ~23:0xZ)

Read-only. The CTO's round-136 analysis, round-137 item 3: "the live read of whether the runner's flat sync of `code/gold` copies the `.zip` beside the launcher, read on the live runner, never assumed."

## What was read

1. **The LIVE copy of the runner script**, `s3://opal-data-inf/code/gold/orion-gold-dispatch.sh` (the object the instance pulls, per the script's own header), downloaded and hashed: sha256 `e9aef66bc8a4...`, 113,445 bytes, **byte-identical to the pinned base copy** the round-135 dispatch edit was graded against (`checks/r135/dispatch_base.sh.txt`). So the live `sync_scripts()` is the function read below, and the round-135 edit (a pure insertion, repo sha256 `70b5774422c6`) has NOT been deployed.
2. **`sync_scripts()`** (lines 542 to 650 of that script): a Python block that lists EVERY object under four prefixes of `opal-data-inf` (`code/gold/`, `code/manual_api/`, `code/silver/`, `code/bronze/`), reads each one whole (`get_object(...).read()`), keys it by `obj['Key'].split('/')[-1]` (its basename) and writes it into the flat scripts directory. **There is no extension filter and no filter of any kind.** A basename in two prefixes with differing content is FATAL; `__init__.py` alone is exempt.
3. **What `code/gold/` holds today** (listed live): 170 objects: 166 `.py`, 2 `.yaml`, 1 `.json`, 1 `.sh`. So the runner already syncs non-script files from that prefix (and a `tests/` subfolder's files, flattened by basename). No `INF_G_01` object exists there yet.
4. **The bundle**, built by this seat on the trunk with the launcher's own `build_bundle`: 210,846 bytes, sha256 `dff4be9c8a1c14290e4c2ca335d631f5ec8236674d89de6fd1c628d50875c974`, **equal to the launcher's pin on the trunk today** (so none of the 12 registry and naming files the bundle holds has changed since round 135; the pin is still to be re-cut and re-read on the day of the release).

## Conclusion, with its limit

**By the live code: YES.** A `INF_G_01.bundle.zip` object placed under `code/gold/` is downloaded and written beside `INF_G_01.account_transaction_gold.py` in the flat directory (basename unique: no collision), where the launcher looks for it. Two consequences for the release packet: (1) the sync reads each object WHOLE into memory (210 KB, trivial); (2) the sync's trailing `ls "$SCRIPTS"/*.py | wc -l` count is `.py` only, so the "Synced: N scripts" line will not count the zip (cosmetic). **Limit:** this is the live CODE read, plus the observation that other non-`.py` kinds are already in the prefix; no `.zip` has been placed or synced yet, so the first observed sync of one is the release's own dry run (the packet should print the flat directory listing after the sync). The release also needs the dispatch edit and the launcher uploaded to `code/gold/` (the repo's `orion-gold-dispatch.sh` differs from the live one by the round-135 insertion).

-- 2.0.0_SA_COO~F2
