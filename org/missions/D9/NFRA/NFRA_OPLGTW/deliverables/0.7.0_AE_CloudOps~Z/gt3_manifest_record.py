#!/usr/bin/env python
"""OG-ap-18 Phase B step 6: write the TRUNK EC2_MANIFEST record for the G1 typed-tools release.

Same shape as hv2_manifest_record.py and for the same two reasons: the deploy wrapper writes its
record on the branch it RUNS from (here rel-nfra-oplgtw-yr2, which never merges to box/sitez), and it
never recomputes file_checksums. Measured here: that branch's pre-image carried deployed_commit
a value older than trunk's, because the release worktree is cut at a base whose manifest predates
later deploys -- so MERGING that commit to trunk would REGRESS the record. Trunk's own value is the only
correct previous_deployed_commit. Measured again here: the wrapper's commit 5f4278f22d sits on the
release branch, which never merges to box/sitez.

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
SERVED = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/GT_SERVED.json"
SERVICE = "opal-gateway"
RELEASE = "047f11aa991e5c7ed188876f07a8599447cf2849"
BASE = "bf7ffb62f4ae5af8298d3c24960c63d2965542d9"
DEPLOYED_AT = "2026-10-15T01:57:04Z"          # the wrapper's own write window, not a re-read clock
DEPLOYED_BY = "0.7.0_AE_CloudOps~Z"
GW = "infra/aws/ec2/opal-gateway"

NOTE = (
    "NFRA_OPLGTW OG-ap-18 (round 37, workstream G1-TYPED, FWD-22): release commit " + RELEASE
    + " (branch rel-nfra-oplgtw-gt3, local, never merged; SEVENTEEN files vs " + BASE
    + ") deployed " + DEPLOYED_AT + " with DEPLOY_BASE_REF=" + BASE
    + " (the stale-base guard read the live ref at both checkpoints and it was equal both times); SSM"
    + " 75235426-49b6-45fe-a98b-b44f1580e652 Success. THE TEN G1 TYPED HARVEST TOOLS go live:"
    + " harvest_resolve_security, harvest_security_coverage, harvest_get_chatter, harvest_search_articles,"
    + " harvest_get_article, harvest_get_fundamentals, harvest_query_columns, harvest_get_research,"
    + " harvest_get_filing_analysis and harvest_get_peers_and_scores -- all READ tools, SAFE in destructive_ops,"
    + " legacy class in data_entitlement (NATIVE_TOOLS, deliberately NOT DATA_GRANT_TOOLS). NO NEW REACH: they read"
    + " s3://opal-data-harvest through the SAME grant and the SAME Opal-only admission OG-hv-2 already put live,"
    + " under the same 24 served prefixes; gateway-global-internal-reader-role gains nothing and harvest_read_iam.tf"
    + " is untouched. What widens is EASE -- ten typed, projected readers over what harvest_read could already fetch"
    + " one object at a time. Each calls harvest_typed.admit_typed BEFORE any S3 call, and the admitted read is capped"
    + " at 64 MB on the body itself then projected to 50 KB. THE ARTIFACT GAINS A NEW MEMBER: /opt/opal-gateway/lib/"
    + " appears for the first time, carrying exactly one file, lib/trading_calendar.py at md5"
    + " 3de6a337e268614698943b038248113b -- the DEPLOY TREE's copy per amendment A6(2), NOT trunk's newer 6596e52f,"
    + " because gt-8 stages $WORKSPACE_ROOT/lib/ and WORKSPACE_ROOT is the deploy tree, pinned at the base for every"
    + " file this cut did not take. Read-back, all against the INSTALLED code (W/GT_SERVED.json, verdict PASS):"
    + " /health {\"ok\":true}; 112 of 112 files under app/ and deploy/ md5-EQUAL to the release blobs with 0"
    + " mismatches and 0 paths on either side only; the registry 46 -> 56, +10 exactly, read from"
    + " app.tools.mcp._tool_manager.list_tools(); and all TEN tools served an enveloped answer to an Opal principal"
    + " while refusing a non-Opal one with harvest_opal_only and ZERO S3 calls on every refusal path -- measured by"
    + " replacing harvest_typed._client with a counter that raises on any attribute access, not inferred from"
    + " reading the code. The served answers now carry a NUMERIC trading_days_behind_t1 rather than an absent reason,"
    + " which closes row Z-S125 (the calendar had never reached the host). The CVO's A3 condition is satisfied:"
    + " harvest_search_articles measures 16.87 s in-region against the ALB's 60 s idle timeout, a 43 s margin, with"
    + " no 502/504. STEP 0, the CTO's read-only condition, reconciled the two registry instruments BY NAME before"
    + " the ledger opened: the repo side (tests/test_entitlement_admin.py's NATIVE|INTEGRATION|INDEX union) reads 65"
    + " at the base and 75 here, the host side reads 46 then 56, and the 19-name difference is EXACTLY"
    + " INTEGRATION_TOOLS (10) | INDEX_TOOLS (9) -- identical name for name before and after, because"
    + " mcp._tool_manager holds only native tools while integration and index tools are served through the"
    + " integration dispatch layer. ONE PAGE OUTSIDE THE TAKE-LIST MOVED, BY RULING: row Z-S133, ruled route (a) in"
    + " amendment A8, means /yearinreview now serves its LF form 3bbd5ab2d325657020357003c3ea387d (47,891 bytes, 0"
    + " CRLF) instead of the CRLF form 0d828b51 that OG-yr-1 shipped. The CONTENT is identical and the data date"
    + " 2026-10-11 is still present; the difference is 344 line terminators, caused by .gitattributes eol=lf making"
    + " the blob LF while yr-1 deployed from a tree whose working copy held the author's CRLFs. This form is the"
    + " reproducible one -- every clean checkout materialises it -- so yr-1's recorded oracle 0d828b51 is"
    + " SUPERSEDED for future reads. tests/test_og_gt8.py is NOT in this release (A6(1)): two of its three tests"
    + " assert on app/news_typed.py, which rides OG-ap-19. 48 of 48 tests pass over nine suites. Rollback: redeploy"
    + " " + BASE + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + RELEASE + "; it leaves"
    + " /opt/opal-gateway/lib/ in place, which no code in the base reads, and the PAGE's form then follows whichever"
    + " tree performs the rollback, so pick that tree deliberately. Ledger nfra-oplgtw-gateway-release-gt."
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
