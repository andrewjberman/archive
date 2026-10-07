"""RIV-au-1 AC2 (row Z-S47; ROUND_ANALYSIS.round10.md ADDENDUM 3 items 1 and 3, re-sequenced by ADDENDUM 4 @56de423b4d): the
publisher writes the audit page as a second dated object beside index.html (written, not yet linked or served), names it in the
manifest, and an over-cap render is no longer silent.

Interface (prescribed):
  - `publish_page` writes `homes.page(day, "audit.html")` (read back) beside `index.html`; a changed rerun keeps the prior
    audit.html under `revisions/<ts>/audit.html` as it keeps index.html; the manifest carries `audit_uri`, `audit_sha256`,
    `audit_bytes` and `holding_dialogs` ("on" | "off");
  - when the main page is rendered without holding dialogs (over `render.DIALOG_SOFT_CAP`), the day still publishes, the
    manifest reads `holding_dialogs: "off"`, the run result's `detail` carries `"holding_dialogs": "off"`, and the stage prints a
    line starting `FAIL: holding dialogs off` to stdout (CloudWatch).
Fixture: the round-5 offline page fixture (test_p2's: TXUE bloomberg, BASG issuer, page day 2026-09-30) on a local sink.
  - (a) a normal publish writes index.html and audit.html, both present; the manifest's audit_uri is homes.page(day,
    "audit.html"), its audit_sha256 matches the stored bytes, holding_dialogs reads "on"; index.html carries no audit block and
    no /rivalfunds/<day>/audit link yet;
  - (b) failure arm: with render.DIALOG_SOFT_CAP set to 1, a fresh publish still writes the page (status not FAILED), the
    manifest reads holding_dialogs "off", the result detail carries holding_dialogs "off", and stdout carries the FAIL line;
  - (c) control: the normal publish's status is OK or PARTIAL and its stdout carries no `FAIL: holding dialogs off` line.
FAIL at base: (a) and (b) FAIL; (c) PASSES."""
import contextlib
import hashlib
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-30"
FAIL_LINE = "FAIL: holding dialogs off"


def _publish(spec):
    from rivalfunds import publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = publish_page.handler_entry(tp2._ev(spec, day=DAY))
    return r, buf.getvalue()


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import homes, render

    spec, s, _ = c.page_fixture()
    r, out = _publish(spec)
    idx_uri, aud_uri, man_uri = homes.page(DAY, "index.html"), homes.page(DAY, "audit.html"), homes.page(DAY, "manifest.json")
    man = json.loads(s.get(man_uri)) if s.exists(man_uri) else {}
    has_aud = s.exists(aud_uri)
    aud_b = s.get(aud_uri) if has_aud else b""
    idx = s.get(idx_uri).decode("utf-8") if s.exists(idx_uri) else ""
    print("normal run:", r.get("status"), "| audit.html:", has_aud, len(aud_b), "B | manifest audit_uri:", man.get("audit_uri"),
          "| holding_dialogs:", man.get("holding_dialogs"))
    v.check(has_aud and man.get("audit_uri") == aud_uri and man.get("audit_sha256") == hashlib.sha256(aud_b).hexdigest()
            and man.get("holding_dialogs") == "on" and '<details id="audit"' not in idx and idx.count(f'href="/rivalfunds/{DAY}/audit"') == 1,
            "(a) index.html and audit.html written; the manifest names audit.html with its sha; dialogs on; index has no audit block, one audit link")

    spec2, s2, _ = c.page_fixture()
    old = render.DIALOG_SOFT_CAP
    render.DIALOG_SOFT_CAP = 1
    try:
        r2, out2 = _publish(spec2)
    finally:
        render.DIALOG_SOFT_CAP = old
    man2 = json.loads(s2.get(man_uri)) if s2.exists(man_uri) else {}
    det = r2.get("detail") if isinstance(r2.get("detail"), dict) else {}
    print("over-cap run:", r2.get("status"), "| manifest holding_dialogs:", man2.get("holding_dialogs"),
          "| detail holding_dialogs:", det.get("holding_dialogs"), "| FAIL line:", FAIL_LINE in out2)
    v.check(r2.get("status") != "FAILED" and s2.exists(idx_uri) and man2.get("holding_dialogs") == "off"
            and det.get("holding_dialogs") == "off" and any(ln.startswith(FAIL_LINE) for ln in out2.splitlines()),
            "(b) over the cap the day still publishes and says so: manifest + detail read off, stdout carries the FAIL line")

    v.check(r.get("status") in ("OK", "PARTIAL") and FAIL_LINE not in out,
            "(c) control: the normal publish is OK/PARTIAL and prints no FAIL line")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
