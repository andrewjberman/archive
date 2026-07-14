"""
nerves_traffic -- NFRA_NERVES L2: the UNIVERSAL TRAFFIC RECORD.

Turns the estate's exhaust into addressed traffic. One record shape for every stream:

    {ts, actor, verb, refs[], node_ids[], outcome, source_stream, unaddressed[]}

AN EVENT WITHOUT AN ADDRESS IS EXHAUST; WITH ONE, IT IS TRAFFIC. Addressing is nerves_resolve (L2's
keystone library); this module is the SENSE side: it reads the streams that ALREADY FLOW, extracts
each event's refs, addresses them, and emits the record.

THE STREAMS, AND WHAT EACH CAN HONESTLY CARRY (grounded 2026-07-14 -- read the shapes, do not assume):
  rail    org/mcp/comp-which-rail.log      11,999 rows. Carries term= / path= / q=. ADDRESSABLE.
                                           Also carries the PHANTOM-LIMB signal (NOFIT / zero-hit /
                                           DENY: what agents searched for and did NOT find).
  runs    org/mcp/comp-tool-runs.jsonl     the second-granularity run sink (NFRA_COMPCLOSE).
                                           args_head carries the TARGET. ADDRESSABLE + has outcome.
  git     `git log --name-only`            6,682 commits / 35 days. File paths. HIGHLY ADDRESSABLE.
                                           The CO_CHANGE goldmine (L3a).
  telem   org/mcp/agent_telemetry/*.jsonl  185,563 rows -- the LARGEST stream, and a HARD LIMIT:
                                           **it records THAT a tool ran, NOT WHAT IT TOUCHED**
                                           (no args in the row: ts/serial/tool_name/kind/session).
                                           So it addresses to the TOOL, never to a data node. It is
                                           genuine ACTOR/SESSION context and a real agent x tool
                                           ATTENTION signal -- and it CANNOT give agent x node
                                           attention. Stated, not papered over: an ATTENTION edge
                                           built on telemetry alone would be a tool-popularity edge
                                           wearing a node-attention costume.

UNADDRESSED IS A FIRST-CLASS FIELD, never a dropped remainder: an unresolvable ref is the F-5 class
repeating (a blind spot in the estate's self-model) and every summary prints its DENOMINATOR.

Read-only over the streams; append-only to org/mcp/nerves-traffic.jsonl (gitignored, rotated).

Usage:
    nerves_traffic scan [--stream rail|runs|git|telem|all] [--since-days N] [--limit N] [--json]
    nerves_traffic emit [--stream all] [--since-days N]     # write the traffic records
    nerves_traffic --self-test
Author: 1.0.0_SA_CTO~Z (NFRA_NERVES L2). 2026-07-14.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_WS = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, _HERE)

from nerves_resolve import resolve_many  # noqa: E402

RAIL = os.path.join(_WS, "org", "mcp", "comp-which-rail.log")
RUNS = os.path.join(_WS, "org", "mcp", "comp-tool-runs.jsonl")
TELEM_DIR = os.path.join(_WS, "org", "mcp", "agent_telemetry")
SINK = os.path.join(_WS, "org", "mcp", "nerves-traffic.jsonl")

# rail: `ts TAG tool=X term=Y src=.. serial=.. q="..."` (+ path=/matches= on RUN rows)
_RAIL_RX = re.compile(r"^(\S+)\s+(\S+)\s+(.*)$")
_KV_RX = re.compile(r"(\w+)=(\S+)")
_Q_RX = re.compile(r'q="([^"]*)"')
# the PHANTOM-LIMB tags: what an agent looked for and did not find.
_PHANTOM_TAGS = {"NOFIT-POSTERIOR", "DENY"}


def _refs_from_rail(line: str):
    """-> (actor, verb, refs, outcome, phantom). A zero-match RUN-GREP is ALSO a phantom limb."""
    m = _RAIL_RX.match(line.strip())
    if not m:
        return None
    ts, tag, rest = m.group(1), m.group(2), m.group(3)
    kv = dict(_KV_RX.findall(rest))
    q = (_Q_RX.search(rest) or [None, ""])[1] if _Q_RX.search(rest) else ""
    refs = [v for v in (kv.get("term"), kv.get("path")) if v and v not in ("-", ".")]
    matches = kv.get("matches")
    phantom = (tag in _PHANTOM_TAGS) or (matches is not None and matches == "0")
    outcome = ("not-found" if phantom else ("found" if matches and matches != "0" else None))
    return {"ts": ts, "actor": kv.get("serial", "-"), "verb": tag, "refs": refs,
            "outcome": outcome, "phantom": phantom, "query": q, "tool": kv.get("tool", "")}


def _refs_from_run(row: dict):
    """The run sink: args_head carries the target; rc/result carry the OUTCOME (the Goodhart-safe
    weight -- value, never popularity)."""
    args = row.get("args_head", "") or ""
    # take path-ish / id-ish tokens out of the arg string
    refs = [t for t in re.findall(r"[\w./\\-]{3,}", args)
            if ("/" in t or "." in t or t.startswith("comp-")) and not t.startswith("--")]
    return {"ts": row.get("ts_epoch"), "actor": row.get("serial", "-"),
            "verb": row.get("tool", "?"), "refs": refs[:8],
            "outcome": row.get("result"), "phantom": False, "query": args, "tool": row.get("tool", "")}


def _git_events(since_days: int, limit: int):
    """Commits -> (actor, files). The CO_CHANGE substrate (L3a) and free."""
    rc = subprocess.run(["git", "-C", _WS, "log", "--since=%d days ago" % since_days,
                         "--format=%x1e%H\x1f%an\x1f%ad", "--date=short", "--name-only"],
                        capture_output=True, text=True, errors="replace")
    out = []
    for block in rc.stdout.split("\x1e"):
        if not block.strip():
            continue
        head, *rest = block.strip().splitlines()
        parts = head.split("\x1f")
        if len(parts) != 3:
            continue
        files = [f.strip() for f in rest if f.strip()]
        if not files:
            continue
        out.append({"ts": parts[2], "actor": parts[1], "verb": "commit",
                    "refs": files, "outcome": None, "phantom": False,
                    "query": parts[0][:12], "tool": "git"})
        if len(out) >= limit:
            break
    return out


def _telem_events(limit: int):
    """THE HARD LIMIT, STATED: telemetry rows carry NO args -- they record THAT a tool ran, not WHAT
    it touched. So the only honest ref is the TOOL itself (agent x tool attention). Never dress this
    up as node attention."""
    out = []
    if not os.path.isdir(TELEM_DIR):
        return out
    for fn in sorted(os.listdir(TELEM_DIR)):
        if not fn.endswith(".jsonl"):
            continue
        try:
            with open(os.path.join(TELEM_DIR, fn), encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        r = json.loads(line)
                    except Exception:  # noqa: BLE001
                        continue
                    tool = r.get("tool_name", "")
                    out.append({"ts": r.get("ts"), "actor": r.get("serial", "-"),
                                "verb": "tool-use", "refs": [tool] if tool.startswith("comp") else [],
                                "outcome": None, "phantom": False, "query": tool, "tool": tool,
                                "session": r.get("session_id", "")})
                    if len(out) >= limit:
                        return out
        except OSError:
            continue
    return out


def collect(stream: str, since_days: int, limit: int):
    evs = []
    if stream in ("rail", "all") and os.path.exists(RAIL):
        with open(RAIL, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                e = _refs_from_rail(line)
                if e:
                    e["source_stream"] = "rail"
                    evs.append(e)
        evs = evs[-limit:] if stream == "rail" else evs
    if stream in ("runs", "all") and os.path.exists(RUNS):
        with open(RUNS, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    e = _refs_from_run(json.loads(line))
                    e["source_stream"] = "runs"
                    evs.append(e)
                except Exception:  # noqa: BLE001
                    continue
    if stream in ("git", "all"):
        for e in _git_events(since_days, limit):
            e["source_stream"] = "git"
            evs.append(e)
    if stream in ("telem", "all"):
        for e in _telem_events(limit):
            e["source_stream"] = "telem"
            evs.append(e)
    return evs


# ---- THE DENOMINATOR CONTROL (found by running it: my own first measurement LIED) ---------------
# The rail's `term=` is the token comp-which EXTRACTED FROM A QUESTION -- often a plain English word
# ("WRITE", "component", "upstream", "threading"). Those are SEARCH VOCABULARY, not references to
# estate nodes. My first pass counted them as UNADDRESSED and reported an 11.6% rail hit-rate with a
# band full of English words -- i.e. it would have sent someone hunting "blind spots in the estate's
# self-model" that are just... words. A REF THAT WAS NEVER AN ADDRESS CANNOT BE A MISSING ADDRESS.
#
# So the denominator is ADDRESSABLE-SHAPED refs only, and a lexical term goes to its own band (where
# it is genuinely useful -- it is the query-vocabulary/phantom-limb signal, not a graph gap).
# PRINT THE DENOMINATOR OF EVERY SCAN YOU REASON FROM -- including the one that flatters you.
_ADDRESSABLE_SHAPE_RX = re.compile(
    r"[/\\]"                      # a path
    r"|\.(py|tsx?|jsx?|json|ya?ml|md|sh|tf|hcl|parquet|sql|cfg|ini|toml)$"   # a file
    r"|^(s3://|arn:)"             # a cloud uri/arn
    r"|^comp-[\w-]+$"             # a comp-tool
    r"|^[a-z0-9]+(-[a-z0-9]+){2,}$"     # a hyphenated cloud name (>=3 segments)
    r"|^[A-Za-z]+_[A-Za-z0-9_]+$"       # snake_case identifier
    r"|^[a-z]+[A-Z][A-Za-z]*$"          # camelCase identifier
    r"|^[A-Z][a-z]+[A-Z][A-Za-z]*$",    # PascalCase identifier
    re.X)


def _is_addressable_shaped(ref: str) -> bool:
    """Was this ref ever an ADDRESS ATTEMPT? A plain English word never was."""
    r = (ref or "").strip()
    return bool(r) and bool(_ADDRESSABLE_SHAPE_RX.search(r))


def address(events: list):
    """Resolve every event's refs -> traffic records. UNADDRESSED refs are KEPT (a finding) -- but
    only ADDRESSABLE-SHAPED refs count in the denominator; a lexical search term was never an
    address attempt and is banded separately."""
    records, all_refs, unaddressed_refs, lexical_refs = [], 0, [], []
    for e in events:
        raw = list(e.get("refs") or [])
        shaped = [r for r in raw if _is_addressable_shaped(r)]
        lexical = [r for r in raw if not _is_addressable_shaped(r)]
        lexical_refs.extend(lexical)
        res, _ = resolve_many(tuple(shaped))
        node_ids, unaddr = [], []
        for r in res:
            if r.addressed:
                node_ids.extend(r.node_ids)
            else:
                unaddr.append(r.ref)
        all_refs += len(res)          # THE DENOMINATOR = address ATTEMPTS, not every token
        unaddressed_refs.extend(unaddr)
        records.append({
            "ts": e.get("ts"), "actor": e.get("actor", "-"), "verb": e.get("verb", "?"),
            "refs": shaped, "node_ids": sorted(set(node_ids)),
            "outcome": e.get("outcome"), "source_stream": e.get("source_stream", "?"),
            "unaddressed": unaddr, "lexical_terms": lexical, "phantom": bool(e.get("phantom")),
            "query": (e.get("query") or "")[:120],
        })
    # AN EVENT WITH NO ADDRESSABLE-SHAPED REF NEVER ATTEMPTED AN ADDRESS -- it cannot be a miss.
    # Two denominators, both printed: events-that-tried, and refs-that-were-address-attempts.
    tried = [r for r in records if r["refs"]]
    addressed_events = sum(1 for r in tried if r["node_ids"])
    n_tried = len(tried)
    stats = {
        "events_total": len(records),
        "events_with_an_address_attempt": n_tried,           # THE DENOMINATOR that matters
        "events_addressed": addressed_events,
        "events_unaddressed": n_tried - addressed_events,
        "event_hit_rate_pct": round(100.0 * addressed_events / n_tried, 1) if n_tried else 0.0,
        "refs_addressable_shaped": all_refs,                 # THE OTHER DENOMINATOR
        "refs_unaddressed": len(unaddressed_refs),
        "ref_hit_rate_pct": round(100.0 * (all_refs - len(unaddressed_refs)) / all_refs, 1) if all_refs else 0.0,
        "lexical_terms_not_address_attempts": len(lexical_refs),   # banded, NOT counted as misses
        "phantom_limb_events": sum(1 for r in records if r["phantom"]),
        "by_stream": {},
    }
    for r in records:
        s = stats["by_stream"].setdefault(r["source_stream"], {"events": 0, "tried": 0, "addressed": 0})
        s["events"] += 1
        if r["refs"]:
            s["tried"] += 1
            if r["node_ids"]:
                s["addressed"] += 1
    return records, stats, unaddressed_refs


def _render(stats, unaddressed_refs):
    from collections import Counter
    L = ["nerves-traffic -- the universal traffic record (NFRA_NERVES L2)",
         "  INVOCATION (pin beside any number you quote -- nothing here is re-derivable without it):",
         "    %s" % stats.get("invocation", "(not recorded -- direct address() call)"),
         "  EVENTS: %d seen | %d MADE AN ADDRESS ATTEMPT | %d addressed | %d UNADDRESSED -> hit-rate %.1f%%"
         % (stats["events_total"], stats["events_with_an_address_attempt"], stats["events_addressed"],
            stats["events_unaddressed"], stats["event_hit_rate_pct"]),
         "  REFS:   %d addressable-shaped (THE DENOMINATOR) | %d UNADDRESSED -> hit-rate %.1f%%"
         % (stats["refs_addressable_shaped"], stats["refs_unaddressed"], stats["ref_hit_rate_pct"]),
         "  LEXICAL: %d search terms that were NEVER address attempts -- banded, NOT counted as misses"
         % stats["lexical_terms_not_address_attempts"],
         "           (a ref that was never an address CANNOT be a missing address. My own first run",
         "            reported an 11.6% rail hit-rate with a band full of English words. Fixed.)",
         "  PHANTOM-LIMB events (searched for, NOT found): %d  <- the demand map for knowledge that does not exist"
         % stats["phantom_limb_events"],
         "",
         "  BY STREAM (addressed / attempted / seen):"]
    for s, v in sorted(stats["by_stream"].items()):
        pct = 100.0 * v["addressed"] / v["tried"] if v["tried"] else 0
        L.append("    %-6s %6d / %-6d / %-6d  (%.1f%% of attempts)" % (s, v["addressed"], v["tried"], v["events"], pct))
    L += ["",
          "  UNADDRESSED BAND -- a blind spot in the estate's self-model, NOT a drop (top 12):"]
    for ref, n in Counter(unaddressed_refs).most_common(12):
        L.append("    x%-4d %s" % (n, ref[:78]))
    if not unaddressed_refs:
        L.append("    (none)")
    L += ["",
          "  NOTE (a HARD LIMIT, stated): the telemetry stream records THAT a tool ran, NOT what it",
          "  touched (no args in the row). It gives agent x TOOL attention, never agent x NODE. An",
          "  ATTENTION edge built on telemetry alone would be tool-popularity in a node-attention costume."]
    return "\n".join(L)


def _self_test() -> int:
    results = []
    def ck(name, ok, detail=""):
        results.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))

    # a rail RUN-GREP row with zero matches IS a phantom limb (searched, not found).
    e = _refs_from_rail('2026-07-14T05:00:00Z  RUN-GREP  tool=comp-grep  term=zz_nope  src=direct  '
                        'serial=1.0.0_SA_CTO~Z  matches=0 files=0 scanned=100 path=org')
    ck("rail.parsed", e is not None and e["actor"] == "1.0.0_SA_CTO~Z" and "zz_nope" in e["refs"])
    ck("rail.zero_match_is_a_phantom_limb", e["phantom"] is True and e["outcome"] == "not-found")

    # a DENY row is a phantom limb too (the rail blocked it; the agent still wanted something).
    e2 = _refs_from_rail('2026-07-14T05:00:00Z  DENY  tool=Bash  class=aws  q=aws s3 ls')
    ck("rail.deny_is_a_phantom_limb", e2 is not None and e2["phantom"] is True)

    # a run row addresses its target AND carries the outcome (the Goodhart-safe weight).
    e3 = _refs_from_run({"ts_epoch": 1, "serial": "X", "tool": "comp-blast",
                         "args_head": "comp-blast data/black_diamond/scripts/gold/A_00.accounts_dimension.py",
                         "rc": 0, "result": "PASS"})
    ck("runs.target_and_outcome",
       any("A_00" in r for r in e3["refs"]) and e3["outcome"] == "PASS")

    # ADDRESSING: a known-good ref addresses; an unknown ref lands in the UNADDRESSED band, kept.
    recs, stats, unaddr = address([
        {"ts": 1, "actor": "a", "verb": "v", "refs": ["CLAUDE.md", "zz_not_a_thing_xyz"],
         "source_stream": "test", "phantom": False, "outcome": None, "query": ""}])
    ck("address.partial_hit_keeps_unaddressed",
       recs[0]["node_ids"] and "zz_not_a_thing_xyz" in recs[0]["unaddressed"])
    ck("address.denominator_always_present",
       stats["refs_addressable_shaped"] == 2 and stats["refs_unaddressed"] == 1
       and stats["ref_hit_rate_pct"] == 50.0,
       f"shaped {stats['refs_addressable_shaped']} hit {stats['ref_hit_rate_pct']}%")
    ck("address.unaddressed_is_never_dropped", unaddr == ["zz_not_a_thing_xyz"])

    # THE DENOMINATOR CONTROL (this bug was in MY first live run): a plain English search term was
    # NEVER an address attempt, so it must NOT be counted as a missing address. It lands in the
    # LEXICAL band instead -- and the hit-rate denominator excludes it.
    recs2, stats2, unaddr2 = address([
        {"ts": 1, "actor": "a", "verb": "RUN-GREP", "refs": ["component", "upstream", "WRITE"],
         "source_stream": "rail", "phantom": False, "outcome": None, "query": ""}])
    ck("denominator.english_words_are_not_missing_addresses",
       stats2["refs_addressable_shaped"] == 0 and stats2["refs_unaddressed"] == 0
       and stats2["lexical_terms_not_address_attempts"] == 3 and unaddr2 == [],
       f"lexical={stats2['lexical_terms_not_address_attempts']} unaddressed={stats2['refs_unaddressed']}")
    ck("denominator.no_attempt_no_miss",
       stats2["events_with_an_address_attempt"] == 0 and stats2["event_hit_rate_pct"] == 0.0,
       "an event that never tried to address cannot be a miss")
    # ...and a REAL blind spot still lands in UNADDRESSED (the control can still fire).
    recs3, stats3, unaddr3 = address([
        {"ts": 1, "actor": "a", "verb": "v", "refs": ["data/nope/ghost_script.py"],
         "source_stream": "test", "phantom": False, "outcome": None, "query": ""}])
    ck("denominator.real_blind_spot_still_fires",
       stats3["refs_addressable_shaped"] == 1 and unaddr3 == ["data/nope/ghost_script.py"],
       "a path-shaped ref that resolves to nothing IS a finding")

    ok = all(results)
    print("\n" + ("OK: exhaust -> traffic; denominators printed; UNADDRESSED is a band; phantom limbs captured"
                  if ok else "ERROR: nerves_traffic self-test FAILED"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="nerves-traffic")
    ap.add_argument("cmd", nargs="?", default="scan", choices=["scan", "emit"])
    ap.add_argument("--stream", default="all", choices=["rail", "runs", "git", "telem", "all"])
    ap.add_argument("--since-days", type=int, default=35)
    ap.add_argument("--limit", type=int, default=4000)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass

    if args.self_test:
        return _self_test()

    events = collect(args.stream, args.since_days, args.limit)
    records, stats, unaddr = address(events)
    # CVO~Z verify P2 (2d2080e1e): a headline number nobody can re-derive is not evidence.
    # RESOLVED args, not raw argv -- defaults are invisible in argv, and rail is uncapped
    # under --stream all, so the effective knobs must ride WITH the numbers they produced.
    stats["invocation"] = "cmd=%s stream=%s since_days=%d limit=%d (argv: %s)" % (
        args.cmd, args.stream, args.since_days, args.limit,
        " ".join(sys.argv[1:]) or "<defaults>")

    if args.cmd == "emit":
        os.makedirs(os.path.dirname(SINK), exist_ok=True)
        with open(SINK, "w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=True, default=str) + "\n")
        print("nerves-traffic: wrote %d records -> %s" % (len(records), os.path.relpath(SINK, _WS)))

    if args.json:
        print(json.dumps({"stats": stats, "unaddressed_sample": unaddr[:50]}, indent=1))
    else:
        print(_render(stats, unaddr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
