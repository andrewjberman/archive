#!/usr/bin/env python
"""OG-hv-2 step 8: write the TRUNK EC2_MANIFEST record for the harvest release.

WHY THIS EXISTS AT ALL. The deploy wrapper writes its own manifest record on the branch it RUNS
from, which for a deploy-only release lineage is the release branch -- a branch that never merges to
box/sitez. Two consequences, both measured in OG-ap-14 and reproduced here:

  previous_deployed_commit   the release branch's manifest carried 2c0f84966d, three releases stale,
                             because that branch's own history is the deploy-only lineage. Trunk's
                             own current value (90967e39ba) is the only correct answer.
  file_checksums             the wrapper NEVER recomputes them. 8 of 10 were wrong in OG-ap-14. They
                             are md5 (32 hex), and here they are recomputed from the RELEASE BLOBS
                             via `git show <release>:<path>`, not from the working tree, so what the
                             record asserts is what was shipped.

WHY A SPAN EDIT AND NOT json.dump. A full re-dump is not byte-stable against this file (tested:
indent 1/2/4 x ensure_ascii x trailing newline all differ), so dumping would reformat 70 KB and put
every other service's lines inside a never-widen act's diff. So the edit is confined to the
`services["opal-gateway"]` VALUE OBJECT, found by brace matching -- and the naive span (first `{`
after the key to the first `}`) was itself the OG-ap-14 defect: it over-reached into two sibling
services and the assertion caught 3 `deployed_commit` matches where 1 was expected.

WHAT IT REFUSES TO DO: anything if the outside-span bytes would change, if any replacement does not
hit exactly once, if the result does not parse, if the key set of the entry changes, or if ANY other
service's entry differs afterwards.

Usage: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/hv2_manifest_record.py
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys

MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
SERVICE = "opal-gateway"
RELEASE = "7c558b4e2176a632d13e6301af3e06d434aa1540"
BASE = "90967e39ba4bdca17c6f84d9806c29cc67f8482e"
DEPLOYED_AT = "2026-10-14T13:58:10Z"          # the wrapper's own write, not a re-read clock
DEPLOYED_BY = "0.7.0_AE_CloudOps~Z"
GW = "infra/aws/ec2/opal-gateway"

NOTE = (
    "NFRA_OPLGTW OG-hv-2 (FWD-21, the asset manager on the gateway MCP): release commit " + RELEASE
    + " (branch rel-nfra-oplgtw-hv, local, never merged; 7 gateway files vs " + BASE
    + ", +450/-4, taken as OG-hv-1's own hunks from 4e26a29872 with add/delete counts identical per file and 0 files"
    + " outside those seven) deployed " + DEPLOYED_AT + " with DEPLOY_BASE_REF=" + BASE
    + " (the stale-base guard read the live ref at both reads, equal); SSM 7934e4ac-eb11-4733-823d-9ff9d41e7b36 Success."
    + " Carries harvest_list and harvest_read: READ-ONLY ListObjectsV2 + one 4 MB-capped GetObject over"
    + " s3://opal-data-harvest under the 24 served prefixes, Opal principals only, raw/ included (Andrew 2026-10-13"
    + " call 8). Tools 63 -> 65, 0 removed (the composite native + per-integration count that"
    + " tests/test_entitlement_admin.py::test_ogz2_ac08 asserts; the NATIVE registry read 46 on the host after the"
    + " deploy, 44 before -- a grep of @mcp.tool is a DIFFERENT denominator and reads 65 on the pre-release host)."
    + " .env key count 51 unchanged and ENABLED_INTEGRATIONS unchanged: the release touches no file under deploy/."
    + " IAM, under its own ledger nfra-oplgtw-harvest-read-grant and applied BEFORE this deploy so no request could run"
    + " the new code without the grant: ONE inline policy gateway-global-harvest-read-policy (builder name) on"
    + " gateway-global-internal-reader-role -- NOT the gateway instance role, which is not the identity that makes the"
    + " S3 call (amendment A5, from CVO row NFRA_OPLGTW-Z-S107) -- s3:GetObject on the 24 prefix ARNs read by AST from"
    + " app/harvest_read.py SERVED_PREFIXES plus s3:ListBucket conditioned on those same 24 prefixes bare and starred;"
    + " targeted safe-apply, 1 to add, 0 to change, 0 to destroy. Read-back: /health ok true on 127.0.0.1:8080;"
    + " 106 of 106 shipped files md5 == the release, with the negative control against the base differing in exactly"
    + " app/tools.py, app/data_entitlement.py and app/destructive_ops.py plus the new app/harvest_read.py;"
    + " simulate on the internal reader role packs allowed, wsj/harvest allowed, zzz-not-served implicitDeny (all three"
    + " were implicitDeny before the grant), with the same-principal portal-v2 control still allowed; and the SERVED read"
    + " through the installed code (W/HV2_SERVED.json, verdict PASS): an Opal principal's harvest_read of one real"
    + " packs/ object parsed, a non-Opal principal refused harvest_opal_only on packs/ AND wsj/harvest/, an off-list"
    + " prefix refused harvest_prefix_not_served, 0 S3 calls on any refusal path (measured by replacing the client with"
    + " a counter, not inferred from the code), and the SAME unprofiled standard-tier Opal principal refused"
    + " schwab_describe_dataset and blackdiamond_list_fees with entitlement_denied while the two harvest tools are not"
    + " denied -- the research-only boundary. Halves: CTO @e777d03b20, CVO @f93d49c306, COO @e11a221c5c, on C1-C3;"
    + " C1 re-verified at the act (ask sha256 9283dd71, grant file sha256 52e2ed23). AC3 (a real Opal asset manager's"
    + " own live read) is owed by 3.0.0_SA_CVO~Z and is NOT claimed here. Rollback: redeploy from C:/tmp/og-rel-hv's"
    + " base " + BASE + " with DEPLOY_BASE_REF=" + RELEASE + " (its parity with the host was 105 of 105 before this"
    + " act), and destroy the one policy with delete-role-policy --role-name gateway-global-internal-reader-role"
    + " --policy-name gateway-global-harvest-read-policy. Ledgers nfra-oplgtw-harvest-read-grant and"
    + " nfra-oplgtw-gateway-release-hv. NOTE: safe-apply's seat gates ran in WARN mode and printed CROSSBOX-DEPLOY"
    + " verdict=STOP on an OPEN-CALL hit naming this terraform root; under ENFORCE the apply would have stopped."
)


def md5_at(ref: str, path: str) -> str:
    out = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    if out.returncode != 0 or not out.stdout:
        raise SystemExit("REFUSED: cannot read %s at %s (a mangled git show returns clean-empty)" % (path, ref))
    return hashlib.md5(out.stdout).hexdigest()


def span(text: str, key: str) -> tuple:
    """The brace-matched VALUE object of services[key]. Naive first-}-after is the OG-ap-14 defect."""
    m = re.search(r'"%s"\s*:\s*\{' % re.escape(key), text)
    if not m:
        raise SystemExit("REFUSED: no %s entry" % key)
    i = text.index("{", m.end() - 1)
    depth, j, instr, esc = 0, i, False, False
    while j < len(text):
        c = text[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    raise SystemExit("REFUSED: unbalanced braces")


def main() -> int:
    raw = io.open(MANIFEST, encoding="utf-8").read()
    before = json.loads(raw)
    i, j = span(raw, SERVICE)
    body = raw[i:j]
    print("  span: %d bytes; parses on its own: %s" % (len(body), isinstance(json.loads(body), dict)))

    checks = before["services"][SERVICE]["file_checksums"]
    new_checks = {k: md5_at(RELEASE, "%s/%s" % (GW, k)) for k in checks}
    moved = [k for k in checks if checks[k] != new_checks[k]]
    print("  file_checksums: %d recomputed from the release blobs; %d differ from the record" % (len(new_checks), len(moved)))
    for k in moved:
        print("    moved: %-40s %s -> %s" % (k, checks[k][:12], new_checks[k][:12]))

    def one(pat: str, repl: str, what: str) -> None:
        nonlocal body
        n = len(re.findall(pat, body))
        if n != 1:
            raise SystemExit("REFUSED: %s matched %d times in the span, want exactly 1" % (what, n))
        body = re.sub(pat, repl.replace("\\", "\\\\"), body, count=1)

    one(r'"deployed_commit"\s*:\s*"[0-9a-f]{7,40}"', '"deployed_commit": "%s"' % RELEASE, "deployed_commit")
    one(r'"previous_deployed_commit"\s*:\s*"[0-9a-f]{7,40}"',
        '"previous_deployed_commit": "%s"' % BASE, "previous_deployed_commit")
    one(r'"deployed_at"\s*:\s*"[^"]*"', '"deployed_at": "%s"' % DEPLOYED_AT, "deployed_at")
    one(r'"deployed_by"\s*:\s*"[^"]*"', '"deployed_by": "%s"' % DEPLOYED_BY, "deployed_by")

    old_note = before["services"][SERVICE].get("release_note") or ""
    note = NOTE + (" ||| PREVIOUS: " + old_note if old_note else "")
    one(r'"release_note"\s*:\s*"(?:[^"\\]|\\.)*"', '"release_note": ' + json.dumps(note), "release_note")

    # The replacement carries the file's OWN indentation, READ from the block it replaces rather than
    # guessed: a correct value at the wrong indent still lands as 10 rewritten lines inside a
    # never-widen act's diff. Both the entry indent and the closing-brace indent are measured.
    ck_i, ck_j = span(body, "file_checksums")
    block = body[ck_i:ck_j]
    entry_pad = re.search(r'\n(\s*)"', block).group(1)
    close_pad = re.search(r'\n(\s*)\}$', block).group(1)
    body = (body[:ck_i] + "{\n"
            + ",\n".join('%s"%s": "%s"' % (entry_pad, k, new_checks[k]) for k in checks)
            + "\n" + close_pad + "}" + body[ck_j:])

    out = raw[:i] + body + raw[j:]
    after = json.loads(out)                                     # refuses a malformed result
    if raw[:i] != out[:i] or raw[j:] != out[len(out) - len(raw[j:]):]:
        raise SystemExit("REFUSED: bytes outside the span changed")
    for name in sorted(before["services"]):
        if name == SERVICE:
            continue
        if before["services"][name] != after["services"][name]:
            raise SystemExit("REFUSED: sibling service %s changed -- the span over-reached" % name)
    if sorted(before["services"][SERVICE]) != sorted(after["services"][SERVICE]):
        raise SystemExit("REFUSED: the entry's key set changed")
    g = after["services"][SERVICE]
    io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(out)
    print("  siblings unchanged: %d of %d services compared" % (len(before["services"]) - 1, len(before["services"])))
    print("  WROTE %s: deployed=%s previous=%s checksums=%d note=%d chars"
          % (MANIFEST, g["deployed_commit"][:10], g["previous_deployed_commit"][:10],
             len(g["file_checksums"]), len(g["release_note"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
