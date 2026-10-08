"""AMGT_RESAPP round 79 -- cell AMGT-cc-4: serve five stored research-note sections.

  python r79_cc4.py --crit AC1|AC2|AC3 --where local

The module under test is `lib/research/api/dossier_sections.py`, function
`dossier_sections(document, read_failed=False)`. It is given the research-notes document the
/thesis path has ALREADY read and returns a list of five entries, in FIELD_ORDER, each
{field, heading, status, text, reason, citation}.

  AC1 (build, no network): planted documents -- a value, each stored absence form, a missing
       field, an unknown extra section, no document, a failed read; the served text is the
       stored text byte for byte; the worker's own test file exists and passes.
  AC2 (build, reads the store, read-only): over every covered name the block is produced
       without raising; per field the served count equals the stored-value count read here
       and the count measured at the cut; every served text equals the stored text; two named
       companies are compared field by field.
  AC3 (bound): the api tests folder passes apart from the failure(s) already present at the
       cut, and lib/research/corpus/dossier.py is the file at the cut.

Prints `PASS|FAIL <clause> <detail>` lines and one verdict line
`R79 CC4 <crit> SERVED: YES|NO`. Exit 0 on YES, 1 on NO. Writes nothing.
"""
from __future__ import annotations

import argparse
import copy
import importlib
import os
import re
import subprocess
import sys

MODULE = "lib.research.api.dossier_sections"
MODULE_PATH = "lib/research/api/dossier_sections.py"
TEST_PATH = "lib/research/api/tests/test_dossier_sections.py"
DOSSIER_PATH = "lib/research/corpus/dossier.py"
ADAPTER_PATH = "lib/research/api/scoped_amgt.py"
TESTS_DIR = "lib/research/api/tests"

FIELD_ORDER = ("company_description", "why_we_own", "positives", "negatives", "special_items")
HEADINGS = {
    "company_description": "Company description",
    "why_we_own": "Why we own it",
    "positives": "Positives",
    "negatives": "Negatives",
    "special_items": "Special items",
}
ENTRY_KEYS = ["field", "heading", "status", "text", "reason", "citation"]

S_NO_NOTES = "We hold no research notes for this company."
S_READ_FAILED = "The research notes for this company could not be read just now."
S_FALLBACK = "This section is not in the research reports we hold for this company."

BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block",
          "estate", "stage", "input ledger", "bronze")

# measured at the cut, 2026-10-08, over the 95 covered names (stored value = a non-blank string)
MEASURED_AT_THE_CUT = {"company_description": 48, "why_we_own": 18, "positives": 13, "negatives": 13,
                       "special_items": 13}
COVERED_AT_THE_CUT = 95
NAMED = ("ASML_NA_Equity", "NU_US_Equity")
NU_NEGATIVES_TAIL = "Mexican deposits declined slightly"

# the bound: the blob of dossier.py at the cut, and the api tests that already failed at the cut
DOSSIER_BLOB_AT_THE_CUT = "a4548412e32d5f835696813ee88863b80ef6e6b8"
KNOWN_BASE_FAILURES = ("lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches",)
PASSED_AT_THE_CUT = 828

_RESULTS = []


def clause(ok, name, detail=""):
    _RESULTS.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


def note(text):
    print("   %s" % text)


def verdict(crit):
    yes = bool(_RESULTS) and all(_RESULTS)
    print("R79 CC4 %s SERVED: %s" % (crit, "YES" if yes else "NO"))
    return 0 if yes else 1


def repo_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=False)
        top = out.stdout.decode("utf-8", "replace").strip()
        if out.returncode == 0 and top:
            return os.path.normpath(top)
    except OSError:
        pass
    return os.getcwd()


def git(root, *args):
    out = subprocess.run(["git", "-C", root] + list(args), capture_output=True, check=False)
    return out.returncode, out.stdout.decode("utf-8", "replace").strip(), out.stderr.decode("utf-8", "replace").strip()


def load_module():
    """(module, None) or (None, why). The module is imported by name, so a caller may place a
    stand-in under that name in sys.modules before calling main()."""
    try:
        mod = importlib.import_module(MODULE)
    except Exception as exc:  # noqa: BLE001 -- the reason is the finding
        return None, "%s: %s" % (type(exc).__name__, exc)
    if not callable(getattr(mod, "dossier_sections", None)):
        return None, "%s has no callable dossier_sections" % MODULE
    return mod, None


def banned_in(sentence):
    low = (sentence or "").lower()
    return [word for word in BANNED if word in low]


def shape_faults(block):
    """Why `block` is not the five-entry list in the fixed order, or []."""
    faults = []
    if not isinstance(block, list):
        return ["the block is a %s, not a list" % type(block).__name__]
    if len(block) != len(FIELD_ORDER):
        faults.append("%d entries, expected %d" % (len(block), len(FIELD_ORDER)))
    for index, entry in enumerate(block):
        if not isinstance(entry, dict):
            faults.append("entry %d is a %s" % (index, type(entry).__name__))
            continue
        if list(entry.keys()) != ENTRY_KEYS:
            faults.append("entry %d keys %s" % (index, list(entry.keys())))
            continue
        want = FIELD_ORDER[index] if index < len(FIELD_ORDER) else None
        if entry["field"] != want:
            faults.append("entry %d field %r, expected %r" % (index, entry["field"], want))
        elif entry["heading"] != HEADINGS[want]:
            faults.append("entry %d heading %r, expected %r" % (index, entry["heading"], HEADINGS[want]))
        if entry["status"] not in ("served", "absent"):
            faults.append("entry %d status %r" % (index, entry["status"]))
        elif entry["status"] == "served" and (not isinstance(entry["text"], str) or entry["reason"] is not None):
            faults.append("entry %d is served without text or with a reason" % index)
        elif entry["status"] == "absent" and (
                entry["text"] is not None or entry["citation"] is not None or not isinstance(entry["reason"], str)
                or not entry["reason"].strip()):
            faults.append("entry %d is absent with text, with a citation or without a reason" % index)
    return faults


def by_field(block):
    return {entry["field"]: entry for entry in block}


def stored_has_value(field):
    """The rule the act states: a stored value is a string holding one non-blank character."""
    return isinstance(field, dict) and isinstance(field.get("value"), str) and bool(field["value"].strip())


# ------------------------------------------------------------------------------------------
# AC1 -- planted documents, no network
# ------------------------------------------------------------------------------------------

def _citation(page):
    return {"report_key": "s3://planted/reports/Planted research pack 5_5_2026.pdf", "report_id": "0123456789abcdef",
            "locator": page, "passage": "planted"}


def planted_document():
    # a value with characters outside ASCII (built with chr), a doubled space, a space at each
    # end, and an end in the middle of a sentence: every one must come back untouched
    odd = " WHY WE OWN:  the company" + chr(0x2019) + "s margin is 40%" + chr(0x2013) + "45% and it should remain a "
    return {
        "artifact": "research_dossier", "method_version": "amgt-corpus-dossier/7",
        "subject": {"security_key": "PLANT_US_Equity"},
        "fields": {
            "company_description": {"value": "COMPANY DESCRIPTION: A planted company. It sells one thing.",
                                    "citation": _citation(2)},
            "why_we_own": {"value": odd, "citation": _citation(0)},
            "positives": {"value": None, "absent": "no POSITIVES section in class A 2026-03-09 or class B 2026-Q2"},
            "negatives": {"value": None,
                          "absent": "NEGATIVES heading has no prose following it in the extracted text of class A 2026-05-07"},
            # special_items is not in the document at all
            "management": {"value": "MANAGEMENT: not one of the five", "citation": _citation(5)},
            "an_unknown_section": {"value": "must never be served", "citation": _citation(9)},
        },
    }


ABSENCE_FORMS = (
    ("no POSITIVES section in class A 2026-03-09 or class B 2026-Q2", "positives",
     'Neither the research pack of 2026-03-09 nor the research update of 2026-Q2 has a "Positives" section.'),
    ("no WHY WE OWN section in class A 2026-03-09 or class B missing", "why_we_own",
     'The research pack of 2026-03-09 has no "Why we own it" section.'),
    ("no COMPANY DESCRIPTION section in class A missing or class B 2026-H1", "company_description",
     'The research update of 2026-H1 has no "Company description" section.'),
    ("no SPECIAL ITEMS section in class A missing or class B missing", "special_items",
     'No research report we hold for this company has a "Special items" section.'),
    ("SPECIAL ITEMS heading has no prose following it in the extracted text of class A 2026-05-07", "special_items",
     'The "Special items" heading in the research pack of 2026-05-07 has no text under it.'),
    ("NEGATIVES heading has no prose following it in the extracted text of class B 2026-Q2", "negatives",
     'The "Negatives" heading in the research update of 2026-Q2 has no text under it.'),
    ("SPECIAL ITEMS heading is followed by a table and no prose in the extracted text of class A 2026-07-02",
     "special_items", 'The "Special items" heading in the research pack of 2026-07-02 is followed by a table and no text.'),
    ("POSITIVES heading has no prose following it in the extracted text of class A missing", "positives",
     'The "Positives" heading in the research pack has no text under it.'),
    # not one of the stored forms, and a stored form whose label would put a refused word in the sentence
    ("the section could not be composed", "negatives", S_FALLBACK),
    ("no NEGATIVES section in class A bronze-copy or class B missing", "negatives", S_FALLBACK),
    ("", "positives", S_FALLBACK),
    (None, "positives", S_FALLBACK),
)


def run_ac1(root):
    mod, why = load_module()
    if not clause(mod is not None, "C1 the module imports and exports dossier_sections", why or MODULE):
        return
    fn = mod.dossier_sections
    sentences = []

    document = planted_document()
    before = copy.deepcopy(document)
    try:
        block = fn(document)
    except Exception as exc:  # noqa: BLE001
        clause(False, "C2 a planted document builds the five entries in the fixed order", "%s: %s" % (type(exc).__name__, exc))
        return
    faults = shape_faults(block)
    if not clause(not faults, "C2 a planted document builds the five entries in the fixed order, six keys each",
                  "; ".join(faults) or "fields %s" % [e["field"] for e in block]):
        return
    got = by_field(block)
    stored = document["fields"]
    value_ok = all(
        got[name]["status"] == "served" and got[name]["text"] == stored[name]["value"]
        and got[name]["text"].encode("utf-8") == before["fields"][name]["value"].encode("utf-8")
        and got[name]["citation"] == before["fields"][name]["citation"]
        for name in ("company_description", "why_we_own"))
    clause(value_ok, "C3 a stored value is served with its text byte-equal and its citation as stored",
           "why_we_own served %d bytes, stored %d bytes" % (
               len((got["why_we_own"]["text"] or "").encode("utf-8")), len(before["fields"]["why_we_own"]["value"].encode("utf-8"))))
    clause(document == before, "C4 the document handed in is not changed", "")
    served_text = " ".join(str(e["text"]) for e in block)
    clause("must never be served" not in served_text and "not one of the five" not in served_text
           and got["special_items"]["status"] == "absent" and got["special_items"]["reason"] == S_FALLBACK,
           "C5 a section outside the five is ignored and a field the document lacks is absent with the plain sentence",
           "special_items reason %r" % got["special_items"]["reason"])

    wrong = []
    for stored_reason, name, want in ABSENCE_FORMS:
        doc = {"fields": {name: {"value": None, "absent": stored_reason}}}
        entry = by_field(fn(doc))[name]
        sentences.append(entry["reason"])
        if entry["status"] != "absent" or entry["reason"] != want:
            wrong.append("%r -> %r, expected %r" % (stored_reason, entry["reason"], want))
    clause(not wrong, "C6 each stored absence form reads as its plain sentence (%d forms)" % len(ABSENCE_FORMS),
           " | ".join(wrong[:3]))

    wrong = []
    for label, field in (("the field is null", None), ("the value is a table, not text", {"value": {"a": 1}, "citation": _citation(1)}),
                         ("the value is an empty string", {"value": "", "citation": _citation(1)}),
                         ("the value is blank", {"value": "  \n ", "citation": _citation(1)}),
                         ("the field is a list", ["x"])):
        entry = by_field(fn({"fields": {"positives": field}}))["positives"]
        sentences.append(entry["reason"])
        if entry["status"] != "absent" or entry["text"] is not None or entry["citation"] is not None or entry["reason"] != S_FALLBACK:
            wrong.append("%s -> %s %r" % (label, entry["status"], entry["reason"]))
    entry = by_field(fn({"fields": {"positives": {"value": "A value with no citation stored."}}}))["positives"]
    if entry["status"] != "served" or entry["citation"] is not None:
        wrong.append("a value with no stored citation -> %s citation %r" % (entry["status"], entry["citation"]))
    clause(not wrong, "C7 a value that is not text is absent, and a value with no stored citation is served with none",
           " | ".join(wrong[:3]))

    wrong = []
    for label, args, kwargs, want in (
            ("no document", (None,), {}, S_NO_NOTES),
            ("no document, read failed", (None,), {"read_failed": True}, S_READ_FAILED),
            ("a document that is not an object", (["x"],), {}, S_READ_FAILED),
            ("a document with no fields", ({},), {}, S_FALLBACK)):
        try:
            blk = fn(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            wrong.append("%s raised %s" % (label, type(exc).__name__))
            continue
        faults = shape_faults(blk)
        reasons = sorted(set(e.get("reason") for e in blk if isinstance(e, dict)))
        sentences.extend(r for r in reasons if isinstance(r, str))
        if faults or reasons != [want]:
            wrong.append("%s -> %s %s" % (label, reasons, faults[:1]))
    clause(not wrong, "C8 no document, a failed read and an empty document each give five absent entries with one plain sentence",
           " | ".join(wrong[:3]))

    sentences.extend(HEADINGS.values())
    sentences.extend(e["reason"] for e in block if e["reason"])
    hits = sorted(set("%r in %r" % (w, s) for s in sentences if isinstance(s, str) for w in banned_in(s)))
    not_ascii = [s for s in sentences if isinstance(s, str) and any(ord(ch) > 127 for ch in s)]
    clause(not hits and not not_ascii, "C9 no sentence the module writes uses a refused word, and each is ASCII (%d read)" % len(sentences),
           "; ".join(hits[:3]))

    path = getattr(mod, "__file__", None) or ""
    source = ""
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    imports = re.findall(r"^\s*(?:from|import)\s+([A-Za-z0-9_.]+)", source, flags=re.M)
    refused = [m for m in imports if m.split(".")[0] in ("boto3", "botocore", "lib", "requests", "urllib")]
    clause(bool(source) and not refused and all(ord(ch) < 128 for ch in source),
           "C10 the module is pure: ASCII source, no store client and no import from lib",
           "imports %s; source %s" % (sorted(set(imports)), path or "not a file"))

    test_file = os.path.join(root, TEST_PATH)
    if not clause(os.path.isfile(test_file), "C11 the worker's test file exists", TEST_PATH):
        return
    run = subprocess.run([sys.executable, "-m", "pytest", TEST_PATH, "-q", "-p", "no:cacheprovider", "--color=no"],
                         cwd=root, capture_output=True, check=False)
    tail = [ln for ln in run.stdout.decode("utf-8", "replace").splitlines() if ln.strip()][-1:]
    note(tail[0] if tail else "no output")
    clause(run.returncode == 0, "C12 the worker's test file passes", "rc=%d" % run.returncode)


# ------------------------------------------------------------------------------------------
# AC2 -- the real store, read-only
# ------------------------------------------------------------------------------------------

def run_ac2(root):
    mod, why = load_module()
    if not clause(mod is not None, "C1 the module imports and exports dossier_sections", why or MODULE):
        return
    fn = mod.dossier_sections
    from concurrent.futures import ThreadPoolExecutor

    from lib.research.corpus import dossier
    from lib.research.coverage.covered_universe import covered_security_keys

    keys = sorted(covered_security_keys())

    def read(key):
        try:
            return key, dossier.read_dossier(key)["document"], None
        except Exception as exc:  # noqa: BLE001 -- counted below, never swallowed
            return key, None, "%s: %s" % (type(exc).__name__, exc)

    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(read, keys))
    unread = [(key, err) for key, _doc, err in rows if err]
    note("covered names %d; research notes read %d; not read %d %s" % (len(keys), len(rows) - len(unread), len(unread), unread[:3]))

    built, raised, shape_bad = {}, [], []
    for key, doc, err in rows:
        if err:
            continue
        try:
            block = fn(doc)
        except Exception as exc:  # noqa: BLE001
            raised.append("%s %s" % (key, type(exc).__name__))
            continue
        faults = shape_faults(block)
        if faults:
            shape_bad.append("%s %s" % (key, faults[0]))
            continue
        built[key] = by_field(block)
    clause(len(keys) == COVERED_AT_THE_CUT and not unread and not raised and not shape_bad and len(built) == len(keys),
           "C2 the block is produced for every covered name without raising",
           "%d of %d; raised %s; wrong shape %s" % (len(built), len(keys), raised[:3], shape_bad[:3]))
    if not built:
        return
    docs = {key: doc for key, doc, err in rows if not err}

    counts_ok, cut_ok = True, True
    text_total, text_equal, citation_equal, reasons = 0, 0, 0, []
    for name in FIELD_ORDER:
        stored_n = sum(1 for key in built if stored_has_value((docs[key].get("fields") or {}).get(name)))
        served_n = sum(1 for key in built if built[key][name]["status"] == "served")
        counts_ok = counts_ok and stored_n == served_n
        cut_ok = cut_ok and stored_n == MEASURED_AT_THE_CUT[name]
        print("   %-20s served %d of %d; stored %d of %d; at the cut %d" % (
            name, served_n, len(built), stored_n, len(built), MEASURED_AT_THE_CUT[name]))
        for key in built:
            field = (docs[key].get("fields") or {}).get(name)
            entry = built[key][name]
            if entry["status"] == "served":
                text_total += 1
                if stored_has_value(field) and entry["text"].encode("utf-8") == field["value"].encode("utf-8"):
                    text_equal += 1
                if isinstance(field, dict) and entry["citation"] == field.get("citation"):
                    citation_equal += 1
            else:
                reasons.append(entry["reason"])
    clause(counts_ok, "C3 per field the served count equals the stored-value count read from the store now", "")
    clause(cut_ok, "C4 per field the stored-value count is the one measured at the cut",
           "" if cut_ok else "the store moved since the cut: file a surprise row, do not change the module to fit")
    clause(text_total > 0 and text_equal == text_total and citation_equal == text_total,
           "C5 every served text equals the stored text byte for byte, with the stored citation",
           "text %d of %d; citation %d of %d" % (text_equal, text_total, citation_equal, text_total))

    wrong = []
    for key in NAMED:
        if key not in built:
            wrong.append("%s not built" % key)
            continue
        line = []
        for name in FIELD_ORDER:
            field = (docs[key].get("fields") or {}).get(name)
            entry = built[key][name]
            if stored_has_value(field):
                same = entry["status"] == "served" and entry["text"].encode("utf-8") == field["value"].encode("utf-8")
                line.append("%s %d bytes %s" % (name, len(field["value"].encode("utf-8")), "equal" if same else "DIFFERENT"))
                if not same:
                    wrong.append("%s %s" % (key, name))
            else:
                line.append("%s absent" % name)
                if entry["status"] != "absent":
                    wrong.append("%s %s served with nothing stored" % (key, name))
        note("%s: %s" % (key, "; ".join(line)))
    tail = ((built.get("NU_US_Equity") or {}).get("negatives") or {}).get("text") or ""
    if not tail.endswith(NU_NEGATIVES_TAIL):
        wrong.append("NU_US_Equity negatives does not end as stored (%r)" % tail[-40:])
    clause(not wrong, "C6 the two named companies are served as stored, the known cut-off value included", "; ".join(wrong[:3]))

    hits = sorted(set("%r in %r" % (w, r) for r in reasons for w in banned_in(r)))
    fallback = sum(1 for r in reasons if r == S_FALLBACK)
    note("absent entries %d; of them the general sentence %d; distinct sentences %d" % (len(reasons), fallback, len(set(reasons))))
    clause(not hits and all(isinstance(r, str) and r.strip() for r in reasons),
           "C7 every absent entry carries a plain reason with no refused word", "; ".join(hits[:3]))


# ------------------------------------------------------------------------------------------
# AC3 -- the bound
# ------------------------------------------------------------------------------------------

def run_ac3(root):
    run = subprocess.run([sys.executable, "-m", "pytest", TESTS_DIR, "-q", "-p", "no:cacheprovider", "--color=no", "-rfE"],
                         cwd=root, capture_output=True, check=False)
    out = run.stdout.decode("utf-8", "replace")
    failed = sorted(set(re.findall(r"^FAILED (\S+)", out, flags=re.M)))
    errors = sorted(set(re.findall(r"^ERROR (\S+)", out, flags=re.M)))
    passed = re.findall(r"(\d+) passed", out)
    passed_n = int(passed[-1]) if passed else 0
    tail = [ln for ln in out.splitlines() if ln.strip()][-1:]
    note(tail[0] if tail else "no output")
    new = [f for f in failed if f not in KNOWN_BASE_FAILURES]
    clause(run.returncode in (0, 1) and not new and not errors and passed_n >= PASSED_AT_THE_CUT,
           "C1 the api tests folder passes apart from what already failed at the cut",
           "passed %d (at the cut %d); failed %s; of them new %s; errors %s" % (passed_n, PASSED_AT_THE_CUT, failed, new, errors))

    rc_ctl, ctl, _ = git(root, "rev-parse", "HEAD:lib/research/api/__init__.py")
    rc_head, head_blob, err = git(root, "rev-parse", "HEAD:" + DOSSIER_PATH)
    rc_work, work_blob, _ = git(root, "hash-object", DOSSIER_PATH)
    rc_diff, _o, _e = git(root, "diff", "--quiet", "HEAD", "--", DOSSIER_PATH)
    clause(rc_ctl == 0 and len(ctl) == 40 and rc_head == 0 and rc_work == 0 and rc_diff == 0
           and head_blob == work_blob == DOSSIER_BLOB_AT_THE_CUT,
           "C2 dossier.py is byte-unchanged against HEAD and is the file at the cut",
           "working %s; HEAD %s; at the cut %s; control read %s %s" % (
               work_blob[:12], head_blob[:12] or err[:60], DOSSIER_BLOB_AT_THE_CUT[:12], "ok" if rc_ctl == 0 else "FAILED", ctl[:8]))

    rc_diff2, _o, _e = git(root, "diff", "--quiet", "HEAD", "--", ADAPTER_PATH)
    clause(rc_diff2 == 0, "C3 scoped_amgt.py carries no uncommitted edit", "git diff --quiet rc=%d" % rc_diff2)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--crit", required=True, choices=("AC1", "AC2", "AC3"))
    parser.add_argument("--where", required=True, choices=("local",))
    args = parser.parse_args(argv)
    root = repo_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    {"AC1": run_ac1, "AC2": run_ac2, "AC3": run_ac3}[args.crit](root)
    return verdict(args.crit)


if __name__ == "__main__":
    sys.exit(main())
