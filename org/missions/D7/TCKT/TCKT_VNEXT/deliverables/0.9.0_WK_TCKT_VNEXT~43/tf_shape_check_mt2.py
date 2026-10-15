"""AC1 (TO TCKT_VNEXT.TO-R18-TR2): shape check of the meeting routing and the meeting route in main.tf.

Reads infra/aws/terraform/ticket-center/main.tf (argv[1] overrides the default path). Prints
TF-SHAPE-OK meeting_request.primary=[jeanette@opalinvest.com] route=meeting   (exit 0) only when:
  (a) ROUTING_MATRIX meeting_request has primary exactly one address, jeanette@opalinvest.com, and secondary and visibility empty;
  (b) the trade_request, service_request, other and analysis_request blocks are byte-identical to the same blocks at the
      base commit BASE_SHA (the parent of this order's first commit on the branch), read with git show;
  (c) ticket_routes holds meeting = "POST /api/scoped/tickets/{ticketId}/meeting" and every other route key is unchanged.
Otherwise prints TF-SHAPE-BAD <why> and exits 1. No AWS or network call; git is read locally only.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
REL = "infra/aws/terraform/ticket-center/main.tf"
BASE_SHA = "2e0b4b59f8"  # parent of b44da4c989, the first commit of TO-R18-TR2 on this branch
MEETING_ADDR = "jeanette@opalinvest.com"
MEETING_ROUTE = "POST /api/scoped/tickets/{ticketId}/meeting"
UNCHANGED_BLOCKS = ["trade_request", "service_request", "other", "analysis_request"]
ROUTE_RE = re.compile(r'^\s{4}([a-z_]+)\s*=\s*"([^"]*)"\s*$')


def bad(why):
    print("TF-SHAPE-BAD " + why)
    sys.exit(1)


def block_lines(lines, name, indent):
    """Lines from '<indent><name> = {' through its matching '<indent>}' (inclusive); None if absent."""
    start = None
    for i, line in enumerate(lines):
        if line == "%s%s = {" % (indent, name):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if lines[j] == indent + "}":
            return lines[start:j + 1]
    return None


def list_items(block, key):
    for line in block:
        m = re.match(r"^\s*%s\s*=\s*\[(.*)\]\s*$" % key, line)
        if m:
            raw = m.group(1).strip()
            if raw == "":
                return []
            return [x.strip().strip('"') for x in raw.split(",")]
    return None


def route_map(text):
    """ticket_routes entries as {key: value}, from the locals block that holds ticket_routes."""
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line == "  ticket_routes = {":
            start = i
            break
    if start is None:
        return None
    routes = {}
    for line in lines[start + 1:]:
        if line == "  }":
            return routes
        m = ROUTE_RE.match(line)
        if m:
            routes[m.group(1)] = m.group(2)
    return None


def base_text():
    proc = subprocess.run(["git", "show", "%s:%s" % (BASE_SHA, REL)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    if proc.returncode != 0:
        bad("cannot read base %s:%s: %s" % (BASE_SHA, REL, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, REL)
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        bad("cannot read %s: %s" % (path, exc))
    lines = text.split("\n")
    base = base_text()
    base_lines = base.split("\n")

    # (a) meeting_request block: exactly one primary address, secondary and visibility empty
    mr = block_lines(lines, "meeting_request", "      ")
    if mr is None:
        bad("meeting_request block not found in ROUTING_MATRIX")
    primary = list_items(mr, "primary")
    if primary != [MEETING_ADDR]:
        bad("meeting_request.primary is %r, expected exactly [%s]" % (primary, MEETING_ADDR))
    if list_items(mr, "secondary") != []:
        bad("meeting_request.secondary is not empty")
    if list_items(mr, "visibility") != []:
        bad("meeting_request.visibility is not empty")

    # (b) the four other routing blocks are byte-identical to the base
    for name in UNCHANGED_BLOCKS:
        now = block_lines(lines, name, "      ")
        was = block_lines(base_lines, name, "      ")
        if now is None or was is None:
            bad("routing block %s missing (now=%s base=%s)" % (name, now is not None, was is not None))
        if now != was:
            bad("routing block %s changed against base %s" % (name, BASE_SHA))

    # (c) ticket_routes: meeting added with the exact key, every other key unchanged
    now_routes = route_map(text)
    was_routes = route_map(base)
    if now_routes is None or was_routes is None:
        bad("ticket_routes block not found (now=%s base=%s)" % (now_routes is not None, was_routes is not None))
    if now_routes.get("meeting") != MEETING_ROUTE:
        bad("ticket_routes.meeting is %r, expected %r" % (now_routes.get("meeting"), MEETING_ROUTE))
    extra = sorted(set(now_routes) - set(was_routes) - {"meeting"})
    if extra:
        bad("unexpected new route keys: %s" % extra)
    missing = sorted(set(was_routes) - set(now_routes))
    if missing:
        bad("route keys removed: %s" % missing)
    changed = sorted(k for k in was_routes if now_routes[k] != was_routes[k])
    if changed:
        bad("existing route keys changed: %s" % changed)

    print("TF-SHAPE-OK meeting_request.primary=[%s] route=meeting" % MEETING_ADDR)
    sys.exit(0)


if __name__ == "__main__":
    main()
