"""AMGT_RESAPP round 77 -- AMGT-ba-25, the research-pull driver (segments, officers): built against FAKES, no vendor call.

  python r77_ba25.py --cell plan|stops|source

The driver is `integrations/bloomberg/research/research_pulls.py`. The contract this check reads:
  plan(kind, names=None) -> {"kind", "names": [yellow keys], "calls_per_name": int, "calls": int, "fields": [..]}
      kind is "segments" or "officers". With names=None the population is read from the stores. plan makes NO Bloomberg call.
  run(kind, names, blp, write, vehicle_ran, health) -> {"kind", "pulled": int, "failed": [..], "calls": int,
                                                        "stopped": None|"CAPACITY"|"VEHICLE_NOT_RUN"|"TERMINAL_DOWN"}
      blp.reference_data(securities, fields) is the only vendor entry; write(kind, security, stamp, body) lands one bronze body;
      vehicle_ran() -> bool and health() -> bool are injected reads. A capacity refusal is an exception of class
      research_pulls.CapacityRefused raised by the blp adapter, or a response whose error text carries "LIMIT" or "-4001".
  EXIT = {"OK": 0, "CAPACITY": 3, "VEHICLE_NOT_RUN": 4, "TERMINAL_DOWN": 5}

plan:   C1 plan("officers", names=N3) and plan("segments", names=N3) each return calls == len(names) * calls_per_name, 3 names,
        and a non-empty fields list; C2 importing the module and calling plan makes zero reference_data calls on a planted fake.
stops:  C1 run with vehicle_ran False returns stopped VEHICLE_NOT_RUN with 0 calls and 0 writes; C2 run with health False returns
        stopped TERMINAL_DOWN with 0 calls and 0 writes; C3 run over 5 names where the fake refuses capacity on the third call
        returns stopped CAPACITY, pulled 2, exactly 3 calls, 2 writes, and never calls again; C4 (the control) run over 3 names
        with a healthy fake pulls 3, writes 3, stopped None.
source: C1 the module's source names no sign-in script (bbg_signin, bbg_credentials) and no path under
        integrations/bloomberg/pipeline or integrations/bloomberg/auth.
Verdict: R77 BA25 <CELL>: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import importlib
import os
import subprocess
import sys

N3 = ["BA US Equity", "AMD US Equity", "ASML NA Equity"]
N5 = N3 + ["KMB US Equity", "COST US Equity"]


class FakeBlp:
    def __init__(self, refuse_on=None, mod=None):
        self.calls = 0
        self.refuse_on = refuse_on
        self.mod = mod

    def reference_data(self, securities, fields, **_kw):
        self.calls += 1
        if self.refuse_on and self.calls >= self.refuse_on:
            raise self.mod.CapacityRefused("planted: daily capacity reached (-4001 LIMIT)")
        return {s: {f: "planted" for f in fields} for s in securities}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("plan", "stops", "source"), required=True)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    sys.path.insert(0, root)
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    src = os.path.join(root, "integrations", "bloomberg", "research", "research_pulls.py")
    if not os.path.isfile(src):
        print(f"   no driver at {src}")
        clause("C0 the driver exists", False)
        return _verdict(a, ok)
    if a.cell == "source":
        text = open(src, encoding="utf-8").read()
        hits = [t for t in ("bbg_signin", "bbg_credentials", "bloomberg/pipeline", "bloomberg/auth", "bloomberg\\pipeline",
                            "bloomberg\\auth") if t in text]
        clause("C1 the driver names no sign-in script and nothing under pipeline/ or auth/", not hits, f"{hits}")
        return _verdict(a, ok)
    mod = importlib.import_module("integrations.bloomberg.research.research_pulls")
    if a.cell == "plan":
        fake = FakeBlp(mod=mod)
        shapes = []
        for kind in ("officers", "segments"):
            p = mod.plan(kind, names=list(N3))
            shapes.append((kind, len(p.get("names") or []), p.get("calls_per_name"), p.get("calls"), len(p.get("fields") or [])))
        print(f"   plans (kind, names, calls_per_name, calls, fields): {shapes}")
        clause("C1 each plan states names, calls per name and the product", all(
            n == 3 and isinstance(c, int) and c >= 1 and t == n * c and f >= 1 for _k, n, c, t, f in shapes))
        clause("C2 a plan makes no Bloomberg call", fake.calls == 0, f"{fake.calls} calls")
    else:
        def go(names, blp, vehicle=True, health=True):
            writes = []
            res = mod.run("officers", list(names), blp, lambda *args, **kw: writes.append(args),
                          vehicle_ran=lambda: vehicle, health=lambda: health)
            return res, len(writes)

        b = FakeBlp(mod=mod)
        res, w = go(N3, b, vehicle=False)
        clause("C1 refused before the vehicle has run: no call, no write",
               res.get("stopped") == "VEHICLE_NOT_RUN" and b.calls == 0 and w == 0, f"{res.get('stopped')} calls {b.calls} writes {w}")
        b = FakeBlp(mod=mod)
        res, w = go(N3, b, health=False)
        clause("C2 a signed-out Terminal pulls nothing", res.get("stopped") == "TERMINAL_DOWN" and b.calls == 0 and w == 0,
               f"{res.get('stopped')} calls {b.calls} writes {w}")
        b = FakeBlp(refuse_on=3, mod=mod)
        res, w = go(N5, b)
        clause("C3 a capacity refusal stops the sequence and is not retried",
               res.get("stopped") == "CAPACITY" and res.get("pulled") == 2 and b.calls == 3 and w == 2,
               f"{res.get('stopped')} pulled {res.get('pulled')} calls {b.calls} writes {w}")
        b = FakeBlp(mod=mod)
        res, w = go(N3, b)
        clause("C4 control: a healthy run pulls and writes every name", res.get("stopped") is None and res.get("pulled") == 3
               and w == 3, f"{res.get('stopped')} pulled {res.get('pulled')} writes {w}")
        want = {"OK": 0, "CAPACITY": 3, "VEHICLE_NOT_RUN": 4, "TERMINAL_DOWN": 5}
        clause("C5 the exit codes are the stated ones", getattr(mod, "EXIT", None) == want, f"{getattr(mod, 'EXIT', None)}")
    return _verdict(a, ok)


def _verdict(a, ok):
    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R77 BA25 {a.cell.upper()}: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
