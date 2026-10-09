"""RIV-tw-1 J1 (AMENDMENT 1) and RIV-tc-1 J1 (AMENDMENT 2) -- the issuer's read of a transcribed vehicle log.

    python tw1_j1_read.py <git ref, e.g. origin/box/sitez> <YYYYMMDD>

Reads deliverables/0.0.3_BG_BBGTerminal/VEHICLE_LOG_<D>_1100Z.txt and, when present, the whole log
VEHICLE_LOG_<D>_1100Z.full.log at the ref (git show; nothing is written). The run REACHED the enrichment leg when its log
carries the `RIVALFUNDS ENRICHMENT STEP` line, an enrichment exit code other than 97, and no vendor-session-failure line.
Only such a run is J1-readable; then J1's evidence is: no `HISTORY OWED` line, and the leg's exit line as printed.
Prints a verdict line `J1-READ: REACHED|NOT-REACHED|NO-FILE` -- the GRADE is the CVO's, never this script's.
"""
import re
import subprocess
import sys

REF, DAY = sys.argv[1], sys.argv[2]
BASE = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.0.3_BG_BBGTerminal/"
FAIL_RE = re.compile(r"Failed to start session|session pool state=Failed|could not start blpapi session|\"unreachable\": true")


def show(path):
    r = subprocess.run(["git", "show", f"{REF}:{path}"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**__import__("os").environ, "MSYS_NO_PATHCONV": "1"})
    return r.stdout if r.returncode == 0 else None


full = show(BASE + f"VEHICLE_LOG_{DAY}_1100Z.full.log")
summ = show(BASE + f"VEHICLE_LOG_{DAY}_1100Z.txt")
text = full if full is not None else summ
if text is None:
    print(f"J1-READ: NO-FILE (neither transcription is at {REF}; control: git show {REF}:{BASE} lists the folder)")
    sys.exit(0)
lines = text.splitlines()
step = [ln for ln in lines if "RIVALFUNDS ENRICHMENT STEP" in ln]
exits = [ln for ln in lines if "RIVALFUNDS ENRICHMENT EXIT CODE" in ln]
fails = [ln for ln in lines if FAIL_RE.search(ln)]
owed = [ln for ln in lines if "HISTORY OWED" in ln and (full is not None or re.match(r"^\s*\d+:", ln))]  # the transcription's own header names HISTORY OWED; only copied log lines (<n>: ...) count
code = None
if exits:
    m = re.search(r"EXIT CODE:\s*(\d+)", exits[-1])
    code = int(m.group(1)) if m else None
print(f"source: {'full log' if full is not None else 'transcription only'} ({len(lines)} lines) at {REF}")
print(f"enrichment STEP lines: {len(step)}; exit lines: {exits or 'none'}; vendor-session-failure lines: {len(fails)}; "
      f"HISTORY OWED lines: {len(owed)}")
reached = bool(step) and code is not None and code != 97 and not fails
print("J1-READ: " + ("REACHED -- J1-readable: " + ("no HISTORY OWED line (switch unset, as expected)" if not owed
                                                    else f"{len(owed)} HISTORY OWED line(s): the switch is NOT unset")
                     if reached else "NOT-REACHED -- J1 reads UNVERIFIABLE for this run, never PASS"))
