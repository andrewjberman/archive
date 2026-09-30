"""DSGN_AMGTV1 round 13, AV-l-1's grant: set the 10 keyed routes of the portal's ui-contract fixture set to the round-13 LIVE
captures' payloads, verbatim (issuer 2.0.0_SA_COO~D; the method measured on the cut's green arm r13-green-a).

Usage (repo root, i.e. the worktree top): python <this file>
Reads org/.../round13/fixtures/*.json (each a {_capture_note, payload} wrapper) and rewrites
portal/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json with json.dump(indent=1, ensure_ascii=False).
"""
import json
import os

ROOT = os.getcwd()
FIX = os.path.join(ROOT, "portal/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json")
CAP = os.path.join(ROOT, "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/fixtures")
P = "/api/scoped/amgt"
MAP = {
    P + "/security/BA_US_Equity/thesis": "thesisBundle.BA_US_Equity.json",
    P + "/security/BA_US_Equity/overlay": "overlay.BA_US_Equity.json",
    P + "/security/BA_US_Equity/peers": "peers.BA_US_Equity.json",
    P + "/security/BA_US_Equity/versions": "versions.BA_US_Equity.json",
    P + "/security/BA_US_Equity/compare": "compare.BA_US_Equity.oldest-latest.json",
    P + "/security/BA_US_Equity/ledger": "ledger.BA_US_Equity.json",
    P + "/security/BA_US_Equity/timeline": "timeline.BA_US_Equity.json",
    P + "/watchlist": "watchlist.json",
    P + "/lead-panel/rankings/trending/chatter": "rankings.trending.chatter.json",
    P + "/lead-panel/timeseries/trending/chatter": "timeseries.trending.chatter.json",
}


def unwrap(x):
    if isinstance(x, dict) and x.get("payload") is not None and (x.get("_capture_note") or x.get("_capture")):
        return x["payload"]
    return x


def main():
    with open(FIX, "r", encoding="utf-8") as f:
        fix = json.load(f)
    before = len(fix)
    for key, name in MAP.items():
        with open(os.path.join(CAP, name), "r", encoding="utf-8") as f:
            fix[key] = unwrap(json.load(f))
    with open(FIX, "w", encoding="utf-8", newline="\n") as f:
        json.dump(fix, f, indent=1, ensure_ascii=False)
    print("OK: keys before %d after %d set %d" % (before, len(fix), len(MAP)))


if __name__ == "__main__":
    main()
