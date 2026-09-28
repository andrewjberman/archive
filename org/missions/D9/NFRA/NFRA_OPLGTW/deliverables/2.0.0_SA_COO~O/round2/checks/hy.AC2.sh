#!/usr/bin/env bash
# OPLGTW OG-h-1 AC2 (items C, D, E): two consecutive single-process runs over the modules the items repair each pass, and
# neither run leaves a tracked file modified. Bounded for the worker's 120 s limit: the full suite does not fit, so the
# run is the four modules the rows name -- test_ratelimit.py first (W3-S6: its module-level fake monotonic clock froze
# asyncio for every later test; at base, ratelimit then test_ogq1_ac02 HANGS), then test_ogq1_ac02 (W6-S9 arm 1),
# test_schwab_export.py (W6-S9 arm 2) and test_oauth_durable.py (the W3-S6 pairing victim). The last two import moto,
# so they need the interpreter <SUITE_INTERPRETER> (.venv-og); without moto they are excluded and the exclusion printed.
# AUDIT_PATH is deliberately UNSET for the runs: item C (tests/conftest.py) must isolate it itself (W3-S2).
# Interpreter: $OG_PY (default: .venv-og/Scripts/python when present, else python).
. "$(dirname "$0")/_root.sh"
if [ -n "${OG_PY:-}" ]; then PY="$OG_PY"; elif [ -x .venv-og/Scripts/python ]; then PY="$(pwd)/.venv-og/Scripts/python"; else PY=python; fi
MODS="tests/test_ratelimit.py tests/test_schwab_engine.py::test_ogq1_ac02"
nx=0
if "$PY" -c "import moto" >/dev/null 2>&1; then MODS="$MODS tests/test_schwab_export.py tests/test_oauth_durable.py"
else nx=2; fi
echo "interpreter $PY; modules: $MODS; moto-importing modules excluded $nx"
before=$(git status --porcelain --untracked-files=no | tr -d '\r')
res=""
for run in 1 2; do
  out=$(cd "$GW" && env -u AUDIT_PATH timeout 50 "$PY" -m pytest $MODS -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
  echo "  run $run rc=$rc: $(printf '%s\n' "$out" | tail -1)"
  [ "$rc" = 0 ] && res="$res run $run passed," || res="$res run $run FAILED,"
done
after=$(git status --porcelain --untracked-files=no | tr -d '\r')
mod=$(comm -13 <(printf '%s\n' "$before" | sort) <(printf '%s\n' "$after" | sort) | grep -c .)
comm -13 <(printf '%s\n' "$before" | sort) <(printf '%s\n' "$after" | sort) | sed 's/^/  modified by runs: /'
restore_audit
echo "${res# } tracked files modified by the runs $mod" | sed 's/, tracked/; tracked/'
case "$res" in *FAILED*) echo "RESULT: FAIL"; exit 1;; esac
[ "$mod" = 0 ] && [ "$nx" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
