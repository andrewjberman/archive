"""Registration + scope-pin read for TRNSPT-DEPS build checks. Run from the gateway dir.

usage: python _reg.py <tool> [<tool> ...]
Prints, per tool, whether it is in destructive_ops.SAFE_TOOLS and data_entitlement.NATIVE_TOOLS, and whether the
config.py GRAPH_SCOPES default equals the 17-scope list pinned at the TRNSPT-DEPS cut (C7: no new Graph scope).
Last line: REG <in-both> of <asked>; SCOPES <same|CHANGED>.
"""
import os
import re
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault("AUDIT_PATH", os.devnull)

PINNED = ("User.Read Mail.Read Mail.Send Mail.ReadWrite Calendars.ReadWrite Files.ReadWrite.All Sites.Read.All "
          "Chat.ReadWrite ChatMessage.Send Team.ReadBasic.All Channel.ReadBasic.All ChannelMessage.Read.All "
          "ChannelMessage.Send OnlineMeetings.ReadWrite OnlineMeetingTranscript.Read.All Presence.Read.All "
          "Notes.ReadWrite.All").split()

from app import data_entitlement as de  # noqa: E402
from app import destructive_ops as dop  # noqa: E402

asked = sys.argv[1:]
both = 0
for t in asked:
    s, n = t in dop.SAFE_TOOLS, t in de.NATIVE_TOOLS
    both += int(s and n)
    print("tool %s: SAFE_TOOLS=%s NATIVE_TOOLS=%s" % (t, s, n))

src = open(os.path.join("app", "config.py"), encoding="utf-8").read()
m = re.search(r'GRAPH_SCOPES: list\[str\] = os\.environ\.get\(\s*"GRAPH_SCOPES",(.*?)\)\.split\(\)', src, re.S)
default = " ".join(re.findall(r'"([^"]*)"', m.group(1))).split() if m else []
same = default == PINNED
print("GRAPH_SCOPES default scopes %d; pinned %d" % (len(default), len(PINNED)))
print("REG %d of %d; SCOPES %s" % (both, len(asked), "same" if same else "CHANGED"))
