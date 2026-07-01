"""SCTY_MCPGUARD S0 -- the destructive_ops registry (G2 classification gate input).

STAGED IMPLEMENTABLE-CHANGE (build-lane 0.5.0_AE_OpalETL). The S0 output the CTO
design-gated in Part-A PASS (171857Z): the classification every guard (G1/G3/G4/G6)
consumes. Destined for `infra/aws/ec2/m365-mcp-gateway/app/` once impl-gated +
0.8.0 confirms _run() (tools.py:47) is the SOLE dispatch path (the S0-close condition).

Grounded 1:1 against tools.py (Read 2026-07-01): 25 @mcp.tool() = 20 read (SAFE) + 5
mutating. NO delete/overwrite/move/mailbox-rule tool exists today -- the mutating
surface is send-class only. The latent delete capability is in the Files.ReadWrite.All
delegated token (tools.py:282), NOT a tool -> handled by B2 (read-only-scope) + the
FAIL-CLOSED default here (a FUTURE delete tool is denied-until-classified).

FAIL-CLOSED AXIOM (CTO arch-gate): a tool NOT in this registry is treated DESTRUCTIVE
(unknown -> deny/guard), so a newly-added write tool cannot slip past G2 unclassified.
"""
from __future__ import annotations

import enum


class OpClass(enum.Enum):
    SAFE = "safe"                    # read-only; bypasses the guard (zero latency on the read path)
    WRITE_REVERSIBLE = "write_reversible"    # a write with a native undo (e.g. a draft)
    IRREVERSIBLE_SEND = "irreversible_send"  # a send that cannot be recalled -> G3 always confirms
    # (future) DELETE / OVERWRITE / MOVE classes activate when such a tool is added.


# The 20 read-only tools (tools.py) -- explicitly SAFE, bypass the guard.
SAFE_TOOLS = frozenset({
    "whoami", "list_recent_email", "search_email", "read_email", "list_calendar",
    "list_onedrive", "search_files", "read_file", "find_sharepoint_site", "list_site_files",
    "read_site_file", "read_site_workbook", "read_workbook", "search_site_files", "get_item",
    "get_site_item", "list_site_drives", "read_document", "list_chats", "read_chat_messages",
    "list_teams", "list_channels", "read_channel_messages", "poll_addressed_teams_messages",
})

# The 5 mutating tools = the ENTIRE current destructive surface (tools.py, line-cited).
# tag = {class, reversible, irreversible, native_undo, blast_dimensions}
DESTRUCTIVE_OPS = {
    "create_draft": {                       # tools.py:112 POST /me/messages
        "class": OpClass.WRITE_REVERSIBLE,
        "reversible": True, "irreversible": False,
        "native_undo": "delete the draft (it is not sent)",
        "blast_dimensions": ["drafts:1"],
    },
    "send_email": {                          # tools.py:126 POST /me/sendMail
        "class": OpClass.IRREVERSIBLE_SEND,
        "reversible": False, "irreversible": True,
        "native_undo": None,
        "blast_dimensions": ["recipients", "external_domains"],
    },
    "reply_email": {                         # tools.py:143 POST /me/messages/{id}/reply
        "class": OpClass.IRREVERSIBLE_SEND,
        "reversible": False, "irreversible": True,
        "native_undo": None,
        "blast_dimensions": ["recipients"],
    },
    "send_chat_message": {                   # tools.py:392 POST /chats/{id}/messages
        "class": OpClass.IRREVERSIBLE_SEND,
        "reversible": False, "irreversible": True,
        "native_undo": None,
        "blast_dimensions": ["chats:1"],
    },
    "send_channel_message": {                # tools.py:430 POST /teams/{id}/channels/{id}/messages
        "class": OpClass.IRREVERSIBLE_SEND,
        "reversible": False, "irreversible": True,
        "native_undo": None,
        "blast_dimensions": ["channel_visibility"],
    },
}

# Tag returned for an UNCLASSIFIED tool (fail-closed): treated destructive + irreversible
# until a human classifies it, and denied/guarded rather than passed through.
_UNKNOWN_TAG = {
    "class": OpClass.IRREVERSIBLE_SEND,   # most-restrictive assumption
    "reversible": False, "irreversible": True,
    "native_undo": None,
    "blast_dimensions": ["UNKNOWN"],
    "unclassified": True,
}


def classify(tool: str) -> dict:
    """G2 classification. Returns {class, reversible, irreversible, ...}.
    SAFE tools -> {class: SAFE} (guard bypass). Known mutating -> its tag.
    UNKNOWN tool -> fail-closed destructive tag (denied-until-classified)."""
    if tool in SAFE_TOOLS:
        return {"class": OpClass.SAFE, "reversible": True, "irreversible": False,
                "native_undo": None, "blast_dimensions": []}
    tag = DESTRUCTIVE_OPS.get(tool)
    if tag is not None:
        return dict(tag)
    return dict(_UNKNOWN_TAG)   # fail-closed


def is_guarded(tool: str) -> bool:
    """True if the call must route through the guard (mutating or unknown); False for SAFE."""
    return classify(tool)["class"] is not OpClass.SAFE


def is_irreversible(tool: str) -> bool:
    """True if the op cannot be undone -> G3 confirm-on-irreversible ALWAYS applies (all tiers)."""
    return bool(classify(tool)["irreversible"])
