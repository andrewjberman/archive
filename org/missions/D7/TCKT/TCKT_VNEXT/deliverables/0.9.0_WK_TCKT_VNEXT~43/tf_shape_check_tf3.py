"""AC1 (TO TCKT_VNEXT.TO-R18-TR3, AMENDMENT 2): shape check of the attachment routes, environment and S3 permission in main.tf.

Reads infra/aws/terraform/ticket-center/main.tf (argv[1] overrides the default path), ATTACH_ADDRESS.json beside this file and
the registry infra/logic/registry/scopes.json. Prints TF-ATTACH-OK routes=2 env=2 resources=3 (exit 0) only when:
  (a) ticket_routes holds attachment_upload and attachment_open with exactly the two route keys of the cell, every key of the
      base BASE_SHA (the parent of this order's first commit) is unchanged, and no other key is added;
  (b) the opal_ticket_api environment_variables carry TICKET_ATTACH_BUCKET_TEMPLATE and TICKET_ATTACH_KEY_TEMPLATE equal to the
      record's bucket_template and key_template (each present once);
  (c) the three module calls of source ../modules/opal_name carry scope = "49financial", "inflection" and "cottonwood" (one each,
      nothing else); the local ticket_attach_key_template equals the record's key_template; the local ticket_attach_arns holds
      exactly the three format() expressions over each module's bucket output (in that order), so the bucket and the firm segment
      come from the module, never typed; each module's bucket, read from scopes.json, equals the record's buckets[firm] and fits
      bucket_template; the TicketAttachmentsTradeForm statement exists once, its Action is exactly ["s3:PutObject", "s3:GetObject"],
      and its Resource is local.ticket_attach_arns;
  (d) no other S3 action token was added (base plus two), the Sid count is the base count plus one, and no line of the base
      was removed or changed (additions only, so no statement was widened).
Otherwise prints TF-ATTACH-BAD <why> and exits 1. Local git and file reads only; no AWS or network call.
"""
import difflib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
REL = "infra/aws/terraform/ticket-center/main.tf"
BASE_SHA = "5cb98dbac4"  # parent of a8a40f308b, the first commit of TO-R18-TR3 on this branch
SERVED = ["49financial", "inflection", "cottonwood"]
MODULE_NAME = {f: "ticket_attach_%s" % f for f in SERVED}
ROUTE_UPLOAD = "POST /api/scoped/tickets/attachment-upload"
ROUTE_OPEN = "GET /api/scoped/tickets/{ticketId}/attachment"
SID = "TicketAttachmentsTradeForm"
ACTIONS = ["s3:PutObject", "s3:GetObject"]
ROUTE_RE = re.compile(r'^\s{4}([a-z_]+)\s*=\s*"([^"]*)"\s*$')
ENV_RE = {
    "TICKET_ATTACH_BUCKET_TEMPLATE": re.compile(r'^    TICKET_ATTACH_BUCKET_TEMPLATE\s*=\s*"([^"]*)"\s*$'),
    "TICKET_ATTACH_KEY_TEMPLATE": re.compile(r'^    TICKET_ATTACH_KEY_TEMPLATE\s*=\s*"([^"]*)"\s*$'),
}
KEY_LOCAL_RE = re.compile(r'^\s*ticket_attach_key_template\s*=\s*"([^"]*)"\s*$')


def bad(why):
    print("TF-ATTACH-BAD " + why)
    sys.exit(1)


def base_text():
    proc = subprocess.run(["git", "show", "%s:%s" % (BASE_SHA, REL)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    if proc.returncode != 0:
        bad("cannot read base %s:%s: %s" % (BASE_SHA, REL, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8")


def route_map(text):
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


def top_block(lines, header):
    """Lines of a top-level block whose header line is exactly `header`, through its closing '}' at column 0."""
    start = None
    for i, line in enumerate(lines):
        if line == header:
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if lines[j] == "}":
            return lines[start:j + 1]
    return None


def statement_block(lines):
    """The lines of the statement whose Sid is SID, from its Sid line to the closing '}]' or '}'."""
    idx = None
    for i, line in enumerate(lines):
        if re.match(r'^\s*Sid\s*=\s*"%s"\s*$' % SID, line):
            idx = i
            break
    if idx is None:
        return None
    for j in range(idx, len(lines)):
        if lines[j].strip() in ("}]", "}"):
            return lines[idx:j + 1]
    return None


def quoted_list(block, key):
    """The quoted strings of a list assigned to key in block (single or multi line)."""
    for i, line in enumerate(block):
        m = re.match(r"^\s*%s\s*=\s*\[(.*)$" % key, line)
        if not m:
            continue
        body = m.group(1)
        if "]" in body:
            return re.findall(r'"([^"]*)"', body.split("]")[0])
        items = []
        for nxt in block[i + 1:]:
            if nxt.strip().startswith("]"):
                return items
            items.extend(re.findall(r'"([^"]*)"', nxt))
        return None
    return None


def attr_value(block, key):
    """The raw right-hand side of `key = ...` on one line of block, or None."""
    for line in block:
        m = re.match(r"^\s*%s\s*=\s*(.+?)\s*$" % key, line)
        if m:
            return m.group(1)
    return None


def locals_list(lines, name):
    """The entries (stripped, trailing comma removed) of `  name = [` ... `  ]` inside the top-level locals block."""
    start = None
    for i, line in enumerate(lines):
        if line == "  %s = [" % name:
            start = i
            break
    if start is None:
        return None
    entries = []
    for line in lines[start + 1:]:
        if line == "  ]":
            return entries
        s = line.strip()
        if s.endswith(","):
            s = s[:-1]
        if s:
            entries.append(s)
    return None


def expected_arn_expr(firm):
    m = MODULE_NAME[firm]
    return ('format("arn:aws:s3:::%%s/%%s*", module.%s.bucket, replace(local.ticket_attach_key_template, '
            '"{firm}", trimprefix(module.%s.bucket, "opal-data-")))' % (m, m))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, REL)
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        bad("cannot read %s: %s" % (path, exc))
    try:
        with open(os.path.join(HERE, "ATTACH_ADDRESS.json"), encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        bad("cannot read ATTACH_ADDRESS.json: %s" % exc)
    try:
        with open(os.path.join(ROOT, "infra", "logic", "registry", "scopes.json"), encoding="utf-8") as fh:
            scopes = json.load(fh)
    except (OSError, ValueError) as exc:
        bad("cannot read the registry scopes.json: %s" % exc)

    base = base_text()
    lines = text.split("\n")
    base_lines = base.split("\n")
    bt = rec.get("bucket_template")
    kt = rec.get("key_template")

    # (a) routes
    now_routes = route_map(text)
    was_routes = route_map(base)
    if now_routes is None or was_routes is None:
        bad("ticket_routes block not found (now=%s base=%s)" % (now_routes is not None, was_routes is not None))
    if now_routes.get("attachment_upload") != ROUTE_UPLOAD:
        bad("ticket_routes.attachment_upload is %r, expected %r" % (now_routes.get("attachment_upload"), ROUTE_UPLOAD))
    if now_routes.get("attachment_open") != ROUTE_OPEN:
        bad("ticket_routes.attachment_open is %r, expected %r" % (now_routes.get("attachment_open"), ROUTE_OPEN))
    added = sorted(set(now_routes) - set(was_routes))
    if added != ["attachment_open", "attachment_upload"]:
        bad("route keys added are %s, expected attachment_open and attachment_upload only" % added)
    if sorted(set(was_routes) - set(now_routes)):
        bad("route keys removed: %s" % sorted(set(was_routes) - set(now_routes)))
    changed = sorted(k for k in was_routes if now_routes[k] != was_routes[k])
    if changed:
        bad("existing route keys changed: %s" % changed)

    # (b) environment variables of the Lambda module
    mod = top_block(lines, 'module "opal_ticket_api" {')
    if mod is None:
        bad('module "opal_ticket_api" block not found')
    env_values = {}
    for name, rx in ENV_RE.items():
        hits = [m.group(1) for m in (rx.match(line) for line in mod) if m]
        if len(hits) != 1:
            bad("%s appears %d times in the module environment, expected once" % (name, len(hits)))
        env_values[name] = hits[0]
    if env_values["TICKET_ATTACH_BUCKET_TEMPLATE"] != bt:
        bad("TICKET_ATTACH_BUCKET_TEMPLATE %r != record bucket_template %r" % (env_values["TICKET_ATTACH_BUCKET_TEMPLATE"], bt))
    if env_values["TICKET_ATTACH_KEY_TEMPLATE"] != kt:
        bad("TICKET_ATTACH_KEY_TEMPLATE %r != record key_template %r" % (env_values["TICKET_ATTACH_KEY_TEMPLATE"], kt))

    # (c1) the three opal_name module calls, one per served firm, input scope only
    for firm in SERVED:
        blk = top_block(lines, 'module "%s" {' % MODULE_NAME[firm])
        if blk is None:
            bad("module %s not found" % MODULE_NAME[firm])
        body = [re.sub(r"\s+", " ", x.strip()) for x in blk[1:-1] if x.strip()]
        if body != ['source = "../modules/opal_name"', 'scope = "%s"' % firm]:
            bad("module %s body is %r, expected the opal_name source and scope = \"%s\" only" % (MODULE_NAME[firm], body, firm))
        if text.count('module "%s" {' % MODULE_NAME[firm]) != 1:
            bad("module %s declared more than once" % MODULE_NAME[firm])

    # (c2) the registry's bucket for each firm (the module's bucket output reads it) equals the record and fits the template
    rows = {r.get("key"): r for r in scopes.get("scopes", [])}
    for firm in SERVED:
        row = rows.get(firm)
        if row is None:
            bad("registry scopes.json has no row %s" % firm)
        if row.get("bucket") != rec["buckets"][firm]:
            bad("registry bucket for %s is %r, record says %r" % (firm, row.get("bucket"), rec["buckets"][firm]))
        if rec["buckets"][firm] != bt.replace("{firm}", firm):
            bad("record bucket for %s does not fit bucket_template %s" % (firm, bt))

    # (c3) the key template local equals the record; the ARN list is exactly the three module-derived expressions
    key_locals = [m.group(1) for m in (KEY_LOCAL_RE.match(line) for line in lines) if m]
    if key_locals != [kt]:
        bad("ticket_attach_key_template local is %r, expected exactly [%r]" % (key_locals, kt))
    arns = locals_list(lines, "ticket_attach_arns")
    if arns is None:
        bad("ticket_attach_arns local list not found")
    expected = [expected_arn_expr(f) for f in SERVED]
    if arns != expected:
        bad("ticket_attach_arns entries are %r, expected exactly the three module-derived format() expressions" % (arns,))

    # (c4) the TicketAttachmentsTradeForm statement: one, exact actions, Resource is the local
    if text.count('"%s"' % SID) != 1:
        bad("%s appears %d times, expected once" % (SID, text.count('"%s"' % SID)))
    block = statement_block(lines)
    if block is None:
        bad("statement %s not found" % SID)
    actions = quoted_list(block, "Action")
    if actions != ACTIONS:
        bad("Action is %r, expected exactly %r" % (actions, ACTIONS))
    if attr_value(block, "Resource") != "local.ticket_attach_arns":
        bad("Resource is %r, expected local.ticket_attach_arns" % (attr_value(block, "Resource"),))

    # (d) no other S3 action token, the Sid count is base plus one, and no base line was removed or changed
    s3_now = len(re.findall(r'"s3:[A-Za-z*]', text))
    s3_base = len(re.findall(r'"s3:[A-Za-z*]', base))
    if s3_now != s3_base + len(ACTIONS):
        bad("S3 action tokens: %d now, %d base; expected base plus %d" % (s3_now, s3_base, len(ACTIONS)))
    sid_now = len(re.findall(r"\bSid\s*=", text))
    sid_base = len(re.findall(r"\bSid\s*=", base))
    if sid_now != sid_base + 1:
        bad("Sid count %d now, %d base; expected base plus one" % (sid_now, sid_base))
    for op in difflib.SequenceMatcher(None, base_lines, lines, autojunk=False).get_opcodes():
        if op[0] in ("delete", "replace"):
            bad("base lines %d-%d were removed or changed (widened or edited outside the spots)" % (op[1] + 1, op[2]))

    print("TF-ATTACH-OK routes=2 env=2 resources=%d" % len(arns))
    sys.exit(0)


if __name__ == "__main__":
    main()
