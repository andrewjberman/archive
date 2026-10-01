"""HVST-ag-2 AC2 (issuer, read-only): a CHALLENGED pass recorded by an input-source instrument (FWD-11; row W91-S8).

Reads `~90/ag2_challenged_pass.json`:
{"instrument": "<name>", "window_start", "window_end", "hardware_input_events": int, "injected_input_events": int,
 "publishers": {"<pub>": {"challenge_met": <signature or "none">, "path": <solver>, "passed": bool,
                          "solved_at": <iso>}}}

PASS requires:
- an instrument that classes each OS input event as hardware or injected (e.g. a low-level hook reading LLMHF_INJECTED /
  LLKHF_INJECTED), named in `instrument`;
- `hardware_input_events` == 0 over the whole window (no human hand), the window covering every `solved_at`;
- at least one publisher of ('ft', 'sa') with `challenge_met` not "none", `passed` true and a named `path`;
- every one of ('ft', 'sa') present in the record (an unmet challenge is recorded "none", honestly).
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~90/ag2_challenged_pass.json")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no challenged-pass record")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    ws, we = str(r.get("window_start")), str(r.get("window_end"))
    print("INSTRUMENT: %s; window %s .. %s; hardware %s, injected %s"
          % (r.get("instrument"), ws, we, r.get("hardware_input_events"), r.get("injected_input_events")))
    if not r.get("instrument"):
        failures.append("no instrument named")
    if r.get("hardware_input_events") != 0:
        failures.append("hardware input events %r (expected 0)" % r.get("hardware_input_events"))
    challenged = []
    wanted = ('ft', 'sa')
    for pub in wanted:
        if pub not in (r.get("publishers") or {}):
            failures.append("%s missing from the record" % pub)
    for pub, p in (r.get("publishers") or {}).items():
        if pub not in wanted:
            continue
        print("  %-8s challenge=%s path=%s passed=%s solved_at=%s" % (pub, p.get("challenge_met"), p.get("path"),
                                                                    p.get("passed"), p.get("solved_at")))
        if str(p.get("challenge_met")) not in ("none", "None", "") and p.get("passed") is True and p.get("path"):
            challenged.append(pub)
            if not (ws <= str(p.get("solved_at")) <= we):
                failures.append("%s solved outside the instrument window" % pub)
    if not challenged:
        failures.append("no publisher met a challenge and passed it")
    print("CHALLENGED PASSES: %d (%s)" % (len(challenged), ", ".join(challenged)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
