#!/usr/bin/env bash
# OPLGTW OG-br-1 AC1 (round-34 E4, records), three records against the SERVED release:
# (1) rb.AC2: runbook 7.2 names the live release (row Z-S88);
# (2) EC2_MANIFEST opal-gateway file_checksums: every entry equals the md5 of that path's blob at deployed_commit
#     (row Z-S84; >= 10 entries);
# (3) the advi-49f-gold-dispatch source-map entry's _build_note no longer claims a BUILD_MANIFEST.json member (row S70).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
rb=FAIL; bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/rb.AC2.sh >/dev/null 2>&1 && rb=PASS
python - "$rb" <<'PY'
import hashlib, json, subprocess, sys
rb = sys.argv[1]
d = json.load(open("infra/aws/ec2/EC2_MANIFEST.json", encoding="utf-8"))["services"]["opal-gateway"]
dep = str(d.get("deployed_commit", "")); fc = d.get("file_checksums") or {}
bad = []
for path, md5 in sorted(fc.items()):
    blob = subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/%s" % (dep, path)], capture_output=True).stdout
    if hashlib.md5(blob).hexdigest() != md5:
        bad.append(path)
sm = json.load(open("infra/aws/lambda/ci/lambda-source-map.json", encoding="utf-8"))
sm = sm.get("functions", sm) if isinstance(sm, dict) else sm
items = sm.items() if isinstance(sm, dict) else enumerate(sm)
note = ""
for k, v in items:
    if isinstance(v, dict) and "advi-49f-gold-dispatch" in (str(k) + str(v.get("source_dir", ""))):
        note = str(v.get("_build_note", ""))
claims = "carries build_manifest" in note.lower()   # the exact false claim row S70 names
print("rb.AC2 %s; file_checksums %d entries at deployed_commit %s, %d differ %s; _build_note claims a BUILD_MANIFEST member: %s"
      % (rb, len(fc), dep[:10], len(bad), bad, claims))
ok = rb == "PASS" and len(fc) >= 10 and not bad and note and not claims
print("RESULT: PASS" if ok else "RESULT: FAIL"); raise SystemExit(0 if ok else 1)
PY
