"""DSGN_IRPTV1 round 30 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6344: the round list after the second walk.

Cells: IV-e-118 a page never prints an unmapped code as a title (where the census names nothing the card takes its section's
name; the word for source_chart_representation lands in the census, proposed by the worker); IV-e-119 a READ, no build: for the
46 cards sharing one title, does section_id through the census give distinct names, and how many stay shared.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV118-AC1  ~66/UNMAPPED_TITLE_RULE.json: rule {file, line (int), unmapped_code_printed false}; chart_card {title_from
             "SECTION_NAME", word_proposed, word_basis}; census {file, entries_added (int >= 1), section_names_unchanged 33,
             drift_test_passes true}; test {file, mutant_failed true}; lint_errors 0; typecheck_errors 0; suite_base.fail and
             suite_after.fail ints with after no greater than base and suite_after.new_failing_ids []; screenshots (1 or more,
             each an existing file) with screenshot_read true; product_files_changed non-empty, all under
             src/pages/InvestorReporting/; portal_commit a 40-hex string.
  IV119-AC1  ~67/SHARED_TITLE_46.json: product_change false; cards (int > 0); source (SERVED_ANSWER / PRODUCER_RULE_ON_CENSUS /
             BOTH) with source_basis; named (int) + unnamed (int) == cards; distinct_names (int); still_shared (int, the cards
             whose resolved name another of the cards also carries, plus the unnamed) with 0 <= still_shared <= cards; verdict
             ALL_SEPARATE (only when still_shared is 0) / SOME_SHARED (only when it is above 0) / NOT_ESTABLISHED; method.
"""
import json
import re
import sys
from pathlib import Path

M = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/"


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV30"))
        sys.exit(1)

    def record(folder, name):
        p = root / (M + folder) / name
        if not p.is_file():
            fail("no record %s/%s" % (folder, name))
        return json.loads(p.read_bytes().decode("utf-8")), root / (M + folder)

    if cid == "IV118-AC1":
        r, folder = record("0.9.0_WK_DSGN_IRPTV1~66", "UNMAPPED_TITLE_RULE.json")
        ru = r.get("rule") or {}
        if not str(ru.get("file") or "").strip() or not is_int(ru.get("line")) or ru.get("unmapped_code_printed") is not False:
            fail("rule needs its file, line and unmapped_code_printed false")
        ch = r.get("chart_card") or {}
        if ch.get("title_from") != "SECTION_NAME" or not str(ch.get("word_proposed") or "").strip() or not str(ch.get("word_basis") or "").strip():
            fail("chart_card needs title_from SECTION_NAME, the proposed word and its basis")
        ce = r.get("census") or {}
        if not str(ce.get("file") or "").strip() or not is_int(ce.get("entries_added")) or ce["entries_added"] < 1 \
                or ce.get("section_names_unchanged") != 33 or ce.get("drift_test_passes") is not True:
            fail("census %r" % {k: ce.get(k) for k in ("entries_added", "section_names_unchanged", "drift_test_passes")})
        t = r.get("test") or {}
        if not str(t.get("file") or "").strip() or t.get("mutant_failed") is not True:
            fail("test needs its file and a mutant that failed")
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        sb, sa = r.get("suite_base") or {}, r.get("suite_after") or {}
        if not is_int(sb.get("fail")) or not is_int(sa.get("fail")) or sa["fail"] > sb["fail"] or sa.get("new_failing_ids") != []:
            fail("suite: base fail %r, after fail %r, new_failing_ids %r" % (sb.get("fail"), sa.get("fail"), sa.get("new_failing_ids")))
        shots = r.get("screenshots") or []
        if not shots or r.get("screenshot_read") is not True or any(not (folder / str(s)).is_file() for s in shots):
            fail("screenshots must each exist in the worker's folder and be read")
        pf = [str(x).replace("\\", "/") for x in (r.get("product_files_changed") or [])]
        if not pf or any("src/pages/InvestorReporting/" not in x for x in pf):
            fail("product_files_changed %r" % pf)
        if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("portal_commit") or "")):
            fail("portal_commit %r" % r.get("portal_commit"))
        print("OK: no unmapped code is printed as a title (rule at %s:%d); the chart card takes its section's name; word proposed for the census: %r; %d screenshot(s) read"
              % (ru["file"], ru["line"], ch["word_proposed"], len(shots)))
    elif cid == "IV119-AC1":
        r, _ = record("0.9.0_WK_DSGN_IRPTV1~67", "SHARED_TITLE_46.json")
        if r.get("product_change") is not False:
            fail("product_change %r" % r.get("product_change"))
        keys = ("cards", "named", "unnamed", "distinct_names", "still_shared")
        if any(not is_int(r.get(k)) for k in keys) or r["cards"] < 1 or r["named"] + r["unnamed"] != r["cards"] or r["still_shared"] > r["cards"]:
            fail("cards, named + unnamed == cards, distinct_names and still_shared are required")
        if r.get("source") not in ("SERVED_ANSWER", "PRODUCER_RULE_ON_CENSUS", "BOTH") or not str(r.get("source_basis") or "").strip() \
                or not str(r.get("method") or "").strip():
            fail("source, source_basis and method are required")
        v = r.get("verdict")
        if v not in ("ALL_SEPARATE", "SOME_SHARED", "NOT_ESTABLISHED") or (v == "ALL_SEPARATE" and r["still_shared"] != 0) \
                or (v == "SOME_SHARED" and r["still_shared"] == 0):
            fail("verdict %r against still_shared %r" % (v, r["still_shared"]))
        print("OK: %d card(s) read from %s: %d named, %d distinct name(s), %d still shared; verdict %s"
              % (r["cards"], r["source"], r["named"], r["distinct_names"], r["still_shared"], v))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
