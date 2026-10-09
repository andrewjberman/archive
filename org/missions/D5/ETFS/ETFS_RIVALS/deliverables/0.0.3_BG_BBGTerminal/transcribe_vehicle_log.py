"""Transcribe ONE day's vehicle (pull) log into the ETFS_RIVALS RIV-tw-1 J1 evidence file.

WHY THIS EXISTS: the ask (dell1 1.0.0_SA_CTO~DELL1 msg 1422, relayed as 0.0.3_BG_BBGTerminal
msg 32267) is for the 11:00Z fire's log lines VERBATIM -- the exit codes, the step names
reached, and whether a HISTORY OWED line appears or not. Retyping a line is how "verbatim"
stops being verbatim, so the lines are copied out of the file by this script and never by hand.

USAGE (from the workspace root, any seat alive after the 11:00Z fire):
    python -I org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.0.3_BG_BBGTerminal/transcribe_vehicle_log.py 20261009
then commit the printed path with .tools/safe-commit.sh and send the hash to 0.0.0_AB_MSTR~Z.

The producer is Scheduled Task OPAL_BBGTML_daily_pull (07:00 local = 11:00Z), which runs
`python -m rivalfunds.enrichment_bloomberg --mode daily` from the repository working tree
(RIV-tw-1 task order :67). Log family: ~/opal_bbg_logs/bbg_tplus1_<YYYYMMDD>_<HHMMSS>.log.

READ-ONLY on the log. Writes exactly one file under this seat's own deliverables dir.
"""
import glob
import os
import re
import sys

# The three field families the ask names. Kept as one pattern so the denominator below is
# over the SAME predicate that selects the lines -- a selector and a count that disagree is
# how a transcription stops matching its own summary.
FIELD_RE = re.compile(r"STEP|EXIT CODE")
OWED_RE = re.compile(r"HISTORY OWED")

# Lines that evidence a vendor-session failure, i.e. a fire that never REACHED the leg. Their
# presence is what makes a zero-HISTORY-OWED reading unverifiable rather than a pass
# (channel row ETFS_RIVALS-Z-S79).
UNREACHED_RE = re.compile(
    r"Failed to start session|session pool state=Failed|could not start blpapi session"
    r"|stopped trying to reconnect|\"unreachable\": true"
)


def main() -> int:
    if len(sys.argv) < 2 or not re.fullmatch(r"\d{8}", sys.argv[1]):
        print("ERROR: give one date as YYYYMMDD, e.g. 20261009")
        return 2
    day = sys.argv[1]
    home = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    pat = os.path.join(home, "opal_bbg_logs", "bbg_tplus1_%s_*.log" % day)
    hits = sorted(glob.glob(pat))
    if not hits:
        # A missing log is a FINDING, not a zero: say so and write nothing.
        print("ERROR: no vehicle log matches %s" % pat)
        print("       The 11:00Z fire did not run, or wrote elsewhere. Report the absence;")
        print("       do NOT substitute an ad-hoc run -- it is a different run (row S79).")
        return 3
    if len(hits) > 1:
        print("NOTE: %d logs match %s -- transcribing ALL of them, newest last." % (len(hits), pat))

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, "VEHICLE_LOG_%s_1100Z.txt" % day)
    L = []
    L.append("ETFS_RIVALS RIV-tw-1 J1 EVIDENCE -- vehicle (pull) log transcription, %s 11:00Z fire" % day)
    L.append("")
    L.append("Transcribed by 0.0.3_BG_BBGTerminal on the ask relayed as msg 32267")
    L.append("(dell1 1.0.0_SA_CTO~DELL1 msg 1422). Lines are COPIED by")
    L.append("transcribe_vehicle_log.py, never retyped.")
    L.append("Producer: Scheduled Task OPAL_BBGTML_daily_pull, 07:00 local = 11:00Z,")
    L.append("running `python -m rivalfunds.enrichment_bloomberg --mode daily` from the")
    L.append("repository working tree (RIV-tw-1 task order :67).")
    L.append("")

    for path in hits:
        with open(path, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8", errors="replace")
        lines = text.split("\n")
        field_hits = [(n + 1, ln) for n, ln in enumerate(lines) if FIELD_RE.search(ln)]
        owed_hits = [(n + 1, ln) for n, ln in enumerate(lines) if OWED_RE.search(ln)]
        unreached = [(n + 1, ln) for n, ln in enumerate(lines) if UNREACHED_RE.search(ln)]

        L.append("=" * 78)
        L.append("FILE:  %s" % path)
        L.append("BYTES: %d   LINES: %d" % (len(raw), len(lines) - 1 if text.endswith("\n") else len(lines)))
        L.append("=" * 78)
        L.append("")
        L.append("-- STEP NAMES REACHED AND EXIT CODES (verbatim, <file line>: <line>) --")
        L.append("   selector: /%s/   matched %d line(s)" % (FIELD_RE.pattern, len(field_hits)))
        L.append("")
        for n, ln in field_hits:
            L.append("%6d: %s" % (n, ln.rstrip("\r")))
        if not field_hits:
            L.append("   (none -- the fire wrote no step or exit-code line at all)")
        L.append("")
        L.append("-- HISTORY OWED --")
        L.append("   selector: /%s/   DENOMINATOR: whole file   occurrences: %d"
                 % (OWED_RE.pattern, len(owed_hits)))
        L.append("")
        if owed_hits:
            L.append("   A HISTORY OWED LINE APPEARS:")
            for n, ln in owed_hits:
                L.append("%6d: %s" % (n, ln.rstrip("\r")))
        else:
            L.append("   NO HISTORY OWED LINE APPEARS.")
        L.append("")
        L.append("-- DID THIS FIRE REACH THE ENRICHMENT LEG? --")
        if unreached:
            L.append("   NO. %d vendor-session-failure line(s) present, so the zero above is" % len(unreached))
            L.append("   NOT evidence the switch is off -- the leg never ran. J1 is")
            L.append("   UNVERIFIABLE on this day. See channel row ETFS_RIVALS-Z-S79")
            L.append("   (ARMED, disarm_owner 2.0.0_SA_COO~RV). Verbatim:")
            L.append("")
            for n, ln in unreached:
                L.append("%6d: %s" % (n, ln.rstrip("\r")))
        else:
            L.append("   No vendor-session-failure line found by /%s/." % UNREACHED_RE.pattern)
            L.append("   On this day the zero-or-one HISTORY OWED reading above is about the")
            L.append("   leg's own behaviour and is J1-readable. The GRADE is still")
            L.append("   3.0.0_SA_CVO~RV's on the issuer's real read (task order :88), never")
            L.append("   this seat's and never this file's.")
        L.append("")

    body = "\n".join(L) + "\n"
    nonascii = sum(1 for ch in body if ord(ch) > 127)
    if nonascii:
        print("WARN: %d non-ASCII character(s) in the output (log content carried through)" % nonascii)
    with open(out, "wb") as fh:
        fh.write(body.encode("utf-8"))
    print("WROTE %s (%d bytes)" % (out, len(body.encode("utf-8"))))
    print("NEXT: .tools/safe-commit.sh --author \"0.0.3_BG_BBGTerminal "
          "<0.0.3_BG_BBGTerminal@opal.agent>\" -F <msgfile> -- %s"
          % os.path.relpath(out).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
