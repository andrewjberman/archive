#!/bin/bash
# AR-y-324 step 6: the named test files, one pytest run each, on the extracted r30 package (repo-depth layout).
set -u
PKGPOSIX=/c/dev/irpt-release-r30/pkgtest/infra/aws/lambda/investor-reporting
OUT=/c/dev/irpt-release-r30/tests_out
mkdir -p "$OUT"
cd "$PKGPOSIX" || exit 9
PP=""
for d in "$PKGPOSIX" "$PKGPOSIX/_scope" "$PKGPOSIX/_ids" "$PKGPOSIX/_keys" "$PKGPOSIX/_authz" "$PKGPOSIX/_contracts" "$PKGPOSIX/intake" "$PKGPOSIX/ops" "$PKGPOSIX/reports" "$PKGPOSIX/ycharts/generate" "$PKGPOSIX/ycharts/session" "$PKGPOSIX/ycharts/extract" "$PKGPOSIX/lib" "$PKGPOSIX/intake/tests" "$PKGPOSIX/ops/tests" "$PKGPOSIX/reports/tests" "$PKGPOSIX/ycharts/session/tests" "$PKGPOSIX/ycharts/generate/tests" "$PKGPOSIX/ycharts/research/tests" "$PKGPOSIX/_authz/tests" "$PKGPOSIX/_scope/tests"; do
  w=$(cygpath -w "$d"); PP="${PP:+$PP;}$w"
done
echo "PYTHONPATH entries: $(echo "$PP" | tr ';' '\n' | wc -l)"
for f in _scope/tests/test_ordinary_viewer.py _scope/tests/test_ordinary_owner_composition.py intake/tests/test_load_input_owner_typed.py ycharts/generate/tests/test_composition_refusal_cause.py ycharts/generate/tests/test_ordinary_owner_legacy_row.py intake/tests/test_correction_words.py intake/tests/test_shares_not_composed_words.py intake/tests/test_deferred_resolution.py ops/tests/test_status.py; do
  name=$(echo "$f" | tr '/' '_')
  PYTHONPATH="$PP" timeout 600 python -m pytest -q -p no:cacheprovider "$f" > "$OUT/$name.txt" 2>&1
  rc=$?
  echo "rc=$rc $f :: $(tail -n 1 "$OUT/$name.txt")"
done
