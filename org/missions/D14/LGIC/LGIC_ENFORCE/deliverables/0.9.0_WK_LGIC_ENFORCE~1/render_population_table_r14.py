"""EN-r-7 (round 14) -- THE ONE RENDERER for PLACEHOLDER_POPULATION_TABLE_R13.md.

S101 (round-13 L9, 0.9.0_WK_LGIC_ENFORCE~1): the r13 table rendered a brace as a parenthesis in the
`current` and `where` columns only -- `canonical` kept real `{`/`}` bytes, `current`/`where` did not,
so the SAME token rendered two different ways depending on which column it sat in.

1.0.0_SA_CTO, round-13 analysis @cf0cf68868, verbatim: "cut it to make both columns render through ONE
path, NOT to 'fix' the current column, or the asymmetry returns the next time a third column is added."

THE RULE CHOSEN HERE (the arm does not dictate which -- escape-everywhere and escape-nowhere both
satisfy it): every column's `{`/`}` bytes render as `(`/`)`. So no column is singled out by carrying
real brace bytes any more -- the escaping the r13 preamble relied on to let its own arm identify the
population (`PLACEHOLDER_POPULATION_TABLE_R13.md:7-16 @f658dc53cb`) is retired, and the population is
now read from the CENSUS JSON's raw `canonical` field directly (see `population_discriminator` in the
round-14 record) -- never from which column's RENDERED bytes still carry `{`.

`render_cell` at line 33 below is the ONE renderer. Every column of every row -- current, canonical,
verdict, type, plane, where -- is passed through it and NOTHING ELSE; there is no second code path.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS_REPORT = os.path.join(HERE, "NAMING_CENSUS_REPORT.r13.md")
OUT_TABLE = os.path.join(HERE, "PLACEHOLDER_POPULATION_TABLE_R13.md")

COLUMNS = ["current", "canonical", "verdict", "type", "plane", "where"]

_FENCE_RE = re.compile(r"```json\r?\n(.*?)\r?\n```", re.S)


def render_cell(value):
    """THE ONE RENDERER -- every column, every row, this function and nothing else.

    Escape-everywhere: `{`/`}` render as `(`/`)`. Chosen so no column is left carrying real brace
    bytes (the r13 asymmetry retired outright), never to single out one column as authoritative.
    """
    s = "" if value is None else str(value)
    return s.replace("{", "(").replace("}", ")")


def load_rows():
    with open(CENSUS_REPORT, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")
    m = _FENCE_RE.search(text)
    if not m:
        raise RuntimeError("no fenced json rows block found in %s" % CENSUS_REPORT)
    data = json.loads(m.group(1))
    return data["rows"]


def build_table_bytes(rows):
    """Every column of every row routed through render_cell -- ONE path, ONE rule."""
    lines = []
    lines.append("# PLACEHOLDER_POPULATION_TABLE_R13 -- one markdown table row per JUDGED census item (EN-p-37)")
    lines.append("")
    lines.append("Derived, at this cell's own write time, from `NAMING_CENSUS_REPORT.r13.md`'s fenced json `rows` list")
    lines.append("(the live+repo census run by this cell: `python lib/opal_naming.py census --live --repo --budget 600 --not-judged .../NOT_JUDGED_R13.json --report .../NAMING_CENSUS_REPORT.r13.md`, rc=0, CENSUS: COMPLETE,")
    lines.append("registry@9f4a569d7a54b53c over all 6 registry file(s)).")
    lines.append("")
    lines.append("**REGENERATED round 14 (EN-r-7) through ONE RENDERER, `render_population_table_r14.py:render_cell`.**")
    lines.append("Every column of every row -- current, canonical, verdict, type, plane, where -- renders through the")
    lines.append("SAME function and the SAME rule: `{`/`}` -> `(`/`)`. No column is singled out by carrying real brace")
    lines.append("bytes any more (that asymmetry was S101's finding, round-13 L9). The POPULATION R-38 measures over is")
    lines.append("read from the census json's raw `canonical` field directly -- never from which column's rendered")
    lines.append("bytes still carry `{` -- see `population_discriminator` in this round's `ONE_RENDER_PATH_R14.json`.")
    lines.append("")
    lines.append("columns: " + " | ".join(COLUMNS))
    lines.append("|".join(["-------"] * len(COLUMNS)))
    for row in rows:
        cells = [render_cell(row.get(c, "")) for c in COLUMNS]
        lines.append("| " + " | ".join(cells) + " |")
    body = "\r\n".join(lines) + "\r\n"
    return body.encode("utf-8")


def main():
    rows = load_rows()
    out = build_table_bytes(rows)
    with open(OUT_TABLE, "wb") as fh:
        fh.write(out)
    print("rows: %d" % len(rows))
    print("wrote: %s (%d bytes)" % (OUT_TABLE, len(out)))


if __name__ == "__main__":
    main()
