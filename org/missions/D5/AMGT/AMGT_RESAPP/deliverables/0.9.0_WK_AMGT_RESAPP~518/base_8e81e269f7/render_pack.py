"""render_pack.py -- Adam's artifact, rendered SERVER-SIDE.

Renders ONE security's model block into a PDF reproducing the blank template's four blocks, in
order (F1): the pasted Excel model block / RECOMMENDATION + COMPANY DESCRIPTION / INVESTMENT
THESIS | RISKS AND CONSIDERATIONS / bio (the template's own "Management/Board" heading).

ROUND 12 (AMGT-rk-6, gap G3, ADDENDUM 1 R2, contract C-ROUND12-PRINT-SERVER-SIDE). THIS FILE
CARRIED THREE THINGS THAT CANNOT EXIST IN A LAMBDA, and the print route returned 500 for all
three at once (direct invoke 04:57Z: `internal error in the AMGT scoped read API`):

  1. THE PLOTTING LIBRARY WAS IMPORTED AT MODULE SCOPE. Any importer of this module -- the
     adapter's route table among them -- paid the import whether or not it rendered anything,
     and in the deployed package the import did not resolve at all. It is now taken INSIDE
     `_plotting()`, at call time, so importing this module costs nothing and an absent
     dependency surfaces on the one request that needs it instead of at cold start.
  2. THE TEMPLATE WAS READ FROM A PER-BOX SYNCED-DOCUMENT PATH. It now lives in the POOL, at
     the address `TEMPLATE_BUCKET`/`TEMPLATE_KEY` below, and is read through the caller's own
     pool client -- the same seam every other pool read in this estate uses.
  3. THE MODEL BLOCK WAS READ FROM ONE WORKER'S DELIVERABLES FOLDER, a directory that does not
     exist in the deployed package. `build_pack()` no longer reads an input at all: the CALLER
     hands it the block it already holds (the adapter reads it from
     `derived/model_block/<key>/<stamp>/model_block.json` and applies the corrected
     fiscal-price overlay before calling). ONE READER, ONE OVERLAY APPLICATION -- this module
     must NOT re-apply it, and does not.

STOP -- NOT A BROWSER PRINT, DELIBERATELY. FWD-5's wording is "Adam forwards a printed pack without
reformatting it": the displacement test is that a person forwards the output AS PRODUCED. A
browser-rendered print is the analyst's own reformatting under another name -- it would satisfy
a criterion while failing the outcome.

LIBRARY CHOICE, STATED (bound: "Use a library python already has or the repo already vendors;
state which"): the Agg PDF backend draws real, TEXT-LAYER pages (verified: text drawn via
`fig.text()` round-trips through `pypdf.PdfReader(...).extract_text()` byte-identical to what
was written, not rendered as unselectable vector paths), and `pypdf` is the extraction
instrument. Both now ship in the function's dependency layer rather than being assumed present
on whatever box happened to run this; nothing is installed at request time.

WHERE THE OUTPUT GOES: `build_pack()` writes into `out_dir`, defaulting to the interpreter's own
temporary directory -- the only writable location in a Lambda. It never writes into the repo.

C-MARK-NOT-DEGRADE: every section the drafting/coverage/bio engines have not yet filled (today:
all of them, per SPEC_SECTION_drafting.md's own admission) says so in plain words (`NOT_WRITTEN`; AMGT-ax-4
removed the raw "[MACHINE-EMPTY: ...]" marker from the PDF) -- never a blank page that looks finished,
never invented prose.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2].parent))  # repo root, for `lib.*`
from lib.research.api import model_words  # noqa: E402  AMGT-ww-4: the ONE served definition of the Model words
from lib.research.freshness.long_day import long_day  # noqa: E402  AMGT-bu-3: the ONE house long form of a date
from lib.research.provenance.render_print import (  # noqa: E402
    NOT_MEASURED_PREFIXES,
    UNRESOLVED_MARKER,
    render_figure_line,
)

# THE TEMPLATE, IN THE POOL (AMGT-rk-6 item 2). Read-only, never written to, and read through a
# pool client the caller supplies -- so a test, an offline render and the deployed function all
# reach it through the one seam.
#
# IT SITS UNDER packs/, WHICH IS A GRANTED PREFIX, AND NOT UNDER A NEW TOP-LEVEL ONE. A new
# top-level prefix would need a read grant neither never-widen half signed, and the CTO half
# says so in terms: the template's key sits under one of the twelve prefixes the role reads
# after this act, "never under a NEW top-level prefix, which would need a grant nobody
# signed." packs/ is also where it belongs -- it is the research PACK template, and packs/ is
# the research pack store. The leading underscore keeps it out of the security-key namespace
# that prefix's other children use, the same convention as the management pool's own "_pool".
TEMPLATE_BUCKET = "opal-data-harvest"
TEMPLATE_PREFIX = "packs/_template/"
TEMPLATE_NAME = "NEW_Research_Pack_Template_2026_03_09_v1.docx"
TEMPLATE_KEY = TEMPLATE_PREFIX + TEMPLATE_NAME

PAGE_SIZE = (8.5, 11.0)
TOP_Y = 0.95
BOTTOM_Y = 0.04
LINE_HEIGHT = 0.020
LEFT_X = 0.06
FONT_SIZE = 9
TITLE_FONT_SIZE = 14
HEAD_FONT_SIZE = 11

# AMGT-aw-2 (AMGT_RESAPP round 73, FWD-5): NO LINE PAST THE PAGE EDGE. The page is 8.5 in wide and text
# starts at LEFT_X (0.06 of the width, 0.51 in); the same margin is kept on the right, so 7.48 in
# (539 pt) of text width remains. A 9 pt monospace character is 0.6 em = 5.4 pt, so 99 characters
# fit; the wrap is set at 92 to leave room. The 11 pt bold heading and 14 pt bold title are
# proportional fonts averaging up to 0.65 em (7.2 pt and 9.1 pt per character), so their wraps are
# set at 66 and 50 characters.
LINE_WRAP_CHARS = 92
HEAD_WRAP_CHARS = 66
TITLE_WRAP_CHARS = 50
WRAP_INDENT = "    "

# AMGT-ax-4 (AMGT_RESAPP round 74, FWD-5, CTO ruling 2): THE PRINT IN OPAL BRAND FORM, FROM THE ESTATE'S
# EXISTING ASSETS, NOTHING INVENTED. The font is Lato (regular for the body, bold for headings): the two
# faces and their licence are copies of `portal/src/pages/InvestorReporting/render/assets/fonts/` (the
# same files the investor-report export uses), kept in `fonts/` beside this module so they ride the
# package. The colours are the portal's design tokens (`portal/design/brands/opal-capital.json`, read
# through `portal/src/index.css`): heading and body ink = `semantic.text.primary` / `semantic.text.body`
# = `palette.navy` #163372; the rule under a heading = `semantic.border.default` = `palette.mutedTint`
# #C4CBDB (the hairline token, `--hairline`).
FONT_DIR = Path(__file__).resolve().parent / "fonts"
FONT_REGULAR_FILE = "Lato-Regular.ttf"
FONT_BOLD_FILE = "Lato-Bold.ttf"
HEADING_COLOUR = "#163372"  # semantic.text.primary -> palette.navy
BODY_COLOUR = "#163372"     # semantic.text.body    -> palette.navy
RULE_COLOUR = "#C4CBDB"     # semantic.border.default -> palette.mutedTint (--hairline)
RULE_WIDTH = 0.8
RULE_DROP = 0.007           # the rule sits this far (page fraction) under a heading's baseline

# Plain words for a section nobody has written yet (never an internal marker).
NOT_WRITTEN = {
    "recommendation": "No recommendation has been written for this company yet.",
    "company_description": "No company description is available for this company yet.",
    "thesis": "No investment thesis has been written for this company yet.",
    "risks": "No risks or considerations have been written for this company yet.",
    "bio": "No chief executive or board biography has been written for this company yet.",
}


# AMGT-bv-2: a day is matched only when no digit touches it, so the day-shaped run inside an accession number
# (`0001234567-12-150001` reads `4567-12-15`) is never rewritten. A real day in prose is never digit-adjacent.
_DAY_IN_TEXT = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?Z?)?(?!\d)")


class _Verbatim(str):
    """AMGT-bv-2 (AMGT_RESAPP round 115, CTO ruling W506-S5): a line printed as a SOURCE'S OWN WORDS. Every other
    printed line passes through `_long_days`; a line carried as this type is never rewritten (a verbatim quotation
    stays byte-faithful, in the pack and in the rich export)."""


def _is_source_quotation(sentence) -> bool:
    """AMGT-bv-2: a served sentence that IS the filing's own text. `drafting_build` writes such a sentence with
    generated=False and quoted_spans == [text] (its filing-sentence branch). A drafted sentence (generated=True), or
    a sentence whose span is only part of its text, is the system's own prose and is NOT a quotation."""
    if not isinstance(sentence, dict) or sentence.get("generated") is not False:
        return False
    return list(sentence.get("quoted_spans") or []) == [str(sentence.get("text") or "")]


def _long_days(value):
    """AMGT-bu-3 (AMGT_RESAPP round 114, CTO ruling 2 of the round-113 analysis): every date a reader sees on the
    printed pack is the house long form (`long_day`). Each ISO day in `value` -- a bare day, or a day inside a served
    sentence -- is replaced by its long form; a timestamp keeps its day only (the time is cut, as `_figure_date_text`
    already cuts it). Any other text, and any non-text value, comes back as it came. DISPLAY ONLY: no served value,
    no sort key, no comparison and no max() over dates is changed by this."""
    if not isinstance(value, str) or isinstance(value, _Verbatim):
        return value
    return _DAY_IN_TEXT.sub(lambda m: long_day(m.group(0)[:10]), value)


def _wrap(text: str, width: int, indent: str = WRAP_INDENT, verbatim: bool = False) -> list:
    """`text` cut at spaces into lines of at most `width` characters, a continuation line indented;
    a word longer than the width is cut (never left to run off the page). Empty text gives one empty line.
    AMGT-bu-3: the long form is applied BEFORE the cut, so a wrap is measured on the text that is printed; this is
    the one place every printed pack line (title, heading, body) passes through.
    AMGT-bv-2: `verbatim=True` prints the text as the source wrote it -- no long form (a verbatim quotation)."""
    text = str(text) if verbatim else _long_days(str(text))
    if not text.strip():
        return [""]
    return textwrap.wrap(text, width=width, subsequent_indent=indent, break_long_words=True,
                         break_on_hyphens=False, replace_whitespace=True, drop_whitespace=True) or [""]


def _plotting():
    """THE DEFERRED IMPORT (AMGT-rk-6 item 1). Returns `(plt, PdfPages)`.

    Taken at CALL time, never at module scope, for two measured reasons. First, the adapter
    imports this module from `_print_pack` and its route table is built by a module that
    imports the adapter -- a module-scope plotting import made every one of those importers pay
    for a library only the print route uses, and made the WHOLE package fail to load when it was
    absent. Second, the plotting library writes a font cache on first use and picks its location
    from the environment BEFORE it is imported; the only writable directory in the deployed
    runtime is the temporary one, so that choice is made here, immediately before the import,
    where it can still take effect. `setdefault` means a caller that has already chosen a
    location keeps it.
    """
    cache_dir = os.path.join(tempfile.gettempdir(), "mplconfig")
    os.environ.setdefault("MPLCONFIGDIR", cache_dir)
    try:
        os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
    except OSError:
        pass  # a read-only location is the library's own fallback path, not this module's
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    return plt, PdfPages


def read_template_block_headers(pool_client, bucket: str = TEMPLATE_BUCKET, key: str = TEMPLATE_KEY) -> dict:
    """Read-only confirmation of the template's own wording (F1: 11 paragraphs, 3 tables, 1
    image), from the POOL, via stdlib zip+XML (a .docx is a zip of XML parts, so no document
    library is needed and none is packaged).

    `pool_client` is the caller's own S3-shaped client -- the same object the adapter's
    `_pool_client()` returns, which is either the live client or the directory-backed one a
    test supplies. This function never constructs a client and never names a filesystem path,
    so there is exactly one place the template's address is configured: the constants above.
    """
    w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    body_bytes = pool_client.get_object(Bucket=bucket, Key=key)["Body"].read()
    import io as _io

    with zipfile.ZipFile(_io.BytesIO(body_bytes)) as z:
        media = [n for n in z.namelist() if "media" in n]
        xml_bytes = z.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    body = root.find(w + "body")
    paras, tables = [], []
    for child in body:
        tag = child.tag.replace(w, "")
        if tag == "p":
            paras.append("".join(t.text or "" for t in child.iter(w + "t")))
        elif tag == "tbl":
            rows = []
            for row in child.findall(w + "tr"):
                rows.append(
                    ["".join(t.text or "" for t in cell.iter(w + "t")) for cell in row.findall(w + "tc")]
                )
            tables.append(rows)
    return {"paragraphs": paras, "tables": tables, "n_images": len(media)}


def security_key(security: str) -> str:
    """Path-safe form of the display security string, for LOCAL FILESYSTEM artifact
    names only (`build_pack()`'s pdf_path/txt_path below) -- never for an S3 key,
    which already tolerates `/` fine. AMGT-rk-23, row AMGT_RESAPP-Z-S141: a raw
    slash (e.g. the LSE ticker root `BP/`) survives the space-only replace and
    lands in `pdf_path`/`txt_path` as a literal path separator, so `pack_NG/_LN_
    Equity.pdf` resolves to a non-existent `pack_NG/` subdirectory and 500s."""
    return security.replace(" ", "_").replace("/", "-")


def _brand_fonts() -> tuple:
    """`(regular, bold)` Lato `FontProperties`, registered with the plotting library's font manager and
    read from the package's own `fonts/` by file, so no system font and no font cache decides the face.
    A missing file is an error, never a silent fall back to the library's default font."""
    from matplotlib import font_manager

    faces = []
    for name in (FONT_REGULAR_FILE, FONT_BOLD_FILE):
        path = FONT_DIR / name
        if not path.is_file():
            raise FileNotFoundError("the brand font file is missing from the package: {0}".format(path))
        font_manager.fontManager.addfont(str(path))
        faces.append(font_manager.FontProperties(fname=str(path)))
    return faces[0], faces[1]


class Paginator:
    """Collects lines and headings, splitting into PDF pages when a page fills.

    `plt` is handed in rather than read from a module global: the plotting library is imported
    at call time (see `_plotting`), so there is no module-level name to reach for. Body text is Lato
    Regular and headings Lato Bold in the portal's ink colour, each heading with a hairline rule under it.
    """

    def __init__(self, pdf, plt):
        self.pdf = pdf
        self.plt = plt
        self._regular, self._bold = _brand_fonts()
        self._fig = None
        self._ax = None
        self._y = TOP_Y
        self._new_page()

    def _new_page(self):
        if self._fig is not None:
            self.pdf.savefig(self._fig)
            self.plt.close(self._fig)
        self._fig = self.plt.figure(figsize=PAGE_SIZE)
        self._ax = self._fig.add_axes([0, 0, 1, 1])
        self._ax.set_xlim(0, 1)
        self._ax.set_ylim(0, 1)
        self._ax.axis("off")
        self._y = TOP_Y

    def _ensure_room(self, n_lines: int = 1):
        if self._y - n_lines * LINE_HEIGHT < BOTTOM_Y:
            self._new_page()

    def _text(self, text: str, face, size: float, colour: str):
        props = face.copy()
        props.set_size(size)
        # a dollar sign is escaped: a bare pair would be read as maths text, and one drafted sentence with
        # two "$" amounts made the whole print refuse (AMGT-ay-1, the BA thesis sentences).
        self._fig.text(LEFT_X, self._y, text.replace("$", chr(92) + "$"), fontproperties=props, color=colour)

    def _rule(self):
        self._ax.hlines(self._y - RULE_DROP, LEFT_X, 1 - LEFT_X, colors=RULE_COLOUR, linewidth=RULE_WIDTH)

    def title(self, text: str):
        parts = _wrap(text, TITLE_WRAP_CHARS, indent="")
        for i, part in enumerate(parts):
            self._ensure_room(2)
            self._text(part, self._bold, TITLE_FONT_SIZE, HEADING_COLOUR)
            if i == len(parts) - 1:
                self._rule()
            self._y -= LINE_HEIGHT * 2

    def heading(self, text: str):
        parts = _wrap(text, HEAD_WRAP_CHARS, indent="")
        for i, part in enumerate(parts):
            self._ensure_room(2)
            self._text(part, self._bold, HEAD_FONT_SIZE, HEADING_COLOUR)
            if i == len(parts) - 1:
                self._rule()
            self._y -= LINE_HEIGHT * 1.5

    def line(self, text: str, verbatim: bool = False):
        for part in _wrap(text, LINE_WRAP_CHARS, verbatim=verbatim):
            self._ensure_room(1)
            self._text(part, self._regular, FONT_SIZE, BODY_COLOUR)
            self._y -= LINE_HEIGHT

    def blank(self):
        self._ensure_room(1)
        self._y -= LINE_HEIGHT

    def page_break(self):
        """Force the next content onto a fresh page (used between the template's four blocks,
        matching the reference pack's own layout: each block starts its own page)."""
        self._new_page()

    def finish(self):
        if self._fig is not None:
            self.pdf.savefig(self._fig)
            self.plt.close(self._fig)
            self._fig = None


def _fiscal_year_sort_key(fy):
    """Normalised sort key for a fiscal-year label that may be stored as `str` or `int`.

    A block whose figures carry fiscal years both as `str` (the common case) and as `int` (the
    15-per-name BBG-sourced figures on CAT_US_Equity/CSL_AU_Equity/6861_JP_Equity) used to raise
    `TypeError: '<' not supported between instances of 'int' and 'str'` under plain `sorted()`.
    Returns `(0, int(str(fy)))` when `str(fy)` is exactly 4 digits, so every numeric year orders
    ascending regardless of its stored type; returns `(1, str(fy))` otherwise, so `"?"` and any
    future non-numeric label sort AFTER every numeric year, deterministically.
    """
    s = str(fy)
    if len(s) == 4 and s.isdigit():
        return (0, int(s))
    return (1, s)


def _group_by_fiscal_year(figures):
    """Group non-header figures by fiscal year, keyed by `str(fiscal_year)` so a year stored once
    as `"2026"` and once as `2026` can never produce two headings. This is the ONE grouping path
    `build_pack` uses."""
    by_fy = {}
    for f in figures:
        by_fy.setdefault(str(f.get("fiscal_year", "?")), []).append(f)
    return by_fy


# ---------------------------------------------------------------------------
# FWD-5 (AMGT_RESAPP round 72, AMGT-av-2): THE PRINTED PACK READS IN PLAIN WORDS. A line of the PDF
# names its figure by a plain label, never by the vendor's UPPER_UNDERSCORE field code. THE
# LABELS' SOURCE, in order: the Model tab's own sheet-row labels (`SHEET_ROWS`, transcribed from
# `modelSheet.ts`); the ONE served map of line names (`model_words.LINE_NAMES`, equal entry for
# entry to `modelSheet.ts` `LINE_NAMES`); the identity header's tile labels (`constants.ts`
# `STAT_TILE_DEFS`) and the four header facts (`modelSheet.ts` `V3_HEADER_LABELS`); the plain-words
# map below for the header lines the page names nowhere; then the figure's own served definition
# with every field code removed (`model_words.formula_words`); then a fixed phrase.
_HEADER_PLAIN_LABELS = {
    # constants.ts STAT_TILE_DEFS (the seven tiles)
    "PX_LAST": "Share price (last close)",
    "CUR_MKT_CAP": "Market cap",
    "CURR_ENTP_VAL": "Enterprise value",
    "NET_DEBT": "Net debt",
    "EQY_BETA": "Beta",
    "SI_PERCENT_EQUITY_FLOAT": "Short interest",
    "VOLUME_AVG_30D": "Average volume (30 trading days)",
    # modelSheet.ts V3_HEADER_LABELS
    "SHORT_NAME": "Company short name",
    "COUNTRY_FULL_NAME": "Country",
    "AVG_DAILY_VALUE_TRADED_3M": "Average daily value traded (three months)",
    "CRNCY_ADJ_MKT_CAP": "Market capitalisation",
    # the identity line (constants.ts IDENTITY_*_MNEMONIC) and the header lines the page names nowhere
    "GICS_SECTOR_NAME": "Sector",
    "CNTRY_OF_DOMICILE": "Country of domicile",
    "CRNCY": "Currency",
    "NAME": "Company name",
    "EQY_SH_OUT_REAL": "Shares outstanding",
    "EQY_FREE_FLOAT_PCT": "Free float",
    "SHORT_INT_RATIO": "Short interest ratio (days to cover)",
    "CIE_DES": "Company description",
    "CIE_DES_BULK": "Company description (full text)",
    "EQY_FUND_CRNCY": "Reporting currency",
    "LONG_COMP_NAME": "Company name (full legal)",
    "EXPECTED_REPORT_DT": "Next expected earnings report date",
    "ERN_ANN_DT_AND_PER": "Earnings announcement dates and the period each covers",
}

def _plain_label(fig) -> str:
    """The figure's name in plain words (the order stated above); never a field code."""
    if fig.get("_print_label"):
        return fig["_print_label"]
    mnemonic = fig.get("mnemonic") or "?"
    sheet_labels = {m: lbl for lbl, m, _forecast in SHEET_ROWS}  # defined below this function; read at call time
    label = sheet_labels.get(mnemonic) or model_words.LINE_NAMES.get(mnemonic) or _HEADER_PLAIN_LABELS.get(mnemonic)
    if label:
        return label
    definition = (fig.get("basis") or {}).get("definition")
    if isinstance(definition, str) and definition.strip():
        # a served forecast says what it estimates: "Consensus estimate of <what>"
        estimate = re.search(r"estimate of (.+?) for the overridden fiscal period", definition)
        if estimate:
            what = model_words.formula_words(estimate.group(1)).strip()
            if what:
                return "Consensus estimate of " + what
        words = model_words.formula_words(definition)
        # the label is the definition's first clause, never a paragraph
        for cut in (". ", "; "):
            if cut in words:
                words = words.split(cut, 1)[0]
        if len(words) > 70 and " (" in words:
            words = words.split(" (", 1)[0]
        words = words.strip().rstrip(".,;: ")
        if words:
            return words[0].upper() + words[1:]
    return model_words.UNNAMED_LINE


NOT_REPORTED = "not reported"


def _currency_of(figures, *mnemonics) -> str:
    """The currency code the block itself carries for the first of `mnemonics` it has (CRNCY = the
    trading currency, EQY_FUND_CRNCY = the reporting currency); "" when the block carries none."""
    for mnemonic in mnemonics:
        for f in figures or []:
            if f.get("mnemonic") == mnemonic and isinstance(f.get("value"), str) and f["value"].strip():
                return f["value"].strip()
    return ""


# AMGT-bw-1 (AMGT_RESAPP round 116, FWD-5 NOT MET, finding C-S186): THE CURRENCY OF A MONEY FIGURE IS THE FIGURE'S OWN.
# The page reads each figure's own served `currency`, trimmed (`priceCurrency.ts` currencyCodeOf; `HeaderCards.tsx`
# resolveFigure), and a money amount that carries none is said in the page's own words (`StatTile.tsx` moneyNoCode:
# "<amount> currency not stated"). This module never borrows a code from another field: trading_cur and reporting_cur
# (CRNCY, EQY_FUND_CRNCY) are read for no money label.
NO_CURRENCY_WORDS = "currency not stated"


def _own_currency(fig) -> str:
    """The currency code the figure ITSELF carries (its served `currency`, trimmed); "" when it carries none. The ONE
    reader of a money figure's currency: every money label in this module goes through it (AMGT-bw-1)."""
    code = fig.get("currency")
    return code.strip() if isinstance(code, str) and code.strip() else ""


def _money(amount_text: str, currency: str, tail: str = "") -> str:
    """`<code> <amount><tail>` when the figure carries its own code; `<amount><tail> currency not stated` when it does not
    (AMGT-bw-1: never a code borrowed from another field, never the words 'local currency')."""
    if not currency:
        return "{0}{1} {2}".format(amount_text, tail, NO_CURRENCY_WORDS)
    return "{0} {1}{2}".format(currency, amount_text, tail)


def _trim(v: float) -> str:
    """A number of no stated unit: thousands separators, at most four decimals, no trailing zeros."""
    text = "{0:,.4f}".format(v).rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def _format_figure_value(fig, trading_currency: str = "", reporting_currency: str = "") -> str:
    """THE VALUE OF ONE FIGURE AS A READER SAYS IT (AMGT-aw-2, FWD-5, CTO ruling 2). The figure's value is
    never changed, only its rounding and wording. THE PER-UNIT RULE, by the served unit text; `currency` is the
    FIGURE'S OWN served code (AMGT-bw-1), and a money amount whose figure carries none reads "currency not stated":
      MILLIONS                       currency + 1 decimal + "million"     "USD 184,627.0 million"
      MILLIONS (share count)         1 decimal + "million shares"         "643.8 million shares"
      PERCENT                        1 decimal + "%"                      "12.4%"
      RATIO (dimensionless multiple) 2 decimals + "x"                     "1.53x"
      PER SHARE ... / PRICE ...      currency + 2 decimals + "per share"  "USD 7.92 per share"
      ABSOLUTE (full currency units) currency + millions to 1 decimal     "USD 152,984.0 million"
      ABSOLUTE (share count)         whole number + "shares"              "7,458,799 shares"
      TEXT / DATE                    the value only
      a unit not measured            separators, at most 4 decimals (the caller adds "[unit not stated]")
    A missing value reads "not reported"; a yes/no reads "yes"/"no"; a list of earnings dates reads as
    its latest entry and its count -- never None, True, False, [] or a dict. The two currency arguments are
    accepted for the call shape and are NOT read for any money label (AMGT-bw-1)."""
    value = fig.get("value")
    if value is None or value == [] or value == {} or value == "":
        return NOT_REPORTED
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        dated = [r for r in value if isinstance(r, dict) and r.get("announcement_date")]
        if dated:
            latest = max(dated, key=lambda r: str(r["announcement_date"]))
            period = " ({0})".format(_long_days(latest["period"])) if latest.get("period") else ""
            return "latest {0}{1}; {2} dates on record".format(_long_days(latest["announcement_date"]), period, len(dated))
        return "{0} entries".format(len(value))
    if isinstance(value, dict):
        return "not shown"
    if isinstance(value, str):
        return _long_days(value)
    if not isinstance(value, (int, float)):
        return str(value)
    unit = str(fig.get("unit") or "")
    if unit.startswith(NOT_MEASURED_PREFIXES):
        return _trim(float(value))
    v = float(value)
    code = _own_currency(fig)  # AMGT-bw-1: the money code is the figure's own, never the block's CRNCY or EQY_FUND_CRNCY
    if unit.startswith("MILLIONS (share count)"):
        return "{0:,.1f} million shares".format(v)
    if unit.startswith("MILLIONS"):
        return _money("{0:,.1f}".format(v), code, " million")
    if unit.startswith("PERCENT"):
        return "{0:.1f}%".format(v)
    if unit.startswith("RATIO"):
        return "{0:.2f}x".format(v)
    if unit.startswith("PRICE"):
        return _money("{0:,.2f}".format(v), code, " per share")
    if unit.startswith("PER SHARE"):
        return _money("{0:,.2f}".format(v), code, " per share")
    if unit.startswith("ABSOLUTE (full currency units)"):
        return _money("{0:,.1f}".format(v / 1e6), code, " million")
    if unit.startswith("ABSOLUTE (share count)"):
        return "{0:,.0f} shares".format(v)
    return _trim(v)


_OWN_DATE_KEYS = ("quote_date", "price_date", "as_of_date", "as_of")  # a date the figure itself carries
_NO_DATE_TEXT = "date not stored with this figure"


def _figure_date_text(fig) -> str:
    """The period or date the figure ITSELF carries, in plain words (AMGT-ay-1, FWD-5, CTO ruling 1).

    A fiscal-year figure sits under its "Fiscal year YYYY" heading and says nothing more, unless it carries its
    own `period_end_date` (a forecast: "period ending <date>"). A header figure reads its quote date from the
    stored figure when the figure carries one; a numeric header figure with none says so in plain words; a text
    header figure (a name, a country) has no date to give. The landing stamp `vintage` is not any of these."""
    if fig.get("scope") != "header":
        end = str(fig.get("period_end_date") or "").split("T", 1)[0]
        return "period ending " + _long_days(end) if end else ""
    for key in _OWN_DATE_KEYS:
        own = str(fig.get(key) or "").split("T", 1)[0]
        if own:
            return "as of " + _long_days(own)
    value = fig.get("value")
    numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
    return _NO_DATE_TEXT if numeric else ""


def _plain_figure_line(fig, trading_currency: str = "", reporting_currency: str = "") -> str:
    """One printed line for one figure: `<plain label>: <value in words> . as of <date> . <source>`.
    The value, any withheld-value marker and the source are the figure's OWN, read through
    `render_figure_line` (so a figure withheld there is withheld here); only the value is re-worded
    (`_format_figure_value`: the unit said in words, never the unit code), the field-code segment is
    replaced by the label, the unit-not-measured marker is said in plain words, the vintage is cut to
    its date and the source's internal names are dropped."""
    basis = fig.get("basis") or {}
    code_part = "{0} ({1})".format(basis.get("mnemonic", fig.get("mnemonic", "?")), basis.get("definition", "?"))
    parts = render_figure_line(fig).split(" " + chr(0xB7) + " ")
    parts = [p for p in parts if p != code_part and not p.startswith("derivation ")]
    head = parts[0]
    unit = fig.get("unit", "") or ""
    unit_not_measured = (not unit) or unit.startswith(NOT_MEASURED_PREFIXES)
    unit_text = UNRESOLVED_MARKER if unit_not_measured else unit
    if head.endswith(" " + unit_text):
        head = head[: -len(" " + unit_text)]
    raw = str(fig.get("value", "?"))
    shown = _format_figure_value(fig, trading_currency, reporting_currency)
    if raw and raw in head:
        head = head.replace(raw, shown, 1)
        if (unit_not_measured and shown not in (NOT_REPORTED, "not shown")
                and not isinstance(fig.get("value"), (str, list, dict))):
            head += " [unit not stated]"
    head = head.replace(UNRESOLVED_MARKER, "[unit not stated]")
    rest = []
    for p in parts[1:]:
        if p.startswith("as of "):
            # AMGT-ay-1 (FWD-5, CTO ruling 1): the stored `vintage` is the day the block was LANDED, never the
            # figure's own period or quote date, so it is never printed as an "as of". Each figure says its own.
            p = _figure_date_text(fig)
            if not p:
                continue
        elif p == "BBG":
            p = "Bloomberg"
        else:
            p = p.replace("bloomberg-dapi", "Bloomberg").replace(", model_block_fye", "").replace("model_block_fye", "model")
            # AMGT-bu-3: the 'observed <observation_date>' segment is a date a reader sees -- the long form.
            p = _long_days(p)
        rest.append(p)
    return "{0}: {1}".format(_plain_label(fig), head) + "".join(" - " + p for p in rest)


_NO_DATE_NOTE = "Figures marked without a date: " + _NO_DATE_TEXT + "."


# AMGT-bx-2 (AMGT_RESAPP round 117, the CTO's round-116 item 3): THE PACK'S CURRENCY RULE IS THE PAGE'S RULE. A header money
# figure whose served `currency_basis` begins UNMEASURED is WITHHELD: no amount and no code; its line carries the page's words
# (`StatTile.tsx` CURRENCY_UNCONFIRMED_WORDS and isUnmeasuredBasis; `HeaderCards.tsx` withheldReason). A measured figure keeps
# the own-code rule of `_money`. Header lines only: the Fiscal year lines do not read this rule.
CURRENCY_UNCONFIRMED_WORDS = "Bloomberg does not confirm this figure's currency"
_MONEY_UNIT_PREFIXES = ("PRICE", "PER SHARE", "MILLIONS", "ABSOLUTE (full currency units)")


def _is_money_unit(fig) -> bool:
    """A unit that carries a money amount (the page's isMoneyFormat): a price, a per-share amount, a MILLIONS amount that is not
    a share count, or an ABSOLUTE amount in full currency units."""
    unit = str(fig.get("unit") or "")
    if unit.startswith("MILLIONS (share count)"):
        return False
    return unit.startswith(_MONEY_UNIT_PREFIXES)


def _currency_unmeasured(fig) -> bool:
    """The page's isUnmeasuredBasis, read as figureBasis reads it: the served `currency_basis` begins UNMEASURED. A string
    `basis` is the older alias; a dict `basis` is the figure's definition and is never read here."""
    for key in ("currency_basis", "basis"):
        basis = fig.get(key)
        if isinstance(basis, str) and basis.strip():
            return bool(re.match(r"\s*UNMEASURED\b", basis))
    return False


def _withheld(fig) -> bool:
    """AMGT-bx-2: the page shows no amount and no code for a header money figure that has a value and an UNMEASURED basis
    (HeaderCards withheldReason). The basis alone decides, whether or not the figure carries its own code."""
    return _has_value(fig) and _is_money_unit(fig) and _currency_unmeasured(fig)


def _source_words(fig) -> str:
    """The figure's source in words, as the page's tooltip says it (HeaderCards sourceWords): Bloomberg's own id is never printed."""
    source = str(fig.get("source") or "").strip()
    if not source:
        return "source not stated"
    if source == "BBG" or re.match(r"(?i)bloomberg", source):
        return "Bloomberg"
    return source


def _withheld_line(fig) -> str:
    """`<plain label>: <the page's words> - <source>`: a withheld figure's amount and code are not printed (AMGT-bx-2)."""
    return "{0}: {1} - {2}".format(_plain_label(fig), CURRENCY_UNCONFIRMED_WORDS, _source_words(fig))


def _header_print_lines(header_figs, trading_currency: str = "", reporting_currency: str = "") -> list:
    """The Header block's printed lines: each figure's line as `_plain_figure_line` makes it, minus the
    " - date not stored with this figure" segment, plus ONE closing line saying it once, only when at least
    one printed header figure is numeric with no date of its own. AMGT-bx-2: a WITHHELD money figure (`_withheld`) prints the
    page's words in place of its amount and code, and does not count toward the closing line."""
    figs = _header_figures_for_print(header_figs, trading_currency, reporting_currency)
    lines = [
        _withheld_line(f) if _withheld(f)
        else _plain_figure_line(f, trading_currency, reporting_currency).replace(" - " + _NO_DATE_TEXT, "")
        for f in figs
    ]
    if any(_figure_date_text(f) == _NO_DATE_TEXT for f in figs if not _withheld(f)):
        lines.append(_NO_DATE_NOTE)
    return lines


_DESCRIPTION_MNEMONICS = ("CIE_DES_BULK", "CIE_DES")  # the full text first, the short form when there is none
_MARKET_CAP_ALIAS = "CRNCY_ADJ_MKT_CAP"  # the same current market cap as CUR_MKT_CAP, named a second time


def _has_value(fig) -> bool:
    value = fig.get("value")
    return not (value is None or value == [] or value == {} or (isinstance(value, str) and not value.strip()))


def _description_figure(header_figs):
    """The ONE company description the print carries: the full text when the block has it, else the short form;
    None when the block carries neither."""
    for mnemonic in _DESCRIPTION_MNEMONICS:
        for f in header_figs:
            if f.get("mnemonic") == mnemonic and _has_value(f):
                return f
    return None


def _description_line(fig, trading_currency: str = "", reporting_currency: str = "") -> str:
    """The description figure's own line without its label (the section heading carries the label)."""
    line = _plain_figure_line(fig, trading_currency, reporting_currency)
    prefix = _plain_label(fig) + ": "
    return line[len(prefix):] if line.startswith(prefix) else line


_CONVERTED_LABEL = "Market value, currency-adjusted (converted, rate not carried)"  # AMGT-bw-1: the pack carries no rate


def _converted(alias, primary) -> bool:
    """AMGT-bw-1: a conversion is NAMED only when it is shown -- the alias and the market cap each carry their own code and
    the two codes differ. A second line in the market cap's own code is not converted and keeps its plain name."""
    a, p = _own_currency(alias), _own_currency(primary)
    return bool(a and p and a != p)


def _header_figures_for_print(header_figs, trading_currency: str = "", reporting_currency: str = "") -> list:
    """The header figures, each current fact ONCE (AMGT-ax-4, FWD-5): the company description leaves the header
    (it prints once, under its own heading), and the second name for the current market cap is dropped when its
    printed value is the first's. A second line whose printed value differs stays under its own plain name, and is
    labelled "currency-adjusted" only when a conversion happened (AMGT-bw-1, `_converted`)."""
    primary = next((f for f in header_figs if f.get("mnemonic") == "CUR_MKT_CAP" and _has_value(f)), None)
    out = []
    for f in header_figs:
        mnemonic = f.get("mnemonic")
        if mnemonic in _DESCRIPTION_MNEMONICS:
            continue
        if mnemonic == _MARKET_CAP_ALIAS and primary is not None:
            if (_format_figure_value(f, trading_currency, reporting_currency)
                    == _format_figure_value(primary, trading_currency, reporting_currency)):
                continue
            if _converted(f, primary):
                f = dict(f, _print_label=_CONVERTED_LABEL)
        out.append(f)
    return out


def _drafted_for_print(security_key_value: str, thesis_bundle=None) -> dict:
    """The drafted half the print reads (AMGT-ay-1, FWD-5, CTO ruling 2): the caller's own bundle when it
    carries `drafted_sections`, else ONE call to `scoped_amgt.read_drafted_sections`, the function /thesis serves
    the same sections from. A read that raises is carried as `error`, never as "not written"."""
    if isinstance(thesis_bundle, dict) and "drafted_sections" in thesis_bundle:
        return thesis_bundle
    try:
        from lib.research.api import scoped_amgt  # lazy: the api package imports this one

        return scoped_amgt.read_drafted_sections(security_key_value)
    except Exception as err:  # noqa: BLE001 -- the print still renders; the section says the read failed
        return {"drafted_sections": [], "error": "{0}: {1}".format(type(err).__name__, err)}


def _served_section(drafted, section_id: str):
    return next((s for s in (drafted or {}).get("drafted_sections") or [] if s.get("section_id") == section_id), None)


def _served_sentences(drafted, section_id: str) -> list:
    return [str(x.get("text")) for x in ((_served_section(drafted, section_id) or {}).get("sentences") or [])
            if str(x.get("text") or "").strip()]


def _served_sentence_items(drafted, section_id: str) -> list:
    """AMGT-bv-2: the served sentence OBJECTS of the section that carry text (`_served_sentences`' own filter), so a
    caller can tell a source quotation (`_is_source_quotation`) from the system's prose."""
    return [x for x in ((_served_section(drafted, section_id) or {}).get("sentences") or [])
            if str(x.get("text") or "").strip()]


def _print_drafted(p, drafted, section_id: str, not_written: str):
    """Each served sentence of the section, one paragraph each; the plain "not written" line only where the
    drafted read serves no sentence for it. AMGT-bv-2: a sentence that IS the filing's own text prints verbatim."""
    sentences = _served_sentence_items(drafted, section_id)
    if sentences:
        for sentence in sentences:
            p.line(str(sentence.get("text")), verbatim=_is_source_quotation(sentence))
            p.blank()
    elif (drafted or {}).get("error"):
        p.line("The drafted text could not be read when this print was made.")
    else:
        p.line(not_written)


# ---------------------------------------------------------------------------
# AMGT-bw-2 (AMGT_RESAPP round 116, FWD-5): the printed pack reads as a NOTE. The narrative sections print first,
# each under its own heading; the model figures follow in an appendix. Each section prints the page's own served
# content, or one plain sentence saying why nothing is on file (never a bare heading).
# ---------------------------------------------------------------------------
APPENDIX_HEADING = "Appendix: model figures"
APPENDIX_SENTENCE = "The model figures follow, grouped by section: the header, then each fiscal year."
NO_PEERS_SENTENCE = "No peer set is on file for this company yet."
POSTURE_DISCLAIMER = "A machine's view for a person to accept or reject, never an instruction."
WHAT_CHANGED_SENTENCE = (
    "What changed between stored model versions is not printed here: this pack is built from one model block, "
    "and the comparison of two stored versions is not an input to it."
)


# AMGT-bx-1 (AMGT_RESAPP round 117, CTO analysis items 1 and 2): the Summary reads the SERVED recommendation -- the /thesis
# body's `dossier_fields.last_stated_position`, which the page's Posture tab shows -- with its citation. A state sentence
# the pack prints says why in plain words: never a storage path, a key, an object name, an order or cell id, a vendor
# error text or an UPPER_SNAKE field code (the reasons travel in the served object; the print does not carry them).
POSITIONING_ABSENT_SENTENCE = "No positioning view is on file for this name."
POSITIONING_NO_CALL_SENTENCE = "No positioning call was made for this name."

# AMGT-by-1 (AMGT_RESAPP round 118, the CTO's round-117 analysis item 1; rows AMGT_RESAPP-D1-W512-S2 and -S3): EVERY
# SERVED REASON THE PDF PRINTS GOES THROUGH ONE PLAIN-SENTENCE MAPPER. A served reason prints only when it is plain words;
# any other reason prints the site's own fixed sentence, never the raw text. The rule is a TOKEN rule, not a substring
# rule: the word `bronze` in prose is a word (it has no slash beside it), a path segment is not; an underscore inside a
# word is a field code and is not plain.
_PLAIN_MAX_CHARS = 300
_NOT_PLAIN_PATTERNS = (
    re.compile(r"s3://", re.IGNORECASE),                                  # a storage address
    re.compile(r"\.(?:json|docx|xlsx|pdf|csv|txt)\b", re.IGNORECASE),     # an object or file name
    re.compile(r"\bAMGT-", re.IGNORECASE),                                # a cell id
    re.compile(r"\b[A-Za-z]+\d*-[A-Za-z]+\d*-\d+\b"),                     # an order id: AMGT-rj-11
    re.compile(r"\b[A-Za-z]+\d*-[A-Za-z]+\d+\b"),                         # a row id: D1-S54
    re.compile(r"\w_\w"),                                                 # an underscore inside a word (UPPER_SNAKE too)
    re.compile(r"\b(?:NoSuchKey|ClientError|Traceback|botocore|NOT_SERVED|READ_FAILED)\b"),
    re.compile(r"\b[A-Z][A-Za-z]*(?:Error|Exception)\b"),                  # a Python or vendor error name
    re.compile(r":\s*[a-z0-9]+(?:-[a-z0-9]+){2,}\b"),                     # a colon, then a bucket-looking token
    re.compile(r"\w\\\w"),                                                # a backslash path
)


def _path_token(token: str) -> bool:
    """One whitespace-delimited token that is a path or a key: a `/` between two word characters AND either a second `/`,
    a file extension at its end, or a bronze/gold SEGMENT beside a slash. A bronze or gold word with no slash is prose."""
    if "/" not in token or re.search(r"\w/\w", token) is None:
        return False
    core = token.rstrip(".,;:)\"'")
    if core.count("/") >= 2 or re.search(r"\.[A-Za-z]{2,5}$", core):
        return True
    return re.search(r"(?:^|/)(?:bronze|gold)(?:/|$)", core, re.IGNORECASE) is not None


def _plain_reason(reason, fixed):
    """AMGT-by-1: the served `reason` when it is PLAIN WORDS, else `fixed` -- the calling site's own plain sentence. Not plain:
    not a string, empty, longer than 300 characters, or matching any `_NOT_PLAIN_PATTERNS` entry or any `_path_token`. A plain
    reason is returned exactly as served (never trimmed, never reworded). `fixed` is returned for every other value."""
    if not isinstance(reason, str) or not reason.strip() or len(reason) > _PLAIN_MAX_CHARS:
        return fixed
    if any(pattern.search(reason) for pattern in _NOT_PLAIN_PATTERNS):
        return fixed
    if any(_path_token(token) for token in reason.split()):
        return fixed
    return reason


UNKNOWN_VERDICT_SENTENCE = "The verdict on file is not one of better, worse, hold or steer_clear: no call is shown."


def _served_position_block(bundle):
    """The served `last_stated_position` block of the /thesis body when it is SERVED with a text, else None."""
    block = ((bundle or {}).get("dossier_fields") or {}).get("last_stated_position")
    if not isinstance(block, dict) or block.get("status") != "SERVED":
        return None
    value = block.get("value")
    if not isinstance(value, dict) or not str(value.get("text") or "").strip():
        return None
    return block


def _report_title(citation: dict) -> str:
    """The research report's title: its file name without the folder and without the extension. Never the key."""
    name = str(citation.get("report_key") or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    stem, dot, _ext = name.rpartition(".")
    return stem if dot and stem else name


def _citation_line(citation: dict) -> str:
    """`Source: research report "<title>", passage <locator>.` -- what the citation carries, nothing invented."""
    title = _report_title(citation)
    head = 'Source: research report "{0}"'.format(title) if title else "Source: research report"
    locator = citation.get("locator")
    if locator is not None and str(locator).strip() != "":
        head += ", passage {0}".format(locator)
    return head + "."


def _served_position_lines(bundle) -> list:
    """The served recommendation line, then (not for a line-only position) its fund and weight in words, then ONE
    citation line when the citation is carried. Empty when no position is served."""
    block = _served_position_block(bundle)
    if block is None:
        return []
    value = block.get("value") or {}
    lines = [str(value.get("text")).strip()]
    if not value.get("line_only"):
        fund = str(value.get("fund") or "").strip()
        size = value.get("size_pct")
        if fund and size not in (None, ""):
            lines.append("Fund {0}, weight {1} per cent of the fund.".format(fund, size))
        elif fund:
            lines.append("Fund {0}.".format(fund))
    citation = block.get("citation")
    if isinstance(citation, dict) and citation:
        lines.append(_citation_line(citation))
    return lines


def _print_summary(p, drafted, bundle) -> None:
    """Summary (AMGT-bx-1, AMENDMENT 1), in this order: (1) the served recommendation block -- its text, the fund and
    weight, and the one citation line -- so a reader meets the recommendation first; (2) the drafted recommendation
    sentences, each as drafted; (3) the drafted thesis sentences, or "No investment thesis has been written for this
    company yet." when there are none; (4) the sentence "No recommendation has been written for this company yet."
    ONLY when neither the drafted recommendation nor the served position is present, and then it leads. A drafted read
    that raised is said so, never printed as absent."""
    rec_items = _served_sentence_items(drafted, "recommendation")
    rec_error = (drafted or {}).get("error")
    position = _served_position_lines(bundle)
    if not rec_items and not rec_error and not position:
        p.line(NOT_WRITTEN["recommendation"])
        p.blank()
    for line in position:
        p.line(line)
    if position:
        p.blank()
    if rec_items or rec_error:
        _print_drafted(p, drafted, "recommendation", "")
        p.blank()
    _print_drafted(p, drafted, "investment_thesis", NOT_WRITTEN["thesis"])
    p.blank()


def _dossier_management_passage(bundle: dict):
    """The research team's management passage the Exec Management tab draws (`dossier_fields.management`), or None
    when it is not served as text."""
    block = (bundle.get("dossier_fields") or {}).get("management") or {}
    value = block.get("value")
    if block.get("status") == "SERVED" and isinstance(value, str) and value.strip():
        return value
    return None


def _officer_line(officer: dict) -> str:
    name = str(officer.get("name") or "?")
    role = officer.get("role")
    text = "{0}: {1}".format(name, role) if role else name
    tenure = officer.get("tenure_years")
    if tenure is not None:
        text += " -- tenure {0:.2f} years".format(float(tenure))
    return text


def _ceo_profile_sentence(management: dict) -> str:
    profile = management.get("ceo_public_profile") or {}
    reading = management.get("ceo_profile_reading") or {}
    who = " ({0})".format(profile["ceo_name"]) if profile.get("ceo_name") else ""
    if reading.get("reading") == "CONFIRMED" and profile.get("url"):
        return "CEO public profile{0}: {1}".format(who, profile["url"])
    # AMGT-by-1 (row AMGT_RESAPP-D1-W512-S3): the reading's reason is printed only when it is plain words
    reason = _plain_reason(reading.get("reason"), "no public profile is on file yet")
    return "CEO public profile{0}: {1}".format(who, reason if reason.endswith((".", "!", "?")) else reason + ".")


# ---------------------------------------------------------------------------
# AMGT-bx-3 (AMGT_RESAPP round 117, CTO ruling, round-116 analysis item 4): a machine-written passage prints where the
# page shows it, only when it is CLEARED, and each printed passage carries its label on the next line. The page's own
# words are in portal/src/pages/SecurityAnalysis/components/AiFillBlock.tsx (sourceWords, the two captions).
# ---------------------------------------------------------------------------
_PAGE_SOURCE_WORDS = {"WEB_SEARCH": "From a web search", "OPAL_SOURCE": "From Opal sources"}
_PAGE_CAPTION = {
    "mgmt_team_view": "Machine-written summary, not the research team's view.",
    "thesis_pillars": "Machine-written, not the research team's pillars.",
}


def _cleared_passage(thesis_bundle, block_id: str):
    """The served text of one machine-written block when the page may show it: the fill is SERVED, the block carries
    non-empty text from a served source class, and its validation is CLEARED with verdict PASS and a dated check. Any
    other state, an absent validation or a null text returns None: nothing prints, no label, no placeholder."""
    fill = (thesis_bundle or {}).get("ai_fill")
    if not isinstance(fill, dict) or fill.get("status") != "SERVED":
        return None
    block = (fill.get("blocks") or {}).get(block_id)
    if not isinstance(block, dict) or block.get("source_class") not in _PAGE_SOURCE_WORDS:
        return None
    text = block.get("text")
    if not isinstance(text, str) or not text.strip():
        return None
    validation = block.get("validation")
    if not isinstance(validation, dict) or validation.get("state") != "CLEARED" or validation.get("verdict") != "PASS":
        return None
    checked = validation.get("checked_at")
    if not isinstance(checked, str) or re.match(r"\d{4}-\d{2}-\d{2}", checked) is None:
        return None  # the label carries the check's day; a check with no day cannot be labelled, so nothing prints
    return {"text": text.strip(), "source_class": block["source_class"], "day": long_day(checked),
            "citations": block.get("citations") or []}


def _citation_words(citation) -> str:
    """One citation as the page words it (AiFillBlock.citationParts) and as the pack prints it: a web citation reads its
    title and the host of its url, never the url's path; an Opal citation reads its plain-words ref."""
    from urllib.parse import urlsplit  # local: the one part of a url the pack prints is its host

    if not isinstance(citation, dict):
        return ""
    url = str(citation.get("url") or "").strip()
    host = (urlsplit(url).hostname or "") if re.match(r"https?://", url, re.IGNORECASE) else ""
    if citation.get("source_kind") == "web":
        title = str(citation.get("title") or "").strip()
        if title and host:
            return "{0} ({1})".format(title, host)
        return title or host or "web source"
    # AMGT-by-1: an Opal citation's ref is printed only when it is plain words (an empty ref reads "Opal source" as before)
    return _plain_reason(str(citation.get("ref") or "").strip(), "Opal source")


def _machine_label(passage, caption=None) -> str:
    """The label line under a printed passage, one line: `machine-drafted, cleared <long day>`, the source words the page
    uses, and the page's caption where the page has one."""
    parts = ["machine-drafted, cleared " + passage["day"], _PAGE_SOURCE_WORDS[passage["source_class"]]]
    if caption:
        parts.append(caption)
    return " | ".join(parts)


def _print_passage(p, passage, caption=None) -> None:
    """A cleared passage: its served text, the label on the next line, then one line per citation. The caller adds the blank."""
    p.line(passage["text"])
    p.line(_machine_label(passage, caption))
    for citation in passage["citations"]:
        words = _citation_words(citation)
        if words:
            p.line(words)


def _dossier_failed(dossier: dict) -> bool:
    """The page's `failed` read (ExecManagementTab, ThesisTab): a dossier whose status is set and is not ABSENT."""
    status = dossier.get("status")
    return bool(status) and status != "ABSENT"


def _team_view_gap_open(bundle: dict) -> bool:
    """mgmt_team_view is a GAP fill on the page: drawn only when no served management passage stands and the read did not fail."""
    dossier = bundle.get("dossier_fields") or {}
    return _dossier_management_passage(bundle) is None and not _dossier_failed(dossier)


def _pillars_gap_open(bundle: dict) -> bool:
    """thesis_pillars is a GAP fill on the page: drawn only when the served pillar list is empty and the read did not fail."""
    dossier = bundle.get("dossier_fields") or {}
    return not (dossier.get("thesis_pillars") or []) and not _dossier_failed(dossier)


def _print_thesis_pillars(p, bundle: dict) -> None:
    """AMGT-bx-3: the `Thesis pillars` section, present only when its cleared passage prints (the page's gap fill)."""
    if not _pillars_gap_open(bundle):
        return
    passage = _cleared_passage(bundle, "thesis_pillars")
    if passage is None:
        return
    p.heading("Thesis pillars")
    _print_passage(p, passage, _PAGE_CAPTION["thesis_pillars"])
    p.blank()


def _print_management(p, bundle: dict, drafted) -> None:
    """Management (AMGT-bw-2): the page's CEO passage (the drafted `ceo_bio` sentences, the Thesis tab's CEO bio), the
    research team's management passage (`dossier_fields.management`), the officer roster and the CEO profile line --
    the same served fields the Thesis and Exec Management tabs read. With none of them, one sentence says why.
    AMGT-bx-3 (amendment 1): the cleared machine-written passages print ABOVE the roster, where the page draws them
    (ExecManagementTab): mgmt_team_view (the gap fill), then mgmt_bio, then mgmt_recent, each labelled. The CEO profile
    line prints only when no management passage (team view, bio or recent) prints."""
    printed = False
    passage = _dossier_management_passage(bundle)
    if passage:
        p.line(passage)
        p.blank()
        printed = True
    for sentence in _served_sentence_items(drafted, "ceo_bio"):
        p.line(str(sentence.get("text")), verbatim=_is_source_quotation(sentence))
        p.blank()
        printed = True
    team_view = _cleared_passage(bundle, "mgmt_team_view") if _team_view_gap_open(bundle) else None
    passages = [(team_view, _PAGE_CAPTION["mgmt_team_view"])] if team_view is not None else []
    for block_id in ("mgmt_bio", "mgmt_recent"):
        cleared = _cleared_passage(bundle, block_id)
        if cleared is not None:
            passages.append((cleared, None))
    for cleared, caption in passages:
        _print_passage(p, cleared, caption)
        p.blank()
        printed = True
    management = bundle.get("management") or {}
    if management.get("management_status") == "SERVED":
        for officer in management.get("officers") or []:
            p.line(_officer_line(officer))
        p.blank()
        if not passages:
            p.line(_ceo_profile_sentence(management))
            p.blank()
        printed = True
    if not printed:
        # the page's existing plain sentence for an unwritten bio, reused as it stands (no rewording): it says why
        p.line(NOT_WRITTEN["bio"])
        p.blank()


def _comparable_label(posture: dict) -> str:
    identity = posture.get("comparable_identity") or {}
    if identity.get("status") == "RESOLVED" and identity.get("display_ticker"):
        return str(identity["display_ticker"])
    if posture.get("comparable_name"):
        return str(posture["comparable_name"])
    return "a comparable the research team has not identified"


def _verdict_sentence(verdict, subject: str, comparable: str) -> str:
    """The Posture tab's own verdict sentence (`postureVerdictSentence`), in the same four words."""
    if verdict == "better":
        return "{0} looks like a BETTER pick than {1}.".format(subject, comparable)
    if verdict == "worse":
        return "{0} looks like a WORSE pick than {1}.".format(subject, comparable)
    if verdict == "hold":
        return "HOLD -- neither {0} nor {1} looks clearly the better pick on this evidence.".format(subject, comparable)
    if verdict == "steer_clear":
        return "STEER CLEAR -- {0}'s own evidence argues against it, whatever {1} shows.".format(subject, comparable)
    # AMGT-by-1: an unknown verdict is named only when it is plain words; otherwise the fixed sentence says so
    shown = _plain_reason(verdict, None)
    if shown is None:
        return UNKNOWN_VERDICT_SENTENCE
    return "Verdict {0} is not one of better, worse, hold or steer_clear: no call is shown.".format(shown)


def _print_positioning(p, posture, subject: str) -> None:
    """Positioning (AMGT-bw-2): the posture verdict and every basis claim, as the Posture tab carries them."""
    if not posture:
        # AMGT-by-1 (row AMGT_RESAPP-D1-W512-S2): a None posture prints the SAME one sentence as an absent posture object
        p.line(POSITIONING_ABSENT_SENTENCE)
        p.blank()
        return
    status = posture.get("status")
    if status == "READ_FAILED":
        # AMGT-bx-1: the read's own reason is not printed (it may carry a storage path); the sentence says what is known
        p.line("Posture: the read did not complete -- not evidence that no posture exists.")
        p.blank()
        return
    if status != "SERVED":
        p.line(POSITIONING_ABSENT_SENTENCE)
        p.blank()
        return
    verdict = posture.get("verdict")
    if verdict == "absent":
        p.line(POSITIONING_NO_CALL_SENTENCE)
    else:
        p.line(_verdict_sentence(verdict, subject, _comparable_label(posture)))
    p.line(POSTURE_DISCLAIMER)
    p.blank()
    claims = [claim for claim in (posture.get("basis") or []) if str(claim.get("claim") or "").strip()]
    if not claims:
        p.line("The posture carries no basis claims.")
        p.blank()
    for claim in claims:
        p.line(str(claim.get("claim")))
        p.blank()


def _print_peers(p, peer_set) -> None:
    """Peers (AMGT-bw-2): the comparable set and the comparison columns the page's CSC table is built on, in words."""
    if not peer_set:
        p.line(NO_PEERS_SENTENCE)
        p.blank()
        return
    if peer_set.get("basis") == "absent":
        # AMGT-bx-1: the served reason is not printed (it may carry a storage path); the absence sentence says it
        p.line(NO_PEERS_SENTENCE)
        p.blank()
        return
    members = peer_set.get("members") or []
    if members:
        named = ["{0} ({1})".format(m.get("name", "?"), m.get("ticker", "?")) for m in members]
        p.line("The comparable set has {0} member(s): {1}.".format(len(members), "; ".join(named)))
    else:
        p.line("The comparable set has no members.")
    csc = peer_set.get("csc_columns") or {}
    declared = csc.get("columns_declared", len(csc.get("columns") or []))
    p.line("Comparison columns carried: {0} of {1} declared.".format(len(csc.get("present") or []), declared))
    p.blank()


def build_pack(
    security: str,
    model_block: dict,
    out_dir=None,
    thesis_bundle: dict = None,
    peer_set: dict = None,
    posture: dict = None,
    run_date: str = None,
    write_text: bool = True,
    write_rich: bool = True,
) -> tuple:
    """Render ONE pack and return `(pdf_path, txt_path)` -- UNCHANGED shape and UNCHANGED bytes
    for a caller passing only `(security, model_block[, out_dir])` (AC2's negative control).

    `thesis_bundle`/`peer_set`/`posture` are OPTIONAL and ADDITIVE (AMGT-rl-10, FWD-30 branch
    (b)): when ANY is supplied, this ALSO writes `build_rich_text`'s machine-readable document
    beside `txt_path`, at `pack_<sec_key>.md` in the same `out_dir` -- one more file, never a
    change to the PDF or the txt this function has always produced. Passing none of the three
    (the default) writes no `.md` at all, byte-identical to before this cell.

    `model_block` IS THE INPUT -- this function reads no store and opens no input file. The
    caller has already read the landed block and applied the corrected fiscal-price overlay
    (the adapter's `read_model_block` does both), so re-reading or re-overlaying here would be
    a second writer of one corrected value. A caller that hands over `None` gets a refusal
    rather than a silently empty pack.

    AMGT-bw-2 (round 116): the PDF reads as a note. The narrative sections (Summary, Risks and considerations, Company
    description, Management, Positioning, Peers, What changed) print first; the model figures follow under
    `Appendix: model figures`. `thesis_bundle` also feeds Management (the CEO passage, the officer roster) and `posture`
    and `peer_set` feed Positioning and Peers. `write_rich=False` skips the markdown write above.

    `write_text` (AMGT-ba-11, row Z-S218; default True, so every other caller keeps its bytes): False skips the
    pypdf re-read of the finished PDF and the `.txt` write (0.22-0.40 s). The PDF and the returned 2-tuple are the same;
    the `txt_path` returned then names a file this call did not write. The served print route passes False because it
    reads only the PDF.

    `out_dir` defaults to the interpreter's temporary directory: the only writable location in
    the deployed runtime, and never a path inside the repository.

    AMGT-ay-1 (FWD-5, CTO rulings 1 and 2): the PDF's RUN date (`run_date`, `YYYY-MM-DD`, default today UTC)
    is printed ONCE, on page 1; every figure line carries only its own period or date; and the drafted
    sections are read from `lib.research.api.scoped_amgt.read_drafted_sections`, the one function the
    /thesis route serves them from (`thesis_bundle["drafted_sections"]` when the caller already holds it).
    """
    if not isinstance(model_block, dict):
        raise ValueError(
            "build_pack needs the caller's already-read model block; got {0!r}".format(
                type(model_block).__name__
            )
        )
    plt, PdfPages = _plotting()

    sec_key = security_key(security)
    figures = model_block.get("figures", [])
    header_figs = [f for f in figures if f.get("scope") == "header"]
    fy_figs = [f for f in figures if f.get("scope") != "header"]
    by_fy = _group_by_fiscal_year(fy_figs)

    name_fig = next((f for f in header_figs if f.get("mnemonic") == "NAME"), None)
    company_name = name_fig["value"] if name_fig else security

    base = Path(out_dir) if out_dir else Path(tempfile.gettempdir())
    base.mkdir(parents=True, exist_ok=True)
    pdf_path = base / "pack_{0}.pdf".format(sec_key)
    txt_path = base / "pack_{0}.txt".format(sec_key)
    run_date = str(run_date or datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    drafted = _drafted_for_print(model_block.get("security_key") or sec_key, thesis_bundle)

    # AMGT-rl-10 (AC2's negative control): matplotlib's PdfPages stamps a `CreationDate` from
    # wall-clock time by default, so two renders of the SAME model_block were never
    # byte-identical even before this cell -- an unrelated, pre-existing non-determinism. Named
    # `metadata=None` removes the stamp (matplotlib's own documented way to do so) rather than
    # fabricating a fixed date; nothing rendered on the page changes.
    with plt.rc_context({"pdf.fonttype": 42}), PdfPages(str(pdf_path), metadata={"CreationDate": None}) as pdf:
        p = Paginator(pdf, plt)

        # The model figures' currency labels are computed here, once, for the figure lines in the appendix AND the
        # company description line (AMGT-bw-2 moved the appendix to the end; the computation itself is unchanged).
        trading_cur = _currency_of(header_figs, "CRNCY", "EQY_FUND_CRNCY")
        reporting_cur = _currency_of(header_figs, "EQY_FUND_CRNCY", "CRNCY")

        # ---- PAGE 1: the title, the run day, and the page's thesis under Summary (AMGT-bw-2, FWD-5) ----
        p.title("{0} [{1}] Research Note".format(company_name, security))
        p.line("Printed {0}".format(_long_days(run_date)))
        p.blank()
        p.heading("Summary")
        _print_summary(p, drafted, thesis_bundle)
        p.blank()
        _print_thesis_pillars(p, thesis_bundle or {})  # AMGT-bx-3: the cleared pillars passage, as its own section when it prints

        # ---- THE NARRATIVE, in the page's order: risks, company description, management, positioning, peers ----
        p.heading("Risks and considerations")
        _print_drafted(p, drafted, "risks", NOT_WRITTEN["risks"])
        p.blank()
        p.heading("Company description")
        desc_fig = _description_figure(header_figs)
        desc_sentences = _served_sentences(drafted, "company_description")
        # AMGT-bx-3: the page's identity fill draws only when the served company-description line is empty
        identity = _cleared_passage(thesis_bundle, "identity_description") if desc_fig is None else None
        if desc_fig is None and not desc_sentences and identity is None:
            p.line(NOT_WRITTEN["company_description"])
        if desc_fig is not None:
            p.line(_description_line(desc_fig, trading_cur, reporting_cur))
        if desc_sentences:
            if (_served_section(drafted, "company_description") or {}).get("description_verdict_state") != "PASSED":
                # the SAME fallback /thesis serves: the filed sentences under an honest heading
                p.line("Filed detail (does not describe the business):")
            for sentence in _served_sentence_items(drafted, "company_description"):
                p.line(str(sentence.get("text")), verbatim=_is_source_quotation(sentence))
                p.blank()
        if identity is not None:
            _print_passage(p, identity)
            p.blank()
        p.blank()
        p.heading("Management")
        _print_management(p, thesis_bundle or {}, drafted)
        p.heading("Positioning")
        _print_positioning(p, posture, company_name)
        p.blank()
        p.heading("Peers")
        _print_peers(p, peer_set)
        p.heading("What changed")
        p.line(WHAT_CHANGED_SENTENCE)
        p.blank()

        # ---- THE APPENDIX: the model figures, grouped by section, the figure lines exactly as before ----
        p.page_break()
        p.heading(APPENDIX_HEADING)
        p.line(APPENDIX_SENTENCE)
        p.blank()
        p.heading("Header")
        for line in _header_print_lines(header_figs, trading_cur, reporting_cur):
            p.line(line)
        p.blank()
        for fy in sorted(by_fy, key=_fiscal_year_sort_key):
            p.heading("Fiscal year {0}".format(fy))
            for fig in by_fy[fy]:
                p.line(_plain_figure_line(fig, trading_cur, reporting_cur))
            p.blank()

        p.finish()

    if write_text:
        import pypdf

        reader = pypdf.PdfReader(str(pdf_path))
        # layout mode: the Lato glyph spacing makes the default extractor split a word after a wide capital
        # ("Information T echnology"); the layout extractor reads the same text layer without the false space.
        full_text = "\n".join(
            ln.rstrip() for page in reader.pages
            for ln in (page.extract_text(extraction_mode="layout") or "").split("\n") if ln.strip()
        )
        txt_path.write_text(full_text, encoding="utf-8")

    # ADDITIVE ONLY (AMGT-rl-10): one more file, never a change to pdf_path/txt_path above --
    # the PDF and the txt were already fully written before this line runs.
    # AMGT-bw-2: `write_rich=False` skips this (the served PDF route passes it: it carries the narrative now, and the
    # rich export is the route that writes the markdown). Every other caller keeps the one write it always had.
    if write_rich and (thesis_bundle or peer_set or posture):
        build_rich_text(
            security,
            model_block,
            thesis_bundle=thesis_bundle,
            peer_set=peer_set,
            posture=posture,
            out_dir=out_dir,
        )

    return pdf_path, txt_path


# ---------------------------------------------------------------------------
# BRANCH (b): "or machine readable rich text output" (FWD-30, AMGT-rl-10).
#
# SAME DISCIPLINE AS `build_pack`: the caller supplies every input; this reads no store and
# opens no input file; it writes only to `out_dir`; it computes NOTHING -- every figure line
# reuses `render_figure_line` (the SAME provenance renderer `build_pack` calls above, so a
# figure withheld on the PDF/txt path is withheld here too, byte-identical reasoning); every
# drafted sentence, evidence passage, officer row, peer member and posture claim is the
# CALLER's own bundle, read once and written through, never reworded, rounded or derived.
# C-MARK-NOT-DEGRADE binds equally: an undrafted section renders `[MACHINE-EMPTY: ...]`, an
# absent block renders `ABSENT -- <reason>`, never a blank that looks finished.
# ---------------------------------------------------------------------------

_DRAFTED_SECTIONS = (
    ("recommendation", "Recommendation"),
    ("company_description", "Company Description"),
    ("investment_thesis", "Investment Thesis"),
    ("risks", "Risks and Considerations"),
    ("ceo_bio", "Management/Board bio"),
)


# ---------------------------------------------------------------------------
# C-EXPORT-ADDS-NOTHING (AMGT-ro-1, FWD-30's DONE WHEN, row Z-S268): `build_rich_text`'s header
# table used to print EVERY header-scope figure on the model block -- 14 of them on the landed
# BA_US_Equity fixture, where the identity header shows only ten: the seven Stat tiles
# (`constants.ts:109-116` STAT_TILE_DEFS) plus the three scalars `IdentityHeader`
# (`components/SecurityOverlay.tsx`) prints as plain text beside them -- sector, country
# (`{sector} -- {country}`) and currency (the price tile's own prefix, `StatTile.tsx`'s
# `formatStatValue` price branch, `IDENTITY_*_MNEMONIC` in `constants.ts:122-124`). The
# remaining four (NAME, EQY_SH_OUT_REAL, EQY_FREE_FLOAT_PCT, SHORT_INT_RATIO) reach NO rendered
# surface on this page at all (measured: no `.tsx` source under `pages/SecurityAnalysis`
# mentions them outside a fixture/test file); NAME in particular is NOT the same value as
# `identity.company_name` -- a DIFFERENT field the header renders only when the identity object
# itself carries it, which this module cannot see (no channel from `build_rich_text`'s inputs to
# the identity block) -- so NAME never gets a value row here.
#
# Transcribed here, never re-derived: this module has no import path to the TS constants file
# (a Python module cannot import a `.ts` file), so the mnemonic list is restated verbatim rather
# than computed. A change to `constants.ts`'s STAT_TILE_DEFS/IDENTITY_*_MNEMONIC is a change here
# too -- named so a future editor finds this comment via `comp-find`.
PAGE_HEADER_MNEMONICS = frozenset(
    {
        # the seven Stat tiles (constants.ts:109-116 STAT_TILE_DEFS)
        "PX_LAST",
        "CUR_MKT_CAP",
        "CURR_ENTP_VAL",
        "NET_DEBT",
        "EQY_BETA",
        "SI_PERCENT_EQUITY_FLOAT",
        "VOLUME_AVG_30D",
        # the identity line's three scalars (constants.ts:122-124)
        "GICS_SECTOR_NAME",
        "CNTRY_OF_DOMICILE",
        "CRNCY",
    }
)

# ---------------------------------------------------------------------------
# FWD-30 (AMGT_RESAPP round 72, AMGT-av-2): THE PAGE'S OWN MODEL-SHEET ROWS. The Model tab renders
# ONLY the rows `modelSheet.ts` names (`FINANCIAL_SUMMARY_ROWS`, `MARGIN_HISTORY_ROWS`, `V3_LINE_ROWS`; the
# old "other lines the block carries" group is gone), so a figure on the model block that no row
# names reaches no rendered surface and must not reach this document. Transcribed here, never
# re-derived (a Python module cannot import a `.ts` file): `(label, mnemonic, forecast mnemonic)`
# in the sheet's own order, the forecast mnemonic being `spec.forecast ?? FORECAST_MNEMONICS[label]`.
# `tests/test_av2_export_equals_page.py` parses `modelSheet.ts` and fails when this table drifts.
SHEET_ROWS = (
    # FINANCIAL_SUMMARY_ROWS
    ('Revenue/Sh', 'REVENUE_PER_SH', None),
    ('EPS', 'IS_EPS', 'BEST_EPS'),
    ('BVPS', 'BOOK_VAL_PER_SH', 'BEST_BPS'),
    ('Diluted shares', 'IS_SH_FOR_DILUTED_EPS', None),
    ('DPS', 'IS_DIV_PER_SHR', 'BEST_DPS'),
    ('Dividend yield', 'EQY_DVD_YLD_IND', 'BEST_DIV_YLD'),
    ('FCF yield', 'FREE_CASH_FLOW_YIELD', None),
    ('P/E', 'PE_RATIO', 'BEST_PE_RATIO'),
    ('P/B', 'PX_TO_BOOK_RATIO', None),
    ('FCF margin', 'FREE_CASH_FLOW_MARGIN', None),
    ('ROA', 'RETURN_ON_ASSET', None),
    ('ROE', 'RETURN_COM_EQY', None),
    ('RoTA', 'RETURN_ON_TANGIBLE_ASSETS', None),
    # MARGIN_HISTORY_ROWS
    ('EBITDA', 'EBITDA', 'BEST_EBITDA'),
    ('EBITDA (adjusted)', 'EBITDA_ADJUSTED', None),
    ('EBITDA margin', 'EBITDA_MARGIN', None),
    ('Earnings margin', 'PROF_MARGIN', None),
    # V3_LINE_ROWS
    ('Goodwill', 'ARD_GOODWLL', None),
    ('Other intangible assets (excluding goodwill)', 'ARD_OTHER_INTANGIBLE_ASSET', None),
    ('Shares outstanding, as reported', 'ARD_SHARES_OUTSTANDING', None),
    ('Total current liabilities', 'ARD_TOTAL_CURRENT_LIABILITIES', None),
    ('Total assets', 'ARD_TOT_ASSETS', None),
    ('Average dividend yield over the year', 'AVERAGE_DIVIDEND_YIELD', None),
    ('Average enterprise value to trailing EBIT', 'AVERAGE_EV_TO_T12M_EBIT', None),
    ('Average enterprise value to trailing sales', 'AVERAGE_EV_TO_T12M_SALES', None),
    ('Average price to earnings over the year', 'AVERAGE_PRICE_EARNINGS_RATIO', None),
    ('Average price to book over the year', 'AVERAGE_PRICE_TO_BOOK_RATIO', None),
    ('Average price to free cash flow over the year', 'AVERAGE_PRICE_TO_FREE_CASH_FLOW', None),
    ('Average enterprise value to trailing EBITDA', 'AVG_EV_TO_T12M_EBITDA', None),
    ('Capital expenditure, as a positive amount', 'CAPEX_ABSOLUTE_VALUE', None),
    ('Cash and marketable securities', 'CASH_AND_MARKETABLE_SECURITIES', None),
    ('Cash flow from operations', 'CF_CASH_FROM_OPER', None),
    ('Dividend yield at the fiscal year end', 'DIVIDEND_YIELD', None),
    ('Earnings available to common shareholders', 'EARN_FOR_COMMON', None),
    ('Fiscal year of the financial statements', 'EQY_FUND_YEAR', None),
    ('Enterprise value to trailing EBIT', 'EV_TO_T12M_EBIT', None),
    ('Enterprise value to trailing EBITDA', 'EV_TO_T12M_EBITDA', None),
    ('Enterprise value to trailing sales', 'EV_TO_T12M_SALES', None),
    ('Free cash flow margin after operating lease payments', 'FCF_MARGIN_AFTER_OPER_LEA_PYMT', None),
    ('Free cash flow per share', 'FREE_CASH_FLOW_PER_SH', None),
    ('Highest price to book over the year (closing prices)', 'HIGH_CLOSING_PRICE_TO_BOOK_RATIO', None),
    ('Highest dividend yield over the year', 'HIGH_DIVIDEND_YIELD', None),
    ('Highest enterprise value to trailing EBIT over the year', 'HIGH_EV_TO_T12M_EBIT', None),
    ('Highest enterprise value to trailing EBITDA over the year', 'HIGH_EV_TO_T12M_EBITDA', None),
    ('Highest enterprise value to trailing sales over the year', 'HIGH_EV_TO_T12M_SALES', None),
    ('Highest price to free cash flow over the year', 'HIGH_PRICE_TO_FREE_CASH_FLOW', None),
    ('Market capitalisation at the fiscal year end', 'HISTORICAL_MARKET_CAP', None),
    ('Lowest price to book over the year (closing prices)', 'LOW_CLOSING_PRICE_TO_BOOK_RATIO', None),
    ('Lowest dividend yield over the year', 'LOW_DIVIDEND_YIELD', None),
    ('Lowest enterprise value to trailing EBIT over the year', 'LOW_EV_TO_T12M_EBIT', None),
    ('Lowest enterprise value to trailing EBITDA over the year', 'LOW_EV_TO_T12M_EBITDA', None),
    ('Lowest enterprise value to trailing sales over the year', 'LOW_EV_TO_T12M_SALES', None),
    ('Lowest price to free cash flow over the year', 'LOW_PRICE_TO_FREE_CASH_FLOW', None),
    ('Minority (non-controlling) interest', 'MINORITY_NONCONTROLLING_INTEREST', None),
    ('Return on assets, normalised', 'NORMALIZED_ROA', None),
    ('Return on equity, normalised', 'NORMALIZED_ROE', None),
    ('Price to earnings at the highest close of the year', 'PX_ERN_RATIO_WITH_HIGH_CLOS_PX', None),
    ('Price to earnings at the lowest close of the year', 'PX_ERN_RATIO_WITH_LOW_CLOS_PX', None),
    ('Short and long-term debt', 'SHORT_AND_LONG_TERM_DEBT', None),
    ('Tangible book value per share', 'TANG_BOOK_VAL_PER_SH', None),
    ('Total equity (including minority interest)', 'TOTAL_EQUITY', None),
    ('Cash flow per share (consensus estimate)', 'BEST_CPS', 'BEST_CPS'),
)
SHEET_MNEMONICS = frozenset(mnemonic for _label, mnemonic, _forecast in SHEET_ROWS)
SHEET_LAST_YEAR = 2028  # modelSheet.ts's own SHEET_LAST_YEAR -- card 3's declared 2016-2028 range


def _refuse_verdicts(check_face) -> tuple:
    """Split the bundle's `check_face` REFUSE verdicts into a header-mnemonic set and a
    `(mnemonic, fiscal_year)` set -- the SAME face `_refused_figures_markdown` reads below, so a
    figure withheld from the page's Model tab (shown there only as its REFUSED sentence) is
    withheld from this document's value tables too, never printed as a value row."""
    header: set = set()
    fiscal: set = set()
    for entry in check_face or []:
        if entry.get("verdict") != "REFUSE":
            continue
        parts = str(entry.get("figure_id", "")).split(":")
        if len(parts) >= 2 and parts[0] == "header":
            header.add(parts[1])
        elif len(parts) >= 3 and parts[0] == "fiscal_year_line_item":
            fiscal.add((parts[1], parts[2]))
    return header, fiscal


# AMGT-by-2 (AMGT_RESAPP round 118, the CTO's round-117 analysis item 2): THE RICH EXPORT FOLLOWS THE PACK'S RULES IN FULL.
# (1) every served reason the export prints goes through `_plain_reason` (AMGT-by-1's ONE mapper) with its own fixed sentence;
#     a served state code (an absent cause, a CEO reading, a read status) prints in plain words, never as the code;
# (2) the Header figure table withholds the figures the PAGE withholds (`_withheld`) and prints the page's words for each.
RICH_NOT_PLAIN_SENTENCE = "the reason on file is not stated in plain words"
ABSENT_POSTURE_SENTENCE = "no positioning view is on file for this name"
ABSENT_DESCRIPTION_SENTENCE = "no description is on file for this name yet"
ABSENT_MANAGEMENT_SENTENCE = "no management object is on file for this name"
ABSENT_COLUMN_SENTENCE = "the registry join for this column is not on file yet"
REFUSED_SENTENCE = "the check did not pass for this figure; no value is shown"
_ABSENT_BECAUSE_WORDS = {
    "NO_OBJECT": "no management object is on file",
    "ZERO_OFFICERS": "the object on file names no officers",
    "ROSTER_UNRESOLVED_NO_FALLBACK": "the filing roster did not resolve and no fallback is carried",
}
_CEO_READING_WORDS = {
    "CONFIRMED": "confirmed",
    "NOT_SEARCHED": "not searched",
    "SEARCHED_NOTHING_FOUND": "searched, nothing found",
    "SEARCHED_LINKS_UNREADABLE": "searched, links unreadable",
    "SEARCH_FAILED": "search failed",
    "UNREADABLE_OBJECT": "the object could not be read",
}
_READ_STATUS_WORDS = {"READ_FAILED": "failed", "SERVED": "served", "ABSENT": "absent"}


def _read_status_words(status) -> str:
    """A served read status in plain words (`READ_FAILED` reads `failed`); a status the table does not name is mapped as a reason."""
    return _READ_STATUS_WORDS.get(status) or _plain_reason(status, RICH_NOT_PLAIN_SENTENCE)


def _withheld_row_text(fig) -> str:
    """AMGT-by-2 rule (2): a withheld header money figure's row reads `<label>: <the page's words>` and carries no amount."""
    return "{0}: {1}".format(_plain_label(fig), CURRENCY_UNCONFIRMED_WORDS)


def _md_escape_row(text) -> str:
    """A markdown TABLE CELL may not carry a bare newline or an unescaped pipe -- both would
    break the row into extra cells/lines. Nothing else about the text is touched."""
    return str(text).replace("|", "/").replace("\n", " ")


def _figures_table(figures, withhold: bool = False) -> list:
    """A GitHub-flavoured markdown table, one row per figure: `| Mnemonic | Line | Rendered |`.
    The MNEMONIC stays the first cell (FWD-30's harness keys each row on that single token). LINE is
    the line's name in words from the ONE served definition (`model_words.line_name`, AMGT-ww-4):
    the served name for a mapped mnemonic, else the figure's own `basis.definition`, else
    "A line this pack does not name" -- the page's `lineName` order. The RENDERED column is
    `render_figure_line`'s own output verbatim -- the same text `build_pack`'s txt carries for
    the same figure, so a figure withheld/marked there reads withheld/marked here too.
    AMGT-by-2: with `withhold=True` (the Header table only) a money figure the page withholds (`_withheld`) reads the
    page's words in its RENDERED cell and no amount; every other row is rendered exactly as before."""
    lines = ["| Mnemonic | Line | Rendered |", "|---|---|---|"]
    for fig in figures:
        mnemonic = fig.get("mnemonic", "?")
        rendered = _withheld_row_text(fig) if withhold and _withheld(fig) else render_figure_line(fig)
        lines.append("| {0} | {1} | {2} |".format(
            _md_escape_row(mnemonic),
            _md_escape_row(model_words.line_name(mnemonic, [fig])),
            _md_escape_row(rendered),
        ))
    return lines


def _drafted_section_markdown(bundle, section_id: str, label: str) -> list:
    """One `## <label>` section: every sentence of the drafted section, each followed by a
    block-quoted evidence passage per citation (verbatim passage text, its accession line, its
    location). ONLY EVER CALLED when the bundle's `drafting_status` is SERVED overall
    (`build_rich_text`'s own branch) -- inside that, an INDIVIDUAL section with zero sentences
    renders NOTHING here, no heading, no marker: `PillarSection`/`CompanyDescriptionSection`
    (`ThesisTab.tsx` :157-158, :186, :211-212, :236-240) all `return null` for that case, so the
    page shows nothing for it either (round 41's item 1, the SERVED-bundle sub-case). The WHOLE
    bundle undrafted is a DIFFERENT state, `_undrafted_thesis_markdown`'s ONE line."""
    sections = (bundle or {}).get("drafted_sections") or []
    section = next((s for s in sections if s.get("section_id") == section_id), None)
    sentences = (section or {}).get("sentences") or []
    if not sentences:
        return []
    out = ["## {0}".format(label), ""]
    if section_id == "company_description" and section.get("description_verdict_state") != "PASSED":
        # AMGT-ro-3 x ro-1, joined by the issuer at the drain: the page's Thesis tab
        # (`ThesisTab.tsx` CompanyDescriptionNotServed) shows the header's ABSENT sentence and
        # keeps the drafted sentences under an honest heading unless the section's own
        # describes-the-business verdict is PASSED -- the same two faces, the same fallback reason.
        out.append("Description: ABSENT -- {0}".format(
            _plain_reason(section.get("description_verdict_reason") or "no reason recorded", ABSENT_DESCRIPTION_SENTENCE)))
        out.append("")
        out.append("### Filed detail (does not describe the business)")
        out.append("")
    for sentence in sentences:
        # AMGT-bv-2: a sentence that IS the filing's own text is carried verbatim (never long-formed by the export pass)
        text = sentence.get("text", "")
        out.append(_Verbatim(text) if _is_source_quotation(sentence) else text)
        for evidence in sentence.get("evidence") or []:
            evidence_id = evidence.get("id", "?")
            passage = evidence.get("passage", "")
            source = evidence.get("source") or {}
            accession = source.get("accession")
            location = source.get("location")
            # SAME identity line the page's own `EvidenceDisclosure` renders
            # (`ThesisTab.tsx`: `{record.id}{... accession ...}{... location ...}`) -- so the
            # SAME evidence id + accession pair extracts identically off both surfaces.
            id_line = "{0}{1}{2}".format(
                evidence_id,
                " -- accession {0}".format(accession) if accession else " -- accession unrecorded",
                " -- {0}".format(location) if location else "",
            )
            out.append("> {0}".format(id_line))
            # AMGT-bv-2 (W506-S5): the passage is the source's own words, printed exactly as served
            out.append(_Verbatim("> \"{0}\"".format(passage)))
        out.append("")
    return out


def _undrafted_thesis_markdown(bundle) -> list:
    """The Thesis tab's OWN ONE empty state for the WHOLE panel (`ThesisTab.tsx`
    `ThesisEmptyState`, :270-292, gated on `served = data.drafting_status === 'SERVED'` at
    :323/:341) -- printed here ONCE, in place of the four separate `[MACHINE-EMPTY: ...]`
    markers `_drafted_section_markdown` used to print per section (company_description,
    investment_thesis, risks, recommendation) whenever the bundle's `drafting_status` is not
    SERVED, including no bundle at all (ABSENT by omission, this module's own docstring).
    Round 41's finding (AMGT_RESAPP round 42, AMGT-rq-1 item 1): the page shows ONE line; the
    export showed four, none of which the page carries.

    `PanelError`'s message+cause (INVALID) and `PanelEmpty`'s message+detail (ABSENT, with an
    incomplete read) are each TWO separate text nodes on the page -- never joined with "--" --
    so this prints them as two separate lines too, never invents the join."""
    bundle = bundle or {}
    status = bundle.get("drafting_status")
    reason = bundle.get("drafting_reason")
    out = ["## Investment Thesis", ""]
    if status == "INVALID":
        out.append("No drafted prose shown -- the drafted document did not clear validation.")
        out.append("Cause: {0}".format(_plain_reason(reason or "no reason recorded", RICH_NOT_PLAIN_SENTENCE)))
    else:
        out.append("No drafted prose for this name yet.")
        if bundle.get("drafting_read_completed") is False:
            out.append("The read did not complete: {0}".format(
                _plain_reason(reason or "no reason recorded", RICH_NOT_PLAIN_SENTENCE)))
    out.append("")
    return out


def _header_description_lines(description) -> list:
    """The header's OWN description object (`overlay.description`, computed server-side by
    `scoped_amgt.read_description`), rendered exactly as `HeaderBrief.tsx`'s DescriptionLine
    renders it: `Description: ABSENT -- <reason>` (the reason verbatim, else "no reason
    recorded") unless the status is SERVED with text, then `Description: <text>`. The page composes
    this reason from the model block's header-scalar census AND the drafting verdict, so it differs
    from the Thesis tab's own shorter verdict reason, which `_drafted_section_markdown` carries."""
    if description.get("status") != "SERVED" or not description.get("text"):
        line = "Description: ABSENT -- {0}".format(
            _plain_reason(description.get("reason") or "no reason recorded", ABSENT_DESCRIPTION_SENTENCE))
    else:
        line = "Description: {0}".format(description["text"])
    return [line, ""]

def _management_markdown(bundle) -> list:
    """The Exec table -- every officer row the bundle's `management.officers` carries, verbatim
    (name, role, tenure, source), plus the CEO public-profile reading.

    C-EXPORT-ADDS-NOTHING (AMGT-ro-1): NO ceo_bio drafted-section narrative here. Measured:
    `ExecManagementTab.tsx` (the ONE surface `management` reaches) renders the officer roster and
    `CeoProfile`'s six profile-LINK readings only -- zero references to `ceo_bio` or a drafted
    narrative bio anywhere in that file. The page has no rendered surface for that narrative at
    all, so a MACHINE-EMPTY marker for it (let alone real drafted text) would be an export figure
    the page can never show, whatever the bundle carries. `_DRAFTED_SECTIONS` still lists
    `ceo_bio` (kept for `_management_markdown`'s own historical callers/tests to name it by), but
    `build_rich_text`'s loop already skips it and nothing calls `_drafted_section_markdown` for it
    here any more."""
    management = (bundle or {}).get("management") or {}
    out = ["## Management/Board", ""]
    status = management.get("management_status", "ABSENT")
    if status == "READ_FAILED":
        # `ExecManagementTab.tsx`'s `ManagementBody` (:203-211): a `PanelError` with `message`
        # and `hint` as TWO separate text nodes -- no "ABSENT --" joiner, never invented here.
        out.append("Exec Management: the read did not complete.")
        out.append(_plain_reason(management.get("reason") or "no reason recorded on the object", RICH_NOT_PLAIN_SENTENCE))
        out.append("")
    elif status != "SERVED" or not management.get("officers"):
        # `ManagementBody` (:213-227): `PanelEmpty` message `Exec Management: ABSENT
        # (<absent_because>).` -- ONE line, the reason on its OWN following line, never joined
        # with "--" (the page never prints that pattern for this branch). AMGT-by-2: the cause is said in
        # plain words (the served code never prints).
        absent_because = management.get("absent_because") or "NO_OBJECT"
        words = _ABSENT_BECAUSE_WORDS.get(absent_because) or _plain_reason(absent_because, RICH_NOT_PLAIN_SENTENCE)
        out.append("Exec Management: ABSENT ({0}).".format(words))
        out.append(_plain_reason(management.get("reason") or "no management object for this name", ABSENT_MANAGEMENT_SENTENCE))
        out.append("")
    else:
        out.append("| Name | Role | Tenure (yrs) | Source |")
        out.append("|---|---|---|---|")
        for officer in management["officers"]:
            out.append(
                "| {0} | {1} | {2} | {3} |".format(
                    _md_escape_row(officer.get("name", "?")),
                    _md_escape_row(officer.get("role", "?")),
                    _md_escape_row(officer.get("tenure_years", "?")),
                    _md_escape_row(officer.get("source", "?")),
                )
            )
        out.append("")
        reading = (management.get("ceo_profile_reading") or {}).get("reading")
        if reading:
            # AMGT-by-2: the served reading state in plain words (the page's own CeoProfile wording), never the code
            out.append("CEO public-profile reading: {0}".format(
                _CEO_READING_WORDS.get(reading) or _plain_reason(reading, RICH_NOT_PLAIN_SENTENCE)))
            out.append("")
    return out


def _peers_markdown(peer_set) -> list:
    """The Peers PRESENT columns (`csc_columns.present`, the registry join CSC actually
    resolved) as a table naming each present column's registry code, plus every peer MEMBER's
    own identity fields, verbatim -- and the ABSENT columns, each `ABSENT -- <reason>`
    (C-MARK-NOT-DEGRADE), never silently dropped from the page's own accounting.

    `PeersTab.tsx` (:199-231) gates the WHOLE CSC table (present columns, members, absent-column
    disclosure) on `peers.basis !== 'absent'` -- when the subject's own classification never
    landed, the page shows ONE line, `{data.reason}{peer_read ? ' (read <status>)' : ''}`, and
    renders no CSC table AT ALL (round 42's own finding on top of round 41's four: the export
    used to print the full present/absent-column breakdown regardless)."""
    if not peer_set:
        return ["## Peers", "", "ABSENT -- no peer set supplied to this export", ""]
    if peer_set.get("basis") == "absent":
        reason = _plain_reason(peer_set.get("reason") or "no basis recorded", NO_PEERS_SENTENCE)
        peer_read = peer_set.get("peer_read") or {}
        status = peer_read.get("status")
        line = "{0}{1}".format(reason, " (read {0})".format(_read_status_words(status)) if status else "")
        return ["## Peers", "", line, ""]
    out = ["## Peers", ""]
    csc = peer_set.get("csc_columns") or {}
    present = csc.get("present") or []
    absent = csc.get("absent") or []
    out.append(
        "Present columns ({0} of {1} declared):".format(len(present), csc.get("columns_declared", len(csc.get("columns", []))))
    )
    out.append("")
    out.append("| Column | Registry code | Relation |")
    out.append("|---|---|---|")
    for col in present:
        out.append(
            "| {0} | {1} | {2} |".format(
                _md_escape_row(col.get("column", "?")),
                _md_escape_row(col.get("code", "?")),
                _md_escape_row(col.get("relation", "?")),
            )
        )
    out.append("")
    members = peer_set.get("members") or []
    if members:
        out.append("| Member | Ticker | Sector | Country | Market cap (musd) |")
        out.append("|---|---|---|---|---|")
        for member in members:
            out.append(
                "| {0} | {1} | {2} | {3} | {4} |".format(
                    _md_escape_row(member.get("name", "?")),
                    _md_escape_row(member.get("ticker", "?")),
                    _md_escape_row(member.get("sector", "?")),
                    _md_escape_row(member.get("country", "?")),
                    _md_escape_row(member.get("market_cap_musd", "?")),
                )
            )
        out.append("")
    for col in absent:
        out.append(
            "{0}: ABSENT -- {1}".format(
                col.get("column", "?"),
                _plain_reason(col.get("reason", "no reason recorded"), ABSENT_COLUMN_SENTENCE),
            )
        )
    out.append("")
    return out


# `LeadPanel.tsx`'s `PostureHeaderLine` (:283), verbatim -- the SERVED-posture header line's own
# fixed closing sentence, on every tab's render, never just the Posture tab's body.
_POSTURE_MACHINE_DISCLAIMER = " -- a machine's view for a person to accept or reject, never an instruction."


def _posture_markdown(posture) -> list:
    """The analyst posture verdict and every basis claim, each with its own cites -- rendered
    the SAME "accession"/cite vocabulary the page uses, never a hardcoded restatement.

    Mirrors `PostureTab.tsx`'s own four-way status branch (`PostureBody`, :409-448): no
    `posture` object at all -> "Posture: not carried on this payload." (`:420-425`);
    `READ_FAILED` -> "Posture: the read did not complete -- not evidence that no posture
    exists." with its own reason (`:429-436`); any other non-SERVED status -> "Posture: ABSENT
    -- <reason>. Nothing is rendered in its place." (`:440-446`). Inside SERVED, a `verdict` of
    `absent` is not a missing object -- it is the judge's own no-call verdict, rendered as
    `postureVerdictSentence`'s "ABSENT -- no call was made" plus the object's reason
    (`PostureTab.tsx:78`, `:344`), never the generic `Verdict: <word>` line below.

    A SERVED posture is ALSO summarised in the page's shared header, every tab, every render
    (`SecurityOverlay.tsx`'s `PostureHeaderLine`/`LeadPanel.tsx`'s copy, :268-284): the SAME
    sentence, ending in the SAME fixed disclaimer, " -- a machine's view for a person to accept
    or reject, never an instruction." -- carried here too (`_POSTURE_MACHINE_DISCLAIMER` below).

    AMGT-tt-1: an ABSENT posture shows on the page in TWO PLACES with TWO DIFFERENT sentences --
    the header line (no "Nothing is rendered in its place." tail; the SERVED+absent header line
    DOES carry the machine disclaimer, the non-SERVED header line does NOT) and the Posture tab's
    own line (the reverse: non-SERVED carries "Nothing is rendered in its place.", SERVED+absent
    carries no disclaimer). Both forms are written here, each as its OWN markdown line, byte-
    identical to the page's words, so neither page absence is missing from this document."""
    if not posture:
        return ["## Analyst Posture", "", "Posture: not carried on this payload.", ""]
    status = posture.get("status")
    if status == "READ_FAILED":
        out = ["## Analyst Posture", "", "Posture: the read did not complete -- not evidence that no posture exists."]
        reason = posture.get("reason")
        if reason:
            out.append(_plain_reason(reason, RICH_NOT_PLAIN_SENTENCE))
        out.append("")
        return out
    if status != "SERVED":
        reason = _plain_reason(posture.get("reason") or "no posture object for this name", ABSENT_POSTURE_SENTENCE)
        return [
            "## Analyst Posture",
            "",
            # The header line (`PostureHeaderLine`, non-SERVED branch, :148-153 SecurityOverlay.tsx):
            # no "Nothing is rendered in its place." tail.
            "Posture: ABSENT -- {0}".format(reason),
            # The Posture tab's own line (`PostureBody`, :440-446 PostureTab.tsx): the tail IS present.
            "Posture: ABSENT -- {0}. Nothing is rendered in its place.".format(reason),
            "",
        ]
    out = ["## Analyst Posture", ""]
    verdict = posture.get("verdict")
    if verdict == "absent":
        reason = _plain_reason(posture.get("reason") or "the object carries no reason", RICH_NOT_PLAIN_SENTENCE)
        # The Posture tab's own line (`ServedPosture`, :342-345 PostureTab.tsx): no disclaimer.
        out.append("ABSENT -- no call was made: {0}".format(reason))
        # The header line (`PostureHeaderLine`, SERVED branch, :155-167 SecurityOverlay.tsx): the
        # disclaimer IS present.
        out.append(
            "ABSENT -- no call was made: {0}{1}".format(reason, _POSTURE_MACHINE_DISCLAIMER)
        )
    else:
        out.append("Verdict: {0} (comparable: {1})".format(verdict or "?", posture.get("comparable", "?")))
    out.append("")
    for claim in posture.get("basis") or []:
        out.append(claim.get("claim", ""))
        cites = claim.get("cites") or []
        if cites:
            out.append("> cites: {0}".format(", ".join(cites)))
        out.append("")
    return out


def _case_currency(case, crncy):
    """AMGT-rs-1: the served case's value is in the unit of the name's OWN price, so its
    currency is CRNCY (the header figure the Price tile prints), never guessed from the case
    itself. Byte-identical to `caseCurrency` on the page (`ModelTab.tsx`): a case carrying its
    own `quote_currency` that DISAGREES with CRNCY, or a name with no CRNCY at all, carries NO
    currency here -- the caller does not choose between them."""
    own = case.get("quote_currency")
    if own and crncy and own != crncy:
        return None
    return crncy or None


def _model_case_line(name, case, crncy=None) -> str:
    """ONE line per case -- byte-identical to `ModelCaseLine` on the page (`ModelTab.tsx`):
    "<Name> case: <STATUS> -- <detail>" (or "<label>: <STATUS> -- <detail>" when the case carries a
    `label`), detail = "<value> <currency> (<formula>)" (currency
    per `_case_currency`, omitted when it carries none; formula omitted when absent) when
    SERVED, the case's own reason when ABSENT. The value prints with exactly two decimals on both
    sides (AMGT-uu-3; supersedes the whole-number `.0` strip of row AMGT_RESAPP-Z-S281)."""
    case = case or {}
    status = case.get("status") or "ABSENT"
    if status == "SERVED":
        value = case.get("value")
        # AMGT-uu-3: a SERVED value prints as a value, exactly two decimals ("537.70"), identical
        # to `value.toFixed(2)` on the page (ModelTab.tsx) -- FWD-30 compares the two lines byte
        # for byte. A non-numeric value (never served) falls back to its text.
        value_text = (
            "%.2f" % value
            if isinstance(value, (int, float)) and not isinstance(value, bool)
            else str(value)
        )
        currency = _case_currency(case, crncy)
        if currency:
            value_text = "{0} {1}".format(value_text, currency)
        formula = case.get("formula")
        detail = "{0} ({1})".format(value_text, formula) if formula else value_text
    else:
        detail = _plain_reason(case.get("reason") or "no {0} case on the landed block".format(str(name).lower()),
                           RICH_NOT_PLAIN_SENTENCE)  # AMGT-by-2: a served reason prints only in plain words
    # AMGT-vv-1: a case carrying a `label` prints "<label>: <STATUS> -- <detail>" (identical on the page).
    label = case.get("label")
    head = "{0}: {1}".format(label, status) if label else "{0} case: {1}".format(name, status)
    return "{0} -- {1}".format(head, detail)


def _model_cases_markdown(cases, crncy=None) -> list:
    """The SAME per-case lines `CasesBlock`/`ModelCaseLine` render on the Model tab, byte-
    identical wording, one line per case name the payload declares (default Upside/Base/
    Downside) -- so a SERVED base case and an ABSENT upside/downside case each read their OWN
    status and content on both surfaces. Row AMGT_RESAPP-Z-S281: the prior top-level-only read
    (`cases.status`/`cases.reason`) showed "SERVED -- the payload carries no case block" for a
    name whose base case IS a real landed number, because the served payload
    (`scoped_amgt._model_cases`) never carries a top-level `reason` key at all -- only nested
    `base`/`upside`/`downside` objects, each with its own. `crncy` is AMGT-rs-1's addition: the
    name's own CRNCY header figure, threaded into every SERVED case's currency."""
    cases = cases or {}
    names = cases.get("cases") or ["Upside", "Base", "Downside"]
    out = ["## Model Cases", ""]
    for name in names:
        out.append(_model_case_line(name, cases.get(str(name).lower()), crncy))
    out.append("")
    return out


def _model_sheet_notes_markdown(fiscal_years, forecast_years=()) -> list:
    """The SAME two footnote lines `ModelTab.tsx`'s `ModelBody` renders, off the SAME years the
    sheet carries -- the y/y-growth line is unconditional; the estimate-years line only when the
    sheet's own 2028 range holds a year NEITHER the history NOR the served forecasts reach
    (`estimateYearsAbsent`). The years it states are the ones actually carried, the forecast years
    included (`firstYear`/`lastYear` are the sheet's first and last column): a name whose
    consensus reaches 2028E states no estimate-years absence at all, and one whose consensus
    stops at 2027E reads "2028E: ABSENT -- the block carries fiscal years 2016 to 2027E only."
    `forecast_years` is the list of `"<year>E"` columns (e.g. `["2026E", "2027E"]`)."""
    years = sorted({str(y) for y in (fiscal_years or [])})
    estimates = [str(y) for y in (forecast_years or [])]
    out = ["y/y growth rows: ABSENT -- the block carries none and this page computes none."]
    if years:
        last = int(years[-1]) if years[-1].isdigit() else None
        if last is not None:
            absent = [
                "{0}E".format(y) for y in range(last + 1, SHEET_LAST_YEAR + 1) if "{0}E".format(y) not in estimates
            ]
            if absent:
                carried = years + estimates
                out.append(
                    "{0}: ABSENT -- the block carries fiscal years {1} to {2} only.".format(
                        ", ".join(absent), carried[0], carried[-1]
                    )
                )
    return out


def _refused_figures_markdown(check_face, declared_years=None) -> list:
    """Every REFUSE verdict the bundle's `check_face` carries FOR A FISCAL-YEAR LINE ITEM
    (`figure_id` scope `fiscal_year_line_item`), grouped by mnemonic and by its DISTINCT reason
    text -- the SAME sentence `ModelTab.tsx`'s `rowRefusal` builds ("REFUSED -- <reason>"), read
    off the check face directly, never re-derived. A header-scope REFUSE (`header:MNEMONIC`) is
    EXCLUDED: the Model sheet is built from `fiscal_year_figures` alone (`modelSheet.ts`), so a
    header mnemonic never gets a `data-model-refused` row there, and the identity header's own
    Stat tile ignores check_face entirely (`StatTile.tsx`) -- the page carries that REFUSE
    nowhere as a REFUSED line, so this footnote must not invent one. A refused year outside the
    sheet's OWN declared window is excluded too (no column for it, so no REFUSED row for it
    either) when `declared_years` is given non-empty."""
    by_mnemonic: dict = {}
    for entry in check_face or []:
        if entry.get("verdict") != "REFUSE":
            continue
        parts = str(entry.get("figure_id", "")).split(":")
        if not parts or parts[0] != "fiscal_year_line_item":
            continue
        if declared_years and len(parts) >= 3 and parts[2] not in declared_years:
            continue
        mnemonic = parts[1] if len(parts) > 1 else entry.get("figure_id", "?")
        reasons = by_mnemonic.setdefault(mnemonic, [])
        reason = _plain_reason(entry.get("reason") or "see check face", REFUSED_SENTENCE)
        if reason not in reasons:
            reasons.append(reason)
    return [
        "{0}: REFUSED -- {1}".format(mnemonic, "; ".join(reasons))
        for mnemonic, reasons in by_mnemonic.items()
    ]


def _thesis_driver_chart_markdown(thesis_bundle) -> list:
    """The SAME line `ThesisDriverChart.tsx` renders when the driver chart is not SERVED --
    "The chart: ABSENT -- the thesis driver is "<series>"" -- read off `thesis_driver`/
    `thesis_driver_chart` verbatim, never re-derived."""
    if (thesis_bundle or {}).get("drafting_status") != "SERVED":
        return []  # the page draws no chart element on an undrafted thesis (AMGT-ba-18)
    chart = (thesis_bundle or {}).get("thesis_driver_chart") or {}
    if chart.get("status") == "SERVED":
        return []
    driver = (thesis_bundle or {}).get("thesis_driver") or {}
    # AMGT-by-2: the driver's name prints only when it is plain words (a served path or key never prints)
    series = _plain_reason(driver.get("series"), None)
    line = "The chart: ABSENT" + (' -- the thesis driver is "{0}"'.format(series) if series else "")
    return [line]


def _page_forecasts(thesis_bundle) -> dict:
    """`{(mnemonic, "<year>E"): figure}` -- the served forecast figures the Model tab's E columns
    read (`ModelBody`: `data.model.forecast_figures`; a payload that carries them at the top level
    is read too), keyed exactly as `buildModelSheet` keys them: the figure's mnemonic and its year
    as a number with an E; a figure with no fiscal year is skipped, the FIRST figure per key wins."""
    bundle = thesis_bundle or {}
    served = bundle.get("forecast_figures")
    if served is None:
        served = (bundle.get("model") or {}).get("forecast_figures")
    out: dict = {}
    for fig in served or []:
        if not isinstance(fig, dict) or fig.get("fiscal_year") is None:
            continue
        try:
            year = int(float(fig.get("fiscal_year")))
        except (TypeError, ValueError):
            continue
        out.setdefault((fig.get("mnemonic"), "{0}E".format(year)), fig)
    return out


def _check_id(fig) -> str:
    """`figureId` (`figureIdentity.ts`): the check-face id the page joins a figure to."""
    scope = fig.get("scope") or "unknown-scope"
    mnemonic = fig.get("mnemonic") or "unknown-mnemonic"
    year = fig.get("fiscal_year")
    return "{0}:{1}:{2}".format(scope, mnemonic, year) if year is not None else "{0}:{1}".format(scope, mnemonic)


def _row_refusals(check_face, cells_by_row) -> dict:
    """`{row mnemonic: [distinct REFUSE reasons]}` -- the Model tab's `rowRefusal`, per sheet row:
    a row with ONE refused cell (history or forecast) renders ONE refusal sentence and none of its
    figures, so ALL of the row's cells are withheld here and the row appears only as a REFUSED
    line. The first check-face entry per figure id is the one the page reads (`checkFor`)."""
    first: dict = {}
    for entry in check_face or []:
        first.setdefault(entry.get("figure_id"), entry)
    out: dict = {}
    for mnemonic, cells in cells_by_row.items():
        reasons: list = []
        for fig in cells:
            entry = first.get(_check_id(fig))
            if entry and entry.get("verdict") == "REFUSE":
                reason = _plain_reason(entry.get("reason") or "see check face", REFUSED_SENTENCE)
                if reason not in reasons:
                    reasons.append(reason)
        if reasons:
            out[mnemonic] = reasons
    return out


def _forecast_table(rows) -> list:
    """The `| Mnemonic | Line | Rendered |` table of ONE forecast year: the row's own mnemonic (the
    key the page's E cell carries -- IS_EPS for the EPS row), the row's label with the words
    "consensus estimate", and `render_figure_line` of the served forecast figure verbatim."""
    lines = ["| Mnemonic | Line | Rendered |", "|---|---|---|"]
    for mnemonic, label, fig in rows:
        lines.append("| {0} | {1} | {2} |".format(
            _md_escape_row(mnemonic),
            _md_escape_row("{0} (consensus estimate)".format(label)),
            _md_escape_row(render_figure_line(fig)),
        ))
    return lines


def build_rich_text(
    security: str,
    model_block: dict,
    thesis_bundle: dict = None,
    peer_set: dict = None,
    posture: dict = None,
    description: dict = None,
    out_dir=None,
) -> Path:
    """Render ONE machine-readable rich-text (GitHub-flavoured markdown) document and return
    its path. Reads no store, opens no input file -- every input is the caller's own, already
    read (the same discipline `build_pack` keeps above). `out_dir` defaults to the interpreter's
    temporary directory, never a path inside the repository.

    `thesis_bundle`, `peer_set`, `posture` and `description` are OPTIONAL: a caller passing only
    `(security, model_block)` gets a document carrying the header + fiscal figure tables and
    every other section as its own `ABSENT`/`[MACHINE-EMPTY: ...]` marker -- never a blank, never
    invented prose -- the same negative-control shape `build_pack`'s own no-bundle render has
    always had.

    C-EXPORT-ADDS-NOTHING (AMGT-ro-1): the header table is limited to `PAGE_HEADER_MNEMONICS`
    -- the page's own seven Stat tiles plus its three identity-line scalars -- and any figure
    (header or fiscal-year) the bundle's `check_face` marks REFUSE is withheld from every value
    table, appearing only in the "Model Notes" REFUSED line below, the same way the page's Model
    tab shows a refused row (never a bare value with no verdict attached). `description` -- the
    header's OWN description object -- is ADDITIVE-ONLY: when a caller supplies it (`_print_pack`
    does), its `Description: ...` line is written beside the header, word for word, and the drafted
    "Company Description" section below is kept, since the page shows both; when omitted, the
    document carries only the drafted section.
    """
    if not isinstance(model_block, dict):
        raise ValueError(
            "build_rich_text needs the caller's already-read model block; got {0!r}".format(
                type(model_block).__name__
            )
        )
    sec_key = security_key(security)
    figures = model_block.get("figures", [])
    header_figs_all = [f for f in figures if f.get("scope") == "header"]
    fy_figs = [f for f in figures if f.get("scope") != "header"]

    # THE MODEL TAB'S OWN YEAR WINDOW (`modelSheet.ts` `buildModelSheet`, :89-97): the sheet's
    # columns are the thesis payload's OWN declared `fiscal_years` when it carries any, else the
    # years its own (already-subset) `fiscal_year_figures` carry -- NEVER the full range the raw
    # model block holds (measured on 9433_JP_Equity: the block runs 2016-2029, the payload
    # declares 2016-2026 only). A block year outside that window has NO column on the page at
    # all, so a figure in it never reaches the table -- round 41's item 4, the largest class.
    declared_years = {str(y) for y in ((thesis_bundle or {}).get("fiscal_years") or [])}
    if not declared_years:
        declared_years = {
            str(f.get("fiscal_year"))
            for f in ((thesis_bundle or {}).get("fiscal_year_figures") or [])
            if f.get("fiscal_year") is not None
        }
    if declared_years:
        fy_figs = [f for f in fy_figs if str(f.get("fiscal_year")) in declared_years]
    # AMGT-av-2 class 1: ONLY the figures a model-sheet row names (`SHEET_ROWS`) -- the page shows no
    # other line, so none reaches this document.
    fy_figs = [f for f in fy_figs if f.get("mnemonic") in SHEET_MNEMONICS]
    # AMGT-av-2 class 2: the served 2026E-2028E forecast cells the sheet's E columns carry, row by row.
    forecast_by_key = _page_forecasts(thesis_bundle)
    forecast_years = sorted(
        {year for (_m, year) in forecast_by_key}, key=lambda y: int(y[:-1])
    )
    forecast_cells = []  # (row mnemonic, row label, forecast figure), in the sheet's own row order
    for label, mnemonic, forecast_mnemonic in SHEET_ROWS:
        if not forecast_mnemonic:
            continue
        for year in forecast_years:
            fig = forecast_by_key.get((forecast_mnemonic, year))
            if fig is not None:
                forecast_cells.append((mnemonic, label, year, fig))
    # AMGT-av-2: a sheet row with one REFUSE cell (a history year or a forecast) is withheld WHOLE and
    # reads once as its REFUSED line (`rowRefusal`), exactly as the page does.
    cells_by_row: dict = {}
    for fig in fy_figs:
        cells_by_row.setdefault(fig.get("mnemonic"), []).append(fig)
    for mnemonic, _label, _year, fig in forecast_cells:
        cells_by_row.setdefault(mnemonic, []).append(fig)
    row_refusals = _row_refusals((thesis_bundle or {}).get("check_face"), cells_by_row)
    by_fy = _group_by_fiscal_year(fy_figs)
    # THE IDENTITY HEADER'S SEVEN STAT TILES (`StatTile.tsx`): rendered off `bundle.header_figures`
    # DIRECTLY, with no check_face import at all -- a REFUSE verdict on a header mnemonic never
    # withholds its Stat tile, so it must not withhold this table's row either (measured on
    # 9433_JP_Equity: `header:CURR_ENTP_VAL` is REFUSE'd and still SERVED on the page).
    #
    # CRNCY REACHES THE PAGE ONLY AS THE PRICE TILE'S OWN PREFIX (`SecurityOverlay.tsx`:
    # `currency={def.format === 'price' ? currencyCode : undefined}`, read only inside
    # `StatTile`'s `figure ? formatStatValue(...) : null` branch) -- when PX_LAST itself carries
    # no header figure, that branch never runs and CRNCY's value reaches NO rendered surface at
    # all (measured on ROG_SW_Equity: CRNCY='CHF' present, PX_LAST absent, 'CHF' nowhere in the
    # rendered page). So CRNCY is withheld here too whenever PX_LAST is absent -- never a value
    # row the page cannot ever show.
    has_px_last = any(f.get("mnemonic") == "PX_LAST" for f in header_figs_all)
    header_figs = [
        f
        for f in header_figs_all
        if f.get("mnemonic") in PAGE_HEADER_MNEMONICS and (f.get("mnemonic") != "CRNCY" or has_px_last)
    ]

    # NAME is never a value row (PAGE_HEADER_MNEMONICS above), but the title line still needs
    # the company's display name -- read from the UNFILTERED header figures, exactly as before.
    name_fig = next((f for f in header_figs_all if f.get("mnemonic") == "NAME"), None)
    company_name = name_fig["value"] if name_fig else security

    lines = [
        "# {0} [{1}] Research Note".format(company_name, security),
        "",
        "Machine-readable rich-text export (FWD-30 branch (b)). Every figure, cite and absence "
        "below is read verbatim from the landed model block{0}; nothing here is summarised, "
        "reworded, rounded differently or derived.".format(
            ", thesis bundle, peer set and posture" if (thesis_bundle or peer_set or posture) else ""
        ),
        "",
        "## Header",
        "",
    ]
    # AMGT-by-2 rule (2): the Header table withholds the money figures the page withholds (the fiscal tables do not)
    lines.extend(_figures_table(header_figs, withhold=True))
    lines.append("")
    if description is not None:
        # The header's OWN description line (row AMGT_RESAPP-Z-S271): `HeaderBrief.tsx`'s
        # DescriptionLine, beside the header, IN ADDITION TO the Thesis tab's drafted section below
        # -- the page shows both, so replacing the section would drop the page's cites.
        lines.extend(_header_description_lines(description))
    for fy in sorted(by_fy, key=_fiscal_year_sort_key):
        lines.append("## Fiscal year {0}".format(fy))
        lines.append("")
        fy_rows = [f for f in by_fy[fy] if f.get("mnemonic") not in row_refusals]
        lines.extend(_figures_table(fy_rows))
        lines.append("")
    for year in forecast_years:
        lines.append("## Fiscal year {0}".format(year))
        lines.append("")
        lines.extend(_forecast_table([
            (m, label, fig) for (m, label, y, fig) in forecast_cells if y == year and m not in row_refusals
        ]))
        lines.append("")

    if (thesis_bundle or {}).get("drafting_status") == "SERVED":
        for section_id, label in _DRAFTED_SECTIONS:
            if section_id == "ceo_bio":
                continue  # rendered inside _management_markdown, beside the officer roster
            lines.extend(_drafted_section_markdown(thesis_bundle, section_id, label))
    else:
        # ThesisTab.tsx replaces ALL FOUR drafted sections with its own ONE empty state when
        # `drafting_status` is not SERVED (:323/:341) -- never four separate MACHINE-EMPTY
        # markers this module used to print per section.
        lines.extend(_undrafted_thesis_markdown(thesis_bundle))

    lines.extend(_management_markdown(thesis_bundle))
    lines.extend(_peers_markdown(peer_set))
    lines.extend(_posture_markdown(posture))

    # THE PAGE'S OWN OTHER ABSENCES (C-EXPORT-ADDS-NOTHING): every ABSENT/REFUSED line the
    # Model tab and the Thesis driver chart render, byte-identical, so nothing shown as an
    # absence on the page is missing from this document.
    lines.append("## Model Notes")
    lines.append("")
    # The years the sheet CARRIES (`buildModelSheet`'s `years`): the thesis payload's declared fiscal
    # years (else the years its figures carry), then the served forecast years (AMGT-av-2 class 3).
    fiscal_years = sorted(declared_years) if declared_years else sorted(
        {str(f.get("fiscal_year")) for f in fy_figs if f.get("fiscal_year") is not None}
    )
    lines.extend(_model_sheet_notes_markdown(fiscal_years, forecast_years))
    for _label, mnemonic, _forecast in SHEET_ROWS:
        if mnemonic in row_refusals:
            lines.append("{0}: REFUSED -- {1}".format(mnemonic, "; ".join(row_refusals[mnemonic])))
    lines.append("")
    lines.extend(_thesis_driver_chart_markdown(thesis_bundle))
    lines.append("")
    # AMGT-av-2 class 4: NO cases section -- the Model tab no longer renders the rule's cases
    # (`ModelTab.tsx`: "case lines are NOT rendered (FWD-12 amended)"), so the export states none.
    # `_model_cases_markdown` is kept for its own unit tests and is not called here.

    vintages = sorted(
        {str(f.get("vintage")) for f in figures if f.get("vintage")}
        | ({str(thesis_bundle.get("generated_at"))} if thesis_bundle and thesis_bundle.get("generated_at") else set())
    )
    lines.append("---")
    lines.append(
        "Source: model block ({0} figures) -- vintages {1}".format(
            len(figures), ", ".join(vintages) if vintages else "unrecorded"
        )
    )
    lines.append("")
    # AMGT-bv-2 (AMGT_RESAPP round 115, W506-S4): every date the export shows in a NON-quote line is the house long
    # form -- the Source line's vintages and generated_at, each figure line's as-of and observed segments, forecast
    # cells, served prose and citation lines. A line carried as _Verbatim (a source's own words) is written as served.
    lines = [str(ln) if isinstance(ln, _Verbatim) else _long_days(ln) for ln in lines]

    base = Path(out_dir) if out_dir else Path(tempfile.gettempdir())
    base.mkdir(parents=True, exist_ok=True)
    md_path = base / "pack_{0}.md".format(sec_key)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def main(argv) -> int:
    """Render one pack from the command line, reading the block through the SAME reader the
    served route uses -- imported here rather than at module scope, because that reader's module
    imports this one."""
    import argparse

    parser = argparse.ArgumentParser(description="Render one research pack to PDF.")
    parser.add_argument("security", nargs="?", default="SAP GY Equity")
    parser.add_argument("--model-block", default=None, help="a landed model_block JSON file")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(argv)

    if args.model_block:
        block = json.loads(Path(args.model_block).read_text(encoding="utf-8"))
    else:
        from lib.research.api.scoped_amgt import read_model_block

        block = read_model_block(security_key(args.security))
    if block is None:
        print("BLOCKED: no landed model block for {0}".format(args.security))
        return 1

    pdf_path, txt_path = build_pack(args.security, block, out_dir=args.out_dir)
    size = pdf_path.stat().st_size
    print("PACK: {0} -> {1} ({2} bytes); text extracted to {3}".format(
        args.security, pdf_path, size, txt_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
