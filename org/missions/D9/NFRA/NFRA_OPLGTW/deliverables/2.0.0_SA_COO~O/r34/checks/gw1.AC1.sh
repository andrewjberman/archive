#!/usr/bin/env bash
# OPLGTW OG-gw-1 AC1 (round-34 E2, row W42-S1): the grant-writer zip built by build_package.py at
# W/mcportal-grant-writer.zip carries data_entitlement.py and the entitlement contract byte-equal (md5) to the blobs at
# the LIVE gateway release (EC2_MANIFEST deployed_commit). The contract-staging test passes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
Z="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~56/mcportal-grant-writer.zip"
[ -f "$Z" ] || { echo "zip absent: $Z"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$Z")" <<'PY'
import hashlib, json, subprocess, sys, zipfile
dep = json.load(open("infra/aws/ec2/EC2_MANIFEST.json", encoding="utf-8"))["services"]["opal-gateway"]["deployed_commit"]
z = zipfile.ZipFile(sys.argv[1]); names = z.namelist()
checked, bad = 0, []
for n in names:
    base = n.rsplit("/", 1)[-1]
    if base == "data_entitlement.py" or base.endswith("_CONTRACT.json") or "contract" in base.lower() and base.endswith(".json"):
        cands = subprocess.run(["git", "ls-tree", "-r", "--name-only", dep, "infra/aws/ec2/opal-gateway/"], capture_output=True,
                               text=True).stdout.split()
        src = [c for c in cands if c.endswith("/" + base)]
        blob = subprocess.run(["git", "show", "%s:%s" % (dep, src[0])], capture_output=True).stdout if src else b""
        checked += 1
        if not src or hashlib.md5(blob).hexdigest() != hashlib.md5(z.read(n)).hexdigest():
            bad.append(n)
print("live release %s; zip members %d; entitlement members checked %d (want >=2); differing %d %s"
      % (dep[:10], len(names), checked, len(bad), bad))
raise SystemExit(0 if checked >= 2 and not bad else 1)
PY
eq=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_schwab_host_inputs.py -k test_grant_writer_stages_the_contract_only_from_the_standard -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
echo "contract-staging test: pytest rc=$rc; $(printf '%s\n' "$out" | tail -1)"
restore_audit
[ "$eq" = 0 ] && [ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
