"""AR362-y-AC3: the one mutant. Copies the run 3 csv to a scratch folder OUTSIDE the product tree with the third row's
ticker changed to ZZZZ, runs csv_check.py's check() against the copy, and prints MUTANT-FIRES only when that check
fails on it (else MUTANT-SURVIVES, exit 1).

The record copy carries the mutant's own sha256 and byte count, so the ONLY rule the mutant can trip is the ticker rule;
an unmutated control copy must pass first, or the run is refused as a broken control.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("csv_check", os.path.join(HERE, "csv_check.py"))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)


def _copy_pair(scratch, csv_bytes, rec):
    csv_path = os.path.join(scratch, cc.CSV_NAME)
    rec_path = os.path.join(scratch, "RUN3_HOLDINGS.json")
    with open(csv_path, "wb") as fh:
        fh.write(csv_bytes)
    rec = dict(rec, csv_sha256=hashlib.sha256(csv_bytes).hexdigest(), csv_bytes=len(csv_bytes))
    with open(rec_path, "wb") as fh:
        fh.write(json.dumps(rec, indent=2).encode("utf-8") + b"\n")
    return csv_path, rec_path


def main():
    with open(os.path.join(HERE, cc.CSV_NAME), "rb") as fh:
        data = fh.read()
    with open(cc.RECORD, "rb") as fh:
        rec = json.loads(fh.read().decode("utf-8"))
    lines = data.split(b"\n")
    ticker_bytes = lines[3].split(b",")[0]
    mutant = b"\n".join(lines[:3] + [b"ZZZZ" + lines[3][len(ticker_bytes):]] + lines[4:])
    scratch = tempfile.mkdtemp(prefix="ar362_mutant_")
    try:
        control_dir = os.path.join(scratch, "control")
        mutant_dir = os.path.join(scratch, "mutant")
        os.mkdir(control_dir)
        os.mkdir(mutant_dir)
        ctl_csv, ctl_rec = _copy_pair(control_dir, data, rec)
        ok_ctl, why_ctl = cc.check(ctl_csv, ctl_rec, cc.BASE_CSV)
        if not ok_ctl:
            print("MUTANT-CONTROL-BAD the unmutated copy fails the check: %s" % why_ctl)
            return 1
        mut_csv, mut_rec = _copy_pair(mutant_dir, mutant, rec)
        ok_mut, why_mut = cc.check(mut_csv, mut_rec, cc.BASE_CSV)
        if ok_mut:
            print("MUTANT-SURVIVES the check passed the ZZZZ copy")
            return 1
        print("MUTANT-FIRES on ZZZZ copy: %s" % why_mut)
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
