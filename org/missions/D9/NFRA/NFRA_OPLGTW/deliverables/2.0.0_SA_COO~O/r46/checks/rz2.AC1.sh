#!/usr/bin/env bash
# OPLGTW OG-rz-2 AC1 (Phase A): the resize is prepared and asked. NO apply, NO deploy.
#  - W/RZ2_BEFORE.json: instance id, type, state, az, eip_attached, public_ip_changes_on_stop_start, target_health, nrestarts,
#    unit_memory_high, unit_memory_max, memory_total_mb, live_ref, public_ip_surfaces {count, names} (counts and names only);
#  - W/RZ2_PLAN.json: add 0, change 1, destroy 0, replace false, attribute instance_type;
#  - W/NEVER_WIDEN_ASK_OG-rz-2.md: three headed halves, a process-wide-state line, the downtime and the SAFE rollback order
#    (redeploy the live ref first, then t4g.small), 0 public IPv4 addresses, 0 runs of 9+ digits.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
python - "$W" <<'EOF'
import json, os, re, sys
W = sys.argv[1]
def load(n):
    try:
        return json.load(open(os.path.join(W, n), encoding="utf-8"))
    except Exception:
        return None
b, p = load("RZ2_BEFORE.json"), load("RZ2_PLAN.json")
keys = ("instance_id", "instance_type", "state", "az", "eip_attached", "public_ip_changes_on_stop_start", "target_health", "nrestarts",
        "unit_memory_high", "unit_memory_max", "memory_total_mb", "live_ref")
ok_b = bool(b) and all(k in b and b[k] is not None for k in keys) and isinstance((b.get("public_ip_surfaces") or {}).get("count"), int)
ok_p = bool(p) and p.get("add") == 0 and p.get("change") == 1 and p.get("destroy") == 0 and p.get("replace") is False and p.get("attribute") == "instance_type"
try:
    ask = open(os.path.join(W, "NEVER_WIDEN_ASK_OG-rz-2.md"), encoding="utf-8").read()
except Exception:
    ask = ""
halves = all(re.search(r"(?mi)^#{2,4}\s.*\b%s\b" % h, ask) for h in ("CTO", "COO", "CVO"))
pws = "process-wide state this change touches" in ask
low = ask.lower()
dt = ("downtime" in low or "down for" in low) and "t4g.small" in low and ("first" in low and "redeploy" in low)
ipv4 = len(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", ask))
digits = len(re.findall(r"\d{9,}", ask))
print("before-record: instance, type, state, EIP answer, public-IP-changes answer, target health, limits, memory total: %s" % ("yes" if ok_b else "no"))
print("plan: change %s add %s destroy %s replace %s attribute %s: %s" % ((p or {}).get("change"), (p or {}).get("add"), (p or {}).get("destroy"), (p or {}).get("replace"), (p or {}).get("attribute"), "yes" if ok_p else "no"))
print("ask: three halves %s; process-wide state line %s; downtime and safe rollback order named %s; public IPv4 addresses %d (want 0); runs of 9+ digits %d (want 0)" % ("yes" if halves else "no", "yes" if pws else "no", "yes" if dt else "no", ipv4, digits))
ok = ok_b and ok_p and halves and pws and dt and ipv4 == 0 and digits == 0
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
