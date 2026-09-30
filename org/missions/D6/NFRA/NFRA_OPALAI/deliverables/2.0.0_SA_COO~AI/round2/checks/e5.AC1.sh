#!/usr/bin/env bash
# OA-e-5 AC1 (the measurement, with its denominator): the re-measure file exists and its counts add up --
# reads_attempted = ok + failed + token_expired, the failure signatures sum to failed, at least one read ran on a LIVE
# token, and the verdict is the one the counts imply (CLEARED iff failed=0 and ok>=1; NOT-CLEARED iff failed>0;
# INCONCLUSIVE iff no read ran on a live token).
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~14/E5_TEAMS_WATCH_REMEASURE.json"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
timeout 30 python - "$F" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    att, ok, fl, ex = (int(d[k]) for k in ("reads_attempted", "reads_ok", "reads_failed", "reads_token_expired"))
    sigs = d.get("failure_signatures") or {}
    sig_sum = sum(int(v) for v in sigs.values())
    chats = int(d.get("chats", 0)); verdict = d.get("verdict", ""); ident = d.get("identity", "")
except Exception as e:
    print(f"file unparseable: {type(e).__name__}: {e}"); print("RESULT: FAIL"); sys.exit(1)
want = "INCONCLUSIVE" if ok + fl == 0 else ("NOT-CLEARED" if fl > 0 else "CLEARED")
print(f"reads attempted={att} ok={ok} failed={fl} token_expired={ex} (sum ok={att == ok + fl + ex}); "
      f"signatures sum={sig_sum} vs failed={fl}; chats={chats}; identity set={'yes' if ident else 'no'}; "
      f"verdict={verdict} implied={want}")
good = att >= 1 and att == ok + fl + ex and sig_sum == fl and chats >= 1 and ident and (ok + fl) >= 1 and verdict == want
print("RESULT: PASS" if good else "RESULT: FAIL"); sys.exit(0 if good else 1)
EOF
