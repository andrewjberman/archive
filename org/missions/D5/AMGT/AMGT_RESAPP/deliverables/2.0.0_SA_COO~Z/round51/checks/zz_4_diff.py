"""AMGT_RESAPP round 51, AMGT-zz-4 AC3 -- the packaged-file CONTENT DIFF against the DEPLOYED artifact (CTO round-50 ruling 4; row Z-S307:
a never-widen half read packaging from code comments). `infra/aws/terraform/harvest/content_diff.py --zip <zip>` compares every file
of <zip> with the artifact `opal-amgt-scoped-api` runs NOW (fetched read-only via get_function's code location) and prints one line
per file, `CONTENT-DIFF <IDENTICAL|CHANGED|ADDED|REMOVED> <archive path>`, then ONE line
`CONTENT-DIFF SUMMARY: files N, IDENTICAL i, CHANGED c, ADDED a, REMOVED r, against <CodeSha256>`.
(build-and-upload-scoped-amgt.sh calls it on the zip it builds; that full build is exercised at AMGT-zz-8, beyond a 120 s bound.)
This check fetches the deployed zip, writes a copy with lib/opal_naming.py CHANGED (a comment appended) and one file ADDED, and runs
the tool on the copy. PASS when the summary reads CHANGED 1, ADDED 1, REMOVED 0, IDENTICAL = deployed files - 1, and the CHANGED
line names lib/opal_naming.py (the difference control: the unmutated files read IDENTICAL, the mutated one does not).
usage: python <this>   (from the repo root; reads Lambda + S3 read-only, writes only a temp dir)"""
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import boto3

TOOL = "infra/aws/terraform/harvest/content_diff.py"
FUNCTION = "opal-amgt-scoped-api"
MUTATE = "lib/opal_naming.py"
ADDED = "zz_4_planted_added.txt"


def main():
    if not Path(TOOL).exists():
        print("no %s" % TOOL)
        print("THE BUILD'S CONTENT DIFF NAMES WHAT CHANGED AGAINST THE DEPLOYED ARTIFACT: NO")
        return 1
    fn = boto3.client("lambda", region_name="us-east-1").get_function(FunctionName=FUNCTION)
    with tempfile.TemporaryDirectory() as tmp:
        dep, mut = Path(tmp) / "deployed.zip", Path(tmp) / "mutated.zip"
        with urllib.request.urlopen(fn["Code"]["Location"], timeout=60) as r:  # the function's own artifact, Opal's S3
            dep.write_bytes(r.read())
        with zipfile.ZipFile(dep) as zi, zipfile.ZipFile(mut, "w", zipfile.ZIP_DEFLATED) as zo:
            names = [i.filename for i in zi.infolist() if not i.is_dir()]
            for n in names:
                data = zi.read(n)
                zo.writestr(n, data + b"\n# zz-4 planted change\n" if n == MUTATE else data)
            zo.writestr(ADDED, b"planted\n")
        print("deployed %s: %d files; %s packaged: %s" % (fn["Configuration"]["CodeSha256"], len(names), MUTATE, MUTATE in names))
        p = subprocess.run([sys.executable, TOOL, "--zip", str(mut)], capture_output=True, text=True, timeout=100)
    out = p.stdout + p.stderr
    s = re.search(r"^CONTENT-DIFF SUMMARY: files (\d+), IDENTICAL (\d+), CHANGED (\d+), ADDED (\d+), REMOVED (\d+), against (\S+)",
                  out, re.M)
    changed = re.findall(r"^CONTENT-DIFF CHANGED (\S+)", out, re.M)
    print("tool rc=%d; %s" % (p.returncode, s.group(0) if s else "no 'CONTENT-DIFF SUMMARY:' line: " + out.strip()[-200:]))
    print("CHANGED lines: %s" % changed[:3])
    ok = (bool(s) and MUTATE in names and int(s.group(3)) == 1 and int(s.group(4)) == 1 and int(s.group(5)) == 0
          and int(s.group(2)) == len(names) - 1 and [c.replace("\\", "/") for c in changed] == [MUTATE])
    print("THE BUILD'S CONTENT DIFF NAMES WHAT CHANGED AGAINST THE DEPLOYED ARTIFACT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
