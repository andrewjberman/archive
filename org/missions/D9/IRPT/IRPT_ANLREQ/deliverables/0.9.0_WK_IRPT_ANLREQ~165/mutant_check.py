#!/usr/bin/env python3
"""AR-y-368 mutant checker (0.9.0_WK_IRPT_ANLREQ~165). Copies the decisions file to a scratch folder OUTSIDE the product
tree, changes one symbol to ZZZZ (a symbol the csv does not contain; when the file has no decision, a decision naming
ZZZZ is appended), re-pins the record's decisions_sha256 to the copy so that only the symbol rule can trip, and runs
inputs_check.check against the copy. Prints MUTANT-FIRES only when the check fails on the copy, the unmutated control
passes first; otherwise MUTANT-SURVIVES, exit 1."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import inputs_check as ic  # noqa: E402

RULE = "every decision names a symbol present in the csv"


def main():
    record = json.loads(ic.RECORD.read_text(encoding="utf-8"))
    control, _ = ic.check(record, ic.CSV, ic.DECISIONS)
    if control:
        print("MUTANT-SURVIVES the unmutated control already fails: " + "; ".join(control))
        return 1
    scratch = Path(tempfile.mkdtemp(prefix="wk165_ar368_mutant_"))
    try:
        doc = json.loads(ic.DECISIONS.read_text(encoding="utf-8"))
        if doc.get("decisions"):
            doc["decisions"][0]["symbol"] = "ZZZZ"
            how = "the first decision symbol changed to ZZZZ"
        else:
            doc.setdefault("decisions", []).append({"symbol": "ZZZZ", "answer": "no"})
            how = "the file has no decision, so a decision naming ZZZZ was appended"
        mutant = scratch / "decisions_mutant.json"
        mutant.write_text(json.dumps(doc) + "\n", encoding="utf-8")
        copy_record = dict(record)
        copy_record["decisions_sha256"] = ic.sha256_file(mutant)
        violations, _ = ic.check(copy_record, ic.CSV, mutant)
    finally:
        shutil.rmtree(str(scratch), ignore_errors=True)
    hits = [v for v in violations if v.startswith(RULE)]
    if hits:
        print("MUTANT-FIRES control passed (0 violations); %s; the check fails on the copy: %s"
              % (how, hits[0]))
        return 0
    print("MUTANT-SURVIVES %s; the check did not fail on the symbol rule (violations: %r)" % (how, violations))
    return 1


if __name__ == "__main__":
    sys.exit(main())
