"""OG-ap-7 B1, addendum to the ask: resolve the ONE conditional CHANNEL_READ_SCOPES_MEASURED.md
could not resolve, because it was a file-only read and this seat has host access.

The question, from that document's section 3: CALLER_GRAPH_SCOPES["teams_route"] does NOT list
Team.ReadBasic.All or Channel.ReadBasic.All. If MS_INGEST_IDENTITY is a SCOPED identity in the
overlay identity_scope._load_overlay() reads, token_broker line 223 cuts the request to the
overlay's union and those two scopes drop out -- so GET /hx/teams/teams and the channels route
would ask for a token without them and Graph would refuse. If the identity is UNSCOPED,
consent_scopes returns None and nothing is cut.

That matters to this order's own grade: term 3 and AC2 require a live 200 on /hx/teams/teams.
A scoped identity missing those two scopes would make AC2 fail at the deploy rather than at a
desk, so the halves should sign knowing which case holds.

PRINTS NO SECRET. It prints: whether the overlay holds the identity, the SCOPE NAMES in the
effective lists and in the overlay union, and booleans. It never prints the identity value, a
token, a bearer, or any .env value. Read-only: it imports the installed app's own modules and
calls no Graph API.
"""
import json
import os
import sys

os.chdir("/opt/opal-gateway")
sys.path.insert(0, "/opt/opal-gateway")

NEEDED = ["Team.ReadBasic.All", "Channel.ReadBasic.All", "ChannelMessage.Read.All"]
R = {}

try:
    from app import config as cfg
    c = cfg.get_config()
    R["GRAPH_SCOPES"] = sorted((c.GRAPH_SCOPES or "").split()) if isinstance(c.GRAPH_SCOPES, str) else sorted(c.GRAPH_SCOPES or [])
    R["READ_ONLY_GRAPH_SCOPES"] = sorted((c.READ_ONLY_GRAPH_SCOPES or "").split()) if isinstance(c.READ_ONLY_GRAPH_SCOPES, str) else sorted(c.READ_ONLY_GRAPH_SCOPES or [])
    # Presence only -- the identity value is never printed.
    R["MS_INGEST_IDENTITY_set"] = bool(getattr(c, "MS_INGEST_IDENTITY", None))
except Exception as e:
    R["config_error"] = type(e).__name__ + ": " + str(e)[:200]

try:
    from app import identity_scope
    ident = None
    try:
        from app import config as cfg2
        ident = cfg2.get_config().MS_INGEST_IDENTITY
    except Exception:
        pass
    ov = None
    try:
        ov = identity_scope._load_overlay()
    except Exception as e:
        R["overlay_error"] = type(e).__name__ + ": " + str(e)[:200]
    if ov is not None:
        # Only the KEY COUNT and whether our identity is among them; no identity is printed.
        try:
            keys = list(ov.keys()) if hasattr(ov, "keys") else []
            R["overlay_entries"] = len(keys)
            R["identity_is_in_overlay"] = bool(ident) and ident in keys
        except Exception as e:
            R["overlay_shape_error"] = type(e).__name__
    cs = None
    if ident:
        try:
            cs = identity_scope.consent_scopes(ident)
        except Exception as e:
            R["consent_scopes_error"] = type(e).__name__ + ": " + str(e)[:200]
    R["consent_scopes_is_None"] = cs is None
    if cs is not None:
        R["consent_scopes"] = sorted(cs)
        R["needed_missing_from_consent"] = sorted(s for s in NEEDED if s not in set(cs))
except Exception as e:
    R["identity_scope_error"] = type(e).__name__ + ": " + str(e)[:200]

# The VERDICT the halves need, derived from the above.
try:
    if R.get("consent_scopes_is_None"):
        R["VERDICT"] = ("UNSCOPED identity: consent_scopes returns None, token_broker line 223 cuts nothing, "
                        "so all three needed scopes survive in the request.")
    else:
        miss = R.get("needed_missing_from_consent") or []
        R["VERDICT"] = (("SCOPED identity and the overlay union is MISSING %s -- the list routes would be "
                         "refused by Graph." % miss) if miss else
                        "SCOPED identity but the overlay union carries all three needed scopes.")
except Exception as e:
    R["VERDICT"] = "UNDETERMINED: " + type(e).__name__

print("AP7SCOPEJSON " + json.dumps(R, sort_keys=True))
