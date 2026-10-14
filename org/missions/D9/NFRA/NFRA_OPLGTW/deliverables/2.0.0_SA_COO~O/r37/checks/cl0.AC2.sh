#!/usr/bin/env bash
# OPLGTW OG-cl-0 AC2 (round-37 G1-TYPED, FWD-22 G2): the client-tool contract names the five core tools, each with its required clauses,
# and the registry proposal exists; nothing was applied (the two registry files are unchanged against the branch's fork point).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~83"
base=$(git merge-base HEAD box/sitez 2>/dev/null | tr -d '\r')
chg=$(git diff --name-only "$base" HEAD -- org/standards/NFRA_OPLGTW_CONTRACT.json infra/logic/registry/scopes.json | grep -c .)
res=$(python - "$(native "$W/G2_CLIENT_TOOLS_CONTRACT.md")" "$(native "$W/G2_SCOPES_PROPOSAL.md")" <<'EOF'
import re, sys
ok = True
tools = ["client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"]
clauses = ["inputs", "freshness", "fence", "refus"]
try:
    t = open(sys.argv[1], encoding="utf-8").read()
    secs = re.split(r"(?m)^#{1,4}\s+", t)
    have = 0; full = 0
    for name in tools:
        body = [s for s in secs if s.startswith("`%s`" % name) or s.startswith(name)]
        if body:
            have += 1
            low = body[0].lower()
            if all(c in low for c in clauses):
                full += 1
    pins = sum(1 for k in ("08403355", "08335338", "08242234", "last-4", "trading day") if k in t.lower() or k.replace("-", " ") in t.lower())
    print("contract: tool sections %d of 5, each with inputs, freshness, fence and refusal clauses %d of 5; decisions carried %d of 5" % (have, full, pins))
    ok = have == 5 and full == 5 and pins == 5
except Exception as e:
    print("contract: absent or unreadable (%s)" % type(e).__name__); ok = False
try:
    p = open(sys.argv[2], encoding="utf-8").read()
    print("scopes proposal: names 08403355 %s" % ("yes" if "08403355" in p else "no"))
    ok = ok and "08403355" in p
except Exception:
    print("scopes proposal: absent"); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
echo "registry files changed by this cell: $chg (want 0)"
[ "$chg" = 0 ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
