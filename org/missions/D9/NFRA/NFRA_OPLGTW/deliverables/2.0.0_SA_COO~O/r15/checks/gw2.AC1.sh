#!/usr/bin/env bash
# OPLGTW OG-gw-2 AC1 (analysis round 14 R1; read-back BY CONTENT, CLAUDE.md rule 22a): the DEPLOYED
# mcportal-grant-writer-lambda zip, read in memory, equals file by file (sha256) the package build_package.py stages
# from EC2_MANIFEST.json's deployed_commit at HEAD. Counts and file names only.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
L="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"; T="${TMP:-/tmp}/og_r15_gw2_$$.zip"
( cd "$L" && timeout 300 python build_package.py --out "$(native "$T")" >/dev/null 2>&1 ); brc=$?
if [ "$brc" != 0 ] || [ ! -f "$T" ]; then echo "build_package.py rc=$brc (no staged zip)"; echo "RESULT: FAIL"; exit 1; fi
url=$(aws lambda get-function --region us-east-1 --function-name mcportal-grant-writer-lambda --query Code.Location --output text | tr -d '\r')
python - "$(native "$T")" "$url" <<'PY'
import hashlib, io, sys, urllib.request, zipfile
staged = zipfile.ZipFile(sys.argv[1])
dep = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(sys.argv[2], timeout=60).read()))
def h(z):
    return {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith("/")}
s, d = h(staged), h(dep)
same = sum(1 for n in s if d.get(n) == s[n])
diff = sorted(n for n in s if n in d and d[n] != s[n])
print("files deployed %d staged %d same %d diff %d only-deployed %d only-staged %d"
      % (len(d), len(s), same, len(diff), len(set(d) - set(s)), len(set(s) - set(d))))
for n in diff:
    print("  DIFF", n)
ok = len(s) > 0 and same == len(s) == len(d)
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
PY
rc=$?; rm -f "$T"; exit $rc
