"""AMGT_RESAPP round 78 -- AMGT-bb-2: ONE statement of inputs per name (round-77 ruling 4, FWD-12; row Z-W286-S2).

  --crit AC1|AC2|AC3 --where local

AC1 (build): `lib.research.api.inputs_statement.statement(input_provenance, thesis)` on planted rows:
    C1 a name whose page uses a filing: the four input rows are copied unchanged and in order, and ONE `filings` row sits
       before `pack` with outcome "landed", the form and filing date, `used_for` naming all five uses, and a reason
       that names the form and the date;
    C2 a name whose page uses no filing: the filings row reads outcome "never read", no date, and a plain reason;
    C3 `thesis` None (the parts could not be read): outcome "failed" with a plain reason, never "never read";
    C4 no served sentence (reason, source, used_for) carries a system word.
AC2 (seam, the real neighbour): the function's own handler, run locally on BA_US_Equity and AMD_US_Equity, supplies the
    real /overlay `input_provenance` and the real /thesis body; the statement reads "landed" with a form on BA (whose
    thesis cites a filing) and "never read" on AMD (whose thesis cites none), and the four existing rows are unchanged.
AC3 (bound): the existing tests of the four-row builder still pass (lib/research/api/tests/test_top_band_provenance.py).
Verdict: R78 BB2 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

BOUND_TEST = "lib/research/api/tests/test_top_band_provenance.py"
PREFIX = "/api/scoped/amgt"
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")

ROWS = [
    {"input": "bloomberg", "source": "Bloomberg data pulls stored for this name", "last_run": "20261006T132334Z",
     "outcome": "landed", "reason": "the newest read of this input for this name is dated 20261006T132334Z"},
    {"input": "seekingalpha", "source": "Seeking Alpha articles and reports stored for this name", "last_run": "NEVER",
     "outcome": "never read", "reason": "nothing has been read from this input for this name yet"},
    {"input": "serp", "source": "web search results stored for this name", "last_run": "NEVER",
     "outcome": "never read", "reason": "nothing has been read from this input for this name yet"},
    {"input": "pack", "source": "the research pack built for this name", "last_run": "20261006T132342Z",
     "outcome": "landed", "reason": "the newest read of this input for this name is dated 20261006T132342Z"},
]
SOURCE = {"form": "10-K", "filing_date": "2026-01-30", "accession": "000162828026004357"}
USED = {
    "passage_coverage": {"sections": [{"key": "risk", "passages": 94}], "source": dict(SOURCE), "reason": None},
    "drafting_provenance": dict(SOURCE),
    "drafted_sections": [{"section_id": "company_description", "sentences": [{"text": "x"}]}],
    "segment_breakdown": {"rows": [{"segment": "Commercial Airplanes", "text": "t", "cite": "c"}], "source": dict(SOURCE)},
    "thesis_driver_chart": {"status": "SERVED", "source": "filing", "points": [{"period": "2023", "value": 528}]},
    "management": {"officers": [{"name": "A", "source": "filing"}, {"name": "B", "source": "bloomberg"}]},
}
UNUSED = {
    "passage_coverage": {"sections": [], "source": None, "reason": "No filing analysis is stored for this name yet"},
    "drafting_provenance": None,
    "drafted_sections": [],
    "segment_breakdown": {"rows": [], "source": None, "reason": "none"},
    "thesis_driver_chart": {"status": "ABSENT", "source": None, "points": []},
    "management": {"officers": [{"name": "B", "source": "bloomberg"}]},
}


def _sentences(row):
    out = [str(row.get("reason") or ""), str(row.get("source") or "")]
    out.extend(str(u) for u in (row.get("used_for") or []))
    return out


def _filings(rows):
    hits = [r for r in rows if isinstance(r, dict) and r.get("input") == "filings"]
    return hits[0] if len(hits) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        if not os.path.isfile(BOUND_TEST):
            clause("C1 the bound test file exists", False, BOUND_TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", BOUND_TEST],
                           capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 the four-row builder's tests pass", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.api import inputs_statement
    except ImportError as err:
        clause("C0 lib.research.api.inputs_statement imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(inputs_statement, "statement", None)
    if not callable(fn):
        clause("C0 inputs_statement.statement exists", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        before = json.dumps(ROWS, sort_keys=True)
        used = fn([dict(r) for r in ROWS], USED)
        names = [r.get("input") for r in used]
        row = _filings(used) or {}
        kept = [r for r in used if r.get("input") != "filings"]
        print(f"   used: order {names}; filings outcome {row.get('outcome')!r} form {row.get('form')!r} "
              f"filing_date {row.get('filing_date')!r} used_for {row.get('used_for')!r}")
        print(f"   reason: {row.get('reason')!r}")
        clause("C1 a page that uses a filing says so, once, before the pack row",
               names == ["bloomberg", "seekingalpha", "serp", "filings", "pack"]
               and json.dumps(kept, sort_keys=True) == before and row.get("outcome") == "landed"
               and row.get("form") == "10-K" and row.get("filing_date") == "2026-01-30" and row.get("last_run") == "2026-01-30"
               and len(row.get("used_for") or []) == 5 and "10-K" in str(row.get("reason")) and "2026-01-30" in str(row.get("reason")))
        none = _filings(fn([dict(r) for r in ROWS], UNUSED)) or {}
        print(f"   unused: outcome {none.get('outcome')!r} last_run {none.get('last_run')!r} reason {none.get('reason')!r}")
        clause("C2 a page that uses no filing reads never read, with a plain reason",
               none.get("outcome") == "never read" and none.get("last_run") is None and not (none.get("used_for") or [])
               and isinstance(none.get("reason"), str) and none["reason"].strip())
        failed = _filings(fn([dict(r) for r in ROWS], None)) or {}
        print(f"   unread: outcome {failed.get('outcome')!r} reason {failed.get('reason')!r}")
        clause("C3 parts that could not be read say failed, never never read",
               failed.get("outcome") == "failed" and isinstance(failed.get("reason"), str) and failed["reason"].strip())
        bad = []
        for r in (row, none, failed):
            for text in _sentences(r):
                bad.extend(w for w in BANNED if w in text.lower())
        clause("C4 no served sentence carries a system word", row and none and failed and not bad, f"found {sorted(set(bad))}")
        return verdict(a, ok)

    from lib.research.api import scoped_amgt

    def body(key, leaf):
        event = {"rawPath": f"{PREFIX}/security/{key}/{leaf}", "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        r = scoped_amgt.handler(event)
        return r.get("statusCode"), json.loads(r.get("body") or "{}")

    got = {}
    for key in ("BA_US_Equity", "AMD_US_Equity"):
        c1, overlay = body(key, "overlay")
        c2, thesis = body(key, "thesis")
        rows = [r for r in (overlay.get("input_provenance") or []) if r.get("input") != "filings"]
        out = fn([dict(r) for r in rows], thesis)
        row = _filings(out) or {}
        got[key] = (c1, c2, rows, out, row)
        print(f"   {key}: overlay {c1} thesis {c2}; rows in {len(rows)}; out {[r.get('input') for r in out]}; "
              f"filings {row.get('outcome')!r} {row.get('form')!r} {row.get('filing_date')!r} used_for {row.get('used_for')!r}")
    ba, amd = got["BA_US_Equity"], got["AMD_US_Equity"]
    clause("C1 BA US, whose thesis cites a filing, reads landed with its form and date",
           ba[0] == 200 and ba[1] == 200 and ba[4].get("outcome") == "landed" and bool(ba[4].get("form"))
           and bool(ba[4].get("filing_date")) and len(ba[4].get("used_for") or []) >= 1)
    clause("C2 AMD US, whose thesis cites none, reads never read", amd[0] == 200 and amd[1] == 200 and amd[4].get("outcome") == "never read")
    same = all(json.dumps([r for r in g[3] if r.get("input") != "filings"], sort_keys=True) == json.dumps(g[2], sort_keys=True)
               and len(g[2]) == 4 for g in (ba, amd))
    clause("C3 the four existing rows are unchanged on both names", same)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB2 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
