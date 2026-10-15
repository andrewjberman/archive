#!/usr/bin/env bash
# OPLGTW OG-cp-2 AC2 (round-37 R37-PERSON): the contract copies stay byte-equal and still declare person_access once with its eight fields and no tier field.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
bash "$(dirname "$0")/../../r38/checks/cp1.AC2.sh" | tail -4
exit "${PIPESTATUS[0]}"
