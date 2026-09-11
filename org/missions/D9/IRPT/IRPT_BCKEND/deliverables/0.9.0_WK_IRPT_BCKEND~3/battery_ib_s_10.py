"""BATTERY IB-s-10 -- S10-AC1: section extraction certified against a paired PDF.

Seven arms: (a)-(e) from the face, (amend) from the IB-s-3 drain, (v0.11) from the L4 hand-off
release. Prints IBS10-EXTRACTION-CERTIFIED only when every arm passes, and WITHHOLDS it (rc 1)
otherwise -- a battery that cannot fail is not a measurement.

Run: timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
     0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_10.py
"""
import json
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
IR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
PKG = os.path.join(IR, "ycharts", "extract")
for p in (os.path.join(PKG, "tests"), PKG, os.path.join(IR, "_authz"),
          os.path.join(IR, "_authz", "tests"), os.path.join(IR, "_keys")):
    sys.path.insert(0, p)

import certify                       # noqa: E402
import enforce as authz              # noqa: E402
import extract                       # noqa: E402
import run_offline_suite as suite    # noqa: E402

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
    say("BATTERY IB-s-10 -- S10-AC1: typed sections, units, dates, coordinates, certified")
    say("repo: %s" % REPO.replace("\\", "/"))
    say("=" * 78)

    res = suite.main()
    backend = res["backend"]
    say("")
    say("    pdf backend: %s %s (available=%s)"
        % (backend["backend"], backend["version"], backend["available"]))
    say("    LAZY BY DESIGN: this package rides the irpt-ycharts-generate zip at its next build "
        "and pdfplumber is NOT in the python3.12 runtime, so a deployed caller reports "
        "extraction_available=false with the reason NAMED rather than dying at import.")

    # ---- (a) -------------------------------------------------------------
    head("(a) THREE VARIANTS EXTRACTED -- typed sections with units, dates and coordinates")
    say("    SECTION ROUTING, by SUBTRACTION over the census's own denominator:")
    say("      %s" % res["routing"]["subtraction"])
    say("      every one of the 33 census sections is in exactly ONE class; the classes are")
    say("      decided by the DATA'S SHAPE (a glossary row is term/definition and carries no")
    say("      unit at all; a section with zero field rows has nothing to type), not by taste")
    ok_a = True
    for v in suite.VARIANTS:
        s = res["synthetic"][v]
        say("      %-11s located %3d  units %3d of %3d  page+bbox %3d of %3d  dated %3d"
            % (v, s["located"], s["with_units"], s["located"], s["with_page_and_bbox"],
               s["located"], s["with_date"]))
        say("                  unlocated %3d %s" % (s["unlocated"],
                                                    json.dumps(s["unlocated_by_reason"])))
        ok_a = ok_a and s["located"] > 0 and s["with_units"] == s["located"] \
            and s["with_page_and_bbox"] == s["located"]
    counts = [res["synthetic"][v]["located"] for v in suite.VARIANTS]
    cols = [sorted({r["_column"] for r in res["synthetic"][v]["_result"]["sections"]})
            for v in suite.VARIANTS]
    say("    ONE ROW PER (FIELD, ENTITY COLUMN) -- the columns each variant actually yields:")
    for v, n, c in zip(suite.VARIANTS, counts, cols):
        say("      %-11s %3d row(s) across column index %s" % (v, n, c))
    scaling = (cols[0] == [0] and cols[1] == [0, 1] and cols[2] == [0, 1, 2]
               and counts[0] < counts[1] < counts[2])
    say("      column indices match the specimen's declared column count, and row counts rise "
        "monotonically: %s" % scaling)
    say("      NOT AN EXACT 1:2:3 -- and that was an over-strong predicate this battery was")
    say("      caught on. A field absent for ONE entity and present for another yields a")
    say("      different number of located rows per column (%d / %d / %d, not %d / %d / %d), so"
        % (counts[0], counts[1], counts[2], counts[0], 2 * counts[0], 3 * counts[0]))
    say("      exact scaling was never a property of the data -- it was a property of an")
    say("      imagined dataset in which every entity has every value. The absences are real")
    say("      and they are carried: MISSING_ON_PAGE below.")
    say("    AN ABSENT CELL IS NEVER A ZERO: '--' becomes MISSING_ON_PAGE with its coordinates,")
    say("      carried in `unlocated` rather than dropped (which would hide an entity) or")
    say("      zeroed (which would be a false number a client could act on).")
    say("    A DATE IS NOT A MEASUREMENT: rows that ARE a 'Data as of:' line are excluded from")
    say("      value candidacy. Without that rule a section heading harvested the DAY OF THE")
    say("      MONTH as its first value and the YEAR as its second, both certifying happily")
    say("      because the digits really were at those coordinates.")
    results["a"] = ok_a and scaling

    # ---- (b) -------------------------------------------------------------
    head("(b) CERTIFIED -- every number ties to the PDF text at its own coordinates")
    say("    THREE LEGS, graded by a module that is given ONLY the rows and the ORIGINAL bytes:")
    say("      L1 the crop at bbox renders this value   L2 the label is on the value's own row")
    say("      or directly above it                     L3 the unit is the census's own")
    ok_b = True
    for v in suite.VARIANTS:
        s = res["synthetic"][v]
        say("      %-11s %-18s %s  status=%s"
            % (v, "%d of %d CERTIFIED" % (s["certified"], s["checked"]),
               json.dumps(s["cert_by_verdict"]), s["certification_status"]))
        ok_b = ok_b and s["all_certified"]
    say("    the verdict vocabulary carries NOT_EVALUATED so an unchecked row can never be")
    say("      scored as a pass; certification_status claims CERTIFIED only when checked > 0")
    results["b"] = ok_b

    # ---- (c) -------------------------------------------------------------
    head("(c) THE DIFFERENCE CONTROL -- one number changed after extraction must FAIL")
    ok_c = True
    for v in suite.VARIANTS:
        d = res["synthetic"][v]["controls"]["difference"]
        say("      %-11s field %-22s p%-2s bbox %s" % (v, str(d["field"])[:22], d["page"],
                                                       d["bbox"]))
        say("                  %s -> %s  verdict %s  holds %s"
            % (d["value_before"], d["value_after"], d["verdict"], d["holds"]))
        ok_c = ok_c and d["holds"] and d["verdict"] == certify.FAIL_VALUE
    d = res["synthetic"]["comparison"]["controls"]["difference"]
    say("    the refusal NAMES THE FIELD AND THE COORDINATES, verbatim:")
    say("      %s" % str(d["detail"])[:150])
    say("    SECOND CONTROL, on the leg L1 cannot reach -- a value left at its own correct")
    say("      coordinates but attached to a NEIGHBOUR'S label. It certifies perfectly on")
    say("      value-at-coordinates, because the number really is printed there:")
    for v in suite.VARIANTS:
        t = res["synthetic"][v]["controls"]["transposed"]
        say("      %-11s label swapped to %-24s -> %s  holds %s"
            % (v, str(t["label_swapped_to"])[:24], t["verdict"], t["holds"]))
        ok_c = ok_c and t["holds"] and t["verdict"] == certify.FAIL_LABEL
    results["c"] = ok_c

    # ---- (d) -------------------------------------------------------------
    head("(d) NO VISUAL GUESS -- a chart-only region yields a representation, never a value")
    ok_d = True
    for v in suite.VARIANTS:
        c = res["synthetic"][v]["charts"]
        say("      %-11s %s  holds %s" % (v, c["denominator"], c["holds"]))
        ok_d = ok_d and c["holds"]
    sample = [r for r in res["synthetic"]["overview"]["_result"]["charts"]][:2]
    for row in sample:
        say("      %-40s value=%s units=%s p%s"
            % (row["section_id"][:40], row["value"], row["units"], row["page"]))
        say("        %s" % row["_representation"][:120])
    say("    the ten chart-only regions are the census's OWN zero-field sections, so the set is")
    say("      read off the data rather than chosen; certify.py grades a chart row FIRST and")
    say("      fails it CHART_REGION_EMITTED_A_VALUE if one ever carries a number")
    results["d"] = ok_d

    # ---- (e) -------------------------------------------------------------
    head("(e) SCHEMA-VALID AND LABELLED")
    ok_e = True
    for v in suite.VARIANTS:
        s = res["synthetic"][v]
        say("      %-11s AnalysisReport.sections: validated=%s over %d row(s)"
            % (v, s["schema"].get("validated"), s["schema_rows"]))
        say("                  label census: %s  holds %s"
            % (s["label_census"]["denominator"], s["label_census"]["holds"]))
        say("                  UNDATED HELD OUT: %d of %d rows"
            % (s["undated"]["held_out"], s["undated"]["total_rows"]))
        ok_e = ok_e and s["schema"].get("validated") and s["label_census"]["holds"]
    say("    WHY ROWS ARE HELD OUT RATHER THAN DATED (row W3-S11): as_of_date is REQUIRED by the")
    say("      contract and pattern-bound, but the documents do not state a date for every")
    say("      section. The only two ways to close that are to write a date the document does")
    say("      not say, or to emit fewer rows and COUNT what was held out. The first is the")
    say("      fabrication this cell exists to refuse, and the contract has no field in which a")
    say("      report-level fallback could be declared as one.")
    say("    THE TWO MARKERS ARE NEVER MIXED: 'synthetic' for the census-generated specimens,")
    say("      'vendor_synthetic_holdings' for the retained real vendor PDFs. Censused, not said.")
    m = res["manifest"]
    say("    FIXTURE MANIFEST RE-DERIVED FROM DISK (the W3-S9 lesson, applied by default):")
    say("      %d of %d rows match, %d pdf(s) on disk, %d unlisted, census sha matches %s"
        % (m["rows_matching"], m["rows_checked"], m["pdfs_on_disk"], len(m["unlisted"]),
           m["census_sha_matches"]))
    det = suite.generator_determinism()
    say("      GENERATOR DETERMINISM: %d of %d variants byte-identical across two runs (rc %d)"
        % (det["byte_identical"], det["variants"], det["rc"]))
    say("        the PDF trailer's random /ID is replaced by one derived from the content, so a")
    say("        regeneration cannot silently invalidate the manifest that pins these files")
    ok_e = ok_e and m["fresh"] and det["holds"]
    results["e"] = ok_e

    # ---- (v0.11) ---------------------------------------------------------
    head("(v0.11) THE THREE RETAINED VENDOR PDFs -- real YCharts output on synthetic holdings")
    say("    AN OPAL S3 READ, NEVER A VENDOR CALL: s3://opal-data-ycharts/research/20260911/...")
    verified = [r for r in res["vendor_inputs"] if r.get("sha_matches")]
    say("    VERIFIED BEFORE USE -- %d of %d:" % (len(verified), len(res["vendor_inputs"])))
    for r in res["vendor_inputs"]:
        if not r.get("fetched"):
            say("      %-11s FETCH REFUSED: %s" % (r["variant"], str(r.get("reason"))[:110]))
            continue
        say("      %-11s %7d bytes  sha256 %s  == pdf_validation.json %s"
            % (r["variant"], r["bytes"], r["sha256"][:16], r["sha_matches"]))
    ok_v = len(verified) == 3
    for v in suite.VARIANTS:
        s = res["vendor"][v]
        if s.get("blocked"):
            say("      %-11s BLOCKED: %s" % (v, str(s.get("reason"))[:120]))
            ok_v = False
            continue
        say("      %-11s pages %2d (declared %2d, match %s)  located %3d  %s"
            % (v, s["pages"], s["pages_declared"], s["pages_match"], s["located"],
               "%d of %d CERTIFIED" % (s["certified"], s["checked"])))
        say("                  units %d of %d | page+bbox %d of %d | dated %d | claims %s"
            % (s["with_units"], s["located"], s["with_page_and_bbox"], s["located"],
               s["with_date"], json.dumps(s["date_claims"])))
        say("                  UNCENSUSED (present in the PDF, NOT named by the census): %d"
            % s["uncensused"]["denominator"]["uncensused_found"])
        say("                  charts %s | labels %s | schema validated=%s over %d row(s)"
            % (s["charts"]["denominator"], s["label_census"]["denominator"],
               s["schema"].get("validated"), s["schema_rows"]))
        d = s["controls"]["difference"]
        say("                  DIFFERENCE CONTROL: %s %s -> %s at p%s %s -> %s (holds %s)"
            % (str(d["field"])[:20], d["value_before"], d["value_after"], d["page"], d["bbox"],
               d["verdict"], d["holds"]))
        ok_v = (ok_v and s["all_certified"] and s["pages_match"] and s["charts"]["holds"]
                and s["label_census"]["holds"] and s["schema"].get("validated")
                and d["holds"] and s["with_units"] == s["located"]
                and s["with_page_and_bbox"] == s["located"])
    say("    THE VENDOR SPECIMENS STATE THEIR OWN DATES: the real documents carry a per-section")
    say("      'Data as of:' line, so every dated vendor row is PAGE_STATED -- the strongest")
    say("      claim available, and strictly better than the census's page-level hint.")
    say("    THE UNCENSUSED LIST IS LISTED, NEVER INVENTED INTO FIELDS: these are label/number")
    say("      pairs the documents carry that this estate's field census does not name. They")
    say("      are reported as a discovery about the specimen, not added to AnalysisReport.")
    results["v011"] = ok_v

    # ---- (amend) ---------------------------------------------------------
    head("(amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE")
    say("    this cell ships NO route handler -- extract.py and certify.py are LIBRARIES that")
    say("      take bytes and return rows; the extractor rides IB-s-9's Lambda package")
    routes = {}
    census_here = authz.unguarded_routes(routes)
    say("    unguarded_routes(this cell's routes) -> %d of %d unguarded"
        % (len(census_here["unguarded"]), census_here["routes"]))
    say("      THE CENSUS IS VACUOUS: True. routes.json is IB-s-15's deliverable at")
    say("      infra/aws/terraform/investor-reporting/api/routes.json and does not exist before")
    say("      that cell lands (channel row S13, adopted from this worker's W3-S5). A 0 of 0 is")
    say("      NOT reported as a pass -- the two CONTROLS below carry the arm instead.")
    import fixtures as authz_fixtures
    directory = authz_fixtures.DIRECTORY
    binding = authz.FirmBinding(authz_fixtures.TENANT, directory["firm_id_opaque"])
    deps = authz_fixtures.Deps()
    enforcer = authz.Enforcer(binding, deps.load_directory, deps.load_ownership,
                              deps.load_policy)

    def plain_handler(request, scope):
        return {"ok": True}

    guarded = enforcer.guard("irpt_sections_read")(plain_handler)
    negative = authz.unguarded_routes({"GET /sections": plain_handler})
    positive = authz.unguarded_routes({"GET /sections": guarded})
    say("      CONTROL, an UNGUARDED handler wired to a route: %d of %d unguarded"
        % (len(negative["unguarded"]), negative["routes"]))
    say("      CONTROL, the SAME handler wrapped by guard():   %d of %d unguarded"
        % (len(positive["unguarded"]), positive["routes"]))

    good_key = extract.sections_artifact_key(binding, directory, "2332257", 0)
    say("    THE ONE FIRM-SCOPED ACT IN THIS CELL is where sections/report.json lands:")
    say("      %s" % good_key)
    bad_binding = authz.FirmBinding(authz_fixtures.TENANT, "fir_not_this_firm")
    refused_code, refused_text = None, ""
    try:
        extract.sections_artifact_key(bad_binding, directory, "2332257", 0)
    except extract.ArtifactRefused as exc:
        refused_text = str(exc)
        refused_code = refused_text.split(":")[0]
    say("    FIRM BINDING: a non-reconciling binding -> refused %s; opaque id echoed: %s"
        % (refused_code, "fir_not_this_firm" in refused_text))
    say("      %s" % refused_text[:150])

    client_name = "Whitfield Family"
    key_code, key_text = None, ""
    try:
        extract.sections_artifact_key(binding, directory, client_name, 0)
    except extract.ArtifactRefused as exc:
        key_text = str(exc)
        key_code = key_text.split(":")[0]
    request = authz.Request(headers=authz_fixtures.headers(),
                            operation="irpt_sections_read",
                            params={"client": client_name, "revision": 1})
    outcome = guarded(request)
    envelope = outcome.as_envelope() if not outcome.ok else {"ok": True}
    whole = json.dumps({"envelope": envelope, "audit": enforcer.audit,
                        "artifact_refusal": key_text})
    occurrences = whole.count(client_name)
    # THE GUARD IS ONLY WORTH ANYTHING IF WHAT IT GUARDS AGAINST IS REAL. Measured here rather
    # than asserted in a comment, because "I added a check" and "the check was needed" are two
    # different claims and only the second one is evidence.
    import keys as _keys
    probe = {}
    for label, value in (("client display name", client_name),
                         ("e-mail address", "redacted@example.com")):
        try:
            k = _keys.s3_evidence_key(authz_fixtures.TENANT, "generations",
                                      [value, "attempts", "0", "sections", "report.json"])
            probe[label] = {"accepted_by_keys": True, "key_shape": k.replace(value, "<VALUE>")}
        except Exception as exc:                                       # noqa: BLE001
            probe[label] = {"accepted_by_keys": False, "refusal": exc.__class__.__name__}
    say("    WHY THIS CELL SHAPE-CHECKS BEFORE CALLING _keys (row W3-S12) -- the gap, MEASURED:")
    for label, row in sorted(probe.items()):
        say("      _keys.s3_evidence_key(%-20s) accepted=%s  %s"
            % (label, row["accepted_by_keys"], row.get("key_shape", row.get("refusal"))))
    say("      its own docstring says 'Each is validated by shape, so a client name cannot become")
    say("      a path'. cache_key in the SAME module refuses both. _keys is not this cell's to")
    say("      edit, so this cell refuses what it would otherwise pass on.")
    keys_gap_real = all(r["accepted_by_keys"] for r in probe.values())
    say("      the gap is real (both accepted): %s" % keys_gap_real)
    say("    _keys SILENCE over the WHOLE envelope (body + reason + audit trail + this cell's")
    say("      own artifact refusal): code=%s, audit entries=%d, %d bytes,"
        % (envelope.get("code"), len(enforcer.audit), len(whole)))
    say("      OCCURRENCES OF THE REFUSED VALUE: %d" % occurrences)
    say("      artifact refusal, verbatim: %s" % key_text[:140])
    results["amend"] = (census_here["routes"] == 0 and not census_here["unguarded"]
                        and len(negative["unguarded"]) == 1 and not positive["unguarded"]
                        and refused_code == "FIRM_BINDING"
                        and "fir_not_this_firm" not in refused_text
                        and key_code == "KEY_REFUSED"
                        and envelope.get("code") == "KEY_REFUSED"
                        and len(enforcer.audit) > 0 and occurrences == 0
                        and good_key.startswith("firms/") and keys_gap_real)

    # ---- verdict ---------------------------------------------------------
    head("=" * 78)
    order = ["a", "b", "c", "d", "e", "v011", "amend"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for k in order if results[k])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBS10-EXTRACTION-CERTIFIED")
        return 0
    say("BLOCKED: not every arm passed -- IBS10-EXTRACTION-CERTIFIED withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
