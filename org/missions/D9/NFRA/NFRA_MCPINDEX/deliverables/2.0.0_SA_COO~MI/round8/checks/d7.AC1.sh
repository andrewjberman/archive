#!/usr/bin/env bash
# MX-d-7 AC1 (FWD-11, FWD-13, PRD v0.7 contract 4): discover's latest_value is READ from the served artifact's own
# vintage_field at answer time (claim measured), never the held certification value; the model-performance ask routes
# to mdpf_get_model_benchmarks. Named tests, offline (injected readers), and no other test in the file fails.
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_opal_discover.py \
  test_latest_value_is_read_from_the_served_artifact \
  test_latest_value_never_falls_back_to_the_held_value \
  test_model_performance_ask_routes_to_the_benchmarks_tool
rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
