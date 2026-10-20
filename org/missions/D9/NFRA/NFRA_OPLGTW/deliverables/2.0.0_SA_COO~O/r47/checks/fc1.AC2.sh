#!/usr/bin/env bash
# OPLGTW OG-fc-1 AC2 (round 47, D3 / Z-S411): client_resolve_account answers a multi-vendor merge under an envelope that describes EVERY vendor read.
# Fixture: three fake adapters, all serving the canonical 49financial firm, registered under vendors fakea (answers, zero candidates, source key a/k),
# fakeb (answers, one candidate, source key b/k), fakec (refuses firm_not_served). Expected envelope after the fix:
#   candidate_count 1; absent_reason None (a candidate was found); source_keys the sorted union [a/k, b/k]; denominator["candidates"] == 1 and
#   denominator["by_vendor"] keyed by exactly fakea and fakeb; refusals == [{"vendor": "fakec", "code": "firm_not_served"}].
# Controls: ONE adapter answering with no refusal -> no "refusals" key, source_keys that adapter's, denominator["candidates"] 1; two adapters answering
# zero candidates -> absent_reason is the adapter's own code, candidate_count 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 100 python3 -I - <<'EOF'
import sys, types
sys.path.insert(0, ".")
from app import client_core as core

class Ctx:
    def freshness_td(self, d):
        return 0

class Refuse(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code

def adapter(name, cands, source, absent=None, refuse=None):
    m = types.ModuleType("fake_" + name)
    m.VENDOR, m.FIRMS = name, ("49financial",)
    def resolve_account(ctx, firm, last4, platform=None, as_of=None):
        if refuse:
            raise Refuse(refuse)
        out = {"candidates": [{"account_ref": "acr_%s_%d" % (name, i), "segment": name, "platform_label": None} for i in range(cands)],
               "_as_of": "2026-10-16", "_partition_date": None, "_source_keys": [source], "_denominator": {"candidates": cands},
               "_platform_label": None, "_platform_label_source": None, "_label_claim": None}
        if absent:
            out["_absent_reason"] = absent
        return out
    m.resolve_account = resolve_account
    return m

def run(mods):
    core._adapters.clear()
    for m in mods:
        core.register_adapter(m)
    core._new_ctx = lambda: Ctx()
    core._admit = lambda tool: None
    return core.client_resolve_account("49financial", "1234", as_of="2026-10-16")

ok = True
env = run([adapter("fakea", 0, "a/k", absent="no_candidate_for_last4"), adapter("fakeb", 1, "b/k"), adapter("fakec", 0, "c/k", refuse="firm_not_served")])
keys_ok = sorted(env.get("source_keys") or []) == ["a/k", "b/k"]
den = env.get("denominator") or {}
den_ok = isinstance(den, dict) and den.get("candidates") == 1 and sorted((den.get("by_vendor") or {}).keys()) == ["fakea", "fakeb"]
ref_ok = env.get("refusals") == [{"vendor": "fakec", "code": "firm_not_served"}]
one_ok = env.get("candidate_count") == 1 and env.get("absent_reason") is None
print("merge: candidate_count %s, absent_reason %s: %s" % (env.get("candidate_count"), env.get("absent_reason"), "ok" if one_ok else "NO"))
print("merge: source_keys %s (want union a/k b/k): %s" % (env.get("source_keys"), "ok" if keys_ok else "NO"))
print("merge: denominator candidates %s, by_vendor keys %s: %s" % (den.get("candidates") if isinstance(den, dict) else None, sorted((den.get("by_vendor") or {}).keys()) if isinstance(den, dict) else None, "ok" if den_ok else "NO"))
print("merge: refusals %s: %s" % (env.get("refusals"), "ok" if ref_ok else "NO"))
ok = ok and one_ok and keys_ok and den_ok and ref_ok
env1 = run([adapter("fakea", 1, "a/k")])
c1 = "refusals" not in env1 and env1.get("candidate_count") == 1 and env1.get("source_keys") == ["a/k"] and (env1.get("denominator") or {}).get("candidates") == 1
print("control one adapter: no refusals key, source_keys %s, denominator %s: %s" % (env1.get("source_keys"), env1.get("denominator"), "ok" if c1 else "NO"))
ok = ok and c1
env0 = run([adapter("fakea", 0, "a/k", absent="no_candidate_for_last4"), adapter("fakeb", 0, "b/k", absent="no_candidate_for_last4")])
c0 = env0.get("candidate_count") == 0 and env0.get("absent_reason") == "no_candidate_for_last4"
print("control zero candidates: candidate_count %s, absent_reason %s: %s" % (env0.get("candidate_count"), env0.get("absent_reason"), "ok" if c0 else "NO"))
ok = ok and c0
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
