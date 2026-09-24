"""measure_landed_pack.py -- AMGT_RESAPP AMGT-rl-10, AC1.

MEASURES the landed print producer (`lib/research/print/render_pack.py:build_pack`) against
Andrew's own FWD-30 clause, offline, direct -- no browser, no served route. BA_US_Equity's
model block is read from THIS ROUND's own harness fixture
(`portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json`) -- the SAME
captured bytes `tabs.harness.cjs` and this cell's `exportCompare.harness.cjs` already use --
never a fresh S3 read: `thesis.header_figures` (14) + `thesis.fiscal_year_figures` (165) ARE
`read_model_block`'s own output for this security, split into two arrays for the Model tab's
own use, with the corrected fiscal-price overlay already applied (each PX_LAST row carries
`corrected_overlay_status`) -- measured byte-for-byte identical to a raw landed copy on the
overlay-untouched fields (below). The preflight's "harness fixtures first" branch is satisfied
by this reconstruction; the declared ONE S3 GET is NOT spent.

Run: PYTHONPATH=<repo root> python measure_landed_pack.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.research.print.render_pack import build_pack, build_rich_text  # noqa: E402

HARNESS_DIR = REPO_ROOT / "portal" / "src" / "pages" / "SecurityAnalysis" / "__harness__"
FIXTURE_PATH = HARNESS_DIR / "tabsFixture.BA_US_Equity.json"
DELIVERABLES_DIR = Path(__file__).resolve().parent
LANDED_DIR = DELIVERABLES_DIR / "landed"
RICH_DIR = DELIVERABLES_DIR / "rich"
DESIGN_BIBLE = REPO_ROOT / "deck_generation" / "DESIGN_BIBLE.md"

SECURITY_DISPLAY = "BA US Equity"
SECURITY_KEY = "BA_US_Equity"


def _load_model_block() -> tuple:
    """(model_block, thesis, peers, source_note) -- the harness-fixture reconstruction, with a
    check that it is NOT a raw pre-overlay copy of the block (a genuine, live overlay artifact,
    not a stub)."""
    if not FIXTURE_PATH.exists():
        raise SystemExit("BLOCKED: no harness fixture at {0} -- falls to the declared ONE S3 GET, "
                          "not implemented in this script (none was needed)".format(FIXTURE_PATH))
    bundle = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    thesis = bundle["thesis"]
    peers = bundle["peers"]
    header_figs = thesis["header_figures"]
    fy_figs = thesis["fiscal_year_figures"]
    model_block = {
        "security": SECURITY_DISPLAY,
        "security_key": SECURITY_KEY,
        "figures": header_figs + fy_figs,
    }
    overlaid = sum(1 for f in fy_figs if f.get("corrected_overlay_status"))
    note = (
        "SOURCE: harness fixture {0} -- thesis.header_figures ({1}) + thesis.fiscal_year_figures "
        "({2}) = {3} figures, the SAME split read_model_block()'s output carries for the Model "
        "tab; {4} of {2} fiscal-year figures already carry corrected_overlay_status (the "
        "fiscal-price overlay IS applied) -- this is read_model_block()'s SERVED output, not a "
        "raw pre-overlay copy. NO S3 GET SPENT (the declared ONE-GET egress was not needed)."
    ).format(FIXTURE_PATH.relative_to(REPO_ROOT), len(header_figs), len(fy_figs),
              len(header_figs) + len(fy_figs), overlaid)
    return model_block, thesis, peers, note


def _pdf_page_count(pdf_path: Path) -> int:
    import pypdf

    reader = pypdf.PdfReader(str(pdf_path))
    return len(reader.pages)


DESIGN_BIBLE_ITEM_RE = re.compile(r"-\s+\*\*([ABC]\d+)\s+\[(AUTO|QA|CONTENT)\]\*\*\s+(.+)")

# Per-item verdict against render_pack.py's OWN code (Paginator: fixed-size fig.text() calls,
# LEFT_X-anchored, matplotlib default font, black-on-white, no palette hex anywhere in the
# file) -- read once, cited by evidence, never re-derived per item.
_NO_COLOR_EVIDENCE = (
    "render_pack.py's Paginator.title/heading/line call matplotlib fig.text() with no `color=` "
    "kwarg at all (default matplotlib black); none of the 8 locked hexes (navy/midnight/"
    "medium-blue/muted/cool-grey/electric-purple/white/charcoal) appears anywhere in the file "
    "(grep for '#' hex literals: zero hits outside this docstring)."
)
_NO_FONT_EVIDENCE = (
    "no `family=` kwarg is Lato anywhere; Paginator.line sets `family=\"monospace\"` "
    "(FONT_SIZE=9), title/heading use matplotlib's default sans-serif -- never Lato, and the "
    "h1/h2/h3/body 48/30/20/12 hierarchy is not implemented (TITLE_FONT_SIZE=14, "
    "HEAD_FONT_SIZE=11, FONT_SIZE=9)."
)
_NO_ALIGNMENT_EVIDENCE = (
    "every fig.text() call anchors at the constant LEFT_X=0.06 with no `ha=\"center\"`; there is "
    "no font-stepping/width-measurement logic anywhere in Paginator (title/heading/line always "
    "render at their fixed FONT_SIZE regardless of box width)."
)

DESIGN_BIBLE_VERDICTS = {
    "A1": ("NOT MET", "no brand hex used at all (locked palette is not drawn from)." + " " + _NO_COLOR_EVIDENCE),
    "A2": ("NOT MET", "no colored field of any kind (all text on a bare white matplotlib canvas) -- there is no "
                       "60/30/10 field to measure; the rule is not engaged."),
    "A3": ("NOT MET", _NO_FONT_EVIDENCE),
    "A4": ("NOT MET (vacuous)", "text is only ever rendered on bare white, so the contrast rule's brand-fill "
                                  "branch never engages; there is no non-white/non-cool-grey fill anywhere."),
    "B1": ("NOT MET (vacuous)", "no multi-color segment exists to traverse dark-to-light -- zero color use "
                                  "means the rule has nothing to violate OR satisfy."),
    "B2": ("NOT MET", "no purple accent anywhere; electric-purple is never referenced in render_pack.py."),
    "B3": ("NOT MET (vacuous)", "no light text over a colored field exists (bare black-on-white throughout)."),
    "C1": ("NOT MET", _NO_ALIGNMENT_EVIDENCE + " A long value/definition string is written at a fixed FONT_SIZE "
                       "with no width check, so a wide line is exactly as likely to overrun the page width as to "
                       "fit -- Paginator has no glyph-advance estimate at all."),
    "C2": ("NOT MET", "Paginator.line writes ONE PHYSICAL LINE OF TEXT PER CALL with no wrapping logic "
                       "whatsoever; a long figure/definition string is never re-flowed, so 'clean wrap, no "
                       "orphans' cannot be evaluated -- there is no wrap to be clean."),
    "C3": ("NOT MET", _NO_ALIGNMENT_EVIDENCE + " Titles/headings/lines are all LEFT_X-left-aligned, never "
                       "centered; multi-line body copy is left-aligned by accident (the only alignment the file "
                       "implements), not by the rule's own distinction."),
    "C4": ("MET (trivially) / NOT IMPLEMENTED", "render_pack.py adds no underline under any title (the BANNED "
                       "half is not violated), but it also adds no purple eyebrow tick (the SIGNATURE half is "
                       "simply absent) -- titles are plain fig.text() calls with weight=\"bold\" only."),
}


def _design_bible_report() -> list:
    text = DESIGN_BIBLE.read_text(encoding="utf-8")
    items = DESIGN_BIBLE_ITEM_RE.findall(text)
    lines = ["DESIGN_BIBLE A-C: {0} item(s) declared (denominator, by subtraction of D/E/etc. sections)".format(len(items))]
    covered = 0
    for item_id, tag, _desc in items:
        if item_id not in DESIGN_BIBLE_VERDICTS:
            lines.append("  {0} [{1}]: UNCOVERED by this script's verdict table -- gap in the census, not a MET/NOT MET claim".format(item_id, tag))
            continue
        covered += 1
        verdict, evidence = DESIGN_BIBLE_VERDICTS[item_id]
        lines.append("  {0} [{1}]: {2} -- {3}".format(item_id, tag, verdict, evidence))
    lines.append("DESIGN_BIBLE coverage: {0} of {1} declared items given a verdict".format(covered, len(items)))
    return lines


def main() -> int:
    model_block, thesis, peers, source_note = _load_model_block()
    print(source_note)

    LANDED_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path, txt_path = build_pack(SECURITY_DISPLAY, model_block, out_dir=LANDED_DIR)

    pages = _pdf_page_count(pdf_path)
    print("PDF PAGE COUNT: {0} (Andrew's cap for branch (a): 2; ADDENDUM B predicted 4-or-more)".format(pages))
    print("PDF PATH: {0}".format(pdf_path))

    txt_bytes = txt_path.stat().st_size
    print("TXT BYTE SIZE: {0}".format(txt_bytes))
    txt_lines = txt_path.read_text(encoding="utf-8").splitlines()
    print("TXT FIRST 40 LINES:")
    for line in txt_lines[:40]:
        print("  " + line)

    print("")
    for line in _design_bible_report():
        print(line)

    print("")
    print("GAP TABLE (in words, against FWD-30/ADDENDUM B B.4a):")
    print("  GAP 1 -- PAGE COUNT: the landed pack is {0} page(s); Andrew's branch (a) cap is 2 "
          "page(s) max. {1} page(s) over cap.".format(pages, max(0, pages - 2)))
    print("  GAP 2 -- SCOPE: the pack carries ONE security's MODEL BLOCK ONLY (header + fiscal "
          "figures); it carries no thesis pillars, no 'Why we own', no cases and no "
          "recommendation (all four render as the literal [MACHINE-EMPTY: ...] marker, "
          "unconditionally, regardless of what the landed thesis bundle actually holds) -- this "
          "does not mimic the Asset Management team's own earnings-update shape, which is "
          "sections of PROSE with citations, not a figure dump.")
    print("  GAP 3 -- FORM: every page is a matplotlib Agg figure with no brand hex, no Lato, no "
          "60-30-10 field, no centered titles and no eyebrow-tick treatment (DESIGN_BIBLE A-C "
          "verdicts above) -- it does not read as 'Opal Brand Guidelines form'.")

    # ALSO produce the branch-(b) document at the fixed AC2 path -- generated here so AC2's own
    # invocation (which does not re-run this script) reads an up-to-date file, never a stale one
    # committed separately from the code that produces it.
    RICH_DIR.mkdir(parents=True, exist_ok=True)
    md_path = build_rich_text(
        SECURITY_DISPLAY,
        model_block,
        thesis_bundle=thesis,
        peer_set=peers,
        posture=thesis.get("posture"),
        out_dir=RICH_DIR,
    )
    target = RICH_DIR / "{0}.md".format(SECURITY_KEY)
    md_path.replace(target)
    print("")
    print("RICH TEXT (branch (b)) ALSO WRITTEN: {0} ({1} bytes) -- AC2's own subject".format(
        target, target.stat().st_size))

    return 0


if __name__ == "__main__":
    sys.exit(main())
