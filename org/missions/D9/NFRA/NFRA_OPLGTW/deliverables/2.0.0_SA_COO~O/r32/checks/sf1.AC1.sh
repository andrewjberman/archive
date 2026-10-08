#!/usr/bin/env bash
# OPLGTW OG-sf-1 AC1 (R54): opal_asker_query is a SAFE (read) tool. Three named tests in tests/test_asker_safe_tool.py,
# offline: (01) destructive_ops.classify("opal_asker_query") is SAFE and write_class("opal_asker_query") is None;
# (02) a call through tools._run as a SCOPED, non-master identity reaches the tool's fn (faked) and its result is NOT
# a `write_class_denied` refusal; (03) negative control: a made-up tool name that is in none of SAFE_TOOLS,
# DESTRUCTIVE_OPS and TOOL_WRITE_CLASS is still refused through the same _run by the same identity.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_sf1_audit_$$.jsonl"
pytest_named tests/test_asker_safe_tool.py test_ogsf1_ac01 test_ogsf1_ac02 test_ogsf1_ac03; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
