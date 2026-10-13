#!/bin/bash
# the dispatcher's own option (line 57) and a stand-in `aws` that fails the way a regional call without a region fails (rc 255 + text)
set -e
CHAIN_LABEL="chain:full"; MODE="chain"; SCRIPT_IDS="A_00 A_01"
log_ts() { date -u +%FT%TZ; }
aws() { echo "You must specify a region. You can also configure your region by running \"aws configure\"."; return 255; }
source "$1"
echo "---- calling emit_chain_complete (the chain-close path)"
emit_chain_complete 0
echo "REACHED: the statement after emit_chain_complete (CDNCOHT invalidation, recon, SHUTDOWN_ARMED follow it)"
