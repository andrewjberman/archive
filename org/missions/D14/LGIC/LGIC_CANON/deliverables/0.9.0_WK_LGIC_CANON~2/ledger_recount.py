#!/usr/bin/env python3
"""ledger_recount.py -- recount infra/logic/06_CONFORMANCE_LEDGER.md by script (LGIC_CANON cell CN-l-1, PRD DEC-7 (a), (d)).

Author: 0.9.0_WK_LGIC_CANON~2, task order LGIC_CANON.TO-CN-l-1.
Usage:  python ledger_recount.py [--ledger <path>]
Default ledger: <repo root>/infra/logic/06_CONFORMANCE_LEDGER.md. The repo root is the first directory above this file that
holds both org/ and .tools/, so the script runs from any cwd.

PRINTS
  SECTION <heading>: <n> rows (instrument: ...)   one line per level-2 section, n = its markdown table rows
  ROW <sec>:<k> <plane> | class=<c> | derived=<d> | column=<v>   one line per plane row
  REGISTER <id>: state=<s> kind=<k> decider=<d>    one line per register entry
  TOTAL <label>: <n>                              one line per row of section 7's count tables, n = THIS SCRIPT's count
  CHECK <label>: ledger=<n> script=<n> AGREES|DIFFERS
  DECIDED: <n>  /  WAITING: <n>                   derived over every plane row
  RECOUNT: OK | RECOUNT: MISMATCH <n>
Exit 0 when every section-7 number and every 'decided' cell equals this script's derivation; 1 otherwise; 2 on a read error.

THE INSTRUMENT
- A table row is a line opening with '|' below a header line and its '---' separator. Cells are split on '|' outside
  backtick code spans (an escaped '\\|' never splits). Every row's cell count is compared with its header's, and the split is
  compared with a plain split on every '|', so a pipe inside a cell is reported rather than absorbed.
- A PLANE TABLE is a table IN SECTIONS 1-5 (by heading number, never by header wording) whose header also has a cell
  exactly 'disposition'; section 7's own count table carries the same header cell today and is excluded by SECTION,
  not by renaming that cell -- the ledger is never shaped to fit this instrument. A plane row's
  CLASS is read from its disposition cell with bold markers and ~~struck~~ text removed, taking the first match in this order:
    AWAITING a word  the token AWAITING, or a named register entry X<n> whose section-6 state is not GRANTED;
    MIGRATE          the token MIGRATE; sub-class from the FIRST MIGRATE: '(format' -> format only; '(grammar' -> grammar;
                     else grammar when every rule in the row's 'rules' cell is an A3 naming rule (R1-R3), else home;
    RETIRE, DECLARED EXCEPTION, CONFORMANT, OUT OF SCOPE   the token itself.
  Tokens are upper-case whole words. Each row is counted ONCE, so the classes partition the plane rows and sum to the
  denominator. A row that groups several planes (x11, a b/s pair) is one row.
- DECIDED / WAITING: a row is WAITING exactly when its class is AWAITING a word. Its deciders are the 'decider:' named in each
  referenced register entry's row. The ledger's 'decided' cell must read exactly DECIDED or WAITING (<those deciders>).
- The REGISTER is the table whose header has an 'acknowledged' column; an entry's state is its 'state' cell.
"""
import argparse
import re
import sys
from pathlib import Path

LEDGER_REL = "infra/logic/06_CONFORMANCE_LEDGER.md"
SEP = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
A3_RULES = {"R1", "R2", "R3"}
MULT = "×"  # the multiplication sign the ledger uses for grouped planes (x11)
PLANE_SECTIONS = {"§1", "§2", "§3", "§4", "§5"}  # A-12: plane tables live ONLY in these sections; section 7's
# count table is excluded by SECTION even though its header cell reads 'disposition' like a plane table's does


def repo_root():
    for p in Path(__file__).resolve().parents:
        if (p / "org").is_dir() and (p / ".tools").is_dir():
            return p
    return None


def split_cells(line):
    """Cells of a markdown table line, split on '|' outside backtick code spans; '\\|' never splits."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, buf, in_code, i = [], [], False, 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def plain_split(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse(text):
    """[{heading, tables:[{hdr, line, rows:[(lineno, cells, plain_cells)]}]}] for each level-2 section."""
    sections, cur = [], None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^## (.+?)\s*$", ln)
        if m:
            cur = {"heading": m.group(1), "tables": []}
            sections.append(cur)
            i += 1
            continue
        if (cur is not None and ln.startswith("|") and i + 1 < len(lines)
                and SEP.match(lines[i + 1]) and "-" in lines[i + 1]):
            hdr = [c.replace("*", "").strip().lower() for c in split_cells(ln)]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append((j + 1, split_cells(lines[j]), plain_split(lines[j])))
                j += 1
            cur["tables"].append({"hdr": hdr, "line": i + 1, "rows": rows})
            i = j
            continue
        i += 1
    return sections


def plain(cell):
    return re.sub(r"~~.*?~~", "", cell).replace("*", "")


def has(token, text):
    return re.search(r"(?<![A-Za-z])" + re.escape(token) + r"(?![A-Za-z])", text) is not None


def sec_tag(heading):
    m = re.match(r"^(\S+?)\.", heading)
    return m.group(1) if m else heading[:6]


def main(argv):
    ap = argparse.ArgumentParser(description="recount the conformance ledger's tables")
    ap.add_argument("--ledger", help="ledger path (default: <repo root>/%s)" % LEDGER_REL)
    args = ap.parse_args(argv[1:])
    try:
        sys.stdout.reconfigure(errors="backslashreplace")
    except AttributeError:
        pass
    root = repo_root()
    path = Path(args.ledger) if args.ledger else (root / LEDGER_REL if root else None)
    if path is None or not path.is_file():
        print("ERROR: ledger not found: %s" % path)
        return 2
    with open(path, "r", encoding="utf-8") as f:  # A-12: explicit utf-8 -- cp1252 (this device's platform
        text = f.read()                            # default) mis-decodes non-ASCII bytes silently instead
                                                     # of raising, so the loud failure would be the lucky case
    shown = LEDGER_REL if not args.ledger else str(path)
    sections = parse(text)
    problems = []

    # ---- the register (section 6)
    reg, reg_order = {}, []
    for s in sections:
        for t in s["tables"]:
            if "acknowledged" in t["hdr"]:
                si = t["hdr"].index("state") if "state" in t["hdr"] else None
                ki = t["hdr"].index("kind") if "kind" in t["hdr"] else None
                for lineno, cells, _ in t["rows"]:
                    xid = cells[0].replace("*", "").strip()
                    joined = " | ".join(cells)
                    dm = re.search(r"decider:\s*([^\s;,()|·]+)", joined.replace("*", ""))
                    reg[xid] = {
                        "state": cells[si].replace("*", "").strip() if si is not None and si < len(cells) else "",
                        "kind": cells[ki].replace("*", "").strip().split()[0] if ki is not None and ki < len(cells) and cells[ki].strip() else "",
                        "decider": dm.group(1) if dm else None,
                        "line": lineno,
                    }
                    reg_order.append(xid)
    if not reg:
        problems.append("no register table (a header with an 'acknowledged' column)")

    # ---- SECTION lines
    for s in sections:
        tabs = s["tables"]
        n = sum(len(t["rows"]) for t in tabs)
        if not tabs:
            instr = "no markdown table in this section of %s; prose and bullets are not rows" % shown
        else:
            bad_count = sum(1 for t in tabs for _, c, _ in t["rows"] if len(c) != len(t["hdr"]))
            bad_split = sum(1 for t in tabs for _, c, p in t["rows"] if c != p)
            kinds = []
            for t in tabs:
                kind = ("plane table" if "disposition" in t["hdr"] else
                        "register table" if "acknowledged" in t["hdr"] else "table")
                kinds.append("%s at line %d [%s], %d rows" % (kind, t["line"], ",".join(t["hdr"]), len(t["rows"])))
            instr = ("%d markdown table(s) of %s read row by row -- a '|' line below a header and its '---' separator, cells "
                     "split on '|' outside backticks; %s; rows whose cell count differs from the header: %d; rows where a "
                     "plain '|' split disagrees: %d" % (len(tabs), shown, "; ".join(kinds), bad_count, bad_split))
            if bad_count:
                problems.append("%s: %d row(s) with a cell count unlike the header" % (s["heading"], bad_count))
            if bad_split:
                problems.append("%s: %d row(s) a plain '|' split reads differently" % (s["heading"], bad_split))
        print("SECTION %s: %d rows (instrument: %s)" % (s["heading"], n, instr))

    # ---- plane rows
    counts = {k: 0 for k in ("CONFORMANT", "MIGRATE (home)", "MIGRATE (format only)", "MIGRATE (grammar)", "RETIRE",
                             "DECLARED EXCEPTION", "AWAITING a word", "OUT OF SCOPE")}
    decided = waiting = plane_rows = plane_tables = 0
    column_missing = column_bad = 0
    smartx = []
    for s in sections:
        if sec_tag(s["heading"]) not in PLANE_SECTIONS:
            continue
        for t in s["tables"]:
            if "disposition" not in t["hdr"]:
                continue
            plane_tables += 1
            di = t["hdr"].index("disposition")
            ri = t["hdr"].index("rules") if "rules" in t["hdr"] else None
            ci = t["hdr"].index("decided") if "decided" in t["hdr"] else None
            if ci is None:
                column_missing += 1
                problems.append("%s: plane table at line %d has no 'decided' column" % (s["heading"], t["line"]))
            for k, (lineno, cells, _) in enumerate(t["rows"], 1):
                plane_rows += 1
                disp = plain(cells[di]) if di < len(cells) else ""
                rules = set(re.findall(r"R\d+", cells[ri])) if ri is not None and ri < len(cells) else set()
                refs = sorted(set("X" + n for n in re.findall(r"(?<![A-Za-z0-9])X(\d+)(?![0-9])", disp)))
                unknown = [r for r in refs if r not in reg]
                if unknown:
                    problems.append("line %d names register entries not in section 6: %s" % (lineno, unknown))
                open_refs = [r for r in refs if r in reg and reg[r]["state"] != "GRANTED"]
                if has("AWAITING", disp) or open_refs:
                    cls = "AWAITING a word"
                elif has("MIGRATE", disp):
                    m = re.search(r"(?<![A-Za-z])MIGRATE(?![A-Za-z])\s*(\([^)]*\))?", disp)
                    paren = (m.group(1) or "").lower()
                    if paren.startswith("(format"):
                        cls = "MIGRATE (format only)"
                    elif paren.startswith("(grammar"):
                        cls = "MIGRATE (grammar)"
                    elif rules and rules <= A3_RULES:
                        cls = "MIGRATE (grammar)"
                    else:
                        cls = "MIGRATE (home)"
                elif has("RETIRE", disp):
                    cls = "RETIRE"
                elif has("DECLARED EXCEPTION", disp):
                    cls = "DECLARED EXCEPTION"
                elif has("CONFORMANT", disp):
                    cls = "CONFORMANT"
                elif has("OUT OF SCOPE", disp):
                    cls = "OUT OF SCOPE"
                else:
                    cls = "UNCLASSIFIED"
                    problems.append("line %d: no disposition token" % lineno)
                if cls in counts:
                    counts[cls] += 1
                if cls == "AWAITING a word":
                    deciders = [reg[r]["decider"] for r in open_refs]
                    if not open_refs or any(d is None for d in deciders):
                        problems.append("line %d waits, but no register entry it names carries a 'decider:'" % lineno)
                    derived = "WAITING (%s)" % ", ".join(d or "?" for d in deciders)
                    waiting += 1
                else:
                    derived = "DECIDED"
                    decided += 1
                col = cells[ci].replace("*", "").strip() if ci is not None and ci < len(cells) else "<absent>"
                if ci is not None and col != derived:
                    column_bad += 1
                    problems.append("line %d: decided cell %r, derived %r" % (lineno, col, derived))
                plane = cells[0].replace("`", "")
                if "smartx/" in plane:
                    mm = re.search(MULT + r"\s*([\d,]+)", plane)
                    if mm:
                        smartx.append(int(mm.group(1).replace(",", "")))
                print("ROW %s:%d %s | class=%s | derived=%s | column=%s" % (sec_tag(s["heading"]), k, plane[:70], cls,
                                                                            derived, col))

    for xid in reg_order:
        r = reg[xid]
        print("REGISTER %s: state=%s kind=%s decider=%s (line %d)" % (xid, r["state"], r["kind"], r["decider"], r["line"]))

    # ---- what section 7 may name, by label
    by_label = {k.lower(): v for k, v in counts.items()}
    by_label["plane rows (the denominator)"] = plane_rows
    by_label["decided"] = decided
    by_label["waiting"] = waiting
    states = {}
    for xid in reg_order:
        states[reg[xid]["state"]] = states.get(reg[xid]["state"], 0) + 1
    for st, n in states.items():
        by_label[st.lower()] = n
    by_label["register entries (the denominator)"] = len(reg_order)

    s7 = [s for s in sections if s["heading"].startswith("§7.")]
    seen = set()
    checks = []
    if not s7:
        problems.append("no section headed 7.")
    else:
        for t in s7[0]["tables"]:
            for lineno, cells, _ in t["rows"]:
                label = cells[0].replace("*", "").strip()
                m = re.match(r"^\**\s*(\d[\d,]*)", cells[1]) if len(cells) > 1 else None
                if not m:
                    continue
                key = label.lower()
                if key not in by_label:
                    problems.append("section 7 line %d: label %r has no recount" % (lineno, label))
                    continue
                seen.add(key)
                mine, theirs = by_label[key], int(m.group(1).replace(",", ""))
                print("TOTAL %s: %d" % (label, mine))
                checks.append((label, theirs, mine))
        sx = re.search(r"SmartX[^\n]*?([\d,]{5,}) (?:entity-tree )?planes", "\n".join(
            ln for ln in text.splitlines()[text.splitlines().index("## " + s7[0]["heading"]):]))
        if smartx:
            print("SMARTX ENTITY-TREE PLANES: %d (%d rows: %s)" % (sum(smartx), len(smartx), " + ".join(map(str, smartx))))
            if sx:
                checks.append(("SmartX entity-tree planes (section 7 prose)", int(sx.group(1).replace(",", "")), sum(smartx)))
    for label, theirs, mine in checks:
        ok = theirs == mine
        print("CHECK %s: ledger=%d script=%d %s" % (label, theirs, mine, "AGREES" if ok else "DIFFERS"))
        if not ok:
            problems.append("section 7 %r: ledger %d, script %d" % (label, theirs, mine))
    for cls in counts:
        if cls.lower() not in seen:
            problems.append("class %r is not a row of section 7" % cls)

    print("DECIDED: %d" % decided)
    print("WAITING: %d" % waiting)
    print("DENOMINATOR: %d plane rows in %d plane tables; %d register entries; decided cells disagreeing: %d; "
          "plane tables without a 'decided' column: %d" % (plane_rows, plane_tables, len(reg_order), column_bad,
                                                           column_missing))
    for p in problems:
        print("PROBLEM: %s" % p)
    print("RECOUNT: OK" if not problems else "RECOUNT: MISMATCH %d" % len(problems))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
