"""RIV-dr-1 AC1 (adjudication C-S38; round-10 analysis ruling 2 @134485f75b; round-9 ruling 3): the G5 drift record names the
data-arrival class's cause as data arrival, never a code commit. Measured: `deliverables/0.9.0_WK_ETFS_RIVALS~6/g5_drift.json`
`classes[g3_latest_pull_supersession].cause` reads {"commit": "4fa3e25f5e", "cell": "RIV-g-4"}, as does its G5_DRIFT.md table row
and the class definition in `tools/g5_drift.py` `CLASSES`. Its 9,467 rows moved under UNCHANGED code because later G3 pulls landed;
round-9 ruling 3 keeps their vintage.

Interface (prescribed): in `tools/g5_drift.py` `CLASSES`, that class carries `"commit": None` and `"cause": "data arrival (later G3
pulls)"`. Its record entry's `cause` reads {"commit": null, "cell": "RIV-g-4", "what": "data arrival (later G3 pulls)"}.
`markdown()` prints that text in the cause-commit column of a class whose commit is null. The two record files are corrected IN
PLACE: the JSON edited, the MD re-rendered by `markdown()` from it. No re-run, no S3 read, no data moves.
  - (a) the JSON's class cause has commit null and `what` "data arrival (later G3 pulls)"; the MD names that text on the class's
    row and contains no `4fa3e25f5e`;
  - (b) the MD equals `g5_drift.markdown(<the JSON>)` byte for byte, and `CLASSES` carries `commit` None for the class;
  - (c) control: the other six classes' `cause.commit` values are unchanged (b723f89d22, ab0a58eaa4, 5cd27dc0d2, b137069123,
    2a655a0180, 0b2981d770), and so are every class's `n_rows`.
FAIL at base: (a) and (b) FAIL; (c) PASSES."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

CLS = "g3_latest_pull_supersession"
TEXT = "data arrival (later G3 pulls)"
OTHERS = {"key_resolution_out_of_confidence": ("b723f89d22", 1040), "full_exit_priced": ("ab0a58eaa4", 266),
          "own_prior_pairing": ("5cd27dc0d2", 7), "implausible_window_refused": ("b137069123", 10),
          "g3_currency_in_income_conversion": ("2a655a0180", 7), "g3_minor_unit_dividend_currency": ("0b2981d770", 13)}


def run(v):
    c.setup_path()
    from rivalfunds.tools import g5_drift as t

    d = c.ROOT / "org" / "missions" / "D5" / "ETFS" / "ETFS_RIVALS" / "deliverables" / "0.9.0_WK_ETFS_RIVALS~6"
    rep = json.loads((d / "g5_drift.json").read_text(encoding="utf-8"))
    md = (d / "G5_DRIFT.md").read_text(encoding="utf-8")
    by = {k["name"]: k for k in rep["classes"]}
    cause = by[CLS]["cause"]
    row = [ln for ln in md.splitlines() if ln.startswith(f"| {CLS} |")]
    print("cause", cause, "| md row", row[0][:90] if row else None, "| md has 4fa3e25f5e", "4fa3e25f5e" in md)
    v.check(cause.get("commit") is None and cause.get("what") == TEXT and bool(row) and TEXT in row[0] and "4fa3e25f5e" not in md,
            "(a) the record names the data-arrival class's cause as data arrival, not a commit")
    defn = [k for k in t.CLASSES if k["name"] == CLS]
    rendered = t.markdown(rep)
    print("CLASSES commit", defn[0].get("commit") if defn else "absent", "| markdown(json) == MD", rendered == md)
    v.check(bool(defn) and defn[0].get("commit") is None and rendered == md,
            "(b) the tool's class definition carries no commit and the MD is the tool's rendering of the JSON")
    moved = {n: (by[n]["cause"].get("commit"), by[n]["n_rows"]) for n in OTHERS if (by[n]["cause"].get("commit"), by[n]["n_rows"]) != OTHERS[n]}
    print("other classes moved:", moved, "| data-arrival n_rows", by[CLS]["n_rows"])
    v.check(not moved and by[CLS]["n_rows"] == 9467, "(c) control: the other six causes and every class's row count unchanged")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
