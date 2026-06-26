"""
NFRA_MSGRAPH S2 -- THE CATASTROPHIC-FLOOR ACCEPTANCE ARTIFACT (CTO binding condition 1).

This is the named adversarial regression that PROVES the SS4 content/comms cert is
gate-impossible, not merely asserted. The proof is the passing+failing PAIR:
  - inject a synthetic COMMS-class node   -> the cert FAILS the derive   (test_comms_node_fails)
  - inject a synthetic CONTENT field       -> the cert FAILS the derive   (test_content_field_fails)
  - inject a comms-surface URL             -> the cert FAILS the derive   (test_comms_url_fails)
  - inject an uncategorized edge_type      -> the cert FAILS the derive   (test_bad_edge_fails)
  - a clean STRUCTURAL-only node           -> the cert PASSES             (test_clean_node_passes)

Plus the ADDITIVE-ONLY cross-domain proof (acceptance #4):
  - MS-disabled  -> the AWS graph is byte-identical (UNCHANGED)           (test_aws_unchanged_when_disabled)
  - MS-enabled   -> AWS nodes identical + MS nodes added (strict SUPERSET) (test_superset_when_enabled)
  - the exclusion policy drops the repo-mirror + synthetic corpus          (test_exclusion_policy)

Run: python -m pytest infra/aws/globgrph/tests/test_ms_cloud_cert.py -v
 or: python infra/aws/globgrph/tests/test_ms_cloud_cert.py   (stdlib fallback runner, no pytest dep)
"""
from __future__ import annotations

import copy
import os
import sys
from pathlib import Path

# import the module under test (sibling dir)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ms_cloud_extract as mx  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures: a fake gateway caller returning canned listings (OFFLINE -- no live
# gateway, no Andrew token). The shapes mirror the real Graph responses observed
# in S1 recon.
# ---------------------------------------------------------------------------

class FakeCaller(mx.MsGatewayCaller):
    def find_sharepoint_site(self, name):
        if name != "opal":
            return {"value": []}
        return {"value": [{
            "id": "opalinvest.sharepoint.com,site-guid,web-guid",
            "displayName": "Opal CIO Office for 49 Financial",
            "name": "OpalCIOOfficefor49Financial",
            "webUrl": "https://opalinvest.sharepoint.com/sites/OpalCIOOfficefor49Financial",
            "createdDateTime": "2024-03-27T10:33:35Z",
            "lastModifiedDateTime": "2024-03-17T05:26:37Z",
            "siteCollection": {"hostname": "opalinvest.sharepoint.com"},
        }]}

    def list_site_files(self, site_id, folder_path=None):
        if folder_path is None:
            return {"value": [{
                "id": "sp-file-1",
                "name": "2024Q2 Investment Packet.pptx",
                "webUrl": "https://opalinvest.sharepoint.com/.../2024Q2.pptx",
                "lastModifiedDateTime": "2024-04-07T02:25:27Z",
                "size": 3411421,
                "file": {"fileExtension": ".pptx", "mimeType": "application/vnd.ms-powerpoint"},
                "lastModifiedBy": {"user": {"email": "andrew@opalinvest.com",
                                            "displayName": "Andrew Berman"}},
            }]}
        return {"value": []}

    def list_onedrive(self, folder_path=None):
        if folder_path is None:
            return {"value": [
                {"id": "od-ws", "name": "ajb_workspace", "folder": {"childCount": 34},
                 "size": 11018128124, "lastModifiedDateTime": "2025-11-12T17:35:23Z"},
                {"id": "od-syn", "name": "afterSentDocuments", "folder": {"childCount": 15},
                 "size": 10666125, "lastModifiedDateTime": "2025-10-24T13:38:55Z"},
                {"id": "od-real", "name": "202511 Model Portfolio Exposure",
                 "folder": {"childCount": 1}, "size": 5040062,
                 "lastModifiedDateTime": "2025-11-04T20:19:36Z"},
            ]}
        if folder_path == "202511 Model Portfolio Exposure":
            return {"value": [{
                "id": "od-real-f1", "name": "exposure.xlsx",
                "webUrl": "https://opalinvest-my.sharepoint.com/.../exposure.xlsx",
                "lastModifiedDateTime": "2025-11-04T20:19:36Z", "size": 100000,
                "file": {"fileExtension": ".xlsx", "mimeType": "application/vnd.ms-excel"},
            }]}
        return {"value": []}

    def search_files(self, query):
        return {"value": []}


def _clean_ms_graph():
    return mx.build_ms_graph(FakeCaller())


# ---------------------------------------------------------------------------
# SS4 cert -- the catastrophic-floor proof (CTO binding condition 1)
# ---------------------------------------------------------------------------

def test_clean_node_passes():
    nodes, edges = _clean_ms_graph()
    # must not raise
    mx.assert_no_content_comms(nodes, edges)
    # and it must actually have produced structural nodes (a vacuous pass is not a pass)
    assert any(n["type"] == "MS_SITE" for n in nodes)
    assert any(n["type"] == "MS_FILE" for n in nodes)
    assert any(e["edge_type"] == "CONTAINS" for e in edges)


def test_comms_node_fails():
    nodes, edges = _clean_ms_graph()
    nodes.append({"id": "ms:chat:1", "type": "MS_CHAT_MESSAGE", "name": "leaked chat",
                  "layer": "ms", "source": "ms"})
    try:
        mx.assert_no_content_comms(nodes, edges)
    except mx.MsContentCommsLeak:
        return  # EXPECTED -- the cert failed the derive on a comms-class node
    raise AssertionError("CERT DID NOT FAIL on a comms-class node -- catastrophic-floor BREACH")


def test_content_field_fails():
    nodes, edges = _clean_ms_graph()
    # a node typed correctly (MS_FILE) but carrying a forbidden CONTENT field
    nodes.append({"id": "ms:item:d:leak", "type": "MS_FILE", "name": "ok.pdf",
                  "layer": "ms", "source": "ms",
                  "content": "the actual file body bytes -- MUST never be graphed"})
    try:
        mx.assert_no_content_comms(nodes, edges)
    except mx.MsContentCommsLeak:
        return  # EXPECTED
    raise AssertionError("CERT DID NOT FAIL on a content-bearing field -- catastrophic-floor BREACH")


def test_content_field_hidden_in_props_fails():
    nodes, edges = _clean_ms_graph()
    # the leak hidden inside the props payload (the additive column) -- the cert must see through it
    nodes.append({"id": "ms:item:d:leak2", "type": "MS_FILE", "name": "ok.pdf",
                  "layer": "ms", "source": "ms",
                  "props": '{"bodyPreview": "first 400 chars of a message body"}'})
    try:
        mx.assert_no_content_comms(nodes, edges)
    except mx.MsContentCommsLeak:
        return  # EXPECTED -- props-hidden leak still caught
    raise AssertionError("CERT DID NOT FAIL on a props-hidden content field -- BREACH")


def test_comms_url_fails():
    nodes, edges = _clean_ms_graph()
    nodes.append({"id": "ms:item:d:leak3", "type": "MS_FILE", "name": "ok.pdf",
                  "layer": "ms", "source": "ms",
                  "web_url": "https://graph.microsoft.com/v1.0/me/messages/AAMk"})
    try:
        mx.assert_no_content_comms(nodes, edges)
    except mx.MsContentCommsLeak:
        return  # EXPECTED
    raise AssertionError("CERT DID NOT FAIL on a comms-surface URL -- BREACH")


def test_bad_edge_fails():
    nodes, edges = _clean_ms_graph()
    edges.append({"source": "ms:item:a", "target": "ms:item:b", "edge_type": "MENTIONS_IN_CHAT",
                  "layer": "ms"})
    try:
        mx.assert_no_content_comms(nodes, edges)
    except mx.MsContentCommsLeak:
        return  # EXPECTED -- uncategorized edge type
    raise AssertionError("CERT DID NOT FAIL on an uncategorized edge_type -- BREACH")


def test_filename_with_forbidden_word_in_value_passes():
    """A file legitimately NAMED 'Body Review.pdf' has 'body' in the name VALUE, not a
    content KEY -- it must PASS (the cert checks field KEYS, not free-text values). Guards
    against an over-eager cert that would block legitimate structural metadata."""
    nodes, edges = _clean_ms_graph()
    nodes.append({"id": "ms:item:d:ok", "type": "MS_FILE", "name": "Annual Body Review.pdf",
                  "layer": "ms", "source": "ms", "file_type": ".pdf"})
    mx.assert_no_content_comms(nodes, edges)  # must not raise


# ---------------------------------------------------------------------------
# ADDITIVE-ONLY cross-domain proof (acceptance #4)
# ---------------------------------------------------------------------------

def _fake_aws_graph():
    return {
        "classes_data": {
            "S3_BUCKET": {"nodes": [
                {"id": "arn:aws:s3:::opal-x", "arn": "arn:aws:s3:::opal-x",
                 "type": "S3_BUCKET", "name": "opal-x", "layer": "aws", "drift_class": "DECLARED"},
            ]},
        },
        "edges": [{"source": "arn:aws:s3:::opal-x", "target": "arn:aws:iam::1:role/r",
                   "edge_type": "HAS_POLICY"}],
    }


def test_aws_unchanged_when_disabled():
    os.environ.pop("GLOBGRPH_MS_ENABLED", None)  # disabled (default)
    g = _fake_aws_graph()
    before = copy.deepcopy(g)
    mx.extract_ms_cloud(g, caller=FakeCaller())
    assert g == before, "AWS graph MUTATED when MS-disabled -- additive-only VIOLATED"


def test_superset_when_enabled():
    os.environ["GLOBGRPH_MS_ENABLED"] = "1"
    try:
        g = _fake_aws_graph()
        aws_nodes_before = copy.deepcopy(g["classes_data"]["S3_BUCKET"]["nodes"])
        aws_edges_before = copy.deepcopy(g["edges"])
        mx.extract_ms_cloud(g, caller=FakeCaller())
        # AWS nodes/edges IDENTICAL (never mutated/dropped)
        assert g["classes_data"]["S3_BUCKET"]["nodes"] == aws_nodes_before, "AWS node mutated"
        assert all(e in g["edges"] for e in aws_edges_before), "AWS edge dropped"
        # MS nodes ADDED (strict superset)
        assert "MS_CLOUD" in g["classes_data"], "MS class not added"
        ms_nodes = g["classes_data"]["MS_CLOUD"]["nodes"]
        assert any(n["type"] == "MS_SITE" for n in ms_nodes)
        assert any(n["layer"] == "ms" and n["source"] == "ms" for n in ms_nodes)
        assert any(e["edge_type"] == "CONTAINS" and e["layer"] == "ms" for e in g["edges"])
    finally:
        os.environ.pop("GLOBGRPH_MS_ENABLED", None)


def test_exclusion_policy():
    nodes, edges = _clean_ms_graph()
    names = {n.get("name") for n in nodes}
    # the repo-mirror + synthetic corpus must be EXCLUDED (never appear as nodes)
    assert "ajb_workspace" not in names, "repo-mirror NOT excluded -- node-explosion risk"
    assert "afterSentDocuments" not in names, "synthetic corpus NOT excluded"
    # the organic folder IS included + recursed
    assert "202511 Model Portfolio Exposure" in names
    assert "exposure.xlsx" in names


def test_owned_by_edge_emitted():
    nodes, edges = _clean_ms_graph()
    # the SP file fixture carries lastModifiedBy -> an OWNED_BY edge + an MS_USER node
    assert any(e["edge_type"] == "OWNED_BY" for e in edges), "OWNED_BY not emitted"
    assert any(n["type"] == "MS_USER" for n in nodes), "MS_USER (owner) node not admitted"


# ---------------------------------------------------------------------------
# stdlib fallback runner (no pytest dependency required)
# ---------------------------------------------------------------------------

def _run_all():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL: {t.__name__} -- {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{'OK' if failed == 0 else 'ERROR'}: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(_run_all())
