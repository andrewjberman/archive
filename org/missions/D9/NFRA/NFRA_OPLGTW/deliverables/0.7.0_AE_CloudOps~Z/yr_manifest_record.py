#!/usr/bin/env python
"""OG-yr-1 Phase B step 6: write the TRUNK EC2_MANIFEST record for the yearinreview release.

Same shape as hv2_manifest_record.py and for the same two reasons: the deploy wrapper writes its
record on the branch it RUNS from (here rel-nfra-oplgtw-yr2, which never merges to box/sitez), and it
never recomputes file_checksums. Measured here: that branch's pre-image carried deployed_commit
daa56d81ac (2026-10-01, 0.9.0_WK_NFRA_OPLGTW~15) because the release worktree was cut at a base whose
manifest predates two later deploys -- so MERGING that commit to trunk would REGRESS the record past
bacec95ccd. Trunk's own value is the only correct previous_deployed_commit.

ONE LIMB THIS ADDS over the hv-2 version: every recomputed checksum is cross-checked against the md5
the HOST actually reported for that path in W/YR_SERVED.json, and a disagreement REFUSES the write.
`git show <release>:<path>` reads the BLOB, and the page in this very release proves blob and shipped
bytes can differ (eol=lf: blob 3bbd5ab2, shipped 0d828b51). None of the ten keys is that path, but
"none of them is affected" is a claim, so it is measured rather than asserted.

WHAT IT REFUSES TO DO: anything if the outside-span bytes would change, if any replacement does not
hit exactly once, if the result does not parse, if the key set of the entry changes, if ANY other
service's entry differs afterwards, or if a recomputed checksum disagrees with the measured host md5.

Usage: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/yr_manifest_record.py
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys

MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
SERVED = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/YR_SERVED.json"
SERVICE = "opal-gateway"
RELEASE = "bf7ffb62f4ae5af8298d3c24960c63d2965542d9"
BASE = "bacec95ccd6cafd2201f7433af24ae2748732355"
DEPLOYED_AT = "2026-10-14T23:04:51Z"          # the wrapper's own write, not a re-read clock
DEPLOYED_BY = "0.7.0_AE_CloudOps~Z"
GW = "infra/aws/ec2/opal-gateway"

NOTE = (
    "NFRA_OPLGTW OG-yr-1 (round 37, workstream YEARINREVIEW): release commit " + RELEASE
    + " (branch rel-nfra-oplgtw-yr2, local, never merged; THREE files vs " + BASE
    + " -- app/static/yearinreview/index.html, app/yearinreview_view.py and tests/test_yearinreview_view.py, the"
    + " last of which is not an artifact member) deployed " + DEPLOYED_AT + " with DEPLOY_BASE_REF=" + BASE
    + " (the stale-base guard read the live ref immediately before upload and it was equal); SSM"
    + " 768a6366-ab1a-4220-aea9-b8e7b2cfcda3 Success. TWO changes, and the second is the one that was signed:"
    + " (1) the /yearinreview page is refreshed to the CRO's final build, carrying the data date 2026-10-11 the live"
    + " page lacked; (2) the VIEWER GATE WIDENS from the owner only -- a verified identity on"
    + " YEARINREVIEW_VIEW_ALLOWED_EMAILS, fail closed on empty, roster size 1 -- to ANY verified non-guest"
    + " Opal-domain identity, the roster still admitting anyone listed on it (Andrew-direct 2026-10-14 ~22:2xZ"
    + " 'I need it viewable by all opal employees', CRO record YEARINREVIEW_OPEN_TO_ALL_OPAL_20261014 @c8f3a38f43,"
    + " issuer amendment A2). The predicate is tools._is_opal_user, NOT a domain suffix, so the Entra guest form"
    + " (#EXT#@opalinvest.com) is still refused -- a suffix check would have admitted it. Nothing else moved: no tool"
    + " (registry 46 before and 46 after, read from app.tools.mcp._tool_manager.list_tools() on the host), no route,"
    + " no IAM, no grant, no store write, no catalog edit, no .env key name (54 before, 54 after, the deploy's own"
    + " before/after lists diffed to DELTA 0). Read-back, all against the INSTALLED code: /health {\"ok\":true} on"
    + " 127.0.0.1:8080; 107 of 107 shipped files under app/ and deploy/ md5-EQUAL to the release blobs with 0"
    + " mismatches and 0 paths on either side only; the SERVED page body md5 0d828b51d433a24f7e2ef2e6ea7967ee =="
    + " the source == the page on disk (48235 bytes, 344 CRLFs) and it carries \"until\": \"2026-10-11\"; and the"
    + " three gate arms through the installed handler (W/YR_SERVED.json) -- a synthetic Opal identity that is NOT on"
    + " the live roster is served 200 with the page, the #EXT# guest form is refused 403 with 42 bytes and no page,"
    + " and an outside domain likewise 403. The admitted arm's identity being OFF the roster is what makes the 200"
    + " evidence of the widening rather than of the roster. The page md5 has THREE values and only one is the oracle:"
    + " the pin as stored and as shipped is 0d828b51 (CRLF), git stores it as 3bbd5ab2 (LF) because the path carries"
    + " .gitattributes text=set eol=lf, and the deploy tars the CHECKED-OUT file -- comparing the host against the"
    + " blob would read a correct deploy as a mismatch (issuer amendment A3). The page is self-contained inside the"
    + " release, so there is no S3 read and no new storage address. The public endpoint is NOT open: an"
    + " unauthenticated GET of https://mcp.opalinvest.dev/yearinreview is answered by the ALB authenticate-oidc"
    + " default action with a 302 to login.microsoftonline.com/<Opal tenant>/oauth2/v2.0/authorize -- this release"
    + " widens who passes the roster gate BEHIND the identity wall, never whether the wall is there. Halves, both"
    + " signed at this release_sha: CTO @64be1ff690, COO @99efc692a1 (on conditions C1-C3; C3 set the served-page"
    + " oracle to the checked-out form). Rollback: redeploy " + BASE + " through safe-ec2-deploy.sh with"
    + " DEPLOY_BASE_REF=" + RELEASE + "; it is complete, because both the old page and the owner-only gate ride this"
    + " one release, and its parity with the host was measured 107 of 107 immediately before the act. Ledger"
    + " nfra-oplgtw-gateway-release-yr. NOTE: the deploy first REFUSED from the release worktree -- deploy-to-ec2.sh"
    + " resolves two .env S3 roots through lib/opal_naming.py address(), whose registry under infra/logic/registry/"
    + " was in the commit but not in that worktree's SPARSE CONE, so address() raised FileNotFoundError before any"
    + " upload (row NFRA_OPLGTW-Z-S131). Fixed by widening the cone, never by hand-typing a root; HEAD did not move"
    + " and the A1 guard was re-read after."
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

    # The added limb: the blob md5 must equal what the HOST reported for that same path.
    host = json.load(io.open(SERVED, encoding="utf-8"))["body"]["tree_md5"]
    disagree = [(k, new_checks[k], host.get(k)) for k in new_checks if host.get(k) != new_checks[k]]
    print("  cross-check against the MEASURED host md5s: %d of %d agree" % (len(new_checks) - len(disagree), len(new_checks)))
    if disagree:
        for k, blob, h in disagree:
            print("    DISAGREE: %-40s blob %s  host %s" % (k, blob[:12], str(h)[:12]))
        raise SystemExit("REFUSED: a recomputed checksum disagrees with the running bytes -- the record would be false")

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
