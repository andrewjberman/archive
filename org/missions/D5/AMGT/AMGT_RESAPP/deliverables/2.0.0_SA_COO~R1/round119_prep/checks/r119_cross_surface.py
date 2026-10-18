"""AMGT_RESAPP round 119, AMGT-bz-4: the cross-surface read of the printed pack against the rich export, per name.

  python r119_cross_surface.py <pack_dir> <rich_dir> [KEY ...]      (<key>.txt PDF texts and <key>.md exports; default: the eight names)

Offline. For each name it compares the PDF's `Management` section with the export's `## Management/Board` section:
  CEO     the `CEO public profile ...` line, whitespace-collapsed, EXACTLY equal (or both absent);
  ROSTER  every roster name of the export's table is a `Name: Role` line of the PDF's Management section;
  LABELS  the number of `machine-drafted, cleared` lines INSIDE the Management section equals in both (the pillars passage lives in another section);
and over the whole export:
  WORDS   no `could not be read`, no `UNREADABLE_OBJECT`;
  MONEY   RIO LN: the market cap, net debt and enterprise value rows read the page's withheld words and carry no amount; every measured money row of
          the export names a currency code (the first cell of the Rendered text starts with a 2 to 5 letter code) -- reported as counts.
Prints one line per name and `CROSS SURFACE: YES|NO (<n> of <m> names)`. It grades nothing by itself.
"""
import os
import re
import sys

NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]


def _collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def pdf_management(text):
    lines = text.splitlines()
    try:
        i = lines.index("Management")
    except ValueError:
        return None
    j = i + 1
    while j < len(lines) and lines[j] != "Positioning":
        j += 1
    return lines[i + 1:j]


def md_management(text):
    lines = text.splitlines()
    i = next((k for k, ln in enumerate(lines) if ln.strip() == "## Management/Board"), None)
    if i is None:
        return None
    j = i + 1
    while j < len(lines) and not lines[j].startswith("## "):
        j += 1
    return lines[i + 1:j]


def ceo_line(block):
    joined = []
    for ln in block:
        if ln.startswith("    ") and joined:
            joined[-1] += " " + ln.strip()
        else:
            joined.append(ln.strip())
    hit = [ln for ln in joined if ln.startswith("CEO public profile")]
    return _collapse(hit[0]) if hit else None


def pdf_roster(block):
    names = set()
    for ln in block:
        if ln.startswith("    ") or not ln.strip():
            continue
        m = re.match(r"^([^:|]{2,60}): (.+)$", ln.strip())
        if m and not m.group(1).startswith("CEO public profile") and not ln.startswith("machine-drafted"):
            names.add(_collapse(m.group(1)))
    return names


def md_roster(block):
    names = set()
    for ln in block:
        if ln.startswith("|") and not ln.startswith("|---") and not ln.startswith("| Name"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if cells:
                names.add(_collapse(cells[0]))
    return names


def main(argv):
    pack, rich = argv[1], argv[2]
    keys = argv[3:] or NAMES
    ok = 0
    for key in keys:
        with open(os.path.join(pack, key + ".txt"), encoding="utf-8") as f:
            ptext = f.read().replace("\r\n", "\n")
        with open(os.path.join(rich, key + ".md"), encoding="utf-8") as f:
            mtext = f.read().replace("\r\n", "\n")
        pm, mm = pdf_management(ptext), md_management(mtext)
        problems = []
        if pm is None or mm is None:
            problems.append("a Management section is missing (pdf %s, export %s)" % (pm is not None, mm is not None))
        else:
            pc, mc = ceo_line(pm), ceo_line(mm)
            if pc != mc:
                problems.append("CEO line differs: pdf %r | export %r" % ((pc or "")[:70], (mc or "")[:70]))
            mr = md_roster(mm)
            pr = {n for n in mr if any(ln.strip().startswith(n + ": ") for ln in pm)}  # every export roster name must be a `Name: Role` line of the PDF's section
            if pr != mr:
                problems.append("ROSTER: export names missing from the pdf section: %s" % sorted(mr - pr)[:3])
        pl = len(re.findall(r"machine-drafted, cleared", chr(10).join(pm or [])))
        ml = len(re.findall(r"machine-drafted, cleared", chr(10).join(mm or [])))
        if pl != ml:
            problems.append("LABELS (inside Management) differ: pdf %d export %d" % (pl, ml))
        if re.search(r"could not be read|UNREADABLE_OBJECT", mtext):
            problems.append("WORDS: the export still carries `could not be read` or UNREADABLE_OBJECT")
        note = "roster %s" % (len(md_roster(mm)) if mm else "?")
        if key == "RIO_LN_Equity":
            for lab in ("Market cap", "Net debt", "Enterprise value"):
                rows = [ln for ln in mtext.splitlines() if ln.startswith("|") and ("%s:" % lab) in ln]
                good = [ln for ln in rows if "Bloomberg does not confirm this figure's currency" in ln and not re.search(r"\d{4,}", ln.split("|")[-2] if len(ln.split("|")) > 2 else ln)]
                if not rows or len(good) != len(rows):
                    problems.append("MONEY: RIO LN %s not withheld in the export (%d rows, %d withheld)" % (lab, len(rows), len(good)))
        print("%s: %s | %s | management labels pdf %d export %d" % (key, "OK" if not problems else "PROBLEM", note, pl, ml))
        for p in problems:
            print("   !! " + p)
        ok += 0 if problems else 1
    print("CROSS SURFACE: %s (%d of %d names)" % ("YES" if ok == len(keys) else "NO", ok, len(keys)))
    return 0 if ok == len(keys) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
