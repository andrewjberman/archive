"""IRPT_ANLREQ TO-RUN-FWD1 window 3, step 5 (0.7.0_AE_CloudOps~AQ2): build run 3's holdings file and decisions file from the probe.

  python build_inputs_run3.py <probe_results.json> <new-folder-outside-the-repo>

Applies the signed selection (already computed by probe_run3.py: U1 Yes, U2 No, U3 Replace with VNQ; a U-row with no qualifying candidate is
UNEXERCISED and the run files without it, never substituted). Writes fwd1_holdings_49financial_r3.csv (header, SPY,100,26000000, AGG,200,32000000,
TIMXX,50,5000000, then one row <U>,50,5000000 per selected U-row, at most six data rows) and fwd1_decisions_r3.json, prints both sha256, and runs
the driver's own validator readDecisionsFile on the decisions file (a refusal exits 3: nothing run-minted). Writes nothing to AWS.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

DRIVER = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs"
FIXED = ["SPY,100,26000000", "AGG,200,32000000", "TIMXX,50,5000000"]
REPLACEMENT = "VNQ"


def build(selection):
    rows = list(FIXED) + ["%s,50,5000000" % selection[k] for k in ("U1", "U2", "U3") if selection.get(k)]
    csv = ("Ticker,Dollars,Acct Market Value\n" + "\n".join(rows) + "\n").encode("ascii")
    decisions = []
    if selection.get("U1"):
        decisions.append({"symbol": selection["U1"], "answer": "yes"})
    if selection.get("U2"):
        decisions.append({"symbol": selection["U2"], "answer": "no"})
    if selection.get("U3"):
        decisions.append({"symbol": selection["U3"], "answer": "replace", "replacement": REPLACEMENT})
    return csv, json.dumps({"decisions": decisions}, indent=1).encode("ascii"), len(rows)


def selftest():
    csv, dec, n = build({"U1": "AAA", "U2": "BBB", "U3": "CCC"})
    assert n == 6 and csv.startswith(b"Ticker,Dollars,Acct Market Value\nSPY,100,26000000\n") and csv.endswith(b"CCC,50,5000000\n")
    assert [d["answer"] for d in json.loads(dec)["decisions"]] == ["yes", "no", "replace"] and json.loads(dec)["decisions"][2]["replacement"] == "VNQ"
    csv, dec, n = build({"U1": "AAA", "U2": None, "U3": None})
    assert n == 4 and len(json.loads(dec)["decisions"]) == 1
    csv, dec, n = build({"U1": None, "U2": None, "U3": None})
    assert n == 3 and json.loads(dec) == {"decisions": []}
    print("SELFTEST-OK build_inputs: full (6 rows), one U-row (4 rows), none (3 rows, empty decisions)")
    return 0


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest()
    probe, out = Path(argv[0]), Path(argv[1])
    sel = json.loads(probe.read_text(encoding="utf-8"))["selection"]
    csv, dec, n = build(sel)
    out.mkdir(parents=True, exist_ok=True)
    (out / "fwd1_holdings_49financial_r3.csv").write_bytes(csv)
    (out / "fwd1_decisions_r3.json").write_bytes(dec)
    print("selection %s" % json.dumps(sel))
    print("holdings fwd1_holdings_49financial_r3.csv data rows %d sha256 %s" % (n, hashlib.sha256(csv).hexdigest()))
    print("decisions fwd1_decisions_r3.json sha256 %s" % hashlib.sha256(dec).hexdigest())
    js = "import('file:///%s').then(m=>{const r=m.readDecisionsFile(process.argv[1]);console.log(r.error?'REFUSED: '+r.error:'VALIDATOR-OK '+r.decisions.length+' decisions');process.exit(r.error?3:0)})" % str(Path(DRIVER).resolve()).replace("\\", "/")
    r = subprocess.run(["node", "-e", js, str(out / "fwd1_decisions_r3.json")], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[:300])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
