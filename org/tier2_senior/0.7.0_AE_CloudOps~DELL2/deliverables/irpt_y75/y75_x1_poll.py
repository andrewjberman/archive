"""Y75 read 4, second half: re-POST the SAME upload token until a terminal state.

The order: every 30 s for up to 15 minutes, until NORMALIZED or NEEDS_CORRECTION. Either terminal
state counts; still RESOLVING at 15 minutes also counts and is recorded as RESOLVING-TIMEOUT.
A re-POST of the same token READS the row's state and never sends a second resolve message
(intake/uploads.py:311-312, upload_resolution.py:1-48), so this loop adds no work to the resident.
"""
import io
import json
import sys
import time

sys.path.insert(0, "org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y75")
import y75_x1_arms as X  # noqa: E402

TOKEN = "y75x1-20261009-admit"
TERMINAL = ("NORMALIZED", "NEEDS_CORRECTION")
OUT = ("C:/Users/Test/AppData/Local/Temp/claude/C--dev-ajb-workspace/"
       "32a60855-c63b-4e98-b745-fa87f5d02864/scratchpad/y75_x1_poll.json")


def main():
    advisor = X.resolve_by_opaque("adv-04b85b8aefda", X.FIRM)
    if advisor is None:
        print("REFUSED: advisor opaque id no longer resolves")
        return 1
    deadline = time.time() + 15 * 60
    seen = []
    state = None
    while time.time() < deadline:
        _sc, _fe, _http, ans = X.invoke(X.event(advisor_email=advisor, token=TOKEN))
        data = ans.get("data") if isinstance(ans, dict) else None
        state = (data or {}).get("state") if isinstance(data, dict) else None
        if state is None and isinstance(ans, dict):
            state = (ans.get("status") or {}).get("public_reason_code")
        stamp = time.strftime("%H:%M:%SZ", time.gmtime())
        if not seen or seen[-1]["state"] != state:
            print("  %s state=%s" % (stamp, state))
        seen.append({"at": stamp, "state": state,
                     "input_id": (data or {}).get("input_id") if isinstance(data, dict) else None})
        if state in TERMINAL:
            break
        time.sleep(30)
    final = state if state in TERMINAL else "RESOLVING-TIMEOUT"
    last = seen[-1] if seen else {}
    rec = {"token": TOKEN, "polls": len(seen), "admit_final_state": final,
           "last_input_id": last.get("input_id"), "transitions": seen}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
    print("admit_final_state:", final, "| polls:", len(seen), "| input_id:", last.get("input_id"))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
