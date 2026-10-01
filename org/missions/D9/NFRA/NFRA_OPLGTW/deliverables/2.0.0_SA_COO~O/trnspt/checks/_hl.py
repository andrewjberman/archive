"""OG-hl-1 AC2 read (run from the worktree root): the shipped sender-table file equals NFRA_TRNSPT's criterion.py
DEFAULT_AUTHORS, the Graph path allowlist gains exactly the listing path, and the route is registered. Prints counts and
booleans, never an address. Last line: HL <ok|FAIL>."""
import importlib
import os
import re
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "data", "transcripts", "scripts", "outlook"))
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
FILE = os.path.join(GW, "deploy", "mail_sender_table.txt")
ok = True
try:
    lines = [ln.strip() for ln in open(FILE, encoding="utf-8").read().splitlines() if ln.strip()]
except OSError as e:
    print("sender table file unreadable: %s" % e)
    lines, ok = [], False
crit = importlib.import_module("criterion").DEFAULT_AUTHORS
print("sender table file entries %d; criterion DEFAULT_AUTHORS %d; equal %s" % (len(lines), len(crit), lines == list(crit)))
ok &= bool(lines) and lines == list(crit)
src = open(os.path.join(GW, "app", "mail_route.py"), encoding="utf-8").read()
listing = bool(re.search(r"\^/me/messages\$", src))
print("Graph allowlist carries ^/me/messages$: %s" % listing)
ok &= listing
srv = open(os.path.join(GW, "app", "server.py"), encoding="utf-8").read()
reg = "mail_route.LIST_ROUTE" in srv
print("listing route registered in server.py: %s" % reg)
ok &= reg
print("HL %s" % ("ok" if ok else "FAIL"))
