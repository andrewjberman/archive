"""HVST-aj-6 AC2 (issuer, read-only): ONE real, unattended ft sign-in whose hCaptcha the NopeCHA BROWSER EXTENSION solved
(CTO 28484; RE-POINTED on Andrew-direct ~16:47Z, open-calls option A; the Ocilar hcaptcha service is not live; row Z-W92-S18:
the NopeCHA Token API is discontinued).

Reads `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/aj6_signin_ext.json`. PASS requires:
- `solved_by` == "nopecha_extension" and `nopecha_token_api_calls` == 0;
- `kimi_vision_calls` == 0 and `hardware_input` == "none";
- `identity_cookie_names` contains "FTSession_s" (the ft identity cookie) and `saved_to_vault` is true;
- `challenge_events` holds a challenge_presented and a challenge_passed (ruling 8b), in that order.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
F = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/aj6_signin_ext.json")


def main():
    failures = []
    if not os.path.exists(F):
        print("RECORD: absent (%s)" % F)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no aj-6 sign-in record")
        return 1
    with open(F, encoding="utf-8") as fh:
        d = json.load(fh)
    print("SIGNIN solved_by=%s token_api_calls=%s kimi_vision_calls=%s hardware_input=%s saved=%s cookies=%s" % (
        d.get("solved_by"), d.get("nopecha_token_api_calls"), d.get("kimi_vision_calls"), d.get("hardware_input"),
        d.get("saved_to_vault"), d.get("identity_cookie_names")))
    if d.get("solved_by") != "nopecha_extension":
        failures.append("solved_by %s, want nopecha_extension" % d.get("solved_by"))
    if d.get("nopecha_token_api_calls") != 0:
        failures.append("nopecha_token_api_calls %s, want 0" % d.get("nopecha_token_api_calls"))
    if d.get("kimi_vision_calls") != 0:
        failures.append("kimi_vision_calls %s, want 0" % d.get("kimi_vision_calls"))
    if d.get("hardware_input") != "none":
        failures.append("hardware_input %s, want none" % d.get("hardware_input"))
    if "FTSession_s" not in (d.get("identity_cookie_names") or []) or d.get("saved_to_vault") is not True:
        failures.append("no FTSession_s identity cookie saved to the vault")
    evs = [e.get("event") for e in (d.get("challenge_events") or [])]
    print("CHALLENGE EVENTS %s" % evs)
    if "challenge_presented" not in evs or "challenge_passed" not in evs \
            or evs.index("challenge_presented") > evs.index("challenge_passed"):
        failures.append("challenge events lack presented-then-passed")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
