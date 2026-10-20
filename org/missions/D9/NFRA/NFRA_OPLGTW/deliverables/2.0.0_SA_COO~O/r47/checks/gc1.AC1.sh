#!/usr/bin/env bash
# OPLGTW OG-gc-1 AC1 (round 47, PHASE A): the client_* tools for Alyssa and Menachem -- the FACTS first. W/GC1_GATES.json:
#  {"principals": {"alyssa": P, "menachem": P}, "write_path": W} where P = {"role", "profile_present": bool, "client_tools": {t: "admitted" | "denied:<gate>"} for the five tools client_resolve_account, client_get_holdings,
#   client_get_transactions, client_get_allocation, client_get_fees, "gates_read": [names of the gates the applier read, from: tool_denial, identity_scope, person_access, tier, entitlements, admit_scope],
#   "needs_write": bool, "reason": "<one or two sentences>"}  and  W = {"mechanism": "<how a person_access record is written today>", "needs_owner_session": bool, "writer": "<the component>"}.
#  Amended 2026-10-20 (row Z-S434): a denied principal with person_access_can_admit false (the gate is entitlements: decide() runs before person_access) needs NO ask, and none may be present.
#  Consistency: needs_write is true exactly when at least one of the five tools reads "denied:..."; when needs_write is true for a principal, the ask W/NEVER_WIDEN_ASK_OG-gc-1.md has three headed halves, names the exact
#  tools_allow set (a subset of the five), states that nothing else is widened (no channel, no other tool), and carries the process-wide-state line; when no principal needs a write, the ask is absent and the record says so (needs_write false for both).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
[ -f "$W/GC1_GATES.json" ] || { echo "GC1_GATES.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$W")" <<'PYEOF'
import json, os, re, sys
W = sys.argv[1]
d = json.load(open(os.path.join(W, "GC1_GATES.json"), encoding="utf-8")); d = d.get("body", d)
TOOLS = ("client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees")
GATES = {"tool_denial", "identity_scope", "person_access", "tier", "entitlements", "admit_scope"}
pr = d.get("principals") or {}
ok = True
need_any = False
pa_can = []
for who in ("alyssa", "menachem"):
    p = pr.get(who) or {}
    ct = p.get("client_tools") or {}
    tools_ok = set(ct) == set(TOOLS) and all(v == "admitted" or (isinstance(v, str) and v.startswith("denied:")) for v in ct.values())
    denied = any(isinstance(v, str) and v.startswith("denied:") for v in ct.values())
    consistent = p.get("needs_write") is denied and isinstance(p.get("needs_write"), bool)
    gates_ok = bool(p.get("gates_read")) and set(p["gates_read"]) <= GATES and len(p["gates_read"]) >= 3
    reason_ok = isinstance(p.get("reason"), str) and len(p["reason"]) >= 30
    need_any = need_any or denied
    if denied and p.get("person_access_can_admit") is not False:
        pa_can.append(who)
    good = p.get("role") == who and isinstance(p.get("profile_present"), bool) and tools_ok and consistent and gates_ok and reason_ok
    ok = ok and good
    print("%s: five client tools classified %s (denied %s), needs_write %s consistent with them %s, gates read %s, reason stated: %s" % (
        who, "yes" if tools_ok else "NO", denied, p.get("needs_write"), "yes" if consistent else "NO", len(p.get("gates_read") or []), "ok" if good else "NOT OK"))
wp = d.get("write_path") or {}
wp_ok = all(isinstance(wp.get(k), str) and wp[k] for k in ("mechanism", "writer")) and isinstance(wp.get("needs_owner_session"), bool)
print("write path named: mechanism and writer stated, needs_owner_session %s: %s" % (wp.get("needs_owner_session"), "ok" if wp_ok else "NOT OK"))
ok = ok and wp_ok
ask_path = os.path.join(W, "NEVER_WIDEN_ASK_OG-gc-1.md")
if need_any and pa_can:
    try:
        ask = open(ask_path, encoding="utf-8").read()
    except Exception:
        ask = ""
    halves = all(re.search(r"(?mi)^#{2,4}\s.*\b%s\b" % h, ask) for h in ("CTO", "COO", "CVO"))
    pws = "process-wide state this change touches" in ask
    named = set(re.findall(r"client_[a-z_]+", ask)) & set(TOOLS)
    nothing_else = bool(re.search(r"(?i)nothing else is widened", ask))
    emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", ask))
    ask_ok = halves and pws and bool(named) and nothing_else and emails == 0
    print("ask (a write is needed): three halves %s, process-wide state line %s, tools_allow set names %d of the five tools, 'nothing else is widened' %s, e-mail-shaped strings %d: %s" % (halves, pws, len(named), nothing_else, emails, "ok" if ask_ok else "NOT OK"))
    ok = ok and ask_ok
else:
    absent = not os.path.exists(ask_path)
    why = "no denial" if not need_any else "a person_access record cannot admit the denied tools (person_access_can_admit false for every denied principal: the denial is decide()'s)"
    print("no person_access write is effective (%s): no ask expected, none present %s: %s" % (why, absent, "ok" if absent else "NOT OK"))
    ok = ok and absent
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
