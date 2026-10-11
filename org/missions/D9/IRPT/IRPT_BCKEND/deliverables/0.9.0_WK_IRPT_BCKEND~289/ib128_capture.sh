#!/usr/bin/env bash
# IB128-1 (0.9.0_WK_IRPT_BCKEND~289): captures the two handler answers the thin fixtures are re-made from.
# LOCAL ONLY: existing tests run UNALTERED with in-memory fakes, under ib128_capture_plugin.py (records the returned envelope).
set -u
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
D="$R/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~289"
IR="$R/infra/aws/lambda/investor-reporting"
A="$R/.scratch/answers"
mkdir -p "$A"; rm -f "$A"/*.json
( cd "$IR/directory/tests" && IB126_WRAP=entry.ENTRY.handle IB126_OP=directory-browse IB126_MATCH='data.next_cursor=null' \
    IB126_OUT="$A/directory-browse.json" PYTHONPATH="$D" timeout 120 python -m pytest -q -p no:cacheprovider \
    -p ib128_capture_plugin "test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable" 2>&1 | tail -3 )
# analysis-input-upload (AMENDMENTS 1 and 2): by ib128_capture_upload.py -- same handler path and fakes as
# intake/tests/test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input, with TWO differences:
# the principal's firm id fir_000000000000000000000001, and IRPT_FIRM_REGISTRY -> ib128_synthetic_firm_registry.json. (cwd = repo root, as the .py expects.)
( cd "$R" && timeout 120 python "$D/ib128_capture_upload.py" )
ls -l "$A"
