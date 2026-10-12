"""IRPT_BCKEND round 153 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order:
  IB153-1  IB-pr-457  the date-basis producer's DESIGN as a read, not a build: where the grading module would be called, what
                      it would serve, every consumer of the date-basis member; and one count: the newly held securities left
                      blank for their first 40 days, apart from those the repeat rule takes (CTO msgs 5896, 5933; PRD v0.44).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB153-1-AC1  where it would be called: the candidate call sites, each with its file:line, its schedule or trigger, the inputs
               it holds there and the inputs the module needs that it does NOT hold; what is served today from that site.
  IB153-1-AC2  every consumer of the date-basis member and of the holdings gold it would ride on, found by subtraction (files
               naming it counted, each placed), each with what it does on an absent, an unknown and a blank value, and the one
               read a release would make through it.
  IB153-1-AC3  the count: security-days the short-history floor leaves ungraded split from those the repeat rule takes, summing
               with no remainder; the bounds held; nothing built, nothing proposed as a build.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~313/"
OUT, READ = D + "IB153-1_producer_design_read.json", D + "IB153-1_PRODUCER_DESIGN_READ.md"
CLAIMS = ("measured", "inferred", "held", "absent")


def at(x):
    return isinstance(x, str) and ":" in x


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB153"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    if cid == "IB153-1-AC1":
        if not re.match(r"^[0-9a-f]{10,40}$", str(a.get("base_commit") or "")):
            fail("base_commit is not stated")
        sites = a.get("candidate_call_sites")
        if not isinstance(sites, list) or not sites:
            fail("candidate_call_sites is empty")
        for s in sites:
            if not s.get("site") or not at(s.get("code_line")) or not s.get("schedule_or_trigger") or not isinstance(s.get("inputs_in_hand"), list) \
                    or not isinstance(s.get("inputs_the_module_needs_and_the_site_lacks"), list) or not s.get("serves_today") or s.get("claim") not in CLAIMS:
                fail("each call site needs site, code_line, schedule_or_trigger, inputs_in_hand, inputs_the_module_needs_and_the_site_lacks, serves_today and a claim")
        n = a.get("module_inputs")
        if not isinstance(n, list) or not n or any(not x.get("input") or not x.get("where_it_lives_today") or x.get("claim") not in CLAIMS for x in n):
            fail("module_inputs must list each input the module takes, where it lives today, and a claim")
        if not isinstance(a.get("what_is_served_today_for_the_date_basis"), dict) or not a["what_is_served_today_for_the_date_basis"].get("in_words"):
            fail("what_is_served_today_for_the_date_basis is not stated")
        print("OK: %d candidate call site(s), %d module input(s) placed" % (len(sites), len(n)))
    elif cid == "IB153-1-AC2":
        c = a.get("consumers") or {}
        fn = c.get("files_naming_the_member_or_the_gold") or {}
        if not all(isinstance(fn.get(k), int) for k in ("total", "consumers", "writers", "neither")) or fn["consumers"] + fn["writers"] + fn["neither"] != fn["total"]:
            fail("files_naming_the_member_or_the_gold must count total = consumers + writers + neither")
        lst = c.get("list")
        if not isinstance(lst, list) or not lst:
            fail("consumers.list is empty")
        for x in lst:
            if not x.get("consumer") or not at(x.get("code_line")) or not x.get("kind") or not x.get("on_absent") or not x.get("on_unknown_value") \
                    or not x.get("on_blank") or not x.get("read_a_release_makes_through_it"):
                fail("each consumer needs code_line, kind, on_absent, on_unknown_value, on_blank and read_a_release_makes_through_it")
        by = c.get("by_kind")
        if not isinstance(by, dict) or sum(by.values()) != len(lst) or not c.get("searched_for") or not isinstance(c.get("not_searched"), list):
            fail("by_kind must account for every consumer; searched_for and not_searched must be stated")
        print("OK: %d file(s) naming it (%d consumers, %d writers, %d neither); %d consumer entries by kind %s" % (
            fn["total"], fn["consumers"], fn["writers"], fn["neither"], len(lst), by))
    elif cid == "IB153-1-AC3":
        s = a.get("short_history_count") or {}
        keys = ("security_days_not_graded_by_the_rule", "of_which_short_history_only", "of_which_repeat_rule_with_a_full_or_sufficient_window")
        if not all(isinstance(s.get(k), int) for k in keys) or s[keys[1]] + s[keys[2]] != s[keys[0]]:
            fail("short_history_count: the two parts must sum to the security-days the rule leaves ungraded")
        if not all(isinstance(s.get(k), int) for k in ("securities_ever_short_of_history", "newly_held_securities_blank_for_their_first_window",
                                                        "account_days_blank_only_for_short_history")) or not s.get("newly_held_rule_in_words") \
                or s.get("computed_by") != "the product module":
            fail("short_history_count needs the three counts, newly_held_rule_in_words, and computed_by 'the product module'")
        for k in ("product_files_edited", "builds_proposed_as_orders", "served_changes", "other_sources_asked", "claims_regraded_in_product"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("open_design_questions"), list) or not isinstance(a.get("not_established"), list):
            fail("open_design_questions and not_established must be stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        if re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text + rd.read_text(encoding="utf-8")):
            fail("an eight-digit token is in the outputs: an account id may not be written")
        print("OK: %d security-days ungraded by the rule: %d for short history only, %d by the repeat rule; %d newly held securities blank for their first window" % (
            s[keys[0]], s[keys[1]], s[keys[2]], s["newly_held_securities_blank_for_their_first_window"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
