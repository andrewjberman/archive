"""IRPT_BCKEND round 163 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msg 6379):
  IB163-1  IB-pr-469  what a column of a vendor section IS: where the producer could know it, one stored report's section ids
                      counted by code, and every consumer of the section id's shape.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB163-1-AC1  for each of S01, S03, S18, S14, S15, S16: where the column's label is in the source, with a verdict from the
               closed set, and a file:line that exists.
  IB163-1-AC2  one stored report's section ids counted by section code, by slug and by column (or a refusal stated, with
               the address tried), and the S18 count set against the 36 the rule predicts.
  IB163-1-AC3  every consumer of the section id's shape, each with a file:line that exists, a census denominator, and the
               bounds (nothing invoked, no sign-in, no figure and no account written).
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~324/"
OUT, READ = D + "IB163-1_column_meaning.json", D + "IB163-1_COLUMN_MEANING_READ.md"
CODES = ("S01", "S03", "S18", "S14", "S15", "S16")
VERDICTS = ("READ_AND_DROPPED", "ON_THE_PAGE_NEVER_READ", "NOT_ON_THE_PAGE", "HELD_ELSEWHERE_BY_THE_PRODUCER", "NOT_ESTABLISHED")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB163"))
        sys.exit(1)

    def cite_ok(c):
        m = re.match(r"^(.+?):(\d+)", str(c))
        if not m:
            return False
        p = root / m.group(1)
        if not p.is_file():
            p = root / "portal" / m.group(1)
        return p.is_file() and int(m.group(2)) <= len(p.read_text(encoding="utf-8", errors="replace").splitlines())

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB163-1-AC1":
        t = a.get("column_label_by_section_code")
        if not isinstance(t, dict) or set(t) != set(CODES):
            fail("column_label_by_section_code must carry exactly %s" % (CODES,))
        for k, v in t.items():
            if v.get("column_is") not in ("ENTITY", "PERIOD", "OTHER") or v.get("verdict") not in VERDICTS or not v.get("in_words"):
                fail("%s: column_is, a verdict of %s, and in_words" % (k, VERDICTS))
            if v["verdict"] != "NOT_ESTABLISHED" and not all(cite_ok(c) for c in (v.get("cites") or [None])):
                fail("%s: every cite must be file:line that exists" % k)
        print("OK: " + "; ".join("%s %s %s" % (k, t[k]["column_is"], t[k]["verdict"]) for k in CODES))
    elif cid == "IB163-1-AC2":
        s = a.get("stored_report")
        if not isinstance(s, dict) or s.get("read") not in (True, False) or not s.get("address_rule_in_words"):
            fail("stored_report {read, address_rule_in_words}")
        if s["read"]:
            by = s.get("sections_by_code")
            if not isinstance(by, dict) or not by or sum(by.values()) != s.get("sections_total"):
                fail("sections_by_code must sum to sections_total")
            e = s.get("s18")
            if not isinstance(e, dict) or e.get("predicted_by_the_rule") != 36 or e.get("stored") != by.get("S18", 0) or sum((e.get("by_column") or {}).values()) != e["stored"] or not e.get("difference_in_words"):
                fail("s18 {stored (equal to sections_by_code.S18), predicted_by_the_rule 36, by_column summing to stored, difference_in_words}")
            print("OK: one stored report read; %d sections; S18 %d against 36" % (s["sections_total"], e["stored"]))
        else:
            if not s.get("refusal_in_words") or not s.get("address_tried_shape"):
                fail("a report not read states refusal_in_words and address_tried_shape")
            print("OK: no stored report was read; the refusal is stated")
    elif cid == "IB163-1-AC3":
        c = a.get("consumers_of_the_section_id_shape")
        if not isinstance(c, list) or not c:
            fail("consumers_of_the_section_id_shape is empty")
        for x in c:
            if not cite_ok(x.get("cite")) or x.get("reads_the_shape_how") not in ("SPLITS_OR_PARSES", "COMPARES_WHOLE", "BUILDS_IT", "DISPLAYS_ONLY") or not x.get("in_words"):
                fail("each consumer: a cite that exists, reads_the_shape_how, in_words (%r)" % (x.get("cite"),))
        d = a.get("consumer_census")
        if not isinstance(d, dict) or not d.get("pattern") or not isinstance(d.get("files_searched"), int) or not isinstance(d.get("files_with_a_hit"), int):
            fail("consumer_census {pattern, files_searched, files_with_a_hit}")
        for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "product_files_edited"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not (root / READ).is_file() or not a.get("base_commit"):
            fail("not_established, base_commit and the read file")
        print("OK: %d consumer(s) cited over %d file(s) searched; nothing invoked, no figure written" % (len(c), d["files_searched"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
