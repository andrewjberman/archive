#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-7 AC3 -- the SERVED peers object carries the units, so the page's P/E reads in band:
# the RELATION criterion (checks/pe-relation.cjs: P/E x percent yield == 100 on every member) over the deployed peers response.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T=$(bash org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/ro-7.served.sh | tail -1); [ -d "$T" ] || { echo "no capture"; exit 1; }
cd portal && cp "$T/served/served_fixture.BA_US_Equity.json" .scratch.ro7.peers.json && node ../org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/pe-relation.cjs --fixture .scratch.ro7.peers.json --route peers; rc=$?; rm -f .scratch.ro7.peers.json; rm -rf "$T"  # the script joins --fixture onto the portal root
echo "served P/E magnitude rc=$rc"; [ "$rc" -eq 0 ]
