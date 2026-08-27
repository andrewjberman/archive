"""DH-6 acceptance: the entrypoint CARRIES a00's flag and never DERIVES it.

Both arms exercised against the real _stage_list, because the criterion is about what argv the
entrypoint actually builds -- reading the diff would only show what I intended it to build.

  ARM A (the nightly's safety)  flagless -> a00's argv is BYTE-PRESERVED against the pre-DH-6
        vintage recovered by CONTENT. Not "looks unchanged": compared element by element to the
        argv the previous commit produced for the same inputs.
  ARM B (the pass-through)      flagged  -> "--declared-historical" appears in the a00 stage's
        argv and in NO OTHER STAGE's argv.
  ARM C (the ban)               the entrypoint must contain no epoch/derive logic -- it may not
        compute pre-epoch-ness itself. Checked at the AST level, not by grepping prose.
"""
import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

# Absolute, so this runs from any cwd -- the entrypoint's own bootstrap needs cwd == RUNNERS
# to resolve lib/trading_calendar, and a cwd-relative RUNNERS then doubles the path.
REPO = Path("C:/Users/AndrewBerman/Desktop/ajb_workspace")
RUNNERS = REPO / "data/assets/scripts/gold/runners_49f"
sys.path.insert(0, str(RUNNERS))
PRE_DH6 = "bc585df628"          # the vintage before the pass-through, recovered by CONTENT
DATE = "2026-03-24"
work = Path(sys.argv[0]).resolve().parent / "_dh6"
work.mkdir(exist_ok=True)


# The entrypoint resolves lib/trading_calendar via HERE.parents[4], so a copy loaded from a
# scratch directory aborts at bootstrap -- the baseline MUST live in the real runners dir for
# its path arithmetic to match the live module's. Written there and removed in the finally.
_TEMPS = []


def load(name, src=None, path=None):
    if src is not None:
        path = RUNNERS / f"_dh6_tmp_{name}.py"
        path.write_bytes(src)
        _TEMPS.append(path)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


live = load("chain_live", path=RUNNERS / "chain_49f_entrypoint.py")
old_src = subprocess.run(
    ["git", "show", f"{PRE_DH6}:data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py"],
    capture_output=True, check=True).stdout
old = load("chain_pre", src=old_src)
assert "declared-historical" not in old_src.decode("utf-8"), \
    "baseline already carries the flag -- wrong pin, both arms would collapse"
print(f"baseline {PRE_DH6} content-checked: entrypoint does NOT carry the flag\n")

wd = work / "wd"
a_old = old._stage_list(DATE, False, wd)
a_new_flagless = live._stage_list(DATE, False, wd, False)
a_new_flagged = live._stage_list(DATE, False, wd, True)


def argv_of(stages, name):
    return next(argv for n, argv in stages if n == name)


# ---- ARM A: byte-preserved flagless -----------------------------------------
old_a00 = argv_of(a_old, "a00_dim_account")
new_a00 = argv_of(a_new_flagless, "a00_dim_account")
same = old_a00 == new_a00
print("ARM A -- FLAGLESS, the nightly's arm (a00 argv vs the pre-DH-6 vintage)")
print(f"    pre-DH-6 : {old_a00}")
print(f"    post     : {new_a00}")
print(f"    BYTE-PRESERVED: {same}")
# and every OTHER stage too -- a pass-through must not disturb the rest of the chain
others_same = all(argv_of(a_old, n) == argv_of(a_new_flagless, n)
                  for n, _ in a_old if n != "a00_dim_account")
print(f"    every other stage's argv identical: {others_same} "
      f"({len(a_old)} stages compared)")

# ---- ARM B: the flag reaches a00 and ONLY a00 -------------------------------
flagged_a00 = argv_of(a_new_flagged, "a00_dim_account")
in_a00 = "--declared-historical" in flagged_a00
leaked = [n for n, argv in a_new_flagged
          if n != "a00_dim_account" and "--declared-historical" in argv]
print("\nARM B -- FLAGGED, the pass-through")
print(f"    a00 argv: {flagged_a00}")
print(f"    flag present in a00 stage: {in_a00}")
print(f"    stages OTHER than a00 carrying it (must be []): {leaked}")

# ---- ARM C: the entrypoint may CARRY but never DERIVE ------------------------
tree = ast.parse(RUNNERS.joinpath("chain_49f_entrypoint.py").read_text(encoding="utf-8"))
names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)} | \
        {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
derive_markers = sorted(n for n in names
                        if "epoch" in n.lower() or "attested" in n.lower()
                        or "attestation" in n.lower())
print("\nARM C -- CARRIES, NEVER DERIVES")
print(f"    epoch/attestation-related identifiers anywhere in the entrypoint AST "
      f"(must be []): {derive_markers}")
print("      (an entrypoint that computed pre-epoch-ness itself would be the banned")
print("       auto-fallback one level up, where a00 cannot see it)")

# CLEANUP IS PART OF THE HARNESS, not an afterthought: the baseline had to be written INTO
# the producer tree for its path arithmetic to match, and an untracked file left there is
# invisible to every count, listing and predicate that would otherwise notice it.
for _t in _TEMPS:
    _t.unlink(missing_ok=True)
print(f"    temp baseline removed from the producer tree: "
      f"{[(p.name, p.exists()) for p in _TEMPS]}  (exists must be False)")

ok = (same and others_same and in_a00 and not leaked and not derive_markers
      and not any(p.exists() for p in _TEMPS))
print(f"\nDH-6 VERDICT: {'PASS' if ok else '*** FAIL ***'}")
sys.exit(0 if ok else 1)
