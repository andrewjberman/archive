"""RIV-pt-1 AC1 (FWD-19 look, amendment A1) -- the theme carries the portal's tokens and the declared classes, and passes the
page's read-back rule.

Pure, offline:
  - `page_theme.TOKENS` holds canvas #F4F6FA, surface #FFFFFF, hairline #C4CBDB, navy #163372 and indigo #5F3BE3, and each
    value appears in `page_theme.CSS` (case-insensitive);
  - `CSS` defines every declared class: rf-card, rf-card-panel, rf-eyebrow, rf-seg, rf-seg-on, rf-select, rf-table, rf-missing,
    rf-muted;
  - `CSS` contains none of `url(`, `@import`, `<script`, `<link`, ` src=`, and is ASCII only;
  - control: the body background is the canvas token (a `body` rule naming #F4F6FA)."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

WANT = {"canvas": "#F4F6FA", "surface": "#FFFFFF", "hairline": "#C4CBDB", "navy": "#163372", "indigo": "#5F3BE3"}
CLASSES = ("rf-card", "rf-card-panel", "rf-eyebrow", "rf-seg", "rf-seg-on", "rf-select", "rf-table", "rf-missing", "rf-muted")


def run(v):
    c.setup_path()
    from rivalfunds import page_theme as pt

    toks = {k: str(x).upper() for k, x in pt.TOKENS.items()}
    css = pt.CSS
    print("tokens:", toks)
    v.check(all(toks.get(k) == x for k, x in WANT.items()) and all(x.lower() in css.lower() for x in WANT.values()),
            "the five portal tokens, each used in the CSS")
    miss = [k for k in CLASSES if not re.search(r"\." + re.escape(k) + r"(?![\w-])", css)]
    print("classes missing:", miss)
    v.check(not miss, "every declared class is defined")
    bad = [b for b in ("url(", "@import", "<script", "<link", " src=") if b in css.lower()]
    v.check(not bad and all(ord(ch) < 128 for ch in css), f"read-back safe and ASCII (forbidden found: {bad})")
    body = re.search(r"(^|[}\s])body\s*\{[^}]*\}", css)
    v.check(body is not None and "#f4f6fa" in body.group(0).lower(), "control: the body background is the canvas")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
