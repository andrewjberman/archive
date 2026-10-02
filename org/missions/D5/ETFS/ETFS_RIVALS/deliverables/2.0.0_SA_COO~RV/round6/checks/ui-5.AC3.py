"""RIV-ui-5 AC3 (RFW-U13, DESIGN.md C14 no system facts on the face): the trade log reads in plain words. Confidence and
key resolution keep their codes only in a tooltip; the bronze key and the sha256 sit behind a copy control inside the
trace, still reachable (FWD-1), not as table columns.
INTERFACE: `render._trades(f, wmax)`. A code survives as a `title` attribute; the bronze key and sha256 sit inside an
element carrying `data-trace-keys` within the trace panel (`<details class="trace">`); text inside `data-trace-keys` is
exempt from the word list.

Pure, offline fixture (`_ui.trade`): TXUE, one window, one trade of Apple Inc: confidence CLEAN, key_resolution
RESOLVED, security_key_kind security_id, flow factor 1.0, bronze key
s3://opal-data-etfs/bronze/fixture/aapl-2026-09-29.json.
  - the trade log text (closed details included, attributes and `data-trace-keys` excluded) carries none of: CLEAN,
    RESOLVED, "(security_id)", G6, canonical_shape, "flow factor";
  - the codes survive as tooltips: an element titled with CLEAN and one titled with RESOLVED;
  - no "Bronze key" or "sha256" column header; the bronze key and the sha256 are both inside a `data-trace-keys` element
    within the trace panel (as text or attribute value);
  - control: Apple Inc's trade renders with exactly one trace panel naming both report dates."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

WORDS = (r"\bCLEAN\b", r"\bRESOLVED\b", r"\(security_id\)", r"\bG6\b", r"canonical_shape", r"flow factor")
BRONZE = "s3://opal-data-etfs/bronze/fixture/aapl-2026-09-29.json"
SHA = "ab" * 32


def _blob(node):
    """Text and every attribute value under `node`."""
    return u.text(node) + " " + " ".join(val for n in node.iter() for val in n.attrs.values())


def run(v):
    c.setup_path()
    from rivalfunds import render

    t0 = u.trade("2026-09-29", "2026-09-30", bronze=BRONZE, sha=SHA)
    html = render._trades(u.fund_view("TXUE", windows=[u.window("2026-09-29", "2026-09-30", [t0])]), 0.02)
    root = u.parse(html)
    t = u.text(root, skip=lambda n: "data-trace-keys" in n.attrs)
    print("trade log text:", t[:500])
    hits = [w for w in WORDS if re.search(w, t)]
    v.check(not hits, f"no system word in the trade log (found {hits})")
    titles = [n.attrs.get("title", "") for n in root.all("title")]
    v.check(
        any("CLEAN" in x for x in titles) and any("RESOLVED" in x for x in titles),
        f"the codes survive as tooltips (titles: {titles[:6]})",
    )
    heads = [u.text(th).lower() for th in root.tags("th")]
    keys = [
        n for n in root.all("data-trace-keys") if u.inside(n, lambda x: "trace" in (x.attrs.get("class") or "").split())
    ]
    reach = " ".join(_blob(n) for n in keys)
    print("column headers:", heads, "| data-trace-keys in the trace:", len(keys))
    v.check(
        "bronze key" not in heads and "sha256" not in heads and BRONZE in reach and SHA in reach,
        "the bronze key and sha256 sit behind a copy control in the trace, not as columns",
    )
    traces = root.cls("trace")
    tt = u.text(traces[0]) if len(traces) == 1 else ""
    v.check(
        "Apple Inc" in t and len(traces) == 1 and "2026-09-29" in tt and "2026-09-30" in tt,
        "control: the trade renders with one trace panel naming both reports",
    )


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
