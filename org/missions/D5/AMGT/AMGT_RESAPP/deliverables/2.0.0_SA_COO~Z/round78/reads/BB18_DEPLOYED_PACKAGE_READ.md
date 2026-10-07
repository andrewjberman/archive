# AMGT_RESAPP `AMGT-bb-18` -- what the deployed `opal-amgt-scoped-api` package holds of pyarrow and rpds-py

Read by `2.0.0_SA_COO~Z`, 2026-10-07 ~17:0xZ, for the laptop `1.0.0_SA_CTO`'s ask (relayed in `0.0.0_AB_MSTR~Z` msg 31172). No
fetch: one `get-function` read of the configuration and one local zip opened.

## The answer

**Yes: the deployed package holds both, at the pinned versions, built for the Lambda's platform.**

| | pyarrow | rpds-py |
|---|---|---|
| dist-info folder in the package | `pyarrow-16.1.0.dist-info` | `rpds_py-2026.6.3.dist-info` |
| WHEEL tags | `cp311-cp311-manylinux_2_17_x86_64`, `cp311-cp311-manylinux2014_x86_64` | the same two |
| files under the package folder | 132 (30 native `.so`) | 4 (1 native `.so`) |
| files its RECORD lists / present in the package | 745 / 138 | 9 / 9 |

- **rpds-py is whole:** 9 of the 9 files its RECORD lists are in the package.
- **pyarrow is the build's own pruned copy:** 138 of 745. The build script prunes it at packaging, so the original wheel cannot be
  rebuilt from the package; what is there is exactly what the last build shipped and what is running.

## The object read

- Deployed function: CodeSha256 `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=`, CodeSize 41,981,131, one layer
  `opal-amgt-print-deps:1` (not opened; it is not rebuilt by this redeploy).
- Local file: `C:/tmp/ba20-r77-14a36147bd.zip`, 41,981,131 bytes, 380 entries; its sha256 in the same form is
  `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=`. **Equal to the deployed hash**, so the file on disk is the deployed package
  byte for byte and nothing was downloaded from the function to read it.

## What taking them from the artifact means for the build

The build script (`infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`) today downloads seven wheels and prunes them. To
take pyarrow and rpds-py from the deployed package it must copy those two folders and their dist-info from that zip in place of
unpacking two wheels. That is an edit to the build script: a change to how a served artifact is made, so it is the CTO's call and
it belongs in the redeploy's pair. With it, the build needs from outside only the five pure wheels (approved, coming by Taildrop)
and the one Windows rpds-py wheel for the script's isolated import check (row B, joined to the batch).

## Not measured

- Whether the script's prune of a fresh pyarrow wheel would yield the same 138 files (the prune list was not compared to the
  package).
- The layer's contents.
- Whether any module added this round imports a pyarrow file the prune removed (the redeploy's own import check answers that).
