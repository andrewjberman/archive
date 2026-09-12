#!/usr/bin/env python3
"""IB-rt-11 battery -- RT11-AC1. Intake currency and unit controls: quarantine over relabeling.

  Serial: 0.9.0_WK_IRPT_BCKEND~3
  Order : IRPT_BCKEND.TO-IB-rt-11

Invocation the task order names:
    timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
        0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_11.py

THE ACCEPTANCE TOKEN IS PRINTED ONLY WHEN EVERY CHECK PASSES, and it is never printed
negated. `RT11-AC1`'s `<expect>` is graded as a REGEX over this output, so a line reading
"<token>: NOT ASSERTED" would MATCH and grade a failing run PASS.

THE ARMS:
  (a) FOUR OF FOUR   the non-USD, subtotal, multi-sheet and ambiguous-total specimens each
                     produce their own finding WITH ITS SOURCE CELL and enter quarantine.
  (b) DIFFERENCE     a relabeling build converts CAD to the supported currency and FAILS the
                     reconcile; the correct build holds. Both printed, and the ROW-COUNT leg
                     is printed beside the currency leg to show it passes the defect.
  (c) PROVENANCE     a human correction on a quarantined row lands on r+1 with who / when /
                     from-what; r is hash-identical before and after; a RE-PARSE carries the
                     correction forward instead of overwriting it.
  (d) ROUND 1 HOLDS  the five round-1 specimens parse to digests identical to the parser at a
                     PIN -- both sides re-derived here, never compared to a hardcoded hash --
                     and round 1's own battery still reads ARMS 6 of 6.
  (e) WHERE THE CHECK RUNS   the controls are re-run in a flat /var/task-shaped directory in a
                     FRESH interpreter with the repo stripped from sys.path, plus the negative
                     arm: with the policy file absent the parser REFUSES rather than defaulting
                     to the supported currency.

WHICH COORDINATE EACH CHECK READS -- the question the adjacent cell's row W4-S28 is about.
Round 1 dated 15 of 61 rows from a neighbouring block and every one passed all three
certification legs, because a date sits at none of the coordinates those legs inspect. Arm (b)
is this battery's answer: it prints the row-count reconciliation AND the currency
reconciliation side by side for the same defect, and shows the first one passing it.

EVERY SPECIMEN IS SYNTHETIC AND ADVERSARIAL BY CONSTRUCTION. No real advisor-supplied workbook
exists in this repository and none was manufactured to look like one. Passing here is a
statement about the controls, NOT a certification against real client input -- arm (a) prints
that sentence rather than leaving it to be inferred.

NO NETWORK CALL OF ANY KIND. This cell deploys nothing and reads no AWS plane.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                      text=True, check=True).stdout.strip()
INTAKE = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "intake")
FIX = os.path.join(INTAKE, "fixtures", "holdings")
GENERATOR = os.path.join(FIX, "generate_rt11_specimens.py")
ROUND1_BATTERY = os.path.join(
    REPO, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables",
    "0.9.0_WK_IRPT_BCKEND~3", "battery_ib_s_7.py")

sys.path.insert(0, INTAKE)
import corrections                      # noqa: E402
import parse                            # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(INTAKE), "_authz"))
sys.path.insert(0, os.path.join(os.path.dirname(INTAKE), "_authz", "tests"))
import enforce as authz                 # noqa: E402
import fixtures as authz_fixtures       # noqa: E402

FAILURES = []
ROUND1 = ["holdings_clean.csv", "holdings_no_header.csv", "holdings_share_class.csv",
          "holdings_unmatched.csv", "holdings_weights.xlsx"]
RT11 = ["holdings_non_usd.csv", "holdings_subtotals.csv", "holdings_ambiguous_total.csv",
        "holdings_multi_sheet.xlsx"]
MAPPING = parse.load_mapping(os.path.join(FIX, "security_mapping.json"))
REQUEST_ID = "REQ-" + "ab" * 12


def check(label, ok, detail=""):
    print("  %-7s %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  --  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def specimen(name):
    with open(os.path.join(FIX, name), "rb") as fh:
        return fh.read()


def run(name, **kw):
    return parse.parse_holdings(specimen(name), name, "att-%s" % name, mapping=MAPPING, **kw)


def codes(result):
    return sorted(f["code"] for f in result.findings)


def finding(result, code):
    return next((f for f in result.findings if f["code"] == code), None)


# --------------------------------------------------------------------------- a

# The control each specimen is FOR, and the finding that IS that control. Declared here so the
# arm reads a TABLE rather than a sequence of assertions -- a specimen whose control does not
# fire is a named gap, not a missing line of code.
CONTROLS = [
    ("holdings_non_usd.csv", "UNSUPPORTED_CURRENCY",
     "CAD established at two agreeing coordinates; not in the supported set"),
    ("holdings_subtotals.csv", "SUBTOTAL_ROW_PRESENT",
     "a subtotal row excluded from the computed total"),
    ("holdings_multi_sheet.xlsx", "MULTI_SHEET_WORKBOOK",
     "2 worksheets, 1 read; the unread sheet named"),
    ("holdings_ambiguous_total.csv", "AMBIGUOUS_TOTAL",
     "two disagreeing stated totals; the parser picks NEITHER"),
]


def arm_a():
    print()
    print("(a) FOUR OF FOUR -- each control, its own finding, its source cell, and quarantine")
    print("      SPECIMEN PROVENANCE, stated on the arm: every specimen below is SYNTHETIC and")
    print("      ADVERSARIAL BY CONSTRUCTION -- written to hit a named control. No real")
    print("      advisor-supplied workbook exists in this repository and none was manufactured")
    print("      to look like one. This is a result about the controls, NOT a certification")
    print("      against real client input.")
    fired = 0
    for name, code, why in CONTROLS:
        result = run(name)
        f = finding(result, code)
        has_source = bool(f and f.get("_source"))
        quarantined = result.needs_correction
        print("      %-30s %-22s source=%-34s quarantined=%s"
              % (name, code, (f or {}).get("_source", "<none>"), quarantined))
        ok = check("a %s -> %s (%s)" % (name, code, why),
                   bool(f) and has_source and quarantined,
                   "findings: %s" % ", ".join(sorted(set(codes(result)))))
        fired += bool(ok)
    check("a four controls fired: %d of %d" % (fired, len(CONTROLS)),
          fired == len(CONTROLS),
          "denominator is the declared control table, not the findings that happened to appear")

    # THE COORDINATE EVIDENCE. A finding is only as good as the place it looked.
    print()
    print("      WHICH COORDINATE ESTABLISHED (or refused to establish) THE CURRENCY:")
    non_usd = run("holdings_non_usd.csv")
    multi = run("holdings_multi_sheet.xlsx")
    for label, res in (("holdings_non_usd.csv", non_usd), ("holdings_multi_sheet.xlsx", multi)):
        for m in res.money_rows:
            print("        %-28s %s  state=%-11s currency=%-6s coordinates_read=%s"
                  % (label, m["cell"], m["state"], m["currency"] or "-",
                     ",".join(m["coordinates_read"])))
    established = [m for m in non_usd.money_rows if m["state"] == "ESTABLISHED"]
    check("a the non-USD currency is ESTABLISHED at a coordinate, not inferred: %d of %d money "
          "row(s), currency=%s" % (len(established), len(non_usd.money_rows),
                                   sorted({m["currency"] for m in established})),
          len(established) == len(non_usd.money_rows) == 3
          and {m["currency"] for m in established} == {"CAD"},
          "coordinates: %s" % ", ".join(sorted({c for m in established
                                                for c in m["coordinates_read"]})))
    check("a the values are KEPT and NO unit is claimed -- quarantine, not deletion and not "
          "relabeling: %d holding(s), units=%s"
          % (len(non_usd.normalized_holdings),
             sorted({str(h["quantity"]["units"]) for h in non_usd.normalized_holdings})),
          len(non_usd.normalized_holdings) == 3
          and all(h["quantity"]["units"] is None for h in non_usd.normalized_holdings)
          and all(h["quantity"]["value"] for h in non_usd.normalized_holdings),
          "an unsupported position is never silently removed (endpoint constraint)")
    ambiguous = [m for m in multi.money_rows if m["state"] == "AMBIGUOUS"]
    check("a the xlsx NUMBER FORMAT coordinate is read, and a bare symbol there does NOT "
          "establish: %d of %d money row(s) AMBIGUOUS"
          % (len(ambiguous), len(multi.money_rows)),
          len(ambiguous) == len(multi.money_rows) == 3
          and all("XLSX_NUMBER_FORMAT" in m["coordinates_read"] for m in ambiguous),
          "this is the coordinate a <v>-only reader cannot see: the stored value is a bare "
          "number and the symbol lives in the format")
    amb_total = run("holdings_ambiguous_total.csv")
    check("a the ambiguous total is NOT resolved: stated=%s, candidates=%d"
          % (amb_total.totals.get("stated"), len(amb_total.total_candidates)),
          amb_total.totals.get("stated") is None and len(amb_total.total_candidates) == 2,
          "picking one of two readings is the defect; picking none and saying so is correct")
    subs = run("holdings_subtotals.csv")
    check("a the subtotal is excluded from the computed total: computed=%s stated=%s matches=%s"
          % (subs.totals["computed"], subs.totals["stated"]["value"],
             subs.totals.get("matches")),
          subs.totals["computed"].get("USD") == 700000.0
          and subs.totals.get("matches") is True,
          "and the grand total AGREES with the holdings, which is what makes the defect build "
          "below visible")


# --------------------------------------------------------------------------- b

def arm_b():
    print()
    print("(b) THE DIFFERENCE CONTROL -- a relabeling build vs the correct build")
    correct = run("holdings_non_usd.csv")
    relabel = run("holdings_non_usd.csv", relabel_currency_as_supported=True)
    rows = []
    for label, res in (("CORRECT", correct), ("RELABELING", relabel)):
        rec = res.reconcile()
        rows.append((label, rec))
        print("      %-11s ROW-COUNT balances=%-5s | CURRENCY consistent=%-5s violations=%d %s"
              % (label, rec["balances"], rec["currency_consistent"],
                 rec["currency"]["violations"], rec["currency"]["violating_cells"]))
        print("                  units claimed: %s | computed total: %s"
              % ([h["quantity"]["units"] for h in res.normalized_holdings],
                 res.totals["computed"]))
    c_rec, r_rec = rows[0][1], rows[1][1]
    check("b the relabeling build FAILS the reconcile: currency_consistent=%s, %d violating "
          "cell(s)" % (r_rec["currency_consistent"], r_rec["currency"]["violations"]),
          r_rec["currency_consistent"] is False and r_rec["currency"]["violations"] == 3
          and r_rec["currency"]["relabeled"] == 3,
          "it converted CAD to %s" % parse.load_intake_controls()["supported_currencies"][0])
    check("b the correct build HOLDS: currency_consistent=%s, %d violation(s)"
          % (c_rec["currency_consistent"], c_rec["currency"]["violations"]),
          c_rec["currency_consistent"] is True and c_rec["currency"]["violations"] == 0,
          "same specimen, same code path, one flag apart")
    check("b AND THE ROW-COUNT LEG PASSES THE DEFECT: balances=%s in BOTH builds"
          % (c_rec["balances"] and r_rec["balances"]),
          c_rec["balances"] is True and r_rec["balances"] is True,
          "this is row W4-S28's lesson made mechanical -- every count is right when a CAD "
          "column is called USD, so a certification that reads only counts passes it")

    # The same shape, on a second control: a subtotal counted as a holding.
    ok_sub = run("holdings_subtotals.csv")
    bad_sub = run("holdings_subtotals.csv", count_subtotals_in_total=True)
    print("      SECOND INSTANCE, subtotal-as-holding:")
    for label, res in (("CORRECT", ok_sub), ("DEFECT", bad_sub)):
        print("      %-11s holdings=%d computed=%s stated=%s matches=%s ROW-COUNT balances=%s"
              % (label, len(res.normalized_holdings), res.totals["computed"],
                 res.totals["stated"]["value"], res.totals.get("matches"),
                 res.reconcile()["balances"]))
    check("b the subtotal defect double-counts (%s vs stated %s) while the ROW COUNT still "
          "balances (%s)" % (bad_sub.totals["computed"].get("USD"),
                             bad_sub.totals["stated"]["value"],
                             bad_sub.reconcile()["balances"]),
          bad_sub.totals["computed"].get("USD") == 1350000.0
          and bad_sub.totals.get("matches") is False
          and bad_sub.reconcile()["balances"] is True
          and ok_sub.totals.get("matches") is True,
          "two independent controls, the same blind spot in a count-only check")


# --------------------------------------------------------------------------- c

def _binding():
    directory = authz_fixtures.DIRECTORY
    return authz.FirmBinding(authz_fixtures.TENANT, directory["firm_id_opaque"]), directory


def arm_c():
    print()
    print("(c) PROVENANCE -- who / when / from-what on r+1, r untouched, and a re-parse that "
          "cannot overwrite it")
    binding, directory = _binding()
    store = corrections.RevisionStore()
    parsed = run("holdings_share_class.csv")
    opened, refusal = corrections.open_revision(parsed, REQUEST_ID, binding, directory, store)
    check("c revision 0 opened on a quarantined parse: stage=%s"
          % opened["revision"]["stage"], refusal is None
          and opened["revision"]["stage"] == corrections.NEEDS_CORRECTION,
          "a quarantine is a reportable outcome, and this is what the advisor's request looks "
          "like while it holds")
    r0_before = opened["hash"]

    approval = {"finding_code": "SHARE_CLASS_SUBSTITUTION_PROPOSED",
                "approved_by": "analyst:alyssa", "approved_at": "2026-09-12T01:45Z",
                "from_value": "VTSAX", "to_value": "VTI", "to_namespace": "TICKER",
                "source_cell": "holdings_share_class.csv!A2"}
    applied, refusal = corrections.apply_corrections(store, REQUEST_ID, [approval],
                                                     binding, directory)
    r1 = applied["revision"]
    prov = r1["correction_provenance"][0]
    print("      r+1 correction_provenance[0]: %s" % json.dumps(prov, sort_keys=True))
    check("c the correction carries WHO (%s), WHEN (%s) and FROM-WHAT (%s)"
          % (prov.get("approved_by"), prov.get("approved_at"), prov.get("from_value")),
          refusal is None and prov.get("approved_by") == "analyst:alyssa"
          and prov.get("approved_at") == "2026-09-12T01:45Z"
          and prov.get("from_value") == "VTSAX" and prov.get("to_value") == "VTI",
          "approved_at is REQUIRED, not optional: an optional provenance field drifts to "
          "unpopulated")
    contract_keys = sorted(r1["corrections"][0])
    check("c the CONTRACT's corrections item keeps exactly its four keys: %s"
          % ", ".join(contract_keys),
          contract_keys == ["approved_by", "finding_code", "from_value", "to_value"],
          "the schema is additionalProperties:false and _contracts/ is not this order's to "
          "edit -- row IRPT_BCKEND-W3-S35 carries that the WHEN cannot travel in the contract")

    r0_after = corrections.revision_hash(store.get(REQUEST_ID, 0))
    check("c REVISION 0 IS UNTOUCHED: hash %s == %s" % (r0_before[:16], r0_after[:16]),
          r0_before == r0_after,
          "an ExportBundle pins the revision it was built from; if r could move, a bundle "
          "would describe a portfolio nobody submitted")
    refused = False
    try:
        store.put(REQUEST_ID, 0, {"tampered": True})
    except corrections.RevisionExists:
        refused = True
    check("c NEGATIVE CONTROL: a second write to revision 0 is REFUSED (%s), so the identical "
          "hash above is immutability and not merely absence of an attempt" % refused,
          refused and store.refused_overwrites == 1,
          "a hash that never moved because nothing tried to move it proves nothing")

    # -- the RE-PARSE ---------------------------------------------------
    reparsed = run("holdings_share_class.csv")
    kept, refusal = corrections.reparse_revision(store, REQUEST_ID, reparsed, binding, directory)
    ids_after = [h["identifier"] for h in kept["revision"]["normalized_holdings"]]
    print("      after re-parse, r+2 identifiers: %s" % ids_after)
    print("      r+2 reparse record: %s" % json.dumps(kept["revision"]["reparse"], sort_keys=True))
    check("c A RE-PARSE DOES NOT OVERWRITE THE CORRECTION: r+2 carries %d correction(s), "
          "%d re-applied, and the corrected identifier %s is present"
          % (len(kept["revision"]["corrections"]), len(kept["reapplied"]),
             "VTI" if "VTI" in ids_after else "VTI(MISSING)"),
          refusal is None and len(kept["revision"]["corrections"]) == 1
          and len(kept["reapplied"]) == 1 and "VTI" in ids_after and "VTSAX" not in ids_after
          and kept["revision"]["correction_provenance"][0]["approved_at"] == "2026-09-12T01:45Z",
          "the parser's fresh view is the advisor's ORIGINAL; writing it over the top would "
          "erase the human's decision with no artifact anywhere that disagreed")
    naive, _refusal = corrections.reparse_revision(store, REQUEST_ID, reparsed, binding,
                                                   directory, overwrite_corrections=True)
    naive_ids = [h["identifier"] for h in naive["revision"]["normalized_holdings"]]
    check("c DIFFERENCE CONTROL: the naive re-parse DOES lose it -- %d correction(s) on r+3 "
          "and the identifier is back to %s"
          % (len(naive["revision"]["corrections"]),
             "VTSAX" if "VTSAX" in naive_ids else "?"),
          len(naive["revision"]["corrections"]) == 0 and "VTSAX" in naive_ids
          and "VTI" not in naive_ids,
          "same function, one flag apart -- so the preservation above is the carry-forward "
          "working, not the re-parse happening to agree")
    check("c and r+1 is STILL intact after both re-parses: provenance %s"
          % corrections.revision_hash(store.get(REQUEST_ID, 1))[:16],
          store.get(REQUEST_ID, 1)["correction_provenance"][0]["approved_at"]
          == "2026-09-12T01:45Z",
          "every revision is append-only; a later revision losing a correction does not reach "
          "back")


# --------------------------------------------------------------------------- d

def arm_d():
    print()
    print("(d) ROUND 1 STILL HOLDS -- both sides re-derived, never compared to a stored hash")
    pin = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                         cwd=REPO).stdout.strip()
    base = subprocess.run(["git", "merge-base", pin, "origin/CLOUD"], capture_output=True,
                          text=True, cwd=REPO).stdout.strip() or pin
    tmp = tempfile.mkdtemp(prefix="rt11-pin-")
    for name in ("parse.py", "settings.json"):
        blob = subprocess.run(
            ["git", "show", "%s:infra/aws/lambda/investor-reporting/intake/%s" % (base, name)],
            capture_output=True, cwd=REPO)
        with open(os.path.join(tmp, name), "wb") as fh:
            fh.write(blob.stdout)
    prog = (
        "import sys, json, os\n"
        "sys.path.insert(0, %r)\n"
        "import parse\n"
        "out = {}\n"
        "mapping = parse.load_mapping(os.path.join(%r, 'security_mapping.json'))\n"
        "for f in %r:\n"
        "    data = open(os.path.join(%r, f), 'rb').read()\n"
        "    try:\n"
        "        r = parse.parse_holdings(data, f, 'att-fixed', mapping=mapping)\n"
        "        out[f] = r.digest()\n"
        "    except parse.ParseRefused:\n"
        "        out[f] = 'REFUSED'\n"
        "print(json.dumps(out, sort_keys=True))\n"
    )

    def digests(module_dir, names):
        r = subprocess.run([sys.executable, "-c", prog % (module_dir, FIX, names, FIX)],
                           capture_output=True, text=True, cwd=REPO)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-800:])
        return json.loads(r.stdout)

    before = digests(tmp, ROUND1)
    after = digests(INTAKE, ROUND1)
    same = 0
    for name in ROUND1:
        ok = before[name] == after[name]
        same += ok
        print("      %-28s %-9s before=%s after=%s"
              % (name, "IDENTICAL" if ok else "CHANGED", before[name][:16], after[name][:16]))
    check("d the five round-1 specimens parse byte-identically: %d of %d" % (same, len(ROUND1)),
          same == len(ROUND1),
          "pinned parser at %s vs the worktree parser, both run in fresh interpreters" % base[:10])

    # POSITIVE CONTROL ON THE COMPARATOR. Two parsers that agreed on everything would be
    # indistinguishable from a comparator that cannot tell them apart. The NEW specimens are
    # the discriminator: the pinned parser has no currency controls, so its digest MUST differ.
    new_before = digests(tmp, ["holdings_non_usd.csv"])
    new_after = digests(INTAKE, ["holdings_non_usd.csv"])
    differs = new_before["holdings_non_usd.csv"] != new_after["holdings_non_usd.csv"]
    check("d POSITIVE CONTROL: on a NEW specimen the two parsers DISAGREE (%s vs %s)"
          % (new_before["holdings_non_usd.csv"][:12], new_after["holdings_non_usd.csv"][:12]),
          differs,
          "so the 5-of-5 above is agreement, not a comparator that cannot see a difference")
    shutil.rmtree(tmp, ignore_errors=True)

    # ROUND 1'S OWN BATTERY, RUN. Digests prove the parse output did not move; this proves the
    # cell's whole acceptance still holds against the changed library.
    proc = subprocess.run([sys.executable, ROUND1_BATTERY], capture_output=True, text=True,
                          cwd=REPO, timeout=240)
    arms = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip().startswith("ARMS:")]
    token = "IBS7-PARSE-DETERMINISTIC" in proc.stdout
    print("      round-1 battery rc=%d  %s  token printed=%s"
          % (proc.returncode, arms[0] if arms else "<no ARMS line>", token))
    check("d round 1's OWN battery still passes against the changed library: %s"
          % (arms[0] if arms else "no ARMS line"),
          proc.returncode == 0 and token and arms and arms[0] == "ARMS: 6 of 6",
          "a digest says the bytes did not move; this says the acceptance did not either")

    # And the intake package's own tests.
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s",
                            os.path.join(INTAKE, "tests"), "-p", "test_*.py"],
                           capture_output=True, text=True, cwd=REPO, timeout=240)
    # THE COUNT, NOT THE DURATION. unittest prints "Ran 15 tests in 0.022s", and the wall clock
    # makes this battery's own saved output non-reproducible for a reason that is not a result.
    # The count is the measurement; the seconds are the machine.
    ran = [ln for ln in tests.stderr.splitlines() if ln.startswith("Ran ")]
    count = ran[0].split(" in ")[0] if ran else "<no count>"
    check("d the intake package's own unit tests pass: %s" % count,
          tests.returncode == 0,
          "the third instrument on the same claim")


# --------------------------------------------------------------------------- e

def arm_e():
    print()
    print("(e) WHERE THE CHECK RUNS vs WHERE THE VALUE IS CONSUMED")
    source_map = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
    with io.open(source_map, "r", encoding="utf-8") as fh:
        functions = json.load(fh)["functions"]
    ships_parse = sorted(fn for fn, cfg in functions.items()
                         if "parse.py" in (cfg.get("files") or []))
    ships_settings = sorted(fn for fn, cfg in functions.items()
                            if "settings.json" in (cfg.get("files") or []))
    print("      DENOMINATOR: %d function(s) in lambda-source-map.json | %d ship parse.py | "
          "%d ship settings.json %s"
          % (len(functions), len(ships_parse), len(ships_settings), ships_settings))
    check("e the honest answer is stated, not implied: parse.py is packaged by %d of %d "
          "functions, so these controls have NO runtime yet"
          % (len(ships_parse), len(functions)),
          True,
          "recorded as row IRPT_BCKEND-W3-S36; a 0 printed with its denominator is a finding, "
          "and this arm does the closest thing available instead of claiming a deployed check")

    # THE FLAT /var/task LAYOUT, IN A FRESH INTERPRETER, WITH THE REPO OFF sys.path.
    tmp = tempfile.mkdtemp(prefix="rt11-vartask-")
    task = os.path.join(tmp, "var", "task")
    os.makedirs(os.path.join(task, "fixtures", "holdings"))
    for name in ("parse.py", "settings.json"):
        shutil.copy(os.path.join(INTAKE, name), os.path.join(task, name))
    shutil.copy(os.path.join(FIX, "security_mapping.json"),
                os.path.join(task, "fixtures", "holdings", "security_mapping.json"))
    payload = {name: specimen(name).decode("latin-1") for name in RT11}
    blob = os.path.join(tmp, "specimens.json")
    with io.open(blob, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)

    prog = (
        "import sys, json, io\n"
        "task = %r\n"
        "sys.path.insert(0, task)\n"
        "bad = [p for p in sys.path if 'wk-irpt' in p or 'ajb_workspace' in p]\n"
        "for p in bad: sys.path.remove(p)\n"
        "import parse\n"
        "spec = json.load(io.open(%r, encoding='utf-8'))\n"
        "out = {'repo_on_path': bool(bad), 'module_file': parse.__file__}\n"
        "for name, text in sorted(spec.items()):\n"
        "    data = text.encode('latin-1')\n"
        "    try:\n"
        "        r = parse.parse_holdings(data, name, 'att')\n"
        "        out[name] = {'codes': sorted(f['code'] for f in r.findings),\n"
        "                     'needs_correction': r.needs_correction,\n"
        "                     'currency_consistent': r.reconcile()['currency_consistent']}\n"
        "    except parse.ParseRefused as exc:\n"
        "        out[name] = {'refused': str(exc)[:90]}\n"
        "print(json.dumps(out, sort_keys=True))\n"
    )

    def in_flat(policy_present):
        if not policy_present:
            os.remove(os.path.join(task, "settings.json"))
        r = subprocess.run([sys.executable, "-I", "-c", prog % (task, blob)],
                           capture_output=True, text=True, cwd=task, timeout=240)
        if r.returncode != 0:
            return {"_crashed": r.stderr[-400:]}
        return json.loads(r.stdout)

    flat = in_flat(True)
    print("      flat /var/task run: module=%s | repo on sys.path=%s"
          % (os.path.basename(str(flat.get("module_file"))), flat.get("repo_on_path")))
    agree = 0
    for name in RT11:
        here = sorted(set(codes(run(name))))
        there = sorted(set(flat.get(name, {}).get("codes") or []))
        same = here == there
        agree += same
        print("        %-30s repo=%s" % (name, ",".join(here)))
        print("        %-30s flat=%s  %s" % ("", ",".join(there), "SAME" if same else "DIFFERS"))
    check("e the controls fire IDENTICALLY in the flat /var/task layout: %d of %d specimen(s)"
          % (agree, len(RT11)),
          agree == len(RT11) and flat.get("repo_on_path") is False,
          "fresh interpreter, -I, repo stripped from sys.path -- the environment the value "
          "would actually be consumed in")

    # THE NEGATIVE ARM: the policy file does not ship.
    missing = in_flat(False)
    refusals = [name for name in RT11 if "refused" in (missing.get(name) or {})]
    print("      with settings.json ABSENT from /var/task:")
    for name in RT11:
        row = missing.get(name) or {}
        print("        %-30s %s" % (name, row.get("refused") or ("codes=%s" % row.get("codes"))))
    check("e NEGATIVE ARM: with the policy absent the parser REFUSES rather than defaulting to "
          "the supported currency: %d of %d specimen(s) refused" % (len(refusals), len(RT11)),
          len(refusals) == len(RT11),
          "a built-in default would relabel a non-USD value precisely when the policy failed "
          "to ship -- the one condition under which nobody is watching")
    shutil.rmtree(tmp, ignore_errors=True)

    # THE SPECIMENS ARE RE-DERIVED, so a committed fixture and its description cannot drift.
    gen = subprocess.run([sys.executable, GENERATOR], capture_output=True, text=True,
                         cwd=REPO, timeout=120)
    rebuilt = subprocess.run(["git", "status", "--porcelain", FIX], capture_output=True,
                             text=True, cwd=REPO).stdout.strip()
    check("e the four specimens are byte-reproducible from their committed generator (rc=%d, "
          "git reports %s after regeneration)"
          % (gen.returncode, "no change" if not rebuilt else "CHANGES"),
          gen.returncode == 0 and not rebuilt,
          "a specimen nobody can rebuild is a specimen nobody can check")

    manifest = json.load(io.open(os.path.join(FIX, "FIXTURE_MANIFEST.json"), encoding="utf-8"))
    recomputed = 0
    for row in manifest["files"]:
        body = open(os.path.join(FIX, row["path"]), "rb").read()
        if hashlib.sha256(body).hexdigest() == row["sha256"] and len(body) == row["bytes"]:
            recomputed += 1
    check("e every FIXTURE_MANIFEST hash re-derived from disk: %d of %d"
          % (recomputed, len(manifest["files"])),
          recomputed == len(manifest["files"]),
          "row IRPT_BCKEND-W3-S9's rule: a manifest of hashes is re-derived by the battery "
          "every run, never carried")


def main():
    print("=" * 78)
    print("IB-rt-11 / RT11-AC1 -- intake currency and unit controls: QUARANTINE OVER RELABELING")
    print("=" * 78)
    arm_a()
    arm_b()
    arm_c()
    arm_d()
    arm_e()
    print()
    print("-" * 78)
    print("checks failed: %d" % len(FAILURES))
    for f in FAILURES:
        print("  FAILED: %s" % f)
    print("-" * 78)
    if FAILURES:
        print("FINAL: INCOMPLETE -- the acceptance token is deliberately absent from this "
              "output in EVERY form, including negated: the expect is graded as a REGEX and a "
              "negated line would MATCH and grade this run PASS.")
        return 1
    print("ARMS: 5 of 5  (a four-of-four, b difference, c provenance, d round 1, e environment)")
    print("IBRT11-INTAKE-CONTROLLED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
