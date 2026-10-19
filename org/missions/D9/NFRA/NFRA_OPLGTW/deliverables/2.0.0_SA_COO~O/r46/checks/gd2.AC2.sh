#!/usr/bin/env bash
# OPLGTW OG-gd-2 AC2 (round-46 OG-gd-2): every arm that RAN names evidence that resolves -- a repo path that exists at HEAD,
# a file under W, or an s3:// key / command whose output is kept as a file under W -- and the record carries no private
# value: 0 email addresses, 0 runs of 8+ digits (account numbers; a date or a master number the PRD prints is exempt),
# 0 bearer-shaped tokens.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~162"
REC="$W/GD2_GRADE_READ.json"
[ -f "$REC" ] || { echo "GD2_GRADE_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" "$W" <<'EOF'
import json, os, re, subprocess, sys
p, W = sys.argv[1], sys.argv[2]
raw = open(p, encoding="utf-8").read()
d = json.loads(raw)
ran = [a for o in d.get("outcomes", []) for a in o.get("arms", []) if a.get("ran")]
def resolves(ev):
    for e in (ev if isinstance(ev, list) else [ev]):
        e = (e or {}) if isinstance(e, dict) else {"path": e}
        path = e.get("path") or e.get("file") or ""
        if not path:
            continue
        if path.startswith(W) and os.path.isfile(path):
            return True
        r = subprocess.run(["git", "cat-file", "-e", "HEAD:" + path.split("@")[0]], capture_output=True)
        if r.returncode == 0:
            return True
    return False
unres = sum(1 for a in ran if not resolves(a.get("evidence")))
emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw))
# A run of 8+ digits is a private value UNLESS it is a date (20YYMMDD...) or a master number the PRD itself prints.
prd = open("org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", encoding="utf-8").read()
public = set(re.findall(r"(?<![0-9])[0-9]{8}(?![0-9])", prd))
runs = re.findall(r"(?<![0-9a-f])[0-9]{8,}(?![0-9a-f])", raw)
digits = sum(1 for r in runs if r not in public and not re.match(r"^20[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])", r))
tokens = len(re.findall(r"(?i)bearer\s+[A-Za-z0-9._-]{16,}|eyJ[A-Za-z0-9_-]{10,}\.", raw))
print("arms run %d; evidence unresolved %d (want 0)" % (len(ran), unres))
print("private-value scan: emails %d, 8+ digit runs %d, token-shaped %d (want 0 each)" % (emails, digits, tokens))
print("VERDICT " + ("PASS" if ran and unres == 0 and emails == 0 and digits == 0 and tokens == 0 else "FAIL"))
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | grep -v '^VERDICT'
printf '%s\n' "$res" | grep -q '^VERDICT PASS' && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
