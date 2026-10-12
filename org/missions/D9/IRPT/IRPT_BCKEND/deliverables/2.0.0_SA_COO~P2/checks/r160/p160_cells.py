"""IRPT_BCKEND round 160 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of three READ-ONLY orders, disjoint write sets
(CTO msg 6245, PRD v0.46: three reads before any cell; no build):
  IB160-1  IB-pr-464  (b) the performance route's reader, per window and per composed firm: accounts with one or more excluded
                      days, and whether those days are the account's first day or interior days.
  IB160-2  IB-pr-465  (a) whether the producer function's network reaches the vendor, read from its configuration.
  IB160-3  IB-pr-466  (c) the pages that render the route's returns, and what each shows of the claim, absences and exclusions.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Every criterion FAILs at base.
  IB160-1-AC1  per entry and per window: accounts read, accounts with an excluded day, summing with no remainder with those
               with none and those the reader refuses; the windows are the reader's own, named from its code.
  IB160-1-AC2  each account with an excluded day placed in exactly one position class (first day only, interior only, both,
               last day) summing to the accounts with an excluded day; the claim the reader gives each class counted.
  IB160-1-AC3  the arm said plainly, a control, and the bounds (no invoke, no sign-in, no account written).
  IB160-2-AC1  the function's network as configured: in a VPC or not, with the subnets' default routes and the security
               group's egress read; one of four words for reach, with its claim.
  IB160-2-AC2  what a run-time fetch would use (the library, the hosts) read from the reader's code, and whether the package
               carries that library; the bounds.
  IB160-3-AC1  every page or component that renders the route's returns, by subtraction (files naming the route or its
               payload's members counted and placed), each with what it shows of claim, absences and days_excluded.
  IB160-3-AC2  the portal checkout's commit stated, what was not searched stated, the bounds.
"""
import json
import re
import sys
from pathlib import Path

B = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
O1 = B + "0.9.0_WK_IRPT_BCKEND~319/IB160-1_reader_excluded_days.json"
O2 = B + "0.9.0_WK_IRPT_BCKEND~320/IB160-2_producer_network_reach.json"
O3 = B + "0.9.0_WK_IRPT_BCKEND~321/IB160-3_pages_rendering_returns.json"
CLAIMS = ("measured", "inferred", "held", "absent")
POS = ("first_day_only", "interior_only", "first_and_interior", "last_day_involved")
REACH = ("REACHES", "DOES_NOT_REACH", "REACHES_ONLY_THROUGH_A_NAMED_PATH", "CANNOT_BE_TOLD_FROM_CONFIGURATION")


def at(x):
    return isinstance(x, str) and ":" in x


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB160"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid.startswith("IB160-1"):
        a = load(O1)
        cells = a.get("per_entry_and_window")
        if not isinstance(cells, list) or not cells:
            fail("per_entry_and_window is empty")
        if cid == "IB160-1-AC1":
            if not isinstance(a.get("windows_from_code"), list) or not a["windows_from_code"] or not at(a.get("windows_code_line")):
                fail("windows_from_code and windows_code_line")
            for c in cells:
                if not c.get("entry") or not c.get("window") or not all(isinstance(c.get(k), int) for k in (
                        "accounts_read", "accounts_with_an_excluded_day", "accounts_with_none", "accounts_the_reader_refuses")):
                    fail("each cell needs entry, window and the four account counts")
                if c["accounts_with_an_excluded_day"] + c["accounts_with_none"] + c["accounts_the_reader_refuses"] != c["accounts_read"]:
                    fail("%s/%s: the three kinds do not sum to accounts_read" % (c["entry"], c["window"]))
            print("OK: %d entry-window cell(s); " % len(cells) + "; ".join("%s %s: %d of %d" % (
                c["entry"], c["window"], c["accounts_with_an_excluded_day"], c["accounts_read"]) for c in cells[:8]))
        elif cid == "IB160-1-AC2":
            for c in cells:
                p = c.get("position_of_the_excluded_days") or {}
                if set(p) != set(POS) or sum(p.values()) != c.get("accounts_with_an_excluded_day"):
                    fail("%s/%s: position classes must be exactly %s and sum to the accounts with an excluded day" % (c.get("entry"), c.get("window"), POS))
                cl = c.get("claim_the_reader_gives") or {}
                if not isinstance(cl, dict) or sum(cl.values()) != c["accounts_with_an_excluded_day"]:
                    fail("%s/%s: claim_the_reader_gives must count every account with an excluded day" % (c["entry"], c["window"]))
                if not isinstance(c.get("excluded_days_per_account_distribution"), dict):
                    fail("%s/%s: excluded_days_per_account_distribution" % (c["entry"], c["window"]))
            if not a.get("position_rule_in_words") or not isinstance(a.get("status_values"), dict):
                fail("position_rule_in_words and status_values")
            print("OK: every account with an excluded day is placed by position and by the claim the reader gives it")
        elif cid == "IB160-1-AC3":
            if a.get("arm") not in ("READER_CODE_OVER_SERVED_GOLD",) or not a.get("arm_in_words") or not (a.get("control") or {}).get("what"):
                fail("arm, arm_in_words and a control")
            for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written"):
                if a.get(k) != 0:
                    fail("%s must be 0" % k)
            if not isinstance(a.get("not_established"), list) or not (root / O1.replace("IB160-1_reader_excluded_days.json", "IB160-1_READER_EXCLUDED_DAYS_READ.md")).is_file():
                fail("not_established and the read file")
            print("OK: the reader's own code over the served gold; a control; nothing invoked or written")
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("IB160-2"):
        a = load(O2)
        if cid == "IB160-2-AC1":
            n = a.get("network") or {}
            if n.get("in_a_vpc") not in (True, False) or not a.get("function") or not a.get("read_at_utc"):
                fail("function, read_at_utc and network.in_a_vpc")
            if n["in_a_vpc"] and (not isinstance(n.get("subnets"), list) or not n["subnets"] or any(
                    not s.get("default_route_target_class") for s in n["subnets"]) or not isinstance(n.get("security_group_egress"), list)):
                fail("a VPC function needs each subnet's default_route_target_class and the security groups' egress")
            if a.get("reach") not in REACH or a.get("claim") not in CLAIMS or not a.get("reason"):
                fail("reach in %s, a claim and a reason" % (REACH,))
            if a["reach"] == "REACHES" and a["claim"] == "measured" and a.get("a_call_was_made_from_the_function") is not False:
                fail("REACHES is from configuration; no call is made from the function")
            print("OK: %s in a VPC: %s; reach: %s (%s)" % (a["function"], n["in_a_vpc"], a["reach"], a["claim"]))
        elif cid == "IB160-2-AC2":
            f = a.get("a_run_time_fetch_would_use") or {}
            if not f.get("library") or not isinstance(f.get("hosts"), list) or not at(f.get("code_line")) \
                    or a.get("package_carries_the_library") not in (True, False, None) or not isinstance(a.get("other_candidate_functions"), list):
                fail("a_run_time_fetch_would_use (library, hosts, code_line), package_carries_the_library and other_candidate_functions")
            for k in ("functions_invoked", "aws_writes_made", "vendor_calls_made", "sign_ins_made"):
                if a.get(k) != 0:
                    fail("%s must be 0" % k)
            if not isinstance(a.get("not_established"), list):
                fail("not_established")
            print("OK: a fetch would use %s; the package carries it: %r; nothing invoked or called" % (f["library"], a["package_carries_the_library"]))
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("IB160-3"):
        a = load(O3)
        if cid == "IB160-3-AC1":
            fn = a.get("files_naming_the_route_or_its_payload") or {}
            if not all(isinstance(fn.get(k), int) for k in ("total", "render", "fetch_or_adapt", "neither")) or fn["render"] + fn["fetch_or_adapt"] + fn["neither"] != fn["total"]:
                fail("files_naming_the_route_or_its_payload: total = render + fetch_or_adapt + neither")
            pg = a.get("pages")
            if not isinstance(pg, list) or any(not x.get("page_or_component") or not at(x.get("code_line")) or not x.get("what_it_renders")
                                               or not x.get("shows_claim") or not x.get("shows_absences") or not x.get("shows_days_excluded") for x in pg):
                fail("pages must list each page with code_line, what_it_renders, shows_claim, shows_absences and shows_days_excluded")
            if not pg and not a.get("no_page_found_explained"):
                fail("no page is listed and no explanation is given")
            print("OK: %d file(s) naming it (%d render, %d fetch or adapt, %d neither); %d page(s) listed" % (
                fn["total"], fn["render"], fn["fetch_or_adapt"], fn["neither"], len(pg)))
        elif cid == "IB160-3-AC2":
            if not re.match(r"^[0-9a-f]{7,40}$", str(a.get("portal_commit") or "")) or not a.get("portal_checkout") or not a.get("searched_for") \
                    or not isinstance(a.get("not_searched"), list) or not isinstance(a.get("not_established"), list):
                fail("portal_commit, portal_checkout, searched_for, not_searched and not_established")
            for k in ("product_files_edited", "sign_ins_made", "pages_opened_in_a_browser"):
                if a.get(k) != 0:
                    fail("%s must be 0" % k)
            print("OK: portal at %s; nothing edited, signed in or opened" % a["portal_commit"][:10])
        else:
            fail("unknown criterion %r" % cid)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
