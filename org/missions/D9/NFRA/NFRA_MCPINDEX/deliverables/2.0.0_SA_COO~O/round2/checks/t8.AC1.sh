#!/usr/bin/env bash
# MX-t-8 AC1 (C2 per tool, on the tool's own cell): the two named tests pass, nothing failed.
#   test_portal_tools_register_dormant_with_class   dormant by default; with its id set it adds exactly its pinned list; every
#                                                   tool resolves through destructive_ops.classify and data_entitlement by name
#   test_portal_tools_catalog_refs_resolve          every tool's catalog-entry reference resolves to an entry in the
#                                                   regenerated DATA_CATALOG.yaml (the limb @5f3b4a20c6 (b) moved here)
. "$(dirname "$0")/_root.sh"
if pytest_named tests/test_portal_index.py test_portal_tools_register_dormant_with_class test_portal_tools_catalog_refs_resolve; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
