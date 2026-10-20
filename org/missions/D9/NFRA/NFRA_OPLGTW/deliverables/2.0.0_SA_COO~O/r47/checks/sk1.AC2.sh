#!/usr/bin/env bash
# OPLGTW OG-sk-1 AC2: the census's citations are TRUE and it names what the dual-read cell needs. Against W/SK_CENSUS.json:
#  (a) every entry's cited line exists in the cited file and that line (read here) holds a Schwab token: schwab/ | 08403355 | prefix | silver | state | complete | backfill | last_run | opal-data | ListBucket | GetObject;
#  (b) reader_iam.tf_file exists, is a .tf, and reader_iam.statements_naming_schwab is an integer equal to the count of lines in that file matching schwab (read here);
#  (c) fence_points lists at least 2 places where a listing by prefix is turned into a per-master set (file, line, what), each citation true as in (a);
#  (d) at least 3 entries carry edit DUAL_READ or NEW_PATH_ONLY, at least one of kind contract in EACH of the two copies (infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json and org/standards/NFRA_OPLGTW_CONTRACT.json), at least one of kind iam.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~177
[ -f "$W/SK_CENSUS.json" ] || { echo "SK_CENSUS.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$W")" <<'PYEOF'
import json, os, re, sys
W = sys.argv[1]
d = json.load(open(os.path.join(W, "SK_CENSUS.json"), encoding="utf-8")); d = d.get("body", d)
tok = re.compile(r"schwab/|08403355|prefix|silver|state|complete|backfill|last_run|opal-data|ListBucket|GetObject", re.I)
GW = "infra/aws/ec2/opal-gateway/"


def line_ok(f, n):
    p = f if f.startswith(("infra/", "org/")) else GW + f
    try:
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        return False
    return 1 <= n <= len(lines) and bool(tok.search(lines[n - 1]))


ents = d.get("entries") or []
bad = [e for e in ents if not line_ok(e.get("file", ""), e.get("line", 0))]
print("entry citations: %d of %d cited lines exist and hold a Schwab token (want all): %s" % (len(ents) - len(bad), len(ents), "ok" if not bad and ents else "NOT OK (first: %s)" % (bad[0].get("file") + ":" + str(bad[0].get("line")) if bad else "none")))
ri = d.get("reader_iam") or {}
tf = ri.get("tf_file", "")
tf_ok = tf.endswith(".tf") and os.path.exists(tf)
cnt = None
if tf_ok:
    cnt = sum(1 for l in open(tf, encoding="utf-8", errors="replace").read().splitlines() if re.search("schwab", l, re.I))
print("reader IAM .tf %s exists %s; statements_naming_schwab %s equals the count of schwab lines read here %s: %s" % (tf or "(none)", tf_ok, ri.get("statements_naming_schwab"), cnt, "ok" if tf_ok and ri.get("statements_naming_schwab") == cnt else "NOT OK"))
fp = d.get("fence_points") or []
fp_ok = len(fp) >= 2 and all(line_ok(x.get("file", ""), x.get("line", 0)) and isinstance(x.get("what"), str) and len(x["what"]) >= 12 for x in fp)
print("fence points: %d listed (want 2 or more), each citation true and described: %s" % (len(fp), "ok" if fp_ok else "NOT OK"))
edits = [e for e in ents if e.get("edit") in ("DUAL_READ", "NEW_PATH_ONLY")]
c1 = any(e.get("kind") == "contract" and "deploy/NFRA_OPLGTW_CONTRACT.json" in e.get("file", "") for e in ents)
c2 = any(e.get("kind") == "contract" and "org/standards/NFRA_OPLGTW_CONTRACT.json" in e.get("file", "") for e in ents)
iam = any(e.get("kind") == "iam" for e in ents)
d_ok = len(edits) >= 3 and c1 and c2 and iam
print("edit entries %d (want 3 or more); contract entry in the deploy copy %s and in the standards copy %s; an iam entry %s: %s" % (len(edits), c1, c2, iam, "ok" if d_ok else "NOT OK"))
print("OK" if (not bad and ents and tf_ok and ri.get("statements_naming_schwab") == cnt and fp_ok and d_ok) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
