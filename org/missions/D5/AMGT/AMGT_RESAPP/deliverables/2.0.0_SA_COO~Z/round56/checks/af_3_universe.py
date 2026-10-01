"""AMGT_RESAPP round 56 -- AMGT-af-3 AC2: the price producer's universe is the covered names.

No Bloomberg call. Imports integrations/bloomberg/research/price_axis_pull.py and calls
`load_covered_universe()` (the function af-3 adds), then grades it against the covered universe read
fresh HERE (lib/research/coverage/covered_universe.py):

  - `denominator` equals the fresh covered count, and `source` names research_dossier;
  - every covered key is accounted for exactly once: mapped to a ticker, or listed in `unmapped`
    with a non-empty `reason`;
  - each mapped ticker equals the identity crosswalk's own `bloomberg` form for that key (the
    overlay's resolver, lib.research.api.scoped_amgt.resolve_identity), never a string transform;
  - the old 34-name file is no longer the default: `main()`'s default universe is not UNIVERSE_PATH.

Verdict: THE PRICE PRODUCER RANKS OVER THE COVERED NAMES: YES|NO
"""
from __future__ import annotations

import inspect
import sys


def main():
    from lib.research.coverage.covered_universe import covered_security_keys
    from lib.research.api import scoped_amgt as s

    covered = covered_security_keys()
    print(f"oracle: covered names {len(covered)} (fresh read of research_dossier/)")
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    sys.path.insert(0, "integrations/bloomberg/research")
    import importlib

    pap = importlib.import_module("integrations.bloomberg.research.price_axis_pull")
    fn = getattr(pap, "load_covered_universe", None)
    clause("C1 load_covered_universe exists", callable(fn))
    if not callable(fn):
        print("THE PRICE PRODUCER RANKS OVER THE COVERED NAMES: NO")
        return 1
    u = fn()
    tickers = u.get("tickers") or []
    mapped = u.get("mapped") or {}
    unmapped = u.get("unmapped") or []
    clause("C2 denominator equals the fresh covered count; source names research_dossier",
           u.get("denominator") == len(covered) and "research_dossier" in str(u.get("source", "")),
           f"denominator={u.get('denominator')} source={u.get('source')}")
    keys_mapped = sorted(mapped)
    keys_unmapped = sorted(x.get("security_key") for x in unmapped)
    clause("C3 every covered key accounted for exactly once",
           sorted(keys_mapped + keys_unmapped) == covered and sorted(set(tickers)) == sorted(set(mapped.values()))
           and all(str(x.get("reason") or "").strip() for x in unmapped),
           f"mapped {len(keys_mapped)} + unmapped {len(keys_unmapped)} vs covered {len(covered)}; tickers {len(tickers)}")
    wrong = []
    for k, t in mapped.items():
        b = (s.resolve_identity(k) or {}).get("bloomberg")
        if b != t:
            wrong.append((k, t, b))
    clause("C4 each mapped ticker is the crosswalk's bloomberg form", not wrong, f"wrong {len(wrong)} {wrong[:3]}")
    src = inspect.getsource(pap.main)
    clause("C5 main() no longer defaults to the 34-name UNIVERSE_PATH",
           "default=UNIVERSE_PATH" not in src.replace(" ", "") and "load_universe(args.universe)" not in src, "")
    verdict = all(ok)
    print(f"THE PRICE PRODUCER RANKS OVER THE COVERED NAMES: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
