"""ETFS_RIVALS round 12 -- the issuer's one real run (2.0.0_SA_COO~RV): render a published day from the LIVE inputs without
writing S3, and measure the served-page outcome ADDENDUM 4 step 2 names.

    python real_run.py <worktree root> <YYYY-MM-DD> <out dir>

Reads live S3 through a read-only layer; every write (the page, the manifest, the batch marker) lands in <out dir>. The A1
producers are switched off (publish_page.PRODUCE_ENV=0), so the page reads the A1 objects already published for the day and no
producer runs; publish-page makes no AI call by construction. Prints, for index.html (and audit.html when written):
bytes, headroom under render.DIALOG_SOFT_CAP, holding-dialogs state, data-sec buttons, dialogs, dead buttons (a popovertarget
with no matching data-sec-dialog in the same document), and the run status. Writes <out dir>/real_run_<day>.json."""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY = sys.argv[2]
OUT = pathlib.Path(sys.argv[3]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))

from rivalfunds import homes, publish_page, render, sinks  # noqa: E402


class OverlaySink:
    """Reads the local layer first, then live S3; writes go to the local layer only."""
    kind = "overlay"

    def __init__(self, local_root: pathlib.Path):
        self.live, self.local = sinks.S3Sink(), sinks.LocalSink(str(local_root))

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.live.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.live.exists(uri)

    def list(self, prefix_uri):
        return sorted(set(self.live.list(prefix_uri)) | set(self.local.list(prefix_uri)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


def measure(html: str) -> dict:
    ids = set(re.findall(r'\bid="?([^"\s>]+)"?', html))
    dialog_ids = {m.group(1): m.group(2) for m in re.finditer(r'<div id=([^\s>]+) popover class=rf-modal data-sec-dialog="([^"]*)"', html)}
    buttons = re.findall(r'<button[^>]*\bdata-sec="([^"]*)"[^>]*>', html)
    targets = re.findall(r'<button[^>]*\bdata-sec="[^"]*"[^>]*\bpopovertarget="?([^"\s>]+)', html) + \
        re.findall(r'<button[^>]*\bpopovertarget="?([^"\s>]+)"?[^>]*\bdata-sec="', html)
    dead = [t for t in targets if t not in dialog_ids and t not in ids]
    b = len(html.encode("utf-8"))
    return {"bytes": b, "headroom_pct": round(100.0 * (render.DIALOG_SOFT_CAP - b) / render.DIALOG_SOFT_CAP, 1),
            "holding_dialogs_off": 'data-holding-dialogs="off"' in html, "data_sec_buttons": len(buttons),
            "dialogs": len(dialog_ids), "dead_buttons": len(dead), "audit_block": '<details id="audit"' in html,
            "audit_link": f"/rivalfunds/{DAY}/audit" in html}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    os.environ[publish_page.PRODUCE_ENV] = "0"
    s = OverlaySink(OUT / "layer")
    batch = "r12-real-run-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    r = publish_page.handler_entry({"date": DAY, "mode": "replay", "batch_id": batch, "sink": s})
    rec = {"day": DAY, "batch_id": batch, "status": r.get("status"), "detail": r.get("detail"),
           "dialog_soft_cap": render.DIALOG_SOFT_CAP, "code_root": str(ROOT)}
    unchanged = isinstance(r.get("detail"), dict) and r["detail"].get("unchanged")
    for name in ("index.html", "audit.html"):
        uri = homes.page(DAY, name)
        if s.local.exists(uri):
            rec[name] = dict(measure(s.local.get(uri).decode("utf-8")), source="rendered (local layer)")
        elif unchanged and name == "index.html":  # the render equals the served bytes: nothing was written, so measure those
            rec[name] = dict(measure(s.live.get(uri).decode("utf-8")), source="rendered == served (unchanged)")
    man = homes.page(DAY, "manifest.json")
    if s.local.exists(man):
        m = json.loads(s.local.get(man))
        rec["manifest"] = {k: m.get(k) for k in ("holding_dialogs", "audit_uri", "audit_bytes", "index_bytes", "funds_updated",
                                                 "funds_total")}
    (OUT / f"real_run_{DAY}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
    print(json.dumps(rec, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
