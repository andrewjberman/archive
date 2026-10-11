"""IRPT_BCKEND round 138 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two READ-ONLY orders with disjoint write sets:
  IB138-1  IB-pr-440  can the SERVED holdings answer carry a sleeve leaf with no security node under it? the producer's rule read
                      in code, and such leaves counted in one firm's served answer for one day (CTO msg 5373).
  IB138-2  IB-pr-441  the two tables an addendum on the second witness would rest on: both witnesses compared per instrument
                      type (the type joined by CUSIP from the transactions table), and each priced fund trade set beside the
                      reader's bar for its date and the days either side (CTO msg 5376).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Every criterion FAILs at base (no file).
  IB138-1-AC1  the producer's rule is stated with the code lines read and its claim.
  IB138-1-AC2  the served answer read is named (object, version, as-of), its nodes are counted with no remainder, and the sleeve
               nodes split into those with a security node beneath them and those with none.
  IB138-1-AC3  the verdict on the portal fixture follows from the rule and the count; the control reads as planted; no account id.
  IB138-2-AC1  every security both witnesses carry is in exactly one type (or NO_TYPE); per type the security-days split with no
               remainder into equal / one day off / neither / no bar; the empty-one-day-off types listed are those the table shows.
  IB138-2-AC2  every priced fund trade is in exactly one outcome (same day only, prior day only, next day only, more than one,
               none, no bar); the fetch for both tables was one pass.
  IB138-2-AC3  the control reads as planted (a shifted series reads one day off; a trade planted on the prior day's bar reads
               prior day only); nothing re-graded; no other source; no account id.
Every count is UNMEASURED by the issuer.
"""
import json
import re
import sys
from pathlib import Path

D1 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~298/"
D2 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~299/"
OUT1, READ1 = D1 + "IB138-1_sleeve_leaf_read.json", D1 + "IB138-1_SLEEVE_LEAF_READ.md"
OUT2, READ2 = D2 + "IB138-2_type_overlap_and_fund_check.json", D2 + "IB138-2_TYPE_OVERLAP_AND_FUND_CHECK_READ.md"
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)
CLAIMS = ("measured", "inferred", "held", "absent")
COLS = ("equal", "one_day_off", "neither", "no_bar")
TRADE = ("same_day_only", "prior_day_only", "next_day_only", "more_than_one", "none", "no_bar")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB138"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def no_ids(*rels):
        hits = 0
        for rel in rels:
            f = root / rel
            if not f.is_file():
                fail("no %s" % rel)
            hits += len(ACCOUNT_ID.findall(f.read_text(encoding="utf-8")))
        if hits:
            fail("%d account-id token(s) in the outputs" % hits)

    if cid == "IB138-1-AC1":
        r = load(OUT1).get("producer_rule") or {}
        if r.get("can_emit_a_sleeve_leaf_with_no_security_node") not in (True, False) or r.get("claim") not in CLAIMS:
            fail("producer_rule needs can_emit_a_sleeve_leaf_with_no_security_node (true/false) and a claim in %s" % (CLAIMS,))
        lines = r.get("code_lines")
        if not isinstance(lines, list) or not lines or any(":" not in str(x) for x in lines) or not r.get("in_words"):
            fail("producer_rule needs code_lines as file:line entries and the rule in words")
        if not isinstance(r.get("node_kinds"), list) or not r["node_kinds"]:
            fail("producer_rule.node_kinds is not stated")
        print("OK: the producer %s emit such a leaf (%s); %d code line(s) cited" % (
            "CAN" if r["can_emit_a_sleeve_leaf_with_no_security_node"] else "cannot", r["claim"], len(lines)))
    elif cid == "IB138-1-AC2":
        s = load(OUT1).get("served_answer") or {}
        if any(not s.get(k) for k in ("object", "version_or_etag", "as_of", "read_by")):
            fail("served_answer needs object, version_or_etag, as_of and read_by")
        kinds = s.get("nodes_by_kind")
        if not isinstance(kinds, dict) or not kinds or sum(kinds.values()) != s.get("nodes_total"):
            fail("nodes_by_kind does not sum to nodes_total")
        need = ("sleeve_nodes", "sleeve_nodes_with_a_security_node_beneath", "sleeve_nodes_with_none")
        if any(not isinstance(s.get(k), int) for k in need) or s[need[1]] + s[need[2]] != s[need[0]]:
            fail("the sleeve nodes do not split with no remainder")
        if not isinstance(s.get("accounts_holding_such_a_leaf"), int) or not s.get("how_a_sleeve_node_is_recognised"):
            fail("accounts_holding_such_a_leaf (a count) and how_a_sleeve_node_is_recognised are not stated")
        print("OK: %d nodes; %d sleeve node(s): %d with a security node beneath, %d with none" % (
            s["nodes_total"], s[need[0]], s[need[1]], s[need[2]]))
    elif cid == "IB138-1-AC3":
        a = load(OUT1)
        v = a.get("verdict") or {}
        rule = (a.get("producer_rule") or {}).get("can_emit_a_sleeve_leaf_with_no_security_node")
        found = (a.get("served_answer") or {}).get("sleeve_nodes_with_none")
        if v.get("the_fixture_shape_is_reachable_in_a_served_answer") not in (True, False) or not v.get("in_one_sentence"):
            fail("verdict needs the_fixture_shape_is_reachable_in_a_served_answer and one sentence")
        if isinstance(found, int) and found > 0 and v["the_fixture_shape_is_reachable_in_a_served_answer"] is not True:
            fail("%d such leaves were counted in a served answer, yet the verdict says the shape is not reachable" % found)
        if rule is False and found == 0 and v["the_fixture_shape_is_reachable_in_a_served_answer"] is not False:
            fail("the rule says no and none were counted, yet the verdict says reachable")
        c = a.get("control") or {}
        if not c.get("planted") or c.get("planted") != c.get("read"):
            fail("the control does not read as planted")
        if a.get("nothing_written_or_served") is not True:
            fail("nothing_written_or_served must be true")
        no_ids(OUT1, READ1)
        print("OK: the fixture's shape is %s in a served answer; control as planted; 0 account-id tokens" % (
            "REACHABLE" if v["the_fixture_shape_is_reachable_in_a_served_answer"] else "not reachable"))
    elif cid == "IB138-2-AC1":
        a = load(OUT2)
        o = a.get("overlap_by_type")
        if not isinstance(o, dict) or not o:
            fail("overlap_by_type is empty")
        empty, secs = [], 0
        for name, r in o.items():
            if any(not isinstance(r.get(k), int) for k in COLS + ("securities", "security_days", "equal_on_days_the_close_moved")):
                fail("type %s lacks an integer count" % name)
            if sum(r[k] for k in COLS) != r["security_days"]:
                fail("type %s: the four columns sum to %d, security_days is %d" % (name, sum(r[k] for k in COLS), r["security_days"]))
            secs += r["securities"]
            if r["one_day_off"] == 0 and r["equal"] > 0:
                empty.append(name)
        j = a.get("type_join") or {}
        if any(not isinstance(j.get(k), int) for k in ("securities_both_witnesses_carry", "found_a_type", "found_no_type", "found_more_than_one_type")):
            fail("type_join lacks an integer count")
        if j["found_a_type"] + j["found_no_type"] + j["found_more_than_one_type"] != j["securities_both_witnesses_carry"] \
                or secs != j["securities_both_witnesses_carry"]:
            fail("the join does not account for every security, or the table's securities (%d) are not the join's (%d)" % (
                secs, j["securities_both_witnesses_carry"]))
        if sorted(a.get("types_with_an_empty_one_day_off_column") or []) != sorted(empty):
            fail("the listed types %r are not the ones the table shows %r" % (a.get("types_with_an_empty_one_day_off_column"), empty))
        if not a.get("one_day_off_rule") or not a.get("unchanged_price_rule") or not j.get("type_fields"):
            fail("one_day_off_rule, unchanged_price_rule and type_join.type_fields are not stated")
        print("OK: %d securities in %d type(s) (%d with no type); empty one-day-off column: %s" % (secs, len(o), j["found_no_type"], empty))
    elif cid == "IB138-2-AC2":
        a = load(OUT2)
        t = a.get("fund_trades") or {}
        if any(not isinstance(t.get(k), int) for k in TRADE + ("trades", "fund_dates", "funds")):
            fail("fund_trades lacks an integer count")
        if sum(t[k] for k in TRADE) != t["trades"]:
            fail("the six outcomes sum to %d, trades is %d" % (sum(t[k] for k in TRADE), t["trades"]))
        if not t.get("unit_counted") or not t.get("how_a_fund_is_recognised") or not t.get("tolerance") \
                or not isinstance(t.get("by_fund"), list):
            fail("fund_trades needs unit_counted, how_a_fund_is_recognised, tolerance and by_fund")
        fe = a.get("fetch") or {}
        calls = fe.get("calls")
        if not isinstance(calls, list) or not calls or any(not isinstance(c.get("tickers"), int) or c["tickers"] > 50 for c in calls):
            fail("fetch.calls must list every call with its ticker count, none over 50")
        if sum(c["tickers"] for c in calls) != fe.get("distinct_tickers_asked") or fe.get("tickers_asked_more_than_once") != 0:
            fail("the fetch is not one pass")
        if fe["distinct_tickers_asked"] > 1500:
            fail("%d tickers were asked, above the 1,500 stop" % fe["distinct_tickers_asked"])
        print("OK: %d trade(s) on %d fund-date(s) of %d fund(s): same day %d, prior %d, next %d, more than one %d, none %d, no bar %d; %d call(s)" % (
            t["trades"], t["fund_dates"], t["funds"], t["same_day_only"], t["prior_day_only"], t["next_day_only"], t["more_than_one"],
            t["none"], t["no_bar"], len(calls)))
    elif cid == "IB138-2-AC3":
        a = load(OUT2)
        c = a.get("control") or {}
        p = c.get("planted") or {}
        if not p or p != c.get("read") or not p.get("shifted_series_reads_one_day_off") or not p.get("trade_on_the_prior_bar_reads_prior_day_only"):
            fail("the control does not read as planted, or does not plant the two cases")
        if a.get("claims_regraded_in_product") is not False or a.get("other_sources_asked") != 0 or a.get("classes_admitted_by_this_cell") != 0:
            fail("claims_regraded_in_product must be false, other_sources_asked 0 and classes_admitted_by_this_cell 0")
        no_ids(OUT2, READ2)
        print("OK: the control reads as planted with both cases; nothing re-graded; no class admitted; 0 account-id tokens")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
