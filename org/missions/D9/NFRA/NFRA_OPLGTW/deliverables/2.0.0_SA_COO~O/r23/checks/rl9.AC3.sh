#!/usr/bin/env bash
# OPLGTW OG-rl-9 AC3 (R30.3, the rest of the bar): as the REAL holder after the release, (a) the DOWNLOAD record
# GA1_DOWNLOAD.json has no duplicates and returns exactly the held set (returned = distinct = held_cusips_in_dim_position);
# (b) the QUERY path read GA1_QUERY.json, attested like ga1.AC2 by its body digest in the host's own SSM output
# (`GA1Q_DIGEST <sha256>`), is OK, held-only (unheld 0) and equals the held set the same way.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
for f in GA1_DOWNLOAD.json GA1_QUERY.json; do [ -f "$W/$f" ] || { echo "$f absent"; echo "RESULT: FAIL"; exit 1; }; done
read -r dl cid iid dig qok <<<"$(python - "$(native "$W/GA1_DOWNLOAD.json")" "$(native "$W/GA1_QUERY.json")" <<'PY' | tr -d '\r'
import hashlib, json, sys
def exact(b, op):
    h = b.get("held_check") or {}
    n = int(h.get("held_cusips_in_dim_position", -1))
    return (b.get(op) == "OK" and b.get("synthetic_principal") is False and b.get("grant_source") == "store"
            and n >= 1 and int(h.get("returned", -2)) == n and int(h.get("distinct_returned", -3)) == n
            and int(h.get("unheld_returned", -1)) == 0)
d = json.load(open(sys.argv[1], encoding="utf-8"))["body"]
q = json.load(open(sys.argv[2], encoding="utf-8")); qb = q.get("body") or {}
print("yes" if exact(d, "dim_asset_download") else "no", q.get("ssm_command_id", "NONE"), q.get("instance_id", "NONE"),
      hashlib.sha256(json.dumps(qb, sort_keys=True).encode("utf-8")).hexdigest(), "yes" if exact(qb, "dim_asset_query") else "no")
PY
)"
out=$(bash .tools/aws ssm get-command-invocation --command-id "$cid" --instance-id "$iid" --region us-east-1 \
      --query '[Status,StandardOutputContent]' --output text 2>&1 | tr -d '\r')
st=$(printf '%s\n' "$out" | head -1 | awk '{print $1}')
found=no; printf '%s\n' "$out" | grep -q "GA1Q_DIGEST $dig" && found=yes
echo "download exact held set, no duplicates: $dl; query exact held set: $qok; query ssm status ${st:-NONE}; query digest in host output: $found"
[ "$dl" = yes ] && [ "$qok" = yes ] && [ "$st" = Success ] && [ "$found" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
