#!/usr/bin/env bash
# MX-r-12 AC3 (FWD-20 depth PROOF, second instrument, on the DEPLOYED catalog bytes): c11_depth.py run against this
# tree's catalog and discover, which equal the deployed bytes once the release's ledger closes (the applier's label
# read-back pins it). Every measured depth agrees with its served artifact read by the aws CLI; the AUA row's depth is
# answered at answer time.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
exec bash "$H/c9.AC3.sh"
