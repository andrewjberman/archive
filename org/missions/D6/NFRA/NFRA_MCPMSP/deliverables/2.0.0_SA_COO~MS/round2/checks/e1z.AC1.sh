#!/usr/bin/env bash
# MS-dn-1 AC1 (the reader census at the Deny cut, CTO ruling 27414 -- printed with its denominator): every S3 client
# call in infra/aws/ec2/opal-gateway/app/** that can read opal-data-portal-v2 reads through an assumed role
# (app/internal_role.py or app/firm_role.py). FILE grain: counts every boto3.client("s3" ...) / .get_object( call site
# (the denominator), the files among them that read portal-v2 (query_v0, portal_index, opal_discover, or naming the
# bucket), and those reader files that reference neither role module (unrouted); PASS only with unrouted = 0 and
# reader files >= 1. File grain because query_v0 keeps its default client as the ARN-unset fallback by design; the
# served proof that reads route through the role is AC3, not this census.
. "$(dirname "$0")/_root.sh"
res=$(python - "$G/app" <<'EOF' 2>&1 | tr -d '\r'
import os, re, sys
root = sys.argv[1]; sites = []; unrouted = []; reader_files = set()
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.py'):
            continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, root).replace('\\', '/')
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:
            continue
        for i, line in enumerate(t.splitlines(), 1):
            if re.search(r'boto3\.client\(\s*["\']s3["\']', line) or re.search(r'\.get_object\(', line):
                sites.append((rel, i))
                if rel in ('internal_role.py', 'firm_role.py'):
                    continue
                if rel in reader_files:
                    continue
                reads_v2 = 'portal-v2' in t or 'query_v0' in rel or 'portal_index' in rel or 'opal_discover' in rel
                if reads_v2:
                    reader_files.add(rel)
                    if not ('internal_role' in t or 'firm_role' in t):
                        unrouted.append(rel)
print('s3 call sites scanned=%d portal-v2 reader files=%d unrouted=%d %s' % (len(sites), len(reader_files), len(unrouted), ' '.join(unrouted[:8])))
print('verdict=%s' % ('OK' if sites and reader_files and not unrouted else 'NO'))
EOF
)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
