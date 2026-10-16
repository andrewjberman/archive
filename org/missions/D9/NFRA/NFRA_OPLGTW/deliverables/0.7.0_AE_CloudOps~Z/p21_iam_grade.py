#!/usr/bin/env python
"""OG-ap-21 Phase B: grade one IAM act by DIFFING two live captures.

The act is named on the command line as what it was ALLOWED to change:
  --expect-added   ROLE/POLICY   (repeatable)
  --expect-removed ROLE/POLICY   (repeatable)
Everything else on either role must be BYTE-IDENTICAL by canonical sha, and any
difference that is not in the expect lists is a FAIL. That is the whole point: an act
graded only on what it meant to do cannot see what else it moved.

It also grades the WIDTH of each added policy against the clauses the never-widen ask
signed -- no wildcard action, no wildcard resource, no write verb, an exact action set
and an exact resource count.
"""
from __future__ import annotations

import argparse
import io
import json
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--before", required=True)
ap.add_argument("--after", required=True)
ap.add_argument("--expect-added", action="append", default=[])
ap.add_argument("--expect-removed", action="append", default=[])
ap.add_argument("--require-present", action="append", default=[],
                help="ROLE/POLICY that must STILL be there after the act")
ap.add_argument("--width", action="append", default=[],
                help="ROLE/POLICY|action,action|nresources -- the exact signed width. The separator is a PIPE, "
                     "not a colon: an IAM action name CONTAINS a colon, so a colon-split reads dynamodb:GetItem as "
                     "two fields and the width clause silently addresses a policy name that does not exist.")
a = ap.parse_args()

b = json.load(io.open(a.before, encoding="utf-8"))
f = json.load(io.open(a.after, encoding="utf-8"))
fails, notes = [], []

WRITE_VERBS = ("Put", "Delete", "Update", "Create", "Write", "Batch", "Scan", "Tag", "Untag", "Attach", "Detach")


def flat(cap):
    out = {}
    for role, rc in cap["roles"].items():
        for name, sha in rc["canon_sha256_by_name"].items():
            out["%s/%s" % (role, name)] = sha
    return out


fb, ff = flat(b), flat(f)
added = sorted(set(ff) - set(fb))
removed = sorted(set(fb) - set(ff))
changed = sorted(k for k in set(fb) & set(ff) if fb[k] != ff[k])

notes.append("denominator: %d policies before, %d after, across %d roles"
             % (len(fb), len(ff), len(f["roles"])))
notes.append("added=%s" % (added or "none"))
notes.append("removed=%s" % (removed or "none"))
notes.append("changed-in-place=%s" % (changed or "none"))

if added != sorted(a.expect_added):
    fails.append("ADDED set is %s, the act was allowed to add %s" % (added, sorted(a.expect_added)))
if removed != sorted(a.expect_removed):
    fails.append("REMOVED set is %s, the act was allowed to remove %s" % (removed, sorted(a.expect_removed)))
if changed:
    fails.append("%d policy document(s) changed IN PLACE and no act claimed them: %s" % (len(changed), changed))

for key in a.require_present:
    if key not in ff:
        fails.append("REQUIRED-PRESENT %s is GONE after the act" % key)
    else:
        notes.append("still present: %s (sha %s, unchanged=%s)" % (key, ff[key], fb.get(key) == ff[key]))

for spec in a.width:
    key, acts, nres = spec.split("|", 2)
    role, name = key.split("/", 1)
    doc = f["roles"][role]["documents"][name]
    want_acts = sorted(acts.split(","))
    got_acts = sorted(doc["actions"])
    if got_acts != want_acts:
        fails.append("WIDTH %s actions are %s, signed %s" % (key, got_acts, want_acts))
    if len(doc["resources"]) != int(nres):
        fails.append("WIDTH %s has %d resource(s), signed %s" % (key, len(doc["resources"]), nres))
    if doc["statement_count"] != 1:
        fails.append("WIDTH %s has %d statements, signed 1" % (key, doc["statement_count"]))
    wild_a = [x for x in got_acts if "*" in x]
    wild_r = [x for x in doc["resources"] if x.rstrip("*").rstrip(":") in ("", "arn") or x == "*"]
    writes = [x for x in got_acts if any(v in x.split(":", 1)[-1] for v in WRITE_VERBS)]
    if wild_a:
        fails.append("WIDTH %s wildcard ACTION: %s" % (key, wild_a))
    if wild_r:
        fails.append("WIDTH %s wildcard RESOURCE: %s" % (key, wild_r))
    if writes:
        fails.append("WIDTH %s carries a WRITE/SCAN verb: %s" % (key, writes))
    notes.append("width ok: %s -> %s on %d resource(s), 1 statement, no wildcard, no write verb"
                 % (key, ",".join(got_acts), len(doc["resources"])))

print("=== %s -> %s" % (b["label"], f["label"]))
for n in notes:
    print("  " + n)
print("  VERDICT: " + ("PASS" if not fails else "FAIL"))
for x in fails:
    print("  FAIL: " + x)
sys.exit(0 if not fails else 1)
