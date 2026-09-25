#!/usr/bin/env bash
# MX-d-2 AC1 (E1, the discover answer): the two named tests pass, nothing failed.
#   test_discover_names_catalogued_dataset   a catalogued subject returns property, dataset, freshness field and latest
#                                            value, firm scope, caveats and the next tool to call, read from the ONE catalog
#   test_discover_uncatalogued_names_nothing (difference) an uncatalogued subject says it is not catalogued and names no
#                                            dataset and no tool, in the same test as a catalogued one that names a tool
. "$(dirname "$0")/_root.sh"
if pytest_named tests/test_opal_discover.py test_discover_names_catalogued_dataset test_discover_uncatalogued_names_nothing; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
