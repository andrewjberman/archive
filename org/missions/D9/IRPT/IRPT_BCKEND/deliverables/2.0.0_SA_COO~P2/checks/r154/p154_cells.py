"""IRPT_BCKEND round 154 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY, CODE-ONLY order:
  IB154-1  IB-pr-458  the commentary draft store's PERSIST answer: its members today and where its shape is declared; every
                      consumer of that answer; whether the store already reads the accepted record at persist; what it returns
                      when the record carries no ticket id (CTO msg 5993).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB154-1-AC1  the persist answer: every member it returns today on each outcome (accepted, replay, each refusal), with the
               line that builds it; where its shape is declared, or that no file declares it.
  IB154-1-AC2  every consumer of that answer, by subtraction (files naming the persist operation counted and placed), each with
               what it does on an unknown member; counted by kind with no remainder.
  IB154-1-AC3  the accepted record at persist: read or not, at which line, which members are taken; what the answer carries
               today when the record has a ticket id and when it has none; the bounds; nothing proposed.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~314/"
OUT, READ = D + "IB154-1_draft_store_persist_answer.json", D + "IB154-1_DRAFT_STORE_PERSIST_ANSWER_READ.md"
CLAIMS = ("measured", "inferred", "held", "absent")


def at(x):
    return isinstance(x, str) and ":" in x


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB154"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB154-1-AC1":
        if not re.match(r"^[0-9a-f]{10,40}$", str(a.get("base_commit") or "")):
            fail("base_commit is not stated")
        p = a.get("persist_answer") or {}
        o = p.get("outcomes")
        if not isinstance(o, list) or not o or any(not x.get("outcome") or not isinstance(x.get("members"), list) or not at(x.get("built_at")) for x in o):
            fail("persist_answer.outcomes must list each outcome with its members and the line that builds it")
        if not at(p.get("entry_point")) or not p.get("how_it_is_called"):
            fail("persist_answer needs entry_point (file:line) and how_it_is_called")
        d = p.get("shape_declared")
        if not isinstance(d, dict) or d.get("declared") not in (True, False) or (d["declared"] and not d.get("where")) \
                or d.get("additional_members_forbidden") not in (True, False, None) or d.get("claim") not in CLAIMS:
            fail("persist_answer.shape_declared needs declared, where (when declared), additional_members_forbidden and a claim")
        print("OK: %d outcome(s) of the persist answer; shape declared: %s" % (len(o), d["declared"]))
    elif cid == "IB154-1-AC2":
        c = a.get("consumers_of_the_answer") or {}
        fn = c.get("files_naming_the_persist_operation") or {}
        if not all(isinstance(fn.get(k), int) for k in ("total", "consumers", "producers", "neither")) or fn["consumers"] + fn["producers"] + fn["neither"] != fn["total"]:
            fail("files_naming_the_persist_operation must count total = consumers + producers + neither")
        lst = c.get("list")
        if not isinstance(lst, list) or any(not x.get("consumer") or not at(x.get("code_line")) or not x.get("kind") or not isinstance(x.get("members_read"), list)
                                            or not x.get("on_an_unknown_member") for x in lst):
            fail("each consumer needs code_line, kind, members_read and on_an_unknown_member")
        by = c.get("by_kind")
        if not isinstance(by, dict) or sum(by.values()) != len(lst) or not c.get("searched_for") or not isinstance(c.get("not_searched"), list):
            fail("by_kind must account for every consumer; searched_for and not_searched must be stated")
        if not lst and not c.get("no_consumer_found_explained"):
            fail("no consumer is listed and no explanation is given")
        print("OK: %d file(s) naming the operation; %d consumer entries by kind %s" % (fn["total"], len(lst), by))
    elif cid == "IB154-1-AC3":
        r = a.get("accepted_record_at_persist") or {}
        if r.get("read_at_persist") not in (True, False) or r.get("claim") not in CLAIMS or not r.get("in_words") \
                or (r["read_at_persist"] and (not at(r.get("code_line")) or not isinstance(r.get("members_taken"), list))):
            fail("accepted_record_at_persist needs read_at_persist, a claim, in_words, and (when read) code_line and members_taken")
        t = a.get("ticket_id_in_the_answer_today") or {}
        for k in ("when_the_record_carries_one", "when_the_record_carries_none"):
            if not t.get(k):
                fail("ticket_id_in_the_answer_today.%s is not stated" % k)
        if t.get("claim") not in CLAIMS:
            fail("ticket_id_in_the_answer_today needs a claim")
        if not isinstance(a.get("who_invokes_persist"), list) or not a["who_invokes_persist"]:
            fail("who_invokes_persist (each caller with its identity and code line) is not stated")
        for k in ("contract_changes_proposed", "aws_calls_made", "vendor_requests_made", "product_files_edited"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not (root / READ).is_file():
            fail("not_established and the read file are required")
        print("OK: the accepted record is read at persist: %s (%s); the ticket id in the answer today is stated for both cases" % (r["read_at_persist"], r["claim"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
