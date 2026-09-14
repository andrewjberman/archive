"""BATTERY IB-rt-10 -- RT10-AC1: glyphs and dates, per-document mapping and provenance.

Four arms, (a)-(d), taken from the acceptance clause verbatim. Prints
IBRT10-GLYPHS-DATES-PROVENANCED only when every arm passes and WITHHOLDS it (rc 1) otherwise --
a battery that cannot fail is not a measurement.

WHAT THIS BATTERY IS RUN AGAINST, stated on the arm rather than buried: the three RETAINED
VENDOR PDFs are real YCharts output on SYNTHETIC HOLDINGS, read from Opal's own S3 and
hash-verified before use, and the two other specimens are generated from the field census. NO
REPRESENTATIVE REAL-CLIENT SPECIMEN EXISTS, none is manufactured here, and nothing in this
output is a certification against real client input. That absence is the standing proof gap on
FWD-4 and FWD-8 and is printed again at the foot of this run.

Run: timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
     0.9.0_WK_IRPT_BCKEND~4/battery_ib_rt_10.py
"""
import json
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
IR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
PKG = os.path.join(IR, "ycharts", "extract")
for p in (os.path.join(PKG, "tests"), PKG):
    sys.path.insert(0, p)

import certify                       # noqa: E402
import extract                       # noqa: E402
import run_offline_suite as suite    # noqa: E402

# The face's own measurement, carried here as the EXPECTATION the run is graded against rather
# than as a number to be read off this run and agreed with.
FACE_CODES = {"overview": 45, "comparison": 45, "multicomp": 46}
FACE_PAGES = {"overview": 23, "comparison": 31, "multicomp": 35}
FACE_ROUND1_UNDATED = {"comparison": (34, 81), "multicomp": (51, 108)}

results = {}
LINES = []


def say(text=""):
    LINES.append(text)
    print(text)


def head(text):
    say("")
    say(text)


def main():
    say("=" * 78)
    say("BATTERY IB-rt-10 -- RT10-AC1: glyphs and dates, per document, with provenance")
    say("repo: %s" % REPO.replace("\\", "/"))
    say("=" * 78)

    res = suite.main()
    say("")
    say("    pdf backend: %s %s (available=%s)"
        % (res["backend"]["backend"], res["backend"]["version"], res["backend"]["available"]))
    say("    font backend: %s %s (available=%s)"
        % (res["font_backend"]["backend"], res["font_backend"]["version"],
           res["font_backend"]["available"]))

    vendor_ok = [v for v in suite.VARIANTS if not res["vendor"].get(v, {}).get("blocked")]
    if len(vendor_ok) != 3:
        for v in suite.VARIANTS:
            if res["vendor"].get(v, {}).get("blocked"):
                say("    BLOCKED: vendor %-11s %s" % (v, res["vendor"][v]["reason"]))

    # ---- (a) -------------------------------------------------------------
    head("(a) PER-DOCUMENT MAPPING -- each document's own font resources, and nothing else")
    ok_a = len(vendor_ok) == 3
    pages_total = 0
    raw_cid_total = 0
    for v in suite.VARIANTS:
        spec = res["vendor"].get(v, {})
        if spec.get("blocked"):
            ok_a = False
            continue
        glyphs = spec["glyphs"]
        pages_total += spec["pages"]
        say("    %-11s pages %2d (declared %2d, match %s)  font resources %d  codes mapped %d"
            % (v, spec["pages"], spec["pages_declared"], spec["pages_match"],
               glyphs["denominator"]["font_resources"],
               glyphs["denominator"]["codes_mapped_total"]))
        for name, row in sorted(spec["font_maps"].items()):
            say("                  %-34s source=%-10s codes=%3d  program tables %s"
                % (name[:34], row["source"], row["codes_mapped"],
                   row["program_tables"] or "[]"))
        codes = glyphs["codes"]
        if len(codes) != 1:
            say("                  EXPECTED exactly one unmapped code in this document, found %d"
                % len(codes))
            ok_a = False
        for row in codes:
            record = row["record"]
            say("                  CODE %-3d  %-10s  rendered by %s on %d of %d page(s)"
                % (row["code"], row["verdict"], row["fonts"], len(row["pages"]), spec["pages"]))
            say("                    the code the face measured for this document: %d -- match %s"
                % (FACE_CODES[v], row["code"] == FACE_CODES[v]))
            say("                    sources asked: %s"
                % json.dumps(record.get("sources_asked", record.get("source"))))
            say("                    the shape of the hole in this font's own map: %s"
                % json.dumps(record.get("map_covers")))
            say("                    verdict provenance: %s" % str(record.get("provenance"))[:150])
            control = row.get("control") or {}
            say("                    CROSS-FONT CONTROL (a NEGATIVE control, never an answer): %s"
                % control.get("denominator"))
            for other in control.get("other_fonts", []):
                say("                      %-34s would_answer=%-5s %s"
                    % (other["font"][:34], other["would_answer"], other["character"]))
            # THE RULING'S TWO BRANCHES, AND THIS RUN TOOK THE SECOND. The CTO's ruling on row
            # W3-S10 is "per-document font mapping OR explicit unresolved for the fi-ligature
            # codes 45/46". The document's OWN resources were exhausted and do not state these
            # codes, so the answer is UNRESOLVED, reached by measurement. Row W4-S26.
            arm = (row["verdict"] in ("RECOVERED", "UNRESOLVED")
                   and row["code"] == FACE_CODES[v]
                   and len(row["fonts"]) == 1
                   and spec["pages_match"]
                   and (row["verdict"] == "RECOVERED"
                        or record.get("reason") in ("EXHAUSTED", "FONT_NOT_DECLARED"))
                   and control.get("other_fonts_that_would_answer", 0) > 0)
            ok_a = ok_a and arm
        emitted = spec["emitted_glyphs"]
        raw_cid_total += emitted["raw_cid_occurrences"]
        say("                  EMITTED: %s; explicit UNRESOLVED_GLYPH markers %d"
            % (emitted["denominator"], emitted["explicit_unresolved_markers"]))
        ok_a = ok_a and emitted["holds"]
    say("    RAW '(cid:' OCCURRENCES IN EVERYTHING THESE THREE DOCUMENTS EMIT: %d of %d page(s)"
        % (raw_cid_total, pages_total))
    ok_a = ok_a and raw_cid_total == 0 and pages_total == sum(FACE_PAGES.values())
    div = res["divergence"]
    say("    WHY THE SCOPE IS THE DOCUMENT AND NOT THE VENDOR -- measured across the three:")
    say("      %s" % div["denominator"])
    say("      a global replacement table would be wrong: %s" % div["a_global_table_would_be_wrong"])
    for row in div.get("diverging", [])[:4]:
        say("      code %-3d %s" % (row["code"], json.dumps(row["by_document"])))
    say("      these three files are the SAME vendor, the SAME template and the SAME day, and")
    say("      they still disagree about what most of their codes mean: a subset code is a")
    say("      property of a FILE. The cross-font controls above show the same argument one")
    say("      level down, inside a single document.")
    ok_a = ok_a and bool(div.get("a_global_table_would_be_wrong"))
    results["a"] = ok_a

    # ---- (b) -------------------------------------------------------------
    head("(b) THE NEGATIVE -- a document that USES a code its own map does not state")
    glyph = res["glyph_specimen"]
    man = res["glyph_manifest"]
    det = suite.glyph_generator_determinism()
    say("    FIXTURE, RE-DERIVED FROM DISK EVERY RUN (row W3-S9): sha matches %s, census sha "
        "matches %s, %d bytes" % (man["sha_matches"], man["census_sha_matches"],
                                  man["bytes_actual"]))
    say("      DETERMINISM: two generator runs byte-identical %s (rc %d)"
        % (det["byte_identical"], det["rc"]))
    expected = man["expected"]
    say("      the fixture DECLARES its own answer, so this arm is not another reading of the")
    say("      instrument under test: code %s is used by the content and withheld from the map"
        % expected["unmapped_code"])
    say("      (the character the document refuses to state: %r)"
        % expected["unmapped_character_the_document_withholds"])
    codes = glyph["glyphs"]["codes"]
    ok_b = (man["fresh"] and det["holds"] and len(codes) == 1
            and glyph["pages"] == expected["pages"])
    for row in codes:
        say("    MEASURED: code %-3d %-10s rendered by %s; the document's answer:"
            % (row["code"], row["verdict"], row["fonts"]))
        say("      %s" % str(row["record"].get("provenance"))[:150])
        say("      sources asked: %s" % json.dumps(row["record"].get("sources_asked")))
        ok_b = (ok_b and row["code"] == expected["unmapped_code"]
                and row["verdict"] == "UNRESOLVED")
    say("    THE EXTRACTOR REFUSES THE VALUE, with its coordinates and the marker (not a guess):")
    for row in glyph["undecoded_unlocated"]:
        say("      %-20s %-26s p%-2s bbox %s" % (row["field"][:20], row["reason"], row["page"],
                                                 row["bbox"]))
        say("        token as extracted: %r" % row["token"])
    ok_b = ok_b and len(glyph["undecoded_unlocated"]) == 1
    control = glyph["controls"]["unresolved_glyph"]
    say("    AND THE CERTIFIER REFUSES IT TOO -- the row a careless extractor WOULD have emitted,")
    say("      rebuilt at its own real coordinates and handed to the real certifier:")
    if control.get("ran"):
        say("      field %-20s p%-2s bbox %s  forced value %s"
            % (str(control["field"])[:20], control["page"], control["bbox"],
               control["forced_value"]))
        say("      verdict %s  (certified %d of %d)  holds %s"
            % (control["verdict"], control["certified"], control["checked"], control["holds"]))
        say("      refusal, verbatim: %s" % str(control["detail"])[:190])
    else:
        say("      DID NOT RUN: %s" % control.get("reason"))
    ok_b = ok_b and control.get("ran") and control.get("holds")
    say("    THE POSITIVE HALF, on the same document: %d row(s) located and %d of %d CERTIFIED,"
        % (glyph["located"], glyph["certified"], glyph["checked"]))
    say("      including a value whose every character is readable ONLY through this document's")
    say("      own CMap. The refusal is therefore specific to the withheld code and not a")
    say("      blanket failure of the specimen.")
    ok_b = ok_b and glyph["all_certified"] and glyph["located"] > 0
    results["b"] = ok_b

    # ---- (c) -------------------------------------------------------------
    head("(c) DATE CLAIMS -- whose date each row carries, and never a neighbour's")
    say("    THE ENUM, MECE over 'every date an extracted row could carry': %s"
        % list(extract.DATE_CLAIMS))
    ok_c = True
    for kind in ("vendor", "synthetic"):
        for v in suite.VARIANTS:
            spec = res[kind].get(v, {})
            if spec.get("blocked"):
                ok_c = False
                continue
            cov = spec["date_claim_coverage"]
            cen = spec["date_claim_census"]
            say("    %-9s %-11s %s" % (kind, v, cov["denominator"]))
            say("                  by claim %s | dated from a neighbour: %d"
                % (json.dumps(cov["by_claim"]), cen["neighbour_dated"]))
            say("                  report header date: %s | pages printing >1 distinct date: %s"
                % (json.dumps(spec["report_header_date"] and
                              spec["report_header_date"]["date"]),
                   json.dumps(spec["multi_date_pages"])))
            say("                  UNDATED HELD OUT: %d of %d row(s), each with document "
                "provenance" % (spec["undated"]["held_out"], spec["undated"]["total_rows"]))
            for row in spec["undated"]["provenance"][:1]:
                say("                    e.g. %s" % json.dumps(row)[:150])
            ok_c = ok_c and cov["holds"] and cen["holds"]
    say("    THE ROUND-1 NUMBER, REPRODUCED FROM THIS RUN'S OWN ROWS (not recalled):")
    for v in suite.VARIANTS:
        spec = res["vendor"].get(v, {})
        if spec.get("blocked"):
            continue
        base = spec["round1_baseline"]
        want = FACE_ROUND1_UNDATED.get(v)
        say("      %-11s %s | by round-1 claim %s%s"
            % (v, base["denominator"], json.dumps(base["by_round1_claim"]),
               ("  == the face's %d of %d: %s" % (want[0], want[1],
                                                  (base["undated"], base["sections"]) == want))
               if want else ""))
        if want:
            ok_c = ok_c and (base["undated"], base["sections"]) == want
    say("    WHAT MOVED, AND WHY IT IS AN IMPROVEMENT RATHER THAN A DRIFT: round 1 took the")
    say("      PAGE'S FIRST date line and, failing that, the FIELD CENSUS's date -- a different")
    say("      document's statement about this one. Measured here: %s"
        % json.dumps({v: res["vendor"][v]["round1_baseline"]["by_round1_claim"]
                      for v in vendor_ok}))
    overview = res["vendor"].get("overview", {})
    if overview and not overview.get("blocked"):
        on_multi = sum(1 for r in overview["_result"]["sections"]
                       if str(r["page"]) in overview["multi_date_pages"])
        say("      and on the overview specimen %d of %d emitted rows sit on a page printing TWO"
            % (on_multi, overview["located"]))
        say("      different 'Data as of' dates, so round 1 gave every one of them whichever")
        say("      date came first in the text stream. That is the neighbour's date.")
    say("    THE MUTANT -- a row given a date its OWN PAGE really prints, for another block:")
    ran_neighbour = 0
    for kind in ("vendor", "synthetic"):
        for v in suite.VARIANTS:
            spec = res[kind].get(v, {})
            if spec.get("blocked"):
                continue
            nd = spec["controls"]["neighbour_date"]
            if not nd.get("ran"):
                say("      %-9s %-11s VACUOUS, not a pass: %s" % (kind, v,
                                                                  str(nd["reason"])[:96]))
                continue
            ran_neighbour += 1
            say("      %-9s %-11s %s: %s -> %s  verdict %s  holds %s"
                % (kind, v, str(nd["section_id"])[:26], nd["date_before"], nd["date_after"],
                   nd["verdict"], nd["holds"]))
            ok_c = ok_c and nd["holds"]
    glyph_nd = glyph["controls"]["neighbour_date"]
    if glyph_nd.get("ran"):
        ran_neighbour += 1
        say("      %-9s %-11s %s: %s -> %s  verdict %s  holds %s"
            % ("fixture", "unmapped", str(glyph_nd["section_id"])[:26],
               glyph_nd["date_before"], glyph_nd["date_after"], glyph_nd["verdict"],
               glyph_nd["holds"]))
        ok_c = ok_c and glyph_nd["holds"]
        say("        %s" % str(glyph_nd["detail"])[:190])
    say("      the mutation RAN on %d specimen(s); a specimen with no page carrying two different"
        % ran_neighbour)
    say("      dates cannot exercise it and is printed VACUOUS above, never folded into a pass.")
    ok_c = ok_c and ran_neighbour >= 2
    say("    THE SECOND MUTANT -- the date kept, the PROVENANCE moved past an intervening line")
    say("      (the leg that value-at-coordinates cannot reach: the RIGHT date of the WRONG block)")
    ran_shift = 0
    for kind in ("vendor", "synthetic"):
        for v in suite.VARIANTS:
            spec = res[kind].get(v, {})
            if spec.get("blocked"):
                continue
            sp = spec["controls"]["shifted_provenance"]
            if not sp.get("ran"):
                continue
            ran_shift += 1
            say("      %-9s %-11s %s -> %s  verdict %s  holds %s"
                % (kind, v, sp["provenance_before"], sp["provenance_after"], sp["verdict"],
                   sp["holds"]))
            ok_c = ok_c and sp["holds"] and sp["verdict"] == certify.FAIL_DATE_NEIGHBOUR
    say("      ran on %d specimen(s)" % ran_shift)
    ok_c = ok_c and ran_shift >= 1
    results["c"] = ok_c

    # ---- (d) -------------------------------------------------------------
    head("(d) SCHEMA-VALID -- both published copies, and the added property byte-identical")
    parity = res["schema_parity"]
    say("    %s" % parity["denominator"])
    for name in sorted(parity["present_in"]):
        say("      %-13s present=%-5s %4d byte(s) sha256 %s"
            % (name, parity["present_in"][name], parity["bytes"][name], parity["sha256"][name]))
    say("      the two FILES are NOT byte-equal and are not meant to be: the published copy")
    say("      carries its own $id and a contract_version const. The claim that matters to a")
    say("      consumer is narrower and is the one measured: the PROPERTY THIS CELL ADDED is")
    say("      identical in both.")
    ok_d = parity["holds"]
    for kind in ("vendor", "synthetic"):
        for v in suite.VARIANTS:
            spec = res[kind].get(v, {})
            if spec.get("blocked"):
                ok_d = False
                continue
            sch = spec["schema"]
            say("    %-9s %-11s validated=%-5s over %d row(s) against %d published copy(ies)"
                % (kind, v, sch.get("validated"), sch["rows"], sch.get("copies", 0)))
            for name, row in sorted((sch.get("by_copy") or {}).items()):
                if not row["validated"]:
                    say("        %-13s REFUSED: %s" % (name, str(row["reason"])[:120]))
            ok_d = ok_d and sch.get("validated")
    sch = glyph["schema"]
    say("    %-9s %-11s validated=%-5s over %d row(s) against %d published copy(ies)"
        % ("fixture", "unmapped", sch.get("validated"), sch["rows"], sch.get("copies", 0)))
    ok_d = ok_d and sch.get("validated")
    say("    additionalProperties:false HOLDS with the new property, which is the whole reason")
    say("      it was added to the CONTRACT rather than carried in a private key: a producer")
    say("      that emitted date_claim without this edit would fail validation on BOTH sides.")
    say("    LABEL CENSUS -- the two provenance markers are never mixed:")
    for kind in ("vendor", "synthetic"):
        for v in suite.VARIANTS:
            spec = res[kind].get(v, {})
            if spec.get("blocked"):
                continue
            say("      %-9s %-11s %s  holds %s" % (kind, v, spec["label_census"]["denominator"],
                                                   spec["label_census"]["holds"]))
            ok_d = ok_d and spec["label_census"]["holds"]
    results["d"] = ok_d

    # ---- verdict ---------------------------------------------------------
    head("=" * 78)
    order = ["a", "b", "c", "d"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for k in order if results[k])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("")
    say("  THE STANDING PROOF GAP, RESTATED RATHER THAN LEFT TO BE INFERRED: every specimen")
    say("  above is a SYNTHETIC-HOLDINGS vendor document or a census-generated fixture. No")
    say("  representative real-client PDF exists in this estate, none was manufactured, and")
    say("  nothing here is a certification against real client input (FWD-4, FWD-8).")
    say("=" * 78)
    if passed == len(order):
        say("IBRT10-GLYPHS-DATES-PROVENANCED")
        return 0
    say("BLOCKED: not every arm passed -- IBRT10-GLYPHS-DATES-PROVENANCED withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
