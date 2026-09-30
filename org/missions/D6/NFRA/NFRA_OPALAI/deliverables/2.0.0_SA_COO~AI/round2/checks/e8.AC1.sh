#!/usr/bin/env bash
# OA-e-8 AC1 (the stage table, OPAL_ANALYST PRD s.11.1 method): >=1 real exchange; each exchange's total equals its two
# Graph clocks (answer createdDateTime - question createdDateTime, +-1 s); all five stages A_DETECTION, B_WAKE,
# C_TURN_OVERHEAD, D_RESEARCH, E_COMPOSE_SEND are present, each either measured (seconds >= 0 plus a named instrument)
# or UNMEASURED with a reason; at least 3 of 5 are measured; and the measured stages sum to no more than the total + 2 s.
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~12/E8_SPEED_STAGES.json"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
timeout 30 python - "$F" <<'EOF'
import json, sys, datetime
ST = ("A_DETECTION", "B_WAKE", "C_TURN_OVERHEAD", "D_RESEARCH", "E_COMPOSE_SEND")
def ts(s): return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
try:
    ex = json.load(open(sys.argv[1], encoding="utf-8"))["exchanges"]
    good_n, notes = 0, []
    for i, e in enumerate(ex):
        tot = float(e["total_seconds"]); clk = ts(e["answer_created"]) - ts(e["question_created"])
        st = e["stages"]; meas = 0; s = 0.0; shape = True
        for k in ST:
            v = st.get(k)
            if isinstance(v, dict) and "seconds" in v and float(v["seconds"]) >= 0 and v.get("instrument"):
                meas += 1; s += float(v["seconds"])
            elif isinstance(v, dict) and v.get("unmeasured"):
                pass
            else:
                shape = False
        ok = abs(tot - clk) <= 1 and shape and meas >= 3 and s <= tot + 2
        good_n += ok
        notes.append(f"#{i+1} total={tot:.0f}s clocks={clk:.0f}s measured={meas}/5 sum={s:.0f}s {'ok' if ok else 'BAD'}")
except Exception as e:
    print(f"file unparseable: {type(e).__name__}: {e}"); print("RESULT: FAIL"); sys.exit(1)
print(f"exchanges={len(ex)} well-formed={good_n}; " + "; ".join(notes))
good = len(ex) >= 1 and good_n == len(ex)
print("RESULT: PASS" if good else "RESULT: FAIL"); sys.exit(0 if good else 1)
EOF
