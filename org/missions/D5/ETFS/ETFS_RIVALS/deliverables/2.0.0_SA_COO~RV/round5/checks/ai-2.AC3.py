"""RIV-ai-2 AC3 (PRD v0.10 web fallback; CTO GO note 1: the instrument is named and graded from its records) -- the web is read
only where the internal readings hold nothing fresh, and every web read is recorded and labelled.

Pure, offline (stub client, the `_common` A1 fixtures):
  - every reading fresh: run_chain makes ZERO web_search calls and every row's web_reads is empty;
  - fear_greed missing: exactly ONE web_search call; the direction_verdict row's web_reads holds one entry with a non-empty
    query, the stub's URL and label "web"; and the prompt-two messages carry the web text marked "[web]";
  - control: the module names the instrument -- `ai_accounts.WEB_SEARCH_TOOL == {"type": "web_search_preview"}`."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import ai_accounts as ai

    g5, g6, hc, bt = c.ai2_tables()
    facts = ai.fact_pack("TXUE", c.AI_DAY, g5, g6, hc, bt)
    fid, val = facts[0]["id"], facts[0]["cited_row"]["value"]

    def replies():
        return [c.ai2_reply(f"It moved {val}.", [fid]), c.ai2_reply(f"It moved {val}.", [fid])]

    fresh = c.StubClient(replies())
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, c.ai2_readings(), fresh, "runW0")
    print("all fresh: web calls", len(fresh.web), "| web_reads", [r.get("web_reads") for r in rows])
    v.check(fresh.web == [] and all(not json.loads(r["web_reads"]) if isinstance(r.get("web_reads"), str) else not r.get("web_reads")
                                    for r in rows),
            "all readings fresh: no web call and no web_reads")
    gap = c.StubClient(replies())
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, c.ai2_readings(missing=("fear_greed",)), gap, "runW1")
    dv = [r for r in rows if r.get("kind") == "direction_verdict"]
    wr = dv[0].get("web_reads") if dv else None
    wr = json.loads(wr) if isinstance(wr, str) else (wr or [])
    print("fear_greed missing: web calls", gap.web, "| web_reads", wr)
    two = gap.calls[1] if len(gap.calls) > 1 else []
    v.check(len(gap.web) == 1 and len(wr) == 1 and wr[0].get("query") and wr[0].get("label") == "web"
            and "https://example.com/a" in json.dumps(wr[0]) and "[web]" in json.dumps(two),
            "one web call, recorded with its query, URL and label 'web', and marked [web] in prompt two")
    print("WEB_SEARCH_TOOL:", getattr(ai, "WEB_SEARCH_TOOL", None))
    v.check(getattr(ai, "WEB_SEARCH_TOOL", None) == {"type": "web_search_preview"}, "control: the instrument is named")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
