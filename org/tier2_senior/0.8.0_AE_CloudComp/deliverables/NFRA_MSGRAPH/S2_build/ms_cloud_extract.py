"""
NFRA_MSGRAPH S2 -- extract_ms_cloud: ingest the MS doc-cloud (SharePoint + OneDrive
structure/metadata/activity) into the SINGLE AWS Nessie/Iceberg globgrph.

ADDITIVE-ONLY (cross-domain coordination, COO 155618Z): this module is a best-effort
fold called from derive_runner.main() alongside ingest_ts_semantic_producer /
stitch_served_from -- it MUTATES the shared `graph` dict by APPENDING a new node-class
("MS_CLOUD") + MS edges. It NEVER refactors, mutates, or drops an AWS node. When
MS-disabled (default), the graph is returned byte-identical -> the AWS-only derive is
UNCHANGED (acceptance #4).

Emitted node/edge shape MATCHES the existing globgrph convention (derive_runner
commit_to_iceberg): node dict fixed keys {id, arn, type, name, layer, drift_class};
every other key auto-flows to the additive `props` JSON column (no-silent-drop guard).
MS nodes carry layer='ms', source='ms', drift_class=<ms_state>.

CATASTROPHIC-FLOOR (CTO invariant #1, S1 schema SS4): STRUCTURE / METADATA / ACTIVITY
ONLY -- NEVER content, NEVER comms. Two fail-closed layers:
  (1) source-call allowlist -- this module calls ONLY the 4 document-storage gateway
      tools (find_sharepoint_site / list_site_files / list_onedrive / search_files);
      it never imports or invokes a comms (email/chat/calendar) or content (read_file)
      surface.
  (2) assert_no_content_comms() -- an emit-time cert that RAISES (fails the derive
      closed, mirroring the UNCATEGORIZED cert) if any emitted MS node carries a
      content/comms field or a non-allowlisted (comms-class / uncategorized) node_type.
The adversarial regression in tests/test_ms_cloud_cert.py PROVES the cert
(inject -> FAIL; clean -> PASS) -- that passing+failing pair is the named
catastrophic-floor acceptance artifact (CTO binding condition 1).

S1 schema (CTO-PASS'd 20260626T155156Z):
  org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_MSGRAPH/S1_MS_GRAPH_SCHEMA.md
"""
from __future__ import annotations

import json
import os
from typing import Any, Callable, Iterable, Optional


# ---------------------------------------------------------------------------
# Schema vocabulary (closed -- mirrors S1_MS_GRAPH_SCHEMA.md SS1/SS2)
# ---------------------------------------------------------------------------

# The CLOSED MS node_type set. A node whose type is NOT in this set is the
# UNCATEGORIZED / comms-class cert-fail (no OTHER/UNKNOWN escape hatch).
ALLOWED_MS_NODE_TYPES = frozenset({
    "MS_SITE",
    "MS_LIBRARY",
    "MS_DRIVE_ONEDRIVE",
    "MS_FOLDER",
    "MS_FILE",
    "MS_USER",
    "MS_GROUP",
})

# The CLOSED MS edge_type set (S1 SS2 -- CTO-approved vocabulary adds).
ALLOWED_MS_EDGE_TYPES = frozenset({
    "CONTAINS",     # day-one
    "OWNED_BY",     # day-one (via $select add)
    "HAS_ACCESS",   # S5 (/permissions) -- defined now, populated at S5
    "SHARED_WITH",  # S5
    "MEMBER_OF",    # S5
})

# ms_state provenance axis (S1 SS3) -- the MS analog of the TF drift axis.
MS_STATE_LIVE = "LIVE"
MS_STATE_STALE = "STALE"
# MS_STATE_REMOVED is S5/delta-gated -- a full-derive cannot distinguish deleted
# from moved-out-of-scope, so day-one never asserts REMOVED (CTO ruling, SS3).

LAYER_MS = "ms"
SOURCE_MS = "ms"

# ---------------------------------------------------------------------------
# SS4 catastrophic-floor cert -- forbidden surfaces
# ---------------------------------------------------------------------------

# Content/comms field keys that must NEVER appear on an emitted MS node (case-insensitive
# substring match over every node-dict key AND every key inside the props payload).
# These are the fields a forbidden source call (read_file / email / chat) would carry.
_FORBIDDEN_FIELD_SUBSTRINGS = (
    "content",       # file body bytes/text (read_file)
    "body",          # mail/message body, bodyPreview
    "bodypreview",
    "mail_body",
    "message_text",
    "messagetext",
    "preview",       # lastMessagePreview / bodyPreview
    "transcript",
)

# URL/path fragments that resolve to a comms surface (never a /drives item).
_FORBIDDEN_URL_FRAGMENTS = (
    "/messages",
    "/me/messages",
    "/chats",
    "/sendmail",
    "/calendarview",
    "/calendar/",
    "/joinedteams",
    "/teams/",
)

# Fields whose VALUES are legitimately allowed to contain the substrings above as
# part of a normal token (e.g. a file named "Quarterly Body Review.pdf" has "body"
# in node['name']). The cert checks KEYS, not free-text values -- except web_url/path
# which are checked for the comms-surface fragments above. So a file literally named
# with a forbidden word is fine (it's a name VALUE, not a content KEY).


class MsContentCommsLeak(Exception):
    """SS4 catastrophic-floor cert failure: an emitted MS node carries a content or
    comms field, or a non-allowlisted (comms-class / uncategorized) node_type. Raised
    LOUD so the derive CLOSE leg fails closed (non-zero exit, no marker stamp) --
    mirrors the UNCATEGORIZED cert. A content/comms leak is the project's firm-sep-class
    catastrophic failure; this is the mechanism that makes 'never' structural."""


def _iter_node_field_keys(node: dict) -> Iterable[str]:
    """Every field KEY associated with a node: the top-level dict keys PLUS the keys
    inside a serialized-or-dict `props` payload (the additive column where all non-fixed
    keys land). The cert must see through props -- a content field hidden in props is
    still a leak."""
    for k in node.keys():
        if k == "props":
            continue
        yield k
    props = node.get("props")
    if isinstance(props, str) and props:
        try:
            props = json.loads(props)
        except (ValueError, TypeError):
            props = {}
    if isinstance(props, dict):
        for k in props.keys():
            yield k


def assert_no_content_comms(nodes: list[dict], edges: list[dict]) -> None:
    """SS4 emit-time cert. RAISES MsContentCommsLeak (fail-closed) on ANY of:
      (a) a node_type not in ALLOWED_MS_NODE_TYPES (comms-class / uncategorized);
      (b) a node field KEY matching a forbidden content/comms substring;
      (c) a node web_url/path resolving to a comms surface;
      (d) an edge_type not in ALLOWED_MS_EDGE_TYPES.
    Returns None on a clean structural-only emit. This is the gate-impossible leg --
    PROVEN by tests/test_ms_cloud_cert.py (the adversarial regression)."""
    for n in nodes:
        ntype = str(n.get("type", ""))
        if ntype not in ALLOWED_MS_NODE_TYPES:
            raise MsContentCommsLeak(
                f"node_type {ntype!r} is not an allowlisted MS node class "
                f"(node id={n.get('id')!r}) -- comms-class or uncategorized node = "
                f"catastrophic-floor cert FAIL")
        for key in _iter_node_field_keys(n):
            kl = key.lower()
            for bad in _FORBIDDEN_FIELD_SUBSTRINGS:
                if bad in kl:
                    raise MsContentCommsLeak(
                        f"content/comms field key {key!r} on MS node id={n.get('id')!r} "
                        f"(matched {bad!r}) -- STRUCTURE/METADATA/ACTIVITY ONLY; cert FAIL")
        # comms-surface URL/path check (value-level, for the two URL fields only)
        for urlfield in ("web_url", "path", "webUrl"):
            val = str(n.get(urlfield, "") or "")
            props = n.get("props")
            if isinstance(props, str) and props:
                try:
                    pj = json.loads(props)
                    val = val or str(pj.get(urlfield, "") or "")
                except (ValueError, TypeError):
                    pass
            vl = val.lower()
            for frag in _FORBIDDEN_URL_FRAGMENTS:
                if frag in vl:
                    raise MsContentCommsLeak(
                        f"comms-surface url/path {val!r} on MS node id={n.get('id')!r} "
                        f"(matched {frag!r}) -- comms surface off-graph; cert FAIL")
    for e in edges:
        etype = str(e.get("edge_type", ""))
        if etype not in ALLOWED_MS_EDGE_TYPES:
            raise MsContentCommsLeak(
                f"edge_type {etype!r} is not an allowlisted MS edge class "
                f"(src={e.get('source')!r}) -- uncategorized edge = cert FAIL")


# ---------------------------------------------------------------------------
# Budget / exclusion policy (S1 recon finding -- named auditable config, NOT a
# magic constant). The budget is set by EXCLUSION, not raw counts: organic
# business nodes are ~10^3; naive full recursion is ~10^4 dominated by
# non-organic subtrees (the repo mirror + a synthetic test corpus).
# ---------------------------------------------------------------------------

# OneDrive top-level subtrees excluded by DEFAULT (case-insensitive exact-name match
# at the level they appear). Each entry carries WHY (auditable).
DEFAULT_ONEDRIVE_EXCLUSIONS = {
    # name (lowercased) -> reason
    "ajb_workspace": "git-repo MIRROR -- already in the AWS graph; recursing = node-explosion + duplication",
    "aftersentdocuments": "synthetic test corpus (docs0-14: 15 identical 30-file folders) -- zero findability value",
    # S6-review (chat-attachment dumps -- comms-adjacent, low findability value). Excluded
    # day-one pending the S6 access/privacy review; structurally /drives items (allowlist-legal)
    # but semantically comms-attachment storage.
    "microsoft teams chat files": "S6-review: comms-attachment dump (Teams-shared files in OneDrive)",
    "microsoft copilot chat files": "S6-review: comms-attachment dump (Copilot-shared files)",
}

# Hard ceiling -- a defensive cap so a runaway recursion can't explode the derive.
# ~10^3 organic target; 5000 is a generous headroom that still trips on a node-explosion.
MS_NODE_CEILING = int(os.environ.get("GLOBGRPH_MS_NODE_CEILING", "5000"))


def is_excluded_onedrive_top(name: str, exclusions: Optional[dict] = None) -> bool:
    excl = DEFAULT_ONEDRIVE_EXCLUSIONS if exclusions is None else exclusions
    return name.strip().lower() in excl


# ---------------------------------------------------------------------------
# Node / edge builders (S1 schema SS1/SS2)
# ---------------------------------------------------------------------------

def _site_node(site: dict) -> dict:
    sid = site.get("id", "")
    return {
        "id": f"ms:site:{sid}",
        "arn": "",
        "type": "MS_SITE",
        "name": site.get("displayName") or site.get("name") or sid,
        "layer": LAYER_MS,
        "drift_class": MS_STATE_LIVE,
        "source": SOURCE_MS,
        "site_id": sid,
        "web_url": site.get("webUrl", ""),
        "created_dt": site.get("createdDateTime", ""),
        "last_modified_dt": site.get("lastModifiedDateTime", ""),
        "host": (site.get("siteCollection") or {}).get("hostname", ""),
    }


def _drive_node(drive_id: str, name: str, node_type: str, web_url: str = "",
                owner_upn: str = "") -> dict:
    nid = f"ms:drive:{drive_id}"
    n = {
        "id": nid,
        "arn": "",
        "type": node_type,  # MS_LIBRARY | MS_DRIVE_ONEDRIVE
        "name": name,
        "layer": LAYER_MS,
        "drift_class": MS_STATE_LIVE,
        "source": SOURCE_MS,
        "drive_id": drive_id,
        "web_url": web_url,
    }
    if owner_upn:
        n["owner_upn"] = owner_upn
    return n


def _item_node(item: dict, drive_id: str, path: str) -> dict:
    """A driveItem -> MS_FOLDER or MS_FILE. Activity field last_modified_dt
    (write-heat, day-one). last_accessed_dt is RESERVED (S5 /insights) -- not set."""
    item_id = item.get("id", "")
    is_folder = "folder" in item
    n = {
        "id": f"ms:item:{drive_id}:{item_id}",
        "arn": "",
        "type": "MS_FOLDER" if is_folder else "MS_FILE",
        "name": item.get("name", ""),
        "layer": LAYER_MS,
        "drift_class": MS_STATE_LIVE,
        "source": SOURCE_MS,
        "item_id": item_id,
        "drive_id": drive_id,
        "web_url": item.get("webUrl", ""),
        "path": path,
        "last_modified_dt": item.get("lastModifiedDateTime", ""),
        "size": item.get("size", 0),
    }
    if is_folder:
        n["child_count"] = (item.get("folder") or {}).get("childCount", 0)
    else:
        f = item.get("file") or {}
        n["file_type"] = (f.get("fileExtension")
                          or _ext(item.get("name", "")))
        n["mime_type"] = f.get("mimeType", "")
    # OWNED_BY source (S1: createdBy/lastModifiedBy via $select add). Stored as
    # owner_upn for the OWNED_BY edge; absent if the gateway $select didn't carry it.
    owner = _owner_upn(item)
    if owner:
        n["owner_upn"] = owner
    return n


def _user_node(upn: str, display_name: str = "") -> dict:
    return {
        "id": f"ms:user:{upn}",
        "arn": "",
        "type": "MS_USER",
        "name": display_name or upn,
        "layer": LAYER_MS,
        "drift_class": MS_STATE_LIVE,
        "source": SOURCE_MS,
        "upn": upn,
    }


def _edge(src_id: str, dst_id: str, edge_type: str) -> dict:
    return {"source": src_id, "target": dst_id, "edge_type": edge_type, "layer": LAYER_MS}


def _ext(name: str) -> str:
    i = name.rfind(".")
    return name[i:] if i >= 0 else ""


def _owner_upn(item: dict) -> str:
    # createdBy/lastModifiedBy.user.email|userPrincipalName (S2 $select add). Defensive:
    # the gateway may not carry it yet -> empty (OWNED_BY simply not emitted for that item).
    for k in ("lastModifiedBy", "createdBy"):
        u = ((item.get(k) or {}).get("user")) or {}
        upn = u.get("email") or u.get("userPrincipalName") or ""
        if upn:
            return upn
    return ""


# ---------------------------------------------------------------------------
# Gateway caller abstraction (injectable -- real impl calls the m365 gateway;
# tests inject a fake so the cert + merge logic is provable OFFLINE)
# ---------------------------------------------------------------------------

class MsGatewayCaller:
    """Wraps the FOUR allowlisted document-storage gateway tools. The real nightly
    constructs one bound to Andrew's delegated Graph token (see the headless-auth
    note in the S2 RAVC -- the token source is the gating implementable-change
    decision the CTO arch-gate owns). Tests subclass / duck-type this with fixtures.

    DELIBERATELY exposes ONLY the 4 allowlisted methods -- there is no email/chat/
    calendar/read_file method on this surface (the allowlist is structural, not a
    runtime check that could be bypassed)."""

    def find_sharepoint_site(self, name: str) -> dict:  # GET /sites?search=
        raise NotImplementedError

    def list_site_files(self, site_id: str, folder_path: Optional[str] = None) -> dict:
        raise NotImplementedError

    def list_onedrive(self, folder_path: Optional[str] = None) -> dict:
        raise NotImplementedError

    def search_files(self, query: str) -> dict:
        raise NotImplementedError


# Site search probes -- the gateway find_sharepoint_site is a NAME search, not a full
# tenant enum (S1 recon caveat). The org tenant is single ("opalinvest"); a small probe
# set covers the surfaced sites. Carried as config (auditable), with the multi-library /
# full-enum gap noted for S5 (CTO binding condition 2).
DEFAULT_SITE_PROBES = ("opal", "49", "financial", "trade", "consulting")

# MULTI-LIBRARY FLAG (CTO binding condition 2 -- deferred to S5, NOT lost): the gateway
# list_site_files reaches only a site's DEFAULT drive. Multi-library sites are
# under-modeled until S5 enumerates /sites/{id}/drives. Tracked here so it is not
# silently treated as "the estate".
MULTI_LIBRARY_GAP = ("S5: enumerate /sites/{id}/drives -- day-one reaches only the "
                     "default doc library per site (S1 recon finding)")


def _crawl_drive(caller_fn: Callable[[Optional[str]], dict], parent_id: str,
                 drive_id: str, base_path: str, nodes: list, edges: list,
                 counter: list, exclusions: Optional[dict], depth: int,
                 max_depth: int, owners: dict, is_onedrive: bool) -> None:
    """Recurse a drive (SP library or OneDrive) emitting MS_FOLDER/MS_FILE nodes +
    CONTAINS edges (parent->child) + OWNED_BY edges. Honors the exclusion policy at
    the OneDrive top level and the node ceiling. caller_fn(folder_path)->listing."""
    if depth > max_depth or counter[0] >= MS_NODE_CEILING:
        return
    folder_path = base_path or None
    try:
        listing = caller_fn(folder_path)
    except Exception as e:  # noqa: BLE001 -- one bad folder must not kill the derive
        print(f"WARN: MS_LIST_FAIL path={base_path!r} err={type(e).__name__}: {e}")
        return
    for item in (listing.get("value") or []):
        name = item.get("name", "")
        # exclusion policy at the OneDrive top level (depth 0 of OneDrive)
        if is_onedrive and depth == 0 and is_excluded_onedrive_top(name, exclusions):
            print(f"INFO: MS_EXCLUDE onedrive-top {name!r} "
                  f"({(exclusions or DEFAULT_ONEDRIVE_EXCLUSIONS).get(name.strip().lower(), '')})")
            continue
        if counter[0] >= MS_NODE_CEILING:
            print(f"WARN: MS_NODE_CEILING {MS_NODE_CEILING} reached -- pausing recursion "
                  f"(node-explosion guard; raise GLOBGRPH_MS_NODE_CEILING if legitimate)")
            return
        child_path = f"{base_path}/{name}".strip("/") if base_path else name
        node = _item_node(item, drive_id, child_path)
        nodes.append(node)
        counter[0] += 1
        edges.append(_edge(parent_id, node["id"], "CONTAINS"))
        owner = node.get("owner_upn")
        if owner:
            owners.setdefault(owner, owner)
            edges.append(_edge(node["id"], f"ms:user:{owner}", "OWNED_BY"))
        if "folder" in item and (item.get("folder") or {}).get("childCount", 0):
            _crawl_drive(caller_fn, node["id"], drive_id, child_path, nodes, edges,
                         counter, exclusions, depth + 1, max_depth, owners, is_onedrive)


def build_ms_graph(caller: MsGatewayCaller, *, site_probes: Iterable[str] = DEFAULT_SITE_PROBES,
                   exclusions: Optional[dict] = None, max_depth: int = 12) -> tuple[list, list]:
    """Enumerate SP + OneDrive via the 4 allowlisted tools -> (nodes, edges) per the S1
    schema. Pure builder: does NOT touch the AWS graph. The caller is the only IO surface.
    Returns (ms_nodes, ms_edges); the SS4 cert is applied by extract_ms_cloud BEFORE merge."""
    nodes: list[dict] = []
    edges: list[dict] = []
    owners: dict = {}
    counter = [0]

    # --- SharePoint: sites -> default library -> tree ---
    seen_sites: set = set()
    for probe in site_probes:
        try:
            resp = caller.find_sharepoint_site(probe)
        except Exception as e:  # noqa: BLE001
            print(f"WARN: MS_SITE_SEARCH_FAIL probe={probe!r} err={type(e).__name__}: {e}")
            continue
        for site in (resp.get("value") or []):
            sid = site.get("id", "")
            if not sid or sid in seen_sites:
                continue
            seen_sites.add(sid)
            snode = _site_node(site)
            nodes.append(snode)
            counter[0] += 1
            # default document library (the site drive). list_site_files reaches the
            # DEFAULT drive only (MULTI_LIBRARY_GAP -- S5).
            lib_id = f"{sid}::default"
            lnode = _drive_node(lib_id, "Documents (default)", "MS_LIBRARY",
                                web_url=site.get("webUrl", ""))
            nodes.append(lnode)
            counter[0] += 1
            edges.append(_edge(snode["id"], lnode["id"], "CONTAINS"))
            _crawl_drive(lambda fp, _sid=sid: caller.list_site_files(_sid, fp),
                         lnode["id"], lib_id, "", nodes, edges, counter, exclusions,
                         0, max_depth, owners, is_onedrive=False)

    # --- OneDrive: root -> tree (with the exclusion policy at the top level) ---
    od_drive_id = "onedrive::me"
    od_node = _drive_node(od_drive_id, "OneDrive", "MS_DRIVE_ONEDRIVE")
    nodes.append(od_node)
    counter[0] += 1
    _crawl_drive(lambda fp: caller.list_onedrive(fp), od_node["id"], od_drive_id, "",
                 nodes, edges, counter, exclusions, 0, max_depth, owners, is_onedrive=True)

    # --- owner user nodes (OWNED_BY targets; typed-principal admission, mirrors AWS) ---
    for upn in owners:
        nodes.append(_user_node(upn))

    return nodes, edges


# ---------------------------------------------------------------------------
# The additive fold (called from derive_runner.main, best-effort, like
# ingest_ts_semantic_producer / stitch_served_from)
# ---------------------------------------------------------------------------

def ms_enabled() -> bool:
    """Day-one rollout gate. Default OFF so the AWS-only derive is provably UNCHANGED
    until the MS extract is arch-gated + the headless-auth token source is wired. Flip
    via the task-def env GLOBGRPH_MS_ENABLED=1 (a deliberate enable, post arch-gate)."""
    return os.environ.get("GLOBGRPH_MS_ENABLED", "0") == "1"


def extract_ms_cloud(graph: dict, *, caller: Optional[MsGatewayCaller] = None,
                     exclusions: Optional[dict] = None) -> dict:
    """ADDITIVE fold. When MS-disabled: returns `graph` UNCHANGED (AWS-only derive
    untouched). When enabled: enumerates the MS doc-cloud, runs the SS4 cert (fail-closed),
    and APPENDS the MS nodes as classes_data['MS_CLOUD'] + MS edges to graph['edges'].

    The SS4 cert runs BEFORE the merge: a content/comms leak RAISES and the derive fails
    closed (the CLOSE leg), so a leaking MS subgraph never reaches the Iceberg commit."""
    if not ms_enabled():
        print("INFO: MS_EXTRACT_DISABLED (GLOBGRPH_MS_ENABLED!=1) -- AWS-only derive unchanged")
        return graph
    if caller is None:
        # The real nightly builds a caller bound to Andrew's delegated token. If none is
        # wired yet, do NOT guess -- skip (best-effort, never fail the AWS derive) and log
        # LOUD so the missing-auth state is visible (the headless-auth gating decision).
        print("ERROR: MS_EXTRACT_NO_CALLER -- MS enabled but no gateway caller wired "
              "(headless delegated-token source unresolved; see S2 RAVC). MS skipped this run.")
        return graph

    print("INFO: MS_EXTRACT_START")
    ms_nodes, ms_edges = build_ms_graph(caller, exclusions=exclusions)

    # SS4 catastrophic-floor cert -- fail closed BEFORE merge (CTO invariant #1).
    assert_no_content_comms(ms_nodes, ms_edges)

    # Merge: APPEND-only. New node-class bucket + extend edges. AWS classes untouched.
    graph.setdefault("classes_data", {})["MS_CLOUD"] = {"nodes": ms_nodes}
    graph.setdefault("edges", []).extend(ms_edges)
    print(f"OK: MS_EXTRACT_COMPLETE nodes={len(ms_nodes)} edges={len(ms_edges)} "
          f"(merged into the single graph as classes_data['MS_CLOUD'])")
    return graph
