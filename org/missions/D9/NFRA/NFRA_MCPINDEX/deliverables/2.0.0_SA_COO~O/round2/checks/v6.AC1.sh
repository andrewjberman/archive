#!/usr/bin/env bash
# MX-v-6 AC1 (E4, the question set from REAL asks): infra/aws/ec2/opal-gateway/tests/routing/questions.yaml holds at least
# 20 questions; every one carries a `source` naming a file that exists at HEAD (a real ask, e.g. the Analyst's thread
# memory under org/tier0_utility/0.0.3_BG_BBGTerminal/threads/) and an `expected_tool`; and NO question shares a run of
# 6 or more consecutive words with any `description` in the catalog (RCN-0014 finding 13: never probe from the index's
# own words).
. "$(dirname "$0")/_root.sh"
Q="$GW/tests/routing/questions.yaml"; CAT="$GW/app/refs/DATA_CATALOG.yaml"
[ -f "$Q" ] || { echo "$Q absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 60 python - "$Q" "$CAT" <<'EOF' 2>&1 | tr -d '\r'
import os, re, subprocess, sys, yaml
qs = yaml.safe_load(open(sys.argv[1], encoding='utf-8')) or []
if isinstance(qs, dict):
    qs = qs.get('questions', [])
cat = yaml.safe_load(open(sys.argv[2], encoding='utf-8'))
descs = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'description' and isinstance(v, str):
                descs.append(v)
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cat)
words = lambda s: re.findall(r"[a-z0-9']+", s.lower())
grams = set()
for d in descs:
    w = words(d)
    for i in range(len(w) - 5):
        grams.add(tuple(w[i:i + 6]))
src_ok = tool_ok = overlap = 0
for q in qs:
    src = str(q.get('source', '')).split(':')[0]
    if src and subprocess.run(['git', 'cat-file', '-e', 'HEAD:' + src], capture_output=True).returncode == 0:
        src_ok += 1
    if str(q.get('expected_tool', '')).strip():
        tool_ok += 1
    w = words(str(q.get('question', '')))
    if any(tuple(w[i:i + 6]) in grams for i in range(len(w) - 5)):
        overlap += 1
print('questions=%d sources_at_head=%d expected_tools=%d catalog_overlap=%d descriptions=%d' % (len(qs), src_ok, tool_ok, overlap, len(descs)))
EOF
)
echo "$out"
n=$(printf '%s' "$out" | sed -n 's/^questions=\([0-9]*\) .*/\1/p'); s=$(printf '%s' "$out" | sed -n 's/.*sources_at_head=\([0-9]*\) .*/\1/p')
t=$(printf '%s' "$out" | sed -n 's/.*expected_tools=\([0-9]*\) .*/\1/p'); o=$(printf '%s' "$out" | sed -n 's/.*catalog_overlap=\([0-9]*\) .*/\1/p')
if [ -n "$n" ] && [ "$n" -ge 20 ] && [ "$s" = "$n" ] && [ "$t" = "$n" ] && [ "$o" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
