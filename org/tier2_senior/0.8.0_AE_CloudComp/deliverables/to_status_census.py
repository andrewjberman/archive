"""One-shot census of the TO <status> field vs. delivery evidence.

READ-ONLY. NOT a monitor, NOT a freshness checker, NOT scheduled -- run it and read it.
Written for 2.0.0_SA_COO dispatch 72182 (2026-08-26) by 0.8.0_AE_CloudComp~F.

Two instruments, crossed:
  FIELD axis    -- what <status> says about itself (A_CONTRADICTS / B_BARE / C_SILENT / D_NO_FIELD)
  EVIDENCE axis -- does an EXACT id-joined proof instance exist, and what do its rows say

The prefix-join is DELIBERATELY ABSENT. Splitting a TO stem on '.' cuts inside the identifier
(D3_MODELOVERLAY.TO-D3.4 -> D3_MODELOVERLAY.TO-D3, which then matches TO-D3.1's instance), so it
manufactured evidence for four gated TOs that had delivered nothing. An instrument with a known
false-positive mode does not get to contribute to a reconciliation list.

Every count prints its denominator.

Usage:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/to_status_census.py
Run from the workspace root.
"""
from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

DECLARED_DOMAIN_GLOB = "org/tier2_senior/*/task_orders/*.md"
INSTANCE_GLOB = "org/**/deliverables/*.json"

# First tokens that read as NOT-TERMINAL to a dispatcher.
# "\u26d4" is the no-entry sign: it genuinely occurs as a status first token in the corpus.
OPEN_TOKENS = {
    "PENDING", "STAGED", "ACTIVE", "BUILD", "DISPATCHED", "HELD",
    "BLOCKED", "IN", "OPEN", "READY", "NOT", "\u26d4",
}

# "\u2014" is the em-dash: used as a status separator alongside '-' and ':'.
TOKEN_SPLIT = "[ \\-\u2014,(:]"

# Words in the PROSE that assert work happened. NOTE: this has a WRONG-SUBJECT failure mode --
# it also fires on prose asserting that a DEPENDENCY landed. Hand-check every hit.
DELIVERED_RE = re.compile(
    r"\b(DELIVERED|BUILT|LANDED|SHIPPED|COMPLETE[D]?|proof VALID|VALID rc=0|"
    r"measured PASS|ACCEPTED|CERTIFIED|DISCHARGED)\b",
    re.I,
)

TERMINAL_GOOD = {"PASS", "N/A-BY-CONSTRUCTION"}


def load_instances(root: pathlib.Path):
    """Index proof instances by their declared to_id. Returns (index, n_parsed)."""
    by_toid = collections.defaultdict(list)
    n = 0
    for p in root.glob(INSTANCE_GLOB):
        try:
            d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        n += 1
        toid = d.get("to_id")
        if toid:
            by_toid[toid].append((p, d))
    return by_toid, n


def classify_field(status):
    """Classify what the <status> field says ABOUT ITSELF."""
    if status is None:
        return "D_NO_FIELD"
    parts = re.split(TOKEN_SPLIT, status.strip(), maxsplit=1)
    prose = parts[1] if len(parts) > 1 else ""
    if not prose.strip():
        return "B_BARE"
    if DELIVERED_RE.search(prose):
        return "A_CONTRADICTS"
    return "C_SILENT"


def derive_delivery(instances):
    """Aggregate acceptance-row status to TO grain: MIN over rows, FAIL dominating.

    Returns one of DELIVERED / PARTIAL / FAILED / UNMEASURED-OR-NOT-STARTED.

    The last value is deliberately FUSED and says so: the absence of an instance is
    byte-identical between 'nobody started' and 'delivered before proof-of-spec existed'.
    Separating them needs a different instrument (assignee's word, or git archaeology).
    """
    if not instances:
        return "UNMEASURED-OR-NOT-STARTED"
    seen = []
    for _p, d in instances:
        for row in d.get("acceptance") or []:
            if isinstance(row, dict):
                seen.append(str(row.get("status", "")).upper())
    if not seen:
        return "UNMEASURED-OR-NOT-STARTED"
    if any(s.startswith("FAIL") for s in seen):
        return "FAILED"
    if all(s in TERMINAL_GOOD for s in seen):
        return "DELIVERED"
    return "PARTIAL"


def main() -> int:
    root = pathlib.Path(".")
    domain = sorted(root.glob(DECLARED_DOMAIN_GLOB))
    if not domain:
        print("ERROR: no TO files matched %s -- run from the workspace root."
              % DECLARED_DOMAIN_GLOB)
        return 2

    by_toid, n_inst = load_instances(root)

    all_rows = []
    for f in domain:
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<status>(.*?)</status>", text, re.S)
        status = " ".join(m.group(1).split()) if m else None
        tid = re.search(r'<task_order[^>]*\bid="([^"]+)"', text)
        issued = re.search(r"<issued_to>(.*?)</issued_to>", text, re.S)
        all_rows.append({
            "path": f,
            "seat": f.parts[2],
            "status": status,
            "token": "<NO-STATUS-FIELD>" if status is None
                     else re.split(TOKEN_SPLIT, status.strip())[0].upper(),
            "to_id": tid.group(1) if tid else None,
            "issued_to": " ".join(issued.group(1).split()) if issued else None,
            "has_pos": "<proof_of_spec>" in text,
        })

    n = len(all_rows)
    print("=== TO STATUS CENSUS ===")
    print("DECLARED DOMAIN : %s" % DECLARED_DOMAIN_GLOB)
    print("DENOMINATOR     : %d files scanned" % n)
    print()

    print("--- <status> FIRST TOKEN (denominator %d) ---" % n)
    for k, v in collections.Counter(r["token"] for r in all_rows).most_common():
        print("   %6d  %s" % (v, k))
    print()

    print("--- FIELD OCCUPANCY (denominator %d) ---" % n)
    for label, pred in (
        ("<status>", lambda r: r["status"] is not None),
        ("id= attribute", lambda r: bool(r["to_id"])),
        ("<issued_to>", lambda r: bool(r["issued_to"])),
        ("<proof_of_spec>", lambda r: r["has_pos"]),
    ):
        present = sum(1 for r in all_rows if pred(r))
        print("   %-18s present: %5d   ABSENT: %5d" % (label, present, n - present))
    print("   distinct full <status> strings: %d"
          % len({r["status"] for r in all_rows if r["status"]}))
    print()

    openset = [r for r in all_rows
               if r["status"] is None or r["token"] in OPEN_TOKENS]
    for r in openset:
        r["klass"] = classify_field(r["status"])
        r["inst"] = by_toid.get(r["to_id"], []) if r["to_id"] else []
        r["delivery"] = derive_delivery(r["inst"])

    print("--- ALLOCATION-RELEVANT SET (reads NOT-TERMINAL to a dispatcher) ---")
    print("COUNT: %d of %d" % (len(openset), n))
    print()
    print("proof instances parsed (dict-shaped) : %d" % n_inst)
    print("distinct to_id keys indexed          : %d" % len(by_toid))
    print()

    klasses = ["A_CONTRADICTS", "B_BARE", "C_SILENT", "D_NO_FIELD"]
    print("--- CROSS-TAB: field class x EXACT-id-join evidence ---")
    print("  %-16s %10s %13s %8s" % ("field class", "INSTANCE", "no-instance", "total"))
    for k in klasses:
        rows_k = [r for r in openset if r["klass"] == k]
        with_i = sum(1 for r in rows_k if r["inst"])
        print("  %-16s %10d %13d %8d" % (k, with_i, len(rows_k) - with_i, len(rows_k)))
    tot_i = sum(1 for r in openset if r["inst"])
    print("  %-16s %10d %13d %8d"
          % ("TOTAL", tot_i, len(openset) - tot_i, len(openset)))
    print()

    print("--- RECONCILIATION LIST: open-reading WITH an exact-joined instance (%d) ---"
          % tot_i)
    for r in sorted((r for r in openset if r["inst"]),
                    key=lambda x: (x["klass"], x["seat"])):
        print()
        print("  [%s -> %s] %s" % (r["klass"], r["delivery"], r["to_id"]))
        print("      seat   : %s" % r["seat"])
        print("      file   : %s" % r["path"].name)
        print("      status : %s" % ((r["status"] or "<no field>")[:150]))
        for p, d in r["inst"]:
            acc = [a for a in (d.get("acceptance") or []) if isinstance(a, dict)]
            tally = collections.Counter(str(a.get("status", "?")).upper() for a in acc)
            print("      proof  : %s  rows=%d  %s"
                  % (p.name, len(acc), dict(tally)))

    print()
    print("--- NOTE ON THE UNJOINABLE REMAINDER ---")
    print("  %d of %d open-reading TOs have NO exact-joined instance." % (len(openset) - tot_i, len(openset)))
    print("  That is UNMEASURED, NOT not-delivered: only %d of %d TOs carry <proof_of_spec> at all,"
          % (sum(1 for r in all_rows if r["has_pos"]), n))
    print("  and only %d carry an id= attribute to join on." % sum(1 for r in all_rows if r["to_id"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
