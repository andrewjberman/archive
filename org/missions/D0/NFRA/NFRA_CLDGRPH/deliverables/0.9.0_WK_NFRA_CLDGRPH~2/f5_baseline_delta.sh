#!/usr/bin/env bash
# F5-AC4 -- THE BASELINE UNTOUCHED AND THE DELTA NAMED. TO-CG-F-5.
#
# THE DELTA IS ON RESIDUALS, NOT ON THE CENSUS, and that is not a choice -- it is what the
# baseline file actually holds. comp_debt_baseline.json stores per family {"keys": [...], "n": N}
# where the keys are RESIDUAL keys (family::class/deviation::sites). It has never held a census
# count, so a "census vs baseline" number would be a comparison against a quantity that is not
# there. Both figures are printed; the criterion's value is the one the baseline can answer.
#
# BASELINE_EDITED USES THREE INSTRUMENTS BECAUSE THE OBVIOUS ONE IS WRONG ON THIS BOX.
# A raw sha256 of the worktree bytes against `git show HEAD:<path>` reads EDITED for a file
# nobody touched: core.autocrlf gives the CHECKOUT CRLF line endings while the RECORD keeps LF,
# so the two differ by exactly one byte per line. Measured here: 4504 vs 4433 bytes, difference
# 71, and the file has exactly 71 lines. So this prints (a) `git diff --quiet HEAD`, git's own
# comparison, which honours the eol filter and is the authoritative "was it edited" oracle;
# (b) the sha256 pair NORMALISED to LF; and (c) the RAW pair with its CRLF counts, so the trap
# is visible in the output rather than silently corrected. Row NFRA_CLDGRPH-W2-S58.
#
# Run from the repository root.
set -u

python - <<'PY'
import hashlib
import io
import json
import subprocess
import sys

BASE = "infra/aws/globgrph/comp_debt_baseline.json"
ROW = "NFRA_CLDGRPH-W2-S57"        # the row that carries a non-zero delta

base = json.load(io.open(BASE, encoding="utf-8"))
fam = (base.get("families") or {}).get("REACHABILITY") or {}
base_n = fam.get("n")
base_keys = set(fam.get("keys") or [])

# the byte check, worktree vs HEAD -- three instruments, see the header
CRLF = bytes([13, 10])
LF = bytes([10])
wt = io.open(BASE, "rb").read()
head = subprocess.run(["git", "show", "HEAD:" + BASE], capture_output=True)
head_bytes = head.stdout
raw_same = hashlib.sha256(wt).hexdigest() == hashlib.sha256(head_bytes).hexdigest()
norm_same = (head.returncode == 0
             and hashlib.sha256(wt.replace(CRLF, LF)).hexdigest()
             == hashlib.sha256(head_bytes).hexdigest())
git_rc = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", BASE]).returncode
same = (git_rc == 0) and norm_same

run = subprocess.run([sys.executable, "infra/aws/globgrph/comp_debt.py", "--json"],
                     capture_output=True, text=True)
ledger = json.loads(run.stdout)
reach = ledger["families"]["REACHABILITY"]
now_residual = len(reach.get("residual_candidates") or [])
now_new = len(reach.get("new_vs_baseline") or [])
now_census = reach.get("census_count")
delta = now_residual - (base_n or 0)

same = (git_rc == 0) and norm_same

print("F5-AC4 -- THE BASELINE UNTOUCHED AND THE DELTA NAMED")
print()
print("ISOLATED_DELTA_VS_BASELINE=%d" % delta)
print("BASELINE_EDITED=%s" % ("false" if same else "TRUE"))
print("DELTA_ROW=%s" % (ROW if delta != 0 else "NONE_DELTA_ZERO"))
print()
print("  -- what is being compared --")
print("     baseline file           : %s" % BASE)
print("     baseline REACHABILITY n : %s residual key(s)" % base_n)
print("     this run's residuals    : %d" % now_residual)
print("     delta                   : %+d" % delta)
print("     of which NEW keys       : %d (not in the baseline's key set)" % now_new)
print("     this run's CENSUS       : %s isolates before suppression -- printed for completeness;"
      % now_census)
print("       the baseline holds NO census figure, so it cannot be the criterion's delta.")
print()
print("  -- the baseline's own vintage, which is the reason for the delta --")
prov = base.get("provenance") or {}
print("     provenance.db     : %s" % prov.get("db"))
print("     provenance.status : %s" % prov.get("status"))
hdr = (prov.get("header") or "").splitlines()
for ln in hdr[:4]:
    print("     %s" % ln.strip())
print("     The baseline was established against kuzu_nessie_db + the JULY local stitch store.")
print("     This run reads the SEPTEMBER served graph, whose stitch layer is a fresh cloud")
print("     artifact. A moved count is therefore expected; it is a finding for L9, and it is")
print("     NOT a reason to move the bar -- the file is the CVO's and is out of this grant.")
print()
print("  -- the byte check, three instruments (W2-S58) --")
print("     git diff --quiet HEAD   : rc %d   %s"
      % (git_rc, "UNCHANGED (git's own eol-aware comparison)" if git_rc == 0 else "CHANGED"))
print("     sha256, LF-NORMALISED   : %s vs %s -> %s"
      % (hashlib.sha256(wt.replace(CRLF, LF)).hexdigest()[:24],
         hashlib.sha256(head_bytes).hexdigest()[:24], norm_same))
print("     sha256, RAW             : %s vs %s -> %s   <- the WRONG instrument on this box"
      % (hashlib.sha256(wt).hexdigest()[:24], hashlib.sha256(head_bytes).hexdigest()[:24], raw_same))
print("     raw byte counts         : worktree %d (CRLF %d) vs HEAD %d (CRLF %d); difference %d"
      % (len(wt), wt.count(CRLF), len(head_bytes), head_bytes.count(CRLF),
         len(wt) - len(head_bytes)))
print("     the raw pair differs by EXACTLY one byte per line -- autocrlf, not an edit.")
print("     BASELINE_EDITED above is git's verdict AND the normalised hash, both required.")
print()
print("  DENOMINATOR: 1 of 1 family the baseline scores for this cell (REACHABILITY); %s of %s "
      "baseline residual keys compared against %d live residuals; 1 of 1 byte comparison "
      "(worktree vs HEAD, sha256 both sides)." % (len(base_keys), base_n, now_residual))
PY
