#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-2 AC1 -- the peers carry harness is green again (rn-2 broke it: its fixture's P/E
# entries carry no transform/units, so the cells rendered the raw yields 0.05/0.04 where 20/25 are asserted).
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
node src/pages/SecurityAnalysis/__harness__/peersCarry.harness.cjs > .scratch.ro2.txt 2>&1; rc=$?
tail -3 .scratch.ro2.txt; rm -f .scratch.ro2.txt; echo "peersCarry exit=$rc"
[ "$rc" -eq 0 ]
