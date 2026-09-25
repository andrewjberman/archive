# AMGT_RESAPP round 40, ro-1: 0.9.0_WK_AMGT_RESAPP~143's handler_rich_to_file.py plus ONE stub. Row Z-S271's
# fix made _print_pack pass the header's description into build_rich_text, a FIFTH reader; the original stubs four.
# Unstubbed it reads the empty hermetic drafting root. The stub returns the fixture's own overlay.description.
"""AMGT_RESAPP AMGT-rm-4 AC2 -- serve BA_US_Equity's rich-text export through the adapter's
OWN dispatch (`scoped_amgt.handler`), over the harness's own captured bytes, and write the
served body to disk so `exportCompare.harness.cjs --rich` can grade it against the ACTUAL
page render.

PATCHED (named here, nothing hidden):
  - `AMGT_POOL_ROOT` / `AMGT_DRAFTING_ROOT` -- pointed at fresh empty temp directories, the
    SAME hermetic contract `lib/research/api/tests/conftest.py`'s `empty_pool_roots` fixture
    gives every pytest run in this package (this script is not a pytest run, so it sets the
    same two variables itself).
  - `scoped_amgt.resolve_identity` -- module-level reassignment to a fixed identity block for
    BA_US_Equity, so the request never touches the crosswalk.
  - `scoped_amgt.read_model_block` -- module-level reassignment to the SAME construction
    `lib/research/print/tests/test_build_rich_text.py` uses (the harness fixture's own
    header + fiscal-year figures, under the display form "BA US Equity"), never the pool.
  - `scoped_amgt.read_thesis_bundle`, `scoped_amgt.read_peer_set`, `scoped_amgt.read_posture`
    -- module-level reassignment to the harness's OWN captured bundle
    (portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json), the SAME
    file `exportCompare.harness.cjs` and `tabs.harness.cjs` read on the node side, so the
    python-served document and the react-rendered page are measured against ONE landed
    record.

Everything else (`scoped_amgt.handler`'s route dispatch, `_print_pack`'s `fmt` branch, the
identity-agreement refusal, `render_pack.build_rich_text`) runs UNPATCHED.

Run (from the repo root):
  PYTHONPATH=<repo root> python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/
    0.9.0_WK_AMGT_RESAPP~143/handler_rich_to_file.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path.cwd()
LEGACY_MODEL_BLOCK_DIR = (
    REPO_ROOT
    / "org"
    / "missions"
    / "D5"
    / "AMGT"
    / "AMGT_RESAPP"
    / "deliverables"
    / "0.9.0_WK_AMGT_RESAPP~1"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "portal"
    / "src"
    / "pages"
    / "SecurityAnalysis"
    / "__harness__"
    / "tabsFixture.BA_US_Equity.json"
)
OUT_DIR = Path(__file__).resolve().parent / "served"

SECURITY_KEY = "BA_US_Equity"
DISPLAY_FORM = "BA US Equity"


def main() -> int:
    pool_root = Path(tempfile.mkdtemp(prefix="amgt_rm4_pool_"))
    drafting_root = Path(tempfile.mkdtemp(prefix="amgt_rm4_drafting_"))

    from lib.research.api import scoped_amgt as sa

    os.environ[sa.ENV_POOL_ROOT] = str(pool_root)
    os.environ[sa.ENV_DRAFTING_ROOT] = str(drafting_root)

    bundle = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    thesis = bundle["thesis"]
    peers = bundle["peers"]
    posture = thesis.get("posture")
    model_block = {
        "security": DISPLAY_FORM,
        "security_key": SECURITY_KEY,
        "figures": thesis["header_figures"] + thesis["fiscal_year_figures"],
    }

    def fake_resolve_identity(requested):
        return {
            "security_key": SECURITY_KEY,
            "requested": requested,
            "identity_status": "RESOLVED",
        }

    def fake_read_model_block(security_key):
        return model_block

    def fake_read_thesis_bundle(security_key, identity=None):
        return thesis

    def fake_read_peer_set(security_key):
        return peers

    def fake_read_posture(security_key, identity=None):
        return posture

    sa.resolve_identity = fake_resolve_identity
    sa.read_model_block = fake_read_model_block
    sa.read_thesis_bundle = fake_read_thesis_bundle
    sa.read_peer_set = fake_read_peer_set
    sa.read_posture = fake_read_posture
    sa.read_description = lambda security_key, identity=None, model_block=None, drafting=None: bundle["overlay"]["description"]

    event = {
        "rawPath": "/api/scoped/amgt/security/{0}/print".format(SECURITY_KEY),
        "httpMethod": "GET",
        "headers": {"X-Firm-Id": "opal-capital"},
        "queryStringParameters": {"format": "rich"},
    }
    response = sa.handler(event)

    if response.get("statusCode") != 200:
        print(
            "ERROR: handler returned statusCode={0} body={1}".format(
                response.get("statusCode"), response.get("body")
            )
        )
        return 1

    body = response["body"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "{0}.md".format(SECURITY_KEY)
    out_path.write_text(body, encoding="utf-8")

    print(
        "OK: wrote {0} bytes={1} Content-Type={2!r} isBase64Encoded={3}".format(
            out_path,
            out_path.stat().st_size,
            response["headers"]["Content-Type"],
            response["isBase64Encoded"],
        )
    )
    shutil.rmtree(pool_root, ignore_errors=True)
    shutil.rmtree(drafting_root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
