#!/bin/bash
# TO-AR-y-338 step 5: the named test files, ONE PROCESS PER FILE, on an extracted package tree in the repo-depth layout.
# usage: run_tests_r31.sh <package-root posix> <out dir posix> <worktree posix: the release worktree at the pin, the source of the test folders and root docs>
# The package tree is the extracted tarball (host bytes); the test folders and the repository-root docs contract are copied
# from the release worktree (the pin), as AR-y-324 did. Nothing is uploaded, installed or run on a host.
set -u
PKG=$1; OUT=$2; WT=$3
DEST=$(dirname "$(dirname "$(dirname "$(dirname "$PKG")")")")
mkdir -p "$OUT"
for d in intake/tests ops/tests reports/tests ycharts/session/tests ycharts/generate/tests ycharts/research/tests _authz/tests _scope/tests; do
  rm -rf "$PKG/$d"; mkdir -p "$PKG/$d"; cp -r "$WT/infra/aws/lambda/investor-reporting/$d/." "$PKG/$d/"
done
# harness addition (not a package member; AR-y-324 did the same): the trunk ordinary-viewer module the _scope test imports
cp "$WT/infra/aws/lambda/investor-reporting/_scope/ordinary_viewer.py" "$PKG/_scope/ordinary_viewer.py"
mkdir -p "$DEST/docs/contracts/investor-reporting/v1"; cp -r "$WT/docs/contracts/investor-reporting/v1/." "$DEST/docs/contracts/investor-reporting/v1/"
cd "$PKG" || exit 9
PP=""
for d in "$PKG" "$PKG/_scope" "$PKG/_ids" "$PKG/_keys" "$PKG/_authz" "$PKG/_contracts" "$PKG/intake" "$PKG/ops" "$PKG/reports" "$PKG/ycharts/generate" "$PKG/ycharts/session" "$PKG/ycharts/extract" "$PKG/lib" "$PKG/intake/tests" "$PKG/ops/tests" "$PKG/reports/tests" "$PKG/ycharts/session/tests" "$PKG/ycharts/generate/tests" "$PKG/ycharts/research/tests" "$PKG/_authz/tests" "$PKG/_scope/tests"; do
  w=$(cygpath -w "$d"); PP="${PP:+$PP;}$w"
done
echo "PYTHONPATH entries: $(echo "$PP" | tr ';' '\n' | wc -l)"
FILES="_scope/tests/test_ordinary_viewer.py _scope/tests/test_ordinary_owner_composition.py intake/tests/test_load_input_owner_typed.py ycharts/generate/tests/test_composition_refusal_cause.py ycharts/generate/tests/test_ordinary_owner_legacy_row.py intake/tests/test_correction_words.py intake/tests/test_shares_not_composed_words.py intake/tests/test_deferred_resolution.py ops/tests/test_status.py reports/tests/test_resident_r31_source.py reports/tests/test_resident_r31_packager_bindings.py ycharts/research/tests/test_commentary_standalone_pdf.py ycharts/research/tests/test_commentary_disclaimer_pending.py ops/tests/test_commentary_pdf_route.py"
for f in $FILES; do
  name=$(echo "$f" | tr '/' '_')
  PYTHONPATH="$PP" timeout 300 python -m pytest -q -p no:cacheprovider "$f" > "$OUT/$name.txt" 2>&1
  rc=$?
  echo "rc=$rc $f :: $(tail -n 1 "$OUT/$name.txt")"
done
