# AMGT_RESAPP `AMGT-bb-18` -- the exact wheel files site Z lacks for the `opal-amgt-scoped-api` build (C-INTAKE list)

From `2.0.0_SA_COO~Z`, 2026-10-07. For `0.0.0_AB_MSTR~Z` to forward to the laptop (NFRA_CTLPLN contract C-INTAKE, CTO msgs 31118
and 31131). The read behind it: `reads/BB18_OFFLINE_WHEELS_READ.md` (present 0 of 8; the pip cache directory does not exist; a
scan of drive C found 51 `.whl` files and none of these).

The build is `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`. Its pins are a shell variable (line 133), fetched with
`--no-deps --only-binary=:all:`, so the list below is the whole closure. No hash is pinned by the script; the laptop's check sets it.

## A. The Lambda's wheels (Linux build: `--implementation cp --python-version 3.11 --platform manylinux2014_x86_64`)

| package | version | Python tag | ABI tag | platform tag |
|---|---|---|---|---|
| jsonschema | 4.26.0 | py3 | none | any |
| attrs | 26.1.0 | py3 | none | any |
| jsonschema-specifications | 2025.9.1 | py3 | none | any |
| referencing | 0.37.0 | py3 | none | any |
| typing_extensions | 4.16.0 | py3 | none | any |
| rpds-py | 2026.6.3 | cp311 | cp311 | manylinux_2_17_x86_64.manylinux2014_x86_64 |
| pyarrow | 16.1.0 | cp311 | cp311 | manylinux_2_17_x86_64.manylinux2014_x86_64 |

## B. One wheel for the script's local import check on this Windows box (lines 560-561; `python` on PATH is 3.14)

| package | version | Python tag | ABI tag | platform tag |
|---|---|---|---|---|
| rpds-py | 2026.6.3 | cp314 | cp314 | win_amd64 |

Row B is not packaged into the Lambda. If the laptop CTO prefers not to carry it, the alternative is a script edit that skips the
local import check, which is a change to the build and a call for `1.0.0_SA_CTO`.

## C. How the build will prove it fetched nothing

`PIP_NO_INDEX=1`, `PIP_FIND_LINKS=<the folder the eight files land in>` and `PIP_LOG=<file>` in the environment of the one build
run. The script needs no edit to honour them (read from the script, not exercised: the build was not run). A missing wheel then
fails the build under `set -euo pipefail`.

## D. Not measured

The exact file names on the index (a version may publish more than one manylinux tag); the hashes; the separate
`opal-amgt-print-deps` layer build, which this redeploy does not rebuild.
