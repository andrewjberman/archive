"""OG-rl-15 (row Z-S67, R49): the refresh families of the scoped concierge (and, for the re-authentication cost, the other two connected roles) by status, with the number
revoked at or after a start time. READ-ONLY: one paginated dynamodb scan of gateway-access-state-table under the CALLER's AWS identity (the host role is not asked), counts only.
The scan is client-side filtered to family HEAD records (the items that carry `status`). Roles are decided from the record's email local part and only the role name is printed:
no tid, oid, email, family id, token hash or client id leaves this process. Reason strings are printed (a fixed vocabulary: refresh_token_reuse ...).

usage: python r29_revoked_read.py <since, e.g. 2026-10-09T11:00:00Z> [<out json>]
Prints  REVOKED_READ {"since", "scanned_items", "heads": {role: {status: n}}, "revoked_since": {role: {reason: n}}, "concierge_revoked_since": n}
The denominator (items scanned, pages) is printed beside the count: a scan that stops early is not a zero."""
import datetime
import json
import os
import subprocess
import sys

since = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else None
t0 = datetime.datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()
HERE = os.path.dirname(os.path.abspath(__file__))
root = HERE
while root != os.path.dirname(root) and not os.path.isdir(os.path.join(root, ".tools")):
    root = os.path.dirname(root)
shim = os.path.join(root, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
# the CLI v2 auto-paginates a scan (--no-paginate is the hazard, CLAUDE.md 22a); the denominator is printed beside the count
p = subprocess.run([shim, "dynamodb", "scan", "--table-name", "gateway-access-state-table", "--region", "us-east-1", "--output", "json"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
if p.returncode != 0:
    print("SCAN FAILED rc=%d %s" % (p.returncode, p.stderr.strip()[:200]))
    sys.exit(2)
d = json.loads(p.stdout)
items, pages = d["Items"], d.get("ScannedCount")
if d.get("LastEvaluatedKey"):
    print("SCAN INCOMPLETE (a LastEvaluatedKey came back): the count below is NOT a count")
    sys.exit(2)


def sv(i, k):
    v = i.get(k)
    return None if v is None else list(v.values())[0]


ROLES = {"opalbloomberg": "concierge", "andrew": "andrew", "alyssa": "alyssa"}
heads, revoked_since = {}, {}
for i in items:
    if not (sv(i, "pk") or "").startswith("RUNTIME#") or "family_id" not in i or "status" not in i:
        continue
    role = ROLES.get(((sv(i, "email") or "").split("@")[0]).lower(), "other")
    st = sv(i, "status")
    heads.setdefault(role, {})
    heads[role][st] = heads[role].get(st, 0) + 1
    if st == "revoked":
        try:
            at = float(sv(i, "revoked_at") or 0)
        except ValueError:
            at = 0.0
        if at >= t0:
            revoked_since.setdefault(role, {})
            reason = sv(i, "revoked_reason") or "none"
            revoked_since[role][reason] = revoked_since[role].get(reason, 0) + 1
body = {"since": since, "scanned_items": len(items), "scanned_count": pages, "heads": heads, "revoked_since": revoked_since,
        "concierge_revoked_since": sum(revoked_since.get("concierge", {}).values())}
print("REVOKED_READ " + json.dumps(body, sort_keys=True))
if out:
    with open(out, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps(body, sort_keys=True, indent=1) + chr(10))
