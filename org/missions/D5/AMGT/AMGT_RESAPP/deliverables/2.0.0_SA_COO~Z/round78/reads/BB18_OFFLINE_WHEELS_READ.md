# BB18 OFFLINE WHEELS READ -- opal-amgt-scoped-api artifact build

Read for issuer `2.0.0_SA_COO~Z`, 2026-10-07. READ ONLY: no pip download/install/index, no curl,
no terraform, no AWS call, the build was not run. Claim class per value is stated in each section.

## VERDICT

PRESENT 0 of 8 wheel files. The build CANNOT be stated as offline today. `pip download --no-index
--find-links <folder>` cannot be satisfied: no folder on drive C holds any of the eight `.whl` files.

## 1. The build and the command that downloads (measured: read from the script)

- Terraform: `infra/aws/terraform/harvest/scoped-amgt-api.tf:446` `module "scoped_amgt_api"`
  (`../modules/yang-lambda`, `function_name = "opal-amgt-scoped-api"`,
  `artifact_key = "research/opal-amgt-scoped-api.zip"`, `runtime = "python3.11"`, x86_64 default).
  Terraform builds nothing; it reads the uploaded S3 object.
- Build script: `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`
  (`--build-only <out.zip>` stops before the upload).
- There is NO requirements or lock file. The pin list is a shell variable in the script (line 133).

DOWNLOAD 1 (lines 135-137), the target-platform wheels, always runs:

    python -m pip download --quiet --disable-pip-version-check --no-deps \
      --only-binary=:all: --implementation cp --python-version 3.11 \
      --platform manylinux2014_x86_64 -d "$WHEELS" $VENDOR_PINS

    VENDOR_PINS = jsonschema==4.26.0 attrs==26.1.0 jsonschema-specifications==2025.9.1
                  referencing==0.37.0 typing_extensions==4.16.0 rpds-py==2026.6.3 pyarrow==16.1.0

DOWNLOAD 2 (lines 560-561), the local overlay, runs when the build interpreter cannot import the
zip's manylinux `rpds` binary. On this Windows box that is every build (all prior build logs
print the overlay line):

    python -m pip download --quiet --disable-pip-version-check --no-deps --only-binary=:all: \
      -d "$LOCAL_WHEELS" "$RPDS_PIN"          # rpds-py==2026.6.3, tags of the BUILD interpreter

TRANSITIVES: `--no-deps` on both commands, so pip resolves nothing. The seven pins ARE the whole
closure, hand-listed. Confirmed against what a prior build packaged: the two newest kept zips
each carry exactly 7 `*.dist-info` folders, the same seven names and versions (section 3).

Both wheel folders are under `TMP="$(mktemp -d)"` with `trap 'rm -rf "$TMP"' EXIT`, so every build
deletes its own wheels. That is why no prior build left a wheel folder.

## 2. Where wheels could be, and what is there (measured)

| Location | Read | Result |
|---|---|---|
| pip cache dir `c:\users\opal bloomberg\appdata\local\pip\cache` | `pip cache dir`, `pip cache info`, `pip cache list`, `Test-Path` | The directory DOES NOT EXIST. HTTP cache (`http-v2`, `http`): 0 files, 0 bytes. Wheel cache (`wheels`): 0 locally built wheels. Parent `...\Local\pip` exists, empty, modified 2026-10-07 04:01. |
| Whole drive C, every `*.whl` | `dir /s /b /a-d C:\*.whl`, completed, exit 0 | 51 files. 0 match any of the seven package names. The 51 are: numpy-1.26.4 cp312 win_amd64 (a repo-tracked layer file, one per worktree), scipy-1.17.1 win_amd64, pip/setuptools ensurepip bundles, test fixtures. |
| Worktrees | `git worktree list` = 76 entries, all under `C:/tmp` plus the main tree | Covered by the drive scan (C:\tmp is inside it). 0 pinned wheels. |
| `%TEMP%`, Anaconda, both Python installs | inside the drive scan | 0 pinned wheels. |
| pip config / `PIP_*` env | `pip config list`, `env` | Both empty: no find-links, no index override configured. |

pip's two caches are different things. The HTTP cache (`http-v2`) stores index responses and
downloaded wheel bodies keyed by URL hash; it is not a folder of `.whl` files and `--find-links`
cannot read it. The wheel cache (`wheels`) holds only wheels pip BUILT locally from sdists; with
`--only-binary=:all:` this build never puts anything there. Here both are empty, so the
distinction changes nothing: neither holds any of the eight.

## 3. Wheel by wheel against the pin list

Exact filenames, sizes and sha256 are from the last kept build log that prints them,
`C:\tmp\az5-buildonly.log` (2026-10-06 15:58), lines `WHEEL-SHA256` and `ISOLATED: native overlay`.
Claim: measured from that log, not re-derived from an index.

| # | requirement | version | needed tag (exact file) | on disk as .whl |
|---|---|---|---|---|
| 1 | jsonschema | 4.26.0 | py3-none-any (`jsonschema-4.26.0-py3-none-any.whl`, 90630 B) | MISSING |
| 2 | attrs | 26.1.0 | py3-none-any (`attrs-26.1.0-py3-none-any.whl`, 67548 B) | MISSING |
| 3 | jsonschema-specifications | 2025.9.1 | py3-none-any (`jsonschema_specifications-2025.9.1-py3-none-any.whl`, 18437 B) | MISSING |
| 4 | referencing | 0.37.0 | py3-none-any (`referencing-0.37.0-py3-none-any.whl`, 26766 B) | MISSING |
| 5 | typing_extensions | 4.16.0 | py3-none-any (`typing_extensions-4.16.0-py3-none-any.whl`, 45571 B) | MISSING |
| 6 | rpds-py | 2026.6.3 | cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64 (371315 B) | MISSING |
| 7 | pyarrow | 16.1.0 | cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64 (40949577 B) | MISSING |
| 8 | rpds-py (local overlay, download 2) | 2026.6.3 | cp314-cp314-win_amd64 (`python` on PATH is 3.14.7, 64-bit) | MISSING |

TOTALS: present 0 of 8 (target-platform 0 of 7; local overlay 0 of 1).

sha256 of the seven target wheels as last downloaded (az5 log):

    c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  attrs-26.1.0-py3-none-any.whl
    d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce  jsonschema-4.26.0-py3-none-any.whl
    98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe  jsonschema_specifications-2025.9.1-py3-none-any.whl
    ddf5aace92d520d3d2a20031d8b0ec27b4395cab9f74e07cc95edf42a5cc0147  pyarrow-16.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
    381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231  referencing-0.37.0-py3-none-any.whl
    9c1255b302953c86a486b81d330d5ee1d5bd937691ce271b6be0ef0e299eaab7  rpds_py-2026.6.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
    481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  typing_extensions-4.16.0-py3-none-any.whl

### What IS on disk: the UNPACKED contents, inside kept build zips (not wheels)

`C:\tmp` keeps about 30 prior build zips of this function. The two newest were opened:

| zip | bytes | sha256 | entries | dist-info folders |
|---|---|---|---|---|
| `C:\tmp\ba20-r77-14a36147bd.zip` (2026-10-07 00:32) | 41981131 | 32433d29fdfb9e623eb61126651fa28fcc9b6f11ab1f1aadb289e3c88ecde5e8 | 380 | 7 |
| `C:\tmp\az5-build-r76.zip` (2026-10-06 15:58) | 41965684 | 395a4385fc031b7073284fbec03c4c94503a26bc294e71f71621c2f8daf3b2b1 | 372 | 7 |

Both carry the same seven: attrs-26.1.0, jsonschema-4.26.0, jsonschema_specifications-2025.9.1,
pyarrow-16.1.0, referencing-0.37.0, rpds_py-2026.6.3, typing_extensions-4.16.0; each with METADATA,
WHEEL and RECORD; pyarrow and rpds_py tagged cp311-cp311-manylinux_2_17_x86_64 /
manylinux2014_x86_64; 31 compiled `.so` members.

These are NOT a find-links source. pip needs `.whl` archives. Four of the seven were pruned at
packaging (az5 log: pyarrow 607 files pruned, jsonschema 13, referencing 6,
jsonschema_specifications 2), so those four cannot be rebuilt into the original wheel at all;
attrs, rpds_py and typing_extensions were packed whole (0 pruned) but a re-zipped wheel would not
carry the recorded sha256. The local overlay's content is also on disk only in installed form:
`C:\Users\Opal Bloomberg\AppData\Roaming\Python\Python314\site-packages\rpds\` at 2026.6.3.

So a no-fetch path that exists today is not "pip offline" but "vendor from a prior artifact":
take the seven vendored trees from a kept zip (already pruned, already the platform's bytes).
That is a different build, needs a script edit, and is a design call for the CTO, not a finding
that the pip step is satisfiable.

## 4. How a build would prove 0 package-index requests

Read from the script: neither `pip download` passes `--no-index`, `--find-links`, `--index-url`
or `--require-hashes`, and the script reads no variable that would add them. But pip itself maps
every long option to a `PIP_<OPTION>` environment variable, and the script does not clear the
environment, so NO SCRIPT EDIT is needed to force offline:

    PIP_NO_INDEX=1 PIP_FIND_LINKS="<folder of the 8 .whl files>" \
      bash infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh --build-only <out.zip>

- `PIP_NO_INDEX=1`: pip never contacts an index; with a wheel absent from the folder, download 1
  or 2 fails ("no matching distribution") and `set -euo pipefail` stops the build before any zip.
  The proof is therefore: the env was set AND the build completed.
- One folder serves both downloads, so it must hold all eight files, including the
  cp314 win_amd64 rpds wheel (or the build runs under an interpreter whose own rpds wheel is there).
- `--quiet` suppresses pip's "Looking in links:" line, so the script's own output does not show
  the offline mode. `PIP_LOG=<file>` (also env-only) records it without an edit. A line in the
  script that echoes `PIP_NO_INDEX`/`PIP_FIND_LINKS`, or hard-codes `--no-index --find-links`
  and `--require-hashes` against the seven sha256 above, would make the proof part of the build
  log; that is an edit, optional for forcing offline, needed for a self-evidencing log.
- Claim class: the env mapping is pip's documented behaviour, INFERRED here, not exercised
  (exercising it means running the build, which this read may not do).

## 5. Not measured

- Whether pip, given `--no-index --find-links`, accepts the folder end to end: not run.
- No drive other than C was scanned; no network share, no S3 (a wheel copy in a bucket was not
  looked for; no AWS call made).
- The 28 older kept zips in `C:\tmp` were listed, not opened.
- The sha256 values are as printed by one prior build log, not compared against an index or
  against a second log.
- Other network use by the same script was not traced: `gen_harvest_prefixes.py --check` and
  `content_diff.py --zip` (its comment says it reads `lambda get_function` and the function's
  code location) and the upload. Those are AWS calls, not package fetches; whether the new rule
  reaches them is not answered here.
- The layer `opal-amgt-print-deps` (matplotlib, numpy, pypdf and closure) is a separate artifact
  with its own builder (`build-and-upload-print-deps-layer.sh`, `build_print_deps_layer.py
  <wheel-dir> <out.zip>`); a function-only redeploy does not rebuild it. Its wheels were not
  checked; the drive scan shows none of them on disk either (no matplotlib/pypdf wheel among
  the 51).
- Why the pip cache directory is absent (never created, or purged) was not determined.
