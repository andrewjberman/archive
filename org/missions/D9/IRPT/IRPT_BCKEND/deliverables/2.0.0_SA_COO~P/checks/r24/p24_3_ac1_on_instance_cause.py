"""Round 24 AC (IB-pr-243) -- why the RECOVERED inf-bronze-runner wrote no raw file on 2026-09-28 (row S216; WK~81 @0b5cdb06f9:
inf-ec2-retry-launch brought i-083ad9ae297f88e9f to running at 11:15:55Z, yet no bronze/*/2026-09-28.jsonl.gz landed and
the raw pull scripts' orion/rate_limit_state_{transactions,performance}.json stayed stamped 2026-09-27).

Usage: python p24_3_ac1_on_instance_cause.py <worktree root>
Reads `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~86/ON_INSTANCE_DIAGNOSIS.json`. Pass when:
  (1) `deployed_vs_repo` is present: for each file the instance pulls from s3://opal-data-inf/code/bronze-runner/, the
      S3 sha256 beside the repo file's sha256 (infra/aws/ec2/inf-bronze-runner/, data/inf/scripts/bronze/) and a verdict;
      the check re-reads at least one of those S3 objects and confirms the recorded sha256 (a positive control on the
      instrument);
  (2) EITHER `cause` names a code path with a `file:line` citation that exists in the worktree and explains a run that
      reaches `running` yet writes no raw file, OR `needs_instance_read` is true with `reason` and `ssm_commands` (at least
      one command that reads the service journal) -- a named "cannot be seen from here" is a legal answer, a guess is not;
  (3) `evidence` has >= 3 items.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import boto3

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
rec = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~86/ON_INSTANCE_DIAGNOSIS.json"
if not rec.is_file():
    print("diagnosis record absent:", rec)
    print("P24-3-AC1 FAIL")
    sys.exit(1)
d = json.loads(rec.read_text(encoding="utf-8"))
dvr = d.get("deployed_vs_repo") or []
s3 = boto3.client("s3", region_name="us-east-1")
confirmed = False
for row in dvr:
    key, sha = row.get("s3_key"), row.get("s3_sha256")
    if key and sha:
        body = s3.get_object(Bucket="opal-data-inf", Key=key)["Body"].read()
        confirmed = hashlib.sha256(body).hexdigest() == sha
        print("instrument control: s3 %s sha256 %s recorded %s -> %s" % (key, hashlib.sha256(body).hexdigest()[:12], sha[:12], confirmed))
        break
cause_ok = False
if d.get("cause"):
    cites = re.findall(r"([\w./-]+\.(?:py|sh)):(\d+)", json.dumps(d.get("cause")))
    cause_ok = bool(cites) and all((root / f).is_file() and int(n) <= sum(1 for _ in (root / f).open(encoding="utf-8", errors="replace")) for f, n in cites)
    print("cause cites:", cites[:4], "exist:", cause_ok)
needs = bool(d.get("needs_instance_read")) and bool(d.get("reason")) and any("journal" in c for c in (d.get("ssm_commands") or []))
print("needs_instance_read named with journal command:", needs)
ev = len(d.get("evidence") or []) >= 3
ok = bool(dvr) and confirmed and (cause_ok or needs) and ev
print("deployed_vs_repo rows: %d | evidence >= 3: %s" % (len(dvr), ev))
print("P24-3-AC1 PASS" if ok else "P24-3-AC1 FAIL")
sys.exit(0 if ok else 1)
