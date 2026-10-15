#!/usr/bin/env bash
# OPLGTW OG-nw-2 AC2 (round-37 G6-INTERNAL): no module-scope AWS client in news_typed.py or internal_role.py, and no fixed-depth parents index in any shipped app module.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PYEOF'
import re
bad = []
for f in ("infra/aws/ec2/opal-gateway/app/news_typed.py", "infra/aws/ec2/opal-gateway/app/internal_role.py"):
    for i, line in enumerate(open(f, encoding="utf-8"), 1):
        if re.match(r"^[A-Za-z_]\w*\s*=\s*boto3\.(client|resource)\(", line):
            bad.append("%s:%d" % (f.rsplit("/", 1)[1], i))
print("module-scope boto3 client constructions: %d (want 0)%s" % (len(bad), (" -- " + ", ".join(bad)) if bad else ""))
raise SystemExit(0 if not bad else 1)
PYEOF
); r0=$?
printf '%s\n' "$res" | tr -d '\r'
g=$(bash "$(dirname "$0")/gt10.AC2.sh"); r1=$?
printf '%s
' "$g" | head -1
[ "$r0" = 0 ] && [ "$r1" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
