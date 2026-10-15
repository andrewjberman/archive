#!/usr/bin/env bash
# OPLGTW OG-sa-1 AC1 (round-37 G1-FIX, FWD-22, PRD v3.8): Seeking Alpha access was READ before anything was changed.
# W/SA1_ACCESS.json = {"read_at": <iso>, "source": <what was read>, "http_status": <int|null>, "runner_profile_login": <bool>, "reason": <str>, "outcome": "ACCESS_HOLDS"|"ACCESS_REFUSED"} (A1: HOLDS iff 2xx AND runner_profile_login).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZW/SA1_ACCESS.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$F" <<'PY'
import json, sys, re
d = json.load(open(sys.argv[1], encoding="utf-8"))
ok_keys = all(k in d for k in ("read_at", "source", "http_status", "outcome"))
ok_out = d.get("outcome") in ("ACCESS_HOLDS", "ACCESS_REFUSED")
hs = d.get("http_status")
two_xx = isinstance(hs, int) and 200 <= hs < 300
ok_cons = (d.get("outcome") == "ACCESS_HOLDS") == (two_xx and d.get("runner_profile_login") is True) and isinstance(d.get("runner_profile_login"), bool) and bool(d.get("reason"))
ok_src = isinstance(d.get("source"), str) and len(d["source"]) > 8
ok_ts = bool(re.match(r"2026-10-1[4-9]T", str(d.get("read_at"))))
print("access read: status %s, outcome %s, source named %s, read_at in the order window %s, outcome consistent with status %s" % (d.get("http_status") if d.get("http_status") is not None else "none", d.get("outcome"), "yes" if ok_src else "no", "yes" if ok_ts else "no", "yes" if ok_cons else "no"))
sys.exit(0 if (ok_keys and ok_out and ok_cons and ok_src and ok_ts) else 1)
PY
); rc=$?
printf '%s\n' "$res" | tr -d '\r'
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
