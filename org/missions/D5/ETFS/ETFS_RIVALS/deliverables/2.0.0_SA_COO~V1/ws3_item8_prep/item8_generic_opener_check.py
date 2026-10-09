"""WS3 item 8 -- a Direction Verdict that opens with the generic lead is sent back once; a specific opening is not.

    python item8_generic_opener_check.py      (run from the repository root)

Drives `ai_accounts.run_chain` with a scripted client on a one-fund fixture (no vendor call).
ARM A: the verdict opens "The last thirty days mostly add to, rather than contradict, the longer trend" (the lead 13 of
19 verdicts shared on the 2026-10-08 page). The chain must send ONE correction for the direction item that quotes that
opening, keep the corrected reply, and not set grounding FAIL for the opening.
ARM C: the verdict opens "From <date> to <date>, the long-run trend is only partly borne out ..." (the lead the
live prompt a1-chain/7 produced on 2026-10-09 for CGIC and IDVZ). Sent back and replaced, as ARM A.
ARM B (control): the verdict opens with a named security. No correction is sent for it.
Exit 0 = PASS, 1 = FAIL.
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "data", "etfs", "scripts"))
from rivalfunds import ai_accounts as A  # noqa: E402

DAY = "2026-10-08"
g5 = pd.DataFrame([
    {"fund_id": "TST", "security_key": "AAA_US", "action": "buy", "window_end": "2026-10-06", "est_notional_base": 5_000_000.0},
    {"fund_id": "TST", "security_key": "CCC_US", "action": "sell", "window_end": "2026-10-07", "est_notional_base": -3_000_000.0},
])
empty = pd.DataFrame(columns=["fund_id"])
FACTS = A.fact_pack("TST", DAY, g5, empty, empty, empty, names={"AAA_US": "Alpha Co", "CCC_US": "Gamma Co"})
WINS = A.period_windows(DAY, FACTS)
W30, W365 = WINS.get("R30"), WINS.get("R365")
GENERIC = "The last thirty days mostly add to, rather than contradict, the longer trend."
DATED = "From 2025-10-07 to 2026-10-07, the long-run trend is only partly borne out by the last 30 days."
SPECIFIC = "Alpha Co is the manager's clearest conviction: it was bought while Gamma Co was cut."


def reply(lead, win):
    dates = f" The period runs from {win[0]} to {win[1]}." if win else ""
    return json.dumps({"text": lead + dates + " The record is short.", "observed": ["Alpha Co was bought."],
                       "inferred": ["The manager favours Alpha Co."], "cited": [], "invalidation": "A sale of Alpha Co."})


class Scripted:
    def __init__(self, lead):
        self.lead, self.calls = lead, []

    def chat(self, messages, model):
        last = str(messages[-1]["content"])
        self.calls.append(last)
        if "activity_30d]" in last:
            return reply("Alpha Co was the largest purchase of the last 30 days.", W30)
        if "direction_verdict]" in last:
            return reply(self.lead, W365)
        return reply(SPECIFIC, W365)  # any correction turn returns the specific opening

    def web_search(self, query, model):
        return {"text": "", "urls": []}


def run(lead):
    c = Scripted(lead)
    rows = A.run_chain("TST", "rival", DAY, FACTS, [], c, "chk", model="scripted")
    d = [r for r in rows if r["kind"] == "direction_verdict"][0]
    corr = [m for m in c.calls if "Your reply has these defects" in m]
    return d, corr


fails = []
d, corr = run(GENERIC)
print(f"ARM A: corrections sent {len(corr)}; final text starts: {d['text'][:60]!r}; grounding {d['grounding']} "
      f"({d['grounding_reason'] or '-'})")
if not any("the last thirty days mostly add to" in m.lower() for m in corr):
    fails.append("A: no correction quoting the generic opening was sent")
if not d["text"].startswith("Alpha Co"):
    fails.append("A: the corrected reply did not replace the generic one")
if "open" in str(d["grounding_reason"] or "").lower():
    fails.append("A: the opening set a grounding reason (it must be corrected, never failed)")
d, corr = run(DATED)
print(f"ARM C: corrections sent {len(corr)}; final text starts: {d['text'][:60]!r}")
if not corr or not d["text"].startswith("Alpha Co"):
    fails.append("C: an opening that leads with the period's dates was not sent back and replaced")
d, corr = run(SPECIFIC)
print(f"ARM B (control): corrections sent {len(corr)}; final text starts: {d['text'][:60]!r}")
if corr:
    fails.append(f"B: a specific opening drew {len(corr)} correction(s)")
for f in fails:
    print("FAIL:", f)
print(f"ITEM8 RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
