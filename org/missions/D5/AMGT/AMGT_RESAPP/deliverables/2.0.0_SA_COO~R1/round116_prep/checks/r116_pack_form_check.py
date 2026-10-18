"""AMGT_RESAPP round 116 (AMGT-bw-2 / bw-5 grade): the FORM of a captured pack against the captured live pack from before the redeploy.

  python r116_pack_form_check.py <before_dir> <after_dir> [KEY ...]      (the dirs hold <key>.txt from r114_pack_capture_compare.py capture or r115_local_candidate_capture.py)

Offline (reads two folders of text). For each name it reads, in the AFTER text:
  ORDER   the narrative headings appear in the note order (Summary, Risks and considerations, Company description, Management, Positioning, Peers,
          What changed, Appendix: model figures) and the figures start AFTER every narrative heading;
  BODY    every narrative heading is followed by at least one body line that is not another heading;
  MGMT    the Management body is not the single not-written sentence;
  FIGURES the figure lines (from the line `Header` to the end, a wrapped line joined to its head) as a MULTISET against the BEFORE text's:
          the lines only in BEFORE and only in AFTER are listed, and every difference must be a money line (it names million, per share or the
          page's currency words) -- a difference on any other line is a figure the redeploy moved by accident.
Prints one line per check and `PACK FORM: YES|NO (<n> of <m> names)`. It grades nothing by itself: the verdict is the issuer's read of the lines.
"""
import os
import re
import sys

NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]
HEADINGS = ["Summary", "Risks and considerations", "Company description", "Management", "Positioning", "Peers", "What changed", "Appendix: model figures"]
MONEY = re.compile(r"million|per share|currency not stated|currency-adjusted|Bloomberg does not confirm", re.I)
OLD_NARRATIVE = ("Recommendation", "Investment thesis", "Company description", "Risks and considerations", "Management/Board")
NOT_WRITTEN = "No chief executive or board biography has been written for this company yet."


def _read(d, key):
    with open(os.path.join(d, key + ".txt"), encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n").split("\n")


def _joined(lines):
    out = []
    for ln in lines:
        if ln.startswith("    ") and out:
            out[-1] = out[-1] + " " + ln.strip()
        elif ln.strip():
            out.append(ln.strip())
    return out


def _figure_lines(lines):
    j = _joined(lines)
    try:
        i = j.index("Header")
    except ValueError:
        return []
    rest = j[i + 1:]
    for k, ln in enumerate(rest):  # the OLD layout printed the narrative AFTER the figures: the region ends at its first narrative heading
        if ln in OLD_NARRATIVE:
            return rest[:k]
    return rest


def _check(key, before_dir, after_dir):
    a = _read(after_dir, key)
    aj = _joined(a)
    problems, notes = [], []
    pos = {}
    for h in HEADINGS:
        if h in aj:
            pos[h] = aj.index(h)
    present = [h for h in HEADINGS if h in pos]
    if [pos[h] for h in present] != sorted(pos[h] for h in present):
        problems.append("ORDER: headings out of note order %r" % present)
    if "Appendix: model figures" not in pos:
        problems.append("ORDER: no 'Appendix: model figures' heading")
    elif "Header" not in aj or aj.index("Header") < pos["Appendix: model figures"]:
        problems.append("ORDER: figures start before the appendix heading")
    for h in present:
        nxt = aj[pos[h] + 1] if pos[h] + 1 < len(aj) else ""
        if not nxt or nxt in HEADINGS or nxt == "Header":
            problems.append("BODY: '%s' has no body line" % h)
    if "Management" in pos:
        body = aj[pos["Management"] + 1: pos["Management"] + 3]
        if len(body) == 1 and body[0] == NOT_WRITTEN or body[:1] == [NOT_WRITTEN] and (len(aj) <= pos["Management"] + 2 or aj[pos["Management"] + 2] in HEADINGS):
            notes.append("MGMT: only the not-written sentence")
    else:
        problems.append("ORDER: no Management heading")
    fb = _figure_lines(_read(before_dir, key))
    fa = _figure_lines(a)
    from collections import Counter
    cb, ca = Counter(fb), Counter(fa)
    only_b = list((cb - ca).elements())
    only_a = list((ca - cb).elements())
    stray = [x for x in only_b + only_a if not MONEY.search(x)]
    if stray:
        problems.append("FIGURES: %d changed non-money line(s), e.g. %r" % (len(stray), stray[0][:120]))
    notes.append("FIGURES: before %d lines, after %d; only-before %d, only-after %d (money lines)" % (len(fb), len(fa), len(only_b), len(only_a)))
    return problems, notes, only_b, only_a, present


def main(argv):
    before, after = argv[1], argv[2]
    keys = argv[3:] or NAMES
    ok = 0
    for key in keys:
        try:
            problems, notes, ob, oa, present = _check(key, before, after)
        except FileNotFoundError as e:
            print("%s: MISSING %s" % (key, e))
            continue
        print("%s: %s | sections %s" % (key, "OK" if not problems else "PROBLEM", ", ".join(present)))
        for n in notes:
            print("   " + n)
        for p in problems:
            print("   !! " + p)
        for x in ob[:4]:
            print("   - " + x[:150])
        for x in oa[:4]:
            print("   + " + x[:150])
        ok += 0 if problems else 1
    print("PACK FORM: %s (%d of %d names)" % ("YES" if ok == len(keys) else "NO", ok, len(keys)))


if __name__ == "__main__":
    main(sys.argv)
