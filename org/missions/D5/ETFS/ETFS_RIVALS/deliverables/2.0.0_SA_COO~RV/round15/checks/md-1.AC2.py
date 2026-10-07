"""RIV-md-1 AC2 (PRD v0.18 FWD-22; ADDENDUM F.7; Andrew-direct script @efc0acb127): the page carries EXACTLY ONE inline script,
the render check admits that one block, and it still refuses every other script and every external resource.

Measured today on the round-8 fc-1 page: 0 `<script` tags; `render.validate` (which enforces `_BAD_CONSTRUCTS = ("<script",
"<link", " src=", "@import", "url(")`, render.py:2161, :2177) passes the page and refuses any script at all; `render.script_count`
does not exist; the page source holds neither "/chart/" nor "Chart could not load".

Interface (prescribed, verbatim): The page carries EXACTLY ONE inline `<script>` block with no `src`; `_BAD_CONSTRUCTS` admits
that one block and still refuses every other script, `src=`, `<link`, `@import`, `url(`; `render.script_count(html) -> int`. The
script: on a dialog opening, fetches `/rivalfunds/<page day>/chart/<FUND>` (same origin, once per fund, cached) ... On a failed or
missing object the status line reads "Chart could not load" and the trade list stays.
Fixture: round 8's fc-1 page, rendered by `render.render_page`; the refusal is exercised through `render.validate(html)`.
  - (a) `render.script_count(html)` is 1, and an independent count finds exactly one `<script` start tag, with no `src` and a
        non-empty body;
  - (b) that script's text names the route (`/rivalfunds/` and `/chart/`), and the page source holds "Chart could not load";
  - (c) `render.validate` passes the page WITH its one script;
  - (d) control (the refusal): `render.validate` passes the page as rendered, and refuses the same page with any one of these
        added before `</body>`: one more inline script, a script with `src=`, an `<img src=...>`, a `<link ...>`, a style with
        `@import`, a style with `url(`.
FAIL at base: (a), (b), (c) FAIL (no script on the page); (d) PASSES.
Not graded here: what the script DRAWS (the curve, the gaps, the markers, the hover text) needs a browser, which this check
does not have -- a JUDGMENT criterion for the CVO. This check reads the HTML and the script's text only."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SCRIPT = re.compile(r"<script\b([^>]*)>(.*?)</script\s*>", re.I | re.S)
PLANTS = {
    "a second inline script": "<script>var x = 1;</script>",
    "a script with src=": '<script src="/x.js"></script>',
    "an img with src=": '<img src="/x.png" alt="">',
    "a link": '<link rel="stylesheet" href="/x.css">',
    "an @import": '<style>@import "/x.css";</style>',
    "a url(": '<p style="background:url(/x.png)">x</p>',
}


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    html = render.render_page(c.load_fc1().fixture())
    opens = len(re.findall(r"<script\b", html, re.I))
    blocks = SCRIPT.findall(html)
    attrs, body = blocks[0] if blocks else ("", "")
    counted = render.script_count(html) if hasattr(render, "script_count") else None
    print("render.script_count:", counted, "| <script start tags:", opens, "| whole blocks:", len(blocks),
          "| first block attrs:", repr(attrs.strip()), "| body chars:", len(body.strip()))
    v.check(counted == 1 and opens == 1 and len(blocks) == 1 and "src" not in attrs.lower() and bool(body.strip()),
            "(a) the page carries exactly one inline script, with no src")

    route = "/rivalfunds/" in body and "/chart/" in body
    print("script names /rivalfunds/ and /chart/:", route, "| 'Chart could not load' in page source:", "Chart could not load" in html)
    v.check(route and "Chart could not load" in html, "(b) the script names the chart route; the could-not-load words are in the page")

    ok, why = render.validate(html)
    print("validate(page as rendered):", ok, "|", why)
    v.check(ok is True and opens == 1, "(c) the render check admits the page with its one script")

    refused = {}
    has_body = "</body>" in html
    for name, plant in PLANTS.items():
        bad_ok, bad_why = render.validate(html.replace("</body>", plant + "</body>", 1))
        refused[name] = bad_ok is False
        print(f"validate(page + {name}): {bad_ok} | {bad_why[:110]}")
    v.check(ok is True and has_body and all(refused.values()),
            f"(d) control: the page as rendered passes; each of {len(PLANTS)} planted constructs is refused")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
