#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPORTAL round-1 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
MP_BASE="d59ee72eba"
# The grant writer's lambda-source-map entry: the one whose source_dir names mcportal and whose key names grant-writer.
# Prints 4 lines: count, key, source_dir, tf_file (blank lines when absent). A parse failure prints "ERROR ..." on line 1
# -- never silenced: the first version swallowed a SyntaxError with 2>/dev/null and read EMPTY on every input
# (row NFRA_MCPORTAL-Z-W3-S1).
mp_writer_entry() {
  python - <<'EOF'
import json
try:
    d = json.load(open('infra/aws/lambda/ci/lambda-source-map.json', encoding='utf-8'))['functions']
except Exception as e:
    print('ERROR %s' % e); print(''); print(''); print(''); raise SystemExit(0)
hits = [(k, v) for k, v in d.items() if 'mcportal' in (v.get('source_dir') or '') and 'grant-writer' in k]
print(len(hits))
k, v = hits[0] if hits else ('', {})
print(k); print(v.get('source_dir', '') if v else ''); print(v.get('tf_file', '') if v else '')
EOF
}
