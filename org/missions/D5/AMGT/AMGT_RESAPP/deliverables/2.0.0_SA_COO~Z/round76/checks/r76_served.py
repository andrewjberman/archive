"""AMGT_RESAPP round 76 -- the CTO's round-75 analysis @326aea63b3, section 4 (PRD v0.40).

  --cell c62|c63|c64|c65 --where local|deployed [--bar N]

c62 (FWD-16 news half, ruling 2): every covered name's /security/<key>/overlay serves `top_band` with C1 `description_line`, one
    line (no newline, 300 characters or fewer) or a plain `description_reason`; C2 `items`, each with a non-empty `url`, `title` and
    `published_utc`, ordered most-discussed first (`mentions` descending), then newest; C3 `social` reads exactly
    "no social source is admitted yet".
c63 (FWD-12 provenance half, ruling 3): every covered name's /overlay serves `input_provenance`, one entry per input (the
    /freshness vendor inputs plus "pack"), each with `input`, `source`, `last_run` and `outcome`; C1 every entry's `last_run` equals
    that name's /freshness row value for the input (`per_input[<input>]`, or `pack`).
c64 (ruling 4, the triage): C1 every OPEN remediation row the project's census lists (comp-surprise --project AMGT_RESAPP) has a
    citing INVESTIGATION row whose `one_line` begins "TRIAGE <its id>:".
c65 (ruling 5, local plane): in a FRESH process, `read_monthly_chatter(30)` logs every `AMGT_PHASE route=chatter phase=<p> ms=<n>`
    with n within the bar (default 1,000 ms). Prints the table.
Verdict: R76 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
SOCIAL = "no social source is admitted yet"
INV_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v*.md"


def _event(path, query=None):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c62", "c63", "c64", "c65"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--bar", type=float, default=0.0)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "c65":
        bar = a.bar or 1000.0
        code = ("import logging, io\nbuf = io.StringIO(); h = logging.StreamHandler(buf)\n"
                "logging.getLogger().addHandler(h); logging.getLogger().setLevel(logging.INFO)\n"
                "from lib.research.api import monthly_chatter\nmonthly_chatter.read_monthly_chatter(30)\nprint(buf.getvalue())\n")
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=900)
        out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
        phases = re.findall(r"AMGT_PHASE route=chatter phase=([a-z ]+?) ms=(\d+)", out)
        for name, ms in phases:
            print(f"   chatter / {name}: {ms} ms")
        over = [(n, int(m)) for n, m in phases if int(m) > bar]
        clause("C1 every chatter phase of a fresh first request is within the bar", phases and not over,
               f"over {over} bar {bar:.0f}")
        return _verdict(a, ok)

    if a.cell == "c64":
        # the tracked implementation, run by this interpreter: the `comp-surprise` name is a bash shim Windows cannot spawn
        p = subprocess.run([sys.executable, ".tools/comp-surprise.py", "--project", "AMGT_RESAPP", "--json"],
                           capture_output=True, timeout=600)
        try:
            census = json.loads(p.stdout.decode("utf-8", errors="replace"))
        except ValueError:
            census = None
        if census is None:
            clause("C1 the census read", False, f"rc={p.returncode}")
            return _verdict(a, ok)
        open_ids = sorted({r.get("id") for r in census.get("remediation_rows") or []
                           if ((r.get("remediation") or {}).get("state") == "OPEN")})
        text = "\n".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(INV_GLOB)))
        cited = set(re.findall(r'"one_line":\s*"TRIAGE ([A-Za-z0-9_\-]+):', text))
        missing = [i for i in open_ids if i not in cited]
        print(f"   OPEN remediation rows {len(open_ids)}; with a TRIAGE citing row {len(open_ids) - len(missing)}; "
              f"e.g. missing {missing[:4]}")
        clause("C1 every OPEN remediation row has a citing triage row", not missing, f"{len(missing)} missing")
        return _verdict(a, ok)

    from lib.research.api import scoped_amgt
    from lib.research.coverage.covered_universe import covered_security_keys

    if a.where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(path, query=None):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(_event(path, query)).encode())["Payload"].read())
    else:
        def raw(path, query=None):
            return scoped_amgt.handler(_event(path, query))

    def body(path, query=None):
        r = raw(path, query)
        try:
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except ValueError:
            return r.get("statusCode"), {}

    keys = sorted(covered_security_keys())
    if a.cell == "c62":
        bad_desc, bad_items, bad_social, n_items, absent = [], [], [], 0, []
        for key in keys:
            code, ov = body(f"{PREFIX}/security/{key}/overlay")
            tb = ov.get("top_band")
            if not isinstance(tb, dict):
                absent.append(key)
                continue
            line = tb.get("description_line")
            if not ((isinstance(line, str) and line.strip() and "\n" not in line and len(line) <= 300)
                    or (not line and str(tb.get("description_reason") or "").strip())):
                bad_desc.append(key)
            items = tb.get("items") or []
            n_items += len(items)
            if any(not (str(i.get("url") or "").strip() and str(i.get("title") or "").strip() and i.get("published_utc"))
                   for i in items):
                bad_items.append(f"{key}:fields")
            order = [(-(i.get("mentions") or 0), str(i.get("published_utc") or "")) for i in items]
            want = sorted(order, key=lambda t: (t[0], [-ord(c) for c in t[1]]))
            if order != want:
                bad_items.append(f"{key}:order")
            if tb.get("social") != SOCIAL:
                bad_social.append(key)
        print(f"   names {len(keys)}; top_band absent {len(absent)}; items {n_items}; bad description {len(bad_desc)}; "
              f"bad items {len(bad_items)} e.g. {bad_items[:3]}; bad social {len(bad_social)}")
        clause("C1 every top band carries a one-line description or a plain reason", not absent and not bad_desc,
               f"absent {len(absent)} bad {len(bad_desc)}")
        clause("C2 every item is followable and the items are most-discussed then newest", not absent and not bad_items,
               f"{len(bad_items)}")
        clause("C3 the social half says no social source is admitted yet", not absent and not bad_social, f"{len(bad_social)}")
    else:
        code, fresh = body(f"{PREFIX}/freshness")
        rows = {r.get("security_key"): r for r in fresh.get("rows") or [] if r.get("covered")}
        absent, bad = [], []
        for key in keys:
            code, ov = body(f"{PREFIX}/security/{key}/overlay")
            prov = ov.get("input_provenance")
            if not isinstance(prov, list) or not prov:
                absent.append(key)
                continue
            row = rows.get(key) or {}
            want = dict((row.get("per_input") or {}))
            want["pack"] = row.get("pack")
            got = {e.get("input"): e for e in prov if isinstance(e, dict)}
            for inp, val in want.items():
                e = got.get(inp)
                if not e or e.get("last_run") != val or not str(e.get("source") or "").strip() or not e.get("outcome"):
                    bad.append(f"{key}/{inp}")
        print(f"   names {len(keys)}; input_provenance absent {len(absent)}; entries disagreeing with /freshness {len(bad)} "
              f"e.g. {bad[:4]}")
        clause("C1 every input's provenance agrees with /freshness", not absent and not bad,
               f"absent {len(absent)} bad {len(bad)}")
    return _verdict(a, ok)


def _verdict(a, ok):
    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R76 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
