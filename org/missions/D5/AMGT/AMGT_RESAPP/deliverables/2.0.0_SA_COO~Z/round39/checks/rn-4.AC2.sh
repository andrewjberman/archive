#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-4 AC2 (BOUND) -- an instrument cell moves no page or component source: the portal
# diff against its base, over src/, is the new fixture alone. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
basecommit=$(git merge-base HEAD DEV)
git diff --name-only "$basecommit" -- src | grep -v '__harness__/tests/uiClipFixture.html' > .scratch.rn4.moved.txt
n=$(wc -l < .scratch.rn4.moved.txt | tr -d ' '); cat .scratch.rn4.moved.txt; rm -f .scratch.rn4.moved.txt
echo "src files moved off the base other than the fixture: $n"
[ "$n" -eq 0 ]
