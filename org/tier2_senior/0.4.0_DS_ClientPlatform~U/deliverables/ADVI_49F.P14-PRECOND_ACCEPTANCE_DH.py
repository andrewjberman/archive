"""ADVI_49F.P14-PRECOND acceptance -- DH-1, DH-2, DH-3 EXERCISED, never asserted.

Every arm invokes a00_runner as a REAL subprocess and reads its true rc and its output, because
the criteria say "exercised" and "run it; do not assert it". Nothing is uploaded: every arm is
--dry-run.

  DH-1  no auto-fallback, FROM THE REAL FAILING STATE. Without the flag, 2026-03-24 must
        reproduce the original abort for the ORIGINAL REASON (the attestation refusal, not some
        other error that happens to be non-zero). With the flag, the same date proceeds past
        a00's guard. The pre-existing refusal IS the negative control and it must still fire.
  DH-2  the mode's own guard. Flag + a date >= the MEASURED epoch must REFUSE loudly, naming
        the epoch and the reason -- so the mode cannot be used to bypass the guard where the
        guard can bind.
  DH-3  the epoch is MEASURED, never typed. Shown two ways: no date literal exists in the code
        path, and a PLANTED extra record MOVES the computed epoch (the mutant control).
"""
import subprocess
import sys
from pathlib import Path

RUNNERS = Path("data/assets/scripts/gold/runners_49f").resolve()
PRE_EPOCH_DATE = "2026-03-24"      # the CF-2 specimen day; the real failing state
ORIGINAL_REFUSAL = "no conversion record attests fact_acc"


def run(args, label):
    p = subprocess.run([sys.executable, "a00_runner.py"] + args, cwd=str(RUNNERS),
                       capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    print(f"\n--- {label}\n    argv: a00_runner.py {' '.join(args)}\n    rc={p.returncode}")
    for line in [x for x in out.splitlines() if x.strip()][:6]:
        print(f"    | {line[:150]}")
    return p.returncode, out


results = {}

# ============ DH-1 =========================================================
print("=" * 78)
print("DH-1  EXPLICIT-MODE ONLY -- exercised from the REAL failing state")
rc_no, out_no = run(["--date", PRE_EPOCH_DATE, "--dry-run"], "DH-1a  WITHOUT the flag")
same_reason = ORIGINAL_REFUSAL in out_no
print(f"    negative control: original refusal reproduced for the ORIGINAL REASON: {same_reason}")
print(f"      (matching on {ORIGINAL_REFUSAL!r} -- a non-zero rc alone would NOT establish this;")
print("       any unrelated error also exits non-zero, and that is the trap being avoided)")
rc_yes, out_yes = run(["--date", PRE_EPOCH_DATE, "--dry-run", "--declared-historical"],
                      "DH-1b  WITH the flag")
past_guard = ("DECLARED-HISTORICAL" in out_yes
              and ORIGINAL_REFUSAL not in out_yes)
print(f"    proceeds past a00's attestation guard: {past_guard}")
dh1 = bool(rc_no != 0 and same_reason and past_guard)
results["DH-1"] = dh1

# ============ DH-2 =========================================================
print("\n" + "=" * 78)
print("DH-2  THE MODE'S OWN GUARD -- run it, do not assert it")
sys.path.insert(0, str(RUNNERS))
import a00_runner as mod  # noqa: E402
epoch = mod.attestation_epoch()
print(f"    measured epoch (read from the converter record set): {epoch}")
rc_epoch, out_epoch = run(["--date", epoch, "--dry-run", "--declared-historical"],
                          f"DH-2  flag + date == epoch ({epoch})")
names_epoch = epoch in out_epoch and "PRE-EPOCH dates only" in out_epoch
print(f"    refuses loudly AND names the epoch + the reason: {names_epoch}")
dh2 = bool(rc_epoch != 0 and names_epoch)
results["DH-2"] = dh2

# ============ DH-3 =========================================================
print("\n" + "=" * 78)
print("DH-3  EPOCH MEASURED, NEVER TYPED")
src = (RUNNERS / "a00_runner.py").read_text(encoding="utf-8")
import ast  # noqa: E402
import re  # noqa: E402

DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
# MY FIRST VERSION OF THIS CHECK WAS WRONG AND FAILED THE CRITERION FOR THE WRONG REASON.
# It filtered lines starting with '#' and containing 'help=', then regexed the rest -- which
# still swept the module DOCSTRING (prose, and a --date usage example) and a TRAILING comment
# on a code line. It reported three "literals", none of them a typed date the code reads.
# A line-based filter cannot tell code from prose; a PARSER can. Walk the AST, take only
# string CONSTANTS that are not docstrings, and comments never enter the tree at all.
tree = ast.parse(src)
docstrings = set()
for node in ast.walk(tree):
    if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        ds = ast.get_docstring(node, clean=False)
        if ds:
            docstrings.add(ds)
literals = sorted({v for n in ast.walk(tree)
                   if isinstance(n, ast.Constant) and isinstance(n.value, str)
                   and n.value not in docstrings
                   for v in DATE_RE.findall(n.value)})
prose_only = sorted(set(DATE_RE.findall(src)))
print(f"    date literals in real CODE (AST constants, docstrings excluded) -- must be []: "
      f"{literals}")
print(f"    date-shaped text anywhere in the file incl. prose/comments: {prose_only}")
print("      (the first list is the criterion; the second is why a line-based check fails --")
print("       a --date usage example in the docstring is not a typed epoch)")
# TARGETED CONTROL: the epoch function's OWN source must contain no date literal at all.
epoch_fn = next(n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name == "attestation_epoch")
epoch_src = ast.get_source_segment(src, epoch_fn) or ""
epoch_code_literals = sorted({v for n in ast.walk(epoch_fn)
                              if isinstance(n, ast.Constant) and isinstance(n.value, str)
                              for v in DATE_RE.findall(n.value)})
print(f"    attestation_epoch()'s own string constants containing a date: "
      f"{epoch_code_literals} (must be [])")
no_literal = (not literals) and (not epoch_code_literals) and bool(epoch_src)

# MUTANT CONTROL: plant an earlier attesting record and the computed epoch MUST move.
class _FakeS3:
    """Wraps the real client; injects ONE extra conversion record naming an earlier date."""
    def __init__(self, real):
        self._r = real
        self.key = "PLANTED/mutant-record.json"
    def get_paginator(self, op):
        real_pag = self._r.get_paginator(op)
        outer = self
        class P:
            def paginate(self, **kw):
                pages = list(real_pag.paginate(**kw))
                if kw.get("Prefix", "").endswith("meta/conversions/"):
                    pages = pages + [{"Contents": [{"Key": outer.key}]}]
                return pages
        return P()
    def get_object(self, Bucket=None, Key=None):
        if Key == self.key:
            import io as _io
            import json as _json
            body = _json.dumps({"partitions": ["2019-01-02"],
                                "per_type": {"fact_acc": {"action": "converted",
                                                          "t1_expected": 1}}}).encode()
            return {"Body": _io.BytesIO(body)}
        return self._r.get_object(Bucket=Bucket, Key=Key)


real = mod.s3
try:
    mod.s3 = _FakeS3(real)
    mutant_epoch = mod.attestation_epoch()
finally:
    mod.s3 = real
moved = mutant_epoch == "2019-01-02" and mutant_epoch != epoch
print(f"    MUTANT: planted a record attesting 2019-01-02 -> epoch computes {mutant_epoch}")
print(f"    epoch MOVED with the record (so it is derived, not pinned): {moved}")
print(f"    control-of-the-control: unplanted epoch re-reads {mod.attestation_epoch()} "
      f"== {epoch} -> {mod.attestation_epoch() == epoch}")
dh3 = bool(no_literal and moved and mod.attestation_epoch() == epoch)
results["DH-3"] = dh3

print("\n" + "=" * 78)
for k, v in results.items():
    print(f"  {k}  {'PASS' if v else '*** FAIL ***'}")
print(f"  ALL_EXERCISED_PASS = {all(results.values())}")
sys.exit(0 if all(results.values()) else 1)
